# Derby Manager — résumé pour les agents (remplace attentes.md + derbymanager.yaml + commun.md)

Lu par chaque agent **à la place** de `docs/attentes/attentes.md` et `docs/attentes/jeux/derbymanager.yaml`. Mis à jour dans le même commit que toute modification de ces fichiers (écrit le 2026-10-30).

## Jeu
- `derbymanager`, préfixe `dm_` (bronze `game = 'derbymanager'`, `source = 'dom'` + `source = 'api'` pour le JSON des matchs). Football, derbymanager.com (DM2, bêta). Userscript `userscripts/derbymanager.user.js` (chaque page ouverte est copiée, `payload.club` = 547 ou 307).
- **Deux clubs, toujours séparés** (un bloc chacun, jamais de total) : **547 Queen of the South** (Écosse, Premier Division = D1, 8 équipes, 4 matchs contre chacune = 28 journées, **pas de relégation « for now »** #updates 2026-09-28) et **307 Marmandes** (France, D4). Référence `silver.dm_clubs`.
- Tout l'argent est **par jour** (salaires, recettes, plafond). Saison ≈ 35 jours, une semaine de pause entre deux saisons (marché plus rapide, condition remise à zéro).
- Sources : Discord intégral lu le 2026-10-30 (125 932 messages, 2019-01-04 → 2026-10-30) → `outputs/derbymanager/veille/connaissance.md` (322 entrées) ; skills `derbymanager-regles`, `derbymanager-tactique`, `derbymanager-effectif-entrainement`, `derbymanager-club`. Le développeur (compte `derbymanager`) fait foi ; le plus récent l'emporte (moteur refait le 2026-09-28, dots de build up le 2026-10-21, remplaçants le 2026-10-25). `[H]` = hypothèse.

## Écrans (ordre de saisie)
1. **Squad** : formation (grille 5×5 : DL DLC DC DRC DR / ML MLC MC MRC MR / FL FLC FC FRC FR), rôle par poste, 5 remplaçants S1-S5 avec statut d'entrée (RAT, CON, AUTO, DEV, IMP, EMR), curseurs Defensive line (Low 0-1-2 High), Pass preference (Short 0-2 Direct), Pass focus (Narrow 0-2 Wide), Shooting (On sight 0-2 From box), Headers (Avoid 0-2 Prioritise), options Pressing / Counters / Through balls / Run with ball (**chaque option cochée = −1 % de condition pour tous**), onglet Set pieces (PEN, FK, COR, DEF, ATT, capitaine).
2. **Training** : un entraînement par groupe (GK, DEF, MID, FWD), intensité par joueur LOW / MED / HIGH (50/100/150 % d'entraînement, +4/+3/+2 % de récupération).
3. Finances, Facilities, School (Promote / Release), Market + Scouting (régions, 20 scouts), Transfers.

## Vues prêtes (colonnes choisies, `LIMIT`)
- **Routine** : `gold.dm_exports_etat` (manquant / en retard par club).
- **Joueur par joueur (à lire en premier)** : `gold.dm_verdict_joueurs` — note au poste et niveau (fort/moyen/faible), cœur (Confident/Reliable/Inconsistent/Volatile), forme, condition, satisfaction de temps de jeu contre l'attente du statut, vestiaire (Leader/Regular/Outsider), `ne_s_entraine_pas` (jours sans match > exigence TR), plainte d'entraînement, mentor, retraite, trait de capitaine, verdict 541, intensité conseillée. `gold.dm_entrainement_plan` (compétence clé la plus basse par groupe). Infobulles brutes : `silver.dm_player_tips`. **Ne pas lire `gold.dm_joueurs`** (première version).
- **Effectif** : `gold.dm_effectif` (slot enregistré, statut Key/First team/Rotation/Backup, contrat en jours, salaire, prix, 16 compétences), `gold.dm_poste_scores` (note par ligne sur les compétences clés [H]), `silver.dm_tactic`, `silver.dm_training`, `gold.dm_entrainement` (gains/pertes).
- **Adversaires** : `gold.dm_adversaires` (par club, chaque adversaire de ligue déjà rencontré : rang, bilan, forme, nos résultats, xG concédé moyen ; pas de calendrier à venir exporté).
- **Matchs** : `gold.dm_matchs` (résultat `my_result` de la base, xG, possession, tirs, formation, force), `gold.dm_saison_bilan` (par compétition et formation), `gold.dm_tirs_profil` (origine des tirs pour/contre), `silver.dm_shots`, `silver.dm_fixtures`, `silver.dm_standings`.
- **Set pieces (2026-11-01)** : `gold.dm_setpieces` (preneurs PEN/FK/COR, placements DEF/ATT, capitaine, rangs par compétence).
- **Argent** : `gold.dm_finances_bilan` (argent, flux du jour, marge salariale = plafond − engagés, installations), `silver.dm_money_flow`.
- **Marché** : `gold.dm_marche_notes` (note au poste bas/milieu de fourchette contre notre dernier titulaire ; **ne pas lire `gold.dm_marche_postes`**, défectueuse), `gold.dm_prix_reference` (médianes par tier et âge), `silver.dm_transfers`, `silver.dm_school`.

## Ordre des agents
Veille → Match → Effectif (moi, vues gold, sans agent depuis le 2026-11-02) → Finances (moi, vues gold, sans agent depuis le 2026-11-02) → Académie (school) → Entraînement → Tactique → Transferts. Trois agents d'analyse au plus par passage ; un tableau = une vue gold, zéro agent.

## Ce que l'utilisateur attend (condensé ; → source : `docs/attentes/attentes.md`, `docs/chose-a-DM.txt`)
- **Horizon : aujourd'hui seulement.** Le match de demain se prépare aujourd'hui.
- **Rendu** : un bloc par club (Queen of the South puis Marmandes), tableau 🟥 URGENT / 🟧 IMPORTANT / 🟩 SUIVI · catégorie · action « fais X » ; composition **poste par poste dans l'ordre de l'écran Squad** (poste, rôle, joueur), puis curseurs, options, remplaçants et statuts, set pieces ; aucun « si » ; donnée manquante = « il me manque X, fais l'export Y ».
- **Compétitions** : ligue et coupe = compo de référence ; **amical = compo de test** (jeunes, autre formation).
- **Décider** : chaque rendu propose un achat, une vente ou un jeune à promouvoir (nommé, prix, finançable avec `capacite_invest` et `marge_salaire_jour`) ou la raison chiffrée de n'en faire aucun ; défaite = analyse contre toute la saison (`gold.dm_saison_bilan`, `gold.dm_tirs_profil`).

## Règles qui décident (détail et sources dans les skills)
- **Temps de jeu** : Key 75 % des matchs, First team 60 %, Rotation 40 %, Backup 25 % (2026-08-20) ; un joueur mis en liste de transfert depuis 24 h n'a plus de pénalité. Trop de joueurs à un poste = plaintes : vendre.
- **Contre plus fort** : jouer défensif (541, FB plutôt que WB) ; défenseurs = empêcher le build up, milieux = le créer, attaquants ≈ 0 sur le build up (dev, 2025-02-07). 13 dots de build up (−10 % par dot vide, 2026-10-21).
- **Entraînement** : Training Requirement 3-7 jours ; −1 à 20 min jouées, −2 à 45 min (2026-10-25) ; un jeune qui ne joue pas ne progresse pas.
- **Argent** : scouter un joueur avant d'enchérir ; le premier enchérisseur est préféré ; mise en vente possible sous 85 jours de contrat ; installations −1 niveau à −5 M ; le conseil investit seul entre 20 et 50 M en caisse ; « Always squad » avant installations.

## Pièges connus
- Les cellules portent une clé de tri collée (« 15000::15k », « 14Useful player ») : silver les retire (`silver.dm_n`, `silver.dm_money`).
- L'onglet Squad laisse vides FRM/SHA/FIT/POT : `silver.dm_team_src` prend la dernière copie complète de la page d'équipe.
- Le marché exporté suit le filtre de prix de l'écran : un export « 0,3-7,5 M » ne montre aucun joueur au-dessus.
- Sens des colonnes = infobulles du jeu (2026-10-30) : SEL sélectionné · TI intensité · TR « jours sans match / exigence » · PT satisfaction de temps de jeu · CON condition · FRM forme (monte à chaque match joué, flèche = vitesse) · SHA sharpness = modificateur attendu (cœur) · BU/PBU capacité 1-20 en plus du rôle · FIT natural fitness (vitesse de perte de condition) · EXP pression + adaptabilité + professionnalisme · POT chance d'atteindre le tier suivant (low/med/high) · SKILL niveau relatif dans l'équipe · SAT effet sur le team spirit · STA leader/regular/outsider · PTR temps de jeu du contrat (Key/First/Rotation/Backup) · DUR jours de contrat · SUB AUTO/RAT (notes)/CON (préserver la condition)/DEV (donner du temps de jeu)/IMP (joueur important)/EMR (urgence seulement) · PEN/FK/COR preneurs · DEF/ATT placement sur CPA · CAP capitaine.
- Les plaintes « Unhappy/Furious with training facilities and mentors » et « Nearing his growth limit at this club » = installations trop basses pour l'effectif.
- **Marmandes (307)** : exports reçus le 2026-10-31 (seul Graduates manque) ; au 2026-11-01 seul 547 a été ré-exporté.

## Règles ajoutées par l'utilisateur (2026-11-02)
- **Achat = contrat, pas enchère** : le prix affiché est fixe, on négocie seulement le contrat (salaire/jour dans la liste de l'écran « Offer contract », Extra fee, durée, statut). Coût total = prix + 5 % + 5 %. Chaque achat donne le salaire/jour à saisir, l'Extra fee et le coût total.
- **Prolongation = montant** : jamais « prolonge » seul ; donner le salaire/jour à proposer (demande de la page contrat, + ~10 k si l'humeur n'est pas verte), borné par `marge_salaire_jour`.
- **Vente** : le jeu refuse une mise en vente qui fait tomber l'effectif non listé à 18 (Bodian, 20 − McCulloch = 19 → 18, refusé le 2026-11-02) : compter avant de proposer, une vente à la fois, ≥ 19 non listés [H].
- **École** : un jeune de l'école reste jusqu'à la fin de son contrat (97-102 j ≈ 3 saisons) sans salaire ; le promouvoir seulement s'il va jouer (sinon il ne grandit pas et coûte le salaire = coût des installations). Chaque rendu école compare aussi les jeunes découverts par les scouts (page `market_regions-tab`) : offrir un contrat à un jeune découvert le place à l'école (utilisateur 2026-11-02) ; potentiel et expérience visibles à 2 scouts de plus ; l'école coûte ≈ 12 k/j par jeune (Marmandes : 35 k/j pour 3, `youth_school`) ; places : 4 (connaissance §6) ou 3 (utilisateur 2026-11-02, à confirmer) : école pleine = libérer un jeune avant d'en signer un.
