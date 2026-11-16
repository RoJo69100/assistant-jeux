"""Étude A (premier essai, 16/11/2026) : caractéristiques d'un joueur associées à sa production, par groupe de postes.

Unité : joueur avec au moins MIN_MATCHS matchs (minutes > 0) dans le périmètre, par groupe de moteur.
Production : éval par minute ; points, rebonds, passes pour 36 min (ratio de sommes sur ses matchs).
Explicatives : milieu de tranche de chaque compétence (silver.bv_club_roster), taille, poids, âge, expérience, forme ;
snapshot d'effectif le plus récent antérieur ou égal au jour du match, sinon le plus proche après ; moyenne par joueur.
Effets : (1) pente univariée pondérée (moindres carrés), par +10 points de compétence ou par +1 écart-type pour les autres ;
(2) ridge multivarié (variables standardisées, lambda par validation croisée généralisée), éval/min seulement.
IC 95 % : bootstrap à deux voies (joueurs rééchantillonnés dans leur groupe de postes ET matchs rééchantillonnés ;
poids d'une ligne joueur-match = multiplicité joueur x multiplicité match), percentiles.
Usage : python -I pipelines/etudes/premier_essai_a_joueurs.py [tirages] [graine]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import premier_essai_communs as C  # noqa: E402

MIN_MATCHS = 3
POSTES = {"PG": "arrières PG/SG", "SG": "arrières PG/SG", "SF": "ailiers SF", "PF": "intérieurs PF/C", "C": "intérieurs PF/C"}
AUTRES = ["height_cm", "weight_kg", "age", "experience", "form"]
FEATS = C.COMPETENCES + AUTRES
SORTIES = ["eval_min", "pts36", "reb36", "ast36"]
PAIRES = [("pts36", "two_point"), ("pts36", "three_point"), ("reb36", "rebounding"), ("reb36", "height_cm"),
          ("ast36", "passing"), ("ast36", "ball_handling")]


def snapshot(R, pid, jour):
    r = R[R.player_id == pid]
    if r.empty:
        return None
    av = r[r.day <= jour]
    if len(av):
        return av.sort_values(["day", "captured_at"]).iloc[-1], "antérieur"
    return r.sort_values(["day", "captured_at"]).iloc[0], "postérieur"


def sorties(pi, w, D, nP):
    smin = np.bincount(pi, w * D["minutes"], nP)
    ok = smin > 0
    with np.errstate(invalid="ignore", divide="ignore"):
        y = {"eval_min": np.bincount(pi, w * D["eval"], nP) / smin,
             "pts36": 36 * np.bincount(pi, w * D["pts"], nP) / smin,
             "reb36": 36 * np.bincount(pi, w * D["reb"], nP) / smin,
             "ast36": 36 * np.bincount(pi, w * D["ast"], nP) / smin}
    return y, ok


def pente_w(x, y, w):
    m = (w > 0) & np.isfinite(x) & np.isfinite(y)
    if m.sum() < 3:
        return np.nan
    x, y, w = x[m], y[m], w[m]
    xb, yb = np.average(x, weights=w), np.average(y, weights=w)
    vx = (w * (x - xb) ** 2).sum()
    return np.nan if vx <= 1e-12 else float((w * (x - xb) * (y - yb)).sum() / vx)


def ridge_fit(Z, y, w, lam):
    sw = np.sqrt(w)
    yb = np.average(y, weights=w)
    Zb = np.average(Z, axis=0, weights=w)
    A, b = (Z - Zb) * sw[:, None], (y - yb) * sw
    return np.linalg.solve(A.T @ A + lam * np.eye(Z.shape[1]), A.T @ b)


def gcv_lambda(Z, y):
    A = Z - Z.mean(0)
    b = y - y.mean()
    n = len(y)
    best = None
    for lam in np.logspace(-2, 3, 41):
        H = A @ np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1]), A.T)
        r = b - H @ b
        g = n * (r @ r) / (n - np.trace(H)) ** 2
        if best is None or g < best[1]:
            best = (lam, g)
    return best[0]


def unite(f, sd):
    return 10.0 if f in C.COMPETENCES else sd


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    graine = int(sys.argv[2]) if len(sys.argv) > 2 else 20261116
    print(f"graine = {graine} ; tirages bootstrap = {nb} ; deux voies : joueurs (dans leur groupe de postes) x matchs")
    M = C.matchs()
    P = C.resume_perimetre(M)
    B = C.box()
    R = C.effectifs()
    b0 = B[(B.period == 0) & (B.minutes > 0)].merge(P[["fixture_id", "groupe", "match_day"]], on="fixture_id")
    print("\nCodes de poste du box (period 0, minutes > 0, périmètre) :", b0.position.value_counts(dropna=False).to_dict())
    print("Visibilité des compétences dans l'effectif :", R.skills_visibility.value_counts(dropna=False).to_dict(),
          f"; snapshots : {R.day.nunique()} jours, du {R.day.min()} au {R.day.max()}")
    print("Largeur moyenne de tranche (bracket) :", R[R.skills_visibility == "bracket"][[f"{c}_largeur" for c in C.COMPETENCES]].mean().round(1).to_dict())

    for g in C.GROUPES:
        bg = b0[b0.groupe == g]
        if bg.empty:
            continue
        nm = bg.groupby("player_id").fixture_id.nunique()
        garde = nm[nm >= MIN_MATCHS].index
        print(f"\n## Groupe {g} : {bg.fixture_id.nunique()} matchs dans le périmètre ; {len(garde)} joueurs avec >= {MIN_MATCHS} matchs")
        bg = bg[bg.player_id.isin(garde)].copy()
        print(f"Après filtre : {bg.fixture_id.nunique()} matchs, {len(bg)} lignes joueur-match")
        pos = bg.groupby("player_id").position.agg(lambda s: s.mode().iloc[0] if s.notna().any() else None)
        feats, sens = [], []
        for (pid, jour), _ in bg.groupby(["player_id", "match_day"]):
            s = snapshot(R, pid, jour)
            if s is None:
                continue
            row, sn = s
            sens.append(sn)
            feats.append({"player_id": pid, **{f: row[f] for f in FEATS}, "vis": row.skills_visibility})
        Fm = pd.DataFrame(feats)
        print(f"Joueurs-matchs avec snapshot : {len(Fm)} / {bg.groupby(['player_id', 'match_day']).ngroups} ; "
              f"snapshot antérieur {sens.count('antérieur')}, postérieur {sens.count('postérieur')}")
        X = Fm.groupby("player_id")[FEATS].mean()
        vis = Fm.groupby("player_id").vis.agg(lambda s: s.mode().iloc[0] if s.notna().any() else None)
        joueurs = pd.DataFrame({"pos": pos}).join(X).join(vis.rename("vis"))
        joueurs["pg"] = joueurs.pos.map(POSTES)
        print("Joueurs par groupe de postes :", joueurs.pg.value_counts(dropna=False).to_dict(),
              "; avec compétences :", int(joueurs.two_point.notna().sum()),
              "; visibilité :", joueurs.vis.value_counts(dropna=False).to_dict())
        print("Écart-type des variables (tous postes) :", joueurs[FEATS].std().round(2).to_dict())
        cs = joueurs[C.COMPETENCES].dropna()
        cr = cs.corr()
        paires = [(a, b_, cr.loc[a, b_]) for i, a in enumerate(C.COMPETENCES) for b_ in C.COMPETENCES[i + 1:]]
        paires.sort(key=lambda x: -abs(x[2]))
        print("Colinéarité (corrélation entre milieux de tranche, tous postes, n = %d) ; 6 plus fortes :" % len(cs))
        for a, b_, r in paires[:6]:
            print(f"  {a} ~ {b_} : r = {r:+.2f}")
        pids = list(joueurs.index)
        pidx = {p: i for i, p in enumerate(pids)}
        fids = list(bg.fixture_id.unique())
        fidx = {f: i for i, f in enumerate(fids)}
        pi = bg.player_id.map(pidx).to_numpy()
        mi = bg.fixture_id.map(fidx).to_numpy()
        D = {c: bg[c].to_numpy(float) for c in ("minutes", "eval", "pts", "reb", "ast")}
        nP, nM = len(pids), len(fids)
        y0, _ = sorties(pi, np.ones(len(pi)), D, nP)
        joueurs = joueurs.assign(**{k: v for k, v in y0.items()})
        print("Production moyenne par groupe de postes :")
        print(joueurs.groupby("pg")[SORTIES].mean().round(3).to_string())
        groupes_postes = ["arrières PG/SG", "ailiers SF", "intérieurs PF/C"]
        masques = {gp: (joueurs.pg == gp).to_numpy() for gp in groupes_postes}
        sds = {gp: {f: float(joueurs.loc[masques[gp], f].std()) for f in FEATS} for gp in groupes_postes}
        Xa = {f: joueurs[f].to_numpy(float) for f in FEATS}
        rid = {}
        for gp in groupes_postes:
            m = masques[gp] & np.all(np.isfinite(np.column_stack([Xa[f] for f in FEATS])), axis=1)
            Z = np.column_stack([Xa[f][m] for f in FEATS])
            mu, sd = Z.mean(0), Z.std(0)
            var = sd > 1e-9
            fk = [f for f, k in zip(FEATS, var) if k]
            Zs = (Z[:, var] - mu[var]) / sd[var]
            lam = gcv_lambda(Zs, y0["eval_min"][m])
            vif = np.diag(np.linalg.pinv(np.corrcoef(Zs, rowvar=False))) if m.sum() > len(fk) else np.full(len(fk), np.nan)
            constantes = [f for f, k in zip(FEATS, var) if not k]
            rid[gp] = {"m": m, "mu": mu[var], "sd": sd[var], "var": var, "fk": fk, "lam": lam, "vif": vif,
                       "constantes": constantes, "beta": ridge_fit(Zs, y0["eval_min"][m], np.ones(m.sum()), lam)}
        est = {}
        for gp in groupes_postes:
            w = masques[gp].astype(float)
            for s_ in SORTIES:
                for f in FEATS:
                    est[(gp, s_, f)] = pente_w(Xa[f], y0[s_], w) * unite(f, sds[gp][f])
        rng = np.random.default_rng(graine)
        bt = {k: [] for k in est}
        btr = {gp: [] for gp in groupes_postes}
        for _ in range(nb):
            wp = np.zeros(nP)
            for gp in groupes_postes:
                idx = np.flatnonzero(masques[gp])
                if len(idx):
                    wp[idx] = rng.multinomial(len(idx), np.ones(len(idx)) / len(idx))
            wm = rng.multinomial(nM, np.ones(nM) / nM).astype(float)
            w = wp[pi] * wm[mi]
            y, ok = sorties(pi, w, D, nP)
            wpl = np.where(ok, wp, 0.0)
            for gp in groupes_postes:
                wg = wpl * masques[gp]
                for s_ in SORTIES:
                    for f in FEATS:
                        bt[(gp, s_, f)].append(pente_w(Xa[f], y[s_], wg) * unite(f, sds[gp][f]))
                r_ = rid[gp]
                m = r_["m"] & (wg > 0) & np.isfinite(y["eval_min"])
                if m.sum() > 3:
                    Zs = (np.column_stack([Xa[f][m] for f in r_["fk"]]) - r_["mu"]) / r_["sd"]
                    btr[gp].append(ridge_fit(Zs, y["eval_min"][m], wg[m], r_["lam"]))
        print("\n### A1. Pentes univariées (par +10 points de compétence ; autres variables par +1 écart-type du groupe de postes)")
        print("| groupe de postes | sortie | variable | unité | n joueurs | n matchs | n joueurs-matchs | estimé | IC 95 % | verdict | n joueurs requis |")
        print("|---|---|---|---|---|---|---|---|---|---|---|")
        lignes_ok, n_tests = 0, 0
        for gp in groupes_postes:
            mp = masques[gp]
            for s_ in SORTIES:
                for f in FEATS:
                    if s_ != "eval_min" and (s_, f) not in PAIRES:
                        continue
                    sel = [p for p, k, x in zip(pids, mp, Xa[f]) if k and np.isfinite(x)]
                    nj = len(sel)
                    sub_f = bg[bg.player_id.isin(sel)]
                    ic = C.intervalle(bt[(gp, s_, f)])
                    e = est[(gp, s_, f)]
                    v = C.verdict(e, ic, sub_f.fixture_id.nunique())
                    if nj < 10:
                        v = "indéterminé : n trop petit"
                    n_tests += 1
                    lignes_ok += v == "association présente"
                    nr = C.n_requis(nj, e, ic) if v != "association présente" else None
                    u = "+10 pts" if f in C.COMPETENCES else f"+1 ET = {sds[gp][f]:.1f}"
                    print(f"| {gp} | {s_} | {f} | {u} | {nj} | {sub_f.fixture_id.nunique()} | {len(sub_f)} | {C.fmt(e)} | "
                          f"{C.fic(ic)} | {v} | {nr if nr else '-'} |")
        print(f"\nLignes « association présente » : {lignes_ok} sur {n_tests} tests (environ {0.05 * n_tests:.1f} faux positifs attendus si aucun effet)")
        print("\n### A2. Ridge multivarié, éval/min (coefficient par +10 points de compétence ; autres par +1 écart-type)")
        for gp in groupes_postes:
            r_ = rid[gp]
            arr = np.array(btr[gp])
            print(f"\n{gp} : n joueurs (cas complets) = {int(r_['m'].sum())}, lambda GCV = {r_['lam']:.2f}, tirages valides = {len(arr)}"
                  f" ; variables constantes exclues : {r_['constantes'] or 'aucune'}")
            print("| variable | VIF | coefficient | IC 95 % | verdict |")
            print("|---|---|---|---|---|")
            for j, f in enumerate(r_["fk"]):
                k = 10.0 / r_["sd"][j] if f in C.COMPETENCES else 1.0
                e = r_["beta"][j] * k
                ic = C.intervalle(arr[:, j] * k) if len(arr) else None
                v = C.verdict(e, ic, 8 if r_["m"].sum() >= 10 else 0)
                print(f"| {f} | {r_['vif'][j]:.1f} | {C.fmt(e)} | {C.fic(ic)} | {v} |")
    print(f"\nRequêtes exécutées par ce script : {C.NB_REQUETES[0]}")


if __name__ == "__main__":
    main()
