-- Silver Team Soccer (football) : lecture des réponses de l'API du site (Supabase/PostgREST, /rest/v1/<table>)
-- capturées dans bronze.raw_pages (game = 'teamsoccer'). Règles du jeu : skills teamsoccer-*.
-- Particularité : chaque écran ne demande que quelques colonnes, et le filtre (team_id, series_id, cup_id) est
-- souvent dans l'adresse, pas dans la ligne. On extrait donc ces filtres de la requête, puis on fusionne,
-- par identifiant, la valeur la plus récente de chaque colonne (vues ts_teams, ts_matches, ts_player_snapshots).
-- Deux clubs sur le compte : chaque vue porte team_id.

create or replace view silver.ts_api with (security_invoker = true) as
select r.id as capture_id, r.captured_at,
       (r.captured_at at time zone 'Europe/Paris')::date as day,
       regexp_replace(split_part(r.source_url, '?', 1), '^https?://[^/]+/rest/v1/', '') as endpoint,
       nullif(split_part(r.source_url, '?', 2), '') as query,
       (substring(r.source_url from '[?&]team_id=eq\.([0-9]+)'))::int as q_team_id,
       (substring(r.source_url from '[?&]series_id=eq\.([0-9]+)'))::int as q_series_id,
       (substring(r.source_url from '[?&]cup_id=eq\.([0-9]+)'))::int as q_cup_id,
       (substring(r.source_url from '[?&](?:manager_id|user_id)=eq\.([0-9]+)'))::int as q_manager_id,
       r.payload->'body' as body
from bronze.raw_pages r
where r.game = 'teamsoccer' and r.source = 'api' and r.payload->>'status' = '200'
  and jsonb_typeof(r.payload->'body') = 'array';

-- Le manager connecté : ses préférences ne sont lues que pour lui.
create or replace view silver.ts_me with (security_invoker = true) as
select q_manager_id as manager_id
from silver.ts_api where endpoint = 'manager_preferences' and q_manager_id is not null
order by captured_at desc limit 1;

-- Équipes vues (toutes, adversaires compris) : dernière valeur connue de chaque colonne.
create or replace view silver.ts_teams with (security_invoker = true) as
with kv as (
  select distinct on ((t->>'team_id')::int, e.key) (t->>'team_id')::int as team_id, e.key, e.value
  from silver.ts_api a, jsonb_array_elements(a.body) t, jsonb_each(t) e
  where a.endpoint = 'teams' and t ? 'team_id' and e.value <> 'null'::jsonb
  order by (t->>'team_id')::int, e.key, a.captured_at desc
), m as (select team_id, jsonb_object_agg(key, value) as j from kv group by team_id)
select team_id, j->>'name' as name, (j->>'series_id')::int as series_id, (j->>'manager_id')::int as manager_id,
       (j->>'is_bot')::text in ('true', '1') as is_bot, (j->>'team_rating')::numeric as team_rating,
       case when j->>'team_morale' ~ '^[0-9.]+$' then (j->>'team_morale')::numeric end as team_morale,
       case when j->>'team_spirit' ~ '^[0-9.]+$' then (j->>'team_spirit')::numeric end as team_spirit,
       case when j->>'coach_level' ~ '^[0-9]+$' then (j->>'coach_level')::int end as coach_level,
       (j->>'fan_count')::int as fan_count, (j->>'country_id')::int as country_id,
       -- l'API renvoie parfois un libellé (« Normal », « poor ») au lieu d'un nombre
       j->>'team_spirit' as team_spirit_label, j->>'coach_level' as coach_level_label
from m;

-- Mes clubs : équipes renvoyées par la requête « teams?manager_id=eq.<moi> ».
-- (Pas de sous-requête latérale vers les séries : elle relisait bronze pour chaque ligne, 40 × 16 ms.)
create or replace view silver.ts_my_teams with (security_invoker = true) as
with mine as (
  select distinct (x->>'team_id')::int as team_id
  from silver.ts_api a cross join silver.ts_me me cross join lateral jsonb_array_elements(a.body) x
  where a.endpoint = 'teams' and a.q_manager_id = me.manager_id and x ? 'team_id'
), ser as (
  select distinct on ((b->>'series_id')::int) (b->>'series_id')::int as series_id, (b->>'division')::int as division, (b->>'region_id')::int as region_id
  from silver.ts_api sa, jsonb_array_elements(sa.body) b
  where sa.endpoint = 'series' and b ? 'division'
  order by (b->>'series_id')::int, sa.captured_at desc
)
select t.team_id, t.name, t.series_id, s.division, s.region_id, t.team_rating, t.team_morale, t.team_spirit, t.coach_level,
       t.coach_level_label
from mine join silver.ts_teams t using (team_id)
left join ser s on s.series_id = t.series_id;

-- Joueurs : un relevé par joueur et par jour de capture, colonnes fusionnées (team_id tiré de l'adresse).
-- `fitness` (0–100) = la Forme ; `form` = libellé (« Good », « 5 ») ; `rating` = OVR [skill teamsoccer-joueurs].
create or replace view silver.ts_player_snapshots with (security_invoker = true) as
with kv as (
  select distinct on ((p->>'player_id')::int, a.day, e.key)
         (p->>'player_id')::int as player_id, a.day, e.key, e.value, a.captured_at,
         a.q_team_id as team_id
  from silver.ts_api a, jsonb_array_elements(a.body) p, jsonb_each(p) e
  where a.endpoint = 'players' and a.q_team_id is not null and p ? 'player_id'
  order by (p->>'player_id')::int, a.day, e.key, a.captured_at desc
), m as (
  select player_id, day, max(team_id) as team_id, max(captured_at) as captured_at, jsonb_object_agg(key, value) as j
  from kv group by player_id, day
)
select day, captured_at, team_id, player_id,
       trim(concat_ws(' ', j->>'first_name', j->>'last_name')) as name, j->>'nickname' as nickname,
       j->>'position' as position, (j->>'age')::int as age, j->>'nationality' as nationality,
       (j->>'rating')::numeric as ovr, (j->>'fitness')::numeric as forme, j->>'form' as form_label,
       (j->>'value')::bigint as value, (j->>'wage')::int as wage, j->>'talent' as talent,
       (j->>'goalkeeper')::numeric as goalkeeper, (j->>'defense')::numeric as defense,
       (j->>'ball_control')::numeric as ball_control, (j->>'passing')::numeric as passing,
       (j->>'crosses')::numeric as crosses, (j->>'dribbling')::numeric as dribbling,
       (j->>'heading')::numeric as heading, (j->>'finishing')::numeric as finishing,
       (j->>'stamina')::numeric as stamina, (j->>'pace')::numeric as pace,
       coalesce((j->>'injury_days_remaining')::int, 0) as injury_days, (j->>'is_suspended')::bool as suspended,
       (j->>'season_yellow_cards')::int as yellow_cards, (j->>'shirt_number')::int as shirt_number,
       (j->>'official_matches_played')::int as official_matches, (j->>'official_goals')::int as official_goals,
       (j->>'official_assists')::int as official_assists, (j->>'official_tackles')::int as official_tackles
from m
where j ? 'goalkeeper';

-- Effectif actuel de mes clubs : joueurs présents dans la dernière capture de leur club.
-- zone = poste de l'API (GK/DEF/MID/FWD), sinon la plus haute de Gardien / Défense / Conduite / Finition
-- (égalités fréquentes à 60 dans l'équipe féminine) ; second_skill = 2e compétence technique,
-- indice du sous-rôle à lire avec le tableau du skill teamsoccer-joueurs (le guide ne donne pas la règle exacte).
-- CTE « materialized » (2026-10-30) : les vues silver lisent le JSON brut et le planificateur les estime à 1 ligne ;
-- sans elles, ts_player_snapshots était recalculé 19 fois et ts_my_teams 358 fois (4,4 s, timeouts en gold).
create or replace view silver.ts_players with (security_invoker = true) as
with snap as materialized (select * from silver.ts_player_snapshots),
last_day as (select team_id, max(day) as day from snap group by team_id),
mt as materialized (select team_id from silver.ts_my_teams)
select s.*,
       z.zone, z.second_skill, s.day as as_of
from snap s
join last_day l on l.team_id = s.team_id and l.day = s.day
join mt on mt.team_id = s.team_id
cross join lateral (
  select coalesce(case s.position when 'GK' then 'GB' when 'DEF' then 'DEF' when 'MID' then 'MIL' when 'FWD' then 'ATT' end,
         (select case k when 'goalkeeper' then 'GB' when 'defense' then 'DEF' when 'dribbling' then 'MIL' else 'ATT' end
          from (values ('goalkeeper', s.goalkeeper), ('defense', s.defense), ('dribbling', s.dribbling), ('finishing', s.finishing)) v(k, x)
          order by x desc nulls last limit 1)) as zone,
         (select k from (values ('goalkeeper', s.goalkeeper), ('defense', s.defense), ('ball_control', s.ball_control), ('passing', s.passing),
                                ('crosses', s.crosses), ('dribbling', s.dribbling), ('heading', s.heading), ('finishing', s.finishing)) v(k, x)
          order by x desc nulls last offset 1 limit 1) as second_skill
) z;

-- Entraînement : réglage actuel par joueur (compétence, intensité 0–100) et progression fractionnaire [P:Entraînement].
create or replace view silver.ts_training with (security_invoker = true) as
select distinct on ((t->>'player_id')::int)
       a.day, a.captured_at, (t->>'player_id')::int as player_id,
       t->>'training_type' as training_type, (t->>'training_intensity')::int as intensity, t->>'last_trained_type' as last_trained_type,
       (t->>'skill_progress')::numeric as skill_progress, (t->>'last_change')::numeric as last_change,
       (t->>'stamina_progress')::numeric as stamina_progress, (t->>'stamina_last_change')::numeric as stamina_last_change,
       (t->>'pace_progress')::numeric as pace_progress, (t->>'pace_last_change')::numeric as pace_last_change
from silver.ts_api a, jsonb_array_elements(a.body) t
where a.endpoint = 'player_training_assignments' and t ? 'training_type'
order by (t->>'player_id')::int, a.captured_at desc;

-- Finances : un relevé par club et par jour (lignes de la semaine en cours et cumuls de la saison) [P:Finances].
create or replace view silver.ts_finances with (security_invoker = true) as
select distinct on ((f->>'team_id')::int, a.day)
       a.day, a.captured_at, (f->>'team_id')::int as team_id,
       (f->>'cash_balance')::bigint as balance, (f->>'last_weekly_process')::timestamptz as last_weekly_process,
       (f->>'weekly_income')::bigint as weekly_income, (f->>'weekly_expenses')::bigint as weekly_expenses,
       (f->>'match_income')::bigint as match_income, (f->>'prize_income')::bigint as prize_income,
       (f->>'player_sales_income')::bigint as player_sales_income, (f->>'other_income')::bigint as other_income,
       (f->>'wages_expenses')::bigint as wages_expenses, (f->>'stadium_maintenance_expenses')::bigint as stadium_maintenance,
       (f->>'stadium_building_expenses')::bigint as stadium_building, (f->>'new_signings_expenses')::bigint as new_signings,
       (f->>'staff_expenses')::bigint as staff_expenses, (f->>'youth_expenses')::bigint as youth_expenses,
       (f->>'other_expenses')::bigint as other_expenses, (f->>'total_wages')::bigint as total_wages,
       (f->>'total_match_income')::bigint as total_match_income, (f->>'total_player_sales')::bigint as total_player_sales,
       (f->>'total_new_signings')::bigint as total_new_signings, (f->>'total_stadium_building')::bigint as total_stadium_building,
       (f->>'total_stadium_maintenance')::bigint as total_stadium_maintenance, (f->>'total_other_income')::bigint as total_other_income
from silver.ts_api a, jsonb_array_elements(a.body) f
where a.endpoint = 'team_finances' and f ? 'weekly_income'
order by (f->>'team_id')::int, a.day, a.captured_at desc;

-- Stade : places par type (dernière capture complète par club) [G:Stades et spectateurs].
create or replace view silver.ts_stadiums with (security_invoker = true) as
select distinct on (a.q_team_id)
       a.day, a.q_team_id as team_id, s->>'name' as name, (s->>'capacity')::int as capacity,
       (s->>'seats_standing')::int as seats_standing, (s->>'seats_basic')::int as seats_basic,
       (s->>'seats_covered')::int as seats_covered, (s->>'seats_vip')::int as seats_vip
from silver.ts_api a, jsonb_array_elements(a.body) s
where a.endpoint = 'stadiums' and a.q_team_id is not null and s ? 'seats_vip'
order by a.q_team_id, a.captured_at desc;

-- Matchs : colonnes fusionnées par match (series_id / cup_id repris de l'adresse quand la ligne ne les porte pas).
create or replace view silver.ts_matches with (security_invoker = true) as
with rows as (
  select a.captured_at,
         x || jsonb_strip_nulls(jsonb_build_object('series_id', case when not x ? 'series_id' then a.q_series_id end,
                                                   'cup_id', case when not x ? 'cup_id' then a.q_cup_id end)) as x
  from silver.ts_api a, jsonb_array_elements(a.body) x
  where a.endpoint = 'matches' and x ? 'match_id_int'
), kv as (
  select distinct on ((x->>'match_id_int')::bigint, e.key) (x->>'match_id_int')::bigint as match_id, e.key, e.value
  from rows, jsonb_each(x) e
  where e.value <> 'null'::jsonb
  order by (x->>'match_id_int')::bigint, e.key, captured_at desc
), m as (select match_id, jsonb_object_agg(key, value) as j from kv group by match_id)
select m.match_id, (j->>'match_date')::timestamptz as match_date,
       ((j->>'match_date')::timestamptz at time zone 'Europe/Paris') as match_date_paris,
       j->>'status' as status, (j->>'home_team_id')::int as home_team_id, (j->>'away_team_id')::int as away_team_id,
       ht.name as home_team, at.name as away_team,
       (j->>'home_score')::int as home_score, (j->>'away_score')::int as away_score,
       (j->>'home_penalties')::int as home_penalties, (j->>'away_penalties')::int as away_penalties,
       (j->>'series_id')::int as series_id, (j->>'cup_id')::int as cup_id, (j->>'cup_round')::int as cup_round,
       case when (j->>'is_friendly')::bool then 'amical'
            when (j->>'is_promotion')::bool then 'barrage'
            when j ? 'cup_id' then 'coupe'
            when j ? 'series_id' then 'ligue'
            when j ? 'custom_tournament_id' or j ? 'room_challenge_id' then 'autre'
            else 'inconnu' end as competition,
       mine.team_id as my_team_id,
       case when mine.team_id = (j->>'home_team_id')::int then 'domicile' when mine.team_id is not null then 'extérieur' end as venue
from m
left join silver.ts_teams ht on ht.team_id = (j->>'home_team_id')::int
left join silver.ts_teams at on at.team_id = (j->>'away_team_id')::int
left join silver.ts_my_teams mine on mine.team_id in ((j->>'home_team_id')::int, (j->>'away_team_id')::int);

-- Composition enregistrée pour un match (formation, style, consignes par zone, banc et remplacements) [skill teamsoccer-match].
create or replace view silver.ts_match_lineups with (security_invoker = true) as
select distinct on (a.q_team_id, coalesce((l->>'match_id')::bigint, (substring(a.query from 'match_id=eq\.([0-9]+)'))::bigint))
       a.day, a.q_team_id as team_id,
       coalesce((l->>'match_id')::bigint, (substring(a.query from 'match_id=eq\.([0-9]+)'))::bigint) as match_id,
       l->>'formation' as formation, l->>'play_style' as play_style, l->'player_positions' as player_positions,
       l->'tactical_orders' as tactical_orders, l->'substitutes' as player_orders, l->'bench' as bench,
       (l->>'updated_at')::timestamptz as updated_at
from silver.ts_api a, jsonb_array_elements(a.body) l
where a.endpoint = 'match_lineups' and a.q_team_id is not null and l ? 'formation'
order by a.q_team_id, coalesce((l->>'match_id')::bigint, (substring(a.query from 'match_id=eq\.([0-9]+)'))::bigint), a.captured_at desc;

-- Compositions par défaut enregistrées (Premium : jusqu'à 5).
create or replace view silver.ts_lineups with (security_invoker = true) as
select distinct on (a.q_team_id, l->>'slot_name')
       a.day, a.q_team_id as team_id, l->>'slot_name' as slot_name, (l->>'is_default')::bool as is_default,
       l->>'formation_name' as formation, l->>'play_style' as play_style, l->'positions' as positions,
       l->'substitutes' as player_orders, l->'bench' as bench
from silver.ts_api a, jsonb_array_elements(a.body) l
where a.endpoint = 'lineups' and a.q_team_id is not null and l ? 'slot_name'
order by a.q_team_id, l->>'slot_name', a.captured_at desc;

-- Classement de la ligue de chacun de mes clubs, recalculé depuis les matchs joués (3 pts victoire, 1 nul).
-- Départage officiel : skill teamsoccer-saison ; ici points, différence, buts marqués.
create or replace view silver.ts_standings with (security_invoker = true) as
with g as (
  select mt.team_id as my_team_id, m.series_id, m.home_team_id as team_id, m.home_score as gf, m.away_score as ga
  from silver.ts_matches m join silver.ts_my_teams mt on mt.series_id = m.series_id
  where m.competition = 'ligue' and m.status in ('finished', 'played') and m.home_score is not null
  union all
  select mt.team_id, m.series_id, m.away_team_id, m.away_score, m.home_score
  from silver.ts_matches m join silver.ts_my_teams mt on mt.series_id = m.series_id
  where m.competition = 'ligue' and m.status in ('finished', 'played') and m.away_score is not null
), t as (
  select my_team_id, series_id, team_id, count(*) as played,
         count(*) filter (where gf > ga) as wins, count(*) filter (where gf = ga) as draws, count(*) filter (where gf < ga) as losses,
         sum(gf) as goals_for, sum(ga) as goals_against, sum(gf - ga) as goal_difference,
         sum(case when gf > ga then 3 when gf = ga then 1 else 0 end) as points
  from g group by my_team_id, series_id, team_id
)
select t.*, tm.name as team, rank() over (partition by t.my_team_id order by t.points desc, t.goal_difference desc, t.goals_for desc) as position,
       t.team_id = t.my_team_id as is_mine
from t left join silver.ts_teams tm on tm.team_id = t.team_id;

-- Marché : chaque annonce vue, dernière capture, joueur à plat (compétences visibles en vente).
create or replace view silver.ts_transfer_listings with (security_invoker = true) as
select distinct on ((l->>'id')::int)
       a.captured_at as seen_at, (l->>'id')::int as listing_id, l->>'listing_type' as listing_type,
       (l->>'asking_price')::bigint as asking_price, (l->>'bids')::int as bids, (l->>'last_bidder_team_id')::int as last_bidder_team_id,
       (l->>'deadline')::timestamptz as deadline, l->'seller_team'->>'name' as seller,
       (l->'player'->>'player_id')::int as player_id,
       trim(concat_ws(' ', l->'player'->>'first_name', l->'player'->>'last_name')) as name,
       l->'player'->>'position' as position, (l->'player'->>'age')::int as age, l->'player'->>'nationality' as nationality,
       (l->'player'->>'rating')::numeric as ovr, (l->'player'->>'fitness')::numeric as forme, (l->'player'->>'value')::bigint as value,
       (l->'player'->>'goalkeeper')::numeric as goalkeeper, (l->'player'->>'defense')::numeric as defense,
       (l->'player'->>'ball_control')::numeric as ball_control, (l->'player'->>'passing')::numeric as passing,
       (l->'player'->>'crosses')::numeric as crosses, (l->'player'->>'dribbling')::numeric as dribbling,
       (l->'player'->>'heading')::numeric as heading, (l->'player'->>'finishing')::numeric as finishing,
       (l->'player'->>'stamina')::numeric as stamina, (l->'player'->>'pace')::numeric as pace
from silver.ts_api a, jsonb_array_elements(a.body) l
where a.endpoint = 'transfer_listings' and l ? 'player' and jsonb_typeof(l->'player') = 'object'
order by (l->>'id')::int, a.captured_at desc;

-- Mes enchères en cours (annonces sur lesquelles un de mes clubs a enchéri).
create or replace view silver.ts_my_bids with (security_invoker = true) as
select distinct on ((substring(a.query from 'bidder_team_id=eq\.([0-9]+)'))::int, (b->>'transfer_listing_id')::int)
       a.day, (substring(a.query from 'bidder_team_id=eq\.([0-9]+)'))::int as team_id, (b->>'transfer_listing_id')::int as listing_id
from (select * from silver.ts_api where endpoint = 'transfer_bids' and query like '%bidder_team_id=eq.%') a
cross join lateral jsonb_array_elements(a.body) b
where a.captured_at = (select max(captured_at) from silver.ts_api x where x.endpoint = 'transfer_bids' and x.query = a.query)
order by (substring(a.query from 'bidder_team_id=eq\.([0-9]+)'))::int, (b->>'transfer_listing_id')::int, a.captured_at desc;

-- Académie : une ligne par club (révélations du jour) et une par jeune (compétences révélées) [G:Académie des Jeunes].
create or replace view silver.ts_youth_academies with (security_invoker = true) as
select distinct on (a.q_team_id)
       a.day, a.q_team_id as team_id, (y->>'id')::int as academy_id, (y->>'daily_reveal_date')::date as daily_reveal_date,
       (y->>'daily_reveal_count')::int as daily_reveal_count, (y->>'fully_revealed_count')::int as fully_revealed_count
from silver.ts_api a, jsonb_array_elements(a.body) y
where a.endpoint = 'youth_academies' and a.q_team_id is not null and y ? 'daily_reveal_count'
order by a.q_team_id, a.captured_at desc;

create or replace view silver.ts_youth_players with (security_invoker = true) as
select distinct on ((p->>'id')::int)
       a.day, ya.team_id, (p->>'academy_id')::int as academy_id, (p->>'id')::int as youth_id,
       trim(concat_ws(' ', p->>'first_name', p->>'last_name')) as name, (p->>'age')::int as age, p->>'position' as position,
       p->>'talent' as talent, (p->>'is_high_performance')::bool as is_high_performance,
       p->'revealed_skills' as revealed_skills, jsonb_array_length(p->'revealed_skills') as revealed_count,
       (p->>'last_reveal_date')::date as last_reveal_date,
       (p->>'goalkeeper')::numeric as goalkeeper, (p->>'defense')::numeric as defense, (p->>'ball_control')::numeric as ball_control,
       (p->>'passing')::numeric as passing, (p->>'crosses')::numeric as crosses, (p->>'dribbling')::numeric as dribbling,
       (p->>'heading')::numeric as heading, (p->>'finishing')::numeric as finishing,
       (p->>'stamina')::numeric as stamina, (p->>'pace')::numeric as pace
from silver.ts_api a
cross join lateral jsonb_array_elements(a.body) p
left join silver.ts_youth_academies ya on ya.academy_id = (p->>'academy_id')::int
where a.endpoint = 'youth_academy_players' and p ? 'revealed_skills'
order by (p->>'id')::int, a.captured_at desc;

-- Centre de Haute Performance : paiements TSC de la saison par club, et solde de TSC du compte [P:Haute Performance].
create or replace view silver.ts_hpc with (security_invoker = true) as
select distinct on ((h->>'team_id')::int, (h->>'season')::int)
       a.day, (h->>'team_id')::int as team_id, (h->>'season')::int as season, h->>'status' as status,
       (h->>'total_tsc')::int as total_tsc, (h->>'last_payment_week')::int as last_payment_week,
       (h->>'options_week')::int as options_week, h->'week_options' as week_options, h->'chosen_skills' as chosen_skills,
       (h->>'youth_player_id')::int as youth_player_id,
       (select (c->>'ts_credits')::int from silver.ts_api x cross join silver.ts_me me, jsonb_array_elements(x.body) c
        where x.endpoint = 'managers' and x.q_manager_id = me.manager_id and c ? 'ts_credits'
        order by x.captured_at desc limit 1) as account_tsc
from silver.ts_api a, jsonb_array_elements(a.body) h
where a.endpoint = 'high_performance_scouts' and h ? 'total_tsc'
order by (h->>'team_id')::int, (h->>'season')::int, a.captured_at desc;

-- Annonces de l'admin (page Communauté), version anglaise datée.
create or replace view silver.ts_news with (security_invoker = true) as
select distinct on ((n->>'id')::int)
       (n->>'id')::int as news_id, (n->>'created_at')::timestamptz as created_at,
       regexp_replace(n->>'title', '^[•\s]+', '') as title, n->>'content' as content
from silver.ts_api a, jsonb_array_elements(a.body) n
where a.endpoint = 'community_news' and n ? 'created_at' and n ? 'content'
order by (n->>'id')::int, a.captured_at desc;

-- Forum : messages avec contenu, auteur et niveau d'administration (veille).
-- `is_admin` de l'API est un niveau : 10 = administrateurs (Admin-Dev, Admin-PIPO68), 2 à 4 = modérateurs.
create or replace view silver.ts_forum_posts with (security_invoker = true) as
with u as (
  select (m->>'user_id')::int as user_id,
         (array_agg(m->>'username' order by a.captured_at desc) filter (where m ? 'username'))[1] as username,
         max(case when (m->>'is_admin') ~ '^[0-9]+$' then (m->>'is_admin')::int when (m->>'is_admin') = 'true' then 10 end) as admin_level
  from silver.ts_api a, jsonb_array_elements(a.body) m
  where a.endpoint = 'managers' and m ? 'user_id'
  group by (m->>'user_id')::int
), th as (
  select distinct on ((t->>'id')::int) (t->>'id')::int as thread_id, t->>'title' as title, (t->>'forum_id')::int as forum_id
  from silver.ts_api a, jsonb_array_elements(a.body) t
  where a.endpoint = 'forum_threads' and t ? 'title'
  order by (t->>'id')::int, a.captured_at desc
)
select distinct on ((p->>'id')::int)
       (p->>'id')::int as post_id, (p->>'thread_id')::int as thread_id, th.title as thread_title, th.forum_id,
       (p->>'created_at')::timestamptz as created_at, (p->>'user_id')::int as user_id, u.username,
       coalesce(u.admin_level >= 10, false) as is_admin,
       p->>'content' as content, u.admin_level
from silver.ts_api a
cross join lateral jsonb_array_elements(a.body) p
left join u on u.user_id = (p->>'user_id')::int
left join th on th.thread_id = (p->>'thread_id')::int
where a.endpoint = 'forum_posts' and p ? 'content'
order by (p->>'id')::int, a.captured_at desc;
