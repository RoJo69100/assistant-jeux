---
name: hockeynation-adversaires
description: Méthode Hockey Nation d'étude des adversaires — quels exports faire sur une équipe adverse (effectif, lignes, coachs, résultats, échanges), comment lire sa force (talents vs poste, coachs de match, head coach et ses compétences spéciales, gardiens et fatigue, plafond), et quoi en tirer pour nos lignes et nos échanges. À charger avant un match important, une série de playoffs, ou pour comprendre pourquoi une équipe gagne.
---

# Hockey Nation — étude des adversaires

Demande de l'utilisateur (contexte `data/contexte/HN_contexte.txt`, 2026-10-23) : « oki, ils sont forts grâce à ça ». Règles de jeu citées depuis les autres skills `hockeynation-*`.

## Exports à demander (pages ouvertes par l'utilisateur, jamais de robot)
| Page de l'équipe adverse | Ce qu'on en tire |
|---|---|
| Roster (PRO, et U21 si échange) | notes, âges, postes, talents, compétences spéciales |
| Coaching staff | head coach : OFP, DFP, BAT, PP, PK (comptent double), compétences spéciales actives |
| Schedule + 3 derniers matchs (game) | forme, score, tirs, supériorités, gardien titulaire |
| Team Ratings de la ligue | notes offense, défense, physique (OFP, DFP et BAT jouent dessus) |
| Trade tracker | ce qu'elle achète ou vend, son plafond |

## Lecture
1. **Coachs** : somme de match du head coach × 2 + assistants ; PP et PK contre nos supériorités et infériorités ; compétences spéciales du head coach (seules actives).
2. **Joueurs** : meilleurs par poste et verdict talents (`gold.hn_player_fit` appliqué à leur effectif quand la vue l'inclut ; sinon lecture manuelle des talents).
3. **Gardiens** : END du titulaire et nombre de matchs d'affilée joués → fatigue probable (saison régulière).
4. **Spéciales collectives** : Inspire, Tactician (égalité cassée par Master Tactician), Team Player, Patriot.
5. **Discipline** : DSC faibles = bagarres et pénalités → notre PP compte plus.

## Livrable
Tableau `point fort | preuve | notre réponse` (3 lignes au plus), puis un réglage concret pour nos lignes A/B/C ou notre plan de jeu.

## Données
Les pages d'autres équipes arrivent dans `bronze.raw_pages` comme les nôtres ; à ce jour (2026-10-23) aucune vue silver ne les sépare des nôtres : à construire au premier export d'adversaire.
