# BasketVibe — fiche Entraînement

Lue par l'agent `entrainement` après `commun.md`. Contenu repris de l'agent BasketVibe validé (checklist BasketVibe, partie E).

## Skills à lire
- `.claude/skills/basketvibe-entrainement/SKILL.md`
- `.claude/skills/basketvibe-joueurs/SKILL.md` (poids du PS, profils)
- `.claude/skills/basketvibe-tactique/SKILL.md` (compétences utilisées par emplacement et par action [M§7.1])

## Règles propres au jeu
1. Delta : lis le dernier brief `outputs/basketvibe/briefs/*-entrainement.md` et ne commente que la nouvelle semaine. Mets à jour les potentiels si une nouvelle mesure les confirme ou les contredit.
2. Donne toujours un niveau de confiance pour le potentiel.
3. Si la fiche du joueur affiche son potentiel (News 2026-10-20), compare-le à `potential_est` (confiance, écart) avant de conclure ; un écart prouve une erreur de facteur d'âge ou de décimales. Dis le format affiché. Constat du 2026-10-23 (un seul joueur, Chomelix Cow, page du 2026-10-22) : la fiche affiche une **tranche** (« ★★☆ Decent potential »), pas un nombre ; ce format sert donc à valider les 2 valeurs plausibles de `potential_est`, pas à les remplacer. Le script Tampermonkey peut devoir être étendu pour lire cette valeur de façon structurée (demander à l'utilisateur) ; à confirmer sur d'autres joueurs. Le manuel §11 dit encore « Unknown » avant test : ⚠️ contradiction avec la News du 2026-10-20.
4. Au passage du dimanche 25/10 : pour chaque joueur de 29 ans, dis que c'est son dernier entraînement utile (+1 an au changement de saison, 0 progression à 30 ans [M§8.5]) ; pour chaque joueur de 16–17 ans, rappelle que le facteur d'âge change au +1 an ; ne pas sauter la saisie du 25/10 [Dev 2026-10-18/22 ; skill basketvibe-saison].

## Données
- `gold.bv_training_gains_exact` : gains **précis** (décimales) par joueur et compétence entre deux relevés hebdomadaires consécutifs (un entraînement entre les deux). `gain_rank` 1 = principale réellement travaillée, 2 = secondaire.
- `gold.bv_potential_estimate` : par joueur et semaine, `implied_mult` = gain de la principale ÷ (niveau × âge), `potential_est` (multiplicateur le plus proche dans le tableau [M§8.3]), `distance_to_table`, `secondary_ratio` (doit valoir 0,50), `age_factor_source` et `confidence`.
  - Âges 16–18 et 25 ans : le facteur d'âge vient du manuel. À ces âges, une distance ≤ 0,03 avec un ratio de 0,50 donne une confiance **élevée**.
  - Autres âges : le facteur vient de `gold.bv_age_factor` (**hypothèse** d'interpolation). Donne alors les **2 potentiels plausibles** (celui de la table et le voisin), sauf si plusieurs semaines concordent.
  - Plusieurs semaines pour un même joueur : prends la médiane de `implied_mult` et signale les écarts.
  - Vérifié le 2026-10-18 : les gains tombent exactement sur le tableau du manuel (Bernard +2,20 → 10 ; Leclerc, Baron +1,60 → 8 ; Gimenez 25 ans → 6 ; Bonnet 25 ans → 7).
- `gold.bv_training_options` : chaque compétence de chaque joueur, avec sa valeur précise, son poids dans le PS du poste (`ps_weight`), son multiplicateur de niveau (`level_mult` [M§8.4]) et le choix actuel (`is_primary`, `is_secondary`).
- `silver.bv_training_changes` / `gold.bv_skill_progress_weekly` : historique affiché (valeurs entières) des ~7 derniers entraînements. Sert de contrôle sur la durée (vitesse moyenne), moins précis.
- `gold.bv_slot_fit` : l'emplacement réel du joueur dans la tactique compte plus que son libellé de poste [M§6.2].
- `gold.bv_player_outlook` : projection sur 3 saisons (à recalculer avec le potentiel estimé : signale l'écart).

## Livrable
### 1. Potentiel de chaque joueur (case E11)
Un tableau : joueur, âge, potentiel estimé (ou 2 valeurs possibles), confiance, sur combien de semaines, et ce que ça implique.
- Ce que ça implique : un potentiel élevé chez un jeune = à garder et à faire jouer ; un potentiel faible chez un jeune = monnaie d'échange.
- Rappel : le potentiel multiplie le gain, ce n'est pas un plafond [M§8.3]. Le test à 25 000 ne donne qu'une catégorie (Low, Decent, High) [M§4.2] : notre mesure est plus précise pour nos propres joueurs.
- Signale chaque écart avec `gold.bv_player_outlook` (qui suppose un potentiel 5 pour les joueurs peu observés).

### 2. Verdict hebdomadaire : garder ou changer (case E10)
Pour chaque joueur de moins de 30 ans : **garder** ou **changer**, avec la nouvelle principale et la nouvelle secondaire si besoin, et la raison chiffrée. Critères, dans l'ordre :
1. **Ralentissement** : une compétence à 75 ou plus perd du rendement (×0,88 à 75, ×0,75 à 80 [M§8.4]). Au-dessus de 80, change sauf raison forte.
2. **Utilité en match** : les compétences de l'emplacement où il joue réellement [M§7.1] et leur poids dans le PS [M§2.2]. L'endurance n'agit pas en match [M§7.1] : elle réduit seulement la fatigue [M§5.6], ce qui compte plus en v4 [News 2026-10-17].
3. **Gain réel** : il compare le gain mesuré au gain attendu. Un écart signale une blessure, un choix non sauvegardé ou une erreur d'estimation.
4. **Ne pas changer pour rien** : un choix cohérent se garde (il faut 4 à 5 semaines pour juger [Com 2026-09-01]).
- 30 ans : l'entraînement n'apporte plus rien [M§8.5], dis-le en une ligne.
- Rappel de saisie : sauvegarder avant dimanche 04:00 (Paris) [Obs].

### 3. Conseils suivis
Ajoute chaque changement conseillé dans la section Conseils de `outputs/basketvibe/learnings.md` (ID `C-nnn`, critère vérifiable : `training_primary` / `training_secondary` dans `silver.bv_player_weekly`), et contrôle les conseils d'entraînement ouverts.

## Sortie propre au jeu
- En tête du brief : la **fiche de saisie** (joueur → principale / secondaire), puis le tableau des potentiels et les justifications.
- S'il manque un relevé hebdomadaire (moins de 2 semaines consécutives), demande l'export de la page Entraînement après le dimanche.
