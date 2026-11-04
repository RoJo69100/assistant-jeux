# Carte sixzeroleague — achat (enchère, joueur libre)

Sources lues : commit 8791d35 (2026-11-02)

Écrite le 2026-11-02 (fiche `transferts.md`, skills `sixzeroleague-club` § Marché, `-joueurs`, `-entrainement`, `-communaute` ; connaissance § 6). Règles : A-4 (jamais d'enchère sans accord) ; `capacite_invest` moins dépenses décidées couvre le prix, sinon cible abandonnée ; règle 20 (marché de plus de 12 h ici, règlement chaque soir : « exporte le marché »).

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:74 | acheter un joueur ? | var. 1, 6 |
| :86 | base « ce type vaut ce prix » | var. 5 |
| :87 | étudier le marché, acheter / revendre | var. 1, 9 |
| :168 | beaucoup d'argent | var. 6 |

## Rendu (figé)
1. Marché vu il y a plus de 12 h (`seen_at`) : « 🟥 URGENT · Export · exporte le marché ».
2. `| Priorité | Cible | Rôle | Âge | Note | Compétences clés du rôle | Notre titulaire / remplaçant au rôle | Gain | Prix actuel | Enchère max | Salaire | Règlement (journée) | Finançable |`.
3. Une ligne par cible : pourquoi, ce qui prouvera l'erreur. Rien n'est lancé sans accord ; aucune annonce à retirer (annulation impossible).

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Annonces | `select role, age, overall, wage, retiring, starting_price, current_bid, next_bid, free_agent, seller_is_bot, settle_after_round, seen_at from silver.sz_transfer_listings order by overall desc limit 20` | Compétences visibles de tous : comparer les 20 compétences au rôle, jamais la note seule | fiche transferts § 2 | |
| 2 | Place dans l'équipe | `select ord, slot, rank_in_slot, name, rating, key_skills_avg, available_depth, no_natural_backup from gold.sz_role_report order by ord, rank_in_slot limit 30` | Cible meilleure que notre titulaire, ou rôle sans remplaçant naturel | fiche effectif § Livrable 1 | |
| 3 | Âge et retraite | `age`, `retiring` | Bonus jeune jusqu'à 20 ans, baisse dès 28, déclin physique dès 30, retraite possible dès 33 ; annonce de retraite = invendable | connaissance 5.9, 5.10, 6.13 | |
| 4 | Salaire | `wage` | Fixé selon le niveau, revu seulement entre les saisons : compter le salaire en plus du prix | fiche transferts § 3 | |
| 5 | Prix de référence | — | Pas de ventes conclues en base : confiance faible, le dire ; prix de départ minimum 1 000 €, pas d'enchère 1 000 € | fiche transferts § 4 ; connaissance 6.10 | |
| 6 | Argent disponible | `select balance, since_last_report, fc_net from silver.sz_finances order by day desc limit 1` ; `gold.sz_finance_projection` | Solde réel = `silver.sz_finances.balance` (pas `closing_balance`) ; prix + salaire > solde moins dépenses décidées (C-044, C-052) = abandon | fiche académie § Règles de données ; CLAUDE.md § Horizon | solde 1 559 € (01/11, C-052) |
| 7 | Règlement | `settle_after_round` | Enchère = 2 journées, réglée au coup d'envoi suivant ; intersaison réglée après la manche 2 du 01/11 | connaissance 6.6 ; `resume.md` § Rythme | |
| 8 | Effectif | `select count(*) from silver.sz_players` | 7 minimum, 30 maximum | connaissance 6.12 | 16 |
| 9 | Revente | — | Garder un joueur à forte éthique de travail pour le revendre si Training Facilities hautes (avis du développeur) | connaissance 5.11 | |
| 10 | Joueur libre | `free_agent` | Joueur libéré : 10 % de chances de réapparaître | connaissance 6.7 | |
| 11 | Avis des amis | connaissance § 6 | « Vends ce dont tu n'as pas besoin pour rester compétitif » ; des bons joueurs apparaissent à vendre | Gazelle (6.8) ; joueur (3.13) | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis | Statut (base) |
| --- | --- | --- | --- | --- |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
