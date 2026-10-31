# Carte basketvibe — achat (enchère, joueur libre)

Sources lues : commit 58975fe (2026-10-31)

Écrite le 2026-10-31 (skills transferts, économie, entraînement ; vues gold du marché). Règles : A-4 (jamais d'enchère lancée sans accord), CLAUDE.md « capacité moins dépenses décidées », règle 20 (cibles nommées, marché de plus de 24 h = « exporte le marché »).

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:20 | acheter un joueur ? | var. 8 |
| :36 | base « ce type vaut ce prix » | var. 5 |
| :37 | étudier le marché, acheter/revendre | var. 1-6 |
| :168 | beaucoup d'argent | var. 8 |

## Rendu (figé)
1. Si le dernier export du marché a plus de 24 h : première ligne « 🟥 URGENT · Export · exporte le marché » (`gold.bv_exports_state`).
2. `| Priorité | Cible | Poste | Âge | PS | Emplacement / fit | Gain vs notre n°2 | Prix actuel | Enchère max proposée | Salaire/sem. | Fin (Paris) | Finançable |`.
3. Une ligne par cible : pourquoi, et ce qui prouvera l'erreur. Rien n'est lancé sans l'accord de l'utilisateur.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Candidats qui améliorent l'effectif | `select name, position, age, ps, best_slot, best_fit, my_best_fit, my_second_fit, gain_vs_my_second, enters_top8, est_weekly_salary, current_price, ends_paris from gold.bv_market_candidates order by gain_vs_my_second desc limit 10` | Gain réel = meilleur que notre n°2 à l'emplacement ; entre dans le top 8 (sinon TS inchangé) | [M§2.2] TS = 8 meilleurs | |
| 2 | Bonnes affaires (revente) | `select name, age, ps, price_now, ref_median, discount_pct, bid_ceiling_resale, resale_margin_median, ends_paris, ref_reliable from gold.bv_market_bargains where ref_reliable order by discount_pct desc limit 10` | Marge nette après taxe 5 % ; revente après 7 jours | skill transferts § Vendre [M§11.1] | |
| 3 | Âge et progression | `age` + `gold.bv_age_factor` | ≥ 30 ans : 0 progression ; ≥ 31 : déclin chaque dimanche | [M§8.5] | |
| 4 | Potentiel | test 25 000 (Low / Decent / High), une fois par club et par joueur | Potentiel 7 ≈ 8 en progression (×1,50 contre ×1,60) mais moins cher | [M§8.3] ; avis dcarra 2026-10-14 | |
| 5 | Prix de référence | `select age_band, position, n, p25, median, p75 from gold.bv_market_price_ref` ; `gold.bv_price_ref_ps` ; `gold.bv_transfer_history` | Enchère max ≤ médiane de la référence sauf gain sportif chiffré ; 3 étoiles de 16 ans : 3,5-4 M (avis) | connaissance 2026-10-29 ; skill transferts § Prix constatés | |
| 6 | Salaire | `est_weekly_salary` ; `gold.bv_salary_scale` | Salaire = moyenne des 8 compétences ; recalculé en fin de saison | [M§10.2] | |
| 7 | Règles d'enchère | skill transferts § Acheter | Enchère max automatique ; anti-snipe 3 min ; phase finale à l'aveugle ; somme des maximums ≤ solde | [M§11.3, §10.3] | |
| 8 | Argent disponible | `select balance, transfer_available, transfer_committed from gold.bv_finance_health` + `gold.bv_finance_s2_projection.investable_now_end_s1` − dépenses déjà décidées (`outputs/basketvibe/fait-*.md`) | Prix max > capacité restante = cible abandonnée | CLAUDE.md § Horizon | |
| 9 | Effectif après l'achat | `select count(*) from gold.bv_roster_now` | Minimum 8 disponibles ; marge actuelle à vérifier | [M§11.1] | |
| 11 | Prix faussés | — | Ne pas caler l'enchère max sur les ventes du 27/09 au 04/10 ni sur des ventes entre comptes suspects | Transferts truqués suspectés (60 k → 850 k), 5 comptes bannis le 08/10 ; connaissance § lecture des joueurs (avis, non vérifié) | |
| 12 | Agent libre | — | Potentiel entre 3 et 9 (jamais 1-2 ni 10) ; aucun joueur de 20-21 ans sur le marché | vachacz 2026-09-07, 2026-10-05 | |
| 10 | Avis des amis | connaissance § Transferts / finances / académie, § Finances / transferts / personnel | — | connaissance | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
| 2026-10-31 | Prix des 16 ans | 3,5-4 M (avis) → un bon 16 ans = 3 à 4 M fin octobre, 7,5 M cité sans nom le 31/10 | dixi2499, montabelas, nathanr_32176 (avis) ; à comparer à `gold.bv_market_price_known` |
| 2026-10-31 | 2 étoiles | — → bon marché depuis que le test à 25 000 est ouvert à tous | #italia 2026-10 (avis) |
| 2026-10-31 | Taxe | 5 % → 5 % confirmé par un virement réel (1 010,0 k → 959,5 k) | heldermoreno 2026-10-03 |
| 2026-10-31 | Jeune « High » vendu | cible 3 étoiles à 3,5-4 M (avis) → potentiel moyen tant que 4-5 semaines d'entraînement ne l'ont pas prouvé | Dev 2026-08-13 cité par carlomtlopes 2026-10-07 (seconde main) |
