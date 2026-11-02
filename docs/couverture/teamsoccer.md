# Registre de couverture — Team Soccer

Créé le 2026-11-02 (plan de conception iso BasketVibe, `docs/decisions/variables.md` § Mise en route). Chaque ligne de la liste de l'utilisateur pour Team Soccer (`docs/chose-a-faire.txt`, lignes 104-157) et du bloc « Tous jeux » (lignes 160-177) → sa réponse et son statut. Statuts : ✅ répondu · 🔧 mécanisme fait, limite connue · ❌ manque, avec le plan. Découvertes en lignes `+N`. **Deux clubs** (Chomelix Cows, Ben Ahmed Donkey) : chaque réponse vaut pour les deux.

Cartes : `docs/decisions/cartes/teamsoccer/<type>.md` (composition, defaite, achat, vente, entrainement, academie, finances).

## Global
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 107 | Premier tour de veille : règles, forum, chat | `outputs/teamsoccer/veille/connaissance.md` (forum lu en entier le 2026-10-27 : 936 messages) + 6 skills `teamsoccer-*` ; pas de Discord | ✅ |
| 108 | Calendrier, savoir quel jour on est | `gold.ts_today`, `gold.ts_agenda`, `gold.ts_season_calendar`, skill `teamsoccer-aujourdhui` | ✅ |
| 109 | Compétitions (coupe, amical, ligue, coupes européennes) et paramètres pour chacune | skill `teamsoccer-saison` ; carte `composition` var. 1, 16 | ✅ |
| 110 | Stats de la ligue : meilleurs joueurs des autres équipes | ❌ pas de vue ; bronze `player_league_stats_per_*` capté (checklist) ; plan : vue `gold.ts_league_top_players` sur le modèle de `gold.bv_league_top_players` (conception, Opus) | ❌ |
| 111 | Export du forum | `userscripts/teamsoccer.user.js` → `silver.ts_forum_posts` | ✅ |
| 112 | Badges de couleur : sens et comment s'améliorer | ❌ `teamsoccer.yaml` § indicateurs « à relever » ; on le réunit par une capture de l'écran qui les montre + recherche forum par la veille | ❌ |

## Jeunes / académie
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 115 | Fonctionnement de l'académie (3 révélations par jour) | carte `academie` var. 1, 5 | ✅ |
| 116 | Monter un jeune ou non | carte `academie` var. 3 (`gold.ts_academie_verdict`) | ✅ |
| 117 | Le monter pour le vendre ? | carte `academie` var. 4 + carte `vente` var. 3 | 🔧 blocage de revente d'un promu inconnu |

## Finances
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 120 | Solde actuel | carte `finances` var. 1 | ✅ |
| 121 | Dépenses | carte `finances` var. 2 | ✅ |
| 122 | Salaires | carte `finances` var. 1-2 (`wage_bill`) | ✅ |
| 123 | Entrées d'argent | carte `finances` var. 3 | ✅ |
| 124 | Acheter un joueur, une infrastructure, rien ? | carte `finances` var. 5-7, 11 + carte `achat` | ✅ |
| 125 | Quoi faire dans le futur | carte `finances` var. 4 | 🔧 projection sans primes ni coupes |
| 126 | Sponsors | pas de sponsor dans ce jeu (connaissance 2.8) ; carte `finances` var. 10 | ✅ |

## Équipe
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 129 | Toutes les caractéristiques des joueurs | `silver.ts_players` (10 compétences), `gold.ts_effectif_bilan` | ✅ |
| 130 | Joueur de l'académie ou non | carte `academie` var. 7 | 🔧 champ d'origine non lu explicitement |
| 131 | Effet de la Forme | carte `composition` var. 8, carte `entrainement` var. 3 | ✅ |
| 132 | Bon à son poste ? sinon lequel | `sous_role`, `key_skill` (`gold.ts_effectif_bilan`) ; carte `composition` var. 7 | ✅ |
| 133 | Ce joueur est-il à vendre | carte `vente` var. 1 | ✅ |
| 134 | Statistiques des joueurs | `gold.ts_player_match_ratings` | ✅ |
| 135 | Blessés ou suspendus | carte `composition` var. 9 | ✅ |

## Transferts
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 138 | Base « ce type vaut ce prix » | carte `achat` var. 6 (`silver.ts_player_snapshots`, prix ≈ 0,99 × valeur) | 🔧 pas de base des ventes passées (yaml `base_transferts` : à créer) |
| 139 | Étudier le marché, acheter / revendre | carte `achat` var. 1, 7 | ✅ |
| 140 | Faut-il vendre nos joueurs | carte `vente` | ✅ |

## Entraînement
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 143 | Compétence et intensité par joueur | carte `entrainement` var. 1-5 | ✅ |
| 144 | Suivre le progrès | carte `entrainement` var. 6 (`gold.ts_player_progress`) | ✅ |
| 145 | Comprendre le progrès | carte `entrainement` var. 3, 5, 7 | ✅ |

## Tactique
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 148 | Quelles tactiques | carte `composition` var. 4-5 | ✅ |
| 149 | Tableau joueurs, postes, remplacements et quand | carte `composition` § Rendu 3-4 | ✅ |
| 150 | 5 zones × dégager / passer / dribbler / centrer / tirer | carte `composition` var. 6 | ✅ |
| 151 | Consigne de jeu | carte `composition` var. 5 | ✅ |
| 152 | Stratégie selon nos matchs contre cet adversaire | carte `composition` var. 2 (`gold.ts_adversaires`) | ✅ |
| 153 | Stratégie selon toute la saison, blessés, Forme, réussite | carte `composition` var. 3, 8, 9, 17 ; carte `defaite` | ✅ |

## Personnel
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 156 | À quoi sert chaque personnel | pas de personnel hors entraîneur (fiche finances) ; carte `finances` var. 10 | ✅ |
| 157 | Augmenter le niveau de l'entraîneur ? | carte `entrainement` var. 8, carte `finances` var. 6 | ✅ |

## Tous jeux
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 160 | Même ordre que l'écran pour la saisie | carte `composition` § Rendu (emplacements 0-10, zones dans l'ordre de l'écran) ; hook `forme.py` (TS emplacements) | ✅ |
| 161 | Meilleures caractéristiques de chaque joueur | compétence clé du poste (`gold.ts_effectif_bilan`) | ✅ |
| 162 | Actions claires, aujourd'hui seulement | CLAUDE.md § Horizon ; rendu des cartes | ✅ |
| 163 | Pas de « si », vérifications | R-5 ; hooks ; checks chiffrés des cartes | 🔧 fiche tactique encore en seuils « si Conduite ≥ 70 » (à remplacer par la compétence la plus haute nommée) |
| 164 | Réponses simples, mise en forme | rendu des cartes ; un bloc par club | ✅ |
| 165 | Des tableaux | rendu des cartes | ✅ |
| 166 | Tout vérifier, apprendre de ses erreurs | `outputs/teamsoccer/learnings.md` (29 leçons) ; § Checks appris | ✅ |
| 167 | Pas d'hypothèse sans vérifier | statuts CONFIRMÉ / EN DOUTE / CONTREDIT de la connaissance | ✅ |
| 168 | Beaucoup d'argent : que faire | carte `finances` var. 5-7, 11 | ✅ |
| 169 | Beaucoup de défaites : agir | carte `defaite` var. 10 | ✅ |
| 170 | Nouveauté : tester en amical | carte `composition` var. 16 | ✅ |
| 171 | Chaque règle parfaite, mine d'or à 100 % | forum lu en entier (2026-10-27) ; 13 annonces dont seul le titre est capté | 🔧 annonces sans contenu |
| 172 | Quel export chaque jour, quoi faire après | `gold.ts_exports_state`, `gold.ts_agenda`, skill `teamsoccer-aujourdhui` | ✅ |
| 173 | Ordre logique, dépendances | `teamsoccer.yaml` § dependances ; `enchainement.md` | ✅ |
| 174 | Mettre à jour agents/skills à chaque nouveauté | veille → skills ; `dossier.py` (nouveau depuis le commit de la carte) | ✅ |
| 175 | Retour des joueurs expérimentés | connaissance (forum) ; variable « avis des amis » des cartes | ✅ |
| 176 | Facteurs cachés | lignes `+N` | ✅ |
| 177 | Export incomplet : le dire | `gold.ts_exports_state`, `gold.sante_collecte`, `gold.exports_nouvelles_cles` | 🔧 `exports_nouvelles_cles` à appliquer en base |

## Règles Team Soccer
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| T1 | Deux clubs, un bloc chacun, jamais un seul | rendu de toutes les cartes ; hook `forme.py` (TS deux clubs) | ✅ |
| T2 | Chaque « Passer » porte sa cible (R-12) | carte `composition` § Rendu 3 | ✅ |
| T3 | Finançable d'abord, sinon abandon | carte `achat` var. 4 | ✅ |

## Découvertes (facteurs cachés)
| Ligne | Fait | Source | Où il sert |
|---|---|---|---|
| +1 | Composition modifiée moins de 2 h avant : non prise en compte ; sans composition, le jeu choisit | connaissance 1.4, 7.7 ; L-023 | carte `composition` var. 1 |
| +2 | Forme = plafond de rendement, baisse toutes les 5 min selon l'Endurance | connaissance 4.9 | cartes `composition` var. 8, `entrainement` var. 3 |
| +3 | Blessure liée à la Forme (85 → 0,20 % … ≤ 30 → 1 % par tacle dur) | connaissance 6.12 | carte `composition` var. 9 |
| +4 | Idole / Magique dans l'effectif = affluence ×1,5, même sans jouer | connaissance 2.3 | cartes `achat` var. 11, `finances` var. 13 |
| +5 | Le secteur dépend du nombre de joueurs, pas de leur qualité | connaissance 1.8 | carte `composition` var. 14 |
| +6 | Le moral baisse après une vente, une perte d'argent, un achat de stade ; une victoire ne compte jamais | connaissance 6.10 | carte `vente` var. 6 |
| +7 | Entretien du stade facturé avec l'ancienne formule (bug 13/10, 19/10) : contrôler chaque lundi | connaissance 2.5, 7.3 | carte `finances` var. 2 |
| +8 | Physique ne monte plus seul ; ≤ 30 = seul l'entraînement d'Endurance | connaissance 4.8 | carte `entrainement` var. 4 |
