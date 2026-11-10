"""Carte de faisabilité BasketVibe (2026-11-10) : n disponible, n requis, délai, pour chaque question de la demande.

Groupes de moteur ouverts seulement (v4 ligue, v5 amical) pour les questions de match ; v4 amical (fermé) en complément
pour la question 1b, qui le nomme. Lecture seule (executer() de sql.py).
n requis : même méthode que pipelines/etudes/trois_points_competence.py (rapport 2026-11-10) : erreur type supposée
proportionnelle à 1/racine(n), puissance 50 % : n = n0 x (1,96 x ET0 / effet minimal)^2.
Usage : python -I pipelines/etudes/carte_faisabilite.py [tirages] [graine] [coup|tick]
  coup (défaut) : un match compte dans l'intervalle de relevés qui contient son coup d'envoi (heure de Paris).
  tick : un match du jour D compte dans le premier relevé d'un jour > D (variante de contrôle).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # pipelines/ ; python -I ne l'ajoute pas
sys.path.insert(0, str(Path(__file__).resolve().parent))         # pipelines/etudes/
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from etude_evenements_basketvibe import _js, charger, lire, preparer  # noqa: E402
import trois_points_competence as tp  # noqa: E402

AUJ = pd.Timestamp("2026-11-10")
Z = 1.96
MULT_DEF = {0: 0.75, 1: 0.875, 2: 1.0, 3: 1.325, 4: 1.65}  # basketvibe-joueurs/references/06-fatigue-0100.md [M§6.3]


def wilson(k, n):
    if n <= 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + Z ** 2 / n
    c = (p + Z ** 2 / (2 * n)) / den
    h = Z * math.sqrt(p * (1 - p) / n + Z ** 2 / (4 * n ** 2)) / den
    return (max(0.0, c - h), c + h)


def boot(cles, stat, B, rng):
    """Bootstrap par grappes : cles = étiquette de grappe par ligne ; stat(idx) -> float."""
    cles = np.asarray(cles)
    lst = [np.flatnonzero(cles == u) for u in pd.unique(cles)]
    out = []
    for _ in range(B):
        t = rng.integers(0, len(lst), len(lst))
        v = stat(np.concatenate([lst[i] for i in t]))
        if v is not None and np.isfinite(v):
            out.append(v)
    out = np.array(out)
    if len(out) < 0.9 * B:
        return None, float("nan"), len(out)
    return (float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))), float(out.std(ddof=1)), len(out)


def n_req(n0, et0, delta):
    if not np.isfinite(et0) or et0 <= 0:
        return None
    return math.ceil(n0 * (Z * et0 / delta) ** 2)


def fic(ic, f="{:+.3f}"):
    return "-" if ic is None else "[" + f.format(ic[0]) + " ; " + f.format(ic[1]) + "]"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    B = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    graine = int(sys.argv[2]) if len(sys.argv) > 2 else 20261110
    regle = sys.argv[3] if len(sys.argv) > 3 else "coup"
    print(f"graine = {graine} ; tirages bootstrap = {B} ; aujourd'hui = {AUJ.date()} ; règle d'horodatage 1a = {regle}")
    d = charger()
    P = preparer(d)
    M, E, T, R, Q, box = d["matchs"], P["evenements"], P["tirs"], P["reglages"], P["quarts"], d["box"]
    M["jour"] = M.match_day.astype(str).str[:10]
    ko = lire("select fixture_id, kickoff_time from silver.bv_matches")
    M = M.merge(ko, on="fixture_id", how="left")
    M["coup_utc"] = [pd.Timestamp(f"{j} {k or '12:00'}").tz_localize("Europe/Paris").tz_convert("UTC") for j, k in zip(M.jour, M.kickoff_time)]
    mm = M[M.mien].copy()

    # ---------------- Rythme ----------------
    print("\n## 0. Rythme des matchs (nos matchs terminés)")
    v5 = mm[mm.groupe == "v5 amical"].sort_values("jour")
    j0, j1 = pd.Timestamp(v5.jour.min()), pd.Timestamp(v5.jour.max())
    rythme_am = len(v5) / ((j1 - j0).days + 1)
    print(f"- v5 amical : {len(v5)} matchs du {j0.date()} au {j1.date()} -> {rythme_am:.2f} match/jour")
    fx = lire("select match_day, round_number, status from silver.bv_fixtures where is_mine and status = 'scheduled' order by match_day")
    fut = [pd.Timestamp(str(x)[:10]) for x in fx.match_day]
    lg = mm[mm.groupe == "v4 ligue"]
    print(f"- v4 ligue : {len(lg)} matchs à nous terminés ({', '.join(sorted(lg.jour))}) ; {len(fut)} journées programmées du "
          f"{fut[0].date()} au {fut[-1].date()} (silver.bv_fixtures)")

    def delai_am(n_manq):
        return 0 if n_manq <= 0 else math.ceil(n_manq / rythme_am)

    def delai_lg(n_manq, decal=0):
        if n_manq <= 0:
            return 0
        if n_manq > len(fut):
            return None
        return (fut[n_manq - 1] + pd.Timedelta(days=decal) - AUJ).days

    # ---------------- 1a fatigue ----------------
    print("\n## 1a. Fatigue ajoutée : amical v5 contre ligue v4")
    J = lire("select d.day, d.player_id, d.fatigue, d.stamina, d.stamina_exact, r.captured_at from silver.bv_player_daily d "
             "join bronze.raw_pages r on r.id::text = d.capture_id::text "
             "where d.team_id::text = (select team_id::text from silver.bv_my_team)")
    J["day"] = J.day.astype(str).str[:10]
    J["t"] = pd.to_datetime(J.captured_at, utc=True)
    J["fatigue"] = pd.to_numeric(J.fatigue).astype(float)
    J["stam"] = [float(e) if e is not None and pd.notna(e) else float(s) for e, s in zip(J.stamina_exact, J.stamina)]
    b0 = box[(box.period == 0) & box.is_mine & (box.minutes > 0)][["fixture_id", "player_id", "minutes"]]
    b0 = b0.merge(mm[["fixture_id", "groupe", "jour"]], on="fixture_id")
    defs = R[["fixture_id", "player_id", "defense"]] if len(R) else pd.DataFrame(columns=["fixture_id", "player_id", "defense"])
    b0 = b0.merge(defs, on=["fixture_id", "player_id"], how="left")
    b0["mult"] = b0.defense.map(lambda x: MULT_DEF.get(int(x), np.nan) if x is not None and pd.notna(x) else np.nan)
    print(f"- joueurs-matchs à nous sans niveau d'agressivité : {int(b0.mult.isna().sum())} sur {len(b0)} (multiplicateur 1,0 alors)")
    b0["mult"] = b0.mult.fillna(1.0)
    jours = sorted(J.day.unique())
    tj = J.groupby("day").t.max()
    lignes, exclus = [], []
    for k in range(len(jours) - 1):
        a, z = jours[k], jours[k + 1]
        if a < "2026-10-29":
            continue
        if regle == "tick":
            ms = mm[(mm.jour >= a) & (mm.jour < z)]
        else:
            ms = mm[(mm.coup_utc > tj[a]) & (mm.coup_utc <= tj[z])]
        gs = sorted(set(ms.groupe))
        if len(ms) == 0 or any(g not in ("v4 ligue", "v5 amical") for g in gs):
            exclus.append(f"{a}->{z} ({', '.join(f'{r.competition} {r.jour}' for r in ms.itertuples()) or 'aucun match'})")
            continue
        nuits = (pd.Timestamp(z) - pd.Timestamp(a)).days
        J0, J1 = J[J.day == a].set_index("player_id"), J[J.day == z].set_index("player_id")
        bb = b0[b0.fixture_id.isin(ms.fixture_id)]
        for pid in J0.index.intersection(J1.index):
            st = J0.loc[pid, "stam"]
            x = bb[bb.player_id == pid]
            g = (x.minutes * 0.19 * x.mult * (1.5 - 0.008 * st))
            lignes.append({"int": f"{a}->{z}", "nuits": nuits, "pid": pid, "f0": J0.loc[pid, "fatigue"], "f1": J1.loc[pid, "fatigue"],
                           "G_am": float(g[x.groupe == "v5 amical"].sum()), "G_lg": float(g[x.groupe == "v4 ligue"].sum()),
                           "min_am": float(x.minutes[x.groupe == "v5 amical"].sum()), "min_lg": float(x.minutes[x.groupe == "v4 ligue"].sum()),
                           "n_am": int((ms.groupe == "v5 amical").sum()), "n_lg": int((ms.groupe == "v4 ligue").sum())})
    F = pd.DataFrame(lignes)
    F["dF"] = F.f1 - F.f0
    print("- intervalles exclus (coupe, v3 ou v4 amical, ou aucun match) : " + (" ; ".join(exclus) or "aucun"))
    print("\n| intervalle | nuits | amicaux v5 | ligue v4 | joueurs | dF moyen | dF min | dF max | min amical moy. | min ligue moy. | dF moyen joueurs sans minute |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for i, g in F.groupby("int", sort=True):
        z0 = g[(g.min_am == 0) & (g.min_lg == 0)]
        print(f"| {i} | {g.nuits.iloc[0]} | {g.n_am.iloc[0]} | {g.n_lg.iloc[0]} | {len(g)} | {g.dF.mean():+.2f} | {g.dF.min():+.2f} | {g.dF.max():+.2f} | "
              f"{g.min_am.mean():.1f} | {g.min_lg.mean():.1f} | {('%+.2f (n=%d)' % (z0.dF.mean(), len(z0))) if len(z0) else '-'} |")
    ints = sorted(F["int"].unique())
    n_am_tot = int(F.groupby("int").n_am.first().sum())
    n_lg_tot = int(F.groupby("int").n_lg.first().sum())
    print(f"- n : {len(F)} joueurs-intervalles, {len(ints)} intervalles, {n_am_tot} amicaux v5, {n_lg_tot} matchs de ligue v4")

    def ajuste(df, ids):
        """dF = effet fixe par intervalle + beta x f0 x nuits + k_am x G_am + k_lg x G_lg. G = gain de la formule ligue du manuel."""
        cols = [np.asarray(ids) == u for u in pd.unique(ids)]
        X = [c.astype(float) for c in cols] + [df.f0.values * df.nuits.values]
        actifs = []
        for nm, col in (("k_am", df.G_am.values), ("k_lg", df.G_lg.values)):
            if np.abs(col).sum() > 0:
                X.append(col)
                actifs.append(nm)
        X = np.column_stack(X)
        coef, *_ = np.linalg.lstsq(X, df.dF.values, rcond=None)
        res = {"k_am": float("nan"), "k_lg": float("nan")}
        for j, nm in enumerate(actifs):
            res[nm] = float(coef[len(cols) + 1 + j])
        res["beta"] = float(coef[len(cols)])
        return res

    est = ajuste(F, F["int"].values)
    rng = np.random.default_rng(graine)
    tir = {"k_am": [], "k_lg": [], "D": []}
    par = {i: F[F["int"] == i] for i in ints}
    for _ in range(B):
        t = rng.integers(0, len(ints), len(ints))
        dd = pd.concat([par[ints[i]] for i in t], ignore_index=True)
        ids = np.concatenate([[f"{n}_{ints[i]}"] * len(par[ints[i]]) for n, i in enumerate(t)])
        r = ajuste(dd, ids)
        for nm in ("k_am", "k_lg"):
            if np.isfinite(r[nm]):
                tir[nm].append(r[nm])
        if np.isfinite(r["k_am"]) and np.isfinite(r["k_lg"]):
            tir["D"].append(r["k_lg"] - r["k_am"])
    est["D"] = est["k_lg"] - est["k_am"]
    g10 = 10 * 0.19 * 1.0 * (1.5 - 0.008 * F.groupby("pid").first().pipe(lambda x: J[J.player_id.isin(x.index)].stam.mean()))
    print(f"- estimé : k_am = {est['k_am']:+.3f}, k_lg = {est['k_lg']:+.3f}, D = k_lg - k_am = {est['D']:+.3f}, beta (f0 x nuits) = {est['beta']:+.4f}")
    print(f"  (k = fraction du gain de la formule ligue du manuel ; le manuel attend k_am ~ 0,1 et k_lg ~ 1 ; "
          f"repère : formule ligue, défense équilibrée, endurance moyenne de l'effectif = {g10:.2f} point de fatigue par 10 minutes)")
    res1a = {}
    for nm, n_m in (("k_am", n_am_tot), ("k_lg", n_lg_tot), ("D", n_lg_tot)):
        v = np.array(tir[nm])
        et = float(v.std(ddof=1)) if len(v) > 10 else float("nan")
        ic = (float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))) if len(v) >= 0.9 * B else None
        res1a[nm] = (et, ic, len(v))
        aff = fic(ic) if n_m >= 8 else "- (< 8 matchs)"
        print(f"  {nm} : tirages valides {len(v)}/{B}, ET bootstrap {et:.3f}, IC 95 % {aff}")
    print(f"  k_am en points de fatigue par 10 minutes d'amical (repère ci-dessus) : {est['k_am'] * g10:+.3f}, IC "
          f"{fic(tuple(x * g10 for x in res1a['k_am'][1]) if res1a['k_am'][1] else None)}")
    nr_am = n_req(n_am_tot, res1a["k_am"][0], 0.10)
    nr_lg = n_req(n_lg_tot, res1a["D"][0], 0.25)
    print(f"- n requis : k_am (effet minimal 0,10) -> {nr_am} amicaux v5 ; D (effet minimal 0,25) -> {nr_lg} matchs de ligue v4 "
          f"(ET de planification tirée de {n_lg_tot} matchs < 8 : approximation fragile) ; plancher 8")
    lg_req = max(8, nr_lg or 8)
    lg_manq = lg_req - n_lg_tot
    print(f"- délai ligue : {lg_manq} matchs de ligue de plus -> {delai_lg(lg_manq, 1)} jours (dernier match requis + relevé du lendemain ; "
          f"None = au-delà de la saison, {len(fut)} journées restantes)")

    # ---------------- 1b blessures ----------------
    print("\n## 1b. Blessures (événements injury) par minutes jouées, deux équipes")
    bt = box[(box.period == 0) & (box.minutes > 0)][["fixture_id", "player_id", "minutes"]].merge(M[["fixture_id", "groupe"]], on="fixture_id")
    avec_pbp = set(E.fixture_id.unique())
    inj = E[E.kind == "injury"][["fixture_id", "player_id", "groupe"]]
    print("| groupe | matchs (box + play-by-play) | joueurs-matchs | minutes | blessures | par 1000 min | Wilson 95 % /1000 min | par joueur-match | Wilson 95 % |")
    print("|---|---|---|---|---|---|---|---|---|")
    taux = {}
    for g in ("v4 ligue", "v5 amical", "v4 amical"):
        x = bt[(bt.groupe == g) & bt.fixture_id.isin(avec_pbp)]
        ij = inj[(inj.groupe == g) & inj.fixture_id.isin(x.fixture_id)]
        mn = float(x.minutes.sum())
        k = len(ij)
        pm = len(x)
        kpm = len(ij.drop_duplicates(["fixture_id", "player_id"]))
        w = wilson(k, mn)
        wp = wilson(kpm, pm)
        taux[g] = (x, ij, k, mn, pm, kpm)
        print(f"| {g} | {x.fixture_id.nunique()} | {pm} | {mn:.0f} | {k} | {1000 * k / mn:.3f} | [{1000 * w[0]:.3f} ; {1000 * w[1]:.3f}] | "
              f"{kpm / pm:.4f} | [{wp[0]:.4f} ; {wp[1]:.4f}] |")
    print("  (Wilson par minute : chaque minute-joueur traitée comme un essai ; approximation d'un taux rare)")
    rng = np.random.default_rng(graine)
    xs = {}
    for g in ("v4 ligue", "v5 amical"):
        x, ij, *_ = taux[g]
        par_m = x.groupby("fixture_id").minutes.sum()
        kij = ij.groupby("fixture_id").size().reindex(par_m.index, fill_value=0)
        xs[g] = (par_m.values, kij.values)
    diffs = []
    for _ in range(B):
        r = []
        for g in ("v5 amical", "v4 ligue"):
            mnv, kv = xs[g]
            t = rng.integers(0, len(mnv), len(mnv))
            r.append(1000 * kv[t].sum() / mnv[t].sum())
        diffs.append(r[0] - r[1])
    diffs = np.array(diffs)
    _, _, k_l, mn_l, pm_l, _ = taux["v4 ligue"]
    _, _, k_a, mn_a, pm_a, _ = taux["v5 amical"]
    nm_l = taux["v4 ligue"][0].fixture_id.nunique()
    print(f"- différence v5 amical - v4 ligue : {1000 * (k_a / mn_a - k_l / mn_l):+.3f} /1000 min, IC 95 % "
          f"[{np.percentile(diffs, 2.5):+.3f} ; {np.percentile(diffs, 97.5):+.3f}] (bootstrap par matchs, chaque groupe à part, {B} tirages)")
    print(f"- matchs de ligue v4 avec au moins une blessure : {int((xs['v4 ligue'][1] > 0).sum())} sur {nm_l}")
    p_l = k_l / mn_l
    p_delta = 0.25 * p_l
    n_min = math.ceil(Z ** 2 * (1 - p_delta) / p_delta)
    n_m_dispo = taux["v5 amical"][0].fixture_id.nunique()
    min_par_match = mn_a / n_m_dispo
    n_m_req = math.ceil(n_min / min_par_match)
    print(f"- effet minimal : taux amical >= 25 % du taux ligue = {1000 * p_delta:.3f} /1000 min ; avec 0 blessure, la borne haute de Wilson "
          f"passe sous ce seuil à partir de {n_min} minutes-joueur, soit {n_m_req} amicaux v5 à {min_par_match:.0f} min par match "
          f"(dispo {n_m_dispo}) ; délai {delai_am(n_m_req - n_m_dispo)} jours")
    for g in ("v5 amical", "v4 amical"):
        wu = wilson(taux[g][2], taux[g][3])[1]
        print(f"- aujourd'hui : borne haute {g} = {1000 * wu:.3f} /1000 min = {wu / p_l:.0%} du taux ligue v4 observé")
    nos = lire("select count(*) n, count(injury_return_on) blesses, min(day) d0, max(day) d1 from silver.bv_player_daily "
               "where team_id::text = (select team_id::text from silver.bv_my_team) and day >= '2026-10-28'")
    print(f"- recoupement relevés quotidiens (nos joueurs, depuis le 28/10) : {nos.n.iloc[0]} lignes, {nos.blesses.iloc[0]} avec date de retour de blessure")

    # ---------------- 1c focus défensif adverse ----------------
    print("\n## 1c. Focus défensif adverse")
    moi = str(d["moi"])
    tac = d["tactiques"]
    n_adv = int((tac.team_id.astype(str) != moi).sum())
    print(f"- réglages utilisés vus côté adversaire (silver.bv_match_tactics, team_id différent du nôtre) : {n_adv} sur {len(tac)}")
    rng = np.random.default_rng(graine)

    def sim_cible(df_tirs):
        """Cible tirée au hasard parmi les 5 plus gros tireurs du camp, à chaque tirage ; bootstrap des camps-matchs."""
        cles = df_tirs.cle.values
        lst = {u: np.flatnonzero(cles == u) for u in pd.unique(cles)}
        top = {u: df_tirs.iloc[ix].player_id.value_counts().index[:5].tolist() for u, ix in lst.items()}
        pid = df_tirs.player_id.values
        mk = df_tirs.make.values.astype(float)
        us = list(lst)
        out = []
        for _ in range(B):
            t = rng.integers(0, len(us), len(us))
            a_m = a_n = o_m = o_n = 0.0
            for i in t:
                u = us[i]
                ix = lst[u]
                c = top[u][rng.integers(0, len(top[u]))]
                s = pid[ix] == c
                a_m += mk[ix][s].sum()
                a_n += s.sum()
                o_m += mk[ix][~s].sum()
                o_n += (~s).sum()
            if a_n > 0 and o_n > 0:
                out.append(a_m / a_n - o_m / o_n)
        return float(np.std(out, ddof=1))

    t5 = T[T.mien & T.nous & (T.groupe == "v5 amical")].copy().reset_index(drop=True)
    t5["cle"] = t5.fixture_id.astype(str)
    et5 = sim_cible(t5)
    n5 = t5.cle.nunique()
    nr5 = n_req(n5, et5, 0.05)
    tl = T[T.groupe == "v4 ligue"].copy().reset_index(drop=True)
    tl["cle"] = tl.fixture_id.astype(str) + "_" + tl.team_side.astype(str)
    etl = sim_cible(tl)
    nl = tl.cle.nunique()
    nrl = n_req(nl, etl, 0.05)
    print(f"- planification (effet minimal 5 pts de réussite aux tirs du joueur ciblé) : v5 amical ET {et5:.3f} sur {n5} matchs -> {nr5} matchs ; "
          f"v4 ligue ET {etl:.3f} sur {nl} camps-matchs (deux camps) -> {nrl} de nos matchs")
    print(f"  délai si l'export arrivait dès aujourd'hui : v5 {delai_am(nr5)} jours ; v4 ligue {delai_lg(nrl - len(lg))} "
          f"(None = au-delà de la saison : {len(lg)} joués + {len(fut)} journées restantes)")

    # ---------------- 1d E1 à E5 ----------------
    print("\n## 1d. Réglages E1 à E5 (amicaux v5)")
    exp = mm[(mm.groupe == "v5 amical") & (mm.jour >= "2026-11-10")]
    print(f"- amicaux v5 joués depuis le début de la file (2026-11-10) : {len(exp)}")
    tv = tac[tac.fixture_id.isin(v5.fixture_id) & (tac.team_id.astype(str) == moi)]
    print(f"- réglages utilisés en base pour {tv.fixture_id.nunique()} des {len(v5)} amicaux v5 (observationnel, pas une expérience) :")
    for r in tv.itertuples():
        dirs = _js(r.player_directives) or []
        foc = _js(r.defensive_focus) or []
        print(f"  {str(r.fixture_id)[:8]} : agressivité (crans) {sorted({x.get('defense_tier') for x in dirs})} ; zones (area_step) "
              f"{sorted({x.get('area_step') for x in foc})} ; joueurs au tir cran 4 {sum(1 for x in dirs if x.get('shot_tier') == 4)} ; "
              f"joueurs au focus offensif cran 4 {sum(1 for x in dirs if x.get('offensive_focus_tier') == 4)}")
    rng = np.random.default_rng(graine)
    adv = T[T.mien & ~T.nous & (T.groupe == "v5 amical")].reset_index(drop=True)
    mk = adv.make.values.astype(float)
    tr = adv.trois.values.astype(bool)
    n0 = adv.fixture_id.nunique()
    _, et_e1, _ = boot(adv.fixture_id.values, lambda ix: mk[ix].mean(), B, rng)
    sig1 = et_e1 * math.sqrt(n0)
    _, et_e5, _ = boot(adv.fixture_id.values, lambda ix: mk[ix][~tr[ix]].mean(), B, rng)
    sig5 = et_e5 * math.sqrt(n0)
    narm1 = math.ceil(2 * (Z * sig1 / 0.05) ** 2)
    narm5 = math.ceil(2 * (Z * sig5 / 0.05) ** 2)
    print(f"- E1 (réussite adverse aux tirs, effet minimal 5 pts) : {len(adv)} tirs adverses, {n0} matchs, réussite {mk.mean():.3f}, "
          f"ET {et_e1:.4f}, sigma match {sig1:.3f} -> {narm1} amicaux par niveau, {2 * narm1} au total")
    print(f"- E5 (réussite adverse à 2 points, effet minimal 5 pts) : {int((~tr).sum())} tirs, ET {et_e5:.4f}, sigma match {sig5:.3f} "
          f"-> {narm5} amicaux par zone, {3 * narm5} au total")
    nous3 = T[T.mien & T.nous & T.trois & (T.groupe == "v5 amical")].groupby("fixture_id").size().reindex(v5.fixture_id, fill_value=0)
    s2 = float(nous3.std(ddof=1))
    narm2 = math.ceil(2 * (Z * s2 / 5) ** 2)
    print(f"- E2 (nos tirs à 3 points tentés par match, effet minimal 5 tirs) : moyenne {nous3.mean():.1f}, écart type {s2:.2f} sur {len(nous3)} matchs "
          f"-> {narm2} amicaux par niveau (A et B joués tous deux), {2 * narm2} au total")
    qq = Q.merge(M[["fixture_id", "groupe", "my_side"]], on="fixture_id")
    qq = qq[(qq.groupe == "v5 amical") & (qq.side == qq.my_side) & (qq.period <= 4)]
    pq = qq.explode("joueurs").rename(columns={"joueurs": "player_id"}).dropna(subset=["player_id"])
    sh = T[T.nous & (T.groupe == "v5 amical")].groupby(["fixture_id", "period", "player_id"]).size().rename("tirs").reset_index()
    pq = pq.merge(sh, on=["fixture_id", "period", "player_id"], how="left").fillna({"tirs": 0})
    m_pq, s_pq, n_pq = float(pq.tirs.mean()), float(pq.tirs.std(ddof=1)), len(pq)
    dE3 = 0.30 * m_pq
    sigA = s_pq / 2.0
    narm3 = math.ceil(2 * (Z * sigA / dE3) ** 2)
    print(f"- E3 (tirs par quart du joueur désigné, effet minimal +30 % = {dE3:.2f} tir) : {n_pq} joueurs-quarts, {pq.fixture_id.nunique()} matchs, "
          f"moyenne {m_pq:.2f}, écart type {s_pq:.2f} -> {narm3} amicaux par niveau, {2 * narm3} au total (4 quarts par match, quarts supposés indépendants)")
    T3 = T[T.nous & T.trois & T.releve.notna() & (T.groupe == "v5 amical")].copy()
    T3["comp"] = T3.releve.map(lambda r: float(r.three_point_exact) if r.three_point_exact is not None and pd.notna(r.three_point_exact) else float(r.three_point))
    rng = np.random.default_rng(graine)
    ic4 = tp.boot(T3, lambda d_: tp.pente(d_.comp, d_.make), B, rng)
    p4 = tp.pente(T3.comp, T3.make)
    et4 = (ic4[1] - ic4[0]) / 3.92
    n4m = T3.fixture_id.nunique()
    nr4 = n_req(n4m, et4, 0.03)
    print(f"- E4 (pente réussite à 3 pts / +10 de compétence, effet minimal 3 pts) : {len(T3)} tirs, {n4m} matchs, pente {p4:+.3f}, "
          f"IC {fic(tuple(ic4))}, ET {et4:.4f} -> {nr4} matchs")
    print(f"- délais à 1 amical/jour, chaque expérience seule : E1 {delai_am(2 * narm1)} j ; E5 {delai_am(3 * narm5)} j ; "
          f"E2 {delai_am(2 * narm2)} j ; E3 {delai_am(2 * narm3)} j ; E4 {delai_am(nr4 - n4m)} j ; "
          f"file complète E1+E5+E2+E3 {delai_am(2 * narm1 + 3 * narm5 + 2 * narm2 + 2 * narm3)} j")

    # ---------------- 2 marché ----------------
    print("\n## 2. Prix d'un joueur (gold.bv_transfer_history, ventes hors agents libres)")
    H = lire("select sold_on, position, age, ps, fee, was_free_agent from gold.bv_transfer_history where ps is not null and fee > 0")
    H = H[~H.was_free_agent.astype(str).str.lower().isin(["true", "t", "1"])].copy()
    n_sans_poste = int(H.position.isna().sum())
    H = H[H.position.notna()].copy()
    for c in ("age", "ps", "fee"):
        H[c] = pd.to_numeric(H[c]).astype(float)
    H["sold_on"] = H.sold_on.astype(str).str[:10]
    H["per"] = np.where(H.sold_on <= "2026-10-26", "saison 1 (<= 26/10)", "saison 2 (>= 27/10)")
    print(f"- postes : {H.position.value_counts().to_dict()} ; ventes sans poste écartées : {n_sans_poste} ; prix {H.fee.min():.0f}-{H.fee.max():.0f}")
    rng = np.random.default_rng(graine)
    for per, h in H.groupby("per"):
        h = h.reset_index(drop=True)
        pos = sorted(h.position.unique())
        ref = "PG" if "PG" in pos else pos[0]
        autres = [p for p in pos if p != ref]
        X = np.column_stack([np.ones(len(h)), h.ps.values, h.age.values] + [(h.position.values == p).astype(float) for p in autres])
        y = np.log(h.fee.values)
        noms = ["const", "ps", "age"] + autres

        def fit(ix):
            c, *_ = np.linalg.lstsq(X[ix], y[ix], rcond=None)
            return c
        c0 = fit(np.arange(len(h)))
        r2 = 1 - ((y - X @ c0) ** 2).sum() / ((y - y.mean()) ** 2).sum()
        cles = h.sold_on.values
        lst = [np.flatnonzero(cles == u) for u in pd.unique(cles)]
        tirs_c = np.array([fit(np.concatenate([lst[i] for i in rng.integers(0, len(lst), len(lst))])) for _ in range(B)])
        njours = len(lst)
        rythme = len(h) / njours
        print(f"\n### {per} : {len(h)} ventes, {njours} jours de vente ({rythme:.1f} ventes/jour), R2 = {r2:.2f}, "
              f"âge {h.age.min():.0f}-{h.age.max():.0f}, PS {h.ps.min():.0f}-{h.ps.max():.0f}, référence de poste {ref}")
        print("| facteur | effet sur le prix | IC 95 % | ET (log) | n requis (effet minimal 10 %) | délai (jours de vente) |")
        print("|---|---|---|---|---|---|")
        for j, nm in enumerate(noms):
            if nm == "const":
                continue
            sc = 5.0 if nm == "ps" else 1.0
            lo, hi = np.percentile(tirs_c[:, j] * sc, [2.5, 97.5])
            et = float((tirs_c[:, j] * sc).std(ddof=1))
            nr = n_req(len(h), et, math.log(1.1))
            dl = 0 if (lo > 0 or hi < 0) or nr <= len(h) else math.ceil((nr - len(h)) / rythme)
            lab = {"ps": "+5 PS", "age": "+1 an"}.get(nm, f"{nm} contre {ref}")
            print(f"| {lab} | {math.expm1(c0[j] * sc):+.1%} | [{math.expm1(lo):+.1%} ; {math.expm1(hi):+.1%}] | {et:.3f} | {nr} | {dl} |")

    # ---------------- 3 meilleures équipes ----------------
    print("\n## 3. Meilleures équipes (dernier classement, saison en cours = v4 ligue)")
    S = lire("select day, team, wins, losses, club_strength, is_human from silver.bv_standings_weekly "
             "where day = (select max(day) from silver.bv_standings_weekly) and season_id = "
             "(select season_id from silver.bv_standings_weekly order by day desc limit 1)")
    for c in ("wins", "losses", "club_strength"):
        S[c] = pd.to_numeric(S[c]).astype(float)
    S = S[(S.wins + S.losses) > 0].reset_index(drop=True)
    S["wp"] = S.wins / (S.wins + S.losses)
    zs = (S.club_strength - S.club_strength.mean()) / S.club_strength.std(ddof=1)
    zv, wv = zs.values, S.wp.values

    def pente_z(ix):
        x = zv[ix]
        y = wv[ix]
        vx = ((x - x.mean()) ** 2).sum()
        return float(((x - x.mean()) * (y - y.mean())).sum() / vx) if vx > 0 else float("nan")
    rng = np.random.default_rng(graine)
    ic3, et3, _ = boot(np.arange(len(S)), pente_z, B, rng)
    tm = float((S.wins + S.losses).sum())
    rounds = float((S.wins + S.losses).mean())
    nr3 = n_req(rounds, et3, 0.10)
    print(f"- classement du {str(S.day.iloc[0])[:10]} : {len(S)} équipes, {tm:.0f} équipes-matchs ({rounds:.2f} matchs par équipe), "
          f"force min-max {S.club_strength.min():.1f}-{S.club_strength.max():.1f}, écart type {S.club_strength.std(ddof=1):.2f}")
    print(f"- pente part de victoires / +1 écart type de force : {pente_z(np.arange(len(S))):+.3f}, IC 95 % {fic(ic3)} (bootstrap par équipes, {B} tirages), "
          f"ET {et3:.3f} -> {nr3} matchs par équipe pour un effet minimal de 10 pts (approximation : ET ~ 1/racine des matchs)")
    tp_ = lire("select count(*) n, count(distinct team) equipes, max(matches) mmax from gold.bv_league_top_players")
    print(f"- gold.bv_league_top_players : {tp_.n.iloc[0]} lignes, {tp_.equipes.iloc[0]} équipes, {tp_.mmax.iloc[0]} matchs au plus")
    ov = lire("select count(distinct team_id) equipes from silver.bv_player_overview")
    print(f"- équipes dont les compétences des joueurs sont en base (silver.bv_player_overview) : {ov.equipes.iloc[0]}")

    # ---------------- 4 finances ----------------
    print("\n## 4. Finances")
    RS = lire("select sold_on, bought_for, resale_net_margin from gold.bv_transfer_history where is_resale and bought_for > 0")
    for c in ("bought_for", "resale_net_margin"):
        RS[c] = pd.to_numeric(RS[c]).astype(float)
    RS["rdt"] = RS.resale_net_margin / RS.bought_for
    rv = RS.rdt.values
    rng = np.random.default_rng(graine)
    ic4r, et4r, _ = boot(RS.sold_on.astype(str).values, lambda ix: float(np.median(rv[ix])), B, rng)
    kg = int((RS.resale_net_margin > 0).sum())
    wg = wilson(kg, len(RS))
    print(f"- reventes du marché : {len(RS)} (sur {RS.sold_on.astype(str).nunique()} jours), achat {RS.bought_for.min():.0f}-{RS.bought_for.max():.0f} ; "
          f"rendement net médian {np.median(rv):+.1%} IC {fic(ic4r, '{:+.1%}')} (bootstrap par jour), moyenne {rv.mean():+.1%} (tirée par les achats à bas prix) ; "
          f"part en gain {kg}/{len(RS)} = {kg / len(RS):.1%} Wilson [{wg[0]:.1%} ; {wg[1]:.1%}] ; n requis médiane (effet minimal 10 pts) {n_req(len(RS), et4r, 0.10)}")
    fs = lire("select season_index, league_tickets, friendlies, cups, sponsor, rewards, transfers_in, transfers_out, salaries, personnel, academy, season_balance "
              "from silver.bv_finance_seasons order by season_index")
    print("- notre club, par saison (silver.bv_finance_seasons) :")
    print(fs.to_string(index=False))
    fw = lire("select count(*) n from silver.bv_finance_weekly")
    print(f"- semaines financières de notre club : {fw.n.iloc[0]} ; une seule équipe observée")

    # ---------------- 5 entraînement, personnel, académie ----------------
    print("\n## 5. Entraînement, personnel, académie")
    G = lire("select player_id, age, week, skill, training_primary, training_secondary, gain from gold.bv_training_gains_exact where gain is not null")
    G["gain"] = pd.to_numeric(G.gain).astype(float)
    G["role"] = np.where(G.skill == G.training_primary, "principal", np.where(G.skill == G.training_secondary, "secondaire", "autre"))
    print(G.groupby("role").gain.agg(["size", "mean", "std"]).round(3).to_string())
    print(f"- semaines avec gain : {sorted(G.week.astype(str).unique())}")
    prin = G[G.role.isin(["principal", "secondaire"])].reset_index(drop=True)
    gv = prin.gain.values
    isp = (prin.role == "principal").values

    def dif(ix):
        a, b = gv[ix][isp[ix]], gv[ix][~isp[ix]]
        return float(a.mean() - b.mean()) if len(a) and len(b) else float("nan")
    rng = np.random.default_rng(graine)
    ic5, et5b, _ = boot(prin.player_id.astype(str).values, dif, B, rng)
    nsem = G.week.astype(str).nunique()
    nr5b = n_req(nsem, et5b, 0.2)
    print(f"- principal - secondaire : {dif(np.arange(len(prin))):+.3f} par semaine, IC {fic(ic5)} (bootstrap par joueurs, {B} tirages), "
          f"{prin.player_id.nunique()} joueurs, {nsem} semaines ; n requis (effet minimal 0,2 point) {nr5b} semaines")
    pw = lire("select count(*) n, count(distinct (doctors, physios, psychologists, marketers)) configs, max(week) derniere from silver.bv_personnel_weekly")
    aw = lire("select count(*) n, count(distinct weekly_investment) niveaux, max(week) derniere from silver.bv_academy_weekly")
    print(f"- personnel : {pw.n.iloc[0]} semaines, {pw.configs.iloc[0]} configurations, dernière semaine {pw.derniere.iloc[0]}")
    print(f"- académie : {aw.n.iloc[0]} semaines, {aw.niveaux.iloc[0]} niveau(x) d'investissement, dernière semaine {aw.derniere.iloc[0]}")


if __name__ == "__main__":
    main()
