# Carte sixzeroleague — finances (solde, sponsor, infrastructures)

Sources lues : commit 0000000 (2026-11-02)

Écrite le 2026-11-02 (fiche `finances.md`, skills `sixzeroleague-club`, `-match` § multiplicateurs, `-communaute` § 4 ; connaissance § 3, § 6). Plus d'agent `finances` depuis le 2026-11-02 : je lis ces vues moi-même. Pas de personnel dans ce jeu. Hypothèses de projection en tête de `sql/gold/013_sz_gold.sql` (9 cycles par saison, ~1 match à domicile par cycle) : les rappeler.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:70 | solde actuel | var. 1 |
| :71 | dépenses | var. 2 |
| :72 | salaires | var. 3 |
| :73 | entrées d'argent | var. 2 |
| :74 | acheter ? infrastructure ? rien ? | var. 5, 6, 8 |
| :75 | quoi faire dans le futur | var. 4 |
| :76 | sponsors | var. 7 |
| :168 | beaucoup d'argent | var. 5, 8 |

## Rendu (figé)
1. `| Solde réel | Dernier cycle net | Prévision du cycle | Salaires / recettes | Fin de saison (sans / avec victoires) |`.
2. Infrastructures : `| Installation | Niveau | Niveau visé | Coût | Gain net par cycle (min–max) | Cycles pour rembourser | Finançable |` (Arena, Fan Shop ; Training Facilities et Youth Academy jugées sur la progression et la relève).
3. Sponsor (si `sponsor_can_choose`) : `| Offre | Fixe × cycles | Prime de victoire × victoires attendues | Prime de signature | Total saison |`.
4. Une décision unique, avec le chiffre qui la justifie.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Solde réel | `select day, balance, since_last_report from silver.sz_finances order by day desc limit 1` | `balance` du dernier jour, pas `closing_balance` (un achat après règlement n'est que dans `since_last_report`) | fiche académie § Règles de données | 1 559 € (01/11) |
| 2 | Cycles | `select applied_at, revenue, expenses, wages, net, tickets, fan_shop, sponsor, prizes, maintenance, infrastructure_spend, transfer_net from gold.sz_finance_cycles order by applied_at desc limit 5` | Hors saison : ni recettes ni entretien | fiche finances § 1 | |
| 3 | Masse salariale | `wages_pct_revenue` de `gold.sz_finance_projection` | Salaires revus entre les saisons : les progrès alourdissent la masse suivante | fiche finances § 2 | |
| 4 | Projection | `select balance, cycles_left, fc_net, end_balance_no_wins, expected_wins_left, end_balance_with_wins, sponsor, sponsor_can_choose from gold.sz_finance_projection` | Revenus, coûts, entretien × division (pas les salaires) | `resume.md` § Rythme | |
| 5 | Infrastructures de revenu | `select facility, current_level, target_level, cost, net_gain_min, net_gain_max, payback_cycles_best, payback_cycles_worst from gold.sz_infrastructure_payback order by payback_cycles_best limit 8` | Fan Shop selon la place (1,6 × leader à 0,7 × dernier) ; coûts cachés, lus seulement dans `silver.sz_infrastructure_levels` | connaissance 3.1, 3.11 | Arena 7, Fan Shop 9 |
| 6 | Infrastructures de progression | `silver.sz_infrastructure_levels` | Training Facilities et Youth Academy : jugées sur la progression et la relève ; retard Youth Academy mesuré contre les autres clubs (carte `academie` var. 7) | fiche finances § 4 ; CLAUDE.md règle 6 | TF 6, YA 6 |
| 7 | Sponsor | `sponsor_offers`, `sponsor_can_choose` de `silver.sz_finances` | Changement une fois par saison, entre les saisons ; re-signer le même = pas de prime de signature ; offres repricées pour la division suivante | connaissance 6.2, 6.3 | C-045 |
| 8 | Dépenses décidées | `outputs/sixzeroleague/learnings.md` (C-044, C-052) ; registre `fait-` | Capacité = solde réel − dépenses décidées ; Youth Academy 6 → 7 = 6 200 € à payer dès que le solde le couvre | C-052 | |
| 9 | Primes | skill match | Top 3 : 15 000 / 8 000 / 4 000 (versée même si non affichée) | connaissance 6.1 | |
| 10 | Avis des amis | connaissance § 3, § 6 | Gazelle : revenus d'abord (Arena, Fan Shop) ; joueur : entraînement en dernier ; snowball des infrastructures | connaissance 3.12-3.14 | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
