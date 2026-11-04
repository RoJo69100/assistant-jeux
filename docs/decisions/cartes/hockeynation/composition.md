# Carte hockeynation — composition (lineups PRO A/B/C, plan de jeu, postes FRM/U21/U17)

Sources lues : commit e018ac2 (2026-11-04)

Écrite le 2026-11-02 (fiche `tactique.md`, `resume.md`, skills `hockeynation-match-calendrier`, `-joueurs`, `-adversaires`, connaissance § Matchs / lignes, learnings L-003, L-004, L-009, L-010, L-016). Règles : rendu FIGÉ du 2026-10-29 (« ne change jamais le rendu », `resume.md` § Tactique PRO), 4 équipes et 20 joueurs (CLAUDE.md § Hockey Nation), horaire « aujourd'hui seulement ».

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:160 | même ordre que l'écran pour la saisie | Rendu (ordre de `gold.hn_tactique_rendu`) |
| :161 | meilleures caractéristiques de chaque joueur | var. 2, 3 |
| :170 | nouveauté : tester en amical | var. 12 |

## Rendu (figé, ne pas réécrire à la main)
1. `select ordre_poste, poste, joueur, age, note, endurance, fof, speciales, roles from gold.hn_tactique_effectif_poste order by ordre_poste, note desc limit 40` (tous les joueurs PRO par poste).
2. `select bloc, line, slot, joueur, note, endurance, fof, poste from gold.hn_tactique_rendu order by ordre limit 60` : un tableau par bloc (Lignes et paires D · Gardiens · Power play · Infériorité 4 hommes · Infériorité 3 hommes · 4 contre 4 · Gardien retiré · Rôles), colonne « dans le jeu » = 🟥 case vide / 🟧 à changer.
3. `select parametre, cible, dans_le_jeu, libelle, statut from gold.hn_tactique_plan_rendu limit 10`.
4. `select * from gold.hn_tactique_controle` : tout `ok` avant de rendre, sinon corriger la cible.
5. Lineups B et C = copie de A. FRM, U21, U17 : lignes automatiques, seul levier = poste principal (« Swap position ») ; une ligne par changement de poste proposé.
6. Première ligne si la lineup exportée date d'avant le dernier changement : « 🟥 URGENT · Export · exporte Lineups PRO » (`gold.hn_exports_state`).

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Prochain match et adversaire | `select equipe, date_paris, game_type, adversaire, domicile, nos_resultats_contre_lui from gold.hn_adversaires where equipe = 'PRO' limit 3` | Lineup saisie au moins 1 h avant le match, sinon risque de −30 % | connaissance § Matchs (hnadmin 2025-07-10) | |
| 2 | Joueur au bon poste | `poste` de `gold.hn_tactique_rendu` ; `gold.hn_player_fit` (verdict) | Hors poste = −20 % : aucune ligne « hors poste » ; contre-emploi des talents toléré (L-010 : aucun effet mesuré) mais règle utilisateur « talents d'abord » prioritaire | skill match-calendrier § Pénalités ; [U] ; L-010 | |
| 3 | Endurance par unité | `endurance` de `gold.hn_tactique_rendu` | L1 7+, L2 6+, D1 8+, D2 6+, G1 7+, tolérance −1 | Discord talonflame1 2026-04-04 (confirmé) | |
| 4 | Gardien titulaire | `gold.hn_tactique_rendu` bloc Gardiens ; arrêts par période dans `silver.hn_game_detail.boxscore` | G1 7+ en END ; Kovalev (END 4) recule en P3 (.868 contre .906/.911) ; 4 départs d'affilée au plus pour END 4 (saison régulière) | L-016, L-003 ; [G:Lineups] | Kovalev END 4, Lauper END 6 (2026-11-02) ; 2026-11-04 : Kovalev 4 départs de ligue d'affilée, jamais 5 sur 29 apparitions (le jeu remplace le gardien fatigué, connaissance B § 3 roadiculous 2023-04-23) : ne pas saisir Lauper SG ; Lauper ligue S26 .877 (121/138, 5 matchs complets), Kovalev .893 ; `tiredness` du boxscore gardien : sens à tester |
| 5 | Mises au jeu | `fof` ; un FOF 7+ par unité de PP | Un bon FOF par ligne suffit, pas forcément le centre ; FOF sans lien avec le résultat (55,2 % en D contre 54,6 % en V) : ne pas sacrifier un poste pour lui | L-004 ; talonflame1 2026-04-04 | |
| 6 | Power play | bloc Power play, score SHO+PAS+SKA | PP = SHO+PAS+SKA, un FOF 7+ par unité ; un joueur une fois par type d'unité | fiche tactique § Règles de choix | PP 20,7 % S26 (L-006) |
| 7 | Infériorité | blocs PK4 / PK3, score DEF+CHK+SKA+PWR | PK = DEF+CHK+SKA+PWR ; PK à 70 % en défaite contre 82,4 % en victoire | fiche tactique ; L-006 | |
| 8 | Discipline | `select name, dsc from silver.hn_players where team_level = 'PRO' order by dsc limit 8` | DSC 3-4 = 3 fois plus de PIM ; ne pas les mettre ensemble en PK | L-008 (à surveiller) | |
| 9 | Plan de jeu | `gold.hn_tactique_plan_rendu` ; libellés mémoire `reference-hn-plan-de-jeu-libelles` | shift length short = test : revenir à normal si la L1 encaisse plus de buts après 10 matchs | `resume.md` § Tactique PRO | short (test depuis 2026-10-29) |
| 10 | Capitaine | caché (leadership) | Aucun effet visible (Seppälä 11-5 contre Pålsson 10-4) : ne pas en faire un levier | L-009 (infirmé) ; d0ghouse 2026-08-24 | |
| 11 | Cases vides et partis | `select lineup, line, slot, joueur, controle from gold.hn_saisie_lignes where controle <> 'ok' limit 20` | Case vide ou joueur parti = amateur, −5 % d'équipe chacun | skill match-calendrier § Pénalités | |
| 12 | Test en amical | amicaux jouables (premium) | Pénalité de mauvais poste s'applique en amical, pas celle du plafond ; pas d'expérience gagnée ; un réglage testé à la fois | connaissance § Entraînement (d0ghouse 2026-10-28, krusher_kev 2026-10-05) | |
| 13 | FRM/U21/U17 : poste principal | `select team, team_level, position, ord, name, verdict, score_poste from gold.hn_depth_chart where own and team_level <> 'PRO' order by team_level, position, ord limit 60` | 20 joueurs : 4 C / 4 LW / 4 RW / 3 LD / 3 RD / 2 G ; « Swap position » si le poste secondaire colle mieux aux talents | CLAUDE.md § Hockey Nation ; fiche effectif § 2 | lignes réellement alignées FRM/U21 absentes de la base (2026-11-02) |
| 14 | Avis des amis | connaissance § Matchs / lignes / plan de jeu ; `connaissance-B-general-2022-2025.md` | « ultra defensive » conseillé par un joueur (en doute) | heymelo27 2026-05-21 | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|
| L-003 | La fatigue du gardien n'explique pas les défaites jusqu'au 3e départ ; rotation au 4e départ pour END 4 | 2026-11-02 | à surveiller |
| L-004 | FOF : critère secondaire, jamais au prix d'un hors-poste | 2026-11-02 | confirmé S26 |
| L-009 | Capitaine sans effet mesurable | 2026-11-02 | infirmé S26 |
| L-010 | Contre-emploi des talents sans effet mesuré ; règle utilisateur gardée | 2026-11-02 | à surveiller |
| L-016 | Gardien END bas : arrêts en P3 plus faibles ; G1 7+ visé (échange ou montée) | 2026-11-02 | à surveiller (J8 .714 en P3) |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
