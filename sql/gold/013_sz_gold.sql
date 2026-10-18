-- Gold SixZero League (handball) : aides à la décision.
-- Règles : skills sixzeroleague-* ([W:Infrastructure], [W:Finances], [W:Match], [Dev chat]).
-- Cycle du jeu (« semaine ») = 2 journées de ligue = 1 jour en saison [W:Finances, Dev chat] ; 9 cycles par saison (18 journées),
-- ~1 match à domicile par cycle ; hors saison, ni recettes ni entretien [W:Finances, Infrastructure].

-- Rentabilité des améliorations d'Arena et de Fan Shop (les deux seules installations qui rapportent [W:Infrastructure]).
-- Fan Shop : revenu selon le classement, entre un minimum et un maximum affichés ; on donne les deux bornes.
create or replace view gold.sz_infrastructure_payback with (security_invoker = true) as
with lv as (
  select l.*,
         nullif(regexp_replace(substring(l.effect_label from 'to ([0-9][0-9,]*)'), ',', '', 'g'), '')::int as effect_max
  from silver.sz_infrastructure_levels l
  where l.facility in ('Arena', 'FanShop')
),
cur as (select * from lv where level = current_level)
select n.facility, n.current_level, n.level as target_level, n.upgrade_cost_from_current as cost,
       n.effect_label,
       -- gain de recette par cycle par rapport au niveau actuel (Arena : 1 match à domicile par cycle en moyenne)
       n.effect_value - c.effect_value                                  as income_gain_min,
       coalesce(n.effect_max - c.effect_max, n.effect_value - c.effect_value) as income_gain_max,
       n.weekly_maintenance - c.weekly_maintenance                      as extra_maintenance,
       (n.effect_value - c.effect_value) - (n.weekly_maintenance - c.weekly_maintenance) as net_gain_min,
       coalesce(n.effect_max - c.effect_max, n.effect_value - c.effect_value) - (n.weekly_maintenance - c.weekly_maintenance) as net_gain_max,
       round(n.upgrade_cost_from_current::numeric
             / nullif(coalesce(n.effect_max - c.effect_max, n.effect_value - c.effect_value) - (n.weekly_maintenance - c.weekly_maintenance), 0), 1) as payback_cycles_best,
       round(n.upgrade_cost_from_current::numeric
             / nullif((n.effect_value - c.effect_value) - (n.weekly_maintenance - c.weekly_maintenance), 0), 1) as payback_cycles_worst
from lv n join cur c on c.facility = n.facility
where n.level between n.current_level + 1 and n.current_level + 4
order by n.facility, n.level;

-- Composition « sûre » : à chaque poste, les joueurs qui y jouent sans pénalité (rôle principal ou rôle appris [W:Training, Dev chat]),
-- classés par leur note à ce poste (roleOveralls, calculée avant la pénalité de hors-poste [Obs SQL 2026-10-18]).
create or replace view gold.sz_lineup_natural with (security_invoker = true) as
with slots(slot, ord) as (values ('GK',1), ('CB',2), ('LB',3), ('RB',4), ('LW',5), ('RW',6), ('P',7)),
cand as (
  select s.slot, s.ord, p.player_id, p.name, p.age, p.role, (p.role_overalls->>s.slot)::int as rating,
         p.injured or p.suspended as unavailable,
         p.role = s.slot as primary_role
  from slots s
  join silver.sz_players p on p.role = s.slot or p.secondary_roles ? s.slot
)
select c.*, rank() over (partition by c.slot order by c.unavailable, c.rating desc, c.age) as rank_in_slot
from cand c
order by c.ord, rank_in_slot;

-- Toutes les options par poste, y compris hors poste (note avant pénalité : à comparer avec prudence).
create or replace view gold.sz_slot_options with (security_invoker = true) as
select s.slot, p.name, p.role, p.age, (p.role_overalls->>s.slot)::int as rating_before_penalty,
       p.role = s.slot or p.secondary_roles ? s.slot as no_penalty,
       rank() over (partition by s.slot order by (p.role_overalls->>s.slot)::int desc, p.age) as rank_in_slot
from (values ('GK'), ('CB'), ('LB'), ('RB'), ('LW'), ('RW'), ('P')) s(slot)
cross join silver.sz_players p
where not (p.injured or p.suspended);
