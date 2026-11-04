# Carte derbymanager — composition (Squad : formation, rôles, curseurs, options, banc, set pieces ; deux clubs)

Sources lues : commit b154711 (2026-11-04)

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

## Valeurs du jour (police 2026-11-02, export 01/11)
- 547 GK : Vigerie (Key 75 %, condition 100, forme 26, slot S3, 0 % satisfait) contre Kjer (forme 21, titulaire, 100 % satisfait pour 25 % attendus). Forme à impact réduit pour GK (connaissance § 3, 2024-11-22) et les gardiens perdent peu de condition (2026-10-30) : Vigerie titulaire.
- 547 forme basse : Bjerg 13, Kjer 21, Vigerie 26 ; condition 83-100 %.
- 307 Marmandes (corrigé par police 2026-11-02 pm) : squad, training et school exportés le 31/10 17:58-18:00 (22 joueurs dans `gold.dm_effectif`), finances/facilities/marché le 30/10 22:55 ; seul overview + régions ont été ré-exportés le 01/11. Composition faisable sur l'export du 31/10 (récupération de condition ≈ +2 à +4 %/jour selon l'intensité). Blessés 307 : Cave, Taddei (« Bruised for 1 match, can play but better not »). Intensité 307 : pill REST, valeur à relever.

## Valeurs du jour (police 2026-11-04, export 307 du 04/11 21:55)
- Effectif 307 : 20 joueurs. Partis : Charbonnier (FC, 27 ans) vendu à Almería 6,5 M le 1er nov ; Aponte (FC, 22 ans) vendu à Venezia 8,3 M le 2 nov (`silver.dm_transfers`, page transfers 37146). Ligne F réduite à Vasilev 13,5, McCulloch 12,5, Vargas 12,3, Ohara 11,8, Luzerne 10,2.
- Prochain match : Nov 5, Quatrième ligue round 1, domicile, Raon-l'Étape 11e (`silver.dm_fixtures`, bloc 307). Amicaux joués : Nov 3 Everton L 1-2, Nov 4 Liège (1er BE1) L 2-4 ; `gold.dm_matchs` n'a pas encore ces matchs.
- Formation 307 en ligue : 343 = 8 matchs, 3 V 4 N 1 D, xG contre 0,79 ; 352 = 22 matchs, 5 V 4 N 13 D, xG contre 1,88 (`gold.dm_saison_bilan`). Les chiffres de notre saison battent l'avis général : 343.
- Aucun blessé (`gold.dm_saisie_squad.blessure` vide) : Cave (condition 100) et Taddei (89) sont jouables ; le brouillon du 02/11 les mettait au repos (blessure « Bruised » disparue).
- Les 11 de l'amical Liège (forme > 0, condition 85-94) : Comonfort, Messimy, Desagnat, Schmitz, Lévêque, Taddei, Cleary, Lerch, Vasilev, Vargas, Luzerne. Reposés (forme 0, condition 100) : Lafleur, La Ferrière, Cave, McCulloch, Bodian, Labourd, Hardt.
- Curseurs exportés : DL 2, PP 0, PF 2, SH 2, HE 2.

## Valeurs du jour 547 (police 2026-11-04, export 21:59-22:02)
- Mansfield (DC, 22 ans, 16,0) acheté le 3/11 (`silver.dm_transfers`) : CD à la place de Pilot (14,4). XI 541 stable sinon (Vigerie GK, Kjer EMR). Prochain : Nov 5 Partick Thistle (ext., 6e, xG concédé 1,07 dans `gold.dm_adversaires`). Curseurs DL 0, PP 2, PF 2, SH 2, HE 2 (`silver.dm_tactic`). Options non exposées par silver : lire l'écran. Amicaux Nov 3 L 0-2, Nov 4 D 0-0 (`silver.dm_fixtures`), pas encore dans `gold.dm_matchs`/`dm_saison_bilan`.

## Variables ajoutées par la police 2026-11-04 (tactique 307)
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 14 | Options cochées (Pressing, Counters, Through balls, Run with ball) | `select substring(payload->>'html' from position('PRESSING' in upper(payload->>'html')) - 1500 for 3500) from bronze.raw_pages where id = <dernière page teams_id_squad-tab du club>` (MCP `execute_sql` ; `sql.py` refuse le payload entier) ; `name="counters"` + `checked=""` = cochée. Valeurs des 5 curseurs : `value=` des `<input type="range">` (0-2) | Silver ne lit pas les options : toujours les lire dans le html brut | police 2026-11-04 | 307 (page 37131) : Counters seule ; DL 2 High, PP 0 Short, PF 2 Wide, SH 2 From box, HE 2 Prioritise |
| 15 | Slots et rôles réels | `select ordre, poste, role, name, note_poste, condition, forme, set_pieces from gold.dm_saisie_squad where team_id = '307' order by ordre` (`team_id` et `club` sont du texte : `'307'`, `'Marmandes'`) | Les slots exportés donnent la formation réelle (3 DEF + 4 M + 3 F = 343) ; l'étiquette « titulaire 541 » de `gold.dm_verdict_joueurs` / `dm_contrats` est un libellé fixe, pas la formation jouée | police 2026-11-04 | 307 : DLC LD, DC CD, DRC LD, MLC CM, MRC DLP, MR DWG, ML DWG, FLC FN, FC CF, FRC FN, GK GK (aucun slot 541) |
| 16 | Même adversaire dans la formation | `select formation, opponent, jour, my_result, xgf, xga from gold.dm_matchs where team_id = 307 and compet = 'Ligue' and opponent = '<adv>'` | 343 n'a été joué que contre Vichy, Istres, Raon, Yzeure ; 352 ne les a jamais affrontés : la comparaison 343/352 est biaisée par l'adversaire (échantillon non apparié) | police 2026-11-04 | Raon : 343 D 0-0 (xG 0,34-0,41) et W 1-0 (1,51-0,52) ; 352 contre Grenoble, Pau, Poitiers, Luçon : 5 V 2 N 1 D, xG 1,81-1,52 |
| 17 | Rôle → compétences à lire | `silver.dm_squad` colonnes `mar, tac, posi, ant, cre, pas, bu, pbu` | DLP = création + passes (BU 4/4) ; DWG = prévention (BU 4/PBU 7, dépense 8) : mettre au DWG le milieu qui tacle, au DLP celui qui crée | connaissance l.72, l.76 (dev 2025-02-07, 2026-10-19) | Cave cre 18 pas 20 (DLP) mais mar 8 tac 7 ; Lévêque mar 4 tac 4 ; Lerch tac 13, PBU 7 au DWG ; Cleary tac 18, PBU 8 |
| 18 | Rang adversaire | `silver.dm_fixtures.opp_rank` (récent) contre `gold.dm_adversaires.rang_adv` (classement exporté plus tôt) | Si les deux diffèrent, le rang du calendrier fait foi | police 2026-11-04 | Raon : 11e (fixtures) contre 13e (dm_adversaires) ; 4-15-11, 16 buts pour, xG concédé 0,47 |

## Valeurs du jour (police 2026-11-04 23:30, tactique 307 contre Raon-l'Étape, domicile)
- Formation 343 (slots exportés). XI : Lafleur ; Desagnat DLC LD, Messimy DC CD, La Ferrière DRC LD ; Taddei MLC CM, Cave MRC DLP, Cleary MR DWG, Lerch ML DWG ; Vargas FLC FN, Vasilev FC CF, McCulloch FRC FN. Banc : S1 Comonfort EMR, S2 Ohara RAT, S3 Hardt DEV, S4 Labourd DEV, S5 Lévêque CON. Curseurs et options inchangés (écran 21:55).
- Set pieces : PEN Vargas, FK Vargas, COR Cave, capitaine Cleary, DEF BOX Messimy + La Ferrière, ATT BOX Vasilev + McCulloch + Messimy (`gold.dm_setpieces` rangs).
- Contrats à 0 j : Desagnat, McCulloch (`gold.dm_contrats`).

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|
| L-002 | 352 à écarter ; 541 contre plus fort à tester | 2026-11-02 | à contrôler (C-001) |
| L-003 | XI stable pour faire monter la forme | 2026-11-02 | à contrôler (C-008) |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
