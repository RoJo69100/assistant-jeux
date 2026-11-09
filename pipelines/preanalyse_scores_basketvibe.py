"""Préanalyse BasketVibe sur les matchs à score seul (questions 5 et 6), ligue saison 1, moteur v3.

Critères écrits avant calcul : docs/refonte-v3/preanalyse-matchs-basketvibe.md, § 2.4 (commit c571b30).
Source : silver.bv_fixtures (264 matchs terminés, 24 équipes). Résultat historique : moteur v3, non transférable à la ligue v4
ni aux amicaux v5. Lecture seule (executer() de sql.py).
Usage : python -I pipelines/preanalyse_scores_basketvibe.py
Tests : pipelines/test_preanalyse_scores_basketvibe.py
Intervalle d'une proportion : Wilson (choisi à l'écriture du script, avant toute exécution) ; effet « présent » si l'intervalle exclut 0,5
et |taux − 0,5| ≥ 0,10 ; « absent » si l'intervalle tient dans ]0,40 ; 0,60[ ; sinon « entre les deux ».
"""
import math
import sys
from pathlib import Path
from statistics import NormalDist

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python -I n'ajoute pas le dossier du script
import preanalyse_matchs_basketvibe as base  # noqa: E402

SAISON_1 = "8fa19101-6f06-4e2e-96d5-e3181a8e69f8"
MIN_PRECEDENTS = 3  # comme pipelines/palier5_test.py
Z = NormalDist().inv_cdf
SQL = ("select match_day, home_team_id, away_team_id, home_score, away_score, is_mine from silver.bv_fixtures "
       f"where status = 'finished' and season_id = '{SAISON_1}' and home_score is not null and away_score is not null "
       "order by match_day")


def jour(x):
    return str(x)[:10]


def wilson(k, n, alpha):
    if n == 0:
        return math.nan, math.nan
    z, p = Z(1 - alpha / 2), k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    demi = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return centre - demi, centre + demi


def verdict_proportion(k, n, n_req, alpha, delta=0.10):
    if n < 5:
        return "n < 5 : aucun calcul"
    if n < n_req:
        return "n trop petit"
    lo, hi = wilson(k, n, alpha)
    p = k / n
    if (lo > 0.5 or hi < 0.5) and abs(p - 0.5) >= delta:
        return "décidable : effet présent"
    if lo > 0.5 - delta and hi < 0.5 + delta:
        return "décidable : effet absent"
    return "décidable : entre les deux"


def q5(df, alpha=0.025, n_req_victoires=236, delta_marge=3.0):
    """(a) victoires à domicile contre 0,5 (binomial exact) ; (b) marge domicile − extérieur (t de Student)."""
    marge = df.home_score - df.away_score
    k, n = int((marge > 0).sum()), int((marge != 0).sum())
    res = {"k": k, "n": n, "taux": k / n if n else math.nan, "p_exact": base.binom_p2(k, n) if n else math.nan,
           "ic": wilson(k, n, alpha), "verdict_a": verdict_proportion(k, n, n_req_victoires, alpha)}
    m = base.moyenne(marge, alpha)
    res["marge"] = m
    if m is not None:
        mm, nn, sd, lo, hi, p = m
        res["n_req_marge"] = math.ceil(((Z(1 - alpha / 2) + base.Z_BETA) * sd / delta_marge) ** 2)
        res["verdict_b"] = base.verdict_moy(m, delta_marge, res["n_req_marge"])
    else:
        res["n_req_marge"], res["verdict_b"] = None, "n < 5 : aucun calcul"
    return res


def forces_anterieures(df, minimum=MIN_PRECEDENTS):
    """[(écart de force domicile − extérieur, marge domicile − extérieur)] pour les matchs dont les deux équipes ont au moins
    `minimum` matchs terminés STRICTEMENT antérieurs (jour inférieur) ; force = moyenne de (points marqués − encaissés)."""
    d = df.copy()
    d["jour"] = d.match_day.map(jour)
    hist = {}  # équipe -> [(jour, marge de l'équipe)]
    for r in d.itertuples():
        mg = r.home_score - r.away_score
        hist.setdefault(r.home_team_id, []).append((r.jour, mg))
        hist.setdefault(r.away_team_id, []).append((r.jour, -mg))
    sortie = []
    for r in d.itertuples():
        f = []
        for eq in (r.home_team_id, r.away_team_id):
            avant = [m for (j, m) in hist[eq] if j < r.jour]
            f.append(sum(avant) / len(avant) if len(avant) >= minimum else None)
        if None not in f:
            sortie.append((f[0] - f[1], r.home_score - r.away_score))
    return sortie


def pente(x, y, alpha):
    """(pente, IC bas, IC haut) par moindres carrés ; None si n < 5 ou x constant."""
    d = pd.DataFrame({"x": x, "y": y}).dropna()
    n = len(d)
    if n < 5 or d.x.std() == 0:
        return None
    r = float(d.x.corr(d.y))
    b = r * d.y.std() / d.x.std()
    se = math.sqrt(max(1 - r * r, 0) / (n - 2)) * d.y.std() / d.x.std()
    t = base.t_ppf(1 - alpha / 2, n - 2)
    return b, b - t * se, b + t * se


def q6(df, alpha=0.05, r_min=0.5, n_req=30):
    paires = forces_anterieures(df)
    x, y = [p[0] for p in paires], [p[1] for p in paires]
    res = base.pearson(x, y, alpha)
    return {"n": len(paires), "pearson": res, "pente": pente(x, y, alpha), "verdict": base.verdict_corr(res, r_min, n_req),
            "n_req": n_req}


def f(x, nd=2):
    return "—" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.{nd}f}"


def charger():
    cols, lignes = base.sqlmod.executer(SQL)
    return pd.DataFrame(lignes, columns=cols)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    df = charger()
    for c in ("home_score", "away_score"):
        df[c] = pd.to_numeric(df[c])
    df["mien"] = df.is_mine.astype(str).str.lower().isin(["true", "t", "1"])
    print(f"## Ligue saison 1, moteur v3 : {len(df)} matchs terminés ({int(df.mien.sum())} à nous, {int((~df.mien).sum())} des autres équipes), "
          f"{df.match_day.map(jour).min()} au {df.match_day.map(jour).max()}, {len(set(df.home_team_id) | set(df.away_team_id))} équipes\n")
    print("### Question 5 : avantage du terrain (α = 0,025 par test)\n")
    print("| population | mesure | résultat | n disponible | n requis | verdict |\n|---|---|---|---|---|---|")
    for nom, d in (("tous les matchs", df), ("nos matchs (description)", df[df.mien]), ("matchs des autres (description)", df[~df.mien])):
        r = q5(d)
        lo, hi = r["ic"]
        print(f"| {nom} | (a) victoires à domicile | {r['k']} sur {r['n']} = {f(r['taux'] * 100, 1)} % [Wilson 97,5 % : {f(lo * 100, 1)} ; {f(hi * 100, 1)}], p exact {f(r['p_exact'], 3)} | {r['n']} | 236 | {r['verdict_a']} |")
        if r["marge"] is None:
            print(f"| {nom} | (b) marge domicile − extérieur | — | {len(d)} | — | n < 5 : aucun calcul |")
        else:
            m, n, sd, lo, hi, p = r["marge"]
            print(f"| {nom} | (b) marge domicile − extérieur | {f(m, 2)} points [{f(lo, 2)} ; {f(hi, 2)}], σ = {f(sd, 2)}, p = {f(p, 3)} | {n} | {r['n_req_marge']} | {r['verdict_b']} |")
    print("\n### Question 6 : force d'équipe (moyenne des marges des matchs antérieurs, au moins 3) et marge\n")
    r = q6(df)
    print("| mesure | résultat | n disponible | n requis | verdict |\n|---|---|---|---|---|")
    pe = r["pearson"]
    if pe is None:
        print(f"| corrélation | — | {r['n']} | {r['n_req']} | {r['verdict']} |")
    else:
        rr, n, lo, hi, p = pe
        print(f"| corrélation de l'écart de force avec la marge | r = {f(rr, 2)} [{f(lo, 2)} ; {f(hi, 2)}], p = {f(p, 4)} | {n} | {r['n_req']} | {r['verdict']} |")
        b, blo, bhi = r["pente"]
        print(f"| pente (points de marge par point d'écart de force) | {f(b, 2)} [{f(blo, 2)} ; {f(bhi, 2)}] | {n} | {r['n_req']} | {r['verdict']} |")
    print(f"\nMatchs écartés faute de 3 matchs antérieurs pour l'une des deux équipes : {len(df) - r['n']} sur {len(df)}.")


if __name__ == "__main__":
    main()
