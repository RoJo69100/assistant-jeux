Amical contre FuzzyTeam (20/11)
Verrou : ven. 20/11 07:45 (match 08:00)
Adversaire : FuzzyTeam (joueurs inconnus)
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
La page du match, après la fin du match (~08:55) : elle donnera les noms adverses.

---
## Annexe — pourquoi

Saisie AUJOURD'HUI jeudi 19/11 (heure Paris 10:41, `pipelines/heure_paris.py`) pour l'amical de demain 20/11 08:00. Amical : pas de preset, moteur v5, fatigue et expérience ≈ 1/10, pas de blessure [M§1.2]. Ta consigne : un seul test, E1 niveau B (`docs/attentes/experiences-amicales-basketvibe.yaml`), agressivité 5 à l'écran (cran 4) pour les 12 joueurs, y compris ceux à 0 min ; tout le reste au neutre.

### Réglage neutre (yaml `neutre` + constants E1)
Zone Perimeter (1), focus défensif 3 sur les adversaires, Off. focus 3 (aucun Primary), aucun Tir cran 4 (Tir 3 écran = cran 2). Rôle 3 et Tir 3 pour tous : le yaml ne fixe pas de neutre pour ces deux colonnes, je prends l'écran 3 (équilibré) pour qu'aucune autre variable ne bouge. Cela écarte les valeurs du 17/11 (Tir 1 ou 2, Off. focus 2 ou 4, Rôle 1 ou 4) : elles étaient des choix, pas le neutre. Zone : Perimeter, pas Middle comme le 19/11, car Perimeter est le neutre et la constante E1 ; L-027 range Middle comme la pire zone en amical (2 matchs).

### Composition (choisie à l'instant T, 7 joueurs utilisés)
Le cinq par quart reprend la logique du 17/11 (jeunes d'abord [M§5.4], titulaires de ligue protégés : ligue J9 samedi 21/11 20:00, `gold.bv_agenda`). Gimenez, Lefebvre, Richard, Bonnet, Fournier : 0 min. Minutes : Baron, Boyer, Leclerc, Bernard, Legrand, Albano 36 ; Durand 24 ; total 240. Jeunes ≤ 21 ans (Baron 17, Boyer 20, Leclerc 17, Bernard 18) : 144 min sur 240. 7 joueurs pour 5 emplacements : c'est ce qui force Legrand et Albano à 36 min.
Remplaçants (depth chart) : aucun programmé ; hors jeu en cas de besoin : Lefebvre (PF/C), Fournier (C), Richard (PG), Gimenez (SF), Bonnet (SG).

### Contrôle SQL (fait, `gold.bv_slot_fit`)
- 5 joueurs différents et 5 emplacements par quart : oui (`values` du plan : 20 lignes).
- Maximum 3 quarts par joueur : oui (6 joueurs à 3 quarts, Durand à 2) ; aucun `over_36` hors prolongation.
- `height_eff` ≥ 95 : oui, minimum 98,4 (Leclerc SF).
- `fit_with_form` moyen : Legrand 53,1, Bernard 50,2, Albano 49,3, Boyer 49,1, Baron 45,3, Durand 44,4, Leclerc 41,9 (le plus bas, seul SG/SF jeune dispo, amical de formation).
- Forme : relevé du 17/11 (`gold.bv_roster_now.day`, semaine du 15/11), postérieur au dernier dimanche 15/11 : à jour. Baron 6, Leclerc 5 et Durand 5 sont sous 7 [M§5.5] ; ils restent pour le temps de jeu des jeunes.
- Blessés : aucun (`injury_return_on` vide pour les 12) ; aucun en vente (`on_transfer_list` faux). Plan B : aucun blessé en amical possible [M§1.2].
- Fatigue actuelle (zone verte ≤ 20) : Bonnet 21,08 (0 min), les autres 1,36 à 15,72. Agressivité cran 4 : le multiplicateur d'amical n'est pas dans une vue ; `gold.bv_fatigue_plan` (ligue, tier 4, 36 min) donne 34,5 à 42,6 stabilisé, soit ≈ 3,5 à 4,3 pour un amical au dixième. Ce surcoût arrive avant J9 (21/11) pour les 7 joueurs du test, tous hors cinq de ligue ; ordre de grandeur, non mesuré en amical.

### Adversaire : FuzzyTeam
`gold.bv_saisie_adversaires` : 0 ligne ; `gold.bv_match_player_lines` : aucun match contre lui ; absent de `gold.bv_next_opponents` (ligue seulement). Joueurs, parts de tirs et 2P/3P inconnus.
**Focus défensif** : aucun joueur adverse connu, donc Normal (3) sur les 12, zone Perimeter, aucun Intense, Light ni Give up. Export à faire : la page du match après ~08:55 le 20/11. Un seul test (agressivité), le focus reste neutre.

### Test E1 niveau B et lecture
Dernier niveau B : aucun amical de la file en cran 4 depuis `debut` 2026-11-10 dans les relevés lus ; le 18/11 (Union Heidelberg, saisie agress. 3) : L −22, `opp_fg2_pct` 78,0, `opp_efg_pct` 67,1, `pf` 22 ; les 12–17/11 : `opp_fg2_pct` 49,0–58,0, `pf` 13–19 (`gold.bv_match_report`). Le résultat de BG Bangers (19/11 08:00) n'est pas encore exporté : donnée absente, export de la page du match à faire pour le verdict E1:A. Anciens crans 4 (amicaux 21 et 23/10, L-011) : FT rate adverse 36,4 puis 44,0, eFG adverse 59,1 puis 60,7, `pf` 20 puis 27 ; le manuel annonce plus de fautes et un meilleur contest au cran haut [M§6.3]. Hypothèse (confiance faible, n=2 en v4/v5 différents) : `pf` et `o_fta` montent sans baisse de `opp_fg2_pct`. Lecture le 20/11 après export : `opp_fg2_pct`, `pf`, `o_fta`, points encaissés contre la série cran 2.
Conseil ajouté : **C-128** dans `outputs/basketvibe/learnings.md`. Aucun levier « interdit » redonné ; l'agressivité de ligue n'est pas touchée (hors périmètre).
Aucun achat, vente ni enchère proposé.
