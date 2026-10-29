# Lecteur d'exports BasketVibe, 2026-10-29, export de 09:59-10:01 UTC (bronze.raw_pages 21298 à 21421)

## 1. Inventaire
| Catégorie | Nombre | Lu par silver ? | Ce qu'on en tire |
|---|---|---|---|
| Match de coupe Maccabi (28/10 18:00, API `cup-fixtures/e2e694ec`: détail, play-by-play, 4 period-box) | 6 (en `unknown`) | OUI en `silver.bv_api`, NON dans `bv_matches`, `bv_fixtures`, `bv_match_player_stats` (0 ligne) | Victoire 121-94, extraction ci-dessous |
| Amical Statyba 29/10 08:00 (`friendlies/95737791`) | 6 (en `friendly`) | Oui (145 lignes de stats) | Défaite 83-113, déjà connue |
| Amical Mallorca 28/10 | 0 détail | Non (aucune page de détail dans l'export, seulement la ligne du calendrier et la notification) | Défaite 111-124 (extérieur), pas de stats joueurs |
| Aperçu coupe PSG (`cup-fixtures/dc345bfb`: preview + match-tactics) | 2 (en `unknown`) | `bv_api` seulement, jamais dans les vues match | Voir §3 |
| Calendrier | 1 (`schedule`) | `bv_fixtures` ne contient ni la coupe ni PSG | Prochains matchs §4 |
| Notifications | 3 (`notifications`: classement, non-lues, liste de 118) | Oui (`bv_api`) | §5 |
| News | 1 (`news`) + 1 `unknown` (copie de l'écran) | `bv_news` 20 lignes, dernière 08:42 UTC (article du 28/10 : voir si lu) | Moteur v5 §5 |
| Joueur Ungureanu (5 appels `player`: historique de transferts, profil, enchère, entraînement, compétences) | 5 | `bv_players` et `gold.bv_roster_now` l'ont | Achat 21 250 $ confirmé (28/10 21:14 UTC, vendeur Free Agents) |
| Finances (`player` 21372 : mal classée), transferts, effectif, académie, entraînement, tactique | 2, 9+7, 2, 1, 1, 2 | Oui (`bv_api`) | Solde 1 086 893 $ |

## 2. Valeurs extraites du brut (silver ne les lit pas)
**Coupe, 28/10 18:00 Europe/Paris, Chomelix Cow (domicile) contre MACCABI, tour 1 : 121-94, résultat pour nous = V** (`result_revealed` vrai ; notification `cup_match_finished` won=true, `human_team_is_home`=true). Quart-temps nous/eux : 25-19, 43-27, 34-25, 19-23. Homme du match : Lefebvre (27 pts, 20 reb, éval 39).
Équipe (nous / Maccabi) : tirs 37/78 / 35/86 ; 3 pts 10/27 / 12/32 ; lancers 37/45 / 12/20 ; rebonds 51 (13 off.) / 40 (12 off.) ; passes 11 / 9 ; interceptions 10 / 12 ; contres 4 / 7 ; pertes 18 / 17 ; fautes 14 / 22. Victoire portée par les lancers (+25).
| Joueur | Poste | Min | Pts | Tirs | 3 pts | LF | Reb | Pd | Éval |
|---|---|---|---|---|---|---|---|---|---|
| Bonnet | SG | 48 | 51 | 10/24 | 6/16 | 25/29 | 3 | 0 | 33 |
| Lefebvre | PF | 48 | 27 | 11/22 | 0/1 | 5/7 | 20 | 0 | 39 |
| Gimenez | SF | 48 | 21 | 9/13 | 3/5 | 0/0 | 6 | 3 | 23 |
| Fournier | C | 48 | 14 | 5/11 | 0/1 | 4/5 | 19 | 2 | 26 |
| Richard | PG | 48 | 8 | 2/8 | 1/4 | 3/4 | 3 | 6 | 9 |
Aucun remplaçant n'a joué (5 titulaires, 48 minutes, mêmes cinq tous les quarts : Bonnet, Fournier, Gimenez, Lefebvre, Richard). Adversaires marquants : Baudry 23 pts, Fernandez 19 pts et 18 reb (éval 28), Thomas 15 pts (éval 24).

**Amical Mallorca Waves, 28/10 08:00, extérieur : 111-124, résultat = D** (notification `friendly_finished` won=false, `human_team_is_home`=false ; le calendrier affiche « notre score:leur score » = 111:124). Aucune stat joueur en base.

**Amical Statyba, 29/10 08:00 : 83-113, D** (déjà en silver, `my_result` L).

## 3. Aperçu coupe, tour 2 : Chomelix Cow (domicile) contre Paris Saint-Germain, 29/10 18:00 Europe/Paris (16:00 UTC)
Chance estimée : 51 % nous / 49 % PSG. `fixture_status` scheduled, `can_edit` vrai, **tactique de match non enregistrée** (`has_saved_match_tactics` faux ; preset de coupe actif = « League Tactic » 3b1936c2... d'après `selected_preset_id`). Aucun historique de forme ni de stats PSG (saison 2 à 0 match). Notre rang affiché : 2.
Tactique adverse : **non exportée** (aucun champ de consigne adverse dans l'aperçu). Notre réglage actuel : focus défensif `normal` (3), `area_step` 3 sur les 13 joueurs PSG ; cinq de départ enregistrés = Bonnet, Fournier, Gimenez, Lefebvre, Richard à tous les quarts.
Effectif PSG (13 joueurs, compétences par fourchettes de 20 points : 2PT/3PT/Déf/Reb/Passes/Dribble/Athl/Endurance) :
| Joueur | Poste | Âge | Taille | Points forts (fourchette) |
|---|---|---|---|---|
| Robert | SG | 28 | 200 | 2PT 81-99, Athl 61-80 |
| Dupont | PG | 26 | 190 | Passes 81-99, 2PT 61-80 |
| Blanchard | C | 29 | 211 | Déf 61-80, Reb 61-80 |
| Głowacki | PF | 29 | 206 | 2PT, Reb, Athl 61-80 |
| Mercier | C | 27 | 212 | 2PT 61-80 |
| Perrin | SF | 25 | 204 | 2PT, Athl 61-80 |
| Lecomte | SF | 31 | 196 | Déf, Reb 61-80 ; 2PT 0-20 |
| Fleury | SG | 25 | 199 | Reb 61-80 |
| Mathieu | PG | 29 | 186 | 3PT 61-80, Passes 61-80 ; Reb 0-20 |
| Veski | PG | 25 | 189 | Athl 61-80 |
| Baudry | PF | 23 | 206 | faible partout ; dribble 0-20 |
| Leroy | SF | 18 | 195 | 21-60 |
| Arnaud | SG | 17 | 187 | 21-60 |
Fatigue PSG : Arnaud 2,19, Baudry 1,95, Leroy 1,76, Mercier 1,73, Veski 1,57, les autres 0 à 0,22. Leur raquette (Blanchard, Mercier, Głowacki) pèse plus que la nôtre sur le papier ; Robert est leur seul scoreur 81-99.
Notre côté dans le même export : Ungureanu (C, 27 ans, 213 cm, 136 kg, forme 5) : Déf 45, Passes 44, Endurance 60, 2PT 45, Reb 53, Athl 70, 3PT 41, Dribble 19.

## 4. Calendrier (schedule, heure Europe/Paris)
29/10 18:00 coupe tour 2 PSG (dom.) · 30/10 08:00 amical Istanbul Cobras (dom.) · 31/10 08:00 amical BC Calije (ext.) · 02/11 20:00 ligue J1 Chara legends (ext.) · 04/11 08:00 amical baker street (ext.) · 04/11 20:00 ligue J2 Eindhoven Wizards (dom.) · 05/11 08:00 amical |HAVEX| (dom.) · 06/11 00:00 amical The Bombers (ext.) · 07/11 20:00 ligue J3 Póvoa Riptide (ext.) · 09/11 Naked Spartans (dom.) · 11/11 BC KIT (dom.). Saison 2 débute le 02/11 ; saison 1 finie 8e sur 12 (sans montée ni descente), ligue actuelle European Division Tier 3 League 13.

## 5. Notifications et news depuis le 27/10
27/10 00:00 `season_ended` rang 8/12 · `sponsor_offers_available` (choix avant le 02/11 18:45 UTC) · 27/10 18:24 sponsor FLUXORA signé (base 80 000/semaine, signé par vous) · 28/10 04:45 enchère perdue Liam Burke (270 000, gagnant Basket pastis) · 28/10 15:45 offre 1 000 sur Klein par Smart Signs. · 28/10 17:48 coupe gagnée · 28/10 21:14 Ungureanu acheté 21 250 · 29/10 07:48 amical perdu · 08:00 académie : score 59 à 70, 100 000 débités, rapport remplacé · 08:52 **Yago Durán perdu, prix final 1 060 500, gagnant Treviso Team**.
News du 28/10 : moteur v5 en amicaux seulement (voir commun.md), vue Historique de ligue, MVP saison/U21 dans le profil, nouveau réglage de club (masquer la vue terrain).

## 6. Classement erroné du script
| page_type | Contenu réel | Critère |
|---|---|---|
| `unknown` (17) | API annexes : session, saisons, ligues, détail/play-by-play/période de la coupe, aperçu et tactique de coupe PSG, effectif tactique, copie écran | clé `body.kind` (`finished`, `scheduled_lineups`) ou `body.presets`, `body.roster` |
| `friendly` (12) | 11 réponses d'API (session, ligues, détail Statyba, play-by-play, période) + 1 écran | `body.fixture_kind` = friendly pour le détail, sinon annexe |
| `notifications` (3) | classement de ligue (21363), non-lus, liste | `body.standings` = classement ; `body.notifications` = liste |
| `player` (5) | 4 réponses sur Ungureanu **et la fiche finances** (21372, `balance` 1 086 893) | clé `body.balance` = finances |
| `academy` (1) | probablement finances/personnel médical (déjà noté le 26/10) | `body.weekly_medical_staff_cost` |

## 7. Reste à exporter
- Détail de l'amical Mallorca du 28/10 (stats joueurs) : ouvrir Schedule, ligne 28.10 08:00, bouton « Report ». Utile seulement pour l'analyse de la défaite, pas pour la décision de ce soir.
- Rien d'autre ne manque pour PSG : la tactique adverse n'existe pas dans le jeu avant le match.

## 8. À corriger côté silver (ne bloque pas l'utilisateur)
`bv_matches`, `bv_fixtures` et `bv_match_player_stats` ne lisent pas les coupes (`/cup-fixtures/...`) : le match Maccabi et l'aperçu PSG sont absents. Vue à concevoir sous Opus.
