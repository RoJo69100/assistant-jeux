# Hockey Nation — brief Entraînement du 2026-10-23 (réécrit : plan A staff actuel, plan B staff S27)

Remplace la version précédente. Lus en entier : `entrainement.md` (agent), `commun.md` (y compris « Précisions du 2026-10-23 (soir) »), fiche `entrainement.md`, `fait-2026-10-23.md`, briefs du jour match (33 matchs), effectif, finances-personnel (nouveau plan S27), academie, tactique, ancien entrainement. Skills : `hockeynation-coachs-entrainement` [G:Coaches, G:Training], `hockeynation-joueurs` [G:Players, G:Teams, G:Lineups]. Vues du 2026-10-23 : `silver.hn_training_log`, `silver.hn_player_snapshots` (plafond `*` par compétence), `silver.hn_league_players` (Mráz, Jenko, Vishnevskiy), `silver.hn_coaches`, `silver.hn_club_staff`, `silver.hn_coach_profiles` (staff U17 ré-exporté), `silver.hn_free_coaches`, `gold.hn_position_keys`.
Clés par poste (`gold.hn_position_keys`, hypothèse [H]) : C = SHO PAS SKA FOF ; LW/RW = SHO PAS SKA ; LD/RD = DEF CHK SKA ; G = REF POS PAD BLO GLO. `*` = plafond atteint (joueur exclu de cette compétence).
Règles citées : un entraînement par jour, réglable en PRO et FRM seulement [G:Training, G:Teams] ; chaque joueur prend le coach le plus fort dans sa compétence, dans l'ordre de choix ; sans coach compétent, aucun bonus ; le niveau du coach pèse fort sur la vitesse ; head coach 9 joueurs, assistant 6 [G:Coaches]. Valeur d'une clé en match, formule de vitesse, départage entre coachs de même niveau : **non trouvés**.

## Corrections et confirmations des autres briefs (en tête)
| Brief | Affirmation | Verdict Entraînement | Preuve |
|---|---|---|---|
| Finances §1 (nouveau plan) | Head Bondar, assistant Lisowsky à la place de Baier | **Confirmé côté entraînement, avec un coût nommé** : Baier est le **seul coach SHO de la PRO** (5). Sans lui, Spinka (SHO 3, clé RW) et Jaworski (SHO 7) n'ont plus de coach SHO ; gains : Bondar END 8 (Kovalev, Papež, Kabát), Lisowsky SKA 6 et PAS 8 (5 joueurs). Je ne contredis pas Finances (PK d'abord), je donne le repli au plan B | `silver.hn_coaches`, `silver.hn_free_coaches` |
| Finances §1 | Aalst disparaît : DEF 7 et PWR 7 perdus | **Confirmé et chiffré** : plus aucun coach DEF en PRO (Bondar, Lisowsky, Németh, Herman, Baier : aucun). Papež, Carpentier, Nokelainen (DEF) et Hateboer perdent leur coach DEF ; Blatter (DEF 5) et Laurin (DEF 6) sont les seuls DEF du marché | `silver.hn_coaches`, `silver.hn_free_coaches` |
| Ancien Entraînement | « Papež : DEF est sa seule compétence ouverte » | **Faux, corrigé** : Papež a aussi END 6 ouverte. En S27 DEF n'a plus de coach, END a Bondar (8) | `silver.hn_player_snapshots` |
| Ancien Entraînement / Effectif §3 | Monter Hateboer : « bon pour son entraînement » (DEF avec Aalst 7) | **Périmé** : Aalst part ; en PRO S27 ses 3 compétences ouvertes (DEF 4, DSC 4, FOF 3) sont toutes hors clés RW ; son meilleur coach = Bondar FOF 7 | `silver.hn_player_snapshots` |
| Ancien Entraînement | Zhitnik : seule clé SKA | **Complété** : PAS 6 est aussi une clé LW/RW ouverte chez lui | `silver.hn_player_snapshots` |
| Effectif §3 | Les 5 contre-emplois (Conte, Blednov, Flink, Sutherland, Eskelinen) | **Confirmé : tous au plafond partout** (9/9 ou 8/8 `*`, Blednov PWR 7 en déclin). Ne pas les entraîner ; seul levier = poste ou échange | `silver.hn_player_snapshots` |
| Finances §3 | Mráz, Jenko arrivent ; Vishnevskiy C | Mráz et Jenko : **tous plafonds atteints**, rien à entraîner. Vishnevskiy : FOF 7 (clé C) et DSC 6 ouvertes, coach FOF = Bondar 7 | `silver.hn_league_players` |
| Finances §3 | Pålsson, Burns, Lauper, Flink, Sutherland, Kub partent | **Aucune perte d'entraînement** : les 6 sont au plafond partout | `silver.hn_player_snapshots` |
| Match (tableau de contrôle) | Spinka en SHO : « sans effet mesurable » | Pas contredit : le but est la clé SHO 3, pas les 18 PIM (DSC 3 reste ouverte, voir plan B) | brief Match |
| Tactique §5 | Kovalev END : un départ de plus par point | **Confirmé** ; en S27 Bondar END 8 contre 5 aujourd'hui | brief Tactique, `silver.hn_free_coaches` |
| Staff U17 ré-exporté | — | Obecny (head), Helgstedt, van den Heuvel, Fehérváry : note 50-52, expérience 3, entraînent au hasard sans bonus ; **aucun lien avec nos réglages** (voir §5) | `silver.hn_coach_profiles` |

## En tête : actions
| Priorité | Action | Pourquoi |
|---|---|---|
| 🟥 URGENT | **Saisir maintenant le plan A (PRO)** : Kabát SKA, Bélanger SKA, Spinka SHO, Lubowitz SKA (Papež, Carpentier, Kovalev, Stone inchangés) | clés de poste ouvertes les plus basses (2, 3, 3, 4) chez des joueurs de 21 à 25 ans ; DEF reste avec Aalst jusqu'à son départ |
| 🟥 URGENT | **Saisir maintenant le plan A (FRM)** : Ahtola, von Arx, Fink, Zhitnik, van den Berg en SKA ; Bach SHO ; Gmür PWR ; Stampfli DEF | 5 joueurs de 22-23 ans travaillent une compétence hors clé |
| 🟧 IMPORTANT | **Garder DEF pour Papež, Carpentier, Nokelainen, Hateboer tant que le coach DEF existe** (Aalst PRO, Gauvin FRM) | après le départ d'Aalst, plus aucun coach DEF en PRO |
| 🟧 IMPORTANT | **S27 jour 1 : appliquer le plan B** après embauche de Bondar et Lisowsky : Papež END, Carpentier SKA, Kovalev END, Stone PAS | coachs 8, 6, 8, 8 contre 7, 7, 5, 7 aujourd'hui |
| 🟧 IMPORTANT | **Si Baier ne peut pas être renvoyé** : Lisowsky à la place de Herman (repli B′) | Herman n'entraîne rien d'utile à nos joueurs (SKA 4 battu par Lisowsky 6) et Baier garde SHO pour Spinka |
| 🟩 SUIVI | Aucun entraînement pour Conte, Blednov, Flink, Eskelinen, Sutherland, Mráz, Jenko | tous au plafond |
| 🟩 SUIVI | Refaire l'export de la page Entraînement chaque jour jusqu'à 7 jours | journal : 1 seul jour (2026-10-23), `gold.hn_player_progress` vide : aucun gain mesuré |

## PLAN A — à saisir maintenant, staff actuel
Staff PRO (`silver.hn_coaches`) : **Stan Aalst** head (64 ans, entraînement 63) END 5, PWR 7, DEF 7, CHK 4, DSC 6, PAD 6 ; **Wolfgang Baier** (61) END 5, PWR 6, SHO 5, PAS 7, DSC 5, PAD 4 ; **Krištof Németh** (63) END 4, PWR 5, CHK 6, DSC 6, FOF 4, GLO 5 ; **Harry Herman** (62) SKA 4, PWR 4, DSC 5, REF 7, GLO 4, BLO 4.
Staff FRM : **Anthony Gauvin** head (57) SKA 7, END 4, DEF 5, DSC 6, GLO 6, STK 5 ; **František Mencl** (39, expérience 0) SKA 7, PWR 2, PAS 7, FOF 4, PAD 2, GLO 1 ; **Harley Blake** (62) PWR 6, DEF 4, CHK 7, DSC 5, POS 4, PAD 4 ; **Medard Beňo** (62) SKA 4, END 8, SHO 6, PAS 5, FOF 4, GLO 5.

### A1. PRO (ordre de choix : du haut vers le bas)
| Ordre | Joueur (âge, note, poste) | Compétence (niveau) | Coach (niveau) | Avant | Décision |
|---|---|---|---|---|---|
| 1 | Aaron Carpentier (19, 43, RD) | **DEF** (4) | Aalst (7) | DEF, Aalst | 🟩 SUIVI garder : clé RD, meilleur coach de la PRO ; ses 3 clés DEF 4, CHK 5, SKA 4 sont toutes ouvertes ; DEF d'abord car Aalst part |
| 2 | Vít Kabát (21, 68, RD) | **SKA** (2) | Herman (4) | PAS 8, Baier | 🟥 URGENT changer : DEF 9 et CHK 7 plafonnées, SKA est sa seule clé RD ouverte et son niveau le plus bas |
| 3 | Darryl Bélanger (23, 60, LW) | **SKA** (3) | Herman (4) | END 5, Aalst | 🟥 URGENT changer : SHO 9 et PAS 7 plafonnées, SKA = seule clé LW ouverte, talent faible ; ensuite CHK 4 (Németh 6) |
| 4 | Vladislav Papež (23, 70, C) | **DEF** (3) | Aalst (7) | DEF, Aalst | 🟩 SUIVI garder : ses 4 clés C sont plafonnées ; DEF 3 coaché par Aalst tant qu'il est là, puis END 6 (plan B) |
| 5 | Perry Spinka (24, 72, RW) | **SHO** (3) | Baier (5) | DSC 3, Németh | 🟥 URGENT changer : SHO = clé RW ouverte au niveau 3 ; DSC 3 reste ouverte pour plus tard |
| 6 | Paul Lubowitz (25, 65, RW) | **SKA** (4) | Herman (4) | PWR 5, Aalst (taux 75) | 🟧 IMPORTANT changer : SHO 9 et PAS 8 plafonnées, SKA = seule clé ouverte ; doute : coach 4 contre Aalst 7 sur PWR, la vitesse en SKA se lira au prochain export |
| 7 | Vasiliy Kovalev (27, 71, G) | **END** (4) | Aalst ou Baier (5, égalité) | END, Aalst | 🟩 SUIVI garder : seule compétence ouverte, toutes ses clés G (REF, POS, PAD, BLO, GLO) plafonnées |
| 8 | Terrence Stone (30, 65, LW) | **PAS** (7) | Baier (7) | PAS, Baier | 🟩 SUIVI garder : clé LW, talent fort, meilleur coach ; SHO 7 plafonnée ; ensuite SKA 5 |

### A2. FRM (ordre de choix : les plus prometteurs d'abord)
| Ordre | Joueur (âge, note, poste) | Compétence (niveau) | Coach (niveau) | Avant | Décision |
|---|---|---|---|---|---|
| 1 | Jukka Nokelainen (22, 68, RD) | **DEF** (4) | Gauvin (5) | DEF, Gauvin | 🟩 SUIVI garder : DEF est sa clé la plus basse (SKA 8 est ouverte aussi, talent fort) et le coach DEF disparaît en PRO ; SKA après sa montée |
| 2 | Jani Ahtola (22, 56, LW) | **SKA** (9) | Gauvin ou Mencl (7) | DEF 5, Gauvin | 🟧 IMPORTANT changer : SKA = clé LW, talent fort, seule clé ouverte ; DEF n'est pas une clé LW |
| 3 | Rafael von Arx (22, 55, LD) | **SKA** (3) | Gauvin ou Mencl (7) | SHO 4, Beňo (taux 14) | 🟧 IMPORTANT changer : DEF 7 et CHK 7 plafonnées, SKA = seule clé LD ouverte |
| 4 | Heinrich Fink (23, 57, RW) | **SKA** (3) | Gauvin ou Mencl (7) | DSC 5, Gauvin | 🟧 IMPORTANT changer : SHO 4 et PAS 7 plafonnées, SKA = seule clé ouverte |
| 5 | Levi Bach (22, 52, C) | **SHO** (6) | Beňo (6) | DEF 3, Gauvin | 🟧 IMPORTANT changer : SHO = clé C ; puis FOF 3 (Mencl ou Beňo 4) |
| 6 | John van den Berg (22, 51, RD) | **SKA** (4) | Gauvin ou Mencl (7) | PAS 5, Mencl | 🟩 SUIVI changer : SKA clé RD au lieu de PAS (hors clé) ; ensuite DEF 3 (Gauvin 5) |
| 7 | Fyodor Zhitnik (22, 50, LW/RW) | **SKA** (3) | Gauvin ou Mencl (7) | PWR 3, Blake | 🟩 SUIVI changer : SKA clé ouverte ; ensuite PAS 6 (Mencl 7) |
| 8 | Jindřich Matouš (23, 48, G) | **GLO** (4) | Gauvin (6) | GLO, Gauvin | 🟩 SUIVI garder : GLO clé G avec le meilleur coach ; puis POS 3 (Blake 4) |
| 9 | Ricky Hateboer (24, 60, RW) | **DEF** (4) | Gauvin (5) | DEF, Gauvin | 🟩 SUIVI garder : SKA 8, PAS 10, SHO 4 plafonnées, aucune clé à travailler |
| 10 | Szymon Jaworski (25, 63, RW) | **SHO** (7) | Beňo (6) | SHO, Beňo | 🟩 SUIVI garder : clé RW, talent fort, seule clé ouverte |
| 11 | Alois Gmür (24, 52, LW) | **PWR** (4) | Blake (6) | FOF 3, Beňo (4) | 🟩 SUIVI changer : SKA, SHO, PAS plafonnées ; coach 6 contre 4 |
| 12 | Jean-Pierre Stampfli (24, 50, RW) | **DEF** (5) | Gauvin (5) | FOF 3, Mencl | 🟩 SUIVI changer : clés plafonnées ; DEF = talent fort, Gauvin 5 contre Mencl/Beňo 4 en FOF |
Capacité : PRO Aalst 3, Baier 2, Herman 3 ; FRM Gauvin jusqu'à 9 (DEF x3, GLO, SKA x5 au pire = 9), Mencl 5, Beňo 2, Blake 1 : aucune limite dépassée.

### A3. Au plafond partout, rien à saisir [G:Training : compétence au hasard]
PRO (14) : de Bruin, Conte, Burns, Kub, Lauper, Seppälä, Pålsson, Flink, Eskelinen, Munk, Blednov (PWR en déclin), Yokoyama, Marquardt, Sutherland. FRM (9) : Chromý, Kerr, Vahvanen, Berg, Vollmer, Busch, Juras, Suomela, Ahmala. **Les 5 contre-emplois (Conte, Blednov, Flink, Sutherland, Eskelinen) sont dans cette liste : ne pas les entraîner.**

## PLAN B — S27, staff Bondar (head) + Lisowsky (assistant à la place de Baier)
Staff PRO S27 (compétences d'entraînement, `silver.hn_free_coaches` et `silver.hn_coaches`) :
| Coach | Rôle | Compétences d'entraînement |
|---|---|---|
| **Gennadiy Bondar** (58) | head (9 joueurs) | END 8, PWR 6, PAS 6, FOF 7, BLO 5, STK 4 |
| **Troy Lisowsky** (61) | assistant (6 joueurs) | SKA 6, PAS 8, CHK 5, DSC 4, POS 5, PAD 9 |
| Krištof Németh | assistant | END 4, PWR 5, CHK 6, DSC 6, FOF 4, GLO 5 |
| Harry Herman | assistant | SKA 4, PWR 4, DSC 5, REF 7, GLO 4, BLO 4 |
| Wolfgang Baier | **renvoyé** | perte : SHO 5 (seul SHO PRO), PAS 7, PWR 6, END 5 |
| Stan Aalst | **retraité** | perte : DEF 7 (seul DEF PRO), PWR 7 (meilleur PWR), PAD 6 |
Sans coach en PRO S27 : **DEF, SHO, STK**. Couverture : SKA Lisowsky 6 ; END Bondar 8 ; PAS Lisowsky 8 ; FOF Bondar 7 ; CHK Németh 6 ; DSC Németh 6 ; PWR Bondar 6 ; REF Herman 7 ; GLO Németh 5 ; POS Lisowsky 5 ; PAD Lisowsky 9 ; BLO Bondar 5.

### B1. PRO S27 : quel coach entraîne quelle compétence de quel joueur
Joueurs PRO S27 retenus par Finances : Pålsson, Burns, Lauper, Flink, Sutherland, Kub partis ; Mráz, Jenko, Vishnevskiy arrivés ; Nokelainen, Hateboer (et Jaworski) montés. Ordre de choix : du haut vers le bas.
| Ordre | Joueur (âge, note, poste) | Compétence (niveau) | Coach (niveau) | Évolution contre aujourd'hui |
|---|---|---|---|---|
| 1 | Carpentier (19, 43, RD) | **SKA** (4) | Lisowsky (6) | DEF avec Aalst 7 devient impossible (aucun coach DEF) ; SKA coaché 6 contre Herman 4 ; ensuite CHK 5 (Németh 6), DEF 4 sans bonus |
| 2 | Kabát (21, 68, RD) | **SKA** (2) | Lisowsky (6) | coach 6 contre 4 aujourd'hui ; PAS 8, PWR 5, END 2, DSC 3 restent ouvertes mais hors clé (END 2 avec Bondar 8 en réserve) |
| 3 | Nokelainen (22, 68, RD), **si monté** | **SKA** (8) | Lisowsky (6) | DEF 4 sans coach en PRO : avis SKA (talent fort, coaché) ; DEF 4 reste bas, confiance moyenne |
| 4 | Bélanger (23, 60, LW) | **SKA** (3) | Lisowsky (6) | coach 6 contre 4 ; ensuite CHK 4 (Németh 6), END 5 (Bondar 8) |
| 5 | Papež (23, 70, C) | **END** (6) | Bondar (8) | DEF 3 sans coach : END coaché 8 (clés C déjà plafonnées) ; DEF 3 en dernier |
| 6 | Spinka (24, 72, RW) | **SHO** (3) | **aucun coach** | perd Baier 5 : SHO sans bonus ; alternative non choisie : DSC 3 avec Németh 6 (hors clé) |
| 7 | Hateboer (24, 60, RW), **si monté** | **FOF** (3) | Bondar (7) | aucune clé ouverte ; FOF 3 est son niveau le plus bas avec le meilleur coach ; puis DSC 4 (Németh 6) |
| 8 | Lubowitz (25, 65, RW) | **SKA** (4) | Lisowsky (6) | coach 6 contre 4 ; PWR 5 avec Bondar 6 en réserve |
| 9 | Jaworski (25, 63, RW), **si monté** | **SHO** (7) | **aucun coach** | perd Beňo 6 (FRM) ; seule clé ouverte |
| 10 | Vishnevskiy (24, 72, C), **si arrivé** | **FOF** (7) | Bondar (7) | FOF clé C ouverte ; puis DSC 6 (Németh 6) |
| 11 | Kovalev (27, 71, G) | **END** (4) | Bondar (8) | coach 8 contre 5 : gain de coach le plus net |
| 12 | Stone (30, 65, LW) | **PAS** (7) | Lisowsky (8) | coach 8 contre Baier 7 ; puis SKA 5 (Lisowsky 6) |
Aucun entraînement : Mráz (tous plafonds), Jenko (tous plafonds), Conte, Blednov, Flink s'il reste, Eskelinen, Seppälä, Yokoyama, Marquardt, Munk, de Bruin.
Charge des coachs S27 : Bondar END x2 (Papež, Kovalev) + FOF x2 (Hateboer, Vishnevskiy) = 4 sur 9 ; Lisowsky SKA x5 (Carpentier, Kabát, Nokelainen, Bélanger, Lubowitz) + PAS x1 (Stone) = 6 sur 6 (**limite atteinte : un 7e joueur en SKA n'aurait pas de coach Lisowsky**, il irait à Herman 4) ; Németh et Herman 0.

### B2. Qui perd son coach (S27)
| Joueur | Compétence | Coach aujourd'hui | Coach S27 | Conséquence |
|---|---|---|---|---|
| **Vladislav Papež** | DEF 3 | Aalst 7 | **aucun** | passer à END 6 (Bondar 8) |
| **Aaron Carpentier** | DEF 4 | Aalst 7 | **aucun** | passer à SKA 4 (Lisowsky 6) |
| Jukka Nokelainen (monté) | DEF 4 | Gauvin 5 | aucun | SKA 8 (Lisowsky 6) |
| Ricky Hateboer (monté) | DEF 4 | Gauvin 5 | aucun | FOF 3 (Bondar 7) |
| **Perry Spinka** | SHO 3 | Baier 5 | **aucun** | reste en SHO sans bonus (ou DSC 3 Németh 6) |
| Szymon Jaworski (monté) | SHO 7 | Beňo 6 | aucun | reste en SHO sans bonus |
| Paul Lubowitz | PWR 5 (actuel) | Aalst 7 | SKA : Lisowsky 6 | gagne (SKA 4 : Herman 4 avant) |
| Stan Aalst (PWR 7) | — | seul PWR fort | Bondar 6 | aucun joueur ouvert en PWR clé |
Gagnent un meilleur coach : Kovalev (END 5 → 8), Stone (PAS 7 → 8), Kabát, Bélanger, Lubowitz, Carpentier, Nokelainen (SKA 4 → 6).

### B3. Repli B′ : si le jeu refuse de renvoyer Baier (protection de la 1re saison, Finances §1)
Lisowsky prend le poste de **Herman** (Finances : somme d'équipe 156 contre 159). Herman n'entraîne rien d'utile à nos joueurs (SKA 4 battu par Lisowsky 6 ; REF 7 : Kovalev, Lauper, Jenko plafonnés en REF ; BLO 4 : plafonnés) mais il porte le PK 8 : coût en match pour Finances, pas pour l'entraînement. Gain d'entraînement de B′ : Baier garde **SHO 5 pour Spinka (3) et Jaworski (7)** et PAS 7. Décision : suivre Finances (Baier remplacé) ; B′ seulement si le renvoi est refusé.

### B4. FRM S27
Staff FRM inchangé (Gauvin, Mencl, Blake, Beňo). Plan A2 reste valable pour Ahtola, von Arx, Fink, Bach, van den Berg, Zhitnik, Matouš, Gmür, Stampfli ; sortent du FRM : Hateboer, Jaworski, Nokelainen (voir B1). Si Nokelainen reste au FRM (cas Mráz acheté, Finances §3) : il continue DEF avec Gauvin 5 puis SKA. Arrivées possibles en S27 (U21 de 21 ans signés Farm, Effectif §4) : **Rudolf Koukal (LD, 58)** DEF 3 et SKA 4 ouvertes (DEF 3 avec Gauvin 5, SKA 4 avec Gauvin ou Mencl 7 : SKA d'abord) ; **Alfréd Višňovský (C, 53)** : FOF 4*, SHO 5*, SKA 7* plafonnés, PAS 4 ouverte (Mencl 7) : PAS. À confirmer à leur arrivée.

## 5. Staff U17 ré-exporté : ce qui change pour l'entraînement
Faits (`silver.hn_coach_profiles`) : Ľubor Obecny (head, 44 ans, note 50, SHO 8*), Maximilian Helgstedt (44, 51, SKA 7*, CHK 7*, PAD 5*), Daan van den Heuvel (45, 52, POS 7*, STK 6), Cyril Fehérváry (44, 51, PWR 8*, BLO 7) ; expérience 3 pour tous ; notes sous le plafond U17 de 54 [G:Coaches] mais expérience au plafond Average (équivalence 3 = Average : [H]).
Verdict : l'U17 s'entraîne au hasard, sans bonus [G:Teams] : ces coachs n'entraînent aucun joueur réglable. Seul usage possible : les former puis les promouvoir (promotion sans retour, vers un poste tenu par un intérimaire, jusqu'au jour 35 [skill coachs-entrainement]). **Helgstedt** (SKA 7, CHK 7) serait le seul à battre Lisowsky en SKA (6) : mais son match est faible (PP 2, DFP 3, note de match 46) ; non retenu. Aucune action.

## 6. Il me manque (à réunir ensemble)
| Donnée | Comment |
|---|---|
| Gains mesurés (niveau avant/après) et vitesse réelle | journal d'entraînement : 1 jour seulement ; export de la page Entraînement + effectif chaque jour, vérifier `select count(distinct day) from silver.hn_training_log` ≥ 7 |
| Vitesse en SKA avec Herman 4 (Kabát, Bélanger, Lubowitz) | lisible dans `training_rate` au prochain export |
| Valeur du plafond (pas seulement atteint ou non) de chaque compétence ouverte | fiche du joueur, partie Skills, lors de l'export effectif |
| Compétences de Koukal et Višňovský en FRM, de Vishnevskiy après contrat | export effectif au jour 1 de S27 |
| Le renvoi de Baier est-il permis | tenter au jour 1 de S27 (Finances §7) |
| Règle de départage entre deux coachs du même niveau (Gauvin/Mencl SKA 7, Aalst/Baier END 5) | non trouvée dans les skills |

## 7. Réserves
- Clés par poste = hypothèse [H] de `gold.hn_position_keys`; l'effet réel d'une clé en match n'est pas chiffré (non trouvé). Les 5 contre-emplois n'ont aucun effet négatif mesuré (brief Effectif).
- Plan B dépend des embauches de Bondar et Lisowsky (réponse au début du jour suivant, meilleure offre du coach [G:Coaches]) et des échanges ; il se refait le jour où le staff est connu.
- Doute sur les saisies A1/A2 : coachs de niveau 4 (Herman) sur SKA ; assumé car aucun autre coach PRO ne couvre SKA avant Lisowsky.
- Conseils ajoutés à `learnings.md` : C-010 (inchangé), C-011 (complété), C-023, C-024.
