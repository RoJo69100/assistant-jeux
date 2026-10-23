# Journal des enseignements — Hockey Nation (Chomelix Cows)

Tenu par l'agent Match (`.claude/agents/match.md`). Créé le 2026-10-23.

**Dernier match analysé : 2026-10-23 — Ottawa Owls (PRO, playoffs, jour 46, ext., D 4-6) ; les 33 matchs PRO de S26 (jours 8-46) sont analysés** (brief `briefs/2026-10-23-match.md`, réécrit le 2026-10-23 sur 33 matchs).

## Journal des matchs
Saison 26, PRO : 21 V 9 D en ligue (147-97, dont 1 défaite en prolongation), 0-3 en playoffs (7-14). Détail des 12 défaites : brief du jour, § 2. Source de tout le journal : `silver.hn_game_detail`.
| Jour | Adversaire | Lieu | Score | Tirs (nous-eux) | PP / PK encaissés | Gardien |
|---|---|---|---|---|---|---|
| 8 | Valcatraz Jailers | ext. | D 3-4 (prol.) | 30-40 | 0/1 ; 1/3 | Kovalev .900 |
| 12 | Ticera Rangers | dom. | D 2-5 | 34-29 | 1/4 ; 0/0 | Kovalev .857 |
| 18 | Ottawa Owls | ext. | D 3-5 | 44-29 | 0/4 ; 0/2 | Kovalev .828 |
| 28 | Helsinki Dragons | ext. | D 4-5 | 50-34 | 1/5 ; 0/2 | Lauper .800 puis Kovalev 9/9 |
| 30 | Deadwood Doom | ext. | D 4-5 | 51-35 | 1/5 ; 2/2 | Kovalev .857 |
| 35 | Essen Ravens | dom. | D 2-4 | 43-22 | 0/4 ; 1/1 | Kovalev 9/12 puis Lauper 9/10 |
| 36 | Rainbow Unicorns | ext. | D 3-7 | 30-33 | 1/3 ; 1/4 | Kovalev .788 |
| 37 | Corunna Giants | ext. | D 1-3 | 40-27 | 1/9 ; 0/1 | Kovalev .889 |
| 38 | Roswell Puck | dom. | D 5-7 | 43-29 | 1/4 ; 1/5 | Lauper .786 |
| 44 | Ottawa Owls (playoffs) | ext. | D 2-4 | 28-35 | 1/1 ; 2/3 | Kovalev .886 |
| 45 | Ottawa Owls (playoffs) | dom. | D 1-4 | 42-40 | 0/5 ; 1/1 | Kovalev .923 |
| 46 | Ottawa Owls (playoffs) | ext. | D 4-6 | 41-26 | 1/5 ; 0/1 | Kovalev .800 |
Les 21 victoires de ligue sont résumées : 120-52 en buts, 954-595 aux tirs, PP 21/90, PK 9/51 encaissés.

## Enseignements
<!-- L-nnn · date · enseignement · matchs à l'appui · statut (à surveiller / confirmé / infirmé) · source. Seuil de confirmation : 3 matchs PRO détaillés dans le même sens [H, à fixer] -->
Mise à jour 2026-10-23 sur 33 matchs : L-001 à L-004 réécrits ci-dessous (anciennes versions à 1 match remplacées) ; L-005 à L-011 ajoutés.
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
| C-010 | 2026-10-23 | Entraînement PRO : Kabát SKA, Bélanger SKA, Spinka SHO, Lubowitz SKA (clés de poste ouvertes) | `select name, skill, training_rate, coach_level from silver.hn_training_log where team_level='PRO' and name in ('Vít Kabát','Darryl Bélanger','Perry Spinka','Paul Lubowitz') order by day desc` : skill = SKA/SKA/SHO/SKA et training_rate comparé à la veille (Kabát 53, Bélanger 28, Spinka 48, Lubowitz 75) | ouvert | — |
| C-011 | 2026-10-23 | Entraînement FRM : Ahtola, von Arx, Fink, Zhitnik, van den Berg en SKA ; Bach en SHO ; Gmür en PWR ; Stampfli en DEF | `select name, skill, training_rate from silver.hn_training_log where team_level='FRM' and day>'2026-10-23'` : skills conformes ; comparer training_rate à la veille (Ahtola 39, von Arx 14, Fink 32, Zhitnik 59, van den Berg 52, Bach 37) | ouvert | — |
| C-012 | 2026-10-23 | Lignes PRO S27 (brief Tactique §1) : L1 Yokoyama-Blednov(C)-Spinka, Seppälä-Marquardt ; L2 Conte-de Bruin-Lubowitz, Burns-Nokelainen ; L3 Stone-Papež-Jaworski, Munk-Kabát ; L4 Bélanger-Flink-Hateboer ; aucune case vide | `select line, slot, count(*) from silver.hn_lineups where lineup='A' and day>'2026-10-23' and line in ('L1','L2','L3','L4') group by 1,2` : 14 cases pleines (L4 sans D) ; aucun joueur hors de ses postes (`positions`) | ouvert | — |
| C-013 | 2026-10-23 | Monter Jukka Nokelainen (FRM RD 68) en PRO avant le jour 8 de S27 : 3e RD obligatoire (3 paires de D jouent) | `select team_level from silver.hn_players where name='Jukka Nokelainen' order by as_of desc limit 1` = PRO | ouvert | — |
| C-014 | 2026-10-23 | PK : Bélanger (Penalty Killer) et Conte dans les unités PK ; PP refait sur SHO/PAS (de Bruin, Yokoyama, Lubowitz, Kabát, Bélanger) | `select line, slot, player_id from silver.hn_lineups where lineup='A' and line like 'PK%' and day>'2026-10-23'` contient Bélanger et Conte ; taux de PP de S27 vs S26 (1 but sur 5 contre Ottawa ; S26 complet à calculer par Match) | ouvert | — |
| C-015 | 2026-10-23 | Un bon FOF sur chaque ligne (Blednov 10 L1, Conte 10 L2, Papež 8 L3, Flink 6 L4) | taux de mises au jeu de l'équipe sur les 10 premiers matchs de S27 ≥ 54,8 % (S26 : 557 gagnées sur 1017, somme `faceoffsWon` / (`faceoffsWon`+`faceoffsLost`) de `silver.hn_game_detail`) | ouvert | — |
| C-016 | 2026-10-23 | Ne pas faire le Swap Blednov RW→C (inutile en PRO) ; garder Kovalev SG / Lauper BG sans réglage (rotation automatique) | `select main_position from silver.hn_players where name='Slava Blednov'` = RW ; en S27 Lauper démarre 1 match après 4 départs d'affilée de Kovalev | ouvert | — |
