# Effectifs des clubs adverses en silver (BasketVibe) — design court, approuvé le 2026-11-10

## Intention
Rendre lisibles les effectifs des clubs captés par les pages `/c/<club>` (bronze.raw_pages, page_type « unknown »),
pour la question 3b de la carte de faisabilité (« pourquoi les premiers le sont ») : compétences des joueurs des autres clubs.

## Étape 0 (relevé du 2026-11-10, 306 captures, 39 clubs)
Chaque onglet déclenche plusieurs appels API ; c'est l'URL de l'appel (`silver.bv_api.endpoint`) qui dit le contenu :
- sans onglet : `/clubs/<slug>/seasons`, `/clubs/<slug>/season-history` (team_id, team_name, lignes ligue et coupe), `/clubs/<slug>/trophies`, plus des appels globaux (auth/me, ligues, notifications) ;
- `?tab=schedule` et `?tab=history` : `/clubs/<slug>/schedule` (matchs) ;
- `?tab=headToHead` : `/clubs/<slug>/head-to-head` (bilan contre nous) + captures DOM ;
- `?tab=statistics` : `/clubs/<slug>/season-roster` = l'effectif (seule source des joueurs ; 37 captures, 35 clubs) ;
- `?tab=skills` : 2 captures sans compétences (invitations, compteur).
Une capture d'effectif (kk-bedex) est rangée sous `?tab=schedule` : on classe par l'URL de l'appel, pas par `page_url`.
Joueurs : 375 lignes `skills_visibility = bracket` (skill_brackets min/max), 9 lignes `full` (stats exactes + player_strength), 8 anciens joueurs (`is_former_roster`).

## Approches
- **Retenue** : vue sur `silver.bv_api` filtrée par endpoint `^/clubs/[^/]+/season-roster$` (même modèle que `bv_academy_candidates`).
- Écartée : filtre de `bronze.raw_pages` par `page_url` (perd l'effectif de kk-bedex rangé sous un autre onglet).

## Design
`silver.bv_club_roster` (migration `sql/silver/054_bv_club_roster.sql`) : un joueur par club et par capture.
Colonnes : capture, slug, team_id et nom (dernier `season-history` du slug), saison, `est_derniere` (dernière capture du club),
joueur, visibilité, min/max des 8 compétences (en `full` : min = max = valeur exacte), player_strength (full seulement),
forme, fatigue, âge, taille, poids, expérience, poste, ancien joueur, blessure, matchs et moyennes de ligue de la saison.
Commentaire de vue : fourchettes de 20 points (classement, pas mesure fine) ; analyses filtrent `is_former_roster = false` par défaut.
Test `pipelines/test_bv_club_roster.py` sur la vraie base : nombre de clubs = clubs ayant un appel d'effectif dans `silver.bv_api`,
nombre de joueurs, une seule dernière capture par club, temps de la vue < 3 s (sinon la matérialiser).
Blocs du gabarit « que faire » : non concernés (vue silver), reportés.
