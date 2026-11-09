"""Test de relier_faits.py (logique seule, sans base ; critère D4 de l'étape 5b-3).

Lancer : python -I pipelines/test_relier_faits.py   (code 1 si un cas se trompe)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from relier_faits import plan, references_lignes  # noqa: E402

LIGNES = [
    "- [10:34 UTC] [clé=Garden City 09/11] [décision=1099] Saisie de l'amical — source : déclaré par l'utilisateur",
    "- [10:40 UTC] [décision=1080] Saisie de la ligue — source : déclaré par l'utilisateur",
    "- [10:45 UTC] [décision=9999] Export Personnel — source : déclaré par l'utilisateur",
    "- [10:50 UTC] Reste à faire : Q3 pour Legrand [décision=1101]",
    "- [11:00 UTC] [clé=Personnel] Export Personnel — aucune décision citée (Legrand 1102)",
    "- [11:05 UTC] [décision=1077] Enchère placée",
]
BASE = {1099: ("proposed", "basketvibe"), 1080: ("done", "basketvibe"), 1101: ("proposed", "basketvibe"),
        1077: ("proposed", "hockeynation")}
REFS = references_lignes("fait-2026-11-09.md", LIGNES)
P = {x["id"]: x for x in plan(REFS, BASE, "basketvibe")}

CAS = [
    ("identifiant valide proposed → done", (P[1099]["a_faire"], P[1099]["ligne"]), (True, 1)),
    ("déjà done → rien écrit", (P[1080]["a_faire"], P[1080]["raison"]), (False, "déjà done")),
    ("identifiant inconnu → rien écrit", (P[9999]["a_faire"], P[9999]["raison"]), (False, "identifiant inconnu")),
    ("ligne « reste à » ignorée", 1101 in P, False),
    ("aucune correspondance floue (nombre hors balise)", 1102 in P, False),
    ("autre jeu → rien écrit", P[1077]["a_faire"], False),
    ("doublon d'identifiant → une action", len(plan(REFS + REFS, BASE, "basketvibe")), len(P)),
    ("seules les décisions proposed du jeu sont à faire", sorted(i for i, x in P.items() if x["a_faire"]), [1099]),
]

if __name__ == "__main__":
    echecs = 0
    for nom, obtenu, attendu in CAS:
        ok = obtenu == attendu
        echecs += not ok
        print(f"{'OK ' if ok else 'ÉCHEC'} {nom}" + ("" if ok else f" : {obtenu!r} au lieu de {attendu!r}"))
    print(f"{len(CAS) - echecs}/{len(CAS)}")
    sys.exit(1 if echecs else 0)
