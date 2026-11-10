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
| 2 Composition de l'amical | **5n** | **Sans fiche, sans aperçu, sans agent** (décision Q1). Le script reprend les réglages du dernier amical joué (`gold.bv_saisie_joueurs`, jeunes et cinq de ligue à 0 minute, comme aujourd'hui) et y applique le niveau du test en cours (agressivité, zone, focus constants). Tableau poste par poste dans l'ordre de l'écran (colonnes du format `tactique`), puis zone et focus défensif, test nommé, heure limite du verrou. |
| 3 Composition de la ligue ou de la coupe | **5n** | **Séparée de l'amical** : elle exige l'aperçu adverse. Aperçu en base → l'agent tactique est lancé dans le passage, puis tableau de saisie + tableau des adversaires (focus défensif par adversaire). Aperçu absent → « donnée manquante : exporte l'aperçu du match de ligue du JJ/MM » (je le demande à l'utilisateur, décision Q1). Vérification à J-1 : chaque joueur proposé est comparé à l'effectif du jour (blessé, forme ≤ 2, fatigue hors zone verte, joueur vendu) ; chaque écart tient en une ligne. |
| 4 Transferts | **5n** (partie) | **Deux tableaux** (demande de l'utilisateur). (1) *Table des prix* : pour chaque tranche d'âge × niveau (note PS par paliers de 5) : nombre de ventes, prix bas (p25), médian, haut (p75), dernière vente — source `gold.bv_price_ref_ps`. (2) *Qui acheter* : annonces du Marché qui se terminent dans les 24 h, dédupliquées entre les pages, rangées dans leur case âge × niveau : nom \| poste \| âge \| note \| prix actuel \| case (p25 / médiane) \| plafond \| fin \| gain pour mon cinq. « Achetable » = prix actuel sous le seuil Q3 et dans la capacité restante (solde moins enchères ouvertes). Les lignes actuelles de vente et d'enchères en cours sont gardées. Les conseils sur les recrues sont reportés. |
| 5 Les meilleurs et les failles | **plus tard** | Bloc présent avec une seule ligne : « reporté : étude des meilleurs prévue après l'étape suivante ». |
| 6 Match Engine | **5n** | Une ligne : « matchs ajoutés depuis hier : n (ligue a, amical b), total en base N, étude relancée le JJ/MM ». **Relance de l'étude** (décision Q2) : après 3 défaites de suite en ligue ou en coupe, ou une fois par semaine (le dimanche, mon choix : le jour de l'analyse hebdomadaire du bloc 7) ; hors de ces cas, le bloc affiche la date de la dernière étude. Avancement des expériences et prochaine hypothèse en dessous. |
| 7 Analyse | étape suivante | En 5n, la ligne actuelle « défaite → analyste » est rangée dans ce bloc, sans changement. |
| 8 Économie | étape suivante | En 5n, les lignes actuelles de finances (solde projeté, seuil) sont rangées dans ce bloc, sans changement. |
| 9 Académie, personnel, entraînement | étape suivante | En 5n, les lignes actuelles d'académie, de personnel et d'entraînement sont rangées dans ce bloc, sans changement. |
| 10 À valider | **5n** | Décisions qui exigent l'accord écrit de l'utilisateur (achat, vente, enchère proposés), puis règles « non tranchées, à valider » déjà produites aujourd'hui (vente pour profit, personnel, valeur d'un High). Une ligne par point. |

Règle de bloc vide (tous les blocs) : « donnée manquante : exporte <écran> », jamais « lance », « python », « exécute ». Un test balaie toute la sortie pour vérifier qu'aucun de ces mots n'y figure.

## 4. Objectifs, non-objectifs, anti-objectifs

- **Objectifs** : le que faire complet du gabarit pour les blocs 0, 1, 2, 3, 4, 6 et 10, et les blocs 7, 8 et 9 rangés. Une sortie reproductible : le script la produit et Claude l'affiche telle quelle.
- **Non-objectifs** : le contenu nouveau des blocs 5, 7, 8 et 9 ; un nouveau moteur de décision de composition ; tout changement des règles de `forme.py` et de `controle.py`.
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

- **Q1 (décidée)** : l'amical n'a besoin ni de fiche ni d'aperçu : il sert à faire jouer les jeunes et à tester des tactiques. La ligue et la coupe sont séparées de l'amical : elles ont besoin de l'aperçu adverse, et s'il manque (ou toute autre information), je demande l'export. Cela remplace ma proposition (a) : le script ne cherche plus de brief pour l'amical.
- **Q2 (décidée)** : l'étude du moteur est relancée après 3 défaites de suite, ou une fois par semaine, pour comprendre au mieux le moteur de match. Durée de l'étude non mesurée ; je la mesure en réception.
- **Bloc 4 (demandé)** : une table qui dit, pour tel âge et tel niveau, quel est le prix, et d'où l'on voit qui on peut acheter. Intégré dans la ligne du bloc 4 ci-dessus. Les cases viennent de `gold.bv_price_ref_ps` (palier de note × tranche d'âge) ; la position n'entre pas dans les cases, elle reste une colonne de l'annonce.
- **Q3 (restante)** : à partir de quel prix une annonce est-elle « achetable » dans sa case ?
  - (a) *Ma proposition* : prix actuel ≤ médiane de la case, case fiable (n suffisant, comme `ref_reliable` aujourd'hui), et dans la capacité restante. La médiane laisse voir plus d'annonces ; le plafond reste calculé par la revente.
  - (b) Prix actuel ≤ p25 de la case : moins d'annonces, uniquement de vraies affaires.

## 8. Choix que je fais sans attendre (à corriger si besoin)

- Le bloc 5 reste présent, avec une ligne « reporté ».
- Les blocs 7, 8 et 9 reprennent les lignes actuelles, déplacées et non refaites.
- Le bloc 4 garde les lignes actuelles de vente et d'enchères. Les conseils sur les recrues sont reportés.
- Le bloc 0 vérifie par match en plus du statut par écran. Cela corrige l'écart du 10/11 : il faut y voir « exporte l'aperçu du match de ligue » dès qu'aucune ligne adverse n'est en base.
- Les cinq de ligue restent à 0 minute à l'amical et les jeunes y jouent, comme la fiche du jeu l'écrit aujourd'hui (`docs/fiches/basketvibe/resume.md`) ; je ne change pas cette règle.
- La sortie reste en texte ; les tableaux sont en Markdown pour `forme.py`.
- Le skill `basketvibe-aujourdhui` est réécrit pour décrire les blocs, sans heures, et sans la limite de 8 lignes.
- L'exécution se fait dans la session et non par des sous-agents, à la demande de l'utilisateur.
- Contrôle du document : il n'existe aucun type d'agent adapté (`general-purpose` est interdit par CLAUDE.md). Je l'ai donc relu moi-même, comme un constructeur le ferait.

## 9. Réception

1. Le jour où le code est livré, le vrai « que faire » tourne sur la vraie journée.
2. La comparaison avec le gabarit est inscrite dans `docs/refonte-v3/journal-aujourdhui.md`, dans un tableau Bloc \| Attendu (gabarit) \| Produit \| Écart. Une ligne par bloc, de 0 à 10, les blocs reportés compris.
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
