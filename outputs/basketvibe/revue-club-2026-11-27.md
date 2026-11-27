# Revue de club BasketVibe — 27/11/2026

**Sources** : `outputs/basketvibe/aujourdhui-2026-11-27.md` (généré 10:40 depuis les vues gold, table « Qui vendre », table des prix, annonces 24 h), `learnings.md` (C-142 à C-146), brief tactique du 27/11 (amical Saile C.B.).
**Base Supabase injoignable de 10:45 à 10:55** (délai de connexion sur `sql.py` et le connecteur, projet pourtant `ACTIVE_HEALTHY`) ; le passage `--relance` s'est arrêté (« base indisponible : 3 sondes sur 3 en échec »). Colonnes marquées « base » = non lues, à compléter quand la base répond. Je n'invente aucune valeur.

Colonnes manquantes partout : PS **au poste** (`gold.bv_slot_fit`) — la note ci-dessous est le PS du meilleur poste (`ps` de `gold.bv_sell_candidates`) ; potentiel et projection seulement là où une décision C-14x les donne.
Prix attendu = médiane de la case âge × palier de note (ventes conclues), entre parenthèses p25–p75. Taxe de vente 5 % (skill basketvibe-transferts).

## Effectif par poste (13 joueurs dans `bv_sell_candidates`)

### PG
| Joueur | Âge | PS | Rang (meilleur poste) | Min. 4 derniers ligue | Potentiel | PS projeté 16 entr. | Salaire hebdo | Prix attendu (p25–p75) |
|---|---|---|---|---|---|---|---|---|
| Oscar Richard | 25 | 56,8 | 2 (PG) | 33,0 | base | base | 25 605 | 1 470 000 (1 010 000–1 889 444) |
| Naël Boyer | 20 | 48,7 | 6 (PG) | 27,0 | base | base | 19 361 | 1 010 000 (520 000–2 187 187) |
| Nolan Baron | 17 | 45,2 | 9 (PG) | 0,0 | 8 (C-145) | ≈ +0,8 avec 3PT/Déf (C-145) | 17 135 | 1 010 000 (520 000–2 187 187) |

### SG
| Joueur | Âge | PS | Rang | Min. | Potentiel | PS proj. 16 | Salaire | Prix attendu (p25–p75) |
|---|---|---|---|---|---|---|---|---|
| Thibault Bonnet | 26 | 52,1 | 4 (SG) | 30,0 | base | base | 21 187 | 490 000 (155 000–700 000) |
| Sacha Leclerc | 17 | 43,0 | 11 (SG) | 3,0 | base | base | 15 114 | 350 000 (100 000–802 500) |

### SF
| Joueur | Âge | PS | Rang | Min. | Potentiel | PS proj. 16 | Salaire | Prix attendu (p25–p75) |
|---|---|---|---|---|---|---|---|---|
| Hadrien Gimenez | 26 | 60,3 | 1 (SG) | 33,0 | base | base | 29 159 | 1 537 500 (1 155 000–1 872 097) |
| Étienne Bourdon | 16 | 52,2 | 5 (SG) | 0,0 | Solid, P5–P7 (C-144) | 52,3–53,6 au SF (C-144) | 22 954 | 3 733 865 (1 622 500–4 912 500) |
| Jonathan Durand | 25 | 43,9 | 9 (SG) | 6,0 | base | base | 15 928 | 4 375 (700–38 750) |

### PF
| Joueur | Âge | PS | Rang | Min. | Potentiel | PS proj. 16 | Salaire | Prix attendu (p25–p75) |
|---|---|---|---|---|---|---|---|---|
| Léo Lefebvre | 29 | 63,2 | 1 (C) | 36,0 | base | base | 32 246 | 1 537 500 (1 155 000–1 872 097) |
| Noé Legrand | 23 | 49,9 | 4 (PF) | 21,0 | base | base | 19 227 | 99 500 (28 000–238 749) |
| Anselmo Albano | 27 | 48,0 | sans rang | 3,0 | base | base | 18 103 | 10 000 (1 000–62 750) |

### C
| Joueur | Âge | PS | Rang | Min. | Potentiel | PS proj. 16 | Salaire | Prix attendu (p25–p75) |
|---|---|---|---|---|---|---|---|---|
| Armand Fournier | 28 | 52,7 | 3 (PF) | 30,0 | base | base | 22 846 | 490 000 (155 000–700 000) |
| Maël Bernard | 18 | 48,8 | 6 (PF) | 18,0 | 10 (C-142) | 56,2 au C, 2PT/Athlé (C-146) | 19 326 | 1 010 000 (520 000–2 187 187) |

Écart à vérifier : le brief tactique du 27/11 compte 12 joueurs, la vue de vente 13 (Albano « sans rang » : c'est le cas qui faisait planter le que-faire le 26/11).

## a. Ventes

| Vente | Argent attendu (net 5 %) | Salaire libéré / sem. | Perte du banc | Effectif après | Verdict |
|---|---|---|---|---|---|
| Durand | 4 375 (≈ 4 156 net) ; p25–p75 700–38 750 | 15 928 | 6,0 min ; remplaçant Leclerc, écart de force 2,0 | 12 (aucun blessé selon le brief du 27/11) | **vendre** : ni plus fort ni jeune qu'on monte ; 0,3 % du produit possible, mais −15 928/sem |
| Baron | 1 010 000 (≈ 959 500 net) ; 520 000–2 187 187 | 17 135 | 0 min ; remplaçant Durand, écart 0,8 | 12 | **garder** : 17 ans, potentiel 8 = « jeune remplaçant qu'on monte » ; > 250 000 → police obligatoire |
| Boyer | 1 010 000 (≈ 959 500 net) | 19 361 | 27,0 min ; remplaçant Baron, écart 3,5 > tolérance 1,0 | 12 | **garder** : « nécessaire » selon la vue |
| Baron + Boyer | ≈ 1 919 000 net | 36 496 | 27,0 min et Richard seul PG | 11 | **non** : un seul PG, contraire à « 2 par poste » |

Prix de Durand : la ligne d'offre du que-faire donne 3 751 (médiane du poste, 3 ventes) contre 4 375 pour la case : même ordre de grandeur.

## b. « 2 joueurs par poste »

Par poste de fiche : PG 3, SG 2, SF 3, PF 3, C 2 = 13. Surplus = 1 en PG (Baron, 0 min), 1 en SF (Durand, 6 min), 1 en PF (Albano, 3 min). Le depth chart et les postes réellement joués par match ne sont pas lus (base) : rang au meilleur poste seulement, et 4 joueurs jouent ailleurs que leur poste de fiche (Gimenez et Bourdon SG, Lefebvre C, Fournier et Bernard PF).

## c. Marché d'aujourd'hui (annonces finissant dans les 24 h, lues à 10:40)

Capacité restante ≈ 880 939 (plafond « borné par la capacité » ; Cadenas à 888 888 refusé pour capacité). Solde exact : base. Avec Durand : ≈ 885 100 ; avec Durand + Baron + Boyer : ≈ 2 804 000.

| Joueur | Poste | Âge | PS | Gain pour le cinq | Prix actuel | Médiane case | Accessible ? |
|---|---|---|---|---|---|---|---|
| Paolo Kim | PF | 26 | 59,2 | +5,6 | 3 500 023 | 1 010 000 | non (fin vers 11:40, au-dessus de tout budget) |
| Edgar Basilio | PG | 29 | 62,0 | +5,2 | 2 000 000 | 1 537 500 | seulement en vendant Baron + Boyer, qu'on garde |
| Sérgio Moreira | PF | 26 | 61,2 | +2,0 | 2 205 000 | 1 537 500 | non |

Jeunes 16–18 au PS haut pour l'âge (≥ 46) : Marko Vuković SF 17 PS 52,6 (5 999 999) ; Oskaras Stonys C 17 PS 51,4 (5 000 000) ; Herbertas Vaičeliūnas C 16 PS 47,7 (5 000 000) ; Gabriel Haas PF 17 PS 46,9 (2 375 000) ; Matan Bouzaglo PF 16 PS 46,2 (2 500 000). Tous au-dessus de la médiane de leur case et de la capacité.
Nombre d'annonces des 7 derniers jours répondant à ces critères : **non calculé (base injoignable)**.

## d. Contrôle

- Académie : **Bourdon est signé** (présent dans la vue des joueurs à 10:40, salaire 22 954) ; Cousin absent de l'effectif → non signé. C-144 tenu pour la signature ; C-143 caduc.
- Entraînement lu le 26/11 à 23:22 contre C-144 (Bourdon Athlé/2PT), C-145 (Baron 3PT/Déf), C-146 (Bernard 2PT/Athlé) : **non contrôlé**, `silver.bv_player_weekly` illisible (base). Les gains se mesureront après dim. 29/11 04:00.

## Action d'aujourd'hui

Mets Durand en vente (proposition : accord écrit requis, montant < 250 000 donc sans police). Aucune enchère : aucune cible à gain ≥ 1,0 n'est dans la capacité. Doute : si `gold.bv_slot_fit` montre Durand utile au poste SG/SF dans le depth chart, je me trompe.
