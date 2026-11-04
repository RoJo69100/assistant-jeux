-- Refonte v2, étape 2.2 : objectif de chacun de mes prochains matchs (7 jours), tous jeux.
-- core.fixture (matchs à venir et série en cours) + gold.season_context + core.objective_rule (sql/core/011).
-- La carte « composition » lit cette vue en première ligne : objectif, raison chiffrée, ce qui prouvera l'erreur (R-8).
-- Contexte de saison absent ou incomplet → la règle par défaut s'applique et la raison le dit.

create or replace view gold.match_objective with (security_invoker = true) as
with joues as (
  select game, team_id, my_result,
         row_number() over (partition by game, team_id order by coalesce(scheduled_at, day::timestamptz) desc) as k
  from core.fixture
  where played and my_result is not null and competition_kind <> 'amical'
),
serie as (  -- défaites d'affilée depuis le dernier match joué
  select game, team_id,
         coalesce(min(k) filter (where my_result <> 'L'), max(k) + 1) - 1 as n_def
  from joues group by game, team_id
),
a_venir as (
  select f.* from core.fixture f
  where not f.played and f.day between current_date and current_date + 6
),
cand as (
  select v.game, v.team_id, v.fixture_id, v.day, v.scheduled_at, v.competition_kind, v.opponent, v.home,
         coalesce(s.n_def, 0) as n_def, c.rank, c.n_teams, c.gap_to_first, c.rounds_left,
         c.parametres_manquants, r.rule_id, r.objectif, r.priorite, r.raison, r.preuve_erreur,
         row_number() over (partition by v.game, v.team_id, v.fixture_id order by r.priorite, r.rule_id) as choix
  from a_venir v
  left join serie s on s.game = v.game and s.team_id = v.team_id
  left join gold.season_context c on c.game = v.game and c.team_id = v.team_id
  join core.objective_rule r
    on r.actif
   and (r.game is null or r.game = v.game)
   and (r.competition_kind is null or r.competition_kind = v.competition_kind)
   and case r.condition
         when 'serie_defaites' then v.competition_kind <> 'amical' and coalesce(s.n_def, 0) >= 2
         when 'titre_acquis'   then coalesce(c.titre_acquis, false)
         when 'rien_a_jouer'   then coalesce(c.rien_a_jouer, false)
         else true end
)
select game, team_id, fixture_id, day, scheduled_at, competition_kind, opponent, home,
       objectif,
       replace(replace(replace(replace(replace(replace(raison,
         '{n_def}', n_def::text), '{rank}', coalesce(rank::text, '?')), '{n_teams}', coalesce(n_teams::text, '?')),
         '{gap_first}', coalesce(gap_to_first::text, '?')), '{left}', coalesce(rounds_left::text, '?')),
         '{manquants}', case when coalesce(parametres_manquants, 'contexte de saison absent') = '' then ''
                             else ' ; contexte incomplet : ' || coalesce(parametres_manquants, 'contexte de saison absent') end)
         as raison,
       preuve_erreur, n_def as defaites_d_affilee, rule_id
from cand where choix = 1
order by game, day, scheduled_at;

grant select on gold.match_objective to assistant_ro;
