"""Étude B (premier essai, 16/11/2026) : minutes et production, par groupe de moteur.

B1. Joueurs avec minutes > 0 aux 4 quarts d'un match : éval/min et pts/min par quart (ratio de sommes sur les
    joueurs-matchs), baisse Q4 - Q1 ; écart de cette baisse entre équipes « à 5 x 48 » (au moins FER joueurs à >= SEUIL min
    au box du match) et équipes qui tournent. IC 95 % : bootstrap par grappes de matchs (percentiles).
B2. Par équipe-match : part des minutes des 5 premiers, nombre de joueurs au-delà de 36 min, marge (points de l'équipe -
    points adverses, depuis le box period 0 ; une marge, pas un résultat). Pente de la marge sur la concentration :
    au niveau équipe (moyennes, équipes avec >= MIN_MATCHS matchs ; bootstrap sur les équipes) et au niveau équipe-match
    (bootstrap par grappes de matchs). Description seule si moins de 8 équipes.
Usage : python -I pipelines/etudes/premier_essai_b_minutes.py [tirages] [graine] [seuil_min] [nb_joueurs]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import premier_essai_communs as C  # noqa: E402

MIN_MATCHS = 3


def taux_quarts(Q, w_match, fidx):
    """Q : lignes joueur-quart ; renvoie {(stat, quart): taux} pondéré par la multiplicité du match."""
    w = w_match[Q.fixture_id.map(fidx).to_numpy()]
    out = {}
    for q in (1, 2, 3, 4):
        m = (Q.period == q).to_numpy()
        mins = (w[m] * Q.minutes.to_numpy()[m]).sum()
        for s in ("eval", "pts"):
            out[(s, q)] = (w[m] * Q[s].to_numpy()[m]).sum() / mins if mins > 0 else np.nan
    return out


def pente(x, y, w=None):
    x, y = np.asarray(x, float), np.asarray(y, float)
    w = np.ones(len(x)) if w is None else np.asarray(w, float)
    m = (w > 0) & np.isfinite(x) & np.isfinite(y)
    if m.sum() < 3:
        return np.nan
    x, y, w = x[m], y[m], w[m]
    xb, yb = np.average(x, weights=w), np.average(y, weights=w)
    vx = (w * (x - xb) ** 2).sum()
    return np.nan if vx <= 1e-12 else float((w * (x - xb) * (y - yb)).sum() / vx)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    graine = int(sys.argv[2]) if len(sys.argv) > 2 else 20261116
    seuil = float(sys.argv[3]) if len(sys.argv) > 3 else 44.0
    fer = int(sys.argv[4]) if len(sys.argv) > 4 else 5
    print(f"graine = {graine} ; tirages bootstrap = {nb} ; « 5 x 48 » = au moins {fer} joueurs à >= {seuil} min")
    M = C.matchs()
    P = C.resume_perimetre(M)
    B = C.box()
    B = B[B.fixture_id.isin(P.fixture_id) & (B.minutes > 0)].merge(P[["fixture_id", "groupe", "overtime_periods"]], on="fixture_id")
    for g in C.GROUPES:
        bg = B[B.groupe == g]
        if bg.empty:
            continue
        rng = np.random.default_rng(graine)
        b0 = bg[bg.period == 0]
        tm = b0.groupby(["fixture_id", "team_side"]).minutes.sum()
        print(f"\n## Groupe {g} : {bg.fixture_id.nunique()} matchs, {len(tm)} équipes-matchs")
        print(f"Contrôle : minutes par équipe-match (attendu 240 sans prolongation) : min {tm.min():.1f}, médiane {tm.median():.1f}, max {tm.max():.1f} ;"
              f" matchs avec prolongation : {int((pd.to_numeric(P[P.groupe == g].overtime_periods, errors='coerce').fillna(0) > 0).sum())}")
        # équipes-matchs
        tmm = b0.groupby(["fixture_id", "team_side"]).agg(team_id=("team_id", "first"), team=("team", "first"),
                                                          pts=("pts", "sum"), mins=("minutes", "sum"),
                                                          n_seuil=("minutes", lambda s: int((s >= seuil).sum())),
                                                          n36=("minutes", lambda s: int((s > 36).sum())),
                                                          top5=("minutes", lambda s: s.nlargest(5).sum())).reset_index()
        tmm["part5"] = 100 * tmm.top5 / tmm.mins
        adv = tmm[["fixture_id", "team_side", "pts"]].copy()
        adv["team_side"] = adv.team_side.map({"home": "away", "away": "home"})
        tmm = tmm.merge(adv.rename(columns={"pts": "pts_adv"}), on=["fixture_id", "team_side"])
        tmm["marge"] = tmm.pts - tmm.pts_adv
        tmm["fer"] = tmm.n_seuil >= fer
        print(f"Distribution du nombre de joueurs à >= {seuil} min par équipe-match :", tmm.n_seuil.value_counts().sort_index().to_dict())
        print("Distribution du nombre de joueurs au-delà de 36 min :", tmm.n36.value_counts().sort_index().to_dict())
        print(f"Part des 5 premiers (%) : min {tmm.part5.min():.1f}, médiane {tmm.part5.median():.1f}, max {tmm.part5.max():.1f}")
        # B1
        bq = bg[bg.period.between(1, 4)]
        nq = bq.groupby(["fixture_id", "player_id"]).period.nunique()
        quatre = nq[nq == 4].reset_index()[["fixture_id", "player_id"]]
        Q = bq.merge(quatre, on=["fixture_id", "player_id"]).merge(tmm[["fixture_id", "team_side", "fer"]], on=["fixture_id", "team_side"])
        fids = list(bg.fixture_id.unique())
        fidx = {f: i for i, f in enumerate(fids)}
        nM = len(fids)
        sous = {"tous": Q, "5 x 48": Q[Q.fer], "tournent": Q[~Q.fer]}
        est = {k: taux_quarts(v, np.ones(nM), fidx) for k, v in sous.items()}
        bt = {k: [] for k in sous}
        for _ in range(nb):
            wm = rng.multinomial(nM, np.ones(nM) / nM).astype(float)
            for k, v in sous.items():
                bt[k].append(taux_quarts(v, wm, fidx))
        print("\n### B1. Production par minute par quart (joueurs aux 4 quarts)")
        print("| sous-ensemble | n joueurs-matchs | n matchs | stat | Q1 | Q2 | Q3 | Q4 | Q4 - Q1 | IC 95 % | verdict | n matchs requis |")
        print("|---|---|---|---|---|---|---|---|---|---|---|---|")
        for k, v in sous.items():
            n_pm = v.groupby(["fixture_id", "player_id"]).ngroups
            n_m = v.fixture_id.nunique()
            for s in ("eval", "pts"):
                e = est[k]
                d = e[(s, 4)] - e[(s, 1)]
                ic = C.intervalle([b[(s, 4)] - b[(s, 1)] for b in bt[k]])
                vd = C.verdict(d, ic, n_m)
                nr = C.n_requis(n_m, d, ic) if vd != "association présente" else None
                print(f"| {k} | {n_pm} | {n_m} | {s}/min | {e[(s, 1)]:.3f} | {e[(s, 2)]:.3f} | {e[(s, 3)]:.3f} | {e[(s, 4)]:.3f} | "
                      f"{C.fmt(d)} | {C.fic(ic)} | {vd} | {nr or '-'} |")
        nf, nt = sous["5 x 48"].fixture_id.nunique(), sous["tournent"].fixture_id.nunique()
        for s in ("eval", "pts"):
            d = (est["5 x 48"][(s, 4)] - est["5 x 48"][(s, 1)]) - (est["tournent"][(s, 4)] - est["tournent"][(s, 1)])
            ic = C.intervalle([(a[(s, 4)] - a[(s, 1)]) - (b[(s, 4)] - b[(s, 1)]) for a, b in zip(bt["5 x 48"], bt["tournent"])])
            vd = C.verdict(d, ic, min(nf, nt))
            print(f"Écart de baisse ({s}/min), 5 x 48 moins tournent : {C.fmt(d)} {C.fic(ic)} ; matchs 5 x 48 {nf}, tournent {nt} ; {vd}"
                  + (f" ; n matchs requis (par sous-ensemble) {C.n_requis(min(nf, nt), d, ic)}" if vd != 'association présente' else ""))
        # B2
        print("\n### B2. Concentration des minutes et marge")
        par_eq = tmm.groupby("team_id").agg(team=("team", "first"), n=("fixture_id", "size"), part5=("part5", "mean"),
                                            n36=("n36", "mean"), marge=("marge", "mean")).sort_values("n", ascending=False)
        eq = par_eq[par_eq.n >= MIN_MATCHS]
        print(f"Équipes : {len(par_eq)} ; avec >= {MIN_MATCHS} matchs : {len(eq)}")
        print("| équipe | matchs | part des 5 premiers (%) | joueurs > 36 min (moy.) | marge moyenne |")
        print("|---|---|---|---|---|")
        for r in eq.itertuples():
            print(f"| {r.team} | {r.n} | {r.part5:.1f} | {r.n36:.2f} | {r.marge:+.1f} |")
        for var, u in (("part5", 10.0), ("n36", 1.0)):
            lab = "+10 points de part des 5 premiers" if var == "part5" else "+1 joueur au-delà de 36 min"
            if len(eq) >= 8:
                e = pente(eq[var], eq.marge) * u
                bts = []
                for _ in range(nb):
                    i = rng.integers(0, len(eq), len(eq))
                    bts.append(pente(eq[var].to_numpy()[i], eq.marge.to_numpy()[i]) * u)
                ic = C.intervalle(bts)
                r_ = float(np.corrcoef(eq[var], eq.marge)[0, 1])
                vd = C.verdict(e, ic, len(eq))
                print(f"Niveau équipe (n = {len(eq)} équipes) : marge pour {lab} = {C.fmt(e, 2)} {C.fic(ic, 2)} ; r = {r_:+.2f} ; "
                      f"bootstrap sur les équipes ; {vd}" + (f" ; n équipes requis {C.n_requis(len(eq), e, ic)}" if vd != 'association présente' else ""))
            else:
                print(f"Niveau équipe : {len(eq)} équipes < 8 : description seulement")
            # niveau équipe-match, grappes de matchs
            fi = tmm.fixture_id.map(fidx).to_numpy()
            e = pente(tmm[var], tmm.marge) * u
            bts = []
            for _ in range(nb):
                wm = rng.multinomial(nM, np.ones(nM) / nM).astype(float)
                bts.append(pente(tmm[var], tmm.marge, wm[fi]) * u)
            ic = C.intervalle(bts)
            vd = C.verdict(e, ic, tmm.fixture_id.nunique())
            print(f"Niveau équipe-match (n = {len(tmm)} équipes-matchs, {tmm.fixture_id.nunique()} matchs) : marge pour {lab} = "
                  f"{C.fmt(e, 2)} {C.fic(ic, 2)} ; grappes de matchs ; {vd}"
                  + (f" ; n matchs requis {C.n_requis(tmm.fixture_id.nunique(), e, ic)}" if vd != 'association présente' else ""))
    print(f"\nRequêtes exécutées par ce script : {C.NB_REQUETES[0]}")


if __name__ == "__main__":
    main()
