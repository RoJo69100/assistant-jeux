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

## Compétences clés (sources lues le 2026-10-23)
| Poste | Ce que disent les sources | Source |
|---|---|---|
| Attaquants | SHO et PAS = buts ; SKA et PWR = possession de la rondelle ; CHK et DEF = défense ; DSC = pénalités ; FOF : un bon joueur de mises au jeu par ligne suffit, pas forcément le centre | Discord talonflame1, 2026-04-04 ; définitions [G:Players] |
| Défenseurs | DEF « crucial pour empêcher les occasions », CHK, SKA ; END de la paire D1 à 8+ | [G:Players] ; talonflame1 |
| Gardiens | REF, POS, PAD, BLO, GLO comptent tous ; STK est le moins utilisé (« tout sauf Stick », a_ferk 2026-04-04) ; END = nombre de matchs avant fatigue, titulaire à 7+ ; un gardien à END faible tombe vers 60 % de condition en 3e période | talonflame1, a_ferk, [G:Players] |
Écarts avec `gold.hn_position_keys` : PWR manque aux attaquants, FOF est compté à tort comme clé du centre. À corriger au recalage après le premier patch (conception, Opus). Le poids exact de chaque compétence dans la note (note par position) n'est dans aucune source lue ; un outil communautaire (nedu92, #game-tools, 2026-01-18) l'utilise sans le publier.

## Données
- Effectifs PRO des 4 clubs étudiés (Leszno Bulls, Seoul Pilots, Miami Maidiacs, Jessup Baldos), exportés le 2026-10-23 : `silver.hn_league_players`, `gold.hn_league_player_fit`, `gold.hn_depth_chart` (lignes probables, les lignes réelles d'un autre club ne sont pas visibles).
- Staffs complets (4 coachs par club) : `silver.hn_club_staff`, `gold.hn_coach_specials`, `gold.hn_club_compare`.
- Matchs joués contre eux : `silver.hn_game_detail` (boxscore, players, coaches).
- Marché, trade chat : `silver.hn_market_players`, `silver.hn_trade_chat`.

## [Veille intégrale 2026-10-29] Note d'équipe (V-A-19, V-B-3, V-C-6)
- **Note d'équipe** : seuls les 18 meilleurs patineurs comptent pour OFF / DEF / PHY (6 groupes de pondération par rang) ; GOA = 80 % du meilleur gardien + 20 % du 2e ; poste vide compté à 25 ; l'expérience n'entre pas encore. Avis talonflame1 (2026-03-26) : moyenne des 20 meilleurs par compétence — écart 18/20 non tranché. Ajouter un joueur ne baisse pas la note. Pour un adversaire : regarder le gardien n° 1 en priorité, puis les 18 patineurs au-dessus du lot. [d0ghouse 2022-11-11, 2023-05-23 ; mr.president13 2024-07-29 ; V-A-19]
