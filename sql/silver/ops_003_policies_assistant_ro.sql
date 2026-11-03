-- Refonte v2, étape 0.4 : les tables avec RLS activée ne renvoyaient aucune ligne à assistant_ro.
-- Politique select seulement, réservée à ce rôle (anon et authenticated restent sans accès).
create policy assistant_ro_select on bronze.raw_pages for select to assistant_ro using (true);
create policy assistant_ro_select on bronze.discord_messages for select to assistant_ro using (true);
create policy assistant_ro_select on gold.hn_tactique_cible for select to assistant_ro using (true);
create policy assistant_ro_select on gold.hn_tactique_journal for select to assistant_ro using (true);
create policy assistant_ro_select on gold.hn_tactique_plan for select to assistant_ro using (true);
create policy assistant_ro_select on silver.ts_depenses_decidees for select to assistant_ro using (true);
