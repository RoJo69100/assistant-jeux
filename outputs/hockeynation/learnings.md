# Journal des enseignements — Hockey Nation (Chomelix Cows)

Tenu par l'agent Match (`.claude/agents/match.md`). Créé le 2026-10-23.

**Dernier match analysé : 2026-10-23 — Ottawa Owls (PRO, playoffs, jour 46, ext., D 4-6)** (brief `briefs/2026-10-23-match.md`).

## Journal des matchs
| Date / jour | Équipe | Adversaire | Lieu | Score | Tirs (nous-eux) | Source |
|---|---|---|---|---|---|---|
| jour 46 (playoffs) | PRO | Ottawa Owls | ext. | D 4-6 | 41-26 | `silver.hn_game_detail` (seul match détaillé) |

## Enseignements
<!-- L-nnn · date · enseignement · matchs à l'appui · statut (à surveiller / confirmé / infirmé) · source. Seuil de confirmation : 3 matchs PRO détaillés dans le même sens [H, à fixer] -->
| ID | Date | Enseignement | Matchs | Statut | Source |
|---|---|---|---|---|---|
| L-001 | 2026-10-23 | Défaite malgré 41 tirs contre 26 : le gardien Vasiliy Kovalev arrête 20 des 25 tirs cadrés (.800) contre 37/41 (.902) pour Marius Villadsen (Ottawa). Notre PP : 1 but sur 5 supériorités (Alexander de Bruin, 3e période, 4-5) ; Ottawa : 0 sur 1. Le volume de tirs n'a pas suffi. | 1 | à surveiller | `silver.hn_game_detail` (periods, summary, boxscore) |
| L-002 | 2026-10-23 | Ottawa marque 2 buts sur 3 tirs en 2e période (nous : 17 tirs) et 3 sur 12 en 3e (nous : 9 tirs, dont le but dans le filet vide) : ses buts tombent quand on domine les tirs. [L-001 précisé : cause gardien non liée à la fatigue, voir L-003.] Calvin Hamill (C, Ottawa) : 3 buts, 4 aides au +/-, 1re étoile. | 1 | à surveiller | `silver.hn_game_detail` (periods, stars) |

| L-003 | 2026-10-23 | Hypothèse « Kovalev fatigué / à remplacer » écartée pour ce match : règle de fatigue = saison régulière seulement, match de playoffs ; aucun seuil de remplacement atteint (retard max 2 en P2, 3 en P3 ; ≥ 79 % d'arrêts au 3e but). Kovalev END 4, Lauper END 6 : la fatigue ne jouera qu'en ligue (à lire sur les 30 matchs, C-002). | 1 | à surveiller | `hockeynation-match-calendrier` [G:Lineups] ; `silver.hn_game_detail` |
| L-004 | 2026-10-23 | Aucun joueur hors poste dans les lignes A en base ; mises au jeu prises par Blednov et Conte (FOF 10, les 2 meilleurs), conforme à la règle : 12 gagnées sur 27, Haugen (Ottawa) 11 sur 13. Contre-emploi en ligne : Conte, Blednov (RW), Flink, Sutherland, Eskelinen. | 1 | à surveiller | `hockeynation-match-calendrier`, `gold.hn_player_fit` |

## Conseils
<!-- C-nnn · date · conseil · critère vérifiable (SQL) · statut · effet -->
| ID | Date | Conseil | Critère vérifiable | Statut | Effet constaté |
|---|---|---|---|---|---|
| C-001 | 2026-10-23 | Exporter le détail des 2 autres matchs PRO de la série contre Ottawa Owls (jours 44 et 45, défaites 2-4 et 1-4) pour savoir si le gardien et le PP expliquent aussi ces défaites | `select count(*) from silver.hn_game_detail where game_id in ('9b22b7d7-a3fc-478d-93b3-1d6782c8683c','36d0e218-91ac-4570-8c58-45ff53280dcc')` = 2 | ouvert | — |
| C-002 | 2026-10-23 | Exporter le détail de tous les matchs PRO de la saison 26 (30 de ligue, dont 21 victoires) pour comparer victoires et défaites en tirs, PP et gardien | `select count(*) from silver.hn_game_detail d join silver.hn_games g using (game_id) where g.game_type='League' and (g.home='Chomelix Cows' or g.away='Chomelix Cows')` = 30 | ouvert | — |
| C-003 | 2026-10-23 | Laisser partir Troy Sutherland et Gordon Kub (3,26 M$ x 3 ans et 2,75 M$ x 7 ans refusés) | `select name from silver.hn_players where name in ('Troy Sutherland','Gordon Kub') and team_level='PRO' and contract_to>=27` = 0 ligne ; cap S27 ≥ 0 | ouvert | — |
| C-004 | 2026-10-23 | Vendre Kjell Pålsson en fenêtre I de S27 sans salaire en retour : cap space S27 1,63 → 4,91 M$ | `select cap_space from gold.hn_cap_outlook where season=27` ≥ 4 910 000 | ouvert | — |
| C-005 | 2026-10-23 | Head coach PRO : Troy Lisowsky à la retraite d'Aalst (repli Bondar) | `select name from gold.hn_coach_board where source='club' and team_level='PRO' and head_coach` = Troy Lisowsky | ouvert | — |
| C-006 | 2026-10-23 | Draft R3 n°55 : cibles Cunningham (C), Degryse (G), Zwart (LD) dans cet ordre | après la draft : `select name, team_level, age from silver.hn_players where name in ('Wesley Cunningham','Jean-Yves Degryse','Quinn Zwart')` (un des trois en U21 au jour 1 de S27) | ouvert | — |
| C-007 | 2026-10-23 | Draft R4 n°75 : Aufderhar, Swaniawski, Beaudin ; R5 n°95 : Norheim, Anglehart, Paradis (Webster et Mayor, jamais repérés, retirés) | même requête sur ces 6 noms en S27 | ouvert | — |
| C-008 | 2026-10-23 | Scouts : 5 au total (recruter 2 centres et 1 LD au jour 4 de S27), 330 000 $/saison | `select num_scouts, budget_left from silver.hn_scouting_budget order by day desc limit 1` = 5 et ≥ 300 000 en fin de S27 | ouvert | — |
| C-009 | 2026-10-23 | Ne rien signer pour Riku Ronkainen (U21, 21 ans, LW 47) ; Koukal et Višňovský déjà en contrat Farm | `select name from silver.hn_players where name='Riku Ronkainen'` = 0 ligne en S27 | ouvert | — |
