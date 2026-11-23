Amical contre Milano Jazz (22/11)
Verrou : dim. 22/11 07:45 (match 08:00)
Adversaire : Milano Jazz (joueurs inconnus)
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
| Baron | PG | PG | — | PG | PG | PG | 36 (+5) | 3 | 3 | 3 | 5 |
| Boyer | PG | SF | PG | SF | — | SG | 36 (+5) | 3 | 3 | 3 | 5 |
| Richard | PG | — | — | — | — | — | 0 | 3 | 3 | 3 | 5 |
| Bonnet | SG | — | — | — | — | — | 0 | 3 | 3 | 3 | 5 |
| Leclerc | SG | SG | SF | SG | — | — | 36 | 3 | 3 | 3 | 5 |
| Durand | SF | — | SG | — | SG | SF | 24 (+5) | 3 | 3 | 3 | 5 |
| Gimenez | SF | — | — | — | — | — | 0 | 3 | 3 | 3 | 5 |
| Albano | PF | — | PF | C | SF | C | 36 (+5) | 3 | 3 | 3 | 5 |
| Lefebvre | PF | — | — | — | — | — | 0 | 3 | 3 | 3 | 5 |
| Legrand | PF | PF | — | PF | PF | PF | 36 (+5) | 3 | 3 | 3 | 5 |
| Bernard | C | C | C | — | C | — | 36 | 3 | 3 | 3 | 5 |
| Fournier | C | — | — | — | — | — | 0 | 3 | 3 | 3 | 5 |
### Écran 3 — Adversaires
| Adversaire | Poste | Focus défensif (1-5) | Zone |
|---|---|---|---|
| Les 12 | tous | 3 (Normal) | Perimeter (1) |
## Après sauvegarde, vérifie
- [ ] Agress. = 5 pour chacun des 12 joueurs
- [ ] Off. focus = 3, Rôle = 3, Tir = 3 pour les 12 joueurs
- [ ] Durand : Min = 24
- [ ] Les 12 adversaires : focus 3, zone Perimeter (1)
## À exporter ensuite
La page du match, après la fin du match (~08:55 le 22/11) : elle donnera les noms adverses.

---
## Annexe — pourquoi

Saisie AUJOURD'HUI vendredi 20/11 (heure Paris 14:15, `pipelines/heure_paris.py`) pour l'amical du 22/11 08:00. Amical : pas de preset, moteur v5, fatigue et expérience ≈ 1/10, pas de blessure [M§1.2]. Consigne : un seul test, E1 niveau B (`docs/attentes/experiences-amicales-basketvibe.yaml`), agressivité 5 à l'écran (cran 4) pour les 12 joueurs, y compris ceux à 0 min ; tout le reste au neutre.

### Réglage neutre (yaml `neutre` + constants E1)
Zone Perimeter (1), focus défensif 3 sur les adversaires, Off. focus 3 (aucun Primary), aucun Tir cran 4 (Tir 3 écran = cran 2). Rôle 3 et Tir 3 : le yaml ne fixe pas de neutre pour ces deux colonnes, je prends l'écran 3 pour qu'aucune autre variable ne bouge. Seule l'agressivité (5) diffère du neutre, par construction du test ; aucune valeur isolée.

### Composition (7 joueurs, choisie à l'instant T)
Jeunes d'abord [M§5.4] (Baron 17, Boyer 20, Leclerc 17, Bernard 18 : 144 min sur 240). Titulaires de ligue protégés : J9 samedi 21/11 20:00 puis J10 lundi 23/11 20:00 (`gold.bv_agenda`) ; Gimenez, Lefebvre, Richard, Bonnet, Fournier à 0 min. Minutes : Baron, Boyer, Leclerc, Bernard, Legrand, Albano 36 ; Durand 24 ; total 240. Sept joueurs pour cinq emplacements : Legrand et Albano à 36 min. Même cinq que l'amical du 21/11 : le seul changement du test est l'agressivité, rien d'autre ne bouge. Remplaçants (depth chart) : aucun programmé ; hors jeu si besoin : Lefebvre (PF/C), Fournier (C), Richard (PG), Gimenez (SF), Bonnet (SG).

### Contrôle SQL (fait : plan en `values` joint à `gold.bv_slot_fit`)
- 5 joueurs différents, un par emplacement, par quart : oui (20 lignes Q1–Q4, plus la prolongation).
- Maximum 3 quarts par joueur : oui (6 joueurs à 3, Durand à 2) ; aucun `over_36` hors prolongation.
- `height_eff` ≥ 95 : oui, minimum 98,4 (Leclerc SG) ; Boyer 99,2.
- `fit_with_form` moyen : Legrand 52,9, Bernard 50,0, Albano 49,1, Boyer 49,0, Baron 45,1, Durand 44,2, Leclerc 41,7 (le plus bas : seul SG/SF jeune disponible, amical de formation).
- Forme : relevé du 20/11 (`gold.bv_roster_now.day`, semaine du 15/11), postérieur au dimanche 15/11 : à jour. Baron 6, Leclerc 5, Durand 5 sous 7 [M§5.5] ; ils restent pour le temps de jeu des jeunes.
- Blessés : aucun (`injury_return_on` vide pour les 12), aucun en vente. Plan B : pas de blessure en amical [M§1.2] ; hors jeu ci-dessus.
- Fatigue (`gold.bv_roster_now`) : les 7 joueurs ≤ 15,1 (Boyer 15,1, Bernard 13,6, Legrand 13,1, Durand 8,8). Le surcoût du cran 4 n'est pas dans une vue : non mesuré. Ces 7 ne sont pas le cinq de ligue de J10.

### Adversaire : Milano Jazz
`gold.bv_saisie_adversaires` : aucune ligne pour lui ; `gold.bv_match_report` : aucun match contre lui. Joueurs, parts de tirs, 2P/3P inconnus ; amical : aucun aperçu à demander (résumé BasketVibe).
**Focus défensif** : aucun joueur adverse connu, donc Normal (3) sur les 12, zone Perimeter (neutre E1), aucun Intense, Light ni Give up. Export à faire : la page du match après ~08:55 le 22/11 (noms adverses).
Ajustement à l'adversaire : aucun, faute de données ; un seul test (agressivité).

### Test E1 niveau B et lecture
`gold.bv_amical_reglage` : le 18/11 (Union Heidelberg, cran 2, L) et le 19/11 (BG Bangers, cran 2, L) sont des niveaux A ; le 20/11 (FuzzyTeam) et le 21/11 (Ironmasters) sont déjà prévus au cran 4 (C-128, C-129) : le 22/11 fait un 3e niveau B de suite, alors que l'ordre du yaml est A, B, A, B. Écart signalé, non tranché ici : réglage demandé appliqué. Série cran 2 : 18/11 L −22, `opp_fg2_pct` 78,0, `pf` 22 (`gold.bv_match_report`). Anciens crans 4 (21 et 23/10, L-011) : `pf` 20 puis 27, eFG adverse 59,1 puis 60,7. Hypothèse (confiance faible) : `pf` et `o_fta` montent sans baisse de `opp_fg2_pct` [M§6.3]. Lecture le 22/11 après export : `opp_fg2_pct`, `pf`, `o_fta`, points encaissés contre la série cran 2.
Conseil ajouté : **C-130** (`outputs/basketvibe/learnings.md`). Aucun levier « interdit » redonné. Aucun achat, vente ni enchère proposé.
