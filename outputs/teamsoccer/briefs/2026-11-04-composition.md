# Team Soccer — brief Composition + Tactique du 2026-11-04 (les deux clubs)

Données : `core.player_daily` du 2026-11-04 (relevé 20:09 UTC), `gold.ts_upcoming`, `gold.ts_saisie_composition`, `gold.ts_vd_comparatif`, `core.fixture`, `core.standing`, `gold.ts_match_report` / `ts_match_plays`. Règles : skills teamsoccer-match et -joueurs, fiche tactique, learnings. Dossier C2 (valeurs du 2026-11-02) relancé : Forme Cows 94 (titulaires) / 70 (jeunes), Donkey 80 (adultes) / 98 (García), 0 blessé, 0 suspendu dans les deux clubs.

## Actions (ce soir)
| Priorité | Catégorie | Décision (écran → champ → valeur) | Pourquoi | Faux si |
|---|---|---|---|---|
| 🟥 URGENT | Composition | Cows – NK Kovinar Maribor (coupe, ext., 2084262) : enregistrer le 1-4-3-3 ci-dessous, mêmes onze qu'au 31/10, banc réordonné ; limite du jeu 05/11 11:00 | `lineup_saved` = false ; onze à Forme 94, 0 blessé/suspendu ; 16 attaques à 4 et 7 tirs contre Bresse (82,7) | tirs < 5 ou buts encaissés ≥ 2 au 05/11 |
| 🟥 URGENT | Composition | Donkey – BOT (ligue, ext., 2080341) : enregistrer le 1-4-4-2 ci-dessous (Schmidt + Suzuki au milieu, García en défense centrale) ; limite 05/11 17:30 | `lineup_saved` = false ; García Défense 90 Forme 98 = 89,5 au match contre 79,9 pour la meilleure suivante | notes MC Schmidt/Suzuki < 5,5 ET pertes > 65 % |
| 🟥 URGENT | Tactique | Donkey : Écran Tactique → Style d'équipe → **Offensif** (les Cows restent Neutre) | Donkey 1re (17 pts, 1 but encaissé en 7 matchs) ; BOT : 0 et 1 tir adverse aux deux derniers déplacements, 0-0 avec 6 et 2 tirs ; la baisse de Défense du style coûte presque rien contre un bot | tirs adverses ≥ 3 ou buts encaissés ≥ 2 ; ou tirs Donkey < 6 |
| 🟧 IMPORTANT | Export | Après l'enregistrement, exporter la page « Compositions » des deux clubs (onglet Avancé inclus) | `silver.ts_match_lineups` s'arrête au 2026-10-31 : les compositions des 02-04/11 manquent | ligne `ts_match_lineups` absente pour 2084262 ou 2080341 |
| 🟧 IMPORTANT | Export | Page de l'équipe NK Kovinar Maribor puis du match Godly Eleven 03/11 (Cows 0-3), à exporter ce soir | il me manque la note, la formation et le style de Kovinar (`opponent_rating` = null, humain ou bot inconnu) et le détail du 0-3 (`with_detail` = 0 sur les 11 défaites Cows) | — |

## Chomelix Cows — NK Kovinar Maribor (coupe, extérieur, 05/11 13:00 Paris, limite 11:00)
- **Situation** : 3es de ligue (16 pts, 5V 1N 1D, 12-6) derrière Godly Eleven (21 pts) et Bresse (16 pts), au 2026-11-03 ; derniers résultats : 1-1 Bresse (31/10), 0-3 Godly Eleven (03/11), 2-1 Mureaux (coupe, 04/11). Note d'équipe 74 (`ts_upcoming`) ; Kovinar inconnu. Pas de série de défaites (dernier match gagné) ; deux matchs de ligue sans victoire contre les deux meilleurs.
- **Mécanisme** : trois attaquants Finition 100 = Finition +10 % et un onze à Forme 94 (×0,982) [skill match : effets des formations ; skill joueurs : Forme]. Les tirs viennent des attaquants : Bonnet 9, Moreau 8, M. David 6 sur 26 tirs depuis le 20/10, aucun milieu (`ts_match_plays`) ; contre Bresse le volume existait (16 attaques/4, 7 tirs/4 cadrés, 1 poteau), le déficit est de conversion et de gardien (L-011, L-017, L-028).
- **Alternative écartée** : repasser en 1-4-4-2 (4e milieu = Jules Leroy, Conduite 89 × 0,91 = 81 contre un 3e attaquant à 98) ; 1-3-4-3 (Défense −10 % sur 3 centraux à 100 pour un milieu à 81). Pas de style Offensif : Kovinar inconnu et L-026 (ne pas tout miser sur l'attaque contre un humain).
- Les consignes ne changent pas : aucun milieu ne tire (0 tir sur 26), donc rien à gagner à les déplacer.

**1-4-3-3 · style Neutre · mode Avancé** (extérieur : 3 milieux contre 4 possibles = désavantage de possession, accepté)

| Empl. | Poste | Joueur | Compétence clé | Forme | Ultra déf. | Défensive | Médiane | Offensive | Finition |
|---|---|---|---|---|---|---|---|---|---|
| 0 | GB | Romain Thomas | Gardien 100 | 94 | Dégager | Dégager | Dégager | Dégager | Dégager |
| 1 | DL | Nicolas Simon | Défense 100 | 94 | Dégager | Passer → milieux | Passer → milieux | Passer → milieux | Tirer |
| 2 | DC | Théo Dubois | Défense 100 | 94 | Dégager | Passer → milieux | Passer → milieux | Passer → milieux | Tirer |
| 3 | DC | Théo Thomas | Défense 100 | 94 | Dégager | Passer → milieux | Passer → milieux | Passer → milieux | Tirer |
| 4 | DR | Noussair Ounahi | Défense 100, Tête 97 | 94 | Dégager | Passer → milieux | Passer → milieux | Centrer → attaquants | Tirer |
| 5 | ML | Adrien Roux (1 jaune) | Conduite 100 | 94 | Dégager | Passer → milieux | Dribbler | Centrer → attaquants | Tirer |
| 6 | MC | Lucas David | Conduite 100 | 94 | Dégager | Passer → milieux | Dribbler | Passer → attaquants | Tirer |
| 7 | MR | Clément Robert | Conduite 100 | 94 | Dégager | Passer → milieux | Dribbler | Passer → attaquants | Tirer |
| 8 | AL | Lucas Moreau | Finition 100 | 94 | Dégager | Passer → milieux | Dribbler | Dribbler | Tirer |
| 9 | AC | Pierre Bonnet | Finition 100 | 94 | Dégager | Passer → milieux | Passer → milieux | Dribbler | Tirer |
| 10 | AR | Mathis David | Finition 100 | 94 | Dégager | Passer → milieux | Dribbler | Centrer → attaquants | Tirer |

Ordre 5-6-7 (ML, MC, MR) et 8-9-10 (AL, AC, AR) repris du 31/10 ; gauche/droite des ailiers à vérifier à l'écran.

| Banc | Joueur | Rôle couvert |
|---|---|---|
| 1 | Thomas David (Gardien 92, Forme 70) | GB |
| 2 | Enzo Roux (Défense 88, Forme 70) | DC |
| 3 | Pierre Leroy (Défense 59, Forme 100) | DC |
| 4 | Jules Leroy (Conduite 89, Forme 70) | MC |
| 5 | Adrien Thomas (Conduite 80, Forme 94) | MC |
| 6 | Thomas Roux (Finition 85, Forme 70) | AC |

Changement de banc : Enzo Roux (88 × 0,91 = 80) passe avant Pierre Leroy (59 × 1,00 = 59) comme premier couvreur de DC (`ts_saisie_composition`). Thomas Roux (AC) couvre l'attaque, comme le 31/10.

**Remplacements programmés** : aucun. Raison : le meilleur remplaçant par poste vaut 77 à 81 contre 98 pour le titulaire (Forme 70 des jeunes), même à la 60e minute.

**Plan B** : blessure = remplaçant du poste couvert. Ounahi sorti : Enzo Roux ; un milieu : Jules Leroy ; un attaquant : Thomas Roux ; gardien : Thomas David.

**À refaire si** : un des onze devient blessé ou suspendu à l'export de ce soir ; l'export de Kovinar montre une note ≥ 85 (alors garder le même onze mais passer en 1-4-4-2 avec Jules Leroy, pour la possession à l'extérieur) ; Kovinar est un bot (alors seulement Neutre inchangé, aucun test).

## Ben Ahmed Donkey — BOT (ligue, extérieur, 05/11 19:30 Paris, limite 17:30)
- **Situation** : 1res de la Women's TS League, 17 pts (5V 2N 0D, 11-1) au 2026-11-02 ; BOT 5e (2-0-4, 6 pts) ; note 64,7 contre 60. Dernier match : 2-0 contre un BOT (02/11) puis amical gagné 2-1 (04/11). Aux deux déplacements précédents contre un bot : 0-0 avec 2 tirs (26/10) et 0-0 avec 6 tirs/4 cadrés (29/10), 0 et 1 tir adverse.
- **Mécanisme** : le bot joue Neutre, compétences ×0,90 et malus Gardien/Finition [skill match : bots]. Le style Offensif ajoute à la Finition et retire à la Défense [skill match § Avancé : ampleur contradictoire, ±10 % ou ±25 %] : le coût est presque nul quand l'adversaire tire 0 à 1 fois par match, le gain est possible sur des tirs de Müller (Finition 91) et Yamamoto (89) dont le déficit de buts vient de la conversion (9 et 6 tirs depuis le 20/10 pour 3 et 2 buts).
- **Alternative écartée** : rester Neutre (zéro risque, mais deux 0-0 de suite en déplacement et un déficit de buts déjà documenté, L-028) ; style Très offensif (écart d'ampleur entre sources non tranché, on commence par un cran).
- **Composition** : García (Défense 90, Forme 98) reste titulaire central ; Schmidt (Passe 84) et Suzuki (Passe 81) au milieu central, Kumar (Passe 60) sur le banc : Conduite 62, 63 et 64, l'écart est de 1 à 2 points, l'écart de Passe est de 21 à 24. Cela contredit C-050 (Suzuki à la place de Schmidt, Kumar gardé) : même Conduite, mais Schmidt et Suzuki servent mieux les deux attaquantes (la Passe du passeur augmente la chance de réception du coéquipier [skill match, moteur v3]). Les notes basses de Schmidt (5,4-5,5) sont des notes de composition, pas de déroulé (L-015, L-019) ; si elles restent sous 5,5 avec les pertes > 65 %, retour à Kumar.

**1-4-4-2 · style Offensif · mode Avancé**

| Empl. | Poste | Joueuse | Compétence clé | Forme | Ultra déf. | Défensive | Médiane | Offensive | Finition |
|---|---|---|---|---|---|---|---|---|---|
| 0 | GB | Chae Abdel | Gardien 83 | 80 | Dégager | Dégager | Dégager | Dégager | Dégager |
| 1 | DL | Yuki Fernández | Défense 85 | 80 | Dégager | Passer → milieux | Passer → milieux | Passer → milieux | Tirer |
| 2 | DC | Zainab García | Défense 90 | 98 | Dégager | Passer → milieux | Passer → milieux | Passer → milieux | Tirer |
| 3 | DC | Anna Fournier | Défense 81 | 80 | Dégager | Passer → milieux | Passer → milieux | Passer → milieux | Tirer |
| 4 | DR | Nour Taylor | Défense 81 | 80 | Dégager | Passer → milieux | Passer → milieux | Passer → milieux | Tirer |
| 5 | ML | Momoka Martínez | Centres 81, Conduite 65 | 80 | Dégager | Passer → milieux | Dribbler | Centrer → attaquants | Tirer |
| 6 | MC | Ama Schmidt | Passe 84 | 80 | Dégager | Passer → milieux | Passer → milieux | Passer → attaquants | Tirer |
| 7 | MC | Lena Suzuki | Passe 81 | 80 | Dégager | Passer → milieux | Passer → milieux | Passer → attaquants | Tirer |
| 8 | MR | Oluwaseun Mansour | Centres 81, Conduite 64 | 80 | Dégager | Passer → milieux | Dribbler | Centrer → attaquants | Tirer |
| 9 | AC | Juliette Yamamoto | Finition 89 | 80 | Dégager | Passer → milieux | Passer → milieux | Dribbler | Tirer |
| 10 | AC | Marie Müller | Finition 91 | 80 | Dégager | Passer → milieux | Passer → milieux | Dribbler | Tirer |

Ordre 1-4 et 5-8 repris de la composition par défaut du 23/10 (`silver.ts_lineups`) et du 29/10 ; à vérifier à l'écran. Latérales et centrales : Centres et Conduite à 60, donc « passer » (départage de la fiche).

| Banc | Joueuse | Rôle couvert |
|---|---|---|
| 1 | Rania Fournier (Gardien 74, Forme 94) | GB |
| 2 | Salma Girard (Défense 78) | DC |
| 3 | Kavya Hayashi (Défense 73) | DC |
| 4 | Uchenna Kumar (Centres 79, Conduite 64) | MC |
| 5 | Adaeze Wilson (Passe 82, 1 jaune) | AC |
| 6 | Ingrid Shimizu (Passe 78) | AC |

**Remplacements programmés** : aucun. Raison : 4 échecs successifs de la suppression (C-018, C-030, C-041, C-050) ; la consigne est de vider l'onglet « Remplacements » dans les modes Simple et Avancé, et de contrôler l'onglet Avancé après l'enregistrement ; l'écart de compétence entre titulaire et remplaçante est de 20 à 30 points.

**Plan B** : blessure = remplaçante du poste couvert. Abdel sortie : Rania Fournier ; une centrale : Girard puis Hayashi ; une milieu : Kumar ; une attaquante : Wilson (Finition 60) puis Shimizu.

**À refaire si** : l'export de ce soir montre une blessée ou suspendue parmi les onze ; le match ne se joue plus contre un BOT.

## Finances et infrastructures (relevé du 2026-11-04, `gold.ts_finance_status`, `ts_capacite_invest`, `ts_stadium_payback`, `ts_hpc_status`)
*Corrigé par la police le 2026-11-04 (voir `police-2026-11-04.md`, section finances).*
| Club | Solde | Semaine clôturée le lundi 02/11 (26/10 → 01/11) | Capacité d'investir | Verdict |
|---|---|---|---|---|
| Cows | 873 653 | recettes 2 102 926, dépenses 3 554 021 = construction de stade 3 369 250 + salaires 155 851 + entretien 28 920 ; net d'exploitation **+1 918 155** | **459 647** (873 653 − réserve 414 006). Les 585 280 du 02/11 sont déjà déduits du solde : ancienne valeur −125 633 = double compte | Voir ci-dessous |
| Donkey | 523 786 | recettes 474 605, dépenses 826 561 = places 705 000 + salaires 101 537 + entretien 20 024 ; net d'exploitation **+353 044** | **251 434** (523 786 − réserve 272 352) | Voir ci-dessous |

- **Les « autres 3 347 018 » des Cows n'existent pas** : `other_expenses` = 0. L'écart vient de la construction de stade du 27–30/10 (3 369 250 en cumul d'export du 31/10) ; le brouillon rapprochait les dépenses de la semaine close de salaires et d'entretien de la semaine nouvelle. À noter : le registre des dépenses décidées ne couvre que 2 138 750 des 3 369 250 (écart 1 230 500, achats du 27–29/10 plus gros que déclaré).
- **Matchs à domicile par saison** : **7 de ligue** (14 journées, `ts_season_calendar` : 7 restantes dont 3 à domicile ; skill saison § Ligue), plus amicaux à un quart du prix. Le brouillon écrivait « 3 par saison » : faux, 3 est le reste de cette saison. Rentabilité (entretien sur 9 semaines compté) : ≈ 13,8 matchs ≈ **2 saisons** pour une place basique de Donkey (13,3 dans la vue), pas 4 à 5.
- **Donkey** : 251 434 → 1 676 places basiques (251 400 $, 13,3 matchs, seuil de la carte ≤ 14 respecté ; il reste 272 386, au-dessus de la réserve et des 200 000 du cercle jaune). Décision : **acheter 1 676 places basiques**, si l'écran Stade affiche encore 10 490 basiques. Faux si Donkey perd la 1re place (80 % → 70 % : 15,2 matchs).
- **Cows** : 459 647 → 5 745 places debout (459 600 $, 13,4 matchs ; basiques au maximum 20 000). Option moins chère : 1 250 couvertes (375 000 $, 13,7). Entretien 47 475 contre 50 767 : **pas un bug**, facturé sur les places d'avant l'achat de 7 316 debout (791 250 × 6 % = 47 475) ; prochain lundi : 50 767 attendus.
- **HPC** (export du 2026-10-30, `bronze.raw_pages` 27151) : 50 TSC, 0 accumulé, 5 semaines restantes, aucun paiement ; un seul paiement de 50 TSC atteint le minimum. L'écran dit **« aucun remboursement » sous 50 TSC** (le skill disait « rendus » : à corriger). Décision Premium laissée à l'utilisateur.
- **Entraîneur** : niveau 1 (rôle coach, niveau 20 sur 100) pour les deux clubs au 2026-10-30 ; niveau 2 = 1 000 000 $, inabordable. **Limite d'achat** : 1 par semaine, remise à zéro lundi 00:00 ; aucun achat de joueur (`new_signings` = 0 les deux clubs) ; export « Mes enchères » vieux de 131 h.

## Conclusion
1. Composition : mêmes onze qu'au dernier match parce que rien n'a changé dans les données (Forme 94 chez les Cows, 0 blessé, 0 suspendu) ; seuls changent le banc des Cows (Thomas Roux au 6e rang) et le style de Donkey (Offensif).
2. Toutes les consignes sont remplies : Ultra déf. = Dégager, Défensive = Passer → cible, Finition = Tirer pour tous, GB Dégager partout (règle du format validé le 2026-10-31).
3. Finances (corrigé par la police) : Donkey 1 676 places basiques (251 400 $) ; Cows 5 745 places debout (459 600 $) ou 1 250 couvertes (375 000 $) ; payback ≈ 2 saisons de 7 matchs à domicile.

## Comment séparer les effets (Donkey, plusieurs changements à la fois)
- Style Offensif : tirs adverses et buts encaissés (`ts_match_report.opp_shots`, `goals_against`), tirs de l'équipe.
- Schmidt + Suzuki : notes des deux MC et part de ballons perdus (`my_lost` / `my_attacks`, `ts_player_match_ratings`).
- Consigne « passer » en Finition des deux milieux centraux : tirs de Müller + Yamamoto (base depuis le 20/10 : 9 et 6 tirs ; un seul tir d'une défenseure, Hayashi) contre tirs des milieux (`ts_match_plays.last_actor`).

## Divergences tranchées
- Contredit C-050 (learnings, 2026-10-30) : Schmidt reste titulaire avec Suzuki, Kumar au banc ; raison : Passe 84 et 81 contre 60 pour la même Conduite à 1-2 points.
- Contredit le brief tactique 2026-10-29 (Cows) sur l'ordre du banc : Enzo Roux avant Pierre Leroy, parce que 80 contre 59 au match.
- Pas de changement de formation ni de consigne chez les Cows malgré 1 nul et 1 défaite en ligue : le volume de jeu est bon, la défaite 0-3 n'a pas de détail en base (il me manque la page du match, voir l'action d'export).

## Conseils ajoutés à `learnings.md`
C-052 (Cows, Kovinar), C-053 (Donkey, style Offensif), C-054 (export Kovinar et Godly).
