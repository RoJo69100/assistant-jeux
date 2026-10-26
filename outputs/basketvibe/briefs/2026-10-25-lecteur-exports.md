# Lecteur d'exports BasketVibe, 2026-10-25 (exports 07:38 à 08:08 UTC, 129 lignes bronze)

## Résumé
1. Entraînement résolu le 25/10 à 02:00 UTC (notification `training_resolved` : 13 joueurs améliorés à l'écran, top = Maël Bernard rebond +2). Le relevé de 07:44 UTC le contient, silver le lit (`gold.bv_training_gains_exact`, semaine 2026-10-25).
2. Seul Fontaine (30 ans) ne gagne rien. Dang (29 ans) gagne 0,176 en 3PT et 0,088 en défense : facteur d'âge 0,12 contre 0,49 pour Albano (26 ans), soit le même rapport (0,176/0,75 = 0,235 ; 0,12/0,49 = 0,245).
3. Dang et Albano ont changé de réglage depuis le relevé du 24/10 20:10 UTC et le nouveau réglage a bien été appliqué par le jeu.
4. Aucun joueur blessé (`roster_injuries` : « No recorded injuries yet »). Âges inchangés depuis le 24/10.
5. Finances : solde 822 993, salaires hebdo 333 212 (292 692 le 18/10), personnel 60 000 (plafond 85 000, 0 marketeur).
6. Aucune enchère ni vente à nous en cours (107 enchères `live_standard` sur le marché, 6 pages) ; dernière annonce à nous = invendue le 22/10.
7. Amical du 25/10 : victoire 111-95 à l'extérieur contre Aquile La Spezia (`my_result` = W).
8. À venir : ligue J22 lun 26/10 20:00 contre Wolves Empire (domicile, chance estimée 53 %) ; amical lun 26/10 contre Debrecen Ravens ; Coupe FR mer 28/10 18:00 contre MACCABI (domicile, tactique non enregistrée).
9. Non lu par silver : match de coupe du 28/10, onglets Progress et Recent changes de l'entraînement, `estimated_chance`, `league_hardiness`.
10. Il ne manque aucun export pour l'entraînement ni l'effectif.

## 1. Catégories
| Catégorie | Nombre | Lu par silver ? | Ce qu'on en tire |
|---|---|---|---|
| Entraînement (réglage + compétences exactes) | 1 API + 1 DOM | Oui (`bv_player_training`, `gold.bv_training_gains_exact`, `gold.bv_potential_estimate`) | Gains et réglages, voir §2 |
| Effectif (forme, fatigue, PS) | 1 roster + copies dans `club` | Oui (`bv_player_daily`, `gold.bv_roster_now`) | 17 joueurs, voir §2 |
| Blessures | 1 DOM | Oui (vide) | Aucune blessure |
| Finances / transactions | 1 API + 1 DOM + copies | Oui (`bv_finance_*`, 42 transactions) | Solde 822 993 |
| Personnel | 1 API + 1 DOM | Oui (`bv_personnel_weekly`, semaine du 19/10) | 2 médecins, 4 kinés, 2 psychologues, 0 marketeur |
| Marché + historique global | 7 + 16 | Oui (`bv_transfer_auctions` 07:45, `bv_transfers` jusqu'à 06:53) | Aucune enchère à nous |
| News | 4 | Oui (`bv_news`) | Dernière : « Season break schedule » (24/10) |
| Notifications | 5 | Non, seulement dans `bv_api` | `training_resolved`, sponsor, coupe, annonce invendue |
| Matchs (1 terminé, 2 à venir) | 6 `match` + 15 `friendly` | Oui (`bv_matches`, `bv_match_tactics`) | Voir résumé 7 et 8 |
| Calendrier / classement | 4 `schedule` + copies dans `club` | Oui (`bv_fixtures`, `bv_standings_weekly`) sauf coupe | Coupe FR 28/10 absente de `bv_fixtures` et `bv_matches` |
| Annexes | 20 `club` + 2 `unknown` | Partiel (`bv_api`) | Voir §3 |

## 2. Joueur par joueur (réglage actuel = colonne P/S, écran du 25/10 07:44 UTC)
Gain = variation exacte du relevé du 24/10 20:10 au 25/10 07:44. PS, forme (F) et fatigue (Fat) : 24/10 → 25/10 (`bv_player_daily`).

| Joueur | Poste, âge | P / S | Gain P / gain S | PS | F | Fat |
|---|---|---|---|---|---|---|
| Bernard | C, 17 | Rebond / Athlé | +2,20 (61→63,2) / +1,10 | 46,3→46,8 | 4→5 | 17,9→16,5 |
| Fournier | C, 27 | Rebond / Déf | +0,57 / +0,29 | 52,2→52,3 | 4→4 | 15,4→13,3 |
| Klein | C, 28 | Rebond / Déf | +0,26 / +0,13 | 44,8 | 6→5 | 4,4→3,9 |
| Albano | PF, 26 | **Rebond / Déf** (était Déf / Athlé) | +0,75 (50,88→51,63) / +0,375 (53,25→53,63) | 47,3→47,5 | 3→4 | 5,4→5,1 |
| Lefebvre | PF, 28 | Déf / Athlé | +0,39 / +0,19 | 62,9→63,0 | 1→2 | 11,3→9,6 |
| Legrand | PF, 22 | Rebond / Déf | +1,30 / +0,65 | 48,5→48,8 | 5→4 | 15,2→13,2 |
| Baron | PG, 16 | Passes / Déf | +1,60 / +0,80 | 43,4→43,8 | 4→5 | 5,4→5,0 |
| Boyer | PG, 19 | Passes / Ball | +1,14 / +0,57 | 47,4→47,7 | 6→7 | 22,6→20,3 |
| Fontaine | PG, 30 | Passes / Déf | 0 / 0 | 43,6 | 7→6 | 1,2→0,5 |
| Richard | PG, 24 | Passes / Déf | +1,06 / +0,53 | 55,7→56,0 | 2→1 | 10,4→8,8 |
| Durand | SF, 24 | 2PT / Déf | +0,81 / +0,41 | 43,1→43,2 | 7→7 | 17,3→15,0 |
| Gimenez | SF, 25 | 2PT / 3PT | +0,82 / +0,41 | 59,5→59,7 | 4→3 | 12,7→10,9 |
| Lecomte | SF, 16 | Déf / Athlé | +1,15 / +0,58 | 37,6→37,9 | 3→3 | 2,3→2,4 |
| Bonnet | SG, 25 | Déf / Ball | +0,91 / +0,46 | 51,2→51,4 | 5→5 | 18,3→16,0 |
| **Dang** | SG, 29 | **3PT / Déf** (était Rebond / Passes) | +0,176 (44→44,18) / +0,088 (43→43,09) | 49,9 | 6→7 | 6,7→5,5 |
| Henry | SG, 26 | 3PT / 2PT | +0,50 / +0,25 | 42,0→42,1 | 6→6 | 6,8→6,1 |
| Leclerc | SG, 16 | 3PT / Déf | +1,60 / +0,80 | 41,2→41,6 | 4→3 | 1,8→1,9 |

- Silver : la colonne `training_primary` de `gold.bv_training_gains_exact` garde le réglage du relevé précédent (Albano « defense/athleticism », Dang « rebounding/passing »). Le `gain_rank` et la colonne `primary_skill` de `gold.bv_potential_estimate` sont justes. Potentiel estimé Albano 7 et Dang 7, confiance faible (âge interpolé).
- Dang : 29 ans, ce relevé est son dernier entraînement utile selon la fiche Entraînement (règle 4) ; la valeur de ce relevé est de 0,176.
- Les 16 ans (Baron, Leclerc, Lecomte) et Bernard (17) sont au facteur d'âge 1,00 : leur facteur changera au +1 an.

## 3. Classement erroné du script
| `page_type` | Contient aussi | Critère de correction |
|---|---|---|
| `club` (20) | roster, finance, classement, calendrier, coupe, amicaux, compteur de notifications | `page_url` = /club mais `body` a `players` (roster), `balance` (finance), `standings`, `cup_fixtures`, `friendlies`, `unread_count` |
| `notifications` (5) | classement (7 181 car.) | `body.standings` = classement ; `body.notifications` = notifications |
| `transfers` (8) | finance (8 170 car.) | `body.balance` = finance ; `body.auctions` = marché |
| `schedule` (4) | liste d'amicaux | `body.friendlies` = amicaux ; `body.fixtures` = ligue |
| `training` (3) | réponse `{marked: 1}` (56 car.) | `body.marked` = réponse d'enregistrement ; `body.players` = fiche entraînement |
| `friendly` (15) | profil club, ligue, play-by-play, lineups par quart | `body.play_by_play`, `body.period`, `body.seasons`, `body.club_id` = annexes |
| `match` (6) | uniquement aperçu et tactique d'un match à venir | pas de résultat : `fixture_status` = scheduled |
| `unknown` (2) | API /promote (parrainage) | sans intérêt pour le jeu |

## 4. Nouveautés (détail dans `docs/fiches/basketvibe/commun.md`, « Options observées »)
`estimated_chance` (53 % / 47 % pour J22), `league_hardiness` 54,4, focus défensif `off` (valeur jamais décrite), onglets Progress et Recent changes, préférence `hide_match_results_until_replay`, Coupe FR.

## 5. Reste à exporter
| Donnée | Écran |
|---|---|
| Match de Coupe FR du 28/10 (tactique non enregistrée, non lu par silver) | Ouvrir Schedule, onglet Cups, ou la page du match MACCABI avant le 28/10 18:00 |
| Onglet Recent changes de l'entraînement (dernier relevé silver : 18/10) | Training, onglet Recent changes ; non indispensable car `gold.bv_training_gains_exact` couvre la semaine |
