# Tactique BasketVibe, brief du 2026-11-04 : AMICAL jeudi 05/11 08:00 Paris, DOMICILE contre |HAVEX|

**Heure limite : verrou 05/11 07:45 Paris ; à saisir CE SOIR (avant la ligue 20:00 ou après).** Pas de preset (tactique du match seulement ; la ligne `gold.bv_agenda` « preset amical » est contredite par la fiche `resume.md`, la fiche gagne). Objectif de la base : « tester » (`gold.match_objective`, 05/11 amical |HAVEX|, domicile). Adversaire sans importance : aucun export de preview. Amont lu : `briefs/2026-11-02-tactique-amical.md`, `briefs/2026-11-04-tactique.md` (ligue J2 ce soir).

## 1. Test unique
**Zone Perimeter (1) pour les 12 adversaires, refaite.** Le test du 03/11 est illisible : `gold.bv_saisie_joueurs`, `gold.bv_saisie_adversaires` et `gold.bv_zone_jouee` s'arrêtent au 31/10 (non sauvegardé), donc on ne sait pas quelle zone ni quels réglages ont été joués le 03/11 et le 04/11 (`gold.bv_match_report` : NY Lighters −21, opp 2P 59,3 %, opp 3P 42,5 % ; baker street +2, opp 2P 64,2 %). Seul Perimeter lisible : 30/10 Istanbul Cobras +27, opp 2P 45,5 % (saved, n = 1). Rien d'autre ne change (un seul test) hormis l'effectif contraint.

## 2. Saisie
**Effectif (`gold.bv_roster_now`, day 2026-11-04) : 14 joueurs, aucun blessé** (`injury_return_on` nul). Lecomte, Henry, Klein, Fontaine absents : retirés du tableau. Richard (fatigue 4,84), Bonnet (5,21), Gimenez (5,75), Lefebvre (4,37), Fournier (4,93) jouent la ligue ce soir : 0 minute en amical. Fatigue des neuf placés : Ungureanu 1,63, Legrand 2,13, Boyer 1,95, Durand 1,23, Dang 1,27, Albano 0,70, Leclerc 0,68, Bernard 0,63, Baron 0,63 (amical : fatigue ≈ 1/10 [M§1.2]).
**Contrainte** : Lecomte parti, Durand est le seul SF disponible (Gimenez en ligue) : il joue les 4 quarts. Seul écart de plan vs 02/11, imposé, pas un test.

### Écran 1 : composition
| | PG | SG | SF | PF | C |
|---|---|---|---|---|---|
| Q1 | Baron | Leclerc | Durand | Albano | Bernard |
| Q2 | Boyer | Leclerc | Durand | Legrand | Bernard |
| Q3 | Baron | Leclerc | Durand | Albano | Ungureanu |
| Q4 | Boyer | Dang | Durand | Legrand | Ungureanu |
| Prolongation | Boyer | Dang | Durand | Legrand | Ungureanu |
Pas de remplacement programmé. Aucun joueur du cinq de ligue.

### Écran 2 : consignes (1 à 5), ordre de l'export
Réglages repris du plan du 02/11 (dernier plan écrit ; le dernier amical enregistré en base est le 30/10 : Leclerc Tir 5 y était, remplacé par Tir 3 depuis C-110 ; Lecomte à Tir 1 sans objet).
| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Minutes | Off. focus | Rôle | Tir | Agress. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baron | PG | PG | — | PG | — | — | 24 | 2 | 1 | 3 | 1 |
| Boyer | PG | — | PG | — | PG | PG | 24 (+5) | 2 | 2 | 3 | 1 |
| Richard | PG | — | — | — | — | — | 0 | 1 | 1 | 3 | 1 |
| Bonnet | SG | — | — | — | — | — | 0 | 5 | 5 | 5 | 1 |
| Dang | SG | — | — | — | SG | SG | 12 (+5) | 3 | 3 | 3 | 3 |
| Leclerc | SG | SG | SG | SG | — | — | 36 | 4 | 4 | 3 | 1 |
| Durand | SF | SF | SF | SF | SF | SF | 48 (+5) | 3 | 3 | 3 | 1 |
| Gimenez | SF | — | — | — | — | — | 0 | 3 | 3 | 3 | 1 |
| Albano | PF | PF | — | PF | — | — | 24 | 3 | 3 | 3 | 3 |
| Lefebvre | PF | — | — | — | — | — | 0 | 4 | 4 | 1 | 1 |
| Legrand | PF | — | PF | — | PF | PF | 24 (+5) | 3 | 3 | 1 | 1 |
| Bernard | C | C | C | — | — | — | 24 | 2 | 2 | 1 | 1 |
| Fournier | C | — | — | — | — | — | 0 | 2 | 2 | 1 | 1 |
| Ungureanu | C | — | — | C | C | C | 24 (+5) | 3 | 3 | 3 | 3 |
Minutes : 24+24+0+0+12+36+48+0+24+0+24+24+0+24 = 240. Les valeurs de Richard, Bonnet, Gimenez, Lefebvre, Fournier sont celles du plan du 02/11 (ils ne jouent pas ; à vérifier sur l'écran, pas de changement voulu).

### Écran 3 : adversaires (|HAVEX|, une ligne par joueur, ordre PG → C)
Je n'ai pas les joueurs de |HAVEX| (cherché dans : `gold.bv_saisie_adversaires` (rien avant 31/10 pour |HAVEX|), `gold.bv_next_opponents` (ligue seulement), `gold.match_objective` (nom seulement)). Règle de la fiche : aucun export demandé. À l'écran : une ligne par joueur affiché, PG, SG, SF, PF, C puis alphabétique, toutes identiques.
| Adversaire (chaque joueur de |HAVEX| affiché, un par ligne) | Focus | Zone |
|---|---|---|
| tous les joueurs, ligne par ligne | 3 (Normal) | Perimeter (1) |
Aucun focus 1 ni 5 : rien pour distinguer un joueur.

## 3. Mesure après le match (export de la page du match après 08:55, plan sauvegardé)
- `gold.bv_zone_jouee` : ligne 05/11 avec `area_step` 1 et `sauvegarde_match` vrai. Sinon, test illisible, à refaire.
- `gold.bv_match_report` : 2P% adverse (`opp_fg2_pct`) et `margin`.
- **Preuve que j'avais tort** : `opp_fg2_pct` > 59,4 % (niveau Rim du 27/10) ; Perimeter confirmé seulement si ≤ 53,4 % et marge ≥ +5. Entre les deux : non tranché (n = 1 par zone, adversaires différents). Référence : Middle 10/20, 10/24, 10/26 → opp 2P 52,4 / 58,2 / 50,9 % (moy. 53,8) ; Rim 10/27 → 59,4 % ; Perimeter 10/30 → 45,5 % (tous `gold.bv_match_report`).

## 4. Ce qui me manque
- Tactique jouée les 03/11 et 04/11 (zone, réglages). Cherché dans : `gold.bv_zone_jouee` (dernière ligne amical : 31/10), `gold.bv_saisie_joueurs` (idem), `gold.bv_saisie_adversaires` (idem), `gold.bv_match_report` (résultats seulement). Export à faire : la page de tactique du match avant le verrou (une page ouverte avant 07:45 suffit, plan enregistré) ; sans elle, le résultat du 05/11 sera encore illisible.
- Joueurs de |HAVEX| : non demandés (règle de la fiche).
- Focus défensif : neutre (3, Perimeter) pour tous, faute de données adverses ; pas de parts de tirs à citer.

Conseil enregistré : **C-114** dans `outputs/basketvibe/learnings.md`. Risque : Durand 48 min (PS 43,4) peut coûter des points ; la mesure juge la zone, pas le score.
