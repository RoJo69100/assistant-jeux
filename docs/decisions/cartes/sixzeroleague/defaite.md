# Carte sixzeroleague — defaite (analyse d'une défaite ou d'un nul)

Sources lues : commit 8791d35 (2026-11-02)

Écrite le 2026-11-02 (fiche `match.md`, skills `sixzeroleague-match`, `-joueurs`, `-communaute` § 3 et 5 ; connaissance § 2, § 7 ; learnings). Règles : CLAUDE.md règle 4, règle 7 (résultat = `silver.sz_matches.result`, notre point de vue) ; enseignement « confirmé » seulement à 3 matchs de ligue dans le même sens (alpha très aléatoire) ; `analyste` d'office.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:100 | stratégie selon le manque de réussite récent | var. 3, 4 |
| :169 | beaucoup de défaites : agir | var. 11 |

## Rendu (figé)
1. `| Match | Compétition | Lieu | Score | Mi-temps | Tirs | Efficacité % | Arrêts % | Pertes | Interceptions | Exclusions | 7 m pour / contre | Possession |` : le match, puis les moyennes W et L de la saison (`gold.sz_vd_comparatif`).
2. `| Joueur | Rôle | Buts / tirs | Arrêts | Exclusions | Fautes techniques |`.
3. `| Cause | Chiffre | Comparaison saison | L-nnn |` (3 à 5).
4. `| Priorité | Catégorie | Correction (fais X) | Ce qui prouvera l'erreur | Match test |`.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Résultat | `select match_day, competition, round, venue, opponent, opponent_is_bot, goals, opp_goals, result, shots, opp_shots, shot_pct from silver.sz_matches order by played_at desc nulls last limit 5` | Toujours `result` (W/L/D) ; ligue = `competition = 'league'` | CLAUDE.md règle 7 ; fiche match | |
| 2 | Comparaison saison | `select * from gold.sz_vd_comparatif` | Écart W-L : efficacité 56,5 / 49,0 %, arrêts 36,5 / 23,0 % ; pertes identiques | L-022 | |
| 3 | Gardien | `silver.sz_match_players` (arrêts) | Arrêts très variables d'un match à l'autre (23,5 % puis 39,4 %) : aléa d'abord | L-001, L-001a | |
| 4 | Efficacité | tirs et buts | Plus de volume mais moins d'efficacité : ne pas changer pour un seul match | L-003, L-003a, L-009 | |
| 5 | Défense | buts encaissés par match ; `silver.sz_standings` | 24,1 encaissés par match, 10e sur 10 (ligue 22,8) | L-027 | |
| 6 | Discipline | exclusions, `silver.sz_match_incidents` | Exclusions → 7 m adverses dans la seconde ; 1er quart d'heure lié au solde d'exclusions | L-002, L-010, L-012, L-023, L-028 | |
| 7 | Pertes de balle | pertes, fautes techniques par joueur | Fautes techniques = Contrôle du ballon et Passe ; les pertes n'expliquent pas une défaite à elles seules | L-005, L-008, L-014, L-015 | |
| 8 | Joueur par joueur | `silver.sz_match_players where is_mine` | Buteur n° 1 et 7 m (Dupont) ; LW en baisse (Lefebvre) | L-011, L-021, L-033 | |
| 9 | Moment du match | incidents par minute | Défaites perdues en 1re mi-temps (−4,5) ; fins de match 29-44 sur 5 matchs | L-004, L-007, L-032 ; `resume.md` § Pièges | |
| 10 | 2e rencontre | `gold.sz_adversaires.nos_confrontations` | Chaque adversaire revu nous bat de plus (−8,2) | L-025 | |
| 11 | Série | `result` des 5 derniers | Deux défaites d'affilée : `analyste` + `decideur`, jamais « ne rien changer » ; changement de moteur (0.6.1 le 24/10) coupe une série en deux | CLAUDE.md usage des agents (4) ; connaissance « Ce qui change » § 5 | 6 matchs sans victoire J10-J15 |
| 12 | Nos réglages | `teams.tactics` du match ; `silver.sz_tactics` | Mêmes réglages des deux côtés = la tactique ne départage pas | L-024 | |
| 13 | Données absentes | — | Zone des tirs, minutes jouées, pertes par joueur absentes de l'export `/matches/<id>/stats` : à lire en Live | fiche match § Données absentes | |
| 14 | Avis des amis | connaissance § 2 | Résultats « très aléatoires » et « affinités » ; runs adverses « comme au vrai handball » | Gazelle (2.9, 2.10) | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis | Statut (base) |
| --- | --- | --- | --- | --- |
| L-001 / L-001a | Arrêts du gardien = aléa d'abord | 2026-11-02 | confirmé | hypothèse / ✅ validée (3 pour / 0 contre) |
| L-002 | Rafale d'exclusions en 1re mi-temps | 2026-11-02 | confirmé (L-010, L-028) | hypothèse |
| L-003 / L-003a | Volume sans efficacité | 2026-11-02 | à surveiller | hypothèse / hypothèse |
| L-004a / L-007a / L-008a / L-009a | Versions J1-J3 réécrites (voir L-004, L-007, L-008, L-009) | 2026-11-02 | remplacées | ✅ validée (3 pour / 0 contre) / hypothèse / hypothèse / hypothèse |
| L-005 | Pertes = fautes techniques | 2026-11-02 | confirmé | hypothèse |
| L-006a | 7 m (version J1) | 2026-11-02 | remplacée par L-006 | hypothèse |
| L-008 | Pertes en baisse puis rebond | 2026-11-02 | à surveiller | hypothèse |
| L-009 | Efficacité adverse > la nôtre dans les défaites | 2026-11-02 | confirmé (L-022) | ✅ validée (4 pour / 0 contre) |
| L-010 | Discipline J9 : 7 exclusions, 7 jets de 7 m | 2026-11-02 | confirmé | hypothèse |
| L-011 | Dupont buteur n° 1 | 2026-11-02 | confirmé | hypothèse |
| L-012 | 7 m adverses après nos exclusions | 2026-11-02 | confirmé (L-023) | hypothèse |
| L-014 | Pertes en baisse, résultat pire | 2026-11-02 | à surveiller | hypothèse |
| L-015 | Fautes techniques Lefebvre, Roger | 2026-11-02 | à surveiller | hypothèse |
| L-022 | Écart W-L : efficacité et arrêts | 2026-11-02 | confirmé (15 matchs) | ✅ validée (15 pour / 0 contre) |
| L-023 | Holm : 7 des 8 jets de 7 m | 2026-11-02 | à surveiller | hypothèse |
| L-025 | 2e rencontre plus dure | 2026-11-02 | confirmé (6/6) | hypothèse |
| L-027 | Défense 10e sur 10 | 2026-11-02 | confirmé | ⛔ retirée — ne plus appliquer |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
