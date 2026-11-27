# Hockey Nation — diagnostic PRO (Chomelix Cows), 27/11/2026

Sources lues ce tour : `silver.hn_games`, `silver.hn_game_detail.events`, `python -I pipelines/match_engine_etat.py`, `bronze.raw_pages`.
**Incomplet** : la base Supabase est devenue injoignable en cours de session (délai dépassé sur `select 1`, puis « connection timeout » par le connecteur). Le tableau des 10 derniers matchs n'a pas pu être calculé ; la requête prête est en fin de fichier.

## 1. Exports du 27/11 vérifiés en base
- Reçus le 27/11 (10:32–10:33) : Roster, Lineups PRO, Scouting staff et budget, Matchs (programme), 41 pages de match.
- **Absents** : Training (dernier journal 25/11 13:37) et Office > Salary cap (31/10). Déclarés faits, non reçus.
- Les matchs PRO J32 (25/11, à Forest Hills Rangers, D) et J33 (26/11, contre Grande Cache Kings, D) ont `team_level` vide dans `silver.hn_games` : à corriger, sinon les vues par équipe les ignorent.

## 2. Derniers résultats PRO lus (`my_result`)
| jour de saison | date (UTC) | adversaire | résultat |
|---|---|---|---|
| 33 | 26/11 17:15 | Grande Cache Kings (dom.) | D |
| 32 | 25/11 22:30 | Forest Hills Rangers (ext.) | D |
| 31 | 24/11 17:00 | Kocúrkovo HK Rakety (ext.) | D |
Trois défaites de suite : agent `analyste` d'office (charte) — non lancé dans cette session (base injoignable).
Buts pour/contre des 10 derniers matchs : **non calculés** (voir requête).

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
Lecture : l'écart qui ressort est la **réalisation** (la nôtre basse et celle de l'adversaire haute en défaite), pas le volume de tirs. PP, PK et gardien : écarts visibles mais intervalles trop larges pour conclure.

## 4. Les événements portent-ils les joueurs sur la glace ?
**Tirs : oui. Joueurs sur la glace : non.**
Exemple (match 2b841297, J33) : `{"type":"Shot","time":7,"period":1,"teamId":"50cf5f9e-…","shooter":"857d534e-…","goalie":"a946b379-…"}` ; but : `{"type":"Goal","scorer":…,"assists":[…],"strength":"EVEN","emptyNet":false}`.
Clés présentes sur tous les événements en base : `id, num, time, timeAt, period, type, teamId` + selon le type `shooter, goalie, scorer, assists, strength, hitter, victim, winner, loser, giver, taker, blocker, on, penalty, in, out`. Aucune liste des 5 patineurs sur la glace.
→ **+/- et tirs contre par ligne : non calculables.** À capturer en plus : la composition sur la glace à chaque tir et but (liste des joueurs par événement, ou les changements de ligne horodatés). Si le jeu n'affiche nulle part cette information, je ne sais pas comment l'obtenir sans requête supplémentaire (interdit, inviolable 1). Les clés `in`/`out` (41 événements en base) ne sont pas lues : probablement les sorties de gardien, à vérifier.

## 5. Requête à relancer quand la base répond
Par match PRO (10 derniers) : BP, BC, tirs pour/contre (événements Shot+Goal), tirs par période, PP buts/occasions (`strength = 'PP'`, `teams.*.stats.ppAttempts`), PK, buts SH, filet vide, PIM (somme `penalty.minutes`), pertes, prises. Script : `silver.hn_games` filtré sur `'Chomelix Cows' in (home, away)` puis `silver.hn_game_detail` par `game_id` (la jointure directe dépasse le délai).
