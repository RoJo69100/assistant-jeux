"""Étude C (premier essai, 16/11/2026) : focus défensif adverse INFÉRÉ (règle T3 levée pour cette étude, décision du 13/11).

Mesure, pour un joueur j dans un match m : Δpart = part des tirs (FGA j / FGA de son équipe, en %) dans m moins sa part
moyenne dans ses autres matchs ; Δtirs/min = FGA/min dans m moins FGA/min de ses autres matchs (ratio de sommes).
Référence exigée : au moins MIN_AUTRES autres matchs du même groupe de moteur dans le pool.
1. Calibration : nos matchs (gold.bv_match_opp_focus), Δ selon le focus que NOUS avons posé sur le joueur adverse.
2. Application : matchs des autres clubs ; étoiles = les 2 joueurs de l'équipe en attaque qui prennent le plus de tirs
   par minute dans leurs autres matchs ; Δ des étoiles (résultat « inféré »).
Pools : « périmètre » (box 0 + Q1..Q4 + événements) et, en contrôle, « box 0 » (tous les matchs du groupe avec box 0).
IC 95 % : bootstrap par grappes de matchs (percentiles) ; moins de 8 matchs : pas d'intervalle.
n requis (calibration) : par niveau, n = 2 (1,96 + 0,84)^2 s^2 / d^2 joueurs-matchs, d = écart observé au niveau normal.
Usage : python -I pipelines/etudes/premier_essai_c_focus.py [tirages] [graine]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402,F401

import premier_essai_communs as C  # noqa: E402

MIN_AUTRES = 3


def avec_reference(b0):
    """Ajoute à chaque ligne joueur-match la référence hors du match (part, tirs/min) et le nombre d'autres matchs."""
    t = b0.groupby("player_id").agg(n=("fixture_id", "nunique"), s_part=("part", "sum"), s_fga=("fga", "sum"), s_min=("minutes", "sum"))
    d = b0.merge(t, left_on="player_id", right_index=True)
    d["autres"] = d.n - 1
    with np.errstate(invalid="ignore", divide="ignore"):
        d["ref_part"] = (d.s_part - d.part) / d.autres
        d["ref_fpm"] = (d.s_fga - d.fga) / (d.s_min - d.minutes)
    d["fpm"] = d.fga / d.minutes
    d["d_part"] = d.part - d.ref_part
    d["d_fpm"] = d.fpm - d.ref_fpm
    return d


def moyenne_boot(df, col, nb, rng):
    ids = df.fixture_id.unique()
    if len(ids) < 8:
        return None
    pos = {f: i for i, f in enumerate(ids)}
    fi = df.fixture_id.map(pos).to_numpy()
    v = df[col].to_numpy(float)
    out = []
    for _ in range(nb):
        w = rng.multinomial(len(ids), np.ones(len(ids)) / len(ids))[fi]
        out.append((w * v).sum() / w.sum() if w.sum() > 0 else np.nan)
    return C.intervalle(out)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    graine = int(sys.argv[2]) if len(sys.argv) > 2 else 20261116
    print(f"graine = {graine} ; tirages bootstrap = {nb} ; grappes = matchs ; référence >= {MIN_AUTRES} autres matchs")
    M = C.matchs()
    C.resume_perimetre(M)
    B = C.box()
    F = C.focus()
    print("\nNiveaux de focus présents (nos matchs), par groupe :")
    print(F.groupby(["groupe", "our_focus"]).agg(lignes=("player_id", "size"), matchs=("fixture_id", "nunique")).to_string())
    print("Niveau « lock » présent :", bool(F.our_focus.str.lower().str.contains("lock").any()))
    Mm = M[["fixture_id", "groupe", "is_mine", "perimetre", "p0"]].rename(columns={"is_mine": "match_mien"})
    b0all = B[(B.period == 0) & (B.minutes > 0)].merge(Mm, on="fixture_id")
    fga_eq = B[B.period == 0].groupby(["fixture_id", "team_side"]).fga.sum().rename("fga_eq")
    b0all = b0all.merge(fga_eq, left_on=["fixture_id", "team_side"], right_index=True)
    b0all["part"] = 100 * b0all.fga / b0all.fga_eq
    for g in C.GROUPES:
        for pool in ("périmètre", "box 0"):
            rng = np.random.default_rng(graine)
            b0 = b0all[(b0all.groupe == g) & (b0all.perimetre if pool == "périmètre" else b0all.p0)]
            if b0.empty:
                continue
            d = avec_reference(b0)
            print(f"\n## Groupe {g}, pool {pool} : {b0.fixture_id.nunique()} matchs (dont {b0[b0.match_mien].fixture_id.nunique()} à nous), "
                  f"{b0.player_id.nunique()} joueurs ; joueurs avec >= {MIN_AUTRES + 1} matchs : {int((b0.groupby('player_id').fixture_id.nunique() > MIN_AUTRES).sum())}")
            f = F[F.groupe == g][["fixture_id", "player_id", "our_focus"]]
            cal = d.merge(f, on=["fixture_id", "player_id"])
            print(f"Calibration : {len(cal)} joueurs adverses de nos matchs dans le pool ({cal.fixture_id.nunique()} matchs) ; "
                  f"avec >= {MIN_AUTRES} autres matchs : {int((cal.autres >= MIN_AUTRES).sum())} ; répartition sans filtre : {cal.our_focus.value_counts().to_dict()}")
            cal = cal[cal.autres >= MIN_AUTRES]
            print("| focus posé par nous | n joueurs-matchs | n matchs | Δpart moyen (pts de %) | IC 95 % | Δtirs/min moyen | IC 95 % | verdict |")
            print("|---|---|---|---|---|---|---|---|")
            stats = {}
            for niv, a in cal.groupby("our_focus"):
                ic1 = moyenne_boot(a, "d_part", nb, rng)
                ic2 = moyenne_boot(a, "d_fpm", nb, rng)
                vd = C.verdict(a.d_part.mean(), ic1, a.fixture_id.nunique())
                stats[niv] = (len(a), a.d_part.mean(), a.d_part.var(ddof=1) if len(a) > 1 else np.nan, a.fixture_id.nunique())
                print(f"| {niv} | {len(a)} | {a.fixture_id.nunique()} | {a.d_part.mean():+.2f} | {C.fic(ic1, 2)} | {a.d_fpm.mean():+.3f} | {C.fic(ic2, 3)} | {vd} |")
            if "normal" in stats:
                nn, mn, vn, fn = stats["normal"]
                for niv, (n, m_, v, fm) in stats.items():
                    if niv == "normal":
                        continue
                    diff = m_ - mn
                    if n > 1 and nn > 1 and diff != 0:
                        s2 = ((n - 1) * v + (nn - 1) * vn) / (n + nn - 2)
                        nreq = int(np.ceil(2 * (1.96 + 0.84) ** 2 * s2 / diff ** 2))
                        print(f"Écart {niv} - normal : {diff:+.2f} pts de part (n {n} contre {nn}) ; écart-type commun {np.sqrt(s2):.2f} ; "
                              f"n requis par niveau ≈ {nreq} joueurs-matchs (≈ {int(np.ceil(nreq / max(n / fm, 1e-9)))} matchs à {n / fm:.1f} joueur visé par match)")
                    else:
                        print(f"Écart {niv} - normal : non calculable (n {n} contre {nn})")
            autres = d[~d.match_mien & (d.autres >= MIN_AUTRES)]
            et = autres.sort_values("ref_fpm", ascending=False).groupby(["fixture_id", "team_side"]).head(2)
            nb_eq = d[~d.match_mien].groupby(["fixture_id", "team_side"]).ngroups
            n2 = et.groupby(["fixture_id", "team_side"]).size()
            print(f"\nApplication (inféré) : {nb_eq} équipes-matchs d'autres clubs ; avec au moins une étoile : {len(n2)} ; avec 2 : {int((n2 == 2).sum())}")
            for lab, a in (("étoiles (2 par équipe-match)", et), ("témoin : tous les joueurs avec référence", autres)):
                if a.empty:
                    print(f"{lab} : n 0")
                    continue
                ic1 = moyenne_boot(a, "d_part", nb, rng)
                ic2 = moyenne_boot(a, "d_fpm", nb, rng)
                vd = C.verdict(a.d_part.mean(), ic1, a.fixture_id.nunique())
                print(f"{lab} : n {len(a)} joueurs-matchs, {a.fixture_id.nunique()} matchs ; Δpart {a.d_part.mean():+.2f} {C.fic(ic1, 2)} ; "
                      f"Δtirs/min {a.d_fpm.mean():+.3f} {C.fic(ic2, 3)} ; {vd} (inféré)")
            if len(et):
                q = et.d_part.quantile([0.1, 0.25, 0.5, 0.75, 0.9]).round(2).to_dict()
                print("Δpart des étoiles, quantiles :", q, "; part de Δpart <= -5 pts :", f"{(et.d_part <= -5).mean():.2f}")
    print(f"\nRequêtes exécutées par ce script : {C.NB_REQUETES[0]}")


if __name__ == "__main__":
    main()
