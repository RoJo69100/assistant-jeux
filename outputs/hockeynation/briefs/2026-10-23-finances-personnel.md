# Hockey Nation — brief Finances-personnel du 2026-10-23

Briefs amont lus : `2026-10-23-match.md`, `2026-10-23-effectif.md`. Registre `fait-2026-10-23.md` lu (Kabát gardé, Pålsson à échanger en fenêtre I de S27). Skills : `hockeynation-contrats-finances` [G:Finances, U21 Team, Farm Team], `hockeynation-coachs-entrainement` [G:Coaches], `hockeynation-draft-scouting` [G:Scouting]. Vues lues le 2026-10-23.
Règles de l'utilisateur [U] : seuls les contrats PRO comptent pour le plafond ; un joueur FRM en négociation part si le GM ne fait rien.

## En tête : actions
| Priorité | Action | Chiffre / pourquoi |
|---|---|---|
| 🟥 URGENT | **Laisser partir Troy Sutherland** (RW 68, 31 ans, contrat 3,18 M$ jusqu'à S26) : ne pas accepter 3,26 M$ x 3 ans | cap space S27 = 1,63 M$ : son contrat le mettrait à −1,63 M$ (interdit : −30 % en match, `gold.hn_cap_outlook`) ; 31 ans, déclin dès 32 [G:Players] ; contre-emploi aux 2 postes (Effectif) |
| 🟥 URGENT | **Laisser partir Gordon Kub** (LW 65, 28 ans, 2,38 M$ jusqu'à S26) : refuser 2,75 M$ x 7 ans | −1,12 M$ de cap space S27 sans la vente de Pålsson ; 7 ans = jusqu'à 35 ans pour un 65 ; Stone (65, 2,07 M$ jusqu'à S28) joue déjà au même niveau |
| 🟥 URGENT | **Vendre Kjell Pålsson en fenêtre I (jours 1-35)** : confirmé | cap space S27 1,63 → **4,91 M$** (`gold.hn_trade_value`) ; le rachat ferait moins bien (voir §3) |
| 🟧 IMPORTANT | **Coach : viser Troy Lisowsky comme head coach PRO** quand Stan Aalst part (repli : Gennadiy Bondar) | voir §5 ; offre le jour même où le poste est vacant (jours 1-35) |
| 🟧 IMPORTANT | Monter 2 attaquants du FRM pour avoir 12 attaquants PRO : **Hateboer** (RW 60, 24 ans, idéal, ELC) et **Jaworski** (RW 63, 25 ans, négociation) | sans Sutherland ni Kub il reste 10 attaquants PRO sous contrat S27 (§2) |
| 🟧 IMPORTANT | Prolonger Vollmer et les 7 autres FRM en négociation dès que leur agent donne un prix | aucun impact plafond [U] ; sinon ils partent (§1) |
| 🟩 SUIVI | Scouts : passer de 2 à 4 (1 centre en priorité) | budget 655 000 $ en S27, 4 scouts = 210 000 $/saison (§6) |
| 🟩 SUIVI | Réexporter les finances (évolution par année) | une seule ligne en base (§4) |

## 1. Négociations : verdict nommé (`silver.hn_expiring`, jour 2026-10-23)
| Joueur (équipe) | Âge / note / poste | Demande | Verdict | Pourquoi |
|---|---|---|---|---|
| Perry Spinka (PRO) | 24 / 72 / RW | 3 010 000 $ x 6 ans (jusqu'à S32), `finished` | ✅ **déjà prolongé** : confirmé | meilleur RW (72) ; déjà compté dans les 55,2 M$ engagés S27. Preuve : contrat 30007621 (6 ans) dans `silver.hn_finances.roster_contracts` |
| Vít Kabát (PRO) | 21 / 68 / RD | 2 160 000 $ x 5 ans (jusqu'à S31), `finished` | ✅ **déjà prolongé** : confirmé (corrige Effectif §7 qui le disait « jusqu'à S26 ») | RD 68 de 21 ans ; compté dans S27 ; remplaçant de Pålsson |
| Troy Sutherland (PRO) | 31 / 68 / RW | 3 260 000 $ x 3 ans, `waiting_for_agent`, humeur happy | **laisser partir** | cap (−1,63 M$), âge, contre-emploi au C et à l'aile (`gold.hn_player_fit`) ; son contrat actuel (3,18 M$, S26) ne pèse pas sur S27 |
| Gordon Kub (PRO) | 28 / 65 / LW | 2 750 000 $ x 7 ans, `waiting_for_agent`, happy | **laisser partir** | −1,12 M$ de cap space ; 7 ans ; équivalent de Stone |
| Jona Vollmer (FRM) | 25 / 57 / RW | 1 560 000 $ x 5 ans, `waiting_for_gm`, happy | **prolonger** | FRM sans impact plafond [U] ; le FRM n'a que 5 RW (Jaworski, Hateboer, Fink, Vollmer, Stampfli 50) ; coût réel hors plafond d'un contrat FRM salarié : non trouvé (le skill dit « Farm sans salaire », contradiction avec les 1,56 M$ affichés) |
| Tino Juras (FRM) | 25 / 67 / LD | pas encore de demande | **prolonger** | niveau PRO des D de fond (Munk 66, Burns 66) |
| Szymon Jaworski (FRM) | 25 / 63 / RW | pas encore de demande | **prolonger** et monter en PRO | meilleur RW du FRM ; 25 ans = pas d'ELC (ELC jusqu'à 24 ans), négociation |
| Daniel Suomela (FRM) | 32 / 65 / RD | pas encore de demande | **prolonger** | 2e RD du FRM ; indispensable si Nokelainen monte |
| Michel Kerr (FRM) | 30 / 59 / LW | pas encore de demande | **prolonger** | LW titulaire FRM (Kerr 59, Ahtola 56, Gmür 52, Zhitnik 50) |
| Kamil Chromý (FRM) | 31 / 57 / C | pas encore de demande | **prolonger** | 4 C seulement au FRM (Chromý, Berg, Bach, Vahvanen) |
| Osmo Vahvanen (FRM) | 25 / 52 / C | pas encore de demande | **prolonger** | 4e C du FRM |
| Kimmo Ahmala (FRM) | 25 / 53 / G | pas encore de demande | **prolonger** | G1 du FRM ; 2 gardiens nécessaires |
| Riku Ronkainen (U21) | 21 / 47 / LW | pas de contrat | **laisser partir** | 47 sous tous les LW du FRM et de l'U21 ; contre-emploi (Effectif) ; un U21 non signé part à 22 ans [G:Farm Team] |
| Rudolf Koukal (U21) | 21 / 58 / LD | contrat FRM actif en S27, salaire 0 | ✅ **déjà signé** (FRM) | `silver.hn_expiring` : contrat frm=true, signé le 2026-08-27 |
| Alfréd Višňovský (U21) | 21 / 53 / C | contrat FRM actif en S27, salaire 0 | ✅ **déjà signé** (FRM) | idem |

Règles :
- Les 7 FRM sans demande (statut `null`) n'ont pas encore de prix. Il me manque leur demande, on la réunit ensemble comme ça : réexporter la page contract-talks-farm-players au jour 1 de S27 ; le prix apparaît quand l'agent répond. Verdict de principe : tout FRM utile se prolonge, car aucun impact plafond [U] et le FRM compte 21 joueurs sur 30 permis [G:Farm Team].
- Départ si rien n'est fait : confirmé pour les FRM [U, commun.md] ; le skill dit « 25 ans et plus : négociation à conclure avant la fin de saison sinon il part » [G:Farm Team].
- U21 → FRM ou PRO : confirmé [G:Farm Team] (contrat Farm signable à 21 ans, effet à 22) et [G:U21 Team] (ELC 3 ans, 50 % moins cher, vers le PRO). U17 → U21 : **non trouvé** dans `hockeynation-contrats-finances` (l'âge U17 15-17 / U21 18-21 est dans `hockeynation-joueurs`, pas la procédure de montée).
- Durée et prix : durée 1-3 ans à 30 ans et plus, 1-7 ans de 23 à 29 ans [G:Finances]. Le prix demandé pour une durée plus courte : non trouvé. Redemander risque une offre pire.
- Dates : négociations validées vers le jour 4-5 de S27 (déclaré, non vérifié, commun.md).

## 2. Plafond S27 et suivantes (`gold.hn_cap_outlook`, `silver.hn_finances`)
| Saison | Plafond | Engagé (contrats) | Rachats | Cap space |
|---|---|---|---|---|
| S26 (en cours) | 57,2 M$ | 57,2 M$ projeté | — | 0 (`silver.hn_finances`) |
| S27 | 57,5 M$ (fourchette 57,5-57,8, `rising`) | 55,2 M$ (20 contrats, dont Spinka 3,01 et Kabát 2,16) | 0,67 M$ | **1,63 M$** (1,93 M$ si le plafond atteint 57,8) |
| S28 | non annoncé | 42,345 M$ (16) | 0 | ~15,2 M$ si le plafond reste à 57,5 [H] |
| S29 | non annoncé | 21,9 M$ (8) | 0 | ~35,6 M$ [H] |
| S30 | non annoncé | 11,13 M$ (4) | 0 | ~46,4 M$ [H] |
Annonces du plafond : jour 1 (hausse ou baisse), jour 28 (fourchette), jour 57 (officiel) [G:Finances].

Scénarios S27 (calcul à partir de 1,63 M$) :
| Scénario | Cap space S27 | Verdict |
|---|---|---|
| Rien (Sutherland et Kub partent) | 1,63 M$ | légal |
| + Sutherland à 3,26 M$ | −1,63 M$ | interdit |
| + Kub à 2,75 M$ | −1,12 M$ | interdit |
| Pålsson vendu, personne d'autre | **4,91 M$** | légal |
| Pålsson vendu + Sutherland | 1,65 M$ | légal, mais refusé (âge, 3 ans) |
| Pålsson vendu + Kub + Sutherland | −1,10 M$ | interdit |
Effectif PRO sous contrat S27 sans Sutherland ni Kub : 10 attaquants (de Bruin, Papež, Conte, Yokoyama, Stone, Bélanger, Blednov, Spinka, Flink, Lubowitz), 6 défenseurs après la vente de Pålsson (Seppälä, Eskelinen, Munk, Burns, Marquardt, Kabát + Carpentier 43), 2 gardiens. Il manque donc 2 attaquants pour 4 lignes de 3 [H : 12 attaquants = 4 lignes, 4 lignes vues dans Match §6].
Plan : Hateboer (24 ans, ELC 1 an : « 24 ans → 1 an, avant la fenêtre I seulement » [G:Finances]) + Jaworski (négociation). Salaire d'un ELC FRM → PRO : non trouvé ; les ELC PRO observés (Spinka, Kabát, Bélanger) sont à 805 000 $ [Obs], soit ~0,8 M$ [H]. Cap space attendu après Pålsson vendu et Hateboer : ~4,1 M$ [H], à réserver à un G1 ou un centre (Transferts), en gardant ~1 M$ de réserve.
Corrections au brief Effectif : (1) Kabát et Spinka sont déjà prolongés (§1) ; (2) **ne pas monter Nokelainen (FRM RD 68, 22 ans)** : sans Pålsson il y a déjà 6 défenseurs PRO (2 RD : Marquardt, Kabát) ; à monter seulement sur blessure (ELC 22 ans : 3 ans avant la fenêtre I, 2 ans après [G:Finances]).

## 3. Kjell Pålsson : vente, impact cap space
Faits (`silver.hn_players`, `gold.hn_trade_value`) : RD, 31 ans, note 68, Sweden, 3 280 000 $ jusqu'à S27 (1 an restant), `on_trade_block` = vrai, capitaine PRO (Match §6).
| Option | Cap space S27 | Remarque |
|---|---|---|
| Garder | 1,63 M$ | |
| **Vendre (échange sans salaire en retour)** | **4,91 M$** (+3,28) | choix retenu |
| Rachat | ~3,27 M$ [H] | pénalité = moitié du salaire restant (1,64 M$) [G:Finances] ; moins bon que la vente de 1,64 M$ |
Avis : vendre ; exiger en retour un choix de draft ou un prospect (le chat #trade montre des GM qui cherchent « draft picks or farm/U21 »), pas de salaire. Conséquence hors cap : Pålsson est capitaine et xp 9 ; sa sortie fait perdre le capitaine (Commander agit via le capitaine : Match §3). Nouveau capitaine à nommer : candidats Blednov (xp 10) ou Seppälä (xp 9, 31 ans). Leadership caché : non relevé (Match §6).

## 4. Finances : évolution
`silver.hn_finances` contient **une seule ligne** (2026-10-23, S26 : plafond 57,2 M$, salaire total 57,2 M$). Il me manque l'évolution par année (déclarée par l'utilisateur, non vue en base après 15:17 UTC) : on la réunit ensemble comme ça : relancer l'export Tampermonkey de la page Finances (onglet par année) ; vérifier avec `select count(*) from silver.hn_finances` ≥ 2.
S26 : cap space 0 (salaire projeté = plafond), dont 2 contrats hors effectif (6,08 M$ et 1,34 M$, `nonRoster`, 0 projeté) et le rachat de 670 000 $ sur S27.

## 5. Coachs
### Stan Aalst (head coach PRO, 64 ans)
`gold.hn_coach_board` : `years_to_retire` = 1 ; retraite à 65 ans [G:Coaches]. Note 65, match 68 (OFP 9, DFP 5, BAT 4, PP 7, PK 5, somme 30), xp 10, Netherlands, au club depuis S21. Spéciales : First Period, Master Patriot, Commander.
Il me manque la date exacte de départ : on la réunit ensemble comme ça : réexporter le staff PRO au jour 1 de S27 (poste head coach occupé ou intérimaire). Embauche possible jours 1-35, une offre par poste et par jour, réponse au début du jour suivant ; le coach prend la meilleure offre (PRO > FRM > U21 > U17, head > assistant, tirage à égalité) [G:Coaches].

### Bonus exact de chaque spéciale (`gold.hn_special_skills`)
| Spéciale | Bonus exact | Joueurs PRO qui en profitent |
|---|---|---|
| Commander (Aalst, Vašák) | notre capitaine : +1 à une compétence au hasard, chaque match | 1 : le capitaine (aujourd'hui Pålsson) |
| First Period (Aalst) | trois joueurs au hasard : +1 à une compétence en 1re période | 3 au hasard sur 22, 1re période seulement |
| Master Patriot (Aalst, Netherlands) | +1 au hasard à deux compatriotes du coach en début de match | 2 : Alexander de Bruin (C 72) et Mason Flink (RW 70) (`porteurs_pro_chez_nous` = 2) |
| Eye For Talent (Lisowsky) | notre meilleur joueur de 25 ans ou moins : +1 à une compétence au hasard | 1 par match, parmi 10 éligibles (Conte 73 en tête, puis Spinka 72, Papež 70, Flink 70, Yokoyama 69, Eskelinen 67, Kabát 68, Lubowitz 65, Bélanger 60, Carpentier 43) |
| Shining Star (Lisowsky, Blatter) | notre meilleur joueur : +1 à une compétence au hasard | 1 : Slava Blednov (74) |
| Meditation (Lisowsky, Bondar) | 20 % de chances de regagner 1 % de condition aux entractes | toute l'équipe, effet faible |
| Master Agitator (Vašák) | −1 en Discipline au meilleur patineur adverse, chaque match | aucun joueur à nous : effet côté adversaire |
| Master Tactician (Bondar) | départage les Tacticians quand un Tactician est sur la glace | 0 si aucun Tactician chez nous ; non lu : il me manque les talents Tactician de nos PRO, on les réunit en lisant `special_skills` des joueurs |
| Overtime Period (Bondar) | les Overtime Heroes : +1 à une compétence de plus en prolongation | seulement les gardiens Overtime Hero ; Kovalev et Lauper : `special_skills` non lu |

### Candidats (`gold.hn_coach_board`, `silver.hn_free_coaches`, head coach compté double)
Équipe PRO si le candidat remplace Aalst : 3 assistants actuels Németh (5/8/6/8/4), Herman (5/7/6/4/8), Baier (4/5/9/4/5). Somme pondérée = head x2 + 3 assistants (OFP, DFP, BAT, PP, PK) ; calcul fait ici, pas en SQL.
| Candidat | Âge / retraite | Match OFP-DFP-BAT-PP-PK | Spéciales (3 débloquées) | Somme équipe PRO |
|---|---|---|---|---|
| Stan Aalst (actuel) | 64 / 1 an | 9-5-4-7-5 | First Period, Master Patriot, Commander | OFP 32, DFP 30, BAT 29, PP 30, PK 27 = **148** |
| **Troy Lisowsky** (Canada, xp 10, note 70) | 61 / 4 ans | 7-5-6-9-5 | Eye For Talent, Shining Star, Meditation | 28, 30, 33, 34, 27 = **152** |
| Gennadiy Bondar (Belarus, xp 10, note 68) | 58 / 7 ans | 5-8-7-6-7 | Master Tactician, Meditation, Overtime Period | 24, 36, 35, 28, 31 = **154** |
| Pavel Vašák (Czechia, xp 9, note 70, entraînement 72) | 57 / 8 ans | 7-5-9-4-6 | Commander, Master Agitator, 1 non révélée | 28, 30, 39, 24, 29 = **150** |
| Fernando Blatter (xp 7, note 64) | 56 / 9 ans | 5-7-9-5-5 | Bulldozer, Shining Star, 1 non révélée | 24, 34, 39, 26, 27 = **150** |
Notes d'équipe du match du jour 46 (Match §2) : PK 59 et défense 66 les plus faibles, PP 68, attaque 74.

**Décision : Troy Lisowsky head coach PRO.** Raison : seul candidat dont les deux spéciales actives garanties donnent chaque match un +1 sur nos deux meilleurs profils (Shining Star sur Blednov, Eye For Talent sur Conte) ; PP 9 doublé = 34 sur le PP, ce qui compense la perte d'OFP (28 contre 32) ; somme 152 contre 148 pour Aalst. Doute : Bondar a la meilleure somme (154) et le meilleur PK (31 contre 27), mais ses spéciales ne servent presque à rien chez nous (Master Tactician non confirmé, Overtime Period dépend des gardiens) ; il est le repli si Lisowsky refuse. Lisowsky part à la retraite dans 4 ans : on renouvelle alors.
Perte à accepter : Master Patriot (+1 pour de Bruin et Flink) et First Period (3 joueurs, 1re période) disparaissent avec Aalst ; Commander revient si on recrute Vašák comme assistant (hors effet : les spéciales d'un assistant ne jouent pas en match [G:Coaches]).

### Master Agitator de Pavel Vašák : effet réel
Bonus exact : −1 en Discipline au meilleur patineur adverse, chaque match (`gold.hn_special_skills`). Un seul joueur adverse, un seul point. La synergie notée dans la vue est « plus de pénalités adverses → notre supériorité (PP) », mais le lien Discipline → probabilité de pénalité n'est dans aucun skill : **non trouvé**, effet chiffré inconnu. Observé : au jour 46, Ottawa a pris 5 pénalités contre 1 pour nous, et notre PP a marqué 1/5 : le problème est la conversion du PP, pas le nombre de supériorités. Vašák a PP 4 (son point le plus faible), doublé s'il est head coach : somme PP 24 contre 30 aujourd'hui. Verdict : Vašák n'est pas le head coach.
Option 🟧 : Vašák comme **assistant PRO à la place de Wolfgang Baier** (61 ans, 4-5-9-4-5) : Vašák fait 7-5-9-4-6, soit mieux ou égal sur les 5 compétences (OFP +3, PK +1) pour le même BAT 9. Le renvoi de Baier n'est possible que s'il a passé sa 1re saison au club (protégé sinon) : date d'arrivée de Baier non relevée, il me manque `at_club_since_season` de Baier, on le lit dans `silver.hn_coaches`. Aucun effet de sa spéciale Master Agitator (assistant). Gain : ~+3 OFP ; gain faible, à faire seulement si Baier est sans protection.

### Jeune coach à former [U]
Isaac Laurin (51 ans, retraite dans 14 ans, entraînement 70, `skills_open` = 3) est le meilleur profil jeune du marché (`gold.hn_coach_board`). Mais sa note (63) dépasse déjà le plafond U17 (54) [G:Coaches] : il n'y progresserait plus. Je le mets sur un poste U21 (plafond 69, Very Good) s'il y en a un de libre ; poste U21 libre non relevé. Head coach U17 : non présent dans les vues (Match §3), il me manque le staff U17, on le réunit en exportant le staff U17.

## 6. Scouts (`silver.hn_scouts`, `silver.hn_scouting_budget`)
| Scout | Âge | Poste préféré | Nationalité | Salaire/jour |
|---|---|---|---|---|
| Darren McDonald (head scout) | 61 | RD | États-Unis | 1 500 $ |
| Zachary Guindon | 46 | LW | Canada | 1 000 $ |
Budget : 510 000 $ cette saison, 357 500 $ restant, **655 000 $ en S27** ; 2 scouts sur 8 possibles. Règle : +300 000 $ par saison, reliquat reporté ; salaires jours 4 à 63 (60 jours) ; mission +1 jour si le poste n'est pas son poste préféré, +1 si la nationalité n'est pas la sienne [G:Scouting].
Coût par saison : 2 scouts = 90 000 + 60 000 = 150 000 $. Revenu 300 000 $/saison : tenable jusqu'à 3 assistants + 1 head (270 000 $), soit 4 scouts. À 8 scouts : 510 000 $/saison, le reliquat de 655 000 $ s'épuise en ~3 saisons.
**Décision : recruter 2 assistants** (4 scouts, 210 000 $/saison) : un **centre** (poste manquant en U21 et mince en PRO) et un **ailier gauche** de nationalité différente de Canada (les U17 LW sont 4 sur 4 en contre-emploi : Effectif §1). Nationalités à cibler : non déterminées, il me manque la liste des 10 candidats du jour (indisponible en base), on la réunit ensemble en ouvrant la page d'embauche des scouts au jour 4 de S27. Un head scout RD US + un LW canadien couvrent déjà ces deux postes avec +1 jour de mission hors poste.

## 7. Réserves
- Cap S28+ : plafond non annoncé ; projections [H] à plafond constant.
- Salaire des ELC FRM → PRO, prix des FRM sans demande, effet Discipline : non trouvés (cités plus haut).
- Retraite d'Aalst : date exacte non relevée.
- Les verdicts FRM sans demande sont de principe ; ils se confirment quand le prix s'affiche.
