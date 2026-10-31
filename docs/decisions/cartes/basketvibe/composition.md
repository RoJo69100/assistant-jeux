# Carte basketvibe — composition (ligue, coupe, amical)

Sources lues : commit 58975fe (2026-10-31)

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
Règles d'origine : R-10 (`resume.md`), mémoires `feedback-format-tactique-parfait`, `feedback-amical-compo-test`, `feedback-rendu-demain-seulement` ; récidive « format tactique » inscrite 3 fois dans `docs/retro/regles-apprises.md`.
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
| 4 | Zone par adversaire | `select adversaire, poste, focus, zone from gold.bv_saisie_adversaires where fixture_id = <id> order by ordre` ; zone réellement jouée : `gold.bv_zone_jouee` | Rim sur les intérieurs qui ne tirent pas à 3 (2P% −3 %, 3P% jusqu'à +5 %) ; Perimeter sur les tireurs à 3 ; Middle par défaut. Existe en ligue, coupe, amical | skill tactique § Defensive area [News 2026-10-19, 27/10 ; utilisateur 2026-10-30] ; L-023 (Rim prouvée) ; avis marekb9231 2026-10-20 | |
| 5 | Fatigue de chaque joueur au coup d'envoi | `select name, stamina, minutes, sat_fatigue, penalty_v4 from gold.bv_fatigue_plan` + `gold.bv_roster_now.fatigue` | v4 : titulaires ≤ 20 (−4 %) ; 40 = −15 % ; 60 = −30 %. Coupe : fatigue 0. Gain = min × 0,19 × agress. × (1,5 − 0,008 × endurance) ; récupération 0,5 + 10 % par nuit | skill joueurs § Fatigue [M§5.6 ; News 2026-10-27] ; connaissance : avis « < 30 ne se remarque pas » contredit | |
| 6 | Forme | `select name, form from gold.bv_roster_now order by form desc` | Tireurs à 7 ou plus ; 5-6 pour les quarts défensifs ; 4 ou moins au repos (−4 % et pire) | skill joueurs § Forme [M§5.5] | |
| 7 | Blessés, indisponibles | `select name, injury_return_on from gold.bv_roster_now where injury_return_on is not null` | Hors du cinq ; depth chart rempli par poste (sinon échelle PG→C) | skill tactique § Depth chart [M§6.2.2] | |
| 8 | Minutes par joueur | calcul du tableau 1 (quarts × 12) ; passé : `gold.bv_match_player_lines.over_36` | ≤ 36 min (−20 % au-delà, +40 % de risque de blessure au Q4) ; en amical, sorties pour 6 fautes entre 28 et 34 min | [M§5.7] ; News 2026-10-19 ; L-026 (Q4 −4 au-delà de 36 min) ; L-021 | |
| 9 | Fit au poste | `select name, slot, fit_with_form, rank_in_slot from gold.bv_slot_fit where rank_in_slot <= 3 order by slot_order, rank_in_slot` | Chaque emplacement : le meilleur `fit_with_form` disponible ; taille sous 100 % d'efficacité = moins de ballons | skill joueurs § Taille [M§6.2.1] ; Dev 2026-07-09 (même emplacement = défenseur) | |
| 10 | Consignes de nos joueurs (rôle, off. focus, tir, agressivité) | `select joueur, poste, q1, q2, q3, q4, prol, minutes, off_focus, role, tir, agress from gold.bv_saisie_joueurs where fixture_id = <id> order by ordre` | Tir 4-5 seulement pour un bon tireur à 3 (`three_point` le plus haut de l'effectif) ; Primary = ~1/3 de tirs en plus ; agressivité : fautes, FT rate adverse et blessures montent (agressif ×2,00 de risque) | skill tactique § Consignes [M§6.3] ; L-020 et L-025 (mauvais tireurs en tir 3 pts = défaites) ; L-011 (crans 0/2/4 en amical) | |
| 11 | Ce qui sépare nos victoires et défaites (saison) | `select competition, my_result, matches, efg_pct, opp_efg_pct, oreb_pct, opp_oreb_pct, tov_pct, opp_tov_pct, fg3a_share from gold.bv_match_factors_by_result` | eFG et OREB décident (corrélations 0,91 et 0,73 avec l'écart) ; écart d'OREB ≤ −13,9 = 6 des 12 défaites | L-001, L-016 | |
| 12 | Tendance récente (manque de réussite) | `select last_n, side, wins, fg_pct, fg3_pct, oreb, tov from gold.bv_match_trends` | Comparer les 5 derniers à la saison ; une baisse du 3P% → baisser `tir` des joueurs concernés | L-002 (moins de 3 pts = meilleure eFG) | |
| 13 | Avis des amis | `outputs/basketvibe/veille/connaissance.md` § Tactique / moteur (deux sections) | Ligne « contredit » ou « en doute » : jamais utilisée seule | connaissance | |
| 15 | Match déjà planifié | `gold.bv_saisie_matchs` (preset, saved, directives) pour CHAQUE match planifié | Après tout changement de préréglage, de tactique générale ou de transfert d'un joueur du préréglage : rouvrir chaque match planifié et re-choisir (sinon le match garde l'ancien plan, ou le plan ne se sauvegarde pas) | grobarbrate 2026-09-05 ; nhegas12, chanceler 2026-09-20/21 ; tankre1792, Dev 2026-09-18/19 (connaissance § lecture des joueurs) | |
| 14 | Avantage du terrain | `gold.bv_saisie_matchs.is_home` | Petit bonus à domicile ; aucun en coupe | [M§6.1] ; News 2026-10-23 | |

## Ligue / coupe
Preset « League Tactic », re-sélectionné sur chaque match planifié ; meilleure composition. Coupe : fatigue nulle, cinq à 48 min possible mais −20 % après 36 min (L-026).

## Amical (`docs/fiches/basketvibe/resume.md` § Rythme)
Composition de **test**, jamais le cinq de ligue/coupe ; pas de preset ; un seul test à la fois, annoncé avec sa mesure (ex. zone Rim : 2P% adverse ; v5 : points de Q4 ; focus offensif 50 % : points du Primary). Réglages repris du dernier amical (`gold.bv_saisie_joueurs`, kind amical). Aucun export d'aperçu à demander.

## Checks appris des matchs
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|
| L-001 / L-016 | Priorité au rebond offensif et à l'eFG dans les choix de cinq | 2026-10-31 | |
| L-006 / L-014 / L-017 | Focus 5 sur le plus gros volume de tirs réel, pas sur la Preview | 2026-10-31 | |
| L-020 / L-025 | Tir 4-5 interdit pour un joueur sans réussite à 3 sur la saison | 2026-10-31 | |
| L-021 / L-026 | ≤ 36 min ; en amical, attention aux 6 fautes entre 28 et 34 min | 2026-10-31 | |
| L-023 | Zone Rim efficace sur un adversaire intérieur à gros volume | 2026-10-31 | |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi (source nouvelle) |
|---|---|---|---|
| 2026-10-31 | Agressivité 4-5 | aucun seuil → à confirmer : défense ≥ 55 (cran 4), ≥ 60 (cran 5) avant de mettre un joueur en agressif | avis chanceler, jorgeac25 (v3, 2026-08/10) ; à tester en amical v4, un joueur à la fois |
| 2026-10-31 | Rotation à 48 min | « ≤ 36 min » seul → ≤ 36 min, sauf cinq de coupe à fatigue nulle : Q4 mesuré (L-026) | Dev 2026-09-12 (5×48 gagne encore le Q4 de +5,12/+2,88, v3) ; v4 non mesuré |
