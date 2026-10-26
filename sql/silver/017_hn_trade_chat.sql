-- Silver Hockey Nation : offres du salon Discord #trade (30 derniers jours), reliées aux joueurs exportés (2026-10-23).
-- Les joueurs cités ne sont reconnus que s'ils sont dans un effectif exporté (silver.hn_league_players) : exporter plus de clubs et le marché élargit la liaison.
create or replace view silver.hn_trade_chat with (security_invoker = true) as
select m.id as message_id, m.posted_at, m.author, m.payload->>'content' as content,
       (select string_agg(distinct pl.name, ', ') from silver.hn_league_players pl
         where length(pl.name) > 6 and m.payload->>'content' ilike '%' || split_part(pl.name, ' ', 2) || '%' and length(split_part(pl.name, ' ', 2)) > 4) as joueurs_cites,
       (m.payload->>'content' ~* '(\d+(\.\d+)?)\s*m\b|aav') as parle_contrat,
       (m.payload->>'content' ~* '(pick|1st|2nd|3rd|round|prospect|farm|u21)') as parle_picks_prospects,
       (m.payload->>'content' ~* '(looking for|wtb|need|searching|want)') as cherche,
       (m.payload->>'content' ~* '(available|selling|wts|offer|shopping|on my block|moving)') as propose
from bronze.discord_messages m
where m.game = 'hockeynation' and m.channel = '#trade' and m.posted_at > now() - interval '30 days';
