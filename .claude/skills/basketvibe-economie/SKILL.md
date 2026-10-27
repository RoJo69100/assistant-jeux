---
name: basketvibe-economie
description: Règles BasketVibe de l'économie et du personnel — billetterie et popularité, sponsor de saison, bonus homegrown, primes de classement, salaires (barème selon la moyenne des compétences), personnel (médecins, kinés, psychologues, marketing : effets, coûts, facturation), blocage des transferts. À charger pour toute question d'argent, de masse salariale, de capacité d'investissement ou de recrutement du personnel.
---

# BasketVibe — économie et personnel

Sources : **[M§x]** = manuel officiel https://www.basketvibe.com/guide (lu le 2026-10-16). **[Obs]** = nos données.

## Généralités [M§10]
- Budget de départ : **600 000** (le même pour tous). Le solde n'est pas remis à zéro entre les saisons.
- Charges fixes de la semaine, prélevées le **dimanche** : salaires, personnel, plus l'académie le **jeudi** [M§1.3].
- [Obs] Charges du 2026-10-16 : salaires 290 619 + personnel 70 000 + académie 100 000 = **460 619 par semaine**.

## Recettes
### Billetterie et popularité [M§10.1.1]
- Salle de **8 000 places**, billet à **50**, dans toutes les ligues. Spectateurs = places × popularité.
- Popularité : **+2 points par victoire à domicile** en ligue ; **−3 points par défaite à domicile**, −1 point de moins par spécialiste marketing (minimum 1 point avec deux). Les matchs à l'extérieur et les amicaux ne la changent pas.
- Popularité bornée entre 40 % et 100 % pendant la saison, remise à **70 %** en début de saison (≈ 5 600 spectateurs, **280 000** par match à domicile).
- Amical : ~6 % de la recette d'un match de ligue à domicile, la même pour les deux clubs.
- Coupes : pas de billetterie par défaut [M§3.3].
- [Obs] Billetterie de ligue de la saison 1 : 1 984 000 pour 8 matchs à domicile, soit 248 000 en moyenne ; popularité à 0,61 le 2026-10-16.

### Sponsor de saison [M§10.1.2]
- Six contrats au choix en début de saison : Stability, Balance, Win bonus, Top half, Podium, Championship. Sans choix avant la date limite (15 min avant la 1re journée) : Stability.
- Un montant de base chaque dimanche (8 versements maximum par saison), plus selon le contrat des primes par victoire ou de classement. Rater l'objectif ne fait perdre que la prime de fin.
- [Obs] Saison 1 : Ironvale « stability », 100 000 par semaine, 200 000 garantis restants le 2026-10-16.
- [Obs] Saison 2 (export 2026-10-27) : six offres, garanti = 8 × taux hebdo ; Stability 800k ; Fluxora 80k + 15k/victoire (640k–970k) ; Asterion 50k + 30k/victoire (400k–1,06M) ; Lunaro « top half » 85k (680k–1M) ; Pulseharbor « podium » 75k (600k–1,12M) ; Harborlane « championship » 70k (560k–1,2M). Choix avant le 02/11/2026 19:45. Le palier exact des primes de classement (top 6 ? 1re place ?) n'est pas confirmé. La saison compte 22 matchs (12 clubs en aller-retour ; KK Uola 22-0 en saison 1). L'écran « Wins: 12 / 22 » est un scénario, pas une prévision.
- [Utilisateur, 2026-10-27] Le sponsor ne peut pas être changé en cours de saison : le choix vaut pour toute la saison. Non écrit dans le manuel ; à reconfirmer si l'écran offre un changement.

### Bonus homegrown [M§10.1.3]
200 par minute de ligue jouée par les juniors signés à l'académie, plafonné à 40 000 par semaine, versé le dimanche. Exemple du manuel : ~20 min par match sur une saison ≈ 88 000.

### Primes de classement (fin de saison) [M§10.1.4]
| Place | 1 | 2 | 3 | 4 | 5–8 | 9–12 |
|---|---|---|---|---|---|---|
| Prime | 400 000 | 300 000 | 200 000 | 100 000 | 50 000 | 0 |
Pas d'autre pénalité financière en cas de relégation.

## Dépenses
### Salaires [M§10.2]
- Salaire hebdomadaire calculé sur la **moyenne des 8 compétences** (pas la forme, ni la fatigue, ni le potentiel). Prélevé chaque semaine pour les joueurs présents dans l'effectif. **Recalculé en fin de saison** : un joueur qui a progressé coûte plus cher.

| Moyenne des compétences | 40 | 50 | 60 | 70 | 80 | 90 | 99 |
|---|---|---|---|---|---|---|---|
| Salaire par semaine | ~14 000 | ~21 000 | ~31 000 | ~41 000 | ~54 000 | ~68 000 | 82 280 |

- [Obs] La somme des salaires affichés (onglet Tiles) donnait 288 517 le 2026-10-16, contre 290 619 payés le 2026-10-11 : écart de 0,7 %, cause inconnue.

### Personnel [M§4.3]
| Rôle | Postes | Effet par embauche | Coût par semaine et par poste |
|---|---|---|---|
| Médecin | 2 | −25 % de temps de récupération | 10 000 |
| Kinésithérapeute | 4 | −12,5 % de risque de blessure en match | 5 000 |
| Psychologue | 2 | +5 points vers l'amélioration de forme du dimanche | 10 000 |
| Spécialiste marketing | 2 | −1 point de perte de popularité par défaite à domicile | 12 500 |
- Personnel au complet en médical (2 médecins + 4 kinés) : −50 % de récupération et −50 % de risque. Coût maximum de tout le personnel : **85 000 par semaine**.
- Facturation : on paie le **nombre maximum** de chaque rôle employé pendant la semaine, même pour un seul match.
- Les kinés et le marketing comptent au coup d'envoi ; les médecins changent la vitesse de guérison à partir du jour de l'embauche (pas les jours déjà passés).
- [Obs] Le 2026-10-16 : 2 médecins, 1 kiné sur 4, 2 psychologues, 2 marketing = 70 000 par semaine.

## Blocage des transferts [M§10.3]
- Solde à zéro : plus d'enchère possible jusqu'au retour en positif (les salaires continuent).
- La somme de tes enchères maximales en cours ne peut pas dépasser le solde.

## Lecture de nos données
- `silver.bv_finance_weekly`, `silver.bv_finance_transactions` (seulement les 20 dernières à chaque export), `silver.bv_finance_seasons`, `silver.bv_sponsor_weekly`, `silver.bv_personnel_weekly`, `silver.bv_player_salary_weekly`.
- `gold.bv_finance_weekly_result` (résultat par semaine ; `complete` = semaine entièrement couverte) et `gold.bv_finance_projection`. La projection ne compte pas les amicaux, les coupes, les transferts ni les primes.
