---
name: reference-hn-plan-de-jeu-libelles
description: "Hockey Nation — libellés officiels du plan de jeu (team playing style) et des instructions en match, donnés par l'utilisateur le 2026-10-29 ; mine d'or à relire avant tout réglage tactique"
metadata:
  node_type: memory
  type: reference
  originSessionId: 0f2646b4-ef59-453b-9697-e4298851915a
  modified: 2026-10-29T16:40:35.789Z
---

Source : texte du jeu collé par l'utilisateur le 2026-10-29. Correspondance export (`gameplan` dans `/team/:id/lineups`) : valeurs 0/1/2 dans l'ordre des libellés [H, à confirmer par un changement test].

| Paramètre (clé export) | Choix 0 / 1 / 2 | Effet |
|---|---|---|
| Mentality (`mentality`) | defensive / balanced / offensive | offensive = plus de chances de marquer mais moins responsable derrière ; defensive sacrifie ses chances pour empêcher les buts |
| Puck Pressure (`puckPressure`) | light / normal / heavy | heavy = plus de vols de palet (takeaways), risque de ne plus tenir les angles de tir ni bloquer |
| Tempo (`tempo`) | slow / normal / fast | fast = plus et meilleures chances, défense exposée, pertes de palet non forcées (giveaways) |
| Aggression (`aggression`) | calm / normal / aggressive | aggressive = plus de mises en échec, plus de pénalités |
| Shift Length (`shiftLength`) | short 35-40 s / normal 41-49 s / long 50-55 s | règle le temps de glace et la perte de condition |
| Pull Goalie 1 goal behind (`pullGoalie1`) | never / sometimes / always | retiré à 1 but de retard dans les 2 dernières minutes ; sometimes = 50 %, standard |
| Pull Goalie 2 goals behind (`pullGoalie2`) | never / sometimes / always | retiré à 2 buts de retard dans les 3 dernières minutes |

Le gardien n'est jamais retiré en infériorité numérique, quand l'adversaire a le palet, ni à moins de 5 secondes de la fin.

In-game instructions (`instructions` dans l'export, tableau vide chez nous) : changent le style selon le temps, le score et les lignes sur la glace ; 10 au maximum ; en cas de conflit la dernière instruction l'emporte (ordre modifiable par glisser-déposer). Les bots, U21 et U17 jouent toujours balanced/normal sans instructions.

Capitaine et assistants : attributs cachés (leadership), non lisibles dans l'export ni à l'écran ; choix par expérience seulement.

**How to apply:** tout réglage du plan de jeu se dit avec ces libellés (jamais « tempo 1 »). Réglage actuel en base : `gold.hn_tactique_plan_rendu`. Voir [[feedback-hn-tactique-rendu-fixe]].
