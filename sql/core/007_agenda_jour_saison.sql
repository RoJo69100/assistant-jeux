-- Refonte v2, étape 1.4 : déclencheur « jour_saison » de core.agenda_rule (jeux à calendrier en jours de saison).
-- Date = core.season.day1 + jour_saison − 1. Heure nulle = événement de la journée, sans heure sourcée.
-- Hockey Nation : les 16 événements de gold.hn_calendar [G:Calendar], heures 21:00 seulement quand le calendrier les donne (CET).

alter table core.agenda_rule add column if not exists jour_saison int check (jour_saison > 0);
alter table core.agenda_rule drop constraint if exists agenda_rule_declencheur_check;
alter table core.agenda_rule add constraint agenda_rule_declencheur_check
  check (declencheur in ('match','jour_semaine','jour_sans_match','vente','fin_saison','jour_saison'));
alter table core.agenda_rule drop constraint if exists agenda_rule_check;
alter table core.agenda_rule add constraint agenda_rule_check
  check (heure is not null or decalage is not null or declencheur = 'jour_saison');
alter table core.agenda_rule drop constraint if exists agenda_rule_jour_saison_check;
alter table core.agenda_rule add constraint agenda_rule_jour_saison_check
  check ((declencheur = 'jour_saison') = (jour_saison is not null));

insert into core.agenda_rule (game, rule_id, declencheur, jour_saison, heure, priority, category, modele, source) values
  ('hockeynation', 'j01', 'jour_saison', 1, null, 2, 'saison', 'J1 : début de saison : âge +1, draftés en U21, U17 de 15 ans, fenêtre d''échanges I et agents libres ouvertes, plafond annoncé en hausse ou en baisse', 'gold.hn_calendar [G:Calendar]'),
  ('hockeynation', 'j03', 'jour_saison', 3, null, 2, 'transfert', 'J3 : premières réponses des coachs ; Free Agent Frenzy (offres jusqu''à 1 h avant)', 'gold.hn_calendar [G:Calendar]'),
  ('hockeynation', 'j04', 'jour_saison', 4, null, 3, 'académie', 'J4 : début des missions de scouting (jusqu''au jour 63)', 'gold.hn_calendar [G:Calendar]'),
  ('hockeynation', 'j08', 'jour_saison', 8, null, 2, 'ligue', 'J8 : 1re journée de saison régulière ; 1er jour de paie', 'gold.hn_calendar [G:Calendar]'),
  ('hockeynation', 'j10', 'jour_saison', 10, null, 3, 'transfert', 'J10 : mise à jour des demandes des agents libres', 'gold.hn_calendar [G:Calendar]'),
  ('hockeynation', 'j20', 'jour_saison', 20, null, 3, 'transfert', 'J20 : mise à jour des demandes des agents libres ; Championnat du monde', 'gold.hn_calendar [G:Calendar]'),
  ('hockeynation', 'j28', 'jour_saison', 28, null, 2, 'finances', 'J28 : fourchette du plafond de la saison suivante', 'gold.hn_calendar [G:Calendar]'),
  ('hockeynation', 'j30', 'jour_saison', 30, null, 3, 'transfert', 'J30 : mise à jour des demandes des agents libres', 'gold.hn_calendar [G:Calendar]'),
  ('hockeynation', 'j35', 'jour_saison', 35, '21:00', 1, 'transfert', 'J35 : fermeture fenêtre I et agents libres (21:00 CET) : effectifs gelés, dernières embauches de coachs, dernières activations de contrat', 'gold.hn_calendar [G:Calendar]'),
  ('hockeynation', 'j42', 'jour_saison', 42, null, 2, 'ligue', 'J42 : dernière journée de saison régulière ; dernier jour de paie', 'gold.hn_calendar [G:Calendar]'),
  ('hockeynation', 'j44', 'jour_saison', 44, null, 2, 'ligue', 'J44 : début des playoffs', 'gold.hn_calendar [G:Calendar]'),
  ('hockeynation', 'j49', 'jour_saison', 49, null, 2, 'académie', 'J49 : début de l''Import Draft (1 joueur de 14 ans révélé par jour pendant 6 jours)', 'gold.hn_calendar [G:Calendar]'),
  ('hockeynation', 'j51', 'jour_saison', 51, null, 2, 'transfert', 'J51 : ouverture fenêtre II', 'gold.hn_calendar [G:Calendar]'),
  ('hockeynation', 'j57', 'jour_saison', 57, null, 2, 'finances', 'J57 : plafond officiel de la saison suivante', 'gold.hn_calendar [G:Calendar]'),
  ('hockeynation', 'j61', 'jour_saison', 61, '21:00', 1, 'transfert', 'J61 : fermeture fenêtre II (21:00 CET)', 'gold.hn_calendar [G:Calendar]'),
  ('hockeynation', 'j63', 'jour_saison', 63, null, 1, 'académie', 'J63 : dernier jour : Youth Draft (pré-instructions 1 h avant), report du budget de scouting', 'gold.hn_calendar [G:Calendar]')
on conflict (game, rule_id) do update set
  declencheur = excluded.declencheur, jour_saison = excluded.jour_saison, heure = excluded.heure,
  priority = excluded.priority, category = excluded.category, modele = excluded.modele, source = excluded.source;
