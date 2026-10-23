# Hockey Nation — brief Entraînement du 2026-10-23 (PRO et FRM)

Briefs amont lus : `2026-10-23-match.md`, `-effectif.md`, `-finances-personnel.md`, `-academie.md`. Registre `fait-2026-10-23.md` lu (rien sur l'entraînement). Skills : `hockeynation-coachs-entrainement` [G:Coaches, G:Training], `hockeynation-joueurs` [G:Players, G:Lineups]. Vues du 2026-10-23 : `silver.hn_training_log`, `silver.hn_players`, `silver.hn_player_snapshots` (drapeau `max` par compétence), `gold.hn_player_fit`, `gold.hn_position_keys`, `silver.hn_coach_profiles`, `silver.hn_coaches`, `silver.hn_free_coaches`, `gold.hn_player_progress` (0 ligne).
Clés par poste (`gold.hn_position_keys`, hypothèse [H]) : C = SHO PAS SKA FOF ; LW/RW = SHO PAS SKA ; LD/RD = DEF CHK SKA ; G = REF POS PAD BLO GLO. `*` = plafond atteint.

## Corrections et confirmations des briefs amont (en tête)
| Brief | Affirmation | Verdict Entraînement | Preuve |
|---|---|---|---|
| Match §6, Effectif §3 | Conte, Blednov, Flink, Sutherland, Eskelinen : « contre-emploi à régler » | **L'entraînement ne règle rien pour eux** : les 5 sont au plafond sur toutes leurs compétences (9/9 ou 8/8 `max`), clés de leur futur poste comprises. Leur niveau est définitif (hors déclin). Seuls le poste (Swap Blednov) ou un échange changent leur verdict | `silver.hn_player_snapshots` |
| Finances §5 | Head coach PRO : Lisowsky à la place d'Aalst | **Confirmé côté entraînement, avec un gain** : Lisowsky entraîne SKA 6, PAS 8, PAD 9 ; nos 4 assistants/head n'ont SKA 4 au mieux (Herman) alors que SKA est la clé la plus ouverte chez nos jeunes. Perte : DEF 7 et PWR 7 d'Aalst (Papež DEF 3 et Carpentier DEF 4 y sont encore) | `silver.hn_free_coaches`, `silver.hn_coaches` |
| Finances §5 | Aalst part dans 1 an (retraite à 65 ans) | Sans effet sur les réglages d'aujourd'hui : refaire ce brief le jour où le poste de head coach change | `gold.hn_coach_board` |
| Finances §2 | Monter Hateboer (FRM) en PRO | **Bon pour son entraînement** : DEF avec Aalst (7) au lieu de Gauvin (5) ; SKA est plafonné chez lui | `silver.hn_coaches` |
| Match §2 | Kovalev : END 4, Lauper END 6 | Kovalev s'entraîne déjà en END (seule compétence encore ouverte) : à garder, c'est ce qui allonge le nombre de matchs avant fatigue [G:Lineups] | `silver.hn_training_log` |
| Effectif §5 | `gold.hn_player_progress` vide | **Confirmé** : 0 ligne, et le journal d'entraînement n'a qu'un jour (2026-10-23). Aucun gain mesuré possible aujourd'hui | requêtes du jour |

## En tête : fiche de saisie (réglage à saisir dans le jeu, PRO et FRM)
Les joueurs absents de ces tables sont **au plafond partout** (section 3) : rien à saisir. Les changements prennent effet à l'entraînement suivant.

### PRO (ordre de choix : du haut vers le bas)
| Ordre | Joueur (âge, note, poste) | Compétence | Coach (niveau) | Avant | Décision |
|---|---|---|---|---|---|
| 1 | Aaron Carpentier (19, 43, RD) | **DEF** (4) | Stan Aalst (7) | DEF, Aalst | 🟩 SUIVI garder : clé RD, coach le plus fort en DEF. Ensuite CHK (Németh 6), puis SKA |
| 2 | Vít Kabát (21, 68, RD) | **SKA** (2) | Harry Herman (4) | PAS 8, Baier | 🟥 URGENT changer : SKA est la seule clé RD encore ouverte (DEF et CHK plafonnées) et son niveau le plus bas (2) |
| 3 | Darryl Bélanger (23, 60, LW) | **SKA** (3) | Harry Herman (4) | END 5, Aalst | 🟥 URGENT changer : SKA = clé LW ouverte et talent faible ; puis CHK |
| 4 | Vladislav Papež (23, 70, C) | **DEF** (3) | Stan Aalst (7) | DEF, Aalst | 🟩 SUIVI garder : ses 4 clés C sont plafonnées, DEF est sa seule compétence ouverte |
| 5 | Perry Spinka (24, 72, RW) | **SHO** (3) | Wolfgang Baier (5) | DSC 3, Németh | 🟥 URGENT changer : SHO = clé RW ouverte (niveau 3) ; DSC n'est pas une clé |
| 6 | Paul Lubowitz (25, 65, RW) | **SKA** (4) | Harry Herman (4) | PWR 5, Aalst | 🟧 IMPORTANT changer : SKA = clé RW ouverte ; coach faible (4), voir doute |
| 7 | Vasiliy Kovalev (27, 71, G) | **END** (4) | Stan Aalst ou Wolfgang Baier (5, égalité) | END, Aalst | 🟩 SUIVI garder : toutes ses clés G sont plafonnées |
| 8 | Terrence Stone (30, 65, LW) | **PAS** (7) | Wolfgang Baier (7) | PAS, Baier | 🟩 SUIVI garder : clé LW, talent fort, meilleur coach. Ensuite SKA |

### FRM (ordre de choix : les plus prometteurs d'abord)
| Ordre | Joueur (âge, note, poste) | Compétence | Coach (niveau) | Avant | Décision |
|---|---|---|---|---|---|
| 1 | Jukka Nokelainen (22, 68, RD) | **DEF** (4) | Anthony Gauvin (5) | DEF, Gauvin | 🟩 SUIVI garder : clé RD, `training_rate` 61 déjà le plus haut du FRM. Ensuite SKA (8, talent fort) |
| 2 | Ricky Hateboer (24, 60, RW) | **DEF** (4) | Anthony Gauvin (5) | DEF, Gauvin | 🟩 SUIVI garder : ses clés RW sont plafonnées ; en PRO ce sera Aalst (7) |
| 3 | Jani Ahtola (22, 56, LW) | **SKA** (9) | Anthony Gauvin ou František Mencl (7) | DEF 5, Gauvin | 🟧 IMPORTANT changer : SKA = clé LW et talent fort, 9 → 10 ; DEF n'est pas une clé LW |
| 4 | Rafael von Arx (22, 55, LD) | **SKA** (3) | Gauvin ou Mencl (7) | SHO 4, Beňo (`training_rate` 14) | 🟧 IMPORTANT changer : DEF et CHK plafonnées, SKA est sa seule clé LD ouverte ; SHO ne sert pas à un D |
| 5 | Heinrich Fink (23, 57, RW) | **SKA** (3) | Gauvin ou Mencl (7) | DSC 5, Gauvin | 🟧 IMPORTANT changer : SKA = clé RW ouverte |
| 6 | Levi Bach (22, 52, C) | **SHO** (6) | Medard Beňo (6) | DEF 3, Gauvin | 🟧 IMPORTANT changer : SHO = clé C ; puis FOF (3, Mencl ou Beňo 4) |
| 7 | John van den Berg (22, 51, RD) | **SKA** (4) | Mencl ou Gauvin (7) | PAS 5, Mencl | 🟩 SUIVI changer : SKA clé RD (coach 7) au lieu de PAS (non clé) ; ensuite DEF (3, Gauvin 5) |
| 8 | Jindřich Matouš (23, 48, G) | **GLO** (4) | Anthony Gauvin (6) | GLO, Gauvin | 🟩 SUIVI garder : GLO clé G avec le meilleur coach (6) ; ensuite POS (3, Blake 4) |
| 9 | Szymon Jaworski (25, 63, RW) | **SHO** (7) | Medard Beňo (6) | SHO, Beňo | 🟩 SUIVI garder : clé RW, talent fort ; 25 ans = effet d'âge maximal |
| 10 | Alois Gmür (24, 52, LW) | **PWR** (4) | Harley Blake (6) | FOF 3, Beňo (4) | 🟩 SUIVI changer : ses clés LW sont plafonnées ; coach 6 (PWR) contre 4 (FOF) |
| 11 | Fyodor Zhitnik (22, 50, LW) | **SKA** (3) | Gauvin ou Mencl (7) | PWR 3, Blake | 🟩 SUIVI changer : SKA = clé LW ouverte ; contre-emploi aux 2 postes, joueur secondaire |
| 12 | Jean-Pierre Stampfli (24, 50, RW) | **DEF** (5) | Anthony Gauvin (5) | FOF 3, Mencl | 🟩 SUIVI changer : ses clés RW sont plafonnées ; DEF est un talent fort et Gauvin (5) bat Mencl/Beňo en FOF (4) |

Capacité (head coach 9 joueurs, assistant 6 [G:Coaches]) : PRO Aalst 3 joueurs, Baier 2, Herman 3 ; FRM Gauvin jusqu'à 9 (DEF x4, GLO, SKA x4 au pire), Mencl jusqu'à 4, Beňo 2, Blake 1 : aucune limite atteinte.

## 1. Pourquoi ces réglages (règles et faits)
- **Règles** : un seul entraînement par jour ; réglable en PRO et FRM seulement [G:Training, G:Teams]. Chaque joueur prend le coach le plus fort dans sa compétence selon l'ordre de choix réglable ; sans coach compétent, aucun bonus [`hockeynation-coachs-entrainement`]. Vitesse = âge (effet maximal dès 25 ans), niveau actuel (9 → 10 plus lent), Work Ethic, niveau du coach (effet fort) [idem]. Seul un niveau entier compte en match [`hockeynation-joueurs`]. Plafond atteint : le joueur passe à une compétence au hasard [idem]. Compétences clés = hypothèse [H] `gold.hn_position_keys`.
- **Faits** : sur 19 entraînements PRO/FRM du journal (`silver.hn_training_log`), le coach choisi est le meilleur disponible dans la compétence à chaque fois (ex. Papež DEF → Aalst 7, Nokelainen DEF → Gauvin 5, van den Berg PAS → Mencl 7) : le jeu applique bien la règle. Seuls 8 joueurs PRO sur 22 et 12 sur 21 au FRM ont encore une compétence ouverte (drapeau `max`, `silver.hn_player_snapshots`) ; **tous les autres entraînent déjà « au hasard »** (aucune ligne au journal).
- **Avis** : la compétence choisie est la clé du poste la plus basse non plafonnée ; à défaut une compétence non clé avec le meilleur coach. Confiance moyenne : la valeur réelle d'une clé en match n'est pas chiffrée dans les skills (non trouvé).
- **Doute** (une demi-ligne) : pour Kabát, Bélanger et Lubowitz le seul coach en SKA est Herman (4), donc la vitesse peut être plus faible que sur leur réglage actuel (ex. Lubowitz PWR avec Aalst 7 : `training_rate` 75, Kabát PAS avec Baier 7 : 53) ; la vitesse en SKA sera lisible dans le journal du prochain export.
- **Égalités de coach** (Gauvin/Mencl en SKA 7, Aalst/Baier en END 5) : la règle de départage n'est pas dans le skill, **non trouvé** ; l'ordre de choix ci-dessus s'applique, les deux conviennent.

## 2. Meilleur coach par compétence (liste nominative, `silver.hn_coaches` du 2026-10-23)
| Compétence | PRO | FRM |
|---|---|---|
| SKA | Harry Herman 4 | Anthony Gauvin 7, František Mencl 7 |
| END | Stan Aalst 5, Wolfgang Baier 5 | Medard Beňo 8 |
| PWR | Stan Aalst 7 | Harley Blake 6 |
| SHO | Wolfgang Baier 5 | Medard Beňo 6 |
| PAS | Wolfgang Baier 7 | František Mencl 7 |
| DEF | Stan Aalst 7 | Anthony Gauvin 5 |
| CHK | Krištof Németh 6 | Harley Blake 7 |
| DSC | Stan Aalst 6, Krištof Németh 6 | Anthony Gauvin 6 |
| FOF | Krištof Németh 4 | František Mencl 4, Medard Beňo 4 |
| REF | Harry Herman 7 | aucun coach |
| POS | aucun coach | Harley Blake 4 |
| PAD | Stan Aalst 6 | Harley Blake 4 |
| BLO | Harry Herman 4 | aucun coach |
| GLO | Krištof Németh 5 | Anthony Gauvin 6 |
| STK | aucun coach | Anthony Gauvin 5 |
Manques de couverture qui comptent : **SKA en PRO (4 seulement)** pour 3 joueurs (Kabát, Bélanger, Lubowitz) + Carpentier ; **POS, STK en PRO et REF, BLO en FRM : aucun coach** (sans bonus). Le recrutement de Lisowsky (SKA 6, PAS 8, PAD 9, CHK 5, POS 5, DSC 4, `silver.hn_free_coaches`) comble SKA, POS et PAD en PRO. Pavel Vašák (entraînement 72 : END 5, PWR 6, SHO 5, DSC 9, REF 6, GLO 8, `silver.hn_coach_profiles`) apporterait DSC et GLO mais aucune clé ouverte de nos joueurs ; Isaac Laurin (PAS 8, DEF 6, CHK 8, POS 7, BLO 5) couvre DEF, CHK, POS, BLO (pas de plafond U17 atteint à vérifier : brief Finances §5).

## 3. Joueurs à ne plus entraîner (tous plafonds atteints ; aucune ligne au journal) 
| Équipe | Joueurs | Remarque |
|---|---|---|
| PRO (14) | de Bruin 30, Conte 24, Burns 27, Kub 28, Lauper 27 (G), Seppälä 31, Pålsson 31, Flink 23, Eskelinen 24, Munk 28, Blednov 32, Yokoyama 22, Marquardt 29, Sutherland 31 | rien à saisir : le jeu leur donne une compétence au hasard sans effet visible. **Blednov : PWR en déclin** (`dec` vrai, 32 ans) ; déclin possible dès 32 ans, les coachs n'y peuvent rien [G:Players, G:Training] |
| FRM (9) | Chromý 31, Kerr 30, Vahvanen 25, Berg 24, Vollmer 25, Busch 24, Juras 25, Suomela 32, Ahmala 25 (G) | idem ; Suomela (32) peut décliner. Vollmer et les autres en négociation : la décision de contrat ne dépend pas de l'entraînement (rien à gagner) |
Avis : le potentiel de progression de l'équipe est concentré sur 8 PRO et 12 FRM. Les gains à venir viennent surtout de la jeunesse (Carpentier, Kabát, Bélanger, Nokelainen, von Arx, Ahtola), pas des titulaires.

## 4. Contre-emplois : clés du poste où ils joueront (niveaux actuels = plafonds, `silver.hn_players`)
| Joueur | Poste à jouer (verdict) | Clés du poste (niveau) | Entraînement |
|---|---|---|---|
| Slava Blednov (32, 74) | **C** (correct) | SHO 7, PAS 6, SKA 7, FOF 10 | aucun : tout plafonné ; PWR en déclin |
| Antonio Conte (24, 73) | LW seul poste listé (contre-emploi) | SHO 6, PAS 5, SKA 6 | aucun : tout plafonné. Au C (correct, non jouable) ses clés seraient SHO 6, PAS 5, SKA 6, FOF 10 |
| Mason Flink (23, 70) | C ou RW (contre-emploi aux deux) | au C : SHO 7, PAS 7, SKA 5, FOF 6 ; à l'aile : SHO 7, PAS 7, SKA 5 | aucun : tout plafonné |
| Troy Sutherland (31, 68) | C ou RW (contre-emploi aux deux) | au C : SHO 7, PAS 5, SKA 5, FOF 7 | aucun : tout plafonné ; part (Finances) |
| Patrik Eskelinen (24, 67) | LD (contre-emploi) | DEF 7, CHK 5, SKA 5 | aucun : tout plafonné |
Conclusion : pour ces cinq joueurs, le seul levier est le poste ou l'échange. Les remplaçants à entraîner sont ceux des sections ci-dessus (Spinka SHO, Lubowitz SKA, Kabát SKA).

## 5. Priorité (joueurs qui progressent encore, clé du poste d'abord)
| Priorité | Action | Pourquoi |
|---|---|---|
| 🟥 URGENT | Saisir SKA pour Kabát et Bélanger, SHO pour Spinka | clés de poste les plus basses (2, 3, 3) chez des joueurs de 21 à 24 ans ; chaque jour sur une compétence non clé est perdu |
| 🟧 IMPORTANT | Saisir SKA pour Lubowitz (PRO), Ahtola, von Arx, Fink (FRM) et SHO pour Bach | clés ouvertes mal ou non travaillées aujourd'hui |
| 🟧 IMPORTANT | Refaire l'export de la page Entraînement chaque jour pendant 7 jours | il me manque l'évolution des niveaux et la vitesse : le journal n'a qu'un jour, `gold.hn_player_progress` est vide. On la réunit ensemble comme ça : export Tampermonkey de la page Entraînement + de l'effectif ; vérifier `select count(distinct day) from silver.hn_training_log` ≥ 7 |
| 🟩 SUIVI | Garder Carpentier, Papež, Kovalev, Stone, Nokelainen, Hateboer, Matouš, Jaworski tels quels | choix déjà cohérents, ne rien changer pour rien |
| 🟩 SUIVI | Revoir tous les réglages le jour où le head coach PRO change (Lisowsky) | les coachs en DEF/PWR (Aalst) et SKA (Lisowsky) changent |

## 6. Réserves
- Aucune mesure de gain (gain mesuré contre attendu) : un seul jour de journal ; les confiances sont moyennes.
- L'effet d'une compétence clé sur le match, la formule de vitesse et la règle de départage entre coachs de même niveau : **non trouvés** dans les skills.
- Les plafonds individuels (valeur du plafond, pas seulement atteint ou non) ne sont pas dans les vues : il me manque le niveau max de chaque compétence ouverte ; on le réunit ensemble comme ça : ouvrir la fiche d'un joueur (partie Skills, `max`) lors de l'export de l'effectif. Sans lui, « 9 → 10 plus lent » n'est appliqué qu'au niveau actuel.
- Les U21 et U17 s'entraînent au hasard, sans réglage [G:Teams] : exclus de ce brief.
