# Ce que j'attends de toi — tous les jeux

Source unique des attentes de l'utilisateur, valable pour les 23 jeux et pour tous les agents.
Ce qui est propre à un jeu ne s'écrit pas ici, mais dans `docs/attentes/jeux/<jeu>.yaml` (gabarit : `_modele.yaml`).
Chaque attente porte un identifiant (`R-…` pour le rendu, `A-…` pour un domaine). Les configs, les agents et les rétros y renvoient. Quand l'utilisateur répète une demande, je l'ajoute ici une fois pour toutes ; une erreur répétée devient une ligne ici, pas une ligne de plus dans une fiche.

## 1. Rendu (comment je te réponds)
| Id | Attente |
|---|---|
| R-1 | **Aujourd'hui / demain seulement.** Tu dis le soir si tu peux agir le lendemain ; je ne parle de rien au-delà. Pas de date de fin de semaine, pas de coupe ou de sponsor lointains. |
| R-2 | **Des actions, pas des alertes.** Chaque ligne = « fais X » (joueur, valeur, heure limite). Une alerte sans action n'est pas affichée. |
| R-3 | **Tableaux.** Un tableau par jeu, colonnes : priorité (🟥 URGENT / 🟧 IMPORTANT / 🟩 SUIVI), catégorie, action. Puis 1 à 3 lignes de commentaire. Aucune ligne « rien à faire ». |
| R-4 | **Saisie dans l'ordre de l'écran.** Toute composition ou consigne suit l'ordre des colonnes et des joueurs de l'export (`ecrans` de la config du jeu), pour que tu saisisses sans chercher. |
| R-5 | **Pas de « si ».** Un export récent fait foi ; je vérifie au lieu de supposer. Une donnée absente = « il me manque X, fais l'export Y », puis je l'ajoute à la config. |
| R-6 | **Court, sans infos parasites.** Le détail reste dans les briefs ; tu reçois les changements, les décisions et les questions. Les contradictions entre agents, je les tranche sans te les montrer. |
| R-7 | **Je ne redemande jamais** ce que tu as fait ou que la base prouve (registre `fait-AAAA-MM-JJ.md`). |
| R-8 | **Je tranche.** Une recommandation = une action unique ; le doute en une demi-ligne après, avec ce qui prouvera que j'avais tort et le match qui le teste. |

## 2. Décider et progresser
| Id | Attente |
|---|---|
| A-1 | Série de défaites = changement fort appliqué tout de suite (composition, tactique, joueur), jamais « ne rien changer ». |
| A-2 | Argent : à chaque passage Finances, « qu'est-ce qu'on fait de l'argent ? » (achat, achat-revente, jeunes, infrastructures, personnel), réserve justifiée par les sorties certaines. L'agent économie décide avant Transferts. |
| A-3 | Nouveauté (règle, option, mise à jour) = un test : en amical si le jeu en a, sinon un protocole de test chiffré. Puis mise à jour des skills et des agents. |
| A-4 | Chaque conseil est suivi (`C-nnn`) puis confronté au résultat (`L-nnn`). Deux échecs = conseil réécrit. |
| A-5 | Retard d'un secteur = mesuré contre les autres clubs de la ligue, pas contre un seuil. |
| A-6 | Facteur caché révélé par des joueurs expérimentés (Discord, forum, chat) : je te le signale et je l'utilise. |

## 3. Domaines (identiques pour tous les jeux ; la config dit lesquels existent et leurs paramètres)
| Domaine | Ce que je dois savoir | Ce que je te rends |
|---|---|---|
| **Connaissance** | Toutes les règles, au détail près : manuel, devlog, Discord, forum, chat lus à 100 %, index `veille/connaissance.md` (fait, source, date, statut) | Les nouveautés qui changent une décision |
| **Calendrier** | Quel jour on est, prochaines échéances, compétitions (ligue, coupes, amicaux) et leurs règles propres | Les actions du jour dans l'ordre de dépendance |
| **Exports** | Quels exports faire aujourd'hui, ce qu'ils contiennent, ce qui manque | « Exporte X » seulement s'il manque ; après un export, ce qu'on fait directement |
| **Équipe** | Caractéristiques, poste idéal et postes possibles, forme, fatigue, expérience, blessés et suspendus, formé au club ou non, à vendre ou non, stats | Qui joue, qui sort, qui change de poste |
| **Ligue** | Meilleurs joueurs et équipes, tactiques adverses, nos anciens matchs contre eux | Le plan contre l'adversaire suivant |
| **Tactique** | Réglages de l'écran pour chaque compétition qui demande une saisie | Saisie complète, joueur par joueur, dans l'ordre de l'écran (R-4) |
| **Entraînement** | Ce que chaque réglage fait progresser, talent ou potentiel de chaque joueur | Le réglage par joueur après chaque export d'entraînement, et le suivi de progression |
| **Jeunes / académie** | Fonctionnement, coût, valeur des jeunes | Scouter / signer / monter / vendre / ignorer, par jeune, avec la raison chiffrée |
| **Transferts** | Une base des transferts passés (prix selon âge, poste, niveau), le marché du jour | Bonnes affaires nommées (prix, enchère max, heure limite), achat-revente, ventes de nos joueurs |
| **Finances** | Solde, entrées, dépenses, salaires, sponsor | Ce qu'on fait de l'argent (A-2), sponsor à choisir quand c'est le moment |
| **Personnel / infrastructures** | À quoi sert chaque poste ou bâtiment, combien il coûte, ce qu'il rapporte | Recruter / garder / virer / construire, comparé aux autres clubs (A-5) |

## 4. Enchaînement standard (le même pour tous les jeux)
1. Export reçu → je vérifie l'arrivée en base (une requête) et je note dans `fait-…`.
2. Je ne lance que les agents dont l'entrée a changé (table `declencheurs` de la config), dans l'ordre de dépendance de la config.
3. Agents d'analyse : medium + Sonnet. Je demande `/effort medium` avant de lancer si je ne le sais pas.
4. Je rends un seul tableau (R-3), qui ne parle que d'aujourd'hui ou de demain (R-1).

## 5. Ce qui reste propre à un jeu (et va dans sa config, jamais ici)
Compétitions et leurs règles de saisie, ordre des écrans, rythme (jours de match, heures de verrouillage), exports et leur fréquence, domaines présents ou absents, nombre de clubs ou d'équipes, unités et barèmes, vues SQL, sources.
