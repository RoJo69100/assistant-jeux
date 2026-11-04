# Carte derbymanager — defaite (analyse d'une défaite ; deux clubs)

Sources lues : commit eba50d0 (2026-11-02)

Écrite le 2026-11-02 (`resume.md`, skills `derbymanager-tactique`, `-regles` ; connaissance § 12 ; learnings). Règles : résultat = `my_result` de la base ; analyse contre toute la saison (`gold.dm_saison_bilan`, `gold.dm_tirs_profil`) ; `analyste` d'office.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-DM.txt:37 | analyser les match reports | var. 2-6 |
| :62 | selon le manque de réussite récent | var. 4 |

## Rendu (figé)
Un bloc par club : 1) `| Match | Compét. | Lieu | Score | xG pour / contre | Possession | Tirs pour / contre | Contres | Corners | Fautes | Force nous / eux |`, puis moyennes V et D de la saison ; 2) `| Origine des tirs | Tirs | Dans la surface | Têtes | Buts | xG |` (pour / contre) ; 3) `| Cause | Chiffre | Comparaison saison | L-nnn |` ; 4) `| Priorité | Catégorie | Correction (fais X) | Ce qui prouvera l'erreur | Match test |`.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Résultat | `select club, jour, compet, opponent, lieu, gf, ga, my_result, xgf, xga, poss_pct, formation, tirs_pour, tirs_contre, force_nous, force_eux from gold.dm_matchs order by jour desc limit 10` | Toujours `my_result` | CLAUDE.md règle 7 | |
| 2 | Saison | `gold.dm_saison_bilan` | Comparer par compétition et par formation | L-001, L-002 | S26 : 2 V 4 N 26 D |
| 3 | Origine des tirs | `select club, camp, origine, tirs, dans_surface, tetes, buts, xg, conversion_pct from gold.dm_tirs_profil` ; `silver.dm_shots` | Taux : normal ~18 %, long ~14 %, tête ~18 %, penalty ~73-80 % | connaissance § 11 (2026-04-22) | |
| 4 | Réussite et xG | `xgf`, `xga`, `xpts` | xG affiché ≠ vérité du match ; barème xPts du dev | connaissance § 12 | |
| 5 | Écart de puissance | `force_nous`, `force_eux` | 56 % contre 44 % = 30 % plus puissant ; gros écart = défaite probable : jouer défensif | connaissance § 12 | |
| 6 | Joueurs | `gold.dm_effectif` (`rating`, `apps`, `goals`) ; `gold.dm_verdict_joueurs` | Les notes montent si l'équipe gagne ; GK sans travail = 6 | connaissance § 13 | |
| 7 | Forme, condition | carte `composition` var. 7 | Forme basse malgré condition correcte (rotation) | L-003 | |
| 8 | Nos réglages | `formation` ; `silver.dm_tactic` | Options cochées = condition ; 13 dots de build up | carte `composition` var. 6, 11 | |
| 9 | Série | `my_result` des 5 derniers | Deux défaites d'affilée : `analyste` + `decideur` | CLAUDE.md usage des agents (4) | |
| 10 | Conseils appliqués | `outputs/derbymanager/learnings.md` § Conseils | Chaque C-nnn confronté ; deux échecs = réécrit | CLAUDE.md § Amélioration continue | C-001 à C-008 à contrôler |
| 11 | Avis des amis | connaissance § 11, § 12 | « Rien dans le moteur ne fait perdre exprès » ; élan ≈ 1 % par but d'écart, sur le build up seulement | dev (connaissance § 12) | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis | Statut (base) |
| --- | --- | --- | --- | --- |
| L-001 | Défaite par volume concédé, pas par finition | 2026-11-02 | confirmé S26 | ✅ validée (32 pour / 0 contre) |
| L-002 | 352 : 10 D sur 10 | 2026-11-02 | confirmé S26 | ✅ validée (28 pour / 0 contre) |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
