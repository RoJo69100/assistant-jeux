> **Décision du 2026-10-23 (arbitrage de la session, remplace les consignes « ne pas monter l'Youth Academy » et « rien avant la fin de saison »)** : monter l'Youth Academy au niveau 4 (9 100 € cumulés, entretien 90/cycle ; prospects 4 à 26 au lieu de 1 à 20 ; source `silver.sz_infrastructure_levels` 2026-10-23) avant l'offre U18 attendue après J15 (26/10). Raison : c'est un investissement sportif (talent), pas un revenu ; le niveau 1 plafonne à 20. Arena 8 vient après. Solde : 5 235 € le 23/10 + environ 3 400 € par cycle, soit ~15 000 € au cycle précédant J15, réserve de 2 300 € conservée.

# Six Zero League — brief Finances du 2026-10-23

**Export manquant : aucun.** `silver.sz_finances` est daté du 2026-10-23 (captures 06:49-06:51 UTC), après le dernier cycle réglé (2026-10-22 20:14 UTC, `gold.sz_finance_cycles`). Briefs amont lus : Match et Effectif du jour (pas de Veille).
**Contradiction avec les briefs amont : aucune sur les faits.** Nuance sur un avis : Effectif conseille de garder la formation RW de Blanc car « l'investissement est fait ». Les 150 par cycle à venir ne sont pas un coût déjà payé (voir Actions 2).

## Alerte
**Pas d'alerte de fonctionnement.** Le cycle du 22/10 est à −6 914 € (solde 12 149 → 5 235) à cause des 10 700 € d'infrastructures (`gold.sz_finance_cycles`). Hors infrastructures : +3 786 € (recettes 6 076 − dépenses 2 290). Prévision du prochain cycle : +3 306 € (`silver.sz_finances`, `fc_net`). Risque : le solde (5 235) est bas ; toute dépense d'investissement avant la fin de saison le met en danger. Pas de pénalité de solde négatif décrite [W:Finances], mais il empêcherait d'acheter.

## Actions
| # | Quoi (écran) | Date limite | Pourquoi | Confiance |
|---|---|---|---|---|
| 1 | Infrastructures : n'améliorer rien avant la fin de saison (~27/10) | en continu | Solde 5 235 pour une réserve de 2 300 (1 cycle de dépenses) : capacité ~2 900, Arena 8 coûte 7 500 et Fan Shop 10 coûte 5 400 | moyenne |
| 2 | Équipe, Training : décider si la formation RW de Blanc continue | avant 21:00 Paris (règlement du soir) | Elle coûte 150 par cycle (2 290 = 1 550 salaires + 590 entretien + 150), pour ~12,5 cycles restants, soit ~1 875 non encore payés. Annuler ne rembourse rien [W:Training] mais arrête la dépense. Arbitrage sportif à l'agent Entraînement (RW a déjà 3 joueurs) | faible |
| 3 | Sponsor : ne rien faire maintenant | — | `sponsor_can_choose` = faux ; le choix ouvre entre deux saisons (voir § Sponsor) | forte |

## 1. Masse salariale (`silver.sz_finances`, `gold.sz_finance_projection`)
Faits : salaires 1 550 par cycle pour des recettes prévues de 5 596, soit 27,7 %. Salaires 1 230 (18/10), 1 325 (20/10), 1 550 (23/10) : +320 en 5 jours (Barros arrivé aux relevés du 23/10 à 110 ; le reste non expliqué ici). Soutenable : oui, marge de recettes sur salaires et entretien de 3 456 par cycle. Règle : les salaires ne changent qu'entre les saisons, et l'entraînement les alourdit à la saison suivante [W:Finances] : on s'attend à une hausse au changement de saison (taille non chiffrable ici).

## 2. Capacité d'investissement
| Horizon | Solde | Réserve | Disponible |
|---|---|---|---|
| Maintenant | 5 235 | 2 300 | ~2 900 |
| Fin de saison sans victoire (5 cycles) | 21 765 | 2 300 | ~19 500 |
| Fin de saison, 8 victoires attendues | 25 605 | 2 300 | ~23 300 |
Hypothèses (`sql/gold/013_sz_gold.sql`, `014_sz_cycles.sql`) : 5 cycles restants, 1 match à domicile par cycle, prévision constante de +3 306, 480 par victoire, aucune prime de ligue (Champion 15 000, 2e 8 000, 3e 4 000 [W:Competitions], clubs humains, à la dernière journée : non comptée, nous sommes 3e). Confiance moyenne : la projection ignore les primes et les hausses de salaire.

## 3. Sponsor (sponsor actuel Yarrow Health, `sponsor_can_choose` = faux)
Faits (`silver.sz_finances.sponsor_offers`) : Trident Freight 1 400 fixe, 0 signature, 120 par victoire ; Yarrow Health 1 070, 1 070, 480 ; Ashford Dairies 600, 600, 1 000. Changement une fois par saison, entre deux saisons [W:Sponsors] ; re-signer le même sponsor fait perdre la prime de signature [Dev chat].
Estimation pour une saison de 9 cycles (hypothèse : prime par victoire de ligue, 18 matchs ; montants de la division actuelle, ils seront multipliés si on monte) :
| Offre | 9 victoires (50 %) | 13 victoires (75 %) |
|---|---|---|
| Trident Freight | 13 680 | 14 220 |
| Yarrow Health (re-signer, sans prime) | 13 950 | 16 110 |
| Yarrow Health (si on le choisit comme nouveau) | 15 020 | 17 180 |
| Ashford Dairies | 15 000 | 19 500 |
Avis (confiance faible à moyenne) : Ashford Dairies à la saison suivante, meilleur dès 7 victoires sur 18 contre un re-signing de Yarrow ; nous en avons 6 sur 8 (`silver.sz_standings`). Limites : les montants perçus ne se rapprochent pas exactement de « fixe + 480 × victoires » (sponsor 2 030 au cycle du 22/10, 2 990 au cycle du 20/10), donc la façon dont les primes sont versées n'est pas confirmée ; relire les offres à l'ouverture du choix et refaire le calcul.

## 4. Infrastructures (`gold.sz_infrastructure_payback`, niveaux Arena 7 et Fan Shop 9)
| Option | Coût | Gain net par cycle | Remboursement (cycles) |
|---|---|---|---|
| Arena 8 | 7 500 | 370 | 20,3 |
| Arena 9 | 16 500 | 790 | 20,9 |
| Fan Shop 10 | 5 400 | 137 à 371 | 14,6 à 39,4 |
| Fan Shop 11 | 11 800 | 276 à 753 | 15,7 à 42,8 |
Lecture : à 9 cycles par saison, le meilleur remboursement est de 1,6 saison (Fan Shop 10 si nous finissons haut), le plus sûr est 2,3 saisons (Arena 8). Le Fan Shop dépend du classement (nous 3e). Recommandation (confiance faible) : rien avant la fin de saison ; ensuite, Fan Shop 10 (5 400) seulement si le solde dépasse ~8 000 après réserve et si nous finissons dans les 3 premiers, sinon Arena 8. Rappel : Training Facilities et Youth Academy se jugent sur la progression, pas en remboursement (non chiffrées ici). La décision « Fan Shop 7 ou Arena 7 » du 18/10 est close : l'argent a été dépensé le 22/10 (10 700) ; le détail par installation n'est pas dans la vue lue.

## Conseils suivis
C-005 ajouté dans `outputs/sixzeroleague/learnings.md`.

## Limites
- Une vue gold ne distingue pas les installations achetées le 22/10 : je n'ai pas relu silver pour le détail.
- Entretien : 590 par cycle (`gold.sz_finance_cycles`) ; l'entretien cesse hors saison [fiche], la formation de rôle hors saison est inconnue.
