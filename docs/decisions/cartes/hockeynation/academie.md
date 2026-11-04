# Carte hockeynation — academie (draft, Import Draft, scouting, U17, U21)

Sources lues : commit d1eaf11 (2026-11-02)

Écrite le 2026-11-02 (fiche `academie.md`, `resume.md` § Rendu scouts, skills `hockeynation-draft-scouting`, `-joueurs`, `-potentiel-joueurs`, `-contrats-finances` § Jeunes ; connaissance § Draft / scouting). Règles : tout ajout de joueur = équipe résultante à 20 (CLAUDE.md règle 8) ; scouts : couvrir le plus de joueurs possible ; rendu scouts en tableau, jamais « requête X » ([U] 2026-10-29).

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:161 | meilleures caractéristiques | var. 3, 4 |
| :176 | facteurs cachés | var. 9 |

## Rendu (figé)
1. Scouts : `gold.hn_scout_liste` en tableau (une ligne par scout : top poste+nation / poste / nation, joueurs nommés et rang), puis `gold.hn_scout_board`.
2. Draft : `| Choix | Cible 1 | Cible 2 | Cible 3 | Repli | Poste | Talents vs poste | Rang | Scouté (fois) |` ; limites de position ; pré-instructions 1 h avant (jour 63, 26/12 21:00).
3. U21 de 21 ans : `| Joueur | Poste | Note | Pot. min–max | Classe | Décision (ELC / Farm / départ) |`.
4. U17 : équipe à 20 après draft (4 C / 4 LW / 4 RW / 3 LD / 3 RD / 2 G, VIDE signalé).

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Classe de draft | `select draft_rank, name, main_position, age, rating, scouted_times, from_my_u17, talent_strongest, talent_weakest, talents_cles, faible_cle, scouting_state from gold.hn_draft_board where season = <saison> order by draft_rank limit 30` | Choisir par build (talents vs poste), pas par note | c0ntrail 2026-10 (avis) ; [U] talents d'abord | |
| 2 | Nos choix | `silver.hn_draft_picks` | 10 choix sur 2 saisons ; ordre inverse du classement ; sans cible principale, la sim suit le classement pré-draft + besoins de poste | skill draft-scouting ; d0ghouse 2026-10-24 | |
| 3 | Potentiel | `select team_level, name, poste, age, rating, pot_min, pot_max, classe, futur from gold.hn_player_potential where team_level in ('U17','U21') order by team_level, pot_max desc limit 40` | Classe Fort / Solide gardée ; futur PRO / FRM / VIRER | skill potentiel-joueurs | |
| 4 | Scouts : couverture | `select scout, nb_top, nb_poste, nb_nation, nb_total from gold.hn_scout_liste limit 10` ; `gold.hn_scout_board` ; `gold.hn_scout_priority` | Embaucher le candidat qui couvre le plus de joueurs NOUVEAUX ; 8 scouts au plus, budget 300 000 $ / saison ; G exclus | skill draft-scouting § Scouts ; `resume.md` § Rendu | |
| 5 | Missions | `gold.hn_scout_targets` ; `silver.hn_scouting_assignments` | Mission plus courte si poste et nation du scout = ceux du joueur ; 3 rapports successifs | skill draft-scouting | |
| 6 | Fraîcheur scouting | `silver.hn_scouts`, `silver.hn_scouting_budget` (date du relevé) | Ne bougent qu'à l'export Scouting : dater avant d'écrire un nombre de scouts | `resume.md` § Pièges | |
| 7 | U21 de 21 ans | `gold.hn_daily_alerts` | ELC PRO ou Farm, sinon départ à 22 ans | `resume.md` § Règles | |
| 8 | U17 entrants | connaissance § Draft | 7 jeunes de 15 ans par saison : on en choisit un, les 6 autres reçoivent un poste manquant ; 5 draftables dans 3 saisons, 2 vont en U21 | hnadmin 2026-09-19 | |
| 9 | Valeur des tours | connaissance § Draft | 2e tour scouté = 70+ possible ; tour tardif = min 64 possible (avis) | trunkxolotl, c0ntrail 2026-10 | |
| 10 | Import Draft | `gold.hn_today` (jours 49-55) | Le meilleur des 6 révélés, talents vs poste | fiche académie § Livrable 4 | |
| 11 | Équipes inactives | connaissance § Draft | Elles draftent aussi ; un draftee d'une équipe sans GM peut être libéré | hnadmin 2026-10-24 | |
| 12 | Avis des amis | connaissance § Draft / scouting ; `connaissance-B-general-2022-2025.md` | — | connaissance | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis | Statut (base) |
| --- | --- | --- | --- | --- |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
