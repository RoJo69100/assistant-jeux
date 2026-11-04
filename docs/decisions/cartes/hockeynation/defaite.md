# Carte hockeynation — defaite (analyse d'une défaite, PRO d'abord, FRM/U21/U17 si exportées)

Sources lues : commit d1eaf11 (2026-11-02)

Écrite le 2026-11-02 (fiche `match.md`, skills `hockeynation-match-calendrier`, `-adversaires`, `-coachs-entrainement` § match, learnings L-001 à L-016). Règles : CLAUDE.md règle 4 (défaite = analyse détaillée, joueur par joueur, contre toute la saison), règle 7 (résultat = `my_result`), `analyste` lancé d'office sur une défaite en base.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:166 | apprendre de ses erreurs | Checks appris |
| :169 | beaucoup de défaites : prendre une action | var. 11 |

## Rendu (figé)
1. `| Match | Score (nous-eux) | Tirs | xG | Réussite % | Arrêts % | PP | PK | Pertes | PIM |` : la défaite, puis moyennes des défaites et des victoires de la saison (deux lignes).
2. `| Joueur | Poste | TOI | Buts | Tirs | +/- | PIM |` pour les patineurs du match ; gardien : arrêts par période.
3. `| Cause | Chiffre | Comparaison saison | Leçon L-nnn |` (3 à 5 causes).
4. `| Priorité | Catégorie | Correction (fais X) | Ce qui prouvera l'erreur | Match test |` : 3 à 5 corrections, aujourd'hui seulement.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Résultat | `select game_id, season_day, game_type, home, away, home_score, away_score, my_result from silver.hn_games where team_level = 'PRO' and my_result is not null order by scheduled_at desc limit 5` | Toujours `my_result`, jamais le score domicile–extérieur | CLAUDE.md règle 7 ; fiche match | |
| 2 | Stats d'équipe | `select teams, summary from silver.hn_game_detail where game_id = '<id>'` (teams.stats) | Comparer tirs, xG, réussite à la moyenne V et D de la saison | L-001 | S26 D : réussite 7,4 % contre 12,6 % en V |
| 3 | Gardien | `boxscore`, `periods` de `silver.hn_game_detail` | Sous .870 = cause probable (8 des 12 défaites S26) ; P3 d'un END bas | L-002, L-016 | J8 S27 : .839, P3 .714 |
| 4 | Unités spéciales | `summary` (scoring) | PK en défaite 70 % ; buts encaissés en infériorité tous en défaite | L-006, L-011 | |
| 5 | Joueur clé muet | `boxscore` (tirs, buts par joueur) | Variation de réalisation, pas de volume (de Bruin 2/61 en D) : ne pas le sortir sur un seul match | L-007 [H] | |
| 6 | Pertes de palet, tirs | `teams.stats` | Nouveaux écarts S27 : 34 tirs (S26 D 40,6 ; V 45,4), 13 pertes (8,0-8,4) | L-015 | J8 S27 |
| 7 | Discipline | `pim` du boxscore ; `silver.hn_players.dsc` | DSC 3-4 = 99 PIM contre 32 pour DSC 7+ | L-008 | |
| 8 | Tactique adverse et force | `coaches` (ratings) de `silver.hn_game_detail` ; `gold.hn_club_compare` ; skill `hockeynation-adversaires` | Coach rating = score des compétences de match, pas la note affichée | connaissance § Coachs (hnadmin 2026-10-29) ; L-011 | |
| 9 | Nos réglages du match | `silver.hn_lineups` (lineup A, `gameplan`) ; `gold.hn_tactique_controle` | Hors poste, case vide, lineup saisie moins d'1 h avant (−30 %) | carte `composition` var. 1, 2, 11 | |
| 10 | Conseils appliqués | `outputs/hockeynation/learnings.md` § Conseils (C-nnn) | Chaque C-nnn ouvert confronté au résultat ; deux échecs = réécrit | CLAUDE.md § Amélioration continue | |
| 11 | Série de défaites | `my_result` des 5 derniers matchs PRO | Deux défaites d'affilée : `analyste` + `decideur`, jamais « ne rien changer » | CLAUDE.md règle 9 ; usage des agents (4) | |
| 12 | Avis des amis | connaissance § Joueurs (condition, gardiens), § Matchs | Perte de condition pèse plus sur les hautes compétences ; un gardien très coté compte moins (en doute) | d0ghouse 2025-12-03 ; heymelo27 2026-04-20 | |
| 13 | Autres équipes | `silver.hn_games` filtré `team_level` ('FRM','U21','U17') | Une défaite FRM/U21/U17 ne s'analyse que si le match est exporté (lignes automatiques) | `resume.md` § Pièges | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|
| L-001 | Défaite = réalisation et arrêts, pas volume de tirs | 2026-11-02 | confirmé (12 matchs S26) |
| L-002 | Gardien < .870 dans 8 défaites sur 12 | 2026-11-02 | confirmé |
| L-006 | PK faible en défaite et en playoffs | 2026-11-02 | à surveiller |
| L-007 | Joueur clé muet = variance, pas une cause à corriger | 2026-11-02 | à surveiller |
| L-008 | Discipline : effet faible sur les résultats | 2026-11-02 | à surveiller |
| L-011 | Série perdue : PP adverse 60 % et coach PK adverse supérieur | 2026-11-02 | à surveiller |
| L-015 | S27 J8 : même schéma + moins de tirs et plus de pertes | 2026-11-02 | à surveiller (1 match) |
| L-016 | Gardien END 4 recule en P3 | 2026-11-02 | à surveiller |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
