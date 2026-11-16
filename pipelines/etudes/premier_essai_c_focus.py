"""Étude C (premier essai, mise à jour du 16/11/2026) : focus défensif adverse INFÉRÉ (règle T3 levée, décision du 13/11).

Libellés : « off » de l'export = Lock (validé par l'utilisateur le 21/10, learnings L-018) ; intense = Intense ;
normal = Normal ; give_up = Give up ; light = Light (gardé à part) ; « normal (pas de plan) » exclu.
1. Calibration sur TOUS nos matchs de gold.bv_match_opp_focus :
   1a. part de tirs du joueur visé (shot_share, en %) par niveau et par groupe de moteur ;
   1b. comparaison de la part en Normal entre groupes (écart au groupe le plus fourni, IC par grappes) :
       comparable (tous les IC contiennent 0) -> estimation regroupée avec le groupe en covariable (écart niveau - Normal
       calculé DANS chaque groupe puis moyenné, poids = n du niveau) ; sinon, calibration par groupe ;
   1c. même chose en écart à la référence du joueur (Δpart = part du match - part moyenne dans ses autres matchs en base
       du même groupe, au moins MIN_AUTRES autres matchs).
2. Application en sens inverse, matchs des autres clubs du périmètre (box 0 + Q1..Q4 + événements), par groupe :
   pour chaque joueur-match, ses autres matchs du groupe sont tirés au hasard en deux moitiés : moitié A pour choisir les
   étoiles (2 plus gros tireurs par minute de l'équipe), moitié B pour la référence (part de tirs, tirs/min) -> pas de
   régression vers la moyenne par sélection. Écart des étoiles au témoin (tous les joueurs avec référence) comparé aux
   écarts calibrés (niveau - Normal) ; niveau le plus proche par joueur-match (écart-type commun) -> répartition « inférée ».
IC 95 % : bootstrap par grappes de matchs (percentiles) ; moins de 8 matchs : pas d'intervalle.
Usage : python -I pipelines/etudes/premier_essai_c_focus.py [tirages] [graine]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import premier_essai_communs as C  # noqa: E402

MIN_AUTRES = 3
NIVEAUX = {"off": "Lock", "intense": "Intense", "normal": "Normal", "give_up": "Give up", "light": "Light"}
ORDRE = ["Lock", "Intense", "Normal", "Light", "Give up"]


def boot_moy(df, col, nb, rng):
    ids = df.fixture_id.unique()
    if len(ids) < 8:
        return None
    fi = df.fixture_id.map({f: i for i, f in enumerate(ids)}).to_numpy()
    v = df[col].to_numpy(float)
    out = []
    for _ in range(nb):
        w = rng.multinomial(len(ids), np.ones(len(ids)) / len(ids))[fi]
        out.append((w * v).sum() / w.sum() if w.sum() > 0 else np.nan)
    return C.intervalle(out)


def boot_stat(df, fonction, nb, rng):
    """IC d'une statistique quelconque fonction(df pondéré) par grappes de matchs ; fonction(df, w) -> float."""
    ids = df.fixture_id.unique()
    if len(ids) < 8:
        return None
    fi = df.fixture_id.map({f: i for i, f in enumerate(ids)}).to_numpy()
    out = []
    for _ in range(nb):
        w = rng.multinomial(len(ids), np.ones(len(ids)) / len(ids))[fi].astype(float)
        out.append(fonction(df, w))
    return C.intervalle(out)


def moy_w(v, w):
    v, w = np.asarray(v, float), np.asarray(w, float)
    return (v * w).sum() / w.sum() if w.sum() > 0 else np.nan


def ecart_stratifie(df, col, niveau, w=None):
    """Écart niveau - Normal calculé dans chaque groupe, moyenné avec poids = n (pondéré) du niveau."""
    w = np.ones(len(df)) if w is None else w
    num = den = 0.0
    for g in df.groupe.unique():
        m = (df.groupe == g).to_numpy()
        ml, mn = m & (df.niveau == niveau).to_numpy(), m & (df.niveau == "Normal").to_numpy()
        if w[ml].sum() > 0 and w[mn].sum() > 0:
            d = moy_w(df[col].to_numpy()[ml], w[ml]) - moy_w(df[col].to_numpy()[mn], w[mn])
            num += w[ml].sum() * d
            den += w[ml].sum()
    return num / den if den > 0 else np.nan


def table_calibration(df, col, nb, rng, titre):
    print(f"\n### {titre}")
    print("| groupe | niveau | n joueurs-matchs | n matchs | moyenne | IC 95 % |")
    print("|---|---|---|---|---|---|")
    for g in [x for x in C.GROUPES if x in set(df.groupe)]:
        for niv in ORDRE:
            a = df[(df.groupe == g) & (df.niveau == niv)]
            if a.empty:
                continue
            print(f"| {g} | {niv} | {len(a)} | {a.fixture_id.nunique()} | {a[col].mean():.2f} | {C.fic(boot_moy(a, col, nb, rng), 2)} |")
    # comparabilité du Normal
    nor = df[df.niveau == "Normal"]
    ref = nor.groupby("groupe").size().idxmax() if len(nor) else None
    comparable = True
    print(f"Part en Normal, écart au groupe de référence ({ref}) :")
    for g in [x for x in C.GROUPES if x in set(nor.groupe) and x != ref]:
        sub = nor[nor.groupe.isin([g, ref])]

        def f(d, w, g=g):
            mg, mr = (d.groupe == g).to_numpy(), (d.groupe == ref).to_numpy()
            return moy_w(d[col].to_numpy()[mg], w[mg]) - moy_w(d[col].to_numpy()[mr], w[mr])
        e = f(sub, np.ones(len(sub)))
        ic = boot_stat(sub, f, nb, rng) if sub[sub.groupe == g].fixture_id.nunique() >= 8 else None
        ok = ic is not None and ic[0] <= 0 <= ic[1]
        comparable &= ok
        print(f"- {g} (n {int((sub.groupe == g).sum())}, {sub[sub.groupe == g].fixture_id.nunique()} matchs) : {C.fmt(e, 2)} {C.fic(ic, 2)}"
              f" -> {'comparable' if ok else ('non testable (< 8 matchs)' if ic is None else 'différent')}")
    print(f"Normal comparable entre groupes : {'oui' if comparable else 'non'} -> "
          f"{'regroupement, groupe en covariable' if comparable else 'calibration par groupe'}")
    eff = {}
    print("| écart niveau - Normal | portée | n joueurs-matchs (niveau) | n matchs | estimé | IC 95 % | verdict |")
    print("|---|---|---|---|---|---|---|")
    portees = [("regroupé (groupe en covariable)", list(set(df.groupe)))] if comparable else [(g, [g]) for g in C.GROUPES if g in set(df.groupe)]
    for lab, gs in portees:
        sub = df[df.groupe.isin(gs)]
        for niv in ["Lock", "Intense", "Light", "Give up"]:
            a = sub[sub.niveau == niv]
            if a.empty:
                continue
            e = ecart_stratifie(sub, col, niv)
            ic = boot_stat(sub, lambda d, w, niv=niv: ecart_stratifie(d, col, niv, w), nb, rng)
            vd = C.verdict(e, ic, a.fixture_id.nunique())
            print(f"| {niv} - Normal | {lab} | {len(a)} | {a.fixture_id.nunique()} | {C.fmt(e, 2)} | {C.fic(ic, 2)} | {vd} |")
            if lab.startswith("regroupé") or lab == "v4 ligue":
                eff[niv] = (e, ic)
    return eff, comparable


def part_equipe(B):
    fe = B.groupby(["fixture_id", "team_side"]).fga.sum().rename("fga_eq")
    B = B.merge(fe, left_on=["fixture_id", "team_side"], right_index=True)
    B["part"] = 100 * B.fga / B.fga_eq
    return B


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    graine = int(sys.argv[2]) if len(sys.argv) > 2 else 20261116
    print(f"graine = {graine} ; tirages bootstrap = {nb} ; grappes = matchs ; référence >= {MIN_AUTRES} autres matchs")
    rng = np.random.default_rng(graine)
    F = C.focus()
    print("Libellés bruts de our_focus :", F.our_focus.value_counts().to_dict())
    F["niveau"] = F.our_focus.map(NIVEAUX)
    F = F[F.niveau.notna() & F.groupe.notna() & F.shot_share.notna()]
    echelle = 100.0 if F.shot_share.max() <= 1.0 else 1.0
    F["part_vue"] = F.shot_share * echelle
    print(f"shot_share max {F.shot_share.max():.3f} -> échelle x{echelle:g} ; lignes gardées {len(F)}, matchs {F.fixture_id.nunique()}")
    # 1a/1b : part absolue
    eff_abs, comp_abs = table_calibration(F, "part_vue", nb, rng, "1a-1b. Part de tirs du joueur visé (%), tous nos matchs")
    # 1c : écart à la référence du joueur
    BA = part_equipe(C.box_toutes_saisons())
    BA = BA[(BA.minutes > 0) & BA.groupe.notna()]
    t = BA.groupby(["groupe", "player_id"]).agg(n=("fixture_id", "nunique"), s_part=("part", "sum"))
    cal = F.merge(BA[["fixture_id", "player_id", "groupe", "part"]], on=["fixture_id", "player_id", "groupe"])
    cal = cal.merge(t, left_on=["groupe", "player_id"], right_index=True)
    cal["autres"] = cal.n - 1
    cal = cal[cal.autres >= MIN_AUTRES].copy()
    cal["d_part"] = cal.part - (cal.s_part - cal.part) / cal.autres
    print(f"\n1c. Joueurs visés avec référence (>= {MIN_AUTRES} autres matchs du groupe en base) : {len(cal)} joueurs-matchs, {cal.fixture_id.nunique()} matchs")
    eff_d, comp_d = table_calibration(cal, "d_part", nb, rng, "1c. Δpart du joueur visé (points de %), tous nos matchs") if len(cal) else ({}, False)
    # 2 : application inverse
    M = C.matchs()
    P = C.resume_perimetre(M)
    B = C.box()
    B = B[(B.period == 0)].merge(P[["fixture_id", "groupe", "is_mine"]].rename(columns={"is_mine": "match_mien"}), on="fixture_id")
    B = part_equipe(B)
    B = B[B.minutes > 0]
    calib = eff_d if eff_d.get("Lock", (np.nan,))[0] == eff_d.get("Lock", (np.nan,))[0] and eff_d else eff_abs
    source = "1c (Δpart)" if calib is eff_d else "1a-1b (part absolue)"
    for g in C.GROUPES:
        b0 = B[B.groupe == g]
        if b0.empty:
            continue
        lignes = []
        for pid, a in b0.groupby("player_id"):
            if len(a) < MIN_AUTRES + 1:
                continue
            for i in range(len(a)):
                autres = a.drop(a.index[i])
                perm = rng.permutation(len(autres))
                k = len(autres) // 2
                A_, B_ = autres.iloc[perm[:max(k, 1)]], autres.iloc[perm[max(k, 1):]]
                if len(B_) < 1:
                    continue
                r = a.iloc[i]
                lignes.append(dict(fixture_id=r.fixture_id, team_side=r.team_side, player_id=pid, mien=r.match_mien,
                                   fpm_A=A_.fga.sum() / A_.minutes.sum(), ref_part=B_.part.mean(),
                                   ref_fpm=B_.fga.sum() / B_.minutes.sum(), part=r.part, fpm=r.fga / r.minutes))
        D = pd.DataFrame(lignes)
        if D.empty:
            continue
        D = D[~D.mien]
        D["d_part"], D["d_fpm"] = D.part - D.ref_part, D.fpm - D.ref_fpm
        D["etoile"] = D.groupby(["fixture_id", "team_side"]).fpm_A.rank(ascending=False, method="first") <= 2
        print(f"\n## 2. Application (inféré), groupe {g} : {D.fixture_id.nunique()} matchs d'autres clubs, {len(D)} joueurs-matchs avec référence "
              f"(moitié A pour choisir, moitié B pour la référence)")
        print("| sous-ensemble | n joueurs-matchs | n matchs | Δpart | IC 95 % | Δtirs/min | IC 95 % | verdict |")
        print("|---|---|---|---|---|---|---|---|")
        for lab, a in (("étoiles (2 par équipe-match)", D[D.etoile]), ("témoin : tous", D), ("non-étoiles", D[~D.etoile])):
            ic1, ic2 = boot_moy(a, "d_part", nb, rng), boot_moy(a, "d_fpm", nb, rng)
            print(f"| {lab} | {len(a)} | {a.fixture_id.nunique()} | {a.d_part.mean():+.2f} | {C.fic(ic1, 2)} | {a.d_fpm.mean():+.3f} | {C.fic(ic2, 3)} | "
                  f"{C.verdict(a.d_part.mean(), ic1, a.fixture_id.nunique())} (inféré) |")

        def ecart_et(d, w):
            m = d.etoile.to_numpy()
            return moy_w(d.d_part.to_numpy()[m], w[m]) - moy_w(d.d_part.to_numpy()[~m], w[~m])
        e = ecart_et(D, np.ones(len(D)))
        ic = boot_stat(D, ecart_et, nb, rng)
        print(f"Écart étoiles - non-étoiles (Δpart) : {C.fmt(e, 2)} {C.fic(ic, 2)} ; {C.verdict(e, ic, D.fixture_id.nunique())} (inféré)")
        print(f"Calibration utilisée pour l'inversion : {source} ; écarts niveau - Normal : "
              + ", ".join(f"{k} {C.fmt(v[0], 2)} {C.fic(v[1], 2)}" for k, v in calib.items()))
        cand = {"Normal": 0.0, **{k: v[0] for k, v in calib.items() if k in ("Lock", "Intense", "Give up") and v[0] == v[0]}}
        et = D[D.etoile].copy()
        base = D[~D.etoile].d_part.mean()
        x = (et.d_part - base).to_numpy()
        noms = list(cand)
        mu = np.array([cand[k] for k in noms])
        choix = np.array(noms)[np.abs(x[:, None] - mu[None, :]).argmin(axis=1)] if len(x) else np.array([])
        rep = pd.Series(choix).value_counts(normalize=True).round(2).to_dict() if len(choix) else {}
        print(f"Niveau le plus proche par étoile-match (écart à la moyenne des non-étoiles, n {len(x)}) : {rep} (inféré ; "
              f"l'écart-type individuel est grand devant les écarts entre niveaux, voir 1c)")
    print(f"\nRequêtes exécutées par ce script : {C.NB_REQUETES[0]}")


if __name__ == "__main__":
    main()
