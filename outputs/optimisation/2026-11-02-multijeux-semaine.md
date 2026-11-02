# Optimisation multi-jeux, 22/10 au 02/11/2026 (53 sessions sur disque)

Mesure : `pipelines/mesure_session.py` (fonctions `analyser`/`usage_total`, agrégées sur les 53 journaux, sous-agents inclus). « Éq. » = unités pondérées : relu x0,1 + écrit x1,25 + sortie x5 + entrée x1. Les sessions du 26, 27 et 28/10 ne sont plus sur disque (le rapport du 27/10 cite une session absente) : la semaine 26/10 est mesurée sur 4 jours (29/10 au 01/11).

## 1. Jours (tous les journaux)
| Jour | Sessions | Relu cache | Écrit cache | Sortie | Agents | Éq. |
|---|---|---|---|---|---|---|
| 22/10 | 3 | 19 M | 0,9 M | 64 k | 7 | 3,4 M |
| 23/10 | 3 | 144 M | 7,2 M | 429 k | 48 | **25,6 M** |
| 24/10 | 3 | 58 M | 4,0 M | 146 k | 39 | 11,5 M |
| 25/10 | 6 | 75 M | 3,6 M | 297 k | 17 | 13,5 M |
| 29/10 | 8 | 80 M | 4,7 M | 475 k | 14 | 16,2 M |
| 30/10 (ven.) | 12 | 131 M | 6,0 M | 711 k | 16 | **24,1 M** |
| 31/10 (sam.) | 8 | 64 M | 3,4 M | 352 k | 5 | 12,4 M |
| 01/11 | 4 | 36 M | 1,7 M | 165 k | 5 | 6,6 M |
| 02/11 | 6 | 37 M | 1,5 M | 141 k | 6 | 6,3 M |

Semaines : 22-25/10 = 53,9 M éq. (4 jours) ; **26/10-01/11 = 59,3 M éq. (4 jours mesurés : 311 M relus, 15,7 M écrits, 1,70 M sortie, 40 agents, 32 sessions)** ; 02/11 seul = 6,3 M. Vendredi 30 (24,1 M, 12 sessions) puis samedi (12,4 M) = 36,5 M en deux jours : c'est ce qui a vidé le quota. Le pic reste le 23/10 (25,6 M, une session de 491 min à 265 %).

## 2. Sessions les plus lourdes (éq.)
| Session | Date | Durée | Contexte max | Agents | Éq. |
|---|---|---|---|---|---|
| 38147e78 | 23/10 | 491 min | 265 % | 30 | 13,9 M |
| 08c2145a | 23/10 | 398 min | 141 % | 16 | 10,3 M |
| 3e03971f | 24/10 | 72 min | 152 % | 34 | 9,9 M |
| a6a6af01 | 25/10 | 403 min | 202 % | 8 | 8,2 M |
| 2a6c3e7a | 31/10 | 105 min | 150 % | 5 | 6,7 M |
| f07efc27 | 30/10 | 136 min | 230 % | 4 | 5,6 M |
| e9f79813 | 29/10 | 98 min | 202 % | 0 | 5,2 M |
| 6207dd4e | 30/10 | 56 min | 151 % | 4 | 4,7 M |

Les 45 autres sessions (tableau par session : relancer le script sur le `.jsonl`) pèsent chacune moins de 4,5 M éq. ; 16 sessions sur 53 dépassent 100 % du contexte de référence (200 k), 8 durent plus de 2 h.

## 3. Cinq plus grosses sources (semaine du 26/10, 59,3 M éq.)
| # | Source | Chiffre |
|---|---|---|
| 1 | Session principale qui relit un contexte gonflé | 22,1 M éq. (37 %) ; 12 sessions sur 32 > 100 %, 25 sur 32 > 30 % sans `/compact` (récidive règle 40) |
| 2 | Agents (général-purpose relisant fiches + attentes + briefs) | 18,1 M éq. (31 %), 40 agents, ~0,45 M éq. chacun. Veilles : 4 à 7,9 M relus pour 86 à 624 tokens de sortie (31/10 : 3 veilles = 15,8 M relus) ; Hardwood veille 7,9 M relus pour 10 k de sortie |
| 3 | Réécriture du cache à chaque nouvelle session / après `/compact` | 10,7 M éq. (18 %) : 32 sessions en 4 jours, chacune repart de CLAUDE.md + mémoire |
| 4 | Sortie (rendus refaits, longues réponses) | 1,70 M tokens = 8,4 M éq. (14 %) ; 29/10 e9f79813 215 k, 30/10 f07efc27 143 k, 78d6b04d 163 k |
| 5 | Gros résultats SQL | 263 résultats > 5 000 car. sur 53 sessions (3,2 M car., ~0,8 M tokens), chacun relu à chaque tour suivant : estimation ~3 M éq. Relectures de fichiers : marginales en session principale (`041_hw_profiles_refs.sql` 4x) ; côté agents, `basketvibe.yaml` lu par 8 agents dans une même passe (rapport du 27/10) |

## 4. Coupes (aujourd'hui seulement)
| Priorité | Constat | Coupe précise | Gain estimé |
|---|---|---|---|
| 🟥 URGENT | Session courante à 46 %, 25/32 sessions > 30 % sans compact | `/clear` dès ce rapport rendu (tâche finie) ; `/compact` à 30 % dans toute session, `/clear` à chaque changement de jeu | ~11 M éq./semaine (moitié de la source 1) |
| 🟥 URGENT | Veilles à 4-8 M relus pour < 700 tokens de sortie | Dans `.claude/agents/veille.md` : lire seulement le delta Discord + les entrées de `connaissance.md` du thème touché (pas le fichier entier, ni `commun.md`) ; une veille par export, jamais trois | ~9 M relus/passage, ~1 M éq. par veille évitée |
| 🟧 IMPORTANT | 40 agents en 4 jours (règle : 3 par passage) | Avant tout lancement, annoncer le nombre (règle Vitesse 3) ; ne lancer aucun agent pour un tableau (vue gold) ; viser 20 agents/semaine | ~9 M éq. (moitié de la source 2) |
| 🟧 IMPORTANT | Gros résultats SQL (263 > 5 000 car.) | Colonnes choisies + `LIMIT 30` systématiques, `left(payload::text, 1500)` jamais plus ; vue gold dédiée dès qu'une requête se répète | ~2 à 3 M éq. |
| 🟧 IMPORTANT | Sorties de 143-215 k tokens dans les sessions de format/tactique | Corriger le rendu en un seul passage (hook `forme.py` déjà en place) au lieu de réécrire ; plafond de 10 lignes hors tableaux | ~3 M éq. |
| 🟩 SUIVI | Sessions de 5 à 8 h (23/10, 25/10) | Une tâche = une session ; au-delà de 90 min, `/compact` proposé | évite les pics > 10 M éq. |

Budget indicatif : viser < 40 M éq. sur une semaine de 4 jours actifs (59 M mesurés) ; avec les trois premières coupes, ~29 M éq. économisés. Comparaison au rapport précédent (27/10, BasketVibe, 85 min, 13 M relus, 9 agents) : non comparable à l'échelle d'une semaine ; la règle « 3 agents au plus » n'a pas tenu (16 agents le 30/10).
