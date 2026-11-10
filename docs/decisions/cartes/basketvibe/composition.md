# Carte basketvibe — composition (ligue, coupe, amical)

Sources lues : commit fa4743a (2026-10-31)

Écrite le 2026-10-31 à partir des skills `basketvibe-tactique`, `-joueurs`, `-saison`, de `connaissance.md`, de `learnings.md` (L-001 à L-026) et des vues gold. Au passage suivant : `python pipelines/dossier.py basketvibe composition --mots "<adversaire, joueurs>"` donne cette carte et seulement le nouveau.

## Lignes de la liste couvertes
| Ligne (fichier:n°) | Texte court | Variable(s) ou section |
|---|---|---|
| chose-a-faire.txt:6 | paramètres par compétition | § Ligue/coupe, § Amical |
| :46 | quelle tactique | toutes |
| :47 | tableau joueurs (quarts, off. focus, rôle, tir, agressivité) | Rendu tableau 1, var. 10 |
| :48 | focus défensif 1-5 et zone | Rendu tableau 2, var. 3-4 |
| :49 | selon nos anciens matchs contre eux | var. 2-3 |
| :50 | selon la saison, blessés, forme, réussite | var. 5-7, 11-12 |
| :27, :29, :30 | forme, fatigue, poste | var. 5, 6, 9 |
| :160 | même ordre que l'export | Rendu |
| :170 | nouveauté = test en amical | § Amical |

## Rendu (figé, identique à chaque fois)
Règles d'origine : R-10 (`resume.md`), mémoires `feedback-format-tactique-parfait`, `feedback-amical-compo-test`, `feedback-rendu-demain-seulement` ; récidive « format tactique » inscrite 3 fois dans `docs/regles/archive/regles-apprises-2026-11-02.md`.
1. Une ligne : match (type, adversaire, heure de Paris, verrou), preset à sélectionner (ligue/coupe : « League Tactic » sur **ce** match ; amical : aucun).
2. **Tableau joueurs**, ordre de `gold.bv_saisie_joueurs order by ordre` (PG, SG, SF, PF, C, puis alphabétique), tous les joueurs de l'effectif :
   `| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Min | Off. focus | Rôle | Tir | Agress. |` — quarts : emplacement joué (PG…C) ou « — » ; consignes en chiffres d'écran 1-5.
3. **Tableau adversaires** (ligue, coupe), ordre de `gold.bv_saisie_adversaires order by ordre` : `| Adversaire | Poste | Focus (1-5) | Zone (Rim/Middle/Perimeter) |`, une ligne par joueur, jamais regroupé. **Amical** : une seule ligne « les 12 : focus 3, zone X ».
4. Tableau d'actions `| Priorité | Catégorie | Action |` (🟥 URGENT / 🟧 IMPORTANT / 🟩 SUIVI), aujourd'hui seulement, puis 1 à 3 lignes : pourquoi, et ce qui prouvera l'erreur (match qui le teste).
Interdits : « preset inchangé », « si », seuil générique, joueur non nommé, réglage sans valeur.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur (date) |
|---|---|---|---|---|---|
| 1 | Match à préparer (type, adversaire, heure, verrou, plan sauvegardé) | `select fixture_id, kind, match_day, kickoff, opponent, status, saved, preset from gold.bv_saisie_matchs order by kickoff desc limit 3` | Ligue lun/mer/sam 20:00, verrou 19:45 ; amical 08:00, verrou 07:45 ; coupe : heure de l'export. `saved` faux = le jeu joue la composition par défaut (L-011) | `resume.md` § Rythme ; skill tactique § Presets [M§6.4] | |
| 2 | Adversaire : rang, bilan, TS, humain ou bot, nos rencontres | `select opponent, opp_rank, opp_wins, opp_losses, opp_ts, my_ts, opp_is_human, meetings, top_scorers from gold.bv_next_opponents limit 3` + `select match_day, my_result, margin, efg_pct, opp_efg_pct, oreb_pct, opp_oreb_pct from gold.bv_match_report where opponent = '<adv>'` | Bot ≈ plus faible (bots −10 partout) ; une victoire passée n'est pas une preuve si les réglages ont changé | News 2026-10-27 ; Dev 2026-08-02 | |
| 3 | Vrais scoreurs adverses (part des tirs) | `select name, position, min, pts, shot_share, our_focus from gold.bv_match_opp_focus where opponent = '<adv>' order by shot_share desc limit 8` + `gold.bv_league_top_players where team = '<adv>'` | Lock (5) ou Intense (4) sur le joueur qui prend le plus de tirs (Hit), jamais sur le meneur passeur (Miss) ; 1 ou 2 joueurs à 4-5, compensés par 1-2 sur le banc ; la Preview seule désigne mal la cible | skill tactique § Focus défensif [M§6.6, §6.6.5] ; L-014 (2026-10-24) ; L-006 (give up sur le scoreur = 34-39 pts) ; L-017 (`off` = Lock : 4,0 % des tirs) | |
| 4 | Zone par adversaire | `select adversaire, poste, focus, zone from gold.bv_saisie_adversaires where fixture_id = <id> order by ordre` ; zone réellement jouée : `gold.bv_zone_jouee` | Rim sur les intérieurs qui ne tirent pas à 3 (jamais face à un C tireur à 3 : +5 % dans la zone non défendue, Dev 2026-10-23) (2P% −3 %, 3P% jusqu'à +5 %) ; Perimeter sur les tireurs à 3 ; Middle par défaut. Existe en ligue, coupe, amical | skill tactique § Defensive area [News 2026-10-19, 27/10 ; utilisateur 2026-10-30] ; L-023 (Rim prouvée) ; avis marekb9231 2026-10-20 | |
| 5 | Fatigue de chaque joueur au coup d'envoi | `select name, stamina, minutes, sat_fatigue, penalty_v4 from gold.bv_fatigue_plan` + `gold.bv_roster_now.fatigue` | v4 : titulaires ≤ 20 (−4 %) ; 40 = −15 % ; 60 = −30 %. Coupe : fatigue 0. Gain = min × 0,19 × agress. × (1,5 − 0,008 × endurance) ; récupération 0,5 + 10 % par nuit | skill joueurs § Fatigue [M§5.6 ; News 2026-10-27] ; connaissance : avis « < 30 ne se remarque pas » contredit | |
| 6 | Forme | `select name, form from gold.bv_roster_now order by form desc` | Tireurs à 7 ou plus ; 5-6 pour les quarts défensifs ; 4 ou moins au repos (−4 % et pire) | skill joueurs § Forme [M§5.5] | |
| 7 | Blessés, indisponibles | `select name, injury_return_on from gold.bv_roster_now where injury_return_on is not null` | Hors du cinq ; depth chart rempli par poste (sinon échelle PG→C) | skill tactique § Depth chart [M§6.2.2] | |
| 8 | Minutes par joueur | calcul du tableau 1 (quarts × 12) ; passé : `gold.bv_match_player_lines.over_36` | ≤ 36 min (−20 % au-delà, +40 % de risque de blessure au Q4) ; en amical, sorties pour 6 fautes entre 28 et 34 min | [M§5.7] ; News 2026-10-19 ; L-026 (Q4 −4 au-delà de 36 min) ; L-021 | |
| 9 | Fit au poste | `select name, slot, fit_with_form, rank_in_slot from gold.bv_slot_fit where rank_in_slot <= 3 order by slot_order, rank_in_slot` | Chaque emplacement : le meilleur `fit_with_form` disponible ; taille sous 100 % d'efficacité = moins de ballons | skill joueurs § Taille [M§6.2.1] ; Dev 2026-07-09 (même emplacement = défenseur) | |
| 10 | Consignes de nos joueurs (rôle, off. focus, tir, agressivité) | `select joueur, poste, q1, q2, q3, q4, prol, minutes, off_focus, role, tir, agress from gold.bv_saisie_joueurs where fixture_id = <id> order by ordre` | Tir 4-5 seulement pour un bon tireur à 3 (`three_point` le plus haut de l'effectif) ; Primary = ~1/3 de tirs en plus ; agressivité : fautes, FT rate adverse et blessures montent (agressif ×2,00 de risque) | skill tactique § Consignes [M§6.3] ; L-020 et L-025 (mauvais tireurs en tir 3 pts = défaites) ; L-011 (crans 0/2/4 en amical) | |
| 11 | Ce qui sépare nos victoires et défaites (saison) | `select competition, my_result, matches, efg_pct, opp_efg_pct, oreb_pct, opp_oreb_pct, tov_pct, opp_tov_pct, fg3a_share from gold.bv_match_factors_by_result` | eFG et OREB décident (corrélations 0,91 et 0,73 avec l'écart) ; écart d'OREB ≤ −13,9 = 6 des 12 défaites | L-001, L-016 | |
| 12 | Tendance récente (manque de réussite) | `select last_n, side, wins, fg_pct, fg3_pct, oreb, tov from gold.bv_match_trends` | Comparer les 5 derniers à la saison ; une baisse du 3P% → baisser `tir` des joueurs concernés | L-002 (moins de 3 pts = meilleure eFG) | |
| 13 | Avis des amis | `outputs/basketvibe/veille/connaissance.md` § Tactique / moteur (deux sections) | Ligne « contredit » ou « en doute » : jamais utilisée seule | connaissance | |
| 16 | Coupe, tour par tour | `select match_day, opponent, status, saved, preset from gold.bv_saisie_matchs where kind='coupe' order by kickoff desc limit 3` | Avant CHAQUE tour de coupe : preset « Cup », titulaires en place (au tour 1 du 28/10, le SF titulaire était sur le banc et le Dev soupçonne le préréglage de ligue) | usylum, jorgeac25 2026-10-28 ; notre match du 28/10 en « League Tactic » | |
| 15 | Match déjà planifié | `gold.bv_saisie_matchs` (preset, saved, directives) pour CHAQUE match planifié | Après tout changement de préréglage, de tactique générale ou de transfert d'un joueur du préréglage : rouvrir chaque match planifié et re-choisir (sinon le match garde l'ancien plan, ou le plan ne se sauvegarde pas) | grobarbrate 2026-09-05 ; nhegas12, chanceler 2026-09-20/21 ; tankre1792, Dev 2026-09-18/19 (connaissance § lecture des joueurs) | |
| 14 | Avantage du terrain | `gold.bv_saisie_matchs.is_home` | Petit bonus à domicile ; aucun en coupe | [M§6.1] ; News 2026-10-23 | |
| 17 | Depth chart du club (plan B : blessure, 6 fautes) | pas de vue gold ; `select id, captured_at, payload->>'text' from bronze.raw_pages where game='basketvibe' and page_type='tactics_depth' order by captured_at desc limit 1` (page `/club/tactics?tab=depth`) | Chaque poste a 2-3 remplaçants, tous dans l'effectif du jour ; un joueur parti ou arrivé depuis la capture = chart à refaire avant le verrou. Usage réel : J1 02/11, Lefebvre sorti à 6 fautes (32,2 min), Legrand l'a remplacé (15,8 min) | skill tactique § Depth chart [M§6.2.2] ; `gold.bv_match_player_lines` (`pf`, `fouled_out`) | 2026-11-04 : seule capture = 2026-10-16 (id 147), 19 jours, cite Henry, Lecomte, Fontaine, Klein (partis) ; Dang, Albano, Ungureanu absents → à refaire |
| 18 | Preview déjà exportée : box de l'adversaire à son dernier match | `select id, captured_at, payload->>'text' from bronze.raw_pages where game='basketvibe' and page_type='match' and page_url like '%<fixture_id>%view=preview' order by captured_at desc limit 1` (silver ne la lit pas : bv_next_opponents, bv_match_opp_focus restent vides) | Avant de dire « adversaire inconnu » : lire ce texte (minutes, PTS, 2P%, 3P% par joueur, « ESTIMATED CHANCE ») ; plus gros marqueur = candidat Lock | L-014 ; skill tactique § Focus défensif [M§6.6] | 2026-11-04 : Eindhoven vs Granada 100-83 : Bosman PF 28 pts 14 reb 48 min, de Boer SF 21 pts 36 min, Kramer C 12, Scholten SG 12 ; chance estimée 51 % / 49 % |
| 19 | Agressivité réellement jouée au dernier plan | `select name, min, defense_tier+1 as agress from gold.bv_match_player_lines where fixture_id = <id>` (écran = tier + 1) | Comparer au plan annoncé : un « agressivité 1 » non saisi reste au défaut du preset (3) | C-106 prescrivait agress 1 ; J1 02/11 joué à 3 pour les 10 joueurs | 2026-11-04 : preset League Tactic = agress 3 partout, à changer joueur par joueur |

## Ligue / coupe
Preset « League Tactic », re-sélectionné sur chaque match planifié ; meilleure composition. Coupe : fatigue nulle, cinq à 48 min possible mais −20 % après 36 min (L-026).

## Amical (`docs/fiches/basketvibe/resume.md` § Rythme)
Composition de **test** choisie le jour même par l'agent tactique à partir des données du jour, chiffres cités et hypothèses signalées, selon la fiche tactique §2 bis, dans l'ordre : minutes aux jeunes de 21 ans ou moins ; un seul réglage testé à la fois (E1 à E5) ; titulaires de la ligue protégés les jours de ligue, fatigue ajoutée calculée en SQL ; minutes réparties entre les joueurs. Jamais reprise du dernier amical ni du dernier brief. Pas de preset. Aucun export d'aperçu à demander.

## Checks appris des matchs
| L-nnn | Check | Ajouté le | Résultat depuis | Statut (base) |
| --- | --- | --- | --- | --- |
| L-001 / L-016 | Priorité au rebond offensif et à l'eFG dans les choix de cinq | 2026-10-31 |  | ✅ validée (21 pour / 0 contre) / hypothèse |
| L-006 / L-014 / L-017 | Focus 5 sur le plus gros volume de tirs réel, pas sur la Preview | 2026-10-31 |  | ✅ validée (3 pour / 0 contre) / hypothèse / hypothèse |
| L-020 / L-025 | Tir 4-5 interdit pour un joueur sans réussite à 3 sur la saison | 2026-10-31 |  | hypothèse / hypothèse |
| L-021 / L-026 | ≤ 36 min ; en amical, attention aux 6 fautes entre 28 et 34 min | 2026-10-31 |  | hypothèse / hypothèse |
| L-023 | Zone Rim efficace sur un adversaire intérieur à gros volume | 2026-10-31 |  | hypothèse |
| L-003 | Rotation à 2 unités de 24 min plutôt que 5×48 : 5 V-2 D depuis J15, +82 contre +34 face aux mêmes adversaires qu'à l'aller | 2026-11-02 | à surveiller (7 matchs) | hypothèse |
| L-004 | Agressivité (`defense_tier`) : cran 0 (Soft, écran 1) = FT rate adverse plus bas (19,1 contre 28,4 au cran 2) ; eFG adverse à l'inverse du manuel ; facteurs confondus, ne pas en faire une règle | 2026-11-02 | à surveiller | ✅ validée (7 pour / 0 contre) |
| L-007 | Au-delà de 36 min (régime 5×48) : Q4 à −4,9 contre −3,2, pas de signal net dans le score ; la règle ≤ 36 min reste celle du manuel | 2026-11-02 | à surveiller (14 matchs) | hypothèse |
| L-008 | Amical : cran 2 (écran 3) avec des jeunes à 36 min = eFG adverse 54,6 et FT rate 27,6 contre 49,8 / 22,3 au cran 0 ; confondu avec les minutes | 2026-11-02 | à surveiller (1 amical) | hypothèse |
| L-010 | Comparer les deux unités de 24 min au plus/moins : J19 unité A +18, unité B −12 ; une unité B faible se corrige d'abord | 2026-11-02 | à surveiller (1 match) | hypothèse |
| L-012 | Fatigue en amical (≈ 1/10) : sans effet exploitable pour la ligue ; la fatigue de ligue se lit dans `gold.bv_player_outlook` | 2026-11-02 | à surveiller | hypothèse |
| L-018 | Focus défensif : `off` dans le plan exporté = Lock (5/5) à l'écran | 2026-11-02 | validé (2026-10-21) | hypothèse |
| L-027 | Zone en amical v4 : Middle = pire mesure (2P% adverse 63,8 et 66,0 %) ; Perimeter 45,5 / 53,4 %, Rim 59,4 % ; ne pas rejouer Middle sans raison chiffrée | 2026-11-02 | à surveiller (adversaires biaisés) | hypothèse |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi (source nouvelle) |
|---|---|---|---|
| 2026-10-31 | Rim | Rim sur les intérieurs → Rim sauf face à un pivot qui tire à 3 | vachacz #polska 2026-10-23 14:47 |
| 2026-10-31 | Coupe | preset « Cup » suffisant → vérifier titulaires et preset avant chaque tour | usylum 2026-10-28 (bug du tour 1) |
| 2026-10-31 | Fautes v4 | — → fautes v4 ≈ v3 (16,4 contre ~17 par match) : un excès de fautes vient de l'agressivité de nos joueurs, pas du moteur | mesure du Dev 2026-10-28 |
| 2026-10-31 | Agressivité 4-5 | aucun seuil → à confirmer : défense ≥ 55 (cran 4), ≥ 60 (cran 5) avant de mettre un joueur en agressif | avis chanceler, jorgeac25 (v3, 2026-08/10) ; à tester en amical v4, un joueur à la fois |
| 2026-10-31 | Rotation à 48 min | « ≤ 36 min » seul → ≤ 36 min, sauf cinq de coupe à fatigue nulle : Q4 mesuré (L-026) | Dev 2026-09-12 (5×48 gagne encore le Q4 de +5,12/+2,88, v3) ; v4 non mesuré |
