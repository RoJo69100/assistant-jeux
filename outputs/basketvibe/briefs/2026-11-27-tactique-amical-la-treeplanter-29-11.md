Amical contre LA TreePlanter (29/11)
Verrou : dim. 29/11 07:45 (match 08:00, à domicile) — pas de preset, composition de TEST, sauvegarde du match ; à saisir aujourd'hui 27/11
Adversaire : LA TreePlanter (joueurs non vérifiés en base : requêtes expirées) — test E1 niveau A, agressivité 3 à l'écran (cran 2) sur tous
## À saisir
### Écran 1 — Composition
| | PG | SG | SF | PF | C |
|---|---|---|---|---|---|
| Q1 | Baron | Leclerc | Bourdon | Legrand | Bernard |
| Q2 | Boyer | Richard | Gimenez | Fournier | Bernard |
| Q3 | Baron | Leclerc | Bourdon | Legrand | Fournier |
| Q4 | Boyer | Richard | Gimenez | Legrand | Fournier |
| Prol. | Boyer | Richard | Gimenez | Legrand | Fournier |
### Écran 2 — Consignes
| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Min | Off. focus | Rôle | Tir | Agress. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baron | PG | PG | — | PG | — | — | 24 | 3 | 3 | 3 | 3 |
| Boyer | PG | — | PG | — | PG | PG | 24 | 3 | 3 | 3 | 3 |
| Richard | PG | — | SG | — | SG | SG | 24 | 3 | 3 | 3 | 3 |
| Bonnet | SG | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Leclerc | SG | SG | — | SG | — | — | 24 | 3 | 3 | 3 | 3 |
| Bourdon | SF | SF | — | SF | — | — | 24 | 3 | 3 | 3 | 3 |
| Durand | SF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Gimenez | SF | — | SF | — | SF | SF | 24 | 3 | 3 | 3 | 3 |
| Lefebvre | PF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Legrand | PF | PF | — | PF | PF | PF | 36 | 3 | 3 | 3 | 3 |
| Bernard | C | C | C | — | — | — | 24 | 3 | 3 | 3 | 3 |
| Fournier | C | — | PF | C | C | C | 36 | 3 | 3 | 3 | 3 |
### Écran 3 — Adversaires
| Adversaire | Poste | Focus défensif (1-5) | Zone |
|---|---|---|---|
| Tous les joueurs de LA TreePlanter | tous | 3 | Perimeter (1) |
## Après sauvegarde, vérifie
- [ ] Min : Legrand 36, Fournier 36 ; Baron, Boyer, Richard, Leclerc, Bourdon, Gimenez, Bernard 24 ; Bonnet, Durand, Lefebvre 0
- [ ] Agress. = 3 pour les 12 ; Off. focus 3, Rôle 3, Tir 3 pour les 12
- [ ] Durand absent des 5 quarts ; aucun joueur au-delà de 36 min
- [ ] Adversaires : focus 3 et zone Perimeter (1) pour tous
## À exporter ensuite
La page du match amical LA TreePlanter (29/11) une fois sauvegardé, avant 07:45 ; après le match, la page du match pour lire le test.
---
## Annexe — pourquoi

### Limite des données (à lire d'abord)
Le 27/11 ~10:50, les requêtes sur `gold.bv_slot_fit`, `gold.bv_saisie_adversaires` (filtre TreePlanter) et `gold.bv_next_opponents` ont expiré (timeout HTTPS 30 s, 4 essais). Lus avec succès : `gold.bv_roster_now` (relevé du 27/11, semaine du 22/11, à jour) et `gold.bv_agenda`. Les valeurs `fit_with_form` et `height_eff` ci-dessous sont celles du brief du jour `2026-11-27-tactique-amical-saile-c-b-28-11.md` (même relevé du 27/11, même effectif), non rejouées. Le contrôle SQL des cinqs n'a donc pas été refait : à relancer dès que la base répond.

### Test (un seul)
E1 niveau A (`docs/attentes/experiences-amicales-basketvibe.yaml`) : agressivité 3 à l'écran (cran 2) sur les 12. Tout le reste au neutre du fichier : zone Perimeter, focus 3, 0 joueur en Tir 5 (max 1), aucun Primary (Off. focus 3). Rôle 3 et Tir 3 uniformes : rien d'autre ne brouille la lecture. Attendu dans `gold.bv_amical_reglage` : `agress_cran` = 2.

### Exclusion demandée
Jonathan Durand : 0 minute, absent des 5 quarts, listé à 0 pour que sa ligne soit complète. Sa vente est proposée au plan ; je n'exécute rien (règle 2). Aucun montant : pas de « police requise » à poser.

### Choix de composition (amical : jeunes d'abord, titulaires de ligue ménagés ; `gold.bv_roster_now` du 27/11, la composition reprend celle de l'amical du 28/11 car l'effectif et les chiffres de fit sont identiques)
- Repos total : Bonnet (fatigue 20,35) et Lefebvre (19,43), titulaires de ligue ; Durand exclu.
- Jeunes en minutes [M§5.4] : Baron 17 ans, Leclerc 17, Bourdon 16, Bernard 18, Boyer 20.
- Richard, Gimenez : 24 min. Legrand, Fournier : 36 min (max).
- Forme : relevé du 27/11, semaine du 22/11 : à jour [M§5.5].
- Risque : le 28/11 20:00 il y a un match de ligue (`gold.bv_agenda`), et le plan ligue n'est pas connu ici. La fatigue au coup d'envoi du 29/11 dépend de ce match : non estimable aujourd'hui. Si l'export du match de ligue (~20:50) montre un joueur du cinq au-delà de 22 de fatigue, le remplacer dans le cinq (règle de l'utilisateur du 25/11) avant le verrou ; sinon aucun retrait de minutes entre 20 et 22. Avec la même règle, la limite 36 min (3 quarts) est respectée pour tous.
- Fit repris du brief Saile (27/11, `gold.bv_slot_fit`) : `height_eff` minimum 98,4 (Bourdon SF), les autres 100 ; `fit_with_form` Baron PG 44,7, Leclerc SG 41,3, Bourdon SF 50,9, Legrand PF 51,9, Bernard C 49,3 ; Boyer PG 50,6, Richard SG 56,9, Gimenez SF 69,3, Fournier PF 56,4. Fit faible Baron et Leclerc : accepté, amical d'expérience sans blessure [M§1.2].
- Contrôle de structure (fait ici à la main) : 4 quarts + prolongation, 5 joueurs différents par ligne, chacun sur un emplacement différent ; minutes totales 240 ; Legrand et Fournier 3 quarts chacun (Q1, Q3, Q4 ; Q2, Q3, Q4), Bernard 2, les autres 2 ; aucun > 3.
- Aucun blessé (`injury_return_on` vide pour les 12, `gold.bv_roster_now`) ; aucun des cinqs en vente sauf Durand, exclu.

### Focus défensif
LA TreePlanter : aucun joueur adverse lu en base (la requête sur `gold.bv_saisie_adversaires` a expiré, aucun match passé confirmé contre lui). Parts de tirs, 2P/3P : inconnues. Donc focus neutre : Normal (3) pour tous, aucun Intense, Light ni Give up ; zone Perimeter (1), neutre E1 constant [fiche tactique § 2 quater]. Export à faire : la page du match (donne les noms pour la prochaine fois). Pas de test du focus par joueur en amical (arbitrage 15). Écran 3 : une ligne regroupée ici faute de noms ; à saisir ligne par ligne dans l'ordre de l'écran, tous en 3 / Perimeter.

### Blessés et plan B
Aucun blessé ; pas de blessure en amical [M§1.2]. Plan B (fit du brief Saile) : PG Baron → Richard (57,4) ; SG Leclerc → Bonnet (54,2) ; SF Bourdon → Gimenez (69,3) ; PF Legrand → Lefebvre (67,6) ; C Bernard → Fournier (56,4). Durand exclu.

### Valeurs qui s'écartent de la règle uniforme
Agress. 3 au lieu de 1 : c'est le test E1 A demandé (L-032 : aucun gain de l'agressivité 1). Aucune autre valeur isolée.

### Évolution
Garde : 36 min max, agressivité 3 uniforme. Teste : E1 A. Conseil **C-148** ajouté dans `learnings.md` (confiance faible : contrôles non rejoués).
