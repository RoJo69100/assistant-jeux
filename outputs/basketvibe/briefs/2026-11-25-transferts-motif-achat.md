# Transferts BasketVibe du 25/11/2026 (14:30 Paris) — brief refait avec la règle de motif d'achat

Propositions seulement : **aucune enchère sans accord écrit**. Remplace le motif « gain de banc » de `2026-11-25-transferts-relance.md`.

## Règle (code : `pipelines/etat_jour.py` `motif_achat`, yaml `offres.motif_achat`)
Un achat n'est proposé que pour :
- **(a) amélioration** : il entre dans le cinq. Seuil : la meilleure affectation du cinq réel avec lui gagne **≥ 1,0 point d'ajustement** (`gain_ajustement_min`, `gold.bv_slot_fit`) sur le cinq actuel (`gain_cinq`) ;
- **(b) jeune** : 16 à 18 ans, test de potentiel connu High ;
- **(c) revente** : prix ≤ **(médiane de la case × 0,95 − 1 semaine de salaire) / 1,25**, soit une marge nette ≥ 25 % après la taxe de 5 % et le salaire ; étiquetée « revente ».
Le gain sur notre n°2 du poste n'est plus un motif.

Correction : le brief de 13:20 comparait au meilleur ajustement du poste dans tout l'effectif (SG 60,7 = Gimenez, qui joue SF). Le cinq réel du 25/11 (fiche Žirmūnai, et 5 joueurs aux plus de minutes de ligue) est Richard PG 56,8 · Bonnet SG 52,1 · Gimenez SF 60,3 · Fournier PF 52,7 · Lefebvre C 63,2 (somme 285,1).

## Les 4 candidats
Données : `gold.bv_market_candidates` (export du Marché de 13:00), cases de prix `prix_cases_poste`, capacité 955 391 (`gold.finance_health` du 25/11).

| Candidat | Poste, âge, PS | Ajustement | Gain du cinq | Motif | Enchère max (règle amélioration : min(p75, capacité − salaire)) | Prix actuel, fin | Police du jour | Survit ? |
|---|---|---|---|---|---|---|---|---|
| Sreten Miletić | SG, 27, 59,9 | SG 59,3 | **+7,2** (remplace Bonnet 52,1) | amélioration | 926 991 (case n = 19, p75 1 208 815) | 39 000 (3 offres), 26/11 20:43 | plafond 750 000 (`police-2026-11-25.md`) | **oui** |
| Svetozar Janketić | PG, 26, 58,9 | PG 58,8 | **+6,2** (Richard passe SG, Bonnet sort) | amélioration | 926 891 (n = 18) | 205 000 (3), 26/11 23:50 | « ne pas acheter » (jugé gain de banc) | **oui** par la règle, police à refaire |
| Angelo Gupta | C, 27, 56,2 | C 55,5 | **+2,8** (Lefebvre passe PF, Fournier sort) | amélioration | 929 291 (n = 12) | 1 260 (3), 26/11 17:16 | plafond 733 875 (`police-2026-11-25-b.md`) | **oui** (gain le plus faible) |
| Jin-woo Tan | SF (joue SG), 28, 58,3 | SG 58,1 | **+6,0** (remplace Bonnet) | amélioration | 928 791 (n = 18) | 0 = prix inconnu (1 offre), 26/11 17:16 | « ne pas enchérir en premier », max 674 500 | **oui**, même poste que Miletić |

Les 4 survivent par le motif (a) ; aucun par la revente seule.

## Décision
**Fais : Miletić seulement, enchère maximale 750 000** (plafond de la police, sous l'enchère max de la règle). Il a le plus gros gain du cinq (+7,2) et la capacité (955 391) ne finance qu'un achat (deux achats à 750 000 = 1,5 M). Ce n'est qu'une proposition : rien n'est posé sans ton accord écrit.
Doute : la police a jugé Miletić sur un gain de +3,0 (comparé au n°2). Avec +7,2, le plafond de 750 000 reste prudent (sous le p25 de 840 000, L-028 : il peut perdre l'enchère). Ce qui prouvera que j'ai tort : prix final > 750 000, ou éval/min de Miletić < Bonnet (52,1) sur 3 matchs de ligue.
Janketić : la police l'a écarté comme gain de banc ; par la nouvelle règle il entre dans le cinq (+6,2). Police à refaire seulement si tu le préfères à Miletić.
