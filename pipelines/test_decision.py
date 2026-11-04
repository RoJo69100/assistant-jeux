"""Test de pipelines/decision.py : prédictions mesurables acceptées, les autres refusées (sans connexion à la base).

Lancer : python -I pipelines/test_decision.py   (code 1 si un cas se trompe)
"""
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from decision import valider_date, valider_prediction  # noqa: E402

CAS = [
    ("résultat W>=2 sur 3", {"metric": "my_result", "fenetre_matchs": 3, "attendu": "W>=2"}, True),
    ("résultat L=0 sur 1", {"metric": "my_result", "fenetre_matchs": 1, "attendu": "L=0"}, True),
    ("résultat impossible", {"metric": "my_result", "fenetre_matchs": 2, "attendu": "W>=3"}, False),
    ("fenêtre absente", {"metric": "my_result", "attendu": "W>=1"}, False),
    ("fenêtre booléenne", {"metric": "my_result", "fenetre_matchs": True, "attendu": "W>=1"}, False),
    ("attendu flou", {"metric": "my_result", "fenetre_matchs": 3, "attendu": "mieux"}, False),
    ("sql lecture", {"metric": "sql", "requete": "select count(*) from gold.x", "attendu": ">= 10"}, True),
    ("sql décimal", {"metric": "sql", "requete": "with a as (select 1) select 1", "attendu": "< 0,5"}, True),
    ("sql écriture", {"metric": "sql", "requete": "delete from gold.x", "attendu": ">= 1"}, False),
    ("sql sans attendu", {"metric": "sql", "requete": "select 1"}, False),
    ("métrique inconnue", {"metric": "ressenti", "attendu": "bien"}, False),
    ("pas un objet", ["W>=2"], False),
]
J = dt.date(2026, 11, 4)
DATES = [("demain", "2026-11-05", True), ("aujourd'hui", "2026-11-04", False), ("illisible", "05/11", False)]

if __name__ == "__main__":
    echecs = 0
    for nom, pred, attendu in CAS:
        ok = (valider_prediction(pred) is None) == attendu
        echecs += not ok
        print(f"{'OK ' if ok else 'ÉCHEC'} {nom}")
    for nom, d, attendu in DATES:
        ok = (valider_date(d, J) is None) == attendu
        echecs += not ok
        print(f"{'OK ' if ok else 'ÉCHEC'} date {nom}")
    total = len(CAS) + len(DATES)
    print(f"{total - echecs}/{total}")
    sys.exit(1 if echecs else 0)
