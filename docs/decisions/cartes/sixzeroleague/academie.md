# Carte sixzeroleague — academie (choix U18 toutes les 8 journées, niveau de la Youth Academy)

Sources lues : commit 8791d35 (2026-11-02)

Écrite le 2026-11-02 (fiche `academie.md`, skills `sixzeroleague-entrainement` § U18, `-club` § Infrastructures, `-joueurs` ; connaissance § 3, § 4). Règles : pas de test payant, pas de jauge, pas d'investissement hebdomadaire (ne pas transposer BasketVibe) ; retard mesuré contre les autres clubs (CLAUDE.md règle 6).

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:66 | comment l'académie fonctionne | var. 1-3 |
| :67 | lequel des 2 selon stats, besoin, revente | var. 4-6 |

## Rendu (figé)
1. `| Prospect | Rôle | Compétences dévoilées | Compétences clés du rôle | Notre titulaire au rôle | Besoin (rôle sans relève, retraite) | Verdict (signer / ignorer) |`.
2. Youth Academy : `| Niveau actuel | Plage (min–max) | Milieu de tirage | Niveau suivant : coût | Entretien en plus par cycle | Finançable |` et la comparaison aux autres clubs.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Offre en cours | `select day, available, squad_full, rounds_until_next_pick, prospects from silver.sz_u18 order by day desc limit 1` | 2 prospects fixes jusqu'à signature ; nouveau choix toutes les 8 journées ; comparer `rounds_until_next_pick` aux matchs joués (`silver.sz_standings.played`) | fiche académie § 1 ; § Règles de données | |
| 2 | Plage de tirage | `silver.sz_infrastructure_levels` (Youth Academy) | min = niveau, max = 18 + 2 × niveau (vérifié aux 20 niveaux) ; tirage cohérent avec le milieu de plage (hypothèse, 4 observations) | connaissance 3.8, 3.9 | niveau 6 (27/10) |
| 3 | Dévoilement | — | Le dévoilement ne grandit qu'aux niveaux 3, 8, 13, 18 ; acheter le niveau **avant** de signer (tirage à la signature) | connaissance 4.6 ; fiche académie § Règles de données | |
| 4 | Besoin | `gold.sz_role_report` (`no_natural_backup`, `retiring`) | L'académie sert surtout à remplacer les retraités ; effectif ≤ 30 | fiche académie § 3 | |
| 5 | Prospect étranger | — | Utile pour les sélections nationales (plus de matchs, plus de progrès) | Gazelle 2026-10-20 (4.2) | |
| 6 | Revente | carte `vente` | Durée de vie d'un joueur d'académie ≈ 5 à 5,5 mois (avis) | connaissance 4.3 | |
| 7 | Retard sur les autres clubs | connaissance § 3 | Youth Academy 6 contre 9-10 chez Stoik et pierrottingchrist (milieu 24 / 22,5 contre le nôtre) ; l'API ne donne pas les infrastructures des autres : témoignages seulement | connaissance 3.3, 3.5, 3.10 ; fiche académie | |
| 8 | Coût du niveau suivant | `silver.sz_infrastructure_levels` | Coût multi-saisons = achat + supplément d'entretien × 9 cycles × saisons ; payer seulement quand le solde réel le couvre | fiche académie § Règles de données ; C-044, C-052 | 6 → 7 : 6 200 € (C-052) |
| 9 | Avis des amis | connaissance § 3, § 4 | Gazelle : revenus d'abord ; Stoik / Squidward : académie d'abord | connaissance 3.12, 3.13 | |

| 10 | Signature faite ? | `select captured_at, source_url from bronze.raw_pages where game='sixzeroleague' and source_url ilike '%u18/pick%' order by captured_at desc limit 3` | Une capture POST u18/pick status 200 après l'export U18 = signature faite ; silver.sz_u18 garde le snapshot d'avant (available=true périmé) | police 2026-11-04 | Rincón 18:11 UTC |
| 11 | Éthique de travail et perk du signé | payload du POST pick (`attributes.workEthic`, `perk`, `talent`) | Éthique = rendement d'entraînement (skill entraînement) ; perk « student » non documenté | police 2026-11-04 | Rincón 99, student, talent 2 |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
