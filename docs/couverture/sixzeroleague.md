# Registre de couverture — Six Zero League

Créé le 2026-11-02 (plan de conception iso BasketVibe, `docs/decisions/variables.md` § Mise en route). Chaque ligne de la liste de l'utilisateur pour Six Zero League (`docs/chose-a-faire.txt`, lignes 56-102) et du bloc « Tous jeux » (lignes 160-177) → sa réponse et son statut. Statuts : ✅ répondu · 🔧 mécanisme fait, limite connue · ❌ manque, avec le plan. Découvertes en lignes `+N`.

Cartes : `docs/decisions/cartes/sixzeroleague/<type>.md` (composition, defaite, achat, vente, entrainement, academie, finances).

## Global
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 59 | Premier tour de veille : règles, Discord, chat | `outputs/sixzeroleague/veille/connaissance.md` (lecture intégrale Discord + chat, 10 thèmes, registre des contradictions) + 6 skills `sixzeroleague-*` | ✅ |
| 60 | Calendrier, savoir quel jour on est | `gold.sz_today`, `gold.sz_agenda`, skill `sixzeroleague-aujourdhui` | ✅ |
| 61 | Coupe / ligue : paramètres de chacune | carte `composition` var. 1 (même tactique ; coupe sur terrain neutre, 17:00) | ✅ |
| 62 | Stats de la ligue : meilleurs joueurs des autres équipes | ❌ pas de vue ; bronze `/seasons/current/teams/<id>/player-stats` (`silver.sz_api`) pour nos joueurs seulement ; statistiques de ligue « idée acceptée, sans date » (connaissance 6.11) ; plan : vue gold dès que l'API les expose | ❌ |
| 63 | Export du chat | `data/chat/sixzeroleague/` + `silver.sz_api` `/chat/messages` | ✅ |

## Jeunes / académie
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 66 | Fonctionnement de l'académie | carte `academie` var. 1-3 | ✅ |
| 67 | Lequel des 2 prospects selon stats, besoin, revente | carte `academie` var. 4-6 | ✅ |

## Finances
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 70 | Solde actuel | carte `finances` var. 1 | ✅ |
| 71 | Dépenses | carte `finances` var. 2 | ✅ |
| 72 | Salaires | carte `finances` var. 3 | ✅ |
| 73 | Entrées d'argent | carte `finances` var. 2 | ✅ |
| 74 | Acheter, infrastructure, rien ? | carte `finances` var. 5, 6, 8 + carte `achat` | ✅ |
| 75 | Quoi faire dans le futur | carte `finances` var. 4 | ✅ |
| 76 | Sponsors : choisir le meilleur | carte `finances` var. 7 | ✅ |

## Équipe
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 79 | Toutes les caractéristiques des joueurs | `silver.sz_players` (20 compétences) | ✅ |
| 80 | Bon à son poste ? sinon lequel | `gold.sz_slot_options`, `role_overalls` ; carte `composition` var. 7 | ✅ |
| 81 | Ce joueur est-il à vendre | carte `vente` var. 1-2 | ✅ |
| 82 | Statistiques des joueurs | `gold.sz_effectif_bilan`, `silver.sz_match_players` | ✅ |
| 83 | Blessés ou suspendus | carte `composition` var. 8 | ✅ |

## Transferts
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 86 | Base « ce type vaut ce prix » | carte `achat` var. 5 | ❌ pas de ventes conclues en base ; plan : relever le prix final des annonces suivies à chaque règlement (export du marché après 21:00) |
| 87 | Étudier le marché, acheter / revendre | carte `achat` var. 1, 9 | ✅ |
| 88 | Faut-il vendre nos joueurs | carte `vente` | ✅ |

## Entraînement
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 91 | Caractéristique à entraîner | carte `entrainement` var. 2, 3 | ✅ |
| 92 | Suivre le progrès | carte `entrainement` var. 4 (`gold.sz_training_progress`) | ✅ |
| 93 | Comprendre le progrès | carte `entrainement` var. 5-7 | ✅ |

## Tactique
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 96 | Quelles tactiques | carte `composition` var. 3-6 | ✅ |
| 97 | Tableau : poste, formations, direction, agressivité, remplacements | carte `composition` § Rendu (`gold.sz_saisie_reglages`, `gold.sz_saisie_tactique`) | ✅ |
| 98 | Ordres de match | carte `composition` var. 9 (ordres 0.6.1, sans remplacement) | 🔧 contenu exact des ordres non relevé à l'écran |
| 99 | Stratégie selon nos matchs contre cet adversaire | carte `composition` var. 2 (`gold.sz_adversaires`) | ✅ |
| 100 | Stratégie selon toute la saison, blessés, réussite | carte `composition` var. 8, 11, 12 ; carte `defaite` | ✅ |

## Tous jeux
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 160 | Même ordre que l'écran | carte `composition` § Rendu (GK, CB, LB, RB, LW, RW, P) ; hook `forme.py` (SZ ordre de saisie) | ✅ |
| 161 | Meilleures caractéristiques de chaque joueur | compétences clés du rôle (`gold.sz_role_report.key_skills`) | ✅ |
| 162 | Actions claires, aujourd'hui seulement | CLAUDE.md § Horizon ; rendu des cartes | ✅ |
| 163 | Pas de « si », vérifications | R-5 ; hooks ; checks chiffrés | ✅ |
| 164 | Réponses simples, mise en forme | rendu des cartes | ✅ |
| 165 | Des tableaux | rendu des cartes | ✅ |
| 166 | Tout vérifier, apprendre de ses erreurs | `outputs/sixzeroleague/learnings.md` (37 leçons, C-001 à C-055) | ✅ |
| 167 | Pas d'hypothèse sans vérifier | registre des contradictions de la connaissance ; « confirmé » à 3 matchs | ✅ |
| 168 | Beaucoup d'argent : que faire | carte `finances` var. 5, 8 | ✅ |
| 169 | Beaucoup de défaites : agir | carte `defaite` var. 11 | ✅ |
| 170 | Nouveauté : tester (pas d'amical) | protocole chiffré en ligue, une option à la fois (A-6) ; carte `composition` | ✅ |
| 171 | Chaque règle parfaite, mine d'or à 100 % | lecture intégrale Discord + chat ; § Delta de la connaissance | ✅ |
| 172 | Quel export chaque jour, quoi faire après | `gold.sz_exports_state`, `gold.sz_agenda` | ✅ |
| 173 | Ordre logique, dépendances | `sixzeroleague.yaml` § dependances ; `enchainement.md` | ✅ |
| 174 | Mettre à jour agents/skills à chaque nouveauté | veille → skills ; `dossier.py` | ✅ |
| 175 | Retour des joueurs expérimentés | connaissance (Stoik, Squidward, pierrottingchrist…) ; « avis des amis » des cartes | ✅ |
| 176 | Facteurs cachés | lignes `+N` | ✅ |
| 177 | Export incomplet : le dire | `gold.sz_exports_state`, `gold.sante_collecte`, `gold.exports_nouvelles_cles` ; `page_type` classé par `source_url` | 🔧 `exports_nouvelles_cles` à appliquer en base |

## Règles Six Zero League
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| S1 | Ne jamais afficher `ownerUsername` (e-mail des autres managers) | `resume.md` § Jeu ; aucune carte ne le lit | ✅ |
| S2 | Pas d'amical, pas de forme, pas de personnel : ne rien transposer de BasketVibe | cartes `composition`, `academie`, `finances` | ✅ |
| S3 | Annulation d'annonce impossible : ne lancer aucune annonce à retirer | cartes `achat`, `vente` | ✅ |

## Découvertes (facteurs cachés)
| Ligne | Fait | Source | Où il sert |
|---|---|---|---|
| +1 | Pénalité de défense selon la place défensive, pas le rôle d'attaque | Gazelle (1.8) | carte `composition` var. 7 |
| +2 | 4-2 d'attaque = pas de CB | Gazelle (1.6) | carte `composition` var. 3 |
| +3 | Remplacement uniquement sur blessure ou rouge ; pas de rotation | wiki + SQL (2.14b, 2.14d) | carte `composition` var. 9 |
| +4 | Un blessé ne reçoit pas de points d'entraînement ; les minutes jouées en donnent | Gazelle (5.3, 5.4) | carte `entrainement` var. 5 |
| +5 | Plage d'un prospect = niveau à 18 + 2 × niveau ; acheter le niveau avant de signer | SQL (3.8) ; fiche académie | carte `academie` var. 2-3 |
| +6 | Re-signer le même sponsor = pas de prime de signature | Gazelle (6.2) | carte `finances` var. 7 |
| +7 | Training Facilities +0,06 par niveau mesuré (Gazelle : +0,04) | SQL (5.8, 3.2) | carte `entrainement` var. 6 |
| +8 | Exclusion → 7 m adverse dans la seconde ; le 1er quart d'heure décide | L-012, L-028 | cartes `composition` var. 6, `defaite` var. 6 |
