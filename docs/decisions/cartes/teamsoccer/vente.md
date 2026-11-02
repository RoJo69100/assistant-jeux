# Carte teamsoccer — vente (banque immédiate ou enchère de manager 72 h ; deux clubs)

Sources lues : commit 81b8350 (2026-11-02)

Écrite le 2026-11-02 (fiche `transferts.md`, `effectif.md`, skills `teamsoccer-club` § Marché, `-joueurs` ; connaissance § 5). Règles : une vente identifiée reste ouverte jusqu'à exécution ; jamais de vente lancée sans accord ; effectif minimum 16.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:133 | ce joueur est-il à vendre | var. 1, 2 |
| :140 | faut-il vendre nos joueurs | var. 1-5 |
| :117 | monter un jeune et le vendre | carte `academie` var. 4 |

## Rendu (figé)
Un tableau par club : `| Priorité | Joueur | Zone | Âge | Compétence clé | Rang dans la zone | Statut | Remplaçant interne | Valeur (banque) | Enchère manager utile ? | Salaire économisé / sem. | Effectif après |`. Une ligne par joueur : pourquoi, ce qui prouvera l'erreur.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Candidats | `select team, zone, name, age, key_name, key_skill, rank_in_zone, starters_needed, statut, value, wage, squad_size, on_sale from gold.ts_effectif_bilan where statut in ('surplus','en vente') order by team, zone limit 20` | Surplus au-delà des titulaires + un remplaçant par zone | fiche effectif § Livrable 2 | |
| 2 | Remplaçant interne | même vue, zone du joueur, `rank_in_zone` suivant | Écart de compétence clé nommé | `resume.md` § Juger un joueur | |
| 3 | Banque ou enchère | `value` | Banque : valeur de la fiche, immédiat, sans commission ; enchère manager : 72 h, prix de départ ≤ valeur, 10 % de commission, utile seulement si l'acheteur dépasse la valeur de plus de 11 % ; sans offre le joueur revient | fiche transferts § 1 ; connaissance 5.7 | |
| 4 | Âge et progression | `age` ; `gold.ts_player_progress` | Progression nette jusqu'à ~23 ans, nulle vers 27-28, perte ensuite ; talents perdus à 32 ans | fiche effectif § 4 | |
| 5 | Effectif minimum | `squad_size` | 16 au moins | fiche effectif § 1 | |
| 6 | Moral | — | Le moral baisse après une vente de joueurs (repart chaque lundi) | connaissance 6.10 | |
| 7 | Joueur en vente encore listé | `statut = 'en vente'` | L'export garde les joueurs vendus jusqu'à la fin de l'enchère ; homonymes : comparer `player_id` | `resume.md` § Pièges | |
| 8 | Financer un achat | carte `achat` var. 4 | Vendre d'abord quand l'enchère dépasse le solde | fiche transferts § Enchère et solde | |
| 9 | Avis des amis | connaissance § 5 | Ventes illimitées depuis le 2026-09-11 | connaissance 5.4 | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
