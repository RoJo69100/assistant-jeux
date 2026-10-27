-- BasketVibe : tableaux de saisie tactique (format R-10 validé le 2026-10-27), sans agent.
-- Source : dernier export de la page du match (`/fixtures|cup-fixtures|friendlies/<id>/match-tactics`)
-- pour chaque match à venir (ligue, coupe, amical). Ordre de l'écran : PG, SG, SF, PF, C puis nom.
-- Tiers de l'API 0–4 = écran 1–5 (+1). Composition : sauvegardée pour le match, sinon preset choisi,
-- sinon composition du club. area_step : 3 = Middle/Neutral, 5 = Rim (constatés) ; 1 = Perimeter (déduit, à vérifier).
--   select * from gold.bv_saisie_joueurs where match_day = '2026-10-28' order by kind, ordre;
--   select * from gold.bv_saisie_adversaires where match_day = '2026-10-28' order by kind, ordre;

create or replace view gold.bv_saisie_matchs as
with mt as (
  select distinct on (fixture_id)
    fixture_id, kind, captured_at, b
  from (
    select r.captured_at, r.payload->'body' b,
           (regexp_match(r.source_url, '/(fixtures|cup-fixtures|friendlies)/([0-9a-f-]{36})/match-tactics$'))[2] fixture_id,
           case (regexp_match(r.source_url, '/(fixtures|cup-fixtures|friendlies)/'))[1]
             when 'fixtures' then 'ligue' when 'cup-fixtures' then 'coupe' else 'amical' end kind
    from bronze.raw_pages r
    where r.game = 'basketvibe' and r.source_url ~ '/match-tactics$'
  ) x
  order by fixture_id, captured_at desc
)
select
  mt.fixture_id, mt.kind,
  (mt.b->'preview'->>'match_day')::date match_day,
  mt.b->'preview'->>'kickoff_time' kickoff,
  coalesce((mt.b->>'is_home')::boolean, false) is_home,
  case when (mt.b->>'is_home')::boolean then mt.b->'preview'->'away_team'->>'name'
       else mt.b->'preview'->'home_team'->>'name' end opponent,
  mt.b->>'fixture_status' status,
  coalesce((mt.b->>'has_saved_match_tactics')::boolean, false) saved,
  coalesce(
    case when (mt.b->>'has_saved_match_tactics')::boolean then mt.b->'saved_lineup_by_quarter' end,
    (select p->'lineup_by_quarter' from jsonb_array_elements(mt.b->'presets') p
      where p->>'id' = mt.b->>'selected_preset_id'),
    mt.b->'club_lineup_by_quarter') lineup,
  (select p->>'name' from jsonb_array_elements(mt.b->'presets') p
    where p->>'id' = mt.b->>'selected_preset_id') preset,
  mt.b->'player_directives' directives,
  mt.b->'defensive_focus' defensive_focus,
  case when (mt.b->>'is_home')::boolean then mt.b->'preview'->'home_players' else mt.b->'preview'->'away_players' end my_players,
  case when (mt.b->>'is_home')::boolean then mt.b->'preview'->'away_players' else mt.b->'preview'->'home_players' end opp_players,
  mt.captured_at at time zone 'Europe/Paris' export_paris
from mt;

create or replace view gold.bv_saisie_joueurs as
with s as (select * from gold.bv_saisie_matchs),
pl as (
  select s.fixture_id, s.kind, s.match_day, s.opponent, s.saved, s.preset, s.export_paris, s.lineup, s.directives,
         p->>'player_id' player_id, p->>'last_name' nom, p->>'position' poste
  from s, jsonb_array_elements(s.my_players) p
),
q as (  -- poste joué par quart-temps (indice 0..4 = Q1..Q4, Prol.), emplacement 0..4 = PG..C
  select pl.fixture_id, pl.player_id, qi.i, (array['PG','SG','SF','PF','C'])[sl.j] slot
  from pl,
       jsonb_array_elements(pl.lineup) with ordinality qi(arr, i),
       jsonb_array_elements_text(qi.arr) with ordinality sl(pid, j)
  where sl.pid = pl.player_id
)
select
  pl.kind, pl.match_day, pl.opponent,
  row_number() over (partition by pl.fixture_id
    order by array_position(array['PG','SG','SF','PF','C'], pl.poste), pl.nom) ordre,
  pl.nom joueur, pl.poste,
  coalesce(max(q.slot) filter (where q.i = 1), '—') q1,
  coalesce(max(q.slot) filter (where q.i = 2), '—') q2,
  coalesce(max(q.slot) filter (where q.i = 3), '—') q3,
  coalesce(max(q.slot) filter (where q.i = 4), '—') q4,
  coalesce(max(q.slot) filter (where q.i = 5), '—') prol,
  12 * count(q.i) filter (where q.i <= 4)
    || case when bool_or(q.i = 5) then ' (+5)' else '' end minutes,
  (d->>'offensive_focus_tier')::int + 1 off_focus,
  (d->>'role_tier')::int + 1 role,
  (d->>'shot_tier')::int + 1 tir,
  (d->>'defense_tier')::int + 1 agress,
  pl.saved sauvegarde_match, pl.preset, pl.export_paris, pl.fixture_id
from pl
left join q on q.fixture_id = pl.fixture_id and q.player_id = pl.player_id
left join lateral (select d from jsonb_array_elements(pl.directives) d where d->>'player_id' = pl.player_id) dd on true
group by pl.fixture_id, pl.kind, pl.match_day, pl.opponent, pl.nom, pl.poste, pl.saved, pl.preset, pl.export_paris, d;

create or replace view gold.bv_saisie_adversaires as
with s as (select * from gold.bv_saisie_matchs),
op as (
  select s.fixture_id, s.kind, s.match_day, s.opponent, s.export_paris, s.defensive_focus,
         p->>'player_id' player_id, p->>'last_name' nom, p->>'position' poste
  from s, jsonb_array_elements(s.opp_players) p
)
select
  op.kind, op.match_day, op.opponent,
  row_number() over (partition by op.fixture_id
    order by array_position(array['PG','SG','SF','PF','C'], op.poste), op.nom) ordre,
  op.nom adversaire, op.poste,
  case coalesce(f->>'focus', 'normal')
    when 'give_up' then 1 when 'light' then 2 when 'normal' then 3 when 'intense' then 4 when 'off' then 5 end focus,
  case coalesce(f->>'area_step', '3')
    when '1' then 'Perimeter (1)' when '3' then 'Middle (3)' when '5' then 'Rim (5)'
    else 'pas ' || (f->>'area_step') end zone,
  op.export_paris, op.fixture_id
from op
left join lateral (select f from jsonb_array_elements(op.defensive_focus) f where f->>'opponent_player_id' = op.player_id) ff on true;
