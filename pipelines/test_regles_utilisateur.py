"""docs/regles-utilisateur.md : chaque règle est datée et chaque clé citée existe dans docs/attentes/jeux/basketvibe.yaml.
Lancer : python -I pipelines/test_regles_utilisateur.py   (code 1 si un cas se trompe)"""
import re
import sys
from pathlib import Path

import yaml

RACINE = Path(__file__).resolve().parent.parent
REGLES = RACINE / "docs" / "regles-utilisateur.md"
YAML = RACINE / "docs" / "attentes" / "jeux" / "basketvibe.yaml"


def existe(y, cle: str) -> bool:
    for k in cle.split("."):
        if not isinstance(y, dict) or k not in y:
            return False
        y = y[k]
    return True


def cas():
    y = yaml.safe_load(YAML.read_text(encoding="utf-8"))
    lignes = [l for l in REGLES.read_text(encoding="utf-8").splitlines() if re.match(r"^\| \d{4}-\d{2}-\d{2} \|", l)]
    yield "au moins 6 règles datées", len(lignes) >= 6
    for l in lignes:
        cellules = [c.strip() for c in l.strip("|").split("|")]
        yield f"{cellules[0]} {cellules[1]} : règle et clé renseignées", len(cellules) == 4 and cellules[2] and cellules[3]
        for cle in re.findall(r"`([^`]+)`", cellules[3]):
            yield f"{cellules[1]} : clé `{cle}` présente dans basketvibe.yaml", existe(y, cle)
    yield "existe() refuse une clé absente", not existe(y, "offres.cle_absente")
    claude = (RACINE / "CLAUDE.md").read_text(encoding="utf-8")
    yield "CLAUDE.md impose la lecture avant toute modification du plan", \
        "Avant toute modification du plan, lire docs/regles-utilisateur.md ; toute règle nouvelle de l'utilisateur y est ajoutée dans la même session." in claude


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    jeux = list(cas())
    echecs = 0
    for n, ok in jeux:
        echecs += not ok
        print("OK " if ok else "ECHEC ", n)
    print(f"{len(jeux) - echecs}/{len(jeux)}")
    sys.exit(1 if echecs else 0)
