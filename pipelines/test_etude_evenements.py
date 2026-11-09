"""Tests figés de pipelines/etude_evenements_calculs.py : rééchantillonnage par matchs, pente, n requis, verdicts, outils d'horloge.

Sans réseau ni base. Lancer : python -I pipelines/test_etude_evenements.py   (code 1 si un cas se trompe)
"""
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import etude_evenements_calculs as c  # noqa: E402


def cas():
    # --- pente et rééchantillonnage ---
    n = 10
    x = np.arange(n, dtype=float)
    y = 3 * x + 1
    S = [n, x.sum(), y.sum(), (x * y).sum(), (x * x).sum()]
    yield "pente exacte : y = 3 x + 1", abs(c.pente(S) - 3) < 1e-9
    yield "pente : x constant = indéfinie", math.isnan(c.pente([4, 8, 4, 8, 16]))
    rng = np.random.default_rng(1)
    # 30 matchs, chaque match : 10 tirs, x entier, y = 0,5 x + bruit : somme par match [n, sx, sy, sxy, sxx]
    A = []
    for _ in range(30):
        xx = rng.integers(0, 10, 10).astype(float)
        yy = 0.5 * xx + rng.normal(0, 1, 10)
        A.append([10, xx.sum(), yy.sum(), (xx * yy).sum(), (xx * xx).sum()])
    r = c.boot(np.array(A), c.pente, b=500, rng=np.random.default_rng(2))
    yield "boot : la pente vraie 0,5 est dans l'intervalle sur 30 matchs", r is not None and r[1] < 0.5 < r[2]
    yield "boot : estimation proche de 0,5", abs(r[0] - 0.5) < 0.1
    yield "boot : sous 8 matchs, aucun intervalle", c.boot(np.array(A[:7]), c.pente, b=100) is None
    yield "boot : déterministe pour une graine donnée", c.boot(np.array(A), c.pente, b=200, rng=np.random.default_rng(5)) == c.boot(np.array(A), c.pente, b=200, rng=np.random.default_rng(5))
    # --- n requis ---
    yield "n requis : 100 tirs, sd 1, effet 1 → 100 × 2,8016² = 785", c.n_requis(100, 1.0, 1.0) == math.ceil(100 * (1.96 + 0.8416) ** 2)
    yield "n requis : sans écart-type, aucun calcul", c.n_requis(100, 0, 1.0) is None
    # --- verdicts ---
    yield "valeur annoncée dans l'intervalle et précis : conforme", c.v_valeur((2.2, 1.5, 3.0, 0.4), 2.25, 1.0) == "conforme"
    yield "valeur annoncée dans l'intervalle trop large : non identifiable", c.v_valeur((2.2, -1.0, 5.0, 1.5), 2.25, 1.0) == "non identifiable"
    yield "valeur annoncée hors intervalle : en écart", c.v_valeur((1.0, -0.35, 1.6, 0.5), 2.25, 1.0) == "en écart"
    yield "condition d'identifiabilité non remplie : non identifiable", c.v_valeur((2.2, 2.0, 2.4, 0.1), 2.25, 1.0, ident=False) == "non identifiable"
    yield "pas d'intervalle : non identifiable", c.v_valeur(None, 2.25, 1.0) == "non identifiable"
    yield "bande : intervalle dans la bande et précis : conforme", c.v_bande((-4, -6, -2, 1), -9, 0, 3.0) == "conforme"
    yield "bande : intervalle hors de la bande : en écart", c.v_bande((5, 2, 8, 2), -9, 0, 3.0) == "en écart"
    yield "bande : intervalle qui déborde : non identifiable", c.v_bande((-14, -22, -5.8, 4), -9, 0, 3.0) == "non identifiable"
    yield "pente annoncée positive : intervalle au-dessus de 0 et précis : conforme", c.v_positif((3, 1.5, 4.5, 1), 2.0) == "conforme"
    yield "pente annoncée positive : effet nul démontré (±2) : en écart", c.v_positif((0.1, -1.0, 1.2, 0.5), 2.0) == "en écart"
    yield "pente annoncée positive : intervalle large qui touche 0 : non identifiable", c.v_positif((6.8, -0.5, 9.0, 2), 2.0) == "non identifiable"
    # --- outils ---
    yield "horloge « 11:54:00 » = 714 s", c.secondes("11:54:00") == 714
    yield "horloge illisible : indéfinie", math.isnan(c.secondes("n/a")) and math.isnan(c.secondes(None))
    yield "binomiale exacte : 4 sur 6 → 0,6875", abs(c.binom_p2(4, 6) - 0.6875) < 1e-9
    # classement du cercle : tirs à 2 étiquetés séparés par shot_y (cercle sous 200, mi-distance au-dessus)
    T = pd.DataFrame({"trois": [False] * 8, "type2": ["cercle"] * 4 + ["mi"] * 4, "shot_y": [50, 100, 150, 180, 250, 300, 350, 400]})
    y0, ex = c.classer_cercle(T)
    yield "classement du cercle : exactitude 100 % sur des tirs séparables, seuil entre 190 et 250", ex == 1.0 and 190 <= y0 <= 250
    mal = T.copy()
    mal["type2"] = ["cercle", "mi", "cercle", "mi", "cercle", "mi", "cercle", "mi"]
    yield "classement du cercle : exactitude faible sur des étiquettes mêlées", c.classer_cercle(mal)[1] < 0.85


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    echecs = 0
    for nom, ok in cas():
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    total = sum(1 for _ in cas())
    print(f"{total - echecs}/{total}")
    sys.exit(1 if echecs else 0)
