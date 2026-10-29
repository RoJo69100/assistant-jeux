---
name: hockeynation-match-calendrier
description: Règles Hockey Nation sur les matchs, les lignes et la saison — ligues (20 équipes, 2 conférences, 4 niveaux), 30 matchs, rival, playoffs au meilleur des 5, montée et descente, lignes A/B/C, pénalités (mauvais poste −20 %, gardien fatigué, amateurs, dépassement du plafond −30 %), condition, fatigue des gardiens, remplacement du gardien, mises au jeu, capitanat, bagarres, tirs au but, amicaux ; calendrier de 63 jours et fenêtres d'échanges. À charger pour composer les lignes, analyser un match ou dater une action.
---

# Hockey Nation — matchs, lignes et calendrier

Sources : **[G:Competitions]**, **[G:Lineups]**, **[G:Trades]**, **[G:Calendar]** (guide du 30/09/2026, lu le 2026-10-23).

## Compétitions
- 15 ligues : 1 (niveau 1), 2, 4, 8 ; 20 équipes en 2 conférences (Est, Ouest).
- 30 matchs en 35 jours : 18 dans la conférence, 10 contre l'autre conférence, 2 contre le **rival** (1er et dernier match). Top 4 de chaque conférence en playoffs, séries au meilleur des 5.
- Les 2 finalistes montent, les 2 derniers de chaque conférence descendent.
- Amicaux : jours 1-7 et 43-63, un par jour ; FRM, U21, U17 seulement pour les comptes premium ; pas d'expérience gagnée.

## Lignes (PRO)
- 3 lignes A, B, C (A par défaut) ; modifiables jusqu'à 1 h avant le match. Lignes invalides corrigées automatiquement (amateurs si besoin).
- Pénalités (cumul plafonné à 30 %) : **mauvais poste −20 %** ; gardien fatigué −20 % ; chaque amateur −5 % pour toute l'équipe ; dépassement des dépenses −30 % (hors amicaux).
- Condition : 100 % au départ, baisse à chaque présence selon END ; une condition de 80 % = compétences à 80 %. Une grosse mise en échec retire 1 à 3 % non récupérables.
- Gardien : perd de la condition à chaque tir ; **fatigué** après autant de matchs d'affilée que son END (saison régulière seulement) : il ne peut pas débuter le suivant. Remplacé automatiquement si fatigué, ou mené de 3 buts en 1re période, 4 en 2e, 5 en 3e, ou 3 buts encaissés à moins de 60 % d'arrêts (jamais dans les 5 dernières minutes).
- Mises au jeu : les 2 attaquants avec le meilleur FOF, surtout le meilleur.
- Capitaine et assistants : expérience + leadership caché ; le leadership des vétérans aide à gagner les duels.
- Bagarres : les moins disciplinés ; issue selon PWR et expérience ; une victoire donne un bonus temporaire ; plus fréquentes contre le rival.
- Tirs au but : les meilleurs tireurs, le meilleur en premier.

## Calendrier (63 jours) — `gold.hn_calendar`
| Jour | Événement |
|---|---|
| 1 | âge +1, draftés en U21, fenêtre I et agents libres ouverts, plafond annoncé en hausse ou baisse |
| 3 | Frenzy des agents libres, 1res réponses des coachs |
| 4 | début du scouting |
| 8 | 1re journée, 1re paie |
| 10, 20, 30 | demandes des agents libres révisées |
| 28 | fourchette du plafond suivant |
| 35 | **fermeture fenêtre I et agents libres (21:00 CET)** : effectifs gelés, fin des embauches de coachs et des activations de contrat |
| 42 / 43 | dernière journée, dernière paie / fin de saison régulière |
| 44 | playoffs |
| 49 | Import Draft |
| 51 → 61 | fenêtre II (21:00 CET) ; un joueur reçu en fenêtre I ne peut pas y être échangé |
| 57 | plafond officiel de la saison suivante |
| 63 | Youth Draft (pré-instructions 1 h avant) |

## Échanges [G:Trades]
- PRO, U21 et choix de draft échangeables, après les avoir marqués disponibles ; un agent libre signé ne s'échange pas dans sa 1re saison.
- Chaque échange accepté passe devant un comité de 21 votants (24 h, décision finale) ; traité à la 2e mise à jour quotidienne ; échanges de choix seuls traités tout de suite.
- Équipe au-dessus du plafond : aucun échange qui augmente sa masse salariale.

## Vues
`silver.hn_lineups`, `silver.hn_games`, `silver.hn_game_detail`, `silver.hn_standings`, `silver.hn_trades`, `silver.hn_market_players`, `gold.hn_calendar`, `gold.hn_daily_alerts`.

## [Veille 2026-10-29] Mises à jour (V-20261029-8, -9)
- **Lignes** : une modification est prise en compte tout de suite, mais **au moins 1 h avant le match**, sinon risque de −30 % aux compétences (hnadmin, 2025-07-10). **Amical** : la pénalité de mauvais poste s'applique, seule la pénalité de plafond est désactivée, et le mauvais poste ne touche que le joueur concerné (d0ghouse, 2026-10-28 11:06/12:59). Les amicaux ne donnent pas d'expérience (krusher_kev, 2026-10-05, avis). [Discord #general ; V-8]
- **Capitaine** : leadership + expérience, limité à 3 joueurs (C + 2 A), plus d'expérience est mieux (d0ghouse, 2026-08-24 19:32). Le temps de glace maximal des défenseurs a été réduit dans une version passée (date non précisée) ; « tout joueur peut jouer 25-30 min quel que soit END » (d0ghouse, 2026-05-11 20:27, portée à vérifier). [Discord #general ; V-9]

## [Veille intégrale 2026-10-29] Condition, plan de jeu, plafond, amicaux (V-A-5 à A-7, A-21, V-B-3, V-C-13)
- **Condition** : mise à jour après chaque présence pour un patineur, toutes les 30 s pour un gardien ; une grosse mise en échec subie ne se récupère pas à l'entracte ; END bas = plus de condition perdue (≈ 60 % à la fin des 20 min). **Gardiens** : chaque match joué, même partiel, réduit le compteur de fatigue de 1 ; remplaçant qui joue = un repos mais fatigue un match plus tôt ; END 0 ou 1 = un seul match ; reposés et sans fatigue en playoffs. [hnadmin 2022-02-21, 2025-04-30 ; d0ghouse 2022-07-31, 2023-11-21, 2025-11-10 ; V-A-5]
- **Temps de glace des défenseurs** : réduit (≈ 2 min pour la 1re paire au patch du 2024-09-09, réduit avant le 2024-05-13) et perte de condition augmentée ; hnadmin 2026-10-28 : le facteur décroissant est « peut-être trop agressif », il va le retoucher — suivre le prochain patch. [V-A-5, B-3]
- **Plan de jeu** : une instruction vaut pour l'unité sur la glace (ex. L2 + paire 3) ; « Against » cible une ligne adverse ; en cas de conflit **la dernière instruction de la liste gagne** ; « Def Pair 1 » sans précision = toutes les combinaisons. Aucun effet chiffré des réglages n'a été donné. [hnadmin 2025-06-16 ; d0ghouse 2022-08-16, 2023-04-01 ; V-A-6]
- **Plafond et match** : les matchs sont simulés 1 h avant avec les lignes de cet instant (postes vides remplis par des joueurs hors lignes) ; amicaux sans pénalité de plafond depuis S9 (en 2023 elle s'appliquait aux amicaux de pré-saison) ; coût journalier d'un échange = différence des salaires totaux / 35 jours de paie. Amateurs : −5 % de toutes les compétences par amateur (guide cité 2024-10-01). [d0ghouse 2025-09-03, 2026-10-28 ; hnadmin 2023-08-23 ; V-A-7, B-3]
- **UA Cup** : équipe copiée (autres ID) ; les lignes A, B, C sont copiées à la fermeture des inscriptions (jour 36), A par défaut ; tout changement du PRO après le jour 36 n'est pas repris. [hnadmin 2025-09-25, 2026-03-31 ; V-A-21]
- **Amicaux de pré-saison S23 (avis jakkysosa 2026-02-15)** : PRO jours 1 et 7, FRM jours 2, 4, 5, 6, 7, U21 jours 1, 3, 4, 5, 7 ; à comparer à `gold.hn_calendar` S27. Non tranché : rétrograder dans l'heure avant un match pour redevenir positif ; moment exact de la libération de plafond après rétrogradation. [V-C-13]
- **Stats** : des buts attendus (xG) existent (stillnoah75 2026-03-02), à chercher dans `silver.hn_game_detail`. [V-C-7]
