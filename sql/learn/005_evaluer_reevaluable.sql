-- Refonte v3, étape 5b-3 (critère D2) : un résultat « inconclusive » n'est plus figé.
-- 1075 et 1099 ont un résultat {"valeur": null} écrit le 09/11 ; l'ancienne vue excluait toute décision ayant un résultat,
-- donc elles n'auraient jamais été réévaluées. Désormais :
--   gold.decisions_a_evaluer inclut une décision dont le seul résultat est « inconclusive » ;
--   public.evaluer_ecrire remplace ce résultat (update, jamais delete) par le nouveau verdict, refuse de toucher un résultat
--   « confirmed » ou « contradicted », et refuse d'écrire « inconclusive » (D1 : une valeur vide reste « en attente »).
-- learn.outcome.decision_id est la clé primaire : un seul résultat par décision.
-- Additive et rejouable : create or replace, aucun drop, droits inchangés (service_role seul pour la fonction).

create or replace view gold.decisions_a_evaluer with (security_invoker = true) as
select d.*
from learn.decision d
where d.status in ('accepted', 'done') and d.eval_after <= now()
  and d.prediction->>'metric' in ('my_result', 'sql')
  and not exists (select 1 from learn.outcome o where o.decision_id = d.id and o.verdict <> 'inconclusive');

create or replace function public.evaluer_ecrire(p jsonb) returns jsonb
language plpgsql volatile security definer set search_path = '' as $$
declare
  v_id bigint := (p ->> 'decision_id')::bigint;
  v_verdict text := p ->> 'verdict';
  v_statut text; v_game text; v_ancien text; v_res text; v_quand timestamptz;
  l jsonb := p -> 'lecon';
  n integer;
begin
  if v_verdict is null or v_verdict not in ('confirmed', 'contradicted') then
    return jsonb_build_object('ok', false, 'erreur', 'verdict ' || coalesce(v_verdict, 'vide') || ' refusé : seule une mesure conclusive s''écrit');
  end if;
  select status, game into v_statut, v_game from learn.decision where id = v_id;
  if not found then
    return jsonb_build_object('ok', false, 'erreur', 'décision ' || v_id || ' introuvable');
  end if;
  if v_statut not in ('accepted', 'done') then
    return jsonb_build_object('ok', false, 'erreur', 'décision ' || v_id || ' non appliquée (statut ' || v_statut || ')');
  end if;
  select verdict, measured_at into v_res, v_quand from learn.outcome where decision_id = v_id for update;
  if found and v_res <> 'inconclusive' then
    return jsonb_build_object('ok', false, 'erreur', 'décision ' || v_id || ' déjà évaluée (' || v_res || ')');
  end if;
  if l is not null and jsonb_typeof(l) = 'object' then
    select status into v_ancien from learn.lesson
     where id = l ->> 'id' and n_for = (l ->> 'n_for_avant')::int and n_against = (l ->> 'n_against_avant')::int;
    if not found then
      return jsonb_build_object('ok', false, 'erreur', 'leçon ' || (l ->> 'id') || ' introuvable ou modifiée depuis sa lecture');
    end if;
    update learn.lesson
       set n_for = (l ->> 'n_for')::int, n_against = (l ->> 'n_against')::int, status = l ->> 'statut',
           promoted_at = case when (l ->> 'statut') <> status then now() else promoted_at end,
           source_decisions = array_append(source_decisions, v_id)
     where id = l ->> 'id';
    get diagnostics n = row_count;
    if (l ->> 'erreur') is not null and (l ->> 'statut') = 'retired' and v_ancien <> 'retired' then
      insert into learn.error (game, description, recurrence, enforcement, guard_ref)
      values (v_game, l ->> 'erreur', greatest((l ->> 'n_against')::int, 1), 'sql', 'garde.py : leçon retirée bloquée');
    end if;
  end if;
  if v_res = 'inconclusive' then
    update learn.outcome
       set observed = coalesce(p -> 'observed', '{}'::jsonb), verdict = v_verdict, measured_at = now(),
           note = concat_ws(' ; ', note, 'remplace inconclusive du ' || v_quand::text)
     where decision_id = v_id;
  else
    insert into learn.outcome (decision_id, observed, verdict) values (v_id, coalesce(p -> 'observed', '{}'::jsonb), v_verdict);
  end if;
  return jsonb_build_object('ok', true, 'decision_id', v_id, 'verdict', v_verdict, 'lecon_maj', coalesce(n, 0) = 1,
                            'remplace', coalesce(v_res = 'inconclusive', false));
end $$;
revoke all on function public.evaluer_ecrire(jsonb) from public, anon, authenticated;
grant execute on function public.evaluer_ecrire(jsonb) to service_role;
