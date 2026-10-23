# Team Soccer — brief Entraînement du 2026-10-23

Agent Entraînement (medium + Sonnet). Fiches : `commun.md`, `entrainement.md` ; skills `teamsoccer-entrainement`, `teamsoccer-joueurs`. Briefs amont lus : Match (corrigé), Effectif, Finances-personnel, Académie du 2026-10-23.
Vues : `silver.ts_training` (T, relevé du 2026-10-23), `silver.ts_players` (J, 2026-10-23), `gold.ts_player_progress` (PP), `gold.ts_hpc_status` (H, as_of 2026-10-19). Pas de brief Entraînement précédent : pas de delta.

## En tête : exports manquants et contradictions
| Point | Constat | Conséquence |
|---|---|---|
| Export manquant | Aucun. T et J datent du 2026-10-23 (après la mise à jour de ce vendredi : PP montre −2 de Forme à 70 % et +10 pour Étienne Roux à 40 %). H date du 19/10 (aucun changement possible depuis : aucun paiement). | Rien à exporter. Un relevé HPC après le lundi 26/10 suffit. |
| Contradiction Effectif | Aucune sur Forme, Étienne Roux (56 → 66 le 30/10) ni Kumar, Schmidt, Suzuki. | Aucune relance. |
| Nuance sur Finances (Ben Ahmed n° 6, achat d'une milieu Conduite ≥ 70) | L'entraînement de Conduite amène Kumar, Mansour, Martínez, Schmidt à ≥ 70 vers le 20/11 (voir § 2). L'achat reste utile avant, il n'est pas annulé. | Agent Transferts : ne pas surpayer ; décision d'achat inchangée. |
| Contradiction avec l'Académie sur le HPC | L'Académie laisse la décision à l'utilisateur ; je tranche ci-dessous (0 TSC). Pas de désaccord de fond. | — |

## Faits mesurés sur les gains (T, cycle du 23/10, intensité 70 %)
| Âge | Gain de la compétence entraînée | Joueurs |
|---|---|---|
| 14–20 | +3 (technique), +3 à +4 (physique) | tous les jeunes, Ounahi, Moreau, Müller |
| 21 | +2 ou +3 | Simon, Théo Thomas (+2), Schmidt, J. Yamamoto (+3) |
| 22–26 | +2 | Dubois (27) aussi |
| 27–28 | +1 | Shimizu, Girard, Hayashi, Ibe |
| 32, intensité 0 % | −2 | Pierre Leroy |
- Le guide dit « 28 ans : aucun point » [G:Entraînements] ; nos données montrent encore +1 à 28 ans à 70 %. La mesure l'emporte pour décider (règle 5 de la fiche).
- Aucun joueur entraîné en technique à 70 % n'a perdu d'Endurance ni de Vitesse (`stamina_last_change` et `pace_last_change` = 0 pour tous) [Obs T]. La règle d'origine « technique > 60–70 % fait perdre le physique » [F:2026-05-07] n'apparaît pas à 70 %. Je ne dépasse pas 70 %.
- Forme au vendredi : 70 % = −2 chez tous (PP, 2 relevés), 40 % = +10 (Étienne Roux) : table du skill confirmée [skill entraînement, Forme et intensité].

## Alertes de la fiche
| Alerte | Club | Joueurs |
|---|---|---|
| Endurance ≤ 30 (seuil critique) | aucun | Plus bas : Takahashi 31 (Ben Ahmed) |
| Endurance ≤ 35 | Chomelix | Hugo Martin 34, Adrien Thomas 35, Étienne Roux (GB, 14 ans) 35 |
| Endurance ≤ 35 | Ben Ahmed | Takahashi 31, Kobayashi 33 |
| Forme < 60 | Chomelix | Étienne Roux (ATT, 19 ans) 56 |
| 28 ans et + à haute intensité | aucun (Hayashi, Ibe 28 ans à 70 % = pas haute ; Pierre Leroy 32 ans à 0 %) | — |
Takahashi et Kobayashi, Hugo Martin sont déjà en Endurance à 70 % (+3 à +4 par semaine) : Takahashi sort de la zone ≤ 35 au 30/10 ou au 6/11. Aucune action de plus.

## 1. Chomelix Cows (team_id 18)
### Fiche de saisie (gymnase) — à saisir avant le vendredi 30/10
| Joueur | Âge | Réglage actuel | Réglage à saisir | Décision | Raison chiffrée |
|---|---|---|---|---|---|
| Noussair Ounahi | 19 | Conduite 70 % | idem | Garder | Défense/Contrôle 100 ; Conduite 71 est la compétence clé suivante du latéral ; +3 |
| Nicolas Simon | 21 | Contrôle 70 % | idem | Garder | Défense 100, Contrôle 73 ; +2 |
| Théo Thomas | 21 | Contrôle 70 % | idem | Garder | Défense 100, Contrôle 61 ; +2 |
| Théo Dubois | 27 | Contrôle 70 % | idem | Garder | Défense 100, Contrôle 71 ; +2 mesuré, 28 ans à la saison 4 |
| Romain Thomas (GB) | 23 | Passe 70 % | **Contrôle 70 %** | **Changer** | Gardien 100 ; Contrôle (66) est la 2e compétence clé du gardien, la Passe n'est que secondaire [skill joueurs, compétences clés] |
| Clément Robert | 25 | Passe 70 % | idem | Garder | Conduite 100 ; Passe 59, secondaire du milieu |
| Adrien Roux | 25 | Centres 70 % | **Contrôle 70 %** | **Changer** | Conduite 100 ; Centres 84 n'est pas une compétence clé du MC ; Contrôle 55 est la plus basse des clés |
| Lucas David | 26 | Contrôle 70 % | idem | Garder | Conduite 100, Contrôle 60 |
| Lucas Moreau | 20 | Contrôle 70 % | idem | Garder | Finition 100, Contrôle 84 ; +3 |
| Mathis David | 25 | Contrôle 70 % | idem | Garder | Finition 100, Contrôle 84 ; +2 |
| Pierre Bonnet | 24 | Vitesse 70 % | **Contrôle 70 %** | **Changer** | Finition 100 ; Contrôle 61 est la 2e compétence clé de l'attaquant ; Vitesse 72 déjà correcte, elle ne monte plus seule mais ne baisse pas (T) |
| Étienne Roux (ATT) | 19 | Endurance 40 % | idem jusqu'au 30/10 | Garder | Forme 56 → 66 (+10) au 30/10, Endurance 67 ; décision Effectif n° 3 |
| Pierre Leroy | 32 | Défense 0 % | idem | Garder | Forme 100, premier couvreur (Match) ; perte −2 par semaine, voir C-021 |
| Jules Leroy | 17 | Passe 70 % | **Conduite 70 %** | **Changer** | Conduite 86 : compétence principale du MC, +3 par semaine → ~100 au 27/11 ; OVR ~49 → ~56 (principal = poids 1/1,9) [skill joueurs, OVR] |
| Adrien Thomas | 14 | Passe 70 % | **Conduite 70 %** | **Changer** | Conduite 77, Passe 44 ; +3 par semaine → ~92 au 27/11 |
| Nathan Lefebvre | 18 | Passe 70 % | **Conduite 70 %** | **Changer** | Conduite 73, Passe 37 ; +3 par semaine → ~88 |
| Thomas Petit | 14 | Conduite 70 % | idem | Garder | Conduite 72 |
| Thomas David (GB) | 17 | Gardien 70 % | idem | Garder | Gardien 89, +3 : relève |
| Étienne Roux (GB) | 14 | Gardien 70 % | idem | Garder | Gardien 72, +3 |
| Enzo Roux | 16 | Défense 70 % | idem | Garder | Défense 85, +3 |
| Thomas Roux | 16 | Finition 70 % | idem | Garder | Finition 82, +3 |
| Hugo Martin (GB) | 15 | Endurance 70 % | idem | Garder | Endurance 34, +3 ; à vendre à 24 joueurs (Effectif) |
Six changements, tous à 70 %. Les compétences des 11 titulaires à 100 sur leur compétence principale vont sur leur 2e clé (Contrôle).

### Forme (mise à jour du vendredi)
- Prochain vendredi : **30/10**. Titulaires 96 → 94 (70 %, −2), banc jeunes 72 → 70, Étienne Roux (ATT) 56 → 66, Pierre Leroy reste 100 (plafond).
- **Décision : intensité 70 % pour tous les titulaires jusqu'à la fin de la saison de ligue.** Calcul : −2 de Forme = −0,6 % d'efficacité (×0,988 → ×0,982) contre +2 à +3 points sur la compétence principale (≈ +1 OVR). Les titulaires sont à 86 au 27/11 au pire (×0,958) : jamais sous 80.
- **Étienne Roux (ATT)** : Endurance 40 % inchangée jusqu'au 30/10 ; il reste hors composition tant que sa Forme est < 70 (Effectif n° 3 ; Match C-002). Décision : le garder à Endurance 40 % aussi après le 30/10 (66) pour atteindre 76 au 6/11 (×0,93) ; il est alors alignable à Finition 100. Ensuite, passer à Contrôle 60 % (Forme stable). Un export après le 6/11 le confirmera.
- Le match de ligue du 24/10 et ceux du 28/10 et 31/10 se jouent avec la Forme en place ; rien ne bouge avant le 30/10 (l'effet du 30/10 s'applique au match FC Bresse du 31/10 : titulaires à 94, ×0,982).

### Entraînement physique
- Aucun joueur en zone critique (Endurance ≤ 30). Pas de bloc physique pour les titulaires : coût de Forme de −10 à 100 %, et rien ne mesure l'effet d'un point d'Endurance au-delà de la règle de fatigue (−9 points de force sur 90 minutes à Forme 100) [skill joueurs]. Hugo Martin reste à Endurance (34).
- Vitesse de Bonnet (72) ne baisse plus : voir mesure ci-dessus.

## 2. Ben Ahmed Donkey (team_id 15858)
### Fiche de saisie (gymnase) — à saisir avant le vendredi 30/10
| Joueuse | Âge | Réglage actuel | Réglage à saisir | Décision | Raison chiffrée |
|---|---|---|---|---|---|
| Marie Müller | 20 | Finition 70 % | idem | Garder | Finition 88, +3 |
| Juliette Yamamoto | 21 | Finition 70 % | idem | Garder | Finition 87, +3 |
| Ama Schmidt | 21 | Contrôle 70 % | **Conduite 70 %** | **Changer** | Joue MC (5,5) ; Conduite 60 = compétence principale du milieu ; +3 par semaine → ~75 au 27/11 (72 au 20/11) ; Passe 84 inchangée |
| Lena Suzuki | 22 | Contrôle 70 % | **Conduite 70 %** | **Changer** | Joue MC (5,5) ; Conduite 60 ; +2 par semaine → ~70 au 27/11 |
| Uchenna Kumar | 24 | Conduite 70 % | idem | Garder | Conduite 62, +2 → 70 au 20/11 |
| Oluwaseun Mansour | 23 | Conduite 70 % | idem | Garder | Conduite 62, +2 |
| Momoka Martínez | 22 | Conduite 70 % | idem | Garder | Conduite 62, +2 |
| Chae Abdel (GB) | 24 | Gardien 70 % | idem | Garder | Gardien 81, +2 |
| Yuki Fernández | 23 | Défense 70 % | idem | Garder | Défense 83, +2 |
| Anna Fournier, Nour Taylor | 26 | Défense 70 % | idem | Garder | Défense 79, +2 |
| Salma Girard | 27 | Défense 70 % | idem | Garder | Défense 77, +1 |
| Hayashi, Ibe | 28 | Défense 70 % | idem | Garder jusqu'à la vente (après le 28/10) | +1 ; elles défendent le 26 et le 28/10 ; Forme figée à 82 jusqu'au 30/10 |
| Adaeze Wilson | 25 | Passe 70 % | idem | Garder | Passe 80 ; poste naturel indéterminé (toutes compétences de poste à 60) : pas de preuve pour mieux |
| Ingrid Shimizu | 27 | Passe 70 % | idem | Garder | Passe 77, +1 |
| Rania Fournier (GB) | 14 | Gardien 70 % | idem | Garder | Gardien 71, +3 |
| Hana Yamamoto | 14 | Défense 70 % | idem | Garder | Défense 64, +3 |
| Zainab Mori | 16 | Passe 70 % | idem | Garder | relève, aucun levier |
| Takahashi, Kobayashi | 14, 15 | Endurance 70 % | idem | Garder | Endurance 31 et 33, +4 ; sortent de la zone ≤ 35 |
| Valentina Williams | 14 | Vitesse 70 % | idem | Garder | Vitesse 36, +4 |
Deux changements, qui visent le trou structurel (milieu centrale, Match C-006, Effectif).

### Forme (mise à jour du vendredi)
- Titulaires à 82 (×0,946) : plus basse des deux clubs. 30/10 → 80, 6/11 → 78. Les matchs du 26/10 (BOT) et du 28/10 (coupe, Potatos y Potitas 77,65) se jouent à 82.
- **Décision : 70 % jusqu'au 30/10 ; à l'export du 6/11 (Forme 78), passer tous les titulaires à 60 %** (Forme stable à 0), sauf Müller et J. Yamamoto qui restent à 70 % tant que leur Finition est < 95. Raison : à 78, chaque −2 coûte autant en efficacité que le gain de +1 à +2 points ne rapporte (les 27–28 ans à +1 le rapportent déjà à peine).
- Pas d'alerte Forme < 60 ; jeunes à 88–96.

### Entraînement physique
Aucune joueuse en zone critique (plus basse : Takahashi 31, relève de 14 ans). Rien à saisir de plus.

## 3. Centre de Haute Performance : décisions fermes
Faits (H, 19/10, aucun paiement depuis) : les deux clubs ont 0 TSC investi, 45 TSC sur le compte (un seul solde pour les deux clubs), 50 requis, `can_complete` faux, 7 lundis restants, options de la semaine : Gardien, Défense, Contrôle.
Règles [skill entraînement, HPC] : 50 TSC investis dans la saison sinon les TSC sont rendus ; paiement 0/10/25/50 par semaine, non modifiable ; depuis la saison 3, un club qui a déjà son joueur HPC ne peut plus en avoir un second.

| Club | Décision | Combien | Sur quoi | Quand |
|---|---|---|---|---|
| Chomelix Cows | **Ne pas investir** | 0 TSC | Aucune des trois options | À chaque lundi restant : paiement 0 |
| Ben Ahmed Donkey | **Ne pas investir** | 0 TSC | Aucune des trois options | À chaque lundi restant : paiement 0 |

Pourquoi :
1. **Impossible à terminer** : 45 TSC pour 50. Même un seul club ne peut pas atteindre 50 avec ce compte ; un paiement partiel serait rendu en fin de saison sans joueur (aucun gain), et il bloquerait le solde de l'autre club. Acheter 5 TSC pour finir serait une dépense Premium dont je ne connais ni le prix ni le jeune obtenu : je ne la recommande pas.
2. **Aucune option ne couvre le besoin** : le seul trou structurel (milieu centrale à Ben Ahmed, banc milieu à Chomelix) demande de la Conduite ; les options sont Gardien, Défense, Contrôle. Chomelix a déjà Thomas David (89) et Romain Thomas (100) ; Ben Ahmed a déjà Fernández 83 et sa défense dense (surplus de 2 en vente).
3. **Occasion unique par club** : un seul joueur HPC par club depuis la saison 3. Le dépenser cette saison sur des options sans valeur gaspille le tirage.
- Condition de réexamen (règle, pas une hésitation) : un relevé HPC postérieur au 26/10 montrant à la fois un compte ≥ 50 TSC et Conduite parmi les 3 options. Alors Ben Ahmed prend 50 TSC en une fois sur Conduite ; Chomelix n'investit pas. Sans les deux conditions, 0 TSC.
- Pas d'export HPC demandé avant lundi : le prochain relevé d'usage suffit.

## 4. Entraîneur
Niveau 1 (« poor ») pour les deux clubs, inchangé. Le niveau 2 (1 000 000 $) n'est pas acheté : Finances n° 8 (aucun solde ne le permet en gardant la réserve).

## 5. Conseils suivis
Ajoutés à `outputs/teamsoccer/learnings.md` : C-017 à C-021. Aucun conseil d'entraînement ouvert avant ce brief.

## Réserves
- Faits : T, J, PP du 23/10 ; H du 19/10. Règles : skills entraînement et joueurs (validés 2026-10-19). Avis : changements de compétence, seuils de Forme, HPC.
- Confiance moyenne sur les projections de gain (+3/+2/+1 par semaine mesurés sur un seul cycle) ; faible sur la valeur exacte de l'OVR par sous-rôle (formules non documentées : je me fonde sur « principal = poids 1 » et les compétences clés du skill).
- Passer Schmidt et Suzuki à Conduite peut changer leur sous-rôle naturel (poste calculé sur Gardien, Défense, Conduite, Finition) : vérifier `position` au prochain export. Le but est le même, un MC naturel.
