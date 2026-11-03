# Carte teamsoccer — composition (ligue, coupe, barrages, amical ; deux clubs)

Sources lues : commit 7d27385 (2026-11-02)

Écrite le 2026-11-02 (fiche `tactique.md`, `resume.md`, skills `teamsoccer-match`, `-joueurs`, `-saison` ; connaissance § 1 et § 6 ; learnings). Règles : **deux clubs, un bloc chacun** (CLAUDE.md § Team Soccer) ; R-12 du 2026-10-30 (fiche complète 11 × 5 zones, banc, remplacements programmés, cible de chaque « Passer ») ; enregistrement au moins 2 h avant ; horizon aujourd'hui (un match de 13:50 se prépare la veille au soir).

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:109 | paramètres par compétition (coupe, amical, ligue) | var. 1, 13 |
| :148 | quelles tactiques | var. 4, 5 |
| :149 | tableau des joueurs, postes, remplacements et quand | Rendu 3-4 |
| :150 | 5 zones × dégager / passer / dribbler / centrer / tirer | var. 6 |
| :151 | consigne de jeu | var. 5 |
| :152 | stratégie selon nos matchs contre cet adversaire | var. 2 |
| :153 | stratégie selon toute la saison, blessés, forme, réussite | var. 3, 8, 9 |
| :160 | même ordre que l'écran | Rendu |

## Rendu (figé)
Pour chaque club (Chomelix Cows, puis Ben Ahmed Donkey), dans l'ordre de l'écran :
1. En-tête : `| Club | Adversaire | Compétition | Date (Paris) | Heure limite (Paris) | Enregistrée ? |` (`gold.ts_upcoming`).
2. `| Formation | Style | Mode (Avancé) |`.
3. Onze, emplacement par emplacement : `| Empl. | Poste | Joueur | Compétence clé | Forme | Ultra déf. | Défensive | Médiane | Offensive | Finition |` ; chaque « Passer » porte sa cible (défenseurs / milieux / attaquants) ; gardien = dégager seul ; pas de Finition pour défenseurs et gardien.
4. Banc de 6 : `| Banc | Joueur | Rôle couvert |`, puis `| Minute | Condition | Sort | Entre |` (remplacements programmés, 3 au plus, mi-temps comprise).
5. Plan B : blessure, carton (remplaçant nommé).

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Prochains matchs et heure limite | `select team, opponent, competition, venue, match_date_paris, lineup_deadline_paris, lineup_saved, saved_formation, opponent_is_bot, opponent_rating, my_rating from gold.ts_upcoming order by match_date_paris limit 8` | Composition modifiée moins de 2 h avant = non prise en compte ; sans composition le jeu choisit (Ajax 0-4) | connaissance 1.4, 7.7 ; L-023 | |
| 2 | Adversaire | `select club, date_paris, competition, adversaire, domicile, rang_adv, bilan_vnd, bp, bc, nos_scores_pour_contre from gold.ts_adversaires limit 6` ; ses matchs : lien « Voir les matchs » de son club | Bot = Neutre, ×0,90 et pénalité Gardien/Finition selon l'écart : reposer les fatigués et les suspendus potentiels | connaissance 1.14, 6.1, 6.3 ; L-010 | |
| 3 | Toute la saison | `select team, result, matches, with_detail, shots, opp_shots, on_target, conversion_pct, balls_lost, formations, vs_bots from gold.ts_vd_comparatif` | Comparer V / N / D, hors bots d'abord | CLAUDE.md règle 19 | |
| 4 | Formation | `saved_formation` ; `formations` de `gold.ts_vd_comparatif` | 1-4-3-3 avec 3 attaquants Finition 100 et 3 milieux Conduite 100 : 4-0, 0 tir encaissé ; retirer un 4e milieu faible | L-029, L-013 | 1-4-3-3 (Cows) |
| 5 | Style | skill match § Style | Contre un humain fort, ne pas tout miser sur l'attaque (2-4 contre Potatos, 10 tirs adverses / 9 cadrés) | L-026 | |
| 6 | Consignes par zone | `select zone, sous_role, name, key_name, key_skill, controle, forme from gold.ts_saisie_composition where team = '<club>'` ; tableau de la fiche tactique § Règles de consignes | Action = compétence la plus haute qui sert l'action (Passe → passer, Conduite → dribbler, Centres → centrer, Finition → tirer), Ultra déf. = dégager ; cohérente ×1,10, incohérente ×0,90 ; centraux ni centrer ni dribbler | skill match § Avancé ; fiche tactique | |
| 7 | Joueur au sous-rôle naturel | `sous_role`, `key_skill` de `gold.ts_effectif_bilan` | Hors sous-rôle naturel = note plus basse ; milieu faible structurel Ben Ahmed (Schmidt, Suzuki : position GK, Passe 84/81) | skill joueurs ; L-007, L-015 | |
| 8 | Forme | `forme`, `key_at_match` de `gold.ts_saisie_composition` | Valeur = compétence × (0,70 + 0,30 × Forme/100) ; préférer un remplaçant en forme à un titulaire < 60 ; Forme = plafond de rendement | `resume.md` ; connaissance 4.9 | |
| 9 | Blessés, cartons | `select team, name, injury_days, suspended, yellow_cards from gold.ts_effectif_bilan where unavailable or yellow_cards >= 2 limit 10` | Suspension : 2 jaunes selon le skill joueurs, 3 selon le forum (6.11) : lire l'écran ; blessure liée à la Forme | skill joueurs ; connaissance 6.11, 6.12 | |
| 10 | Banc et remplacements | fiche tactique § Livrable | Remplacements à programmer (minute, sortant, entrant) ; banc vide au pré-calcul = à 10 sur blessure ; 3 changements au total, aucun à 10 | connaissance 1.3, 1.9, 7.8 | |
| 11 | Dépendance à un joueur | `select player, matches, avg_rating, goals, involvements from gold.ts_player_match_ratings order by goals desc limit 8` | Cows : Ounahi (buts de la tête) ; Ben Ahmed : Yamamoto (7 des 8 buts) : prévoir le remplaçant nommé | L-002, L-006 | |
| 12 | Coups de pied arrêtés et têtes | `my_headers`, `my_penalties`, `my_posts` de `gold.ts_match_report` | Buts surtout sur penaltys et têtes, peu en jeu ouvert | L-001, L-017 | |
| 13 | Domicile / extérieur | `venue` de `gold.ts_match_report` | À l'extérieur 13-14 attaques et 2-7 tirs contre 19-24 à domicile | L-024 | |
| 14 | Notes et secteurs | `my_sector_avg`, `my_weakest_zone` | Les notes dépendent de la composition, pas du déroulé ; le secteur dépend surtout du nombre de joueurs | fiche match ⚠️ ; connaissance 1.8 ; L-019 | |
| 15 | Composition réellement jouée | `silver.ts_match_lineups` | Trou de données sur les coupes (21, 22, 28/10) : formation NULL = exporter la page du match | L-016, L-027 | |
| 16 | Amical | connaissance 6.9 | Un par semaine, bloqué tant qu'on est en Coupe nationale ; pas de blessure ni de carton reporté : un test à la fois | connaissance 6.9 | |
| 17 | Réussite récente | `my_posts`, `opp_gk_sector`, `my_conversion_pct` | Poteaux et gardien adverse expliquent un déficit de buts : ne pas changer un XI qui crée | L-011, L-028 | |
| 18 | Avis des amis | connaissance § 1, § 6 | Placer défenseurs et milieux en tir = dribbler, dribbler, tirer, au prix de ballons pour les attaquants | PIPO68 2026-09-15 (1.7) | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|
| L-001 | Peu de buts en jeu ouvert : la finition des attaquants d'abord | 2026-11-02 | à surveiller |
| L-002 | Cows dépendants d'Ounahi | 2026-11-02 | à surveiller |
| L-006 | Ben Ahmed dépendant de Yamamoto | 2026-11-02 | à surveiller |
| L-007 | Milieu Ben Ahmed = point faible structurel | 2026-11-02 | confirmé (L-015) |
| L-010 | Victoires contre bots : ne prouvent presque rien | 2026-11-02 | confirmé |
| L-011 | Poteaux et gardien adverse : ne pas casser un XI qui crée | 2026-11-02 | à surveiller |
| L-013 | 1-4-3-3 retire le 4e milieu faible | 2026-11-02 | confirmé (L-029) |
| L-015 | Schmidt-Suzuki à 5,5, secteur Milieu le plus faible | 2026-11-02 | confirmé |
| L-016 | Compositions de coupe absentes de la base : exporter le match | 2026-11-02 | récurrent (L-027) |
| L-017 | Dominance : buts de la tête | 2026-11-02 | à surveiller |
| L-019 | XI stable = notes stables | 2026-11-02 | confirmé |
| L-023 | Toujours enregistrer : sans composition, défaite 0-4 | 2026-11-02 | confirmé |
| L-024 | Extérieur : moitié moins d'attaques | 2026-11-02 | à surveiller |
| L-027 | Coupes du 28/10 sans lignes en base | 2026-11-02 | récurrent |
| L-028 | 0-0 contre bot : volume normal, gardien adverse | 2026-11-02 | à surveiller |
| L-029 | 1-4-3-3 Finition 100 / Conduite 100 : 4-0 | 2026-11-02 | à surveiller (1 match) |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
