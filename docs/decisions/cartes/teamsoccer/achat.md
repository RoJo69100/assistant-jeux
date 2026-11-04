# Carte teamsoccer — achat (enchère banque ou manager ; deux clubs, deux marchés)

Sources lues : commit 7d27385 (2026-11-02)

Écrite le 2026-11-02 (fiche `transferts.md`, skills `teamsoccer-club` § Marché, `-joueurs` ; connaissance § 5). Règles : finançable d'abord (`capacite_invest`, règle apprise 16) sinon cible abandonnée ; jamais d'enchère sans accord ; Cows = marché masculin, Ben Ahmed = marché féminin, économies séparées ; règle 20 (marché de plus de 24 h = « exporte le marché »).

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:124 | acheter un joueur ? | var. 1, 4 |
| :138 | base « ce type vaut ce prix » | var. 6 |
| :139 | étudier le marché, acheter / revendre | var. 1, 7 |
| :168 | beaucoup d'argent | var. 4 |

## Rendu (figé)
1. Marché exporté il y a plus de 24 h : « 🟥 URGENT · Export · exporte le marché (Cows et Ben Ahmed) » (`gold.ts_exports_state`).
2. Un tableau par club : `| Priorité | Cible | Zone | Âge | Compétence clé | Contrôle | Titulaire le plus faible (clé) | Gain | Prix actuel | Offres | Enchère max | Fin (Paris) | Finançable |`.
3. Une ligne par cible : pourquoi, ce qui prouvera l'erreur. Cible non finançable = une ligne « abandonnée ».

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Cibles | `select team, zone, name, age, key_skill, controle, weakest_starter, weakest_starter_key, gain_key, asking_price, bids, deadline_paris, financable from gold.ts_marche_cibles order by team, gain_key desc limit 20` | Meilleure que le titulaire le plus faible sur la compétence clé du poste, jamais l'OVR | `resume.md` § Juger un joueur | |
| 2 | Club de l'annonce | `silver.ts_transfer_listings.market` | Masculin → Cows, féminin → Ben Ahmed | `resume.md` § Jeu | |
| 3 | Forme de la cible | — | Un nouveau joueur commence à Forme 85 ; la Forme de l'annonce ne compte pas | fiche transferts § 3, 5 | |
| 4 | Argent disponible | `select team, balance, wage_bill, reserve_2_weeks, decided_not_settled, decided_list, capacite_invest, finances_age_days from gold.ts_capacite_invest` | Enchère max > `capacite_invest` = abandon ; solde négatif = aucun achat ; le jeu refuse une enchère > solde à l'instant | règle apprise 16 ; fiche transferts § Enchère et solde | |
| 5 | Limites | `squad_size` ; registre `fait-` (achat de la semaine) | 1 achat par semaine (enchères en tête comprises), remise à zéro lundi 00:00 Canaries ; effectif ≤ 24 enchères comprises ; revente bloquée 7 semaines | skill club ; connaissance 5.4 | |
| 6 | Prix | `asking_price`, `bids` ; `silver.ts_player_snapshots` (valeurs) | Départ ≈ 0,99 × valeur ; chaque offre ≈ +8,2 % ; enchère max = 3 offres de marge (×1,28) | fiche transferts § Prix et valeur [Obs 2026-10-23] | |
| 7 | Revente | valeur des jeunes `gold.ts_player_progress.d_value` | Jeune : valeur +4,4 à +6,4 % par semaine ; revente après 7 semaines | fiche transferts § Historique de valeur | |
| 8 | Salaire | `value` | ≈ 1 % de la valeur par semaine | fiche transferts § 3 | |
| 9 | Moment | `deadline_paris` | Une enchère se joue dans les dernières heures ; vente de financement à la banque le matin de la fin | fiche transferts § Règle d'attente | |
| 10 | Mes enchères | `silver.ts_my_bids` | Vérifiées à chaque passage (en tête, battue, gagnée) | CLAUDE.md règle 11 | |
| 11 | Idole / Magique | talent de la cible | Idole dans l'effectif = affluence ×1,5 à domicile, même sans jouer | connaissance 2.3 | |
| 12 | Avis des amis | connaissance § 5 | Marché sans joueur de chaque pays (aléatoire) ; enchère « terminated » encore cliquable | connaissance 5.5, 5.6 | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
