-- Refonte v2, étape 0.4 : les vues silver et gold sont en security_invoker et lisent le payload bronze ;
-- sans select sur toute la table, assistant_ro ne pouvait lire aucune vue qui en dépend (gold.bv_agenda…).
-- La limite « pas de payload complet » est tenue côté pipelines/sql.py (refus de `payload` hors vue, --payload-path).
grant select on bronze.raw_pages, bronze.discord_messages to assistant_ro;
