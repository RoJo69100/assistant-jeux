---
name: basketvibe-joueurs
description: Règles BasketVibe sur les joueurs — 8 compétences et ce qu'elles font, PS/TS par poste, taille et poids, forme, fatigue (formules et tables), expérience, minutes lourdes, blessures, vieillissement et retraite. À charger pour évaluer un joueur, expliquer une performance, gérer la rotation, la fatigue ou les blessures.
---

# BasketVibe — joueurs : compétences, condition, blessures

Sources : **[M§x]** = manuel officiel https://www.basketvibe.com/guide (lu le 2026-10-16). **[Obs]** = constaté dans nos données. Pas de règle inventée : si ce n'est pas ici, dire « je ne sais pas ».

## Les 8 compétences entraînables (1–99) [M§5.1, §5.3, §5.8]
| Compétence | Rôle en match |
|---|---|
| Deux points | Trois zones : **au cercle** (+ taille, athlétisme, poids dans la norme), **mi-distance** (toucher seul, pas de physique), lancers francs (2/3 du mélange) [M§5.1.2] |
| Trois points | Réussite derrière l'arc + 1/3 des lancers francs. La taille n'aide qu'en cas d'avantage sur le défenseur, effet le plus faible sur les tirs à 3 [M§5.1.3] |
| Passe | Qualité du dernier passeur : % de tirs assistés et bonus au tireur ; réduit les pertes sur passe [M§5.1.4] |
| Dribble (ball handling) | Moins de pertes en dribble ; plus de chances d'être celui qui attaque la raquette [M§5.1.5] |
| Défense | Défense extérieure (rapidité latérale) et intérieure (taille, force) ; interceptions et contres [M§5.1.6] |
| Rebond | Base, puis multipliée par la position sur le terrain et la taille [M§5.1.1] |
| Athlétisme | Ne mène presque jamais un jet seul ; booste finition au cercle, défense latérale, protection du ballon, interceptions, contres, rebonds [M§5.3.1, §7.1] |
| Endurance (stamina) | **Aucun effet pendant une possession.** Réduit la fatigue accumulée après le match et le risque de blessure quand le joueur est fatigué [M§5.3.2] |

Effet de la passe (dernier passeur) [M§5.1.4] :
| Passe | Tir assisté | Bonus si assisté | Si non assisté |
|---|---|---|---|
| 50 | ~49 % | +1 pt | −2 pts |
| 70 | ~62 % | +6 pts | 0 |
| 80 | ~69 % | +10 pts | +1 pt |
| 90 | ~75 % | +14 pts | +2 pts |

Rebond, portée selon la position sur le terrain : C 100 %, PF ~89 %, SF ~78 %, SG ~66 %, PG ~55 %. Selon la taille (200 cm = 100 %) : ~±1,8 % par cm ; 180 cm ~64 %, 190 ~82 %, 210 ~118 %, 220 ~136 %, plancher 62 %, plafond 142 %. Les deux effets se cumulent [M§5.1.1].
- En ligue et en coupe, la lutte au rebond d'équipe fait la moyenne des 5 joueurs sur le terrain. La position et la taille décident surtout **qui** est crédité. En amical, la distance du tir compte aussi [M§5.1.1].

## PS / TS [M§2.2]
Seules les 8 compétences comptent (ni forme, ni fatigue, ni taille, ni potentiel). Poids de chaque compétence par poste (le premier libellé du poste sur la carte du joueur) :

| Compétence | PG | SG | SF | PF | C |
|---|---|---|---|---|---|
| Deux points | 15 | 15 | 15 | 15 | 15 |
| Trois points | 15 | 15 | 15 | 10 | 10 |
| Passe | 15 | 10 | 10 | 10 | 10 |
| Dribble | 15 | 15 | 10 | 10 | 10 |
| Défense | 15 | 15 | 15 | 15 | 15 |
| Rebond | 5 | 5 | 10 | 15 | 15 |
| Athlétisme | 10 | 15 | 15 | 15 | 15 |
| Endurance | 10 | 10 | 10 | 10 | 10 |

- Le PS utilise les valeurs précises : il peut différer d'un point du calcul fait sur les chiffres arrondis [M§2.2].
- TS = moyenne du PS des 8 meilleurs du roster (blessés compris) [M§2.2].
- PS visible chez les autres clubs seulement quand le joueur est en vente [M§2.2]. Les compétences adverses apparaissent en tranches (0–20, 21–40, 41–60, 61–80, 81–99) [M§4].
- [Obs] Nos données d'entraînement (`silver.bv_player_daily.*_exact`) donnent les valeurs précises. La valeur affichée = partie entière, vérifié sur 15 joueurs le 2026-10-16.

## Potentiel révélé [News 2026-10-20]
- Le potentiel d'un de ses propres joueurs peut être révélé depuis son profil et reste ensuite visible pour nous. Il ne compte toujours pas dans PS/TS [M§2.2].
- À vérifier : le coût et d'éventuelles limites (la News ne les donne pas) ; si l'export Tampermonkey capte la valeur révélée. `gold.bv_potential_estimate` et `bv_sell_candidates.potential_est` sont des estimations : une valeur révélée les remplace.

## Taille et poids [M§5.2, §6.2.1]
Taille adulte par poste : PG 180–200, SG 186–203, SF 192–209, PF 196–212, C 205–222 cm.
- Le **libellé de poste ne compte pas** en match. Ce qui compte : l'emplacement sur le terrain (PG–C) dans le cinq du quart-temps, et l'adéquation de la taille à cet emplacement [M§6.2].
- Efficacité offensive selon la taille et l'emplacement (100 = pleine), extrait [M§6.2.1] :

| cm | PG | SG | SF | PF | C |
|---|---|---|---|---|---|
| 175 | 96 | 82 | 69 | 60 | 55 |
| 180 | 100 | 93 | 80 | 71 | 55 |
| 185 | 100 | 98 | 91 | 82 | 63 |
| 190 | 100 | 100 | 98 | 93 | 74 |
| 195 | 100 | 100 | 100 | 98 | 85 |
| 200 | 100 | 100 | 100 | 100 | 96 |
| 205 | 95 | 98 | 100 | 100 | 100 |
| 210 | 83 | 90 | 98 | 100 | 100 |
| 215 | 71 | 78 | 93 | 98 | 100 |

  Sous 100 : moins de ballons, pas d'avantage de taille au contest, conversion plus difficile [M§6.2.1].
- Poids : hors de la plage saine pour sa taille, le joueur est pénalisé. Trop lourd : défense extérieure, protection du ballon et interceptions. Trop léger : contact, défense au poste et rebond [M§5.2].
- Jeunes : ils grandissent jusqu'à 22 ans (+0 à +4 cm par saison, vers une taille cible cachée), +0,9 kg par cm [M§5.2].
- Changement de libellé de poste possible à partir de 22 ans, purement cosmétique [M§4]. Depuis le 14/10, il se fait sur la fiche du joueur, dans la plage permise par sa taille [News 2026-10-14].

## Forme (1–10) [M§5.5]
- Mise à jour chaque dimanche : en général ±1 ou stable, avec un retour vers le milieu. Remise à 6 en début de saison. Les psychologues font légèrement pencher vers la hausse.
- Effet sur la compétence utilisée (multiplicateur) :

| Forme | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Attaque | −11 % | −8 % | −5 % | −4 % | −1 % | +1 % | +4 % | +7 % | +11 % | +15 % |
| Défense | −10 % | −7 % | −5 % | −3 % | −1 % | +1 % | +3 % | +5 % | +7 % | +10 % |

  Le rebond utilise la moyenne attaque/défense.
- Conseil du manuel : aligner les bons tireurs à 7 ou plus, garder les joueurs à 5–6 pour les quart-temps défensifs, reposer ceux à 4 ou moins, surtout s'ils sont fatigués [M§5.5].

## Fatigue (0–100) [M§5.6]
- **Gain après un match** = minutes × 0,19 × multiplicateur d'agressivité défensive × (1,5 − 0,008 × Endurance).
- **Récupération chaque nuit** = 0,5 + 10 % de la fatigue actuelle (identique pour tous ; l'endurance n'aide pas).
- Amical ≈ 1/10. Coupe : 0 par défaut. Remise à 0 en début de saison.
- La pénalité est fixée par la fatigue au coup d'envoi et reste la même tout le match (s'asseoir un quart-temps ne la réduit pas) :

| Fatigue | 0 | 20 | 40 | 60 | 100 |
|---|---|---|---|---|---|
| Attaque | 0 % | −3 % | −10 % | −20 % | −40 % |
| Défense | 0 % | −2 % | −6 % | −13 % | −26 % |

  Variation linéaire entre ces points. Zones : vert 0–20, jaune 20–40, orange 40–60, rouge 60–100 [M§5.6.1].
- ⚠️ **Moteur v4 (amicaux depuis le 17/10, ligue en saison 2)** : une seule échelle, plus dure, pour l'attaque et la défense : 20 → −4 % ; 40 → −15 % ; 60 → −30 % ; 80 → −50 % [News 2026-10-17]. Détail dans basketvibe-communaute. *Avis (pas une règle)* : en saison 2, viser une fatigue au coup d'envoi en zone verte (≤ 20) pour les titulaires.
- Multiplicateur d'agressivité défensive : soft ×0,75 · ×0,875 · équilibré ×1,00 · ×1,325 · agressif ×1,65 [M§6.3].
- Fatigue stabilisée avant un match du samedi (même usage chaque semaine), extrait [M§5.6.4] :
  - défense équilibrée, endurance 50 : 24 min → 12 ; 36 min → 21 ; 48 min → 30 ;
  - défense agressive, endurance 50 : 36 min → 38 ; 48 min → 52 (orange).

## Expérience (0–99) [M§5.4]
- Jusqu'à environ **+10 %** d'efficacité en match au sommet de l'échelle. Elle ne baisse jamais.
- Elle augmente avec les minutes en match (ligue ; amical à 1/10 ; coupe seulement si l'édition l'autorise). Plus vite jusqu'à 21 ans. Petit gain pour un jeune convoqué sans jouer. Bonus pour le MVP du match.

## Minutes lourdes [M§5.7]
- À partir de 36 minutes jouées dans le match : **−20 % fixe** sur toutes les actions jusqu'à la fin du match, prolongation comprise. Le compteur est cumulé sur le match.
- Un joueur qui joue les 4 quart-temps atteint ~36 min au début du 4e QT.

## Pile d'effets en match [M§7.2]
Valeur de la carte → forme → fatigue → expérience → minutes lourdes → tactique (agressivité, focus, choix de tirs) → taille et poids au duel → avantage du terrain. Chaque couche multiplie puis arrondit (minimum 1).

## Blessures [M§9.3, §4.3]
- **Ligue uniquement** selon le manuel, pas en coupe par défaut [M§9.3]. ⚠️ Mais depuis le moteur v4, les amicaux ont des blessures : la News règle leurs probabilités [News 2026-10-19]. Un amical v4 n'est donc plus sans risque ; le manuel n'est pas encore à jour (on garde le manuel, on signale).
- [v4, amicaux] Défense soft : risque ×0,60 (avant ×0,85) ; medium soft ×0,80 (avant ×0,95). Au-delà de 36 min, +40 % de risque au dernier quart-temps (contre la stratégie 5×48). 48 min en soft reste à peu près au même niveau ; 5×48 en équilibré ou agressif donne beaucoup plus de blessures [News 2026-10-19]. La table ci-dessous reste celle du manuel (ligue v3).
- Risque pendant le match, augmenté par : minutes jouées, fatigue avant le match, endurance basse, agressivité défensive (soft ×0,85, équilibrée ×1,00, ×1,50, agressive ×2,00). Réduit par les kinés (−12,5 % chacun).
- Référence (endurance 70, fatigue 0, sans kiné), risque de blessure sur le match :

| Minutes | Soft | Équilibré | Agressif |
|---|---|---|---|
| 12 | 0,6 % | 0,5 % | 1,1 % |
| 24 | 1,3 % | 1,6 % | 3,1 % |
| 36 | 1,9 % | 2,6 % | 5,4 % |
| 48 | 3,5 % | 4,2 % | 7,4 % |

- Indisponibilité : 3 à 12 jours avant l'effet des médecins (−25 % par médecin). Une nouvelle blessure pendant la convalescence s'ajoute. Un joueur blessé **ne s'entraîne pas** cette semaine-là [M§8].

## Âge
- La progression ralentit avec l'âge ; **0 gain à partir de 30 ans** ; déclin chaque dimanche à partir de 31 ans ; retraite à la fin de la saison des 38 ans [M§8.2, §8.5, §4]. Détail dans basketvibe-entrainement.

## [Veille 2026-10-29] Blessures (V-20261029-5)
- Chaque blessure a des **points de blessure** décomptés chaque jour ; les médecins en retirent davantage, donc la durée est fractionnaire. L'âge n'est pas un facteur de blessure (le développeur envisage de l'ajouter). [Dev 2026-08-31 15:43, general ; 2026-08-10 16:22, help]
