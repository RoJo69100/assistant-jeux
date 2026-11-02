# Team Soccer — fiche Finances et Stade

Lue par moi (session principale) après `resume.md` : l'agent `finances` est retiré depuis le 2026-11-02 (étape 0d), son travail = les vues gold ci-dessous + ce livrable, sans brief d'agent. Cases E7 (finances) et E8 (stade) de la checklist Team Soccer. Pas de sponsor ni de personnel dans ce jeu, sauf l'entraîneur.

## Skills à lire
- `.claude/skills/teamsoccer-club/SKILL.md` (finances, stade, affluence, entretien)
- `.claude/skills/teamsoccer-entrainement/SKILL.md` (§ Entraîneurs : prix des niveaux)
- `.claude/skills/teamsoccer-saison/SKILL.md` (primes des compétitions)

## Règles propres au jeu
1. Semaine financière close le **lundi 00:05** (heure du site). Recettes : billetterie à domicile, ventes, primes. Dépenses : salaires, entretien du stade, achats, construction, entraîneur.
2. **Solde négatif** : pas de faillite, mais ni achat, ni agrandissement, ni entraîneur ; le moral baisse [skill club].
3. **Entretien = 6 % de la recette d'un match à guichets fermés**, chaque semaine. Bug de facturation déjà vu deux fois (2026-10-13, 2026-10-19) : **contrôler chaque lundi** (`maintenance_gap` doit valoir 0).
4. **Stade** : prix d'achat et recette par place (debout 80 $ / 7,50 $, basique 150 / 15, couverte 300 / 27,50, VIP 1 500 / 75) ; affluence selon division et rang ; coupes et amicaux partagés 50/50.
5. Entraîneur : niveau 2 à 1 000 000 $, puis 4, 10 et 25 millions ; un niveau à la fois.

## Données
- `gold.ts_finance_status` : par club, `balance`, `week_net`, `wage_bill` (= ligne salaires, vérifié), `stadium_maintenance` / `maintenance_expected` / `maintenance_gap`, `attendance_rate` (rang et division actuels), `gate_per_home_match`, `mondays_left`, `home_league_left`, `projected_season_end`, `alert_negative`.
- `silver.ts_finances` : un relevé par jour et par club, lignes de la semaine et cumuls de la saison.
- `gold.ts_stadium_payback` : par type de place, places, marge jusqu'au maximum, `home_matches_to_repay`, `repaid_this_season`.
- `gold.ts_season_calendar`.
- `projected_season_end` est une approximation : salaires + entretien chaque lundi, billetterie de ligue à domicile au rang actuel ; ni primes, ni coupes, ni ventes, ni amicaux.

## Livrable
1. Alerte et cause pour chaque club, date estimée du retour au positif.
2. Masse salariale soutenable ou non ; capacité d'investissement (entraîneur, places).
3. Stade : quelles places acheter, combien, quand (remboursement en matchs à domicile).

## Méthode d'analyse du stade (à suivre à chaque passage)
Le brief contient une section « Stade » par club avec quatre réponses chiffrées : (1) rentabilité, (2) remplissage, (3) agrandissement, (4) prix.
1. **Rentabilité** : billetterie par match à domicile (`gold.ts_finance_status.gate_per_home_match`) ; entretien annuel = `stadium_maintenance` × 9 semaines ; net par match = billetterie − entretien × 9/7 ; coût d'achat = `silver.ts_finances.total_stadium_building` ; remboursement = coût ÷ net par match. Les places non facturées (531 250 $, déduction identique chez les deux clubs) expliquent l'écart avec la valeur au prix d'achat.
2. **Remplissage** : `gold.ts_match_report` (`venue` = 'domicile', `spectators`, `fill_pct`) ; le taux est celui de la table division × rang et vaut pour chaque type de place ; places vides par type = places × (1 − taux). Capacité d'un match passé = spectateurs ÷ taux.
3. **Agrandissement** : remboursement d'une place avec entretien = prix ÷ (recette × (taux − 0,06 × 9/7)) ; comparer les types (le basique est le meilleur chez les deux clubs) ; acheter si ≤ 14 matchs ; taille de l'achat limitée par la capacité (solde − réserve de 2 semaines). Recalculer le taux avec la division et le rang de la saison suivante avant d'acheter en fin de saison.
4. **Prix** : fixés par le jeu (skill club) ; ne pas en conclure qu'ils sont modifiables.

## Données à exporter pour le stade
- Pages de match à domicile passées (historique d'affluence avant le 12/10 ; spectateurs par type de place s'ils sont affichés).
- **Ouvert** : un prix de billet est-il modifiable sur la page Stade ? L'utilisateur le vérifie et le dit ; à enregistrer ici.
- `silver.ts_stadiums` : dernier relevé au 2026-10-19 ; nouvel export Stade après chaque achat de places.
- Écart non expliqué : Ben Ahmed, 22/10, `match_income` 275 355 contre 266 980 attendus (8 375 $).

## Constat au 2026-10-19 [Obs SQL]
- Chomelix Cows −185 283 $, Ben Ahmed Donkey −112 482 $ ; entretien conforme (écart 0) ; projection fin de saison positive pour les deux (+878 706 $ et +413 078 $) si l'affluence suit.
- Aucune place n'est remboursée en une saison (12 à 27 matchs à domicile pour 5 ou 6 restants) : l'agrandissement est un investissement sur plusieurs saisons.

## Prix des billets (confirmé par l'utilisateur, 2026-10-23)
Le prix des billets est **fixe** : aucun champ modifiable sur la page Stade. Aucun levier prix ; ne plus le demander.
