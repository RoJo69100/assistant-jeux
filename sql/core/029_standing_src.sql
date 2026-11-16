-- Noyau : union des adaptateurs adapt.<jeu>_standing (source de core.standing).
-- Reprise de la définition en base (pg_get_viewdef, 2026-11-16, brique base) : l'objet existait sans fichier source.
-- À comparer à la base avant tout rejeu.
create or replace view core.standing_src with (security_invoker = true) as
SELECT basketvibe_standing.game,
    basketvibe_standing.team_id,
    basketvibe_standing.team_label,
    basketvibe_standing.is_mine,
    basketvibe_standing.season_id,
    basketvibe_standing.day,
    basketvibe_standing.round_no,
    basketvibe_standing.rank,
    basketvibe_standing.played,
    basketvibe_standing.points,
    basketvibe_standing.wins,
    basketvibe_standing.draws,
    basketvibe_standing.losses,
    basketvibe_standing.gf,
    basketvibe_standing.ga,
    basketvibe_standing.extras
   FROM adapt.basketvibe_standing
UNION ALL
 SELECT derbymanager_standing.game,
    derbymanager_standing.team_id,
    derbymanager_standing.team_label,
    derbymanager_standing.is_mine,
    derbymanager_standing.season_id,
    derbymanager_standing.day,
    derbymanager_standing.round_no,
    derbymanager_standing.rank,
    derbymanager_standing.played,
    derbymanager_standing.points,
    derbymanager_standing.wins,
    derbymanager_standing.draws,
    derbymanager_standing.losses,
    derbymanager_standing.gf,
    derbymanager_standing.ga,
    derbymanager_standing.extras
   FROM adapt.derbymanager_standing
UNION ALL
 SELECT hardwood_standing.game,
    hardwood_standing.team_id,
    hardwood_standing.team_label,
    hardwood_standing.is_mine,
    hardwood_standing.season_id,
    hardwood_standing.day,
    hardwood_standing.round_no,
    hardwood_standing.rank,
    hardwood_standing.played,
    hardwood_standing.points,
    hardwood_standing.wins,
    hardwood_standing.draws,
    hardwood_standing.losses,
    hardwood_standing.gf,
    hardwood_standing.ga,
    hardwood_standing.extras
   FROM adapt.hardwood_standing
UNION ALL
 SELECT hockeynation_standing.game,
    hockeynation_standing.team_id,
    hockeynation_standing.team_label,
    hockeynation_standing.is_mine,
    hockeynation_standing.season_id,
    hockeynation_standing.day,
    hockeynation_standing.round_no,
    hockeynation_standing.rank,
    hockeynation_standing.played,
    hockeynation_standing.points,
    hockeynation_standing.wins,
    hockeynation_standing.draws,
    hockeynation_standing.losses,
    hockeynation_standing.gf,
    hockeynation_standing.ga,
    hockeynation_standing.extras
   FROM adapt.hockeynation_standing
UNION ALL
 SELECT sixzeroleague_standing.game,
    sixzeroleague_standing.team_id,
    sixzeroleague_standing.team_label,
    sixzeroleague_standing.is_mine,
    sixzeroleague_standing.season_id,
    sixzeroleague_standing.day,
    sixzeroleague_standing.round_no,
    sixzeroleague_standing.rank,
    sixzeroleague_standing.played,
    sixzeroleague_standing.points,
    sixzeroleague_standing.wins,
    sixzeroleague_standing.draws,
    sixzeroleague_standing.losses,
    sixzeroleague_standing.gf,
    sixzeroleague_standing.ga,
    sixzeroleague_standing.extras
   FROM adapt.sixzeroleague_standing
UNION ALL
 SELECT teamsoccer_standing.game,
    teamsoccer_standing.team_id,
    teamsoccer_standing.team_label,
    teamsoccer_standing.is_mine,
    teamsoccer_standing.season_id,
    teamsoccer_standing.day,
    teamsoccer_standing.round_no,
    teamsoccer_standing.rank,
    teamsoccer_standing.played,
    teamsoccer_standing.points,
    teamsoccer_standing.wins,
    teamsoccer_standing.draws,
    teamsoccer_standing.losses,
    teamsoccer_standing.gf,
    teamsoccer_standing.ga,
    teamsoccer_standing.extras
   FROM adapt.teamsoccer_standing;

grant select on core.standing_src to assistant_ro;
