# Police vente — Nolan Baron — 2026-11-19 11:40 (Paris)

Verdict : police partielle : manque (1) prix d'achat/origine de Baron (académie ou achat : délai 7 jours non vérifié, `silver.bv_transfers` non interrogé), (2) liste des ventes comparables par PS exact (colonne de `gold.bv_transfer_history` non trouvée), (3) lecture de `bronze.raw_pages`. Plafond de 12 appels atteint.

Décision : vendre Baron, prix minimum 290 000 (= départ), annonce d'environ 2 jours (non annulable), sur accord écrit.

## Corrections au brouillon
- Le remplaçant interne n'est pas Jonathan Durand (SF 25 ans, 43,7, rang 2 SF). Baron est PG : Richard 56,6 (rang 1), Boyer 48,5 (rang 2). Écart avec Boyer = 3,6 (pas 0,6). Source : `gold.roster_bilan`.
- Minutes : `gold.bv_player_outlook` = 0 match, 0,0 min sur la saison (pas seulement 4 matchs). `gold.bv_sell_candidates` : rang 7 à son meilleur emplacement (PG).

## Variables
| variable | valeur | source |
|---|---|---|
| Joueur, âge | Nolan Baron, PG, 17 ans, PS 44,9 | `gold.roster_bilan` |
| Minutes saison, rôle V/D | 0 match, 0,0 min, aucun rôle | `gold.bv_player_outlook` |
| Remplaçant interne, écart | Boyer 48,5 (+3,6) ; Richard 56,6 (+11,7) | `gold.roster_bilan` |
| Valeur marché | case PS 40, ≤21 ans : n=86, p25 90 000, médiane 299 999,5, p75 801 250 (dernière vente 17/11) | `gold.bv_price_ref_ps` |
| Comparables PG 16-18 ans, 30 derniers jours | 17 ans : n=36, p25 287 500, médiane 925 250 ; 16 ans : n=11, p25 238 000, médiane 500 000 | `core.market_listing` (dernier prix vu, pas prix final) |
| Salaire économisé | 16 691/sem. (372 par PS, rang 7 à l'emplacement) | `gold.bv_sell_candidates` |
| Taxe, délai, effectif min | 5 % (reçu 95 %), enchère ~2 jours non annulable ; effectif 12 pour un minimum de 8 (11 après vente, 9 requis avant) ; 0 vente en cours | skill transferts `01-vendre.md` ; carte vente C2/C3 ; `core.market_listing` |
| Progression | +0,4 en 7 jours (44,5 → 44,9), TSP 383 → 399, tendance « progression », potentiel estimé 8 ; pas de déclin | `core.player_daily`, `gold.bv_player_outlook` |
| Revente nette | médiane de marge 13 750 (n=16, ≤21 ans, bande 40) : achat-revente peu rentable | `gold.bv_resale_stats` |
| Avis des amis | kb vente : 5 total / 5 affichées. #47 (0,45) effectif min 8 retenu ; #2716 taxe 5 %, retenu ; #121 écarté (20-21 ans) ; #87, #100 écartés (visibilité du potentiel, force). Thème transferts : 31 total / 29 affichées (2 obsolètes) : #144 (doute 0,4) « 17 ans à 2-3 M facile » en fin octobre, écarté (doute, prix de pic) ; #2720 (0,4) juniors 16 ans se vendent bien, retenu comme appui faible | `pipelines/kb.py` |
| Conseil passé | C-016 (18/10) « garder Bernard, Baron, Leclerc » ; C-075 (26/10) pas d'achat de 16-17 ans à revendre. Contredit par 0 minute sur toute la saison, salaire 16 691/sem. ; le conseil date d'avant le +1 an et ne portait pas sur le prix | `outputs/basketvibe/learnings.md` via dossier |
| Exports périmés | Équipe 37 h, Mes enchères 145 h (ventes en cours non vérifiables par export, mais `core.market_listing` n'en montre aucune) | carte C7 |
| Ce qui prouvera l'erreur | Baron invendu après 2 jours (reste au club, pas de perte) ; ou prix final < 90 000 (p25 de la case) ; ou Boyer/Richard blessés et PG manquant sous 4 jours | dérivé |

## Prix
- Départ et minimum : 290 000 (≈ p25 des 17 ans PG, 287 500 ; médiane de la case 300 000). Net vendeur 275 500.
- Ne pas descendre sous 90 000 (p25 de la case) ; en dessous, garder Baron.
- Conflit : médiane de la case (300 000, tous postes) contre PG 17 ans récents (médiane 925 000, mais dernier prix vu et pic) : les chiffres de notre marché récent battent l'avis #144 ; on prend le bas de fourchette comme minimum.

## Couverture
| Source | trouvés | lus | retenus | écartés (pourquoi) |
|---|---|---|---|---|
| Dossier vente.md | 1 | 1 | carte C1-C8, kb | learnings anciens non liés |
| Discord brut | 0 | 0 | — | export vide |
| kb vente | 5 | 5 | #47, #2716 | #121, #87, #100 hors sujet |
| kb transferts | 31 | 29 affichées | #2720 | 2 obsolètes ; #144 doute |
| Skill vendre | 1 | 1 | taxe, délai, minimum | — |
| Vues gold | 6 | 6 | roster_bilan, sell_candidates, player_outlook, price_ref_ps, resale_stats, market_listing | — |

## Correction du prix — 11:40 (session principale)
Ventes réelles (`gold.bv_transfer_history`, hors joueurs libres) : PG 17 ans, PS 42–48, 21/10–13/11 : n=7, p25 1 449 926, médiane 1 575 000, p75 2 670 302. PG 16–18 ans, même PS : 12 ventes, dont 5 entre 910 000 et 1 562 794 depuis le 10/11. La case `bv_price_ref_ps` (PS 40, ≤ 21 ans, médiane 300 000) mélange les postes : prix minimum corrigé de 290 000 à 950 000. Achat de Baron absent de l'historique (`bought_by_me`) : délai de 7 jours à vérifier en jeu.

## Récidive
Brouillon : remplaçant nommé hors poste (Durand SF pour un PG) et minutes sur 4 matchs au lieu de la saison. Ligne pour `docs/regles/actives.md` : « Vente : le remplaçant interne se lit au même poste (`gold.roster_bilan`, même `position`) ; minutes sur la saison (`gold.bv_player_outlook.games`). »
