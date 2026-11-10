"""Réussite des tirs au cercle de nos joueurs selon la compétence Deux points, groupe v4 amical.

Usage : python -I pipelines/etudes/tirs_cercle_deux_points_v4_amical.py
Lecture seule. Probabilité linéaire (réussite 0/1 ~ Deux points / 10), IC 95 % bootstrap par grappes de matchs.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # pipelines/
import numpy as np
import pandas as pd
import sql as sqlmod
from etude_evenements_basketvibe import groupe

GROUPE = "v4 amical"
GRAINE = 20261110
TIRAGES = 2000
SEUIL_EXACTITUDE = 0.85


def lire(q):
    cols, lignes = sqlmod.executer(q)
    return pd.DataFrame(lignes, columns=cols)


def pente(y, x):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    xc = x - x.mean()
    d = (xc ** 2).sum()
    return np.nan if d == 0 else (xc * (y - y.mean())).sum() / d


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    M = lire("select fixture_id, competition, match_day, my_side, status from silver.bv_matches where status = 'finished'")
    M["groupe"] = [groupe(c, j) for c, j in zip(M.competition, M.match_day)]
    M = M[(M.groupe == GROUPE) & M.my_side.notna()].copy()
    M["match_day"] = M.match_day.astype(str).str[:10]
    print(f"Groupe {GROUPE} : {len(M)} matchs terminés à nous")
    ids = ",".join(f"'{f}'" for f in M.fixture_id)
    E = lire("select fixture_id, seq, team_side, kind, detail, player_id, is_three, shot_y, payload->>'shot_zone' as zone "
             f"from silver.bv_match_events where fixture_id in ({ids}) "
             "and (kind in ('fg2','fg3') or (kind = 'miss' and detail = 'miss_fg'))")
    E = E.merge(M[["fixture_id", "my_side", "match_day"]], on="fixture_id")
    E = E[E.team_side == E.my_side].copy()
    E["make"] = E.kind.isin(["fg2", "fg3"]).astype(int)
    E["trois"] = (E.kind == "fg3") | ((E.kind == "miss") & (E.is_three == True))  # noqa: E712
    print(f"Tirs de nos joueurs (fg2, fg3, miss_fg ; sans block ni lancers francs) : {len(E)} dont 3 points {int(E.trois.sum())}")

    D = E[~E.trois].copy()
    lab = {"fg2_make_paint": "cercle", "fg2_make_mid": "mi"}
    D["etiq"] = [lab.get(dt) if k == "fg2" else {"paint": "cercle", "mid": "mi"}.get(z) for k, dt, z in zip(D.kind, D.detail, D.zone)]
    L = D[D.etiq.notna()]
    print(f"Tirs à 2 : {len(D)} ; étiquetés {len(L)} (cercle {int((L.etiq == 'cercle').sum())}, mi {int((L.etiq == 'mi').sum())}) ; "
          f"non étiquetés {int(D.etiq.isna().sum())} (dont réussis {int(D[D.etiq.isna()].make.sum())}) ; "
          f"étiquetés par réussite : réussis {int(L.make.sum())}, ratés {int((1 - L.make).sum())}")
    Ly = L[L.shot_y.notna()]
    y = pd.to_numeric(Ly.shot_y).to_numpy()
    c = (Ly.etiq == "cercle").to_numpy()
    res = [(y0, float(((y < y0) == c).mean())) for y0 in range(100, 401, 10)]
    best = max(a for _, a in res)
    ex_aequo = [y0 for y0, a in res if a == best]
    Y0 = ex_aequo[0]
    print("Exactitude par Y0 : " + " ; ".join(f"{y0} {a:.4f}" for y0, a in res))
    print(f"Y0 = {Y0} (ex aequo : {ex_aequo}), exactitude {best:.4f} sur {len(Ly)} tirs à 2 étiquetés avec shot_y")

    U = D[D.etiq.isna()]
    if best >= SEUIL_EXACTITUDE:
        u_y = pd.to_numeric(U.shot_y)
        D.loc[U.index, "etiq"] = np.where(u_y.notna() & (u_y < Y0), "cercle", np.where(u_y.notna(), "mi", None))
        print(f"Non étiquetés classés par shot_y : cercle {int((D.loc[U.index, 'etiq'] == 'cercle').sum())}, "
              f"mi {int((D.loc[U.index, 'etiq'] == 'mi').sum())}, sans shot_y {int(u_y.isna().sum())}")
    else:
        print(f"Exactitude < 85 % : {len(U)} tirs à 2 non étiquetés exclus")
    C = D[D.etiq == "cercle"].copy()

    J = lire("select day, player_id, two_point, two_point_exact from silver.bv_player_daily")
    J["day"] = J.day.astype(str).str[:10]
    J["dp"] = [float(e) if pd.notna(e) else (float(v) if pd.notna(v) else np.nan) for e, v in zip(J.two_point_exact, J.two_point)]
    J["exact"] = J.two_point_exact.notna()
    J = J[J.dp.notna()]
    comp, exact = [], []
    for p, jr in zip(C.player_id, C.match_day):
        veille = (pd.Timestamp(jr) - pd.Timedelta(days=1)).strftime("%Y-%m-%d")
        j = J[(J.player_id == p) & (J.day <= jr) & (J.day >= veille)].sort_values("day")
        comp.append(j.dp.iloc[-1] if len(j) else np.nan)
        exact.append(bool(j.exact.iloc[-1]) if len(j) else False)
    C["dp"], C["exact"] = comp, exact
    print(f"Tirs au cercle : {len(C)} ; sans relevé Deux points (jour ou veille) exclus : {int(C.dp.isna().sum())}")
    C = C[C.dp.notna()]
    n, nm = len(C), C.fixture_id.nunique()
    print(f"Échantillon final : {n} tirs, {nm} matchs, {C.player_id.nunique()} joueurs ; Deux points à une décimale {int(C.exact.sum())}/{n} ; "
          f"Deux points min {C.dp.min()}, max {C.dp.max()}, écart-type {C.dp.std():.2f} ; réussite {C.make.mean():.4f}")
    b = pente(C.make, C.dp / 10)
    print(f"Pente : {100 * b:.2f} points de % pour +10 points de Deux points")
    if nm < 8:
        print("Moins de 8 matchs : pas d'intervalle")
        return
    rng = np.random.default_rng(GRAINE)
    grappes = [g for _, g in C.groupby("fixture_id")]
    bs = []
    for _ in range(TIRAGES):
        s = pd.concat([grappes[i] for i in rng.integers(0, len(grappes), len(grappes))])
        bs.append(pente(s.make, s.dp / 10))
    bs = np.array(bs)
    bs = bs[~np.isnan(bs)]
    lo, hi = np.percentile(bs, [2.5, 97.5])
    print(f"IC 95 % bootstrap par grappes de matchs ({TIRAGES} tirages, graine {GRAINE}, centiles, {len(bs)} tirages valides) : "
          f"[{100 * lo:.2f} ; {100 * hi:.2f}] points de %")
    print("Par joueur (tirs, réussite, Deux points moyen) :")
    for p, g in C.groupby("player_id"):
        print(f"  {str(p)[:8]} {len(g)} {g.make.mean():.3f} {g.dp.mean():.1f}")


if __name__ == "__main__":
    main()
