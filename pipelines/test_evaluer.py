"""Test de evaluer_decisions.py et garde.py (logique seule, sans base).

Scénario de fin de phase 3 : une leçon contredite deux fois passe « retired » (puis decision.py refuse de s'y appuyer).
Lancer : python -I pipelines/test_evaluer.py   (code 1 si un cas se trompe)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evaluer_decisions import SEUILS_DEFAUT as S, statut_lecon, verdict_resultats, verdict_valeur  # noqa: E402
from garde import revirement  # noqa: E402

CAS = [
    ("W>=2 sur W,L,W", verdict_resultats(["W", "L", "W"], "W>=2"), "confirmed"),
    ("W>=2 sur W,L,L", verdict_resultats(["W", "L", "L"], "W>=2"), "contradicted"),
    ("L=0 sur W,D", verdict_resultats(["W", "D"], "L=0"), "confirmed"),
    ("valeur >= 10 avec 12", verdict_valeur(12, ">= 10"), "confirmed"),
    ("valeur < 0,5 avec 0.7", verdict_valeur(0.7, "< 0,5"), "contradicted"),
    ("valeur absente", verdict_valeur(None, ">= 1"), "inconclusive"),
    ("hypothèse, 1 contradiction", statut_lecon("hypothesis", 0, 1, S)[0], "hypothesis"),
    ("hypothèse, 2 contradictions → retirée", statut_lecon("hypothesis", 0, 2, S)[0], "retired"),
    ("validée, 2 contradictions → retirée", statut_lecon("validated", 4, 2, S)[0], "retired"),
    ("3 confirmations → validée", statut_lecon("hypothesis", 3, 0, S)[0], "validated"),
    ("3 pour, 1 contre → reste hypothèse", statut_lecon("hypothesis", 3, 1, S)[0], "hypothesis"),
    ("5 confirmations → règle dure proposée", statut_lecon("validated", 5, 0, S)[1] is not None, True),
    ("retirée reste retirée", statut_lecon("retired", 9, 0, S)[0], "retired"),
    ("vente après achat accepté", revirement("vente", [("achat", "accepted")]), True),
    ("vente après achat refusé", revirement("vente", [("achat", "rejected")]), False),
    ("composition sans opposé", revirement("composition", [("composition", "done")]), False),
]

if __name__ == "__main__":
    echecs = 0
    for nom, obtenu, attendu in CAS:
        ok = obtenu == attendu
        echecs += not ok
        print(f"{'OK ' if ok else 'ÉCHEC'} {nom}" + ("" if ok else f" : {obtenu!r} au lieu de {attendu!r}"))
    print(f"{len(CAS) - echecs}/{len(CAS)}")
    sys.exit(1 if echecs else 0)
