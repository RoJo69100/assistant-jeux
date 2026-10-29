# Team Soccer — brief Tactique du 2026-10-29 (Ben Ahmed Donkey uniquement)

Briefs amont lus : Match du 29/10 (C-018/C-041/C-045), Tactique Cows (format). Données : `gold.ts_upcoming` (match 2080331), `gold.ts_saisie_composition`, `silver.ts_players` (équipe 15858, jour 2026-10-29, export 13:06 UTC), `silver.ts_lineups` (défaut du 23/10). Règles : fiche tactique, skill teamsoccer-match.

## Actions
| Priorité | Action | Heure limite |
|---|---|---|
| 🟥 URGENT | Enregistrer la composition ci-dessous (Ben Ahmed Donkey à l'extérieur contre BOT 60, nous 63,7, ligue, match 2080331) | **17:30 Paris aujourd'hui** (`lineup_deadline_paris`), `lineup_saved` = false ; match 19:30 |
| 🟥 URGENT | Aucun remplacement programmé (supprimer les 3 changements à 60' de la composition par défaut du 23/10) | idem |
| 🟧 IMPORTANT | Après l'enregistrement : exporter la page « Compositions » (onglet Avancé inclus) avec le script | ce soir |

## Saisie : 1-4-4-2 · style Neutre · aucun remplacement programmé
Pourquoi : bot (Neutre, compétences réduites), même formation que la composition par défaut ; deux changements seulement : García titulaire (Défense 90 × Forme 100 = 90,0 contre Girard 77 × 0,946 = 72,8, `ts_saisie_composition`) et suppression des remplacements (C-018/C-041).

| Empl. | Joueuse (id) | Rôle | Compétence clé | Forme |
|---|---|---|---|---|
| 0 | Chae Abdel (288411) | GB | Gardien 81 | 82 |
| 1 | Yuki Fernández (288410) | latérale | Défense 83 | 82 |
| 2 | Zainab García (297342) | centrale | Défense 90 (Contrôle 20) | 100 |
| 3 | Anna Fournier (288423) | centrale | Défense 79 | 82 |
| 4 | Nour Taylor (288413) | latérale | Défense 79 | 82 |
| 5 | Momoka Martínez (288419) | milieu côté | Centres 81, Conduite 62 | 82 |
| 6 | Ama Schmidt (288408) | milieu central | Passe 84 | 82 |
| 7 | Uchenna Kumar (288421) | milieu central | Centres 79, Conduite 62 | 82 |
| 8 | Oluwaseun Mansour (288420) | milieu côté | Centres 81, Conduite 62 | 82 |
| 9 | Juliette Yamamoto (288418) | avant-centre | Finition 87 | 82 |
| 10 | Marie Müller (288417) | avant-centre | Finition 88 | 82 |

Ordre 5-6-7-8 et 1-4 repris de la composition par défaut du 23/10 (`silver.ts_lineups`).

**Banc (6)** : 1 Rania Fournier (296386, GB, Gardien 71, Forme 96) · 2 Kavya Hayashi (288415, DC, Défense 72) · 3 Salma Girard (288414, DC, Défense 77) · 4 Lena Suzuki (288409, couvre le milieu, Passe 81) · 5 Adaeze Wilson (288422, attaquante, Passe 80, 1 jaune) · 6 Ingrid Shimizu (288424, attaquante, Passe 77).

## Consignes par joueuse × 5 zones (convention fiche : action = meilleure compétence ; 60 partout = passer)
| Joueuse | Ultra défensive | Défensive | Médiane | Offensive | Finition |
|---|---|---|---|---|---|
| Abdel (GB) | dégager | — | — | — | — |
| Fernández (lat.) | dégager | passer (milieux) | passer | passer | — |
| García (DC) | dégager | passer (milieux) | passer (milieux) | passer | — |
| A. Fournier (DC) | dégager | passer (milieux) | passer (milieux) | passer | — |
| Taylor (lat.) | dégager | passer (milieux) | passer | passer | — |
| Martínez (côté) | passer | passer | dribbler (62 > 60) | centrer vers attaquants (81) | tirer |
| Schmidt (central) | passer | passer | passer (84) | passer vers attaquants | tirer |
| Kumar (central) | passer | passer | dribbler (62 > 60) | passer vers attaquants | tirer |
| Mansour (côté) | passer | passer | dribbler (62 > 60) | centrer vers attaquants (81) | tirer |
| J. Yamamoto (att.) | passer | passer | passer | dribbler puis tirer | tirer |
| Müller (att.) | passer | passer | passer | dribbler puis tirer | tirer |

Latérales : Centres et Conduite à 60, donc passer (règle de départage de la fiche) ; le défaut du 23/10 faisait dribbler/centrer, c'est la variable testée en moins. Kumar central : Centres 79 mais un milieu central passe vers l'attaquant (fiche) ; hypothèse, à confirmer.

## Adversaire
BOT, note 60 (`ts_upcoming`), tactique inconnue. Pas de focus défensif dans Team Soccer ; seul levier défensif = style, laissé Neutre. Bot : pénalité Gardien/Finition −10/−18/−25 % selon l'écart [connaissance 6.3] : notre écart de 3,7 donne le palier bas, pas de gain à forcer.

## Plan B
Blessure : remplacement automatique par le couvreur. Abdel sortie : Rania Fournier. Une centrale : Girard puis Hayashi. Un milieu : Suzuki. Une attaquante : Wilson (Finition 60, Passe 80) puis Shimizu. Aucun joueur blessé ni suspendu (SQL 29/10), 1 jaune (Wilson, banc).

## Contrôle SQL (`silver.ts_players` 29/10)
11 titulaires distincts, 6 remplaçants distincts sans doublon avec le onze, 0 blessée, 0 suspendue, talent NULL pour toutes.

## Test (C-048, confiance faible)
Pari : García (Contrôle 20) en centrale et Schmidt milieu central tiennent contre un bot 60. **Ce qui prouvera que j'avais tort** : après le match du 29/10 19:30, `ts_match_report` : plus de 1 but encaissé, ou `silver.ts_match_lineups` 2080331 sans formation 1-4-4-2 ; alors García retourne au banc et Girard titulaire. Aussi C-045 : Müller ≥ 2 tirs.
