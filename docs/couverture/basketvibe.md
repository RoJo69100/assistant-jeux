# Registre de couverture — BasketVibe

Créé le 2026-10-31 (mise en route, `docs/decisions/variables.md` § Mise en route). Chaque ligne de la liste de l'utilisateur (`docs/chose-a-faire.txt`, lignes 1-54 + bloc « Tous jeux » 159-177) → sa réponse et son statut. Statuts : ✅ répondu (mécanisme en place, vérifié) · 🔧 mécanisme fait, limite connue · ❌ manque, avec le plan. Les découvertes (règles ou facteurs cachés que l'utilisateur ne connaît peut-être pas) sont ajoutées en lignes `+N`. Les lignes 155-157 sont celles de Team Soccer (pas ici).

Cartes : `docs/decisions/cartes/basketvibe/<type>.md` (composition, defaite, achat, vente, entrainement, academie, finances).

## Global
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 4 | Premier tour de veille : règles, Discord, forum, chat, mine d'or | `outputs/basketvibe/veille/connaissance.md` (123 lignes, statut par ligne) + 9 skills `basketvibe-*`. Les 642 messages du développeur et les release-notes sont lus en entier ; les ~9 100 messages de joueurs n'ont été balayés que par mots-clés (connaissance § Lecture intégrale) | ✅ lu en entier le 2026-10-31 : 3 agents, 26 193 lignes, ~490 entrées (`lecture-joueurs-1/2/3.md`), intégré dans `connaissance.md` (corpus jusqu'au 09/10) |
| 5 | Calendrier, savoir quel jour on est | `gold.bv_agenda`, skill `basketvibe-aujourdhui`, `basketvibe-saison` § Rythme | ✅ |
| 6 | Différence Coupe / Amical / Ligue, paramètres pour chacun (preset ligue/coupe, amical sans preset, tests) | `docs/fiches/basketvibe/resume.md` § Rythme ; carte `composition` § Ligue/coupe et § Amical | ✅ |
| 7 | Stats de la ligue : meilleurs joueurs des équipes | `gold.bv_league_top_players` (créée le 2026-10-31, migration 052) : pts, éval, %, rang par compétition | 🔧 seulement les joueurs croisés dans nos matchs (chaque club 2 fois par saison) ; les autres matchs de la ligue ne sont pas exportés |

## Jeunes / académie
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 10 | Comprendre l'académie | skill `basketvibe-academie` (cycle, jauge, −50 % à la signature, fourchettes, probabilités) | ✅ |
| 11 | Savoir si on scoute (teste) le joueur | carte `academie` variables 4-6 (test 25 000, `gold.bv_academy_potential_odds`) | ✅ |
| 12 | Savoir si le joueur scouté est intégrable | carte `academie` variables 7-9 (besoin par poste `gold.bv_position_summary`, fit) | ✅ |
| 13 | Combien on dépense dans l'académie | `gold.bv_finance_health.weekly_academy`, `silver.bv_academy_weekly.weekly_investment` ; carte `finances` var. 3 | ✅ |

## Finances
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 16 | Solde actuel | `gold.bv_finance_health.balance` | ✅ |
| 17 | Dépenses | `gold.bv_finance_health.weekly_fixed_costs`, `gold.bv_finance_season_rates` | ✅ |
| 18 | Salaires | `gold.bv_finance_health.weekly_salaries`, `silver.bv_player_salary_weekly` (par joueur) | ✅ |
| 19 | Entrées d'argent | `gold.bv_finance_health` (sponsor, billetterie, amicaux, homegrown), `gold.bv_finance_weekly_result` | ✅ |
| 20 | Quelles actions : acheter un joueur, du personnel, rien ? | carte `finances` var. 8-10 (capacité d'investissement moins dépenses décidées, alternatives) | ✅ |
| 21 | Quoi faire dans le futur | `gold.bv_finance_s2_projection` (résultat saison 2, réserve, investissable) ; carte `finances` var. 6 | ✅ |
| 22 | Comprendre les sponsors, choisir le meilleur | skill `basketvibe-economie` § Sponsor ; `silver.bv_sponsor_weekly` ; carte `finances` var. 11. Saison 2 : Fluxora Balance choisi par l'utilisateur le 27/10 (`fait-2026-10-27.md`) | ✅ (signature à confirmer au prochain export sponsor : la base dit encore `choosing` au 26/10) |

## Équipe
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 25 | Toutes les caractéristiques des joueurs | `gold.bv_roster_now` (8 compétences, forme, fatigue, expérience, taille, poids, PS) | ✅ |
| 26 | Joueur de l'académie ou non | `gold.bv_player_outlook.academy_junior` | ✅ |
| 27 | Effet de forme | skill `basketvibe-joueurs` § Forme (−11 % à +15 % en attaque) ; carte `composition` var. 6 | ✅ |
| 28 | Effet d'expérience | skill `basketvibe-joueurs` § Expérience (jusqu'à +10 %) | ✅ |
| 29 | Effet de fatigue | skill `basketvibe-joueurs` § Fatigue (v4 : −4/−15/−30/−50 %) ; `gold.bv_fatigue_plan` ; carte `composition` var. 5 | ✅ |
| 30 | Bon à son poste ? sinon lequel ? | `gold.bv_slot_fit` (fit par emplacement, taille, rang) ; carte `composition` var. 9 | ✅ |
| 31 | Ce joueur est-il à vendre | `gold.bv_roster_now.on_transfer_list` (nos ventes ouvertes) et `gold.bv_sell_candidates` (faut-il le vendre) ; carte `vente` | ✅ |
| 32 | Statistiques des joueurs | `gold.bv_player_outlook` (saison), `gold.bv_match_player_lines` (par match) | ✅ |
| 33 | Blessés ou suspendus | `gold.bv_roster_now.injury_return_on` | 🔧 suspensions : aucune règle de suspension trouvée (cherché dans : skills joueurs, saison, tactique, communauté ; connaissance ; manuel via skills) ; seule l'exclusion à 6 fautes existe, dans le match |

## Transferts
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 36 | Base de données « tel joueur vaut tel prix » | `gold.bv_transfer_history`, `gold.bv_market_price_ref` (âge × poste), `gold.bv_price_ref_ps` (PS × âge) | ✅ |
| 37 | Étudier le marché : acheter / revendre | `gold.bv_market_candidates`, `gold.bv_market_bargains`, `gold.bv_resale_stats` ; carte `achat` | ✅ |
| 38 | Faut-il vendre nos joueurs | `gold.bv_sell_candidates` ; carte `vente` | ✅ |

## Entraînement
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 41 | Principale et secondaire après un export | `gold.bv_training_options` ; carte `entrainement` | ✅ |
| 42 | Suivre les progrès | `gold.bv_skill_progress_weekly`, `gold.bv_training_gains_exact` | 🔧 `silver.bv_training_changes` arrêtée au 18/10 : export « Recent changes » le dimanche après 04:00 (skill entraînement) |
| 43 | Comprendre le progrès, définir le talent (potentiel) | skill `basketvibe-entrainement` § Potentiel ; `gold.bv_potential_estimate` ; potentiel révélé sur la fiche [News 2026-10-20] | ✅ |

## Tactique
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 46 | Quelle tactique mettre en place | carte `composition` | ✅ |
| 47 | Tableau joueurs : poste, quarts, off. focus, rôle, tir, agressivité (1-5) | carte `composition` § Rendu, tableau 1 ; `gold.bv_saisie_joueurs` | ✅ |
| 48 | Focus défensif 1-5 et zone par adversaire | carte `composition` § Rendu, tableau 2 ; `gold.bv_saisie_adversaires` | ✅ |
| 49 | Stratégie selon nos anciens matchs contre cet adversaire | `gold.bv_next_opponents.meetings`, `gold.bv_match_report` et `gold.bv_match_opp_focus` filtrés sur l'adversaire ; carte `composition` var. 2-3 | ✅ |
| 50 | Stratégie selon toute la saison, blessés, forme, manque de réussite | `gold.bv_match_factors_by_result`, `gold.bv_match_trends`, `gold.bv_roster_now` ; carte `composition` var. 5-7, 11-12 | ✅ |

## Personnel
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 53 | À quoi sert chaque personnel | skill `basketvibe-economie` § Personnel ; `gold.bv_personnel_status` | ✅ |
| 54 | En a-t-on besoin | carte `finances` var. 12 | ✅ (piège : médical 85 000 au journal contre 60 000 affichés, `resume.md` § Pièges) |

## Tous jeux (appliqué à BasketVibe)
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 160 | Même ordre que l'export pour la saisie | rendu figé des cartes ; `gold.bv_saisie_*` `order by ordre` (PG→C puis alphabétique) | ✅ |
| 161 | Meilleures caractéristiques de chaque joueur | `gold.bv_roster_now` + `gold.bv_ps_weight` (poids par poste) | ✅ |
| 162 | Actions claires, aujourd'hui seulement | CLAUDE.md § Horizon ; rendu des cartes | ✅ |
| 163 | Pas de « si », vérifications tout le temps | R-5 ; hook `pipelines/police.py` ; checks chiffrés des cartes | ✅ |
| 164 | Réponses simples, mise en forme | rendu des cartes ; CLAUDE.md § Présentation | ✅ |
| 165 | Des tableaux | rendu des cartes | ✅ |
| 166 | Tout vérifier, apprendre de ses erreurs | `outputs/basketvibe/learnings.md` (C-nnn → L-nnn) ; § Checks appris de chaque carte ; `docs/retro/regles-apprises.md` | ✅ |
| 167 | Pas d'hypothèse sans vérifier | statut confirmé / en doute de la connaissance ; colonne Source des cartes | ✅ |
| 168 | Beaucoup d'argent : que faire, axes à améliorer | carte `finances` var. 8-10 + carte `achat` | ✅ |
| 169 | Beaucoup de défaites : prendre une action | carte `defaite` + agent `decideur` (jamais « ne rien changer ») | ✅ |
| 170 | Nouveauté : tester en amical, sinon proposer comment | carte `composition` § Amical (un test à la fois, mesure nommée) | ✅ |
| 171 | Chaque règle parfaite, mine d'or étudiée à 100 % | voir ligne 4 | 🔧 règles lues à 100 % ; aucune mesure v4 (zone, agressivité, focus) dans le corpus : à acquérir par des amicaux de test |
| 172 | Quel export chaque jour, quoi faire après | `gold.bv_exports_state`, skill `basketvibe-aujourdhui` | ✅ |
| 173 | Ordre logique des actions, dépendances | `docs/fiches/basketvibe/resume.md` § Ordre des agents ; `enchainement.md` ; `docs/attentes/jeux/basketvibe.yaml` | ✅ |
| 174 | Mettre à jour agents/skills à chaque nouveauté | veille → skills ; `dossier.py` donne le nouveau depuis le dernier passage et l'agent modifie le check de la carte | ✅ |
| 175 | Retour des joueurs expérimentés Discord | connaissance (lignes « Com ») ; variable « avis des amis » de chaque carte | ✅ (limite : ligne 4) |
| 176 | Facteurs cachés révélés dans les discussions | lignes `+N` ci-dessous | ✅ |
| 177 | Export incomplet : le dire, je le refais | R-5 « il me manque X, fais l'export Y » ; agent `lecteur-exports` | ✅ |

## Découvertes à connaître (ajoutées par Claude)
| # | Fait | Source | Statut |
|---|---|---|---|
| +1 | À partir de 36 min dans le match : −20 % sur toutes les actions jusqu'à la fin | [M§5.7] | confirmé |
| +2 | Fatigue v4 (tous les matchs depuis le 27/10) : −4 % à 20, −15 % à 40, −30 % à 60, −50 % à 80, fixée au coup d'envoi | News 2026-10-17, 2026-10-27 | confirmé |
| +3 | Coupes : ni blessure, ni revenu, ni expérience, ni fatigue, ni avantage du terrain | News 2026-10-23 | confirmé |
| +4 | Lock est exporté sous le libellé `off` | Utilisateur 2026-10-21, L-018 | confirmé |
| +5 | Moteur v5 en amicaux seulement (pas de 20 s mortes, tirs de fin de quart) | News 2026-10-28 | complété (effet inconnu) |
| +6 | Compétences adverses de coupe en fourchettes de 20 points | export coupe, `resume.md` | confirmé |
| +7 | Focus offensif : jusqu'à 50 % des points vers un seul joueur (Primary + autres Low/passeurs) | Dev 2026-09-07 | complété (v3) |
| +8 | Fin de match serré : l'équipe menée fait des fautes tactiques (les LF adverses de fin de Q4 ne sont pas forcément un défaut de discipline) | Dev 2026-09-08/09 | complété |
| +9 | Le défenseur principal est celui du même emplacement que le tireur ; taille et physique pèsent plus que le libellé | Dev 2026-07-09/18 | confirmé |
| +10 | En ligue et en coupe, le rebond d'équipe = moyenne des 5 sur le terrain ; la taille décide surtout qui est crédité | [M§5.1.1] | confirmé |
| +11 | Passeur à 90 : tir assisté +14 pts de bonus ; à 50 : +1 | [M§5.1.4] | confirmé |
| +12 | Poids hors de la plage saine pour la taille : pénalité (trop lourd : défense extérieure ; trop léger : rebond, contact) | [M§5.2] | confirmé |
| +13 | Popularité remise à 70 % en début de saison peut-être seulement pour les clubs sous 70 | Dev 2026-10-07 | en doute |
| +14 | Le développeur a remis la fatigue à zéro à la main plusieurs fois (août-septembre) : une fatigue plus basse que prévu peut venir de là | Dev 2026-08-19 … 09-13 | en doute |
| +15 | Le TS est recalculé une fois par jour et juste après un transfert réglé | Dev 2026-09-03, release-notes 2026-09-04 | complété |
| +16 | Prime de fin de saison : 1er 400 000, 2e 300 000, 3e 200 000, 4e 100 000, 5-8e 50 000 | [M§10.1.4] | confirmé |
| +17 | Bonus homegrown : 200 par minute de ligue des juniors signés, plafond 40 000 par semaine (~66 min par match) | [M§10.1.3] | confirmé |
| +18 | Un joueur blessé ne s'entraîne pas cette semaine-là | [M§8] | confirmé |
| +20 | Après tout transfert ou changement de préréglage, rouvrir chaque match planifié : le plan ne se met pas à jour tout seul | grobarbrate 2026-09-05 ; tankre1792, Dev 2026-09-18/19 | confirmé (3 sources) |
| +21 | Prix du marché du 27/09 au 04/10 probablement faussés (transferts truqués, 5 comptes bannis le 08/10) | carlomtlopes, chanceler 2026-10-05/08 | en doute |
| +22 | Potentiel d'un agent libre : 3 à 9 ; aucun joueur de 20-21 ans en vente | Dev 2026-09-07, 2026-10-05 | confirmé |
| +23 | Défense agressive : fautes et lancers francs adverses en forte hausse ; défense ≥ 55-60 proposée pour les crans 4-5 | #portugal 2026-08/10 | avis (v3) |
| +24 | Le Dev conseille de tirer l'académie vers 70-80 % ; 71 000 par semaine = même force que 100 000 (affirmé, non prouvé) | vachacz 2026-07-21 ; nhegas12 2026-09-13 | avis / en doute |
| +19 | Potentiel 7 progresse presque comme un 8 (×1,50 contre ×1,60) mais se vend bien moins cher | [M§8.3] + Com dcarra 2026-10-14 | avis + calcul |
