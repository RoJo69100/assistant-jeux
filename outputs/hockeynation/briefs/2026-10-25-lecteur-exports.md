# Lecteur d'exports — Hockey Nation — 2026-10-25 (exports depuis 07:45 UTC, derniers à 09:27)

Contexte : le jeu est passé en **saison 27, phase regular** (season-phase = regular à 09:22 ; next-event raffle-event 2026-10-25 20:00 UTC). Fenêtre agents libres : open, expire 2026-11-28 20:00 UTC. Fenêtre échanges : timestamp 2026-11-28 20:00 (sens à confirmer). Paydays S27 : 35 restants, prochain jour 8.

## 1. Rosters (dernier export de chaque équipe, `silver.hn_player_snapshots` day 2026-10-25)
| Équipe | Joueurs | C | LW | RW | LD | RD | G | Âge moy. | Note moy. |
|---|---|---|---|---|---|---|---|---|---|
| PRO | 20 | 2 | 4 | 4 | 4 | 4 | 2 | 27,0 | 67,6 |
| FRM | 22 | 5 | 4 | 4 | 4 | 3 | 2 | 25,2 | 56,4 |
| U21 | 24 | 3 | 6 | 6 | 3 | 3 | 3 | 19,5 | 44,5 |
| U17 | 21 | 4 | 4 | 4 | 3 | 4 | 2 | 16,0 | 42,9 |
Poste = premier poste de `positions`. PRO : seulement 2 C purs (de Bruin, Papež) ; Blednov et Flink sont RW/C. Les 4 équipes sont couvertes.
Piège silver : `silver.hn_players` garde des joueurs absents du roster du jour (comptes affichés 22/23/26/25 au lieu de 20/22/21/24). Fantômes (as_of 10-23) : PRO Kub, Sutherland ; FRM Vollmer ; U21 Ronkainen ; U17 Bogan, Kruchinin, Zwart, Odermatt, Hekkaharju. Filtrer sur les snapshots du jour.

## 2. Passage en silver
| Catégorie | Pages brutes | Lu par silver ? | Ce qu'on en tire |
|---|---|---|---|
| Rosters 4 équipes | 3 club_roster + 10 club_roster_id (2 sont related/version, 3 HTML) | Oui (snapshots 10-25, 4 équipes) | Effectif complet, talents, contrats |
| Coachs | 402 coach_id (63 coachs x 6-7 appels) + 61 coaching-staff (56 pages de recherche sur 58) | Oui : `hn_club_staff` 16 coachs à nous, `hn_coach_profiles` 63, `hn_free_coaches` 840. Non lu : season-stats (tout à 0), career-stats, jobs, news, last-games, coach-applications | Staff, bonus, marché |
| Finances | 20 office_finances | Oui `hn_finances` S27 ; extension/farm/prospects lus (ligne 120 de 015). Non lu : contract-extension-talks, new-extension-offer | Plafond, expirations |
| Draft | 9 draft-center | Oui `hn_draft_class` (mais sans colonne saison : S26 et S27 mélangés, 100+100) et `hn_draft_picks` (5 tours, `overall_rank` NULL). Non lu : draft (date), position-limits | Classe, picks |
| Scouting | 8 office_scouting | Oui `hn_scouts` (2), `hn_scouting_budget`. Non lu : scouting-assignments, scout-applications, scout-reports (vide) | Scouts, budget |
| Ligue | league_overview 5, league_ratings 2, club_overview 14 | Partiel : standings oui ; team-ratings, scoring-leaders, game-overview seulement dans `hn_api` (JSON) | Classement |
| Annexes | news 7, messages 2, puck 2, raffle 3, forum 2, auth 5 | Non utile (messages = anciens, 2026-09-10) ; puck/raffle brut dans `hn_api` | Rien d'actionnable |

## 3. Valeurs lues dans le brut (non lues par silver)
- **Plafond S27** (hn_finances, lu mais pas dans gold) : cap 57 500 000, salaires projetés 55 870 000, **marge 1 630 000** (dont rachat 670 000 non-roster). `gold.hn_cap_outlook` commence à la saison 28 : il n'a pas de ligne S27.
- **Prolongation Bélanger** (LW, 24 ans, 60, 805 000, fin S27) : offre 3 ans à 1 870 000, humeur happy, statut `waiting_for_gm` (talks) / `waiting_for_agent` (offer).
- **Expirant fin S27** : Blednov (33, 74, 4 370 000), Seppälä (32, 73, 4 400 000), Pålsson (32, 68, 3 280 000), Bélanger.
- **FRM en négociation (12)** : Juras LD 26 ans 67 ; Suomela RD 33/65 ; Jaworski RW 26/63 ; Busch LD-RD 25/61 ; Hateboer RW 25/60 ; Kerr LW 31/59 ; Chromý C 32/57 ; Berg C 25/53 ; Ahmala G 26/53 ; Gmür LW 25/52 ; Vahvanen C-RW 26/52 ; Stampfli RW 25/50.
- **Prospects U21 sans contrat (7, 21 ans)** : Öhgren LW 50, Roponen RW 49, Krejčí G 47, Cooper C 46, Arhosuo RD 44, Drouin LD 43, Daněk LW 40 ; Öhgren, Krejčí, Cooper, Arhosuo, Drouin, Daněk : ELC possible et droits perdus si rien.
- **PRO staff** : head coach Henry Byström (56 ans, note 41, aucun spécial) ; Németh 61 (Third Period, Overtime), Herman 59 (Master Tactician), Baier 59 (Commander, Master Equalizer).
- **Draft S27** : tirage le 2026-12-26 20:00 UTC (limite 19:00), 5 picks (tours 1 à 5), ordre inconnu. Nos 5 U17 dans la classe S27 (100 joueurs) : Duguay LD-RD rang 12 (55), Dunn C 17 (50), Klose RW 26 (48), Adams RD 52 (48), Hardie RW 71 (43) ; chacun scouté 3 fois.
- **Scouting** : 2 scouts sur 8 (McDonald chef 1 500/j, Guindon 1 000/j), budget restant 655 000, S28 : 805 000 ; 2 missions en cours (1 et 2 jours). Candidats : scout-applications ouvertes (canHire true, ex. O'Conner LW 57, Táborský C 55).
- **Coachs libres** : 837 coachs lus en brut (pages 7 et 10 sur 58 absentes), silver en montre 840.

## 4. Classement erroné du script
| page_type | Contient autre chose | Critère |
|---|---|---|
| coach_id | 402 lignes : fiche /coach/uuid (63), season-stats, jobs, news, last-games, career-stats, HTML (63), plus 6 appels world/user/season | `source_url` = `/api/coach/<id>` seulement |
| club_roster_id | `/related` (liste des 4 équipes) et `/world/version` | `body.data.players` présent |
| office_finances | player-info (5), contract-extension-talks, new-extension-offer, notifications, world/version, frm-next-season-overview | `source_url` finit par `/finances` |
| player_id (9 aujourd'hui) | trade-window, FA window, payday, salary-cap-overview (data null), news, stats ; une seule vraie fiche `/api/player/<id>` | `body.data.lastname` et `skills` |
| club_news, club_overview, coaching-staff, office_draft-center, league_* | endpoints annexes (version, notifications, next-event, season-current) | `source_url` ne contient pas le nom |
| auth_login | api world/user/season/version, aucun login | ignorer |

## 5. Reste à exporter
- Marché des échanges (fenêtre ouverte jusqu'au 28/11) : écran Transfers > Trade Center, liste des joueurs. Aucun export de marché dans ce lot.
- Les 2 pages manquantes de la recherche de coachs : Coach Center, tri note décroissante, pages 7 et 10.
- Lignes FRM/U21/U17 : non nécessaires (composition auto, règle du 2026-10-23).
- Matchs S27 : aucun export de match dans ce lot (saison commencée, rien à lire encore).
- Fiche détaillée des nouveaux coachs PRO : lue (Byström, 41). Rien d'autre.
