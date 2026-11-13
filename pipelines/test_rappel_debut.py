"""Test de pipelines/rappel_debut.py (hook SessionStart) : le fichier se compile et le rappel s'affiche.
Défaut réel (phase 0, 13/11) : deux print() sur la même ligne 67, SyntaxError, le rappel de début de session ne s'affichait plus.
Lancer : python -I pipelines/test_rappel_debut.py   (code 1 si un cas se trompe)
"""
import ast
import subprocess
import sys
from pathlib import Path

DOSSIER = Path(__file__).resolve().parent
SOURCE = DOSSIER / "rappel_debut.py"


def cas():
    try:
        ast.parse(SOURCE.read_text(encoding="utf-8"))
        compile_ok = True
    except SyntaxError:
        compile_ok = False
    yield "rappel_debut.py se compile", compile_ok
    r = subprocess.run([sys.executable, str(SOURCE)], capture_output=True, text=True, encoding="utf-8", timeout=60)
    yield "rappel affiché, code 0", r.returncode == 0 and "RAPPEL DE DÉBUT DE SESSION" in r.stdout
    ligne = next((l for l in r.stdout.splitlines() if "dossier.py" in l), "")
    # inviolable 6 de CLAUDE.md : le dossier ne concerne que les gros transferts, plus la composition ni l'entraînement
    yield "dossier seulement pour les gros transferts", "gros" in ligne and "composition" not in ligne and "entraînement" not in ligne


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    jeux = list(cas())
    echecs = sum(not ok for _, ok in jeux)
    for nom, ok in jeux:
        print(("OK " if ok else "ECHEC "), nom)
    print(f"{len(jeux) - echecs}/{len(jeux)}")
    sys.exit(1 if echecs else 0)
