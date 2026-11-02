# Carte hockeynation — achat (échange entrant, agent libre, signature ELC)

Sources lues : commit 0000000 (2026-11-02)

Écrite le 2026-11-02 (fiche `transferts.md`, `resume.md`, skills `hockeynation-compositions-trades`, `-contrats-finances`, `-joueurs`, `-potentiel-joueurs`, `-match-calendrier` § Échanges ; connaissance § Échanges, § Contrats). Règles : dire « échanger », jamais « acheter » ni « vendre » ; transferts toujours proposés (CLAUDE.md § Règle d'or, exception) ; aucun nouveau joueur dans une lineup avant son arrivée (tableau à part) ; équipe résultante à 20 (CLAUDE.md règle 8).

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:161 | meilleures caractéristiques des joueurs | var. 2, 3 |
| :168 | beaucoup d'argent : que faire | var. 7 |
| :175 | retour des joueurs expérimentés Discord | var. 12 |

## Rendu (figé)
1. Si le dernier export du marché (Trade Center ou agents libres) a plus de 24 h : « 🟥 URGENT · Export · exporte Trade Center / Free agents » (`gold.hn_exports_state`).
2. `| Priorité | Cible | Équipe actuelle | Poste | Âge | Note | Potentiel min–max | Classe | Talents vs poste | END | Contrat (salaire, fin) | Cap space avant → après | Ce qu'on donne | Gain dans la lineup |`.
3. Équipe résultante (PRO, et équipe d'arrivée si autre) à 20 : 4 C / 4 LW / 4 RW / 3 LD / 3 RD / 2 G, VIDE signalé.
4. Une ligne par cible : pourquoi, et ce qui prouvera l'erreur. Rien n'est envoyé sans l'accord de l'utilisateur.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Cibles disponibles | `select source, name, age, rating, main_position, team, fa_salary, fa_years from silver.hn_market_players order by rating desc limit 20` ; joueurs de la ligue : `gold.hn_league_player_fit` | Partenaires = Trade Center ; jamais Leszno, Seoul, Miami, Jessup (comparaison seulement) | [U] `resume.md` § Échanges | |
| 2 | Talents vs poste | `select name, team, position, verdict, talents_cles, faible_cle, score_poste from gold.hn_league_player_fit where not own and name = '<nom>'` | Idéal ou correct au poste visé ; contre-emploi refusé | [U] talents d'abord | |
| 3 | Potentiel | `gold.hn_potential(skills, talents, rating)` sur la cible ; nos joueurs : `gold.hn_player_potential` | Classe Fort / Solide pour un jeune ; plafonds réels (maxings) | skill `hockeynation-potentiel-joueurs` | |
| 4 | Gain dans la lineup | `gold.hn_tactique_effectif_poste` (notre titulaire et notre n°2 au poste) | La cible remplace qui, sur quelle unité (L1-L2, PP, PK), END au seuil | fiche tactique § Rendu figé et objectif | |
| 5 | Cap space | `select name, salary, contract_to, salaire_saison_suivante, cap_space_avant, cap_space_apres from gold.hn_trade_value where name = '<nom>'` ; `silver.hn_cap_now` | Jamais négatif (−30 % en match si négatif plus d'1 h avant) ; allègement à l'approbation | skill contrats-finances ; hnadmin 2026-03-12 | |
| 6 | Saisons suivantes | `select season, committed, buyouts, cap_space from gold.hn_cap_outlook order by season limit 4` | S28 : plancher salarial 50 % (base non publiée) | hnadmin 2026-10-25 (en doute) | |
| 7 | Ce qu'on donne | `gold.hn_trade_value where own` ; `gold.hn_buyout_calc` (`sur_liste_echange`) | Valeur selon la note minimale : 80+ / 70-79 = 1er tour, 60-70 = 2e… (avis) | talonflame1 2026-04-14 (avis, jamais une règle) | |
| 8 | Délai et fenêtre | `gold.hn_today` (`season_day`, `next_event`) | Comité ≈ 24 h + mise à jour : 2-3 jours ; fenêtre I ferme jour 35 (28/11 21:00) ; joueur reçu en fenêtre I non échangeable en fenêtre II | `resume.md` § Saison 27 ; fiche transferts | |
| 9 | Agent libre / ELC | `fa_salary`, `fa_years`, âge | ELC : 24 ans ou moins et « ovr max 69 » (sens contesté : lire l'écran) ; ELC de 24 ans impossible après la fenêtre I ; agent libre signé probablement intransférable la saison (avis) | gordie_79 2026-10-25 (en doute) ; d0ghouse 2026-10-03 | |
| 10 | Prix de marché | connaissance § Contrats (repères Frenzy S27) ; `silver.hn_trades` (échanges conclus) | Baker LD/RD 4 ans 9,05 M ; Borer (min 81) demande 5,5 M × 5 | .coleh / seany148 2026-10-27 | |
| 11 | Demande de la ligue | connaissance § Échanges | U21 en surplus partout ; demande : U21 C/RW/LD, RD de 1er rang, gardiens U21 | #trade 2026-10-24 à 29 | |
| 12 | Avis des amis | connaissance § Échanges, § Contrats ; `connaissance-C-2026-trade-events.md` | — | connaissance | |
| 13 | Offres en cours | `select direction, offering_team, receiving_team, they_give, they_get, salary_change_receiving from silver.hn_trade_offers limit 10` | Ne pas doubler une offre déjà envoyée (registre `fait-`) | `resume.md` § Pièges | |
| 14 | Exclusions [U] | `resume.md` § Noms et consignes | Bélanger (prolongation) et échanges de centres : gérés par l'utilisateur, ne pas les proposer | [U] 2026-10-30 | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|
| L-016 | Priorité de poste : un gardien G1 END 7+ (ni Kovalev 4 ni Lauper 6) | 2026-11-02 | à surveiller |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
