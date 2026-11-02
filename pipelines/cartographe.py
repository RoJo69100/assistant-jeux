"""Cartographe : ce qui manque aux cartes de décision, par jeu (étape 0b du plan de conception).

Usage : python pipelines/cartographe.py [jeu …] [--court]

Pour chaque jeu :
  1. cartes manquantes parmi les 7 types (achat, vente, composition, defaite, entrainement, academie,
     finances) dans docs/decisions/cartes/<jeu>/ ;
  2. leçons L-nnn de outputs/<jeu>/learnings.md citées dans aucune carte, avec le type de carte
     probable (mots-clés de pipelines/dossier.py) et leur statut s'il dit « réfuté », « remplacé »…
Il ne rédige rien : je rédige les checks en session, puis `dossier.py <jeu> <type> --marquer`.
Code 1 s'il reste au moins une carte manquante ou une leçon active sans check.
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dossier import MOTS  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent
JEUX = ["basketvibe", "hockeynation", "teamsoccer", "sixzeroleague", "derbymanager", "hardwood"]
TYPES = list(MOTS)
LECON = re.compile(r"^\|\s*\**(L-\d{3}[a-z]?)\**\s*\|(.*)$", re.M)
CITE = re.compile(r"\bL-\d{3}[a-z]?\b")
CLOS = re.compile(r"refute|remplace|abandonn|caduc|obsolete|reecrit")


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def type_probable(texte: str) -> str:
    n = norm(texte)
    scores = {t: sum(n.count(norm(m)) for m in mots) for t, mots in MOTS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] else "?"


def lecons(jeu: str) -> list[tuple[str, str]]:
    p = RACINE / f"outputs/{jeu}/learnings.md"
    if not p.exists():
        return []
    vus = {}
    for lid, reste in LECON.findall(p.read_text(encoding="utf-8", errors="replace")):
        vus[lid] = reste  # la dernière version d'une leçon réécrite l'emporte
    return list(vus.items())


def analyse(jeu: str) -> dict:
    d = RACINE / f"docs/decisions/cartes/{jeu}"
    cartes = {p.stem: p.read_text(encoding="utf-8", errors="replace") for p in d.glob("*.md")} if d.is_dir() else {}
    citees = set(CITE.findall("\n".join(cartes.values())))
    sans, closes = [], []
    for lid, reste in lecons(jeu):
        if lid in citees:
            continue
        cellules = [c.strip() for c in reste.split("|")]
        texte = max(cellules, key=len) if cellules else ""
        (closes if CLOS.search(norm(reste)) else sans).append((lid, type_probable(reste), texte))
    return {"manquantes": [t for t in TYPES if t not in cartes], "cartes": sorted(cartes),
            "learnings": (RACINE / f"outputs/{jeu}/learnings.md").exists(),
            "nb_lecons": len(lecons(jeu)), "sans": sans, "closes": closes}


def rendu(jeu: str, a: dict, court: bool) -> str:
    out = [f"## {jeu}",
           f"Cartes : {len(a['cartes'])}/{len(TYPES)}"
           + (f" — manquent : {', '.join(a['manquantes'])}" if a["manquantes"] else ""),
           f"Leçons : {a['nb_lecons']}" + ("" if a["learnings"] else " (learnings.md absent : à créer)")
           + f" — sans check : {len(a['sans'])}, closes non citées : {len(a['closes'])}"]
    if not court and a["sans"]:
        out += ["", "| L-nnn | Carte probable | Leçon (début) |", "|---|---|---|"]
        out += [f"| {lid} | {t} | {texte[:110].replace('|', '/')} |" for lid, t, texte in a["sans"]]
    return "\n".join(out)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("jeux", nargs="*", choices=JEUX + [[]], default=[])
    ap.add_argument("--court", action="store_true", help="résumé par jeu, sans la liste des leçons")
    args = ap.parse_args()
    reste = 0
    for jeu in args.jeux or JEUX:
        a = analyse(jeu)
        reste += len(a["manquantes"]) + len(a["sans"])
        print(rendu(jeu, a, args.court) + "\n")
    return 1 if reste else 0


if __name__ == "__main__":
    sys.exit(main())
