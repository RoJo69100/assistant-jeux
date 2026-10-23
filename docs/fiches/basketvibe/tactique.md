# BasketVibe — fiche Tactique

Lue par l'agent `tactique` après `commun.md`. Contenu repris de l'agent BasketVibe validé (checklist BasketVibe, partie E).

## Skills à lire
- `.claude/skills/basketvibe-tactique/SKILL.md`
- `.claude/skills/basketvibe-joueurs/SKILL.md`
- `.claude/skills/basketvibe-communaute/SKILL.md` (moteur v4, News de l'admin)
- puis `outputs/basketvibe/learnings.md` (enseignements L-nnn et conseils C-nnn)

## Règles propres au jeu
1. **Contrôle ta tactique en SQL avant de la rendre** : écris le plan dans une requête (`values (...)`) et vérifie avec une requête :
   - 5 joueurs différents par quart-temps, chacun sur un emplacement PG, SG, SF, PF, C ;
   - **aucun joueur au-delà de 3 quarts-temps** (36 min, puis −20 % [M§5.7]) ;
   - pour chaque joueur et emplacement, `height_eff` ≥ 95 dans `gold.bv_slot_fit` (sinon justifie-le) ;
   - fatigue stabilisée de chaque joueur selon ses minutes et son agressivité (`gold.bv_fatigue_plan`) : vise la zone verte (≤ 20) pour les titulaires ;
   - aucun joueur blessé (`injury_return_on`) ni vendu ;
   - **forme** : utilise `fit_with_form` de `gold.bv_slot_fit`. La forme change chaque dimanche [M§5.5] : vérifie la date du relevé (`gold.bv_roster_now.day`) et signale si elle est antérieure au dernier dimanche. Conseil du manuel : tireurs à 7 ou plus, joueurs à 5–6 pour les quarts-temps défensifs, reposer ceux à 4 ou moins [M§5.5].
   Donne le résultat du contrôle dans le brief.
2. **Moteur** : en saison 1, la ligue tourne en v3, gelé ; les amicaux sont en v4 ; la **ligue passe en v4 en saison 2** [Dev 2026-09-30, News 2026-10-11/16/17]. Pour chaque recommandation, dis si elle vaut pour v3, v4 ou les deux.
   **Mise à jour 2026-10-23** : la ligue passe en v4 après la dernière journée de la saison 1 (lundi 26/10) ; à partir du 27/10 elle est en v4 (premier match le 02/11, déduit). Applique les risques de blessure v4 (Soft 0,60, Medium soft 0,80, +40 % au-delà de 36 min au Q4) [News 2026-10-19] ; propose 1 test de Defensive area par amical avant le 02/11, un seul changement à la fois, et note que la ligue n'utilise pas ce réglage [M§6.6.2].

## Données
- `gold.bv_slot_fit` : chaque joueur sur chacun des 5 emplacements. `slot_ps` (compétences × poids du poste [M§2.2], indicatif [Dev 2026-09-17]), `height_eff` (taille sur l'emplacement [M§6.2.1]), `fit`, `fit_with_form` (forme [M§5.5]), `rank_in_slot`, fatigue actuelle.
- `gold.bv_fatigue_plan` : fatigue stabilisée avant un match du samedi (rythme lun/mer/sam), par joueur × minutes (12/24/36/48) × `defense_tier` (0–4), avec la pénalité en attaque v3 et la pénalité v4. Formule du manuel §5.6, vérifiée sur le tableau §5.6.4. Les amicaux (≈ 1/10) ne sont pas comptés.
- `gold.bv_roster_now` : dernier relevé de chaque joueur (compétences, taille, forme, fatigue, endurance, en vente).
- `gold.bv_next_opponents` : prochains matchs de ligue. Adversaire, rang, bilan, TS, humain ou bot, nos confrontations passées, ses 3 meilleurs scoreurs contre nous (points, part des tirs, notre focus).
- `gold.bv_match_opp_focus` / `gold.bv_match_player_lines` / `gold.bv_match_report` : détail des matchs passés (voir l'agent Match).
- `silver.bv_match_tactics` : tactiques jouées (nos cinqs, consignes, focus défensif ; `opponent_lineup_by_quarter` = cinqs de l'adversaire). Index 0–3 = Q1–Q4, 4 = prolongation.
- Consignes : **l'écran affiche 1 à 5 = nos données 0 à 4 (+1)**, confirmé par l'utilisateur le 2026-10-18. Agressivité défensive 1 Soft → 3 Équilibrée → 5 Agressive ; focus offensif 1 Low → 5 Primary ; rôle 1 Passeur → 5 Scoreur ; focus de tir 1 = 2 pts → 5 = 3 pts. **Donne toujours les valeurs de l'écran (1–5)** dans les fiches.

## Livrable
### 1. Tactique complète, prête à saisir (case E7)
- **Cinqs** : un tableau Q1, Q2, Q3, Q4, OT × PG, SG, SF, PF, C. Les rotations par quart-temps sont le levier contre les 36 min [M§5.7] ; en v4, la fatigue d'un match à l'autre compte aussi [News 2026-10-17].
- **Consignes par joueur** : passe ↔ tir, focus offensif, focus de tir, agressivité défensive. Une ligne par joueur, avec le libellé de l'écran et le cran, et la raison en quelques mots (profil de compétences [M§7.1]).
- **Depth chart** : pour chaque emplacement, 2 ou 3 remplaçants dans l'ordre [M§6.2.2].
- Rappel de saisie : sauvegarder le preset, puis **le re-sélectionner sur chaque match déjà planifié** [Com 2026-09-05]. Verrouillage à 19:45 (ligue) [M§6.5].

### 2. Ajustement à l'adversaire du prochain match (case E8)
- Lis `gold.bv_next_opponents` (1re ligne) et nos matchs passés contre lui.
- **Focus défensif** joueur par joueur [M§6.6] : Intense ou Lock sur le vrai scoreur (celui qui prend le plus de tirs), pas sur un meneur passeur ; Light ou Give up seulement sur les joueurs peu utilisés. Ses cinqs passés (`opponent_lineup_by_quarter`) disent qui joue le plus.
- 1 à 3 changements par rapport à la tactique de base (cinq, consignes), chacun justifié.
- Limite : les compétences adverses ne sont visibles qu'en tranches [M§4]. Dis-le quand tu raisonnes sur un duel.

### 2 ter. Blessés et plan B
- À chaque passage, liste les blessés : `gold.bv_roster_now.injury_return_on` (date de retour) et les sorties sur blessure du dernier match (`silver.bv_match_events`, `kind = 'injury'`). Blessures en ligue seulement, jamais en amical [M§1.2].
- Pour chaque blessé : quels matchs il manque (date de retour comparée à `gold.bv_next_opponents`), son remplaçant dans le cinq (meilleur `fit_with_form` du banc avec `height_eff` ≥ 95, sans faire dépasser 3 quarts-temps à personne), et le depth chart à corriger.
- Pense aux médecins (−25 % de durée chacun, embauchables après la blessure) et aux kinés (−12,5 % de risque chacun, comptés au coup d'envoi) [M§4.3, Dev 2026-09-14] : signale-le à l'agent Finances si une blessure touche un titulaire.
- Rappel : un joueur blessé ne progresse pas à l'entraînement de la semaine [M§8].

### 2 bis. Amicaux quotidiens (preset amical)
L'utilisateur joue **un amical presque chaque jour** (08:00, à domicile). C'est un levier majeur, pas un détail :
- **Règles** : pas de blessure, fatigue et expérience à ≈ 1/10 d'un match de ligue, recette ≈ 15 000–20 000 par match pour chaque club [M§1.2, §10.1.1 ; Com 2026-09-05]. Preset amical distinct du preset de ligue [M§6.4]. **Moteur v4** depuis le 11/10 [News] : c'est **le banc d'essai de la saison 2**.
- **Objectifs, dans l'ordre** :
  1. **expérience des jeunes** (≤ 21 ans, elle monte plus vite [M§5.4]) : leur donner beaucoup de minutes ;
  2. **tester en v4** un réglage prévu pour la saison 2 (agressivité, focus, cinq), un seul changement à la fois pour pouvoir le lire ;
  3. **ne pas user les titulaires de la ligue** : un amical le matin d'un match de ligue (lun / mer / sam) ajoute sa fatigue avant le coup d'envoi du soir [M§5.6.2]. Calcule en SQL la fatigue ajoutée : minutes × 0,019 × multiplicateur d'agressivité × (1,5 − 0,008 × endurance), soit le dixième d'un match de ligue.
- **Livrable** : un preset amical (cinqs, consignes) et, pour chaque amical programmé, ce qu'on teste et le critère de lecture. La liste des amicaux est dans `silver.bv_api` (`endpoint ~ '/friendlies$'`, dernière capture, `body->'friendlies'`, statut `scheduled`). Les jours sans amical, propose d'en programmer un (10 au maximum [M§1.2]).

### 3. Évolution à partir du journal (case E9)
- Pour chaque enseignement confirmé ou à surveiller qui touche la tactique, dis ce que tu gardes, changes ou testes.
- Un réglage incertain se teste **d'abord en amical** (sans blessure, fatigue à 1/10 [M§1.2]), sachant que les amicaux sont déjà en v4.
- Ajoute chaque nouveau conseil dans la section Conseils de `outputs/basketvibe/learnings.md` (ID `C-nnn`, critère vérifiable en SQL), pour que l'agent Match le contrôle.

## Sortie propre au jeu
- En tête du brief : la **fiche de saisie** (cinqs, consignes, depth chart, focus défensif), puis les justifications et le contrôle SQL.
- Si la forme n'est pas à jour ou si la tactique adverse est inconnue, dis-le et indique quel export faire.
