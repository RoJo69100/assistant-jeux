# Six Zero League — brief Entraînement, 2026-10-26 (cycle 7 réglé le 25/10 à 21:16 UTC ; prochain cycle ce soir, après J16)

Briefs amont lus : Match, Effectif, Finances, Académie (2026-10-26) et Veille (2026-10-26). Brief Entraînement précédent : 2026-10-24 (delta : cycle 7 seulement). Sources : `gold.sz_training_progress`, `silver.sz_player_cycles`, `silver.sz_players` (export du 2026-10-26 17:48 UTC), `silver.sz_training_plan` (day 2026-10-26, 15 lignes), `silver.sz_role_training` (dernier relevé : 2026-10-23), `silver.sz_match_incidents`, `silver.sz_schedule`. Règles : skills `sixzeroleague-entrainement` [W:Training, W:Injuries] et `sixzeroleague-joueurs` [W:Attributes].

## En tête
- **Fiche de saisie : aucun changement ce soir.** Intensité Normal, les 15 focus du plan du 26/10 inchangés. **Date limite : avant 21:00 Paris le 26/10** (le cycle se règle après le match de 21:00 [Dev chat]).
- **Je contredis deux briefs amont (relance à faire seulement si tu veux passer outre)** :
  1. **C-023 (Match) et la partie « Stamina » de C-024 (Effectif) : à ne pas appliquer.** La règle d'endurance existe en général (voir § 4) mais nos données ne montrent aucune faiblesse de fin de match propre à notre équipe. C-023 devient « non retenu ».
  2. Le brief Match écrit que la règle de fatigue est absente des skills : le skill joueurs la donne en une ligne qualitative [W:Attributes] (« peu d'endurance = plus d'erreurs et moins d'efficacité à mesure que le match avance »). Il manque son **ampleur**, pas son existence.
- **Simon reprend le CB (C-024)** : aucune modification d'entraînement. Simon et Denis restent en Attaque / Passe (clé de demi-centre). Le point de Marquage prévu par C-016 n'est pas lancé (§ 3).
- **Fournier (CB), s'il est signé avant 21:00** : à saisir en Attaque / Passe dès la signature (sinon son effort est réparti sur 20 compétences). Voir § 5.
- **2e rôle : ne rien lancer ce soir** ; décision demain, une fois Fournier connu (§ 5).
- **Il me manque** : la durée restante des blessures de Simon et Roger (pas dans l'export) et un relevé de `silver.sz_role_training` postérieur au 23/10. Le plan du 26/10 est à jour (Blanc est bien en Gardien / Handling).

## 1. Fiche de saisie (avant 21:00 Paris)
| Réglage | Valeur | Action |
|---|---|---|
| Intensité d'équipe | Normal | Garder |
| 15 joueurs | focus du § 2 | Garder tous |
| Formation de rôle | slot 1 libre | Ne rien lancer ce soir |
| Fournier (si signé) | Attaque / Passe | À saisir juste après la signature |

## 2. Verdict par joueur (cycle 7 mesuré, `gold.sz_training_progress` + `silver.sz_players.training_progress`)
Cycle 7 : **17 points, tous sur des compétences clés**, 14 joueurs sur 15 ; c'est le plus haut cycle de la saison (cycles 1, 2, 4, 5, 6 : 12, 11, 15, 13, 12 points ; pas de cycle 3 dans la table). Seul Roger n'a rien (§ 6). « Point suivant » = ce qu'il reste avant le prochain point sur le focus.
| Joueur (rôle, âge, éthique) | Focus actuel | Cycle 7 | Point suivant | Verdict |
|---|---|---|---|---|
| Simon (CB, 19, 22) | Attaque / Passe | Passe 6→8 (+1,19 par cycle, constant depuis 2 cycles) | Passe 0,17 | **Garder** (CB titulaire, bonus jeune) |
| Denis (CB, 26, 3) | Attaque / Passe | Passe 6→7 | Passe 0,49 | **Garder** (pas de Stamina, § 4) |
| Bourgeois (GK, 30, 26) | Gardien / Placement | Placement 8→9 | Placement 0,69 | **Garder** (clés non physiques) |
| Blanc (GK, 26, 48) | Gardien / Prise de balle (`Handling`) | Prise de balle 8→9 | 0,84 : point attendu ce soir | **Garder** (C-016 appliqué : 0 point clé avant, 1 sur 1 cycle depuis) |
| A. Bertin (LB, 26, 32) | Attaque / Passe | Passe 13→14 | Passe 0,46 | **Garder** (+1,07 par cycle) |
| Leroy (LB, 24, 29) | Attaque / Tir | Tir 11→12 | Tir 0,43 | **Garder** |
| Lefebvre (LW, 27, 2) | Attaque / Tir | Tir 18→19 | Tir 0,18 | **Garder** (28 ans à la prochaine saison : gain en baisse) |
| Sundberg (LW, 29, 28) | Attaque / Tir | Tir 10→11 | Tir 0,88 : point attendu ce soir | **Garder** (30 ans bientôt : le Tir n'est pas physique) |
| Benoit (P, 19, 40) | Attaque / Tir | Tir 8→10 (2 points) | Tir 0,19 | **Garder** (+1,42 par cycle, meilleur rythme de l'effectif) |
| Chevalier (P, 24, 5) | Physique / Force | Force 11→12 | Force 0,67 | **Garder** |
| Roger (RB, 27, 78) | Attaque / Passe | **0 point** (+0,07 contre +1,66 au cycle 6) | Passe 0,57 | **Garder**, ne pas juger ce cycle (§ 6) |
| Barros (RB, 30, 24) | Attaque / Technique | Technique 16→17 | Technique 0,13 | **Garder** (appliqué depuis C-007) |
| Dupont (RW, 18, 1) | Attaque / Tir | Tir 21→22 | Tir 0,75 : point attendu ce soir | **Garder** |
| G. Bertin (RW, 25, 61) | Physique / Vitesse | Vitesse 15→17 (2 points) | Vitesse 0,09 | **Garder** (0 match joué, mais progresse le plus vite) |
| Lemaire (RW, 22, 19) | Attaque / Tir | Tir 14→15 | Tir 0,43 | **Garder** |
- Aucun focus mal choisi : les 17 points du cycle 7 sont tous sur une clé de rôle ou sur le focus saisi. Cycles 1, 2, 4, 5, 6, 7 : 80 points, dont 73 sur des clés.
- **Ailiers (Effectif, action 3) : je ne remplace pas Tir par Vitesse/Agilité pour Dupont (Vitesse 5).** Aucune source ne donne le poids relatif des 4 clés d'ailier dans la note ; Tir est « la compétence de finition principale » [W:Attributes] et Dupont (Tir 22, 53 % au tir) gagne 1 point par cycle. Pas de rendement décroissant [Dev chat 2026-10-19] : « Vitesse est basse » n'est pas un argument. Je ne change pas un choix cohérent pour rien.
- **Éthique de travail, mesuré** (points sur les cycles 5 à 7) : éthique ≥ 40 (Blanc, Roger, G. Bertin, Benoit) : 3,5 points en moyenne ; éthique < 40 (les 11 autres) : 2,5. Soit environ +0,3 point par cycle, mais l'âge domine (Dupont, éthique 1, fait 3 sur 3). Échantillon petit, confiance faible. L'éthique n'est pas modifiable [W:Training] ; ce n'est pas un motif de changer un focus.

## 3. Verdict sur le point « Simon → Marquage » (C-016, 2e partie)
- Condition posée le 24/10 : « si Simon est à Passe 7 au rapport du 25 ». Elle est remplie (Passe 8).
- **Je ne le lance pas.** Raisons chiffrées : (1) le brief Match montre que les exclusions séparent peu nos victoires de nos défaites (3,9 contre 4,7 par match, `silver.sz_matches`) ; (2) un point de Marquage (6→7) n'est pas une clé de CB, donc 0 de gain de note, et aucune source ne donne son effet en fautes ; (3) il reste 2 cycles dans la saison, donc 3 matchs (J16 à J18) pour mesurer, ce qui ne prouve rien. Passe reste la clé du CB et Simon la fait monter à +1,19 par cycle.
- C-016 passe en « partiel » : Blanc appliqué, Simon non (décision prise, pas oubli).

## 4. Intensité d'équipe et réponse à C-023 (Stamina)
### Intensité : Normal (confiance moyenne)
- Faits : 15 joueurs, 2 par rôle sauf RW (`gold.sz_role_report`, brief Effectif) ; une blessure laisse zéro couverture. Calendrier : **il ne reste que 2 cycles dans la saison** (ce soir après J16 et le 27/10 après J18, `silver.sz_schedule`) ; la finale de coupe est le 28/10 17:00.
- Règle : High = progrès plus rapides mais plus de blessures, et plus longues (~3 matchs, parfois 6) ; un club qui s'entraîne dur a besoin d'un effectif plus profond [W:Training, W:Injuries]. **Le skill ne chiffre pas le gain de High** : je ne peux pas dire s'il vaut le risque.
- Avis : Normal. Le gain possible de High sur 2 cycles est inconnu ; le risque (un CB ou un RB blessé 3 matchs, sans remplaçant en réserve profonde, et une blessure peut déborder sur la saison suivante) est connu. Light ne se justifie pas : personne à ménager (0 blessé à l'entraînement signalé ; les blessures de Simon, Roger, Benoit, A. Bertin sont venues de matchs).
- Ce qui me ferait changer : une source qui chiffre le gain de High, ou un effectif à 3 par rôle.

### C-023 (Stamina) : hypothèse, non prouvée, et les données existantes la contredisent
| Point | Statut | Source |
|---|---|---|
| Une endurance basse fait baisser l'efficacité en fin de match | **Règle qualitative** (sans chiffre) | [W:Attributes], skill joueurs |
| Notre équipe s'effondre en fin de match | **Non confirmé sur la saison** | ci-dessous |
| Entraîner Stamina à Denis / A. Bertin règle ce problème | **Hypothèse sans source** (ampleur d'un point de Stamina inconnue) | aucune ; confiance faible |
- Fait 1 (`silver.sz_match_incidents`, buts, 16 matchs de ligue et coupe relevés) : buts dans les 20 dernières minutes (`clock_s` ≥ 2400) : **nous 117 sur 357 (32,8 %), adversaires 124 sur 387 (32,0 %)**, pour 33,3 % du temps. Nous ne faiblissons pas plus que nos adversaires. Le 17-24 de J13 à J15 est un échantillon de 3 matchs ; sur la saison, l'écart de fin de match est de -7 buts, contre -23 sur les 40 premières minutes.
- Fait 2 (part des buts marqués après 40 min, par endurance actuelle, `silver.sz_match_incidents` + `silver.sz_players`) :
| Groupe | Joueurs | Buts après 40 min / total | Part |
|---|---|---|---|
| Endurance ≥ 15 | Dupont 16, Roger 16, Lemaire 15 | 35 / 115 | 30 % |
| Endurance 11 à 13 | Benoit 11, Leroy 13 | 18 / 50 | 36 % |
| Endurance ≤ 8 | Lefebvre 8, A. Bertin 7, Simon 6, Denis 4, Chevalier 3 | 61 / 183 | 33 % |
  Aucun gradient : les joueurs à faible endurance marquent autant (33 %) que ceux qui en ont (30 %). Réserves : on ne compte que les buts (pas les tirs ratés ni les minutes jouées par période) ; confiance moyenne-faible.
- **Le test qui réfute C-023** : « notre part de buts marqués après 40 min est inférieure à celle des adversaires, et inférieure chez les joueurs à faible endurance ». Test fait sur 16 matchs : **réfuté dans les deux sens**. Aucun test à terme n'est possible dans cette saison : 2 cycles ne donnent que +1 à +2 points de Stamina, soit 4→5 ou 4→6 sur Denis, qui joue peu. Si tu veux quand même tester Stamina plus tard : attendre la saison suivante et le faire sur un titulaire à faible endurance (Lefebvre 8, A. Bertin 7, Simon 6), avec comme repère sa part de buts après 40 min (36 %, 26 %, 31 % aujourd'hui).
- **Décision : C-023 « non retenu »** ; la partie « Stamina pour Simon plutôt que Denis » de C-024 est abandonnée (la reprise du CB par Simon reste valable côté Effectif/Tactique).

## 5. 2e rôle à former et Fournier
- Faits : Training Facilities niveau 6, **slot 1 libre** (`silver.sz_role_training`, relevé du 23/10, rien de plus récent). 36 journées (≈ 18 cycles, 2 saisons), 150 € par cycle, soit **2 700 €** ; annuler ne rembourse rien ; rôle de départ définitif [W:Training, Dev chat]. Ces 2 700 € s'ajoutent à C-026 (Finances) : solde 1 843 € aujourd'hui, 4 767 € attendus après ce soir.
- Règle : un rôle appris supprime la pénalité de hors-poste [W:Training]. Les notes `role_overalls` sont **avant** pénalité (fiche commune) : elles donnent donc la note qu'aurait le joueur à ce poste une fois la formation finie (avis, hypothèse).
| Candidat (surplus) | Rôle visé | Note au rôle (`role_overalls`) | Couverture actuelle | Lecture |
|---|---|---|---|---|
| Lemaire (RW3, 22, éthique 19) | **CB** | 10 | Denis 8 | +2 sur le CB2 ; moins utile si Fournier est signé |
| Lemaire | **GK** | 11 | Blanc 9 (140 € de salaire, 0 match) | Meilleure note de remplaçant GK que Blanc ; Bourgeois a 30 ans (retraite possible dans 3 saisons [brief Effectif]). **Je ne sais pas si le jeu autorise un joueur de champ à apprendre GK** : à lire à l'écran |
| Lemaire | LB | 10 | Leroy 9 | +1 seulement |
| G. Bertin (RW, 25) | GK | 10 | Blanc 9 | Idem, plus faible |
- **Avis (confiance faible) : ne rien lancer ce soir.** Le gain n'arrive qu'à la fin des 36 journées (≈ 20 jours), et la décision dépend de Fournier. Demain (export Équipe + U18 du 27/10) :
  - Fournier **non signé** : Lemaire → CB (note 10 contre 8 pour Denis).
  - Fournier **signé** : Lemaire → GK si l'écran le permet (le poste le plus exposé après le RB), sinon rien.
  - Le coût de 2 700 € et le moment restent à valider avec Finances (C-026) : décision à l'utilisateur.
- **Fournier (CB, 18 ans), s'il est signé** : bonus d'entraînement complet jusqu'à 20 ans [W:Training] ; ses 18 compétences inconnues se lisent dans `silver.sz_players` après l'export. Saisie par défaut : **Attaque / Passe** (clé de demi-centre, même choix que Simon et Denis). Au prochain export, choisir la clé de CB (Passe, Technique, Jeu sans ballon, Tir) qui lui apporte le plus ; sans poids connu, ne pas la choisir parce qu'elle est basse (pas de rendement décroissant). Il progressera aussi par ses minutes de jeu [Dev chat, devlog 0.5.7], donc plus vite s'il joue : à lier au choix de Tactique.
- Si Fournier est signé, Denis reste en Passe (CB3, aucun coût) ; Simon, titulaire CB, reste en Passe.

## 6. Blessés et règle V-4 (un blessé ne reçoit pas de points d'entraînement)
- V-4 est **cohérent avec une mesure**, pas démontré : Roger, blessé à 43:46 de J14 (21:00 Paris), gagne **+0,07** de progression de Passe au cycle 7 (0,51→0,57, aucun point) contre +1,66 au cycle 6 (`silver.sz_player_cycles`). A. Bertin, marqué `injured` vrai au relevé du 23/10 (cycle 5) : aucun point au cycle 5, puis +1,07 par cycle une fois valide (cycles 6 et 7). Simon, absent de J14 et J15, gagne +1,19 au cycle 7 comme au 6 : il n'était donc pas blessé au règlement (ou la blessure ne bloque pas).
- Limite : le drapeau `injured` de l'API est faux pour Roger et Simon à 17:48 UTC alors qu'ils n'ont pas joué J15 (brief Effectif) : je ne peux pas dater leur blessure. Les chiffres de progression sont donc le meilleur indice disponible.
- **Ne compter aucun gain pour Roger tant qu'il est blessé.** Contrôle demain : Roger valide = +1,2 à +1,7 de Passe attendus (0,57→ nouveau point) ; s'il reste à +0,07, il est toujours blessé et V-4 se confirme (2e cas).

## 7. Suivi de la saison qui se termine
- Dernier cycle de la saison : le 27/10 après J18. Le passage à +1 an arrive ensuite (vers le 27-28/10, brief Effectif). **Mesure à prendre au premier relevé suivant** : pertes de compétences physiques de Bourgeois, Barros (30 → 31) et Sundberg (29 → 30) ; le skill ne donne aucun chiffre et rien ne dit si l'entraînement les limite. Comparer les compétences physiques de `silver.sz_players` avant et après. Aucun levier d'entraînement à proposer avant ce chiffre.

## 8. Conseils suivis (ajoutés à `outputs/sixzeroleague/learnings.md`)
- **C-030** : plan du soir inchangé (Normal, 15 focus, aucun Stamina) ; critère : `silver.sz_training_plan` (day >= 2026-10-26) sans `focus_skill` = Stamina, et `gold.sz_training_progress` du cycle du 26/10 avec >= 11 points dont >= 90 % de clés (repère : 11 à 17 sur les cycles 1 à 7).
- **C-031** : 2e rôle, décision au 27/10 selon Fournier (Lemaire → CB si non signé ; Lemaire → GK si signé et autorisé) ; complète C-026 (coût) ; critère : `silver.sz_role_training` slot 1 occupé par Lemaire.
- **C-032** : Fournier (si signé) saisi en Attaque / Passe ; critère : `silver.sz_training_plan` (day >= 2026-10-27) ligne Fournier `focus_skill` = Passing.
- Statuts mis à jour : C-023 non retenu ; C-016 partiel (Blanc appliqué, Simon décidé non) ; C-006 (Match, endurance) reste « non appliqué », réécrit puis écarté.
- Aussi à contrôler : C-014a (Benoit blessé, « blessé = pas d'entraînement ») : Benoit n'a plus de blessure ; le cas Roger du § 6 sert de test, à reprendre au prochain cycle.

## 9. À refaire si
- Export Équipe + Training du 27/10 : Fournier signé ou non (focus à saisir), Roger et Simon valides (gain de Passe), plan et slot de formation à relever (`silver.sz_role_training` est resté au 23/10).
- Si l'écran Équipe montre encore Simon ou Roger blessé : aucun point d'entraînement n'est à attendre pour eux ce soir.
