-- Derby Manager : tirs arrêtés et capitaine, joueur par joueur (conçu le 2026-11-01, demande : « set pieces très important »).
-- Source : silver.dm_squad (onglet Squad : colonnes PEN, FK, COR, DEF, ATT, CAP ; sp_sho/sp_acc/sp_pas = finition, précision, passe).
-- Règles (connaissance.md, dev 2025-02 → 2026-09) : preneurs réglables depuis S25 ; sans réglage = un des 3 meilleurs ;
-- coup franc = tireur « long shot » (accuracy), corner = « long pass » (passing + accuracy), penalty = finishing (shooting) ;
-- 6 joueurs aux valeurs les plus hautes (aerial/headers) montent dans la surface ; « tous dans la surface = ne rien régler ».
-- PRI = preneur prioritaire réglé ; BOX = monte dans la surface (DEF = marque dans la surface, ATT = va dans la surface).
create or replace view gold.dm_setpieces with (security_invoker = true) as
with s as (
  select q.*, v.condition, v.forme, v.blessure, v.verdict
  from silver.dm_squad q
  left join gold.dm_verdict_joueurs v on v.team_id = q.team_id and v.name = q.name
)
select s.team_id, c.club, s.name, s.pos, s.slot,
       s.sp_sho as finition, s.sp_acc as precision, s.sp_pas as passe, s.sp_aer as aerien, s.sp_hea as tete, s.xp, s.captain as cap_regle,
       s.sp_pen as pen_regle, s.sp_fk as fk_regle, s.sp_cor as cor_regle, s.sp_def as def_regle, s.sp_att as att_regle,
       row_number() over (partition by s.team_id order by s.sp_sho desc nulls last, s.sp_acc desc nulls last) as rang_penalty,
       row_number() over (partition by s.team_id order by s.sp_acc desc nulls last, s.sp_sho desc nulls last) as rang_coup_franc,
       row_number() over (partition by s.team_id order by (s.sp_pas + s.sp_acc) desc nulls last) as rang_corner,
       row_number() over (partition by s.team_id order by (coalesce(s.sp_aer, 0) + coalesce(s.sp_hea, 0)) desc) as rang_surface,
       row_number() over (partition by s.team_id order by s.xp desc nulls last, s.sp_pas desc nulls last) as rang_capitaine,
       s.condition, s.forme, s.blessure, s.verdict
from s join silver.dm_clubs c using (team_id)
order by s.team_id, s.sp_sho desc nulls last;
