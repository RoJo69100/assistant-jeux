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


MEM = (Path(__file__).resolve().parent.parent / "sql/core/036_rafraichir_memoire.sql").read_text(encoding="utf-8")
META = (Path(__file__).resolve().parent.parent / "sql/core/035_page_meta.sql").read_text(encoding="utf-8")


def cas_memoire():
    corps = MEM.split("create or replace function core.rafraichir_vues", 1)[1]
    i_refresh = corps.find("refresh materialized view")
    yield "mémoire : sans worker parallèle ni hachage doublé, avant le premier rafraîchissement", \
        -1 < corps.find("set local max_parallel_workers_per_gather = 0") < i_refresh \
        and -1 < corps.find("set local hash_mem_multiplier = 1") < i_refresh
    yield "mémoire : page_meta rattrapée avant les vues", -1 < corps.find("core.page_meta_rattraper(") < i_refresh
    yield "mémoire : garde de 034 conservée (verrou puis créneaux et attente)", \
        -1 < corps.find("pg_try_advisory_xact_lock(7140001)") < corps.find("core.rafraichir_bloque(now())") < i_refresh
    yield "mémoire : les 7 vues restent rafraîchies", corps.count("refresh materialized view concurrently") == 7
    vue = META.split("create or replace view gold.exports_state", 1)[1]
    yield "exports_state : lit core.page_meta, et bronze seulement au-delà du dernier rattrapage", \
        "from core.page_meta m" in vue and "r.id > (select coalesce(max(page_id), 0) from core.page_meta)" in vue
    yield "exports_state : mêmes colonnes (game, ordre, ecran, pour_quoi, dernier_paris, age_h, statut, team_id, club)", \
        all(c in vue for c in ("as dernier_paris", "as age_h", "as statut", "e.team_id, e.club"))
    yield "page_meta : aucun déclencheur sur bronze.raw_pages (ingestion intacte)", "trigger" not in META.lower()


JEUX = list(cas()) + list(cas_memoire())

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    echecs = 0
    for nom, ok in JEUX:
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    print(f"{len(JEUX) - echecs}/{len(JEUX)}")
    sys.exit(1 if echecs else 0)
