# Checklist Derby Manager (périmètre : `docs/chose-a-DM.txt`, demandé le 2026-10-30)

Deux clubs : Queen of the South (547) et Marmandes (307). Une case est cochée quand son critère est vérifié, avec la date.

## Global
- [x] Veille intégrale Discord (125 932 messages, 2019-01-04 → 2026-10-30) → `outputs/derbymanager/veille/connaissance.md` + 4 skills — 2026-10-30
- [x] Userscript d'export (pages + JSON des matchs, club marqué) — 2026-10-30
- [ ] Calendrier : savoir quel jour de saison on est (le calendrier de la saison 27 n'est pas encore exporté)
- [x] Compétitions Ligue / Coupe / Amical distinguées dans `gold.dm_matchs` — 2026-10-30
- [x] Stats de la ligue (meilleurs joueurs) : `competitions_id_stats-tab` capturé ; vue gold à faire quand il servira
- [ ] Gérer deux équipes : vues par `team_id` faites ; **aucun export de Marmandes reçu**

## Jeunes / School
- [x] Fonctionnement du school (durée, places, salaire, croissance) : skill `derbymanager-effectif-entrainement` — 2026-10-30
- [x] Prospects lus (`silver.dm_school`) : potentiel, personnalité, jours restants — 2026-10-30
- [ ] Décision scout / intégration validée sur un cas réel (Almgren promu ?)

## Finances
- [x] Solde, dépenses, salaires, entrées : `gold.dm_finances_bilan` (Queen of the South) — 2026-10-30
- [x] Mouvements de la saison : `silver.dm_money_flow` — 2026-10-30
- [ ] Actions possibles chiffrées pour Marmandes

## Équipe
- [x] Toutes les caractéristiques des joueurs : `gold.dm_effectif` (64 colonnes) — 2026-10-30
- [ ] Sens confirmé de TI, TR, PT, SKILL, STA, PTR (glossaire « inconnu »)
- [x] Forme, condition, sharpness, satisfaction, statuts : skill `derbymanager-regles` — 2026-10-30
- [x] Bon poste ou non : `gold.dm_poste_scores` (note par ligne [H]) — 2026-10-30
- [x] Statistiques joueur (apps, buts, note) et blessés : `gold.dm_effectif` — 2026-10-30
- [x] Analyse des matchs de la saison (xG, tirs, formation) : `gold.dm_matchs`, `gold.dm_saison_bilan`, `gold.dm_tirs_profil` — 2026-10-30

## Transferts
- [x] Base de prix (591 transferts de la semaine) : `gold.dm_prix_reference` — 2026-10-30
- [x] Marché comparé à nos titulaires : `gold.dm_marche_notes` — 2026-10-30
- [ ] Marché au-dessus de 7,5 M exporté (filtre de prix de l'écran)
- [ ] Historique des transferts sur plusieurs semaines (exporter `/transfers` chaque semaine)

## Entraînement
- [x] Groupes, intensité, gains/pertes par joueur : `silver.dm_training`, `gold.dm_entrainement` — 2026-10-30
- [x] Règles (TR, intensité, mentors, potentiel, installations) : skill — 2026-10-30
- [ ] Réglage par poste validé par la progression d'une semaine

## Tactique
- [x] Formations, rôles, curseurs, options, set pieces, remplaçants : skill `derbymanager-tactique` — 2026-10-30
- [x] Réglages enregistrés lus (`silver.dm_tactic`) — 2026-10-30
- [ ] Stratégie par adversaire (exporter les pages des adversaires : `/teams/<id>`)
- [ ] Composition proposée confrontée au résultat (learnings `L-nnn`)

## Infrastructures
- [x] Bâtiments, niveaux, maintenance, dégradation, conseil : skill `derbymanager-club` + `silver.dm_facilities` — 2026-10-30
- [ ] Décision d'investissement chiffrée pour Marmandes
