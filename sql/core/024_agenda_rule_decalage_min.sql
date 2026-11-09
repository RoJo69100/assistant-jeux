-- Plan du jour, étape 5d (docs/refonte-v3/journal-aujourdhui.md, critère H6) : les règles d'agenda de ligue
-- BasketVibe à heure écrite (19:30, 19:45, 20:50) reçoivent un décalage en minutes relatif au coup d'envoi
-- de core.fixture.scheduled_at. `heure` reste en repli (match sans coup d'envoi connu) ; gold.agenda et
-- gold.bv_agenda ne changent pas : pipelines/aujourdhui.py recale la ligne quand le coup d'envoi est connu.
-- Source des valeurs : coup d'envoi de la ligue 20:00 Europe/Paris (preview J4, constat J1 de l'étape 5c),
-- verrou 19:45 (core.fixture.extras.verrou_at, 18:45 UTC) : preview −30, preset −15 (verrou), export +50.
-- Additif : add column if not exists, update des seules lignes encore nulles. Aucun drop.

alter table core.agenda_rule add column if not exists decalage_min integer;

comment on column core.agenda_rule.decalage_min is
  'Minutes relatives au coup d''envoi (core.fixture.scheduled_at) ; prioritaire sur heure quand le coup d''envoi est connu (pipelines/aujourdhui.py), heure en repli.';

update core.agenda_rule
set decalage_min = case rule_id when 'ligue_preview' then -30 when 'ligue_preset' then -15 when 'ligue_export' then 50 end
where game = 'basketvibe'
  and rule_id in ('ligue_preview', 'ligue_preset', 'ligue_export')
  and decalage_min is null;
