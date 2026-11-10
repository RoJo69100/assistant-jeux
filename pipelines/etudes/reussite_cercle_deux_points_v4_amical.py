"""Réussite des tirs au cercle selon la compétence Deux points, groupe v4 amical, nos tirs.

Probabilité linéaire : réussite (0/1) ~ a + b * (Deux points / 10) ; pente en points de % pour +10 points.
IC 95 % par bootstrap par grappes de matchs (2 000 tirages, centiles 2,5 / 97,5).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # pipelines/

import numpy as np
import pandas as pd
import sql as sqlmod
from etude_evenements_basketvibe import groupe

GRAINE = 20261110
TIRAGES = 2000
GROUPE = "v4 amical"


def lire(q):
    cols, lignes = sqlmod.executer(q)
    return pd.DataFrame(lignes, columns=cols)


def pente(x, y):
    xm = x.mean()
    sxx = ((x - xm) ** 2).sum()
    if sxx == 0:
        return np.nan
    return ((x - xm) * (y - y.mean())).sum() / sxx


def main():
    M = lire("select fixture_id, competition, match_day, my_side, status from silver.bv_matches "
             "where status = 'finished' and my_side is not null")
    M["groupe"] = [groupe(c, j) for c, j in zip(M.competition, M.match_day)]
    M = M[M.groupe == GROUPE].copy()
    M["fixture_id"] = M.fixture_id.astype(str)
    print(f"Groupe {GROUPE} : {len(M)} matchs terminés à nous, du {M.match_day.min()} au {M.match_day.max()}")

    E = lire("select fixture_id, seq, team_side, kind, detail, is_three, shot_y, player_id, "
             "payload->>'shot_zone' as zone from silver.bv_match_events "
             "where kind in ('fg2','fg3') or (kind = 'miss' and detail = 'miss_fg')")
    E["fixture_id"] = E.fixture_id.astype(str)
    E = E.merge(M[["fixture_id", "match_day", "my_side"]], on="fixture_id", how="inner")
    E = E[E.team_side == E.my_side].copy()
    print(f"Tirs à nous (fg2, fg3, miss_fg ; sans block ni LF) : {len(E)} dans {E.fixture_id.nunique()} matchs")

    E["reussi"] = E.kind.isin(["fg2", "fg3"]).astype(int)
    E["trois"] = (E.kind == "fg3") | ((E.kind == "miss") & (E.is_three == True))  # noqa: E712
    # Étiquette de zone pour les tirs à 2 : paint / mid / None
    def etiq(r):
        if r.kind == "fg2":
            return "paint" if r.detail == "fg2_make_paint" else ("mid" if r.detail == "fg2_make_mid" else None)
        if r.kind == "miss" and not r.trois:
            return r.zone if r.zone in ("paint", "mid") else None
        return None
    E["etiq"] = [etiq(r) for r in E.itertuples()]
    D = E[~E.trois].copy()
    print(f"Tirs à 3 exclus : {int(E.trois.sum())} ; tirs à 2 : {len(D)} "
          f"(étiquetés {int(D.etiq.notna().sum())}, non étiquetés {int(D.etiq.isna().sum())})")
    print("Tirs à 2 par (réussi, étiquette) : " + "; ".join(
        f"{k}: {v}" for k, v in D.groupby([D.reussi, D.etiq.fillna('aucune')]).size().items()))

    # Choix de Y0 sur les tirs à 2 étiquetés, sans regarder la réussite
    L = D[D.etiq.notna() & D.shot_y.notna()]
    print(f"Étiquetés avec shot_y : {len(L)} (sans shot_y : {int((D.etiq.notna() & D.shot_y.isna()).sum())})")
    res = []
    for y0 in range(100, 401, 10):
        acc = ((L.shot_y < y0) == (L.etiq == "paint")).mean()
        res.append((y0, acc))
    print("Y0 -> exactitude : " + " ; ".join(f"{y}:{a:.3f}" for y, a in res))
    amax = max(a for _, a in res)
    ex_aequo = [y for y, a in res if a == amax]
    y0 = ex_aequo[0]
    print(f"Y0 retenu = {y0} (exactitude {amax:.4f} ; ex aequo : {ex_aequo} ; règle : le plus petit)")

    NL = D[D.etiq.isna()].copy()
    if amax >= 0.85:
        NL_sans_y = int(NL.shot_y.isna().sum())
        NL = NL[NL.shot_y.notna()]
        NL["etiq"] = np.where(NL.shot_y < y0, "paint", "mid")
        print(f"Exactitude >= 85 % : {len(NL)} tirs à 2 non étiquetés classés par shot_y "
              f"({int((NL.etiq == 'paint').sum())} au cercle) ; sans shot_y exclus : {NL_sans_y}")
        D2 = pd.concat([D[D.etiq.notna()], NL])
    else:
        print(f"Exactitude < 85 % : {len(NL)} tirs à 2 non étiquetés exclus")
        D2 = D[D.etiq.notna()]
    C = D2[D2.etiq == "paint"].copy()
    print(f"Tirs au cercle : {len(C)} dans {C.fixture_id.nunique()} matchs (réussis {int(C.reussi.sum())})")

    # Compétence Deux points au jour du match, sinon la veille
    P = lire("select day, player_id, two_point, two_point_exact from silver.bv_player_daily")
    P["player_id"] = P.player_id.astype(str)
    P["day"] = P.day.astype(str).str[:10]
    P["val"] = [float(e) if e is not None and not pd.isna(e) else (float(i) if i is not None and not pd.isna(i) else np.nan)
                for e, i in zip(P.two_point_exact, P.two_point)]
    P["exact"] = P.two_point_exact.notna()
    P = P[P.val.notna()]
    idx = {(d, p): (v, x) for d, p, v, x in zip(P.day, P.player_id, P.val, P.exact)}
    C["player_id"] = C.player_id.astype(str)
    C["jour"] = C.match_day.astype(str).str[:10]
    vals, exacts, src = [], [], []
    for p, j in zip(C.player_id, C.jour):
        veille = (pd.Timestamp(j) - pd.Timedelta(days=1)).strftime("%Y-%m-%d")
        if (j, p) in idx:
            v, x = idx[(j, p)]; s = "jour"
        elif (veille, p) in idx:
            v, x = idx[(veille, p)]; s = "veille"
        else:
            v, x, s = np.nan, False, "absent"
        vals.append(v); exacts.append(x); src.append(s)
    C["dp"] = vals; C["exact"] = exacts; C["src"] = src
    print("Relevé de compétence : " + "; ".join(f"{k} {v}" for k, v in C.src.value_counts().items())
          + f" ; dont à une décimale {int((C.exact & C.dp.notna()).sum())}")
    print("Matchs sans aucun relevé : " + str(C[C.dp.isna()].groupby("jour").fixture_id.nunique().to_dict()))
    A = C[C.dp.notna()].copy()
    n_tirs, n_matchs = len(A), A.fixture_id.nunique()
    print(f"Échantillon du modèle : {n_tirs} tirs au cercle, {n_matchs} matchs, {A.player_id.nunique()} joueurs ; "
          f"Deux points de {A.dp.min()} à {A.dp.max()} ; réussite {A.reussi.mean():.3f}")

    x = (A.dp / 10).to_numpy(); y = A.reussi.to_numpy().astype(float)
    b = pente(x, y)
    print(f"Pente = {100 * b:.2f} points de % pour +10 points de Deux points")

    rng = np.random.default_rng(GRAINE)
    fx = A.fixture_id.to_numpy()
    ids = np.unique(fx)
    pos = {f: np.where(fx == f)[0] for f in ids}
    bs = []
    for _ in range(TIRAGES):
        tir = rng.choice(ids, size=len(ids), replace=True)
        ii = np.concatenate([pos[f] for f in tir])
        bs.append(pente(x[ii], y[ii]))
    bs = np.array(bs)
    nan = int(np.isnan(bs).sum())
    bs = bs[~np.isnan(bs)]
    lo, hi = np.percentile(bs, [2.5, 97.5]) * 100
    print(f"Bootstrap par grappes de matchs : {TIRAGES} tirages, graine {GRAINE}, tirages dégénérés {nan} ; "
          f"IC 95 % (centiles) = [{lo:.2f} ; {hi:.2f}] points de %")
    print(f"Contient zéro : {lo <= 0 <= hi}")


if __name__ == "__main__":
    main()
