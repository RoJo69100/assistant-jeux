"""Réussite à 3 points de nos tireurs selon la compétence Trois points (relevé du jour ou de la veille), par groupe de moteur.

Mesure : pente de la probabilité de réussite (modèle linéaire de probabilité, moindres carrés) par +10 points de compétence.
IC 95 % : bootstrap par grappes de matchs (percentiles). Variante intra-joueur (compétence et réussite centrées par joueur).
Usage : python -I pipelines/etudes/trois_points_competence.py [tirages] [graine]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # pipelines/ ; python -I ne l'ajoute pas
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from etude_evenements_basketvibe import GROUPES, charger, preparer  # noqa: E402


def pente(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    vx = ((x - x.mean()) ** 2).sum()
    if vx <= 0:
        return np.nan
    return float(((x - x.mean()) * (y - y.mean())).sum() / vx) * 10


def pente_intra(df):
    x = df.comp - df.groupby("player_id").comp.transform("mean")
    y = df.make.astype(float) - df.groupby("player_id").make.transform(lambda s: s.astype(float).mean())
    return pente(x, y) if (x ** 2).sum() > 0 else np.nan


def boot(df, f, B, rng):
    ids = df.fixture_id.unique()
    par = {i: g for i, g in df.groupby("fixture_id")}
    out = []
    for _ in range(B):
        tir = rng.choice(ids, size=len(ids), replace=True)
        d = pd.concat([par[i] for i in tir], ignore_index=True)
        v = f(d)
        if v == v:
            out.append(v)
    if len(out) < B * 0.9:
        return None
    return np.percentile(out, [2.5, 97.5])


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    B = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    graine = int(sys.argv[2]) if len(sys.argv) > 2 else 20261110
    print(f"graine = {graine} ; tirages bootstrap = {B} ; grappes = matchs")
    d = charger()
    T = preparer(d)["tirs"]
    t = T[T.nous & T.trois & T.releve.notna()].copy()
    def comp(r):
        e = r.three_point_exact
        return float(e) if e is not None and pd.notna(e) else float(r.three_point)
    t["comp"] = t.releve.map(comp)
    t["exact"] = t.releve.map(lambda r: r.three_point_exact is not None and pd.notna(r.three_point_exact))
    tous3 = T[T.nous & T.trois]
    print("\n| groupe | tirs à 3 pts nôtres | dont avec relevé | matchs | joueurs | à une décimale | compétence min-max | réussite brute | pente /+10 | IC 95 % | pente intra-joueur /+10 | IC 95 % intra |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for g in GROUPES:
        rng = np.random.default_rng(graine)
        a = t[t.groupe == g]
        n_all = int((tous3.groupe == g).sum())
        nm = a.fixture_id.nunique()
        if len(a) == 0:
            print(f"| {g} | {n_all} | 0 | 0 | 0 | 0 | - | - | - | - | - | - |")
            continue
        p = pente(a.comp, a.make)
        pi = pente_intra(a)
        if nm >= 8:
            ic = boot(a, lambda d_: pente(d_.comp, d_.make), B, rng)
            ici = boot(a, pente_intra, B, rng)
        else:
            ic = ici = None
        f = lambda v: "nan" if v != v else f"{v:+.3f}"  # noqa: E731
        fi = lambda i: "-" if i is None else f"[{i[0]:+.3f} ; {i[1]:+.3f}]"  # noqa: E731
        print(f"| {g} | {n_all} | {len(a)} | {nm} | {a.player_id.nunique()} | {int(a.exact.sum())} | {a.comp.min():.1f}-{a.comp.max():.1f} | "
              f"{a.make.mean():.3f} | {f(p)} | {fi(ic)} | {f(pi)} | {fi(ici)} |")
    print("\nDétail par joueur et groupe (tirs, réussite, compétence moyenne) :")
    det = t.groupby(["groupe", "player_id"]).agg(tirs=("make", "size"), reussite=("make", "mean"), comp=("comp", "mean"),
                                                 comp_min=("comp", "min"), comp_max=("comp", "max")).round(3)
    print(det.to_string())


if __name__ == "__main__":
    main()
