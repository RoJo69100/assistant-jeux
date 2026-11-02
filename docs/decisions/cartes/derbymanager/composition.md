# Carte derbymanager — composition (Squad : formation, rôles, curseurs, options, banc, set pieces ; deux clubs)

Sources lues : commit 0000000 (2026-11-02)

Écrite le 2026-11-02 (`resume.md`, skills `derbymanager-tactique`, `-regles` ; connaissance § 3, § 11, § 12 ; learnings). Règles : deux clubs, un bloc chacun (Queen of the South 547 puis Marmandes 307) ; poste par poste dans l'ordre de l'écran Squad ; ligue et coupe = compo de référence, amical = compo de test (jeunes, autre formation) ; horizon aujourd'hui.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-DM.txt:6 | coupe / amical / ligue : preset et tests | var. 1, 13 |
| :8 | gérer deux équipes distinctes | Rendu |
| :57 | quelles tactiques (442, 343…) | var. 3 |
| :58 | curseurs et options | var. 5, 6 |
| :59 | set pieces, remplaçants, capitaine | var. 8, 9 |
| :60 | tableau : poste, set pieces, tactique | Rendu |
| :61 | stratégie selon nos matchs contre cet adversaire | var. 2 |
| :62 | stratégie selon toute la saison, blessés, forme, réussite | var. 4, 7, 10 |

## Rendu (figé)
Pour chaque club, dans l'ordre de l'écran Squad :
1. `| Club | Adversaire | Compétition | Lieu | Formation |`.
2. `| Poste (grille) | Rôle | Joueur | Note au poste | Forme | Condition | Cœur |` de DL à FR, puis GK.
3. `| Curseur | Valeur |` : Defensive line, Pass preference, Pass focus, Shooting, Headers ; `| Option | Cochée |` : Pressing, Counters, Through balls, Run with ball.
4. `| Banc | Joueur | Statut d'entrée (RAT / CON / AUTO / DEV / IMP / EMR) |` S1 à S5.
5. Set pieces : `| PEN | FK | COR | DEF (placements) | ATT (placements) | Capitaine |` (`gold.dm_setpieces`).

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Compétition | `silver.dm_fixtures` ; `gold.dm_matchs.compet` | Ligue / coupe = référence ; amical = test d'une seule chose | `resume.md` § Ce que l'utilisateur attend | |
| 2 | Adversaire | `select club, competition, rang_adv, adversaire, bilan_vnd, bp, bc, forme_adv, nos_resultats, xg_concede_moy from gold.dm_adversaires limit 16` | Contre plus fort : 541 défensif, FB plutôt que WB ; contre des attaquants larges FB + DLP + BTB, contre étroits IWB + 2 BTB | dev #italy 2025-08-13, 2025-02-07 ; connaissance § 11 | pas de calendrier à venir exporté |
| 3 | Formation | `select club, compet, formation, j, v, n, d, xg_pour_moy, xg_contre_moy, tirs_pour_moy, tirs_contre_moy from gold.dm_saison_bilan` | 352 = 10 D sur 10 (S26) ; bots : 433 1,82 pt/match, 442 1,79, 343 1,77 ; formations non standard très perdantes | L-002 ; connaissance § 11 | 541 (C-001) |
| 4 | Joueur par poste | `select club, ligne, rang_ligne, name, pos, note_poste, niveau_equipe, forme, condition, coeur_txt from gold.dm_verdict_joueurs order by club, ligne, rang_ligne limit 60` ; `gold.dm_poste_scores` [H] | Pénalité de famille de poste : jusqu'à 25 % même ligne, 50 % autre ligne, 75 % au but | connaissance § 3 (2024-10-28) | |
| 5 | Curseurs | `silver.dm_tactic` | Ligne défensive = positionnement seulement ; pass focus narrow = plus de points au centre ; short passing vers CM/BTB hauts | connaissance § 11 | Low / Direct / Wide / From box (C-001) |
| 6 | Options | `silver.dm_tactic` | **Chaque option cochée = −1 % de condition pour tous** ; Pressing consomme plus ; contre joué si le ratio défenseurs/attaquants le permet | `resume.md` § Écrans ; connaissance § 11 | Counters seule |
| 7 | Forme, condition, cœur | `forme`, `condition`, `coeur_txt` de `gold.dm_verdict_joueurs` | Forme monte à chaque match joué, baisse sinon ; blessure ≈ condition manquante : jouer au-dessus de 80 % ; sharpness = forme + club fit + aléa | connaissance § 3 ; L-003 | |
| 8 | Banc | statuts S1-S5 | 5 remplaçants ; CON remplace sous 80 % ; RAT note < 6,5 ou 0,5 sous la moyenne ; DEV minutes d'un jeune ; EMR blessure seulement ; changements vers 55e-65e minute | connaissance § 11 (2026-10-21/25) ; reprise 2026-10-31 § 2 | |
| 9 | Set pieces | `select club, name, pos, finition, precision, passe, aerien, tete, rang_penalty, rang_coup_franc, rang_corner, rang_surface, rang_capitaine, verdict from gold.dm_setpieces order by club limit 30` | Preneur parmi les 3 meilleurs ; 6 joueurs aux valeurs les plus hautes montent ; finishing → PEN, long shots → FK, crossing → COR (en partie renommé 2026-04-05) | connaissance § 11 | « très importants » [U 2026-11-01] |
| 10 | Toute la saison | `gold.dm_saison_bilan`, `gold.dm_tirs_profil` | Défaite par volume concédé (16,7 tirs contre) : prévention du build up d'abord | L-001 | |
| 11 | Build up | écran « Test your tactic » (BU/PBU par rôle) ; `bu`, `pbu` | 13 dots (5 pressing + 8 build up), −10 % par dot vide ; défenseurs empêchent, milieux créent, attaquants ≈ 0 | dev 2026-10-21 ; connaissance § 12 | |
| 12 | Temps de jeu | `temps_jeu_satisf_pct`, `temps_jeu_attendu_pct` | Key 75 %, First team 60 %, Rotation 40 %, Backup 25 % | dev 2026-08-20 | |
| 13 | Avis des amis | connaissance § 11 (conseils de joueurs) | 442 et ligne plus haute à domicile, 541/451 ligne basse à l'extérieur (avis) | connaissance § 11 (en doute) | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|
| L-002 | 352 à écarter ; 541 contre plus fort à tester | 2026-11-02 | à contrôler (C-001) |
| L-003 | XI stable pour faire monter la forme | 2026-11-02 | à contrôler (C-008) |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
