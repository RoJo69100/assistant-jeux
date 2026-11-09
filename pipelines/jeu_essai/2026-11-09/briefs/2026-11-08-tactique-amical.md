# Tactique AMICAL lun. 09/11 08:00 (verrou 07:45), DOMICILE contre Garden City, à saisir AUJOURD'HUI 08/11

Pas de preset d'amical, pas de Preview (arbitrage 15). Plan D-1099 repris du 04/11 et du 06/11. Amical : fatigue et expérience ≈ 1/10, pas de blessure [M§1.2]. Moteur v4.

## Action : fais X
**Sur la page du match d'amical contre Garden City, remplace tout ce que l'écran affiche par la fiche ci-dessous, puis sauvegarde le plan et exporte la page avant 07:45.** À l'écran (export 08/11 11:12) le plan préchargé met encore Gimenez 48 min, Baron 36, Bonnet / Lefebvre / Fournier en jeu, Dang, Albano et Ungureanu à agressivité 3 : tout est à corriger (`gold.bv_saisie_joueurs`, sauvegarde_match faux).

## Test unique
**Zone Perimeter (1) pour les 12 adversaires, focus 3.** Perimeter lisible : 30/10 +27, opp 2P 45,5 % ; 01/11 +9, 53,4 % ; 05/11 −14, 55,2 % (`gold.bv_match_report`, L-027). Le 08/11 (New York City, L 94-96, opp 2P 55,6 %) : zone non lisible, donc non compté. Middle en amical : 63,8 à 66,0 % (L-027). **Faux si** `opp_fg2_pct` > 55,2 % ; confirmé seulement si ≤ 53,4 % et marge ≥ +5. Illisible si la page n'est pas exportée sauvegardée (`gold.bv_zone_jouee`).
Limite : les amicaux avec ce banc donnent 55 à 66 % de 2P adverse quelle que soit la zone (fit 43-52 contre 53-66 en ligue) ; le test mesure surtout la zone si le banc reste constant : c'est le cas (même neuf joueurs que les 05/11 et 06/11).

## 1. Composition (écran 1)
| | PG | SG | SF | PF | C |
|---|---|---|---|---|---|
| Q1 | Baron | Leclerc | Durand | Albano | Bernard |
| Q2 | Boyer | Leclerc | Durand | Legrand | Bernard |
| Q3 | Baron | Leclerc | Durand | Albano | Ungureanu |
| Q4 | Boyer | Dang | Durand | Legrand | Ungureanu |
| Prol. | Boyer | Dang | Durand | Legrand | Ungureanu |

Aucun remplaçant programmé. Richard, Bonnet, Gimenez, Lefebvre, Fournier : 0 minute (ligue à 19:45, fatigue 9,8 à 11,2 au 08/11). Durand seul SF sur 48 min : contrainte (Gimenez est en ligue) ; il dépasse 36 min (−20 % au-delà [M§5.7]) mais c'est constant depuis le 05/11, donc sans effet sur la comparaison de zone.

## 2. Consignes (écran 2, 1-5, ordre de l'export)
| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Min | Off. focus | Rôle | Tir | Agress. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baron | PG | PG | — | PG | — | — | 24 | 2 | 1 | 3 | 1 |
| Boyer | PG | — | PG | — | PG | PG | 24 (+5) | 2 | 2 | 3 | 1 |
| Richard | PG | — | — | — | — | — | 0 | 1 | 1 | 3 | 1 |
| Bonnet | SG | — | — | — | — | — | 0 | 5 | 5 | 5 | 1 |
| Dang | SG | — | — | — | SG | SG | 12 (+5) | 3 | 3 | 3 | 1 |
| Leclerc | SG | SG | SG | SG | — | — | 36 | 4 | 4 | 3 | 1 |
| Durand | SF | SF | SF | SF | SF | SF | 48 (+5) | 3 | 3 | 3 | 1 |
| Gimenez | SF | — | — | — | — | — | 0 | 4 | 3 | 3 | 1 |
| Albano | PF | PF | — | PF | — | — | 24 | 3 | 3 | 3 | 1 |
| Lefebvre | PF | — | — | — | — | — | 0 | 4 | 4 | 1 | 1 |
| Legrand | PF | — | PF | — | PF | PF | 24 (+5) | 3 | 3 | 1 | 1 |
| Bernard | C | C | C | — | — | — | 24 | 2 | 2 | 1 | 1 |
| Fournier | C | — | — | — | — | — | 0 | 2 | 2 | 1 | 1 |
| Ungureanu | C | — | — | C | C | C | 24 (+5) | 3 | 3 | 3 | 1 |

Minutes : 24+24+0+0+12+36+48+0+24+0+24+24+0+24 = 240.
Raisons des valeurs qui diffèrent de la ligue ou d'une règle :
- Agressivité 1 pour les 14 : règle uniforme L-004. Dang, Albano, Ungureanu étaient à 3 sur le plan préchargé, sans raison lue : corrigés.
- Leclerc Tir 3 (et non 5, valeur préchargée) : 2 sur 29 à 3 pts sur deux amicaux (L-020, L-025, C-110).
- Albano Tir 3 : valeur du plan du 04/11 ; je n'ai pas lu ses compétences de tir pour la justifier autrement (en ligue il est à Tir 1) ; sans objet pour le test de zone.
- Les cinq de ligue : valeurs du plan de ligue, ils ne jouent pas.

## 3. Adversaires (écran 3) : Garden City, 12 joueurs connus de l'écran, aucune statistique
Source : `gold.bv_saisie_adversaires` (export 08/11 11:12). Aucun match passé ni Preview : focus neutre, aucun Give up, aucun Light.
| Adversaire | Poste | Focus (1-5) | Zone |
|---|---|---|---|
| Caune | PG | 3 Normal | Perimeter (1) |
| Colin | PG | 3 Normal | Perimeter (1) |
| Roze | PG | 3 Normal | Perimeter (1) |
| Siliņš | SG | 3 Normal | Perimeter (1) |
| Vītols | SG | 3 Normal | Perimeter (1) |
| Franzoni | SF | 3 Normal | Perimeter (1) |
| Ozoliņķis | SF | 3 Normal | Perimeter (1) |
| Trajković | SF | 3 Normal | Perimeter (1) |
| Bērziņš | PF | 3 Normal | Perimeter (1) |
| Kalniņš | PF | 3 Normal | Perimeter (1) |
| Cunanan | C | 3 Normal | Perimeter (1) |
| Jansons | C | 3 Normal | Perimeter (1) |

### Focus défensif
Garden City : noms connus, parts de tirs et 2P/3P inconnus (jamais affronté, `gold.bv_match_opp_focus` vide). Donc Normal sur tous, zone Perimeter pour tous (le test). Pas d'export à faire : adversaire sans importance en amical.

## 4. Blessés et plan B
Aucun blessé ni joueur en vente (`gold.bv_roster_now`, 08/11) ; pas de blessure en amical [M§1.2]. Si un des neuf manque : Gimenez ne remplace personne (ligue) ; Leclerc peut tenir SG, Dang prendre Q3.

## 5. Contrôle SQL (values + gold.bv_slot_fit, 08/11)
- 5 joueurs différents par quart, un par emplacement : OK (Q1-Q4).
- Plus de 3 quarts : **Durand 4 quarts (48 min)** : écart assumé et justifié ci-dessus ; tous les autres ≤ 3.
- `height_eff` ≥ 95 : OK (100 partout).
- `fit_with_form` : Durand SF 43,2 ; Leclerc SG 42,7 ; Baron PG 44,9 ; Bernard C 49,7 ; Albano PF 48,3 ; Boyer 51,6 ; Legrand PF 51,4 ; Dang 51,9 ; Ungureanu 49,0. Faibles par construction (amical de test).
- Fatigue des neuf : 0,42 à 4,14 (≤ 20). Aucun blessé ni vendu.
- Forme : relevé du 08/11 (dimanche), à jour.

## 6. Preuve que j'avais tort et lecture
Voir « Test unique ». Conseil : **C-116** dans `outputs/basketvibe/learnings.md`. Doute : un amical sans fiche adverse et avec le banc en jeu mesure autant le banc que la zone ; si `opp_fg2_pct` > 55,2 % la zone Perimeter n'apporte rien et on retourne à Middle ligue-style.
