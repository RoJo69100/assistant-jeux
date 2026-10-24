# Six Zero League — Académie : mesure du retard et chiffrage multi-saisons, 2026-10-24

Briefs amont relus : `2026-10-24-academie.md`, `2026-10-24-finances-personnel.md`. Règles : skill `sixzeroleague-entrainement` (§ Académie U18, § L'âge), skill `sixzeroleague-club` (§ Infrastructures). Chiffres : `silver.sz_infrastructure_levels`, `silver.sz_finances`, `silver.sz_u18`, `silver.sz_standings`, `silver.sz_players`, `gold.sz_role_report`, `gold.sz_training_progress`, `silver.sz_api` (pages des autres clubs).

## 0. Deux corrections aux briefs du jour (en tête)
1. **Le solde n'est pas 6 645 €, il est de 3 045 €.** `silver.sz_finances` (2026-10-24) : `balance` 3 045 et `since_last_report` = « Youth Academy 3 -> 4, -3 600 € » (après le règlement du cycle 6, 20:15 UTC). Le 6 645 est le `closing_balance` du cycle 6, avant cet achat. Les briefs Finances et Académie partaient de 6 645 : périmé.
2. **La Youth Academy est déjà au niveau 4** (1 -> 4 en 3 jours : 2 500 + 3 000 + 3 600 = 9 100 € d'infrastructure, `gold.sz_finance_cycles` + `since_last_report`). Le verdict « ne pas monter » ne portait donc que sur le niveau 5, et il est réexaminé ci-dessous. Autre écart : `silver.sz_standings` donne 12 matchs joués pour nous (journée en cours : 13) et `rounds_until_next_pick` = 3, donc le prochain choix tombe après **J15 (26/10, 13:00 Paris)**, comme dit en C-006, pas après J14.

## 1. Retard contre les autres clubs : ce qui est mesurable
| Mesure | Nous | Autres clubs de la ligue Vanadium (9) | Verdict |
|---|---|---|---|
| Niveau d'infrastructure (Arena, Fan Shop, Training, Youth Academy) | 7 / 9 / 6 / 4 (`silver.sz_infrastructure_levels`) | **aucune donnée** : l'API d'un autre club (`/teams/<id>`) ne renvoie que nom, note, pays, bot ou non (`silver.sz_api`) | non mesurable |
| Note d'équipe (`rating`) | 11 | Miloslav Stružinsky 12 (relevé 18/10), Nenaa 11 (18/10) ; 7 clubs sans note | 2 clubs sur 9, périmé : pas de conclusion |
| Âge moyen / jeunes | 24,8 ans ; 3 joueurs de 20 ans ou moins ; 3 de 28 ans ou plus ; 2 de 30 ans ou plus (15 joueurs, `silver.sz_players`) | 0 effectif de la ligue relevé. Deux effectifs d'autres ligues seulement : un club à 24,8 ans (3 de ≤ 20 ans) et Smashing Melons à 24,1 ans (5 de ≤ 20 ans) | non comparable (autres ligues) |
| Relève par rôle | voir § 3 | rien | non mesurable |
| Clubs bots | — | 0 sur 10 (`is_bot` faux partout) : ligue 100 % humaine | à retenir : pas de faiblesse de bot à exploiter |

Conclusion honnête : **« très en retard » n'est pas démontrable sur ces données.** Ce qui est sûr : notre note (11) est dans la moyenne basse des 2 rivaux relevés, et la Youth Academy était au niveau 1 il y a 3 jours.

**Il me manque** : le niveau d'infrastructure, l'effectif (âges, rôles, retraites) et la note des 9 autres clubs de la ligue. On le réunit comme ça :
1. Ouvrir dans le jeu, avec le script Tampermonkey actif, la page d'équipe de chacun des 9 clubs, dans cet ordre : Leões do Bombarral, Pretok, voleibol aljarafe, Miloslav Stružinsky, HC Roslund, FC Cete, HB PILARES, London Legion HC, Nenaa. Chaque ouverture enregistre `/teams/<id>` (note) et `/teams/<id>/players` (âge, rôle, retraite). Les `overall` et compétences des autres joueurs sont nuls dans les captures déjà faites : seuls l'âge et le rôle seront exploitables.
2. Pendant ces ouvertures, regarder si la page d'un rival affiche ses infrastructures ; si oui, m'envoyer une capture d'écran de la page d'un club (je ne sais pas si le jeu les montre ; si non, ce point restera non mesurable et je ne ferai plus de comparaison d'infrastructures).

## 2. Chiffrage Youth Academy et Training Facilities (9 cycles par saison, fiche)
Coûts et entretien : `silver.sz_infrastructure_levels` (`weekly_maintenance` est l'entretien par cycle de 2 journées). Supplément = différence avec le niveau actuel. Coût cumulé = achat + supplément d'entretien x 9 x saisons.

**Youth Academy** (niveau 4 : 90 par cycle ; compétences des prospects 4 à 26)
| Niveau | Plage à la signature | Achat depuis 4 | Entretien en plus par saison | Coût cumulé 1 / 3 / 5 saisons | Gain moyen par prospect* |
|---|---|---|---|---|---|
| 5 | 5-28 | 4 300 | +360 | 4 660 / 5 380 / 6 100 | +1,5 par compétence |
| 6 | 6-30 | 9 500 | +765 | 10 265 / 11 795 / 13 325 | +3 |
| 7 | 7-32 | 15 700 | +1 260 | 16 960 / 19 480 / 22 000 | +4,5 |
| 8 | 8-34, 4 compétences dévoilées au lieu de 2 | 23 200 | +1 845 | 25 045 / 28 735 / 32 425 | +6 |
*Hypothèse : tirage uniforme entre min et max (moyenne = 9 + 1,5 x niveau). Le skill donne la plage, pas la loi de tirage. Seul indice : Denis Dupont, signé à 18 ans, a 10,6 de moyenne sur 20 compétences (`silver.sz_players`), cohérent avec un niveau 1 (1-20, moyenne 10,5) ; un seul cas, confiance faible.
- À titre de repère, nos 15 joueurs ont entre 8,0 et 12,5 de moyenne sur 20 compétences (Lefebvre 12,5, Denis 8,0). Un prospect de niveau 4 serait donc, en moyenne (hypothèse), à 15 : déjà au-dessus de tout l'effectif. C'est pourquoi l'académie est le levier le plus fort du club.
- Cadence : un choix toutes les 8 journées terminées, soit au plus 2 signatures par saison de 18 journées [skill entraînement § U18] ; l'horloge repart à chaque signature.
- Coût d'une signature en plus : le salaire. Notre salaire vaut environ 8 à 16 € par point de note et par cycle (`gold.sz_role_report.wage_per_point`) ; un prospect à 16 coûterait environ 130 à 250 € par cycle, soit 1 200 à 2 300 € par saison (hypothèse, salaires non écrits dans le skill). Effectif : 15 sur 30, de la place.

**Training Facilities** (niveau 6 : 1,30x, 175 par cycle)
| Niveau | Rendement | Achat | Entretien en plus par saison | Coût cumulé 1 / 3 / 5 saisons | Gain |
|---|---|---|---|---|---|
| 7 | 1,36x | 6 200 | +495 | 6 695 / 7 685 / 8 675 | +0,06 sur 1,30 = +4,6 % de points |
| 8 | 1,42x | 13 700 | +1 080 | 14 780 / 16 940 / 19 100 | +9,2 % |
| 10 | 1,54x + 2e emplacement de formation de rôle | 33 400 | +2 520 | 35 920 / 40 960 / 46 000 | +18,5 % |
- Le squad gagne en ce moment **11 à 15 points de compétence par cycle** en tout (`gold.sz_training_progress`, cycles 4 à 6 : 15, 13, 12), soit environ 110 par saison. Hypothèse (effet linéaire, non écrit dans le skill) : +4,6 % = +5 points par saison, soit environ 350 € par point sur 5 saisons (8 675 / 25).
- Comparaison : un prospect de niveau 5 vaut +1,5 x 20 = 30 points de compétence de plus qu'un prospect de niveau 4, définitifs ; à 1 signature par saison, 4 300 + 360 x 5 = 6 100 € pour 5 x 30 = 150 points, environ 40 € par point. **La Youth Academy est environ 8 fois plus rentable que les Training Facilities** (confiance moyenne : les deux calculs reposent sur des hypothèses). Le niveau 10 des Training Facilities (emplacement de formation de rôle) est hors de portée (33 400 €).
- Effet de l'âge : le gain d'entraînement baisse dès 28 ans et plus rien dès 25 ans côté bonus [skill entraînement § L'âge] : monter les Training Facilities profite surtout à Simon (19), Benoit (19), Dupont (18).

## 3. Relève par rôle sur 3 saisons (+1 an par saison [Dev chat])
| Rôle | Titulaire / remplaçant | S+1 | S+2 | S+3 | Besoin de relève |
|---|---|---|---|---|---|
| GK | Bourgeois 30 ans (11) / Blanc 26 (9) | 31 / 27 | 32 / 28 | 33 (retraite possible) / 29 | oui, un GK d'ici S+2 |
| RB | Barros 30 (10) / Roger 27 (10) | 31 / 28 | 32 / 29 | 33 / 30 | oui, un RB d'ici S+2 |
| LW | Lefebvre 27 (13) / Sundberg 29 (10) | 28 / 30 | 29 / 31 | 30 / 32 | un LW d'ici S+3 |
| CB | Simon 19 (10) / Denis 26 (8) | 20 / 27 | 21 / 28 | 22 / 29 | pas par l'âge : écart de qualité (Denis 8, moyenne des compétences clés 5,3, éthique de travail 3 sur 100) |
- Retraite possible dès 33 ans [skill entraînement § L'âge] ; perte de compétences physiques à chaque changement de saison dès 30 ans (part non chiffrée dans le skill) : Bourgeois, Barros perdent déjà à S+1 ; Sundberg à partir de S+1 (30 ans).
- **Il me manque** : la règle de tirage du rôle des prospects (non écrite dans le skill ; la fiche l'indique déjà). On le réunit comme ça : noter le rôle des 2 prospects à chaque offre dans la fiche (`silver.sz_u18.prospects`) ; après 3 offres, on aura la fréquence réelle. Tant que cette règle manque, **aucune relève par rôle n'est garantie** : l'académie ne sert qu'à ajouter de la qualité, le rôle manquant se règle au marché (agent Transferts) ou par formation à un 2e rôle.
- Calcul des places : 2 signatures par saison au maximum ; 3 retraites probables d'ici S+4 (Bourgeois, Barros, Sundberg) ; l'effectif de 15 laisse 15 places.

## 4. Ce qui manque pour rattraper
| Objectif | Niveau Youth Academy | Montant depuis 4 | Quand c'est atteignable (balance projetée 3 045 + environ 3 060 par cycle, hors victoires) |
|---|---|---|---|
| Mieux que maintenant, avant la prochaine offre | 5 | 4 300 | 25/10 au soir : balance prévue 6 143 |
| Dévoiler 4 compétences au lieu de 2 | 8 | 23 200 | 23 200 / 3 060 = environ 8 cycles de net sans autre achat, soit presque une saison de recettes (3 cycles restants cette saison, puis la saison suivante) |
| Niveau 6 (suite) | 6 | 5 200 de plus après le niveau 5 | environ 28/10, si le solde le permet |

## 5. Décision unique
**Fais : monter la Youth Academy du niveau 4 au niveau 5 le 25/10 au soir, après le règlement du cycle 7 (vers 22:15 Paris), pour 4 300 €. Solde nécessaire : 4 300 € ; solde attendu à ce moment : 6 143 € (3 045 + net prévu du cycle 7 de 3 098 € de `gold.sz_finance_projection`), soit 1 843 € après l'achat. Ne rien acheter d'autre (ni Training Facilities, ni Arena, ni Fan Shop) avant d'avoir signé le prospect de J15.**
- Pourquoi avant l'offre : les compétences se tirent « au niveau actuel de l'académie » à la signature [skill entraînement § U18] ; l'achat doit donc précéder la signature (26/10 après J15). Le prospect qui sort de J15 sera tiré avec une plage de 5 à 28 au lieu de 4 à 26.
- Pourquoi pas plus haut maintenant : le niveau 6 coûte 5 200 de plus, la balance après le niveau 5 serait de 1 843 € ; à réexaminer le 28/10 selon le solde et le prospect signé.
- Pourquoi pas les Training Facilities : environ 350 € par point contre environ 40 € par point à la Youth Academy (voir § 2).
- Risque : aucune recette ne manque (recettes de 5 328 par cycle contre dépenses de 2 230 + 40, `gold.sz_finance_projection`), donc pas de risque de solde négatif. Hypothèse faible : un match à domicile par cycle. Si le cycle 7 sort sous 4 300 €, acheter le 26/10 au soir et signer le 27/10 (un jour de perte).
- Confiance moyenne (les gains reposent sur l'hypothèse d'un tirage uniforme) ; le coût est un fait SQL.

## 6. Conseil suivi
- **C-020** (voir `outputs/sixzeroleague/learnings.md`) : Youth Academy niveau 5 le 25/10 au soir. Critère : `silver.sz_infrastructure_levels` YouthAcademy `current_level` = 5 au 26/10 ; `silver.sz_u18.prospects` non vide après J15 ; plage de compétences du joueur signé de 5 à 28.
- Remplace le volet « garder le niveau 4 » de C-015 ; la partie « exporter la page U18 après J15 » de C-015 reste valable.
