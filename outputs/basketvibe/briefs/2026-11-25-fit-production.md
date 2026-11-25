# BasketVibe : le fit au poste prédit-il la production ? (25/11/2026)

Aucun accord n'est proposé sur Miletić (consigne de l'utilisateur).

Sources :
- `silver.bv_match_player_stats` : ligne `period = 0`, nos joueurs, `silver.bv_matches.competition = 'league'`, 32 matchs du 07/09 au 23/11 ;
- `gold.bv_slot_fit` : ajustement au poste naturel du joueur (`gold.bv_roster_now.position`).

## Nos 12 joueurs, saison de ligue

| Joueur | Poste | Fit au poste | Matchs joués | Minutes | Points | Points / 36 min | Éval | Éval / min | +/- | +/- / 36 min |
|---|---|---|---|---|---|---|---|---|---|---|
| Thibault Bonnet | SG | 52,1 | 31 | 1 123 | 706 | 22,6 | 495 | 0,441 | −157 | −5,0 |
| Naël Boyer | PG | 48,7 | 31 | 1 024 | 353 | 12,4 | 228 | 0,223 | −151 | −5,3 |
| Armand Fournier | C | 52,7 | 26 | 882 | 359 | 14,6 | 556 | 0,630 | +110 | +4,5 |
| Maël Bernard | C | 48,8 | 20 | 758 | 224 | 10,6 | 366 | 0,483 | −124 | −5,9 |
| Jonathan Durand | SF | 43,9 | 21 | 679 | 294 | 15,6 | 214 | 0,315 | −193 | −10,2 |
| Hadrien Gimenez | SF | 60,3 | 19 | 582 | 199 | 12,3 | 225 | 0,387 | +103 | +6,4 |
| Léo Lefebvre | PF | 63,2 | 17 | 502 | 306 | 21,9 | 438 | 0,873 | +79 | +5,7 |
| Oscar Richard | PG | 56,8 | 19 | 490 | 97 | 7,1 | 137 | 0,280 | +47 | +3,5 |
| Noé Legrand | PF | 49,9 | 22 | 470 | 258 | 19,8 | 240 | 0,511 | +39 | +3,0 |
| Nolan Baron | PG | 45,2 | 4 | 156 | 63 | 14,5 | 47 | 0,301 | −103 | −23,8 |
| Anselmo Albano | PF | 48,0 | 3 | 48 | 19 | 14,2 | 12 | 0,250 | +25 | +18,8 |
| Sacha Leclerc | SG | 43,0 | 2 | 24 | 10 | 15,0 | 9 | 0,375 | +6 | +9,0 |

## Le fit prédit-il la production ?
Corrélation de Pearson, IC95 par la transformation de Fisher :

| Production | n = 10 (≥ 100 min) | n = 12 (tous) |
|---|---|---|
| Éval / min | r = 0,56 (IC95 −0,11 à 0,88) | r = 0,57 (IC95 −0,01 à 0,86) |
| Points / min | r = 0,10 (IC95 −0,56 à 0,69) | r = 0,10 (IC95 −0,50 à 0,64) |
| +/- / 36 min | r = 0,78 (IC95 0,29 à 0,95) | r = 0,34 (IC95 −0,30 à 0,76) |

**Verdict : le fit ne prédit pas la production de façon prouvée.**
- Éval / min et points / min : l'intervalle contient 0.
- +/- : le lien n'apparaît qu'à 100 minutes et plus. Or le +/- dépend des coéquipiers sur le terrain.

La règle « gain du cinq » (fit seul) n'est donc **pas fiable pour un achat à 750 000**. Un achat devra aussi montrer un gain de production : éval / min mesurée, ou statistiques réelles du joueur.

**Écart de Bonnet** : il est notre meilleur marqueur (22,6 points par 36 min, le plus de minutes) mais son fit de SG est le plus bas du cinq (52,1). Le fit pondère les compétences du poste. Le volume de tirs et de points de Bonnet n'y entre pas. Son éval / min (0,441) est dans la moyenne et son +/- est négatif.

## Police de Miletić refaite (motif « entre dans le cinq », +7,2)
Verdict complet : [outputs/basketvibe/police-2026-11-25-c.md](https://github.com/RoJo69100/assistant-jeux/blob/main/outputs/basketvibe/police-2026-11-25-c.md). Verdict : **police partielle, ne pas enchérir sur ce motif**.

Pourquoi :
- +7,2 est un écart de fit, pas de production (corrélation ci-dessus) ;
- 750 000 est sous le p25 de 840 000 : l'enchère est perdue presque sûrement (2 ventes sur 19 à 750 000 ou moins) ;
- le plafond de revente vaut 676 480. Un achat au-dessus de ce plafond ne serait justifié ni par la revente ni par le cinq.

## Ce qui manque en base pour Miletić
Potentiel, forme, blessure, contrat et statistiques réelles de match : `gold.bv_market_candidates` n'a aucune de ces colonnes.

Page à exporter : la page joueur de Miletić (`basketvibe.com/player/<id>`, type `player` en base ; 160 déjà captées) ouverte depuis son annonce du Marché, puis son onglet Carrière (type `player_career`) pour les statistiques réelles.

Test de potentiel (25 000) seulement si tu veux l'achat.
