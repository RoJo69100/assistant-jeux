"""Compile le dossier complet d'une décision importante (règles, avis des amis, chiffres).

Usage : python pipelines/dossier.py basketvibe achat [--mots "Jean Dupont,pivot"] [--date 2026-10-31]

Types : achat, vente, composition, defaite, entrainement, academie, finances
(voir docs/decisions/variables.md). Écrit :
  outputs/<jeu>/dossier/<date>-<type>.md          index à lire en entier
  outputs/<jeu>/dossier/<date>-<type>-discord.txt toutes les lignes Discord/chat trouvées
Le dossier ne résume rien : il liste tout ce qui existe sur le sujet, pour que rien ne soit lu à moitié.
"""

import argparse
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MOTS = {
    "achat": ["transfer", "market", "auction", "bid", "buy", "free agent", "price", "transfert",
              "marché", "enchère", "achat", "prix", "agent libre"],
    "vente": ["sell", "sold", "sale", "release", "transfer", "market", "price", "vente", "vendre",
              "libér", "transfert", "prix"],
    "composition": ["tactic", "lineup", "line-up", "rotation", "minutes", "fatigue", "focus", "preset",
                    "depth", "formation", "tactique", "composition", "consigne"],
    "defaite": ["engine", "fatigue", "rebound", "turnover", "foul", "lost", "loss", "focus", "moteur",
                "défaite", "rebond", "perte", "faute"],
    "entrainement": ["training", "train ", "progress", "potential", "skill gain", "intensity",
                     "entraînement", "progression", "potentiel", "intensité"],
    "academie": ["academy", "youth", "scout", "prospect", "draft", "junior", "u18", "u21", "u17",
                 "académie", "jeune", "recrue"],
    "finances": ["finance", "money", "salary", "salaries", "sponsor", "arena", "stadium", "facility",
                 "facilities", "staff", "ticket", "infrastructure", "salaire", "budget"],
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("jeu")
    ap.add_argument("type", choices=sorted(MOTS))
    ap.add_argument("--mots", default="", help="mots précis séparés par des virgules (noms de joueurs, réglage)")
    ap.add_argument("--date", default=date.today().isoformat())
    a = ap.parse_args()

    jeu = a.jeu.lower()
    forts = [norm(m.strip()) for m in a.mots.split(",") if m.strip()]
    mots = [norm(m) for m in MOTS[a.type]]
    out_dir = ROOT / "outputs" / jeu / "dossier"
    out_dir.mkdir(parents=True, exist_ok=True)
    md, txt = out_dir / f"{a.date}-{a.type}.md", out_dir / f"{a.date}-{a.type}-discord.txt"
    rel = lambda p: p.relative_to(ROOT).as_posix()
    L = [f"# Dossier {jeu} — {a.type} — {a.date}", "",
         "À lire **en entier**, puis remplir la grille `docs/decisions/variables.md` § "
         f"`{a.type}` et le tableau Couverture. Mots : {', '.join(MOTS[a.type])}"
         + (f" ; précis : {a.mots}" if forts else ""), ""]

    # 1. Règles
    skills = sorted((ROOT / ".claude" / "skills").glob(f"{jeu}-*/SKILL.md"))
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
          "| Source | trouvés | lus | retenus | écartés (pourquoi) |", "|---|---|---|---|---|"]

    md.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{rel(md)} ; {rel(txt)} ({len(forts_rows)} lignes Discord/chat à lire, dont {precis} précises ; {len(faibles)} faibles à part) ; {len(skills)} skills ; {len(vues)} vues gold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
