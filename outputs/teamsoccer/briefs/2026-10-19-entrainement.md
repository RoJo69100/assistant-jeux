# Team Soccer — Entraînement, brief du 2026-10-19

## À faire (en tête)
- **Date limite : jeudi 22/10 au soir.** La mise à jour tombe le vendredi vers 00:00-01:00 UTC, soit 02:00-03:00 à Paris dans la nuit de jeudi à vendredi [skill entraînement, F:2026-07-20 PIPO68 ; l'heure exacte varie selon les messages]. Seul le réglage en place à ce moment compte.
- **20 changements** (Chomelix 9, Ben Ahmed 11), dont 2 tests (Lefebvre, Leroy, marqués TEST). Tout le reste : garder.
- Après le vendredi 23/10 : exporter les pages **Effectif et Entraînement des deux clubs** ; sans ce 2e relevé, `gold.ts_player_progress` reste vide (0 ligne au 2026-10-19) et aucun gain ne se mesure.

## Données et limites
- Relevé unique du 2026-10-19 (`silver.ts_players.day` = `silver.ts_training.day` = 2026-10-19) ; `gold.ts_player_progress` : 0 ligne.
- **Gain mesuré = `last_change` de `silver.ts_training`** : gain de la dernière séance (vendredi 16/10), entier. C'est une seule séance, arrondie : lecture indicative, pas une règle (fiche règle 5).
- `silver.ts_training` n'a pas de `team_id` : jointure sur `player_id` avec `silver.ts_players`.
- Le niveau d'entraîneur (1) n'est pas dans mes vues ; je reprends la fiche [P:Entraînement] : niveau 1 pour les deux clubs. Niveau 2 = 1 000 000 $ : décision finances, hors de ce brief.
- Titulaires = joueurs avec minutes dans `gold.ts_player_match_ratings` (2 matchs Chomelix, 3 Ben Ahmed, tous contre des bots).

## Faits clés (SQL)
1. **Gain par intensité, joueurs de 14 à 16 ans** (`silver.ts_training.last_change`, `stamina_last_change`, `pace_last_change`) : 40 % → +2 (Hugo Martin 15 ans, endurance) ; 70 % → +3 (Enzo Roux, Thomas Roux, Hana Yamamoto, Petit, Adrien Thomas…) ; **100 % → +3** (Williams, Takahashi, Kobayashi, Ben Ahmed). Le 100 % ne rapporte pas plus que le 70 % et coûte 10 de Forme au lieu de 2 (Forme de ces trois joueuses : 90). Échantillon : 3 joueuses à 100 %. Confiance **faible à moyenne** (+3 peut être un plafond d'affichage).
2. **Gain par âge à 70 %** : 14-20 ans +3 ; 21-26 ans +2 à +3 ; 25-28 ans +1 à +2 (Dubois 27 ans +1, Hayashi et Ibe 28 ans +1) ; **Pierre Leroy 32 ans à 40 % : −2** (progression −0,235) ; Louis Lefebvre 28 ans à 40 % : 0. Concordant avec le tableau d'âge du skill (perte dès 30 ans, rien à 28) [skill entraînement, G:Entraînements].
3. **Forme actuelle** (`silver.ts_players.forme`) : Chomelix titulaires 98, jeunes 74, Étienne Roux (FWD 19 ans) **46** ; Ben Ahmed adultes 84, jeunes 90 à 98.
4. **Matchs** (`gold.ts_upcoming`) : Chomelix coupe 21/10 (bot), coupe 22/10 (Luku Bratislava, humain), ligue 24/10 (Ballon Athletique hawaien 65,65), 27/10 (bot), **31/10 (FC Bresse 81,87)**, **3/11 (Godly Eleven 87,17)** ; Ben Ahmed : bots seulement jusqu'au 12/11 (60).

## Règles utilisées
- Forme par intensité : 100 % −10, 90 % −6, 80 % −4, 70 % −2, 60 % 0, 50 % +6, ≤ 40 % +10 ; 30 ans et plus −2 de plus à 80-100 % [skill entraînement, F:2026-06-27 Admin-Dev].
- Multiplicateur de match 0,70 + 0,30 × Forme / 100 [skill joueurs, F:2026-06-27 Admin-Dev].
- Physique : ne monte plus seul depuis fin septembre ; Endurance ≤ 30 : seul l'entraînement d'Endurance est possible [F:2026-10-09 PIPO68, P:Entraînement].
- Compétences clés par poste [skill joueurs, G:Commencer à jouer 2.1] ; pondération exacte de l'OVR non connue [F:2026-09-23 PIPO68].
- Note de match calculée dans le sous-rôle **naturel**, défini par la plus haute des 4 compétences Gardien / Défense / Conduite / Finition [skill joueurs, G:Effectif].

---

## Chomelix Cows (team 18) — fiche de saisie

Intensité : 70 % par défaut, sauf indication. Rappel : compétences à 100 déjà atteintes = pas d'intérêt à les entraîner.

| Joueur | Âge | Poste | Réglage actuel | **Saisie** | Décision | Raison |
|---|---|---|---|---|---|---|
| Romain Thomas | 23 | GB | Passe 70 | **Contrôle 70** | CHANGER | Gardien 100 ; Contrôle (66) est la 2e clé du gardien ; Passe n'est que secondaire |
| Noussair Ounahi | 19 | LAT | Centres 70 | **Conduite 70** | CHANGER | Défense et Contrôle à 100, Physique à 100 ; Conduite (68) est secondaire de latéral, Centres seulement de piston |
| Nicolas Simon | 21 | LAT | Conduite 70 | **Contrôle 70** | CHANGER | Défense 100 ; Contrôle (71) est la 2e clé du latéral |
| Théo Thomas | 21 | DC | Vitesse 70 | Vitesse 70 | GARDER | Choix physique cohérent (+2 vitesse mesuré) ; Physique requis partout |
| Théo Dubois | 27 | DC | Passe 70 | **Contrôle 70** | CHANGER | Défense 100 ; Contrôle (69) est la 2e clé du DC ; gain attendu faible (+1 à 27 ans) |
| Lucas David | 26 | MC | Passe 70 | **Contrôle 70** | CHANGER | Conduite 100 et Passe 89 déjà hautes ; Contrôle (58) est secondaire de milieu |
| Clément Robert | 25 | MC | Passe 70 | Passe 70 | GARDER | Conduite 100 ; Passe (57) secondaire, note 7,4 |
| Adrien Roux | 25 | EXT | Centres 70 | Centres 70 | GARDER | Conduite 100 ; Centres secondaire d'ailier, note 8,9 |
| Adrien Thomas | 14 | EXT/MC | Passe 70 | **Endurance 70** | CHANGER | Endurance 35 (alerte ≤ 35) pour un titulaire de 90 min ; la fatigue en match dépend de l'Endurance [skill joueurs] ; +3 attendu à 14 ans |
| Lucas Moreau | 20 | AC | Contrôle 70 | Contrôle 70 | GARDER | Finition 100 ; Contrôle 81, 2e clé |
| Mathis David | 25 | AC | Contrôle 70 | Contrôle 70 | GARDER | idem |
| Pierre Bonnet | 24 | AC | Vitesse 70 | Vitesse 70 | GARDER | Choix physique cohérent (+2 vitesse mesuré) |
| Étienne Roux (FWD) | 19 | AC | Endurance 40 | Endurance 40 | GARDER | **Forme 46** : 40 % donne le maximum (+10) ; 46 → 56 le 23/10, 66 le 30/10 ; ne pas l'aligner avant ~66 |
| Louis Lefebvre | 28 | AC | Endurance 40 | **Endurance 100 (TEST)** | CHANGER (test) | Endurance 28 ≤ 30 : seule l'Endurance est possible ; +0 mesuré à 40 % ; il ne joue pas, la Forme (100) ne coûte rien ; teste si l'intensité fait bouger un joueur de 28 ans. Si +0 encore : cas clos |
| Pierre Leroy | 32 | DC (banc) | Défense 40 | **Défense 0 (TEST)** | CHANGER (test) | −2 mesuré à 40 % ; Forme 100 déjà au plafond, rien à perdre ; mesure si 0 % évite la perte d'âge (non établi) |
| Hugo Martin | 15 | GB | Endurance 40 | **Endurance 70** | CHANGER | Endurance 31, +2 à 40 % contre +3 à 70 % chez les 14-17 ans ; Forme 100, il ne joue pas |
| Enzo Roux (DEF) | 16 | DC | Défense 70 | Défense 70 | GARDER | +3 mesuré, plein gain à 16 ans |
| Thomas Roux | 16 | AC | Finition 70 | Finition 70 | GARDER | +3 mesuré |
| Étienne Roux (GB) | 14 | GB | Gardien 70 | Gardien 70 | GARDER | +3 mesuré |
| Thomas David | 17 | GB | Gardien 70 | Gardien 70 | GARDER | +3 mesuré |
| Thomas Petit | 14 | MC | Conduite 70 | Conduite 70 | GARDER | +3 mesuré |
| Jules Leroy | 17 | MC | Passe 70 | Passe 70 | GARDER | +3 mesuré |
| Nathan Lefebvre | 18 | MC | Passe 70 | Passe 70 | GARDER | +3 mesuré |

Ounahi : le joueur le plus important (L-002) a déjà ses 3 compétences-clés à 100 ou presque, d'où le passage à Conduite. Les titulaires dont j'ai changé la cible n'ont pas d'intensité modifiée.

## Ben Ahmed Donkey (team 15858) — fiche de saisie

| Joueur | Âge | Poste | Réglage actuel | **Saisie** | Décision | Raison |
|---|---|---|---|---|---|---|
| Ama Schmidt | 21 | MC (GB natif) | Passe 70 | **Conduite 70** | CHANGER | Titulaire au milieu, note 5,4 (L-007) ; Conduite 60 est la 1re clé du milieu ; les 4 compétences de poste sont toutes à 60, donc le poste « naturel » (GB) n'est qu'un ex æquo : monter Conduite la rend naturellement milieu et la note se calcule dans ce rôle [skill joueurs, G:Effectif] |
| Lena Suzuki | 22 | MC (GB natif) | Passe 70 | **Conduite 70** | CHANGER | idem |
| Momoka Martínez | 22 | EXT | Centres 70 | **Conduite 70** | CHANGER | Centres 81 déjà haut ; Conduite 60 = clé d'ailier et de milieu (C-006) |
| Oluwaseun Mansour | 23 | EXT/MC | Centres 70 | **Conduite 70** | CHANGER | idem ; 6 ballons perdus en 3 matchs |
| Uchenna Kumar | 24 | MC | Centres 70 | **Conduite 70** | CHANGER | idem ; Centres 79 |
| Yuki Fernández | 23 | LAT | Défense 70 | Défense 70 | GARDER | Défense = 1re clé, +3 mesuré |
| Anna Fournier, Nour Taylor | 26 | DC | Défense 70 | Défense 70 | GARDER | +2 mesuré |
| Salma Girard | 27 | DC | Défense 70 | Défense 70 | GARDER | +2 mesuré |
| Kavya Hayashi, Suki Ibe | 28 | DC (réserve) | Défense 70 | Défense 70 | GARDER | +1 mesuré ; elles ne jouent pas, Forme sans enjeu (alerte 28 ans et plus notée, aucun coût réel) |
| Marie Müller | 20 | AC | Finition 70 | Finition 70 | GARDER | +3 mesuré, Finition 85 = clé |
| Juliette Yamamoto | 21 | AC | Finition 70 | Finition 70 | GARDER | +2 mesuré |
| Adaeze Wilson | 25 | AC (réserve) | Passe 70 | **Finition 70** | CHANGER | Finition 60 = clé d'avant-centre ; C-007 : partager la finition avec Yamamoto |
| Ingrid Shimizu | 27 | AC (réserve) | Passe 70 | **Finition 70** | CHANGER | idem |
| Zainab Mori | 16 | AC | Passe 70 | **Finition 70** | CHANGER | Finition 49 = clé ; plein gain à 16 ans |
| Chae Abdel | 24 | GB | Gardien 70 | Gardien 70 | GARDER | +2 mesuré |
| Rania Fournier | 14 | GB | Gardien 70 | Gardien 70 | GARDER | +3 mesuré |
| Hana Yamamoto | 14 | DC | Défense 70 | Défense 70 | GARDER | +3 mesuré |
| Valentina Williams | 14 | DC | Vitesse 100 | **Vitesse 70** | CHANGER | +3 à 100 % comme à 70 % chez les 14 ans ; Forme 90 → 88 au lieu de 80 |
| Natalia Takahashi | 14 | AC | Endurance 100 | **Endurance 70** | CHANGER | Endurance 27 ≤ 30 : Endurance seule possible, reste ; +3 mesuré à 100 %, même gain attendu à 70 % ; Forme 90 → 88 |
| Mariana Kobayashi | 15 | MC | Endurance 100 | **Endurance 70** | CHANGER | Endurance 29 ≤ 30 ; idem ; elle a joué 1 match (EXT) |

Le niveau d'équipe pèse peu : Ben Ahmed ne joue que des bots (60) jusqu'au 12/11 (`gold.ts_upcoming`), donc la Forme des titulaires (84 → 82 à 70 %) n'a pas d'enjeu immédiat.

---

## Verdict et gestion de la Forme

**Garder 70 % pour les titulaires des deux clubs.** À 70 %, −2 de Forme par vendredi (30 ans et plus : −2 de plus à 80-100 %, aucun titulaire concerné) :
- Chomelix titulaires 98 → 96 le 23/10 (×0,988) → 94 le 30/10 (×0,982). Écart avec la Forme actuelle : 1,2 point de multiplicateur [formule skill joueurs].
- Ben Ahmed titulaires 84 → 82 (×0,946) puis 80.
- **Point de décision le jeudi 29/10 au soir** (avant Bresse 31/10 et Godly Eleven 3/11, adversaires à 81,87 et 87,17) : si le gain mesuré le 23/10 est faible, passer les titulaires à 60 % (Forme 0) pour garder 96. Je ne chiffre pas le coût en progrès : aucun relevé à 60 %.
- Pas de 80 % ni 100 % : le gain de 100 % n'est pas supérieur au 70 % chez les 14-16 ans (fait 1), le coût Forme est de −4 à −10. À vérifier sur les adultes quand on aura un 2e relevé.

**Joueurs à reposer ou surveiller (Forme < 60)** : Étienne Roux (FWD, Chomelix) 46 → 56 le 23/10, 66 le 30/10 (cohérent avec C-002). Aucun autre joueur sous 60.

**Alertes (fiche)**
- Endurance ≤ 35 : Chomelix, Adrien Thomas 35 (titulaire), Étienne Roux (GB) 35, Hugo Martin 31, Louis Lefebvre 28 ; Ben Ahmed, Takahashi 27, Kobayashi 29 (les deux ≤ 30 : Endurance seule).
- 28 ans et plus à haute intensité : Hayashi et Ibe (Ben Ahmed) à 70 %, +1 mesuré, réserves, risque nul. Pierre Leroy (32 ans) perd 2 par séance même à 40 % : test à 0 %.
- Forme < 60 : Étienne Roux (FWD).

**Gain mesuré contre attendu** : un seul relevé, donc pas de verdict chiffré par joueur. Attendu = +3 pour les 14-20 ans, +2 pour 21-26, +1 pour 27-28, négatif à partir de 30 (skill, tableau d'âge) ; mesuré : conforme dans les 3 tranches (faits 1 et 2), sauf Théo Dubois 27 ans (+1, conforme) et Étienne Roux FWD (+2 d'endurance à 40 %, conforme). À refaire avec le relevé suivant.

## Potentiel
Non prévu par la fiche pour ce jeu : non traité.

## Autres rappels (hors entraînement)
- HPC : 45 TSC disponibles, 0 investi, décision Premium à l'utilisateur [skill entraînement, P:Haute Performance].
- Chomelix : effectif 23/24 (une seule place pour monter un jeune de l'académie) [P:Académie].

## Conseils suivis
Nouveaux conseils C-009 à C-013 ajoutés à `outputs/teamsoccer/learnings.md`. Conseils d'entraînement ouverts avant ce passage : aucun ; C-002 (Étienne Roux, Forme 46) concerne la composition et reste ouvert.
