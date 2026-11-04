-- Refonte v2, étape 4.3 (fin) : vérification des affirmations par nos données.
-- kb.claim.data_check_sql = une requête de lecture qui rend une ligne (verdict, preuve) :
--   verdict ∈ confirmé | infirmé | indécis. public.kb_verify(<jeu>) les exécute, écrit data_verdict,
--   data_checked_at et la preuve dans origine.preuve, puis recalcule la confiance.
-- Seul service_role écrit data_check_sql (assistant_ro n'a que select) ; garde : une seule instruction select/with.

create or replace function public.kb_verify(p_game text)
returns jsonb
language plpgsql
security definer
set search_path = kb, public
as $$
declare c record; v text; p text; res jsonb := '[]';
begin
  for c in select id, data_check_sql from kb.claim
           where game = p_game and data_check_sql is not null order by id loop
    if c.data_check_sql !~* '^\s*(select|with)\s' or position(';' in c.data_check_sql) > 0 then
      v := 'indécis'; p := 'requête refusée (une seule instruction select/with)';
    else
      begin
        execute c.data_check_sql into v, p;
      exception when others then
        v := 'indécis'; p := 'erreur : ' || left(sqlerrm, 200);
      end;
    end if;
    update kb.claim set data_verdict = coalesce(v, 'indécis'), data_checked_at = now(),
                        origine = coalesce(origine, '{}') || jsonb_build_object('preuve', p)
     where id = c.id;
    res := res || jsonb_build_object('id', c.id, 'verdict', coalesce(v, 'indécis'), 'preuve', p);
  end loop;
  perform kb.recompute_confidence(p_game);
  return res;
end $$;
revoke all on function public.kb_verify(text) from public, anon, authenticated;
grant execute on function public.kb_verify(text) to service_role;

-- Derby Manager : 10 affirmations testables (repérées par le début de leur texte, pas par id).
update kb.claim set data_check_sql = $q$select case when max(played) = 30 then 'confirmé' else 'infirmé' end, 'France D4 s26 : ' || max(played) || ' matchs joués en fin de saison' from silver.dm_standings where competition = 'ME LIGUE' and season = 26$q$
 where game = 'derbymanager' and text like 'Saison = 30 matchs de ligue%';
update kb.claim set data_check_sql = $q$select case when count(distinct team) = 8 and max(played) = 28 then 'confirmé' else 'infirmé' end, 'Écosse s26 : ' || count(distinct team) || ' équipes, ' || max(played) || ' matchs' from silver.dm_standings where competition = 'SCOTLAND - PREMIER DIVISION' and season = 26$q$
 where game = 'derbymanager' and text like 'Nouvelles ligues S26 (2026-09-28)%';
update kb.claim set data_check_sql = $q$select case when count(distinct team) = 16 then 'confirmé' else 'infirmé' end, 'D4 France s26 : ' || count(distinct team) || ' équipes (la source parle de l''Italie)' from silver.dm_standings where competition = 'ME LIGUE' and season = 26$q$
 where game = 'derbymanager' and text like 'Nombre d''équipes : D4 Italie 16%';
update kb.claim set data_check_sql = $q$select case when count(*) filter (where split_part(tr, '/', 2)::int not between 3 and 7) = 0 and count(*) > 0 then 'confirmé' else 'infirmé' end, 'exigences TR vues : ' || string_agg(distinct split_part(tr, '/', 2), ',') || ' sur ' || count(*) || ' lignes' from silver.dm_squad where tr ~ '^\d+/\d+$'$q$
 where game = 'derbymanager' and text like 'Training Requirement (TR, 2026-05-10)%';
update kb.claim set data_check_sql = $q$select case when count(*) filter (where minute in (1, 46)) > 0 then 'confirmé' else 'indécis' end, count(*) filter (where minute in (1, 46)) || ' but(s) à la 1re ou 46e minute' from silver.dm_shots where outcome = 'goal'$q$
 where game = 'derbymanager' and text like 'Minutes de match : 1 et 46%';
update kb.claim set data_check_sql = $q$select case when count(*) > 0 then 'confirmé' else 'indécis' end, count(*) || ' jour(s) avec une coupe et une ligue le même jour' from (select 1 from silver.dm_matches group by team_id, played_at::date having count(*) filter (where comp = 'C') > 0 and count(*) filter (where comp = 'L') > 0) x$q$
 where game = 'derbymanager' and text like 'Un match de coupe et un de ligue peuvent%';
update kb.claim set data_check_sql = $q$select case when bad > 0 then 'infirmé' when ties > 0 then 'confirmé' else 'indécis' end, ties || ' égalité(s) de points, ' || bad || ' rang(s) contraire(s) à différence puis buts' from (select count(*) filter (where a.pts = b.pts) ties, count(*) filter (where a.pts < b.pts or (a.pts = b.pts and (a.gd < b.gd or (a.gd = b.gd and a.gf < b.gf)))) bad from silver.dm_standings a join silver.dm_standings b on a.competition = b.competition and a.season = b.season and a.captured_at = b.captured_at and a.rank < b.rank where a.played >= 28) x$q$
 where game = 'derbymanager' and text like 'Départage ligue : différence de buts%';
update kb.claim set data_check_sql = $q$select case when count(distinct team_id) > 0 and min(n) = 2 and max(n) = 2 then 'confirmé' else 'infirmé' end, 'amicaux de pré-saison par équipe : ' || string_agg(n::text, ',') from (select team_id, count(*) n from silver.dm_matches where comp = 'F' and played_at >= '2026-09-25' and played_at < '2026-10-02' group by 1) x$q$
 where game = 'derbymanager' and text like 'Pré-saison (2026-09-25)%';
update kb.claim set data_check_sql = $q$select case when count(*) filter (where left(sub_policy, 3) not in ('RAT','CON','AUT','DEV','IMP','EMR')) = 0 and count(*) > 0 then 'confirmé' else 'infirmé' end, 'statuts vus : ' || string_agg(distinct sub_policy, ',') from silver.dm_squad where sub_policy is not null$q$
 where game = 'derbymanager' and text like 'Remplacements (2026-10-21/25)%';
update kb.claim set data_check_sql = $q$select case when count(*) filter (where comp_name ilike '%coupe nationale%' or comp_name ilike '%national cup%') > 0 then 'confirmé' else 'indécis' end, count(*) filter (where comp_name ilike '%coupe nationale%' or comp_name ilike '%national cup%') || ' match(s) de coupe nationale joués' from silver.dm_matches$q$
 where game = 'derbymanager' and text like 'Coupes : Coupe nationale (NC)%';
