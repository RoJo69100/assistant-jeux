# Six Zero League — brief Finances, 2026-10-24

Briefs amont lus : `2026-10-24-match.md`, `2026-10-24-effectif.md`. Export Finances et infrastructures du 2026-10-24 (20:13 UTC, cycle 6 réglé) : à jour. Règles : skill `sixzeroleague-club` [W:Finances, W:Sponsors, W:Infrastructure], fiche finances. Chiffres : `silver.sz_finances`, `gold.sz_finance_cycles`, `gold.sz_finance_projection`, `gold.sz_infrastructure_payback`, `silver.sz_infrastructure_levels`.

## En tête : pas d'alerte, une action
- **Ne rien acheter aujourd'hui** (ni Arena, ni Fan Shop, ni Training Facilities, ni Youth Academy). Aucun transfert (déclaré). Garde le solde de 6 645 €.
- Pas de perte : cycle 6 net +133 € seulement parce que 3 000 € ont été investis (infrastructure) ; hors investissement, +3 133 €.
- Sponsor : rien à faire, choix impossible avant l'inter-saison (`sponsor_can_choose` faux).

## 1. Alerte (faits)
| Cycle | Net | Recettes | Dépenses | Dont infra | Solde fin |
|---|---|---|---|---|---|
| 5 (23/10) | +1 277 | 5 942 | 4 665 | 2 500 | 6 512 |
| 6 (24/10) | +133 | 5 328 | 5 195 | 3 000 | 6 645 |
| 7 (prévision) | +3 133 | 5 328 | 2 195 | 0 | ~9 778 |
- Cause du net faible du cycle 6 : investissement de 3 000 € (non récurrent). Recettes en baisse de 614 € : prime de victoire 480 € absente (aucune victoire de ligue dans le cycle), Fan Shop 1 742 -> 1 608 (-134).
- Prévision cycle 7 : billetterie 2 650 + Arena 1 750 (inclus dans les 4 400 du cycle) + Fan Shop 1 608 + sponsor 1 070 ; entretien 645 € (Obs : 615 -> 645, +30 avec le niveau Fan Shop 9).
- Projection (`gold.sz_finance_projection`) : 3 cycles restants ; fin de saison **16 044 € sans victoire**, 17 964 € avec 4 victoires attendues. Hypothèses : 1 match à domicile par cycle, 9 cycles par saison (fiche). Confiance moyenne : la ligne « 4 victoires attendues » est celle de la vue, non recalculée ; nos résultats récents sont mauvais (J11 17-27).

## 2. Masse salariale
- `fc_wages` 1 550 / `fc_revenue` 5 328 = **29,1 %**. Soutenable sans vente de joueurs : le cycle reste à +3 133 €.
- Marge avant le rouge : 6 645 € de solde, soit environ 2 cycles de dépenses sans aucune recette (2 195 € de dépenses hors infra). Salaires fixes jusqu'à l'inter-saison ; ils montent ensuite avec les progrès d'entraînement [W:Finances]. Salaires cycle 2 -> 6 : 1 325 -> 1 550 (+225).

## 3. Sponsor (Yarrow Health, Medium)
- Actuel : fixe 1 070 / prime 480 par victoire de ligue. `sponsor_can_choose` faux : changement possible seulement entre deux saisons [W:Sponsors].
- Règle : re-signer le même sponsor = pas de prime de signature [Dev chat, skill communaute § 4].
- Offres actuelles (`sponsor_offers`), calcul sur 9 cycles, sans prime de signature, w = victoires de ligue de la saison :
| Offre | Fixe x 9 | Prime | Total |
|---|---|---|---|
| Trident Freight (Low) | 12 600 | 120 x w | 12 600 + 120 w |
| Yarrow Health (Medium) | 9 630 | 480 x w | 9 630 + 480 w |
| Ashford Dairies (High) | 5 400 | 1 000 x w | 5 400 + 1 000 w |
- Trident bat Yarrow tant que w < 8,25 ; Trident bat Ashford tant que w < 8,2. Avec 18 journées de ligue, un seuil de 8 victoires = moins de la moitié des matchs. Cette saison, nos résultats récents (défaites en J8, J10, J11) donnent w faible : **choix à l'inter-saison : Trident Freight**, sauf si le nombre de victoires de la saison dépasse 8 (à vérifier dans `silver.sz_standings` à ce moment). Les offres seront recalculées pour la division suivante [W:Sponsors], et la prime de signature (0 pour Trident, 1 070 Yarrow, 600 Ashford) compte une seule fois, donc ne change pas le classement. Confiance moyenne.
- Il me manque : le nombre de victoires de ligue de la saison en cours. On le réunit comme ça : `silver.sz_standings` (colonne victoires), à relire au début de l'inter-saison.

## 4. Infrastructures
| Installation | Niveau | Suivant : coût | Gain net / cycle | Remboursement (cycles) | Verdict |
|---|---|---|---|---|---|
| Arena | 7 | 8 : 7 500 | +370 | 20,3 | non |
| Fan Shop | 9 | 10 : 5 400 | +137 à +371 | 14,6 à 39,4 | non |
| Training Facilities | 6 | 7 : 6 200 (entretien 230/cycle) | non mesuré | — | non |
| Youth Academy | 4 | 5 : 4 300 (entretien 130/cycle) | non mesuré | — | non |
- Pourquoi attendre : 9 cycles par saison. Le meilleur remboursement (Fan Shop 10, 14,6 cycles) dépasse une saison et demie ; le pire (39,4) plus de quatre saisons. Les remboursements de l'Arena (20,3 cycles) ne s'améliorent pas avec les niveaux (24,2 au niveau 11). Hors saison, ni recettes ni entretien (fiche) : acheter maintenant ne rapporte que 3 cycles sur cette saison.
- Fan Shop 10 : le gain dépend de la place en ligue (1,6 x leader à 0,7 x dernier [Dev chat, devlog 0.5.7]). Notre place actuelle (8e avant J11) donne le bas de la fourchette (+182 brut, 39,4 cycles au pire). Pas rentable.
- Training Facilities et Youth Academy : se jugent sur la progression et la relève, pas en remboursement (fiche). Training Facilities 7 : 1,36 x rendement d'entraînement ; la fiche note l'effet comme incertain [Dev chat 2026-10-19]. Je ne l'achète pas : 6 200 € laisseraient 445 € au solde.
- Décision en attente depuis le 2026-10-18 (Fan Shop 7 ou Arena 7) : **tranchée, déjà faite** (Arena 7 et Fan Shop 9 atteints). Prochain achat à reconsidérer en inter-saison, quand le solde dépasse 16 000 € : le candidat est Fan Shop 10 (5 400 €), à condition d'être monté dans le classement.

## 5. Capacité d'investissement
- Maintenant : 0 € conseillé. Réserve de sécurité = 2 cycles de dépenses = 4 400 € ; solde 6 645 € -> 2 245 € disponibles, insuffisant pour toute amélioration (la moins chère coûte 4 300 €).
- Fin de saison : 16 044 € sans victoire ; réserve 4 400 € -> environ 11 600 € disponibles. Hypothèse : aucun transfert, aucune prime de ligue (le cycle 9 de la saison précédente a rapporté 15 000 € de primes : dépend du classement final, non projeté).

## 6. Conseil suivi
- **C-014** ajouté à `outputs/sixzeroleague/learnings.md` (critère : aucune dépense d'infrastructure d'ici la fin de saison, solde >= 6 645 €).
