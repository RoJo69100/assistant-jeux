# Hockey Nation — brief Étude des adversaires du 2026-10-23 (Leszno Bulls, Seoul Pilots, Miami Maidiacs, Jessup Baldos)

Demande : `2026-10-23-adversaires-demande.md`. Lus : skill `hockeynation-adversaires`, `commun.md`, `learnings.md`, `2026-10-23-tactique-v2.md`, skill `hockeynation-coachs-entrainement`. Requêtes (colonnes choisies, LIMIT) : `gold.hn_club_compare`, `gold.hn_depth_chart`, `gold.hn_league_player_fit`, `silver.hn_league_players` (END, DSC, spéciales), `silver.hn_club_staff`, `gold.hn_coach_specials`, `gold.hn_coach_board`, `silver.hn_games`, `silver.hn_game_detail`, `silver.hn_standings`. Légende : sc = score au poste (`score_poste`), E = END, D = DSC, I/C/X = idéal / correct / contre-emploi. Total = 4 C + 4 LW + 4 RW + 3 LD + 3 RD + 2 G (meilleurs de chaque poste, `gold.hn_depth_chart`), à comparer à notre lineup S27 du brief tactique-v2 : **C 301, LW 273, RW 275, LD 212, RD 213, G 140 = 1414**.

## 0. Deux faits qui changent la demande
| Fait | Preuve | Conséquence |
|---|---|---|
| 🟥 URGENT — **Aucun des 4 clubs n'a joué contre nous** | `silver.hn_games` (home_is_mine ou away_is_mine) avec Leszno, Seoul, Miami ou Jessup : 0 ligne ; les 33 matchs PRO de `silver.hn_game_detail` sont contre d'autres clubs (Ottawa, Valcatraz, Ticera...) | Les points 3 (part de matchs du gardien dans nos rencontres) et 4 (résultats contre nous) n'ont **aucune donnée** : ligne « il me manque » ci-dessous. Rien n'est inventé |
| 🟧 IMPORTANT — **Ces 4 clubs sont dans l'autre ligue** | `silver.hn_standings` : Leszno, Seoul, Miami, Jessup sont dans la ligue `0b9ee186…` ; Chomelix, Ottawa, Victoria dans `a40e48a8…` | Pas de rencontre de ligue possible. Leur étude sert à juger le niveau de référence et les cibles d'échange, pas un plan de match direct |
| 🟩 SUIVI — l'écart « +27 » de Leszno sur nous ne se reproduit pas | Total Leszno 1445 contre notre lineup S27 1414 = **+31** ; contre l'effectif actuel (C à 2 postes principaux seulement) l'écart n'est pas comparable | Je garde +31 (méthode ci-dessus). Si +27 vient d'une autre vue, il me manque sa source |

## 1. Tableau de synthèse
| Club | Fiche ligue (30 matchs) | Total au poste | Écart sur nos 1414 | Head coach (match_rating) | Somme staff, HC x2 | Gardien G1 (END) |
|---|---|---|---|---|---|---|
| **Jessup Baldos** | 20 V 10 D, 125-84 (+41) | **1481** | **+67** | Rene Flatley (72) | 162 | Vaněk 73 (E5) |
| **Leszno Bulls** | 26 V 4 D, 123-66 (+57) | **1445** | **+31** | Aleksandr Kravchenko (81) | **169** | Hansen 82 (E7) |
| **Miami Maidiacs** | 20 V 9 D 1 prol., 131-104 (+27) | **1435** | **+21** | Christian Moran (74) | 147 | Jenko 84 (E8) |
| **Seoul Pilots** | 16 V 11 D 3 prol., 107-85 (+22) | **1360** | **−54** (3 LW seulement) | Ilja Mašek (72) | 159 | Davis 89 (E8) |
| Chomelix (nous) | 21 V 9 D, 147-97 (+50) | 1414 (lineup S27) | — | Aalst (68) puis Bondar | 148 (Aalst) / 159 (plan Bondar) | Kovalev 71 (E4) |
Lecture : sur le papier Jessup et Leszno nous dépassent ; Leszno gagne le plus (26-4) avec moins de score que Jessup, donc **c'est le coaching (81, DFP 10) et le gardien qui font la différence, pas le total au poste**. Seoul : total faible parce que `gold.hn_depth_chart` ne lui voit que 3 LW (Hudson, Vodák, Alanen) ; ses 6 RW pourraient en couvrir un, lignes réelles non visibles.

## 2. Leszno Bulls (référence)
| # | Point | Données |
|---|---|---|
| 1 | **Point fort** | C : 309 contre 301 chez nous (**+8**) : Urtāns 80 (32 ans, C, E6, D7), Martens 79 (33, C, E6, D6), Bagatskis 76 (28, C, E7, D5, **sur la trade block**), Runolfsdottir 74 (35, E5, D4). RD : Deursen 81 (idéal, E6, D7, Telepathy) + Magnusson 76 (E7, D7) = 228 contre 213 (**+15**). G1 Hansen 82 contre Kovalev 71 (**+11**). LW 275 (**+2**), RW 286 (+11), LD 219 (+7). **Notre réponse** : notre point d'appui est l'ailier (LW 273) et le RW (275) ; on ne les égale pas au centre (C4 Flink 70 contre Runolfsdottir 74) sans l'échange C-029 (Flink contre Bagatskis) |
| 2 | **Staff** | HC **Kravchenko : OFP 9, DFP 10, BAT 6, PP 5, PK 6 (somme 36, match_rating 81, le plus haut des 4)** ; spéciales actives Overtime Period, Shining Star, Master Patriot. Master Patriot : **0 compatriote** dans son effectif PRO (`silver.hn_league_players.nation_id`) = bonus perdu. Assistants : Kristiansen (OFP 8, BAT 8, **PP 8**, PK 4 ; First/Second Period, Master Tactician), Nowak (PK 8), Šteinbergs (**PK 9**, PP 7). Somme 169 contre Aalst 148 (**−21**) et Bondar plan B 159 (**−10**) ; DFP : 35 contre notre 30 (Aalst) / 36 (Bondar). Contre notre PP (20,7 %) : leur PK coaching = HC 6 x2 + 4 + 8 + 9 = **33**, le plus haut des 4 (Aalst 27, Bondar 31). Contre notre PK (76,3 %) : leur PP = 5 x2 + 8 + 5 + 7 = **30**, au niveau d'Aalst (30). **Effet chiffré exact de PP/PK du coach adverse sur notre unité : non trouvé** |
| 3 | **Gardiens** | Hansen 79 (sc 82, 33 ans, E7 = seuil 7+ atteint, mais END est son talent faible) ; Voigt 43 (sc 46, E4, Goalie Tandem, Patriot). Si Hansen se fatigue, la relève vaut 46 : trou de 36 points. Part de ses matchs dans nos rencontres : **aucune rencontre** (§0) |
| 4 | **Résultats contre nous** | 0 match. Bilan global 26 V 4 D, 123-66, 10-0 sur les 10 derniers |
| 5 | **Discipline** | DSC faible : Smutný (LW, D3), Runolfsdottir (C, D4), Jacobi (C, D4), Gilbert Kohler (LD, D4), Jörg Köhler (LD, D4), Tomášek (RW, D4). Leurs 3 titulaires de pointe sont disciplinés : Urtāns D7, Deursen D7, Magnusson D7 |
| 6 | **Réglage** | **Ne pas inverser L1 et L2** : notre L1 (de Bruin E8, Yokoyama E9, Spinka E7, D1 Eskelinen–Nokelainen) est à END 7+, leurs L2-L3 sont à END 4-5 (Fomenko 4, Schläpfer 4, Crosby 4, Runolfsdottir 5) ; la différence de condition joue pour nous en 2e et 3e périodes [H, seuils Discord talonflame1, 2026-04-04 ; chiffre de la perte de condition non trouvé] |

## 3. Seoul Pilots
| # | Point | Données |
|---|---|---|
| 1 | **Point fort** | G : Davis 86 (sc 89, 26 ans, E8) contre Kovalev 71 (**+18**). RD : Mrkvička 88 (34 ans, **E10**, D6) + Muller 76 + Vorobey 69 = 233 (+20). RW : Borovička 87 (E9) + Michalec 72 + Walsh 71 + Mante 69 = 299 (**+24**). LW : Hudson 84 (E9, D8) + Vodák 74 (D9, Buzzer Beater, Equalizer) + Alanen 72 = 3 titulaires seulement. **Notre réponse** : le centre — leurs C valent 256 (Hunter 71, Cho 69, Smith 60, Dickens 56) contre 301 chez nous (**+45 pour nous**) ; de Bruin 78, Papež 76, Blednov 77 y dominent |
| 2 | **Staff** | HC **Mašek : OFP 8, DFP 4, BAT 8, PP 5, PK 7** (somme 32, match 72) ; spéciales actives Commander (capitaine +1), Shining Star (meilleur joueur : Mrkvička 88), **Bracket Boss (2 joueurs +1 en playoffs de ligue)**. Assistants : Keeling (DFP 8 ; **Eye For Talent inactif**, assistant), Nikiforov (OFP 7, PP 7, PK 7), Maassen (**PP 8**). Somme 159 = Bondar plan B (159), +11 contre Aalst. Leur DFP totale 29 (HC 4) = la plus faible des 4. Contre notre PP : PK coaching 14 + 4 + 7 + 5 = **30**. Contre notre PK : PP coaching 10 + 7 + 7 + 8 = **32** |
| 3 | **Gardiens** | Davis E8 (seuil 7+ OK, aucun talent END faible signalé), Huot 47 (E4, 22 ans). Aucune rencontre : part de matchs non mesurable |
| 4 | **Résultats contre nous** | 0 match. Bilan global 16 V 11 D 3 prol., 107-85 |
| 5 | **Discipline** | Ferguson (RW, D4), Annala (LD, D7 mais E3). Équipe disciplinée : Hudson D8, Vodák D9, Mante D7 ; seul Tony Kub (RW, D7, Mr. Game Five) n'est pas un risque |
| 6 | **Réglage** | **Garder Blednov au C3 et de Bruin au C1 sans toucher** : l'avantage (+45) est au centre ; les mises au jeu seront gagnées par Blednov (56,9 %) et Conte (60,3 %) (brief Match, L-004) [H : FOF de leurs C non relevé] |

## 4. Miami Maidiacs
| # | Point | Données |
|---|---|---|
| 1 | **Point fort** | LD : Forget 86 (34 ans, **E10**, sc 89) + Gavran 72 (**E9**, D3) + Kellman 72 = 233 (**+21**). RD Bae 81 (sc 84, E8). G Jenko 81 (sc 84, E8, Patriot, Rivalry) contre Kovalev 71 (+13). LW : Pirttijärvi 77 (idéal, Penalty Killer, On Fire), Beleshev 76, Towne 73, Krejčíř 71 = 297 (**+24**). **Notre réponse** : leur RD2-RD3 vaut 63 + 63 (Vysloužil, Wegmann) contre Nokelainen 71 + Marquardt 71 chez nous : attaquer la 3e paire (D3) avec notre L3 (Conte-Blednov-Jaworski) |
| 2 | **Staff** | HC **Moran : OFP 10, DFP 8, BAT 4, PP 4, PK 6** (somme 32, match 74) ; spéciales actives Shining Star (Forget 89), Meditation (20 % de regagner 1 % de condition aux entractes). Assistants : Lukáč (OFP 8, **PK 9**), Schubert (DFP 8, BAT 7, PK 2), Abrahamsson (**BAT 10**, PK 1). Somme 147, la plus basse des 4 (−1 contre Aalst, −12 contre Bondar). **PK coaching 12 + 9 + 2 + 1 = 24 : le plus faible des 4 (notre Bondar 31, Aalst 27) ; PP coaching 8 + 4 + 6 + 7 = 25** |
| 3 | **Gardiens** | Jenko (sc 84, E8, âge 26) ; Fay 43 (E4, Brick Wall). Cible d'échange déjà dans C-029/brief tactique §7 (Jenko G1 contre Lauper). Aucune rencontre |
| 4 | **Résultats contre nous** | 0 match. Bilan global 20 V 9 D 1 prol., 131-104 (la plus mauvaise défense des 4 : 104 buts contre) |
| 5 | **Discipline** | **Le plus mal discipliné** : Mayor (RW, D2), Gavran (LD, D3), Ellefsen (RW **1er de la ligne**, sc 79, D4), Sušnik (RW, D4), An (RW, D4), Kellman (LD, D4). Seul Ford (C, D9) est très discipliné ; Forget (LD, 86) D5 |
| 6 | **Réglage** | **PP : garder PP1 (de Bruin, Bélanger, Lubowitz, Kabát, Hateboer) et envoyer Bélanger + Lubowitz en EXT en fin de match** : leur PK coaching est le plus faible (24) et leurs titulaires pénalisés sont Ellefsen D4 et Gavran D3 ; plus de supériorités attendues [H] |

## 5. Jessup Baldos
| # | Point | Données |
|---|---|---|
| 1 | **Point fort** | Le plus fort sur le papier : **1481 (+67)**. LW Filatov 82 (sc 85, E8) + Kellermann 76 (**E9**) ; RW Kalina 83 (sc 86, E9) ; **RD Mráz 84 (sc 90, E9, D9) + Beaudry 78 (sc 84, Penalty Killer, Telepathy) = 240 contre 213 (+27)** ; C 307 (Feeney 79 E4 D7, Samuelsson 79 E7, Kariya 78 E9 D10 Agitator + Powerplay Specialist, Charvát 71). G faible : Vaněk 70 (37 ans, **E5, sous le seuil 7+**) + Conn 65 ; 138 contre notre 140. **Notre réponse** : leur G1 vieux à END 5 est le seul trou : volume de tirs et L1 à END 7+ |
| 2 | **Staff** | HC **Flatley : OFP 8, DFP 5, BAT 8, PP 6, PK 6** (somme 33, match 72) ; **First Period, Second Period et Third Period actifs** (3 joueurs au hasard +1 par période, soit 9 bonus par match). Assistants : Fontana (DFP 8, Master Equalizer), Bieri (**PP 8**, OFP 7, DFP 7 ; Bulldozer), Toikkanen (PK 7, BAT 7 ; Master Agitator). Somme 162 (+14 contre Aalst, +3 contre Bondar). PK coaching 12 + 6 + 6 + 7 = **31** ; PP coaching 12 + 7 + 8 + 7 = **34, le plus haut des 4**. Contre notre PK (76,3 %) c'est le PP à craindre |
| 3 | **Gardiens** | Vaněk 70 (E5), Conn 65 (E6, Goalie Telepathy). Seul club dont le G1 est sous le seuil 7+ : fatigue probable en saison régulière [G:Lineups, skill match-calendrier : 4 départs d'affilée pour END 4]. Part de ses matchs dans nos rencontres : aucune rencontre |
| 4 | **Résultats contre nous** | 0 match. Bilan global 20 V 10 D, 125-84 (la 2e défense des 4) |
| 5 | **Discipline** | Zhukov (LD, D4), Samuelsson (C, D4), Larivière (RW, D4), John Robinson (LW, D4), Casey (RD, D4). Kariya D10, Mráz D9 : pointe disciplinée |
| 6 | **Réglage** | **PK1 inchangé (Spinka, Blednov, Burns, Marquardt) : ne jamais remplacer Burns ni Marquardt par Nokelainen au PK1** ; contre le PP coaching le plus haut (34), garder les DEF 8-9 sur la 1re unité et Nokelainen (SKA 8, E9) au PK2 [H] |

## 6. Cibles d'échange qui ressortent (déjà au brief tactique §7 et C-029, disponibilité non confirmée)
| Joueur | Club | Score | END | Intérêt pour nous |
|---|---|---|---|---|
| Sallijs Bagatskis | Leszno | C 76 | 7 | C4 : +6 contre Flink |
| Marcus Schoen | Leszno | RW 76 | **10** | L2 RW : END 4 → 10 (Lubowitz) |
| Sandro Gavran | Miami | LD 72 | **9** | D1 LD : END 7 → 9 ; D3 pour lui |
| Bogomir Jenko | Miami | G 84 | 8 | G1 : +13 ; END 4 → 8 |
| Ernest Mráz | Jessup | RD 90 (idéal) | 9 | Plus grosse cible du lot ; coût et disponibilité inconnus |
| Andreas Kellermann | Jessup | LW 76 | 9 | LW4 : +13 contre Bélanger |
Règle : un joueur qui entre dans notre lineup se juge sur ses talents d'abord (verdict ci-dessus) ; aucun joueur adverse n'est placé dans nos lignes.

## 7. Fin du brief
### (a) Ce qui manque (à réunir ensemble)
| Donnée | Comment |
|---|---|
| Matchs des 4 clubs (gardien titulaire, tirs, PP/PK) | ouvrir la page Schedule + 3 derniers matchs (game) de chaque club et lancer l'export (jamais de robot) ; pour la part de matchs jouée par le gardien : au moins 10 matchs par club |
| Résultats contre nous | impossible tant qu'on n'est pas dans la même ligue ; seule possibilité : playoffs inter-ligues, calendrier à lire sur la page Schedule |
| Lignes réelles (A/B/C) des adversaires | non visibles dans le jeu ; `gold.hn_depth_chart` donne les lignes probables |
| Source du « +27 » de Leszno | dire d'où vient ce chiffre (vue ou calcul) |
| Taux PP/PK de la ligue (Team Ratings) | ouvrir la page Team Ratings et lancer l'export |
| Nationalité du coach de chaque club vs Master Patriot / Patriot | `nation_id` de Mašek et Flatley lu : 4 compatriotes chacun (Seoul, Jessup) ; effet exact de Patriot non lu |

### (b) Règles non trouvées
| Règle | État |
|---|---|
| Effet chiffré de PP et PK du coach adverse sur notre supériorité ou infériorité | non trouvé (le guide dit seulement « supériorité » et « infériorité », ligne 14 du skill coachs) |
| Perte de condition par présence selon l'END | non trouvée |
| Cumul des bonus de période (First/Second/Third) avec plusieurs coachs | non trouvé |
| Départage de Tactician / Master Tactician entre deux head coachs | non trouvé |

### (c) Enseignements ajoutés au journal : C-030, C-031, C-032 (voir `learnings.md`)
