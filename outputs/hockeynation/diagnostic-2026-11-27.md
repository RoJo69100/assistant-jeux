# Hockey Nation — diagnostic PRO (Chomelix Cows), 27/11/2026

Sources lues ce jour : `silver.hn_games`, `silver.hn_game_detail` (`events`, `teams`), `python -I pipelines/match_engine_etat.py`, `bronze.raw_pages`, `silver.hn_api`.
Mis à jour à 11:05 Paris (base de nouveau joignable) : tableau des 10 derniers matchs calculé.

## 1. Exports du 27/11 vérifiés en base
- Reçus le 27/11 (10:32–10:33) : Roster, Lineups PRO, Scouting staff et budget, Matchs (programme), 41 pages de match.
- **Training** : toujours absent à 11:05 (dernier `club_training` 25/11 13:37). Aucune page Office ni Training reçue le 27/11, hors Scouting.
- **Salary cap** : la route `/office/salary-cap-overview` (10 relevés, dernier 31/10) n'a jamais été capturée depuis une page « Salary cap » : elle n'arrive que depuis **Office > Shortlist**, **Free agent center** et la page d'un joueur. Le userscript capture tous les JSON sans filtre de route : rien à corriger dans le script. Ce qui manque : ouvrir **Office > Shortlist** (ou une fiche joueur) pour qu'elle arrive. Le libellé « Office > Salary cap » de `gold.hn_exports_state` est trompeur (à renommer, non fait).
- `team_level` vide pour PRO J32 et J33 : la dernière capture de ces matchs (`/club/:id/game-overview`) n'a pas `teams.<côté>.level`. Corrigé (`sql/silver/056`, repli sur le niveau du roster de notre équipe) : J32 et J33 = PRO ; 0 match à nous sans niveau sur 402.

## 2. Les 10 derniers matchs PRO (ligue)
Tirs = événements `Shot` + `Goal` (tirs cadrés ; J33 : 46 = `teams.*.stats.shots`). PP = buts `strength = PP` / `ppAttempts` ; PK = buts encaissés en infériorité / occasions adverses. Résultat = `my_result`.
| date (Paris) | jour | adversaire | résultat | BP | BC | tirs pour | tirs contre | PP | PK (enc./occ.) | PIM nous/eux |
|---|---|---|---|---|---|---|---|---|---|---|
| 26/11 18:15 | 33 | Grande Cache Kings (dom.) | D (t.a.b.) | 3 | 3 | 46 | 32 | 1/2 | 0/3 | 6/4 |
| 25/11 23:30 | 32 | Forest Hills Rangers (ext.) | D (t.a.b.) | 3 | 3 | 38 | 48 | 0/5 | 1/3 | 6/10 |
| 24/11 18:00 | 31 | Kocúrkovo HK Rakety (ext.) | D | 0 | 6 | 36 | 29 | 0/4 | 0/1 | 2/8 |
| 23/11 22:15 | 30 | Corunna Giants (ext.) | D | 4 | 5 | 40 | 31 | 0/5 | 0/4 | 13/15 |
| 22/11 18:45 | 29 | Helsinki Dragons (dom.) | V | 8 | 2 | 60 | 15 | 1/4 | 0/1 | 2/10 |
| 21/11 19:45 | 28 | Valcatraz Jailers (dom.) | V | 4 | 1 | 12 | 31 | 0/2 | 1/3 | 6/4 |
| 19/11 17:30 | 26 | Whitefish Tourists (dom.) | V | 9 | 7 | 41 | 45 | 1/3 | 0/2 | 4/8 |
| 18/11 19:30 | 25 | Rainbow Unicorns (dom.) | D | 2 | 5 | 26 | 44 | 0/— | 1/1 | 2/— |
| 17/11 17:45 | 24 | Essen Ravens (dom.) | V | 7 | 2 | 35 | 23 | 0/6 | 1/2 | 4/12 |
| 17/11 01:00 | 23 | Everett Assassins (ext.) | D | 2 | 3 | 34 | 25 | 2/5 | 2/3 | 11/17 |
BP et BC hors tirs au but (J32 et J33 : 3-3 à la fin des prolongations, perdus aux tirs au but, `result.shootout = true`). J25 : `ppAttempts` et `pim` absents, écarté du PP et des PIM.

**Totaux (n = 10)** : 4 V, 6 D (dont 2 aux tirs au but).
| mesure | valeur | IC95 |
|---|---|---|
| Buts pour / match | 4,2 | 2,4–6,0 |
| Buts contre / match | 3,7 | 2,5–4,9 |
| Tirs pour / contre | 368 / 323 | — |
| Réalisation nous | 11,4 % (42/368) | 8,6–15,1 % |
| Réalisation adverse | 11,5 % (37/323) | 8,4–15,4 % |
| Arrêts (aucun but dans un filet vide) | 88,5 % (286/323) | 84,6–91,6 % |
| PP (9 matchs) | 13,9 % (5/36) | 6,1–28,7 % |
| PK (9 matchs) | 73,9 % (17/23) | 53,5–87,5 % |
| Buts en infériorité (SH) pour / contre | 1 / 1 | — |
| PIM nous / eux (9 matchs) | 56 / 88 | — |
| Tirs par période P1 / P2 / P3 / prol. (pour-contre) | 106-123 / 140-98 / 116-98 / 6-4 | — |
| Buts par période P1 / P2 / P3 (pour-contre) | 12-12 / 15-11 / 15-14 | — |
Gardiens : les événements `Goal` n'ont pas de clé `goalie` ; les arrêts par gardien (145 et 141) ne se rapportent à aucun but encaissé : % par gardien non calculable depuis les événements.

## 3. Où l'on perd — registre du Match Engine (PRO, toutes saisons en base, 27/11)
Descriptif, sans règle d'action. Recopié de `match_engine_etat.py`.
| mesure | valeur | n | IC95 | verdict du script |
|---|---|---|---|---|
| Réalisation (tirs) | D : nous 7,6 %, eux 14,4 % ; V : nous 12,7 %, eux 8,3 % | 24 matchs | — | L-001 confirmé |
| xG pour nous, réussite contre nous | 13 défaites sur 24 avec xG nous > eux ; réussite 7,6 % contre 17,2 % | 13 | — | L-015 confirmé |
| Supériorité numérique (saison en cours) | PP 16,1 % ; 4 buts SH encaissés ; ligue 19,3 % | 87 sup. | 9,8–25,2 % | indéterminé : n trop petit (seuil `SEUILS["pp"]`) |
| Infériorité numérique | PK D 69,5 % (59 sup. adv.) ; PK V 85,5 % ; 4 matchs écartés (ppAttempts absent) | 22 matchs | D 56,9–79,7 % / V 76,4–91,5 % | indéterminé : n trop petit (toutes équipes, 136 matchs : confirmé) |
| Gardien en défaite | D 86,8 % ; V 92,2 % | 24 | D 84,1–89,1 % | indéterminé : n trop petit |
| Gardien Kovalev, P3 | 89,4 % contre 92,7 % P1-P2 | 25 | 84,7–92,8 % | indéterminé : n trop petit |
| Fatigue gardien (3e départ et plus) | 89,2 % contre 90,0 % au 1er départ | 21 | 86,6–91,4 % / 87,4–92,1 % | indéterminé : n trop petit |
| Pénalités (DSC ≤ 4 contre ≥ 7) | 0,43 contre 0,22 PIM/match par joueur | 56 matchs, 15 joueurs | — | L-008 confirmé |
| Mises au jeu | D 52,2 % ; V 53,7 % | 24 | 48,4–55,8 % / 50,6–56,8 % | indéterminé |
| Shift length court | 3,41 BC/match (court, 22 m) contre 3,36 (normal non prouvé, 33 m) | 55 | 2,64–4,18 / 2,74–3,99 | indéterminé |
Lecture (descriptive) : sur toute la base, l'écart est la **réalisation** en défaite, pas le volume de tirs. Sur les 10 derniers matchs, les deux réalisations sont égales (11,4 % contre 11,5 %) ; le PP (5/36) est le chiffre le plus bas, mais son intervalle (6–29 %) contient la moyenne de la ligue (19,3 %) : rien de prouvé. Discipline : nous pénalisés moins que l'adversaire (56 contre 88 PIM).

## 4. Les événements portent-ils les joueurs sur la glace ?
**Tirs : oui. Joueurs sur la glace : non.**
Exemple (match 2b841297, J33) : `{"type":"Shot","time":7,"period":1,"teamId":"50cf5f9e-…","shooter":"857d534e-…","goalie":"a946b379-…"}` ; but : `{"type":"Goal","scorer":…,"assists":[…],"strength":"EVEN","emptyNet":false}`.
Clés présentes sur tous les événements en base : `id, num, time, timeAt, period, type, teamId` + selon le type `shooter, goalie, scorer, assists, strength, hitter, victim, winner, loser, giver, taker, blocker, on, penalty, in, out`. Aucune liste des 5 patineurs sur la glace.
→ **+/- et tirs contre par ligne : non calculables.** À capturer en plus : la composition sur la glace à chaque tir et but (liste des joueurs par événement, ou les changements de ligne horodatés). Si le jeu n'affiche nulle part cette information, je ne sais pas comment l'obtenir sans requête supplémentaire (interdit, inviolable 1). Les clés `in`/`out` (41 événements en base) ne sont pas lues : probablement les sorties de gardien, à vérifier.

## 5. Suite
- Agent `analyste` lancé le 27/11 sur J31, J32, J33 : brief `outputs/hockeynation/briefs/2026-11-27-analyste-pro.md`.
