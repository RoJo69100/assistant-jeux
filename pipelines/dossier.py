"""Compile le dossier complet d'une décision importante (règles, avis des amis, chiffres).

Usage : python pipelines/dossier.py basketvibe achat [--mots "Jean Dupont,pivot"] [--date 2026-10-31]

Types : achat, vente, composition, defaite, entrainement, academie, finances
(voir docs/decisions/variables.md). Écrit :
  outputs/<jeu>/dossier/<date>-<type>.md          index à lire en entier
  outputs/<jeu>/dossier/<date>-<type>-discord.txt toutes les lignes Discord/chat trouvées
Le dossier ne résume rien : il liste tout ce qui existe sur le sujet, pour que rien ne soit lu à moitié.

Carte (2026-10-31, « si la première fois il a trouvé l'information à un endroit, il faut qu'il le garde ») :
si docs/decisions/cartes/<jeu>/<type>.md existe, le dossier ne relit plus tout. Il donne la carte
(chaque variable, où la lire, son check) et seulement le NOUVEAU depuis le commit noté dans la carte
(git diff des skills, fiches, connaissance, learnings, Discord/chat + fichiers non commités).
  --marquer  après mise à jour de la carte : note le commit courant comme « sources lues »
  --complet  ignore la carte et recompile tout (première fois, ou sur demande)

Cœur commun (refonte v2, 1.5) : docs/decisions/cartes/_core/<type>.md, variables lues dans les vues génériques
(paramètre :game). Chaque dossier commence par ce cœur, requêtes lancées en lecture seule (sql.py) et « Dernière
valeur » remplie ; la carte du jeu suit en delta.
"""

import argparse
import re
import subprocess
import sys
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))  # sql.py, même avec python -I

MOTS = {
    "achat": ["transfer", "market", "auction", "bid", "buy", "free agent", "price", "transfert",
              "marché", "enchère", "achat", "prix", "agent libre",
              "trade", "échange", "signing", "elc", "cap space"],
    "vente": ["sell", "sold", "sale", "release", "transfer", "market", "price", "vente", "vendre",
              "libér", "transfert", "prix", "trade", "échange", "buyout", "rachat"],
    "composition": ["tactic", "lineup", "line-up", "rotation", "minutes", "fatigue", "focus", "preset",
                    "depth", "formation", "tactique", "composition", "consigne",
                    "lines", "goalie", "power play", "penalty kill", "gameplan", "gardien",
                    "remplacement", "mi-temps", "style"],
    "defaite": ["engine", "fatigue", "rebound", "turnover", "foul", "lost", "loss", "focus", "moteur",
                "défaite", "rebond", "perte", "faute", "save", "goalie", "shots", "gardien"],
    "entrainement": ["training", "train ", "progress", "potential", "skill gain", "intensity",
                     "entraînement", "progression", "potentiel", "intensité", "maxed", "plafonn", "gymnase", "entraîneur"],
    "academie": ["academy", "youth", "scout", "prospect", "draft", "junior", "u18", "u21", "u17",
                 "académie", "jeune", "recrue", "recruit", "recruiting", "commit", "scholarship",
                 "recrutement", "bourse", "hpc", "haute performance", "révél"],
    "finances": ["finance", "money", "salary", "salaries", "sponsor", "arena", "stadium", "facility",
                 "facilities", "staff", "ticket", "infrastructure", "salaire", "budget",
                 "salary cap", "buyout", "contract", "extension", "coach", "rachat", "contrat", "prolong"],
}
SEUIL = 1500
HEADER = re.compile(r"^\[(\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})[ T]\d{2}:\d{2}")


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def find_dir(base: Path, jeu: str) -> Path | None:
    if not base.is_dir():
        return None
    for d in base.iterdir():
        if d.is_dir() and re.sub(r"[^a-z0-9]", "", norm(d.name)) == jeu:
            return d
    return None


def scan(path: Path, mots: list[str], forts: list[str]):
    """Rend (n° de ligne, en-tête du message, texte, score) pour chaque ligne qui contient un mot."""
    out, header = [], ""
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return out
    for i, line in enumerate(lines, 1):
        if HEADER.match(line):
            header = line[:120]
        n = norm(line)
        score = sum(1 for m in mots if m in n) + 10 * sum(1 for m in forts if m in n)
        if score:
            out.append((i, header, line.strip(), score))
    return out


CORE = ROOT / "docs" / "decisions" / "cartes" / "_core"
REQ = re.compile(r"`(select\b[^`]*)`", re.I)


def valeur(cur, requete: str) -> str:
    """Résumé d'une requête de la carte _core : 5 lignes au plus, une cellule de tableau."""
    from sql import cellule, verifie
    try:
        q = verifie(requete)
    except SystemExit as e:
        return f"⚠ {e}"
    try:
        cur.execute(f"select * from ({q}) t limit 6")
        cols, rows = [d.name for d in cur.description], cur.fetchall()
    except Exception as e:  # requête cassée ou vue absente : on le dit, on continue
        cur.connection.rollback()
        return f"⚠ erreur : {str(e).splitlines()[0]}"
    if not rows:
        return "aucune ligne"
    out = " ; ".join(", ".join(f"{c}={'' if v is None else v}" for c, v in zip(cols, r)) for r in rows[:5])
    return cellule(out + (" ; …" if len(rows) > 5 else ""), 600)


def coeur(jeu: str, type_: str, jour: str) -> list[str]:
    """Carte _core du type, :game remplacé, « Dernière valeur » calculée maintenant (refonte v2, 1.5)."""
    carte = CORE / f"{type_}.md"
    if not carte.exists():
        return []
    lignes = carte.read_text(encoding="utf-8").replace(":game", f"'{jeu}'").splitlines()
    L = [f"## 0. Cœur commun `{carte.relative_to(ROOT).as_posix()}` (valeurs calculées le {jour})", ""]
    try:
        import psycopg
        from sql import url_ro
        conn = psycopg.connect(url_ro(), connect_timeout=15)
    except BaseException as e:  # pas de base : la carte reste utile sans valeurs
        conn = None
        L += [f"⚠ base injoignable ({str(e).splitlines()[0] if str(e) else type(e).__name__}) : valeurs à lire à la main.", ""]
    suite = lignes[lignes.index("## Variables") + 1:] if "## Variables" in lignes else []
    fin = next((i for i, l in enumerate(suite) if l.startswith("## ")), len(suite))
    try:
        for l in suite[:fin]:
            if l.startswith("| # "):
                L.append(l + " Dernière valeur |")
            elif l.startswith("|---"):
                L.append(l + "---|")
            elif l.startswith("| C"):
                m = REQ.search(l)
                v = valeur(conn.cursor(), m.group(1)) if (m and conn) else ""
                L.append(f"{l} {v} |")
    finally:
        if conn:
            conn.close()
    L += [""] + [l.replace("## ", "### ", 1) if l.startswith("## ") else l for l in suite[fin:]]  # couverture : ce que le delta doit fournir
    return L + ["", "La carte du jeu ci-dessous est le **delta** : ses variables s'ajoutent au cœur ; une variable qui répète une variable C renvoie à son numéro.", ""]


LUES = re.compile(r"^Sources lues : .*$", re.M)
COMMIT = re.compile(r"^Sources lues : commit ([0-9a-f]{7,40})", re.M)


def git(*args: str) -> str:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout if r.returncode == 0 else ""


def sources(jeu: str) -> list[str]:
    """Chemins suivis pour le delta : règles, fiches, config, avis des amis, learnings."""
    ps = [f".claude/skills/{d.name}" for d in sorted((ROOT / ".claude" / "skills").glob(f"{jeu}-*"))]
    ps += [f"docs/fiches/{jeu}", f"docs/attentes/jeux/{jeu}.yaml", f"outputs/{jeu}/veille", f"outputs/{jeu}/learnings.md"]
    for base in (ROOT / "data" / "discord", ROOT / "data" / "chat"):
        d = find_dir(base, jeu)
        if d:
            ps.append(d.relative_to(ROOT).as_posix())
    return [p for p in ps if (ROOT / p).exists()]


def delta(jeu: str, depuis: str) -> dict[str, list[str]]:
    """Lignes ajoutées depuis le commit `depuis` (commits suivants, modifications et fichiers non commités)."""
    ps, out, f = sources(jeu), {}, None
    for line in git("-c", "core.quotepath=off", "diff", "--unified=0", "--no-color", depuis, "--", *ps).splitlines():
        if line.startswith("+++ "):
            f = line[6:] if line.startswith("+++ b/") else None
        elif line.startswith("+") and f:
            out.setdefault(f, []).append(line[1:])
    for f in git("-c", "core.quotepath=off", "ls-files", "--others", "--exclude-standard", "--", *ps).splitlines():
        out[f] = (ROOT / f).read_text(encoding="utf-8", errors="replace").splitlines()
    return out


def marquer(carte: Path, jeu: str, jour: str) -> int:
    if not carte.exists():
        print(f"pas de carte {carte.relative_to(ROOT).as_posix()} : écris-la d'abord (modèle docs/decisions/cartes/MODELE.md)")
        return 1
    ligne = f"Sources lues : commit {git('rev-parse', '--short', 'HEAD').strip()} ({jour})"
    t = carte.read_text(encoding="utf-8")
    t = LUES.sub(ligne, t) if LUES.search(t) else t.replace("\n", f"\n\n{ligne}\n", 1)
    carte.write_text(t, encoding="utf-8")
    sale = git("status", "--porcelain", "--", *sources(jeu)).strip()
    print(ligne + (f"\nattention, non commité (sera relu au prochain passage) :\n{sale}" if sale else ""))
    return 0


DOMAINE_LEARN = {"defaite": "tactique"}  # type de dossier → domaine de learn.* (les autres ont le même nom)


def garde_bloc(jeu: str, type_: str, mots: str) -> list[str]:
    """Sortie de garde.py (leçons à suivre, retirées, erreurs, revirement sur le premier mot précis) — étape 3.5."""
    sujet = next((m.strip() for m in mots.split(",") if m.strip()), None)
    try:
        from export_learnings_md import lire_base
        from garde import rapport
        lignes, code = rapport(jeu, DOMAINE_LEARN.get(type_, type_), sujet, lire_base(jeu))
    except (Exception, SystemExit) as e:  # base injoignable : le dire, sans bloquer le dossier
        return ["## Garde-fou (learn)", f"- ❌ garde.py non exécuté : {e}", ""]
    return (["## Garde-fou (learn) — à respecter dans le rendu", *[f"- {l.strip()}" for l in lignes]]
            + (["- **Revirement : le rendu le déclare comme correction, avec le plan de sortie (R-8).**"] if code == 2 else [])
            + [f"- Le conseil rendu s'enregistre : `python -I pipelines/decision.py new {jeu} <domaine> …` (prédiction mesurable).", ""])


def dossier_carte(a, jeu, carte, depuis, mots, forts, md, txt, rel) -> int:
    """Mode carte : la carte dit où lire chaque variable ; on ne lit que le nouveau."""
    nouveau = delta(jeu, depuis)
    L = [f"# Dossier {jeu} — {a.type} — {a.date} — carte + nouveau", "",
         f"1. **Carte** `{rel(carte)}` : lis-la en entier. Chaque variable y a son endroit et son check : "
         "lance ses requêtes (groupées, colonnes choisies, `LIMIT`) et remplis les valeurs du jour. Ne relis pas les sources déjà notées.",
         f"2. **Nouveau depuis le commit {depuis}** (ci-dessous) : à lire en entier. Une ligne qui change une règle, un avis "
         "ou un seuil → modifie le check de la carte (cite la source et la date) ; une variable nouvelle → ajoute une ligne.",
         "3. **Joueur ou réglage absent de la carte** : recherche ciblée sur son nom dans tout l'historique (`--mots`, fichier `-cible.txt`).",
         f"4. **Fin** : carte à jour (valeurs, checks, sources), commit, puis `python pipelines/dossier.py {jeu} {a.type} --marquer`.", ""]
    L += coeur(jeu, a.type, a.date)
    L += garde_bloc(jeu, a.type, a.mots)
    regles, amis = [], []
    for f, lines in sorted(nouveau.items()):
        regle = f.startswith((".claude/", "docs/"))  # une règle modifiée compte en entier, même hors sujet
        hits = [l.strip() for l in lines if l.strip() and (regle or any(m in norm(l) for m in mots + forts))]
        (regles if regle or not f.startswith("data/") else amis).append((f, len(lines), hits))
    L.append(f"## Nouveau — règles, fiches, connaissance, learnings")
    for f, n, hits in regles:
        L += [f"### `{f}` — {n} lignes ajoutées, {len(hits)} sur le sujet", *hits, ""]
    if not regles:
        L += ["- rien de nouveau.", ""]
    with txt.open("w", encoding="utf-8") as fh:
        fh.write(f"# Nouveau Discord/chat depuis {depuis}, lignes sur le sujet.\n")
        for f, n, hits in amis:
            fh.writelines(f"{f} | {h}\n" for h in hits)
    nb = sum(len(h) for _, _, h in amis)
    L += ["## Nouveau — Discord / chat",
          f"- {nb} lignes sur le sujet ({sum(n for _, n, _ in amis)} ajoutées) → `{rel(txt)}`, **à lire en entier**." if amis else "- rien de nouveau.", ""]
    if forts:
        cible, rows = txt.with_name(txt.stem.replace("-discord", "") + "-cible.txt"), []
        for base in (find_dir(ROOT / "data" / "discord", jeu), find_dir(ROOT / "data" / "chat", jeu)):
            if base:
                for f in sorted(base.rglob("*.txt")):
                    rows += [(rel(f), i, t) for i, _, t, _ in scan(f, [], forts)]
        uniq = list(dict.fromkeys((f, i, t) for f, i, t in rows))
        with cible.open("w", encoding="utf-8") as fh:
            fh.writelines(f"{f}:{i} | {t}\n" for f, i, t in uniq)
        L += [f"## Recherche ciblée ({a.mots}) dans tout l'historique", f"- {len(uniq)} lignes → `{rel(cible)}`, à lire en entier.", ""]
    L.append("## Du jour")
    L += [f"- brief : `{rel(f)}`" for f in sorted((ROOT / "outputs" / jeu / "briefs").glob(f"{a.date}-*.md"))]
    fait = ROOT / "outputs" / jeu / f"fait-{a.date}.md"
    L += [f"- registre : `{rel(fait)}`" if fait.exists() else "- registre `fait-` : absent",
          f"- exports : `bronze.raw_pages` where game = '{jeu}' and captured_at >= '{a.date}'", "",
          "## Couverture (à remplir)", "| Source | trouvés | lus | retenus | écartés (pourquoi) |", "|---|---|---|---|---|",
          "| carte (variables) | | | | |", "| nouveau règles | | | | |", "| nouveau Discord/chat | | | | |"]
    md.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{rel(md)} ; carte {rel(carte)} ; nouveau depuis {depuis} : {len(regles)} fichiers de règles/connaissance, {nb} lignes Discord/chat")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("jeu")
    ap.add_argument("type", choices=sorted(MOTS))
    ap.add_argument("--mots", default="", help="mots précis séparés par des virgules (noms de joueurs, réglage)")
    ap.add_argument("--date", default=date.today().isoformat())
    ap.add_argument("--marquer", action="store_true", help="note le commit courant comme sources lues dans la carte")
    ap.add_argument("--complet", action="store_true", help="ignore la carte et recompile tout")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    jeu = a.jeu.lower()
    forts = [norm(m.strip()) for m in a.mots.split(",") if m.strip()]
    mots = [norm(m) for m in MOTS[a.type]]
    carte = ROOT / "docs" / "decisions" / "cartes" / jeu / f"{a.type}.md"
    if a.marquer:
        return marquer(carte, jeu, a.date)
    out_dir = ROOT / "outputs" / jeu / "dossier"
    out_dir.mkdir(parents=True, exist_ok=True)
    md, txt = out_dir / f"{a.date}-{a.type}.md", out_dir / f"{a.date}-{a.type}-discord.txt"
    rel = lambda p: p.relative_to(ROOT).as_posix()
    m = COMMIT.search(carte.read_text(encoding="utf-8")) if carte.exists() and not a.complet else None
    if m and git("cat-file", "-t", m.group(1)).strip() == "commit":
        return dossier_carte(a, jeu, carte, m.group(1), mots, forts, md, txt, rel)
    if m:  # commit disparu (historique réécrit en 0.2) : dossier complet, mais on le dit
        print(f"⚠ commit {m.group(1)} de la carte {rel(carte)} introuvable : dossier complet ; "
              f"corrige la ligne « Sources lues » (--marquer après relecture)")
    L = [f"# Dossier {jeu} — {a.type} — {a.date}", "",
         "À lire **en entier**, puis remplir la grille `docs/decisions/variables.md` § "
         f"`{a.type}` et le tableau Couverture. Mots : {', '.join(MOTS[a.type])}"
         + (f" ; précis : {a.mots}" if forts else ""), ""]
    L += coeur(jeu, a.type, a.date)
    L += garde_bloc(jeu, a.type, a.mots)

    # 1. Règles
    skills = sorted((ROOT / ".claude" / "skills").glob(f"{jeu}-*/SKILL.md")
                    ) + sorted((ROOT / ".claude" / "skills").glob(f"{jeu}-*/references/*.md"))
    L += ["## 1. Règles (skills à lire en entier)"] + [f"- `{rel(s)}`" for s in skills]
    resume = ROOT / "docs" / "fiches" / jeu / "resume.md"
    fiches = sorted((ROOT / "docs" / "fiches" / jeu).glob("*.md"))
    L += [f"- fiches : " + ", ".join(f"`{rel(f)}`" for f in fiches)] if fiches else ["- **aucune fiche**"]
    L.append("")

    # 2. Avis des amis : connaissance (lignes complètes, par section)
    L.append("## 2. Avis des amis — connaissance (toutes les lignes sur le sujet)")
    for f in sorted((ROOT / "outputs" / jeu / "veille").glob("connaissance*.md")):
        section, hits = "", []
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("#"):
                section = line
            elif line.startswith("|") and not line.startswith("|---"):
                n = norm(line)
                if any(m in n for m in mots + forts):
                    if section:
                        hits.append(section)
                        section = ""
                    hits.append(line)
        L += [f"### `{rel(f)}` — {sum(1 for h in hits if h.startswith('|'))} lignes", *hits, ""]

    # 3. Avis des amis : Discord et chat bruts (tout dans le .txt)
    rows = []
    for base in (find_dir(ROOT / "data" / "discord", jeu), find_dir(ROOT / "data" / "chat", jeu)):
        if base:
            for f in sorted(base.rglob("*.txt")):
                rows += [(rel(f), *r) for r in scan(f, mots, forts)]
    seen, uniq = set(), []
    for r in sorted(rows, key=lambda r: -r[4]):  # les exports qui se recouvrent donnent des doublons
        if (r[2], r[3]) not in seen:
            seen.add((r[2], r[3]))
            uniq.append(r)
    # Au-delà de SEUIL lignes, les lignes à un seul mot générique vont dans un 2e fichier, listé à part.
    forts_rows = [r for r in uniq if r[4] >= 2 or len(uniq) <= SEUIL]
    faibles = [r for r in uniq if r not in forts_rows]
    faible_txt = txt.with_name(txt.stem + "-faible.txt")
    for path, part in ((txt, forts_rows), (faible_txt, faibles)):
        with path.open("w", encoding="utf-8") as fh:
            fh.write(f"# {len(part)} lignes, triées par pertinence (mots précis d'abord).\n")
            for f, i, h, t, s in part:
                fh.write(f"{f}:{i} | {t}\n" if t.startswith(h[:40]) else f"{f}:{i} | {h} | {t}\n")
    precis = sum(1 for r in uniq if r[4] >= 10)
    L += ["## 3. Avis des amis — Discord / chat bruts",
          f"- {len(forts_rows)} lignes (dont {precis} avec un mot précis) → `{rel(txt)}`, **à lire en entier**."
          if uniq else "- aucun export Discord/chat pour ce jeu : chercher dans le skill `-communaute` et en base (`bronze.discord_messages`, chat).",
          f"- {len(faibles)} lignes à un seul mot générique → `{rel(faible_txt)}` : relancer avec `--mots` précis pour les remonter."
          if faibles else "- aucune ligne écartée.",
          "- Avant « absent » : `bronze.discord_messages` et le chat en base (`silver.sz_api` pour Six Zero League).", ""]

    # 4. Chiffres
    vues = sorted(set(re.findall(r"gold\.\w+", resume.read_text(encoding="utf-8")))) if resume.exists() else []
    L += ["## 4. Chiffres (à interroger, toute la saison)",
          "- vues gold citées par le résumé : " + (", ".join(f"`{v}`" for v in vues) or "**aucune**"),
          f"- exports du jour : `bronze.raw_pages` where game = '{jeu}' and captured_at >= '{a.date}'"]
    for f in sorted((ROOT / "outputs" / jeu / "briefs").glob(f"{a.date}-*.md")):
        L.append(f"- brief du jour : `{rel(f)}`")
    learn = ROOT / "outputs" / jeu / "learnings.md"
    if learn.exists():
        hits = [l for l in learn.read_text(encoding="utf-8", errors="replace").splitlines()
                if any(m in norm(l) for m in mots + forts)]
        L += [f"- `{rel(learn)}` : {len(hits)} lignes sur le sujet", *[f"  {h}" for h in hits]]
    fait = ROOT / "outputs" / jeu / f"fait-{a.date}.md"
    L.append(f"- registre : `{rel(fait)}`" if fait.exists() else f"- registre `fait-{a.date}.md` : absent (rien déclaré aujourd'hui)")
    L += ["", "## 5. Couverture (à remplir par l'agent)",
          "| Source | trouvés | lus | retenus | écartés (pourquoi) |", "|---|---|---|---|---|",
          "", "## 6. Carte (pour ne plus jamais tout relire)",
          f"- `{rel(carte)}` " + ("existe mais son commit est illisible : réécris la ligne « Sources lues »." if carte.exists()
                                  else "n'existe pas : écris-la (modèle `docs/decisions/cartes/MODELE.md`)")
          + f" — chaque variable, l'endroit exact où tu l'as trouvée (requête, fichier § section) et son check. "
          f"Commit, puis `python pipelines/dossier.py {jeu} {a.type} --marquer`. Les prochaines fois, seul le nouveau sera lu."]

    md.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{rel(md)} ; {rel(txt)} ({len(forts_rows)} lignes Discord/chat à lire, dont {precis} précises ; {len(faibles)} faibles à part) ; {len(skills)} skills ; {len(vues)} vues gold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
