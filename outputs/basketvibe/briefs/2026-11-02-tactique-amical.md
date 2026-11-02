# Tactique BasketVibe, brief du 2026-11-02 : AMICAL mardi 03/11 08:00 Paris, DOMICILE contre NY Lighters

**Heure limite : verrou 03/11 07:45 Paris ; à saisir AUJOURD'HUI.** Pas de preset (tactique du match seulement). Amont : `briefs/2026-11-02-match.md` (C-107 faux, Perimeter, Leclerc Tir 3, C-110), fiche 3 de `briefs/2026-11-01-tactique.md`, `fait-2026-11-02.md`. Sources : `gold.bv_roster_now` (relevé du 02/11), `silver`/bronze 33139 (schedule 02/11 13:38 UTC : NY Lighters, 03/11 08:00, HOME, Tactics « - » = rien enregistré), `gold.bv_saisie_adversaires`.

## Effectif et fatigue (`gold.bv_roster_now`, day 2026-11-02)
- Placés : Baron, Boyer, Leclerc, Dang, Durand, Lecomte, Albano, Legrand, Bernard, Ungureanu. Aucun blessé (`injury_return_on` nul pour tous). Klein et Fontaine : lignes périmées (25/10 et 29/10), vendus, **non placés**. Henry (en vente) et Lecomte (en vente jusqu'à demain ~08:57 selon C-111, annonce encore active, `on_transfer_list` vrai) restent dans l'effectif : Lecomte joue (08:00 < 08:57).
- Fatigue relevée : Lecomte 0,95, Leclerc 0,66, Albano 0,47, Ungureanu 0,47, Bernard 0,42, Baron 0,42, Boyer 0,38, Legrand 0,35, Dang 0,23, Durand 0,17. Seuil de pénalité v4 = 20 [skill basketvibe-joueurs, News 2026-10-27] : tout est sous 1, après une nuit de récupération rien ne s'approche du seuil. Le plan ne change pas.
- Richard, Bonnet, Gimenez, Lefebvre, Fournier : 0 minute (ligue ce soir 20:00 à Chara, verrou 19:45, déjà saisie [fait-2026-11-02]). Fatigue 0 pour les cinq.

## Test unique (C-110 du brief Match)
Zone **Perimeter (1)** pour tous les adversaires + Leclerc Tir 5 → 3. Le reste est identique au plan joué le 02/11 contre Galit (D 103-112). Le changement Leclerc agit sur son 3P%, pas sur le 2P% adverse : la lecture de la zone reste propre.
Mesure (export du match après 08:55, plan sauvegardé) : `gold.bv_zone_jouee` area_step 1 ; 2P% adverse et marge dans `gold.bv_match_report`.
Preuve contraire : **faux** si 2P% adverse > 59,4 % (niveau Rim). Perimeter confirmé si 2P% adverse ≤ 53,4 % et marge ≥ +5. Leclerc : faux si 3P% < 15 % sur 3 tirs ou plus ; Tir 3 réussi si ≥ 25 % ou moins de 8 tirs à 3. Plan non sauvegardé = test illisible.

## Écran 1 : composition
| | PG | SG | SF | PF | C |
|---|---|---|---|---|---|
| Q1 | Baron | Leclerc | Lecomte | Albano | Bernard |
| Q2 | Boyer | Leclerc | Lecomte | Legrand | Bernard |
| Q3 | Baron | Leclerc | Durand | Albano | Ungureanu |
| Q4 | Boyer | Dang | Lecomte | Legrand | Ungureanu |
| Prolongation | Boyer | Dang | Lecomte | Legrand | Ungureanu |
Pas de remplacement programmé.

## Écran 2 : consignes (1 à 5)
| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Min | Off. focus | Rôle | Tir | Agress. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baron | PG | PG | — | PG | — | — | 24 | 2 | 1 | 3 | 1 |
| Boyer | PG | — | PG | — | PG | PG | 24 (+5) | 2 | 2 | 3 | 1 |
| Richard | PG | — | — | — | — | — | 0 | 1 | 1 | 3 | 1 |
| Bonnet | SG | — | — | — | — | — | 0 | 5 | 5 | 5 | 1 |
| Dang | SG | — | — | — | SG | SG | 12 (+5) | 3 | 3 | 3 | 3 |
| Henry | SG | — | — | — | — | — | 0 | 4 | 4 | 4 | 1 |
| Leclerc | SG | SG | SG | SG | — | — | 36 | 4 | 4 | **3** | 1 |
| Durand | SF | — | — | SF | — | — | 12 | 3 | 3 | 3 | 1 |
| Gimenez | SF | — | — | — | — | — | 0 | 3 | 3 | 3 | 1 |
| Lecomte | SF | SF | SF | — | SF | SF | 36 (+5) | 3 | 3 | 1 | 1 |
| Albano | PF | PF | — | PF | — | — | 24 | 3 | 3 | 3 | 3 |
| Lefebvre | PF | — | — | — | — | — | 0 | 4 | 4 | 1 | 1 |
| Legrand | PF | — | PF | — | PF | PF | 24 (+5) | 3 | 3 | 1 | 1 |
| Bernard | C | C | C | — | — | — | 24 | 2 | 2 | 1 | 1 |
| Fournier | C | — | — | — | — | — | 0 | 2 | 2 | 1 | 1 |
| Ungureanu | C | — | — | C | C | C | 24 (+5) | 3 | 3 | 3 | 3 |
Minutes : 24+24+12+36+12+36+24+24+24+24 = 240. Seul changement vs 02/11 : Leclerc Tir 5 → 3 (en gras).

## Écran 3 : adversaires (NY Lighters)
**Il me manque les 12/13 joueurs de NY Lighters** (aucun aperçu ni box score exporté : `gold.bv_saisie_adversaires` ne contient que nos plans d'amicaux passés ; `gold.bv_next_opponents` ne couvre que la ligue ; bronze 33139 et 32124 ne citent NY Lighters que dans la liste du calendrier). Cherché dans : `gold.bv_saisie_adversaires`, `gold.bv_next_opponents`, `gold.bv_match_opp_focus`, `silver.bv_fixtures`, `bronze.raw_pages` (texte « Lighters », 6 pages, toutes des calendriers). Règle de la fiche : adversaire d'amical sans importance, aucun aperçu à demander. On le réunit comme ça : à l'écran, tous les joueurs que le jeu affiche sont réglés pareil, dans l'ordre de l'écran (PG, SG, SF, PF, C, puis alphabétique) ; la ligne « Tous » ci-dessous s'applique à chacun.
| Adversaire | Poste | Focus | Zone |
|---|---|---|---|
| Chaque joueur de NY Lighters, ligne par ligne (PG, SG, SF, PF, C) | tous | 3 | 1 (Perimeter) |
Aucun focus 1 ni 5 : pas de donnée pour distinguer un joueur (test de zone seul).

## Évolution
C-110 (Match) : deux changements seulement. C-112 ajouté (voir `learnings.md`) : même saisie, critère de lecture. Les ids C-110 sont en double dans `learnings.md` (Transferts Lazauskas et Match NY Lighters) : à renuméroter côté Match.
