"""Calculs de l'étude des événements BasketVibe (huit chiffres) : effet, intervalle par rééchantillonnage des matchs, n requis, verdict.

Critères : docs/refonte-v3/etude-evenements-basketvibe.md, § 2 (commit 4d63ea8), écrits avant ces calculs. Lecture seule.
Usage : python -I pipelines/etude_evenements_basketvibe.py calculs
Tests : pipelines/test_etude_evenements.py
"""
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import etude_evenements_basketvibe as base  # noqa: E402

GROUPES = ["v3 ligue", "v4 ligue", "v4 coupe", "v4 amical", "v5 amical"]  # le seul amical v3 (1 match) est écarté
B = 2000
Z_BETA, Z_ALPHA = 0.8416, 1.9600
MIN_MATCHS = 8
RNG = np.random.default_rng(20261109)


# ---------- rééchantillonnage par matchs ----------
def boot(A, f, b=B, rng=None):
    """A : matrice (matchs × k) de sommes par match ; f : vecteur de sommes → statistique. Renvoie (estimation, bas, haut, écart-type)
    ou None sous MIN_MATCHS matchs. Les matchs sont rééchantillonnés avec remise : des tirs d'un même match ne sont jamais indépendants."""
    rng = rng or RNG
    A = np.asarray(A, dtype=float)
    n = A.shape[0]
    if n < MIN_MATCHS:
        return None
    est = f(A.sum(axis=0))
    idx = rng.integers(0, n, size=(b, n))
    comptes = np.stack([np.bincount(r, minlength=n) for r in idx])
    vals = np.array([f(s) for s in comptes @ A])
    vals = vals[np.isfinite(vals)]
    if len(vals) < b // 2 or not math.isfinite(est):
        return None
    lo, hi = np.percentile(vals, [2.5, 97.5])
    return float(est), float(lo), float(hi), float(vals.std(ddof=1))


def n_requis(n, sd, delta):
    """Événements nécessaires pour que l'erreur-type permette de voir l'effet minimal : n × (sd × (1,96 + 0,84) / delta)²."""
    return None if not (sd and delta and n) else math.ceil(n * (sd * (Z_ALPHA + Z_BETA) / delta) ** 2)


def pente(S):
    n, sx, sy, sxy, sxx = S[:5]
    d = n * sxx - sx * sx
    return (n * sxy - sx * sy) / d if d > 1e-12 else math.nan


def somme_par_match(df, matchs_col, cols):
    return df.groupby(matchs_col)[cols].sum().to_numpy()


# ---------- verdicts (règles du § 2.1) ----------
def v_valeur(r, annonce, delta, ident=True):
    """Valeur annoncée unique : conforme / en écart / non identifiable."""
    if r is None or not ident:
        return "non identifiable"
    _, lo, hi, _ = r
    if annonce < lo or annonce > hi:
        return "en écart"
    return "conforme" if (hi - lo) / 2 <= delta else "non identifiable"


def v_bande(r, a, b, delta, ident=True):
    """Valeur annoncée sous forme de bande [a ; b] : conforme si l'intervalle y tient (et assez précis), en écart s'il est hors de la bande."""
    if r is None or not ident:
        return "non identifiable"
    _, lo, hi, _ = r
    if hi < a or lo > b:
        return "en écart"
    return "conforme" if (lo >= a and hi <= b and (hi - lo) / 2 <= delta) else "non identifiable"


def v_positif(r, delta, ident=True):
    """Annoncé : pente positive. Conforme si l'intervalle est au-dessus de 0 et précis ; en écart s'il est au-dessous de 0 ou dans ±delta."""
    if r is None or not ident:
        return "non identifiable"
    _, lo, hi, _ = r
    if hi < 0 or (lo > -delta and hi < delta and (hi - lo) / 2 <= delta):
        return "en écart"
    return "conforme" if (lo > 0 and (hi - lo) / 2 <= delta) else "non identifiable"


def fmt(r, nd=2, unite=""):
    return "—" if r is None else f"{r[0]:.{nd}f} [{r[1]:.{nd}f} ; {r[2]:.{nd}f}]{unite}"


# ---------- mesure 1 : réussite selon le type et la compétence ----------
COMP = {"3": ("three_point", "two_point"), "cercle": ("two_point", "three_point"), "mi": ("two_point", "three_point")}


def competence(releve, nom):
    ex = releve.get(nom + "_exact")
    return float(ex) if ex is not None and ex == ex else float(releve[nom])


def classer_cercle(T):
    """Choisit Y0 (pas de 10, de 100 à 400) sur les tirs à 2 étiquetés, sans la réussite ; classe les non étiquetés. Renvoie (Y0, exactitude)."""
    e = T[~T.trois & T.type2.notna() & T.shot_y.notna()]
    y = pd.to_numeric(e.shot_y)
    meilleur = max(((y0, float(((y < y0) == (e.type2 == "cercle")).mean())) for y0 in range(100, 401, 10)), key=lambda t: t[1])
    return meilleur


def mesure1(P):
    T = P["tirs"]
    T = T[T.nous & T.releve.notna()].copy()
    T["shot_y"] = pd.to_numeric(T.shot_y)
    y0, exact = classer_cercle(P["tirs"])
    sortie = [f"Classement des tirs à 2 non étiquetés par `shot_y` : seuil Y0 = {y0}, exactitude sur les tirs étiquetés = {exact * 100:.1f} % "
              f"({'retenu' if exact >= 0.85 else 'REJETÉ : tirs non étiquetés exclus'})."]
    cl = np.where(T.trois, "3", np.where(T.type2.notna(), T.type2, np.where(exact >= 0.85, np.where(T.shot_y < y0, "cercle", "mi"), None)))
    T["type"] = cl
    lignes = []
    for g in GROUPES:
        for typ in ("cercle", "mi", "3"):
            a = T[(T.groupe == g) & (T.type == typ)]
            nomme, autre = COMP[typ]
            ident = len(a) >= 150 and a.fixture_id.nunique() >= MIN_MATCHS
            if len(a) < 5:
                lignes.append([g, typ, len(a), a.fixture_id.nunique(), "—", "—", "—", "non identifiable"])
                continue
            res = {}
            for lab, comp in (("nommée", nomme), ("non nommée", autre)):
                x = a.releve.map(lambda r: competence(r, comp)) / 10
                d = pd.DataFrame({"m": a.fixture_id.values, "n": 1.0, "x": x.values, "y": a.make.astype(float).values * 100})
                d["xy"], d["xx"] = d.x * d.y, d.x * d.x
                A = somme_par_match(d, "m", ["n", "x", "y", "xy", "xx"])
                res[lab] = boot(A, pente)
            vn = v_positif(res["nommée"], 2.0, ident)
            vo = v_valeur(res["non nommée"], 0.0, 2.0, ident)
            nreq = n_requis(len(a), res["nommée"][3], 2.0) if res["nommée"] else None
            lignes.append([g, typ, len(a), a.fixture_id.nunique(), fmt(res["nommée"]), fmt(res["non nommée"]), nreq if nreq else "—",
                           f"nommée : {vn} ; non nommée : {vo}"])
    sortie.append(base.md(pd.DataFrame(lignes, columns=["groupe", "type de tir", "tirs", "matchs", "pente compétence nommée (points / +10)",
                                                         "pente non nommée (points / +10)", "n requis (tirs)", "verdict"]), index=False))
    return "\n\n".join(sortie)


# ---------- mesure 2 : fautes sur tir selon l'agressivité ----------
def mesure2(P):
    E, R, Q = P["evenements"], P["reglages"], P["quarts"]
    M = E[["fixture_id", "groupe", "my_side"]].drop_duplicates("fixture_id")
    q = Q.merge(M, on="fixture_id")
    q = q[(q.side == q.my_side) & (q.period <= 4)]
    tier = R.set_index(["fixture_id", "player_id"]).defense.to_dict()
    lignes = []
    for r in q.itertuples():
        ts = [tier.get((r.fixture_id, p)) for p in (r.joueurs or [])]
        if len(ts) == 5 and all(t is not None for t in ts):
            lignes.append({"fixture_id": r.fixture_id, "groupe": r.groupe, "period": r.period, "x": sum(ts) / 5})
    D = pd.DataFrame(lignes)
    adv = E[E.kind.isin(["fg2", "fg3", "miss"]) & E.mien & ~E.nous].groupby(["fixture_id", "period"]).size().rename("tirs")
    fau = E[(E.kind == "foul") & (E.detail == "shooting_foul") & E.mien & E.nous].groupby(["fixture_id", "period"]).size().rename("fautes")
    D = D.merge(adv, on=["fixture_id", "period"], how="left").merge(fau, on=["fixture_id", "period"], how="left").fillna({"tirs": 0, "fautes": 0})
    D["N"] = D.tirs + D.fautes
    sortie, lignes_t = [], []
    for g in GROUPES:
        a = D[D.groupe == g].copy()
        if a.empty:
            lignes_t.append([g, 0, 0, "—", "—", "—", "—", "—", "non identifiable"])
            continue
        a["n"], a["sx"], a["sy"] = a.N, a.N * a.x, a.fautes * 100
        a["sxy"], a["sxx"] = a.x * a.fautes * 100, a.N * a.x * a.x
        A = somme_par_match(a.assign(n=a.n), "fixture_id", ["n", "sx", "sy", "sxy", "sxx"])
        res = boot(A, pente)
        tr = {"moins de 1": a[a.x < 1], "de 1 à 3": a[(a.x >= 1) & (a.x <= 3)], "plus de 3": a[a.x > 3]}
        ident = sum(len(t) > 0 and t.N.sum() >= 150 for t in tr.values()) >= 3
        taux = []
        for nom, t in tr.items():
            if t.N.sum() < 20:
                taux.append(f"{nom} : {int(t.N.sum())} tirs")
            else:
                At = somme_par_match(t.assign(f=t.fautes, N2=t.N), "fixture_id", ["f", "N2"])
                rr = boot(At, lambda s: 100 * s[0] / s[1] if s[1] else math.nan) if len(t.fixture_id.unique()) >= MIN_MATCHS else None
                taux.append(f"{nom} : {int(t.N.sum())} tirs, " + (fmt(rr, 1, " %") if rr else f"{100 * t.fautes.sum() / t.N.sum():.1f} % (moins de 8 matchs)"))
        annonce = 0.0 if g.startswith("v3") else 2.25
        lignes_t.append([g, int(a.N.sum()), a.fixture_id.nunique(), fmt(res), annonce, n_requis(int(a.N.sum()), res[3], 1.0) if res else "—",
                         " ; ".join(taux), "identifiable" if ident else "tranches insuffisantes (3 tranches de 150 tirs requises)",
                         v_valeur(res, annonce, 1.0, ident)])
    sortie.append(base.md(pd.DataFrame(lignes_t, columns=["groupe", "tirs adverses + fautes", "matchs", "pente (points par niveau)", "annoncée",
                                                           "n requis (tirs)", "taux par tranche d'exposition", "identifiabilité", "verdict"]), index=False))
    return "\n\n".join(sortie)


# ---------- mesure 3 : fatigue ----------
def mesure3(P, d):
    T = P["tirs"]
    T = T[T.nous & T.releve.notna()].copy()
    T["fat"] = T.releve.map(lambda r: float(r.fatigue))
    PEN = {"v3": [(20, .03), (40, .10), (60, .20), (100, .40)], "v4": [(20, .04), (40, .15), (60, .30), (80, .50)]}
    lignes = []
    for g in GROUPES:
        a = T[T.groupe == g]
        if len(a) < 5:
            lignes.append([g, 0, "—", "—", "—", "—", "—", "non identifiable"])
            continue
        x = a.fat / 10
        dd = pd.DataFrame({"m": a.fixture_id.values, "n": 1.0, "x": x.values, "y": a.make.astype(float).values * 100})
        dd["xy"], dd["xx"] = dd.x * dd.y, dd.x * dd.x
        res = boot(somme_par_match(dd, "m", ["n", "x", "y", "xy", "xx"]), pente)
        fmax = float(a.fat.max())
        paliers = PEN["v3" if g.startswith("v3") else "v4"]
        atteints = [p for p, _ in paliers if fmax >= p]
        pen_max = np.interp(fmax, [0] + [p for p, _ in paliers], [0] + [v for _, v in paliers])
        borne = -pen_max * float(a.make.mean()) * 100
        ident = bool(atteints) and int((a.fat >= 20).sum()) >= 100
        mde = (Z_ALPHA + Z_BETA) * res[3] * (fmax / 10) if res else None
        lignes.append([g, len(a), fmt(res), f"{fmax:.2f}", f"{pen_max * 100:.1f} % soit {borne:.2f} point de réussite", f"{mde:.2f}" if mde else "—",
                       f"{int((a.fat >= 20).sum())} tirs à fatigue ≥ 20 ; paliers atteints : {atteints or 'aucun'}",
                       "non identifiable" if not ident else v_bande(res, borne / max(fmax / 10, 0.1), 0.0, 2.0, ident)])
    sortie = [base.md(pd.DataFrame(lignes, columns=["groupe", "tirs", "pente de la réussite (points / +10 de fatigue)", "fatigue maximale observée",
                                                    "effet annoncé à cette fatigue", "effet détectable à cette fatigue (points)",
                                                    "paliers", "verdict"]), index=False)]
    # pertes de balle par quart (box score : nos joueurs, fatigue connue)
    box = d["box"][d["box"].is_mine & d["box"].period.between(1, 4) & (d["box"].minutes > 0)].merge(d["matchs"][["fixture_id", "groupe", "match_day"]], on="fixture_id")
    J = d["joueurs"]
    fat = {}
    for (pid, jr), _ in box.groupby(["player_id", "match_day"]):
        j = J[(J.player_id == pid) & (J.day <= str(jr)[:10]) & (J.day >= base.jour_avant(jr))]
        if len(j):
            fat[(pid, jr)] = float(j.sort_values("day").iloc[-1].fatigue)
    box["fat"] = [fat.get((p, j)) for p, j in zip(box.player_id, box.match_day)]
    lignes = []
    for g in GROUPES:
        a = box[(box.groupe == g) & box.fat.notna()]
        if len(a) < 5:
            lignes.append([g, len(a), "—", "non identifiable"])
            continue
        dd = pd.DataFrame({"m": a.fixture_id.values, "n": 1.0, "x": (a.fat / 10).values, "y": a.tov.values})
        dd["xy"], dd["xx"] = dd.x * dd.y, dd.x * dd.x
        res = boot(somme_par_match(dd, "m", ["n", "x", "y", "xy", "xx"]), pente)
        lignes.append([g, len(a), fmt(res, 3), "non identifiable (aucune valeur annoncée sur les pertes de balle ; fatigue maximale insuffisante)"])
    sortie.append("Pertes de balle par joueur-quart (box score), pente par +10 de fatigue :\n\n" + base.md(
        pd.DataFrame(lignes, columns=["groupe", "joueurs-quarts", "pente (pertes de balle par quart / +10 de fatigue)", "verdict"]), index=False))
    return "\n\n".join(sortie)


# ---------- mesure 4 : minutes lourdes au dernier quart ----------
def mesure4(P, d):
    E, box = P["evenements"], d["box"]
    b = box[box.period.between(1, 3)].groupby(["fixture_id", "player_id", "team_side"]).minutes.sum().reset_index(name="cum")
    sh = E[E.kind.isin(["fg2", "fg3"]) | ((E.kind == "miss") & (E.detail == "miss_fg"))].copy()
    sh["make"] = sh.kind.isin(["fg2", "fg3"]).astype(float)
    sh = sh.merge(b, on=["fixture_id", "player_id", "team_side"])
    sh["cat"] = np.where(sh.cum >= 35.5, "lourd", np.where((sh.cum >= 12) & (sh.cum < 30), "controle", None))
    sh = sh[sh.cat.notna()]
    sh["q4"] = sh.period == 4
    lignes = []
    for g in GROUPES:
        a = sh[sh.groupe == g]
        cells = {}
        for cat in ("lourd", "controle"):
            for q4 in (True, False):
                c = a[(a.cat == cat) & (a.q4 == q4)]
                cells[(cat, q4)] = c
        if len(cells[("lourd", True)]) < 5:
            lignes.append([g, "—", "—", "—", "non identifiable"])
            continue
        d4 = pd.concat([cells[k].assign(cell=i) for i, k in enumerate([("lourd", True), ("lourd", False), ("controle", True), ("controle", False)])])
        piv = d4.groupby(["fixture_id", "cell"]).make.agg(["sum", "count"]).unstack(fill_value=0)
        piv = piv.reindex(columns=pd.MultiIndex.from_product([["sum", "count"], [0, 1, 2, 3]]), fill_value=0)
        A = np.column_stack([piv[("sum", i)] for i in range(4)] + [piv[("count", i)] for i in range(4)])

        def did(s):
            if min(s[4:8]) == 0:
                return math.nan
            return 100 * ((s[0] / s[4] - s[1] / s[5]) - (s[2] / s[6] - s[3] / s[7]))
        res = boot(A, did)
        n4 = len(cells[("lourd", True)])
        ident = n4 >= 100 and a.fixture_id.nunique() >= MIN_MATCHS
        lignes.append([g, f"{n4} (Q4 lourds) ; {len(cells[('controle', True)])} (Q4 contrôle) ; {len(cells[('lourd', False)])} (Q1-3 lourds) ; {len(cells[('controle', False)])} (Q1-3 contrôle)",
                       fmt(res), n_requis(len(a), res[3], 3.0) if res else "—", v_bande(res, -9.0, 0.0, 3.0, ident)])
    return base.md(pd.DataFrame(lignes, columns=["groupe", "tirs par cellule", "différence de différences de réussite (points) [intervalle]",
                                                  "n requis (tirs)", "verdict (annoncé : entre −9 et 0)"]), index=False)


# ---------- mesure 5 : part de tirs à 3 points selon le focus de tir ----------
def mesure5(P):
    T, R = P["tirs"], P["reglages"]
    t = T[T.nous].groupby(["fixture_id", "player_id"]).agg(tirs=("make", "size"), trois=("trois", "sum")).reset_index()
    t = t[t.tirs >= 8].merge(R, on=["fixture_id", "player_id"]).merge(T[["fixture_id", "groupe"]].drop_duplicates("fixture_id"), on="fixture_id")
    t["part"] = t.trois / t.tirs
    lignes = []
    for g in GROUPES:
        a = t[t.groupe == g]
        for niv in (0, 2, 3, 4):
            c = a[a.tir == niv]
            if len(c) < 5:
                lignes.append([g, niv, len(c), "—", "non identifiable (moins de 5 joueurs-matchs)"])
                continue
            A = somme_par_match(c.assign(n=1.0), "fixture_id", ["part", "n"])
            res = boot(A, lambda s: 100 * s[0] / s[1])
            v = "—"
            if niv == 4:
                ident = len(c) >= 15
                v = f"plafond 66,7 % : {v_bande(res, 0, 66.7 + 5, 5.0, ident)} ; plafond 50 % : {v_bande(res, 0, 55.0, 5.0, ident)}" if res else "non identifiable"
            lignes.append([g, niv, len(c), fmt(res, 1, " %"), v])
    return base.md(pd.DataFrame(lignes, columns=["groupe", "niveau de tir", "joueurs-matchs (≥ 8 tirs)", "part de tirs à 3 points [intervalle]",
                                                  "verdict (niveau 4 : annoncé ≤ 66,7 % et ≤ 50 %)"]), index=False)


# ---------- mesure 6 : tirs par quart selon le focus offensif ----------
def mesure6(P):
    T, R, Q = P["tirs"], P["reglages"], P["quarts"]
    M = P["evenements"][["fixture_id", "groupe", "my_side"]].drop_duplicates("fixture_id")
    q = Q.merge(M, on="fixture_id")
    q = q[(q.side == q.my_side) & (q.period <= 4)]
    lignes = []
    for r in q.itertuples():
        for p in r.joueurs or []:
            lignes.append({"fixture_id": r.fixture_id, "period": r.period, "player_id": p, "groupe": r.groupe})
    pq = pd.DataFrame(lignes).merge(R, on=["fixture_id", "player_id"])
    tq = T[T.nous].groupby(["fixture_id", "period", "player_id"]).size().reset_index(name="tirs")
    pq = pq.merge(tq, on=["fixture_id", "period", "player_id"], how="left").fillna({"tirs": 0})
    out = []
    for g in GROUPES:
        a = pq[pq.groupe == g]
        n2, n4 = int((a.focus_off == 2).sum()), int((a.focus_off == 4).sum())
        if n4 < 5 or n2 < 5:
            out.append([g, n4, n2, "—", "non identifiable (moins de 5 joueurs-quarts au niveau 4 ou 2)"])
            continue
        x = a.assign(t4=np.where(a.focus_off == 4, a.tirs, 0.0), n4=(a.focus_off == 4) * 1.0, t2=np.where(a.focus_off == 2, a.tirs, 0.0), n2=(a.focus_off == 2) * 1.0)
        A = somme_par_match(x, "fixture_id", ["t4", "n4", "t2", "n2"])
        res = boot(A, lambda s: (s[0] / s[1]) / (s[2] / s[3]) if s[1] and s[3] and s[2] else math.nan)
        ident = n4 >= 30 and n2 >= 30
        out.append([g, n4, n2, fmt(res), v_valeur(res, 1.33, 0.15, ident) + ("" if ident else " (moins de 30 joueurs-quarts au niveau 4)")])
    return base.md(pd.DataFrame(out, columns=["groupe", "joueurs-quarts Primary (niveau 4)", "joueurs-quarts Normal (niveau 2)",
                                               "rapport des tirs par quart, Primary / Normal [intervalle]", "verdict (annoncé 1,33)"]), index=False)


# ---------- mesure 7 : rythme ----------
def secondes(c):
    try:
        m, s, _ = str(c).split(":")
        return int(m) * 60 + int(s)
    except (ValueError, AttributeError):
        return math.nan


def mesure7(P, d):
    box, M, E = d["box"], d["matchs"], P["evenements"]
    t = box[box.period == 0].groupby(["fixture_id", "team_side"]).agg(fga=("fga", "sum"), fta=("fta", "sum"), oreb=("oreb", "sum"), tov=("tov", "sum")).reset_index()
    t["poss"] = t.fga + 0.44 * t.fta - t.oreb + t.tov
    t = t.merge(M[["fixture_id", "groupe"]], on="fixture_id")
    out, moy = [], {}
    for g in GROUPES:
        a = t[t.groupe == g]
        A = somme_par_match(a.assign(n=1.0), "fixture_id", ["poss", "n"])
        res = boot(A, lambda s: s[0] / s[1])
        moy[g] = (A, res)
        out.append([g, len(a), fmt(res, 1)])
    s = base.md(pd.DataFrame(out, columns=["groupe", "équipes-matchs", "possessions par équipe et par match [intervalle]"]), index=False)
    diff = []
    for a, b2 in (("v3 ligue", "v4 ligue"), ("v4 amical", "v5 amical")):
        ra, rb = moy[a][1], moy[b2][1]
        if ra and rb:
            dist = []
            for _ in range(B):
                ia = RNG.integers(0, len(moy[a][0]), len(moy[a][0]))
                ib = RNG.integers(0, len(moy[b2][0]), len(moy[b2][0]))
                sa, sb = moy[a][0][ia].sum(axis=0), moy[b2][0][ib].sum(axis=0)
                dist.append(sb[0] / sb[1] - sa[0] / sa[1])
            lo, hi = np.percentile(dist, [2.5, 97.5])
            diff.append(f"- {b2} − {a} : {rb[0] - ra[0]:+.1f} possessions [{lo:+.1f} ; {hi:+.1f}] par équipe et par match (effet minimal 3).")
    s += "\n\nComparaison entre moteurs (deux groupes sans mélange) :\n\n" + "\n".join(diff)
    # écarts d'horloge entre événements consécutifs
    E2 = E[~E.kind.isin(["period_start", "period_end", "dead_ball", "substitution", "jump_ball", "endgame", "injury"])].copy()
    E2["s"] = E2.clock.map(secondes)
    E2 = E2.sort_values(["fixture_id", "period", "seq"])
    E2["ecart"] = (E2.groupby(["fixture_id", "period"]).s.shift(1) - E2.s)
    g24 = E2[(E2.ecart >= 0) & E2.ecart.notna()]
    out = []
    for g in GROUPES:
        a = g24[g24.groupe == g]
        A = somme_par_match(a.assign(sup=(a.ecart > 24) * 1.0, n=1.0, ecart2=a.ecart), "fixture_id", ["sup", "n", "ecart2"])
        res = boot(A, lambda s: 100 * s[0] / s[1])
        res_m = boot(A, lambda s: s[2] / s[1])
        pas = sorted(set((a.ecart % 6).round(0).astype(int).tolist()))[:4]
        out.append([g, len(a), fmt(res, 2, " %"), fmt(res_m, 1, " s"), int(a.ecart.max()), pas])
    s += "\n\nÉcarts d'horloge entre événements consécutifs d'un quart (hors début et fin de quart, balle morte, remplacements, entre-deux) :\n\n" + base.md(
        pd.DataFrame(out, columns=["groupe", "écarts", "part des écarts de plus de 24 s [intervalle]", "écart moyen [intervalle]", "écart maximal (s)", "restes modulo 6 s"]), index=False)
    return s


# ---------- mesure 8 : avantage du terrain ----------
def binom_p2(k, n, p0=0.5):
    pr = [math.comb(n, i) * p0 ** i * (1 - p0) ** (n - i) for i in range(n + 1)]
    return min(1.0, sum(x for x in pr if x <= pr[k] * (1 + 1e-9)))


def mesure8(P):
    E, T = P["evenements"], P["tirs"]
    out, lecture = [], []
    # lecture de payload.side : camp du premier tir qui suit l'entre-deux
    jb = E[E.kind == "jump_ball"][["fixture_id", "seq", "payload", "groupe"]].copy()
    jb["cote"] = jb.payload.map(lambda p: (p or {}).get("side"))
    prem = {}
    for r in jb.itertuples():
        s = E[(E.fixture_id == r.fixture_id) & (E.seq > r.seq) & E.kind.isin(["fg2", "fg3", "miss"])].sort_values("seq")
        if len(s):
            prem[(r.fixture_id, r.seq)] = s.iloc[0].team_side
    jb["premier_tir"] = [prem.get((f, s)) for f, s in zip(jb.fixture_id, jb.seq)]
    ok = jb.dropna(subset=["premier_tir"])
    accord = float((ok.cote == ok.premier_tir).mean()) if len(ok) else math.nan
    lecture.append(f"Lecture de `payload.side` : le camp du premier tir qui suit l'entre-deux est le même dans {accord * 100:.0f} % des {len(ok)} entre-deux ; "
                   f"part de `home` : {100 * float((jb.cote == 'home').mean()):.0f} % des {len(jb)}.")
    lecture_ok = accord >= 0.9 or accord <= 0.1
    for g in GROUPES:
        j = jb[jb.groupe == g]
        k, n = int((j.cote == "home").sum()), len(j)
        pa = f"{k} sur {n} (p exact {binom_p2(k, n):.3f})" if n else "—"
        t = T[T.groupe == g].copy()
        t["dom"] = t.team_side == "home"
        d = t.groupby(["fixture_id", "dom"]).make.agg(["sum", "count"]).unstack(fill_value=0)
        d = d.reindex(columns=pd.MultiIndex.from_product([["sum", "count"], [True, False]]), fill_value=0)
        A = np.column_stack([d[("sum", True)], d[("count", True)], d[("sum", False)], d[("count", False)]])
        res = boot(A, lambda s: 100 * (s[0] / s[1] - s[2] / s[3]) if s[1] and s[3] else math.nan)
        va = "non identifiable (moins de 194 entre-deux)" if n < 194 else "à évaluer"
        out.append([g, n, pa, len(t), fmt(res, 2, " points"), n_requis(len(t), res[3], 1.5) if res else "—", va + " ; (b) " + v_bande(res, 0.0, 3.0, 1.5, True)])
    s = "\n\n".join(lecture) + "\n\n" + base.md(pd.DataFrame(out, columns=["groupe", "entre-deux", "(a) gagnés par l'équipe qui reçoit", "tirs", "(b) réussite à domicile moins à l'extérieur [intervalle]",
                                                                         "n requis (tirs)", "verdict"]), index=False)
    if not lecture_ok:
        s += "\n\nLa lecture de `payload.side` n'est pas confirmée par le premier tir : le point (a) est non identifiable dans tous les groupes."
    return s


def run():
    d = base.charger()
    P = base.preparer(d)
    sections = [("1. Réussite d'un tir selon le type et la compétence du tireur (nos joueurs)", lambda: mesure1(P)),
                ("2. Tirs provoquant une faute selon l'agressivité défensive", lambda: mesure2(P)),
                ("3. Fatigue : réussite et pertes de balle", lambda: mesure3(P, d)),
                ("4. Pénalité au-delà de 36 minutes au dernier quart", lambda: mesure4(P, d)),
                ("5. Part de tirs à 3 points selon le focus de tir", lambda: mesure5(P)),
                ("6. Tirs par quart selon le focus offensif", lambda: mesure6(P)),
                ("7. Rythme", lambda: mesure7(P, d)),
                ("8. Avantage du terrain", lambda: mesure8(P))]
    for titre, f in sections:
        print(f"\n### {titre}\n")
        print(f())
