"""Test de evaluer_decisions.py et garde.py (logique seule, sans base).

Scénario de fin de phase 3 : une leçon contredite deux fois passe « retired » (puis decision.py refuse de s'y appuyer).
Lancer : python -I pipelines/test_evaluer.py   (code 1 si un cas se trompe)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evaluer_decisions import (SEUILS_DEFAUT as S, charge_ecriture, dans_fenetre, fenetre_resultats,  # noqa: E402
                               statut_lecon, verdict_resultats, verdict_valeur)
from garde import revirement  # noqa: E402

D = {"id": 1070, "decided_at": "2026-11-04T10:54:06+00:00"}
LECON = {"id": "basketvibe:L-004", "status": "hypothesis", "n_for": 0, "n_against": 1, "claim": "x"}
SANS_LECON, _ = charge_ecriture(D, "contradicted", {"valeur": -8.0}, None, S)
AVEC_LECON, _ = charge_ecriture(D, "contradicted", {"matchs": ["L"]}, LECON, S)
NC_LECON, _ = charge_ecriture(D, "inconclusive", {"valeur": None}, LECON, S)
# Ligue du 04/11 (jour de la décision, heure vide) puis du 07/11 : la fenêtre d'un match commence au 04/11.
MATCHS = [("2026-11-03", None, "W"), ("2026-11-04", None, "L"), ("2026-11-07", None, "W")]

CAS = [
    ("C3 confirmé : 115000 <= 190000", verdict_valeur(115000, "<= 190000"), "confirmed"),
    ("C3 contredit : -8 >= -5", verdict_valeur(-8, ">= -5"), "contradicted"),
    ("C3 non concluant : valeur vide", verdict_valeur(None, "<= 53.4"), "inconclusive"),
    ("C3 sans leçon : charge sans leçon", SANS_LECON["lecon"], None),
    ("C3 sans leçon : verdict transmis", (SANS_LECON["decision_id"], SANS_LECON["verdict"]), (1070, "contradicted")),
    ("C3 avec leçon : 2e contradiction → retirée + erreur",
     (AVEC_LECON["lecon"]["n_against_avant"], AVEC_LECON["lecon"]["n_against"], AVEC_LECON["lecon"]["statut"],
      AVEC_LECON["lecon"]["erreur"] is not None), (1, 2, "retired", True)),
    ("C3 non concluant : leçon inchangée", NC_LECON["lecon"], None),
    ("C2 match du jour, heure vide → compté", dans_fenetre("2026-11-04", None, D["decided_at"]), True),
    ("C2 veille, heure vide → exclu", dans_fenetre("2026-11-03", None, D["decided_at"]), False),
    ("C2 heure connue avant la décision → exclu", dans_fenetre("2026-11-04", "2026-11-04T09:00:00+00:00", D["decided_at"]), False),
    ("C2 décision 23:30 UTC = lendemain à Paris", dans_fenetre("2026-11-04", None, "2026-11-04T23:30:00+00:00"), False),
    ("C2 fenêtre d'un match = ligue du jour (L)", fenetre_resultats(MATCHS, D["decided_at"], 1), ["L"]),
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
