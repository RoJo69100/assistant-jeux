Amical contre BG Bangers (19/11)
Verrou : jeu. 19/11 07:45 (match 08:00)
Adversaire : BG Bangers (joueurs inconnus)
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
| Baron | PG | PG | — | PG | PG | PG | 36 (+5) | 2 | 1 | 2 | 3 |
| Boyer | PG | SF | PG | SF | — | SG | 36 (+5) | 4 | 3 | 2 | 3 |
| Richard | PG | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Bonnet | SG | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Leclerc | SG | SG | SF | SG | — | — | 36 | 3 | 3 | 2 | 3 |
| Durand | SF | — | SG | — | SG | SF | 24 (+5) | 3 | 3 | 2 | 3 |
| Gimenez | SF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Albano | PF | — | PF | C | SF | C | 36 (+5) | 3 | 4 | 1 | 3 |
| Lefebvre | PF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Legrand | PF | PF | — | PF | PF | PF | 36 (+5) | 4 | 4 | 1 | 3 |
| Bernard | C | C | C | — | C | — | 36 | 3 | 3 | 1 | 3 |
| Fournier | C | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
### Écran 3 — Adversaires
| Adversaire | Poste | Focus défensif (1-5) | Zone |
|---|---|---|---|
| Les 12 | tous | 3 (Normal) | Middle (3) |
## Après sauvegarde, vérifie
- [ ] Agress. = 3 pour chacun des 12 joueurs
- [ ] Boyer : Tir = 2
- [ ] Durand : Min = 24
- [ ] Les 12 adversaires : focus 3, zone Middle (3)
## À exporter ensuite
La page du match, après la fin du match (~08:55) : elle donnera les noms adverses.

---
## Annexe — pourquoi

Saisie AUJOURD'HUI mardi 17/11 (heure Paris 11:06, `pipelines/heure_paris.py`), match jeudi 19/11 08:00, verrou 07:45. Amical : pas de preset, moteur v5, fatigue et expérience ≈ 1/10, pas de blessure [M§1.2]. Entrées lues : brief analyste du 17/11 (points d'amical seulement), `learnings.md`, brief tactique amical du 13/11 (le plus récent).

### Action (ancienne section « Action : fais X »)
Sur la page du match d'amical contre BG Bangers : saisis la composition, **agressivité 3 (écran, cran 2 « équilibrée ») pour les 12 joueurs de l'effectif**, zone Middle (3) et focus 3 sur les 12 adversaires (un seul test : E1), puis sauvegarde. **Vérifie à l'écran après sauvegarde que la colonne Agress. affiche 3 pour chaque joueur** : le test n'a eu lieu que le 14/11 (`defense_tier` 2 pour les 9 joueurs, `gold.bv_match_player_lines`). Les amicaux du 15/11 et du 16/11 sont repartis à `defense_tier` 0 (Albano seul à 2). Après le match (~08:55), exporte la page du match : l'export donnera les noms adverses.

Calendrier lu en SQL (`gold.bv_next_opponents`, `gold.bv_agenda`) : ligue J8 à C.B.Granada **mercredi 18/11 20:00** (verrou 19:45) ; la ligue suivante est J9 **samedi 21/11** (Águias do Guadiana, dom.), pas le 20/11 : le 20/11 est un amical (FuzzyTeam). Écart avec ton énoncé signalé. Les titulaires de ligue ne jouent pas ce match : l'amical du 19/11 vient après J8 et ajoute sa fatigue avant J9.

Brief analyste du 17/11, points qui concernent un amical : Durand 24 min maximum (point 2) et Bernard au C de départ (point 5) sont appliqués ; les points de ligue (preset à sauvegarder, Dang/Richard/Bonnet, Intense sur Granada) sont hors périmètre.

### Composition (écran 1)
Remplaçants : aucun programmé (7 joueurs sur le terrain, aucun joueur supplémentaire). Gimenez, Lefebvre, Richard, Bonnet, Fournier : 0 minute (titulaires de ligue protégés pour J9 du 21/11).

### Tableau de saisie (écran 2, 1-5, ordre de l'écran)
Âges : Baron 17 ans, Boyer 20 ans, Leclerc 17 ans, Bernard 18 ans.

Dans les colonnes Q, la valeur est l'emplacement tenu (Boyer : SF Q1 et Q3, PG Q2). (+5) = prolongation éventuelle. Dang et Ungureanu n'apparaissent plus dans `gold.bv_roster_now` (relevé du 16/11, 12 joueurs) : pas de ligne.

Minutes : Baron 36 + Boyer 36 + Leclerc 36 + Bernard 36 + Legrand 36 + Albano 36 + Durand 24 = 240. Jeunes ≤ 21 ans (Baron 17, Boyer 20, Leclerc 17, Bernard 18) : 144 min sur 240 (60 %), 36 chacun, aucun au-delà. Ordre des objectifs : jeunes d'abord, test E1 ensuite, titulaires de ligue protégés. 7 joueurs seulement pour 5 emplacements : c'est ce qui force Legrand et Albano à 36 ; la prolongation ferait dépasser 36 min (hypothèse rare, cinq choisi parmi les moins fatigués).

Valeurs qui s'écartent du neutre (3) ou de la règle uniforme, avec leur raison (lecture `gold.bv_match_player_lines`, amicaux + ligue depuis le 27/10, 3PA = part des tirs à 3 pts, réussite à 3 pts, réussite à 2 pts) :
- Agressivité 3 partout au lieu de 1 (L-004) : test E1, seul réglage défensif modifié, même cran pour tous (y compris 0 min).
- Tir 2 (2 pts favorisés) : Leclerc (64 % à 3 pts tentés, 26 % réussis, 2P 54 %), Baron (44 %, 31 %, 2P 52 %), Durand (42 %, 27 %, 2P 52 %), **Boyer** (47 %, 33 %, 2P 64 % : 0,99 pt par tir à 3 contre 1,28 à 2 ; passe de 3 à 2 par rapport au 13/11).
- Tir 1 : Albano (43 %, 23 %, 2P 55 %), Legrand (13 %, 29 %, 2P 52 %), Bernard (8 %, 27 %, 2P 51 %). Variable secondaire (offensive), ne change pas la lecture défensive du test.
- Rôle 1 Baron (meilleure passe du banc jeune) ; Rôle 4 Albano et Legrand (intérieurs, 2P 55 % / 52 %). Off. focus 4 Legrand et Boyer, 2 Baron : reprise du 13/11, faibles parts de tirs de Baron (82 tirs).
- Les 5 hors jeu (0 min) : 3 partout, sans effet.

### Adversaires (écran 3) : BG Bangers
Joueurs adverses inconnus : `gold.bv_saisie_adversaires` n'a aucune ligne pour BG Bangers, ni match passé en base (`gold.bv_match_report`) ; adversaire absent de `gold.bv_next_opponents` (ligue seulement). Ligne du tableau : les 12 (noms inconnus, export à faire). Focus neutre, zone Middle (comme le test du 14/11, pour garder E1 comparable). Export à faire : la page du match après ~08:55, qui donnera la liste et les scoreurs.

### Focus défensif (section obligatoire)
Aucun joueur adverse connu : pas de parts de tirs ni de 2P/3P (`gold.bv_match_opp_focus` n'a rien pour cet adversaire). Normal sur les 12, Middle, aucun Intense ni Give up faute de données. Un seul test à la fois : E1 (agressivité) ; zone et focus restent neutres. L-027 range Middle comme la pire zone mesurée en amical (2 matchs, adversaires biaisés) : on la garde exprès pour isoler E1.

### Contrôle SQL (fait)
- 5 joueurs différents par quart-temps, un par emplacement : oui (`values` du plan, 5 lignes / 5 joueurs / 5 emplacements aux 4 quarts).
- Maximum 36 min (hors prolongation éventuelle) : oui, 6 joueurs à 3 quarts, Durand à 2 ; aucun `over_36`.
- `height_eff` ≥ 95 sur chaque emplacement : oui (minimum 98,4, Leclerc SF), `gold.bv_slot_fit`.
- `fit_with_form` moyen par joueur : Legrand 52,9, Bernard 50,0, Albano 49,1, Boyer 49,0, Baron 45,1, Durand 44,2, Leclerc 41,7 (Leclerc au SF : 41,0, le plus bas ; seul SG/SF jeune disponible, amical de formation). Forme : relevé du 16/11 (semaine 15/11), postérieur au dernier dimanche 15/11 : à jour.
- Blessés : aucun (`injury_return_on` vide pour les 12 ; Gimenez de retour).
- Fatigue actuelle (zone verte ≤ 20) : Durand 8,96, Legrand 8,55, Boyer 7,29, Bernard 6,03, Baron 1,69, Albano 1,45, Leclerc 1,42. Fatigue ajoutée par l'amical (minutes × 0,019 × 1,0 × (1,5 − 0,008 × endurance), multiplicateur du cran 3 supposé 1,0) : Baron 0,84, Bernard 0,83, Leclerc 0,77, Boyer 0,76, Legrand 0,70, Albano 0,70, Durand 0,47. Titulaires de ligue (Gimenez 10,48, Bonnet 13,94, Lefebvre 13,08, Fournier 13,13, Richard 12,60) : ajoutée 0.
- Vendus : aucun (`on_transfer_list` faux).

### Blessés et plan B
Aucun blessé au 16/11. Si Intense / Perimeter tombe sur Leclerc (hypothèse, aucune donnée sur les focus adverses) : Leclerc est à Off. focus 3, Tir 2 ; Boyer (Off. focus 4, 2P 64 %), Legrand (4) et Bernard sont sur le terrain à chacun de ses 3 quarts (Q1 : Boyer, Legrand, Bernard ; Q2 : Boyer, Albano, Bernard ; Q3 : Boyer, Legrand, Albano).

### Test unique et évolution
Test E1 niveau A : agressivité écran 3 au lieu de 1 (L-004). Constat à ce jour (`gold.bv_match_report`) : un seul amical joué au cran 2, le 14/11 (Artificial Instinct, W +2) : `opp_fg2_pct` 56,5, `opp_efg_pct` 51,2, `o_fta` 28 ; 4 amicaux à `defense_tier` 0 (12, 13, 15, 16/11) : 49,0 / 58,0 / 50,0 / 56,4 (moyenne 53,4), eFG adverse 48,8, `o_fta` 21 en moyenne. Pas de gain défensif visible à un match ; le manuel annonce plus de fautes au cran élevé, ici `o_fta` monte (28 contre 21). Adversaires différents, effectifs différents : bruit.
Lecture à la date du 19/11 : `opp_fg2_pct`, points encaissés (`gold.bv_match_report`) et `pf` (`gold.bv_match_player_lines`) contre la série à agressivité 1. Faux si les points encaissés ou les fautes montent sans baisse de `opp_fg2_pct`. Doute : un seul match de plus, adversaire inconnu. Conseil ajouté : **C-125** dans `outputs/basketvibe/learnings.md`. Aucun levier marqué « interdit » par un compteur n'est redonné : l'agressivité 1 de ligue n'est pas touchée (hors périmètre).
