"""Chargement commun du « premier essai » (16/11/2026) : joueurs, minutes, focus adverse. Lecture seule.

Périmètre (recalculé à chaque lancement, aucune liste codée en dur) : matchs de silver.bv_fixtures de la saison SAISON,
status = 'finished', avec box joueur (period 0), box par quart (periods 1 à 4 tous présents) et play-by-play.
Chaque match reçoit son groupe de moteur par groupe(competition, jour) ; un résultat par groupe, jamais de mélange.
Requêtes : matchs (1), box (1), effectifs (1, étude A), focus (1, étude C).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # pipelines/ ; python -I ne l'ajoute pas
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import sql as sqlmod  # noqa: E402
from etude_evenements_basketvibe import GROUPES, groupe  # noqa: E402,F401

SAISON = "86a63498-c133-44ea-aedb-f1310ad51ae8"
COMPETENCES = ["two_point", "three_point", "defense", "passing", "ball_handling", "rebounding", "stamina", "athleticism"]
NB_REQUETES = [0]


def lire(q):
    NB_REQUETES[0] += 1
    cols, lignes = sqlmod.executer(q)
    return pd.DataFrame(lignes, columns=cols)


def matchs():
    """Tous les matchs terminés de la saison avec drapeaux de couverture ; `perimetre` = box 0 + Q1..Q4 + événements."""
    q = ("with b as (select fixture_id, count(distinct period) filter (where period between 1 and 4) as nq, "
         "bool_or(period = 0) as p0 from silver.bv_match_player_stats group by fixture_id), "
         "e as (select fixture_id, count(*) as nev from silver.bv_match_events group by fixture_id) "
         "select f.fixture_id, f.match_day, f.round_number, f.is_mine, m.competition, left(m.league_id::text, 4) as ligue, "
         "m.my_side, m.overtime_periods, coalesce(b.nq, 0) as nq, coalesce(b.p0, false) as p0, coalesce(e.nev, 0) as nev "
         "from silver.bv_fixtures f left join silver.bv_matches m on m.fixture_id = f.fixture_id "
         "left join b on b.fixture_id = f.fixture_id left join e on e.fixture_id = f.fixture_id "
         f"where f.season_id = '{SAISON}' and f.status = 'finished'")
    M = lire(q)
    M["match_day"] = M.match_day.astype(str).str[:10]
    M["nq"] = pd.to_numeric(M.nq)
    M["nev"] = pd.to_numeric(M.nev)
    M["p0"] = M.p0.astype(str).str.lower().isin(["true", "t", "1"])
    M["is_mine"] = M.is_mine.astype(str).str.lower().isin(["true", "t", "1"])
    M["groupe"] = [groupe(c, j) for c, j in zip(M.competition, M.match_day)]
    M["perimetre"] = M.p0 & (M.nq == 4) & (M.nev > 0)
    return M


def box():
    """Box par joueur et par période des matchs terminés de la saison (minutes > 0 filtrées plus tard)."""
    q = ("select s.fixture_id, s.period, s.player_id, s.name, s.team_side, s.team_id, s.team, s.position, "
         "s.\"min\" as minutes, s.pts, s.fga, s.fg3a, s.fta, s.reb, s.ast, s.eval, s.is_mine "
         "from silver.bv_match_player_stats s join silver.bv_fixtures f on f.fixture_id = s.fixture_id "
         f"where f.season_id = '{SAISON}' and f.status = 'finished'")
    B = lire(q)
    for c in ("period", "minutes", "pts", "fga", "fg3a", "fta", "reb", "ast", "eval"):
        B[c] = pd.to_numeric(B[c], errors="coerce")
    B["is_mine"] = B.is_mine.astype(str).str.lower().isin(["true", "t", "1"])
    return B


def box_toutes_saisons():
    """Box period 0 de tous les matchs en base (toutes saisons, toutes compétitions), avec groupe de moteur."""
    q = ("select s.fixture_id, s.player_id, s.team_side, s.team_id, s.\"min\" as minutes, s.fga, s.is_mine, "
         "m.competition, m.match_day from silver.bv_match_player_stats s join silver.bv_matches m on m.fixture_id = s.fixture_id "
         "where s.period = 0")
    B = lire(q)
    for c in ("minutes", "fga"):
        B[c] = pd.to_numeric(B[c], errors="coerce")
    B["match_day"] = B.match_day.astype(str).str[:10]
    B["is_mine"] = B.is_mine.astype(str).str.lower().isin(["true", "t", "1"])
    B["groupe"] = [groupe(c, j) for c, j in zip(B.competition, B.match_day)]
    return B


def forces():
    """Force du club (club_strength du classement) par équipe et par jour, saison SAISON."""
    q = ("select team_id, day, club_strength from silver.bv_standings_weekly "
         f"where season_id = '{SAISON}' and club_strength is not null")
    S = lire(q)
    S["day"] = pd.to_datetime(S.day.astype(str).str[:10])
    S["club_strength"] = pd.to_numeric(S.club_strength, errors="coerce")
    return S.drop_duplicates(["team_id", "day"]).sort_values("day")


def effectifs():
    cols = ", ".join(f"{c}_min, {c}_max" for c in COMPETENCES)
    q = ("select player_id, day, captured_at, club_slug, team_id, skills_visibility, position, height_cm, weight_kg, age, "
         f"experience, form, {cols} from silver.bv_club_roster")
    R = lire(q)
    R["day"] = R.day.astype(str).str[:10]
    for c in COMPETENCES:
        lo, hi = pd.to_numeric(R[f"{c}_min"], errors="coerce"), pd.to_numeric(R[f"{c}_max"], errors="coerce")
        R[c] = (lo + hi) / 2  # milieu de tranche (valeur exacte : min = max)
        R[f"{c}_largeur"] = hi - lo
    for c in ("height_cm", "weight_kg", "age", "experience", "form"):
        R[c] = pd.to_numeric(R[c], errors="coerce")
    return R


def focus():
    q = ("select fixture_id, competition, match_day, player_id, name, position, \"min\" as minutes, fga, shot_share, our_focus "
         "from gold.bv_match_opp_focus")
    F = lire(q)
    F["match_day"] = F.match_day.astype(str).str[:10]
    for c in ("minutes", "fga", "shot_share"):
        F[c] = pd.to_numeric(F[c], errors="coerce")
    F["groupe"] = [groupe(c, j) for c, j in zip(F.competition, F.match_day)]
    return F


def resume_perimetre(M):
    p = M[M.perimetre]
    print(f"Matchs terminés de la saison : {len(M)} ; dans le périmètre (box 0 + Q1..Q4 + événements) : {len(p)}")
    print("Périmètre par groupe de moteur et ligue :")
    t = p.groupby([p.groupe.fillna("sans groupe"), p.ligue.fillna("?")]).agg(
        n=("fixture_id", "size"), a_nous=("is_mine", "sum"), du=("match_day", "min"), au=("match_day", "max"))
    print(t.to_string())
    return p


def intervalle(vals, alpha=0.05):
    v = np.asarray([x for x in vals if x == x], float)
    if len(v) == 0:
        return (np.nan, np.nan)
    return tuple(np.percentile(v, [100 * alpha / 2, 100 * (1 - alpha / 2)]))


def verdict(est, ic, n_matchs):
    if n_matchs < 8 or ic is None or ic[0] != ic[0]:
        return "indéterminé : n trop petit"
    if ic[0] > 0 or ic[1] < 0:
        return "association présente"
    return "indéterminé : n trop petit"


def n_requis(n, est, ic):
    """n pour qu'un effet de la taille observée sorte de zéro (95 %, puissance 80 %), en supposant l'IC en 1/sqrt(n)."""
    if ic is None or ic[0] != ic[0] or est != est or est == 0:
        return None
    se = (ic[1] - ic[0]) / (2 * 1.96)
    return int(np.ceil(n * ((1.96 + 0.84) * se / abs(est)) ** 2))


def fmt(x, d=3):
    return "-" if x is None or x != x else f"{x:+.{d}f}"


def fic(ic, d=3):
    return "-" if ic is None or ic[0] != ic[0] else f"[{ic[0]:+.{d}f} ; {ic[1]:+.{d}f}]"
