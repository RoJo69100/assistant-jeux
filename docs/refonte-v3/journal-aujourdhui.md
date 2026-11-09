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
