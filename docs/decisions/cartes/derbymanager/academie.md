# Carte derbymanager — academie (school : promouvoir / libérer, scouting des jeunes ; deux clubs)

Sources lues : commit 87dc954 (2026-11-02)

Écrite le 2026-11-02 (`resume.md`, skill `derbymanager-effectif-entrainement` § School, § Scouting ; connaissance § 6, § 8 ; learnings). Un bloc par club.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-DM.txt:11 | fonctionnement de la school, durée, choix, progression | var. 1-4 |
| :12 | scouter le joueur ? | var. 6 |
| :13 | intégrable dans le club après scout ? | var. 5 |

## Rendu (figé)
Un tableau par club : `| Jeune | Poste | Âge | Jours restants | Compétences clés | Rapport de potentiel | Notre dernier titulaire au poste | Coût (salaire = installations) | Décision (promouvoir / garder / libérer) |`.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Jeunes à l'école | `silver.dm_school` | 4 jeunes au plus ; salaire = coût des installations (hors plafond salarial, compte contre le revenu) | connaissance § 6 (S25) | Almgren, Minkkinen (30/10) |
| 2 | Durée et redistribution | `silver.dm_school` (jours restants) | Tous les jeunes sont libérés et redistribués au début de chaque saison ; promouvoir pour garder | connaissance § 6 (2026-06-16/17) | |
| 3 | Croissance | — | ~2-3 étoiles à l'école sans temps de jeu ; un promu sans minutes ne grandit pas | connaissance § 6 | |
| 4 | Coût | `gold.dm_finances_bilan.youth_school` | Installations dans les 40 : 1 an d'école + 3 ans ≈ 6 M ; dans les 20 : ≈ 3 M ; en D4 seulement des « 3 M » | connaissance § 6 | |
| 5 | Intégrable | `gold.dm_verdict_joueurs` (note au poste du dernier titulaire) | Promouvoir si le jeune approche le dernier titulaire ou remplace un départ ; promotion impossible à 25 joueurs ; statut raisonnable (pas Key) | connaissance § 6, § 13 | |
| 6 | Scouting des jeunes | — | Les 5 jeunes découverts ont déjà un scout, il en faut 2 de plus ; niveau 2 = potentiel et expérience | dev 2026-10-18 ; connaissance § 8 | |
| 7 | Team spirit | `effet_ts_pct` | École ≈ −1 % de team spirit par jeune (fringe) | dev 2026-08-19 | |
| 9 | Almgren (547) | `silver.dm_school` ; brief 2026-10-30-plan § 4 | MR 19 ans, passing 16, positioning 19, 55 j au 30/10, « high potential to become a lower division player » ; Minkkinen 16 ans 88 j. Promotion impossible à 25 joueurs : nombre d'effectif à relever (`count(*) from gold.dm_effectif where club = 547`) | police 2026-11-02 | Absent de l'effectif au 01/11 |
| 10 | Échelle des tiers de potentiel | `gold.dm_prix_reference` (médiane par tier) | Fringe 2,5 M < Useful 4,5 < Lower division 6,8 < Solid 11,0 < Established 15,3 : « solid player » vaut mieux que « lower division player » | police 2026-11-02 | Beth (307) high → solid ; Loría, Almgren high → lower division ; Minkkinen moderate → established |
| 11 | Quand le jeune part | `silver.dm_school.days_left` | Données : Almgren 55 j (30/10) → 53 j (01/11), pas de remise à zéro ; contrat d'école ≈ 105 j (99-104 j pour les 16-17 ans). La redistribution « début de saison » (2026-06-17) est modifiée par les contrats d'1 an (2026-08-22/24) : la fin se lit sur `days_left`, pas sur la date de saison | connaissance § 6 ; police 2026-11-02 | |
| 12 | Coût d'un jeune à l'école | `gold.dm_finances_bilan.youth_school` / nombre de jeunes | 547 : 22 k/j pour 2 = 11 k ; 307 : 21 k/j pour 3 = 7 k | police 2026-11-02 | |
| 8 | Avis des amis | connaissance § 6 | Dev : jamais vu de jeune « D1 worthy » issu de l'école ; « Facilities as a bet » | connaissance § 6 | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
