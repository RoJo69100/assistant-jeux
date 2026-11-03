-- Refonte v2, étape 1.4 : règles d'agenda par jeu (données, pas du SQL par jeu), lues par gold.agenda.
-- Déclencheurs :
--   match            un match non joué de competition_kind : à heure fixe le jour du match, ou à scheduled_at + decalage
--   jour_semaine     chaque jour isodow (1 = lundi) de la fenêtre, à heure
--   jour_sans_match  chaque jour futur sans match de competition_kind, jusqu'au lendemain du dernier match de ligue
--   vente            chaque vente à moi (core.market_listing.is_mine) qui finit dans la fenêtre, à ends_at
--   fin_saison       le jour du dernier match de ligue connu, à heure
-- Trous du modèle : {round} {opponent} {venue} {hhmi} {sans_plan} {player} {bids} {price}.

create table if not exists core.agenda_rule (
  game              text not null,
  rule_id           text not null,
  declencheur       text not null check (declencheur in ('match','jour_semaine','jour_sans_match','vente','fin_saison')),
  competition_kind  text check (competition_kind in ('ligue','coupe','amical','playoff','autre')),
  isodow            int  check (isodow between 1 and 7),
  heure             time,
  decalage          interval,
  priority          int  not null check (priority between 1 and 3),
  category          text not null,
  modele            text not null,
  source            text not null,
  actif             boolean not null default true,
  primary key (game, rule_id),
  check (heure is not null or decalage is not null)
);
alter table core.agenda_rule enable row level security;
drop policy if exists assistant_ro_select on core.agenda_rule;
create policy assistant_ro_select on core.agenda_rule for select to assistant_ro using (true);
grant select on core.agenda_rule to assistant_ro;

-- BasketVibe : reprise une à une des lignes de gold.bv_agenda (sql/gold/018_bv_fixes_2026_10_22.sql).
insert into core.agenda_rule (game, rule_id, declencheur, competition_kind, isodow, heure, decalage, priority, category, modele, source) values
  ('basketvibe', 'ligue_preset',     'match', 'ligue', null, '19:45', null, 1, 'ligue',
   'Avant 19:45 : vérifier le preset de ligue et régler le focus défensif sur la page du match J{round} contre {opponent} ({venue})',
   'gold.bv_agenda ; verrouillage 19:45 (basketvibe.yaml rythme)'),
  ('basketvibe', 'ligue_preview',    'match', 'ligue', null, '19:30', null, 2, 'export',
   'Avant 19:45 si possible : exporter la page Preview du match J{round} (effectif adverse à jour)',
   'gold.bv_agenda ; basketvibe.yaml exports (preview)'),
  ('basketvibe', 'ligue_export',     'match', 'ligue', null, '20:50', null, 2, 'export',
   'Après le match (~20:50) : exporter la page du match J{round} (puis analyse de l''agent Match)',
   'gold.bv_agenda ; basketvibe.yaml exports (match)'),
  ('basketvibe', 'amical_preset',    'match', 'amical', null, null, '-15 minutes', 1, 'amical',
   'Avant {hhmi} : preset amical sur le match contre {opponent} ({venue}){sans_plan}',
   'gold.bv_agenda ; verrouillage 15 min avant (basketvibe.yaml rythme)'),
  ('basketvibe', 'amical_export',    'match', 'amical', null, null, '55 minutes', 3, 'export',
   'Après l''amical (~{hhmi}) : exporter la page du match',
   'gold.bv_agenda ; basketvibe.yaml exports (match)'),
  ('basketvibe', 'amical_manquant',  'jour_sans_match', 'amical', null, '12:00', null, 3, 'amical',
   'Aucun amical programmé ce jour : en programmer un (recette ~17 500, minutes pour les jeunes, test v4)',
   'gold.bv_agenda ; mémoire amicaux quotidiens'),
  ('basketvibe', 'entrainement_sam', 'jour_semaine', null, 6, '23:00', null, 2, 'entraînement',
   'Avant dimanche 04:00 : vérifier et sauvegarder les choix d''entraînement (fiche de l''agent Entraînement)',
   'gold.bv_agenda ; basketvibe.yaml rythme (dimanche 04:00)'),
  ('basketvibe', 'routine_dim',      'jour_semaine', null, 7, '04:30', null, 1, 'export',
   'Après 04:00 : exporter Entraînement, Finances et Personnel (routine du dimanche)',
   'gold.bv_agenda ; basketvibe.yaml exports (dimanche après 04:00)'),
  ('basketvibe', 'academie_jeu',     'jour_semaine', null, 4, '09:30', null, 3, 'export',
   'Après 09:00 : exporter la page Académie (nouveau rapport du scout) ; Finances en option',
   'gold.bv_agenda ; basketvibe.yaml exports (jeudi après 09:00)'),
  ('basketvibe', 'fin_vente',        'vente', null, null, null, '0 minutes', 2, 'transfert',
   'Fin de la vente de {player} ({bids} enchère(s), prix affiché {price})',
   'gold.bv_agenda'),
  ('basketvibe', 'fin_saison',       'fin_saison', null, null, '21:00', null, 1, 'saison',
   'Dernier match de la saison : maintien et prime de classement se jouent ce soir',
   'gold.bv_agenda')
on conflict (game, rule_id) do nothing;
