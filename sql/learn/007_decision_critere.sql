-- Refonte v3, boucle d'apprentissage (diagnostic du 09/11, cause K3) : les conseils migrés de learnings.md ont un critère
-- en prose (prediction.metric = 'migre') que evaluer_decisions.py ne sait pas mesurer. Nouvelle opération 'critere' de
-- public.decision_ecrire : remplace ce critère par une prédiction mesurable (sql ou my_result) et garde l'ancien dans
-- prediction.ancien. Refus si le critère actuel n'est pas 'migre' (un critère mesurable n'est jamais écrasé).
-- Le reste de la fonction est inchangé (sql/learn/002_decision_ecrire_https.sql).

create or replace function public.decision_ecrire(p jsonb) returns jsonb
language plpgsql volatile security definer set search_path = '' as $$
declare
  op text := p ->> 'op';
  v_statut text; v_charte jsonb; v_id bigint; n integer; v_pred jsonb;
begin
  if op = 'new' then
    if p ->> 'lecon' is not null then
      select status into v_statut from learn.lesson where id = p ->> 'lecon';
      if not found then
        return jsonb_build_object('ok', false, 'erreur', 'leçon ' || (p ->> 'lecon') || ' introuvable');
      end if;
      if v_statut = 'retired' then
        return jsonb_build_object('ok', false, 'erreur', 'la leçon ' || (p ->> 'lecon') || ' est retirée (contredite) — conseil à réécrire (A-7)');
      end if;
    end if;
    select to_jsonb(s) - 'game' - 'team_id' into v_charte from core.club_strategy s
     where s.game = p ->> 'jeu' and s.team_id is not distinct from (p ->> 'equipe') and s.valide_le is not null;
    insert into learn.decision (game, team_id, domain, label, hypothesis, prediction, eval_after, evidence,
                                strategy_snapshot, lesson_id, sujet)
    values (p ->> 'jeu', p ->> 'equipe', p ->> 'domaine', p ->> 'label', p ->> 'hypothese', p -> 'prediction',
            (p ->> 'eval_after')::timestamptz, p -> 'preuve', v_charte, p ->> 'lecon', p ->> 'sujet')
    returning id into v_id;
    return jsonb_build_object('ok', true, 'id', v_id, 'charte', v_charte is not null);
  elsif op = 'statut' then
    update learn.decision set status = p ->> 'statut', user_note = coalesce(p ->> 'note', user_note)
     where id = (p ->> 'id')::bigint;
    get diagnostics n = row_count;
    return jsonb_build_object('ok', n = 1, 'erreur', case when n = 1 then null else 'décision introuvable' end);
  elsif op = 'critere' then
    select prediction into v_pred from learn.decision where id = (p ->> 'id')::bigint;
    if not found then
      return jsonb_build_object('ok', false, 'erreur', 'décision introuvable');
    end if;
    if coalesce(v_pred ->> 'metric', '') <> 'migre' then
      return jsonb_build_object('ok', false, 'erreur', 'critère déjà mesurable (' || coalesce(v_pred ->> 'metric', 'null') || ') : non remplacé');
    end if;
    if coalesce(p -> 'prediction' ->> 'metric', '') not in ('sql', 'my_result') then
      return jsonb_build_object('ok', false, 'erreur', 'prédiction sql ou my_result attendue');
    end if;
    update learn.decision set prediction = (p -> 'prediction') || jsonb_build_object('ancien', v_pred)
     where id = (p ->> 'id')::bigint;
    return jsonb_build_object('ok', true);
  end if;
  return jsonb_build_object('ok', false, 'erreur', 'opération inconnue : ' || coalesce(op, 'null'));
end $$;
revoke all on function public.decision_ecrire(jsonb) from public, anon, authenticated;
grant execute on function public.decision_ecrire(jsonb) to service_role;
