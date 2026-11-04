# Carte hockeynation — entrainement (Training PRO et FRM : compétence + coach par joueur, ordre de choix)

Sources lues : commit d1eaf11 (2026-11-02)

Écrite le 2026-11-02 (fiche `entrainement.md`, skills `hockeynation-coachs-entrainement`, `-joueurs`, `-potentiel-joueurs`). Réglable en PRO et FRM seulement ; U21 et U17 sans levier d'entraînement. Saisie dans l'ordre de l'écran Training (`pipelines/forme.py`, ordre d'entraînement HN).

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:160 | même ordre que l'écran | Rendu |
| :161 | meilleures caractéristiques | var. 2 |

## Rendu (figé)
Un tableau par équipe (PRO, puis FRM) dans l'ordre de choix : `| Ordre | Joueur | Âge | Poste | Compétence à travailler | Coach | Niveau du coach dans la compétence | Compétences plafonnées | Pot. min–max | Changement (🟧 à changer / ok) |`. Puis « Joueurs sans coach compétent » si non vide.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Plan proposé | `select * from gold.hn_training_plan order by team_level limit 60` | Compétence clé du poste, non plafonnée, de préférence un talent fort ; jamais une compétence plafonnée | fiche entraînement § Livrable 1 ; skill coachs-entraînement | |
| 2 | Compétences clés du poste | `select * from gold.hn_position_keys` | Hypothèse [H] : C = SHO PAS SKA FOF ; ailiers SHO PAS SKA ; D = DEF CHK SKA ; PWR manque pour tous | connaissance § Joueurs (talonflame1 2026-04-04, complété) | |
| 3 | Gains mesurés | `select name, team_level, skill, skill_level, coach_level, training_rate, day from silver.hn_training_log order by day desc limit 40` ; `gold.hn_player_progress` | Un gain nul deux cycles de suite = changer de compétence ou de coach | fiche entraînement § Livrable 3 | |
| 4 | Coachs disponibles | `gold.hn_coach_board` (6 compétences d'entraînement par coach) | Meilleur niveau du coach dans la compétence ; aucun coach compétent = aucun bonus | skill coachs-entraînement § Entraînement | |
| 5 | Ordre de choix | âge (`gold.hn_player_potential`) | Les plus jeunes et prometteurs d'abord (l'âge ralentit jusqu'à 25 ans) | fiche entraînement § Livrable 2 | |
| 6 | Plafonds | `silver.hn_players` (`skills_maxed`, `skills_declining`) | Compétence plafonnée = gain perdu ; déclin = ne pas compter dessus | skill joueurs § Plafonds, déclin | |
| 7 | Coach Development Boost | — | Contenu exact non publié (S27) : ne pas compter dessus | hnadmin 2026-10-25 (en doute) | |
| 8 | Avis des amis | connaissance § Entraînement, § Coachs | Un coach PB 80+ : investir dans des joueurs physiques ; les notes de coach renforcent un style, ne comblent pas une faiblesse | d0ghouse 2026-08-24 | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
