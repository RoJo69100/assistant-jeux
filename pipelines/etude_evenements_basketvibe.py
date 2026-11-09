"""Étude du moteur de match BasketVibe au niveau de l'événement (tir, possession, joueur-quart), refonte v3.

Rapport et critères : docs/refonte-v3/etude-evenements-basketvibe.md. Lecture seule (executer() de sql.py).
Usage : python -I pipelines/etude_evenements_basketvibe.py inventaire     (étape 1)
        python -I pipelines/etude_evenements_basketvibe.py calculs        (étape 3, après les critères)
Les groupes de moteur ne sont jamais mélangés : v3 ligue, v3 amical, v4 ligue, v4 coupe, v4 amical, v5 amical.
"""
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


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "inventaire":
        inventaire()
    elif cmd == "calculs":
        import etude_evenements_calculs  # noqa: F401  (ajouté à l'étape 3)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
