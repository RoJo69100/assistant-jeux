# Carte sixzeroleague — entrainement (intensité d'équipe, focus par joueur, formation de rôle ; cycle chaque soir)

Sources lues : commit 8791d35 (2026-11-02)

Écrite le 2026-11-02 (fiche `entrainement.md`, skills `sixzeroleague-entrainement`, `-joueurs`, `-communaute` § 1-2 ; connaissance § 5). Règles : cycle = 2 journées, réglé chaque soir après 21:00 Paris ; saisie avant 21:00 ; pas de potentiel caché à estimer.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:91 | caractéristique à entraîner | var. 2, 3 |
| :92 | suivre le progrès | var. 4 |
| :93 | comprendre le progrès | var. 5-7 |

## Rendu (figé)
1. `| Intensité d'équipe | Valeur | Dans le jeu |`.
2. Dans l'ordre de l'écran : `| Joueur | Rôle | Âge | Éthique | Focus (groupe ou compétence) | Points du dernier cycle (clés) | Garder / changer |`.
3. Formation de rôle : `| Emplacement | Occupant | Rôle appris | Journées /36 | Coût par cycle |`.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Réglage actuel | `silver.sz_training_plan` (`intensity`, `focus_group`, `focus_skill`) | Saisie avant 21:00 Paris. Plan réel = `bronze.raw_pages` page_type `app_team` le plus récent, HTML : aria-label « Training focus for X: Y » + select Intensity (silver.sz_training_plan périmé depuis 10-26) | fiche entraînement § 1 ; police 2026-11-04 | 2026-11-04 19:28 UTC : Normal (« Standard gains. Injury chance about 1.5 % … out for about two matches ») + 16 focus conformes, Rincón « All skills » (C-056) |
| 2 | Focus | compétences clés du rôle (skill joueurs) | Compétences clés du rôle où il joue réellement | fiche entraînement § 3 | |
| 3 | Intensité | — | Plus haut = plus de progrès, plus de blessures et plus longues ; 0.6.1 : risque divisé par deux ; texte de High et Light à relever au sélecteur | connaissance 2.6, 7.1 ; C-055 | |
| 4 | Progrès mesuré | `select applied_at, week_number, name, role, points, key_points, overall_gain from gold.sz_training_progress order by applied_at desc limit 30` | Un cycle s'identifie par `applied_at` (`weekNumber` repart à 1) | `resume.md` § Pièges | |
| 5 | Temps de jeu | `silver.sz_training_changes.match_share` | Les minutes jouées alimentent l'entraînement ; un blessé ne reçoit pas de points | connaissance 5.3, 5.4 | |
| 6 | Rendement | — | Pas de rendement décroissant (4 → 5 = 24 → 25) ; Training Facilities ×1,30 (niv. 6) → ×2,14 (niv. 20), +0,06 par niveau mesuré (Gazelle disait +0,04) | connaissance 5.2, 5.8, 3.2 | |
| 7 | Âge et éthique | `silver.sz_players` (`age`, `work_ethic`) | Bonus jeune jusqu'à 20 ans, nul à 25, baisse dès 28 ; vitesse selon l'éthique | connaissance 5.9, 5.11 | |
| 8 | Formation de rôle | `silver.sz_role_training` | Training Facilities ≥ 5, 2 saisons, 3 rôles max, rôle initial définitif ; 1 emplacement aux niv. 6-8 | connaissance 5.5, 5.6, 5.8 | slot libre, non lancé (C-054) |
| 9 | Avis des amis | connaissance § 5 | Un 2e rôle permet de jouer de l'autre côté sans pénalité (avis) | Draugar (5.7) | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
