"""Contrôle de silver.bv_club_roster sur la vraie base (effectifs des autres clubs BasketVibe, 2026-11-10).

Lancer : python -I pipelines/test_bv_club_roster.py   (code 1 si un contrôle échoue)
Contrôles :
  1. nombre de clubs de la vue = nombre de clubs ayant un appel /clubs/<slug>/season-roster dans silver.bv_api ;
  2. nombre de joueurs de la vue = nombre de joueurs des payloads d'effectif ;
  3. une seule dernière capture par club (est_derniere), et c'est bien la plus récente ;
  4. chaque joueur a ses 8 compétences, min <= max, et un team_id ;
  5. temps de la vue (select complet, moins une requête vide) < 3 s ; sinon : matérialiser la vue.
"""
import importlib.util
import sys
import time
from pathlib import Path

spec = importlib.util.spec_from_file_location("sqlmod", Path(__file__).resolve().parent / "sql.py")
sqlmod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sqlmod)

SEUIL_S = 3.0
COMPETENCES = ["two_point", "three_point", "defense", "passing", "ball_handling", "rebounding", "stamina", "athleticism"]


def une(sql: str):
    _, lignes = sqlmod.executer(sql)
    return lignes[0]


def chrono(sql: str) -> float:
    t0 = time.perf_counter()
    sqlmod.executer(sql)
    return time.perf_counter() - t0


def main() -> int:
    echecs = 0

    def controle(nom: str, ok: bool, detail: str):
        nonlocal echecs
        echecs += 0 if ok else 1
        print(f"{'ok ' if ok else 'ÉCHEC'} {nom} : {detail}")

    attendu = une("select count(distinct substring(endpoint from '^/clubs/([^/]+)/season-roster$')) as n, "
                  "coalesce(sum(jsonb_array_length(body->'players')), 0) as joueurs "
                  "from silver.bv_api where endpoint ~ '^/clubs/[^/]+/season-roster$' and jsonb_typeof(body->'players') = 'array'")
    vue = une("select count(distinct club_slug) as n, count(*) as joueurs from silver.bv_club_roster")
    controle("clubs", vue[0] == attendu[0], f"vue {vue[0]}, appels d'effectif {attendu[0]}")
    controle("joueurs", vue[1] == attendu[1], f"vue {vue[1]}, payloads {attendu[1]}")

    der = une("select count(*) filter (where nb <> 1) as clubs_mal, count(*) filter (where not recente) as pas_recente from ("
              "select club_slug, count(distinct capture_id) filter (where est_derniere) as nb, "
              "bool_and(not est_derniere or captured_at = mx) as recente from ("
              "select r.*, max(captured_at) over (partition by club_slug) as mx from silver.bv_club_roster r) q group by club_slug) z")
    controle("dernière capture", der[0] == 0 and der[1] == 0, f"{der[0]} club(s) sans dernière capture unique, {der[1]} non la plus récente")

    trous = " or ".join(f"{c}_min is null or {c}_max is null or {c}_min > {c}_max" for c in COMPETENCES)
    cmp = une(f"select count(*) filter (where {trous}) as comp_ko, count(*) filter (where team_id is null) as sans_team from silver.bv_club_roster")
    controle("compétences et team_id", cmp[0] == 0 and cmp[1] == 0, f"{cmp[0]} ligne(s) de compétences incomplètes, {cmp[1]} sans team_id")

    par_club = sqlmod.executer("select club_slug, count(*) as joueurs, max(captured_at at time zone 'Europe/Paris') as derniere_paris "
                               "from silver.bv_club_roster where est_derniere and not is_former_roster group by club_slug order by 3 desc")[1]
    print(f"     dernière capture par club ({len(par_club)} clubs, joueurs actifs) : "
          + " ; ".join(f"{s} {j} j. {str(d)[:16]}" for s, j, d in par_club[:5]) + (" ; …" if len(par_club) > 5 else ""))

    base = min(chrono("select 1") for _ in range(2))
    duree = min(chrono("select * from silver.bv_club_roster") for _ in range(2)) - base
    controle("temps de la vue", duree < SEUIL_S, f"{duree:.2f} s (seuil {SEUIL_S} s ; au-delà : matérialiser la vue)")

    print(f"{5 - echecs}/5")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
