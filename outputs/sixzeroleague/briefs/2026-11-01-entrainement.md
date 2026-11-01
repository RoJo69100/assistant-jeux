# Six Zero League — brief Entraînement, 2026-11-01 (saison 4, J1 à 13:00 Paris ; cycle ce soir après J2, 21:00)

Sources : export Équipe/Training du 2026-11-01 07:26 UTC (`bronze.raw_pages` id 31829, focus + rapport « Week 9 »), `silver.sz_players` (as_of 2026-10-31, mêmes âges et notes que l'écran 07:28), `gold.sz_training_progress`, `silver.sz_player_cycles`, `silver.sz_role_training`, `gold.sz_finance_projection`, `gold.sz_effectif_bilan`. Règles : skills `sixzeroleague-entrainement`, `-joueurs` [W:Training, Attributes, Injuries]. Brief amont lu : brief Entraînement du 2026-10-26 (pas de brief du jour des autres agents).

## En tête (à faire AUJOURD'HUI avant 21:00 Paris)
- **Aucun changement de focus : les 16 focus à l'écran sont à garder.** Cycle 10-28 (rapport Week 9) : 17 points, 15 joueurs, 100 % sur la compétence ciblée. Cycle 10-26 : 17 points, 100 % clés. Aucun focus n'a échoué à produire un gain : rien à réécrire.
- **Intensité : Normal** (écran : « Standard gains. Injury chance about 1.5% per player each week, out for about two matches »). Le sélecteur de l'export ne dit pas quelle option est cochée ; dernier plan en base (10-26) = Normal et le texte « Standard » correspond : à vérifier d'un coup d'œil, c'est l'option à laisser.
- **Slot de formation de rôle : il est UTILISABLE, ta prémisse est inexacte.** L'écran dit « Next slot at Training Facilities level 10 » = le **2e** emplacement. Le slot 1 est « Free » (débloqué au niveau 5, `silver.sz_role_training` : slot 1 `unlocked` = true, slot 2 niveau 10). **Décision : ne pas le lancer aujourd'hui** (voir § 3).

## 1. Fiche de saisie (ordre de l'écran ; « garder » = rien à toucher, puis Save plan)
| Réglage | Actuel | À mettre |
|---|---|---|
| Intensité d'équipe | Normal | **Normal** |
| Role training, slot 1 | Free | **laisser libre** |
| Blanc (GK, 27) | Handling 12 | **garder Handling** |
| Bourgeois (GK, 31) | Positioning 11 | **garder Positioning** |
| Simon (CB, 20) | Passing 10 | **garder Passing** |
| Denis (CB, 27, en vente) | Passing 8 | **garder Passing** |
| Fournier (CB, 19) | Passing 27 | **garder Passing** |
| A. Bertin (LB, 27) | Passing 16 | **garder Passing** |
| Leroy (LB, 25) | Shooting 14 | **garder Shooting** |
| Barros (RB, 31) | Technique 18 | **garder Technique** |
| Roger (RB, 28) | Passing 17 | **garder Passing** |
| Sundberg (LW, 30) | Shooting 13 | **garder Shooting** |
| Lefebvre (LW, 28) | Shooting 20 | **garder Shooting** |
| G. Bertin (RW, 26) | Speed 19 | **garder Speed** |
| Dupont (RW, 19) | Shooting 24 | **garder Shooting** |
| Lemaire (RW, 23) | Shooting 17 | **garder Shooting** |
| Benoit (P, 20) | Shooting 13 | **garder Shooting** |
| Chevalier (P, 25) | Strength 14 | **garder Strength** |
Rien ne change : si le plan est déjà celui de l'écran, aucun « Save plan » n'est nécessaire.

## 2. Verdict par joueur (gains réels, `gold.sz_training_progress`)
« Points » = points gagnés sur le focus actuel sur les 3 derniers cycles (10-25, 10-26, 10-28). « Prochain » = progression fractionnaire vers le point suivant (`silver.sz_players.training_progress`). Clés = compétences clés du rôle [W:Attributes] (CB traité comme demi-centre : Passe, Technique, Jeu sans ballon, Tir ; arrières : Tir, Détente, Technique, Passe ; ailiers : Vitesse, Agilité, Tir, Contrôle ; pivot : Force, Contrôle, Jeu sans ballon, Tir ; gardien : Réflexes, 1c1, Placement, Prise, Relance).
| Joueur (âge, éthique) | Focus : valeur | Points 3 cycles | Prochain | Pourquoi garder |
|---|---|---|---|---|
| Blanc (27, 48) | Prise de balle 12 | 4 | 0,39 | Clé gardien ; Handling 8→12 en 4 cycles depuis le changement (C-016) ; avant, BallControl non clé |
| Bourgeois (31, 26) | Placement 11 | 3 | 0,27 | Clé, titulaire (19 matchs) ; 3→11 en 8 cycles ; non physique, épargné par le déclin |
| Simon (20, 22) | Passe 10 | 4 | 0,54 | Clé CB ; bonus jeune (≤ 20 ans) ; 1→10 en 7 cycles |
| Denis (27, 3) | Passe 8 | 2 | 0,87 | Clé, point probable ce soir ; en vente (résolution à l'intersaison [Dev chat 2026-10-28]) : aucun coût à garder |
| Fournier (19, 90) | Passe 27 | 4 (2 cycles) | 0,14 | +2 par cycle (éthique 90, bonus jeune) ; CB titulaire ; 23→27 ; C-032 validé |
| A. Bertin (27, 32) | Passe 16 | 3 | 0,79 | Clé LB titulaire ; +1 à chaque cycle depuis 7→8 |
| Leroy (25, 29) | Tir 14 | 3 | 0,54 | Clé ; +1 à chaque cycle, 3→14 |
| Barros (31, 24) | Technique 18 | 2 | 0,67 | Clé ; non physique ; 14→18 sur 4 points |
| Roger (28, 78) | Passe 17 | 3 | 0,90 | Clé RB titulaire ; 2→17 ; point probable ce soir |
| Sundberg (30, 28) | Tir 13 | 3 | 0,68 | Clé ; Tir non physique |
| Lefebvre (28, 2) | Tir 20 | 2 | 0,63 | Clé, titulaire ; rythme le plus lent (éthique 2, 28 ans) : 4 points en 6 cycles ; changer de compétence ne change pas l'éthique ni l'âge, donc pas de gain à attendre d'un autre focus |
| G. Bertin (26, 61) | Vitesse 19 | 4 | 0,98 | Clé ailier ; point imminent ; 5→19 ; surplus RW3 (0 match) mais progresse sans jouer |
| Dupont (19, 1) | Tir 24 | 3 | 0,77 | Clé RW titulaire ; +1 à chaque cycle, bonus jeune |
| Lemaire (23, 19) | Tir 17 | 3 | 0,47 | Clé ; 9→17 |
| Benoit (20, 40) | Tir 13 | 5 | 0,03 | Meilleur rythme de l'effectif (+1,4 par cycle) |
| Chevalier (25, 5) | Force 14 | 3 | 0,15 | Clé pivot ; +1 à chaque cycle |
- **Total mesuré** : 17 points aux cycles 10-26 et 10-28 (contre 11 à 17 sur les cycles 1 à 7) ; Denis est le seul sans point au dernier rapport (progrès 0,87 acquis).
- **Conseils contrôlés** : C-030 (Normal, aucun Stamina, ≥ 11 points dont ≥ 90 % clés) = **appliqué, confirmé** (17 points, 100 %). C-032 (Fournier en Passe) = **appliqué, confirmé** (+2 par cycle sur 2 cycles). C-031 (formation de rôle) = **non lancé**, voir § 3. Aucun conseil d'entraînement n'a échoué : rien n'est réécrit.
- **Non modifiable / non tranché par une source** : le poids relatif des clés dans la note n'est dans aucune source (cherché dans : skills joueurs/entrainement, wiki via skills, connaissance.md, Discord part1, chat). Donc aucun focus n'est remplacé « parce qu'une autre clé est plus basse » : pas de rendement décroissant [Dev chat 2026-10-19].

## 3. Intensité et formation de rôle
### Intensité : Normal (confiance moyenne)
- Faits : écran = ~1,5 % de blessure par joueur et par semaine, ~2 matchs d'absence. 16 joueurs = ~0,24 blessure par cycle attendue ; saison de 9 cycles = ~2 blessures. Un blessé ne reçoit pas de points [Dev chat 2026-10-25/26]. Couverture : 2 joueurs par rôle (GK, CB, LB, LW, P, RB, RW) + G. Bertin ; Denis part à l'intersaison.
- Règles : High = progrès plus rapides mais plus de risque et blessures plus longues (devlog 0.6.0) ; en 0.6.1 le risque d'entraînement est divisé par deux et « les trois intensités sont rééquilibrées » ; **aucun chiffre de gain ni de risque pour Light et High n'est dans nos sources**.
- **Il me manque** : gain et risque de High (et de Light). Cherché dans : export 11-01 (seul le texte de l'option affichée est présent), skills, wiki, connaissance.md, Discord part1 (0.6.0 et 0.6.1 : qualitatif seulement), chat. **On le réunit comme ça** : ce soir avant de quitter l'écran, ouvre le sélecteur, passe sur High puis Light **sans enregistrer**, recopie la ligne sous le sélecteur (elle change selon l'option) et remets Normal.
- Décision : **Normal**. Ce qui prouverait que j'avais tort : la ligne « High » donne un gain nettement supérieur pour un risque proche de 1,5 % ; test à date : le cycle du 02/11 se jugerait au rapport (points par cycle ≥ 17 en Normal).

### Slot 1 de formation de rôle : utilisable, mais pas lancé (confiance faible)
- Faits : Training Facilities niveau 6, slot 1 libre, 150 € par cycle, 36 journées (≈ 2 saisons), annuler ne rembourse rien [W:Training ; API]. Solde 1 559 €, net attendu +3 396 € par cycle (`gold.sz_finance_projection`). Rôle appris : pénalité de hors-poste supprimée, rôle gardé si vendu [devlog 0.5.7].
- Candidat connu (`role_overalls`, avant pénalité) : Lemaire GK 11 contre Blanc 9 (GK2, 0 match, ne joue que sur blessure ou rouge de Bourgeois) ; Fournier est maintenant CB titulaire (17), donc le besoin CB2 n'existe plus (Simon 10).
- Raison de ne pas lancer : gain nul en 2 saisons (rôle fini après 36 journées), sur un poste de doublure qui joue sur blessure seulement, et 2 700 € en concurrence avec C-044 (Fan Shop 5 400 €, Youth Academy 11 400 €). **Décision : rien aujourd'hui** ; à rouvrir si Bourgeois (31 ans) annonce sa retraite.

## 4. Déclin physique mesuré au passage à +1 an (nouveau fait)
`silver.sz_player_cycles` 10-27 contre 10-31 : Sundberg (29→30) −1 sur Vitesse, Agilité, Force, Détente, Endurance (19→18, 5→4, 6→5, 19→18, 19→18) ; Barros (30→31) −1 sur Vitesse, Agilité, Force, Détente, Endurance ; Bourgeois (30→31) −1 sur Vitesse, Agilité, Détente, Endurance (Force reste à 1). Soit **−1 par compétence physique, à 30 et 31 ans, en continuant de s'entraîner sur du non physique** [Obs SQL 2026-11-01, 3 joueurs]. Les compétences focalisées (Tir, Technique, Placement) n'ont pas baissé. Aucune donnée sur les 28-29 ans (Lefebvre, Roger) : à relever au prochain passage à +1 an (~9 à 11 jours).

## 5. Conseils suivis (ajoutés à `outputs/sixzeroleague/learnings.md`)
- **C-053** : plan du jour inchangé (Normal, 16 focus actuels) ; critère : `silver.sz_training_plan` (day >= 2026-11-01) `intensity` = Normal et mêmes focus ; `gold.sz_training_progress` du cycle du 11-01 : >= 11 points dont >= 90 % de clés (repère : 17 aux deux derniers cycles).
- **C-054** : slot 1 de formation de rôle non lancé ; critère : `silver.sz_role_training` (day >= 2026-11-01) slot 1 sans occupant ; à rouvrir si retraite de Bourgeois annoncée.
- **C-055** : relever ce soir la ligne d'explication de High et Light (intensité) ; critère : valeurs notées dans `docs/fiches/sixzeroleague/entrainement.md`.
- C-031 clos (remplacé par C-054).
