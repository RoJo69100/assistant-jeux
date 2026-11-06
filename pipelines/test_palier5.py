"""Test de pipelines/palier5_test.py sur des données figées (sans réseau ni base).

Lancer : python pipelines/test_palier5.py   (code 1 si un cas se trompe)
"""
import datetime as dt
import importlib.util
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("p5", Path(__file__).resolve().parent / "palier5_test.py")
p5 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p5)


def rel(team, day, w, l, pf, mine=False):
    return {"team": team, "day": dt.date.fromisoformat(day), "wins": w, "losses": l, "points_for": pf,
            "is_mine": mine, "club_strength": 50}


CLASSEMENT = [
    rel("Moi", "2026-11-01", 1, 1, 200, True),   # 100,0 par match
    rel("Fort", "2026-11-01", 2, 0, 230),         # 115,0
    rel("Faible", "2026-11-01", 0, 2, 180),       # 90,0
    rel("Pareil", "2026-11-01", 1, 1, 200),       # 100,0 : écart nul
    rel("Fort", "2026-11-05", 3, 0, 240),         # relevé POSTÉRIEUR au match du 11-03 : 80,0 s'il était lu
]
MATCHS = [
    {"match_day": dt.date(2026, 11, 3), "opponent": "Fort", "my_result": "L"},
    {"match_day": dt.date(2026, 11, 3), "opponent": "Faible", "my_result": "W"},
    {"match_day": dt.date(2026, 11, 3), "opponent": "Pareil", "my_result": "W"},
    {"match_day": dt.date(2026, 11, 3), "opponent": "Inconnu", "my_result": "W"},
    {"match_day": dt.date(2026, 11, 1), "opponent": "Fort", "my_result": "W"},  # relevé du jour même exclu
]


def cas():
    lignes, sans = p5.evaluer(MATCHS, CLASSEMENT)
    par_adv = {l["adversaire"]: l for l in lignes}
    yield "adversaire plus fort : prédit défaite, juste", par_adv["Fort"]["prediction"] == "L" and par_adv["Fort"]["issue"] == "juste"
    yield "relevé postérieur jamais lu", abs(par_adv["Fort"]["eux"] - 115.0) < 1e-9
    yield "adversaire plus faible : prédit victoire", par_adv["Faible"]["prediction"] == "W" and par_adv["Faible"]["issue"] == "juste"
    yield "écart sous E : équivalent", par_adv["Pareil"]["prediction"] == "=" and par_adv["Pareil"]["issue"] == "équivalent"
    yield "adversaire inconnu : sans classement", len(sans) == 2 and len(lignes) == 3
    yield "relevé du jour du match exclu", any(m["match_day"] == dt.date(2026, 11, 1) for m in sans)
    b = p5.bilan(lignes, sans)
    yield "part hors équivalent", b["juste"] == 2 and b["faux"] == 0 and b["part_justes"] == 1.0 and b["equivalent"] == 1
    yield "moins de 20 matchs : non mesurable", b["verdict"].startswith("non mesurable : 3 match(s)")
    # 20 matchs, prédictions toutes justes mais base naïve haute : pas de marge de 10 points
    f = [{"issue": "juste", "reel": "W"}] * 19 + [{"issue": "faux", "reel": "L"}]
    yield "base naïve trop proche : non utilisable", p5.bilan(f, [])["verdict"] == "non utilisable"
    g = [{"issue": "juste", "reel": "L"}] * 20
    yield "marge de 10 points tenue : utilisable", p5.bilan(g, [])["verdict"] == "utilisable avec confiance faible"
    yield "prédiction à E pile", p5.predire(100.3, 100.0) == "W" and p5.predire(100.0, 100.3) == "L" and p5.predire(100.2, 100.0) == "="


if __name__ == "__main__":
    echecs = 0
    for nom, ok in cas():
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    n = sum(1 for _ in cas())
    print(f"{n - echecs}/{n}")
    sys.exit(1 if echecs else 0)
