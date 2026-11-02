# Registre de couverture — Derby Manager

Créé le 2026-11-02 (plan de conception iso BasketVibe, `docs/decisions/variables.md` § Mise en route). Chaque ligne de la liste de l'utilisateur pour Derby Manager (`docs/chose-a-DM.txt`, lignes 4-67) et du bloc « Tous jeux » (`docs/chose-a-faire.txt`, lignes 160-177) → sa réponse et son statut. Statuts : ✅ répondu · 🔧 mécanisme fait, limite connue · ❌ manque, avec le plan. Découvertes en lignes `+N`. Deux clubs (Queen of the South 547, Marmandes 307) : chaque réponse vaut pour les deux.

Cartes : `docs/decisions/cartes/derbymanager/<type>.md`.

## Global
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 4 | Premier tour de veille : règles, Discord | Discord intégral lu le 2026-10-30 (125 932 messages) → `outputs/derbymanager/veille/connaissance.md` + 4 skills `derbymanager-*` | ✅ |
| 5 | Calendrier, savoir quel jour on est | `silver.dm_fixtures` | 🔧 pas de calendrier à venir exporté ni de vue « aujourd'hui » ; plan : exporter Competitions / Matches de la saison 27 |
| 6 | Coupe / amical / ligue : preset en ligue et coupe, tests en amical | carte `composition` var. 1 | ✅ |
| 7 | Stats de la ligue : meilleurs joueurs | ❌ pas de vue ; plan : « scouter une équipe entière coûte 1 scout » (bouton de la page des matchs, connaissance § 8) puis vue gold sur ces rapports | ❌ |
| 8 | Gérer deux équipes distinctes | rendu de toutes les cartes (un bloc par club) ; hook `forme.py` (DM clubs) | ✅ |

## Jeunes / school
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 11 | Fonctionnement de la school, durée, choix, progression | carte `academie` var. 1-4 | ✅ |
| 12 | Scouter le jeune ? | carte `academie` var. 6 | ✅ |
| 13 | Intégrable après scout ? | carte `academie` var. 5 | ✅ |

## Finances
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 16 | Solde actuel | carte `finances` var. 1 | ✅ |
| 17 | Dépenses | carte `finances` var. 2 | ✅ |
| 18 | Salaires | carte `finances` var. 3 | ✅ |
| 19 | Entrées d'argent | carte `finances` var. 2 | ✅ |
| 20 | Acheter un joueur ? rien ? | carte `finances` var. 4, 8 + carte `achat` | ✅ |
| 21 | Quoi faire dans le futur | carte `finances` var. 5 | 🔧 pas de projection de fin de saison |

## Équipe
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 24 | Toutes les caractéristiques des joueurs | `gold.dm_effectif` (16 compétences) | ✅ |
| 25 | Effet du sharpness | `resume.md` § Pièges (glossaire) ; carte `composition` var. 7 | ✅ |
| 26 | Effet de la condition | carte `composition` var. 7 (blessure ≈ condition manquante) | ✅ |
| 27 | Effet de la forme | carte `composition` var. 7 ; L-003 | ✅ |
| 28 | Le POT | carte `entrainement` var. 3 | ✅ |
| 29 | Le FIT | glossaire (`resume.md`) : vitesse de perte de condition | ✅ |
| 30 | Le SKILL | glossaire : niveau relatif dans l'équipe | ✅ |
| 31 | BU et PBU | carte `composition` var. 11 | ✅ |
| 32 | Bon à son poste ? sinon lequel | `gold.dm_verdict_joueurs.note_poste`, `gold.dm_poste_scores` [H] | 🔧 notes par poste sur compétences clés supposées |
| 33 | Ce joueur est-il à vendre | carte `vente` var. 1 | ✅ |
| 34 | Statistiques des joueurs | `gold.dm_effectif` (`apps`, `goals`, `assists`, `rating`) | ✅ |
| 35 | Blessés ou suspendus | `gold.dm_setpieces.blessure` ; `gold.dm_verdict_joueurs` | 🔧 suspensions non lues explicitement |
| 36 | Rapports sur un joueur (futur, actuel) | `silver.dm_player_tips` ; rapport de potentiel du scouting (connaissance § 8) | ✅ |
| 37 | Analyse des match reports | carte `defaite` | ✅ |

## Transferts
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 40 | Base « ce type vaut ce prix » | `gold.dm_prix_reference` ; carte `achat` var. 4 | ✅ |
| 41 | Étudier le marché, acheter / revendre | carte `achat` var. 1, 2 | ✅ |
| 42 | Faut-il vendre nos joueurs | carte `vente` | ✅ |
| 43 | Faut-il scouter ce joueur | carte `achat` var. 3 | ✅ |

## Entraînement
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 46 | Caractéristiques à entraîner | carte `entrainement` var. 1 | ✅ |
| 47 | Suivre le progrès | carte `entrainement` var. 4 | ✅ |
| 48 | Comprendre le progrès, talent | carte `entrainement` var. 2, 3 | ✅ |
| 49 | Mentor | carte `entrainement` var. 7 | ✅ |
| 50 | Intensité | carte `entrainement` var. 5 | ✅ |
| 51 | Satisfaction | carte `entrainement` var. 8 ; carte `vente` var. 3 | ✅ |
| 52 | Lien avec le pot de l'équipe | carte `entrainement` var. 3 | ✅ |
| 53 | Entraînement par poste | carte `entrainement` var. 1 (par groupe) | ✅ |

## Tactique
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 57 | Quelles tactiques (442, 343…) | carte `composition` var. 3 | ✅ |
| 58 | Curseurs et options | carte `composition` var. 5, 6 | ✅ |
| 59 | Set pieces, remplaçants, capitaine | carte `composition` var. 8, 9 | ✅ |
| 60 | Tableau : poste, set pieces, tactique | carte `composition` § Rendu | ✅ |
| 61 | Stratégie selon nos matchs contre cet adversaire | carte `composition` var. 2 (`gold.dm_adversaires`) | ✅ |
| 62 | Stratégie selon toute la saison, blessés, forme, réussite | carte `composition` var. 7, 10 ; carte `defaite` | ✅ |

## Infrastructures
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 66 | Comprendre tous les bâtiments | carte `finances` var. 6 ; carte `entrainement` var. 1 (3 installations d'entraînement) | ✅ |
| 67 | Les augmenter ou non | carte `finances` var. 6-8 | 🔧 effet chiffré d'un niveau non publié par le développeur |

## Tous jeux (`docs/chose-a-faire.txt`)
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 160 | Même ordre que l'écran | carte `composition` § Rendu (ordre de l'écran Squad) ; hook `forme.py` (DM clubs + set pieces) | ✅ |
| 161 | Meilleures caractéristiques de chaque joueur | `gold.dm_verdict_joueurs` | ✅ |
| 162 | Actions claires, aujourd'hui seulement | CLAUDE.md § Horizon | ✅ |
| 163 | Pas de « si », vérifications | R-5 ; hooks ; checks chiffrés | ✅ |
| 164 | Réponses simples, mise en forme | rendu des cartes | ✅ |
| 165 | Des tableaux | rendu des cartes | ✅ |
| 166 | Tout vérifier, apprendre de ses erreurs | `outputs/derbymanager/learnings.md` (créé le 2026-11-02 : L-001 à L-004, C-001 à C-008) | 🔧 aucun match analysé un par un |
| 167 | Pas d'hypothèse sans vérifier | statut confirmé / en doute de la connaissance ; [H] | ✅ |
| 168 | Beaucoup d'argent : que faire | carte `finances` var. 4, 6, 8 | ✅ |
| 169 | Beaucoup de défaites : agir | carte `defaite` var. 9 | ✅ |
| 170 | Nouveauté : tester en amical | carte `composition` var. 1 | ✅ |
| 171 | Chaque règle parfaite, mine d'or à 100 % | Discord intégral (2026-10-30) ; § Questions encore ouvertes de la connaissance | 🔧 questions ouvertes (prix d'un scout, effet d'un niveau) |
| 172 | Quel export chaque jour, quoi faire après | `gold.dm_exports_etat` | ✅ |
| 173 | Ordre logique, dépendances | `resume.md` § Ordre des agents | 🔧 pas de config `docs/attentes/jeux/derbymanager.yaml` (dépendances) |
| 174 | Mettre à jour agents/skills à chaque nouveauté | veille → skills ; `dossier.py` | ✅ |
| 175 | Retour des joueurs expérimentés | connaissance ; « avis des amis » des cartes | ✅ |
| 176 | Facteurs cachés | lignes `+N` | ✅ |
| 177 | Export incomplet : le dire | `gold.dm_exports_etat`, `gold.sante_collecte`, `gold.exports_nouvelles_cles` | 🔧 `exports_nouvelles_cles` à appliquer en base |

## Découvertes (facteurs cachés)
| Ligne | Fait | Source | Où il sert |
|---|---|---|---|
| +1 | Chaque option tactique cochée = −1 % de condition pour tous | `resume.md` § Écrans | carte `composition` var. 6 |
| +2 | La forme ne monte qu'en jouant : tourner tout l'effectif la fait baisser | dev 2026-10-21 ; L-003 | carte `composition` var. 7 |
| +3 | Blessure ≈ condition manquante (à 70 % : 30 %) | connaissance § 3 | carte `composition` var. 7 |
| +4 | Transfer-lister un mécontent depuis 24 h annule sa pénalité | connaissance § 4 | carte `vente` var. 3 |
| +5 | L'export du marché suit le filtre de prix de l'écran | `resume.md` § Pièges ; L-004 | carte `achat` var. 2 |
| +6 | Installations −1 niveau à −5 M ; le conseil investit seul entre 20 et 50 M | dev 2026-08-24 | carte `finances` var. 6 |
| +7 | TR : −1 à 20 min jouées, −2 à 45 min, retombe à 1 à 75 min | dev 2026-10-25 | carte `entrainement` var. 6 |
| +8 | « Oldies are really worth it » : Solid 31+ à 8,0 M contre 11,1 M à 24-27 ans | dev 2026-10-05 ; `gold.dm_prix_reference` | carte `achat` var. 4 |
