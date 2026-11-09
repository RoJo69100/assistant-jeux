-- Refonte v3, étape 5b-2 : evaluer_decisions.py en session cloud. Le port 5432 est bloqué et assistant_ro n'a pas le droit
-- de mettre à jour learn.lesson (diagnostic-boucle-apprentissage.md, B2) : le résultat et la leçon liée sont écrits par
-- une fonction côté base, appelée en POST (clé de service), dans une seule transaction.
-- Le verdict et le nouveau statut de la leçon sont calculés par pipelines/evaluer_decisions.py (logique testée) ;
-- la fonction refuse sans rien écrire si la décision n'est pas appliquée, si elle a déjà un résultat, ou si la leçon
-- a changé depuis sa lecture. Une décision sans leçon n'échoue pas. Accès : service_role seulement (comme decision_ecrire).
-- Additive et rejouable : create or replace, aucun drop.
--
-- p = {"decision_id": 1070, "observed": {...}, "verdict": "confirmed|contradicted|inconclusive",
--      "lecon": null | {"id": "...", "n_for_avant": 0, "n_against_avant": 0, "n_for": 1, "n_against": 0,
--                       "statut": "hypothesis", "erreur": null | "texte de learn.error"}}

create or replace function public.evaluer_ecrire(p jsonb) returns jsonb
language plpgsql volatile security definer set search_path = '' as $$
declare
  v_id bigint := (p ->> 'decision_id')::bigint;
  v_statut text; v_game text; v_ancien text;
  l jsonb := p -> 'lecon';
  n integer;
begin
  select status, game into v_statut, v_game from learn.decision where id = v_id;
  if not found then
    return jsonb_build_object('ok', false, 'erreur', 'décision ' || v_id || ' introuvable');
  end if;
  if v_statut not in ('accepted', 'done') then
    return jsonb_build_object('ok', false, 'erreur', 'décision ' || v_id || ' non appliquée (statut ' || v_statut || ')');
  end if;
  if exists (select 1 from learn.outcome where decision_id = v_id) then
    return jsonb_build_object('ok', false, 'erreur', 'décision ' || v_id || ' déjà évaluée');
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
  insert into learn.outcome (decision_id, observed, verdict) values (v_id, coalesce(p -> 'observed', '{}'::jsonb), p ->> 'verdict');
  return jsonb_build_object('ok', true, 'decision_id', v_id, 'verdict', p ->> 'verdict', 'lecon_maj', coalesce(n, 0) = 1);
end $$;
revoke all on function public.evaluer_ecrire(jsonb) from public, anon, authenticated;
grant execute on function public.evaluer_ecrire(jsonb) to service_role;
