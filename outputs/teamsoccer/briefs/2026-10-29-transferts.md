# Team Soccer — brief Transferts du 2026-10-29 (deux clubs)

Briefs amont lus : Match, Tactique Cows, Tactique Donkey du 29/10. Données : `gold.ts_capacite_invest` (finances du 27/10, 2 jours), `gold.ts_effectif_bilan` (29/10), `silver.ts_transfer_listings` (masculin vu 29/10 13:07 UTC ; **féminin vu 27/10 21:08 UTC, plus de 24 h**). Règles : un achat par semaine, revente bloquée 7 semaines [skill teamsoccer-club].

## Chomelix Cows (marché masculin)
**Finançabilité** : capacité 831 582 $ (solde 2 328 978 − réserve 374 896 − places de stade décidées 1 122 500).

| Poste | Titulaire / clé | Meilleure annonce | Verdict |
|---|---|---|---|
| GB | R. Thomas, Gardien 100 | Coufal 44 OVR, 239 034 $ | Garder : plafond atteint |
| DEF | Ounahi, Simon, Dubois, Th. Thomas : Défense 100 | Zieliński 47 OVR, 267 689 $ (fin 11:04 UTC, passée) | Garder : 4 titulaires à 100 |
| MIL | L. David, C. Robert, A. Roux : Conduite 100 | Klein 48 OVR, 349 144 $ | Garder : annonces à OVR ≤ 51, Conduite inférieure à 100 |
| ATT | Moreau, M. David, Bonnet : Finition 100 | Marica 48 OVR, 188 006 $ | Garder |

- **Achat : aucun.** Aucune annonce masculine ne dépasse un titulaire (OVR max 51 contre titulaires 65 à 90, compétence clé 100). Gain d'un achat = 0 point sur les 11 ; seul le banc à Forme 72 (Jules Leroy) est faible, et le jeu l'améliore le vendredi.
- 🟥 **Vente à décider : Baptiste Girard (298192)**, DEF 16 ans, Défense 67, surplus rang 6 sur 4 places (`ts_effectif_bilan`), exclu du banc par la Tactique. **Vendre à la banque ce soir : 267 689 $** (valeur de la fiche, sans commission, immédiat), salaire économisé 2 677 $/semaine. Effectif 22 → 21 (min 16). Doute : sa valeur monte de 4 à 6 % par semaine (≈ +11 à 16 k$), négligeable face à une place de banc qu'il n'occupe pas. Pas de contrainte de revente : il n'a pas été acheté.
- Surplus à garder (vente non chiffrée utile) : Thomas Roux (367 200 $), Étienne Roux, Hugo Martin, Lefebvre, Petit sont des jeunes qui progressent ; aucune vente conseillée aujourd'hui, un seul départ à la fois pour ne pas fragiliser le moral (chute après vente [connaissance 6.10]).
- **Ventes ouvertes** : Jules Bonnet (297340, FWD 16, 135 162 $, 0 offre, fin 30/10 22:08 UTC) et Jules Bernard (297339, MID 16, 282 838 $, 0 offre, fin 30/10 22:08 UTC) sont encore listés par Chomelix Cows dans le marché de 13:07 UTC et absents de l'effectif : ventes à la banque en attente du règlement, rien à faire.
- **Enchères ouvertes** : `silver.ts_my_bids` (Cows) liste 8 identifiants d'annonces au 29/10, sans prix ni statut en base (il me manque l'état de ces enchères : l'export Marché Cows montre la colonne « mon offre »). Le brief Basket précédent n'est pas concerné ; aucune enchère maximale à poser aujourd'hui puisqu'aucune cible n'est retenue.

## Ben Ahmed Donkey (marché féminin)
**Finançabilité** : capacité 253 315 $ (solde 505 349 − réserve 252 034). Aucune dépense décidée.

🟥 **Il me manque** le marché féminin d'aujourd'hui : dernier relevé le 27/10 21:08 UTC (plus de 24 h). On l'obtient ainsi : ouvrir le Marché de Ben Ahmed Donkey et lancer le script d'export. Sans cela le verdict ci-dessous porte sur les annonces encore ouvertes du 27/10.

| Poste | Titulaires / clé | Meilleure annonce ouverte | Verdict |
|---|---|---|---|
| GB | Abdel, Gardien 81 | González 38 de Gardien, 72 888 $ | Garder |
| DEF | García 90, Fernández 83, Taylor 79, A. Fournier 79 | Mori 48 de Défense, 144 813 $ | Garder (annonce de Ben Ahmed lui-même) |
| MIL | Kumar, Martínez, Mansour : Conduite 62 | Hernández Dribbling 48, 154 912 $ | Garder : 48 < 62 |
| ATT | Müller 88, Yamamoto 87 | Rao Finition 48, 154 912 $ | Garder |

- **Achat : aucun.** Les 6 annonces encore ouvertes ont toutes une compétence clé inférieure à celle de nos titulaires (écart 14 à 40 points). Les milieux à 62 de Conduite sont le seul poste faible, mais aucune annonce ouverte ne dépasse 48.
- **Vente : aucune.** Surplus (Ibe 488 743 $, Hayashi 488 743 $, Schmidt et Suzuki en GB 466 862 / 445 645 $) mais ce sont des remplaçantes ou surplus utiles en cas de blessure (effectif 23 sur 24) et la capacité n'est pas à financer : aucune vente aujourd'hui.
- **Ventes ouvertes** : Min-ji Mori (297341, 144 813 $, 0 offre, fin 30/10 22:08 UTC) reste listée par Ben Ahmed ; Nanami Rousseau (297198, 239 034 $) a une fin passée (27/10 22:08 UTC), vendue ou retirée : à confirmer par l'export du marché féminin.
- **Enchères ouvertes** : aucune du club en base.

## Conseils suivis
C-049 (vente de Girard) ajouté à `outputs/teamsoccer/learnings.md`. Preuve : Girard (298192) absent de `silver.ts_players` équipe 18 et solde en hausse de 267 689 $ au prochain relevé finances.

## Ce qui prouvera que j'avais tort
Aucun achat : faux si un titulaire (Moreau, Bonnet, Ounahi...) est blessé ou suspendu et que le banc (Forme 72) coûte plus de 6 points de clé par poste ; dans ce cas, réexaminer le marché de la semaine, en respectant la limite d'un achat par semaine.
