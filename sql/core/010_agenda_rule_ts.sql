-- Refonte v2, étape 1.4 : core.agenda_rule pour Team Soccer (reprise de gold.ts_agenda, sql/gold/018_ts_agenda.sql).
-- Nouvelles colonnes (lues par gold.agenda, sql/gold/062_agenda.sql) :
--   soir_min          heure calculée avant soir_min → la veille à soir_min (l'utilisateur n'agit que le soir, après 19:00)
--   avant_coup_envoi  ligne gardée seulement tant que le coup d'envoi n'est pas passé (comme gold.ts_upcoming)
--   fait_cle          clé booléenne de core.fixture.extras ; vraie → priorite_si_fait et modele_si_fait
--   ancienne_vue      déclencheur « ancienne_vue » : lignes reprises telles quelles d'une ancienne vue, par catégorie
--                     (académie : révélations restantes de gold.ts_academy ; amical : un par semaine — pas encore dans core)
-- Trous ajoutés : {quand} (« Ce soir », « Pour demain », « Pour JJ/MM ») et {formation}.

alter table core.agenda_rule add column if not exists soir_min time;
alter table core.agenda_rule add column if not exists avant_coup_envoi boolean not null default false;
alter table core.agenda_rule add column if not exists fait_cle text;
alter table core.agenda_rule add column if not exists priorite_si_fait int check (priorite_si_fait between 1 and 3);
alter table core.agenda_rule add column if not exists modele_si_fait text;
alter table core.agenda_rule add column if not exists ancienne_vue text;
alter table core.agenda_rule drop constraint if exists agenda_rule_declencheur_check;
alter table core.agenda_rule add constraint agenda_rule_declencheur_check
  check (declencheur in ('match','jour_semaine','jour_sans_match','vente','fin_saison','jour_saison','ancienne_vue'));
alter table core.agenda_rule drop constraint if exists agenda_rule_check;
alter table core.agenda_rule add constraint agenda_rule_check
  check (heure is not null or decalage is not null or declencheur in ('jour_saison','ancienne_vue'));
alter table core.agenda_rule drop constraint if exists agenda_rule_fait_check;
alter table core.agenda_rule add constraint agenda_rule_fait_check
  check ((fait_cle is null) = (priorite_si_fait is null) and (fait_cle is null) = (modele_si_fait is null));
alter table core.agenda_rule drop constraint if exists agenda_rule_ancienne_vue_check;
alter table core.agenda_rule add constraint agenda_rule_ancienne_vue_check
  check ((declencheur = 'ancienne_vue') = (ancienne_vue is not null));

-- Composition : coup d'envoi − 2 h (match pré-calculé) [skill teamsoccer-match] ; avant 19:00 → la veille au soir.
-- Export : le jour du match, sauf amical (comme l'ancienne vue).
insert into core.agenda_rule (game, rule_id, declencheur, competition_kind, decalage, soir_min, avant_coup_envoi,
                              priority, category, modele, fait_cle, priorite_si_fait, modele_si_fait, source) values
  ('teamsoccer', 'compo_ligue',   'match', 'ligue',   '-2 hours', '19:00', true, 1, 'composition',
   '{quand} (ligue, {venue}, contre {opponent}) : enregistrer la composition (agent Tactique)', 'lineup_saved', 3,
   '{quand} (ligue, {venue}, contre {opponent}) : composition déjà enregistrée ({formation}), à revoir seulement si Forme ou blessure ont changé',
   'gold.ts_agenda ; limite 2 h avant [skill teamsoccer-match] ; soir après 19:00 (CLAUDE.md horizon)'),
  ('teamsoccer', 'compo_coupe',   'match', 'coupe',   '-2 hours', '19:00', true, 1, 'composition',
   '{quand} (coupe, {venue}, contre {opponent}) : enregistrer la composition (agent Tactique)', 'lineup_saved', 3,
   '{quand} (coupe, {venue}, contre {opponent}) : composition déjà enregistrée ({formation}), à revoir seulement si Forme ou blessure ont changé',
   'gold.ts_agenda ; limite 2 h avant [skill teamsoccer-match]'),
  ('teamsoccer', 'compo_amical',  'match', 'amical',  '-2 hours', '19:00', true, 1, 'composition',
   '{quand} (amical, {venue}, contre {opponent}) : enregistrer la composition (agent Tactique)', 'lineup_saved', 3,
   '{quand} (amical, {venue}, contre {opponent}) : composition déjà enregistrée ({formation}), à revoir seulement si Forme ou blessure ont changé',
   'gold.ts_agenda ; limite 2 h avant [skill teamsoccer-match]'),
  ('teamsoccer', 'compo_playoff', 'match', 'playoff', '-2 hours', '19:00', true, 1, 'composition',
   '{quand} (barrage, {venue}, contre {opponent}) : enregistrer la composition (agent Tactique)', 'lineup_saved', 3,
   '{quand} (barrage, {venue}, contre {opponent}) : composition déjà enregistrée ({formation}), à revoir seulement si Forme ou blessure ont changé',
   'gold.ts_agenda ; limite 2 h avant [skill teamsoccer-match]'),
  ('teamsoccer', 'compo_autre',   'match', 'autre',   '-2 hours', '19:00', true, 1, 'composition',
   '{quand} (match de type inconnu, {venue}, contre {opponent}) : enregistrer la composition (agent Tactique) ; vérifier dans la page Matchs de quoi il s''agit', 'lineup_saved', 3,
   '{quand} (match de type inconnu, {venue}, contre {opponent}) : composition déjà enregistrée ({formation}) ; vérifier dans la page Matchs de quoi il s''agit',
   'gold.ts_agenda ; limite 2 h avant [skill teamsoccer-match]'),
  ('teamsoccer', 'export_ligue',   'match', 'ligue',   '0 minutes', null, true, 2, 'export',
   'Après le match : exporter la page du match (ligue contre {opponent}), puis agent Match', null, null, null, 'gold.ts_agenda'),
  ('teamsoccer', 'export_coupe',   'match', 'coupe',   '0 minutes', null, true, 2, 'export',
   'Après le match : exporter la page du match (coupe contre {opponent}), puis agent Match', null, null, null, 'gold.ts_agenda'),
  ('teamsoccer', 'export_playoff', 'match', 'playoff', '0 minutes', null, true, 2, 'export',
   'Après le match : exporter la page du match (barrage contre {opponent}), puis agent Match', null, null, null, 'gold.ts_agenda'),
  ('teamsoccer', 'export_autre',   'match', 'autre',   '0 minutes', null, true, 2, 'export',
   'Après le match : exporter la page du match (match de type inconnu contre {opponent}), puis agent Match', null, null, null, 'gold.ts_agenda')
on conflict (game, rule_id) do update set
  declencheur = excluded.declencheur, competition_kind = excluded.competition_kind, decalage = excluded.decalage,
  soir_min = excluded.soir_min, avant_coup_envoi = excluded.avant_coup_envoi, priority = excluded.priority,
  category = excluded.category, modele = excluded.modele, fait_cle = excluded.fait_cle,
  priorite_si_fait = excluded.priorite_si_fait, modele_si_fait = excluded.modele_si_fait, source = excluded.source;

-- Lundi et vendredi (rythme [skill teamsoccer-saison]) ; 19:00 = le soir.
insert into core.agenda_rule (game, rule_id, declencheur, isodow, heure, priority, category, modele, source) values
  ('teamsoccer', 'lundi_finances', 'jour_semaine', 1, '19:00', 1, 'finances',
   'Lundi : exporter Finances et Stade (semaine close), contrôler l''entretien du stade (bug déjà vu), puis agent Finances ; limite d''achat remise à zéro ; paiement HPC possible',
   'gold.ts_agenda ; lundi 00:05 [skill teamsoccer-saison]'),
  ('teamsoccer', 'vendredi_entrainement', 'jour_semaine', 5, '19:00', 1, 'entrainement',
   'Vendredi : exporter Effectif et Entraînement (entraînement de la nuit), puis agent Entraînement',
   'gold.ts_agenda ; vendredi ~00:00–01:00 UTC [skill teamsoccer-saison]')
on conflict (game, rule_id) do update set
  declencheur = excluded.declencheur, isodow = excluded.isodow, heure = excluded.heure, priority = excluded.priority,
  category = excluded.category, modele = excluded.modele, source = excluded.source;

-- Repris de l'ancienne vue : révélations d'académie et amical de la semaine.
insert into core.agenda_rule (game, rule_id, declencheur, ancienne_vue, priority, category, modele, source) values
  ('teamsoccer', 'academie_reprise', 'ancienne_vue', 'gold.ts_agenda', 2, 'académie', '(texte de l''ancienne vue)',
   'gold.ts_agenda ; 3 révélations par jour [skill teamsoccer-saison]'),
  ('teamsoccer', 'amical_reprise',   'ancienne_vue', 'gold.ts_agenda', 3, 'amical', '(texte de l''ancienne vue)',
   'gold.ts_agenda ; un amical par semaine [skill teamsoccer-saison]')
on conflict (game, rule_id) do update set
  declencheur = excluded.declencheur, ancienne_vue = excluded.ancienne_vue, priority = excluded.priority,
  category = excluded.category, modele = excluded.modele, source = excluded.source;
