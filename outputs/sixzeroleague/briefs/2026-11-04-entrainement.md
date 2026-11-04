# Six Zero League — brief Entraînement, 2026-11-04 (cycle ce soir après la manche de 21:00 Paris)

Sources : export Équipe/Training du 2026-11-04 19:10 UTC (rapport « Week 2 »), `gold.sz_training_progress`, `gold.sz_role_report`, `gold.sz_effectif_bilan`, `silver.sz_players` (as_of 2026-11-04), `silver.sz_role_training`, `silver.sz_training_plan`. Règles : skill `sixzeroleague-entrainement` (01-fonctionnement) [W:Training]. Briefs amont du jour : aucun (dernier brief Entraînement : 2026-11-01).

## Limite de données
`silver.sz_training_plan` s'arrête au 2026-10-26 (périmé) : je ne peux pas prouver les focus saisis à l'écran. Je pars des 16 focus du 11-01 (rapport 11-03 : chaque joueur a gagné sur la compétence ciblée, donc le plan est resté en place) et je traite à part Rincón, absent du plan. Export à refaire pour fermer ça : page Équipe → Training (écran des focus) après avoir saisi.

## En tête (à faire AUJOURD'HUI avant 21:00 Paris)
- **Intensité : Normal, à garder.**
- **Un seul changement : Ramiro Rincón (LB, 18 ans, éthique 99) n'a aucun progrès enregistré (`training_progress` vide) et aucun focus connu : mets-lui Tir (Shooting).**
- **Les 16 autres focus : à garder.** Cycle 11-03 (Week 2) : 16 points, 14 joueurs, 16 sur 16 en compétence clé (`gold.sz_training_progress`). Repère C-053 (≥ 11 points dont ≥ 90 % clés) : atteint.
- Blessés Fournier, Roger, Dupont : **ne change rien à leur focus**, il reste en place pendant l'absence (un blessé ne reçoit pas de points [Dev chat 2026-10-25]). `gold.sz_role_report` les marque indisponibles.

## 1. Fiche de saisie (ordre de l'écran)
| Réglage | À mettre |
|---|---|
| Intensité d'équipe | **Normal** (garder) |
| Role training, slot 1 | **laisser libre** (garder) |
| Blanc (GK, 27) | Handling, garder |
| Bourgeois (GK, 31) | Positioning, garder |
| Simon (CB, 20) | Passing, garder |
| Denis (CB, 27) | Passing, garder |
| Fournier (CB, 19, blessé) | Passing, garder |
| Rincón (LB, 18) | **Shooting, CHANGER (aucun focus connu)** |
| A. Bertin (LB, 27) | Passing, garder |
| Leroy (LB, 25) | Shooting, garder |
| Barros (RB, 31) | Technique, garder |
| Roger (RB, 28, blessé) | Passing, garder |
| Sundberg (LW, 30) | Shooting, garder |
| Lefebvre (LW, 28) | Shooting, garder |
| G. Bertin (RW, 26) | Speed, garder |
| Dupont (RW, 19, blessé) | Shooting, garder |
| Lemaire (RW, 23) | Shooting, garder |
| Benoit (P, 20) | Shooting, garder |
| Chevalier (P, 25) | Strength, garder |
Puis Save plan seulement si Rincón a changé.

## 2. Verdict par joueur (cycle 11-03, `gold.sz_training_progress` ; « prochain » = `silver.sz_players.training_progress` sur la compétence focus)
| Joueur | Gain mesuré | Gain attendu | Prochain | Verdict |
|---|---|---|---|---|
| Blanc | Handling 13→14 (+1) | ≥ 1 | 0,94 | garder, point imminent |
| Bourgeois | 0 | ≥ 0 (1 point tous les ~2 cycles) | Positioning 0,93 | garder, point imminent |
| Simon | Passing 11→12 (+1, note +1) | +1 | 0,91 | garder |
| Denis | Passing 9→10 (+1) | +1 | 0,25 | garder (aucun coût) |
| Fournier | Passing 29→31 (+2) | +2 (éthique 90, jeune) | 0,28 | garder ; blessé, pas de points tant qu'il l'est |
| A. Bertin | Passing 17→18 (+1) | +1 | 0,92 | garder |
| Leroy | Shooting 15→16 (+1) | +1 | 0,59 | garder |
| Barros | Technique 19→20 (+1) | +1 | 0,13 | garder |
| Roger | Passing 19→21 (+2) | +1 | 0,23 | garder ; blessé |
| Sundberg | Shooting 14→15 (+1) | +1 | 0,47 | garder |
| Lefebvre | 0 | ~0,5 par cycle (éthique 2) | Shooting 0,30 | garder : rythme lent attendu, pas un focus raté |
| G. Bertin | Speed 21→22 (+1) | +1 | 0,86 | garder |
| Dupont | Shooting 25→26 (+1) | +1 | 0,80 | garder ; blessé |
| Lemaire | Shooting 18→19 (+1) | +1 | 0,46 | garder |
| Benoit | Shooting 14→15 (+1) | +1 | 0,87 | garder |
| Chevalier | Strength 14→15 (+1) | +1 | 0,58 | garder |
| Rincón | aucune donnée | — | — | focus Tir à poser (éthique 99, 18 ans : meilleur profil de progression de l'effectif, `silver.sz_players`) |
Total : 16 points au cycle 11-03 contre 17 aux cycles 10-26 et 10-28. Écart = Bourgeois et Lefebvre sans point (progrès acquis), pas un échec de focus.
- **Pourquoi Tir pour Rincón (avis, confiance faible)** : ses compétences clés LB sont Saut 25, Passe 12, Tir 16, Technique 29 (`gold.sz_role_report`). Aucune source ne dit quelle clé pèse le plus dans la note, et le rendement ne décroît pas avec le niveau [Dev chat 2026-10-19] : le choix est donc un départage. Tir est la clé qui sert directement les tirs d'arrière, et A. Bertin (Passe) et Leroy (Tir) couvrent déjà le poste en doublure. Ce qui prouverait que j'avais tort : un autre focus donne +2 par cycle quand Tir donne +1 sur 2 cycles de Rincón.
- Temps de jeu : Rincón a 0 match en feuille (`gold.sz_effectif_bilan`), alors qu'il est titulaire LB au bilan ; le temps de jeu alimente l'entraînement [Dev chat 0.5.7], donc son rythme réel se jugera après ses premiers matchs.

## 3. Intensité (confiance moyenne)
- Faits : 3 blessés au bilan (Fournier, Roger, Dupont), tous titulaires de leur poste (`gold.sz_effectif_bilan` : blesse = true). Profondeur par poste : RB 1 joueur disponible (`gold.sz_role_report` available_depth 1, no_natural_backup = true), les autres postes 2 ou 3.
- Règle : plus d'intensité = plus de blessures et plus longues [W:Training, Injuries]. Le gain et le risque de High et Light ne sont dans aucune source (C-055 toujours ouvert).
- Décision : **Normal**. Passer à High avec 3 titulaires déjà absents et RB sans doublure naturelle serait le mauvais moment. Ce qui prouverait que j'avais tort : la ligne de texte de High (C-055) donne un gain nettement supérieur pour un risque proche de 1,5 %.

## 4. Formation de rôle
Slot 1 libre (niv. 5 ; Training Facilities niv. 6, 150 € par cycle ; `silver.sz_role_training`, dernier relevé 10-23, périmé). Rien à lancer (C-054 inchangé). Le RB n'a qu'un joueur disponible, mais former un 2e rôle prend 36 journées : ce n'est pas la réponse à une absence de quelques matchs.

## 5. Conseils suivis (`outputs/sixzeroleague/learnings.md`)
- **C-053 : confirmé** sur sa partie rapport (16 points, 100 % clés au cycle 11-03). La partie plan (`sz_training_plan` day ≥ 2026-11-01) ne peut pas être vérifiée : table périmée.
- C-054, C-055 : toujours ouverts.
- **C-056 (nouveau)** : Rincón, focus Tir ; critère : `silver.sz_training_changes` (cycle ≥ 2026-11-04) une ligne Rincón Shooting, ou à défaut ≥ 1 point sur 2 cycles.
