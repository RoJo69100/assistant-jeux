-- Silver BasketVibe : salaire hebdomadaire par joueur.
-- L'API ne le fournit pas : il est lu dans le texte de l'onglet Effectif > Tiles (capture DOM),
-- format « <Prénom Nom> / PS / <n> / <POS>|<âge> yrs / <taille>|<poids> / Salary 15.660 » (point = séparateur de milliers).
-- Contrôle du 2026-10-16 : somme 288 517 contre 290 619 payés le 2026-10-11 (écart 0,7 %, cause inconnue).
create or replace view silver.bv_player_salary_weekly with (security_invoker = true) as
with parsed as (
  select r.captured_at,
         (r.captured_at at time zone 'Europe/Paris')::date as day,
         x[1] as name,
         replace(replace(x[2], '.', ''), ',', '')::numeric as salary
  from bronze.raw_pages r,
       regexp_matches(r.payload->>'text', '([^\n]+)\nPS\n\d+\n[A-Z]+\|\d+ yrs\n[^\n]*\nSalary ([0-9.,]+)', 'g') x
  where r.game = 'basketvibe' and r.source = 'dom' and r.page_type = 'roster_tiles'
)
select distinct on (p.player_id, date_trunc('week', s.day))
       date_trunc('week', s.day)::date as week,
       p.player_id,
       s.name,
       s.salary,
       s.day
from parsed s
join silver.bv_players p on p.first_name || ' ' || p.last_name = s.name
order by p.player_id, date_trunc('week', s.day), s.captured_at desc;
