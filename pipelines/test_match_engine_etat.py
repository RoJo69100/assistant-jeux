"""Test de pipelines/match_engine_etat.py sur un jeu d'essai figé (sans connexion à la base).

Lancer : python -I pipelines/test_match_engine_etat.py   (code 1 si un cas se trompe)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import match_engine_etat as me  # noqa: E402


def match(i, res, bn, bo, tn=30, te=30, ppn=2, ppe=2, ppgn=0, ppge=0, jour="2026-09-01", type_="League", niveau="PRO"):
    return {"game_id": f"g{i}", "team_level": niveau, "game_type": type_, "jour": jour, "my_result": res, "bn": bn, "bo": bo,
            "tn": tn, "te": te, "xn": 3.0, "xe": 2.0, "gvn": 8, "ppn": ppn, "ppe": ppe, "ppgn": ppgn, "ppge": ppge, "shge": 0,
            "fow": 20, "fol": 10, "s12": 20, "g12": 1, "s3": 10, "g3": 3, "capitaine": "Seppälä"}


# 4 défaites (nous 3/30 = 10 %, eux 6/30 = 20 %) et 2 victoires, dont un match sans ppAttempts adverse.
MS = [match(i, "L", 3, 6, ppge=1) for i in range(4)] + [match(10, "W", 5, 2), match(11, "W", 4, 1, ppe=None)]
GARDIENS = [{"game_id": f"g{i}", "nom": "Kovalev", "toi": 3600, "arrets": 24, "tirs": 30, "buts": 6} for i in range(4)] + \
           [{"game_id": "g10", "nom": "Kovalev", "toi": 3600, "arrets": 28, "tirs": 30, "buts": 2}]
JOUEURS = [{"nom": "Conte", "res": "L", "n": 4, "buts": 0, "tirs": 20, "diff": -2, "pim": 4},
           {"nom": "Conte", "res": "W", "n": 2, "buts": 4, "tirs": 20, "diff": 6, "pim": 0},
           {"nom": "Spinka", "res": "L", "n": 4, "buts": 1, "tirs": 20, "diff": 0, "pim": 0}]
DSC = {"Gordon Conte": 3, "Perry Spinka": 8}


def par_regle(lignes):
    return {l["regle"].split(" ")[0]: l for l in lignes}


def cas():
    r = par_regle(me.evaluer(MS, GARDIENS, JOUEURS, DSC))
    l1 = r["L-001"]
    yield "L-001 : 4 défaites, toutes moins réalistes que l'adversaire", (l1["n"], l1["pour"], l1["contre"]) == (4, 4, 0)
    yield "confiance faible sous la moitié de n requis (4 sur 10)", l1["confiance"] == "faible" and l1["verdict"].startswith("à surveiller")
    l6 = r["L-006"]
    yield "L-006 : un match sans ppAttempts est écarté, pas compté 0", "1 match(s) écarté(s)" in l6["mesure"]
    yield "L-002 : 24/30 = .800 sous .870 dans 4 défaites sur 4", (r["L-002"]["pour"], r["L-002"]["contre"]) == (4, 0)
    yield "L-008 : DSC lu par nom de famille (Conte 3, Spinka 8)", "(1 joueurs)" in r["L-008"]["mesure"]
    yield "L-011 : descriptif, jamais de verdict", r["L-011"]["verdict"].startswith("descriptif")
    yield "L-005 : une branche non lue, verdict partiel", r["L-005"]["verdict"].startswith("partiel")


def seuils():
    yield "confiance : 4/10 faible", me.confiance(4, 10) == "faible"
    yield "confiance : 5/10 moyenne", me.confiance(5, 10) == "moyenne"
    yield "confiance : 10/10 solide", me.confiance(10, 10) == "solide"
    yield "verdict : jamais confirmé sous solide", me.verdict(9, 1, "moyenne") == "à surveiller (penche pour)"
    yield "verdict : confirmé en solide", me.verdict(9, 1, "solide") == "confirmé"
    yield "verdict : infirmé en solide", me.verdict(1, 9, "solide") == "infirmé"
    yield "verdict : égalité indécise", me.verdict(3, 3, "solide") == "indécis"
    yield "verdict : zéro match", me.verdict(0, 0, "faible") == "aucun match"


def rapport():
    txt = me.rapport(MS + [match(20, "L", 1, 2, niveau="FRM", jour="2026-11-02")], GARDIENS, JOUEURS, DSC)
    yield "rapport : équipes non PRO marquées expérience sans notre choix", "expérience sans notre choix" in txt
    yield "rapport : non mesurable écrit avec ce qui manque", "non mesurable : il manque l'heure de saisie par match" in txt
    nm = [l.split(" | ") for l in txt.splitlines() if "non mesurable" in l]
    yield "rapport : aucune ligne non mesurable chiffrée", bool(nm) and all(set(c[1:7]) <= {"—"} for c in nm)
    yield "rapport : pas de ligne à zéro match hors PRO", not any("expérience" in l and "aucun match" in l for l in txt.splitlines())


if __name__ == "__main__":
    echecs = total = 0
    for groupe in (cas, seuils, rapport):
        for nom, ok in groupe():
            total += 1
            echecs += not ok
            print(("OK " if ok else "ECHEC "), nom)
    print(f"{total - echecs}/{total}")
    sys.exit(1 if echecs else 0)
