Amical contre Garden City (26/11)
Verrou : jeu. 26/11 07:45 (match 08:00)
Adversaire : Garden City (joueurs du 09/11 connus)
## À saisir
### Écran 1 — Composition
| | PG | SG | SF | PF | C |
|---|---|---|---|---|---|
| Q1 | Baron | Leclerc | Durand | Legrand | Bernard |
| Q2 | Boyer | Leclerc | Durand | Legrand | Fournier |
| Q3 | Baron | Leclerc | Boyer | Fournier | Bernard |
| Q4 | Baron | Durand | Legrand | Fournier | Bernard |
| Prol. | Baron | Leclerc | Durand | Legrand | Bernard |
### Écran 2 — Consignes
| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Min | Off. focus | Rôle | Tir | Agress. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baron | PG | PG | — | PG | PG | PG | 36 | 3 | 3 | 3 | 3 |
| Boyer | PG | — | PG | SF | — | — | 24 | 3 | 3 | 3 | 3 |
| Richard | PG | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Bonnet | SG | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Leclerc | SG | SG | SG | SG | — | SG | 36 | 3 | 3 | 3 | 3 |
| Durand | SF | SF | SF | — | SG | SF | 36 | 3 | 3 | 3 | 3 |
| Gimenez | SF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Albano | PF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Lefebvre | PF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Legrand | PF | PF | PF | — | SF | PF | 36 | 3 | 3 | 3 | 3 |
| Bernard | C | C | — | C | C | C | 36 | 3 | 3 | 3 | 3 |
| Fournier | C | — | C | PF | PF | — | 36 | 3 | 3 | 3 | 3 |
### Écran 3 — Adversaires
| Adversaire | Poste | Focus défensif (1-5) | Zone |
|---|---|---|---|
| Caune | PG | 3 (Normal) | Perimeter (1) |
| Colin | PG | 3 (Normal) | Perimeter (1) |
| Roze | PG | 3 (Normal) | Perimeter (1) |
| Vītols | PG | 3 (Normal) | Perimeter (1) |
| Siliņš | SG | 3 (Normal) | Perimeter (1) |
| Franzoni | SF | 3 (Normal) | Perimeter (1) |
| Ozoliņķis | SF | 3 (Normal) | Perimeter (1) |
| Trajković | SF | 3 (Normal) | Perimeter (1) |
| Bērziņš | PF | 3 (Normal) | Perimeter (1) |
| Kalniņš | PF | 3 (Normal) | Perimeter (1) |
| Cunanan | C | 3 (Normal) | Perimeter (1) |
| Jansons | C | 3 (Normal) | Perimeter (1) |
## Après sauvegarde, vérifie
- [ ] Agress. = 3 pour chacun des 12 joueurs
- [ ] Off. focus = 3, Rôle = 3, Tir = 3 pour les 12 joueurs
- [ ] Min : Boyer 24 ; Baron, Leclerc, Durand, Legrand, Bernard, Fournier 36 ; les 5 autres 0
- [ ] Albano (en vente) absent de tous les quarts et de la prolongation
- [ ] Les 12 adversaires : focus 3, zone Perimeter (1)
## À exporter ensuite
La page du match, après la fin du match (~08:55 le 26/11).
---
## Annexe — pourquoi

Heure de Paris 24/11 08:43. Amical du 26/11 08:00, sans preset, moteur v5, fatigue et expérience ≈ 1/10, pas de blessure [M§1.2]. Aucun brief Match du jour lu : signalé. Données du relevé du 23/11 (`gold.bv_roster_now`) : le match de ligue du 25/11 20:00 les modifiera ; si les fatigues exportées après lui ont changé, la fiche est à refaire.

### Joueurs exclus
Albano : seul joueur `on_transfer_list` = True (`gold.bv_roster_now`) ; 0 min dans tous les quarts. La consigne de l'utilisateur est tronquée (« 1) ») : seul Albano est identifiable. Aucune vente exécutée ici (règle 2).

### Test E1 niveau A (un seul test)
`docs/attentes/experiences-amicales-basketvibe.yaml` : agressivité 3 à l'écran (cran 2) sur les 12, y compris ceux à 0 min. Neutre : zone Perimeter, focus 3, Off. focus 3, aucun Tir cran 4. Rôle 3 et Tir 3 non fixés par le yaml, mis à 3 pour ne faire bouger aucune autre variable. L'agressivité du test égale le neutre : aucune valeur isolée. L-004 (agressivité 1) non appliqué : le test impose le niveau A. Aucun nouveau conseil (test inchangé, C-134 en vigueur).

### Contrôle SQL (plan en `values` joint à `gold.bv_slot_fit`)
- 20 lignes Q1–Q4 : 5 joueurs différents par quart, un par emplacement ; max 3 quarts par joueur (Boyer 2) ; minutes 6 × 36 + 24 = 240.
- `height_eff` minimum 99,2 (Boyer SF, Legrand SF) ≥ 95 ; `fit_with_form` de 41,3 (Leclerc SG) à 56,4 (Fournier) : amical de formation, fit bas assumé.
- En vente ou blessés dans le plan : 0 (`on_transfer_list`, `injury_return_on` vide pour les 12).
- Fatigue au 23/11 : Boyer 21,33 (24 min), Fournier 19,62, Legrand 18,85, Bernard 15,79, Durand 10,34, Leclerc 3,96, Baron 3,32. Pas de match de ligue le 26/11 au soir (agenda : ligue 25/11 et 28/11) : surcoût amical ≈ 1/10, non mesuré en vue. Forme du 23/11 (postérieure au dimanche 22/11).

### Adversaire : Garden City
Nos résultats (`gold.bv_match_report`) : un amical, 09/11, défaite 104-120 (L), 2P adverse 64,8 %, 3P adverse 33,3 %, eFG adverse 58,9 %. Un seul match, non concluant ; ligue : aucune ligne (`gold.bv_next_opponents` en timeout, non relevé). Rang et bilan : non relevés.

**Focus défensif** (`gold.bv_match_opp_focus`, match du 09/11, notre focus alors Normal partout) :
| Joueur | Poste | Min | Part de tirs | 3PA/FGA | Focus visé après le test |
|---|---|---|---|---|---|
| Cunanan | C | 48 | 25,6 % | 11/23 | Intense (4) |
| Jansons | C | 48 | 24,4 % | 7/22 | Normal |
| Kalniņš | PF | 48 | 21,1 % | 5/19 | Normal |
| Franzoni | SF | 48 | 14,4 % | 7/13 | Normal |
| Siliņš | SG | 24 | 8,9 % | 2/8 | Normal |
| Caune | PG | 24 | 5,6 % | 4/5 | Light envisageable |
| Six autres | — | 0 | 0 % | — | Normal (inconnus en jeu) |

Saisie du jour : Normal (3) et Perimeter (1) partout, car E1 fixe `constants: {zone: Perimeter, focus: 3}` (yaml) ; Cunanan Intense ajouterait une seconde variable et fausserait la lecture de l'agressivité. Avis : Intense sur Cunanan (30 pts, 23 tirs) dès la fin de E1. Limite : effectif adverse du 09/11 ; il a pu changer, aucun export récent.

### Blessés et plan B
Aucun blessé (`injury_return_on` vide, 12 joueurs) ; pas de blessure en amical [M§1.2]. Plan B si un export post-ligue montre un joueur à fatigue > 25 : le remplacer par Lefebvre (PF, forme 8) ou Gimenez (SF, forme 10), à recontrôler en SQL.

### Transferts
« Pas d'enchère avant le test ; Police : ne pas acheter — tester le potentiel » : respecté, aucun achat, vente ni enchère dans cette fiche. Aucune somme au-dessus de 250 000.

Anticipation : sans objet (amical).
