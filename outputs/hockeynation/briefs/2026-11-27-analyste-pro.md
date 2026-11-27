# Analyste PRO — série J31-J33 (27/11/2026)

Sources lues ce tour : `silver.hn_games` (my_result, team_level), `silver.hn_game_detail.events` par game_id, `diagnostic-2026-11-27.md`, `resume.md`. Événements : Shot+Goal = tirs ; Penalty compté pour l'équipe sanctionnée (hypothèse, cohérente avec PIM 56 contre 88).
Limite honnête : plafond d'appels atteint. NON analysés : joueur par joueur (boxscore/+/-), minutes des séries, gardien par match, joueurs clés adverses, composition/réglages d'un match à l'autre. Voir « Il me manque ».

## 1. Par période (nous / eux)
| match | P1 | P2 | P3 | prol./TaB |
|---|---|---|---|---|
| J31 0-6 (ext.) | tirs 13-14, buts 0-4 (4 buts à forces égales) | 11-5, 0-1 | 12-10, 0-1 | — |
| J32 3-3, TaB perdu (ext.) | 10-9, 0-0 | 13+3 buts / 14+2, 3-2 | 9-20, 0-1 (but en PP contre, 2 pén. nôtres) | 3-3 tirs, perdu aux TaB |
| J33 3-3, TaB perdu (dom.) | 16-13, 0-0 | 22-9, 2-3 | 5-9, 1-0 | 3-1 tirs, perdu aux TaB |
Totaux tirs : J31 36-29 ; J32 38-48 ; J33 46-32.
- J31 : défaite par la réalisation adverse (6/29 = 20,7 %) et zéro but sur 36 tirs, dont 4 supériorités (0 but). Tout se joue en P1 (0-4 sur 14 tirs).
- J32 : on menait 3-2 après P2, puis P3 à 9 tirs contre 20, égalisation en PP adverse, tirs au but perdus. Seul match de la série avec un effondrement de volume.
- J33 : on domine (+14 tirs), 3 buts encaissés en P2 sur 9 tirs, égalisation, tirs au but perdus.
- Discipline : J31 1 pén. nôtre / 4 adverses ; J32 3 / 5 ; J33 3 / 2. Nos PP : 1 but sur 11 occasions ; PP adverse : 1 but sur 7.

## 2-4. Séries, joueurs, adversaire
Non fait (voir « Il me manque »). Seule série vue par période : 0-4 de P1 en J31. Les minutes exactes sont dans `time` des événements Goal : non extraites.

## 5. Comparaison saison (PRO, ligue, toutes matchs en base : 26 D, 30 V ; ≠ du registre à 24 matchs, filtre de saison différent)
| mesure | défaites | victoires | sépare ? |
|---|---|---|---|
| tirs nous / eux (moy.) | 36,5 / 33,5 | 42,3 / 28,2 | oui (écart +3 contre +14) |
| réalisation nous / eux | 7,6 % / 13,5 % | 13,0 % / 8,4 % | oui (mais mélange hasard et gardien) |
| pénalités nous / eux | 2,7 / 4,3 | 2,8 / 4,5 | ne sépare pas |
| pertes de rondelle nous / eux | 7,9 / 7,9 | 8,4 / 8,3 | ne sépare pas |
Défaites avec tirs au but : 12 buts de TaB comptés sur les 26 défaites, résultat à pile ou face, non exploitable.
Série J31-J33 contre la moyenne des défaites : volume +7, −10, +14 (meilleur que la moyenne des défaites sur 2 matchs sur 3) ; réalisation nous 0 % / 7,9 % / 6,5 % (3/38, 3/46) = en dessous de nos 13 % de victoires.

## Échelle de la charte
1. Composition : pas de signal chiffré dans ces données (volume de tirs correct). Non testable sans +/- par joueur.
2. Tactique : le volume de tirs n'est mauvais qu'en J32 P3 (9-20). Discipline et pertes ne séparent pas. Pas de preuve contre le plan.
3. Force relative : adversaires non étudiés ce tour ; en 2 matchs sur 3 on les domine en tirs.
4. Hasard : dominant. Deux défaites aux tirs au but, 0/36 en J31, réalisation 6,5-7,9 % contre 13 % attendu. PP 5/36 sur 10 matchs, IC 6-29 % : trop large pour conclure.

## Pouvait-on gagner ?
- J31 : oui en volume (36-29), mais 4 buts en P1 sur 14 tirs : non réaliste de le dire « évitable » sans voir le gardien. Moyenne confiance.
- J32 : oui, menait 3-2 ; l'effondrement P3 est la seule trace tactique possible. Confiance faible sur la cause.
- J33 : oui, +14 tirs, perdu aux tirs au but : hasard.

## Changer la structure : NON
Preuve : la structure produit un écart de tirs positif dans 2 défaites sur 3 et dans 30 victoires (+14) ; ce qui sépare victoires et défaites est la réalisation, pas un réglage mesuré. n = 3 matchs de série, 56 en saison ; IC du registre trop large (PP, PK, gardien : « indéterminé »). Série de défaites = « changement fort » (attente utilisateur) : voici ce que je recommande sans toucher à la structure.

## Points d'amélioration
| # | réglage exact (aujourd'hui, avant verrouillage 28/11 23:45) | chiffre | confiance | prouvé faux si |
|---|---|---|---|---|
| 1 | Ne pas changer lignes ni plan pour Roswell Puck 29/11 | +7/−10/+14 tirs ; réalisation 6,5 % | moyenne | écart de tirs < 0 sur Roswell et les 2 matchs suivants (29/11 et suivants) |
| 2 | **Test** : shift length short → normal (Plan de jeu, vérifier le réglage actuel à l'écran) | J32 P3 9-20 ; registre : 3,41 contre 3,36 BC/match, « indéterminé » | faible | tirs en P3 nôtres ≥ P1-P2 sur les 5 prochains matchs avec « short » ou sans amélioration avec « normal » (compter par `periods`) |
| 3 | Corriger `team_level` = PRO de J32 et J33 dans `silver.hn_games` | diagnostic §1 | élevée (donnée) | — |
| 4 | Fournir export Training (dernier journal 25/11) | diagnostic §1 | élevée | — |
| 5 | PP : ne rien changer tant que n < 87 supériorités ; lire `gold.hn_saisie_lignes` PP1/PP2 pour contre-emploi | PP 1/11 série, 5/36 sur 10 matchs | faible (test) | PP ≥ 15 % sur les 30 prochaines supériorités |

## Il me manque
- Joueur par joueur (boxscore, +/−, pertes, minutes) pour les nôtres et 2-3 adverses : à lire dans `silver.hn_game_detail.boxscore` (clé = id joueur, champs pim, toi…) et `players` (home/away) par game_id.
- Gardien par match (arrêts) : `events` Shot/Goal avec `goalie`.
- Réglages et compositions du match précédent : `gold.hn_saisie_lignes` ne garde que la saisie actuelle.

## Propositions
- C-à numéroter : fixer `team_level` PRO automatiquement à l'import (J32, J33 vides).
- C-à numéroter : ne pas tirer de conclusion tactique d'une défaite aux tirs au but (hasard) ; distinguer « D prolongation/TaB » dans `my_result` ou un champ, pour séparer les séries.
- L-à numéroter (hypothèse) : sur 56 matchs, pertes et pénalités ne séparent pas V et D ; tirs et réalisation oui.
