"""Migration des learnings.md et des règles E du triage vers learn.* (refonte v2, étape 3.5).

- L-nnn (section « Enseignements ») → learn.lesson, id « <jeu>:L-nnn » (suffixe « #2 » si l'identifiant est en double
  dans le fichier). Statut : validated si « confirmé » et au moins 3 matchs à l'appui (seuil lecon_valider),
  retired si « infirmé », « contredit » ou « faux », sinon hypothesis.
- C-nnn (section « Conseils ») → learn.decision, prediction {"metric": "migre", "attendu": <critère>} : jamais évaluée
  par evaluer_decisions.py (critère en prose). Statut : done (appliqué, partiel), rejected (non appliqué),
  expired (sans objet, abandonné, caduc), sinon proposed.
- Règle E de docs/regles/triage.md → learn.error, ref = identifiant ; fermée si le garde-fou existe (« existant »).
Chaque ligne garde son origine (jeu, section, ordre, ligne brute) : export_learnings_md.py régénère les fichiers.
Import idempotent par la fonction public.learn_import (clé secrète, .env ou environnement).

Usage : python -I pipelines/migrer_learnings.py [--essai] [--json fichier]
  --essai : compte et contrôle sans écrire ; --json : écrit la charge utile dans un fichier.
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
JEUX = ["basketvibe", "hockeynation", "teamsoccer", "sixzeroleague", "derbymanager", "hardwood"]
LIGNE = re.compile(r"^\|\s*([CL]-\d+[a-z]?)\s*\|")  # L-001a : variantes de Six Zero League
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
ENTIER = re.compile(r"^\s*(\d{1,3})\b(?!\d)")
IDS_MATCH = re.compile(r"\b\d{5,}\b")
SEUIL_VALIDER = 3

# Premier motif trouvé dans le texte du conseil ou de la leçon ; défaut : tactique.
DOMAINES = [
    ("vente", r"\bvend|mise en vente|mettre en vente"),
    ("achat", r"achet|achat|ench[èé]r|offre"),
    ("academie", r"acad[ée]mie|prospect|draft|recru|scout|r[ée]v[ée]l|u18|u17|u21"),
    ("entrainement", r"entra[îi]n|gymnase|intensit|secondaire|maxing"),
    ("infrastructure", r"infrastructure|stade|places|installation|haute performance|agrandiss"),
    ("finances", r"financ|solde|sponsor|billet|salaire|budget|entretien|contrat|prolong"),
    ("personnel", r"\bcoach|staff|personnel|scout"),
    ("composition", r"compo|titulaire|align|\bxi\b|cinq|ligne[s ]|banc|formation|rotation|minutes|depth"),
]


def domaine(texte: str) -> str:
    t = texte.lower()
    return next((d for d, m in DOMAINES if re.search(m, t)), "tactique")


def cellules(ligne: str) -> list[str]:
    return [c.strip() for c in ligne.strip().strip("|").split("|")]


def statut_lecon(statut: str, matchs: int) -> str:
    s = statut.lower()
    retrait = re.search(r"infirm|contredi|\bfaux\b|retir", s)
    confirme = re.search(r"(?<!non )confirm", s)
    if retrait and not (confirme and confirme.start() < retrait.start()):  # « confirmé (lien : infirmé) » reste confirmé
        return "retired"
    if not s.lstrip("* ").startswith("à surveiller") and re.search(r"(?<!non )confirm", s) and matchs >= SEUIL_VALIDER:
        return "validated"
    return "hypothesis"


def statut_conseil(statut: str) -> str:
    s = statut.lower()
    if re.search(r"sans objet|abandonn|caduc|annul|obsol", s):
        return "expired"
    if re.search(r"non appliqu|refus|pas appliqu", s):
        return "rejected"
    if re.search(r"appliqu|partiel|fait\b|r[ée]alis|tenu|conforme|constat|vendu|achet|enregistr|atteint", s):
        return "done"
    return "proposed"


def lire_jeu(jeu: str) -> tuple[list[dict], list[dict]]:
    texte = (RACINE / f"outputs/{jeu}/learnings.md").read_text(encoding="utf-8")
    lecons, conseils, vus = [], [], {}
    section, avec_club = None, False
    for ligne in texte.splitlines():
        if ligne.startswith("## "):
            section = "L" if "Enseignement" in ligne else "C" if "Conseil" in ligne else None
        if ligne.startswith("| ID"):
            avec_club = "Club" in cellules(ligne)[:3]
        m = LIGNE.match(ligne)
        if not m or section is None or m.group(1)[0] != section:
            continue
        c = cellules(ligne)
        debut = 2 if avec_club else 1
        club = c[1] if avec_club else None
        date = (DATE.search(c[debut]) or DATE.search(ligne))
        jour = date.group(0) if date else "2026-10-01"
        ident = m.group(1)
        vus[ident] = vus.get(ident, 0) + 1
        origine = {"jeu": jeu, "section": section, "ref": ident, "club": club, "ligne": ligne}
        if section == "L":
            texte_l = " | ".join(c[debut + 1:-3]) or c[debut + 1]
            m_n = ENTIER.match(c[-3])
            matchs = int(m_n.group(1)) if m_n else len(IDS_MATCH.findall(c[-3]))
            st = statut_lecon(c[-2], matchs)
            origine.update(ordre=len(lecons), statut_brut=c[-2], matchs=c[-3])
            lecons.append({
                "id": f"{jeu}:{ident}" + (f"#{vus[ident]}" if vus[ident] > 1 else ""),
                "game": jeu, "domain": domaine(texte_l), "claim": texte_l, "status": st,
                "n_for": matchs if st == "validated" else 0, "n_against": 0,
                "created_at": f"{jour}T12:00:00+00:00", "origine": origine})
        else:
            texte_c = " | ".join(c[debut + 1:-3]) or c[debut + 1]
            origine.update(ordre=len(conseils), statut_brut=c[-2], effet=c[-1])
            conseils.append({
                "game": jeu, "domain": domaine(texte_c), "label": texte_c[:200], "hypothesis": texte_c,
                "prediction": {"metric": "migre", "attendu": c[-3]},
                "decided_at": f"{jour}T12:00:00+00:00", "eval_after": f"{jour}T12:00:01+00:00",
                "status": statut_conseil(c[-2]), "origine": origine})
    return lecons, conseils


def regles_e() -> list[dict]:
    res = []
    for ligne in (RACINE / "docs/regles/triage.md").read_text(encoding="utf-8").splitlines():
        if not ligne.startswith("| "):
            continue
        c = cellules(ligne)
        if len(c) < 5 or c[2] != "E":
            continue
        enf = c[4]
        existe = enf.startswith("existant")
        outil = c[3].lower() + " " + enf.lower()
        sorte = ("prose" if not existe else "sql" if re.search(r"gold\.|core\.|silver\.", outil)
                 else "test" if "test" in outil else "hook")
        res.append({"ref": c[0], "game": None, "description": c[1], "enforcement": sorte,
                    "guard_ref": f"{c[3]} — {enf}"[:500],
                    "closed_at": "2026-11-04T12:00:00+00:00" if existe else None})
    return res


def charge() -> dict:
    lecons, conseils = [], []
    for jeu in JEUX:
        lj, cj = lire_jeu(jeu)
        lecons += lj
        conseils += cj
    return {"lessons": lecons, "decisions": conseils, "errors": regles_e()}


def env(cle: str) -> str | None:
    f = RACINE / ".env"
    if f.exists():
        for l in f.read_text(encoding="utf-8").splitlines():
            if l.startswith(cle + "="):
                return l.split("=", 1)[1].strip().strip('"')
    return os.environ.get(cle)


def envoyer(p: dict) -> dict:
    url, cle = env("SUPABASE_URL"), env("SUPABASE_SECRET_KEY")
    if not url or not cle:
        sys.exit("❌ SUPABASE_URL ou SUPABASE_SECRET_KEY absente (.env ou environnement)")
    req = urllib.request.Request(url.rstrip("/") + "/rest/v1/rpc/learn_import", method="POST",
                                 data=json.dumps({"p": p}).encode(),
                                 headers={"apikey": cle, "Authorization": f"Bearer {cle}",
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"❌ Supabase {e.code} : {e.read().decode(errors='replace')}")


def main(argv=None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    a = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    a.add_argument("--essai", action="store_true")
    a.add_argument("--json")
    args = a.parse_args(argv)
    p = charge()
    for jeu in JEUX:
        lj = [x for x in p["lessons"] if x["game"] == jeu]
        cj = [x for x in p["decisions"] if x["game"] == jeu]
        st = {s: sum(x["status"] == s for x in lj) for s in ("hypothesis", "validated", "retired")}
        print(f"{jeu} : {len(lj)} leçons {st} ; {len(cj)} conseils")
    print(f"Règles E : {len(p['errors'])} ({sum(e['closed_at'] is None for e in p['errors'])} sans garde-fou)")
    if args.json:
        Path(args.json).write_text(json.dumps(p, ensure_ascii=False), encoding="utf-8")
    if args.essai:
        return 0
    print(f"✅ importé : {envoyer(p)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
