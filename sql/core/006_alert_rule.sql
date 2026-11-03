-- Refonte v2, étape 1.4 : alertes du jour par jeu (données, pas du SQL par jeu), lues par gold.daily_alerts.
-- declencheur : joueur_blesse | joueur_fatigue | joueur_forme | effectif_dispo | export_perime
--               | match_sans_resultat | dernier_match | ancienne_vue (domaine repris tel quel de gold.<jeu>_daily_alerts,
--               en attendant son portage sur core).
-- Seuils dans l'échelle du jeu (core.game_params echelle_*) : alerte si seuil_bas < valeur <= seuil_haut (null = sans borne).
-- effectif_dispo : alerte si disponibles <= seuil_haut ; match_sans_resultat : seuil_haut = fenêtre en jours.
-- modele : champs {name} {valeur} {retour} {n} {ecran} {statut} {age_h} {kind} {round} {day} {result} {score} {opponent}.

create table if not exists core.alert_rule (
  game             text not null,
  rule_id          text not null,
  priority         int  not null check (priority between 1 and 3),
  domaine          text not null,
  declencheur      text not null check (declencheur in ('joueur_blesse','joueur_fatigue','joueur_forme','effectif_dispo',
                                                         'export_perime','match_sans_resultat','dernier_match','ancienne_vue')),
  competition_kind text,
  seuil_bas        numeric,
  seuil_haut       numeric,
  modele           text,
  source           text not null,
  actif            boolean not null default true,
  primary key (game, rule_id)
);
alter table core.alert_rule enable row level security;
drop policy if exists assistant_ro_select on core.alert_rule;
create policy assistant_ro_select on core.alert_rule for select to assistant_ro using (true);
grant select on core.alert_rule to assistant_ro;

-- Remplace chaque {clé} de modele par la valeur de v (texte vide si absente).
create or replace function core.remplir(modele text, v jsonb) returns text
language plpgsql immutable as $$
declare k text;
begin
  for k in select jsonb_object_keys(v) loop
    modele := replace(modele, '{' || k || '}', coalesce(v ->> k, ''));
  end loop;
  return regexp_replace(modele, '\{[a-z_]+\}', '', 'g');
end $$;
grant execute on function core.remplir(text, jsonb) to assistant_ro;

-- BasketVibe : repris de gold.bv_daily_alerts (sql/gold/012_bv_daily_alerts.sql).
insert into core.alert_rule (game, rule_id, priority, domaine, declencheur, competition_kind, seuil_bas, seuil_haut, modele, source) values
  ('basketvibe', 'blessure', 1, 'blessure', 'joueur_blesse', null, null, null, '{name} blessé{retour}', 'gold.bv_daily_alerts'),
  ('basketvibe', 'fatigue', 2, 'fatigue', 'joueur_fatigue', null, 20, null, '{name} : fatigue {valeur} (hors zone verte)',
   'basketvibe-joueurs/06-fatigue-0100 [M§5.6.1] (au-dessus de 20 = sortie de la zone verte)'),
  ('basketvibe', 'forme_1', 2, 'forme', 'joueur_forme', null, null, 1, '{name} : forme {valeur} (attaque −11 %)',
   'basketvibe-joueurs/05-forme-110 [M§5.5]'),
  ('basketvibe', 'forme_2', 2, 'forme', 'joueur_forme', null, 1, 2, '{name} : forme {valeur} (attaque −8 %)',
   'basketvibe-joueurs/05-forme-110 [M§5.5]'),
  ('basketvibe', 'dispo', 1, 'transferts', 'effectif_dispo', null, null, 8, 'Moins de 9 joueurs disponibles : vente impossible',
   'basketvibe-transferts [M§11.1] (9 joueurs disponibles minimum pour vendre)'),
  ('basketvibe', 'exports', 3, 'export', 'export_perime', null, null, null, 'Export {ecran} : {statut} ({age_h} h)',
   'core.export_rule (écart voulu : remplace la fraîcheur par type de page de gold.bv_daily_alerts)'),
  ('basketvibe', 'ligue_sans_resultat', 2, 'match', 'match_sans_resultat', 'ligue', null, 7, 'Match de {kind} joué non exporté : {round}du {day}',
   'gold.bv_daily_alerts'),
  ('basketvibe', 'coupe_sans_resultat', 2, 'match', 'match_sans_resultat', 'coupe', null, 7, 'Match de {kind} joué non exporté : {round}du {day}',
   'écart voulu : les matchs de coupe passés sans résultat n''étaient pas signalés'),
  ('basketvibe', 'dernier_match', 2, 'match', 'dernier_match', null, null, null, 'Dernier match exporté : {day} ({kind}, {result} {score} contre {opponent})',
   'gold.bv_daily_alerts'),
  ('basketvibe', 'finances', 1, 'finances', 'ancienne_vue', null, null, null, null,
   'gold.bv_daily_alerts (semaine type déficitaire, gold.bv_finance_health ; à porter avec gold.finance_health)')
on conflict (game, rule_id) do update set
  priority = excluded.priority, domaine = excluded.domaine, declencheur = excluded.declencheur,
  competition_kind = excluded.competition_kind, seuil_bas = excluded.seuil_bas, seuil_haut = excluded.seuil_haut,
  modele = excluded.modele, source = excluded.source;

-- Hockey Nation : repris de gold.hn_daily_alerts (sql/gold/026_hn_routine.sql). Seuls les exports sont portés ;
-- les autres domaines lisent des tables silver propres au jeu (offres, lignes, draft, scouts, U21, talents).
insert into core.alert_rule (game, rule_id, priority, domaine, declencheur, competition_kind, seuil_bas, seuil_haut, modele, source) values
  ('hockeynation', 'exports', 2, 'export', 'export_perime', null, null, null, 'Export {ecran} : {statut} ({age_h} h)', 'gold.hn_daily_alerts'),
  ('hockeynation', 'ligue_sans_resultat', 2, 'match', 'match_sans_resultat', 'ligue', null, 7, 'Match de {kind} joué non exporté : du {day} contre {opponent}',
   'écart voulu : les matchs passés encore « upcoming » n''étaient pas signalés'),
  ('hockeynation', 'draft', 1, 'draft', 'ancienne_vue', null, null, null, null, 'gold.hn_daily_alerts'),
  ('hockeynation', 'transferts', 1, 'transferts', 'ancienne_vue', null, null, null, null, 'gold.hn_daily_alerts'),
  ('hockeynation', 'tactique', 1, 'tactique', 'ancienne_vue', null, null, null, null, 'gold.hn_daily_alerts'),
  ('hockeynation', 'contrats', 2, 'contrats', 'ancienne_vue', null, null, null, null, 'gold.hn_daily_alerts (à porter avec gold.finance_health)'),
  ('hockeynation', 'scouting', 2, 'scouting', 'ancienne_vue', null, null, null, null, 'gold.hn_daily_alerts'),
  ('hockeynation', 'U21', 3, 'U21', 'ancienne_vue', null, null, null, null, 'gold.hn_daily_alerts'),
  ('hockeynation', 'effectif', 3, 'effectif', 'ancienne_vue', null, null, null, null, 'gold.hn_daily_alerts')
on conflict (game, rule_id) do update set
  priority = excluded.priority, domaine = excluded.domaine, declencheur = excluded.declencheur,
  competition_kind = excluded.competition_kind, seuil_bas = excluded.seuil_bas, seuil_haut = excluded.seuil_haut,
  modele = excluded.modele, source = excluded.source;
