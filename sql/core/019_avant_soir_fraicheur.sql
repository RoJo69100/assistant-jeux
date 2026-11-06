-- Refonte v3, S4b : public.rafraichir_avant_soir() ne relance pas un rafraîchissement de ~3 min quand rien n'a changé :
-- « à jour » si le dernier rafraîchissement date de moins d'une minute, OU s'il date de moins de 10 minutes et qu'aucune page
-- n'est arrivée dans bronze.raw_pages depuis (le job pg_cron « rafraichir-vues » tourne toutes les 10 minutes avec cette garde).
-- Toujours au plus une demande par minute.

create or replace function public.rafraichir_avant_soir() returns text
language plpgsql volatile security definer set search_path = '' as $$
declare e core.rafraichi_etat%rowtype; cur bigint;
begin
  select * into e from core.rafraichi_etat where id = 1 for update;
  if exists (select 1 from pg_locks where locktype = 'advisory' and classid = 0 and objid = 7140001 and granted) then
    return 'en cours : relance dans 30 s';
  end if;
  select max(id) into cur from bronze.raw_pages;
  if e.rafraichi_a is not null and (e.rafraichi_a > now() - interval '1 minute'
       or (e.last_page_id is not distinct from cur and e.rafraichi_a > now() - interval '10 minutes')) then
    return 'à jour : rafraîchi à ' || to_char(e.rafraichi_a at time zone 'Europe/Paris', 'HH24:MI:SS');
  end if;
  if e.demande_a is not null and e.demande_a > now() - interval '1 minute' then
    return 'déjà demandé à ' || to_char(e.demande_a at time zone 'Europe/Paris', 'HH24:MI:SS') || ' : relance dans 60 s';
  end if;
  update core.rafraichi_etat set demande_a = now() where id = 1;
  return 'demandé : le job démarre dans la minute (durée ~3 min), relance dans 90 s';
end $$;
revoke all on function public.rafraichir_avant_soir() from public, anon, authenticated;
grant execute on function public.rafraichir_avant_soir() to service_role, assistant_ro;
