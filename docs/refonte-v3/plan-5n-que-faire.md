# Plan d'implémentation — étape 5n : le « que faire » BasketVibe bloc par bloc

> **Pour l'exécutant** : exécution dans la session, par l'auteur, sans sous-agents (demande de l'utilisateur, 10/11). Le skill `executing-plans` est retiré du dépôt (il dépend de `subagent-driven-development`, non installé) : on suit ce plan à la main. Les étapes se cochent (`- [ ]`). Avant de dire « terminé » : skill `verification-before-completion`. Une modification = un commit ; commit et push dans des appels séparés, sans `-q` ; fichiers écrits avec Write/Edit, jamais en heredoc ; fusion par `python -I pipelines/fusion_main.py` ; fin d'étape par `python -I pipelines/fin_etape.py`, sortie collée dans le journal.

**Objectif** : `python -I pipelines/aujourdhui.py basketvibe` produit le document de `docs/attentes/gabarit-que-faire-basketvibe.md`, bloc 0 à 10, sans heures (sauf le verrou), sans aucune commande donnée à l'utilisateur.

**Architecture** : `plan()` de `aujourdhui.py` garde tout le calcul. Un nouveau module `pipelines/que_faire_blocs.py` classe chaque action dans un bloc et rend les 11 blocs. `aujourdhui.rendre()` l'appelle. Les consignes destinées à Claude (lancer un agent, relancer l'étude) sortent de l'affichage et vont dans une liste « session » imprimée après un séparateur.

**Technique** : Python 3 (stdlib), `pipelines/sql.py` (lecture seule), tests en scripts `pipelines/test_*.py` (code 1 si un cas se trompe), contrôle de format par `pipelines/forme.py`.

**Conception** : `docs/refonte-v3/conception-5n-que-faire.md` (approuvée le 10/11). Fichiers lus par les exécutants : ce plan, la conception, le gabarit.

## Couverture du gabarit (chaque bloc cité ou reporté)

| Bloc | Tâche | Statut en 5n |
|---|---|---|
| 0 Exports d'abord | T5 | livré |
| 1 Aujourd'hui, puis demain | T2 | livré |
| 2 Composition de l'amical | T3 | livré |
| 3 Composition de la ligue ou de la coupe | T3 | livré |
| 4 Transferts (prix, qui acheter, qui vendre) | T4 | livré (conseils sur les recrues **reportés**) |
| 5 Les meilleurs et les failles | T6 | **reporté** : une ligne « reporté » |
| 6 Match Engine | T5 | livré |
| 7 Analyse détaillée | T6 | **étape suivante** : lignes actuelles rangées ici |
| 8 Économie | T6 | **étape suivante** : lignes actuelles rangées ici |
| 9 Académie, personnel, entraînement | T6 | **étape suivante** : lignes actuelles rangées ici |
| 10 À valider | T6 | livré |
| Réception sur la vraie journée | T8 | livré |

## Contraintes globales (valeurs reprises de la conception)

- Un bloc vide s'écrit exactement `donnée manquante : exporte <écran>` ; jamais « lance », « relance », « python », « pipelines/ », « exécute » dans le texte affiché à l'utilisateur.
- Pas d'heure `HH:MM` dans l'affichage, sauf l'heure limite du verrou dans la ligne de composition.
- Horizon = aujourd'hui : « Demain » liste ce qui se prépare aujourd'hui, jamais un report.
- Catégories du tableau de plan : celles de `forme.CATEGORIES` ; pastilles `🟥 URGENT`, `🟧 IMPORTANT`, `🟩 SUIVI`. Aucune ligne « rien à faire ».
- Compositions : format `tactique` (Joueur \| Poste \| Q1–Q4 \| Prol. \| Minutes \| Off. focus \| Rôle \| Tir \| Agress.) puis `adversaires` ; valeurs d'écran 1–5.
- Amical : jamais d'aperçu ni de fiche ; réglages repris du dernier amical, cinq de ligue à 0 minute, niveau du test en cours.
- Bloc 4 : « achetable » = prix actuel ≤ médiane de sa case (palier de note de 5 × tranche d'âge), case fiable, dans la capacité restante ; fenêtre d'enchère = 24 h ; une vente ou un achat reste une proposition (bloc 10).
- Étude du moteur : relancée après 3 défaites de suite en ligue ou en coupe, ou le dimanche.
- Durée du script : au plus 15 s (valeur actuelle) ; si dépassée, la mesure est inscrite et signalée, pas masquée.
- `forme.py` et `controle.py` : règles inchangées.

## Revue ciblée (cas que la conception suppose sans les tester)

1. **Aucune annonce ne finit dans les 24 h** (cas réel du 10/11 : 20 annonces ouvertes, aucune dans la fenêtre). Attendu : la phrase « aucune annonce du Marché ne se termine dans les 24 h (export du JJ/MM, n annonces) », pas un bloc vide ni « donnée manquante ». Test en T4.
2. **Aperçu adverse absent pour le match de ligue de demain** (cas réel du 11/11). Attendu : `donnée manquante : exporte l'aperçu du match de ligue du 11/11` dans les blocs 0 et 3, et aucune consigne d'agent affichée. Test en T3.
3. **Joueur proposé blessé, trop fatigué ou vendu à J-1.** Attendu : une ligne d'écart par joueur, nommée. Test en T3.
4. **Aucun amical aujourd'hui ni demain.** Attendu : le bloc 2 existe avec « aucun amical programmé aujourd'hui ni demain ». Test en T3.
5. **Vue illisible (clé dans `erreurs`).** Attendu : le bloc concerné dit `donnée manquante : vue <nom> illisible`, le script ne plante pas. Test en T6.

## Tâche 1 — Socle : règle du bloc vide, classement des actions

**Fichiers** : créer `pipelines/que_faire_blocs.py`, `pipelines/test_que_faire_blocs.py`.

**Produit** :
- `INTERDITS: re.Pattern` : mots interdits dans l'affichage (liste des contraintes globales).
- `manque(export: str, debloque: str = "") -> str` : `"donnée manquante : exporte <export>"` + `" (<debloque>)"` si fourni.
- `classer(action: str) -> tuple[int, str]` : (numéro de bloc, catégorie affichée) d'après le début du texte d'une action de `plan()`. Table explicite préfixe → (bloc, catégorie) couvrant chaque `ajoute(...)` de `aujourdhui.py` (lignes 413 à 1059 au 10/11) ; préfixe inconnu → `(10, "Question")`.
- `separer(actions: list) -> tuple[list, list[str]]` : actions affichables, et consignes de session (texte contenant « lance l'agent », « relance l'agent », « python -I »).

- [ ] **Étape 1 : tests d'abord** dans `test_que_faire_blocs.py` : `test_manque_format` (`manque("l'aperçu du match de ligue du 11/11")` == `"donnée manquante : exporte l'aperçu du match de ligue du 11/11"`) ; `test_interdits_attrape_python_et_lance` ; `test_interdits_laisse_etude_relancee` (« étude relancée le 09/11 » passe) ; `test_classer_couvre_chaque_ajoute` (lit `aujourdhui.py`, extrait chaque texte de premier argument f-string des appels `ajoute(`, vérifie qu'aucun ne tombe dans le défaut sauf liste blanche écrite dans le test) ; `test_separer_met_les_consignes_en_session`.
- [ ] **Étape 2** : `python pipelines/test_que_faire_blocs.py` → attendu : échec (module absent).
- [ ] **Étape 3** : implémenter les trois fonctions ci-dessus dans `que_faire_blocs.py`. Les catégories affichées viennent de `forme.CATEGORIES` (accents et majuscule restitués par une table de 9 entrées).
- [ ] **Étape 4** : relancer → attendu : tous les cas passent.
- [ ] **Étape 5** : commit « 5n T1 : socle des blocs du que faire (bloc vide, classement) ».

## Tâche 2 — Bloc 1 : aujourd'hui, puis demain

**Fichiers** : modifier `pipelines/que_faire_blocs.py`, `pipelines/test_que_faire_blocs.py`.

**Consomme** : `classer`, `separer` (T1) ; `plan()` → `{"actions": [(limite|None, prio, action, détail, source)], ...}`.
**Produit** : `bloc_1(actions: list, jour: dt.date) -> list[str]` : deux sections « Aujourd'hui » et « Demain (préparé aujourd'hui) », chacune en tableau `Priorité | Catégorie | Action` ; action = texte + détail sans `HH:MM` ; pastille selon `prio` (1 🟥 URGENT, 2 🟧 IMPORTANT, 3 🟩 SUIVI). Une action avec `limite` datée du lendemain va en « Demain » ; `limite` None ou du jour va en « Aujourd'hui » ; les actions des blocs 0, 2 à 10 n'y figurent pas (elles sont rendues dans leur bloc).

- [ ] **Étape 1 : tests** : `test_bloc_1_deux_sections` (une action datée J et une J+1 → chacune dans sa section) ; `test_bloc_1_sans_heure` (aucune sous-chaîne `\d\d:\d\d` dans la sortie) ; `test_bloc_1_passe_forme` (`forme.fautes_tableaux(texte, "basketvibe") == []`) ; `test_bloc_1_pas_de_ligne_vide` (section sans action : la section est omise, pas « rien à faire »).
- [ ] **Étape 2** : lancer → échec.
- [ ] **Étape 3** : implémenter `bloc_1`.
- [ ] **Étape 4** : lancer → succès.
- [ ] **Étape 5** : commit « 5n T2 : bloc 1, aujourd'hui puis demain, sans heures ».

## Tâche 3 — Blocs 2 et 3 : compositions

**Fichiers** : modifier `pipelines/que_faire_blocs.py`, `pipelines/composition.py` (ajout d'une entrée sans fiche pour l'amical), tests des deux.

**Consomme** : `composition.composer`, `aujourdhui.prochain_amical`, `aujourdhui.test_en_cours`, requêtes `apercus_matchs`, `fatigue_avant_match`, `gold.bv_daily_alerts`, `transferts_recents`.
**Produit** :
- `composition.composer_amical(donnees_saisie: list[dict], test) -> str` : tableau `tactique` bâti sur le dernier amical joué (`gold.bv_saisie_joueurs`, `kind = 'amical'`, cinq de ligue à 0 minute), agressivité, zone et focus du test en cours ; ne lit ni fiche ni aperçu.
- `bloc_2(donnees, S, jour, maintenant) -> list[str]` : tableau + zone + focus + test nommé + heure limite du verrou ; sinon « aucun amical programmé aujourd'hui ni demain ».
- `bloc_3(donnees, S, jour, maintenant) -> tuple[list[str], list[str]]` : (lignes affichées, consignes de session). Aperçu en base et pas de fiche à jour → consigne de session « lancer l'agent tactique … » et ligne affichée « composition en préparation » (jamais la consigne elle-même) ; aperçu absent → `manque("l'aperçu du match de ligue du JJ/MM")`. Fiche à jour → tableaux `tactique` + `adversaires` puis la vérification J-1 : une ligne par joueur du tableau présent dans les alertes de blessure/fatigue/forme, dans `fatigue_avant_match`, ou vendu depuis (transferts où `achete` est faux).

- [ ] **Étape 1 : tests** : `test_amical_sans_fiche_ni_apercu` ; `test_amical_applique_le_niveau_du_test` (agress de l'écran = cran + 1) ; `test_aucun_amical` (phrase exacte de la revue ciblée 4) ; `test_ligue_apercu_absent` (phrase exacte de la revue ciblée 2, et `INTERDITS` absent) ; `test_ligue_apercu_sans_fiche_met_la_consigne_en_session` ; `test_j_moins_1_signale_blesse_fatigue_vendu` (revue ciblée 3, un joueur par motif) ; `test_blocs_2_3_passent_forme`.
- [ ] **Étape 2** : lancer → échec.
- [ ] **Étape 3** : implémenter `composer_amical`, `bloc_2`, `bloc_3`.
- [ ] **Étape 4** : lancer ces tests et `python pipelines/test_composition.py` → succès (les 3 cas de composition existants restent verts).
- [ ] **Étape 5** : commit « 5n T3 : blocs 2 et 3, compositions amical et ligue, vérification J-1 ».

## Tâche 4 — Bloc 4 : prix, qui acheter, qui vendre

**Fichiers** : modifier `pipelines/aujourdhui.py` (`REQUETES`), `pipelines/que_faire_blocs.py`, tests.

**Requêtes ajoutées à `REQUETES`** : `prix_cases` (`gold.bv_price_ref_ps`, toutes les cases) ; `annonces_24h` (`gold.bv_market_candidates` dont `ends_paris` est dans les 24 h, dédupliquées par `auction_id`, avec `ref_n` et `ref_median_age_pos` — la médiane de la case est jointe depuis `prix_cases` dans le module) ; `vendre` (jointure `gold.bv_sell_candidates` / `gold.bv_sell_replacement` sur `player_id` : poste, âge, note, salaire, rang au poste, minutes des 4 derniers matchs, remplaçant, écart, joueurs disponibles).
**Produit** : `bloc_4(donnees, erreurs, capacite: int | None, tolerance: float | None) -> list[str]` : (1) table des prix, 3 colonnes de prix par case ; (2) annonces des 24 h avec colonnes Nom \| Poste \| Âge \| Note \| Prix actuel \| Médiane de la case \| Plafond \| Fin \| Gain pour mon cinq \| Achetable ; (3) qui vendre avec le verdict « vendable » / « nécessaire (<raison>) » (règle de la conception) ; puis les lignes d'enchères en cours existantes.

- [ ] **Étape 1 : tests** : `test_table_prix_une_ligne_par_case` ; `test_achetable_sous_la_mediane` (prix ≤ médiane, case fiable, ≤ capacité → oui ; au-dessus de la médiane → non ; case non fiable → non) ; `test_aucune_annonce_24h` (phrase exacte de la revue ciblée 1) ; `test_deduplication_des_pages` (même `auction_id` sur deux captures = une ligne) ; `test_vendre_vendable_et_necessaire` (écart ≤ tolérance et 9 disponibles → vendable ; écart > tolérance ou 8 disponibles → nécessaire avec la raison) ; `test_bloc_4_sans_commande`.
- [ ] **Étape 2** : lancer → échec.
- [ ] **Étape 3** : ajouter les 3 requêtes et implémenter `bloc_4`. Le seuil des 9 joueurs reste `DISPONIBLES_APRES_VENTE` de `aujourdhui.py`.
- [ ] **Étape 4** : lancer → succès ; `python -I pipelines/sql.py` sur chacune des 3 requêtes du vrai jeu : sortie non vide pour `prix_cases` et `vendre`, collée dans le journal.
- [ ] **Étape 5** : commit « 5n T4 : bloc 4, table des prix, achats et ventes ».

## Tâche 5 — Blocs 0 et 6 : exports et Match Engine

**Fichiers** : modifier `pipelines/aujourdhui.py` (`REQUETES`), `pipelines/que_faire_blocs.py`, tests.

**Requêtes ajoutées** : `captures_marche` (nombre de captures et d'annonces du Marché vues depuis 24 h, `core.market_listing`) ; `matchs_ajoutes` (matchs en base par type, ajoutés depuis la veille et total) ; `defaites_suite` (déjà fournie par `objectifs.defaites_d_affilee` : réutilisée, pas de nouvelle requête).
**Produit** :
- `bloc_0(donnees, res, jour, maintenant) -> list[str]` : une ligne par export à refaire, avec « → bloc N » ; par match : aperçu absent → `manque(...)` ; Marché : « n captures, m annonces » (la valeur est affichée, aucun seuil n'est inventé).
- `etude_a_relancer(defaites_d_affilee: int, jour: dt.date, derniere_etude: dt.date | None) -> bool` : vrai si `defaites_d_affilee >= 3`, ou si `jour` est un dimanche et que la dernière étude a plus de 6 jours.
- `bloc_6(donnees, jour, derniere_etude) -> tuple[list[str], list[str]]` : ligne « matchs ajoutés depuis hier : n (ligue a, amical b), total en base N, étude relancée le JJ/MM » ; avancement des expériences et prochaine hypothèse (`aujourdhui.verifier`, `texte_avancement`) ; consigne de session « relancer l'étude » quand `etude_a_relancer`. Date de la dernière étude = date du dernier commit qui touche `docs/refonte-v3/etude-evenements-basketvibe-sortie.md` (`git log -1 --format=%cs`).

- [ ] **Étape 1 : tests** : `test_etude_a_relancer_trois_defaites` ; `test_etude_a_relancer_dimanche` ; `test_etude_pas_relancee_un_mardi_sans_defaites` ; `test_bloc_0_cite_le_bloc_debloque` ; `test_bloc_0_apercu_absent_par_match` ; `test_bloc_6_ligne_quotidienne` (format exact de la ligne) ; `test_bloc_6_consigne_session`.
- [ ] **Étape 2** : lancer → échec.
- [ ] **Étape 3** : ajouter les 2 requêtes, implémenter `bloc_0`, `etude_a_relancer`, `bloc_6`.
- [ ] **Étape 4** : lancer → succès.
- [ ] **Étape 5** : commit « 5n T5 : blocs 0 et 6, exports par match et ligne Match Engine ».

## Tâche 6 — Blocs 5, 7, 8, 9, 10 et assemblage

**Fichiers** : modifier `pipelines/que_faire_blocs.py`, tests.

**Produit** :
- `bloc_5() -> list[str]` : `["reporté : l'étude des meilleurs et des failles est prévue après l'étape suivante"]`.
- `bloc_7`, `bloc_8`, `bloc_9(actions) -> list[str]` : lignes de `plan()` classées dans ces blocs par `classer`, inchangées ; bloc vide → `manque(...)` avec l'export concerné (match, Finances, Académie/Personnel/Entraînement).
- `bloc_10(actions, garder: list[str]) -> list[str]` : propositions d'achat, de vente et d'enchère à valider par écrit, puis les règles « à valider » de `garder`.
- `rendre_blocs(res, donnees, erreurs, jour, maintenant, S) -> tuple[str, list[str]]` : concatène « Bloc 0 … Bloc 10 » dans l'ordre, chaque bloc avec son titre ; clé de `erreurs` d'un bloc → `donnée manquante : vue <nom> illisible` dans ce bloc (revue ciblée 5) ; renvoie aussi la liste des consignes de session.

- [ ] **Étape 1 : tests** : `test_onze_blocs_dans_l_ordre` ; `test_aucun_bloc_absent` (données minimales : chaque titre « Bloc 0 » à « Bloc 10 » présent) ; `test_vue_illisible_ne_plante_pas` (revue ciblée 5) ; `test_aucun_mot_interdit_dans_tout_le_rendu` (`INTERDITS` absent du texte complet) ; `test_rendu_passe_forme_et_controle` (`forme.fautes_de(texte, "basketvibe") == []`).
- [ ] **Étape 2** : lancer → échec.
- [ ] **Étape 3** : implémenter les fonctions ci-dessus.
- [ ] **Étape 4** : lancer → succès.
- [ ] **Étape 5** : commit « 5n T6 : blocs 5, 7 à 10 et assemblage des onze blocs ».

## Tâche 7 — Branchement, anciens tests, skill

**Fichiers** : modifier `pipelines/aujourdhui.py` (`rendre`, `main`), `pipelines/test_aujourdhui.py`, `.claude/skills/basketvibe-aujourdhui/SKILL.md`.

- [ ] **Étape 1** : `aujourdhui.rendre()` appelle `que_faire_blocs.rendre_blocs`, imprime le rendu, puis un séparateur `--- session (à exécuter, ne pas afficher) ---` et les consignes ; l'instantané `aujourdhui-AAAA-MM-JJ.md` contient le rendu sans les consignes.
- [ ] **Étape 2** : lancer `python pipelines/test_aujourdhui.py` ; les cas qui figeaient la forme de 8 lignes (par exemple autour de `auj.rendre(...)`, ligne 142) et les cas Y2/Y3 qui attendent « lance l'agent tactique » / « python -I pipelines/composition.py » (autour de la ligne 679) échouent : pour chacun, réécrire le test selon le nouveau format et écrire une ligne dans la table des tests réécrits du journal (ancien attendu, nouvel attendu, raison : bloc 3 et règle « jamais une commande »).
- [ ] **Étape 3** : réécrire `SKILL.md` de `basketvibe-aujourdhui` : première action = le script ; afficher le rendu **avant** le séparateur tel quel ; exécuter les consignes de session après le séparateur (agents, étude) puis relancer le script une fois ; demander à l'utilisateur les exports signalés « donnée manquante » ; supprimer « au plus 8 lignes `HH:MM` ».
- [ ] **Étape 4** : lancer `python pipelines/test_aujourdhui.py`, `python pipelines/test_composition.py`, `python pipelines/test_que_faire_blocs.py`, `python pipelines/test_forme.py` → tous verts, comptes collés.
- [ ] **Étape 5** : commit « 5n T7 : branchement du rendu en blocs, tests réécrits, skill du que faire ».

## Tâche 8 — Réception sur la vraie journée

**Fichiers** : modifier `docs/refonte-v3/journal-aujourdhui.md`.

- [ ] **Étape 1** : exécuter `python -I pipelines/aujourdhui.py basketvibe` sur la journée réelle ; coller la sortie telle quelle dans le journal ; noter la durée (comparer aux 15 s).
- [ ] **Étape 2** : tableau `Bloc | Attendu (gabarit) | Produit | Écart` : une ligne par bloc de 0 à 10 (les blocs 5, 7, 8, 9 marqués reportés ou rangés), chaque écart nommé.
- [ ] **Étape 3** : vérifier à la main trois critères : aucun mot de `INTERDITS` dans le rendu, aucun bloc absent, `forme.py` et `controle.py` passent. Un critère raté = un correctif et un nouveau commit, pas une réécriture du tableau.
- [ ] **Étape 4** : `python -I pipelines/fusion_main.py` puis `python -I pipelines/fin_etape.py` ; coller les deux sorties dans le journal ; commit « 5n T8 : réception, comparaison bloc par bloc ».

## Auto-relecture

- **Couverture de la conception** : blocs 0 à 10 → tableau de couverture ; Q1 → T3 ; Q2 → T5 ; Q3 et « qui vendre » → T4 ; réception → T8 ; skill → T7.
- **Cohérence des noms** : `manque`, `classer`, `separer`, `bloc_0` à `bloc_10`, `rendre_blocs`, `etude_a_relancer`, `composer_amical` sont définis dans la tâche qui les produit et utilisés ensuite avec la même signature.
- **Proportion** : la conception fait ~100 lignes, ce plan ~150 ; aucune fonction n'est écrite en entier.
- **Hors plan, à signaler à l'utilisateur** : le nombre de pages du Marché n'a pas de seuil connu (le bloc 0 affiche le compte sans conclure) ; les conseils sur les recrues sont reportés ; la durée de l'étude n'est pas mesurée avant T5.
