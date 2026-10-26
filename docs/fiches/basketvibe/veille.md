# BasketVibe — fiche Veille

Lue par l'agent `veille` après `commun.md`. Contenu repris de l'agent BasketVibe validé (checklist BasketVibe, partie E).

## Skills à lire
- tous les `.claude/skills/basketvibe-*/SKILL.md` concernés par les messages lus

## Règles propres au jeu
1. **Hiérarchie des sources** (skill basketvibe-communaute) : manuel `[M§x]` > News de l'admin `[News date]` et développeur `[Dev date, salon]` > communauté `[Com date, auteur, salon]`.
2. Coût : filtre en SQL (`is_dev`, salon, mots-clés : engine, v4, fatigue, training, potential, academy, transfer, salary, sponsor, bug, fix…) avant de lire le texte complet. Lis tous les messages du développeur et toutes les News ; pour la communauté, seulement ceux qui touchent une règle ou un chiffre.
3. Delta : `outputs/basketvibe/veille/etat.md` (date « lu jusqu'au » par source), puis seulement les posts plus récents dans `gold.bv_veille_feed`.
4. **Codes de citation** : ajouter `[GM date, auteur, salon]` pour les Game Masters (par ex. `elemke.`), entre la News/développeur et la communauté : réponses de modération et d'usage, pas des règles de moteur.
5. **Export Discord** : le dossier réel est `data/discord/BasketVibe/` (identifiant de jeu : `basketvibe`). `discord_BasketVibe_export.txt` = historique déjà lu jusqu'au 2026-10-09 ; `discord_BasketVibe_partN.txt` = delta. Lire seulement le delta après `etat.md`. Rappeler d'importer le delta en base (`pipelines/import_discord.py`) pour que `gold.bv_veille_feed` suive.

## Données
- `gold.bv_veille_feed` : `source` (news | discord), `posted_at`, `author`, `is_dev`, `channel`, `content`, `ref`.
- `outputs/basketvibe/veille/etat.md` : dernière date lue par source.
- Pour vérifier une affirmation chiffrée de la communauté contre nos données : vues gold (ex. `gold.bv_potential_estimate`, `gold.bv_academy_gauge_projection`, `gold.bv_fatigue_plan`). Dis si nos données la confirment, l'infirment ou ne permettent pas de trancher.

## Livrable
`outputs/basketvibe/veille/AAAA-MM-JJ.md` (date du jour) :
1. **Résumé** : période lue, nombre de messages par source, ce qui change pour le jeu en 3 lignes.
2. **Propositions de mise à jour**, numérotées `V-AAAAMMJJ-n`, une par ligne de tableau : skill visé et section, texte proposé (prêt à coller, avec sa source), type (ajout / correction / contradiction ⚠️), impact sur nos agents ou nos vues SQL (ex. une formule à changer dans `sql/gold/…`), priorité (haute si ça change une décision de la semaine).
3. **À surveiller** : annonces sans date ni chiffre, rumeurs, sondages en cours.
Puis mets à jour `etat.md` (date « lu jusqu'au » = dernier `posted_at` lu, par source). Renvoie un résumé de 10 lignes maximum avec le nombre de propositions.

## Sortie propre au jeu
- Si aucun nouveau message n'est en base depuis `etat.md`, demande l'export (Discord : fichiers dans `data/discord/basketvibe/` puis `pipelines/import_discord.py` ; News : ouvrir la page News avec le script actif).
