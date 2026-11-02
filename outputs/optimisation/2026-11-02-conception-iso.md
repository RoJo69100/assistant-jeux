# Mesure de session — 7ec7ae02-70a8-4aac-8202-0c43b71152cf.jsonl

Durée 37.9 min · 110 requêtes · contexte max 495,531 (247 %) · relu en cache 29,591,628 · écrit en cache 441,597 · sortie 169,587

## Par demande de l'utilisateur
| # | Demande | Durée (min) | Requêtes | Contexte max | Relu en cache | Sortie | Outils | Agents |
|---|---|---|---|---|---|---|---|---|
| 1 | Fais 0d | 4.6 | 26 | 146,060 | 3,079,206 | 22,222 | Bash×22, Write×3 | 0 |
| 2 | On attaque Hockey Nation | 7.0 | 27 | 235,547 | 5,261,448 | 34,258 | Bash×25, Write×9 | 0 |
| 3 | On attaque Team Soccer | 5.8 | 14 | 303,299 | 3,734,729 | 30,249 | Bash×11, Write×9 | 0 |
| 4 | On attaque Six Zero League | 5.2 | 14 | 370,176 | 4,768,088 | 27,101 | Bash×12, Write×9 | 0 |
| 5 | On attaque Derby Manager | 6.8 | 12 | 432,417 | 4,771,970 | 27,949 | Write×10, Bash×9, Read×1 | 0 |
| 6 | On attaque Hardwood | 5.4 | 9 | 481,406 | 4,070,279 | 22,902 | Write×10, Bash×6 | 0 |
| 7 | Rattache les 11 leçons BasketVibe aux cartes | 2.8 | 5 | 491,676 | 2,428,218 | 4,001 | Bash×4 | 0 |
| 8 | Fais la rétro et la mesure de session | 0.2 | 3 | 495,531 | 1,477,690 | 905 | Bash×2, Skill×1 | 0 |

## Agents (journaux des sous-agents)
| Agent (début de la demande) | Durée (min) | Requêtes | Relu en cache | Sortie | Fichiers lus | Relus 2× ou plus |
|---|---|---|---|---|---|---|

## Fichiers lus par plusieurs agents (candidats à un résumé partagé)

## Fichiers relus dans la session principale

## Résultats SQL les plus lourds (caractères ajoutés au contexte)

## Coupes
| Priorité | Constat chiffré | Coupe précise | Gain estimé |
|---|---|---|---|
| 🟥 URGENT | Contexte max 495 k ; relu en cache 3,1 M (demande 1) → 4,8 M (demandes 4-5) : chaque jeu relit les précédents | `/clear` entre deux jeux (CLAUDE.md règle 14, regles-apprises 71) | ≈ 15 M relus sur cette session (demandes 2-7 à ~2,5 M chacune au lieu de 3,7-5,3 M) |
| 🟧 IMPORTANT | Lecture des sources de chaque jeu par `sed`/`grep` larges (connaissance DM : 32 Ko d'un coup) | Lire la connaissance par section ciblée (`grep -A` sur le thème de la carte) | ≈ 10 k tokens par jeu |
| 🟩 SUIVI | 0 agent, 0 SQL lourd : coût dominé par le contexte, pas par les outils | rien à couper côté agents | — |

Comparaison avec `2026-11-02-multijeux-semaine.md` (semaine à 59,3 M éq.) : cette session fait 29,6 M relus sans agent ; le levier restant est le `/clear` entre jeux.
