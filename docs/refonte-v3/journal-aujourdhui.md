# Journal de `aujourdhui.py` (BasketVibe)

## Critères d'acceptation (écrits le 2026-11-06, avant le code ; le script doit produire le même « que faire » que le skill `basketvibe-aujourdhui`, en plus complet que les vues seules)

Jeu d'essai figé : `pipelines/jeu_essai/2026-11-06/` (copie des fichiers du 06/11). Test : `pipelines/test_aujourdhui.py` ; aucun commit de code tant qu'il n'est pas vert.

| # | Critère | Vérifié par |
|---|---|---|
| L1 | Brief tactique du jour (`briefs/<jour>-tactique.md`, `-tactique-amical.md`) : une ligne par match avec l'heure limite (verrou) et les tests « prouvera que j'avais tort ». Absent : le plus récent du même type. Plus de 3 jours pour un match du jour : la ligne le dit. | Plan 06/11 : Póvoa 19:45, Knight Jays 07:45 |
| L2 | Dossier d'achat (`dossier/<jour>-achat.md`) et `police-<jour>.md` : une ligne par cible avec montant maximum et heure limite (fin d'enchère en base). `police-<jour>.md` absent : la ligne dit « police d'abord ». | Plan 06/11 : Fujita 150 000, Stankevičius 100 000, police d'abord |
| L3 | Registre `fait-<jour>.md` : une ligne « reste à corriger / à faire » sort comme action (une par réglage), elle n'est pas seulement retirée. | Plan 06/11 : Knight Jays + 4 corrections d'écran |
| L4 | `learnings.md` : conseils ouverts dont l'échéance (date du critère) tombe aujourd'hui ou demain. | Fichier figé |
| F1 | Au plus 8 lignes, `HH:MM — action — détail (source)`, triées par heure limite (ce qui a une heure limite en tête), dernière ligne « Exports à faire aujourd'hui : … ». Le surplus va dans une ligne « Autres points ». Aucune ligne `clé=valeur`. | Sortie 06/11 |
| F2 | Le Personnel reste étiqueté Personnel. | Sortie 06/11 |
| D1 | Poste le plus faible : « acheter un <poste> de note ≥ X » ou « garder » en demi-ligne (jamais en ligne). Finances et transferts : même règle. Une règle absente de `docs/attentes/regles-decision-basketvibe.yaml` est marquée « (à valider) ». | Sortie 06/11 |

## Hockey Nation — `pipelines/aujourdhui_hockeynation.py` (critères H1 à H7, écrits le 2026-11-06 avant le code)
Même plan que le skill `hockeynation-aujourdhui` (il fait foi, le script ne le réécrit pas). Lecture seule, sans modèle ni agent, **8 requêtes au plus** via `sql.py`, **60 secondes au plus**. `--temps 1` = Lire (blocs 1 à 3), `--temps 2` = Agir (blocs 4 et 5, **5 actions au plus**). Écrit `outputs/hockeynation/aujourdhui-AAAA-MM-JJ.md` et une ligne de durée dans le tableau ci-dessous. Réutilise `aujourdhui_sources.py` (lecture du registre `fait-<jour>.md`) et `match_engine_etat.py` (registre des règles). Les 8 requêtes : (1) divers (exports, jour de saison, plafond, contrôle de lineup, derniers journaux d'entraînement), (2) liste des scouts, (3) cibles des scouts, (4) scouts embauchés, (5) matchs avec détail (tirs, xG, périodes, PP), (6) tous les matchs de nos équipes (joué ou à venir, avec ou sans détail), (7) gardiens, (8) plan d'entraînement.
| # | Critère | Mesure |
|---|---|---|
| H1 | **Bloc 1.** Trois exports seulement : Roster (4 équipes), page du match d'avant de chaque équipe, Scouting staff. Roster et Scouting staff : demandés si leur statut n'est pas « à jour ». Page du match : demandée pour l'équipe dont le dernier match joué n'a pas de détail en base. Training : seulement si son dernier journal est plus vieux que la dernière ligne du registre du jour qui parle d'entraînement avec « changé », « modifié » ou « saisi », ou s'il manque pour PRO ou FRM. **Un export cité comme refait / exporté dans `fait-<jour>.md` n'est jamais redemandé.** | Un export déjà dans le registre n'apparaît pas ; une ligne par export en retard |
| H2 | **Bloc 2.** Un tableau, une ligne par scout, sa cible : la première cible de la catégorie A (poste + nation), sinon B (poste), sinon C (nation), par rang croissant, avec 0 rapport. Une cible dont le nom figure dans une ligne « déjà scouté » de `fait-<jour>.md` ou dans `silver.hn_declared` est retirée. Constat avant le code : `silver.hn_declared` n'a aucune ligne de ce genre (types : scouts embauchés, joueurs bloqués, coachs…) ; seul le registre porte « Kevin Uden déjà scouté ». Relevé Scouting plus vieux que 24 h : ligne Export. | Un scout = une ligne ; Uden absent des cibles |
| H3 | **Bloc 3.** Une ligne par match joué des 4 équipes depuis le dernier passage (matchs de ligue et amicaux, victoire ou défaite) : équipe, numéro (rang de ligue de l'équipe cette saison, plus la date ; les amicaux à part), résultat = `my_result`, jamais le score brut, « mérité ou non » avec le nombre de matchs de la comparaison, règle pour ou contre dite en mots. Un match sans `team_level` est rattaché à l'équipe de notre club (`silver.hn_my_teams`) qui y joue ; sinon ligne « équipe inconnue » visible, jamais ignorée. **Constat avant le code : aucun match de nos clubs n'a `team_level` vide dans la base du 2026-11-06 (0 sur 278) ; les deux matchs « sans équipe » du jeu d'essai (jours 10 et 11) sont donc fabriqués en vidant `team_level` de deux matchs réels, et le jeu d'essai le dit.** | 0 ligne ignorée |
| H3a | **Mérité ou non.** Sur la ligue de la saison en cours de l'équipe (les autres matchs de l'équipe, n affiché) : volume = xG nous contre xG eux ; réalisation = buts ÷ tirs ; arrêts = arrêts ÷ tirs subis du gardien. Défaite « non méritée » si volume en notre faveur (xG nous > eux) et réalisation ou arrêts sous la moyenne de l'équipe ; victoire « non méritée » si volume contre nous (xG nous < eux) et réalisation ou arrêts au-dessus de la moyenne ; « mérité » si le volume va dans le sens du résultat ; sinon « indéterminé ». | Nombre de matchs de comparaison dans la cellule |
| H3b | **Pouvait-on gagner (défaite).** « Oui » si xG nous > eux ET (réalisation du match OU arrêts du match) avec un intervalle de Wilson à 95 % entièrement sous la moyenne de l'équipe ; « non » si xG nous < eux ET tirs nous < tirs eux ; sinon « indéterminé », intervalle affiché. **Changer la structure : « oui » seulement si « pouvait-on gagner » = non ET le volume est contre nous dans au moins 3 des 5 derniers matchs de ligue de l'équipe (n affiché) ; sinon « non », avec le chiffre.** Les seuils (3 sur 5) sont à valider. Échelle de la charte en une cellule : composition (contrôle de lineup pour PRO, « non lu » pour les autres), tactique (« non mesurable »), force relative (xG), hasard (écart de réalisation ou d'arrêts décelable ou non). | Chiffre et intervalle dans la cellule |
| H4 | **Bloc 4, déclenché seulement par** (a) l'export Lineups PRO plus vieux que la dernière ligne du registre du jour qui parle de lineup avec « changée », « modifiée » ou « changement » ; (b) un contrôle de lineup en défaut (`gold.hn_tactique_controle` ou une case de `gold.hn_saisie_lignes` dont `controle` n'est pas `ok`) ; (c) un test arrivé à échéance : plan de jeu short, 10 matchs de ligue PRO depuis le 2026-10-29 ; PP/PK, 5 matchs de ligue PRO depuis le 2026-11-02 (date de la décision de PP1/PP2, **à valider**) ; (d) deux défaites de suite en ligue d'une équipe ; (e) nouveau joueur : **non mesurable aujourd'hui** (`silver.hn_players` ne garde qu'un seul relevé, 2026-11-06) ; lu seulement dans le registre du jour (ligne avec « nouveau joueur », « monté » ou « signé »). Aucun déclencheur = bloc absent. Plafond salarial négatif (`silver.hn_cap_now`) = ligne 🟥, seule alerte hors plan. | Bloc absent sans déclencheur |
| H5 | **Bloc 5.** Un tableau par équipe (PRO, FRM, U21, U17, jamais mélangés) : ordre de choix, joueur, compétence, coach, lus dans `gold.hn_training_plan`, qui ne propose que des compétences ouvertes (règle du skill, § 5 : « jamais une compétence déjà au plafond »). Un joueur sans compétence ouverte est en fin de liste, « aucune compétence ouverte ». U21 et U17 : l'ordre seul. | Aucune compétence plafonnée proposée |
| H6 | **Format.** Le rendu passe `pipelines/forme.py` : `pipelines/forme.py` reconnaît pour Hockey Nation le plan (Priorité, Catégorie, Action), le tableau d'effectif (Poste, Joueur, Note, Endurance, FOF) et le tableau de plan de jeu (Paramètre, Cible, Dans le jeu), avec 4 équipes exigées pour tout rendu d'effectif. **Différence : il n'existe pas de format Hockey Nation pour les tableaux de scouts, de matchs et d'ordre d'entraînement ; ils passent comme formats inconnus.** Aucun code interne dans le rendu : règles dites en mots (pas de numéro L-nnn, C-nnn ni de code de saison), pas de nom de vue. | `pipelines/forme.py` ne relève rien sur le rendu |
| H7 | **Tests figés.** Jeu d'essai du 2026-11-06 dans `pipelines/jeu_essai/hockeynation/2026-11-06/` et `pipelines/test_aujourdhui_hockeynation.py` : un cas par critère H1 à H6, dont les deux matchs sans équipe et la lineup à 18 cases vides. Tous verts avant tout commit de code ; les 55 tests de `aujourdhui.py` restent verts. | Tests verts |

## Porte BasketVibe (critères écrits le 2026-11-09, avant le branchement ; jour 1 = 2026-11-09)

Constat avant le branchement : `basketvibe-aujourdhui` ne citait pas `pipelines/aujourdhui.py` ; le script n'a donc pas servi le week-end du 07 au 08/11.

| # | Critère |
|---|---|
| PB1 | **Branchement.** Pour « que faire », « reprenons » ou « plan du jour » BasketVibe, la première action est `python -I pipelines/aujourdhui.py basketvibe`. Sa sortie est affichée telle quelle, sans reformulation, sans tableau. Aucune requête avant : le script lit lui-même le registre du jour. |
| PB2 | **Complément à la main**, une ligne chacun, sous la sortie du script, jusqu'à l'étape 5 du plan : (a) matchs joués depuis le dernier passage, résultat par `my_result` (`gold.bv_match_report` ; `silver.bv_fixtures` pour un match de ligue joué non exporté) ; (b) académie, seulement si un rapport est arrivé depuis le dernier passage ; (c) aperçu adverse et brief tactique du prochain match de ligue ou de coupe : `gold.bv_saisie_adversaires` et dernier brief, sinon « brief manquant » ; (d) une ligne fixe : « Règle du 09/11 : pas de réserve fixe, solde jamais négatif ; le script utilise encore la réserve, sa ligne de capacité est à ignorer ». |
| PB3 | **Hooks.** La réponse passe `forme.py` et `controle.py` sans que leurs règles changent. Si un hook rejette, seule la ligne rejetée est corrigée, et le rejet est noté ici. |
| PB4 | **Porte de 5 jours.** Chaque jour l'utilisateur donne quatre lignes : verdict (mieux, équivalent ou moins bien que la réponse habituelle), il manquait, en trop, faux. Réussite : au moins 4 jours sur 5 « mieux » ou « équivalent », et aucun « faux » sur un fait (état, donnée, résultat) deux jours de suite. Les quatre lignes sont inscrites dans le tableau ci-dessous le jour même, sans interprétation ni défense. Les « il manquait » forment la liste de l'étape 5 du plan. |

### Corrections de la sortie du 09/11 (critères écrits le 2026-11-09, avant le code ; sortie fautive : `outputs/basketvibe/aujourdhui-2026-11-09.md`)
| # | Critère | Test figé |
|---|---|---|
| PB5 | **Registre.** Une ligne de n'importe quel `fait-<jour>.md` antérieur ou égal au jour, qui déclare la saisie d'un match à venir (adversaire, date), retire l'action de saisie de ce match. | La ligne de 10:34 UTC de `fait-2026-11-08.md` (amical Garden City du 09/11) supprime « saisis la tactique » pour ce match. |
| PB6 | **Mes enchères.** Jamais en ligne Export s'il n'y a aucune enchère d'achat dont la fin est dans le futur (règle de `docs/memoire-claude/feedback-bv-mes-encheres-vide-si-aucune-enchere.md`, à coder). | 09/11 : aucune ligne Mes enchères. |
| PB7 | **Enchère terminée.** Une décision d'achat dont l'heure de fin est passée n'est plus une action. Elle sort en une ligne « terminée le <jour> : résultat lu dans silver.bv_transfers (acheté ou non) ». Le script reste en lecture seule. | Fujita et Stankevičius au 09/11. |
| PB8 | **Capacité.** Solde moins les enchères encore ouvertes, sans réserve (décision de l'utilisateur du 09/11 : solde jamais négatif, on dépense pour être meilleur). Le texte « réserve de sécurité à valider » disparaît. `docs/attentes/regles-decision-basketvibe.yaml` : les règles qui citent la réserve (lignes 29, 107, 145) portent la date et la source de la décision. Seuls les tests existants qui encodent l'ancienne réserve changent. | Capacité = solde − enchères ouvertes ; plus de « réserve » dans la sortie. |
| PB9 | **Heure.** Une action dont le verrou est passé n'est plus « à faire maintenant ». Heure de Paris par `pipelines/heure_paris.py` ; option `--maintenant HH:MM` pour les tests, défaut inchangé. | À 09:18, la ligne amical de 07:45 est absente. |

**Résultat des corrections (2026-11-09 10:35, heure de Paris).** Commits : PB5 `cd8bfa5`, PB6 `487c492`, PB7 `b92c314`, PB8 `198e83d`, PB9 `bddd7bd`, PB9 suite `0af86f6`. `python -I pipelines/test_aujourdhui.py | tail -1` → `90/90` (55 d'origine, dont 2 réécrits pour la réserve : « capacité restante » et « E8 », plus la fixture `capacite` remplacée par `balance`).
- Écart de lecture à connaître : PB7 demande « une ligne » ; la ligne « terminée le … » sort comme élément de « Autres points », pas comme neuvième ligne (le format limite à 8 lignes).
- Ajout hors critères, même principe que PB9 : une enchère du Marché (`gold.bv_market_bargains`, `gold.bv_market_candidates`) dont la fin est passée n'est plus proposée (le script proposait Zhang et Tan, finies le 08/11 à 19:55 et 19:56 ; commit `0af86f6`).
- Reste dans le plan : « Après l'amical (~08:55) : exporter la page du match », ligne d'export de l'agenda dont l'heure est passée mais dont l'action (exporter) reste à faire ; ce n'est pas un verrou. À trancher par l'utilisateur.
- Les deux fichiers d'origine (briefs, registre) du jeu d'essai du 09/11 sont des copies figées dans `pipelines/jeu_essai/2026-11-09/`.

### Retours de la Porte (quatre lignes de l'utilisateur, inscrites telles quelles)
| Jour | Verdict | Il manquait | En trop | Faux |
|---|---|---|---|---|

### Rejets de hooks pendant la Porte
| Jour | Hook | Ligne rejetée | Correction |
|---|---|---|---|

## Registre d'état (critères écrits le 2026-11-09, avant le code ; jour 1 = 2026-11-09)

| # | Critère |
|---|---|
| R1 | **Une seule liste.** `core.export_rule` porte les 14 écrans de BasketVibe (ordre, motif d'endpoint, âge maximal, raison, colonne `optionnel_si_vide`) ; `gold.bv_exports_state` est redéfinie depuis cette table, avec les mêmes colonnes et le même nombre de lignes qu'avant. |
| R2 | **Arrivée lue dans `bronze.raw_pages`** (toute page reçue, traitée en silver ou non), pas seulement dans `silver.bv_api`. |
| R3 | **Écran optionnel si vide.** Un écran « optionnel si vide » sans page récente sort en statut « 🟩 optionnel », jamais « à refaire » (Mes enchères). **Corrigé :** « optionnel » ne cache la ligne Mes enchères que s'il n'y a aucune enchère ouverte (`encheres_en_cours`) ; avec une enchère ouverte et une page de plus de 24 h, la ligne Export « Mes enchères » revient. |
| R4 | **Couverture des pages.** Vue `gold.bv_couverture_pages` : pour chaque type de page reçu en bronze depuis 30 jours (nombre, dernière arrivée), « lu par silver : oui ou non ». Table `core.page_reader` (jeu, motif, lecteur) semée à partir des vues silver existantes ; un type sans lecteur sort en alerte « page reçue, non lue ». |
| R5 | **Déclarations structurées.** Une ligne du registre `fait-<jour>.md` porte une clé `[clé=<écran ou match>]`. Le script lit les registres des 7 derniers jours par clé ; l'ancienne correspondance par mots reste en repli. Le skill `deja-fait` écrit la clé. |

Mesure : avant et après chaque migration, nombre de lignes de `gold.bv_exports_state`, `gold.bv_agenda` et `gold.bv_daily_alerts` (identiques).
Tests figés : Mes enchères non demandé ; saisie Garden City déclarée le 08/11 reconnue le 09/11 ; un type de page sans lecteur détecté.
Preuve (étape 3) : comptes avant et après, `gold.bv_couverture_pages`, script rejoué ; tableau critère / commande / sortie collée.

## Playbook (critères écrits le 2026-11-09, avant le fichier `docs/refonte-v3/playbook-basketvibe.md`)

Une routine = une ligne : déclencheur | condition | lancement (commande, vue ou fichier réel du dépôt, ou « à créer ») | ce qu'elle apprend | état | preuve. État : « existe » (un script ou une vue le fait déjà, dans le plan du jour), « à relier » (vue ou donnée présente, le plan du jour ne l'utilise pas), « à créer ». Preuve : fichier:ligne ou vue lue dans le tour d'écriture ; sinon « non vérifié ».

| # | Critère |
|---|---|
| P1 | **Aucune heure fixe.** Chaque routine a un déclencheur (donnée ou événement) et une limite calculée depuis le calendrier du jeu, jamais une heure écrite à la main. |
| P2 | **Sections** : Chaque passage ; Chaque match (ligue, coupe, amical) ; Chaque cycle (entraînement, académie, paie, semaine) ; Sur événement ; Phases de saison ; Marché ; Comprendre le moteur de match ; Veille ; Nettoyage. |
| P3 | **Règles de tête**, reprises de CLAUDE.md et des décisions de l'utilisateur : au plus tôt (sauf enchères et résultats) ; solde jamais négatif, sans réserve fixe ; vente pour baisser la masse salariale quand la force ne baisse pas ; étude de tous les prospects d'académie, même sous 100 % ; aucun paramètre fixé à la main (calculé sur l'historique, revu chaque semaine). |
| P4 | Chaque routine du plan du jour actuel (`pipelines/aujourdhui.py`) apparaît avec l'état « existe » ; aucune ligne « existe » sans preuve. |
| P5 | **Comprendre le moteur de match** : faits de `etude-evenements-basketvibe.md` et de la préanalyse (50 possessions par quart-temps ; effet cercle +6,81 [4,02 ; 9,01] ; fautes 6,5 % contre 16,5 % annoncés, dénominateur non défini ; tireur niveau 4 vers 65 % de tirs à 3 points ; fatigue observée au plus 24,6 ; règle des 24 s conforme en v5), avec le verdict exact du fichier, ni durci ni adouci. |
| P6 | **File d'expériences amicales**, une ligne par expérience : réglage testé, niveaux, pourquoi, n visé, export requis (4 pages du match et la page Équipe), statut. Besoins de l'étude repris tels quels : au moins 4 amicaux à agressivité uniforme 2 et 4 ; 3 avec deux tireurs de niveau 4 ; 7 avec Primary à chaque quart-temps ; 16 de plus pour les tirs à 3 points (environ 14 amicaux contrôlés au total). Un seul réglage change à la fois ; niveaux en alternance A, B, A, B. |
| P7 | Chaque routine « à créer » porte « ce qui prouvera qu'elle sert » (une mesure, pas une opinion). Le fichier finit par la liste ordonnée de l'étape 5, avec l'effort (petit, moyen, gros) de chaque ligne. |
| P8 | **Trous constatés** : chaque écran ou type de page reçu et non lu (`gold.bv_couverture_pages`), avec la question « sert-il à une routine ? » ; chaque doublon de règles (`core.export_rule`, `core.agenda_rule`, `core.alert_rule`, `aujourdhui.py`, skills), avec la source qui fait foi. |
| P9 | **Routines convenues ajoutées** au même fichier, sans réécrire l'existant, chacune en ligne de tableau (mêmes colonnes) avec état et preuve ; source cherchée dans le dépôt (skills `basketvibe-*`, `docs/attentes/jeux/basketvibe.yaml`, `docs/attentes/regles-decision-basketvibe.yaml`, `core.agenda_rule`, `core.alert_rule`, `learnings.md`, checklist), sinon « non vérifié ». Sur événement : deux défaites de suite en ligue (analyse ; à la 3e, changement chiffré obligatoire ; levier échoué deux fois interdit), titre acquis ou rien à jouer (minutes aux jeunes), moins de 5 joueurs éligibles (alerte forfait), solde projeté proche de zéro (cause, enchères limitées), compétence gagnée (rôle et potentiel recalculés), annonce du développeur ou nouvelle version du moteur (conseils concernés périmés), test de la file au nombre de matchs requis (verdict). Coupe : règles de la saison 2 et ce qui est déjà saisi, avec source. Phases de saison : début, milieu, fin, entre deux saisons. Chaque semaine : revue des matchs, conseils échus, marché, matchs d'autres équipes, veille, remise en question du modèle (une mesure par question et ce qui existe déjà en base). Nettoyage : inventaire en lecture seule chiffré. |
| P10 | Chaque ligne « existe » ajoutée a sa preuve fichier:ligne lue dans le tour ; chaque ligne « à créer » a « ce qui prouvera qu'elle sert » (une mesure). |
| P11 | La liste « Étape 5 » est mise à jour : routines ajoutées classées par effort ; la remise en question hebdomadaire en tête de l'étape 6. |

## Plan du jour, étape 5a (critères écrits le 2026-11-09, avant le code)

Source : `docs/refonte-v3/playbook-basketvibe.md`, liste « Étape 5 », actions 1, 2, 13, 15, 16. Fichiers modifiés : `pipelines/aujourdhui.py`, `aujourdhui_sources.py`, `test_aujourdhui.py`, skill `basketvibe-aujourdhui` ; aucune vue, migration ni règle.

| # | Critère |
|---|---|
| A1 | **Alertes de domaine « match ».** Dernier match → ligne « Analyse : … » ; match de ligue ou de coupe joué non exporté (`ligue_sans_resultat`, `coupe_sans_resultat`) → élément de la ligne « Exports à faire aujourd'hui ». Sans doublon : l'export de ligue n'est pas ajouté si l'écran « Match de ligue : box » est déjà demandé ou déclaré fait ; la ligne « Dernier match » n'est pas ajoutée si la ligne analyste (A2) porte le même match. **Écart constaté :** `coupe_sans_resultat` n'existe pas dans `gold.bv_daily_alerts` (`sql/gold/012_bv_daily_alerts.sql:38-44` : dernier match et ligue seulement) ; il est lu dans `gold.daily_alerts` (domaine `match`, colonne `rule_id`), qui porte les trois règles de `core.alert_rule`. Le domaine `match` de `gold.bv_daily_alerts` reste ignoré (pas de doublon). |
| A2 | **Défaite de ligue ou de coupe.** Ligne « Analyse : lance l'agent analyste ce soir » si le dernier match de ligue ou de coupe joué (`core.fixture`, `my_result`) est une défaite plus récente que le dernier brief analyste (`briefs/*-analys*.md`). Si `gold.match_objective` porte la règle `serie`, la ligne dit « N défaites de ligue d'affilée ». Amicaux exclus (arbitrage 15). Une seule ligne. |
| A3 | **Titre acquis ou rien à jouer.** Ligne Composition « minutes aux jeunes » seulement si un match à venir de `gold.match_objective` a la règle `titre`, `titre_former`, `rien` ou `rien_former`. **Écart constaté :** l'objectif `tester` sort aussi de la règle `amical` (7 lignes sur 10 le 09/11) ; filtrer sur l'objectif seul déclencherait la ligne chaque jour d'amical, d'où le filtre sur `rule_id`. Sinon aucune ligne. |
| A4 | **Solde projeté.** Ligne Finances si `balance_end_projected` de `gold.bv_finance_projection` est négatif ou inférieur à `weekly_salaries` de `gold.bv_finance_health` (une semaine de masse salariale ; aucun seuil écrit à la main). La ligne dit la cause : charges restantes contre recettes restantes, et la plus grosse charge hebdomadaire. Sinon aucune ligne. |
| A5 | Skill `basketvibe-aujourdhui` : la ligne fixe (d) périmée est supprimée ; rien d'autre ne change. |
| A6 | Au plus 8 lignes (surplus en « Autres points », priorité d'abord) ; script en 25 s au plus ; les 104 tests existants restent verts. |
| A7 | Un test figé par critère A1 à A4 : cas présent et cas absent. |
| A8 | Constat de la base avant le code (09/11, 12:40 Paris) : `gold.match_objective` basketvibe 10 lignes (3 `serie`, ligue 09/11, 11/11, 14/11, `defaites_d_affilee` 2 ; 7 `amical` ; 0 `titre`/`rien`) ; `gold.bv_daily_alerts` domaine `match` 1 ligne (dernier match 2026-11-08, amical, L 94-96) ; `gold.daily_alerts` basketvibe domaine `match` 1 ligne (`dernier_match`), 0 `ligue_sans_resultat`/`coupe_sans_resultat` ; `gold.bv_finance_projection` 1 ligne (`as_of` 08/11, solde projeté 1 512 431, `weekly_salaries` 294 625 : A4 absent aujourd'hui) ; `core.fixture` : dernières ligues jouées 07/11 Póvoa Riptide L, 04/11 Eindhoven Wizards L ; dernier brief analyste `2026-11-05-analyste.md`. Aucune source vide ni instable. |
| A9 | Constat du calendrier de coupe (pour l'étape 5c, rien modifié) : dernière page `bronze.raw_pages` id 34675, `/api/v1/teams/<id>/cup-fixtures`, reçue le 2026-11-04 10:35 UTC. 7 matchs : `Season 1 Edition` tour 1 (13/09) ; `National cups` tours 1 à 5 (28/10 au 01/11, `finished`, 18:00 UTC) ; `Season 2 Edition` **tour 1 seulement**, 12/11, `kickoff_time_local` 19:00, `kickoff_timezone` UTC, `scheduled`, contre Stare Kotlety (domicile). La saison 2 est présente, les 10 tours ne le sont pas. Écart : `core.fixture` dit les coupes du 29/10 et du 31/10 non jouées, la page les dit `finished`. |

## Boucle d'apprentissage (critères écrits le 2026-11-09 13:30 Paris, avant toute lecture de `learn.decision`)

Source : `docs/refonte-v3/playbook-basketvibe.md`, étape 5, action 19. Diagnostic en lecture seule : `docs/refonte-v3/diagnostic-boucle-apprentissage.md`. Aucune écriture en base, aucune vue ni règle modifiée.

**Liste fermée des causes (B1), écrite avant de regarder.** Chaque conseil échu non jugé reçoit **une seule** cause : la première qui s'applique, dans cet ordre.
| Code | Cause | Test |
|---|---|---|
| K1 | Pas de date d'échéance | `eval_after` vide |
| K2 | Jamais marqué appliqué | statut resté « proposé » (jamais « accepté » ni « fait ») |
| K3 | Pas de critère mesurable | aucune métrique ni seuil lisible par une requête (champ de critère vide, ou texte sans nombre ni métrique nommée) |
| K4 | Filtre de la vue qui l'exclut | échu, appliqué, mesurable, mais absent de `gold.decisions_a_evaluer` à cause d'une condition de la vue |
| K5 | Donnée d'évaluation absente | mesurable et dans la vue (ou exclu seulement faute de donnée), mais la donnée nécessaire (match, relevé) n'est pas en base |
| K6 | Autre | aucune des causes ci-dessus ; la raison est écrite |

| # | Critère |
|---|---|
| B1 | Pour chaque conseil échu non jugé, une cause K1 à K6 ; compte par cause ; 3 exemples collés par cause (identifiant, date, texte court). |
| B2 | Définition SQL de `gold.decisions_a_evaluer` et code de `pipelines/evaluer_decisions.py` : le filtre exact qui vide la vue (ligne de SQL ou de code), et ce que le script ferait d'une ligne. |
| B3 | Les conseils « faits » : combien ont un critère mesurable et une échéance passée ; leur évaluation calculée dans la réponse, rien n'est écrit. |
| B4 | Chemin du « fait » jusqu'à `learn.decision` aujourd'hui ; le registre `fait-<jour>.md` y est-il relié ? Preuve fichier:ligne. |
| B5 | Proposition d'une page, non appliquée : le plus petit changement qui ferait remonter les conseils échus et mesurables ; preuve = nombre de lignes de `learn.outcome` après un cycle. Les causes K1 à K6 classées en : se corrige par une vue ; demande un changement de skill ou d'agent ; sans critère mesurable, à reformuler. |

## Boucle d'apprentissage, étape 5b-2 (critères écrits le 2026-11-09 13:40 Paris, avant le code)

Source : `docs/refonte-v3/diagnostic-boucle-apprentissage.md` (`7ee5ce8`), sections B2 et B5. Écritures autorisées : la migration `sql/learn/004_evaluer_ecrire_https.sql` ; `learn.decision.status` par `python -I pipelines/decision.py statut <id> done`, seulement pour un conseil dont l'exécution est prouvée ; `learn.outcome` et `learn.lesson` par la fonction de la migration. Les 98 conseils `migre` proposés et les 32 faits ne sont pas touchés.

| # | Critère |
|---|---|
| C1 | `public.evaluer_ecrire(p jsonb)` (security definer, `search_path = ''`, exécution réservée à `service_role`, comme `decision_ecrire`) insère `learn.outcome` et met à jour la leçon liée dans **une** transaction. Refus sans rien écrire si la décision n'est pas `accepted`/`done`, si elle a déjà un résultat, ou si la leçon a changé depuis sa lecture (compteurs différents). Une décision sans leçon n'échoue pas. Migration additive et rejouable (`create or replace`), aucun drop. |
| C2 | `pipelines/evaluer_decisions.py` : lectures par le transport de `sql.py` (HTTPS en cloud), écriture par `evaluer_ecrire` en HTTPS ; plus aucune écriture par le port 5432. Fenêtre `my_result` : un match dont `scheduled_at` est vide compte si son jour est `>=` la date de la décision (date de Paris, `decided_at at time zone 'Europe/Paris'`) ; avec `scheduled_at`, il compte s'il est postérieur à `decided_at`. |
| C3 | `python -I pipelines/evaluer_decisions.py --essai` liste le verdict de chaque ligne de `gold.decisions_a_evaluer` sans écrire et sort avec le code 0. Tests figés sans base dans `pipelines/test_evaluer.py` : verdict confirmé, contredit, non concluant (valeur vide), décision sans leçon (charge sans leçon), match du jour (jour = date de la décision, `scheduled_at` vide → compté ; veille → exclu). |
| C4 | Les 9 conseils mesurables échus (1070 à 1076, 1088, 1099) : pour chacun, la ligne de `outputs/basketvibe/fait-*.md`, d'un brief ou du journal qui prouve son application, collée. Preuve trouvée → `done`. Sinon il reste proposé et va dans la liste « à confirmer par l'utilisateur » avec son texte court. Aucune supposition. |
| C5 | Évaluateur lancé hors `--essai` ; `select count(*) from learn.outcome` avant et après, et le verdict de chaque ligne. Nombre attendu = nombre de conseils prouvés appliqués en C4, pas 9. |
| C6 | Pour chaque verdict écrit : il mesure l'exécution (présence, achat) ou l'effet (résultat, solde). Pas d'interprétation. |

**Résultats (2026-11-09 13:42 Paris).** Migration `004` appliquée (`prosecdef` vrai, `search_path=""`, exécution : `service_role` seul). Écart trouvé au code : les 9 décisions ont `team_id` vide, `core.fixture` porte l'identifiant de l'équipe ; l'ancien filtre `team_id is not distinct from` ne trouvait aucun match. Décision sans équipe → pas de filtre d'équipe.

C4, preuves d'exécution :
| Id | Preuve collée | Statut |
|---|---|---|
| 1070 | `fait-2026-11-04.md` : « [soir, déclaré] Composition de la ligue J2 (Eindhoven Wizards) saisie » ; `briefs/2026-11-05-tactique.md:3` : « plan « League Tactic » sauvegardé le 04/11 contre Eindhoven (gold.bv_saisie_joueurs, sauvegarde_match = true) » | done |
| 1071 | `fait-2026-11-04.md` : « [soir, déclaré] Composition de l'amical du 05/11 (/HAVEX/) saisie » et « [19:43 Paris] Export de la tactique de l'amical du 05/11 : sauvegardée » | done |
| 1073, 1074 | `fait-2026-11-06.md` : « [13:47 UTC] Saisie de la ligue à Póvoa (J3, 07/11 20:00) — source : déclaré par l'utilisateur (« les deux compos sont faites ») » ; `resume-session-2026-11-06.md:8` : « D-1073 (tactique Póvoa), D-1074 (Lefebvre Q2) » | done |
| 1075 | `fait-2026-11-06.md` : « [13:47 UTC] Saisie de l'amical contre Knight Jays (07/11 07:45) » ; `resume-session-2026-11-06.md:7` : « Correction faite : Agress. 1 pour tous » | done |
| 1099 | `fait-2026-11-08.md` : « [10:34 UTC] Saisie de l'amical du 09/11 contre Garden City (composition, consignes, adversaires Perimeter) » ; `session-2026-11-08.md:26` : « D-1099 composition, amical du 09/11 (Garden City, nom corrigé ici) » | done |

À confirmer par l'utilisateur (restent proposés) : 1072 « Ligue J3 Póvoa 07/11 : Lefebvre Q1-Q2-Q4, Legrand Q3 SF » (plan du 05/11, aucune saisie déclarée le 05/11 ; la saisie du 06/11 suit les décisions 1073-1074) ; 1076 « Enchères 07-08/11 : Fujita C (max 150 000) et Stankevičius » (aucune enchère déclarée ; `fait-2026-11-06.md` : « Mes enchères — aucune enchère en cours ») ; 1088 « Enchère maximale 190 000 sur Salvador Aquino » (`session-2026-11-07.md:25` : « L'utilisateur ne misera pas »).

C5 : `learn.outcome` 0 → 6. 1070 contredit (`["L"]`), 1071 confirmé (55,2), 1073 contredit (50,6), 1074 contredit (81,9), 1075 et 1099 non concluants (valeur vide). `basketvibe:L-004` : `n_against` 0 → 1, reste `validated`, `source_decisions` `[1070]` ; `learn.error` 88 → 88. Relance `--essai` : « Aucune décision à évaluer. »

C6 : les 6 verdicts mesurent l'effet (résultat du match, `opp_fg2_pct`, `opp_efg_pct`, `off_rtg`) ; aucun ne mesure l'exécution.

## Boucle d'apprentissage, étape 5b-3 (critères écrits le 2026-11-09 13:58 Paris, avant le code)

Constat : les résultats « inconclusive » de 1075 et 1099 (`{"valeur": null}`) sont figés, car `gold.decisions_a_evaluer` exclut toute décision ayant déjà un résultat. Écritures autorisées : la migration `sql/learn/005_evaluer_reevaluable.sql` (`create or replace` de `public.evaluer_ecrire` et de `gold.decisions_a_evaluer`, aucun drop, aucun GRANT élargi) ; `learn.decision.status` par `python -I pipelines/decision.py statut` pour les trois conseils ci-dessous ; `learn.outcome` et `learn.lesson` par `evaluer_ecrire`.

Réponses de l'utilisateur (telles quelles) : « 1088 = rejeté (il n'a pas misé) ; 1072 = rejeté, remplacé par 1073 ; 1076 = [MISÉ ou PAS MISÉ]. » La réponse pour 1076 est restée à l'état de gabarit : son statut n'est pas touché tant que l'utilisateur n'a pas répondu.

| # | Critère |
|---|---|
| D1 | `evaluer_decisions.py` n'écrit jamais un verdict « inconclusive » : une valeur vide laisse la décision « en attente », affichée avec la donnée qui manque. Test figé dans `pipelines/test_evaluer.py`. |
| D2 | Les deux résultats « inconclusive » (1075, 1099) redeviennent évaluables : `gold.decisions_a_evaluer` inclut une décision dont le seul résultat est « inconclusive » ; `evaluer_ecrire` remplace un résultat « inconclusive » par le nouveau verdict, jamais un résultat « confirmed » ou « contradicted ». Aucune ligne supprimée à la main. |
| D3 | 1088 et 1072 passent `rejected` ; 1076 `done` ou `rejected` selon la réponse de l'utilisateur ; aucun autre statut n'est touché. |
| D4 | Une ligne de `fait-<jour>.md` peut porter `[décision=<id>]` (en plus de `[clé=…]`). `pipelines/relier_faits.py` lit les registres des 7 derniers jours et appelle `decision.py statut <id> done` pour chaque identifiant dont la décision est encore « proposed ». Jamais de correspondance floue, jamais d'identifiant inventé. `--essai` liste sans écrire. Tests figés (`pipelines/test_relier_faits.py`) : identifiant valide, déjà done, inconnu, ligne « reste à ». |
| D5 | Skill `deja-fait` : une phrase qui dit d'ajouter `[décision=<id>]` quand la saisie déclarée vient d'une décision ouverte (identifiant lu avec `decision.py` ou dans le brief). Rien d'autre ne change dans les skills. |
| D6 | Après le cycle : la vue contient 1075 et 1099 si leur valeur est toujours vide, chacune évaluée ou en attente selon silver ; `learn.outcome` n'a aucun doublon par décision ; chaque verdict collé. |

**Résultats (2026-11-09 15:05 Paris).** Migration `005` appliquée (`ea4bee1`). D1 (`904fe09`) : `test_evaluer.py` 34/34. D3 : 1088 `rejected` (« 1088 = rejeté (il n'a pas misé) »), 1072 `rejected` (« 1072 = rejeté, remplacé par 1073 ») ; 1076 reste `proposed` (réponse non donnée). D4-D5 (`4962921`) : `test_relier_faits.py` 8/8 ; `relier_faits.py basketvibe --essai` : « Aucune ligne [décision=<id>] dans les registres des 7 derniers jours. »
D6 : `gold.decisions_a_evaluer` = 1075, 1099. Cycle réel : les deux « en attente » (`gold.bv_match_report` n'a pas les amicaux des 07/11 et 09/11 ; seule ligne : ligue du 07/11, `opp_fg2_pct` 53,0). `learn.outcome` : 6 lignes, aucun doublon ; 1075 et 1099 gardent leur ancien « inconclusive » jusqu'à l'arrivée de la donnée, puis seront remplacés. Refus contrôlés : 1070 `confirmed` → « déjà évaluée (contradicted) » ; 1075 `inconclusive` → « verdict inconclusive refusé ».

## Garde-fous mécaniques (critères écrits le 2026-11-09 15:10 Paris, avant le code)

Constat : un Claude de cloud enfreint de façon répétée trois règles de forme (heredoc pour écrire un fichier, push sur une branche de session au lieu de main, commit et push enchaînés). Les règles écrites ne tiennent pas ; on les rend mécaniques.

| # | Critère |
|---|---|
| T1 | Hook PreToolUse Bash `pipelines/garde_heredoc.py` : refuse une commande qui écrit un fichier par heredoc (une redirection, ou python/cat/tee, avec `<<` suivi d'un délimiteur) ; accepte `git commit -m "$(cat <<'EOF' ...)"`. Message du refus : « écris le fichier avec Write ». Tests figés (`pipelines/test_garde_heredoc.py`) : cas refusés et acceptés. |
| T2 | `pipelines/garde_push.py` : le texte du refus de `git push -q/--quiet` devient « retire -q/--quiet, la sortie doit être lue ». Même hook, aucun autre changement. |
| T3 | `pipelines/fusion_main.py` : sur la branche courante, `git fetch`, vérifie que main peut avancer en fast-forward, sinon refuse sans rien changer ; puis pousse main et imprime avant/après les hashs (HEAD, origin/main). `--essai` imprime sans pousser. Jamais de `--force`. Tests figés sur un dépôt temporaire (`pipelines/test_fusion_main.py`) : fast-forward, divergent, déjà à jour. |
| T4 | `pipelines/fin_etape.py` (lecture seule, code retour 1 si HEAD n'est pas dans origin/main) : branche, HEAD, origin/main, commits d'avance sur main, `git status --short`, dernière ligne de chaque `pipelines/test_*.py`. Tests figés (`pipelines/test_fin_etape.py`). |
| T5 | Aucun autre hook, aucune autre règle en prose ; `CLAUDE.md` reçoit une seule ligne : « fin d'étape = python -I pipelines/fusion_main.py puis python -I pipelines/fin_etape.py, sortie collée ». |

## Boucle d'apprentissage, étape 5b-4 (critères écrits le 2026-11-09 15:20 Paris, avant toute requête)

Réponses de l'utilisateur : 1076 = pas misé ; E1 = oui, agressivité défensive uniforme 2 puis 4 en amical, le résultat de ces amicaux lui est indifférent ; l'amical Knight Jays du 07/11 a été exporté, il peut le réexporter si besoin. Écriture autorisée sur la base : `python -I pipelines/decision.py statut 1076 rejected --note "1076 = rejeté (l'utilisateur n'a pas misé)"`. Aucun script, vue, règle ni skill modifié.

| # | Critère |
|---|---|
| F1 | La décision 1076 passe en `rejected` avec la note ci-dessus ; aucun autre statut n'est touché. |
| F2 | `docs/refonte-v3/playbook-basketvibe.md`, file d'expériences amicales, ligne E1 : statut « validé par l'utilisateur le 2026-11-09 : agressivité défensive uniforme 2 puis 4 en amical ; le résultat de ces amicaux lui est indifférent ». Cette ligne seule change. |
| F3 | Diagnostic de l'amical Knight Jays du 07/11 (conseil 1075 ; `opp_fg2_pct` de `gold.bv_match_report`, `competition = 'friendly'`, valeur déjà bonne pour 1071). Cause choisie dans la liste fermée, écrite avant de regarder : (a) aucune page du match en bronze ; (b) pages en bronze mais aucune vue silver ne les lit ; (c) lues mais exclues par `gold.bv_match_report` ; (d) match absent de `core.fixture` ou non marqué joué ; (e) autre. Pour chaque hypothèse écartée, une requête collée (`bronze.raw_pages` par date et type de page autour du 07/11, `silver.bv_matches`, `core.fixture`, définition SQL de la vue). |
| F4 | Pour chaque amical joué des 10 derniers jours (`core.fixture`) : présent ou non dans `gold.bv_match_report`, avec la date. Tableau collé. |
| F5 | Cause (a) : liste exacte des pages à réexporter (box score, play-by-play, réglages utilisés, aperçu). Causes (b), (c), (e) : la plus petite correction, en une phrase, sans l'appliquer. |

**F1 (2026-11-09 15:24 Paris).** `decision.py statut 1076 rejected` → « ✅ D-1076 : rejected » ; `decision.py liste basketvibe` : 9 done, 18 proposed, 3 rejected (1072, 1076, 1088). Pronostic de cause F3, écrit avant les requêtes : **(b)** pages arrivées en bronze, non lues par silver (l'utilisateur dit avoir exporté ; la ligue du 07/11 est lue). Faux si `bronze.raw_pages` n'a aucune page du match.

**F3-F5, résultats (2026-11-09 15:40 Paris).** Pronostic (b) **faux**. Cause retenue : **(a) aucune page de ce match en bronze**, avec (d) en conséquence (aucune fixture « Knight Jays »).

Requêtes (via `python -I pipelines/sql.py`) :
- (b) écarté — silver ne manque rien de ce qui est arrivé : `silver.bv_matches` depuis le 01/11, aucune ligne dont `home_team`/`away_team` contient « Knight » ou « Brasa » (0 ligne) ; chaque amical joué de `core.fixture` y est (colonne `sil` = 1 partout).
- (c) écarté : chaque amical joué de `core.fixture` a 1 ligne dans `gold.bv_match_report` (F4). La vue joint `gold.bv_match_team_totals` à `silver.bv_matches` et ne filtre pas la compétition (`sql/gold/003_bv_match_report.sql`).
- (d) : `select … from core.fixture where opponent ilike '%knight%' or opponent ilike '%brasa%'` → 0 ligne. Aucun amical daté 07/11 dans `core.fixture` (le 07/11 : seulement la ligue Póvoa). La fixture `17bcb69d` exportée le 07/11 à 12:09 (6 pages : preview, 4 period-box, match-tactics) est **BC Calije, amical du 31/10**, déjà en base : c'est un réexport, pas Knight Jays.
- (a) : amicaux avec pages en bronze depuis le 04/11 (`bronze.raw_pages`, `source_url like '%friendlies/%'`) : baker street (11/04), NY Lighters (11/03), Istanbul Cobras (10/30), /HAVEX/ (11/05), The Bombers (11/06), BC Calije (10/31, réexport 07/11), New York City Cyclones (11/08), Garden City (11/09, 2 pages, `played` = faux). Aucun Knight Jays.
- Limite : le garde-fou de `sql.py` refuse toute recherche dans le texte des payloads ; je n'ai pas pu chercher « Knight Jays » dans les pages elles-mêmes (un autre libellé d'adversaire reste possible).

F4 (amicaux joués de `core.fixture`, 10 derniers jours, tous présents dans `gold.bv_match_report`) :

| jour | adversaire | joué | résultat | dans le rapport |
|---|---|---|---|---|
| 2026-10-30 | Istanbul Cobras | oui | W | oui |
| 2026-10-31 | BC Calije | oui | L | oui |
| 2026-11-01 | Granada Sentinel | oui | W | oui |
| 2026-11-02 | Galit sa gobyerno | oui | L | oui |
| 2026-11-03 | NY Lighters | oui | L | oui |
| 2026-11-04 | baker street | oui | W | oui |
| 2026-11-05 | /HAVEX/ | oui | L | oui |
| 2026-11-06 | The Bombers | oui | L | oui |
| 2026-11-08 | New York City Cyclones | oui | L | oui |
| 2026-11-09 | Garden City | non (pas encore joué en base) | — | non |

Aucun amical joué n'est absent du rapport. Le rapport est complet : il manque seulement des matchs qui n'existent pas en base.

F5 (cause a) : pages à réexporter pour l'amical Knight Jays du 07/11 — celles qu'un export d'amical produit (vues pour BC Calije) : l'**aperçu** (`friendlies/<id>/preview`), les **4 box scores par quart-temps** (`period-box`, Q1 à Q4) et les **réglages utilisés** (`match-tactics`). Je ne connais pas la page « play-by-play » : je ne l'ai vue sous aucun export d'amical, donc je ne la cite pas. Condition : ce match doit exister dans la liste des amicaux du jeu. Si le jeu ne montre aucun amical à cette date contre Knight Jays, 1075 décrit un match qui n'a pas eu lieu et la décision reste « en attente » (pas de correction de vue). Même constat pour 1099 : « Brasa Bombe » (09/11) est absent de `core.fixture`, qui ne contient que Garden City (09/11, non joué) ; le nom de l'adversaire dans 1099 est à vérifier. Ce qui prouvera que j'ai tort : un export d'amical 07/11 qui arrive en bronze et que `gold.bv_match_report` lit.

## Calendrier, étape 5c (critères écrits le 2026-11-09 15:34 Paris, avant toute requête et tout code)

Constat de départ : les pages calendrier (friendlies, league-fixtures, fixtures/round/<n>, cup-fixtures) sont en `bronze.raw_pages`, mais `core.fixture` n'a l'heure que pour 9 amicaux sur 37, 0 des 44 matchs de ligue et 0 des 4 de coupe ; aucune vue silver ne lit ces pages (`gold.bv_couverture_pages`). Faits de l'utilisateur à retrouver : amical Garden City 09/11 joué ce matin ; ligue J4 contre Naked Spartans ce soir 09/11, verrou 19:45 Paris ; amical Knight Jays 07/11 07:45 ; premier tour de coupe jeudi 12/11 (page : 19:00 UTC, soit 20:00 Paris). Écritures autorisées : une migration additive (create or replace, aucun drop) via le connecteur Supabase, et la mise à jour de `core.fixture` par le chemin qui l'alimente déjà.

| # | Critère |
|---|---|
| J1 | Constat sur les pages calendrier : pour la dernière page de chaque type (date de réception), champs utiles lus avec `sql.py --page-id <N> --payload-path <chemin>` (adversaire, date, heure, fuseau, statut, résultat, identifiant du match, domicile/extérieur, compétition), 5 lignes collées par type. Réponse pour le 09/11 (amical du matin, ligue du soir), le 07/11 (Knight Jays présent ? identifiant ?) et la coupe. |
| J2 | Alimentation de `core.fixture` (fichier:ligne) ; pourquoi `scheduled_at` est vide en ligue et coupe ; pourquoi Garden City 09/11 n'est pas joué ; pourquoi Knight Jays 07/11 est absent. Une cause par constat, avec la requête qui la prouve. |
| J3 | Plus petit changement qui fait porter à `core.fixture`, pour toute journée dont une page est en bronze : jour, coup d'envoi en UTC avec le fuseau lu dans la page (jamais supposé), statut, résultat, adversaire, compétition, identifiant du match. Le tableau « champ de la page → colonne » est une configuration lisible (fichier ou table), pas du code en dur ; sinon, dire pourquoi. |
| J4 | Preuve : comptes de `core.fixture` avant/après (heure renseignée par compétition) ; les quatre faits retrouvés (ou absence prouvée dans la page) ; aucune ligne supprimée ; les 123 tests de `test_aujourdhui.py` verts. |
| J5 | `aujourdhui.py` : si `scheduled_at` est renseigné, limite et heure affichées viennent de lui (heure de Paris) ; sinon l'ancienne heure. Test figé sur la ligue J4 de ce soir (verrou 19:45) et le premier tour de coupe (20:00 Paris). Règles de `core.agenda_rule` qui portent une heure écrite, avant et après. |
| J6 | Rejeu de `python -I pipelines/aujourdhui.py basketvibe` avant et après (sortie collée) ; au plus 8 lignes, 25 s au plus. |

**J1, constat (2026-11-09 16:00 Paris).** Lecture par `silver.bv_api` (même payload que `bronze.raw_pages`, `--page-id` renvoie le JSON entier en une cellule, illisible ; `jsonb_array_elements` sur la dernière capture de chaque type). Dernières pages : league-fixtures 39315 (09/11 14:26 UTC), cup-fixtures 34675 (04/11 10:35 UTC), friendlies 38576 (09/11 09:57 UTC), fixtures/round/4 38938 (09/11 09:59 UTC), preview par match (fixtures/friendlies/cup-fixtures/<id>/preview).

Champs par type : league-fixtures et fixtures/round/<n> = `id`, `match_id`, `match_day`, `status`, `round_number`, `home/away_team_id`, `home/away_score` ; **aucune heure ni fuseau** (noms dans `team_labels`/`team_names`). cup-fixtures = mêmes champs + `cup_name`, `edition_label`, `home/away_team_name`, **`kickoff_time_local` + `kickoff_timezone`**. friendlies = mêmes + noms + **`kickoff_at` (ISO en UTC, suffixe Z)**. preview = **`kickoff_time` + `league_timezone`** (fuseau de l'hôte : The Bombers 06/11 « 08:00 Asia/Tokyo », cohérent avec `kickoff_at` 05/11 23:00Z).

| type | jour | tour | statut | id | domicile | extérieur | score | heure |
|---|---|---|---|---|---|---|---|---|
| league-fixtures | 04/11 | 2 | finished | 40c7cd3b | (id) | (id) | 107-114 | — |
| league-fixtures | 07/11 | 3 | finished | aca88448 | (id) | (id) | 106-82 | — |
| league-fixtures | 09/11 | 4 | scheduled | ddb4d263 | (id) | (id) | — | — |
| league-fixtures | 11/11 | 5 | scheduled | 46f9ae01 | (id) | (id) | — | — |
| league-fixtures | 14/11 | 6 | scheduled | 6d0ced02 | (id) | (id) | — | — |
| cup-fixtures | 29/10 | 2 | finished | dc345bfb | Chomelix Cow | Paris Saint-Germain | 107-97 | 18:00 Europe/Paris |
| cup-fixtures | 30/10 | 3 | finished | 720d9d11 | Yannick Skulls | Chomelix Cow | 97-106 | 18:00 Europe/Paris |
| cup-fixtures | 31/10 | 4 | finished | a536c811 | Chomelix Cow | Ploppers | 82-72 | 18:00 Europe/Paris |
| cup-fixtures | 01/11 | 5 | finished | 16c8812a | Reims Monarchs | Chomelix Cow | 107-102 | 18:00 Europe/Paris |
| cup-fixtures | 12/11 | 1 | scheduled | 3667d243 | Chomelix Cow | Stare Kotlety | — | 19:00 UTC (BasketVibe Cup, Season 2) |
| friendlies | 06/11 | — | finished | 9b8afa39 | The Bombers | Chomelix Cow | 120-67 | 2026-11-05T23:00Z |
| friendlies | 07/11 | — | finished | 92fe979b | Chomelix Cow | Knight Jays | 86-104 | 2026-11-07T07:00Z |
| friendlies | 08/11 | — | finished | e57c6b05 | Chomelix Cow | New York City Cyclones | 94-96 | 2026-11-08T07:00Z |
| friendlies | 09/11 | — | finished | 44f3e0f3 | Chomelix Cow | Garden City | 104-120 | 2026-11-09T07:00Z |
| friendlies | 10/11 | — | scheduled | 1632fa97 | Chomelix Cow | Opper Cards | — | 2026-11-10T07:00Z |
| round/4 (autre ligue) | 09/11 | 4 | scheduled | e100123d | Bibim Bożejewice | Sakar SuperSonics | — | — |
| round/4 (autre ligue) | 09/11 | 4 | scheduled | a6cd5b28 | KK Glen Johnson | Rifiuti Organici | — | — |
| round/4 (autre ligue) | 09/11 | 4 | scheduled | 9a1fe025 | Artica Slayers | Suricata Squad | — | — |
| round/4 (autre ligue) | 09/11 | 4 | scheduled | fbe5562d | KK Bedex | Bratrstwo Wlkodlaka | — | — |
| round/4 (autre ligue) | 09/11 | 4 | scheduled | f2990c58 | Milano Jazz | DenverNug | — | — |
| preview ligue J4 | 09/11 | 4 | scheduled_lineups | ddb4d263 | Chomelix Cow | Naked Spartans | — | 20:00 Europe/Paris |
| preview amical | 09/11 | — | finished | 44f3e0f3 | Chomelix Cow | Garden City | — | 08:00 Europe/Paris |

Réponses : **09/11** — amical Garden City (44f3e0f3) `finished` 104-120 dans la liste des amicaux de 09:57 UTC ; ligue J4 Naked Spartans (ddb4d263) `scheduled`, heure seulement dans la preview : 20:00 Europe/Paris, verrou 19:45 = 15 min avant (skill `basketvibe-saison`, 01-rythme, [M§1.3]). **07/11** — Knight Jays présent dans la liste des amicaux, fixture `92fe979b-031f-446e-aaed-43991bfdb176`, 07:00Z = 08:00 Paris, verrou 07:45 ; F3 se trompait (le garde-fou de `sql.py` sur le texte des payloads m'avait empêché de lire la liste). **Coupe** — 12/11, tour 1, BasketVibe Cup Season 2, contre Stare Kotlety (3667d243), 19:00 `UTC` lu dans la page = 20:00 Paris ; verrou au coup d'envoi (skill `basketvibe-saison`, 05-coupes, V-20261108-1).

**J2, constat.** `core.fixture` = vue `sql/core/002_core_views.sql:17`, union de `adapt.basketvibe_fixture` (`sql/adapters/basketvibe.sql:47`, définition en base identique au fichier : elle lit `bv_api`). Trois branches : matchs exportés (`silver.bv_matches`, l. 5-11), calendrier de saison non exporté (`silver.bv_fixtures`, l. 12-17, ligue seulement), amicaux `status = 'scheduled'` de la liste (l. 48-63).
- `scheduled_at` vide en ligue et coupe : écrit `null::timestamptz` en dur, l. 73 (« fuseau de kickoff_time non sourcé ») et l. 87. Le fuseau existe pourtant dans la preview (`league_timezone`) et la liste de coupe (`kickoff_timezone`). Preuve : requête preview ci-dessus (20:00 Europe/Paris) ; `core.fixture` coupe et ligue : `count(scheduled_at)` = 0.
- Garden City non joué : `played` = statut de la dernière capture de `silver.bv_matches` ; la seule page du match jusqu'à 14:33 UTC était la preview d'avant-match (08/11 10:12, `scheduled_lineups`). La liste des amicaux (09:57, `finished`) n'est pas lue pour un match déjà exporté (branche 3 : `not exists … played`). Preuve : `bronze.raw_pages` du fixture 44f3e0f3, première capture 08/11 10:12, `silver.bv_matches` `finished` seulement à 14:33. Corrigé de fait par le réexport de 14:33 ; même cause encore active en coupe : PSG 29/10 et Ploppers 31/10 sont `played = false` dans `core.fixture` (`scheduled_lineups`) alors que la liste de coupe dit `finished` 107-97 et 82-72.
- Knight Jays absent : aucune page du match en bronze avant 09/11 14:26 UTC (première capture de 92fe979b à 14:26:16), et la branche 3 ne garde que `status = 'scheduled'` : un amical fini, non exporté, présent dans la liste (finished 86-104), est jeté. Depuis le réexport de 14:26, il est dans `core.fixture` (joué, L).
- Coupe du 12/11 absente : aucune branche ne lit la liste de coupe pour un match non exporté (branche 2 = ligue seulement). Preuve : `core.fixture` coupe = 4 lignes, toutes ≤ 31/10.

**J3 (2026-11-09 16:20 Paris).** Migration `sql/core/023_calendrier_pages.sql` (connecteur, `core_023_calendrier_pages`) : deux tables de configuration, `core.calendrier_page` (6 types de page : listes amicaux, coupe, ligue ; aperçus ligue, amical, coupe — motif d'URL, chemin, compétition, statuts « joué », minutes de verrou et leur source) et `core.calendrier_champ` (le tableau « champ de la page → colonne », 69 lignes), et une vue générique `silver.calendrier` (dernière valeur non nulle par champ ; coup d'envoi = instant ISO de la page, sinon jour + heure locale dans le fuseau lu ; sans fuseau : null). Puis `adapt.basketvibe_fixture` (`sql/adapters/basketvibe.sql`, migration `adapt_basketvibe_fixture_calendrier`) : `scheduled_at`, `played`, score et résultat complétés depuis `silver.calendrier`, `extras.verrou_at` / `fuseau_lu` / `source_heure`, et une 4ᵉ branche pour les matchs connus seulement d'une page calendrier. Un autre jeu : des lignes dans les deux tables, et son adaptateur lit `silver.calendrier where game = '<jeu>'` (le lien « mon équipe » reste dans l'adaptateur). Non fait (hors écritures autorisées) : lignes `core.page_reader` pour que `gold.bv_couverture_pages` voie ces pages lues.

**J4.** Avant / après (`core.fixture`, BasketVibe) :

| compétition | lignes avant | heure avant | joués avant | lignes après | heure après | joués après |
|---|---|---|---|---|---|---|
| amical | 38 | 9 | 29 | 40 | 40 | 31 |
| coupe | 4 | 0 | 2 | 7 | 7 | 6 |
| ligue | 44 | 0 | 25 | 44 | 26 | 25 |

Ligue sans heure : 18 journées futures sans aperçu en bronze (la liste de ligue n'a pas d'heure ; jamais supposée). Lignes : 86 → 91, **0 disparue** (comparaison des `fixture_id`), 5 nouvelles (coupe Blood Wolves 13/09, Reims Monarchs 01/11, Stare Kotlety 12/11 ; amicaux Woodlands Wizards 14/10, Mallorca Waves 28/10). Faits : Garden City 09/11 joué, L, 08:00 Paris ; ligue J4 Naked Spartans 09/11 20:00 Paris, verrou 19:45 ; Knight Jays 07/11 joué, L, 08:00, verrou 07:45 ; coupe Stare Kotlety 12/11 20:00 Paris (fuseau lu : UTC), verrou 20:00. Coupe PSG 29/10 et Ploppers 31/10 passent joués (W). `test_aujourdhui.py` : 123/123.

**J5.** `pipelines/aujourdhui.py` : requête `calendrier` (core.fixture à venir, `scheduled_at` et `extras.verrou_at` en heure de Paris) et `verrou_calendrier()` : pour un match du brief tactique, la limite et l'heure du verrou viennent de `core.fixture` si elle a l'heure, sinon du brief ; titre « Coupe contre » pour une coupe. Tests figés ajoutés (127/127) : ligue J4 → 19:45 depuis `scheduled_at` (brief d'essai à 19:30), 19:30 sans calendrier ; coupe 12/11 → 20:00 Paris, « verrou inconnue » sans calendrier. Règles de `core.agenda_rule` (BasketVibe, déclencheur match) avec heure écrite, avant et après (inchangées, aucune écriture autorisée sur cette table) : `ligue_export` 20:50, `ligue_preset` 19:45, `ligue_preview` 19:30. Prochaine étape possible : les passer en `decalage` relatif à `scheduled_at` (+00:50, −00:15, −00:30), comme les règles d'amical — demande une écriture sur `core.agenda_rule`.

**J6.** Rejeu avant (19,9 s) et après (22,0 s) : 8 lignes chacun ; mêmes heures (19:30, 19:45, 20:50) ; la ligne 19:45 de la ligue vient maintenant de `scheduled_at` ; « Dernier match exporté » passe du 08/11 (New York City Cyclones) au 09/11 (Garden City, L 104-120), effet du réexport de 15:33 Paris.

## Plan du jour, étape 5d (critères écrits le 2026-11-09 16:10 Paris, avant le code)

Étape 0 (`python -I pipelines/evaluer_decisions.py`, 15:53) : D-1075 `contradicted` (63,3), D-1099 `contradicted` (64,8) ; `learn.outcome` = 6 lignes (5 contredites, 1 confirmée).

| # | Critère |
|---|---|
| H1 | `docs/attentes/experiences-amicales-basketvibe.yaml` : une entrée par expérience (id, réglage testé, niveaux A et B, ordre, nombre d'amicaux visé, export requis). E1 agressivité défensive uniforme sur les cinq, A = 2, B = 4, ordre A,B,A,B, au moins 4 amicaux ; E2 focus de tir de deux tireurs, niveau 4, 3 amicaux ; E3 focus offensif Primary à chaque quart-temps, 7 amicaux ; E4 aucun réglage, 16 amicaux de plus (réglage habituel). Elles passent dans cet ordre ; la suivante démarre quand la précédente a son nombre d'amicaux. |
| H2 | Une expérience avance quand une ligne du registre `fait-<jour>.md` porte `[expérience=<id>:<niveau>]`, lue par `aujourdhui_sources.py` avec le même parseur que les clés R5 (ligne « reste à » ignorée). Aucune table. **Écart à la demande, tranché** : fenêtre = tout le registre, pas 7 jours (sur 7 jours E1 redémarrerait au 8e jour et E4, 16 amicaux à un par jour, ne finirait jamais). Une ligne qui porte aussi la clé du prochain amical (`[clé=Opper Cards 10/11]`) n'avance pas l'expérience pour ce match : elle le dit saisi à ce niveau. |
| H3 | Pour le prochain amical à saisir (aujourd'hui ou demain, d'après `core.fixture`, verrou non passé), la ligne du plan porte : le réglage du test (« test E1 niveau A : agressivité 2 sur les cinq »), qui remplace l'agressivité du brief pour ce match ; l'heure limite lue dans `core.fixture` (verrou) ; les exports à faire après le match (aperçu, box scores par quart-temps, réglages utilisés, page Équipe du jour). Sans brief amical, la ligne est créée depuis `core.fixture` ; la ligne d'agenda du même amical n'est pas répétée. |
| H4 | Aucune expérience en cours (toutes terminées ou fichier absent) : aucune ligne ajoutée, aucun plantage. |
| H5 | Skill `deja-fait` : une phrase « quand la saisie d'un amical vient du réglage de test du plan, ajoute `[expérience=<id>:<niveau>]` à la ligne ». Rien d'autre ne change. |
| H6 | `core.agenda_rule` : nouvelle colonne `decalage_min` (entier, minutes relatives au coup d'envoi de `core.fixture`), migration additive, aucun drop ; les règles de ligue à heure écrite (19:30, 19:45, 20:50) la reçoivent ; l'ancienne `heure` reste en repli. `aujourdhui.py` recale la ligne d'agenda (heure et heures citées dans le texte) quand le coup d'envoi du match de ligue du jour est connu. Liste avant/après collée. |
| H7 | Tests figés, cas présent et cas absent pour chacun : alternance A,B,A,B de E1 ; passage à E2 quand E1 est complète ; fichier absent ; ligne « reste à » ignorée ; amical sans brief ; règle d'agenda avec décalage et sans coup d'envoi. Sortie ≤ 8 lignes, script ≤ 25 s, les 127 tests existants restent verts. |
| H8 | Rejeu `python -I pipelines/aujourdhui.py basketvibe` avant et après (sortie collée). L'amical du 10/11 contre Opper Cards (coup d'envoi 08:00 Paris, verrou 07:45) affiche E1 niveau A avec l'heure limite du calendrier. |

## Plan du jour, étape 5e (critères écrits le 2026-11-09 16:05 Paris, avant le code)

Contexte : playbook, étape 5, actions 3 et 6 ; main = 9dc4365, plan en 22,5 s (limite 25 s), 8 lignes au plus. Seuls `aujourdhui.py`, `aujourdhui_sources.py`, `test_aujourdhui.py` et ce journal bougent ; lecture seule sur la base, aucune migration ni vue modifiée.

| # | Critère |
|---|---|
| K1 | Durée d'abord : temps de chaque requête du script (tableau collé). Total > 20 s → regrouper ou paralléliser les requêtes indépendantes, sans changer la sortie, pour tomber à 15 s au plus ; sortie avant/après identique, preuve collée. |
| K2 | Masse salariale (règle de l'utilisateur : on vend pour baisser la masse salariale quand l'équipe n'y perd pas en force) : lire la définition de `gold.bv_sell_candidates` et dire si elle sait répondre « la force ne baisse pas ». Si oui : une ligne « Vendre X : salaire … par semaine, remplaçant au poste Y de même force » quand un candidat existe, aucun seuil écrit à la main (comparaison avec le remplaçant du même poste). Si non : dire exactement ce qui manque, aucune règle inventée. |
| K3 | Académie (règle : étudier tous les prospects, même sous 100 % de jauge) : à l'arrivée d'un rapport (`gold.bv_academy_prospects`), une ligne par prospect « tester / signer / ignorer » d'après `gold.bv_academy_potential_odds` ; valeur d'un High et coût du test lus dans la base, pas écrits. Une des deux données manque → la dire ; la ligne dit « donnée manquante : … ». |
| K4 | Boucle d'apprentissage : une ligne de compte « n décisions à mesurer, n faits à relier » lue dans `gold.decisions_a_evaluer` et dans les registres (lecture seule, aucune écriture), seulement si n > 0 ; sinon aucune ligne. |
| K5 | Tests figés, un cas présent et un cas absent pour K2, K3 et K4 ; sortie ≤ 8 lignes ; les 143 tests existants restent verts. |
| K6 | Rejeu `python -I pipelines/aujourdhui.py basketvibe` avant et après (sortie collée telle quelle) ; durée ≤ 25 s, visée 15 s. |

**K2, réponse : non, `gold.bv_sell_candidates` ne sait pas dire « la force ne baisse pas ».** Définition lue en base (`pg_get_viewdef`, 3 013 caractères, mêmes tables que `sql/gold/006_bv_transfers.sql:102`). Elle rend par joueur `ps` (note globale), `salary`, `best_slot` (poste où son `fit` est le plus haut dans `gold.bv_slot_fit`) et `rank_in_slot` (rang à ce poste, sur tout l'effectif, trié par `fit_with_form`). Ce qui manque :
1. **La force au poste** : ni `fit` ni `fit_with_form` ne sont exposés ; `ps` est la note globale, pas la force au poste `best_slot`.
2. **Le remplaçant** : aucune colonne ne nomme le joueur de rang suivant au même poste ni sa force ; les rangs ne se suivent pas dans la vue (au poste C : rangs 3, 4, 5, 6, car les rangs 1 et 2 ont un autre `best_slot`), donc on ne peut pas le retrouver en relisant la vue.
3. **Le sens de « même force »** : le remplaçant de rang r+1 a par construction un `fit_with_form` inférieur ou égal ; « même force » n'est vrai qu'à égalité stricte, sauf à écrire une tolérance, c'est-à-dire un seuil à la main (interdit par K2). Règle à fixer par l'utilisateur avant tout code.
Incohérence relevée au passage : `best_slot` est choisi sur `fit`, `rank_in_slot` sur `fit_with_form`.
Conséquence : aucune ligne « Vendre X » ajoutée au plan, aucun test K2 (rien à tester). La ligne « Garder : effectif, vendre pour profit : règle non écrite » reste telle quelle.

**Résultats 5e (2026-11-09 16:10 Paris).**
- **K1** (`d57c796`) : durée par requête, en série (script de mesure hors dépôt, `sql.executer` sur chaque entrée de `REQUETES`), avant K3-K4 : agenda 0,89 · exports_state 1,19 · daily_alerts 2,31 · finance_health 0,50 · **position_summary 4,49** · market_bargains 0,60 · market_candidates 1,39 · personnel_status 0,57 · joueurs_declin 0,62 · decisions_achat 0,46 · encheres_ouvertes 0,86 · transferts_recents 0,55 · apercus 0,45 · derniere_vente 0,55 · alertes_match 0,44 · objectifs 0,47 · dernier_officiel 1,15 · calendrier 1,05 · regles_agenda 0,45 · finance_projection 0,73 ; **total 19,73 s** (+ ~3 s de démarrage : 23,0 s mesurés par le script). Total > 20 s → `lire_tout` lance les requêtes en parallèle (8 fils, résultat rangé dans l'ordre de `REQUETES`) : **23,0 s → 7,5 s**, `diff` avant/après : « sortie identique ». Le plancher est `gold.bv_position_summary` (≈ 4,3-4,5 s).
- **K2** (`34a4193`) : non, voir ci-dessus ; rien de codé.
- **K3** (`34e1776`) : valeur d'un High et coût du test **absents de la base** (`core.game_params` n'a aucune des deux clés ; le 25 000 n'existe que dans le commentaire de `sql/gold/010_bv_academy.sql:6` et le skill `06-tests.md`). Clés lues : `academie_valeur_high`, `academie_cout_test` de `core.game_params`. Rapport du 05/11 09:00 : 3 lignes « donnée manquante : valeur d'un High …, coût du test … » (Nael Lopez PG, Nathan Vidal PF, Sacha Aubert C), rangées dans « Autres points ». Quand les deux clés existeront : « tester » si P(High) × valeur > coût, sinon « ignorer » (règle d'espérance, marquée « à valider ») ; « signer » demande le résultat d'un test, absent de la base, donc jamais rendu. P(High) = `p_high_8_10` à la jauge actuelle (79 → 21,2 %), le même pour les trois : la vue ne donne pas de cote par prospect. Fin de la ligne : `[clé=Académie]` au registre après le rapport, ou rapport de plus de 7 jours.
- **K4** (`2040ea3`) : `gold.decisions_a_evaluer` = 0 ligne, aucun `[décision=<id>]` dans les registres des 7 derniers jours → aucune ligne (conforme). Lecture des registres par `relier_faits.lire_references`, aucune écriture.
- **K5** : `test_aujourdhui.py` 143 → **157/157** (K3 : 8 cas, K4 : 6 cas, présents et absents ; K2 : aucun, rien de codé). Sortie réelle : 8 lignes logiques.
- **K6** : rejeu avant 23,0 s (20 requêtes), après **7,6 s** (25 requêtes ; en série elles font 24,3 s). Différence de sortie : seule la ligne « Autres points » passe de 2 à 5 éléments (les 3 prospects).
- Hors périmètre, non commité : `outputs/basketvibe/aujourdhui-2026-11-09.md` (instantané réécrit par chaque exécution du script).

## Plan du jour, étape 5f (critères écrits le 2026-11-09 16:20 Paris, avant le code)

Contexte : main = 1d45858 ; suite de K2 et K3 (étape 5e). Décisions de l'utilisateur : même force = écart de 1 point de PS au poste ; coût du test = 25 000 ; valeur d'un High dérivée de l'historique si possible. Écritures en base autorisées : une migration additive (nouvelle vue) et des lignes de `core.game_params` avec leur source.

| # | Critère |
|---|---|
| L1 | Nouvelle vue `gold.bv_sell_replacement` (`sql/gold/072_bv_sell_replacement.sql`, additive, `security_invoker`, `grant select … to assistant_ro`), une ligne par joueur de `gold.bv_slot_fit` : `best_slot`, `fit_best` (force au meilleur poste), `replacement_id`, `replacement_name`, `replacement_fit`, `gap` (= `fit_best − replacement_fit`), `weekly_salary` (salaire économisé, `gold.bv_player_outlook.salary`, lu dans `silver.bv_player_salary_weekly`), `on_transfer_list`, `available_players`. **Colonne de force : `fit`** (sans la forme) pour le poste ET pour le rang : une vente est définitive, la forme (1-10, −11 % à +15 %) change d'un jour à l'autre. Le rang est recalculé sur `fit` dans la vue (l'incohérence de `bv_sell_candidates`, `best_slot` sur `fit` et `rank_in_slot` sur `fit_with_form`, n'est pas reprise). Meilleur poste : `fit` le plus haut, égalité départagée par l'ordre des postes (PG→C). Remplaçant : le meilleur autre joueur disponible (ni en vente, ni blessé) dont le `fit` au même poste est inférieur ou égal (égalité départagée par `player_id`) ; aucun → colonnes nulles. |
| L2 | `core.game_params` (`basketvibe`, `vente_tolerance_force`, `1.0`, source « décision de l'utilisateur du 2026-11-09 : même force = écart de 1 point de PS au poste », `verified_on` 2026-11-09). Le script lit la clé ; aucune valeur écrite dans le code. Clé absente → aucune ligne de vente. |
| L3 | Une seule ligne Transferts « Vendre X : économie S par semaine, remplaçant Y au poste Z, écart E » pour le joueur qui remplit `gap ≤ tolérance`, n'est pas déjà en vente, et laisse au moins 9 joueurs disponibles après la vente (`available_players` moins lui s'il est disponible) ; plusieurs candidats → le plus gros salaire. Sinon aucune ligne. La demi-ligne « vendre pour profit » reste. |
| L4 | `core.game_params` (`basketvibe`, `academie_cout_test`, `25000`, source `.claude/skills/basketvibe-academie/references/06-tests.md` — le 25 000 est dans ce skill, pas dans `basketvibe-economie`). Valeur d'un High : recherche dans `gold.bv_transfer_history` et dans les pages brutes (catégorie de potentiel connue d'un joueur vendu) ; requête et résultat collés ; ligne `academie_valeur_high` écrite seulement si au moins un High vendu existe. |
| L5 | Académie : les deux clés présentes → tester / ignorer comme à l'étape 5e ; sinon UNE ligne pour tout le rapport « Académie, rapport du JJ/MM : n prospects ; valeur d'un High inconnue » (donnée manquante nommée), au lieu d'une par prospect. |
| L6 | Tests figés, cas présent et cas absent pour L3 et L5 ; sortie ≤ 8 lignes, durée ≤ 15 s ; les 157 tests existants restent verts (ceux de K3 qui attendent une ligne par prospect sans donnée sont remplacés par L5, dit dans le résultat). |
| L7 | Rejeu `python -I pipelines/aujourdhui.py basketvibe` avant et après, sortie collée. Avant (16:17, 7,8 s) : 3 lignes « donnée manquante » par prospect dans « Autres points ». |

**L4, valeur d'un High : non calculable.** `gold.bv_transfer_history` (1 025 ventes, 02/09 → 08/11) n'a aucune colonne de potentiel ; `silver` non plus (recherche `information_schema.columns` sur `%potential%`). Dans les pages brutes, la catégorie n'apparaît que sous `potential_bucket` (pages `club`, `player`, `roster` ; les 5 pages `transfers` n'ont que `player_roster_potential_tests`). Requête (connecteur Supabase, lecture) :
```sql
with o as (select distinct p.page_type, j->>'potential_bucket' b, coalesce(j->>'player_id', j->>'id') pid
  from bronze.raw_pages p, jsonb_path_query(p.payload, 'strict $.**') j
  where p.game='basketvibe' and p.page_type in ('club','player','roster') and jsonb_typeof(j)='object' and j ? 'potential_bucket')
select o.page_type, o.b, count(distinct o.pid) joueurs, count(distinct h.player_id) vendus_en_historique, round(avg(h.fee)) prix_moyen
from o left join gold.bv_transfer_history h on h.player_id::text = o.pid group by 1,2 order by 1,2
```
Résultat : `club | decent | 1 | 1 | 10250` ; `player | decent | 1 | 1 | 10250` ; `roster | decent | 1 | 1 | 10250`. Un seul joueur à catégorie connue (Decent), **aucun High** : `academie_valeur_high` n'est pas écrite. Lignes écrites (`sql/core/025_game_params_vente_academie.sql`) : `vente_tolerance_force` = 1, `academie_cout_test` = 25 000.

**Résultats 5f (2026-11-09 16:25 Paris).**
- **L1** (`a3148fb`) : `gold.bv_sell_replacement` appliquée (migration `gold_072_bv_sell_replacement`), 14 lignes lues en `assistant_ro`. Écart ≤ 1 : Bernard/Albano (PF, 0,0, l'un remplace l'autre), Baron (PG, 0,4), Ungureanu (C, 0,7) ; tous les autres ≥ 1,2.
- **L2, L4** (`ba113e1`) : `vente_tolerance_force` = 1, `academie_cout_test` = 25 000 ; `academie_valeur_high` non écrite (aucun High, requête ci-dessus).
- **L3, L5** (`c6cb630`) : ligne « Vendre Catalin Ungureanu : économie 19 030 par semaine, remplaçant Maël Bernard au poste C, écart 0,7 » (plus gros salaire des 4 candidats, 14 disponibles → 13 après). Elle tombe dans « Autres points » : les lignes à heure limite passent d'abord et la ligne analyste (sans heure) prend la 5e place ; ordre de `rendre` inchangé. Académie : une ligne « Académie, rapport du 05/11 : 3 prospects ; valeur d'un High inconnue » au lieu de 3.
- **L6** : `test_aujourdhui.py` 157 → **167/167**. 3 cas K3 réécrits pour L5 (« une ligne par prospect sans donnée » → une ligne par rapport ; « clé antérieure → 3 lignes » → 1), 1 cas L5 ajouté de plus (singulier) et 1 cas absent (données présentes) ; L3 : 8 cas (4 présents, 4 absents). Autres suites : toutes vertes (`fin_etape.py`).
- **L7** : avant 7,8 s (25 requêtes), après **9,6 s** (27 requêtes) ; 8 lignes logiques. `diff` : seule « Autres points » change (5 → 4 éléments : + Vendre, 3 lignes académie → 1).
- `fusion_main.py` : `origin/main == HEAD` (c6cb630). `fin_etape.py` : 0 commit d'avance, tous les tests verts.
- Hors périmètre, non commité : `outputs/basketvibe/aujourdhui-2026-11-09.md`.

## Plan du jour, étape 5g (critères écrits le 2026-11-09 16:35 Paris, avant le code)

Contexte : l'avancement des expériences amicales E1 à E4 (`docs/attentes/experiences-amicales-basketvibe.yaml`) compte les lignes `[expérience=<id>:<niveau>]` du registre sans vérifier que le réglage a été joué ; la page « réglages utilisés » (`match-tactics-used`) arrive en bronze pour chaque amical exporté. Écritures en base autorisées : une migration additive (nouvelle vue, aucun drop) et des lignes de configuration avec leur source.

| # | Critère |
|---|---|
| M1 | Constat : où et comment les réglages utilisés d'un amical sont lus aujourd'hui (`silver.bv_fixture_api`, `gold.bv_match_tactics_used` ou autre). Pour les 3 derniers amicaux joués, tableau : match, quart-temps, agressivité par joueur, focus offensif, zone. Une lecture existe déjà → la nommer et ne pas en créer une deuxième. |
| M2 | Si le niveau d'agressivité joué est lisible par match : vue `gold.bv_amical_reglage` (additive, `security_invoker`, `grant select … to assistant_ro` comme les autres vues gold) : match, date, niveau uniforme (oui/non et valeur), focus offensif, zone. Sinon, dire ce qui manque. |
| M3 | Le plan du jour distingue, pour chaque expérience : déclarés, joués, vérifiés. La ligne dit « E1 : 1 vérifié sur 4, 1 déclaré non vérifié (match à exporter) » ; un amical déclaré dont le réglage joué ne correspond pas au niveau demandé est signalé « réglage joué ≠ réglage du test ». Le passage à l'expérience suivante ne compte que les amicaux vérifiés. |
| M4 | Les amicaux joués avant le début du test E1 ne comptent pour aucune expérience ; rien n'est écrit rétroactivement dans le registre. |
| M5 | Tests figés, un cas présent et un cas absent pour M3 ; sortie ≤ 8 lignes, durée ≤ 15 s ; les 167 tests existants restent verts. |
| M6 | Rejeu `python -I pipelines/aujourdhui.py basketvibe` avant et après (sortie collée telle quelle). |

**M1, constat (2026-11-09 16:45 Paris).** `gold.bv_match_tactics_used` n'existe pas. Lectures en place :
1. **`silver.bv_match_tactics`** (`sql/silver/003_bv_matches.sql:125`) : dernière capture `match-tactics-used` (page « réglages utilisés ») de `silver.bv_fixture_api`, par match et par équipe : `player_directives` (par joueur, pour tout le match : `defense_tier`, `offensive_focus_tier`, `shot_tier`, `role_tier`, crans 0–4 de l'API), `lineup_by_quarter` (5 tableaux de 5 `player_id` : Q1 à Q4, puis prolongation), `defensive_focus` (par adversaire : `focus`, `area_step`). Amicaux finis : 29, dont 26 avec cette page.
2. **`gold.bv_match_player_lines`** (`sql/gold/003_bv_match_report.sql:75-103`) : la relit par joueur et par match (consignes jouées) ; pas de lecture par quart-temps ni de niveau d'équipe.
3. **`gold.bv_zone_jouee`** (`sql/gold/025_bv_zone_jouee.sql`) : zone lue dans `match-tactics` (page **avant** le match), pas dans les réglages utilisés. Écart constaté le 09/11 (Garden City) : `bv_zone_jouee` = Middle (3), capture du 08/11 10:12 UTC ; réglages utilisés = Perimeter (1) pour les 12 adversaires. Les deux autres amicaux n'ont pas de page `match-tactics`. Vue non modifiée (hors périmètre).

Aucune lecture ne donne « niveau d'agressivité uniforme par match » : la vue M2 est créée sur `silver.bv_match_tactics` (pas de deuxième lecture du bronze).

Échelle (`docs/fiches/basketvibe/match.md:19`, confirmée par l'utilisateur le 2026-10-18) : écran = cran API + 1. L'étude (`etude-evenements-basketvibe.md:135`, tranches « moins de 1 ; de 1 à 3 ; plus de 3 ») compte en crans API : E1 A = cran 2 (**écran 3**), B = cran 4 (**écran 5**). Le texte du YAML « agressivité 2 sur les cinq » fait saisir écran 2 = cran 1, dans la même tranche que B mal saisi (écran 4 = cran 3) : E1 ne séparerait aucune tranche. Corrigé avec M3 (texte écran + cran attendu).

3 derniers amicaux joués (`silver.bv_match_tactics` × `silver.bv_my_team`), valeurs **écran** ; joueurs dans l'ordre C, PF, PG, SF, SG ; focus offensif dans le même ordre ; Q5 = case prolongation (aucune prolongation jouée, `overtime_periods` = 0) :

| Match | Q | Agressivité par joueur | Focus offensif | Zone (12-13 adversaires) |
|---|---|---|---|---|
| 09/11 Garden City (L) | 1 | Bernard 1, Albano 1, Baron 1, Durand 1, Leclerc 1 | 2 3 2 3 4 | Perimeter (1), focus normal |
| | 2 | Bernard 1, Legrand 1, Boyer 1, Durand 1, Leclerc 1 | 2 3 2 3 4 | |
| | 3 | Ungureanu 1, Albano 1, Baron 1, Durand 1, Leclerc 1 | 3 3 2 3 4 | |
| | 4 | Ungureanu 1, Legrand 1, Boyer 1, Durand 1, Dang 1 | 3 3 2 3 3 | |
| 08/11 New York City Cyclones (L) | 1 | Bernard 1, Albano 1, Baron 1, Durand 1, Leclerc 1 | 2 3 2 3 4 | Perimeter (1), focus normal |
| | 2 | Bernard 1, Legrand 1, Boyer 1, Durand 1, Leclerc 1 | 2 3 2 3 4 | |
| | 3 | Ungureanu 1, Albano 1, Baron 1, Durand 1, Leclerc 1 | 3 3 2 3 4 | |
| | 4 | Ungureanu 1, Legrand 1, Boyer 1, Durand 1, Dang 1 | 3 3 2 3 3 | |
| 07/11 Knight Jays (L) | 1 | Bernard 1, Albano 1, Baron 1, Durand 1, Leclerc 1 | 2 3 2 3 4 | Perimeter (1), focus normal |
| | 2 | Bernard 1, Lefebvre 1, Boyer 1, Durand 1, Leclerc 1 | 2 3 2 3 4 | |
| | 3 | Ungureanu 1, Albano 1, Baron 1, Durand 1, Leclerc 1 | 3 3 2 3 4 | |
| | 4 | Ungureanu 1, Lefebvre 1, Boyer 1, Durand 1, Dang 1 | 3 3 2 3 3 | |

Les trois : agressivité uniforme écran 1 (cran 0, Soft), aucun focus offensif Primary (écran 5). Aucun n'est un amical E1.

**Résultats 5g (2026-11-09 17:00 Paris).**
- **M1** (`c20d3ae`) : constat ci-dessus ; lecture réutilisée = `silver.bv_match_tactics`.
- **M2** (`8d0184c`) : `gold.bv_amical_reglage` (`sql/gold/073_bv_amical_reglage.sql`, migration `gold_073_bv_amical_reglage`, `security_invoker`, `grant select … to assistant_ro`) : `match_day`, `opponent`, `my_result`, `joueurs`, `agress_uniforme`, `agress_cran`, `agress_ecran`, `agress_min/max`, `primary_quarts`, `focus_off_max`, `tir_cran4_joueurs`, `zone` (lue dans les réglages utilisés). 26 lignes en `assistant_ro` ; 07, 08, 09/11 : uniforme, écran 1, 0 quart Primary, Perimeter. Requête seule : 1,2 s.
- **M3** (`f2cad2f`) : un fait `[expérience=…]` est rattaché au match de sa clé, sinon au premier amical joué le jour du registre ou le lendemain. Vérifié = réglage joué conforme à `joue` du YAML (E1 : `agress_cran` 2 ou 4 ; E2 : ≥ 2 joueurs au focus de tir cran 4 ; E3 : Primary aux 4 quarts ; E4 : tout amical joué) ; écart → « réglage joué ≠ réglage du test (Club JJ/MM) » ; non exporté → « déclaré non vérifié (match à exporter) ». Passage à l'expérience suivante : vérifiés seuls ; niveau A/B suivant : vérifiés + en attente (un écart fait rejouer le même niveau). L'avancement est ajouté au détail de la ligne du test (pas de ligne de plus). **Correction du YAML** : textes des niveaux en valeurs écran (E1 A « agressivité 3 à l'écran (cran 2, équilibrée) », B « 5 (cran 4) » ; E2 « focus de tir 5 à l'écran (cran 4) ») ; avant, « agressivité 2 » faisait saisir le cran 1.
- **M4** : `debut: 2026-11-10` dans le YAML (E1 validée le 09/11 vers 16:00, amical du 09/11 déjà joué) ; un fait dont l'amical est antérieur ne compte pour rien. Aucune écriture au registre (test : fichiers inchangés).
- **M5** : `test_aujourdhui.py` 167 → **181/181**. Réécrits : « passage à E2 » (absent, présent) et « H4 toutes terminées » (ils comptaient les déclarés ; ils ont maintenant des réglages joués), H3 sans brief et avec brief (nouveau texte du niveau A) ; les anciens cas H7 neutralisent `debut` (cas d'avant 5g). Ajoutés 14 : M3 passage sans export, écart (niveau rejoué), ligne présente / absente, écart présent / absent, rattachement sans clé, match compté une fois, plan sans déclaration, plan avec saisie déclarée ; M4 avant début présent / absent, début lu, aucune écriture. Autres suites : vertes (`fin_etape.py`). Sortie : 8 lignes logiques.
- **M6** : avant 9,3 s (27 requêtes), après **11,2 s** (28 requêtes). `diff` : seule la ligne 07:45 change.

Avant :
```
07:45 — Amical contre Opper Cards (mar. 10/11) : saisis le test E1 niveau A : agressivité 2 sur les
    cinq — heure limite du verrou 07:45 ; réglage du test à la place de celui du brief ; après le
    match exporte : aperçu, box scores par quart-temps, réglages utilisés, page Équipe du jour
```
Après :
```
07:45 — Amical contre Opper Cards (mar. 10/11) : saisis le test E1 niveau A : agressivité 3 à
    l'écran (cran 2, équilibrée) sur tous les joueurs — heure limite du verrou 07:45 ; réglage du
    test à la place de celui du brief ; après le match exporte : aperçu, box scores par quart-temps,
    réglages utilisés, page Équipe du jour ; E1 : 0 vérifié sur 4
```
(Les 7 autres lignes sont identiques, sortie complète dans le rapport de session.)
- `fusion_main.py` : 4 commits ajoutés, `origin/main == HEAD` (f2cad2f). `fin_etape.py` : 0 commit d'avance, 22 suites vertes (dont `test_aujourdhui.py` 181/181).
- Hors périmètre, non commité : `outputs/basketvibe/aujourdhui-2026-11-09.md`.

## Plan du jour, étape 5h (critères écrits le 2026-11-09 16:50 Paris, avant le code)

Contexte : main = c202605 ; playbook, étape 5, actions 7 et 8. `gold.bv_zone_jouee` lit la page d'avant-match (09/11 : Middle, zone jouée Perimeter). Écritures en base autorisées : une migration additive (`create or replace` de `gold.bv_zone_jouee` seulement ; autres vues nouvelles), rien d'autre.

| # | Critère |
|---|---|
| N1 | Zone jouée : lister d'abord les lecteurs de `gold.bv_zone_jouee` (vues dépendantes, scripts, skills, cartes : grep et `pg_depend`) ; puis la vue lit la zone des réglages utilisés (`match-tactics-used`, `silver.bv_match_tactics`) quand le match est joué, la page d'avant-match seulement pour un match à venir. Mêmes colonnes en tête (aucune colonne retirée ni renommée). Preuve : amicaux des 07, 08, 09/11, avant et après (Perimeter pour les trois après). |
| N2 | Entraînement : lire `gold.bv_saisie_entrainement` et la règle `entrainement_sam` (`core.agenda_rule`) ; le jour de la règle, une ligne du plan avec la fiche de saisie (joueur, focus attendu) et le contrôle focus attendu contre focus saisi : seulement les écarts ; zéro écart = zéro ligne. Dire ce que la vue sait faire et ce qui manque. |
| N3 | Fatigue : lire `gold.bv_fatigue_plan` ; une ligne « sors X avant le match Y » seulement quand la fatigue projetée dépasse la zone verte de `core.alert_rule` (règle `fatigue`, `seuil_bas`) pour un joueur qui doit jouer (minutes > 0 dans la saisie du match de ligue ou de coupe à venir) ; aucun seuil écrit dans le code. |
| N4 | Tests figés, un cas présent et un cas absent pour N2 et N3 ; sortie ≤ 8 lignes, durée ≤ 15 s ; les 181 tests existants restent verts. |
| N5 | Rejeu `python -I pipelines/aujourdhui.py basketvibe` avant et après (sortie collée telle quelle). |

**Résultats 5h (2026-11-09 17:15 Paris).**
- **N1** (`d8bce39`, migration `gold_074_bv_zone_jouee_reglages_utilises`). Lecteurs de `gold.bv_zone_jouee` avant changement : aucune vue dépendante (`pg_depend` : 0 ligne) ; aucun script de `pipelines/` (seuls des briefs du jeu d'essai la citent) ; `docs/attentes/tests/basketvibe.yaml` (Q2, Q3), cartes `docs/decisions/cartes/basketvibe/defaite.md:31` et `composition.md:35`, `docs/regles/triage.md:132` (L36, ce défaut), briefs et learnings (texte). Colonnes d'origine gardées, `source` ajoutée (`reglages_utilises` / `avant_match`) ; 20 → 58 lignes. Amicaux 07, 08, 09/11 : **avant** absent, absent, Middle (3) ; **après** Perimeter (1) ×3, source `reglages_utilises`. Ligue J4 du 09/11 (à venir) : Middle, `avant_match`.
- **N2** (`6640a53`). `gold.bv_saisie_entrainement` sait : l'entraînement **saisi** (principale, secondaire) par joueur, dans l'ordre de l'écran, d'après le dernier export `training` (08/11 10:08 UTC, 14 joueurs). Il manque : le **focus attendu** (aucune table, aucune colonne ; `learn.decision` domaine entrainement : texte libre, dernière décision le 25/10). Source retenue : la fiche « Poste | Joueur | Principale | Secondaire » du dernier brief `briefs/<date>-entrainement.md` (aujourd'hui celui du 25/10, 17 joueurs dont 4 partis ; Ungureanu absent). Règle `entrainement_sam` : `isodow` 6, 23:00. Le samedi avant 23:00, une ligne « Entraînement (fin du cycle …) : corrige n écarts » (focus attendu et saisi), à la place de la ligne d'agenda ; « indifférent » non contrôlé ; joueur hors fiche signalé ; zéro écart → la ligne d'agenda seule. Contrôle à blanc sur les données du jour : 0 écart de focus, 1 joueur hors fiche (Ungureanu). Aujourd'hui lundi : aucune ligne.
- **N3** (`805bde3`, migration `gold_075_bv_fatigue_avant_match`, nouvelle vue). Joueurs à minutes > 0 dans la saisie d'un match de ligue ou de coupe à venir (`gold.bv_saisie_joueurs`) × `gold.bv_fatigue_plan` (minutes, cran d'agressivité) ; zone verte = `seuil_bas` de la règle `fatigue` (20) lue dans la vue. Jointure par nom de famille (la saisie n'expose pas `player_id`). J4 du 09/11 : 10 joueurs à 24 min, cran 2, fatigue 11,0 à 14,1 : aucune ligne. Ligne « Sors X, Y avant le match de ligue contre Z (jour) » à l'heure du verrou, seulement si dépassement.
- **N4** : `test_aujourdhui.py` 181 → **193/193** (N2 : 8 cas, dont zéro écart / écarts, autre jour, cycle passé, fiche absente, règle absente, lecteur présent / absent ; N3 : 4 cas, dépassement / vue vide / verrou passé / seuil venu de la vue). Aucun test existant modifié. Sortie : 8 lignes logiques.
- **N5** : avant 11,0 s (28 requêtes), après **10,1 s** (31 requêtes). Sortie **identique** (`diff`) : lundi, pas de fin de cycle ; aucune fatigue hors zone verte.
- `fusion_main.py` : 5 commits ajoutés, `origin/main == HEAD` (805bde3). `fin_etape.py` : 0 commit d'avance, 22 suites vertes.

## Revue hebdomadaire, étape 6a (critères écrits le 2026-11-09 17:00 Paris, avant le code)

Contexte : playbook, « Remise en question du modèle (chaque semaine) », huit questions, la plupart « à créer ». Première version : seulement ce que la base permet aujourd'hui ; « n insuffisant » ou « donnée manquante » pour le reste ; aucune interprétation, aucun conseil. Lecture seule sur la base, aucune migration ni vue modifiée.

| # | Critère |
|---|---|
| R1 | `python -I pipelines/revue_hebdo.py basketvibe` écrit `outputs/basketvibe/revue-hebdo-AAAA-MM-JJ.md` : une page, 60 lignes au plus, 20 s au plus. Chaque section a un chiffre, un n et la source. Semaine = les 7 jours finissant le jour de Paris. |
| R2 | Décisions : verdicts de la semaine (`learn.outcome` × `learn.decision`, `measured_at` dans la semaine) par domaine : confirmés, contredits, non concluants ; en attente = décisions prises dans la semaine sans verdict. Chaque verdict dit s'il mesure l'**exécution** (la requête lit un réglage saisi ou joué : `tier`, `bv_match_tactics`, `bv_saisie`, `player_directives`, `bv_amical_reglage`, `bv_zone_jouee`) ou l'**effet** (résultat ou statistique du match). Part contredite par domaine avec son n ; « n insuffisant » sous 10 verdicts. |
| R3 | Leçons : comptes par état de `learn.lesson` (hypothèse, validée, retirée) ; « contre » ajoutés cette semaine = somme des `n_against` moins celle de l'instantané précédent du dossier de sorties (aucun instantané : « pas d'instantané précédent ») ; hypothèses sans nouvelle mesure depuis 14 jours = aucun `learn.outcome` depuis 14 jours sur une décision liée (`lesson_id`), liste des identifiants. |
| R4 | Matchs de la semaine (`gold.bv_match_report`) : une ligne par match, résultat par `my_result` ; marge moyenne ; compte par compétition. « Matchs les plus mal prédits » : « donnée manquante : aucune prédiction de marge en base ». |
| R5 | Expériences amicales : par expérience, amicaux vérifiés sur visés (`gold.bv_amical_reglage`, même règle que le plan du jour). Le dimanche, n disponible de l'étude : `etude_evenements_basketvibe.py calculs` mesuré à **11,4 s** le 09/11 17:00 (> 10 s) → « non calculé » écrit, le script de l'étude n'est pas lancé. |
| R6 | Données : nombre de types de pages reçus et non lus (`gold.bv_couverture_pages`, `lu_par_silver = 'non'`) et écart avec la semaine précédente ; instantané JSON écrit dans `outputs/basketvibe/revue-hebdo/` (même instantané que R3). |
| R7 | Paramètres écrits à la main : la liste du playbook (« Paramètres écrits à la main », lue dans le fichier) avec la date de leur dernière vérification dans `core.game_params` (source et `verified_on`) ; correspondance paramètre → clé écrite dans le script ; sans clé : « jamais calculé ». |
| R8 | Plan du jour : le dimanche, une ligne « Revue de la semaine : à lire (outputs/basketvibe/revue-hebdo-AAAA-MM-JJ.md) », sinon rien ; test figé présent / absent ; plan ≤ 8 lignes, ≤ 15 s. **Écart à la consigne, tranché** : R8 oblige à toucher `pipelines/aujourdhui.py` et `pipelines/test_aujourdhui.py`, en plus du nouveau script, de son test, du dossier de sorties et du journal. |
| R9 | Tests figés (données factices) pour R2 à R7, un cas présent et un cas absent chacun (`pipelines/test_revue_hebdo.py`) ; les 193 tests existants restent verts. |

**Résultats 6a (2026-11-09 17:20 Paris).**
- **R1** (`723a661`) : `python -I pipelines/revue_hebdo.py basketvibe` → `écrit outputs/basketvibe/revue-hebdo-2026-11-09.md (55 lignes, 2.2 s)` ; 7 requêtes en parallèle ; au-delà de 60 lignes la page est coupée et la dernière ligne le dit (testé).
- **R2** : 6 verdicts de la semaine (composition 1 confirmé / 3 contredits, tactique 0 / 2), tous « effet » (requêtes sur `gold.bv_match_report` ou `my_result`) ; 5 décisions en attente (académie 1, achat 2, composition 1, tactique 1) ; part contredite : « n insuffisant » partout (n ≤ 4 < 10).
- **R3** : hypothèse 34, validée 3, aucune retirée ; « contre » : pas d'instantané précédent (total 1) ; hypothèses sans mesure depuis 14 jours : 34 sur 34 (aucune décision liée n'a de verdict).
- **R4** : 9 matchs (7 amicaux, 2 ligue), 1 V – 8 D par `my_result`, marge moyenne −17,0 ; « matchs les plus mal prédits : donnée manquante ». Le nom d'adversaire `|HAVEX|` est échappé dans le tableau.
- **R5** : E1 à E4 : 0 vérifié (aucun fait déclaré) ; le n de l'étude n'est pas calculé (11,4 s mesurés > 10 s) ; la ligne ne paraît que le dimanche.
- **R6** : 93 types non lus sur 126 ; pas d'instantané précédent ; instantané écrit : `outputs/basketvibe/revue-hebdo/instantane-2026-11-09.json` = `{"n_against": 1, "non_lus": 93}`. Instantané de comparaison = le plus récent daté de 7 jours ou plus, sinon le plus récent avant le jour.
- **R7** : 8 paramètres lus dans le playbook ; 1 avec date (Âge de déclin, `age_declin`, 2026-11-03) ; 7 « jamais calculé ». Âge des écrans et seuils de fatigue/forme sont en base (`core.export_rule`, `core.alert_rule`) mais sans date de calcul : marqués « jamais calculé » comme la consigne le demande.
- **R8** (`b5364d9`) : ligne le dimanche seulement (priorité 3, sans heure ; page absente → la commande en détail). Rejeu du lundi : sortie identique (10,3 s).
- **R9** : `test_revue_hebdo.py` **28/28** ; `test_aujourdhui.py` 193 → **197/197** (R8 : 4 cas) ; autres suites vertes.
- `fusion_main.py` : 3 commits ajoutés, `origin/main == HEAD` (b5364d9). `fin_etape.py` : 0 commit d'avance, 23 suites vertes.

## Revue hebdomadaire, étape 6b (critères écrits le 2026-11-09 17:10 Paris, avant le code)

Contexte : main = ff98afe. La revue du 09/11 montre 34 hypothèses sur 34 sans mesure depuis 14 jours ; les décisions ne sont pas reliées aux leçons qu'elles testent. Lecture seule sur la base, aucune écriture dans `learn.*` ; seuls le fichier de configuration des expériences, le script de revue, ses tests et le journal bougent.

| # | Critère |
|---|---|
| S1 | Inventaire en lecture seule des leçons de `learn.lesson` (34 hypothèses, 3 validées) : identifiant, énoncé court, domaine, et un classement parmi « testable par la file d'expériences » (laquelle), « testable sur l'historique » (étude des événements ou vue gold nommée), « à reformuler », « sans mesure possible avec les données actuelles », avec une phrase de justification. Tableau dans ce journal. |
| S2 | Pour chaque expérience du fichier `docs/attentes/experiences-amicales-basketvibe.yaml` : nouvelle clé `lecons` (identifiants des leçons que son verdict met à jour). Aucune hypothèse ne correspond → une phrase de leçon à créer dans ce journal, non écrite en base. |
| S3 | `pipelines/revue_hebdo.py` : section « Expériences à conclure » ; pour chaque expérience dont les amicaux vérifiés atteignent le visé : « verdict à produire : E1, n = 4, leçons L-xxx » ; sinon « aucune expérience à conclure ». Aucun verdict écrit. Page ≤ 60 lignes. |
| S4 | Champs de `pipelines/decision.py` qui permettent de relier une décision à une leçon (`lesson_id`), et changements proposés dans `decision.py` ou un skill pour que le lien soit rempli à la création ; proposé, non appliqué. |
| S5 | Tests figés pour S2 (lecture de la clé `lecons`) et S3, un cas présent et un cas absent chacun ; 197 tests du plan et 28 de la revue verts. |

**S1, inventaire (lecture seule, `select id, domain, status, claim from learn.lesson where game = 'basketvibe'`, 37 lignes, 2026-11-09 17:15).** Aucune leçon n'a de `check_sql` ; `n_for`/`n_against` non nuls seulement pour L-001 (21/0), L-004 (7/1), L-006 (3/0). Expériences : E1 agressivité défensive uniforme (cran 2 / 4) ; E2 focus de tir cran 4 sur deux tireurs ; E3 focus offensif Primary aux 4 quarts ; E4 réglage habituel (chiffre 1 de l'étude : réussite du tir selon la compétence). Étude = `pipelines/etude_evenements_basketvibe.py`, chiffres 1 à 8.

| Leçon | État | Domaine | Énoncé court | Classement | Justification |
|---|---|---|---|---|---|
| L-001 | validée | tactique | V et D se séparent par eFG, eFG adverse, OREB, pertes adverses | historique : `gold.bv_match_report` | les quatre facteurs sont des colonnes de la vue, par `my_result`, recalculables chaque semaine |
| L-002 | hypothèse | tactique | moins de tirs à 3 → meilleure eFG | expériences : E2 | E2 fait varier le focus de tir et mesure la part de tirs à 3 (chiffre 5) ; seul le réglage change |
| L-003 | hypothèse | composition | rotation 2 × 24 min meilleure que 5 × 48 | historique : `gold.bv_match_report` × `gold.bv_match_player_lines` | minutes par joueur et marge en base, mais adversaires et moteur différents : comparaison confondue, à dire |
| L-004 | validée | tactique | `defense_tier` 0 : eFG adverse plus basse, FT rate adverse plus bas | expériences : E1 | E1 joue les crans 2 et 4 uniformes ; mesure du FT rate et de l'eFG adverse par cran (chiffre 2) |
| L-005 | hypothèse | tactique | matchs serrés perdus sur une perte de balle en fin de match | historique : `silver.bv_match_events` | les actions de fin de match sont en base ; n = 3 matchs serrés, n insuffisant aujourd'hui |
| L-006 | validée | achat | le give_up sur le vrai scoreur lui laisse 34 à 39 pts | historique : `gold.bv_match_opp_focus` | focus défensif et part de tirs du joueur adverse par match ; domaine `achat` probablement faux (tactique) |
| L-007 | hypothèse | tactique | sous 5 × 48, pas de signal net de la pénalité au Q4 | historique : étude, chiffre 4 | l'étude mesure la pénalité au-delà de 36 min sur les tirs du Q4 |
| L-008 | hypothèse | tactique | amical cran 2 : eFG, FT rate, fautes adverses plus hauts qu'au cran 0 | expériences : E1 | E1 niveau A = cran 2 uniforme, comparé au cran 0 déjà en base |
| L-009 | hypothèse | tactique | Q4 du preset amical à −10, Boyer 6 fautes | à reformuler | constat d'un match nommé, aucune règle générale à tester |
| L-009#2 | hypothèse | tactique | 3 amicaux sur 3 avec un Q4 négatif | à reformuler | doublon de L-009 avec une généralisation ; à écrire « Q4 des amicaux négatif » et mesurer par `quarter_margins` |
| L-010 | hypothèse | tactique | écart entre les deux unités de 24 min en J19 | à reformuler | un match, deux unités nommées ; pas de règle |
| L-010#2 | hypothèse | tactique | idem L-010 avec J20 | à reformuler | doublon de L-010 ; deux matchs, pas de règle |
| L-011 | hypothèse | composition | amical Carnage joué sans plan sauvegardé | à reformuler | constat de donnée (plan absent), pas une hypothèse de jeu |
| L-011#2 | hypothèse | tactique | fautes et FT rate adverses montent avec l'agressivité, eFG adverse aussi | expériences : E1 | énoncé exact du chiffre 2 ; E1 donne 2 matchs par cran |
| L-012 | hypothèse | tactique | en amical, fatigue des plus chargés sous la zone jaune | historique : `gold.bv_fatigue_plan`, `gold.bv_player_outlook` | fatigue par joueur et projection en base |
| L-012#2 | hypothèse | composition | aucun Lock dans nos données, effet du focus 4/5 inconnu | sans mesure possible | 5 cas `off` (Lock) en base ; aucune expérience ne fait varier le focus défensif |
| L-013 | hypothèse | composition | pas de lien entre minutes et rendement des jeunes | historique : `gold.bv_match_player_lines` | minutes et éval par minute par joueur et par match en base |
| L-013#2 | hypothèse | tactique | J21 perdu aux rebonds | à reformuler | un match ; la règle générale est L-016#2 |
| L-014 | hypothèse | composition | amical Vigolana : consignes absentes de l'export | à reformuler | constat de donnée, pas une hypothèse de jeu |
| L-014#2 | hypothèse | tactique | la Preview désigne mal la cible du focus | historique : pages `preview` × `gold.bv_match_opp_focus` | effectif de la Preview et part de tirs réelle sont tous deux en base |
| L-015 | hypothèse | tactique | cran 5 supposé : fautes au maximum, eFG adverse aussi | expériences : E1 | E1 niveau B = cran 4 uniforme, réglage enfin vérifié par les réglages utilisés |
| L-015#2 | hypothèse | tactique | J21 : 1re mi-temps perdue au tir, 2e aux lancers | à reformuler | un match, pas de règle |
| L-016 | hypothèse | composition | Q4 à −18 après la sortie de Baron (6 fautes) | à reformuler | un match ; la règle générale (fautes des meneurs) est L-021 |
| L-016#2 | hypothèse | tactique | écart d'OREB ≤ −13,9 : défaites lourdes | historique : `gold.bv_match_report` | OREB et marge par match en base |
| L-017 | hypothèse | tactique | focus sur les stars adverses : leurs coéquipiers reprennent les tirs | historique : `gold.bv_match_opp_focus` | part de tirs par adversaire et focus en base |
| L-017#2 | hypothèse | composition | `off` = Lock : part de tirs adverse 4 % | historique : `gold.bv_match_opp_focus` | 8 cas en base, n petit ; mesure possible, n insuffisant |
| L-018 | hypothèse | tactique | libellé d'export `off` = Lock | à reformuler | confirmé par l'utilisateur ; c'est une règle de lecture (skill ou vue), pas une hypothèse |
| L-019 | hypothèse | tactique | J22 gagné aux rebonds et aux pertes forcées | à reformuler | un match ; la règle générale est L-001 |
| L-020 | hypothèse | tactique | Debrecen perdu par l'attaque, un tireur faible au focus de tir élevé | expériences : E2 | E2 fait varier le focus de tir de deux tireurs et mesure leur part de tirs à 3 |
| L-021 | hypothèse | tactique | sorties pour 6 fautes en amical entre 28 et 34 min | expériences : E1 | E1 mesure les fautes par cran d'agressivité ; les sorties pour 6 fautes sont dans `gold.bv_match_player_lines` (`fouled_out`) |
| L-022 | hypothèse | tactique | New Generation gagné au tir | à reformuler | un match ; la règle générale est L-001 |
| L-023 | hypothèse | tactique | adversaire à 5 × 48 ; zone Rim prouvée | à reformuler | un match, trois facteurs (minutes adverses, zone, focus) |
| L-024 | hypothèse | tactique | lire les réglages d'un amical dans `gold.bv_zone_jouee` | à reformuler | règle de lecture, dépassée par l'étape 5h (la vue lit désormais les réglages utilisés) |
| L-025 | hypothèse | tactique | Statyba perdu par l'attaque : 37 tirs à 3 à 16 % | expériences : E2 | même mécanisme que L-020 (focus de tir) |
| L-026 | hypothèse | composition | en coupe, le Q4 au-delà de 36 min coûte | historique : étude, chiffre 4 | l'étude mesure la pénalité au-delà de 36 min (coupe v4 : 78 tirs) |
| L-027 | hypothèse | tactique | zone Middle en amical v4 = pire 2P % adverse | historique : `gold.bv_zone_jouee` × `gold.bv_match_report` | zone jouée corrigée en 5h et 2P % adverse par match en base |
| L-028 | hypothèse | achat | enchères maximales trop basses sur les SG 57-60 | historique : `gold.bv_transfer_history` | prix de vente par poste et PS en base |

Bilan (37) : expériences 8 (E1 : 5, E2 : 3, E3 : 0, E4 : 0) ; historique 14 ; à reformuler 14 (dont 4 doublons `#2` ou constats d'un seul match) ; sans mesure possible 1.

**S4, lien décision → leçon (proposé, non appliqué).** État : `learn.decision` = 149 décisions BasketVibe, **1** avec `lesson_id` (47 des 14 derniers jours, 1 liée). Champs de `pipelines/decision.py new` qui peuvent porter le lien :
1. `--lecon L-nnn` → `lesson_id` : seul lien direct ; **optionnel**, préfixé `basketvibe:` par le script (`decision.py:117`), refusé si la leçon est retirée. Aucun agent ni skill ne le passe (grep de `--lecon` dans `.claude/` : 0 résultat ; `pipelines/dossier.py:221` donne la commande sans `--lecon`).
2. `domaine` → `domain` : même vocabulaire que `learn.lesson.domain` ; filtre possible, pas un lien.
3. `--hypothese` → `hypothesis` et `--label` → `label` : texte libre ; un lien par texte serait une supposition.
4. `--prediction` → `prediction` (`metric`, `requete`) : la requête pourrait être comparée au `check_sql` de la leçon, mais les 37 leçons ont `check_sql` vide.
5. `--sujet` → `sujet` : joueur ou réglage visé, utile pour retrouver une leçon sur le même réglage, pas un lien.

Changements proposés :
- **`decision.py`** : `--lecon` obligatoire, ou `--sans-lecon "<raison>"` explicite (raison dans `evidence`) ; la commande affiche les leçons ouvertes du même domaine (`select id, left(claim, 80) from learn.lesson where game = … and domain = … and status <> 'retired'`) pour que l'agent choisisse. Refus si l'identifiant n'existe pas (aujourd'hui seul « retirée » est refusé).
- **`decision.py`** : si le libellé porte `[expérience=<id>:<niveau>]`, `lesson_id` = première leçon de la clé `lecons` de cette expérience (fichier de configuration), plusieurs leçons → la décision cite les autres dans `evidence`.
- **`pipelines/dossier.py:221`** : la commande proposée contient `--lecon <L-nnn | aucune>`.
- **Skill `deja-fait` et agents `tactique`, `match`, `decideur`** : une phrase « toute décision enregistrée cite la leçon qu'elle teste (`--lecon`) ou dit pourquoi aucune ».
- **`learn.lesson.check_sql`** : remplir pour les 14 leçons « historique » (S1) ; sans ce champ, ni le lien ni la mesure ne sont automatiques.

**Résultats 6b (2026-11-09 17:30 Paris).**
- **S1** (`dc8a12f`) : inventaire ci-dessus ; 37 leçons classées.
- **S2** (`ef7ab19`) : clé `lecons` : E1 [L-004, L-008, L-011#2, L-015, L-021] ; E2 [L-002, L-020, L-025] ; E3 [] ; E4 []. Les 8 identifiants existent en base (`select count(*) … in (…)` = 8). Leçons à créer, proposées en commentaire du fichier, non écrites : E3 « Un joueur au focus offensif Primary tente environ 1,33 fois les tirs d'un joueur Normal sur le même quart [M§6.3] » ; E4 « La réussite à 3 points de nos tireurs monte avec leur compétence Trois points, à type de tir égal ».
- **S3** (`3eb37ed`) : section « 5. Expériences à conclure » ; page réelle du 09/11 : « aucune expérience à conclure (0 sur 4 au nombre visé d'amicaux vérifiés) — source : fichier d'expériences (clé lecons) × gold.bv_amical_reglage ; verdict non écrit ». Page : 58 lignes, 1,9 s. Limite : une semaine de 14 matchs dépasse 60 lignes ; la page est alors coupée et la dernière ligne le dit (comportement R1).
- **S4** : ci-dessus, rien appliqué.
- **S5** : `test_revue_hebdo.py` 28 → **34/34** (S2 : 2 cas, S3 : 4 cas) ; `test_aujourdhui.py` **197/197**.
- `fusion_main.py` : 4 commits ajoutés, `origin/main == HEAD` (3eb37ed). `fin_etape.py` : 0 commit d'avance, 23 suites vertes.

## Versions du moteur, étape 6c (critères écrits le 2026-11-09 17:13 Paris, avant le code)

Contexte : aucune version du moteur en base ; l'étude des événements et la préanalyse la déduisent des dates (`preanalyse-matchs-basketvibe.md` § 1.1). v5 annoncé en ligue « vers le milieu de la saison », sans date. Écritures autorisées : une migration additive (une table, une vue, aucun drop) et les lignes de la table.

| # | Critère |
|---|---|
| V1 | Table `core.engine_version` (`game`, `version`, `competition_kind`, `start_date`, `end_date` nullable, `source`, `statut` ∈ {annoncé, déduit}), lecture pour `assistant_ro`. Vocabulaire de `competition_kind` = celui de `core.fixture` (ligue, coupe, amical). Cinq lignes BasketVibe, exactement : ligue v3 du 07/09 au 26/10 ; ligue v4 depuis le 02/11 ; coupe v4 du 28/10 au 31/10 ; amical v4 du 11/10 au 27/10 ; amical v5 depuis le 28/10. Chaque ligne cite sa source (skill `basketvibe-communaute` 02-1, skill `basketvibe-saison`, préanalyse § 1.1, étude) et dit si sa date est annoncée ou déduite. Début de la ligue v3 = 07/09 (premier match de la saison 1, déduit) : le skill dit aussi « v3 en ligue depuis la journée 12 » (03/10) ; conflit écrit dans la source de la ligne, la règle de l'étude (v3 jusqu'au 26/10) est gardée. |
| V2 | Vue `gold.bv_match_engine_version` : un match joué de `core.fixture` = une ligne (aucun doublon), version et statut de la ligne dont la compétition est la sienne et la période contient son jour ; aucune ligne → version « non attribuée ». Compte par version et compétition collé ; matchs « non attribuée » listés. Connu avant le code : coupe du 13/09, amical du 10/10 et coupe du 01/11 sont hors des cinq lignes. |
| V3 | Contrôle sur les 78 matchs de `silver.bv_match_events` : version de la vue (nos matchs) ou, pour les matchs des autres équipes absents de `core.fixture`, la même jointure sur `core.engine_version` (competition `league/cup/friendly` → `ligue/coupe/amical`) ; comparée à `groupe()` de `etude_evenements_basketvibe.py` (fonction importée, script non modifié). Liste des écarts ; cible zéro. Connu avant le code : l'amical du 10/10 est « v3 amical » dans l'étude et hors des cinq lignes (écart attendu : 1). |
| V4 | Revue hebdomadaire, une ligne sous l'en-tête : « Version du moteur : ligue v4, amical v5 ; décisions ouvertes d'une version antérieure : n » (version en cours = ligne dont la période contient le jour de la revue ; décision ouverte = `learn.decision` BasketVibe au statut `proposed` ou `done`, sans `learn.outcome` ; version antérieure = décidée, en jour de Paris, avant le `start_date` le plus récent). Nouvelle ligne de version = clé `jeu/compétition/version/début` absente de l'instantané précédent ; alors une ligne liste les identifiants de ces décisions ouvertes, sans rien marquer. Instantané précédent sans clé de versions : aucune liste. Lecture seule. |
| V5 | Tests figés (`test_revue_hebdo.py`) : V4 présent et absent (ligne de version, liste après une nouvelle ligne, aucune liste sans nouvelle ligne) ; 197 tests du plan et 34 de la revue verts ; page réelle ≤ 60 lignes. |

**Résultats 6c (2026-11-09 17:40 Paris).**
- **V1** (`99bb125`, migration `core_026_engine_version` appliquée par le connecteur, fichier `sql/core/026_engine_version.sql`) : `select version, competition_kind, start_date, end_date, statut from core.engine_version order by start_date` → v3 ligue 2026-09-07 → 2026-10-26 déduit ; v4 amical 2026-10-11 → 2026-10-27 déduit ; v4 coupe 2026-10-28 → 2026-10-31 déduit ; v5 amical 2026-10-28 → (en cours) annoncé ; v4 ligue 2026-11-02 → (en cours) annoncé. Source de chaque ligne dans la colonne `source`.
- **V2** : `select competition_kind, version, statut, count(*) from gold.bv_match_engine_version group by 1,2,3` →
```
| amical | non attribuée |  | 1 |
| amical | v4 | déduit | 17 |
| amical | v5 | annoncé | 13 |
| coupe | non attribuée |  | 2 |
| coupe | v4 | déduit | 4 |
| ligue | v3 | déduit | 22 |
| ligue | v4 | annoncé | 3 |
```
  62 lignes = 62 matchs distincts = 62 matchs joués de `core.fixture` (aucun doublon). Non attribuées : coupe 13/09 (Blood Wolves, L), amical 10/10 (Isotopi&aAllies, W), coupe 01/11 (Reims Monarchs, L).
- **V3** (script de contrôle hors dépôt, `groupe()` importé, aucun script modifié) : `matchs contrôlés : 80 (dans la vue : 56, autres équipes par la table : 24)` ; `écarts : 1` → `| 2026-10-10 | friendly | 3373b15f | vue | non attribuée | v3 amical |`. 80 et non 78 : `select count(distinct fixture_id) from silver.bv_match_events` → 80 (2 matchs détaillés arrivés depuis l'étude). L'écart est celui annoncé avant le code (amical du 10/10 hors des cinq lignes). Pour l'annuler : une ligne « amical v3 jusqu'au 10/10, déduit (préanalyse § 1.1) » ; non insérée (hors de la liste de V1).
- **V4** (`0ff013e`) : page du 09/11, ligne 4 : « Version du moteur : ligue v4, amical v5 ; décisions ouvertes d'une version antérieure : 126 (avant le 02/11) ». Contrôle : `select count(*), count(*) filter (where (decided_at at time zone 'Europe/Paris')::date < '2026-11-02') … status in ('proposed','done') and not exists (learn.outcome)` → 132 ouvertes, 126 avant. Instantané du 09/11 : clé `versions` (5 clés) ; aucune liste aujourd'hui (pas d'instantané précédent avec versions).
- **V5** : `test_revue_hebdo.py` 34 → **38/38** (4 cas V4) ; `test_aujourdhui.py` **197/197** ; page **59 lignes**, 3,4 s.
- `fusion_main.py` : `commits à ajouter à main (3)` (f6ab108, 99bb125, 0ff013e) ; `Poussé : origin/main == HEAD.` (0ff013e). `fin_etape.py` : `commits d'avance sur origin/main : 0`, `git status --short : (propre)`, 23 suites vertes (dont revue 38/38, aujourdhui 197/197), `HEAD dans origin/main : oui`.

## Journal de durée (une ligne par exécution)

| Date | Jour du plan | Durée (s) | Requêtes |
|---|---|---|---|
| 2026-11-06 10:02 | aujourd'hui | 14.3 | 13 |
| 2026-11-06 10:02 | 2026-11-03 | 0.3 | 1 |
| 2026-11-06 10:02 | 2026-11-04 | 0.3 | 1 |
| 2026-11-06 10:02 | 2026-11-05 | 0.3 | 1 |
| 2026-11-06 10:02 | 2026-11-05 | 0.3 | 1 |
| 2026-11-06 10:29 | aujourd'hui | 30.0 | 13 |
| 2026-11-06 10:29 | aujourd'hui | 12.9 | 13 |
| 2026-11-06 14:45 | aujourd'hui | 17.6 | 13 |
| 2026-11-06 14:52 | aujourd'hui | 17.4 | 13 |
| 2026-11-06 15:18 | aujourd'hui | 13.4 | 12 |
| 2026-11-06 15:19 | aujourd'hui | 11.4 | 12 |
| 2026-11-06 15:19 | aujourd'hui | 11.1 | 12 |
| 2026-11-06 15:20 | aujourd'hui | 11.5 | 13 |
| 2026-11-06 15:30 | aujourd'hui | 13.7 | 14 |
| 2026-11-06 21:29 | hockeynation temps 1 (2026-11-06) | 16.9 | 8 |
| 2026-11-06 21:30 | hockeynation temps 2 (2026-11-06) | 18.1 | 8 |
| 2026-11-09 09:17 | aujourd'hui | 20.2 | 14 |
| 2026-11-09 10:35 | aujourd'hui | 14.4 | 14 |
| 2026-11-09 12:35 | aujourd'hui | 15.5 | 14 |
| 2026-11-09 12:38 | aujourd'hui | 19.2 | 18 |
| 2026-11-09 12:39 | aujourd'hui | 16.1 | 18 |
| 2026-11-09 15:34 | aujourd'hui | 19.8 | 18 |
| 2026-11-09 15:46 | aujourd'hui | 21.9 | 19 |
| 2026-11-09 15:54 | aujourd'hui | 22.2 | 19 |
| 2026-11-09 16:00 | aujourd'hui | 22.5 | 20 |
| 2026-11-09 16:05 | aujourd'hui | 23.0 | 20 |
| 2026-11-09 16:07 | aujourd'hui | 7.5 | 20 |
| 2026-11-09 16:10 | aujourd'hui | 7.6 | 25 |
| 2026-11-09 16:17 | aujourd'hui | 7.8 | 25 |
| 2026-11-09 16:21 | aujourd'hui | 9.6 | 27 |
| 2026-11-09 16:26 | aujourd'hui | 9.3 | 27 |
| 2026-11-09 16:32 | aujourd'hui | 11.1 | 28 |
| 2026-11-09 16:44 | aujourd'hui | 10.9 | 28 |
| 2026-11-09 16:47 | aujourd'hui | 9.8 | 30 |
| 2026-11-09 16:48 | aujourd'hui | 10.0 | 31 |
| 2026-11-09 16:57 | aujourd'hui | 10.2 | 31 |
