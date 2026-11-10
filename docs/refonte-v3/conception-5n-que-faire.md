# Conception — étape 5n : le « que faire » BasketVibe bloc par bloc

Statut : **à approuver** (aucun code avant l'approbation de l'utilisateur, règle 13 de CLAUDE.md).
Écrit le 2026-11-10 (Paris) avec le skill brainstorming. Référence : `docs/attentes/gabarit-que-faire-basketvibe.md` (blocs 0 à 10).

## 1. Intention

Le « que faire » du jour doit être le document du gabarit, bloc par bloc, et non plus une liste de 8 lignes horodatées. Chaque bloc contient des données réelles ou la ligne « donnée manquante : exporte X ». Aucun bloc n'est absent. Aucune commande n'est donnée à l'utilisateur. Pourquoi : l'utilisateur veut une décision quotidienne complète qu'il peut contrôler bloc par bloc contre son gabarit.

## 2. Ce qui existe aujourd'hui (lu le 10/11)

| Élément | État | Écart avec le gabarit |
|---|---|---|
| `pipelines/aujourdhui.py` (1 139 lignes, 989 lignes de tests) | Sortie de 8 lignes au plus, triées par heure `HH:MM`, puis « Autres points », « Garder », « Exports ». | Les blocs n'existent pas. Il y a des heures. Les actions de demain ne sont pas séparées. |
| Skill `basketvibe-aujourdhui` | Impose « au plus 8 lignes `HH:MM` » et l'affichage tel quel du script. | Contredit le gabarit. Il faut le réécrire. |
| `pipelines/composition.py` (Y1) | Produit le tableau de saisie et le tableau des adversaires à partir du dernier brief tactique valide. Pour un amical, il ajoute l'agressivité du test en cours. | Le format est déjà validé par `forme.py`. Sans brief, il dit « aucune fiche : lance l'agent tactique ». C'est une commande, donc interdit par le gabarit. |
| Ligne J-1 (Y3) | Rappelle de réexporter l'aperçu si le verrou est dans moins de 24 h. | Ne compare pas la composition proposée à l'état de l'effectif (blessure, forme, fatigue). |
| `gold.bv_exports_state` | 14 écrans, avec leur âge et un statut. | Le statut est par écran, pas par match. Le 10/11, il dit « aperçu de ligue à jour » alors que le plan dit « aucune ligne adverse en base » pour le match du 11/11. |
| `gold.bv_market_bargains` | Cibles, prix, plafond de revente, `ends_paris`. | Pas de filtre sur 24 h. Pas de compte des pages du Marché reçues. |
| Étude du moteur (`etude_evenements_basketvibe.py`) | Lancée à la main. Dernière sortie : 09/11. | Aucune ligne quotidienne « matchs ajoutés, total, étude relancée ». |
| Lignes actuelles d'analyse, de finances, d'académie et de personnel | Déjà produites par le script. | Seront rangées dans les blocs 7, 8 et 9 sans être refaites. |

## 3. Périmètre de l'étape 5n (le plan doit citer chaque bloc)

| Bloc | Étape | Contenu livré en 5n |
|---|---|---|
| 0 Exports | **5n** | Liste de ce qui manque, avec pour chaque export le bloc qu'il débloque (« → bloc 3 »). Contrôle par match et non par écran : aperçu du prochain match de ligue ou de coupe, page du match joué, amical. Marché : nombre de pages reçues depuis 24 h. Source : `bv_exports_state` et requêtes par match. |
| 1 Aujourd'hui, puis demain | **5n** | Tableau Priorité \| Catégorie \| Action (format `plan` de `forme.py`), en deux sections « Aujourd'hui » et « Demain (préparé aujourd'hui) ». Sans heures. La seule heure permise est celle du verrou, dans la ligne de composition. |
| 2 Composition de l'amical | **5n** | **Sans aperçu** (décision Q1), choisie le jour même par l'agent tactique à partir des données du jour (correction du 10/11 après-midi), selon la fiche tactique §2 bis, dans l'ordre : minutes aux jeunes de 21 ans ou moins ; un seul réglage testé à la fois (E1 à E5) ; titulaires de la ligue protégés les jours de ligue, fatigue ajoutée calculée en SQL ; minutes réparties entre les joueurs. Jamais reprise du dernier amical ni du dernier brief ; le script rend le brief du jour et la composition est enregistrée avec ses minutes pour l'étude. Tableau poste par poste dans l'ordre de l'écran (colonnes du format `tactique`), puis zone et focus défensif, test nommé, heure limite du verrou, vérification à J-1 comme au bloc 3. |
| 3 Composition de la ligue ou de la coupe | **5n** | **Séparée de l'amical** : elle exige l'aperçu adverse. Aperçu en base et pas de fiche à jour (brief tactique daté du jour et produit après l'aperçu adverse et le dernier export de l'équipe ; la fiche d'hier n'est jamais à jour) → l'agent tactique est lancé dans le passage, puis tableau de saisie + tableau des adversaires (focus défensif par adversaire). Aperçu absent → « donnée manquante : exporte l'aperçu du match de ligue du JJ/MM » (je le demande à l'utilisateur, décision Q1). Vérification à J-1 : chaque joueur proposé est comparé à l'effectif du jour (blessé, forme ≤ 2, fatigue hors zone verte, joueur vendu) ; chaque écart tient en une ligne. |
| 4 Transferts | **5n** (partie) | **Deux tableaux** (demande de l'utilisateur). (1) *Table des prix* : pour chaque tranche d'âge × niveau (note PS par paliers de 5) : nombre de ventes, prix bas (p25), médian, haut (p75), dernière vente — source `gold.bv_price_ref_ps`. (2) *Qui acheter* : annonces du Marché qui se terminent dans les 24 h, dédupliquées entre les pages, rangées dans leur case âge × niveau : nom \| poste \| âge \| note \| prix actuel \| case (p25 / médiane) \| plafond \| fin \| gain pour mon cinq. « Achetable » = prix actuel sous le seuil Q3 et dans la capacité restante (solde moins enchères ouvertes). (3) *Qui vendre* (demande de l'utilisateur) : tableau des joueurs vendables avec, pour chacun, s'il est nécessaire : nom \| poste \| âge \| note \| salaire hebdomadaire \| rang au poste \| minutes jouées sur les 4 derniers matchs de ligue \| remplaçant \| écart de force avec le remplaçant \| verdict. Verdict : « vendable » si l'écart est dans la tolérance (`core.game_params.vente_tolerance_force`) et qu'il reste assez de joueurs disponibles après la vente (9 aujourd'hui) ; « nécessaire » sinon, avec la raison. Source : `gold.bv_sell_replacement` et `gold.bv_sell_candidates`, déjà utilisées par la ligne de vente actuelle. Le prix de vente attendu s'y ajoute à partir de la case âge × niveau de la table (1). Une vente reste une proposition : rien n'est vendu sans l'accord écrit de l'utilisateur (bloc 10). Les lignes actuelles d'enchères en cours sont gardées. Les conseils sur les recrues sont reportés. |
| 5 Les meilleurs et les failles | **5n** (état), contenu en 5o | Une ligne d'état de l'étude lue dans `docs/etudes/` : faisable, bloquée par tel export, ou dernier résultat avec intervalle ; sans étude : « étude pas encore commencée, carte de faisabilité à faire ». Jamais « reporté ». |
| 6 Match Engine | **5n** | Une ligne : « matchs ajoutés : n (ligue a, amical b) · N en base · étude à jour au JJ/MM, k pas encore étudiés » (JJ/MM = date du dernier fichier de `docs/etudes/`, jamais « appris » ni « relancée le »). Puis les demandes « Pour comprendre le Match Engine, j'ai besoin de : exporte X, parce que Y » recopiées des études (la plus récente par question, avec sa date). **Étude** (décision Q2) : après 3 défaites de suite en ligue ou en coupe, ou le dimanche, et dans les deux cas k >= 1 (au moins un match en base joué après la dernière étude), consigne de session « lancer l'agent data-scientist sur la question ouverte » (« ne demande un export que pour les groupes de moteur encore ouverts (v4 ligue, v5 amical) »), 1 lancement par jour au plus. Avancement des expériences et prochaine hypothèse en dessous. |
| 7 Analyse | **5n** (ligne d'état), contenu étape suivante | Toujours une ligne d'état, jamais vide (« défaite du 09/11 : analyse non faite, lancée dans ce passage »), puis les lignes actuelles rangées dans ce bloc. |
| 8 Économie | **5n** (état), contenu en 5o | État de l'étude (comme le bloc 5), puis les lignes actuelles de finances (solde projeté, seuil), sans changement. |
| 9 Académie, personnel, entraînement | **5n** (état), contenu en 5o | État de l'étude (comme le bloc 5), puis les lignes actuelles d'académie, de personnel et d'entraînement, sans changement. |
| 10 À valider | **5n** | Décisions qui exigent l'accord écrit de l'utilisateur (achat, vente, enchère proposés), puis règles « non tranchées, à valider » déjà produites aujourd'hui (vente pour profit, personnel, valeur d'un High). Une ligne par point. |

Règle de bloc vide (tous les blocs) : « donnée manquante : exporte <écran> », jamais les mots entiers « lance », « relance », « python », « exécute » (un participe comme « lancée dans ce passage » n'est pas une commande). Le bloc 0 liste aussi les exports hebdomadaires pour l'étude (onglets Équipes, Joueurs, Blessés, Transferts de la saison courante ; pages /c/<club>) et les mêmes demandes d'export que le bloc 6. Le bloc 1 liste toutes les actions, chacune avec « → bloc N », et n'est jamais vide. Un test balaie toute la sortie pour vérifier qu'aucun de ces mots n'y figure.

## 4. Objectifs, non-objectifs, anti-objectifs

- **Objectifs** : le que faire complet du gabarit pour les blocs 0, 1, 2, 3, 4, 6 et 10 ; l'état des études aux blocs 5, 8 et 9 ; la ligne d'état du bloc 7 ; les blocs 7, 8 et 9 rangés. Une sortie reproductible : le script la produit et Claude l'affiche telle quelle.
- **Non-objectifs** : le contenu des études des blocs 5, 8 et 9 (étape 5o) et de l'analyse du bloc 7 ; un nouveau moteur de décision de composition ; tout changement des règles de `forme.py` et de `controle.py`.
- **Anti-objectifs** (échec même si « ça marche ») :
  - un bloc qui donne une commande à l'utilisateur ;
  - une action reportée à demain au lieu d'être préparée aujourd'hui ;
  - une composition affichée sans la vérification à J-1 ;
  - un chiffre qui ne sort pas d'une requête du même passage ;
  - une durée qui dépasse nettement les 15 s actuelles.

## 5. Contraintes

- Inviolables de CLAUDE.md : collecte passive, aucun achat sans accord, horizon = aujourd'hui, chiffres tirés de requêtes, plafond d'enchère donné près de la fin. Sur ce dernier point, la fenêtre de 24 h du bloc 4 est prise comme « près de la fin » : c'est mon choix, à corriger si besoin.
- Formats contrôlés par `forme.py` : `plan`, `tactique` (colonnes Joueur \| Poste \| Q1–Q4 \| Prol. \| Minutes \| Off. focus \| Rôle \| Tir \| Agress.) et `adversaires`. Dans le gabarit, « valeurs d'écran » désigne l'échelle 1–5 de ces colonnes et non une colonne de plus (mémoire `feedback-bv-fiche-saisie-complete`). Je garde donc le format `tactique` déjà validé.
- Agents : au plus 3 par passage et 20 par semaine. Un tableau de données = une vue gold et zéro agent.
- Tests : les tests existants (`test_aujourdhui.py`, `test_composition.py`) restent verts. Ceux qui figent la sortie à 8 lignes sont réécrits pour la sortie en blocs, avec une ligne de journal pour chaque test réécrit.

## 6. Approches

1. **Étendre `aujourdhui.py`** *(recommandée)*. `plan()` garde le calcul et range chaque action dans un bloc. `rendre()` produit les 11 blocs dans l'ordre. Les blocs 2 et 3 appellent `composition.composer()`. Les blocs 0, 4 et 6 ajoutent quelques requêtes à `REQUETES`. Avantages : on réutilise 1 139 lignes testées, la sortie est reproductible et le skill reste « afficher tel quel ». Inconvénients : `rendre()` et les tests qui figent les 8 lignes sont réécrits.
2. **Script pour les données, Claude de session pour les compositions**. Le script produit les blocs 0, 1, 4, 6 et 10. Claude assemble les blocs 2 et 3 à chaque passage. Avantage : moins de code. Inconvénients : la sortie n'est plus reproductible ni testable, et contredit la méthode « le script d'abord ».
3. **Un module par bloc** (`pipelines/que_faire/bloc_*.py`), assemblé par un script court. Avantage : structure plus nette. Inconvénients : réécriture de l'essentiel de `aujourdhui.py` et de ses tests, gros risque de régression pour aucun gain visible.

## 7. Décisions de l'utilisateur (10/11 à 11:09) et question restante

- **Q1 (décidée)** : l'amical n'a besoin ni de fiche ni d'aperçu : il sert à faire jouer les jeunes et à tester des tactiques. La ligue et la coupe sont séparées de l'amical : elles ont besoin de l'aperçu adverse, et s'il manque (ou toute autre information), je demande l'export. Corrigée le 10/11 après-midi : l'amical n'a toujours pas besoin d'aperçu, mais sa composition est choisie le jour même par l'agent tactique (fiche tactique §2 bis), jamais reprise du dernier amical ; le script rend le brief du jour. « Ni de fiche » signifie ni preset sauvegardé : le tableau de composition du jour est produit chaque jour (fiche tactique l. 64, corrigée en T3).
- **Q2 (décidée)** : l'étude du moteur est lancée après 3 défaites de suite, ou une fois par semaine, pour comprendre au mieux le moteur de match. Corrigée le 10/11 après-midi : c'est l'agent data-scientist qui la fait, 1 lancement par jour au plus. Durée non mesurée ; je la mesure en réception.
- **Bloc 4 (demandé)** : une table qui dit, pour tel âge et tel niveau, quel est le prix, et d'où l'on voit qui on peut acheter. Intégré dans la ligne du bloc 4 ci-dessus. Les cases viennent de `gold.bv_price_ref_ps` (palier de note × tranche d'âge) ; la position n'entre pas dans les cases, elle reste une colonne de l'annonce.
- **Q3 (décidée, 10/11 11:12)** : une annonce est « achetable » si son prix actuel est ≤ la médiane de sa case, la case est fiable (n suffisant, comme `ref_reliable` aujourd'hui) et l'achat tient dans la capacité restante. Le plafond reste calculé par la revente.
- **Bloc 4, qui vendre (demandé 10/11 11:12)** : ajouté comme troisième tableau du bloc 4, avec la colonne « nécessaire ou non ».

Plus aucune question ouverte. Ce document attend l'approbation de l'utilisateur pour passer au plan (skill writing-plans), plan qui citera chaque bloc 0 à 10.

## 8. Choix que je fais sans attendre (à corriger si besoin)

- Le bloc 5 reste présent, avec l'état de son étude (jamais « reporté »).
- Les blocs 7, 8 et 9 reprennent les lignes actuelles, déplacées et non refaites, sous leur ligne d'état.
- Le bloc 4 garde les lignes actuelles de vente et d'enchères. Les conseils sur les recrues sont reportés.
- Le bloc 0 vérifie par match en plus du statut par écran. Cela corrige l'écart du 10/11 : il faut y voir « exporte l'aperçu du match de ligue » dès qu'aucune ligne adverse n'est en base.
- À l'amical, les jeunes jouent et les titulaires de la ligue sont protégés les jours de ligue (fiche tactique §2 bis, correction du 10/11 après-midi) ; `docs/fiches/basketvibe/resume.md` l. 15 dit encore « jamais le cinq de la coupe/ligue » et reste à aligner (hors plan).
- La sortie reste en texte ; les tableaux sont en Markdown pour `forme.py`.
- Le skill `basketvibe-aujourdhui` est réécrit pour décrire les blocs, sans heures, et sans la limite de 8 lignes.
- L'exécution se fait dans la session et non par des sous-agents, à la demande de l'utilisateur.
- Contrôle du document : il n'existe aucun type d'agent adapté (`general-purpose` est interdit par CLAUDE.md). Je l'ai donc relu moi-même, comme un constructeur le ferait.

## 9. Réception

1. Le jour où le code est livré, le vrai « que faire » tourne sur la vraie journée.
2. La comparaison avec le gabarit est inscrite dans `docs/refonte-v3/journal-aujourdhui.md`, dans un tableau Bloc \| Attendu (gabarit) \| Produit \| Écart. Une ligne par bloc, de 0 à 10, les blocs 5, 8 et 9 compris (état de leur étude).
3. Elle est réussie si :
   - chaque bloc de 5n contient des données réelles ou une ligne « donnée manquante : exporte X » ;
   - aucune commande n'est donnée à l'utilisateur ;
   - `forme.py` et `controle.py` passent sans changer leurs règles ;
   - tous les tests sont verts ;
   - la durée est mesurée et inscrite.

## 10. Laissé au constructeur

- Les noms des fonctions et l'ordre interne des requêtes.
- La forme exacte des lignes d'écart J-1, en une ligne par joueur.
- Le seuil de fatigue « hors zone verte » : il est repris de `gold.bv_daily_alerts` et non redéfini.
