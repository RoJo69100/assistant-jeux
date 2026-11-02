# Registre de couverture — Hardwood

Créé le 2026-11-02 (plan de conception iso BasketVibe, `docs/decisions/variables.md` § Mise en route). Chaque ligne de la liste de l'utilisateur pour Hardwood (`docs/chose-a-faire-hardwood.txt`, lignes 4-39) et du bloc « Tous jeux » (`docs/chose-a-faire.txt`, lignes 160-177) → sa réponse et son statut. Statuts : ✅ répondu · 🔧 mécanisme fait, limite connue · ❌ manque, avec le plan. Découvertes en lignes `+N`.

Cartes : `docs/decisions/cartes/hardwood/<type>.md` (achat = sans objet, vente = départs, finances = coachs).

## Global
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 4 | Premier tour de veille | Discord intégral (230 000 messages, 2026-10-30), manuel et doc d'aide → `outputs/hardwood/veille/` (4 fichiers par thème) + 3 skills `hardwood-*` | ✅ |
| 5 | Calendrier, savoir quel jour on est | `gold.hw_today`, `silver.hw_schedule`, skill `hardwood-aujourdhui` | ✅ |
| 6 | Coupe / amical / ligue : paramètres | carte `composition` var. 1 (exhibition = test ; conférence et tournois = Game Plan de référence) | ✅ |
| 7 | Stats de la ligue : meilleurs joueurs | ❌ seule notre page Statistics est exportée ; plan : exporter `/statistics/<id adverse>` des adversaires de conférence au fil des matchs, puis vue gold | ❌ |

## Recrutement / jeunes
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 10 | Fonctionnement du recrutement, points, classes | carte `academie` var. 1-4 ; carte `achat` (pas de transferts) | ✅ |
| 11 | Nombre de joueurs à recruter | carte `academie` var. 5 ; carte `vente` var. 1-2 | ✅ |
| 12 | Recruter ce jeune ? | carte `academie` var. 6-9 | ✅ |

## Finances
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 15 | Aucune notion de finance | carte `finances` var. 5 (seul effet : salaire d'un assistant) | ✅ |

## Équipe
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 18 | Toutes les caractéristiques des joueurs | `gold.hw_effectif` ; carte `entrainement` var. 1 | ✅ |
| 19 | Effet de la fatigue | carte `composition` var. 10 ; carte `defaite` var. 5 (Overwork) | ✅ |
| 20 | Bon à son poste ? sinon lequel | `gold.hw_player_pos_scores`, `gold.hw_player_fit` ; carte `composition` var. 2 | 🔧 pondération des notes par poste [H] |
| 21 | Statistiques des joueurs | `gold.hw_effectif` (g, min, pts, reb, ast…) | ✅ |
| 22 | Blessés ou suspendus | `injury_days` ; pas de suspension dans le jeu (5 fautes = sorti du match) | ✅ |
| 23 | Redshirter un jeune ? | carte `vente` var. 3 | ✅ |

## Entraînement
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 26 | Caractéristiques et entraînement additionnel | carte `entrainement` var. 1-3 | ✅ |
| 27 | Suivre le progrès | carte `entrainement` var. 4 | ✅ |

## Tactique
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 30 | Quelles tactiques | carte `composition` var. 4-8 | ✅ |
| 31 | Composition par poste | carte `composition` § Rendu 1 (`gold.hw_depth_suggest`) | ✅ |
| 32 | Game Tactics | carte `composition` var. 4-9 | ✅ |
| 33 | Game Management | carte `composition` var. 10 | ✅ |
| 34 | Stratégie selon nos matchs contre cet adversaire | carte `composition` var. 11 (`gold.hw_adversaires`) | ✅ |
| 35 | Stratégie selon toute la saison, réussite | carte `composition` var. 12 ; carte `defaite` | ✅ |

## Personnel
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 38 | Head coach et assistants | carte `finances` var. 1-2 | ✅ |
| 39 | Changer de coach : impacts et bénéfices | carte `finances` var. 3-4 | ✅ |

## Tous jeux (`docs/chose-a-faire.txt`)
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 160 | Même ordre que l'écran | cartes `composition`, `entrainement` § Rendu ; hook `forme.py` (hw-recrues, ordre de saisie) | ✅ |
| 161 | Meilleures caractéristiques de chaque joueur | compétences clés par poste (carte `composition` var. 2) | ✅ |
| 162 | Actions claires, aujourd'hui seulement | CLAUDE.md § Horizon | ✅ |
| 163 | Pas de « si », vérifications | R-5 ; hooks ; checks chiffrés | ✅ |
| 164 | Réponses simples, mise en forme | rendu des cartes | ✅ |
| 165 | Des tableaux | rendu des cartes | ✅ |
| 166 | Tout vérifier, apprendre de ses erreurs | `outputs/hardwood/learnings.md` (créé le 2026-11-02 : L-001, L-002, C-001 à C-004) | 🔧 aucun match analysé un par un |
| 167 | Pas d'hypothèse sans vérifier | statuts confirmé / en doute de la veille ; [H] | ✅ |
| 168 | Beaucoup d'argent : que faire | sans objet (pas d'argent) ; levier = recrutement et coachs | ✅ |
| 169 | Beaucoup de défaites : agir | carte `defaite` var. 8 | ✅ |
| 170 | Nouveauté : tester en amical | exhibitions (3 en début de saison) ; carte `composition` var. 1 | 🔧 plus d'exhibition en cours de saison : tester en conférence, un réglage à la fois |
| 171 | Chaque règle parfaite, mine d'or à 100 % | Discord intégral + manuel + doc d'aide | ✅ |
| 172 | Quel export chaque jour, quoi faire après | `gold.hw_exports_state`, `gold.hw_daily_alerts`, skill `hardwood-aujourdhui` | ✅ |
| 173 | Ordre logique, dépendances | `hardwood.yaml` § dependances | ✅ |
| 174 | Mettre à jour agents/skills à chaque nouveauté | veille → skills ; `dossier.py` | ✅ |
| 175 | Retour des joueurs expérimentés | veille (naph7777, furysk, eljefe7705…) ; « avis des amis » des cartes | ✅ |
| 176 | Facteurs cachés | lignes `+N` | ✅ |
| 177 | Export incomplet : le dire | `gold.hw_exports_state`, `gold.sante_collecte`, `gold.exports_nouvelles_cles` | 🔧 `exports_nouvelles_cles` à appliquer en base |

## Règles Hardwood
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| W1 | Walk-ons jamais exportés ni proposés [U] | cartes `composition` var. 3, `vente` var. 1 | ✅ |
| W2 | Recrues : 4 lignes, jamais High, un grand ≥ 2,02 m, engagés retirés [U] | carte `academie` § Rendu, var. 3, 8, 9 | ✅ |

## Découvertes (facteurs cachés)
| Ligne | Fait | Source | Où il sert |
|---|---|---|---|
| +1 | Overwork : près de 40 min sans repos = baisse jusqu'à la fin de la saison | v-joueurs § 2 | carte `composition` var. 10 |
| +2 | Valeurs affichées ±20 % ; elles convergent avec les matchs joués | v-joueurs § 1 | carte `entrainement` var. 4 |
| +3 | Changer de head coach = forte pénalité sur les recrues suivies | v-recrutement § 2 | carte `finances` var. 4 |
| +4 | Points au-delà de 10 non dépensés au dernier jour : divisés par 2 ; plafond 45 | v-recrutement § 1 | carte `academie` var. 1 |
| +5 | La zone est une 3-2 unique ; pression = plus de fautes et de fatigue | v-tactique § 1-2 | carte `composition` var. 6 |
| +6 | Assistant payé 1 M$ ou plus (ou de 50 ans) = head coach la saison suivante | v-calendrier § 5 | carte `finances` var. 5 |
