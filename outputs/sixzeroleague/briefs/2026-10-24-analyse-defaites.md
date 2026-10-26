# Six Zero League — analyse détaillée des défaites J11 (17-27) et J12 (18-28), 2026-10-24

Briefs amont lus : `2026-10-24-match.md`, `-match-j12.md`, `-effectif.md`, `-tactique-j13.md`, `learnings.md`. Sources chiffrées : `silver.sz_matches`, `sz_match_players`, `sz_match_incidents`, `sz_players` (as_of 2026-10-24), `sz_fixtures`, et les clés de `silver.sz_api` (endpoint `/matches/<id>/stats`). Résultat lu par `result` (L) dans `sz_matches` et par `sz_fixtures.is_mine`. Règles : skills `sixzeroleague-match` [W:Match] et `sixzeroleague-joueurs` [W:Attributes, Injuries].

## En tête (ce qu'il faut retenir)
- **Les deux défaites se jouent avant la pause** : 8-20 (J11) et 6-14 (J12). Deuxièmes mi-temps : 9-7 (J11, gagnée) et 12-14 (J12). Sur les 5 défaites de la saison, la 1re mi-temps vaut -6,2 buts en moyenne (J6 -4, J8 -8, J10 +1, J11 -12, J12 -8) contre +0,4 dans les 7 victoires ; la 2e mi-temps vaut 0,0 en défaite contre +1,9 en victoire (`sz_match_incidents`, `half-time`). Ce n'est donc pas une question d'endurance ou de fatigue de fin de match.
- **J11 = conversion (36,2 % contre 58,7 %) + gardien (20,6 % contre 45,2 %). J12 = gardien (15,2 % contre 33,3 %) + volume (38 tirs contre 49, 15 pertes contre 8).** Aucun changement de composition ni de réglage entre les deux : mêmes 7, 5-1 / 6-0 (`sz_match_players`, `sz_matches`).
- **Discipline et pertes de balle ne séparent PAS victoires et défaites** (tableau § 4) : le levier n'est pas là. Ce qui sépare : efficacité adverse (50,3 % en victoire, 59,2 % en défaite) et arrêts de Bourgeois (36,5 % contre 23,7 %).
- **Il me manque** (données absentes de l'export, vérifié dans `silver.sz_api`, clés de l'endpoint : `teams`, `players`, `incidents`) : (1) la **zone de chaque tir** hors 7 m (9 m, 6 m, ailes) : seuls les buts de 7 m sont distingués (`detail = '7m'`) ; (2) les **minutes jouées** par joueur ; (3) les **pertes de balle par joueur** (équipe seulement ; je prends les fautes techniques comme repère). On les réunit comme ça : ouvre un match en direct (bouton Live) et dis-moi si l'écran donne la zone ou le type de chaque tir ; sinon la zone ne peut pas être reconstituée et je ne la déduirai pas. Minutes : les 7 titulaires ont 60 min (7 lignes `sz_match_players`, aucune entrée de remplaçant, donc aucun remplacement ; c'est une déduction, pas une donnée).

## 1. J11 — HB PILARES (domicile, 17-27, 8-20 à la pause)
### Minute par minute (`sz_match_incidents`, nous en premier)
| Phase | Score | Ce qui s'est passé |
|---|---|---|
| 0:00-1:12 | 1-1 | Simon 0:42 ; Tavares 1:12 |
| **4:42-11:00** | 1-1 -> **1-6** (série 0-5, 6 min 18 s) | Moreira 4:42, Branco 6:00, **Tavares 7 m 8:18** (après exclusion de Simon à 8:00), Dias 9:00, Branco 11:00. Simon jaune à 4:36. Aucun but de chez nous de 0:42 à 11:18 (10 min 36 s) |
| 11:18-11:48 | 3-6 | Simon, Leroy (2-0) |
| **12:06-13:42** | 3-6 -> **3-9** (série 0-3) | Branco, Dias, Tavares |
| 13:48-14:00 | 4-10 | Simon 4-9 ; **Dupont exclu 13:54 et Simon exclu 14:00** (deux joueurs en moins) ; **Tavares 7 m 14:00** ; puis 4 min 18 s sans but de chez nous (Chevalier 18:36) |
| 18:18-21:42 | 6-12 -> **6-16** (série 0-4 en 2 min 18 s) | Salgueiro 19:42, Dias 20:30, Moreira 21:30, Dias 21:42 (juste après Chevalier 18:36 et Lefebvre 19:24) |
| 22:48-29:48 | 7-16 -> 8-20 | Lefebvre, Tavares, Simon ; **Chevalier exclu 27:18 puis Tavares 7 m 27:18** ; Salgueiro 28:42 ; Tavares 29:48 (série 0-3 de fin de période) |
| 2e mi-temps | 8-20 -> 17-27 (9-7) | 13 min sans but de chez nous (30:00 à 43:18) mais seulement 2 pour eux ; puis 3-0 (43:18 à 44:54) ; leurs buts : Branco, Salgueiro, Guedes, Tavares x2, Dias, Moreira |
- Les 3 jets de 7 m de Tavares (3/3) ont tous suivi une exclusion de chez nous, à la même seconde ou à 18 s près (Simon 8:00, Dupont/Simon 13:54-14:00, Chevalier 27:18). Cohérent avec [W:Match] (une faute qui donne un 7 m entraîne plus souvent l'exclusion) ; causalité non prouvée (L-012).
- Fait : 7 des 9 buts de Tavares sont tombés en 1re mi-temps (1:12 à 29:48, dont les 3 jets de 7 m) ; la zone des 6 buts de jeu n'est pas dans l'export.

### Par joueur (`sz_match_players`, 60 min chacun déduit)
| Joueur (rôle) | Buts/tirs | % | 7 m | Fautes tech. | Exclusions | Remarque |
|---|---|---|---|---|---|---|
| A. Simon (CB) | 6/12 | 50,0 | — | 0 | 2 (+1 jaune) | meilleur ; exclu à 8:00 et 14:00 |
| J. Lefebvre (LW) | 3/12 | 25,0 | — | 0 | 0 | 9 tirs ratés ; saison 52,4 % avant J11 |
| B. Chevalier (P) | 3/4 | 75,0 | — | 1 | 1 | |
| G. Leroy (LB) | 2/6 | 33,3 | — | 2 | 1 | |
| D. Dupont (RW) | 2/8 | 25,0 | 1/2 | 1 | 2 | |
| N. Roger (RB) | 1/5 | 20,0 | — | 1 | 0 | |
| E. Bourgeois (GK) | 7 arrêts / 34 cadrés | 20,6 | contre 3/3 | — | 0 | 7 arrêts sur 31 hors 7 m = 22,6 % |
Équipe : 17/47 = 36,2 % ; hors 7 m 16/45 = 35,6 % (`sz_matches`, `sz_match_players`).

### L'adversaire (ce qu'il a fait de mieux)
- **Fábio Tavares (CB) : 9 buts sur 10 tirs, 3/3 aux 7 m** (en J2 : 5/11, 0/1 au 7 m). Francisco Dias (RB) 5/14 (volume, 35,7 %), Adriano Moreira (P) 5/7, Nuno Branco (LW) 4/7, Salgueiro (RW) 3/5.
- Araújo (GK adverse) : 14 arrêts sur 31 cadrés = 45,2 % (J2 : 9 sur 30 = 30,0 %). Eux : 27 buts sur 34 tirs cadrés (79 %) ; en victoires nous concédons en moyenne 64 % des tirs cadrés (calcul `sz_matches`).
- HB PILARES a changé 4 de ses 6 joueurs de champ entre J2 (nous avons gagné 21-20) et J11 : sortis Jakab, Ramos, Costa, Loureiro ; entrés Branco, Moreira, Dias, Salgueiro (`sz_match_players`). Je n'ai pas leurs compétences (privées [W:Players]) : je ne peux pas dire s'ils sont plus forts.

## 2. J12 — London Legion HC (extérieur, 18-28, 6-14 à la pause)
### Minute par minute
| Phase | Score (London - nous) | Ce qui s'est passé |
|---|---|---|
| **2:24-7:06** | 0-0 -> **5-0** (série 5-0, 4 min 42 s) | Reynolds, Wilson, Holmes, Green, Anderson : 5 buteurs différents ; jaunes de Dupont (3:24) et Lefebvre (5:24) ; premier but de chez nous à 7:54 (Roger) |
| 8:18-13:30 | 6-1 -> 8-3 | White 8:18 ; **Holmes 7 m 10:06** (jaune de Simon à 10:06) ; Lefebvre 13:00, Wilson 13:06, Dupont 13:30 |
| 13:30-20:18 | 8-3 -> 10-3 | 6 min 48 s sans but de chez nous (Reynolds 15:48, Holmes 20:00) ; Dupont 20:18 |
| 22:48-29:54 | 11-4 -> **14-6** | Green 22:48, Dupont 23:18 ; **Lefebvre exclu 26:36**, Green 26:48 ; Leroy 27:36 ; **Leroy exclu 28:30**, Wilson 28:54, Reynolds 29:54 |
| 30:18-35:42 | 14-6 -> 16-10 (4-2) | Dupont 30:18, 30:48, 33:54 ; Roger 35:42 : meilleur passage de la 2e mi-temps |
| 38:18-41:48 | 16-11 -> 18-13 | écart minimal de la 2e mi-temps : -5 |
| **49:36-51:12** | 19-14 -> **23-14** (série 4-0 en 1 min 36 s) | **Dupont exclu 49:36 + Holmes 7 m 49:36**, White 50:00, Green 50:42, Reynolds 51:12 |
| 51:18-59:54 | 23-15 -> 28-18 | (but contre son camp inscrit à Leroy 51:18, `detail = 'own-net'`, sens à confirmer), Holmes 7 m 53:18, Green 54:18, Simon 56:36, Green 57:36, Holmes 58:54 ; Chevalier 59:24, Leroy 59:54 |
- 7 m de London : 3/4 (Holmes) ; un seul suit une exclusion de chez nous à la même seconde (49:36, Dupont).

### Par joueur
| Joueur (rôle) | Buts/tirs | % | 7 m | Fautes tech. | Exclusions | Remarque |
|---|---|---|---|---|---|---|
| D. Dupont (RW) | 6/10 | 60,0 | 0/1 | 0 | 1 (+1 jaune) | meilleur ; 3 buts de 30:18 à 33:54 |
| N. Roger (RB) | 3/6 | 50,0 | — | **4** | 0 | |
| G. Leroy (LB) | 3/7 | 42,9 | — | 2 | 1 | |
| A. Simon (CB) | 3/7 | 42,9 | — | 2 | 0 (+1 jaune) | |
| B. Chevalier (P) | 2/3 | 66,7 | — | 0 | 0 | |
| J. Lefebvre (LW) | 1/5 | 20,0 | — | **4** | 1 (+1 jaune) | |
| E. Bourgeois (GK) | 5 arrêts / 33 cadrés | **15,2** | contre 3/4 | — | 0 | plus bas de la saison ; 5 sur 29 hors 7 m = 17,2 % |
Équipe : 18/38 = 47,4 % ; fautes techniques 12 (Lefebvre 4, Roger 4).

### L'adversaire
- **Craig Green (CB) 8/11, Jake Holmes (LW) 7/9 dont 3/4 aux 7 m, Kyle Wilson (RW) 6/11, Rory Reynolds (RB) 4/8** : 25 des 28 buts. Holmes était déjà à 10/12 en J3 (que nous avions gagné 25-24) : 17/21 (81 %) sur les deux matchs. Green 14/22 (64 %) sur les deux.
- Hill (GK) : 9 arrêts sur 27 cadrés = 33,3 % (J3 : 12 arrêts, 32,4 %) : le gardien adverse est le même qu'en J3 et ne fait pas mieux ; l'écart vient de Bourgeois (15,2 % contre 31,4 % en J3).
- London a changé 3 joueurs de champ depuis J3 : sortis Clark, Ribeiro, Ward ; entrés Wilson, White, Anderson.
- Eux : 28 buts sur 33 cadrés (85 %) ; nous 18 sur 27 cadrés (67 %).

## 3. Bourgeois contre les deux gardiens adverses
| | Cadrés contre | Arrêts | % | Si 31,2 % (moyenne J1-J12) | Si le % de l'adversaire |
|---|---|---|---|---|---|
| J11 vs Araújo (45,2 %) | 34 | 7 | 20,6 | 23 buts encaissés au lieu de 27 : 17-23, défaite | 19 buts : 17-19, défaite |
| J12 vs Hill (33,3 %) | 33 | 5 | 15,2 | 23 buts au lieu de 28 : 18-23, défaite | 22 buts : 18-22, défaite |
- Calcul : buts encaissés = cadrés x (1 - taux d'arrêt). **Même avec un gardien normal, nous perdons les deux matchs** (avis ; le gardien explique 4 à 6 buts sur 10). L'autre moitié vient de J11 la conversion adverse et notre tir (47 tirs à 55,9 %, notre moyenne J1-J10, donnent 26 buts), de J12 le volume (38 tirs contre 42,3 en moyenne J1-J10, adversaire 49 contre 43,7).
- Bourgeois sur 12 matchs : arrêts 8, 13, 11, 21, 11, 7, 11, 11, 13, 12, 7, 5 (`sz_match_players`). Cadrés subis : 33,4 en moyenne en victoire, 36,6 en défaite : même charge, pas la même réussite. Compétences (`sz_players`) : Bourgeois Réflexes 13, Un contre un 11, Placement 8, Prise de balle 16, 188 cm ; Blanc Réflexes 15, Un contre un 14, Placement 4, Prise de balle 8, 176 cm. Notes 11 contre 9. Le skill dit que la taille avantage les gardiens et que Réflexes est la compétence d'arrêt principale [W:Attributes].

## 4. Pourquoi nous gagnons ailleurs : moyennes de la saison (`sz_matches`)
| Indicateur | 7 victoires (J1-5, J7, J9) | 5 défaites (J6, J8, J10, J11, J12) | J11 | J12 | Sépare ? |
|---|---|---|---|---|---|
| Buts pour / contre | 23,9 / 21,6 | 20,8 / 27,0 | 17 / 27 | 18 / 28 | — |
| Notre efficacité | 56,5 % | 49,4 % | 36,2 | 47,4 | oui |
| Efficacité adverse | 50,3 % | 59,2 % | 58,7 | 57,1 | oui |
| Arrêts de Bourgeois | 36,5 % | 23,7 % | 20,6 | 15,2 | oui |
| Arrêts du gardien adverse | 27,7 % | 35,4 % | 45,2 | 33,3 | oui |
| Nos tirs / tirs adverses | 42,4 / 43,4 | 42,2 / 45,6 | 47 / 46 | 38 / 49 | peu (J12 seul) |
| Pertes de balle nous / eux | 14,0 / 11,1 | 13,6 / 10,4 | 11 / 6 | 15 / 8 | **non** |
| Exclusions nous / eux | 3,9 / 5,6 | 4,0 / 5,0 | 6 / 2 | 3 / 3 | **non** |
| 7 m concédés (tirs) | 2,6 | 2,6 | 3 | 4 | **non** |
| Retard à 15 min (nous - eux) | 5 victoires sur 7 en tête ou à égalité | 5 défaites sur 5 menées | -6 | -5 | oui |
- Mené à 15 min : J2, J6, J7, J8, J10, J11, J12 = 2 victoires (J2, J7) et 5 défaites ; à égalité ou en tête à 15 min : J1, J3, J4, J5, J9 = 5 victoires sur 5 (`sz_match_incidents`, dernier score à 15:00).
- **Différences de J11/J12 avec les victoires** : mêmes 7 titulaires qu'en victoire sur 5 postes (GK, CB, RB, LW, RW) ; **LB = Leroy (au lieu d'A. Bertin) et P = Chevalier (au lieu de Benoit)** dans les deux défaites, parce que Bertin et Benoit étaient blessés (brief Effectif). A. Bertin LB a joué 7 des 7 victoires de titulaire ; Benoit P 5 des 7. Sans les deux : 0 victoire sur 3 (J10 partiellement, J11, J12). Trois matchs, sous le seuil de confirmation de la fiche [fiche match, règle 1] : à lire comme un indice, pas une preuve.

## 5. Ce que nous avons changé ou pas entre J11 et J12
| Point | J11 -> J12 | Effet |
|---|---|---|
| Composition (7) | identique (Bourgeois, Simon, Leroy, Roger, Lefebvre, Dupont, Chevalier) | aucun |
| Formations / réglages | 5-1 / 6-0 ; J12 : `aggression = normal`, `attackDirection = mixed` pour les deux équipes (J11 non capté : `tactics` nul) | inchangés d'après ce qui est capté |
| Discipline (C-013) | exclusions 6 -> 3, Simon 2 -> 0, Chevalier 1 -> 0 | amélioré, résultat pire |
| Efficacité de tir | 36,2 % -> 47,4 % | amélioré |
| Pertes / fautes tech. | 11 -> 15 / 5 -> 12 | pire (Lefebvre 0 -> 4, Roger 1 -> 4) |
| Bourgeois | 20,6 % -> 15,2 % | pire |
- Conclusion : nous avons corrigé la discipline et le tir, pas le gardien, et ni l'un ni l'autre ne règle la 1re mi-temps. La consigne « ne rien changer » (C-013, C-017) a été appliquée à la lettre : on ne peut donc pas lui imputer un échec ni un succès.

## 6. Cinq points d'amélioration (J13 à Nenaa le 25/10 13:00 Paris, puis la suite)
| # | Action à l'écran (Équipe > Tactics) | Chiffre | Confiance |
|---|---|---|---|
| 1 | 🟥 **URGENT — LB : Alain Bertin titulaire, Guillaume Leroy remplaçant du LB.** Si Bertin est blessé ou suspendu à l'export, Leroy titulaire et remplaçant LB vide | Défense (Marquage + Contre + Anticipation + Duels + Récupération, somme non pondérée, mon calcul `sz_players`) : Bertin 52, Leroy 29 (Marquage 1, Contre 1, Anticipation 1). Buts encaissés : 22,9 par match avec Bertin (J1-J9) contre 26,7 avec Leroy titulaire (J10-J12). Tir : Bertin 26/46 = 56,5 %, Leroy 8/21 = 38,1 %. Exclusions par apparition : Bertin 0,44, Leroy 1,25 | moyenne-faible (3 matchs) |
| 2 | 🟧 **IMPORTANT — P : Alexandre Benoit titulaire, Benoît Chevalier remplaçant.** Sorti en cas de blessure : Chevalier titulaire | Benoit 25/32 = 78,1 % (7 matchs), Chevalier 16/24 = 66,7 % (7 matchs, dont 5/7 aux 7 m). Note 10 contre 9 ; Endurance 11 contre 3 (peu d'endurance = plus d'erreurs en fin de match [W:Attributes]). Contre-indice : compétences clés du pivot (Force, Contrôle, Jeu sans ballon, Tir) : Chevalier 11+7+17+18 = 53, Benoit 5+9+19+8 = 41 | faible (les deux indicateurs se contredisent ; je tranche sur le tir réel et la note) |
| 3 | 🟧 **IMPORTANT — GK : garder Bourgeois pour J13 et J14. Si son taux d'arrêts est < 25 % en J13 aussi (3e de suite après J11 et J12), mettre Blanc titulaire en J14 (FC Cete, domicile) et Bourgeois remplaçant** | Moyenne 31,2 % sur 12 matchs, 5 à 21 arrêts ; charge de cadrés quasi identique en victoire (33,4) et en défaite (36,6) ; un taux normal ne sauve pas J11 ni J12 (§ 3). Blanc : Réflexes 15 contre 13, Un contre un 14 contre 11, mais Placement 4 contre 8, Prise de balle 8 contre 16, note 9 contre 11. Le seuil de 25 % est mon avis, pas une règle du jeu | faible |
| 4 | 🟧 **IMPORTANT — Ne rien changer à Simon (CB), Dupont (RW), Lefebvre (LW), Roger (RB) pour cause de discipline ou de fautes techniques** (ni Denis CB 8, ni G. Bertin RW 9 en titulaire) | Exclusions par match : 3,9 en victoire contre 4,0 en défaite ; pertes 14,0 contre 13,6 : ces deux facteurs ne séparent pas. Simon : 48 buts, 45,3 % sur 106 tirs (le plus gros volume du club) ; Dupont : 31 buts, 57,4 % en 5 matchs ; remplaçants notés 8 (Denis) et 9 (G. Bertin) | moyenne |
| 5 | 🟩 **SUIVI — Ouvrir Équipe > Tactics et me dire si les champs « Aggression » et « Attack direction » existent, avec leurs options.** Ne rien modifier avant ma réponse | L'export J12 contient `aggression = normal` et `attackDirection = mixed` pour les deux équipes ; le skill communauté dit « pas encore de réglage d'agressivité » [Dev chat], donc soit le jeu a changé, soit ces champs sont fixes. Le sens des valeurs n'est dans aucun skill : je ne propose aucun test tant que je ne le connais pas. Seul levier non testé qui toucherait le départ (5 défaites sur 7 matchs où nous sommes menés à 15 min) | n/a (donnée manquante) |
- Pour les points 1 et 2 : le brief `2026-10-24-tactique-j13.md` les avait déjà posés (C-018) ; cette analyse les confirme avec des chiffres de défense et de tir, avec une réserve sur le P.
- J13 Nenaa : nous les avions battus 22-17 en J4 ; leurs meilleurs ce jour-là : Sanches (CB) 4/7, Luís Pacheco (RW) 3/15 (20 %), Coelho (LW) 3/9, gardien Alves 10 arrêts (31,3 %) (`sz_match_players`, un seul match). Ils sont à domicile : petit avantage du terrain [W:Match]. Aucun ajustement de tactique n'est fondé sur ces chiffres.

## 7. Conseils et enseignements à noter (pour l'agent Match / journal)
- **C-019** (2026-10-24, avant 13:00 Paris le 25) : exécuter les points 1 à 3 ci-dessus (LB Bertin, P Benoit, Bourgeois gardé) ; critère : `sz_match_players` (J13, `is_mine`) LB = Alain Bertin, P = Alexandre Benoit, GK = Bourgeois ; `sz_matches` J13 : score à 15 min (dernier but avant 900 s) pas en retard de plus de 2. Confiance faible. Reprend et précise C-018.
- **L-017** (nouveau) : la 1re mi-temps fait les défaites : -6,2 en moyenne (5 défaites) contre +0,4 (7 victoires) ; 2e mi-temps 0,0 contre +1,9. Matchs à l'appui : 12 de ligue (seuil atteint pour le constat, pas pour une cause).
- **L-018** (nouveau) : mené à 15 min = 2 victoires sur 7 ; pas mené = 5 sur 5.
- **L-019** (nouveau) : exclusions, pertes et 7 m concédés ne séparent pas victoires et défaites (3,9 contre 4,0 ; 14,0 contre 13,6 ; 2,6 contre 2,6) ; L-010 passe de « à surveiller » à « sans lien avec le résultat sur 12 matchs ».
- Donnée manquante enregistrée dans `docs/fiches/sixzeroleague/match.md` (zones de tir, minutes, pertes par joueur).
