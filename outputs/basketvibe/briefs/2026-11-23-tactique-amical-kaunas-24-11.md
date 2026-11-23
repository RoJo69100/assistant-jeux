Amical contre Kaunas (24/11)
Verrou : mar. 24/11 07:45 (match 08:00)
Adversaire : Kaunas (joueurs inconnus)
## À saisir
### Écran 1 — Composition
| | PG | SG | SF | PF | C |
|---|---|---|---|---|---|
| Q1 | Baron | Leclerc | Boyer | Legrand | Bernard |
| Q2 | Boyer | Durand | Leclerc | Albano | Bernard |
| Q3 | Baron | Leclerc | Boyer | Legrand | Albano |
| Q4 | Baron | Durand | Albano | Legrand | Bernard |
| Prol. | Baron | Boyer | Durand | Legrand | Albano |
### Écran 2 — Consignes
| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Min | Off. focus | Rôle | Tir | Agress. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baron | PG | PG | — | PG | PG | PG | 36 | 3 | 3 | 3 | 3 |
| Boyer | PG | SF | PG | SF | — | SG | 36 | 3 | 3 | 3 | 3 |
| Richard | PG | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Bonnet | SG | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Leclerc | SG | SG | SF | SG | — | — | 36 | 3 | 3 | 3 | 3 |
| Durand | SF | — | SG | — | SG | SF | 24 | 3 | 3 | 3 | 3 |
| Gimenez | SF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Albano | PF | — | PF | C | SF | C | 36 | 3 | 3 | 3 | 3 |
| Lefebvre | PF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Legrand | PF | PF | — | PF | PF | PF | 36 | 3 | 3 | 3 | 3 |
| Bernard | C | C | C | — | C | — | 36 | 3 | 3 | 3 | 3 |
| Fournier | C | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
### Écran 3 — Adversaires
| Adversaire | Poste | Focus défensif (1-5) | Zone |
|---|---|---|---|
| Les 12 | tous | 3 (Normal) | Perimeter (1) |
## Après sauvegarde, vérifie
- [ ] Agress. = 3 pour chacun des 12 joueurs
- [ ] Off. focus = 3, Rôle = 3, Tir = 3 pour les 12 joueurs
- [ ] Min : Baron, Boyer, Leclerc, Albano, Legrand, Bernard 36 ; Durand 24 ; les 5 autres 0
- [ ] Les 12 adversaires : focus 3, zone Perimeter (1)
## À exporter ensuite
La page du match, après la fin du match (~08:55 le 24/11) : elle donnera les noms adverses.
---
## Annexe — pourquoi

Saisie AUJOURD'HUI lundi 23/11 (Paris 16:43, `pipelines/heure_paris.py`) pour l'amical du 24/11 08:00. Amical : pas de preset, moteur v5, fatigue et expérience ≈ 1/10, pas de blessure [M§1.2]. Brief amont : aucun brief Match du jour lu (aucun pour le 23/11), signalé ; brief Entraînement du 23/11 sans effet sur ce match.

### Test E1 niveau A et réglage neutre
Consigne : un seul test, E1 niveau A (`docs/attentes/experiences-amicales-basketvibe.yaml`) : agressivité 3 à l'écran (cran 2, équilibrée) pour les 12, y compris ceux à 0 min. Neutre (yaml `neutre` + constants E1) : zone Perimeter (1), focus défensif 3 sur les adversaires, Off. focus 3 (aucun Primary), aucun Tir cran 4. Rôle 3 et Tir 3 : le yaml ne fixe pas ces deux colonnes, j'ai pris 3 pour qu'aucune autre variable ne bouge. Seule l'agressivité est celle du test ; ici elle égale le neutre (cran 2), donc aucune valeur isolée. L-004 (agressivité 1) n'est pas appliqué : le test impose le niveau A.
Série E1 (`gold.bv_amical_reglage`) : 19/11 BG Bangers cran 2 (L), 08/11 NYC Cyclones cran 0 (L) ; les amicaux du 20 et 21/11 sont prévus au cran 4 (C-128/C-129, hors vue à ce jour). Ordre du yaml A, B, A, B : niveau A conforme à la consigne. Lecture après export : `opp_fg2_pct`, `pf`, `o_fta`, `opp_efg_pct` contre la série cran 2 (18/11 : `opp_fg2_pct` 78,0, `pf` 22).

### Composition (7 joueurs)
Jeunes d'abord [M§5.4] : Baron 17, Leclerc 17, Boyer 20, Bernard 18 (144 min sur 240). Les cinq de J10 (Richard, Bonnet, Gimenez, Lefebvre, Fournier) à 0 min : la ligue J11 est mercredi 25/11 19:45 (`gold.bv_agenda`), aucune ligue le 24/11. Minutes : six joueurs à 36, Durand 24, total 240. Même sept que l'amical du 23/11 : seule l'agressivité est l'objet du test. Remplaçants (depth chart) : aucun programmé ; hors jeu : Lefebvre, Fournier, Richard, Gimenez, Bonnet.

### Contrôle SQL (fait : plan en `values` joint à `gold.bv_slot_fit`)
- 20 lignes Q1–Q4, 20 couples (quart, joueur) distincts : 5 joueurs différents, un par emplacement, par quart.
- Maximum 3 quarts par joueur : oui (6 à 3, Durand à 2) ; aucun `over_36` hors prolongation.
- `height_eff` minimum 98,4 (Leclerc SF) ≥ 95 ; `fit_with_form` moyen 47,2 (Durand SG 43,0, Leclerc SG 41,2 : le plus bas, seul SG/SF jeune dispo, amical de formation).
- Blessés ou en vente : 0 (`injury_return_on`, `on_transfer_list`).
- Forme : relevé du 23/11 (`gold.bv_roster_now.day`), postérieur au dimanche 22/11 : à jour. Leclerc 4 et Durand 4 (≤ 4 : repos conseillé [M§5.5]), Baron 5 : ils jouent pour le temps de jeu des jeunes ; Durand seulement 24 min.
- Fatigue (`gold.bv_roster_now`) : Boyer 16,24, Bernard 15,79, Legrand 14,2, Durand 10,34, Leclerc 3,96, Albano 3,81, Baron 3,32. Le surcoût amical n'est pas dans une vue : non mesuré (≈ 1/10). Ces joueurs ne sont pas le cinq de J11.

### Adversaire : Kaunas
`gold.bv_saisie_adversaires` : aucune ligne ; `gold.bv_match_report` : aucun match contre lui. Joueurs, parts de tirs, 2P/3P inconnus ; amical : aucun aperçu à demander.
**Focus défensif** : aucun joueur adverse connu : Normal (3) sur les 12, zone Perimeter (neutre E1), aucun Intense, Light ni Give up. Export à faire : la page du match après ~08:55 le 24/11.
Ajustement à l'adversaire : aucun, faute de données ; un seul test.

### Blessés et plan B
Aucun blessé. Pas de blessure en amical [M§1.2]. Plan B : sans objet.

### Évolution
Garde : composition et minutes du 23/11. Teste : agressivité 3. Conseil ajouté : **C-133** (`outputs/basketvibe/learnings.md`). Aucun levier « interdit » redonné. Aucun achat, vente ni enchère proposé.

Anticipation : sans objet (amical).
