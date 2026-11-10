# Plan d'implémentation — étape 5n : le « que faire » BasketVibe bloc par bloc

> **Pour l'exécutant** : exécution dans la session, par l'auteur, sans sous-agents (demande de l'utilisateur, 10/11). Le skill `executing-plans` est retiré du dépôt (il dépend de `subagent-driven-development`, non installé) : on suit ce plan à la main. Les étapes se cochent (`- [ ]`). Avant de dire « terminé » : skill `verification-before-completion`. Une modification = un commit ; commit et push dans des appels séparés, sans `-q` ; fichiers écrits avec Write/Edit, jamais en heredoc ; fusion par `python -I pipelines/fusion_main.py` ; fin d'étape par `python -I pipelines/fin_etape.py`, sortie collée dans le journal.

**Objectif** : `python -I pipelines/aujourdhui.py basketvibe` produit le document de `docs/attentes/gabarit-que-faire-basketvibe.md`, bloc 0 à 10, sans heures (sauf le verrou), sans aucune commande donnée à l'utilisateur.

**Architecture** : `plan()` de `aujourdhui.py` garde tout le calcul. Un nouveau module `pipelines/que_faire_blocs.py` classe chaque action dans un bloc et rend les 11 blocs. `aujourdhui.rendre()` l'appelle. Les consignes destinées à Claude (lancer un agent, lancer l'agent data-scientist) sortent de l'affichage et vont dans une liste « session » imprimée après un séparateur.

**Technique** : Python 3 (stdlib), `pipelines/sql.py` (lecture seule), tests en scripts `pipelines/test_*.py` (code 1 si un cas se trompe), contrôle de format par `pipelines/forme.py`.

**Conception** : `docs/refonte-v3/conception-5n-que-faire.md` (approuvée le 10/11, corrigée le 10/11 après-midi). Fichiers lus par les exécutants : ce plan, la conception, le gabarit, `.claude/agents/data-scientist.md` (non modifié par ce plan).

## Couverture du gabarit (chaque bloc cité ou reporté)

| Bloc | Tâche | Statut en 5n |
|---|---|---|
| 0 Exports d'abord | T5 | livré (exports par match, exports hebdomadaires de l'étude, demandes reprises des études) |
| 1 Aujourd'hui, puis demain | T2 | livré (toutes les actions, chacune avec « → bloc N ») |
| 2 Composition de l'amical | T3 | livré (brief du jour de l'agent tactique, vérification J-1) |
| 3 Composition de la ligue ou de la coupe | T3 | livré (vérification J-1) |
| 4 Transferts (prix, qui acheter, qui vendre) | T4 | livré (conseils sur les recrues **reportés**) |
| 5 Les meilleurs et les failles | T6 | livré : état de l'étude lu dans `docs/etudes/` (contenu de l'étude : étape 5o) |
| 6 Match Engine | T5 | livré |
| 7 Analyse détaillée | T6 | livré : ligne d'état de l'analyse, puis lignes actuelles rangées ici |
| 8 Économie | T6 | livré : état de l'étude, puis lignes actuelles rangées ici (contenu : 5o) |
| 9 Académie, personnel, entraînement | T6 | livré : état de l'étude, puis lignes actuelles rangées ici (contenu : 5o) |
| 10 À valider | T6 | livré |
| Réception sur la vraie journée | T8 | livré |

## Contraintes globales (valeurs reprises de la conception)

- Un bloc vide s'écrit exactement `donnée manquante : exporte <écran>`. Aucune commande dans le texte affiché : `INTERDITS` attrape les mots entiers « lance », « relance », « exécute », « lancer », « relancer », « exécuter », « python » et la chaîne « pipelines/ » ; un participe (« lancée dans ce passage ») n'est pas une commande et passe.
- Pas d'heure `HH:MM` dans l'affichage, sauf l'heure limite du verrou dans la ligne de composition.
- Horizon = aujourd'hui : « Demain » liste ce qui se prépare aujourd'hui, jamais un report.
- Catégories du tableau de plan : celles de `forme.CATEGORIES` ; pastilles `🟥 URGENT`, `🟧 IMPORTANT`, `🟩 SUIVI`. Aucune ligne « rien à faire ».
- Compositions : format `tactique` (Joueur \| Poste \| Q1–Q4 \| Prol. \| Minutes \| Off. focus \| Rôle \| Tir \| Agress.) puis `adversaires` ; valeurs d'écran 1–5.
- Amical : règle écrite de la fiche tactique §2 bis (`docs/fiches/basketvibe/tactique.md`, l. 60-63), dans l'ordre : (1) minutes aux jeunes de 21 ans ou moins ; (2) un seul réglage testé à la fois (expériences E1 à E5 de `docs/attentes/experiences-amicales-basketvibe.yaml`) ; (3) titulaires de la ligue protégés les jours de ligue (amical le matin, ligue le soir), fatigue ajoutée calculée en SQL par la formule de §2 bis. Minutes réparties entre les joueurs (en v5 amical, un joueur porte 133 des 423 tirs à 3 points, soit 31 % : `docs/etudes/2026-11-10-trois-points-competence.md`). **Jamais reprise du dernier amical ni du dernier brief** : choix du jour par l'agent tactique à partir des données du jour, chiffres cités, hypothèses signalées ; le script ne fait que rendre le brief du jour ; la composition est enregistrée avec ses minutes pour l'étude.
- Blessures en amical : la sortie n'écrit jamais « pas de blessure » ni « sans blessure » pour un amical (contradiction du dépôt, voir « Hors plan »).
- Bloc 4 : « achetable » = prix actuel ≤ médiane de sa case (palier de note de 5 × tranche d'âge), case fiable, dans la capacité restante ; fenêtre d'enchère = 24 h ; une vente ou un achat reste une proposition (bloc 10).
- Étude du moteur : 3 défaites de suite en ligue ou en coupe, ou le dimanche, et dans les deux cas au moins un match en base joué après la dernière étude ; consigne de session « lancer l'agent data-scientist sur la question ouverte », avec dans la consigne « ne demande un export que pour les groupes de moteur encore ouverts (v4 ligue, v5 amical) » ; 1 lancement par jour au plus. L'ancien script `etude_evenements_basketvibe.py` n'est plus lancé par le que faire.
- Études lues par le que faire : fichiers `docs/etudes/AAAA-MM-JJ-<sujet>.md` ; un fichier dont l'en-tête dit « invalidé » est ignoré ; « la plus récente par question » = le fichier de date la plus récente pour un même `<sujet>`. Date de dernière étude = date du dernier de ces fichiers (jamais `git log`).
- Bloc 6 : jamais « appris », jamais « relancée le ».
- Durée du script : au plus 15 s (valeur actuelle) ; si dépassée, la mesure est inscrite et signalée, pas masquée.
- `forme.py` et `controle.py` : règles inchangées.

## Revue ciblée (cas que la conception suppose sans les tester)

1. **Aucune annonce ne finit dans les 24 h** (cas réel du 10/11 : 20 annonces ouvertes, aucune dans la fenêtre). Attendu : la phrase « aucune annonce du Marché ne se termine dans les 24 h (export du JJ/MM, n annonces) », pas un bloc vide ni « donnée manquante ». Test en T4.
2. **Aperçu adverse absent pour le match de ligue de demain** (cas réel du 11/11). Attendu : `donnée manquante : exporte l'aperçu du match de ligue du 11/11` dans les blocs 0 et 3, et aucune consigne d'agent affichée. Test en T3.
3. **Joueur proposé blessé, trop fatigué ou vendu à J-1**, dans la composition de l'amical comme dans celle de la ligue. Attendu : une ligne d'écart par joueur, nommée, dans le bloc concerné. Test en T3.
4. **Aucun amical aujourd'hui ni demain.** Attendu : le bloc 2 existe avec « aucun amical programmé aujourd'hui ni demain ». Test en T3.
5. **Vue illisible (clé dans `erreurs`).** Attendu : le bloc concerné dit `donnée manquante : vue <nom> illisible`, le script ne plante pas. Test en T6.
6. **Étude invalidée la plus récente** (cas réel : `2026-11-10-tirs-cercle-deux-points-v4-amical.md`, en-tête « T1 invalidé »). Attendu : ignorée pour la date de dernière étude et pour les demandes d'export. Test en T5.

## Tâche 1 — Socle : règle du bloc vide, classement des actions

**Fichiers** : créer `pipelines/que_faire_blocs.py`, `pipelines/test_que_faire_blocs.py`.

**Produit** :
- `INTERDITS: re.Pattern` : mots entiers interdits dans l'affichage (liste des contraintes globales).
- `manque(export: str, debloque: str = "") -> str` : `"donnée manquante : exporte <export>"` + `" (<debloque>)"` si fourni.
- `classer(action: str) -> tuple[int, str]` : (numéro de bloc, catégorie affichée) d'après le début du texte d'une action de `plan()`. Table explicite préfixe → (bloc, catégorie) couvrant chaque `ajoute(...)` de `aujourdhui.py` (lignes 413 à 1059 au 10/11) ; préfixe inconnu → `(10, "Question")`.
- `separer(actions: list) -> tuple[list, list[str]]` : actions affichables, et consignes de session (texte contenant « lance l'agent », « relance l'agent », « lancer l'agent », « relancer l'agent », « python -I »).

- [ ] **Étape 1 : tests d'abord** dans `test_que_faire_blocs.py` : `test_manque_format` (`manque("l'aperçu du match de ligue du 11/11")` == `"donnée manquante : exporte l'aperçu du match de ligue du 11/11"`) ; `test_interdits_attrape_python_et_lance` ; `test_interdits_attrape_les_infinitifs` (« lancer », « relancer », « exécuter », mots entiers, sont attrapés) ; `test_interdits_laisse_lancee_dans_ce_passage` (« analyse non faite, lancée dans ce passage » et « étude à jour au 09/11 » passent) ; `test_classer_couvre_chaque_ajoute` (lit `aujourdhui.py`, extrait chaque texte de premier argument f-string des appels `ajoute(`, vérifie qu'aucun ne tombe dans le défaut sauf liste blanche écrite dans le test) ; `test_separer_met_les_consignes_en_session`.
- [ ] **Étape 2** : `python pipelines/test_que_faire_blocs.py` → attendu : échec (module absent).
- [ ] **Étape 3** : implémenter les trois fonctions ci-dessus dans `que_faire_blocs.py`. Les catégories affichées viennent de `forme.CATEGORIES` (accents et majuscule restitués par une table de 9 entrées).
- [ ] **Étape 4** : relancer → attendu : tous les cas passent.
- [ ] **Étape 5** : commit « 5n T1 : socle des blocs du que faire (bloc vide, classement) ».

## Tâche 2 — Bloc 1 : aujourd'hui, puis demain

**Fichiers** : modifier `pipelines/que_faire_blocs.py`, `pipelines/test_que_faire_blocs.py`.

**Consomme** : `classer`, `separer` (T1) ; `plan()` → `{"actions": [(limite|None, prio, action, détail, source)], ...}`.
**Produit** : `bloc_1(actions: list, jour: dt.date) -> list[str]` : deux sections « Aujourd'hui » et « Demain (préparé aujourd'hui) », chacune en tableau `Priorité | Catégorie | Action` ; action = texte court + `→ bloc N` (N = bloc de `classer`), sans `HH:MM` ; pastille selon `prio` (1 🟥 URGENT, 2 🟧 IMPORTANT, 3 🟩 SUIVI). **Toutes** les actions affichables y figurent, y compris celles des blocs 0 et 2 à 10 (le détail reste dans leur bloc ; le bloc 1 est le sommaire). Une action avec `limite` datée du lendemain va en « Demain » ; `limite` None ou du jour va en « Aujourd'hui ». Le bloc 1 n'est jamais vide : sans aucune action affichable, une ligne `🟩 SUIVI | Analyse | aucune action ouverte, détail des blocs 0 à 10 ci-dessous → bloc 0`.

- [ ] **Étape 1 : tests** : `test_bloc_1_deux_sections` (une action datée J et une J+1 → chacune dans sa section) ; `test_bloc_1_liste_toutes_les_actions` (une action de chaque bloc 0, 2 à 10 → toutes présentes, chacune avec son `→ bloc N` exact) ; `test_bloc_1_jamais_vide` (aucune action → la ligne de sommaire ci-dessus) ; `test_bloc_1_sans_heure` (aucune sous-chaîne `\d\d:\d\d` dans la sortie) ; `test_bloc_1_passe_forme` (`forme.fautes_tableaux(texte, "basketvibe") == []`) ; `test_bloc_1_section_vide_omise` (aucune action pour demain : la section « Demain » est omise, pas « rien à faire »).
- [ ] **Étape 2** : lancer → échec.
- [ ] **Étape 3** : implémenter `bloc_1`.
- [ ] **Étape 4** : lancer → succès.
- [ ] **Étape 5** : commit « 5n T2 : bloc 1, toutes les actions avec leur bloc, sans heures ».

## Tâche 3 — Blocs 2 et 3 : compositions

**Fichiers** : modifier `pipelines/que_faire_blocs.py`, `pipelines/aujourdhui.py` (`REQUETES`), `pipelines/composition.py` (lecture du brief du jour pour l'amical), `docs/decisions/cartes/basketvibe/composition.md` (ligne 56), `docs/fiches/basketvibe/tactique.md` (l. 64), `docs/fiches/basketvibe/resume.md` (l. 15), tests.

**Fiche à jour (bloc 3)** : brief tactique daté du jour **et** produit après l'aperçu adverse en base et après le dernier export de l'équipe. La fiche d'hier n'est jamais à jour : à sa place, consigne de session.

**Consomme** : `composition.composer`, `aujourdhui.prochain_amical`, `aujourdhui.test_en_cours`, requêtes `apercus_matchs`, `fatigue_avant_match`, `gold.bv_daily_alerts`, `transferts_recents`.
**Requête ajoutée** : `fatigue_amical` : pour chaque titulaire de ligue, fatigue ajoutée par l'amical du matin selon la formule de §2 bis (minutes × 0,019 × multiplicateur d'agressivité × (1,5 − 0,008 × endurance)), seulement un jour de ligue.
**Produit** :
- `composition.composer_amical(brief_du_jour: Path | None, test) -> str | None` : tableau `tactique` lu dans le brief tactique **daté du jour** pour cet amical (minutes par joueur, réglage E testé) ; `None` si aucun brief du jour. Ne lit jamais le dernier amical joué ni un brief d'un autre jour.
- `verifier_j_moins_1(tableau, donnees) -> list[str]` : une ligne par joueur du tableau présent dans les alertes de blessure/fatigue/forme, dans `fatigue_avant_match`, ou vendu depuis (transferts où `achete` est faux). Commune aux blocs 2 et 3.
- `bloc_2(donnees, S, jour, maintenant) -> tuple[list[str], list[str]]` : (lignes affichées, consignes de session). Brief du jour présent → tableau + zone + focus + réglage testé nommé (un seul) + heure limite du verrou + fatigue ajoutée des titulaires un jour de ligue + `verifier_j_moins_1`. Brief du jour absent → ligne affichée « composition de l'amical en préparation » et consigne de session « lancer l'agent tactique (BasketVibe, amical du JJ/MM, horizon aujourd'hui) : composition de l'amical selon la fiche tactique §2 bis, dans l'ordre jeunes ≤ 21 ans, un seul réglage (E du test en cours), titulaires protégés si ligue le soir (fatigue ajoutée de `fatigue_amical`) ; minutes réparties entre les joueurs ; chiffres cités, hypothèses signalées ; jamais reprise du dernier amical ni du dernier brief ; minutes par joueur dans le tableau ». Aucun amical → « aucun amical programmé aujourd'hui ni demain ».
- `bloc_3(donnees, S, jour, maintenant) -> tuple[list[str], list[str]]` : (lignes affichées, consignes de session). Aperçu en base et pas de fiche à jour (définition ci-dessus) → consigne de session « lancer l'agent tactique … » et ligne affichée « composition en préparation » (jamais la consigne elle-même) ; aperçu absent → `manque("l'aperçu du match de ligue du JJ/MM")`. Fiche à jour → tableaux `tactique` + `adversaires` puis `verifier_j_moins_1`.
- Enregistrement pour l'étude : le brief du jour de l'amical reste dans `outputs/basketvibe/` avec les minutes prévues par joueur et le réglage testé ; l'étude les compare aux minutes jouées (`gold.bv_match_player_lines`).

- [ ] **Étape 1 : tests** : `test_amical_rend_le_brief_du_jour` ; `test_amical_jamais_le_dernier_amical` (brief d'hier présent, aucun du jour → pas de tableau, consigne de session, ligne « en préparation ») ; `test_amical_consigne_cite_la_regle` (consigne contient « 21 ans », « un seul réglage », « titulaires protégés », « minutes réparties ») ; `test_amical_fatigue_ajoutee_jour_de_ligue` (affichée un jour de ligue, absente sinon) ; `test_amical_jamais_pas_de_blessure` (ni « pas de blessure » ni « sans blessure » dans le bloc 2) ; `test_aucun_amical` (phrase exacte de la revue ciblée 4) ; `test_ligue_apercu_absent` (phrase exacte de la revue ciblée 2, et `INTERDITS` absent) ; `test_ligue_apercu_sans_fiche_met_la_consigne_en_session` ; `test_ligue_fiche_d_hier_pas_a_jour` (brief tactique d'hier présent, aucun du jour : pas de tableau, consigne de session, ligne « composition en préparation ») ; `test_j_moins_1_signale_blesse_fatigue_vendu` (revue ciblée 3, un joueur par motif, **pour le bloc 2 et pour le bloc 3**) ; `test_blocs_2_3_passent_forme`.
- [ ] **Étape 2** : lancer → échec.
- [ ] **Étape 3** : ajouter `fatigue_amical`, implémenter `composer_amical`, `verifier_j_moins_1`, `bloc_2`, `bloc_3`.
- [ ] **Étape 4** : lancer ces tests et `python pipelines/test_composition.py` → succès (les 3 cas de composition existants restent verts).
- [ ] **Étape 5** : remplacer la ligne 56 de `docs/decisions/cartes/basketvibe/composition.md` par : « Composition de **test** choisie le jour même par l'agent tactique à partir des données du jour, chiffres cités et hypothèses signalées, selon la fiche tactique §2 bis, dans l'ordre : minutes aux jeunes de 21 ans ou moins ; un seul réglage testé à la fois (E1 à E5) ; titulaires de la ligue protégés les jours de ligue, fatigue ajoutée calculée en SQL ; minutes réparties entre les joueurs. Jamais reprise du dernier amical ni du dernier brief. Pas de preset. Aucun export d'aperçu à demander. »
- [ ] **Étape 6** : commit « 5n T3 : blocs 2 et 3, amical au brief du jour, vérification J-1 des deux compositions ».
- [ ] **Étape 7** : `docs/fiches/basketvibe/tactique.md` l. 64 : garder « aucun preset sauvegardé » pour l'amical (le preset « Friendly » existant reste intact) ; retirer « ni fiche de saisie d'amical » et « On analyse seulement le résultat d'un amical exporté (agent Match) » ; écrire à la place : « La composition du jour de l'amical (tableau poste par poste) est produite chaque jour par l'agent tactique, choisie à l'instant T, jamais reprise du dernier amical ni du dernier brief ; de même pour la ligue et la coupe. » Commit « 5n T3 : fiche tactique, composition de l'amical choisie chaque jour ».
- [ ] **Étape 8** : `docs/fiches/basketvibe/resume.md` l. 15 : « réglages repris du dernier amical » devient « choix du jour ». Commit « 5n T3 : résumé, réglages de l'amical choisis le jour même ».

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

**Requêtes ajoutées** : `captures_marche` (nombre de captures et d'annonces du Marché vues depuis 24 h, `core.market_listing`) ; `matchs_ajoutes` (matchs en base par type : ajoutés depuis la veille, total, et nombre joués après une date donnée) ; `defaites_suite` (déjà fournie par `objectifs.defaites_d_affilee` : réutilisée, pas de nouvelle requête).
**Produit** :
- `lire_etudes(dossier=Path("docs/etudes")) -> list[dict]` : un dict par fichier `AAAA-MM-JJ-<sujet>.md` non invalidé (`date`, `sujet`, verdicts du tableau, intervalle du premier résultat qui en a un, demandes d'export) ; garde le plus récent par `sujet`. Les demandes d'export sont les lignes qui commencent exactement par « Pour comprendre le Match Engine, j'ai besoin de : », recopiées telles quelles ; le script n'en écrit aucune.
- `bloc_0(donnees, res, etudes, jour, maintenant) -> list[str]` : une ligne par export à refaire, avec « → bloc N » ; par match : aperçu absent → `manque(...)` ; Marché : « n captures, m annonces » (la valeur est affichée, aucun seuil n'est inventé) ; exports hebdomadaires pour l'étude : onglets Équipes, Joueurs, Blessés et Transferts de la saison courante, pages `/c/<club>` → blocs 5 et 6 ; puis les demandes d'export de `etudes`, chacune suivie de « (étude du JJ/MM) » → bloc 6.
- `etude_a_lancer(defaites_d_affilee: int, jour: dt.date, derniere_etude: dt.date | None, k: int) -> bool` : vrai si (`defaites_d_affilee >= 3` et k >= 1 (au moins un match en base joué après la dernière étude), ou `jour` est un dimanche, la dernière étude a plus de 6 jours et k >= 1 (au moins un match en base joué après la dernière étude)) **et** aucune étude n'est datée de `jour` (1 lancement par jour au plus). k = celui de la ligne du bloc 6 (`matchs_ajoutes`).
- `bloc_6(donnees, etudes, jour) -> tuple[list[str], list[str]]` : ligne exacte `matchs ajoutés : n (ligue a, amical b) · N en base · étude à jour au JJ/MM, k pas encore étudiés` (JJ/MM = date de la dernière étude ; k = matchs en base joués après cette date ; sans étude : `aucune étude encore, N pas encore étudiés`) ; les demandes d'export des études (même texte qu'au bloc 0, avec leur date) ; avancement des expériences et prochaine hypothèse (`aujourdhui.verifier`, `texte_avancement`) ; consigne de session quand `etude_a_lancer` : « lancer l'agent data-scientist (BasketVibe, horizon aujourd'hui) sur la question ouverte : <sujet de l'étude la plus récente dont un verdict est « indéterminé » ou « donnée absente » ; sinon la prochaine hypothèse> ; ne demande un export que pour les groupes de moteur encore ouverts (v4 ligue, v5 amical) ».

- [ ] **Étape 1 : tests** : `test_lire_etudes_ignore_invalidee` (revue ciblée 6) ; `test_lire_etudes_plus_recente_par_sujet` ; `test_demandes_recopiees_des_etudes` (le texte du bloc 0 et du bloc 6 est la ligne de l'étude, mot pour mot, suivie de sa date ; aucune étude → aucune demande) ; `test_etude_a_lancer_trois_defaites` ; `test_etude_pas_lancee_sans_nouveau_match` (série de 3 défaites, k = 0 : pas de lancement) ; `test_etude_a_lancer_dimanche` ; `test_etude_pas_lancee_un_mardi_sans_defaites` ; `test_etude_pas_lancee_deux_fois_le_meme_jour` ; `test_bloc_0_cite_le_bloc_debloque` ; `test_bloc_0_apercu_absent_par_match` ; `test_bloc_0_exports_hebdomadaires` ; `test_bloc_6_ligne_quotidienne` (format exact, ni « appris » ni « relancée ») ; `test_bloc_6_consigne_session` (nomme `data-scientist` et « v4 ligue, v5 amical »).
- [ ] **Étape 2** : lancer → échec.
- [ ] **Étape 3** : ajouter les 2 requêtes, implémenter `lire_etudes`, `bloc_0`, `etude_a_lancer`, `bloc_6`.
- [ ] **Étape 4** : lancer → succès.
- [ ] **Étape 5** : commit « 5n T5 : blocs 0 et 6, exports par match, demandes des études, ligne Match Engine ».

## Tâche 6 — Blocs 5, 7, 8, 9, 10 et assemblage

**Fichiers** : modifier `pipelines/que_faire_blocs.py`, tests.

**Produit** :
- `etat_etude(etudes, bloc: int) -> str` : état de l'étude du bloc, lu dans `lire_etudes` (T5) par une table explicite sujet → bloc (5 meilleurs et failles, 8 économie, 9 académie, personnel, entraînement ; table vide en 5n, remplie en 5o) : « faisable », « bloquée par : exporte X », ou « dernier résultat du JJ/MM : estimé [IC 95 %] » ; sans étude : « étude pas encore commencée, carte de faisabilité à faire ». Jamais « reporté ».
- `bloc_5(etudes) -> list[str]` : `[etat_etude(etudes, 5)]`.
- `bloc_7(actions, donnees) -> list[str]` : toujours une ligne d'état en tête, jamais vide : défaite de ligue ou de coupe sans brief `analyste` → « défaite du JJ/MM : analyse non faite, lancée dans ce passage » (et consigne de session) ; avec brief → « défaite du JJ/MM : analyse faite » ; aucune défaite depuis la dernière analyse → « aucune défaite de ligue ou de coupe non analysée » ; puis les lignes de `plan()` classées dans ce bloc, inchangées.
- `bloc_8`, `bloc_9(actions, etudes) -> list[str]` : `etat_etude` du bloc, puis les lignes de `plan()` classées dans ce bloc, inchangées ; sans ligne → `manque(...)` avec l'export concerné (Finances ; Académie/Personnel/Entraînement).
- `bloc_10(actions, garder: list[str]) -> list[str]` : propositions d'achat, de vente et d'enchère à valider par écrit, puis les règles « à valider » de `garder`.
- `rendre_blocs(res, donnees, erreurs, jour, maintenant, S) -> tuple[str, list[str]]` : concatène « Bloc 0 … Bloc 10 » dans l'ordre, chaque bloc avec son titre ; clé de `erreurs` d'un bloc → `donnée manquante : vue <nom> illisible` dans ce bloc (revue ciblée 5) ; renvoie aussi la liste des consignes de session.

- [ ] **Étape 1 : tests** : `test_onze_blocs_dans_l_ordre` ; `test_aucun_bloc_absent` (données minimales : chaque titre « Bloc 0 » à « Bloc 10 » présent) ; `test_etat_etude_sans_etude` (phrase exacte) ; `test_aucun_reporte` (« reporté » absent des blocs 5, 8, 9) ; `test_bloc_7_ligne_d_etat_toujours` (trois cas : défaite non analysée, analysée, aucune défaite) ; `test_vue_illisible_ne_plante_pas` (revue ciblée 5) ; `test_aucun_mot_interdit_dans_tout_le_rendu` (`INTERDITS` absent du texte complet) ; `test_rendu_passe_forme_et_controle` (`forme.fautes_de(texte, "basketvibe") == []`).
- [ ] **Étape 2** : lancer → échec.
- [ ] **Étape 3** : implémenter les fonctions ci-dessus.
- [ ] **Étape 4** : lancer → succès.
- [ ] **Étape 5** : commit « 5n T6 : blocs 5, 7 à 10, états des études et assemblage des onze blocs ».

## Tâche 7 — Branchement, anciens tests, skill

**Fichiers** : modifier `pipelines/aujourdhui.py` (`rendre`, `main`), `pipelines/test_aujourdhui.py`, `.claude/skills/basketvibe-aujourdhui/SKILL.md`.

- [ ] **Étape 1** : `aujourdhui.rendre()` appelle `que_faire_blocs.rendre_blocs`, imprime le rendu, puis un séparateur `--- session (à exécuter, ne pas afficher) ---` et les consignes ; l'instantané `aujourdhui-AAAA-MM-JJ.md` contient le rendu sans les consignes.
- [ ] **Étape 2** : lancer `python pipelines/test_aujourdhui.py` ; les cas qui figeaient la forme de 8 lignes (par exemple autour de `auj.rendre(...)`, ligne 142) et les cas Y2/Y3 qui attendent « lance l'agent tactique » / « python -I pipelines/composition.py » (autour de la ligne 679) échouent : pour chacun, réécrire le test selon le nouveau format et écrire une ligne dans la table des tests réécrits du journal (ancien attendu, nouvel attendu, raison : bloc 3 et règle « jamais une commande »).
- [ ] **Étape 3** : réécrire `SKILL.md` de `basketvibe-aujourdhui` : première action = le script ; afficher le rendu **avant** le séparateur tel quel ; exécuter les consignes de session après le séparateur (agents tactique et analyste, agent data-scientist au plus une fois par jour) puis relancer le script une fois ; demander à l'utilisateur les exports signalés « donnée manquante » ; supprimer « au plus 8 lignes `HH:MM` ».
- [ ] **Étape 4** : lancer `python pipelines/test_aujourdhui.py`, `python pipelines/test_composition.py`, `python pipelines/test_que_faire_blocs.py`, `python pipelines/test_forme.py` → tous verts, comptes collés.
- [ ] **Étape 5** : commit « 5n T7 : branchement du rendu en blocs, tests réécrits, skill du que faire ».

## Tâche 8 — Réception sur la vraie journée

**Fichiers** : modifier `docs/refonte-v3/journal-aujourdhui.md`.

- [ ] **Étape 1** : exécuter `python -I pipelines/aujourdhui.py basketvibe` sur la journée réelle ; coller la sortie telle quelle dans le journal ; noter la durée (comparer aux 15 s).
- [ ] **Étape 2** : tableau `Bloc | Attendu (gabarit) | Produit | Écart` : une ligne par bloc de 0 à 10 (les blocs 5, 8, 9 avec l'état de leur étude), chaque écart nommé.
- [ ] **Étape 3** : vérifier à la main, dans le rendu réel :
  - aucun mot de `INTERDITS`, aucun bloc absent, `forme.py` et `controle.py` passent ;
  - blocs 0 et 6 : chaque ligne « Pour comprendre le Match Engine, j'ai besoin de : » se retrouve mot pour mot dans l'étude de `docs/etudes/` qu'elle cite, à la date citée, et aucune ne vient d'une étude invalidée ;
  - bloc 6 : la ligne suit exactement `matchs ajoutés : n (ligue a, amical b) · N en base · étude à jour au JJ/MM, k pas encore étudiés`, JJ/MM = date du dernier fichier d'étude non invalidé, k recompté par `python -I pipelines/sql.py` ;
  - bloc 1 : chaque action des blocs 0 et 2 à 10 y figure avec son « → bloc N », et le bloc n'est pas vide ;
  - bloc 7 : la ligne d'état est présente et correspond à la base (dernière défaite de ligue ou de coupe, brief `analyste` présent ou non) ;
  - blocs 2 et 3 : vérification J-1 présente ; bloc 2 : composition tirée du brief du jour, aucune mention « pas de blessure ».
  Un critère raté = un correctif et un nouveau commit, pas une réécriture du tableau.
- [ ] **Étape 4** : `python -I pipelines/fusion_main.py` puis `python -I pipelines/fin_etape.py` ; coller les deux sorties dans le journal ; commit « 5n T8 : réception, comparaison bloc par bloc ».

## Auto-relecture

- **Couverture de la conception** : blocs 0 à 10 → tableau de couverture ; Q1 (amical, ligue) → T3 ; Q2 (étude) → T5 ; Q3 et « qui vendre » → T4 ; états des études → T6 ; réception → T8 ; skill → T7.
- **Cohérence des noms** : `manque`, `classer`, `separer`, `lire_etudes`, `etat_etude`, `verifier_j_moins_1`, `bloc_0` à `bloc_10`, `rendre_blocs`, `etude_a_lancer`, `composer_amical` sont définis dans la tâche qui les produit et utilisés ensuite avec la même signature.
- **Proportion** : la conception fait ~100 lignes, ce plan ~190 ; aucune fonction n'est écrite en entier.
- **Hors plan, à signaler à l'utilisateur** :
  - le nombre de pages du Marché n'a pas de seuil connu (le bloc 0 affiche le compte sans conclure) ;
  - les conseils sur les recrues sont reportés ;
  - la durée d'un lancement de l'agent data-scientist n'est pas mesurée avant T8 ;
  - **blessures en amical, le dépôt se contredit** : le manuel et les fiches disent « aucune » (`docs/fiches/basketvibe/resume.md` l. 19, `commun.md` l. 20, `tactique.md` l. 52, 59, 68 [M§1.2]) ; les skills `basketvibe-joueurs` (`references/10-blessures.md` l. 2) et `basketvibe-saison` (`references/06-amicaux.md` l. 2) disent que le moteur v4 en met [News 2026-10-19]. La sortie n'en dit rien ; la première étude de l'agent data-scientist tranchera, puis les fiches seront corrigées.