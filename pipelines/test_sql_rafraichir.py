"""Tests de structure de sql/core/034_rafraichir_garde.sql (24/11) : lecture du texte, aucune base requise.
Le contrôle sur la base (core.rafraichir_bloque à 08:40, 18:30, 08:24, 09:15, maintenant) est fait par requête de lecture."""
import re
import sys
from pathlib import Path

SQL = (Path(__file__).resolve().parent.parent / "sql/core/034_rafraichir_garde.sql").read_text(encoding="utf-8")


def cas():
    corps = SQL.split("create or replace function core.rafraichir_vues", 1)[1]
    yield "plafond : les deux jobs passent à 8 min", SQL.count("statement_timeout = '8min'") == 2 \
        and "15min" not in SQL.split("select cron.alter_job", 1)[1]
    yield "créneau : aucun lancement de 08:25 à 09:15", "h >= time '08:25' and h < time '09:15'" in SQL
    yield "créneau : aucun lancement de 18:15 à 19:05", "h >= time '18:15' and h < time '19:05'" in SQL
    yield "attente : 60 min après un timeout, une annulation ou un redémarrage", \
        all(m in SQL for m in ("%statement timeout%", "%canceling statement%", "%server restarted%")) and "interval '60 minutes'" in SQL
    yield "attente : levée par un rafraîchissement réussi après l'échec", "e.rafraichi_a < echec" in SQL
    i_verrou, i_garde, i_refresh = corps.find("pg_try_advisory_xact_lock(7140001)"), corps.find("core.rafraichir_bloque(now())"), corps.find("refresh materialized view")
    yield "ordre : verrou, puis garde, puis rafraîchissement", -1 < i_verrou < i_garde < i_refresh
    yield "garde : s'applique aussi à une demande forcée (avant le test p_force)", i_garde < corps.find("if not p_force")
    yield "vues : les 7 vues matérialisées restent rafraîchies", len(re.findall(r"refresh materialized view concurrently", corps)) == 7


JEUX = list(cas())

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    echecs = 0
    for nom, ok in JEUX:
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    print(f"{len(JEUX) - echecs}/{len(JEUX)}")
    sys.exit(1 if echecs else 0)
