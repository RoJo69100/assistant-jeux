-- Refonte v2, étape 1.1 : état connu à une date passée (backtests, plan §8.2).
-- Pour chaque joueur du jeu : le dernier relevé de core.player_daily au plus tard à p_day, dans sa dernière équipe
-- (HN : un joueur monté de FRM en PRO ne garde pas sa ligne FRM), et pas plus vieux que p_max_age jours
-- (un joueur parti n'est plus relevé : il sort au bout de p_max_age).
-- Aucune donnée postérieure à p_day n'est lue : pas de fuite du futur dans un backtest.

create or replace function core.player_daily_asof(p_game text, p_day date, p_max_age int default 7)
returns setof core.player_daily
language sql stable security invoker
set search_path = ''
as $$
  select distinct on (p.player_id) p.*
  from core.player_daily p
  where p.game = p_game
    and p.day <= p_day
    and p.day > p_day - p_max_age
  order by p.player_id, p.day desc, p.extras->>'capture_id' desc nulls last
$$;

revoke all on function core.player_daily_asof(text, date, int) from public, anon, authenticated;
grant execute on function core.player_daily_asof(text, date, int) to assistant_ro;
