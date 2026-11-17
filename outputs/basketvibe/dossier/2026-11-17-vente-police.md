# Police vente — Maël Bernard — 2026-11-17 (heure de Paris 09:50)

Verdict : COMPLÉTÉ PAR LA POLICE (corrige le brouillon).

## Conclusion
1. **Ne pas vendre aujourd'hui** (décision : garder Bernard).
2. Prix de mise en vente si l'utilisateur vend quand même : minimum 525 000 (p25 de la case ≤21 / PS 45, n = 47) ; 795 000 est la médiane, pas un plancher. Net vendeur après taxe 5 % : 755 250 à 795 000.
3. Le brouillon nomme un mauvais remplaçant : Albano est PF, 6e au slot C (47,7). Bernard est 5e au slot C (48,1) derrière Lefebvre 62,8, Gimenez 53,1, Fournier 52,4, Legrand 49,4. Écart Bernard-Albano 0,4 : exact. Mais les vrais remplaçants sont Legrand (écart 1,3) ; vendre Bernard ne coûte presque rien en force.
4. Pourquoi ne pas vendre quand même : (a) il progresse (+0,5 PS en 7 jours, TSP 406 → 423, trend « progression ») ; la seule saison lue = 1 match (24 min, éval 27,0, la meilleure du club) ; 6,0 min sur 4 matchs de ligue = rotation, pas un rebut ; (b) 17 303 de salaire par semaine, soit 358 par PS, comparable à Albano (369) : économie faible face à une valeur de revente ≥ 525 000 qui monte avec l'âge-PS ; (c) la bande PS 50 ≤21 vaut 3,13 M (médiane) : à +0,5 par semaine, 48,3 → 50 en ~3-4 semaines, la valeur de revente pourrait quadrupler ; (d) le C du 18-21 ans par poste (`bv_market_price_ref`) a une médiane de 220 000 (n = 11, p25 3 861) : l'estimation 795 000 repose sur la bande PS tous postes, donc moins sûre pour un C ; (e) la leçon L-028 dit que la médiane sous-estime plutôt le prix final, ce qui joue pour attendre.
5. Ce qui prouverait que j'ai tort : Bernard stagne (gain 7 jours ≤ 0 deux semaines de suite) ou la bande PS 45 ≤21 chute sous 525 000 (p25) au prochain relevé ; ou un besoin de trésorerie à ≥ 755 000 net.

## Variables (variables.md § vente)
| variable | valeur | source |
|---|---|---|
| Joueur, âge | Maël Bernard, C, 18 ans, PS 48,3 | `gold.bv_sell_candidates` |
| Minutes, rôle | 6,0 min sur 4 matchs de ligue ; saison : 1 match, 24 min, éval 27,0 (Fournier 34 min, éval 14,5 sur 6) | `bv_sell_candidates`, `bv_player_outlook` |
| Remplaçant interne, écart | ➕ rang 5 au slot C ; Legrand 49,4 (écart 1,3) ; Albano est PF 6e (47,7) : écart 0,4 | `gold.bv_slot_fit` slot C |
| Valeur marché | ≤21 / PS 45 : p25 525 000, médiane 795 000, p75 1 568 897 (n = 47, dernière vente 13/11) ; ➕ C 18-21 : p25 3 861, médiane 220 000, n = 11 | `gold.bv_price_ref_ps`, `gold.bv_market_price_ref` |
| Salaire économisé | 17 303 par semaine | `gold.roster_bilan` |
| Taxe, délai, effectif | 5 % ; enchère ~2 jours ; 8 disponibles minimum, 12 aujourd'hui, 11 après vente ; aucune vente en cours | skill transferts § Vendre [M§11.1] ; C2, C3 |
| Déclin / progression | progression, +0,5 en 7 jours, TSP 406 → 423 ; pas de déclin (C5 vide) ; potentiel : nulle (pas de gain) | C5, C8, `bv_player_outlook` |
| Avis des amis | kb vente : 5 total / 5 affichées ; rien ne contredit ; taxe 5 % (#2716, #118) et effectif minimum 8 (#47, 0,45) confirment la règle ; aucun avis sur la valeur de Bernard | `kb.py basketvibe vente`, thème transferts du dossier |

## Couverture
| Source | trouvés | lus | retenus | écartés (pourquoi) |
|---|---|---|---|---|
| kb vente | 5 | 5 | #2716, #47 | #121, #87, #100 (sans effet sur cette vente) |
| kb transferts (dossier) | 31 (29 affichées, 2 obsolètes) | 29 | #118, #95, #2716, #144 (prix des jeunes élevés) | #127 (contredit, hors sujet), les autres sans rapport |
| Skill transferts § Vendre | 1 | 1 | taxe, délai, effectif min | — |
| Vues gold (candidats, outlook, slot_fit, prix) | 5 | 5 | toutes | — |
| Learnings / C-016 | 2 | 2 | C-016 « garder les jeunes (Bernard…) » ; L-028 | C-068 : déjà lu comme positif |
| Discord/chat bruts | 0 export | 0 | — | police partielle : manque la lecture de `bronze.discord_messages` (plafond d'appels) |

Police partielle : manque `bronze.discord_messages` sur Bernard, et la carte `docs/decisions/cartes/basketvibe/vente.md` n'est pas réécrite (« Sources lues » illisible) ; à noter, non commité.

## Récidive
Brouillon incomplet : remplaçant nommé hors poste (PF pour un C) ; ligne proposée pour `docs/regles/actives.md` : « Remplaçant interne = lire `gold.bv_slot_fit` au slot du joueur, pas le poste d'une autre ligne. »
