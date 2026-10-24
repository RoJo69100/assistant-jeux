# Team Soccer — brief Entraînement du 2026-10-24

Agent Entraînement (medium + Sonnet). Fiches : `commun.md`, `entrainement.md` ; skills `teamsoccer-entrainement`, `teamsoccer-joueurs`. Briefs amont lus : Match, Effectif, Finances-personnel, Académie du 24/10. Delta : brief Entraînement du 23/10 (réglages C-017 à C-021).
Vues : `silver.ts_training` (T, relevé 24/10 20:13 UTC, 44 lignes = 22 + 22), `silver.ts_players` (J, 24/10), `gold.ts_player_progress` (PP), `silver.ts_teams` (entraîneur).

## En tête : verdict
| Point | Constat |
|---|---|
| Urgence | **Aucune avant vendredi.** La mise à jour est hebdomadaire, le vendredi ; seul compte le réglage en place à ce moment [skill entraînement, F:2026-07-20 PIPO68]. |
| Échéance exacte | **Vendredi 30/10, vers 00:00-01:00 UTC** [skill entraînement]. Je compte la marge sur 00:00 UTC : tout saisi **avant jeudi 29/10 23:00 Paris** (Paris passe à l'heure d'hiver le 25/10, soit 01:00 Paris = 00:00 UTC ; conversion de mon calcul, pas du skill). |
| Changements à saisir | **Aucun.** T du 24/10 montre les 8 réglages du 23/10 déjà saisis (liste ci-dessous). Pas de relevé postérieur au vendredi 23/10 : rien de nouveau à mesurer avant le 30/10. |
| Entraîneur | Niveau 1 « poor » pour les deux clubs (`ts_teams.coach_level_label`, 24/10). Niveau 2 = 1 000 000 $ [skill entraînement] : non acheté (brief Finances : réserve de 2 semaines de charges non tenue pour Ben Ahmed ; Cows possible après le 26/10 mais sans l'agrandissement du stade en même temps). |

## Contradictions avec les briefs amont (relance Effectif)
| Brief Effectif | T / J du 24/10 |
|---|---|
| « huit jeunes à 72 » de Forme chez les Cows | **5** à 72 : Enzo Roux (DEF 16), Thomas Roux (ATT 16), Thomas David (GB 17), Jules Leroy (MIL 17), Nathan Lefebvre (MIL 18). Les autres jeunes sont à 96-98. |
| Ounahi « Conduite 100 », Moreau « Conduite 84 » | Ounahi : Conduite **71**, Contrôle **100**. Moreau : Conduite 63, Contrôle **84**. L'Effectif a pris Contrôle pour Conduite (même confusion possible ailleurs). |

## Contrôle de la saisie (C-017, C-018) : appliqué
| Club | Joueur | Réglage voulu (23/10) | T du 24/10 |
|---|---|---|---|
| Cows | Romain Thomas, Adrien Roux, Pierre Bonnet | Contrôle 70 % | Contrôle 70 % (conforme) |
| Cows | Jules Leroy, Adrien Thomas, Nathan Lefebvre | Conduite 70 % | Conduite 70 % (conforme) |
| Cows | Pierre Leroy | Défense 0 % | Défense 0 % (conforme) |
| Ben Ahmed | Ama Schmidt, Lena Suzuki | Conduite 70 % | Conduite 70 % (conforme) |
`last_trained_type` montre encore l'ancien type (passing, crosses, pace) : c'est la séance du 23/10, pas la prochaine. Les gains du nouveau type se lisent au relevé du 30/10.

## Règles utilisées (sources)
- Gains par âge à 70 % mesurés (T, séance du 23/10) : 14-20 ans +3 ; 21-26 +2 (Simon, Théo Thomas 21 ans : +2 ; Müller 20, Yamamoto 21, Schmidt 21 : +3) ; 27-28 +1 (Girard, Shimizu, Hayashi, Ibe) ; Pierre Leroy 32 ans à 0 % : −2. Un seul cycle : confiance moyenne [fiche règle 5].
- Forme au vendredi : 70 % = −2, 60 % = 0, 50 % = +6, ≤ 40 % = +10 ; 30 ans et + : −2 de plus à 80-100 % [skill entraînement, F:2026-06-27 Admin-Dev]. Confirmé en mesure : PP du 23/10 (−2 à 70 %, +10 à 40 %).
- Aucune perte d'Endurance/Vitesse chez les joueurs entraînés en technique à 70 % (`stamina_last_change` et `pace_last_change` = 0 sauf pour les joueurs entraînés en physique) [Obs T].
- Seuil critique : Endurance ≤ 30 → seule l'Endurance est entraînable [P:Entraînement, skill entraînement].

## 1. Chomelix Cows (team_id 18)

### Fiche de saisie (gymnase) : aucun changement
| Joueur | Âge | Réglage en place (T) | Décision |
|---|---|---|---|
| Noussair Ounahi (DEF) | 19 | Conduite 70 % (71) | Garder (+3) |
| Nicolas Simon, Théo Thomas (DEF) | 21 | Contrôle 70 % (73 / 61) | Garder (+2) |
| Théo Dubois (DEF) | 27 | Contrôle 70 % (71) | Garder (+2 mesuré) |
| Romain Thomas (GB) | 23 | Contrôle 70 % (66) | Garder |
| Adrien Roux, Lucas David (MIL) | 25, 26 | Contrôle 70 % (55 / 60) | Garder |
| Clément Robert (MIL) | 25 | Passe 70 % (59) | Garder (Contrôle 57 en parallèle : écart de 2, pas de preuve pour changer) |
| Lucas Moreau (ATT) | 20 | Contrôle 70 % (84) | Garder (+3) |
| Mathis David (ATT) | 25 | Contrôle 70 % (84) | Garder (+2) |
| Pierre Bonnet (ATT) | 24 | Contrôle 70 % (61) | Garder |
| Jules Leroy (MIL) | 17 | Conduite 70 % (86) | Garder (+3) |
| Adrien Thomas, Thomas Petit (MIL) | 14 | Conduite 70 % (77 / 72) | Garder (+3) |
| Nathan Lefebvre (MIL) | 18 | Conduite 70 % (73) | Garder (+3) |
| Enzo Roux (DEF) | 16 | Défense 70 % (85) | Garder |
| Thomas Roux (ATT) | 16 | Finition 70 % (82) | Garder |
| Thomas David (GB) | 17 | Gardien 70 % (89) | Garder |
| Étienne Roux (GB) | 14 | Gardien 70 % (72) | Garder ; Endurance 35 |
| Hugo Martin (GB) | 15 | Endurance 70 % (34) | Garder |
| Pierre Leroy (DEF) | 32 | Défense 0 % (61) | Garder (Forme 100 ; −2 par semaine, C-021) |
| Étienne Roux (ATT) | 19 | Endurance 40 % (67) | Garder (voir ci-dessous) |

### Formes à 72 (les 5 jeunes) : on ne touche à rien
- Faits (J, 24/10) : Enzo Roux, Thomas Roux, Thomas David, Jules Leroy, Nathan Lefebvre = 72 (×0,916). Au vendredi 30/10 à 70 % : 72 → 70 (×0,910) ; 6/11 : 68 ; 13/11 : 66 ; 20/11 : 64 ; 27/11 : 62 (arithmétique de la table, jamais sous 30).
- Avis : la différence de rendement entre 72 et 70 est de 0,6 point de pourcentage (×0,916 contre ×0,910) ; aucun des cinq n'est titulaire. Seuls Thomas David (banc GB) et Jules Leroy (banc MIL) peuvent entrer en cours de match, et un remplaçant entre avec son plafond de Forme [skill joueurs]. Le gain +3 par semaine (16-18 ans, pleins gains) vaut plus que 0,6 point de rendement. **Décision : 70 % maintenus.**
- Pour remonter la Forme de l'un d'eux il faudrait 50 % (+6) ou ≤ 40 % (+10) : je ne le fais que le jour où l'un devient titulaire (Jules Leroy est le candidat milieu, brief Effectif ; il passerait alors à ≤ 40 % deux semaines avant le match). Gain à 50 % et 40 % : non mesuré chez nous (il me manque la valeur ; on la réunit en passant un seul jeune à 50 % la semaine où il n'est pas nécessaire, lecture au relevé suivant).

### Étienne Roux (ATT, 19 ans, Forme 56) : à vendre après le 25/10
- Réglage en place : Endurance 40 % → Forme 56 → **66 au vendredi 30/10** (+10), 76 au 6/11 [skill entraînement, table ; PP du 23/10 : +10 mesuré]. Plan du 23/10 conservé (C-019).
- Si la vente à la banque est faite avant le vendredi 30/10, ce réglage ne sert plus : rien à saisir. S'il est encore au club le 29/10, **ne rien changer** : l'Endurance 67 ne baisse pas et la Forme remonte. Il reste hors composition tant que Forme < 70 (C-002).
- Il me manque l'effet de la Forme sur le prix de vente à la banque : le skill club ne le dit pas, je ne l'affirme pas (valeur « fondée sur les compétences, l'OVR et le poste » [skill joueurs, F:2026-07-12 Admin-Dev]). Je ne peux donc pas dire si attendre le 30/10 (Forme 66) change son prix ; on le réunit en lisant sa valeur sur la fiche avant et après le 30/10 s'il est encore là.

### Formes des titulaires
- XI à 96 (×0,988) → 94 au 30/10 (×0,982) à 70 %. Coût 0,6 point pour +2 à +3 points de compétence par semaine : on garde 70 % (décision du 23/10, aucune donnée nouvelle).
- Milieu mince : les trois jeunes MIL (Jules Leroy 49,2, Lefebvre 44,7, A. Thomas 44,4) sont tous sur Conduite, la compétence principale du milieu [skill joueurs] ; projection du 23/10 inchangée (confiance moyenne).

### Alertes
| Alerte | Joueur |
|---|---|
| Endurance ≤ 30 | aucun (plus bas : Hugo Martin 34) |
| Endurance ≤ 35 | Hugo Martin 34 (entraîne l'Endurance), Adrien Thomas 35, Étienne Roux (GB) 35 |
| Forme < 60 | Étienne Roux (ATT) 56 |
| 28 ans et + à haute intensité | aucun (Pierre Leroy 32 ans à 0 %) |

## 2. Ben Ahmed Donkey (team_id 15858)

### Fiche de saisie (gymnase) : aucun changement
| Joueuse | Âge | Réglage en place (T) | Décision |
|---|---|---|---|
| Marie Müller, Juliette Yamamoto (ATT) | 20, 21 | Finition 70 % (88 / 87) | Garder (+3) |
| Adaeze Wilson, Ingrid Shimizu (ATT) | 25, 27 | Passe 70 % (80 / 77) | Garder (poste naturel indéterminé, toutes les compétences de poste à 60 ; aucune preuve pour mieux) |
| Ama Schmidt, Lena Suzuki (GB listées) | 21, 22 | Conduite 70 % (60 / 60) | Garder (C-018) |
| Kumar, Mansour, Martínez (MIL) | 24, 23, 22 | Conduite 70 % (62) | Garder (+2) |
| Chae Abdel (GB) | 24 | Gardien 70 % (81) | Garder |
| Yuki Fernández (DEF) | 23 | Défense 70 % (83) | Garder (+2) |
| Anna Fournier, Nour Taylor (DEF) | 26 | Défense 70 % (79) | Garder (+2) |
| Salma Girard (DEF) | 27 | Défense 70 % (77) | Garder (+1) |
| Kavya Hayashi, Suki Ibe (DEF) | 28 | Défense 70 % (72) | Garder jusqu'à la vente prévue après le 28/10 (C-025) ; +1 mesuré |
| Rania Fournier (GB) | 14 | Gardien 70 % (71) | Garder |
| Hana Yamamoto (DEF) | 14 | Défense 70 % (64) | Garder |
| Zainab Mori (ATT) | 16 | Passe 70 % (60) | Garder |
| Natalia Takahashi (ATT), Mariana Kobayashi (MIL) | 14, 15 | Endurance 70 % (31 / 33) | Garder |
| Valentina Williams (DEF) | 14 | Vitesse 70 % (36) | Garder |

### Formes
- Seniors à 82 (×0,946). Vendredi 30/10 à 70 % : 80 ; 6/11 : 78. Matchs du 26/10 et 28/10 avec Forme 82 (aucune mise à jour avant le 30/10).
- **Règle déjà fixée (C-019), non avancée** : à l'export où les titulaires sont ≤ 78 (attendu le 6/11), passer à 60 % (Forme stable) sauf Müller et J. Yamamoto, à 70 % tant que Finition < 95. Raison : à 78 le −2 coûte plus en rendement que +1 ou +2 points ne rapportent.
- Pas de Forme < 60 ; jeunes 88-96.

### Alertes
| Alerte | Joueuse |
|---|---|
| Endurance ≤ 30 | aucune (plus basse : Takahashi 31, une marge de 1 point) |
| Endurance ≤ 35 | Takahashi 31 et Kobayashi 33, toutes deux déjà en Endurance à 70 % (+4 par semaine mesuré) : hors zone au 30/10 pour Takahashi (35 attendu : limite) |
| 28 ans et + à haute intensité | Hayashi, Ibe à 70 % : 70 % n'est pas « haute » à leur âge (pas de −2 de plus avant 30 ans) ; vente prévue |

## 3. Données manquantes
| Donnée | Pourquoi | On la réunit comme ça |
|---|---|---|
| Gain réel à 50 % et 40 % pour la technique | seule la Forme est mesurée à ces intensités (Étienne Roux, physique) | un jeune non titulaire à 50 % une semaine, lecture de `last_change` au relevé suivant |
| Effet chiffré d'un point d'Endurance sur la baisse par 5 min | le skill donne −9 / −16 points sur 90 min, sans barème par point | comparer, après un match, des titulaires d'Endurance 55 (Dubois) et 72 (Moreau) dans le rapport v3 (force en direct) : à demander à l'export du rapport |
| Effet de la Forme sur le prix de vente | non écrit dans le skill club | valeur d'Étienne Roux avant et après le 30/10 |
| Relevé après le vendredi 30/10 | prochain verdict | export Effectif + Entraînement des deux clubs le 30/10 après la mise à jour |

## 4. Conseils suivis (journal `outputs/teamsoccer/learnings.md`)
- C-017 : appliqué (T du 24/10), effet à lire le 30/10 (`last_change` ≥ 2 pour les trois jeunes en Conduite).
- C-018 : appliqué (T du 24/10) ; critère Conduite de Schmidt ≥ 69 au 13/11.
- C-019, C-021 : ouverts, premier relevé le 30/10.
- C-033 (nouveau) : aucune modification du gymnase avant le 30/10 ; tout est saisi.

## Réserves
Faits : T, J, PP, `ts_teams` du 24/10. Règles : skills entraînement et joueurs. Avis : maintien des 70 %, absence de changement. Confiance moyenne : un seul cycle de gains mesuré. Le tableau « Étienne Roux, 19 ans, Forme 56 » vient de l'Effectif, recoupé avec J.
