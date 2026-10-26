# Brief Transferts BasketVibe — 2026-10-24

Briefs amont lus : effectif, finances, académie, tactique-j22 du 24/10. Skills : basketvibe-transferts [M§11.1, §11.3, §11.4, §10.3], fiche transferts. Données : `gold.bv_market_candidates`, `gold.bv_sell_candidates`, `gold.bv_market_price_ref`, `silver.bv_transfer_auctions`.

## Alerte donnée : marché périmé
**Il me manque un export du marché.** Dernière capture `transfers` : 22/10 13:20 UTC (`bronze.raw_pages`), soit plus de 48 h ; la dernière fin d'enchère vue est le 24/10 15:17 (Paris) ; `open_now` = 0 dans `silver.bv_transfer_auctions`. On le réunit comme ça : ouvrir la page Transferts (marché mondial, pages de 20, tri par temps restant) et lancer le script ; faire un export dimanche 25/10 après 04:00 et un autre lundi 26/10 après le tirage des 3 joueurs libres du jour de match [M§11.4]. Règle fiche : export de plus de 24 h = nouvel export.
Aucune enchère engagée de notre côté (`transfer_committed` = 0, brief Finances).

## Actions (en tête)
| Priorité | Action | Montant / limite | Heure |
|---|---|---|---|
| 🟥 URGENT | **Mets Min-jun Dang en vente maintenant**, prix minimum 50 000 | prix net attendu 95 % du prix final [M§11.1] | enchère d'environ 2 jours : fin ≈ lundi 26/10 soir, avant le +1 an de la nuit 26→27 (il aurait 30 ans) |
| 🟥 URGENT | **Mets Nael Fontaine en vente maintenant**, prix minimum 10 000 | net 95 % | fin ≈ lundi 26/10 soir |
| 🟧 IMPORTANT | **Refais l'export du marché dimanche 25/10 après 04:00**, puis lundi 26/10 | — | — |
| 🟧 IMPORTANT | **Enchère sur un joueur libre C/PF d'au moins 205 cm et Rebond 60 ou plus : maximale 80 000** (seule enchère, somme des maximales ≤ 82 000 [brief Finances ; M§10.3]) | 80 000 | heure de fin à lire dans l'export (aucun joueur ouvert aujourd'hui) |
| 🟩 SUIVI | Garder Richard (pas de vente) | — | — |
| 🟩 SUIVI | Aucune enchère sur un joueur d'un autre club (PF/C à 500 000–3 750 000) | dépasse 82 000 | — |

## 1. Marché du jour : rien d'ouvert, voici ce qui était à portée
Faits (`gold.bv_market_candidates`, 110 enchères vues entre le 22/10 et le 24/10, toutes terminées) :
| Joueur | Poste / âge / taille | PS / Rebond | Prix à la dernière lecture | Joueur libre | Salaire estimé |
|---|---|---|---|---|---|
| Tommaso Gasperoni | C, 27, 214 | 51,9 / 70 | 160 250 (3 enchères) | oui | 20 930 |
| Miroslav Holub | C, 25, 217 | 46,6 / 41 | 10 000 (0) | oui | n.c. |
| Maël Renaud | C, 32, 213 | 47,1 / 39 | 10 000 (0) | oui | n.c. |
| Manuel Faria | PF, 28, 205 | 59,7 / 76 | 1 200 000 (0) | non | 29 000 |
| Sérgio Gomes | C, 25, 208 | 55,1 / 77 | 1 000 000 (0) | non | 25 400 |
| Rakan Al-Dossary | C, 28, 211 | 54,9 / 63 | 750 000 (0) | non | 25 500 |
| Lamar Howard | C, 28, 217 | 54,3 / 67 | 610 000 (7) | non | 24 000 |
Lecture :
- Besoin (brief Tactique) : indice rebond 51,5 contre 61–66 chez Wolves. Mon calcul d'indice (Rebond × facteur de taille, [M§5.1.1] repris du brief Effectif) pour Gasperoni : 70 × 1,25 (214 cm) ≈ **87,6**, au-dessus de Lefebvre (76,8 en forme 1). Un profil de ce type est ce qu'il faut ; les autres C/PF du tableau coûtent 610 000 à 1 200 000, hors de notre plafond de **82 000**.
- Seuls les joueurs libres (départ 10 000 [M§11.4]) sont accessibles. Sur 4 joueurs libres vus, un seul a été disputé (Gasperoni, 160 250 après 3 enchères) : 3 ventes comparables de joueurs libres C, **confiance faible**.
- Prix de référence `gold.bv_market_price_ref` : C 26–29 ans médiane 314 159 (n=23, quartiles 7 500 – 750 000) ; C 30+ médiane 24 500 (n=8). Dispersion énorme, compétences inconnues : référence peu fiable. `bv_market_price_known` ne couvre que 89 ventes du 16 au 22/10 (fiche).

## 2. Enchère maximale conseillée (joueur libre grand)
- **Maximale : 80 000, une seule enchère à la fois** (82 000 de plafond moins 2 000 de marge) — calcul : solde fin S1 1 064 409 − réserve 981 992 = 82 417 (`investable_now_end_s1`, brief Finances).
- Mécanisme : maximale automatique secrète, palier de 250 à 10 000 puis 1 000 / 5 000 / 10 000 ; anti-snipe 3 min ; phase finale à l'aveugle 15 min après la fin initiale ; prix final = ce qu'il faut pour battre la 2e maximale, jamais plus que la nôtre [M§11.3].
- Critères d'achat (mon avis, confiance moyenne) : taille ≥ 205 cm (100 % au C [M§6.2.1]), Rebond ≥ 60, PS ≥ 50 pour entrer devant Klein (44,8) dans la rotation C. Pas de limite d'âge au-delà de 30 ans, mais à 31 ans et plus le déclin joue chaque semaine [M§8.5]; préférer 24–29 ans.
- Coût total : prix + salaire ≈ 21 000 par semaine (exemple Gasperoni, estimation) ; marge salariale **74 000/sem.** en S1 et ≈119 000/sem. en S2 (brief Finances). 8 semaines de S2 ≈ 168 000 de salaire en plus du prix.
- Le joueur n'arrivera pas pour J22 (verrouillage lundi 19:45) sauf enchère close avant : l'intérêt est la saison 2 (première journée lundi 02/11). Il sera bloqué une semaine à la revente [M§11.1]. Les salaires sont recalculés au +1 an [M§10.2] : le montant exact après le 27/10 manque, à lire dans l'export club de mardi.
- Test de potentiel (25 000) : non, il consommerait 30 % du plafond pour un joueur de 25–29 ans dont le potentiel pèse peu (âge, [M§8.5]).

## 3. Ventes (taxe 5 %, minimum de 8 disponibles : 17 aujourd'hui, 15 après les deux ventes)
| Joueur | Âge / poste | PS (S1 → S2) | Salaire | Minutes ligue (4 derniers) | Rang à sa place | Référence de prix | Verdict |
|---|---|---|---|---|---|---|---|
| **Min-jun Dang** | 29, SG | 49,9 → 48,9 | 20 636 | 24,0 | 4e SG | SG 26–29 médiane 300 000 (n=29, p25 10 000, p75 700 000) ; SG 30+ médiane 10 000 (n=7) | **Vendre maintenant** |
| **Nael Fontaine** | 30, PG | 43,6 → 42,6 | 16 289 | 6,0 | 7e PG | PG 30+ médiane 51 000 (n=13, p25 10 000, p75 86 804) | **Vendre maintenant** |
| Oscar Richard | 24, PG | 55,7 → 57,3 | 24 719 | 18,0 | 2e PG | PG 22–25 médiane 70 000 (n=29) | **Garder** |
Raisons :
- Dang : sa valeur s'effondre à 30 ans (médiane SG 300 000 → 10 000 entre les tranches 26–29 et 30+), et le +1 an tombe la nuit du 26 au 27/10 ; une enchère lancée aujourd'hui finit avant. Il est à 0 min dans le plan J22 (brief Tactique). Il économise 20 636/sem. Net attendu : 95 % du prix final, **confiance faible** (tranche 26–29 très dispersée ; PS 49,9 sans potentiel connu). Son dernier entraînement (brief Effectif, dimanche 04:00) reste sans coût pendant la vente.
- Fontaine : 30 ans, déclin dès 31 [M§8.5], eval 2,8 en 40,7 min, 6 min sur les 4 derniers matchs. Net attendu ≈ 48 000 si le prix reste à la médiane (95 % de 51 000), confiance faible ; la vente économise 16 289/sem., soit ≈130 000 sur 8 semaines de S2.
- Richard : 24 ans, progression, potentiel 8 (confiance élevée), 2e PG. Le brief Effectif note sa faible production (eval 4,4) mais l'âge et le PS prévu 57,3 pèsent plus ; une vente à ~70 000 n'apporte pas d'argent utile.
- Impact sur les autres briefs (**à relancer côté Tactique si l'utilisateur met Dang et Fontaine en vente**) : Fontaine est PG de l'amical Debrecen (lundi 08:00, Q2 et OT) et Dang est 2e PG/SG/SF du depth chart ; je ne sais pas si un joueur en vente peut jouer. Il me manque cette règle, on la réunit comme ça : lire le manuel [M§11.1] sur l'écran de mise en vente, ou mettre Fontaine en vente seulement après l'amical de lundi 08:00 si l'écran l'empêche de jouer.
- Réserve des deux ventes : aucun besoin d'argent immédiat (solde 1 107 000) ; l'enjeu est la masse salariale S2 (−36 925/sem. pour les deux).
- Taxe dégressive à l'étude chez le dev (pas décidée, [Dev 2026-10-22, economy]) : sans effet ici, ce ne sont pas des reventes d'achats récents.

## 4. Conseils suivis
Ajoutés dans `outputs/basketvibe/learnings.md` : C-053 (vente Dang), C-054 (vente Fontaine), C-055 (libre grand, maximale 80 000).

## Données manquantes
1. Export du marché de moins de 24 h (ci-dessus).
2. Salaires recalculés de la saison 2 : export club de mardi 27/10.
3. Règle « un joueur en vente peut-il jouer » : à lire sur l'écran de mise en vente.
4. PS et compétences exactes des vendus pour la référence de prix de Dang/Fontaine : `bv_market_price_known` en couvre 89 ventes seulement.
