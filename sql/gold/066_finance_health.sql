-- Refonte v2, étape 1.4 : santé financière pour tous les jeux, sur core.finance_daily et core.game_params.
-- Une ligne par équipe : dernier relevé. capacite_invest = solde − réserve (reserve_periodes × charges de la période).
-- Jeu sans trésorerie (Hockey Nation : économie au plafond salarial) : capacite_invest nulle, cap_space à la place.
-- Dépenses décidées non encore relevées : pas encore en base (learn.decision, phase 3) ; la carte les soustrait à la main.
-- Parité : pipelines/finances_parite.py (gold.bv_finance_health, silver.hn_cap_now).

insert into core.game_params (game, key, value, source, verified_on) values
  ('basketvibe', 'reserve_periodes', '2',
   'docs/fiches/basketvibe/finances.md (réserve de sécurité = 2 semaines de charges, gold.bv_finance_s2_projection) ; learnings C-083', '2026-11-03')
on conflict (game, key) do nothing;

create or replace view gold.finance_health with (security_invoker = true) as
with dernier as (
  select distinct on (game, team_id) *
  from core.finance_daily
  order by game, team_id, day desc
),
k as (
  select game, value::text::numeric as reserve_periodes from core.game_params where key = 'reserve_periodes'
)
select d.game, d.team_id, d.day as as_of,
       d.extras ->> 'periode'                         as periode,
       d.balance,
       d.expenses                                     as charges_periode,
       d.salaries,
       d.wage_cap,
       d.wage_cap - d.salaries                        as cap_space,
       k.reserve_periodes,
       k.reserve_periodes * d.expenses                as reserve,
       d.balance - k.reserve_periodes * d.expenses    as capacite_invest,
       current_date - d.day                           as finances_age_days
from dernier d
left join k on k.game = d.game;

grant select on gold.finance_health to assistant_ro;
