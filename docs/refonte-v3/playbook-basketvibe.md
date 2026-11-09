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

## Chaque semaine

| Déclencheur | Condition | Lancement | Ce qu'elle apprend | État | Preuve |
|---|---|---|---|---|---|
| Fin de semaine | matchs de la semaine en base | `gold.bv_match_report`, `gold.bv_match_trends` : revue de tous les matchs | ce qui a marché, les L-nnn | à relier | `docs/attentes/tests/basketvibe.yaml:201`, `:210` (bilan de la semaine) ; `sql/gold/003_bv_match_report.sql:6` |
| Fin de semaine | conseils dont l'échéance est passée | `python pipelines/evaluer_decisions.py` | si les conseils ont marché | à relier | `learn.decision` : 107 conseils « proposed » échus non jugés (premier le 16/10), `gold.decisions_a_evaluer` : 0 ligne, `learn.outcome` : 0 ligne (lus le 09/11) : la vue ne remonte pas les conseils échus |
| Fin de semaine | ventes de la semaine en base | `gold.bv_price_ref_ps`, `gold.bv_market_price_ref` : prix de référence ; seuils recalculés (Chaque cycle, « Nouvelle semaine ») | les prix du marché à jour | à relier | `sql/gold/022_bv_transfer_history.sql:45` ; `sql/gold/006_bv_transfers.sql:11` |
| Fin de semaine | matchs d'autres équipes exportés | `python -I pipelines/preanalyse_matchs_basketvibe.py` | si une question passe « décidable » | à relier | `docs/refonte-v3/preanalyse-matchs-basketvibe.md`, étape 4 (b) ; hors du plan du jour |
| Fin de semaine : veille | nouveaux messages Discord depuis le curseur | `python pipelines/kb_ingest.py estimer`, agent `veille` | le delta de la semaine | à relier | `pipelines/kb_ingest.py` (docstring) ; table `kb.ingest_cursor` (lue le 09/11) |
| Fin de semaine : versions du moteur | annonce de version | à créer : table des versions du moteur (date, compétition, version) | à quel moteur appartient chaque match et chaque conseil | à créer | aucune table de versions (`learn`, `kb`, `core` lus le 09/11) ; versions déduites des dates (`preanalyse-matchs-basketvibe.md`, étape 4 (c)) ; ce qui prouvera qu'elle sert : 0 match « à la frontière » mal classé dans l'étude rejouée |
| Fin de semaine : couverture des sources | types de pages reçus | `gold.bv_couverture_pages` | les pages reçues et non lues | à relier | `sql/core/022_page_reader.sql:43` (91 types non lus le 09/11) |

### Remise en question du modèle (chaque semaine)

| Question | Mesure | Ce qui existe en base | État | Ce qui prouvera qu'elle sert |
|---|---|---|---|---|
| Prédictions contre résultats, et biais | part de prédictions justes ; biais = prédit moins observé, par domaine | `learn.decision` : 109 proposées, 32 faites ; `learn.outcome` : 0 ligne | à créer | prouvera : le taux de prédictions justes est publié chaque semaine et le biais baisse sur 4 semaines |
| Part de variance expliquée | r² de la marge prédite contre la marge observée, en ligue v4 | préanalyse : r = 0,65 en ligue v3 (scores seuls, historique, r² ≈ 0,42) ; ligue v4 : « n trop petit » | à créer | prouvera : r² calculé chaque semaine sur la ligue v4 dès 30 matchs avec force connue |
| Cinq matchs les plus mal prédits | écart absolu entre marge prédite et marge observée, 5 plus grands | `estimated_chance` des pages de match (27 pages, étude, faisabilité 4 (c)) ; aucune prédiction de marge stockée | à créer | prouvera : chacun des 5 matchs a une cause écrite et une règle revue |
| Règles confirmées retestées | taux de réussite de chaque leçon validée sur les matchs de la semaine | `learn.lesson` : 3 « validated », 34 « hypothesis » | à créer | prouvera : une leçon validée qui échoue 2 semaines repasse en hypothèse |
| Hypothèses bloquées | hypothèses sans nouvelle mesure depuis 2 semaines, et la donnée qui manque | `learn.lesson` : 34 « hypothesis » | à créer | prouvera : le nombre d'hypothèses bloquées baisse |
| Données non collectées | types de pages non lus ; pages manquantes de l'étude | `gold.bv_couverture_pages` (91 types non lus) ; étude, étape 4 (b) | à relier | le nombre de types non lus baisse chaque semaine |
| Ce que font les meilleures équipes | profil des meilleurs joueurs et des 3 premiers du classement | `gold.bv_league_top_players` ; tactiques adverses illisibles (préanalyse, étape 4 (c)) | à relier | une différence chiffrée avec notre effectif, reprise dans une décision d'achat ou de composition |
| Le playbook lui-même | routines jamais déclenchées en 4 semaines | aucun journal de déclenchement ; G1 et G2 « jamais déclenchée sur ces 19 matchs » (`regles-decision-basketvibe.yaml:266`) | à créer | prouvera : chaque routine jamais déclenchée est supprimée ou sa condition corrigée |

## Coupe

Règles de la BasketVibe Cup, édition saison 2 (`.claude/skills/basketvibe-saison/references/05-coupes.md:6`, [News 2026-11-03]) : 10 tours ; premier tour jeudi 12/11/2026, puis jeudis et dimanches ; finale dimanche 13/12/2026 ; même coup d'envoi pour tous, non modifiable, tactique verrouillée au coup d'envoi ; tableau complété par des bots ; prime de 100 000 par équipe ; fatigue = 25 % de celle de la ligue ; billetterie 0 ; blessures désactivées ; avantage du terrain désactivé ; expérience non citée (ne pas la supposer). Règle générale : le plus faible reçoit (`05-coupes.md:3`).

Déjà saisi en base (lu le 09/11) : `core.fixture` a 4 matchs de coupe, du 28/10 au 31/10 (2 joués, 2 gagnés), aucun de l'édition saison 2, aucun avec heure ; `core.agenda_rule` n'a aucune règle de coupe ; `core.alert_rule` a `coupe_sans_resultat`.

| Déclencheur | Condition | Lancement | Ce qu'elle apprend | État | Preuve |
|---|---|---|---|---|---|
| Calendrier de coupe exporté | page `/api/v1/teams/<id>/cup-fixtures` reçue | à créer : lecture en silver vers `core.fixture` | les 10 tours datés | à créer | `gold.bv_couverture_pages` : 18 pages, « page reçue, non lue » ; ce qui prouvera qu'elle sert : les tours de l'édition saison 2 sont dans `core.fixture` avant le premier tour |
| Match de coupe à venir | ligne de coupe dans `core.fixture`, limite = coup d'envoi | à créer : règle de coupe dans `core.agenda_rule` (saisie et verrou) | la saisie de coupe à faire | à créer | `core.agenda_rule` (aucune règle de coupe) ; ce qui prouvera qu'elle sert : chaque match de coupe a sa saisie déclarée avant le verrou |
| Match de coupe joué non exporté | règle `coupe_sans_resultat` | `gold.bv_daily_alerts` ; domaine `match` ignoré par `aujourdhui.py` | l'export à faire | à relier | `core.alert_rule` (`coupe_sans_resultat`) ; `pipelines/aujourdhui.py:37-38` |
| Défaite de coupe | `my_result = 'L'` en coupe | agent `analyste` (arbitrage 15) | les causes | à relier | voir « Chaque match » ; `docs/regles/actives.md:35` (S3) |

## Sur événement

| Déclencheur | Condition | Lancement | Ce qu'elle apprend | État | Preuve |
|---|---|---|---|---|---|
| Joueur de 31 ans ou plus | ligne de `gold.bv_roster_now` | `aujourdhui.py` : « Mets X en vente » | le déclin à venir | existe | `pipelines/aujourdhui.py:398-405` |
| Poste mince ou faible | profondeur basse ou PS moyen le plus bas (`gold.bv_position_summary`), candidat au marché | `aujourdhui.py` : « Acheter un X de note ≥ … » | le poste à renforcer | existe | `pipelines/aujourdhui.py:381-397` |
| Blessure, fatigue, forme | règle de `core.alert_rule` | `gold.bv_daily_alerts` lu par `aujourdhui.py` | le joueur à ménager | existe | `pipelines/aujourdhui.py:351-358` |
| Vente pour profit, place aux jeunes | toujours | `aujourdhui.py`, ligne « Garder » | rien de décidé : « règle non écrite — à valider » | existe | `pipelines/aujourdhui.py:406-407` |
| Fatigue projetée | ligne de `gold.bv_fatigue_plan` | vue | les minutes à couper avant le match | à relier | `sql/gold/004_bv_tactics.sql:75` (280 lignes) |
| Gros transfert | montant au-dessus de `SEUIL_GROS_MONTANT` | `python pipelines/dossier.py basketvibe <type>` puis agent `police` (hook `pipelines/police.py`) | si la décision repose sur toutes les informations | existe | `pipelines/aujourdhui.py:287` ; `.claude/settings.json:74` |
| Deux défaites de ligue de suite | `my_result = 'L'` deux fois de suite en ligue, amicaux exclus (G3) | `gold.match_objective` (règle `serie` de `core.objective_rule`) ; agent `analyste` le soir même | les causes chiffrées ; un changement fort ce soir | à relier | `docs/attentes/regles-decision-basketvibe.yaml:271-275` ; `sql/gold/070_match_objective.sql:7` ; `gold.match_objective` (10 lignes basketvibe) ; absente des requêtes de `pipelines/aujourdhui.py:54-78` |
| Troisième défaite de suite | série de 3 défaites ou plus, toutes compétitions | brief de l'agent `match` : au moins un changement de composition ou de tactique chiffré | si le changement chiffré corrige la série | à relier | `.claude/agents/match.md:54` ; hors du plan du jour |
| Levier échoué deux fois | 2 échecs ou plus sur un même levier | agent `match` : levier interdit, levier différent nommé ; `docs/regles/actives.md:32` (K10) | quels leviers ne marchent pas | à créer | `.claude/agents/match.md:53` (consigne d'agent, aucun contrôle par code) ; `learn.outcome` : 0 ligne, donc aucun échec compté ; ce qui prouvera qu'elle sert : 0 décision proposée sur un levier qui a 2 échecs dans `learn.outcome` |
| Titre acquis ou rien à jouer | condition `titre_acquis` ou `rien_a_jouer` de `core.objective_rule` | `gold.match_objective` (objectif `former`, `tester`) | minutes aux jeunes sans risque de classement | à relier | `core.objective_rule` (règles `titre`, `rien`, `titre_former`, `rien_former`, lues le 09/11) ; `docs/attentes/regles-decision-basketvibe.yaml:9`, `:79-87` (EFF-4) |
| Moins de 5 joueurs éligibles | joueurs disponibles < 5 | à créer : règle de `core.alert_rule` « forfait » | le forfait évité (défaite 20-0) | à créer | `.claude/skills/basketvibe-saison/references/02-ligue-et-saison.md:4` ; `core.alert_rule` n'a que `dispo` (moins de 9 joueurs : vente impossible) ; ce qui prouvera qu'elle sert : rejouée sur l'historique, l'alerte sort chaque jour où `available_players` < 5, et 0 forfait en base |
| Solde projeté proche de zéro | solde de fin de saison projeté bas (FIN, « solde proche de 0 ») | `gold.bv_finance_projection` : cause | la charge qui fait baisser le solde | à relier | `docs/attentes/regles-decision-basketvibe.yaml:32` ; `sql/gold/018_bv_fixes_2026_10_22.sql:11` |
| Solde proche de zéro : enchères | capacité = solde moins les enchères ouvertes | `aujourdhui.py` : toute enchère hors capacité est abandonnée | la limite d'enchère du jour | existe | `pipelines/aujourdhui.py:366-379` |
| Joueur qui gagne une compétence | hausse d'une compétence dans `gold.bv_skill_progress_weekly` | `gold.bv_slot_fit`, `gold.bv_potential_estimate` | le poste et le potentiel recalculés | à relier | `sql/gold/001_bv_gold.sql:77` ; `sql/gold/004_bv_tactics.sql:32` ; `sql/gold/005_bv_training.sql:48` |
| Annonce du développeur ou nouvelle version du moteur | nouvelle News ou message du développeur | à créer : version du moteur sur chaque conseil (`learn.decision`), conseils de l'ancienne version marqués périmés | quels conseils ne valent plus | à créer | `.claude/skills/basketvibe-communaute/references/02-1-moteur-de-match-versions-et-calibrage.md:2` (versions v3, v4, v5) ; aucune table de versions en base (`learn`, `kb`, `core` lus le 09/11) ; ce qui prouvera qu'elle sert : le jour d'un changement de version, 100 % des conseils ouverts de l'ancienne version sont marqués périmés |
| Test de la file au nombre de matchs requis | n disponible ≥ n requis (étude) ou échéance du test (n = 3 au départ) | à créer : verdict confirmé, réfuté ou non concluant | si le réglage testé marche | à créer | `docs/attentes/regles-decision-basketvibe.yaml:278-288` ; ce qui prouvera qu'elle sert : chaque expérience E1 à E4 a son verdict écrit le jour où son n est atteint |

## Phases de saison

| Déclencheur | Condition | Lancement | Ce qu'elle apprend | État | Preuve |
|---|---|---|---|---|---|
| Dernier match de la saison | règle `fin_saison` | `gold.bv_agenda` lu par `aujourdhui.py` | maintien et prime de classement | existe | `core.agenda_rule` (`fin_saison`) |
| Début de saison : sponsor | nouvelle saison ; date limite = 1re journée moins le délai du jeu (sinon contrat Stability) | à créer : ligne du plan avec les six offres comparées à la force du club | le contrat qui rapporte le plus pour notre niveau | à créer | `.claude/skills/basketvibe-economie/references/02-recettes.md:12` ; `docs/attentes/attentes.md:37` (A-11) ; ce qui prouvera qu'elle sert : le sponsor est choisi avant la date limite, et l'écart entre prime prévue et prime touchée est mesuré en fin de saison |
| Début de saison : forme, fatigue, popularité | 1er jour de la saison | à créer : contrôle des remises à zéro lues en base | si le jeu applique ses règles | à créer | `.claude/skills/basketvibe-saison/references/02-ligue-et-saison.md:11` (forme 6, fatigue 0, popularité 70 %) ; ce qui prouvera qu'elle sert : écart entre valeurs lues le 1er jour et valeurs du skill = 0, ou écart signalé |
| Début de saison : objectif, marketing | nouvelle saison | à créer | objectif du sponsor, personnel marketing | à créer | non vérifié (moment de la décision : aucune source ; faits : `02-recettes.md:13`, `.claude/skills/basketvibe-economie/references/03-depenses.md:17`) ; ce qui prouvera qu'elle sert : popularité de fin de saison comparée à celle de la saison 1 |
| Milieu de saison : bilan | moitié des journées jouées | à créer | où en est l'objectif, ce qu'il faut changer | à créer | non vérifié (aucune source) ; ce qui prouvera qu'elle sert : au moins une décision prise au bilan, avec sa prédiction dans `learn.decision` |
| Fin de saison : ventes avant le recalcul des salaires | dernières journées | à créer : liste des ventes à faire avant le changement de saison | la masse salariale de la saison suivante | à créer | fait : salaires recalculés en nouvelle saison (`02-ligue-et-saison.md:11`) ; règle « vendre avant » : non vérifié (consigne de l'utilisateur, aucune source écrite) ; ce qui prouvera qu'elle sert : masse salariale du 1er jour de la saison suivante plus basse que sans les ventes |
| Fin de saison : primes, âge, retraite | dernière journée | à créer : primes de classement, +1 an, retraite à 38 ans | les recettes de fin et les départs | à créer | `.claude/skills/basketvibe-economie/references/02-recettes.md:21` ; `02-ligue-et-saison.md:11` ; ce qui prouvera qu'elle sert : chaque départ à la retraite annoncé avant la fin, 0 surprise |
| Entre deux saisons | semaine sans match de ligue | à créer : déroulé A-11 (sponsor, nouvelle ligue, effectifs) | la préparation de la saison | à créer | `.claude/skills/basketvibe-saison/references/03-fin-de-la-saison-1-saison-2-dates-2026.md:3` ; `docs/attentes/attentes.md:37` ; ce qui prouvera qu'elle sert : les étapes d'A-11 faites avant la 1re journée |
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
| Fin de semaine | toujours | à créer : inventaire en lecture seule (tableau ci-dessous), rien n'est supprimé sans accord | ce qui encombre le contexte des agents | à créer | ce qui prouvera qu'elle sert : chaque chiffre de l'inventaire baisse ou reste stable d'une semaine sur l'autre |

Inventaire en lecture seule (mesuré le 09/11 dans le dépôt et la base) :

| Objet | Chiffre | Commande |
|---|---|---|
| Briefs | 75 fichiers, dont 60 d'octobre | `find outputs/basketvibe/briefs -type f`, `-name '2026-10-*'` |
| Registres `fait-*` | 14 (du 24/10 au 08/11) ; le plan n'en lit que 7 jours | `ls outputs/basketvibe/fait-*.md` ; `pipelines/aujourdhui.py:35` |
| Veilles | 13 fichiers | `find outputs/basketvibe/veille -type f` |
| Notes de session | 3 (`resume-session-2026-11-06.md`, `session-2026-11-07.md`, `session-2026-11-08.md`) et `discussion-2026-11-06.md` | `ls outputs/basketvibe` |
| Vues gold `bv_*` sans référence | 5 sur 53 hors de leur définition (`bv_academy_chat`, `bv_academy_prospects`, `bv_finance_season_rates`, `bv_resale_stats`, `bv_training_options`) ; 16 sur 53 si l'on ne compte que `pipelines/` et `.claude/` | script de recherche (scratchpad), sur `pipelines`, `.claude`, `sql` |
| Connaissance en double | `kb.claim` basketvibe : 375 lignes, 375 textes distincts (0 doublon exact) ; doublons de règles : « Trous constatés » | `select count(*), count(distinct lower(text)) from kb.claim where game='basketvibe'` |
| Conseils périmés | `learn.decision` : 107 « proposed » échus non jugés, 1 « expired » | `select … from learn.decision where game='basketvibe'` |

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

Ajouts du 09/11 (routines convenues), classés par effort :

| # | Action | Effort |
|---|---|---|
| 13 | Lire `gold.match_objective` dans le plan : série de 2 défaites de ligue (analyste), titre acquis ou rien à jouer (jeunes) | petit |
| 14 | Règle d'alerte « moins de 5 joueurs éligibles » (forfait) dans `core.alert_rule` | petit |
| 15 | Relier défaite de coupe et `coupe_sans_resultat` au plan (même correction que l'action 1) | petit |
| 16 | Lire `gold.bv_finance_projection` dans le plan quand le solde projeté est bas (cause) | petit |
| 17 | Lancer `preanalyse_matchs_basketvibe.py` et `kb_ingest.py estimer` chaque semaine | petit |
| 18 | Inventaire de nettoyage hebdomadaire en lecture seule | petit |
| 19 | Comprendre pourquoi `gold.decisions_a_evaluer` est vide alors que 107 conseils sont échus, puis évaluer chaque semaine | moyen |
| 20 | Calendrier de la coupe saison 2 en base et règle de coupe dans `core.agenda_rule` | moyen |
| 21 | Compétence gagnée : poste et potentiel recalculés dans le plan | moyen |
| 22 | Verdict automatique d'un test de la file à son n requis | moyen |
| 23 | Table des versions du moteur ; version sur chaque conseil, conseils périmés au changement | moyen |
| 24 | Revue hebdomadaire des matchs et des prix de référence | moyen |
| 25 | Phases de saison : début (sponsor, remises à zéro, objectif, marketing), milieu (bilan), fin (ventes avant le recalcul des salaires, primes, âge, retraite), entre deux saisons | gros |
| 26 | Contrôle par code du levier échoué deux fois (`learn.outcome`) | gros |

## Étape 6 : à faire, dans l'ordre

| # | Action | Effort |
|---|---|---|
| 1 | **Remise en question hebdomadaire du modèle** (tableau de « Chaque semaine ») : prédictions contre résultats et biais, variance expliquée, cinq matchs les plus mal prédits, règles confirmées retestées, hypothèses bloquées, données non collectées, meilleures équipes, routines jamais déclenchées | gros |
