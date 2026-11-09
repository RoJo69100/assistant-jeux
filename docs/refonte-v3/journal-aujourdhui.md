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
