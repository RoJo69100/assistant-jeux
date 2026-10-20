# Six Zero League — Entraînement, 2026-10-20 (Chomelix Cow)

# MISE À JOUR du soir (cycle semaine 2 réglé le 2026-10-20 à 22:15 Paris) — prime sur la suite

## À faire (avant 21:00 Paris, mercredi 2026-10-21 ; le prochain cycle se règle après J6 de 21:00)
Un seul changement : donner un focus à Sundberg. Les 12 autres restent comme au plan du 2026-10-20 (`silver.sz_training_plan`, intensité Normal).

| Joueur | Rôle | Focus actuel | Saisie | Décision |
|---|---|---|---|---|
| Intensité d'équipe | | Normal | Normal | garder |
| Nils Sundberg | LW (29 ans) | All skills (aucune ligne au plan) | **Attaque → Tir** | **changer** |
| Emmanuel Bourgeois | GK | Gardien → Placement | idem | garder |
| Sébastien Blanc | GK (apprend RW) | Attaque → Contrôle du ballon | idem | garder |
| Aurélien Simon | CB | Attaque → Passe | idem | garder |
| Frédéric Denis | CB | Attaque → Passe | idem | garder |
| Alain Bertin | LB | Attaque → Passe | idem | garder |
| Guillaume Leroy | LB | Attaque → Tir | idem | garder |
| Nicolas Roger | RB | Attaque → Passe | idem | garder |
| Jordan Lefebvre | LW | Attaque → Tir | idem | garder |
| Gabriel Bertin | RW | Physique → Vitesse | idem | garder |
| Gilbert Lemaire | RW | Attaque → Tir | idem | garder |
| Alexandre Benoit | P (blessé) | Attaque → Tir | idem | garder (rien à gagner à changer) |
| Benoît Chevalier | P | Physique → Force | idem | garder |

Formation de rôle : ne rien toucher (Blanc → RW, 7 / 36 journées, 150 € par cycle, `silver.sz_role_training` 2026-10-20).

## Verdict du cycle semaine 2 (applied_at 2026-10-20 20:15 UTC)
Faits : 9 joueurs listés, 10 points franchis ; gains de note : Simon 9→10, Denis 7→8 (`gold.sz_training_progress`). Cycle précédent (2026-10-19) : 12 points, 2 gains de note.

Les gains fractionnaires viennent de `silver.sz_player_cycles.training_progress` (relevés 2026-10-18 et 2026-10-20 20:52 UTC, soit 2 cycles) moins le gain du cycle 1 déjà mesuré dans la version du matin ci-dessous. Repère « attendu » = rendement du cycle 1 pour le même focus (le skill ne chiffre rien [W:Training]).

| Joueur (éthique) | Focus | Gain cycle 2 mesuré (points) | Attendu | Verdict |
|---|---|---|---|---|
| Roger (78) | Passe | 1,77 (Passe 5→7) | 1,76 | garder |
| G. Bertin (61) | Vitesse | 1,45 (8→9) | 1,44 | garder |
| Blanc (48) | Contrôle du ballon | 1,28 (6→7) | 1,27 | garder |
| Leroy (29) | Tir | 1,07 (5→7) | 1,08 | garder |
| A. Bertin (32) | Passe | 1,06 (9→10) | 1,07 | garder |
| Bourgeois (26) | Placement | 0,83 (4→5) | 0,83 | garder |
| Chevalier (5) | Force | 0,77, aucun point (reste 0,85 sur Force) | 0,76 | garder : point attendu au prochain cycle, pas un retard |
| Denis (3) | Passe | 0,69 (3→4, note +1) | 0,69 | garder |
| **Simon (22)** | Passe (nouveau) | **1,19 (Passe 1→2, note +1)** | 0,23 sur sa meilleure compétence en groupe Défense, 0 point | **le changement a marché** : garder |
| **Lemaire (19)** | Tir (nouveau) | **1,14 (Tir 9→10)** | 1,05 sur Jeu sans ballon | garder (rendement égal, cible désormais clé) |
| **Lefebvre (2)** | Tir (nouveau) | **0,68 (Tir 15, reste 0,70)** ; aucune ligne au rapport | 0,68 sur Jeu sans ballon | garder : rendement identique, point attendu au prochain cycle |
| Benoit (40) | Tir | **0,00** (progrès Tir inchangé à 4,51) ; aucune ligne | 1,42 au cycle 1 | blessé : voir ci-dessous |

Le changement de focus a joué dès le cycle réglé le soir même (22:15 Paris), pas « au cycle suivant » : Simon, Lemaire et Lefebvre avaient été modifiés avant 21:00 le 2026-10-20 et leurs gains portent sur la nouvelle compétence [Obs SQL 2026-10-20]. Les rendements restent proportionnels à l'éthique et à l'âge, comme le dit le skill.

### Ce que l'absence de ligne au rapport permet de conclure (sans deviner)
Une absence signifie seulement « aucun point entier franchi » [skill entraînement, rapport]. Il faut regarder le progrès fractionnaire :
- **Lefebvre** : Tir 15 + 0,70 (contre 0,03 au relevé du 2026-10-18). Il a donc bien progressé de 0,68 sur Tir ; son prochain point tombera au cycle de demain soir si le rendement tient (0,70 + 0,68 > 1). Pas de retard. Éthique 2 : le plus lent de l'équipe, par construction.
- **Chevalier** : Force 8 + 0,85. Même logique : point attendu au prochain cycle (confiance moyenne, rendement 0,77 par cycle).
- **Benoit** : blessure à 32:53 du match de 21:00 (J4, 13-10), `silver.sz_match_incidents`. Son progrès Tir est resté à 4,508 entre le relevé post-cycle 1 et celui post-cycle 2 : 0,00 de gain, alors qu'il gagnait 1,42 au cycle précédent. Observation sur un seul joueur et un seul cycle : un joueur blessé semble ne pas s'entraîner (hypothèse, le skill ne le dit pas ; confiance faible). La durée de l'absence (1 à 6 matchs [W:Injuries]) n'est pas dans nos données : ce qu'il faut vérifier dans l'écran. Tant qu'il est blessé son focus ne sert à rien mais ne coûte rien ; ne pas le changer.
- **Sundberg** : voir ci-dessous.

### Nils Sundberg (LW, 29 ans, 185 cm, droitier, note 10, salaire 95 €, éthique 28)
Correction de la demande : il est bien dans `silver.sz_players` (relevé 2026-10-20 20:52 UTC, `as_of` 2026-10-20), mais absent de `silver.sz_training_plan` (12 lignes, sans lui). Le texte brut `bronze.raw_pages` app_team (id 8535, 2026-10-20 20:57 UTC) confirme : focus « All skills », donc aucun focus (effort réparti sur les 20 compétences [W:Training]). Profil conforme à C-007 (Vitesse, Détente, Endurance à 19, salaire 95).
- Compétences clés d'ailier [W:Attributes] : Vitesse 19, Agilité 5, Tir 7, Contrôle du ballon 15 (`silver.sz_players`).
- Gain mesuré : aucune ligne au rapport de la semaine 2 ; son progrès est réparti à ~0,22 sur 11 compétences (Tir 0,215), 0,05 sur les compétences de gardien. Cela correspond à un effort dispersé sur un cycle ; je n'en tire pas plus (on ne sait pas s'il a été présent à ce cycle ni son historique chez l'ancien club).
- **Changer : Attaque → Tir.** « Le focus bat la dispersion » [W:Training]. Tir (7) est la finition principale et la plus basse des clés avec Agilité (5). Je préfère Tir à Agilité parce qu'il a 29 ans : il aura 30 ans à la fin de saison et perdra alors des compétences **physiques** à chaque changement de saison [W:Training, Players] ; Agilité en fait partie, pas Tir. À 29 ans le gain hebdomadaire est déjà réduit (dès 28 ans) : attendre ~0,8 à 1,0 par cycle, estimation faible (éthique 28 proche de Leroy 29 : 1,07 à 24 ans). Confiance faible : le skill ne donne pas de rendement chiffré. Lefebvre étant aussi sur Tir, Sundberg est la doublure du poste : sa note (10) est inférieure à celle de Lefebvre (13).

### Intensité : garder Normal (confiance moyenne)
Un blessé (Benoit) laisse Chevalier seul pivot sain ; RB et LW sont couverts un cran mieux avec Sundberg, mais High augmente blessures et durées [W:Training, Injuries], surtout arrières et pivots. Aucun chiffre de gain de High dans le skill : rien ne justifie le risque.

### Formation de rôle
Blanc → RW : 7 / 36 journées (6 au relevé du 2026-10-20 du matin ; attendu 8 : la progression est de 1 par cycle et non 2, à vérifier), 150 € par cycle. Rien à décider. Pas de second emplacement avant Training Facilities 10.

## Conseils d'entraînement (suivi, voir `outputs/sixzeroleague/learnings.md`)
- C-009 (Simon), C-010 (Lefebvre), C-011 (Lemaire) : appliqués ; effets mesurés ci-dessus.
- Nouveau : C-013 (Sundberg → Tir). Nouveau : C-014 (Benoit : vérifier la durée de blessure à l'écran).

## Données manquantes
- Durée d'absence de Benoit (écran Équipe) et date de retour.
- Prochain export Équipe → Training après le match de 21:00 du 2026-10-21 (J6) pour le cycle suivant.

À refaire si : Sundberg change de rôle ou de focus, Benoit revient plus tôt que prévu, ou un blessé de plus apparaît.

---

# VERSION DU MATIN (cycle semaine 1, périmée pour la saisie ; gardée pour l'étude de formation de rôle)

## À faire (saisie avant 21:00 Paris, mardi 2026-10-20)
Page Équipe → Training. Le cycle se règle après le match J4 de 21:00 (Nenaa) [W:Training ; Dev chat] ; un changement de focus joue au cycle suivant [W:Training].

**Fiche de saisie**
| Joueur | Rôle | Focus actuel (plan du 2026-10-18) | Saisie | Décision |
|---|---|---|---|---|
| Intensité d'équipe | | Normal | Normal | garder |
| Emmanuel Bourgeois | GK | Gardien → Placement | idem | garder |
| Sébastien Blanc | GK (apprend RW) | Attaque → Contrôle du ballon | idem | garder |
| Aurélien Simon | CB | Défense (groupe) | **Attaque → Passe** | **changer** |
| Frédéric Denis | CB | Attaque → Passe | idem | garder |
| Alain Bertin | LB | Attaque → Passe | idem | garder |
| Guillaume Leroy | LB | Attaque → Tir | idem | garder |
| Nicolas Roger | RB | Attaque → Passe | idem | garder |
| Jordan Lefebvre | LW | Attaque → Jeu sans ballon | **Attaque → Tir** | **changer** |
| Gabriel Bertin | RW | Physique → Vitesse | idem | garder |
| Gilbert Lemaire | RW | Attaque → Jeu sans ballon | **Attaque → Tir** | **changer** |
| Alexandre Benoit | P | Attaque → Tir | idem | garder |
| Benoît Chevalier | P | Physique → Force | idem | garder |

Formation de rôle : ne rien toucher (Blanc → RW continue). Pas de second emplacement avant Training Facilities 10.

**Limite des données** : le dernier plan en base date du 2026-10-18 (`silver.sz_training_plan`). Il est cohérent avec le cycle du 2026-10-19 (chaque point gagné tombe sur la compétence ciblée), donc je le crois encore en vigueur. Si tu l'as modifié depuis, ré-exporte Équipe → Training avant 21:00 ; sinon la colonne « Focus actuel » est à vérifier à l'écran.

## Verdict du cycle du 2026-10-19 (21:00, semaine 1 de la saison)
Faits : un seul cycle nouveau, 12 points franchis pour 11 joueurs sur 12 ; seuls 2 gagnent une note générale (A. Bertin, Chevalier : +1) (`gold.sz_training_progress`, applied_at 2026-10-19 20:12 UTC). Cycle précédent (2026-10-16) : 10 points, aucun gain de note. Aucun blessé (`silver.sz_players.injured` = false pour les 12, 2026-10-20).

Gain attendu : le skill ne chiffre pas de rendement ; je prends comme repère ce que l'on observe, soit environ 1 point par cycle sur une compétence ciblée seule contre ~0,05 à 0,07 sur une compétence non ciblée [Obs SQL 2026-10-18/20 ; `silver.sz_player_cycles.training_progress`]. « Le focus bat la dispersion » [W:Training].

| Joueur | Gain mesuré sur la compétence ciblée (points) | Verdict |
|---|---|---|
| Roger (éthique 78) | 1,76 (Passe 4→5, reste 0,99 : prochain point imminent) | garder, plus rapide de l'équipe |
| G. Bertin (61) | 1,44 (Vitesse 6→8) | garder |
| Benoit (40) | 1,42 (Tir 3→4) | garder |
| Blanc (48) | 1,27 (Contrôle du ballon 5→6) | garder |
| Leroy (29) | 1,08 (Tir 4→5) | garder |
| A. Bertin (32) | 1,07 (Passe 8→9, note +1) | garder |
| Lemaire (19) | 1,05 (Jeu sans ballon 2→3) | rendement bon, **cible hors clés** : changer |
| Bourgeois (26) | 0,83 (Placement 3→4) | garder |
| Chevalier (5) | 0,76 (Force 7→8, note +1) | garder |
| Denis (3) | 0,69 (Passe 2→3) | garder |
| Lefebvre (2) | 0,68 (Jeu sans ballon 3→4) | rendement bas par éthique 2, **cible hors clés** : changer |
| Simon (22) | aucun point ; 0,23 sur Anticipation (la plus avancée du groupe Défense) | **en retard, focus mal choisi** : changer |

Les rendements suivent l'éthique de travail (2 à 5 : 0,68 à 0,76 ; 61 à 78 : 1,44 à 1,76), ce que dit le skill [W:Training]. Source des gains : `silver.sz_player_cycles.training_progress` (2026-10-18 et 2026-10-20) + `gold.sz_training_progress`.

### Pourquoi ces trois changements (règle fiche n° 3 : viser les compétences clés du rôle où il joue)
- **Simon (CB, 19 ans, bonus complet [W:Training])** : focus sur le groupe Défense, qui ne contient aucune compétence clé de demi-centre (Passe, Technique, Jeu sans ballon, Tir [W:Attributes]). Son niveau : Passe 1, Jeu sans ballon 4, Technique 14, Tir 13 (`silver.sz_players`, 2026-10-20). Un groupe de 5 dilue l'effort (0,23 sur la meilleure compétence). Passe seule : c'est sa clé la plus basse et elle touche les passes ratées ou interceptées [W:Attributes]. Lien avec le match : 9 interceptions adverses et 21 pertes de balle en J2, Simon 4 fautes techniques (journal L-005, confiance faible, un seul match).
- **Lefebvre (LW)** : Jeu sans ballon n'est pas clé d'ailier (Vitesse, Agilité, Tir, Contrôle du ballon [W:Attributes]). Ses valeurs : Agilité 20, Contrôle 18, Tir 15, Vitesse 13. Tir est la compétence de finition principale et sert à désigner le tireur de 7 m [W:Attributes] ; il a tiré les 3 jets de 7 m de J2 et n'a marqué qu'1 but sur 7 tirs hors 7 m (L-006). Vitesse (13) est l'alternative si tu préfères la plus basse des clés ; Tir reste mon choix. Confiance moyenne.
- **Lemaire (RW, 22 ans)** : même défaut (Jeu sans ballon 3 n'est pas clé). Clés : Contrôle 15, Tir 9, Vitesse 8, Agilité 5 ; Tir pour la finition (6/11 sur 2 matchs, L-002). Le progrès fractionnaire déjà accumulé sur Jeu sans ballon (0,70) reste acquis [W:Training]. Confiance faible : Agilité (5) est défendable aussi.

### Intensité d'équipe : garder Normal (confiance moyenne)
High = progrès plus rapides mais plus de blessures, plus longues (~3 matchs, parfois 6) ; arrières et pivots sont les plus exposés [W:Training, Injuries]. Notre profondeur : RB et LW n'ont qu'un joueur (Roger, Lefebvre) (`gold.sz_lineup_natural`) ; une blessure sur eux force un hors-poste. Effectif de 12 joueurs. Aucun chiffre de gain de High dans le skill : je ne peux pas dire ce qu'on y gagnerait, donc rien ne justifie le risque.

## Étude : former un 2e rôle pour couvrir LW (Lefebvre) et RB (Roger)

### Faits
- 1 seul emplacement ouvert (Training Facilities niveau 6 ; emplacements aux niveaux 5, 10, 15, 20 [W:Infrastructure]). Occupant : **Blanc (GK) → RW, 6 / 36 journées, 150 € par cycle** (`silver.sz_role_training`, 2026-10-20). Il reste 30 journées, soit 15 cycles : 8 dans la saison en cours (`gold.sz_finance_projection.cycles_left`), le reste à la saison suivante.
- Anomalie à vérifier : 3 journées au relevé du 18/10 et 6 au relevé du 20/10, alors qu'un seul cycle (2 journées) est passé. Attendu après le cycle de ce soir : 8. Le coût de 150 € est négligeable (cycle net prévu 6 400 €, `gold.sz_finance_projection`).
- Cout de la formation sur 36 journées : 18 cycles x 150 = 2 700 € (non multiplié par la division [W:Competitions]) ; annuler ne rembourse rien [W:Training]. On ne sait pas si les journées déjà faites se conservent en changeant de rôle cible : le skill ne le dit pas.
- Emplacement 2 : Training Facilities niveau 10 = **33 400 €** depuis le niveau 6, entretien de 175 à 455 € par cycle (+280), et rendement d'entraînement 1,30x → 1,54x (`silver.sz_infrastructure_levels`, 2026-10-18). Trésorerie 10 531 €, fin de saison prévue 61 731 € sans victoire (`gold.sz_finance_projection`, 2026-10-20). Pas de ligne Training Facilities dans `gold.sz_infrastructure_payback` (Arena et FanShop seulement) : le retour sur investissement n'est pas calculé.
- Couverture actuelle (note par rôle avant pénalité de hors-poste, donc à lire avec prudence [Obs SQL 2026-10-18]) :

| Poste | Titulaire | Meilleurs remplaçants hors poste (note au poste) | Écart au titulaire |
|---|---|---|---|
| LW | Lefebvre 13 | Blanc 11 (GK2), A. Bertin 10 (titulaire LB), Simon 10 (titulaire CB), Benoit 10 (titulaire P) ; sans titulaire déplacé : G. Bertin 9, Chevalier 9 | -2 à -4 |
| RB | Roger 10 | Lemaire 9 (titulaire RW), Blanc 9 (GK2), A. Bertin 9, Simon 9, Benoit 9, Chevalier 8, G. Bertin 8, Leroy 7 | -1 à -3 |

  La pénalité de hors-poste est « légère » et non chiffrée [W:Attributes] ; l'écart réel est donc plus grand que celui du tableau. Tous les joueurs de champ sauf Denis sont droitiers (`silver.sz_players.preferred_hand`) : l'effet de la main forte [W:Attributes] ne départage donc personne.

### Avis
1. **Ne pas toucher à la formation de Blanc.** Sa raison d'être existe : en RW il vaut 10 contre 8 pour Lemaire et G. Bertin (`role_overalls`, avant pénalité) et la formation supprime la pénalité [W:Training]. Mais ce n'est pas la couverture demandée (RW a déjà deux naturels). Le basculer sur LW (note 11 pour lui) ferait perdre des journées et 900 € déjà versés sans garantie de report (inconnu). Confiance moyenne ; décision à toi si tu veux LW plus tôt que la saison prochaine.
2. **Pas de nouvel emplacement maintenant.** 33 400 € pour le niveau 10, avec 10 531 € en caisse. Le sujet est à arbitrer avec l'agent Finances : l'argument en faveur est le rendement +18 % pour tous (1,30x → 1,54x), pas seulement le slot. Au cycle net prévu de 6 400 € (`gold.sz_finance_projection`), il faudrait ~4 cycles pour réunir 33 400 €, sans rien dépenser d'autre (confiance faible : projection).
3. **Candidats quand un emplacement se libère** (ordre de priorité, confiance faible, notes très proches) :
   - **RB d'abord** : poste exposé aux blessures (arrières bien plus que ailiers [W:Injuries]) et sans doublure. Candidat : **Chevalier** (P2, 24 ans ; Tir 18, Technique 15, Passe 10 = clés d'arrière), doublure du pivot (Benoit est titulaire). Le skill ne dit pas si l'éthique de travail (5 chez lui) joue sur la formation de rôle.
   - **LW ensuite** : **G. Bertin** (RW2 ; Contrôle 20, Tir 13), qui deviendrait disponible quand Blanc aura terminé son RW (RW couvert à trois). Ailier = poste le moins exposé [W:Injuries] ; Lefebvre est notre meilleur joueur (13), mais la probabilité de perte est plus faible.
   - Écarté : A. Bertin (titulaire LB, mouvement de chaîne), Leroy (notes 7), Denis (7).
4. Durée : 36 journées par rôle, donc ~2 saisons : aucun de ces rôles ne sera utilisable avant la saison 3, et les joueurs prennent un an par saison [Dev chat] (Chevalier 24 → 26). Ce chantier n'a donc d'intérêt que s'il tient dans la durée ; à comparer avec un achat de joueur naturel du poste (agent Transferts), souvent plus rapide.

## Fiches : suivi des conseils ouverts
- C-001, C-003, C-004 : agent Match/Tactique, hors périmètre ici.
- Nouveaux conseils d'entraînement : C-009 à C-011 (journal `outputs/sixzeroleague/learnings.md`).

## Données manquantes
- Plan d'entraînement à jour (dernier : 2026-10-18).
- Après le cycle de ce soir : export Équipe → Training (rapport) puis agent Entraînement.
