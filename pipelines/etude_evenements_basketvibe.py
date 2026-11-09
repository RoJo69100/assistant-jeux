"""Étude du moteur de match BasketVibe au niveau de l'événement (tir, possession, joueur-quart), refonte v3.

Rapport et critères : docs/refonte-v3/etude-evenements-basketvibe.md. Lecture seule (executer() de sql.py).
Usage : python -I pipelines/etude_evenements_basketvibe.py inventaire     (étape 1)
        python -I pipelines/etude_evenements_basketvibe.py calculs        (étape 3, après les critères)
Les groupes de moteur ne sont jamais mélangés : v3 ligue, v3 amical, v4 ligue, v4 coupe, v4 amical, v5 amical.
"""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python -I n'ajoute pas le dossier du script
import sql as sqlmod  # noqa: E402

GROUPES = ["v3 ligue", "v3 amical", "v4 ligue", "v4 coupe", "v4 amical", "v5 amical"]


def groupe(competition, jour):
    """Règle de version du rapport de préanalyse (§ 1.1) : ligue v3 jusqu'au 26/10, amical v3 le 10/10, v4 ensuite, amical v5 dès le 28/10."""
    jour = str(jour)[:10]
    if competition == "league":
        return "v3 ligue" if jour <= "2026-10-26" else "v4 ligue"
    if competition == "cup":
        return "v4 coupe"
    if competition == "friendly":
        if jour <= "2026-10-10":
            return "v3 amical"
        return "v5 amical" if jour >= "2026-10-28" else "v4 amical"
    return None


def md(df, index=True):
    """Tableau Markdown (pas de dépendance à tabulate)."""
    d = df.reset_index() if index else df
    cols = [str(c) for c in d.columns]
    lignes = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in d.itertuples(index=False):
        lignes.append("| " + " | ".join("" if (isinstance(v, float) and v != v) else str(v) for v in r) + " |")
    return "\n".join(lignes)


def lire(sql):
    cols, lignes = sqlmod.executer(sql)
    return pd.DataFrame(lignes, columns=cols)


def charger():
    """DataFrames : matchs terminés, événements, box score, réglages tactiques, compétences et fatigue de nos joueurs."""
    d = {}
    d["matchs"] = lire("select fixture_id, season_id, competition, match_day, my_side, home_team_id, away_team_id, home_score, away_score "
                       "from silver.bv_matches where status = 'finished'")
    d["matchs"]["groupe"] = [groupe(c, j) for c, j in zip(d["matchs"].competition, d["matchs"].match_day)]
    d["matchs"]["mien"] = d["matchs"].my_side.notna()
    d["evenements"] = lire("select fixture_id, seq, period, clock, team_side, kind, detail, player_id, player2_id, home_score, away_score, "
                           "is_three, shot_x, shot_y, payload from silver.bv_match_events")
    box = lire("select fixture_id, period, player_id, team_side, \"min\" as minutes, pts, fgm, fga, fg3m, fg3a, ftm, fta, oreb, dreb, tov, pf, eval, is_mine "
               "from silver.bv_match_player_stats")
    for c in ("period", "minutes", "pts", "fgm", "fga", "fg3m", "fg3a", "ftm", "fta", "oreb", "dreb", "tov", "pf", "eval"):
        box[c] = pd.to_numeric(box[c])
    box["is_mine"] = box.is_mine.astype(str).str.lower().isin(["true", "t", "1"])
    d["box"] = box
    d["tactiques"] = lire("select fixture_id, team_id, opponent_id, defensive_focus, lineup_by_quarter, opponent_lineup_by_quarter, player_directives "
                          "from silver.bv_match_tactics")
    d["joueurs"] = lire("select day, player_id, fatigue, form, experience, ps, two_point, three_point, defense, passing, ball_handling, rebounding, "
                        "stamina, athleticism, two_point_exact, three_point_exact, defense_exact, passing_exact, ball_handling_exact, "
                        "rebounding_exact, stamina_exact, athleticism_exact from silver.bv_player_daily")
    d["joueurs"]["day"] = d["joueurs"].day.astype(str).str[:10]
    d["moi"] = lire("select team_id from silver.bv_my_team").team_id.iloc[0]
    return d


def inventaire():
    d = charger()
    M, E = d["matchs"], d["evenements"]
    E = E.merge(M[["fixture_id", "groupe", "mien"]], on="fixture_id")
    print("## b) Événements par type et par groupe (nombre d'événements)\n")
    E["type"] = E.kind + " / " + E.detail.fillna("")
    t = E.pivot_table(index="type", columns="groupe", values="seq", aggfunc="count", fill_value=0).reindex(columns=GROUPES, fill_value=0)
    t["total"] = t.sum(axis=1)
    print(md(t.sort_values("total", ascending=False)))
    print("\n## b) Couverture par groupe\n")
    lignes = []
    for g in GROUPES:
        e = E[E.groupe == g]
        tirs = e[e.kind.isin(["fg2", "fg3"]) | (e.kind == "miss")]
        lignes.append({"groupe": g, "matchs": int(M[M.groupe == g].shape[0]), "événements": len(e), "tirs": len(tirs),
                       "tirs avec coordonnées": int(tirs.shot_x.notna().sum()),
                       "fautes sur tir": int(((e.kind == "foul") & (e.detail == "shooting_foul")).sum()),
                       "remplacements": int((e.kind == "substitution").sum()),
                       "matchs avec remplacement": int(e[e.kind == "substitution"].fixture_id.nunique()),
                       "entre-deux": int((e.kind == "jump_ball").sum())})
    print(md(pd.DataFrame(lignes), index=False))
    print("\n## b) Compositions de début de quart et réglages tactiques par groupe (matchs avec leur page match-tactics)\n")
    T = d["tactiques"].merge(M[["fixture_id", "groupe", "mien"]], on="fixture_id")
    lignes = []
    for g in GROUPES:
        mg, tg = M[(M.groupe == g)], T[T.groupe == g]
        lignes.append({"groupe": g, "matchs": len(mg), "dont à nous": int(mg.mien.sum()), "avec réglages": tg.fixture_id.nunique(),
                       "composition nôtre": int(tg.lineup_by_quarter.notna().groupby(tg.fixture_id).any().sum()),
                       "composition adverse": int(tg.opponent_lineup_by_quarter.notna().groupby(tg.fixture_id).any().sum()),
                       "réglages par joueur (nôtres)": int(tg.player_directives.notna().groupby(tg.fixture_id).any().sum()),
                       "focus défensif (nôtre)": int(tg.defensive_focus.notna().groupby(tg.fixture_id).any().sum())})
    print(md(pd.DataFrame(lignes), index=False))
    print("\n## c) Compétences de nos joueurs (silver.bv_player_daily)\n")
    J = d["joueurs"]
    print(f"- {len(J)} lignes, {J.player_id.nunique()} joueurs, {J.day.nunique()} jours distincts, du {J.day.min()} au {J.day.max()} ; "
          f"compétences à une décimale (`*_exact`) : {int(J.two_point_exact.notna().sum())} lignes sur {len(J)}.")
    print("- Joueurs par jour : " + " ; ".join(f"{j} {n}" for j, n in J.groupby("day").size().items()))
    box0 = d["box"][(d["box"].period == 0) & d["box"].is_mine & (d["box"].minutes > 0)].merge(M[["fixture_id", "groupe", "match_day"]], on="fixture_id")
    lignes = []
    for g in GROUPES:
        b = box0[box0.groupe == g]
        n_vis = n_exact = 0
        for r in b.itertuples():
            j = J[(J.player_id == r.player_id) & (J.day <= str(r.match_day)[:10]) & (J.day >= (pd.Timestamp(str(r.match_day)[:10]) - pd.Timedelta(days=1)).strftime("%Y-%m-%d"))]
            if len(j):
                n_vis += 1
                n_exact += int(j.sort_values("day").iloc[-1].two_point_exact is not None and pd.notna(j.sort_values("day").iloc[-1].two_point_exact))
        lignes.append({"groupe": g, "joueurs-matchs à nous (≥ 1 min)": len(b), "avec un relevé de compétences ≤ 1 jour avant": n_vis, "dont à une décimale": n_exact})
    print("\n" + md(pd.DataFrame(lignes), index=False))


def _js(x):
    if x is None or (isinstance(x, float) and x != x):
        return None
    return json.loads(x) if isinstance(x, str) else x


def jour_avant(jour, n=1):
    return (pd.Timestamp(str(jour)[:10]) - pd.Timedelta(days=n)).strftime("%Y-%m-%d")


def preparer(d):
    """Données d'événements prêtes pour les huit mesures (aucun effet calculé ici).

    tirs : un tir (réussi `fg2`/`fg3`, raté `miss_fg`, sans les contrés), avec son type (3 points ; cercle ou mi-distance quand
    le moteur l'étiquette), le tireur, son camp, `nous` (le tireur est de notre équipe) et les compétences de nos tireurs (relevé de
    la veille ou du jour). reglages : réglages tactiques de nos joueurs par match. quarts : composition de chaque quart (deux camps).
    """
    M = d["matchs"]
    E = d["evenements"].merge(M[["fixture_id", "groupe", "mien", "my_side", "match_day"]], on="fixture_id").copy()
    E["payload"] = E.payload.map(_js)
    E["zone"] = E.payload.map(lambda p: (p or {}).get("shot_zone"))
    E["nous"] = E.mien & (E.team_side == E.my_side)
    E["period"] = pd.to_numeric(E.period)
    tirs = E[E.kind.isin(["fg2", "fg3"]) | ((E.kind == "miss") & (E.detail == "miss_fg"))].copy()
    tirs["make"] = tirs.kind.isin(["fg2", "fg3"])
    tirs["trois"] = (tirs.kind == "fg3") | ((tirs.kind == "miss") & (tirs.is_three == True))  # noqa: E712
    z = {"fg2_make_paint": "cercle", "fg2_make_mid": "mi", "paint": "cercle", "mid": "mi"}
    tirs["type2"] = [None if t else z.get(dt if m else zn) for t, m, dt, zn in zip(tirs.trois, tirs.make, tirs.detail, tirs.zone)]
    J = d["joueurs"]
    snap = {}
    for (pid, jr), _ in tirs[tirs.nous].groupby(["player_id", "match_day"]):
        j = J[(J.player_id == pid) & (J.day <= str(jr)[:10]) & (J.day >= jour_avant(jr))]
        if len(j):
            snap[(pid, jr)] = j.sort_values("day").iloc[-1]
    tirs["releve"] = [snap.get((p, j)) if n else None for p, j, n in zip(tirs.player_id, tirs.match_day, tirs.nous)]
    reglages, quarts = [], []
    for r in d["tactiques"].itertuples():
        m = M[M.fixture_id == r.fixture_id]
        if m.empty:
            continue
        for x in _js(r.player_directives) or []:
            reglages.append({"fixture_id": r.fixture_id, "player_id": x["player_id"], "role": x.get("role_tier"), "tir": x.get("shot_tier"),
                             "focus_off": x.get("offensive_focus_tier"), "defense": x.get("defense_tier")})
        side = m.iloc[0].my_side
        autre = "away" if side == "home" else "home"
        for q, ids in enumerate(_js(r.lineup_by_quarter) or []):
            quarts.append({"fixture_id": r.fixture_id, "period": q + 1, "side": side, "joueurs": ids})
        for q, ids in enumerate(_js(r.opponent_lineup_by_quarter) or []):
            quarts.append({"fixture_id": r.fixture_id, "period": q + 1, "side": autre, "joueurs": ids})
    return {"evenements": E, "tirs": tirs, "reglages": pd.DataFrame(reglages), "quarts": pd.DataFrame(quarts)}


def comptes():
    """Nombre d'événements disponibles par question et par groupe (comptages seulement, aucun effet)."""
    d = charger()
    P = preparer(d)
    E, T, R, Q, M, box = P["evenements"], P["tirs"], P["reglages"], P["quarts"], d["matchs"], d["box"]
    lignes = []
    # 1. tirs de nos joueurs avec compétences connues
    t1 = T[T.nous & T.releve.notna()]
    for g in GROUPES:
        a = t1[t1.groupe == g]
        lignes.append({"question": "1 tirs de nos joueurs avec compétences", "groupe": g, "n": len(a),
                       "dont 3 points": int(a.trois.sum()), "dont cercle étiqueté": int((a.type2 == "cercle").sum()),
                       "dont mi-distance étiquetée": int((a.type2 == "mi").sum()), "dont 2 points non étiquetés": int((~a.trois & a.type2.isna()).sum())})
    # 2. tirs adverses dans des quarts où notre composition est connue, fautes sur tir de notre défense
    qn = Q[Q.side.isin(["home", "away"])].merge(M[["fixture_id", "groupe", "my_side"]], on="fixture_id")
    qn = qn[(qn.side == qn.my_side) & (qn.period <= 4)]
    adv = E[E.kind.isin(["fg2", "fg3", "miss"]) & E.mien & ~E.nous].merge(qn[["fixture_id", "period"]], on=["fixture_id", "period"])
    fau = E[(E.kind == "foul") & (E.detail == "shooting_foul") & E.mien & E.nous].merge(qn[["fixture_id", "period"]], on=["fixture_id", "period"])
    for g in GROUPES:
        lignes.append({"question": "2 tirs adverses (quarts à composition connue) et fautes de notre défense", "groupe": g,
                       "n": int((adv.groupe == g).sum()), "fautes sur tir": int((fau.groupe == g).sum()),
                       "quarts": int((qn.groupe == g).sum())})
    # 3. tirs de nos joueurs avec fatigue connue ; au-dessus de 10 et de 20
    for g in GROUPES:
        a = t1[t1.groupe == g]
        f = a.releve.map(lambda r: float(r.fatigue))
        lignes.append({"question": "3 tirs de nos joueurs avec fatigue connue", "groupe": g, "n": len(a),
                       "fatigue ≥ 10": int((f >= 10).sum()), "fatigue ≥ 20": int((f >= 20).sum()),
                       "fatigue maximale": round(float(f.max()), 2) if len(a) else None})
    # 4. tirs au Q4 de joueurs ayant joué 36 minutes aux Q1-Q3 ; contrôle : de 12 à 30 minutes
    b = box[box.period.between(1, 3)].groupby(["fixture_id", "player_id", "team_side"]).minutes.sum().reset_index(name="cum")
    sh = E[E.kind.isin(["fg2", "fg3"]) | ((E.kind == "miss") & (E.detail == "miss_fg"))]
    q4 = sh[sh.period == 4].merge(b, left_on=["fixture_id", "player_id", "team_side"], right_on=["fixture_id", "player_id", "team_side"])
    for g in GROUPES:
        a = q4[q4.groupe == g]
        lignes.append({"question": "4 tirs au Q4 selon les minutes cumulées avant le Q4", "groupe": g, "n": len(a),
                       "joueurs à 36 min ou plus": int((a.cum >= 35.5).sum()), "contrôle (12 à 30 min)": int(((a.cum >= 12) & (a.cum < 30)).sum())})
    # 5. joueurs-matchs de nos tireurs avec niveau de tir, au moins 8 tirs
    if len(R):
        ct = T[T.nous].groupby(["fixture_id", "player_id"]).size().reset_index(name="tirs").merge(R, on=["fixture_id", "player_id"]).merge(M[["fixture_id", "groupe"]], on="fixture_id")
        for g in GROUPES:
            a = ct[(ct.groupe == g) & (ct.tirs >= 8)]
            lignes.append({"question": "5 joueurs-matchs (≥ 8 tirs) selon le niveau de tir", "groupe": g, "n": len(a),
                           **{f"niveau {k}": int((a.tir == k).sum()) for k in (0, 1, 2, 3, 4)}})
        # 6. joueurs-quarts sur le terrain selon le niveau de focus offensif
        qq = Q.merge(M[["fixture_id", "groupe", "my_side"]], on="fixture_id")
        qq = qq[(qq.side == qq.my_side) & (qq.period <= 4)]
        lignes6 = []
        for r in qq.itertuples():
            for pid in r.joueurs or []:
                lignes6.append({"fixture_id": r.fixture_id, "period": r.period, "player_id": pid, "groupe": r.groupe})
        pq = pd.DataFrame(lignes6).merge(R, on=["fixture_id", "player_id"]) if lignes6 else pd.DataFrame()
        tirs_q = T[T.nous].groupby(["fixture_id", "period", "player_id"]).size().reset_index(name="tirs")
        pq = pq.merge(tirs_q, on=["fixture_id", "period", "player_id"], how="left").fillna({"tirs": 0}) if len(pq) else pq
        for g in GROUPES:
            a = pq[pq.groupe == g] if len(pq) else pq
            lignes.append({"question": "6 joueurs-quarts sur le terrain selon le focus offensif", "groupe": g, "n": len(a),
                           **{f"niveau {k}": int((a.focus_off == k).sum()) for k in (0, 1, 2, 3, 4)}, "tirs": int(a.tirs.sum()) if len(a) else 0})
    # 7. équipes-matchs
    for g in GROUPES:
        lignes.append({"question": "7 équipes-matchs (box score des deux côtés)", "groupe": g, "n": int(2 * (M.groupe == g).sum())})
    # 8. entre-deux et tirs à domicile / à l'extérieur
    for g in GROUPES:
        lignes.append({"question": "8 entre-deux et tirs", "groupe": g, "n": int(((E.groupe == g) & (E.kind == "jump_ball")).sum()),
                       "tirs": int((T.groupe == g).sum())})
    df = pd.DataFrame(lignes)
    for q, a in df.groupby("question", sort=False):
        print(f"\n### {q}\n")
        print(md(a.drop(columns="question").dropna(axis=1, how="all"), index=False))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "inventaire":
        inventaire()
    elif cmd == "comptes":
        comptes()
    elif cmd == "calculs":
        import etude_evenements_calculs
        etude_evenements_calculs.run()
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
