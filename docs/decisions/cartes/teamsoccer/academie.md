# Carte teamsoccer — academie (révélations, montée des jeunes, Centre de Haute Performance ; deux clubs)

Sources lues : commit 7d27385 (2026-11-02)

Écrite le 2026-11-02 (fiche `academie.md`, skills `teamsoccer-entrainement` § Académie et § HPC, `-joueurs` ; connaissance § 3). Règles : compter les jeunes complets à chaque export (règle apprise 17) ; ne jamais utiliser les compétences non révélées présentes dans l'API ; les TSC sont ceux du compte, partagés entre les deux clubs.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:115 | comprendre l'académie (3 jeunes visibles par jour) | var. 1, 2 |
| :116 | monter un jeune ou non | var. 3, 4 |
| :117 | le monter et le vendre ? | var. 4 |
| :130 | joueur de l'académie ou non | var. 7 |

## Rendu (figé)
Un tableau par club : 1) `| Révélation | Jeune | Compétence à révéler |` (1 par jour) ; 2) `| Jeune | Âge | Poste | Révélées /10 | Compétence clé | Titulaire le plus faible (clé) | Verdict | Blocage |` ; 3) HPC (compte) : `| TSC compte | TSC investis | Manque pour 50 | Lundis restants | Options de la semaine |`.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Révélations du jour | `select team, name, position, revealed_count, best_revealed, hidden_skills, team_reveals_left_today from gold.ts_academy order by team, revealed_count desc limit 32` | 1 par jour et par club, remise à zéro 01:00 UTC ; révéler d'abord Gardien, Défense, Conduite, Finition (déduction) | fiche académie § 1-2 | |
| 2 | Jeunes complets | `revealed_count = 10` | Compter par club à chaque export | règle apprise 17 | |
| 3 | Verdict | `select team, name, age, position, revealed_count, key_col, key_skill, weakest_starter, weakest_starter_key, squad_size, verdict, blocage from gold.ts_academie_verdict order by team limit 32` | MONTER si la clé dépasse le titulaire le plus faible, effectif ≤ 24 | fiche académie § 3 | |
| 4 | Monter pour vendre | carte `vente` var. 3 | Valeur d'un jeune monte de 4-6 % par semaine ; blocage de revente d'un jeune promu : inconnu, à lire à l'écran Vente au premier cas | fiche transferts § Historique de valeur | |
| 5 | Niveau de l'académie | `silver.ts_youth_academies` | Totaux 250 / 300 / … / 500 (±25) selon le niveau, aucune compétence > 75 à la création ; niveau qui monte avec les jeunes complétés | connaissance 3.3, 3.5 | |
| 6 | Talent | — | Visible seulement après la montée (7 %, Magique 3 %) | connaissance 3.2 | |
| 7 | Origine du joueur | `silver.ts_players` | Les jeunes ne vieillissent pas au changement de saison ; seuls les promus changent d'âge | connaissance 3.6 | |
| 8 | HPC | `select team, status, total_tsc, account_tsc, tsc_needed, can_complete, mondays_left, week_options, chosen_skills from gold.ts_hpc_status` | 50 TSC investis dans la saison sinon remboursés ; un seul joueur HPC par club ; la compétence demandée n'est pas garantie ; promouvoir le jeune de la saison passée d'abord | connaissance 3.8-3.13 | 45 TSC au compte, 0 investi (19/10) |
| 9 | Avis des amis | connaissance § 3 | Un 16 ans n'est pas meilleur qu'un 14 ans (aléatoire) | connaissance 3.1 | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis | Statut (base) |
| --- | --- | --- | --- | --- |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
