-- Étape 5f, L2 et L4 (docs/refonte-v3/journal-aujourdhui.md) : paramètres lus par pipelines/aujourdhui.py, jamais écrits dans le code.
-- Lignes seulement (aucun DDL). academie_valeur_high n'est PAS écrite : aucun joueur de catégorie High dans l'historique
-- des transferts (requête et résultat au journal, étape 5f, L4).
insert into core.game_params (game, key, value, source, verified_on) values
  ('basketvibe', 'vente_tolerance_force', '1.0',
   'décision de l''utilisateur du 2026-11-09 : même force = écart de 1 point de PS au poste (fit de gold.bv_sell_replacement)', '2026-11-09'),
  ('basketvibe', 'academie_cout_test', '25000',
   '.claude/skills/basketvibe-academie/references/06-tests.md (25 000 par prospect, une seule fois par rapport)', '2026-11-09')
on conflict (game, key) do nothing;
