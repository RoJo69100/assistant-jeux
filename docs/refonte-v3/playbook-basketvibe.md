# Playbook BasketVibe : ce qui se déclenche, ce qui s'apprend

Écrit le 2026-11-09. Critères P1 à P8 : `docs/refonte-v3/journal-aujourdhui.md`, section « Playbook ».

Une routine = une ligne : déclencheur | condition | lancement | ce qu'elle apprend | état | preuve.
- État : **existe** (un script ou une vue le fait déjà, dans le plan du jour `pipelines/aujourdhui.py`), **à relier** (la vue ou la donnée existe, le plan du jour ne l'utilise pas), **à créer**.
- Preuve : fichier:ligne ou vue lue le 2026-11-09 en écrivant ce fichier ; sinon « non vérifié ».
- Limite : toujours calculée depuis le calendrier du jeu (`core.fixture`, verrou du jeu, fin d'enchère) ; aucune heure n'est écrite dans ce fichier.

## Règles de tête

1. **Au plus tôt.** Toute action se fait le jour même, dès que sa donnée est arrivée (CLAUDE.md, inviolable 3). Deux exceptions : une enchère se règle près de sa fin ; un résultat se lit après le match.
2. **Solde jamais négatif, sans réserve fixe.** Capacité = solde moins les enchères encore ouvertes ; on dépense pour être meilleur (décision de l'utilisateur du 09/11, critère PB8 ; `pipelines/aujourdhui.py:366-369`).
3. **Vendre pour baisser la masse salariale** quand la force de l'équipe ne baisse pas (décision de l'utilisateur, consigne du playbook du 09/11).
4. **Académie : étudier tous les prospects**, même sous 100 % de jauge (décision de l'utilisateur, consigne du playbook du 09/11).
5. **Aucun paramètre fixé à la main.** Chaque seuil est calculé sur l'historique et revu chaque semaine (décision de l'utilisateur, consigne du playbook du 09/11). Les seuils écrits à la main aujourd'hui sont listés dans « Trous constatés ».
6. Jamais d'achat, de vente ni d'enchère sans accord écrit ; au-dessus du seuil de gros montant, dossier puis agent `police` (CLAUDE.md, inviolables 2 et 6).

## Chaque passage

| Déclencheur | Condition | Lancement | Ce qu'elle apprend | État | Preuve |
|---|---|---|---|---|---|
| Message de l'utilisateur | toujours | hook `pipelines/heure_paris.py` | l'heure de Paris, base de toutes les limites | existe | `.claude/settings.json:42` |
| « que faire », « reprenons » | toujours | `python -I pipelines/aujourdhui.py basketvibe` | le plan du jour | existe | `.claude/skills/basketvibe-aujourdhui/SKILL.md:11` |
| Déclaration de l'utilisateur (export fait, saisie faite) | ligne du registre `fait-<jour>.md` avec `[clé=…]`, ou mots connus | `aujourdhui.py` : `declare`, `cle_match` | ce qui est déjà fait : plus redemandé | existe | `pipelines/aujourdhui.py:148-168` |
| Écran plus vieux que son âge maximal | statut ≠ « à jour » / « optionnel » dans `gold.bv_exports_state` | `aujourdhui.py`, ligne « Exports à faire aujourd'hui » | quels exports manquent | existe | `pipelines/aujourdhui.py:320-335` ; `gold.bv_exports_state` (14 écrans) |
| Mes enchères | enchère ouverte (`encheres_en_cours`) et page de plus de 24 h | `aujourdhui.py` | l'état de nos enchères en cours | existe | `pipelines/aujourdhui.py:325-335` |
| Historique des transferts | dernière vente lue antérieure à la veille | `aujourdhui.py`, `gold.bv_transfer_history` | les prix réels du marché | existe | `pipelines/aujourdhui.py:344-349` |
| Alerte du jour (blessure, fatigue, forme, finances, transferts) | ligne dans `gold.bv_daily_alerts` | `aujourdhui.py` | ce qui touche l'effectif aujourd'hui | existe | `pipelines/aujourdhui.py:351-358` |
| Alerte de domaine « match » (dernier match, match joué non exporté) | ligne de `core.alert_rule` domaine `match` | `gold.bv_daily_alerts` ; `aujourdhui.py` ne garde pas ce domaine (`CAT_ALERTE`) | le match à exporter ou à analyser | à relier | `pipelines/aujourdhui.py:37-38` ; `gold.bv_daily_alerts` (1 ligne, domaine `match`) |
| Conseil arrivant à échéance | critère daté du jour ou du lendemain dans `learnings.md` | `aujourdhui.py` | si un conseil passé a marché | existe | `pipelines/aujourdhui.py:297-299` |
| Brief tactique trop vieux | âge du brief au-delà du seuil de `aujourdhui_sources.py` | `aujourdhui.py` : « relance l'agent tactique » | qu'un conseil repose sur des données périmées | existe | `pipelines/aujourdhui.py:270-271` |
| Vues matérialisées périmées | avant le plan | `python -I pipelines/rafraichir_avant_aujourdhui.py` | des vues gold à jour | à relier | le script existe ; aucun appel dans `pipelines/aujourdhui.py` ni dans le skill (recherche du 09/11) |
| Décision échue | ligne dans `gold.decisions_a_evaluer` | `python pipelines/evaluer_decisions.py` | si la prédiction d'une décision était juste (`learn.outcome`) | à relier | `gold.decisions_a_evaluer` (0 ligne le 09/11) ; aucun appel dans `aujourdhui.py` |

## Chaque match (ligue, coupe, amical)

| Déclencheur | Condition | Lancement | Ce qu'elle apprend | État | Preuve |
|---|---|---|---|---|---|
| Match à venir avec brief tactique | verrou non passé (`limite < maintenant` exclu) | `aujourdhui.py`, brief `*-tactique.md` | la saisie à faire et le test qui la prouvera fausse | existe | `pipelines/aujourdhui.py:245-283` |
| Match de ligue ou d'amical à venir | règle `ligue_preset`, `amical_preset` de `core.agenda_rule` | `gold.bv_agenda` lu par `aujourdhui.py` | le preset à vérifier avant le verrou | existe | `pipelines/aujourdhui.py:301-318` ; `core.agenda_rule` |
| Match de ligue dans les 2 jours | aucune ligne adverse dans `gold.bv_saisie_adversaires` | `aujourdhui.py` | l'aperçu adverse à exporter | existe | `pipelines/aujourdhui.py:336-343` |
| Match joué | règles `ligue_export`, `amical_export` de `core.agenda_rule` | `gold.bv_agenda` lu par `aujourdhui.py` | la page du match à exporter | existe | `pipelines/aujourdhui.py:301-318` ; `core.agenda_rule` |
| Jour sans amical | règle `amical_manquant` | `gold.bv_agenda` lu par `aujourdhui.py` | un amical de plus, donc un match de plus pour la file d'expériences | existe | `core.agenda_rule` (`amical_manquant`) |
| Défaite de ligue ou de coupe en base | `my_result = 'L'`, compétition ligue ou coupe (jamais un amical, arbitrage 15) | agent `analyste` | les causes chiffrées de la défaite | à relier | `gold.bv_match_report` (`sql/gold/003_bv_match_report.sql:6`) ; aucun appel dans `aujourdhui.py` |
| Match exporté (tous) | nouvelle page de match plus récente que `learnings.md` | agent `match` | le journal des enseignements | à relier | CLAUDE.md, section Agents ; aucun appel dans `aujourdhui.py` |
| Prochain adversaire connu | ligne dans `gold.bv_next_opponents` | `gold.bv_match_opp_focus` | le focus défensif à poser sur l'adversaire | à relier | `sql/gold/004_bv_tactics.sql:113` ; `sql/gold/003_bv_match_report.sql:106` ; `gold.bv_next_opponents` (19 lignes) |
| Amical à jouer | expérience en tête de la file (section « File d'expériences amicales ») | à créer : lecture de la file par `aujourdhui.py` | une mesure du moteur de match | à créer | ce qui prouvera qu'elle sert : le n disponible du chiffre visé dans `etude_evenements_basketvibe.py calculs` augmente après chaque amical exporté |
| Match de ligue à venir | `core.fixture.scheduled_at` renseigné | à créer : limite = coup d'envoi moins le verrou du jeu | une limite juste, sans heure écrite à la main | à créer | ce qui prouvera qu'elle sert : 0 ligne de `core.agenda_rule` avec une heure pour la ligue, et le même plan rendu sur les 3 journées de la semaine |

## Chaque cycle (entraînement, académie, paie, semaine)

| Déclencheur | Condition | Lancement | Ce qu'elle apprend | État | Preuve |
|---|---|---|---|---|---|
| Fin du cycle d'entraînement | règles `entrainement_sam`, `routine_dim` | `gold.bv_agenda` lu par `aujourdhui.py` | l'entraînement à sauvegarder, les écrans à exporter | existe | `core.agenda_rule` ; `pipelines/aujourdhui.py:301-318` |
| Export Entraînement arrivé | page plus récente que le dernier brief entraînement | `gold.bv_saisie_entrainement`, `gold.bv_training_gains_exact`, agent `entrainement` | le gain réel de chaque joueur, garder ou changer | à relier | `sql/gold/054_bv_saisie_entrainement.sql:6` (14 lignes) ; `sql/gold/005_bv_training.sql:19` |
| Nouveau rapport d'académie | règle `academie_jeu` | `gold.bv_agenda` lu par `aujourdhui.py` | l'export Académie à faire | existe | `core.agenda_rule` (`academie_jeu`) |
| Export Académie arrivé | chaque prospect, même sous 100 % de jauge (règle 4) | `gold.bv_academy_prospects`, `gold.bv_academy_potential_odds`, agent `academie` | tester, signer, ignorer | à relier | `sql/gold/010_bv_academy.sql:83` (3 prospects) ; `sql/gold/010_bv_academy.sql:60` |
| Semaine financière | `weekly_result_est < 0` dans `gold.bv_finance_health` | `aujourdhui.py` | le poste de charges à réduire | existe | `pipelines/aujourdhui.py:408-419` |
| Personnel | toujours | `aujourdhui.py`, ligne « Garder » | rien de décidé : règle non tranchée | existe | `pipelines/aujourdhui.py:437-443` |
| Paie : masse salariale | joueur à fort salaire par point de PS dont la vente ne baisse pas la force (règle 3) | `gold.bv_sell_candidates` (`salary_per_ps`, `rank_in_slot`) | qui vendre pour baisser la masse salariale | à relier | `sql/gold/006_bv_transfers.sql:102` (14 lignes) |
| Projection de saison | nouvelle semaine financière | `gold.bv_finance_projection` | le solde de fin de saison | à relier | `sql/gold/018_bv_fixes_2026_10_22.sql:11` (1 ligne) |
| Nouvelle semaine | une semaine d'historique de plus | à créer : recalcul de chaque seuil de « Trous constatés » sur l'historique | des seuils qui suivent le jeu (règle 5) | à créer | ce qui prouvera qu'elle sert : chaque seuil a une date de calcul de moins de 7 jours et sa valeur change au moins une fois en 4 semaines |

## Sur événement

| Déclencheur | Condition | Lancement | Ce qu'elle apprend | État | Preuve |
|---|---|---|---|---|---|
| Joueur de 31 ans ou plus | ligne de `gold.bv_roster_now` | `aujourdhui.py` : « Mets X en vente » | le déclin à venir | existe | `pipelines/aujourdhui.py:398-405` |
| Poste mince ou faible | profondeur basse ou PS moyen le plus bas (`gold.bv_position_summary`), candidat au marché | `aujourdhui.py` : « Acheter un X de note ≥ … » | le poste à renforcer | existe | `pipelines/aujourdhui.py:381-397` |
| Blessure, fatigue, forme | règle de `core.alert_rule` | `gold.bv_daily_alerts` lu par `aujourdhui.py` | le joueur à ménager | existe | `pipelines/aujourdhui.py:351-358` |
| Vente pour profit, place aux jeunes | toujours | `aujourdhui.py`, ligne « Garder » | rien de décidé : « règle non écrite — à valider » | existe | `pipelines/aujourdhui.py:406-407` |
| Fatigue projetée | ligne de `gold.bv_fatigue_plan` | vue | les minutes à couper avant le match | à relier | `sql/gold/004_bv_tactics.sql:75` (280 lignes) |
| Gros transfert | montant au-dessus de `SEUIL_GROS_MONTANT` | `python pipelines/dossier.py basketvibe <type>` puis agent `police` (hook `pipelines/police.py`) | si la décision repose sur toutes les informations | existe | `pipelines/aujourdhui.py:287` ; `.claude/settings.json:74` |

## Phases de saison

| Déclencheur | Condition | Lancement | Ce qu'elle apprend | État | Preuve |
|---|---|---|---|---|---|
| Dernier match de la saison | règle `fin_saison` | `gold.bv_agenda` lu par `aujourdhui.py` | maintien et prime de classement | existe | `core.agenda_rule` (`fin_saison`) |
| Changement de phase (saison, intersaison, promotion) | ligne de `core.season` pour basketvibe | à créer : remplir `core.season` et lire `phase` | ce qui change selon la phase | à créer | `core.season` : 0 ligne pour basketvibe le 09/11 ; ce qui prouvera qu'elle sert : chaque phase a sa date de début dans `core.season` et le plan du jour change de règles le jour même |

## Marché

| Déclencheur | Condition | Lancement | Ce qu'elle apprend | État | Preuve |
|---|---|---|---|---|---|
| Décision d'achat ouverte | `learn.decision` domaine `achat`, enchère non finie | `aujourdhui.py` : maximum, fin, police | l'enchère à poser | existe | `pipelines/aujourdhui.py:285-295` |
| Enchère finie | fin passée | `aujourdhui.py`, `silver.bv_transfers` | acheté ou non, et à qui | existe | `pipelines/aujourdhui.py:215-231` |
| Marché frais (moins de 24 h) | marge de revente p25 positive, `ref_n ≥ 5`, dans la capacité | `aujourdhui.py`, `gold.bv_market_bargains` | les affaires à revendre | existe | `pipelines/aujourdhui.py:420-436` |
| Fin d'une vente à nous | règle `fin_vente` | `gold.bv_agenda` lu par `aujourdhui.py` | le prix obtenu | existe | `core.agenda_rule` (`fin_vente`) |
| Prix de référence du marché | nouvelles ventes en base | `gold.bv_price_ref_ps`, lue par `gold.bv_market_bargains` | le prix de référence par tranche de PS et d'âge | existe | `sql/gold/022_bv_transfer_history.sql:92` (`left join gold.bv_price_ref_ps`) ; `pipelines/aujourdhui.py:420-436` |
| Marge de revente réelle | nouvelles ventes en base | `gold.bv_resale_stats` | la marge réelle par profil | à relier | `sql/gold/022_bv_transfer_history.sql:56` ; lue par aucune autre vue ni par `aujourdhui.py` (recherche du 09/11) |
| Joueurs de la ligue | nouvelle journée | `gold.bv_league_top_players` | les meilleurs joueurs adverses (cibles, adversaires) | à relier | `sql/gold/052_bv_league_top_players.sql:4` |

## Comprendre le moteur de match

Faits repris de `docs/refonte-v3/etude-evenements-basketvibe.md` et de `docs/refonte-v3/preanalyse-matchs-basketvibe.md`, avec leur verdict exact.

| Fait | Valeur | Verdict du fichier | Source |
|---|---|---|---|
| Rythme | `possessions_per_quarter_n` vaut 50 sur les 86 pages de match (3 moteurs) ; 100,3 à 102,2 possessions par équipe et par match | niveau de rythme « non identifiable (aucune valeur annoncée), mais constant » | `etude-evenements-basketvibe.md:190` |
| Tir au cercle, amical v4 | +6,81 points de réussite par +10 de Deux points [4,02 ; 9,01] | « effet présent, taille imprécise » (demi-largeur 2,5 au-dessus de l'effet minimal 2,0) | `etude-evenements-basketvibe.md:184`, `:197` |
| Tir à 3 points, amical v5 | +2,32 [0,61 ; 5,06] | « effet présent, taille imprécise » | `etude-evenements-basketvibe.md:184` |
| Mi-distance, amical v4 | Trois points +8,63 [1,36 ; 14,77] | « en écart » (la compétence non nommée pèse) | `etude-evenements-basketvibe.md:184`, `:194` |
| Fautes sur tir, amical v4 | 6,5 % pour une défense équilibrée contre 16,5 % annoncés ; pente 1,01 point par niveau au lieu de 2,25 | « écart de niveau, dénominateur du manuel non défini » ; « pente de 2,25 exclue » ; non identifiable pour v3, ligue v4, coupe v4, v5 | `etude-evenements-basketvibe.md:185`, `:204` |
| Part de tirs à 3 points, tireur niveau 4 | 65,4 % [58,2 ; 72,3] (ligue v3), 65,5 % [59,1 ; 71,9] (amical v4) | « non identifiable » (15 joueurs-matchs au niveau 4 requis) ; indice : environ 2 pour 1 à 2, pas 50 % | `etude-evenements-basketvibe.md:188`, `:208` |
| Fatigue | fatigue maximale observée 24,63 (v3 et amical v4) ; paliers 40, 60, 80 jamais observés | « non identifiable » | `etude-evenements-basketvibe.md:186`, `:196` |
| Règle des 24 s, v5 | 0,00 % d'écarts de plus de 24 s (maximum 17 s) | « conforme » | `etude-evenements-basketvibe.md:190`, `:195` |
| Fatigue du matin, amical v4 (préanalyse) | r = −0,04 [−0,26 ; 0,17], n = 107 | « décidable, effet absent » ; « historique, non applicable aux amicaux v5 » ni à la ligue | `preanalyse-matchs-basketvibe.md:13`, `:151` |
| Ligue v4 (préanalyse) | 16 matchs avec box score | tous les verdicts « n trop petit » | `preanalyse-matchs-basketvibe.md:5-20` |

| Déclencheur | Condition | Lancement | Ce qu'elle apprend | État | Preuve |
|---|---|---|---|---|---|
| Amical exporté (4 pages et page Équipe) | moteur v5 | `python -I pipelines/etude_evenements_basketvibe.py calculs` | le n disponible et le verdict de chaque chiffre | à relier | `pipelines/etude_evenements_basketvibe.py` (docstring) ; aucun appel dans `aujourdhui.py` |
| Matchs de ligue de notre division sans box score | `silver.bv_fixtures` moins `silver.bv_matches` | liste ordonnée de la préanalyse | des matchs de plus pour les questions 1, 3, 4, 6 | à relier | `preanalyse-matchs-basketvibe.md`, étape 4 (b) : 8 matchs de notre division |
| Chiffre qui passe « identifiable » | n disponible ≥ n requis | à créer : comparaison des deux derniers calculs | quelle règle du skill confirmer ou corriger | à créer | ce qui prouvera qu'elle sert : un chiffre change de verdict et le skill de règles correspondant est mis à jour dans la semaine |

## File d'expériences amicales

Un seul réglage change à la fois ; les niveaux alternent A, B, A, B. Export requis pour chaque amical : les 4 pages du match et la page Équipe du jour. Les 16 amicaux du chiffre 1 ne demandent aucun réglage : chaque amical contrôlé exporté compte aussi pour eux.

| # | Réglage testé | Niveaux | Pourquoi | n visé | Export requis | Statut |
|---|---|---|---|---|---|---|
| E1 | agressivité défensive, uniforme sur nos cinq | A = 2, B = 4 | chiffre 2 (fautes) : 3 tranches de 150 tirs adverses, 859 tirs disponibles, tous en tranche « soft » | au moins 4 amicaux (2 à 2, 2 à 4) | 4 pages du match et page Équipe | non commencé — non vérifié (aucune table de suivi) ; réglage qui change le jeu : à décider par l'utilisateur |
| E2 | focus de tir de deux tireurs | A = niveau 4 ; B = niveau 2 (référence) | chiffre 5 (part de tirs à 3 points) : 15 joueurs-matchs au niveau 4 requis, 9 en v5 | 3 amicaux en A (6 joueurs-matchs de plus) | 4 pages du match et page Équipe | non commencé — non vérifié |
| E3 | focus offensif Primary à chaque quart-temps | A = Primary ; B = Normal (référence) | chiffre 6 (focus offensif) : 30 joueurs-quarts Primary requis, 2 en v5 | 7 amicaux en A (4 joueurs-quarts par match) | 4 pages du match et page Équipe | non commencé — non vérifié |
| E4 | aucun (réglage habituel) | — | chiffre 1, 3 points en v5 : 871 tirs requis, 347 disponibles | 16 amicaux de plus | 4 pages du match et page Équipe | non commencé — non vérifié |

Total contrôlé selon l'étude : 4 + 3 + 7 = environ 14 amicaux. L'alternance A, B, A, B appliquée à E2 et E3 ajoute les matchs B (3 et 7) : 24 amicaux contrôlés au lieu de 14. Pour E2 et E3, je retiens les matchs A seuls (la référence B est déjà en base : 22 joueurs-matchs au niveau 2, 91 joueurs-quarts Normal en v5) ; l'alternance vaut pour E1. Faux si un calcul montre que la référence B a changé depuis le passage au moteur v5.

## Veille

| Déclencheur | Condition | Lancement | Ce qu'elle apprend | État | Preuve |
|---|---|---|---|---|---|
| News (devlog) plus vieille que son âge maximal | écran 14 de `core.export_rule` | `aujourdhui.py`, ligne Exports | le devlog à exporter | existe | `core.export_rule` (ordre 14) ; `pipelines/aujourdhui.py:320-335` |
| Export Discord déposé | fichiers dans `data/discord/basketvibe/` | `python pipelines/import_discord.py basketvibe` | les messages en base | à relier | `pipelines/import_discord.py` (docstring) |
| Nouveaux messages en base | lignes de `gold.bv_veille_feed` depuis le dernier passage | agent `veille`, `pipelines/kb_ingest.py` | les règles qui changent (skills à valider) | à relier | `sql/gold/011_bv_veille.sql:13` (15 550 lignes) |

## Nettoyage

| Déclencheur | Condition | Lancement | Ce qu'elle apprend | État | Preuve |
|---|---|---|---|---|---|
| Chaque exécution du plan | toujours | `aujourdhui.py`, journal de durée | le coût du plan | existe | `pipelines/aujourdhui.py:465-470` |
| Plan du jour rendu | ni rejeu ni heure imposée | `aujourdhui.py`, instantané `aujourdhui-<jour>.md` | ce qui a été proposé ce jour-là | existe | `pipelines/aujourdhui.py:507-510` |
| Sauvegarde du bronze ancienne | âge de la dernière sauvegarde | hook de début `pipelines/rappel_debut.py`, `pipelines/sauvegarde_bronze.py` | rien : protège les pages reçues | à relier | `pipelines/rappel_debut.py:33-40` ; hors du plan du jour |
| Type de page reçu et non lu | alerte « page reçue, non lue » dans `gold.bv_couverture_pages` | à créer : ligne du plan du jour | une page à lire ou à ne plus envoyer | à créer | `sql/core/022_page_reader.sql:43` ; ce qui prouvera qu'elle sert : le nombre de types « page reçue, non lue » baisse (91 le 09/11) |

## Trous constatés

### Pages reçues et non lues (`gold.bv_couverture_pages`, lue le 09/11)

91 types « page reçue, non lue » (943 pages), 2 types « lue par gold seulement » (54 pages), 33 types lus (1 143 pages). Les plus fréquents :

| Type de page | Pages | Sert-il à une routine ? |
|---|---|---|
| `/api/v1/leagues/<id>` | 82 | non vérifié : classement ou division (routine Phases de saison) |
| `dom:match` | 63 | non vérifié : doublon possible des pages de match lues par l'API |
| `/api/v1/leagues/<id>/seasons` | 53 | oui, probablement : remplir `core.season` (Phases de saison) |
| `/api/v1/teams/<id>/tactics` | 52 | oui : saisie tactique enregistrée, preuve que la saisie est faite (Chaque match) et réglage de la File d'expériences |
| `/api/v1/teams/<id>/notifications` | 42 | non vérifié : événements (vente, blessure) |
| `/api/v1/leagues/<id>/seasons/<id>/fixtures/round/<n>` | 38 | oui, probablement : heure du coup d'envoi de la ligue (`core.fixture.scheduled_at` vide pour 44 matchs de ligue et 4 de coupe) |
| `/api/v1/teams/<id>` | 31 | non vérifié |
| `dom:friendly` | 31 | non vérifié |
| `/api/v1/teams/<id>/league-fixtures` | 22 | oui, probablement : même besoin que les journées de ligue |
| `/api/v1/teams/<id>/cup-fixtures` | 18 | oui, probablement : heure des matchs de coupe |
| `/api/v1/teams/<id>/my-transfer-offers` | 11 | non vérifié : offres reçues (Marché) |
| `/api/v1/players/<id>/training-history` | 7 | oui, probablement : gains d'entraînement par joueur |
| `/api/v1/teams/<id>/friendlies`, `/my-transfer-auctions` | 40, 14 | lues par `gold.bv_agenda` seulement, pas par silver |

### Calendrier

- `core.fixture` : `scheduled_at` renseigné pour 9 amicaux sur 37, 0 match de ligue sur 44, 0 de coupe sur 4. Les limites de la ligue et de la coupe viennent donc d'une heure écrite dans `core.agenda_rule`, pas du calendrier (critère P1 non tenu par le code).
- `core.season` : 0 ligne pour basketvibe. Aucune phase de saison n'est calculable.

### Doublons de règles et source qui fait foi

| Règle | Où elle est écrite | Source qui fait foi |
|---|---|---|
| Écrans à exporter et âge maximal | `core.export_rule` ; `docs/attentes/jeux/basketvibe.yaml` (exports) ; mots de `MOTS_FAIT` (`aujourdhui.py:41-52`) | `core.export_rule` (critère R1 du registre d'état) |
| Mes enchères seulement avec une enchère ouverte | `core.export_rule.optionnel_si_vide` ; `aujourdhui.py:325-335` | `aujourdhui.py` (seul à connaître les enchères ouvertes) |
| Heures de verrou et d'export | `core.agenda_rule.heure` ; `docs/attentes/jeux/basketvibe.yaml:35-37`, `:73-75` ; skill `basketvibe-saison` | à créer : `core.fixture.scheduled_at` ; d'ici là `core.agenda_rule` |
| Seuils d'alerte (fatigue, forme, joueurs disponibles) | `core.alert_rule` ; skill `basketvibe-joueurs` | `core.alert_rule` (porte la source du skill) |
| Domaines d'alerte retenus | `core.alert_rule.domaine` ; `CAT_ALERTE` (`aujourdhui.py:37-38`, sans `match`) | `core.alert_rule` ; `CAT_ALERTE` à aligner |
| Réserve de sécurité | skill `basketvibe-aujourdhui` ligne fixe (d) : « le script utilise encore la réserve » ; `aujourdhui.py:366-369` : sans réserve | `aujourdhui.py` (PB8 fait) ; la ligne (d) du skill est périmée (`SKILL.md:16`) |
| Matchs joués, aperçu adverse | complément à la main du skill (`SKILL.md:13-15`) ; `aujourdhui.py:336-343` pour l'aperçu | `aujourdhui.py` pour l'aperçu ; les matchs joués restent à la main (alerte `match` à relier) |

### Paramètres écrits à la main (règle 5)

| Paramètre | Valeur | Où |
|---|---|---|
| Âge de déclin | 31 ans | `pipelines/aujourdhui.py:66`, `:405` |
| Poste mince | profondeur ≤ 2 | `pipelines/aujourdhui.py:385` |
| Note visée à l'achat | PS maximal du poste + 1 | `pipelines/aujourdhui.py:391` |
| Affaire fiable | `ref_n ≥ 5` | `pipelines/aujourdhui.py:427` |
| Mes enchères ancienne | 24 h | `pipelines/aujourdhui.py:333` |
| Validité d'une clé de match | 7 jours | `pipelines/aujourdhui.py:35` |
| Âge maximal des écrans | 24, 72 ou 168 h | `core.export_rule.max_age_h` |
| Fatigue hors zone verte, forme basse | 20 ; 1 et 2 | `core.alert_rule` (`fatigue`, `forme_1`, `forme_2`) |

## Étape 5 : à faire, dans l'ordre

| # | Action | Effort |
|---|---|---|
| 1 | Relier les alertes de domaine `match` au plan (`CAT_ALERTE`) et lancer `analyste` sur une défaite de ligue ou de coupe | petit |
| 2 | Supprimer la ligne fixe (d) périmée du skill `basketvibe-aujourdhui` | petit |
| 3 | Appeler `rafraichir_avant_aujourdhui.py` et `evaluer_decisions.py` avant le plan | petit |
| 4 | Lire les journées de ligue et de coupe en silver et remplir `core.fixture.scheduled_at` ; limites calculées depuis le coup d'envoi | moyen |
| 5 | Créer la file d'expériences amicales (table et ligne du plan : réglage du prochain amical), avec E1 à E4 | moyen |
| 6 | Relier `gold.bv_sell_candidates` (masse salariale à force constante) et `gold.bv_academy_prospects` (tous les prospects) au plan | moyen |
| 7 | Relier entraînement (`gold.bv_saisie_entrainement`), fatigue projetée (`gold.bv_fatigue_plan`), focus adverse (`gold.bv_match_opp_focus`) et projection de saison | moyen |
| 8 | Lire `/api/v1/teams/<id>/tactics` en silver (preuve de saisie, réglages des expériences) | moyen |
| 9 | Recalcul hebdomadaire de chaque paramètre écrit à la main, avec sa date de calcul | gros |
| 10 | Remplir `core.season` (phases) depuis `/api/v1/leagues/<id>/seasons` | moyen |
| 11 | Ligne « pages reçues, non lues » dans le plan et tri des 91 types (lire ou ne plus envoyer) | gros |
| 12 | Veille : import Discord et agent `veille` déclenchés par l'arrivée de messages | petit |
