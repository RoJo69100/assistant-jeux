-- Refonte v3, S4b : les sessions pg_cron ont statement_timeout = 2 min (sonde du 2026-11-05 : « SONDE statement_timeout=2min,
-- user=postgres »). Un rafraîchissement complet (4 vues) dépasse 2 min : le job « rafraichir-demande » a échoué après 130 s
-- (« canceling statement due to statement timeout », dans refresh … gold.daily_alerts) et s'est relancé chaque minute.
-- Correctif : « set statement_timeout » placé devant l'instruction dans la commande du job (sonde : un timeout de 3 s posé ainsi
-- coupe bien l'instruction suivante, donc la valeur posée s'applique) ; une demande n'est honorée que pendant 5 minutes
-- (pas de boucle de relances si un rafraîchissement échoue).

create or replace function core.rafraichir_si_demande() returns void
language plpgsql security definer set search_path = '' as $$
declare e core.rafraichi_etat%rowtype;
begin
  select * into e from core.rafraichi_etat where id = 1;
  if e.demande_a is not null
     and e.demande_a > now() - interval '5 minutes'
     and (e.debut_a is null or e.demande_a > e.debut_a) then
    perform * from core.rafraichir_vues(true);
  end if;
end $$;
revoke all on function core.rafraichir_si_demande() from public;

select cron.schedule('rafraichir-vues', '*/10 * * * *',
  $$set statement_timeout = '15min'; select * from core.rafraichir_vues(false)$$);
select cron.schedule('rafraichir-demande', '* * * * *',
  $$set statement_timeout = '15min'; select core.rafraichir_si_demande()$$);
select cron.unschedule('sonde2');
