# Six Zero League — Entraînement, 2026-10-20 (Chomelix Cow)

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
