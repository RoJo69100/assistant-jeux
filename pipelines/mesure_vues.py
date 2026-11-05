"""Mesure le temps de lecture des vues qui bloquent le soir (refonte v3, S4).

Usage : python -I pipelines/mesure_vues.py [--passes 3] [--vues gold.season_context,core.standing] [--jeux basketvibe,...]
Pour chaque vue et chaque jeu : `select count(*) from (select * from <vue> where game = '<jeu>') t` par le transport de sql.py
(HTTPS ou Postgres direct), temps mural en ms, comme le vit l'utilisateur. Erreur ou timeout (20 s du rôle) = « timeout ».
Sortie : tableau Markdown vue | jeu | 1er passage | médiane | lignes | verdict (seuil 2 s).
"""
import argparse
import statistics
import sys
import time

sys.path.insert(0, __import__("os").path.dirname(__file__))
import sql as q  # noqa: E402

VUES = ["gold.season_context", "gold.match_objective", "gold.daily_alerts", "core.player_daily", "core.fixture",
        "core.standing", "core.finance_daily", "core.market_listing", "core.academy_prospect", "core.staff",
        "core.training_plan", "core.facility", "core.season"]
JEUX = ["basketvibe", "derbymanager", "hardwood", "hockeynation", "sixzeroleague", "teamsoccer"]
SEUIL_MS = 2000


TRANSPORT = q.transport()  # une seule fois : la sonde du port 5432 coûte ~6,5 s par appel quand il est bloqué


def une_mesure(vue: str, jeu: str):
    sql = f"select count(*) as n from (select * from {vue} where game = {q.litteral(jeu)}) t"
    t0 = time.perf_counter()
    try:
        cols, lignes = q.via_https(sql) if TRANSPORT == "https" else q.via_pg(sql, None)
        return (time.perf_counter() - t0) * 1000, int(lignes[0][0])
    except SystemExit as e:  # sql.py quitte avec un message en cas d'erreur SQL
        return None, str(e)[:60]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--passes", type=int, default=3)
    p.add_argument("--vues", default=",".join(VUES))
    p.add_argument("--jeux", default=",".join(JEUX))
    a = p.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    print("| vue | jeu | 1er passage (ms) | médiane (ms) | lignes | verdict |\n|---|---|---|---|---|---|", flush=True)
    for vue in a.vues.split(","):
        for jeu in a.jeux.split(","):
            temps, n = [], None
            for _ in range(a.passes):
                ms, r = une_mesure(vue, jeu)
                temps.append(ms)
                n = r if ms is not None else n
                if ms is None:  # timeout : inutile de refaire 20 s deux fois, verdict certain
                    break
            ok = [t for t in temps if t is not None]
            premier = "timeout" if temps[0] is None else f"{temps[0]:.0f}"
            med = "timeout" if len(ok) < len(temps) else f"{statistics.median(ok):.0f}"
            verdict = "✅" if None not in temps and statistics.median(ok) < SEUIL_MS else "❌"
            print(f"| {vue} | {jeu} | {premier} | {med} | {n} | {verdict} |", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
