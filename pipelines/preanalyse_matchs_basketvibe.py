"""Préanalyse des matchs BasketVibe (refonte v3) : effet, intervalle, n disponible contre n requis, verdict.

Critères écrits avant tout calcul : docs/refonte-v3/preanalyse-matchs-basketvibe.md, § 2 (commit 5f5831c).
Lecture seule (executer() de sql.py), sans scipy : lois de Student et binomiale écrites ici.
Usage : python -I pipelines/preanalyse_matchs_basketvibe.py [--sensibilite]
Les groupes ne sont jamais mélangés : G1 ligue v3, G2 ligue v4, G3 coupe v4, G4 amical v4, G5 amical v5.
"""
import argparse
import math
import sys
from pathlib import Path
from statistics import NormalDist

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python -I n'ajoute pas le dossier du script
import sql as sqlmod  # noqa: E402

Z = NormalDist().inv_cdf
Z_BETA = Z(0.80)
GROUPES = {"G1": "ligue v3", "G2": "ligue v4", "G3": "coupe v4", "G4": "amical v4", "G5": "amical v5"}


def groupe(competition, jour):
    """Règle de version du § 1.1 du rapport (écrite avant tout calcul)."""
    jour = str(jour)[:10]
    if competition == "league":
        return "G1" if jour <= "2026-10-26" else "G2"
    if competition == "cup":
        return "G3"
    if competition == "friendly":
        if jour <= "2026-10-10":
            return None  # un seul amical v3 : non analysé
        return "G5" if jour >= "2026-10-28" else "G4"
    return None


# ---------- statistiques (pas de scipy) ----------
def _betacf(a, b, x):
    tiny, qab, qap, qam = 1e-30, a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    d = 1.0 / (d if abs(d) > tiny else tiny)
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > tiny else tiny)
        c = 1.0 + aa / c
        c = c if abs(c) > tiny else tiny
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > tiny else tiny)
        c = 1.0 + aa / c
        c = c if abs(c) > tiny else tiny
        de = d * c
        h *= de
        if abs(de - 1.0) < 3e-12:
            break
    return h


def _betai(a, b, x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x))
    return bt * _betacf(a, b, x) / a if x < (a + 1) / (a + b + 2) else 1 - bt * _betacf(b, a, 1 - x) / b


def t_cdf(t, df):
    p = 0.5 * _betai(df / 2, 0.5, df / (df + t * t))
    return 1 - p if t > 0 else p


def t_ppf(p, df):
    lo, hi = -200.0, 200.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if t_cdf(mid, df) < p else (lo, mid)
    return (lo + hi) / 2


def binom_p2(k, n, p0=0.5):
    """p exact bilatérale : somme des probabilités au plus égales à celle de k."""
    pr = [math.comb(n, i) * p0 ** i * (1 - p0) ** (n - i) for i in range(n + 1)]
    return min(1.0, sum(x for x in pr if x <= pr[k] * (1 + 1e-9)))


def n_corr(r, alpha):
    return math.ceil(((Z(1 - alpha / 2) + Z_BETA) / math.atanh(r)) ** 2 + 3)


def pearson(x, y, alpha):
    """(r, n, IC bas, IC haut, p) ; IC de Fisher au niveau 1 − alpha ; None si n < 4 ou variance nulle."""
    d = pd.DataFrame({"x": x, "y": y}).dropna()
    n = len(d)
    if n < 5 or d.x.std() == 0 or d.y.std() == 0:  # critère : n disponible < 5, aucun effet calculé
        return None
    r = float(d.x.corr(d.y))
    r = max(min(r, 0.999999), -0.999999)
    se = 1 / math.sqrt(n - 3)
    z = math.atanh(r)
    lo, hi = math.tanh(z - Z(1 - alpha / 2) * se), math.tanh(z + Z(1 - alpha / 2) * se)
    t = r * math.sqrt((n - 2) / (1 - r * r))
    p = 2 * (1 - t_cdf(abs(t), n - 2))
    return r, n, lo, hi, p


def moyenne(v, alpha):
    """(moyenne, n, sd, IC bas, IC haut, p) ; t de Student ; None si n < 2."""
    v = pd.Series(v).dropna()
    n = len(v)
    if n < 5 or v.std() == 0:  # critère : n disponible < 5, aucun effet calculé
        return None
    m, sd = float(v.mean()), float(v.std())
    h = t_ppf(1 - alpha / 2, n - 1) * sd / math.sqrt(n)
    p = 2 * (1 - t_cdf(abs(m / (sd / math.sqrt(n))), n - 1))
    return m, n, sd, m - h, m + h, p


def verdict_corr(res, r_min, n_req):
    if res is None:
        return "n < 5 : aucun calcul"
    r, n, lo, hi, _ = res
    if n < 5:
        return "n < 5 : aucun calcul"
    if n < n_req:
        return "n trop petit"
    if (lo > 0 or hi < 0) and abs(r) >= r_min:
        return "décidable : effet présent"
    if lo > -r_min and hi < r_min:
        return "décidable : effet absent"
    return "décidable : entre les deux"


def verdict_moy(res, delta, n_req):
    if res is None:
        return "n < 5 : aucun calcul"
    m, n, sd, lo, hi, _ = res
    if n < 5:
        return "n < 5 : aucun calcul"
    if n < n_req:
        return "n trop petit"
    if (lo > 0 or hi < 0) and abs(m) >= delta:
        return "décidable : effet présent"
    if lo > -delta and hi < delta:
        return "décidable : effet absent"
    return "décidable : entre les deux"


def f(x, nd=3):
    return "—" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.{nd}f}"


def ligne_corr(g, nom, res, r_min, n_req, alpha):
    if res is None:
        return f"| {g} | {nom} | — | — | — | — | {verdict_corr(None, r_min, n_req)} |"
    r, n, lo, hi, p = res
    return f"| {g} | {nom} | {f(r, 2)} [{f(lo, 2)} ; {f(hi, 2)}] | {p:.3f} | {n} | {n_req} | {verdict_corr(res, r_min, n_req)} |"


# ---------- données ----------
def lire(sql):
    cols, lignes = sqlmod.executer(sql)
    return pd.DataFrame(lignes, columns=cols)


def charger():
    matchs = lire("select fixture_id, season_id, competition, match_day, my_side, home_team_id, away_team_id, home_score, away_score "
                  "from silver.bv_matches where status = 'finished'")
    matchs["groupe"] = [groupe(c, d) for c, d in zip(matchs.competition, matchs.match_day)]
    box = lire("select fixture_id, period, player_id, team_side, \"min\" as minutes, pts, fgm, fga, fg3m, fg3a, ftm, fta, oreb, dreb, tov, eval, is_mine "
               "from silver.bv_match_player_stats")
    for c in ("minutes", "pts", "fgm", "fga", "fg3m", "fg3a", "ftm", "fta", "oreb", "dreb", "tov", "eval", "period"):
        box[c] = pd.to_numeric(box[c])
    fatigue = lire("select day, player_id, fatigue from silver.bv_player_daily")
    force = lire("select day, team_id, club_strength from silver.bv_standings_weekly")
    moi = lire("select team_id from silver.bv_my_team").team_id.iloc[0]
    return matchs, box, fatigue, force, moi


def equipes(matchs, box):
    """Une ligne par match avec les agrégats des deux côtés (période 0 = match entier) et les écarts « nous − eux »."""
    tot = box[box.period == 0]
    lignes = []
    for fid, d in tot.groupby("fixture_id"):
        cote = {}
        for s, e in d.groupby("team_side"):
            m = e.sort_values("minutes", ascending=False)
            cote[s] = dict(fga=e.fga.sum(), fgm=e.fgm.sum(), fg3a=e.fg3a.sum(), fg3m=e.fg3m.sum(), fta=e.fta.sum(), ftm=e.ftm.sum(),
                           oreb=e.oreb.sum(), dreb=e.dreb.sum(), tov=e.tov.sum(), pts=e.pts.sum(),
                           utilises=int((e.minutes > 0).sum()), top5=float(m.minutes.head(5).sum() / m.minutes.sum()) if m.minutes.sum() else math.nan)
        if len(cote) != 2:
            continue
        lignes.append((fid, cote["home"], cote["away"]))
    out = []
    for fid, h, a in lignes:
        def facteurs(x, y):
            return dict(efg=(x["fgm"] + 0.5 * x["fg3m"]) / x["fga"], orb=x["oreb"] / (x["oreb"] + y["dreb"]),
                        tov=x["tov"] / (x["fga"] + 0.44 * x["fta"] + x["tov"]), ftr=x["fta"] / x["fga"],
                        part3=x["fg3a"] / x["fga"],
                        ppa3=3 * x["fg3m"] / x["fg3a"] if x["fg3a"] else math.nan,
                        ppa2=2 * (x["fgm"] - x["fg3m"]) / (x["fga"] - x["fg3a"]) if x["fga"] > x["fg3a"] else math.nan)
        fh, fa = facteurs(h, a), facteurs(a, h)
        out.append(dict(fixture_id=fid, pts_h=h["pts"], pts_a=a["pts"], util_h=h["utilises"], util_a=a["utilises"], top5_h=h["top5"], top5_a=a["top5"],
                        **{f"{k}_h": v for k, v in fh.items()}, **{f"{k}_a": v for k, v in fa.items()}))
    return matchs.merge(pd.DataFrame(out), on="fixture_id")


def orienter(df, moi):
    """« Nous » = notre côté dans nos matchs, le côté domicile dans les autres ; écarts nous − eux et marge."""
    df = df.copy()
    nous_dom = (df.my_side == "home") | df.my_side.isna()
    for k in ("efg", "orb", "tov", "ftr", "part3", "ppa3", "ppa2", "util", "top5", "pts"):
        n, e = df[f"{k}_h"].where(nous_dom, df[f"{k}_a"]), df[f"{k}_a"].where(nous_dom, df[f"{k}_h"])
        df[f"{k}_nous"], df[f"{k}_eux"] = n, e
    df["marge"] = df.pts_nous - df.pts_eux
    df["nous_id"] = df.home_team_id.where(nous_dom, df.away_team_id)
    df["eux_id"] = df.away_team_id.where(nous_dom, df.home_team_id)
    df["mien"] = df.my_side.notna()
    return df


def dernier(df, cle, jour, col):
    d = df[(df[cle[0]] == cle[1]) & (df.day <= jour)]
    return float(d.sort_values("day").iloc[-1][col]) if len(d) else math.nan


# ---------- les six questions ----------
def q1(M, alpha=0.0125, r_min=0.5, n_req=40):
    print("\n### Question 1 : ce qui sépare victoires et défaites (ligue seulement)\n")
    print(f"Corrélation de l'écart « nous − eux » du facteur avec la marge ; IC de Fisher à {100 * (1 - alpha):.2f} % (α = {alpha} par test) ; effet minimal r = {r_min} ; n requis {n_req}.\n")
    print("| groupe | facteur | r [IC] | p | n disponible | n requis | verdict |\n|---|---|---|---|---|---|---|")
    for g in ("G1", "G2"):
        d = M[M.groupe == g]
        for k, nom in (("efg", "eFG %"), ("orb", "rebonds offensifs %"), ("tov", "pertes de balle %"), ("ftr", "lancers francs par tir")):
            print(ligne_corr(g, nom, pearson(d[f"{k}_nous"] - d[f"{k}_eux"], d.marge, alpha), r_min, n_req, alpha))
    print("\nDescription (moyenne en victoire / en défaite de « nous », écart « nous − eux » du facteur) :\n")
    print("| groupe | facteur | victoires (n) | défaites (n) |\n|---|---|---|---|")
    for g in ("G1", "G2"):
        d = M[M.groupe == g]
        for k, nom in (("efg", "eFG %"), ("orb", "rebonds off. %"), ("tov", "pertes %"), ("ftr", "LF par tir")):
            e = d[f"{k}_nous"] - d[f"{k}_eux"]
            v, l = e[d.marge > 0], e[d.marge < 0]
            print(f"| {g} | {nom} | {f(v.mean())} ({len(v)}) | {f(l.mean())} ({len(l)}) |")


def q2(M, box, fatigue, moi, sens):
    print("\n### Question 2 : minutes lourdes et fatigue\n")
    alpha = 0.025
    # (a) joueur-match : au moins 3 quarts joués, au moins 27 minutes cumulées avant le Q4, au moins 1 minute au Q4
    q = box[box.period.between(1, 4)].copy()
    rows = []
    for (fid, pid, side), d in q.groupby(["fixture_id", "player_id", "team_side"]):
        p = d.set_index("period")
        joues = int((p.minutes > 0).sum())
        m13, e13 = p.loc[p.index.isin([1, 2, 3]), "minutes"].sum(), p.loc[p.index.isin([1, 2, 3]), "eval"].sum()
        m4 = p.minutes.get(4, 0.0)
        e4 = p["eval"].get(4, 0.0)  # p.eval est la méthode de pandas
        if joues >= 3 and m13 >= 27 and m4 >= 1:
            rows.append(dict(fixture_id=fid, r13=e13 / m13, r4=e4 / m4, diff=e4 / m4 - e13 / m13))
    A = pd.DataFrame(rows).merge(M[["fixture_id", "groupe"]], on="fixture_id")
    print(f"(a) Évaluation par minute au Q4 contre Q1 à Q3, joueurs avec ≥ 3 quarts, ≥ 27 min avant le Q4, ≥ 1 min au Q4. "
          f"Effet = différence moyenne / moyenne de base (rapport des moyennes) ; IC par la méthode du delta (dénominateur fixé) ; α = {alpha} ; effet minimal −15 % ; "
          "joueurs d'un même match non indépendants.\n")
    print("| groupe | effet relatif [IC] | différence moyenne par minute | n disponible (joueurs-matchs, matchs) | n requis | verdict |\n|---|---|---|---|---|---|")
    for g in GROUPES:
        a = A[A.groupe == g]
        res = moyenne(a["diff"], alpha) if len(a) else None
        if res is None:
            print(f"| {g} | — | — | {len(a)} / {a.fixture_id.nunique()} | — | {verdict_moy(None, 0.15, 0)} |")
            continue
        m, n, sd, lo, hi, _ = res
        base = float(a.r13.mean())
        rel, rlo, rhi, sig_rel = m / base, lo / base, hi / base, sd / abs(base)
        n_req = math.ceil(((Z(1 - alpha / 2) + Z_BETA) * sig_rel / 0.15) ** 2)
        vr = verdict_moy((rel, n, sig_rel, rlo, rhi, 0), 0.15, n_req)
        print(f"| {g} | {rel * 100:.1f} % [{rlo * 100:.1f} ; {rhi * 100:.1f}] | {f(m)} (base {f(base)}) | {n} / {a.fixture_id.nunique()} | {n_req} (σ relatif {f(sig_rel, 2)}) | {vr} |")
    # Contrôle HORS CRITÈRES (non retenu pour le verdict) : mêmes mesures pour les joueurs moins sollicités (< 27 min avant le Q4)
    ctl = []
    for (fid, pid, side), d in q.groupby(["fixture_id", "player_id", "team_side"]):
        p = d.set_index("period")
        m13, e13 = p.loc[p.index.isin([1, 2, 3]), "minutes"].sum(), p.loc[p.index.isin([1, 2, 3]), "eval"].sum()
        m4, e4 = p.minutes.get(4, 0.0), p["eval"].get(4, 0.0)
        if int((p.minutes > 0).sum()) >= 3 and 5 <= m13 < 27 and m4 >= 1:
            ctl.append(dict(fixture_id=fid, r13=e13 / m13, diff=e4 / m4 - e13 / m13))
    C = pd.DataFrame(ctl).merge(M[["fixture_id", "groupe"]], on="fixture_id")
    print("\nContrôle hors critères (non retenu pour le verdict) : mêmes mesures pour les joueurs avec ≥ 3 quarts et de 5 à 26 minutes avant le Q4.\n")
    print("| groupe | effet relatif au Q4 [IC] | n (joueurs-matchs) |\n|---|---|---|")
    for g in GROUPES:
        c = C[C.groupe == g]
        res = moyenne(c["diff"], alpha) if len(c) else None
        if res is None:
            print(f"| {g} | — | {len(c)} |")
        else:
            base = float(c.r13.mean())
            print(f"| {g} | {res[0] / base * 100:.1f} % [{res[3] / base * 100:.1f} ; {res[4] / base * 100:.1f}] | {res[1]} |")
    # (b) fatigue le matin du match (nos joueurs), évaluation par minute dans le match
    tot = box[(box.period == 0) & (box.is_mine.astype(str).str.lower().isin(["true", "t", "1"]))].merge(M[["fixture_id", "groupe", "match_day"]], on="fixture_id")
    fat = fatigue.copy()
    fat["day"] = fat.day.astype(str).str[:10]
    fat["fatigue"] = pd.to_numeric(fat.fatigue)
    out = []
    for _, r in tot.iterrows():
        jour = str(r.match_day)[:10]
        d = fat[(fat.player_id == r.player_id) & (fat.day <= jour)]
        if len(d) and r.minutes >= 1:
            dd = d.sort_values("day").iloc[-1]
            ecart = (pd.Timestamp(jour) - pd.Timestamp(dd.day)).days
            if ecart <= 1:
                out.append(dict(groupe=r.groupe, fixture_id=r.fixture_id, fatigue=float(dd.fatigue), taux=r["eval"] / r.minutes, minutes=r.minutes))
    B = pd.DataFrame(out)
    print(f"\n(b) Fatigue (dernier relevé du jour ou de la veille) et évaluation par minute dans le match, nos joueurs, ≥ 1 minute ; r de Pearson, IC de Fisher à {100 * (1 - alpha):.1f} % ; effet minimal r = −0,3 ; n requis {n_corr(0.3, alpha)}.\n")
    print("| groupe | r [IC] | p | n disponible (joueurs-matchs) | n requis | verdict |\n|---|---|---|---|---|---|")
    for g in GROUPES:
        b = B[B.groupe == g] if len(B) else B
        print(ligne_corr(g, "fatigue → évaluation/minute", pearson(b.fatigue, b.taux, alpha) if len(b) else None, 0.3, n_corr(0.3, alpha), alpha).replace(f"| {g} | fatigue → évaluation/minute | ", f"| {g} | ", 1))
    if len(B):
        print("\nPlage de fatigue observée (valeurs du relevé, échelle non documentée ; le skill cite des paliers 0, 20, 40, 60, 80) :\n")
        print("| groupe | minimum | médiane | maximum | écart-type | joueurs-matchs au-dessus de 10 |\n|---|---|---|---|---|---|")
        for g in GROUPES:
            b = B[B.groupe == g]
            if len(b):
                print(f"| {g} | {f(b.fatigue.min(), 2)} | {f(b.fatigue.median(), 2)} | {f(b.fatigue.max(), 2)} | {f(b.fatigue.std(), 2)} | {int((b.fatigue > 10).sum())} |")
    if sens and len(B):
        print("\nSensibilité (non retenue pour le verdict) : joueurs-matchs avec ≥ 10 minutes.\n")
        for g in GROUPES:
            b = B[(B.groupe == g) & (B.minutes >= 10)]
            res = pearson(b.fatigue, b.taux, alpha) if len(b) else None
            print(f"- {g} : " + ("aucun calcul" if res is None else f"r = {f(res[0], 2)} [{f(res[2], 2)} ; {f(res[3], 2)}], n = {res[1]}"))


def q3(M, alpha=0.025, r_min=0.4, n_req=56):
    print("\n### Question 3 : rotation\n")
    print(f"Corrélation de l'écart « nous − eux » avec la marge ; IC de Fisher à {100 * (1 - alpha):.1f} % ; effet minimal r = {r_min} ; n requis {n_req}.\n")
    print("| groupe | mesure | r [IC] | p | n disponible | n requis | verdict |\n|---|---|---|---|---|---|---|")
    for g in GROUPES:
        d = M[M.groupe == g]
        for k, nom in (("util", "joueurs utilisés"), ("top5", "part des minutes des 5 premiers")):
            print(ligne_corr(g, nom, pearson(d[f"{k}_nous"] - d[f"{k}_eux"], d.marge, alpha), r_min, n_req, alpha))


def q4(M, alpha=0.025, r_min=0.4, n_req=56):
    print("\n### Question 4 : tirs à 3 points\n")
    print(f"(i) Points par tir à 3 tenté moins points par tir à 2 tenté, moyenne des deux équipes par match ; t de Student, IC à {100 * (1 - alpha):.1f} % ; effet minimal 0,10 ; n requis = ((z + z_β)·σ/0,10)².")
    print(f"(ii) Corrélation de l'écart « nous − eux » de la part de tirs à 3 avec la marge ; IC de Fisher ; effet minimal r = {r_min} ; n requis {n_req}.\n")
    print("| groupe | mesure | effet [IC] | n disponible | n requis | verdict |\n|---|---|---|---|---|---|")
    for g in GROUPES:
        d = M[M.groupe == g]
        diff = ((d.ppa3_h - d.ppa2_h) + (d.ppa3_a - d.ppa2_a)) / 2
        res = moyenne(diff, alpha)
        if res is None:
            print(f"| {g} | (i) 3 pts − 2 pts par tir | — | {len(d)} | — | n < 5 : aucun calcul |")
        else:
            m, n, sd, lo, hi, _ = res
            n_r = math.ceil(((Z(1 - alpha / 2) + Z_BETA) * sd / 0.10) ** 2)
            print(f"| {g} | (i) 3 pts − 2 pts par tir | {f(m, 3)} [{f(lo, 3)} ; {f(hi, 3)}] pt/tir (σ {f(sd, 3)}) | {n} | {n_r} | {verdict_moy(res, 0.10, n_r)} |")
        res = pearson(d.part3_nous - d.part3_eux, d.marge, alpha)
        print(f"| {g} | (ii) part de tirs à 3 → marge | " + ("—" if res is None else f"r = {f(res[0], 2)} [{f(res[2], 2)} ; {f(res[3], 2)}]")
              + f" | {0 if res is None else res[1]} | {n_req} | {verdict_corr(res, r_min, n_req)} |")


def q5(M, alpha=0.025):
    print("\n### Question 5 : avantage du terrain\n")
    print(f"(a) Marge domicile − extérieur, t de Student, IC à {100 * (1 - alpha):.1f} % ; effet minimal 3 points ; n requis = ((z + z_β)·σ/3)². (b) Victoires à domicile contre 0,5, test binomial exact ; effet minimal 60 % ; n requis 236.\n")
    print("| groupe | mesure | effet [IC] ou taux | n disponible | n requis | verdict |\n|---|---|---|---|---|---|")
    for g in GROUPES:
        d = M[M.groupe == g]
        marge_dom = d.pts_h - d.pts_a
        res = moyenne(marge_dom, alpha)
        if res is None:
            print(f"| {g} | (a) marge à domicile | — | {len(d)} | — | n < 5 : aucun calcul |")
        else:
            m, n, sd, lo, hi, _ = res
            n_r = math.ceil(((Z(1 - alpha / 2) + Z_BETA) * sd / 3) ** 2)
            print(f"| {g} | (a) marge à domicile | {f(m, 1)} [{f(lo, 1)} ; {f(hi, 1)}] pts (σ {f(sd, 1)}) | {n} | {n_r} | {verdict_moy(res, 3, n_r)} |")
        k, n = int((marge_dom > 0).sum()), int((marge_dom != 0).sum())
        p = binom_p2(k, n) if n else math.nan
        v = "n < 5 : aucun calcul" if n < 5 else ("n trop petit" if n < 236 else "décidable")
        print(f"| {g} | (b) victoires à domicile | {k} sur {n} (p exact {f(p, 3)}) | {n} | 236 | {v} |")


def q6(M, force, moi, alpha=0.05, r_min=0.5, n_req=30):
    print("\n### Question 6 : points de différence par point de force d'équipe (ligue seulement)\n")
    F = force.copy()
    F["day"] = F.day.astype(str).str[:10]
    F["club_strength"] = pd.to_numeric(F.club_strength)
    print(f"Écart de `club_strength` (dernier relevé ≤ jour du match) et marge ; r de Pearson, IC de Fisher à {100 * (1 - alpha):.0f} % ; effet minimal r = {r_min} ; n requis {n_req}.\n")
    print("| groupe | r [IC] | pente (points de marge par point de force) [IC] | n disponible / matchs du groupe | n requis | verdict |\n|---|---|---|---|---|---|")
    for g in ("G1", "G2"):
        d = M[M.groupe == g].copy()
        d["jour"] = d.match_day.astype(str).str[:10]
        d["fn"] = [dernier(F, ("team_id", t), j, "club_strength") for t, j in zip(d.nous_id, d.jour)]
        d["fe"] = [dernier(F, ("team_id", t), j, "club_strength") for t, j in zip(d.eux_id, d.jour)]
        d["ecart"] = d.fn - d.fe
        u = d.dropna(subset=["ecart", "marge"])
        res = pearson(u.ecart, u.marge, alpha)
        if res is None:
            print(f"| {g} | — | — | {len(u)} / {len(d)} | {n_req} | n < 5 : aucun calcul |")
            continue
        r, n, lo, hi, _ = res
        sx, sy = u.ecart.std(), u.marge.std()
        pente = r * sy / sx
        se_pente = abs(pente) * math.sqrt((1 - r * r) / max(n - 2, 1)) / abs(r) if r else math.nan
        tc = t_ppf(1 - alpha / 2, n - 2)
        print(f"| {g} | {f(r, 2)} [{f(lo, 2)} ; {f(hi, 2)}] | {f(pente, 2)} [{f(pente - tc * se_pente, 2)} ; {f(pente + tc * se_pente, 2)}] | {n} / {len(d)} | {n_req} | {verdict_corr(res, r_min, n_req)} |")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sensibilite", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    matchs, box, fatigue, force, moi = charger()
    M = orienter(equipes(matchs, box), moi)
    print("## Matchs analysés par groupe (box score des deux côtés)\n")
    print("| groupe | matchs | dont nous | dont autres équipes |\n|---|---|---|---|")
    for g, nom in GROUPES.items():
        d = M[M.groupe == g]
        print(f"| {g} {nom} | {len(d)} | {int(d.mien.sum())} | {int((~d.mien).sum())} |")
    q1(M)
    q2(M, box, fatigue, moi, a.sensibilite)
    q3(M)
    q4(M)
    q5(M)
    q6(M, force, moi)


if __name__ == "__main__":
    main()
