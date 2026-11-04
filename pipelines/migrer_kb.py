"""Migre les fichiers de veille (outputs/<jeu>/veille/connaissance*.md, v-*.md) vers kb.claim (refonte v2, étape 4.1).

Une affirmation = une ligne d'un tableau dont l'en-tête a une colonne « Fait », ou une puce « - » d'un fichier
sans tableau de faits (Derby Manager). Domaine = thème du titre de section (## ou ###) ; les sections de méthode,
propositions, écarts, décomptes et questions ouvertes sont ignorées.
Source : auteur officiel (développeur, administrateur) → devlog ; « News », « #updates », patch → patchnote ;
vues SQL → observation ; wiki, guide, manuel → manuel ; chat du jeu → chat ; forum / QA → forum ; sinon discord.
Les autres auteurs d'une même ligne (séparés par « ; ») comptent comme soutiens (kb.support).
Import idempotent (import_key = md5 jeu|fichier|texte), puis kb.recompute_confidence côté base.

Usage : python -I pipelines/migrer_kb.py [<jeu> …] [--dry-run]   (REST public.kb_import, SUPABASE_SECRET_KEY)
"""

import argparse
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from migrer_learnings import JEUX, RACINE, cellules, env  # noqa: E402
from police import norm  # noqa: E402

THEMES = [  # (domaine, motif sur le titre normalisé) : le premier qui correspond l'emporte
    ("bugs", r"\bbugs?\b|panne|incident|piege"),
    ("versions", r"version|mise a jour|mises a jour|devlog|calendrier du developpeur|patch|changements"),
    ("glossaire", r"glossaire|interface"),
    ("academie", r"academie|draft|scout|school|jeunes|recrut|u18|u17|relev"),
    ("entrainement", r"entrainement|potentiel|progression"),
    ("forme", r"forme|condition|fatigue|sharpness|blessure|discipline|satisfaction|team spirit|experience"),
    ("transferts", r"transfert|marche|echange|trade"),
    ("finances", r"financ|salaire|contrat|plafond|sponsor|argent|economie|premium|rachat|agent"),
    ("infrastructures", r"infrastructure|stade|billet|installation|haute performance|hpc"),
    ("personnel", r"coach|staff|personnel"),
    ("calendrier", r"calendrier|competition|coupe|division|saison|classement|rythme|bots?\b|evenement|events"),
    ("roles", r"^roles?$"),  # définitions des rôles (Derby Manager), distinctes des consignes tactiques
    ("tactique", r"tactique|formation|composition|role|lignes|plan de jeu|depth|direction"),
    ("match", r"match|moteur"),
    ("joueurs", r"joueur|talent|competence|attribut|poste|notes? d'equipe|formules"),
]
IGNORE = re.compile(r"propos|ecarts?\b|decompte|comment lire|perimetre|non lu|questions|limites|methode"
                    r"|a surveiller|autres clubs|lecture integrale du 2026-10-29|^index|reste inconnu")
OFFICIELS = {
    "basketvibe": ("dev", "developpeur", "basketvibe", "vachacz"),
    "derbymanager": ("dev", "derbymanager", "developpeur"),
    "hockeynation": ("hnadmin", "d0ghouse", "d0", "developpeur"),
    "sixzeroleague": ("gazelle", "gazellemag", "urban fox", "dev chat", "developpeur"),
    "teamsoccer": ("admin-dev", "admin-pipo68", "developpeur"),
    "hardwood": ("developpeur", "admin"),
}
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def fichiers(jeu: str) -> list[Path]:
    d = RACINE / f"outputs/{jeu}/veille"
    fs = sorted(d.glob("connaissance*.md")) + sorted(d.glob("v-*.md"))
    return [f for f in fs if f.exists()]


def theme(titre: str, defaut: str = "divers") -> str:
    t = norm(titre)
    return next((d for d, m in THEMES if re.search(m, t)), defaut)


def statut(s: str, officiel: bool) -> str:
    s = norm(s)
    if re.search(r"obsolet|caduc|perime|n'existe plus", s):
        return "obsolete"
    if re.search(r"^\W*(contredit|infirm|remplace|faux)", s):
        return "contredit"
    if re.search(r"^\W*confirm", s):
        return "confirme"
    if re.search(r"^\W*compl", s):
        return "complete"
    if re.search(r"en doute|incertain|a verifier|a confirmer|non tranch", s):
        return "en_doute"
    return "confirme" if officiel else "en_doute"


def auteurs(cell: str) -> list[str]:
    res = []
    for a in re.split(r"[;,/]| et ", cell):
        a = re.sub(r"[`*()\[\]]", "", DATE.sub("", a)).strip()
        if a and len(a) <= 40 and a not in res:
            res.append(a)
    return res


def genre(jeu: str, source: str, auteur: str, statut_lu: str) -> str:
    s, a = norm(source), norm(auteur)
    if re.search(r"\bnews\b|#updates|patch|devlog|\[n \d", s):
        return "patchnote"
    if any(o == a or o in norm(statut_lu) for o in OFFICIELS.get(jeu, ())) or "dev" == a:
        return "devlog"
    if re.search(r"\bsql\b|gold\.|silver\.|nos vues|export du jour|infobulle", s):
        return "observation"
    if re.search(r"\bw:|wiki|guide|manuel|\bfaq\b", s):
        return "manuel"
    if re.search(r"\bc:|chat", s):
        return "chat"
    if re.search(r"\bqa\b|fil:|forum", s):
        return "forum"
    return "discord"


def affirmation(jeu, f, n, section, texte, source, date_, auteur_cell, statut_lu, defaut="divers") -> dict | None:
    texte = texte.replace("**", "").strip()
    if len(texte) < 12 or texte.startswith(("---", ":--")):
        return None
    auts = auteurs(auteur_cell)
    if not auts:  # « #general, hnadmin » / « #discussion 2024-06-19 dev »
        m = (re.search(r"\bdev\s+([A-Za-z0-9_.-]+)", source, re.I)
             or re.search(r"\d{4}-\d{2}-\d{2}\s+([A-Za-z][A-Za-z0-9_.-]*)", source + " " + texte)
             or re.search(r",\s*([A-Za-z][A-Za-z0-9_.-]+)\s*$", source))
        auts = [m.group(1)] if m else []
    a0 = auts[0] if auts else None
    officiel = any(norm(x) in OFFICIELS.get(jeu, ()) for x in auts) or "developpeur" in norm(statut_lu)
    d = DATE.search(date_) or DATE.search(source) or DATE.search(texte)
    rel = f.relative_to(RACINE).as_posix()
    return {"game": jeu, "domain": theme(section, defaut), "text": texte[:4000],
            "source_kind": genre(jeu, source, a0 or "", statut_lu),
            "source_ref": (source.strip() or f"{rel}:L{n}")[:300], "author": a0,
            "said_at": d.group(0) if d else None, "status": statut(statut_lu, officiel),
            "import_key": hashlib.md5(f"{jeu}|{rel}|{texte}".encode()).hexdigest(),
            "origine": {"fichier": rel, "ligne": n, "section": section, "statut_lu": statut_lu[:200]},
            "_soutiens": auts[1:]}


def lire(jeu: str) -> list[dict]:
    res = []
    for f in fichiers(jeu):
        lignes = f.read_text(encoding="utf-8").splitlines()
        a_tableau = any(l.startswith("|") and "fait" in [norm(c) for c in cellules(l)] for l in lignes)
        section, ignore, cols = f.stem.replace("v-", ""), False, None
        defaut = theme(section.replace("-", " "))  # Hardwood : un fichier par thème
        for n, l in enumerate(lignes, 1):
            if l.startswith("#"):
                section = l.lstrip("#").strip()
                ignore = bool(IGNORE.search(norm(section))) or l.startswith("# ")
                cols = None
                continue
            if ignore:
                continue
            if l.startswith("|"):
                c = cellules(l)
                nc = [norm(x) for x in c]
                if "fait" in nc:
                    cols = nc
                    continue
                if cols is None or set(l) <= set("|-: "):
                    continue
                g = lambda k: c[cols.index(k)] if k in cols and cols.index(k) < len(c) else ""  # noqa: E731
                x = affirmation(jeu, f, n, section, g("fait"), g("source"), g("date"), g("auteur"), g("statut"), defaut)
            elif l.startswith("- ") and not a_tableau:
                parts = [p.strip() for p in l[2:].split(" — ")]
                st = parts[-1] if len(parts) >= 3 else ""
                x = affirmation(jeu, f, n, section, parts[0], " — ".join(parts[1:-1] if st else parts[1:]),
                                "", "", st, defaut)
            else:
                cols = None if not l.strip() else cols
                continue
            if x:
                res.append(x)
    vus, uniq = set(), []
    for x in res:
        if x["import_key"] not in vus:
            vus.add(x["import_key"])
            uniq.append(x)
    return uniq


def charge(jeu: str) -> dict:
    claims = lire(jeu)
    support = [{"import_key": x["import_key"], "author": a, "source_ref": x["source_ref"], "said_at": x["said_at"]}
               for x in claims for a in x.pop("_soutiens")]
    return {"game": jeu, "claims": claims, "support": support}


def envoyer(p: dict) -> dict:
    url, cle = env("SUPABASE_URL"), env("SUPABASE_SECRET_KEY")
    if not url or not cle:
        sys.exit("❌ SUPABASE_URL ou SUPABASE_SECRET_KEY absente (.env ou environnement)")
    req = urllib.request.Request(url.rstrip("/") + "/rest/v1/rpc/kb_import", method="POST",
                                 data=json.dumps({"p": p}).encode(),
                                 headers={"apikey": cle, "Authorization": f"Bearer {cle}",
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"❌ Supabase {e.code} : {e.read().decode(errors='replace')[:500]}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("jeux", nargs="*", default=JEUX)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    for jeu in a.jeux:
        p = charge(jeu)
        dom = Counter(x["domain"] for x in p["claims"])
        src = Counter(x["source_kind"] for x in p["claims"])
        print(f"{jeu} : {len(p['claims'])} affirmations, {len(p['support'])} soutiens — "
              f"{dict(dom.most_common())} — {dict(src.most_common())}")
        if not a.dry_run and p["claims"]:
            print("   →", envoyer(p))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
