-- Team Soccer : vues de décision (2026-10-27), pour remplacer les agents sur les tableaux récurrents
-- (rétro du 2026-10-27, règles apprises 16, 17, 19 ; CLAUDE.md « Vitesse » 1 et 4).
-- Jugement d'un joueur = compétences nommées au poste, jamais l'OVR [skill teamsoccer-joueurs § Compétences clés par poste].
-- Compétence clé par zone : GB Gardien · DEF Défense · MIL Conduite (dribbling) · ATT Finition ; Contrôle = 2e partout.
-- Valeur au match = compétence × (0,70 + 0,30 × Forme / 100) [F:2026-06-27 Admin-Dev].

-- Dépenses décidées mais pas encore visibles dans le dernier relevé finances (achat de places, enchère posée…).
-- Je les inscris dès que l'utilisateur dit « j'ai acheté / j'ai enchéri » ; settled = true quand le relevé les montre.
create table if not exists silver.ts_depenses_decidees (
  id bigint generated always as identity primary key,
  team_id int not null,
  decided_on date not null default current_date,
  label text not null,
  amount numeric not null,
  settled boolean not null default false,
  source text
);
alter table silver.ts_depenses_decidees enable row level security;

-- Capacité d'investissement = solde − 2 semaines de (salaires + entretien) − dépenses décidées non encore relevées
-- (règle de la fiche finances ; règle apprise 16 : un achat n'est proposé que si cette capacité le couvre).
create or replace view gold.ts_capacite_invest with (security_invoker = true) as
with d as (
  select team_id, sum(amount) as decided, string_agg(label || ' ' || amount::bigint, ' ; ' order by decided_on) as decided_list
  from silver.ts_depenses_decidees where not settled group by team_id
)
select fs.team_id, fs.team, fs.as_of as finances_as_of, fs.balance,
       fs.wage_bill, fs.stadium_maintenance,
       2 * (fs.wage_bill + coalesce(fs.stadium_maintenance, 0)) as reserve_2_weeks,
       coalesce(d.decided, 0) as decided_not_settled, d.decided_list,
       fs.balance - 2 * (fs.wage_bill + coalesce(fs.stadium_maintenance, 0)) - coalesce(d.decided, 0) as capacite_invest,
       current_date - fs.as_of as finances_age_days
from gold.ts_finance_status fs
left join d on d.team_id = fs.team_id;

-- Stade : les 4 types comparés pour chaque club (rentabilité et nombre de places achetables avec la capacité).
-- Le relevé du stade peut précéder un achat déjà fait : voir stadium_as_of et ts_depenses_decidees.
create or replace view gold.ts_stade_choix with (security_invoker = true) as
select p.team_id, p.team, p.seat_type, p.seats, p.room_left, p.price,
       round(p.revenue * p.attendance_rate * 0.94, 2) as net_per_seat_per_home_match,
       p.home_matches_to_repay,
       greatest(0, least(p.room_left, floor(greatest(c.capacite_invest, 0) / p.price)))::int as seats_affordable,
       greatest(0, least(p.room_left, floor(greatest(c.capacite_invest, 0) / p.price))) * p.price as cost_affordable,
       rank() over (partition by p.team_id order by p.home_matches_to_repay nulls last) as rank_payback,
       p.home_league_left, c.capacite_invest,
       (select max(day) from silver.ts_stadiums s where s.team_id = p.team_id) as stadium_as_of
from gold.ts_stadium_payback p
left join gold.ts_capacite_invest c on c.team_id = p.team_id
where p.room_left > 0;

-- Effectif actuel (dernier relevé de chaque club), compétence clé du poste, valeur au match, rang dans la zone.
-- Titulaires par zone = formation de la dernière composition enregistrée (à défaut 1-4-4-2).
-- CTE « materialized » (2026-10-30) : chaque vue silver (JSON brut) n'est lue qu'une fois ; avant, la jointure latérale
-- relisait ts_transfer_listings pour chaque joueur et la vue dépassait le délai de l'API.
create or replace view gold.ts_effectif_bilan with (security_invoker = true) as
with pl as materialized (select * from silver.ts_players),
mts as materialized (select team_id, name from silver.ts_my_teams),
tls as materialized (select player_id, seller, deadline from silver.ts_transfer_listings where deadline > now() - interval '30 days'),
last as (select team_id, max(as_of) as as_of from pl group by team_id),
f as materialized (
  select distinct on (team_id) team_id, formation from silver.ts_match_lineups
  where formation ~ '^1-\d-\d-\d$' order by team_id, updated_at desc nulls last, day desc
),
need as (
  select mt.team_id, coalesce(f.formation, '1-4-4-2') as formation, z.zone, z.n
  from mts mt left join f on f.team_id = mt.team_id
  cross join lateral (values
    ('GB', 1), ('DEF', split_part(coalesce(f.formation, '1-4-4-2'), '-', 2)::int),
    ('MIL', split_part(coalesce(f.formation, '1-4-4-2'), '-', 3)::int), ('ATT', split_part(coalesce(f.formation, '1-4-4-2'), '-', 4)::int)
  ) z(zone, n)
),
p as (
  select p.*, case p.zone when 'GB' then 'Gardien' when 'DEF' then 'Défense' when 'MIL' then 'Conduite' else 'Finition' end as key_name,
         case p.zone when 'GB' then p.goalkeeper when 'DEF' then p.defense when 'MIL' then p.dribbling else p.finishing end as key_skill,
         coalesce(p.injury_days, 0) > 0 or coalesce(p.suspended, false) or s.player_id is not null as unavailable,
         s.player_id is not null as on_sale
  from pl p join last l on l.team_id = p.team_id and l.as_of = p.as_of
  join mts t on t.team_id = p.team_id
  -- Vendu ou mis en vente par nous : il reste dans l'export d'effectif (Min-ji Mori le 2026-10-27).
  left join lateral (select tl.player_id from tls tl
                     where tl.player_id = p.player_id and tl.seller = t.name and tl.deadline > p.captured_at limit 1) s on true
)
select p.team_id, mt.name as team, p.zone, p.player_id, p.name, p.age, p.key_name, p.key_skill, p.ball_control as controle,
       p.second_skill,
       case p.zone
         when 'DEF' then case when p.second_skill = 'ball_control' then 'LAT (indice)' when p.second_skill = 'crosses' then 'WB (indice)' else 'DC (indice)' end
         when 'MIL' then case p.second_skill when 'defense' then 'MD (indice)' when 'crosses' then 'ML (indice)' when 'finishing' then 'MO (indice)' else 'MC (indice)' end
         when 'ATT' then case when p.second_skill = 'heading' then 'AC tête (indice)' else 'DR (indice)' end
         else 'GB' end as sous_role,
       p.forme, round(p.key_skill * (0.70 + 0.30 * coalesce(p.forme, 100) / 100.0), 1) as key_at_match,
       p.unavailable, p.injury_days, p.suspended, p.yellow_cards,
       rank() over (partition by p.team_id, p.zone order by p.unavailable, p.key_skill desc, p.ball_control desc) as rank_in_zone,
       n.n as starters_needed, n.formation,
       case when p.on_sale then 'en vente' when p.unavailable then 'indisponible'
            when rank() over (partition by p.team_id, p.zone order by p.unavailable, p.key_skill desc, p.ball_control desc) <= n.n then 'titulaire'
            when rank() over (partition by p.team_id, p.zone order by p.unavailable, p.key_skill desc, p.ball_control desc) <= n.n + 1 then 'remplaçant'
            else 'surplus' end as statut,
       p.value, p.wage, p.ovr, count(*) filter (where not p.on_sale) over (partition by p.team_id) as squad_size, p.as_of, p.on_sale
from p join mts mt on mt.team_id = p.team_id
join need n on n.team_id = p.team_id and n.zone = p.zone;

-- Marché : annonces encore ouvertes dont la compétence clé dépasse le plus faible titulaire de la zone,
-- avec le prix demandé comparé à la capacité. asking_price = prix de départ (une enchère peut monter).
create or replace view gold.ts_marche_cibles with (security_invoker = true) as
with eb as materialized (select team_id, zone, statut, name, key_skill, squad_size from gold.ts_effectif_bilan),
c as materialized (select team_id, team, capacite_invest from gold.ts_capacite_invest),
l as materialized (
  select distinct on (listing_id) * from silver.ts_transfer_listings
  where deadline > now() order by listing_id, seen_at desc
),
lz as (
  select l.*, case l.position when 'GK' then 'GB' when 'DEF' then 'DEF' when 'MID' then 'MIL' else 'ATT' end as zone,
         case l.position when 'GK' then l.goalkeeper when 'DEF' then l.defense when 'MID' then l.dribbling else l.finishing end as key_skill
  from l
),
weak as (
  select team_id, zone, min(key_skill) as weakest_starter_key,
         (array_agg(name order by key_skill))[1] as weakest_starter
  from eb where statut = 'titulaire' group by team_id, zone
)
select w.team_id, c.team, lz.zone, lz.listing_id, lz.listing_type, lz.name, lz.age, lz.key_skill, lz.ball_control as controle,
       lz.forme, w.weakest_starter, w.weakest_starter_key, lz.key_skill - w.weakest_starter_key as gain_key,
       lz.asking_price, lz.bids, lz.deadline at time zone 'Europe/Paris' as deadline_paris,
       c.capacite_invest, lz.asking_price <= c.capacite_invest as financable,
       (select max(squad_size) from eb e where e.team_id = w.team_id) as squad_size,
       lz.seen_at
from lz join weak w on w.zone = lz.zone
join c on c.team_id = w.team_id
where lz.key_skill > w.weakest_starter_key
  and coalesce(lz.last_bidder_team_id, -1) <> w.team_id
  -- Ben Ahmed Donkey (15858, équipe féminine) achète sur le marché féminin, Chomelix Cows sur le masculin (silver 014).
  and lz.market = case when w.team_id = 15858 then 'feminin' else 'masculin' end;

-- Académie : verdict par jeune (dernier relevé de chaque club), comparé au plus faible titulaire de sa zone.
-- Complet (10 révélées) : MONTER si la compétence clé atteint le plus faible titulaire, sinon VENDRE.
-- Incomplet : RÉVÉLER la compétence clé si cachée ; VENDRE si elle est révélée et sous le plus faible titulaire ;
-- sinon RÉVÉLER la compétence suivante du poste [skill teamsoccer-joueurs § Compétences clés par poste].
create or replace view gold.ts_academie_verdict with (security_invoker = true) as
with last as (select team_id, max(day) as day from silver.ts_youth_players group by team_id),
eb as materialized (select * from gold.ts_effectif_bilan),
sold as materialized (select tl.name, t.team_id from silver.ts_transfer_listings tl join silver.ts_my_teams t on t.name = tl.seller),
y as (
  select y.*, case y.position when 'GK' then 'GB' when 'DEF' then 'DEF' when 'MID' then 'MIL' else 'ATT' end as zone,
         case y.position when 'GK' then 'goalkeeper' when 'DEF' then 'defense' when 'MID' then 'dribbling' else 'finishing' end as key_col,
         case y.position
           when 'GK' then array['goalkeeper', 'ball_control', 'passing', 'stamina', 'pace']
           when 'DEF' then array['defense', 'ball_control', 'heading', 'passing', 'pace', 'dribbling']
           when 'MID' then array['dribbling', 'ball_control', 'passing', 'defense', 'stamina', 'crosses']
           else array['finishing', 'ball_control', 'heading', 'dribbling', 'pace'] end as order_cols
  from silver.ts_youth_players y join last l on l.team_id = y.team_id and l.day = y.day
  where not coalesce(y.is_high_performance, false)
    -- déjà monté en équipe première ou vendu : la page académie le garde parfois (Min-ji Mori le 2026-10-27)
    and not exists (select 1 from eb where eb.team_id = y.team_id and eb.name = y.name)
    and not exists (select 1 from sold s where s.team_id = y.team_id and s.name = y.name)
),
v as (
  select y.*, case when y.revealed_skills ? y.key_col then (to_jsonb(y) ->> y.key_col)::numeric end as key_skill,
         (select k from unnest(y.order_cols || array['goalkeeper', 'defense', 'ball_control', 'passing', 'crosses', 'dribbling',
                                                      'heading', 'finishing', 'stamina', 'pace']) with ordinality u(k, i)
          where not y.revealed_skills ? k order by i limit 1) as next_reveal
  from y
),
weak as (select team_id, zone, min(key_skill) as weakest_starter_key, (array_agg(name order by key_skill))[1] as weakest_starter
         from eb where statut = 'titulaire' group by team_id, zone),
sq as (select team_id, max(squad_size) as squad_size from eb group by team_id)
select v.team_id, mt.name as team, v.youth_id, v.name, v.age, v.position, v.talent, v.revealed_count, v.key_col, v.key_skill,
       w.weakest_starter, w.weakest_starter_key, sq.squad_size,
       case when v.revealed_count >= 10 and v.key_skill >= w.weakest_starter_key then 'MONTER'
            when v.revealed_count >= 10 then 'VENDRE'
            when v.key_skill is null then 'RÉVÉLER ' || v.key_col
            when v.key_skill < w.weakest_starter_key then 'VENDRE'
            else 'RÉVÉLER ' || v.next_reveal end as verdict,
       case when v.revealed_count >= 10 and v.key_skill >= w.weakest_starter_key and sq.squad_size >= 24 then 'effectif plein (24) : vendre d''abord un surplus'
            end as blocage,
       a.team_reveals_left_today, v.day as as_of
from v join silver.ts_my_teams mt on mt.team_id = v.team_id
left join weak w on w.team_id = v.team_id and w.zone = v.zone
left join sq on sq.team_id = v.team_id
left join gold.ts_academy a on a.youth_id = v.youth_id;

-- Victoires / nuls / défaites comparés sur toute la saison disponible (règle « Vitesse » 5 : jamais un match seul).
-- Base = tous les matchs joués (silver.ts_matches, buts de notre côté selon venue) ; les statistiques viennent de
-- ts_match_report quand le détail du match est en base (with_detail), sinon null (ex. Ajax–Cows 2080875, match d'admin).
drop view if exists gold.ts_vd_comparatif;
create view gold.ts_vd_comparatif with (security_invoker = true) as
with m as (
  select m.my_team_id, mt.name as my_team, m.match_id, m.match_date_paris, m.competition,
         case when m.venue = 'domicile' then m.home_score else m.away_score end as goals_for,
         case when m.venue = 'domicile' then m.away_score else m.home_score end as goals_against
  from silver.ts_matches m join silver.ts_my_teams mt on mt.team_id = m.my_team_id
  where m.status = 'finished' and m.home_score is not null
),
r as (
  select m.*, case when m.goals_for > m.goals_against then 'V' when m.goals_for < m.goals_against then 'D' else 'N' end as result,
         mr.match_id is not null as with_detail, mr.my_shots, mr.opp_shots, mr.my_on_target, mr.opp_on_target, mr.my_conversion_pct,
         mr.my_lost, mr.my_yellows, mr.my_avg_rating, mr.opp_avg_rating, mr.my_sector_avg, mr.opp_sector_avg, mr.opp_is_bot, mr.formation
  from m left join gold.ts_match_report mr on mr.match_id = m.match_id and mr.my_team_id = m.my_team_id
)
select my_team_id as team_id, my_team as team, coalesce(result, 'tous') as result, count(*) as matches,
       count(*) filter (where with_detail) as with_detail,
       string_agg(distinct competition, ', ') as competitions,
       round(avg(goals_for), 2) as gf, round(avg(goals_against), 2) as ga,
       round(avg(my_shots), 1) as shots, round(avg(opp_shots), 1) as opp_shots,
       round(avg(my_on_target), 1) as on_target, round(avg(opp_on_target), 1) as opp_on_target,
       round(avg(my_conversion_pct), 1) as conversion_pct, round(avg(my_lost), 1) as balls_lost,
       round(avg(my_yellows), 2) as yellows, round(avg(my_avg_rating), 2) as my_rating, round(avg(opp_avg_rating), 2) as opp_rating,
       round(avg(my_sector_avg), 1) as my_sectors, round(avg(opp_sector_avg), 1) as opp_sectors,
       count(*) filter (where opp_is_bot) as vs_bots, count(*) filter (where formation is null) as lineup_unknown,
       string_agg(distinct formation, ', ') as formations, min(match_date_paris)::date as first_match, max(match_date_paris)::date as last_match
from r
group by grouping sets ((my_team_id, my_team, result), (my_team_id, my_team));

-- Saisie du prochain match de chaque club : composition enregistrée si elle existe, sinon proposition
-- (meilleure valeur au match par zone, formation de ts_effectif_bilan) et banc de 6 (1 gardien + 5 meilleurs restants).
-- Ordre de l'écran : GB, DEF, MIL, ATT, puis banc. Les consignes par joueur restent à l'agent Tactique.
create or replace view gold.ts_saisie_composition with (security_invoker = true) as
with nx as (
  select distinct on (team_id) team_id, match_id, match_date_paris, opponent, competition, lineup_saved, saved_formation, lineup_deadline_paris
  from gold.ts_upcoming order by team_id, match_date_paris
),
e as (
  select e.*, row_number() over (partition by e.team_id, e.zone order by e.unavailable, e.key_at_match desc, e.controle desc) as r
  from gold.ts_effectif_bilan e
),
xi as (select * from e where not unavailable and r <= starters_needed),
rest as (
  select e.*, row_number() over (partition by e.team_id order by (e.zone = 'GB' and e.r = 2) desc, e.key_at_match desc) as br
  from e where not unavailable and r > starters_needed
)
select nx.team_id, x.team, nx.opponent, nx.competition, nx.match_date_paris, nx.lineup_deadline_paris, nx.lineup_saved,
       coalesce(nx.saved_formation, x.formation) as formation,
       case x.zone when 'GB' then 1 when 'DEF' then 2 when 'MIL' then 3 else 4 end * 100 + x.r as ordre,
       'titulaire' as role, x.zone, x.sous_role, x.name, x.key_name, x.key_skill, x.controle, x.forme, x.key_at_match, x.yellow_cards
from nx join xi x on x.team_id = nx.team_id
union all
select nx.team_id, b.team, nx.opponent, nx.competition, nx.match_date_paris, nx.lineup_deadline_paris, nx.lineup_saved,
       coalesce(nx.saved_formation, b.formation), 500 + b.br, 'banc', b.zone, b.sous_role, b.name, b.key_name, b.key_skill, b.controle,
       b.forme, b.key_at_match, b.yellow_cards
from nx join rest b on b.team_id = nx.team_id and b.br <= 6;
