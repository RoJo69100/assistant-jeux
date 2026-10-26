# Lecteur d'exports BasketVibe — 2026-10-26, 22:10 Paris

Export lu : `bronze.raw_pages`, 20:08:29 à 20:09:32 UTC (29 lignes : match 12, friendly 11, notifications 3, training 2, academy 1). Résultats via `my_result`.

## 1. Catégories
| Catégorie | N | Lu par silver ? | Ce qu'on en tire |
|---|---|---|---|
| Match de ligue J22 (détail, play-by-play, 4 stats par période, focus défensif adverse) | 8 (page `match`) | Oui : `bv_matches` (W 125-80), `bv_match_player_stats`, `bv_match_events` (830 événements pour les 2 matchs), `bv_match_tactics`. **Pas à jour : `bv_fixtures` garde J22 « scheduled », sans score** | Voir §2 |
| Amical Debrecen Ravens (idem) | 8 (page `friendly`) | Oui : `bv_matches` (L 73-93) | Voir §2 |
| Tactique / presets (2 presets, effectif de 16, depth chart) | 2 (une par page) | Non lu (pas de fixture_id ; aucune table silver pour les presets) | §3 |
| Entraînement : réglages (API) + HTML | 2 | API oui (`bv_player_training`, 16 joueurs, 26/10 20:09) ; HTML Progress / Recent changes non (`bv_training_changes` s'arrête au 18/10) | §4 |
| « Academy » : en fait finances (solde, journal) | 1 | Oui (`bv_finance_seasons` 26/10, `bv_finance_transactions` 26/10 19:48). **Aucune offre ni rapport d'académie** | §5 |
| Notifications (liste, liste complète, classement) | 3 | Classement oui (`bv_standings_weekly` 26/10) ; notifications seulement dans `bv_api` | §6 |
| Profil, non lus, ligue, HTML | 5 (profil x2, `unread_count`, ligue x2, HTML x2 : classés match/friendly) | Sans objet | rien |

## 2. Matchs (valeurs lues, `my_result`)
| Match | Résultat | Quarts (nous-eux) | Tirs / 3 pts / LF | Rebonds | Pertes | Homme du match |
|---|---|---|---|---|---|---|
| J22, 26/10 20:00, domicile, Wolves Empire | **W 125-80** | 28-21, 35-26, 34-12, 28-21 | 53/96, 4/18, 15/17 | 52-32 (off. 19-10) | 15 contre 27 | A. Fournier : 14 pts, 13 reb, éval. 26 |
| Amical 26/10 08:00, domicile, Debrecen Ravens | **L 73-93** | 22-24, 20-26, 8-26, 23-17 | 29/87, 4/30, 11/20 | 48-55 | 13 contre 17 | M. Bernard : 6 pts, 24 reb, éval. 23 |

- J22 : Casadei (Wolves) blessé. Recette billets 260 000 (5 200 fans), amical 22 200 (444).
- Amical : le 3e quart (8-26) fait la défaite. Les cinq alignés diffèrent du preset « Friendly » enregistré en Q2 : O. Richard à la place de N. Boyer, et le 5e bloc (prolongation) S. Henry à la place de T. Bonnet.

## 3. Presets (brut, silver ne les lit pas)
- Presets : « League Tactic » (43d784f8) et « Friendly » (924952fc). Actifs : amical = Friendly, ligue = League Tactic, **coupe = League Tactic**.
- « Friendly » (contenu identique depuis l'export du 25/10 08:56 UTC) : Q1 Baron / Leclerc / Lecomte / Albano / Bernard ; Q2 Boyer / Leclerc / Lecomte / Klein / Bernard ; Q3 Baron / Henry / Lecomte / Albano / Bernard ; Q4 Baron / Leclerc / Henry / Albano / Klein ; Q5 Richard / Bonnet / Gimenez / Lefebvre / Fournier. `defense_tier` 0 pour tous sauf Dang et Albano (2).
- **Le preset de l'amical New Generation (mardi 27/10, coup d'envoi 08:00, limite 07:45) : le preset « Friendly » est sauvegardé et actif, mais ce n'est pas une preuve qu'il est appliqué à ce match.** Les pages 26/10 n'ont pas de `fixture_id`. Le dernier Schedule exporté (25/10 08:56 UTC) montrait « Tactics - » (aucune tactique) pour New Generation, Mallorca Waves (28/10), MACCABI (coupe) et BC Calije (31/10) ; `gold.bv_agenda` dit « aucun plan sauvegardé » à partir de cet export. **Réponse : sauvegardé en preset, non confirmé sur le match.**

## 4. Entraînement : le 25/10 est-il réglé ?
- Brief 25/10 (« déjà saisi ») et registre (« exporté, PAS réglé », déclaré 09:15) ne se contredisent pas : le registre dit que l'utilisateur n'a rien modifié ; le brief dit que les 17 réglages préexistants étaient à garder. L'export du 25/10 07:44 UTC et celui du 26/10 20:09 UTC sont **identiques sur les 16 joueurs** ; seul Fontaine (30 ans, renvoyé) a disparu. Les 16 couples principale / secondaire correspondent un à un au tableau du brief Entraînement du 25/10 : **réglé, rien à saisir** pour le run du dim. 01/11 03:00 Paris.
- Réglages actuels (principale / secondaire) : Baron Passes/Déf · Boyer Passes/Dribble · Richard Passes/Déf · Bonnet Déf/Dribble · Dang 3 pts/Déf · Henry 3 pts/2 pts · Leclerc 3 pts/Déf · Durand 2 pts/Déf · Gimenez 2 pts/3 pts · Lecomte Déf/Athl · Albano Rebond/Déf · Lefebvre Déf/Athl · Legrand Rebond/Déf · Bernard Rebond/Athl · Fournier Rebond/Déf · Klein Rebond/Déf. Compétences : par ex. Bonnet 78 en 2 pts, 72 en 3 pts ; Gimenez 75 en défense.

## 5. « Academy » (page de finances)
- Solde 1 105 193 ; salaires hebdo 316 923 ; investissement académie 100 000 ; personnel médical 60 000 ; popularité 0,67 ; saison 1 : solde 933 845 (billets ligue 2 740 000, sponsor 956 400, salaires 1 961 805, académie 925 000).
- **Aucune offre U18 ni rapport de scout dans cet export.** Dernier rapport en base : 22/10 07:00 UTC (score académie 45 → 59, `bv_academy_candidates` : 6 candidats). Prochain : jeudi 29/10 09:00. Il ne manque rien avant.

## 6. Notifications et classement final
- Lues : match_finished J22 (W) ; friendly_finished Debrecen (L) ; friendly_scheduled : New Generation (27/10), baker street (04/11, extérieur), Statyba Telsiai (29/10), Afacian (30/10), HAVEX (05/11) ; `training_resolved` du 25/10 (13 améliorés, Bernard rebond +2) ; sponsor 100 000 (25/10).
- **Classement final saison 1 : Chomelix Cow 8e, 10 victoires - 12 défaites, 32 points, 2164-2231 (-67)**. Forme : W W W L W. 7e Mind Readers 33 pts, 9e Wolves Empire 28 pts (6-16), 1er KK Uola 22-0, 12e San pancrazio 1-21. Force de club : Chomelix Cow 53,6 ; `league_hardiness` 54,5.

## 7. Classement erroné du script
| page_type | Contient aussi | Critère |
|---|---|---|
| `match` / `friendly` | profil (`club_id`), `unread_count`, ligue, play-by-play, stats par période, tactique du match, presets, HTML | `body.kind`+`quarter_scores` = détail ; `play_by_play` ; `period`+`players` ; `defensive_focus` ; `presets` ; `text`+`tables` = HTML |
| `academy` | **finances**, pas d'académie | `body.balance` + `recent_transactions`. Une vraie page académie a `candidates` / `scout_report` |
| `notifications` | liste de notifications (x2) et **classement** | `body.standings` = classement ; `body.notifications` = liste |
| `training` | API (`skills`, `players`) et HTML | `body.players` ou `text` |

## 8. Reste à exporter
- **Schedule** (écran Schedule du menu Club) : voir si « Tactics ✓ » apparaît pour New Generation (27/10), Mallorca Waves (28/10) et MACCABI (coupe 28/10). Avant 07:45 mardi.
- Effectif, onglet **Tiles** (mardi 27/10, après +1 an) : salaires par joueur (déjà noté au brief Finances 25/10).
- Rien d'autre : entraînement, académie, classement et matchs sont en base.
- Nouveautés ajoutées à `docs/fiches/basketvibe/commun.md` (section « Options observées ») : presets actifs (la coupe prend League Tactic), tiers de consignes (`role`, `shot`, `offensive_focus`), `possessions_per_quarter_n`, `club_strength`, `injuries`, champs « manager », finances médicales (60 000 affichés contre 85 000 prélevés le 25/10).
