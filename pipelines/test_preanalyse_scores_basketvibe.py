"""Tests figés de pipelines/preanalyse_scores_basketvibe.py (questions 5 et 6, ligue saison 1) : sans réseau ni base.

Chaque question a ses cas : lois (binomiale exacte, Student), mesure sur un jeu de six matchs aux valeurs calculées à la main,
force d'équipe sur quatre équipes et quatre journées (strictement antérieur, minimum de 3 matchs), pente et verdicts.
Lancer : python -I pipelines/test_preanalyse_scores_basketvibe.py   (code 1 si un cas se trompe)
"""
import math
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import preanalyse_scores_basketvibe as ps  # noqa: E402

base = ps.base


def proche(a, b, tol=1e-3):
    return a is not None and abs(a - b) <= tol


def matchs(lignes):
    return pd.DataFrame(lignes, columns=["match_day", "home_team_id", "away_team_id", "home_score", "away_score"])


# Quatre équipes, quatre journées : les forces antérieures se calculent à la main (voir test_force).
SAISON = matchs([
    ("2026-09-07", "A", "B", 80, 60), ("2026-09-07", "C", "D", 70, 70),
    ("2026-09-09", "A", "C", 90, 70), ("2026-09-09", "B", "D", 60, 80),
    ("2026-09-12", "B", "C", 70, 60), ("2026-09-12", "A", "D", 75, 85),
    ("2026-09-14", "A", "B", 85, 70), ("2026-09-14", "C", "D", 60, 75),
])
# Six matchs : marges à domicile 10, −4, 6, 8, −2, 12 (moyenne 5, écart-type √42,8 = 6,5422 ; 4 victoires sur 6).
SIX = matchs([("2026-09-07", f"H{i}", f"E{i}", 100 + m, 100) for i, m in enumerate([10, -4, 6, 8, -2, 12])])


def cas():
    # --- lois ---
    yield "binomiale exacte : 4 sur 6 → p = 0,6875 (calcul à la main)", proche(base.binom_p2(4, 6), 0.6875, 1e-9)
    yield "binomiale exacte : 13 sur 22 → p = 0,523 (sortie du premier script)", round(base.binom_p2(13, 22), 3) == 0.523
    yield "binomiale exacte : 0 sur 10 → p très petit", base.binom_p2(0, 10) < 0.003
    yield "Student : t(0,975 ; 10) = 2,2281", proche(base.t_ppf(0.975, 10), 2.2281)
    yield "Student : t(0,975 ; 21) = 2,0796", proche(base.t_ppf(0.975, 21), 2.0796)
    yield "Wilson 50 sur 100 à 95 % : [0,4038 ; 0,5962]", all(proche(a, b, 5e-4) for a, b in zip(ps.wilson(50, 100, 0.05), (0.4038, 0.5962)))
    # --- question 5 : mesure sur six matchs ---
    r = ps.q5(SIX)
    yield "Q5 (a) six matchs : 4 victoires sur 6, p exact 0,6875", r["k"] == 4 and r["n"] == 6 and proche(r["p_exact"], 0.6875, 1e-9)
    yield "Q5 (a) six matchs : n < 236, verdict « n trop petit »", r["verdict_a"] == "n trop petit"
    m, n, sd, lo, hi, p = r["marge"]
    yield "Q5 (b) six matchs : moyenne 5, écart-type 6,5422, n = 6", proche(m, 5.0) and proche(sd, 6.5422) and n == 6
    yield "Q5 (b) n requis = ((2,2414 + 0,8416) × σ / 3)² arrondi : 46", r["n_req_marge"] == 46 and r["verdict_b"] == "n trop petit"
    yield "Q5 (b) intervalle à 97,5 % autour de la moyenne et p du t de Student cohérents", lo < 5.0 < hi and 0 < p < 0.2
    quatre = ps.q5(SIX.head(4))
    yield "Q5 moins de 5 matchs : aucun calcul de marge", quatre["marge"] is None and quatre["verdict_b"] == "n < 5 : aucun calcul"
    yield "Q5 (a) verdict d'une proportion : 160 sur 236 (67,8 %) = effet présent", ps.verdict_proportion(160, 236, 236, 0.025) == "décidable : effet présent"
    yield "Q5 (a) verdict d'une proportion : 118 sur 236 (50 %) = effet absent", ps.verdict_proportion(118, 236, 236, 0.025) == "décidable : effet absent"
    yield "Q5 (a) verdict d'une proportion : 136 sur 236 (57,6 %) = entre les deux", ps.verdict_proportion(136, 236, 236, 0.025) == "décidable : entre les deux"
    # --- question 6 : force d'équipe ---
    paires = ps.forces_anterieures(SAISON)
    yield "Q6 force : A +10 (20, 20, −10), B −10, C −10, D +10 → écarts (20 ; −20), marges (15 ; −15)", paires == [(20.0, 15), (-20.0, -15)]
    yield "Q6 les matchs sans 3 matchs antérieurs (journées 1 à 3) sont écartés", len(paires) == 2
    yield "Q6 minimum 2 : les matchs de la 3e journée entrent (priors des 2 premières journées seulement)", \
        ps.forces_anterieures(SAISON, minimum=2) == [(-10.0, 10), (10.0, -10), (20.0, 15), (-20.0, -15)]
    yield "Q6 un match du jour même ne compte pas comme antérieur", \
        ps.forces_anterieures(matchs([("2026-09-07", "A", "B", 80, 60), ("2026-09-07", "A", "C", 50, 40), ("2026-09-07", "B", "C", 70, 60)]), minimum=1) == []
    x = list(range(40))
    ligne = ps.pente(x, [0.5 * v + 3 for v in x], 0.05)
    yield "Q6 pente d'une droite exacte y = 0,5 x + 3 : 0,5", ligne is not None and proche(ligne[0], 0.5, 1e-9)
    yield "Q6 pente sous 5 points : aucun calcul", ps.pente([1, 2, 3, 4], [1, 2, 3, 4], 0.05) is None
    present = base.verdict_corr(base.pearson(x, [0.5 * v for v in x], 0.05), 0.5, 30)
    yield "Q6 corrélation parfaite sur 40 points : décidable, effet présent", present == "décidable : effet présent"
    bruit = base.verdict_corr(base.pearson(x, [(-1) ** i for i in x], 0.05), 0.5, 30)
    yield "Q6 signe alterné sur 40 points : décidable, effet absent", bruit == "décidable : effet absent"
    yield "Q6 corrélation sur 12 points : n trop petit (n requis 30)", \
        base.verdict_corr(base.pearson(list(range(12)), [2 * v for v in range(12)], 0.05), 0.5, 30) == "n trop petit"
    yield "Q6 quatre points : aucun calcul", base.pearson([1, 2, 3, 4], [1, 2, 4, 3], 0.05) is None


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    echecs = 0
    for nom, ok in cas():
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    n = sum(1 for _ in cas())
    print(f"{n - echecs}/{n}")
    sys.exit(1 if echecs else 0)
