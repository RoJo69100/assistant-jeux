# Hockey Nation — brief Entraînement du 2026-10-25 (S27, jour 1)

Lus : agent `entrainement`, `commun.md` + fiche Entraînement, briefs du jour effectif / finances / academie, registre `fait-2026-10-25`, règles apprises, skills coachs-entrainement et joueurs. Vues : `silver.hn_training_log`, `hn_coaches` (jour 2026-10-25), `hn_free_coaches`, `hn_player_snapshots` (10-25, drapeau `max` par compétence), `hn_players`. Codes : [G:...] guide via skills, [Obs] observation, [H] hypothèse. Compétences clés par poste = hypothèse `gold.hn_position_keys` (C : SHO PAS SKA FOF ; ailiers : SHO PAS SKA ; D : DEF CHK SKA ; G : REF POS PAD BLO GLO), non confirmée par le jeu.
Pas de brief Entraînement précédent : première version.

## 0. Faits à lire d'abord
| Point | Constat | Preuve |
|---|---|---|
| Saisie du 10-24 | **Non vérifiable.** Le dernier journal d'entraînement en base est du **2026-10-23 14:47 UTC** (8 PRO, 12 FRM, 20 U21, 21 U17). Aucune page `club_training` plus récente. Je tiens ta saisie du 10-24 pour faite, mais je ne peux pas dire ce qu'elle contient : ce brief compare à la saisie du 10-23. | `silver.hn_training_log` (max day), `bronze.raw_pages` page_type `club_training*` (max 10-23 14:47) |
| Coach disparu | Le coach `49794442…` (Stan Aalst, retraité) supervisait **5 PRO au 10-23** : Carpentier, Bélanger, Lubowitz, Kovalev, Papež. Il n'est plus dans `hn_coaches` : ces 5 sont passés à un autre coach ou à aucun. | `hn_training_log` 10-23 vs `hn_coaches` 10-25 |
| Joueurs entraînables | **PRO : 8** joueurs ont une compétence libre (Kabát, Papež, Spinka, Lubowitz, Stone, Bélanger, Kovalev, Carpentier) = les 8 lignes du journal. Les **12 autres PRO sont plafonnés partout**. **FRM : 14** ont une compétence libre, dont 2 absents du journal : **Višňovský et Koukal** (voir §3). | `hn_player_snapshots` 10-25 (compétences sans `max`) |
| Maxings | **20 joueurs entièrement plafonnés** (pas 18) : PRO de Bruin, Conte, Yokoyama, Flink, Blednov, Seppälä, Eskelinen, Burns, Munk, Marquardt, Pålsson, **Lauper** ; FRM Chromý, Berg, Vahvanen, Juras, Busch, Kerr, Suomela, **Ahmala**. Ne les entraîne pas (pas de gain possible ; le jeu les passe à une compétence au hasard [G:Training]). Lauper et Ahmala sont les 2 de plus que la liste de l'Effectif. | idem |
| Staff qui change l'entraînement | Seuls le **head PRO** (Byström, intérimaire, remplacé par Bondar) et **Baier** (remplacé par Lisowsky au jour 3) bougent. Le FRM (Gauvin, Mencl, Beňo, Blake) ne change pas. | brief Finances §2 |

## 1. Résumé d'une page
Compétences d'entraînement de chaque coach PRO (`hn_coaches`, `hn_free_coaches`) :
| Staff | Compétences d'entraînement (niveau) |
|---|---|
| Actuel (jours 1-3) | Németh END4 PWR5 CHK6 DSC6 FOF4 GLO5 · Herman SKA4 PWR4 DSC5 REF7 GLO4 BLO4 · Baier END5 PWR6 SHO5 PAS7 DSC5 PAD4 · Byström PWR4 PAS4 DEF4 DSC4 FOF2 PAD5 |
| **Plan A** (Bondar head, Lisowsky à la place de Baier) | **Bondar END8 PWR6 PAS6 FOF7 BLO5 STK4** · **Lisowsky SKA6 PAS8 CHK5 DSC4 POS5 PAD9** · Németh (idem) · Herman (idem). Perdus : SHO (Baier 5), DEF (Byström 4), END5, PWR6. **Aucun coach SHO ni DEF** |
| **Plan B** (Bondar refuse : Lisowsky head, Mei assistant) | Lisowsky (idem) · **Mei SKA4 END7 SHO6 PAS5 PAD4 STK5** · Németh · Herman. SHO6 et END7 gardés, PWR et FOF retombent à 5 et 4 |

Verdict sur le staff, du point de vue de l'entraînement (ma part du choix, la décision reste à Finances) : **Plan A est meilleur pour END (8 contre 7 : Kovalev END4) et FOF (7 contre 4 : Hateboer)**, **Plan B est meilleur pour SHO (6 contre rien : Spinka SHO3, Jaworski SHO7)**. Écart faible (2 joueurs de chaque côté) : je ne change pas la recommandation Bondar du brief Finances. Confiance faible.

| Priorité | Catégorie | Action unique |
|---|---|---|
| 🟥 URGENT | Entraînement | **Aujourd'hui, sur l'écran Training PRO : Bélanger SKA, Lubowitz SKA, Stone SKA, Kabát SKA** (coach : Herman SKA4 jusqu'au jour 4, puis Lisowsky SKA6). Les 4 sont sortis de leurs choix du 10-23 (END, PWR, PAS, PAS) qui ne sont pas clés du poste (§2). |
| 🟥 URGENT | Entraînement | **Kovalev (G) : END** avec Baier (END5) maintenant, Bondar (END8) dès son arrivée. Son END est à 4 pour un seuil G1 de 7+ [Discord, talonflame1, 2026-04-04] : c'est la seule compétence qu'il peut encore gagner. |
| 🟥 URGENT | Entraînement | **Spinka : SHO** jusqu'au départ de Baier (jour 3) ; **plan A : DSC avec Németh (6)** ensuite ; **plan B : SHO avec Mei (6)**. SHO3 est sa seule compétence clé libre. |
| 🟧 IMPORTANT | Entraînement | **Papež : DEF** (sa seule compétence libre, 3). Aucun coach DEF après le jour 3 : il s'entraîne sans bonus. Rien d'autre à choisir. |
| 🟧 IMPORTANT | Entraînement | **FRM, 10 changements** par rapport au journal du 10-23 : Koukal SKA, von Arx SKA, Zhitnik SKA, van den Berg SKA, Fink SKA, Ahtola SKA, Gmür PWR, Višňovský PAS, Bach FOF, Hateboer FOF (détail §3). Si ta saisie du 10-24 les contient déjà, rien à faire. |
| 🟧 IMPORTANT | Entraînement | **Ordre de choix des coachs** : PRO et FRM, listes complètes en §4. |
| 🟧 IMPORTANT | Export | **Ré-exporter la page Training (PRO + FRM) après la réponse de Bondar (jour 3, 10-27) et à nouveau après l'arrivée de Lisowsky** : le journal s'arrête au 10-23 et les coachs ont changé. |
| 🟩 SUIVI | Entraînement | **Montées prévues** : Nokelainen → DEF (key, 4) ; Hateboer → FOF (Bondar 7 en plan A) ; Jaworski → SHO. Détail §5. |
| 🟩 SUIVI | Question | Višňovský et Koukal ont des compétences libres mais **ne sont pas dans le journal** du 10-23. Il me manque pourquoi. On le réunit ainsi : ouvre Training FRM, regarde si les deux apparaissent ; exporte la page. Je l'enregistre ensuite dans la fiche. |

Tests (preuve contraire) :
- **SKA via Lisowsky (Kabát, Lubowitz, Stone, Bélanger)** : j'ai tort si, au premier journal après l'arrivée de Lisowsky, `training_rate` de SKA est inférieur à celui de leur ancien choix (Lubowitz PWR : 75 ; Kabát PAS : 53 ; Stone PAS : 18 ; Bélanger END : 28). Un taux plus bas ne prouve pas un gain plus faible (la note monte par le poste, pas par le taux) [H] : le vrai test est le **niveau de SKA au jour 14 (2026-11-07)** : Lubowitz ≥ 5, Kabát ≥ 4, Bélanger ≥ 4, Stone ≥ 6. Sinon retour aux anciens choix.
- **Kovalev END** : j'ai tort si son END est encore 4 au jour 14.
- **Nokelainen DEF sans coach en PRO** : j'ai tort si son taux DEF en PRO tombe sous 40 (FRM avec Gauvin 5 : 61 le 10-23).

## 2. PRO, joueur par joueur (saisie à l'écran Training PRO)
Niveau de compétence du joueur ; `*` = plafonné. Ordre : par poste. « Interim » = jours 1-3 avec le staff actuel.
Les 8 joueurs entraînables :
| Joueur (âge, note) | Compétences libres | Journal 10-23 (compétence, coach, taux) | **Saisie recommandée** | Coach interim | Plan A | Plan B | Pourquoi |
|---|---|---|---|---|---|---|---|
| Vít Kabát RD (22, 68) | SKA2 END2 PWR5 PAS8 DSC3 | PAS8, Baier 7, 53 | **SKA** | Herman 4 | Lisowsky 6 | Lisowsky 6 | SKA est clé D et à 2 (niveau bas = progression rapide) ; PAS8 n'est pas clé D. Ensuite END2 (Bondar 8 en A, Mei 7 en B) quand SKA ≥ 5. Le plus de marge de la défense |
| Vladislav Papež C (24, 70) | DEF3 | DEF3, Aalst 7, 60 | **DEF** | Byström 4 | aucun | aucun | seule compétence libre ; 8/9 plafonnées. Sans coach = pas de bonus |
| Perry Spinka RW (25, 72) | SHO3 DSC3 | DSC3, Németh 6, 48 | **SHO** puis (A) **DSC** | Baier 5 | DSC, Németh 6 | SHO, Mei 6 | SHO3 est clé ailier et sa vraie faiblesse (talent faible PAS, SHO 3) ; DSC n'est pas clé |
| Paul Lubowitz RW (26, 65) | SKA4 PWR5 | PWR5, Aalst 7, 75 | **SKA** | Herman 4 | Lisowsky 6 | Lisowsky 6 | SKA clé ailier à 4 ; PWR n'est pas clé. SHO9* PAS8* déjà plafonnés |
| Terrence Stone LW (31, 65) | SKA5 PAS7 CHK6 DSC3 | PAS7, Baier 7, 18 | **SKA** | Herman 4 | Lisowsky 6 | Lisowsky 6 | PAS7 progresse à 18 (31 ans, niveau haut) ; SKA5 est plus bas et clé. Gain attendu faible à 31 ans [H] |
| Darryl Bélanger LW (24, 60) | SKA3 END5 CHK4 DSC3 | END5, Aalst 5, 28 | **SKA** | Herman 4 | Lisowsky 6 | Lisowsky 6 | SKA3 est son talent faible mais la seule clé libre (SHO9* PAS7*) ; c'est ce qui bride sa note de 60. Test du prolongement (offre 1 870 000) : SKA ≥ 5 au jour 35 |
| Vasiliy Kovalev G (28, 71) | END4 | END4, Aalst 5, 20 | **END** | Baier 5 | Bondar 8 | Mei 7 | seule compétence libre, et seuil G1 7+ |
| Aaron Carpentier RD (20, 43) | tout | DEF4, Aalst 7, 39 | DEF (indifférent) | Byström 4 | — | — | à échanger avant le jour 8 : ne pas y penser |

Lisowsky supervise 6 joueurs au plus (assistant) : 4 en SKA (Kabát, Lubowitz, Stone, Bélanger) ; si Nokelainen SKA s'ajoute, 5 : suffisant. Bondar (head) en supervise 9 : Kovalev et Hateboer.

Les 12 plafonnés : ne rien saisir (de Bruin, Conte, Yokoyama, Flink, Blednov, Seppälä, Eskelinen, Burns, Munk, Marquardt, Pålsson, Lauper). Jamais d'entraînement choisi pour eux.

### Ce que change le nouveau staff (par rapport à la saisie du 10-23)
| Joueur | Effet |
|---|---|
| Kovalev | END : coach 5 (Aalst) → **8 (Bondar)** : +3 niveaux de coach, le plus gros gain du staff |
| Spinka | perd SHO (Baier 5) en plan A ; garde SHO6 en plan B |
| Papež | perd DEF (Byström 4, Aalst) : plus aucun coach |
| Kabát, Lubowitz, Stone, Bélanger | gagnent SKA6 (Lisowsky) contre SKA4 (Herman) |
| Hateboer, Jaworski, Nokelainen (montées) | voir §5 |

## 3. FRM, joueur par joueur (saisie à l'écran Training FRM)
Staff FRM stable : Gauvin (head) SKA7 END4 DEF5 DSC6 GLO6 STK5 · Mencl SKA7 PWR2 PAS7 FOF4 PAD2 GLO1 · Beňo SKA4 END8 SHO6 PAS5 FOF4 GLO5 · Blake PWR6 DEF4 CHK7 DSC5 POS4 PAD4.
Les 14 entraînables (12 du journal + Višňovský, Koukal) :
| Joueur (âge, note, poste) | Libre | Journal 10-23 | **Saisie** | Coach | Raison |
|---|---|---|---|---|---|
| Jukka Nokelainen RD (23, 68) | SKA8 DEF4 DSC5 | DEF4, Gauvin 5, **61** | **garder DEF** | Gauvin 5 | meilleur taux FRM ; clé D, 4 |
| Rudolf Koukal LD (22, 58) | SKA4 END5 SHO5 PAS4 DEF3 DSC4 | absent | **SKA** | Gauvin 7 ou Mencl 7 | clé D à 4, coach 7 ; marge 2/8 plafonnées |
| Alfréd Višňovský C (22, 53) | PAS4 DEF4 CHK3 | absent | **PAS** | Mencl 7 | seule clé libre du C (SKA7* SHO5* FOF4*) ; PAS7 avec Mencl |
| Jani Ahtola LW (23, 56) | SKA9 PWR5 DEF5 CHK6 DSC3 FOF4 | DEF5, Gauvin 5, 39 | **SKA** | Gauvin 7 | seule clé libre (SHO5* PAS5*) et talent fort ; niveau 9 : progression lente, test du taux |
| Rafael von Arx LD/RD (23, 55) | SKA3 PWR3 SHO4 | SHO4, Beňo 6, **14** | **SKA** | Gauvin 7 | taux 14 = le pire du FRM ; SKA3 clé D |
| Levi Bach C (23, 52) | SHO6 FOF3 END6 PWR6 DEF3 CHK3 DSC2 | DEF3, Gauvin 5, 37 | **FOF** | Mencl 4 ou Beňo 4 | clé C à 3 (4e centre) ; 2/9 plafonnées |
| Fyodor Zhitnik LW/RW (23, 50) | SKA3 PWR3 DEF3 DSC3 FOF4 | PWR3, Blake 6, 59 | **SKA** | Gauvin 7 | clé à 3 ; PWR n'est pas clé |
| John van den Berg RD (23, 51) | SKA4 SHO4 DEF3 PAS5 DSC5 | PAS5, Mencl 7, 52 | **SKA** | Gauvin 7 | clé D à 4 ; PAS n'est pas clé D |
| Heinrich Fink RW (24, 57) | SKA3 DEF3 DSC5 FOF5 | DSC5, Gauvin 6, 32 | **SKA** | Gauvin 7 | seule clé libre (PAS7* SHO4*) |
| Jindřich Matouš G (24, 48) | REF6 POS3 PAD4 GLO4 BLO4 STK5 | GLO4, Gauvin 6, 38 | **garder GLO** | Gauvin 6 | meilleur coach G du FRM ; POS3 (Blake 4) serait le second choix |
| Alois Gmür LW (25, 52) | PWR4 FOF3 | FOF3, Mencl 4, 28 | **PWR** | Blake 6 | clés SHO8* PAS5* SKA5* déjà plafonnées ; coach 6 contre 4 |
| Jean-Pierre Stampfli RW (25, 50) | DEF5 FOF3 | FOF3, Mencl 4, 36 | **garder FOF** | Mencl 4 | clés plafonnées, rien de mieux |
| Szymon Jaworski RW (26, 63) | SHO7 DEF4 | SHO7, Beňo 6, 21 | **garder SHO** | Beňo 6 | clé et talent fort ; en PRO : voir §5 |
| Ricky Hateboer RW (25, 60) | DEF4 DSC4 FOF3 | DEF4, Gauvin 5, 48 | **FOF** | Mencl 4 / Beňo 4 | clés plafonnées ; FOF3 est la plus basse. En PRO plan A : Bondar 7 |

Changements FRM vs 10-23 : **10** (Koukal et Višňovský, absents du journal ; Ahtola, von Arx, Bach, Zhitnik, van den Berg, Fink, Gmür, Hateboer). Gardés : Nokelainen, Matouš, Stampfli, Jaworski.
Capacité : Gauvin 9 joueurs, les trois assistants 6 : 14 joueurs au total sans problème. Gauvin et Mencl ont tous deux SKA7 : 7 joueurs demandent SKA (Koukal, Ahtola, von Arx, Zhitnik, van den Berg, Fink + Nokelainen après) : Gauvin en prend 9 au maximum, Mencl 6.
Plafonnés à ne pas saisir : Chromý, Berg, Vahvanen, Juras, Busch, Kerr, Suomela, Ahmala.

## 4. Ordre de choix des coachs (liste à saisir)
Règle : les plus jeunes et les plus prometteurs d'abord (l'âge réduit la vitesse jusqu'à 25 ans [G:Training]) ; le premier de la liste choisit le meilleur coach disponible.
| Rang | PRO | FRM | U21 | U17 |
|---|---|---|---|---|
| 1 | Kabát (22) | Nokelainen (23) | non réglable | non réglable |
| 2 | Nokelainen (23, à la montée) | Koukal (22) | | |
| 3 | Hateboer (25, à la montée) | Višňovský (22) | | |
| 4 | Papež (24) | Ahtola (23) | | |
| 5 | Bélanger (24) | von Arx (23) | | |
| 6 | Spinka (25) | Bach (23) | | |
| 7 | Lubowitz (26) | Zhitnik (23) | | |
| 8 | Jaworski (26, à la montée) | van den Berg (23) | | |
| 9 | Kovalev (28) | Matouš (24) | | |
| 10 | Stone (31) | Fink (24) | | |
| 11 | Carpentier (20, sortant) | Hateboer (25), Gmür (25), Stampfli (25), Jaworski (26) | | |
Les plafonnés se placent après, sans importance. Pour U21 et U17 : voir §6 (je ne peux pas dire si l'écran propose un ordre ; la fiche commune en demande un, le guide dit non réglable). **Il me manque** : si l'écran Training U21/U17 affiche un ordre de choix. On le réunit ainsi : ouvre l'écran Training de l'U21 ; s'il n'y a pas de réglage, je corrige la fiche commune.

## 5. Montées prévues et VIDE
| Joueur | Date (brief Finances/Effectif) | Entraînement à la montée | Coach | Pourquoi |
|---|---|---|---|---|
| Nokelainen RD (23, 68) | ELC avant le 2026-11-28 ; sert à remplacer Pålsson (échange avant le 11-01) | **DEF4**, puis SKA8 | **aucun coach DEF en PRO** (Gauvin 5 est FRM) | il est à 61 de taux avec Gauvin ; **reste en FRM jusqu'à la montée** pour garder Gauvin. Test : taux DEF en PRO ≥ 40 |
| Hateboer RW (25, 60) | négociation à ouvrir (Finances) | **FOF3** | Bondar 7 (plan A), Németh 4 (B) | PAS10* SKA8* SHO4* déjà plafonnés ; FOF est la plus basse |
| Jaworski RW (26, 63) | idem | **SHO7** | Baier 5 puis aucun (A), Mei 6 (B) | SHO7 clé et talent fort ; 7/9 plafonnées ; gain possible limité à 26 ans [H] |
VIDE : aucune compétence-VIDE à combler par l'entraînement. PRO après montées = 20 sans VIDE ; FRM = 1 poste RW VIDE (Effectif). L'entraînement ne remplit pas un VIDE : le prospect FRM qui s'en rapproche le plus est **Višňovský** (C, SKA7* PWR7*), pas un ailier. Prospects Farm à suivre (marge de progression, `skills_maxed` sur total) : Bach 2/9, Koukal 2/8, Ahtola 3/9, van den Berg 3/8, Višňovský 6/9, von Arx 5/8, Nokelainen 5/8, Matouš 1/7, Zhitnik 4/9, Fink 5/9.

## 6. U21 et U17 : ce qui est réglable
- **Pas de choix de compétence ni d'ordre** [G:Training, G:U21 Team] : le journal montre pourtant un coach et un taux pour chaque joueur (U21 18 coachs sur 20 joueurs, taux moyen 38 ; U17 20 sur 21, moyen 35 ; 10-23). Donc **le coach compte dans le taux** même sans réglage.
- Ce que tu peux influencer : (1) **le poste d'assistant U21** : Ahn (intérimaire, END5 SHO4 PAS4 DEF3 FOF4 POS4, somme 18) → **Cozma** (DSC7 PWR5 CHK5 FOF4 END3 REF3, somme 29) : remplace des compétences de niveau 3-5 par DSC7, mais perd END5 et PAS4 ; (2) les **plafonds de coach** : U17 54 / Average, U21 69 / Very Good (un coach au plafond ne progresse plus) ; (3) **qui est dans l'équipe** (les 20 joueurs, brief Effectif).
- Plafonds de joueur U21/U17 : non réglables, déjà dans les snapshots (`max`). Přikryl 0/9, Carbone 0/9 ont toute leur marge.
- Test : taux d'entraînement moyen U21 au jour 14 (avec Cozma) ≥ 38. J'ai tort si ≤ 35.

## 7. Ce que tu as pu oublier
| Point | Donnée | Action |
|---|---|---|
| Âge | Effet maximal dès 25 ans : à 22-24 ans l'effet est plus fort. Les moins de 25 ans entraînables : Kabát 22, Papež 24, Bélanger 24 et les prospects FRM | ils passent en premier dans l'ordre (§4) |
| Déclin dès 32 ans | Blednov (33, 3 compétences en déclin), Seppälä (32, 1), Pålsson (32, 1), Chromý (32, 3). Les coachs n'y peuvent rien [G:Training] | rien à saisir ; c'est un argument pour prolonger 1 an seulement (Finances) |
| Retraite | Dès 35 ans, jour 1 : personne en S27. Plus âgés : Blednov, Suomela 33 | prochaine échéance S29 (Blednov 35) |
| Plafond atteint | Le joueur passe à une compétence **au hasard** : les 20 plafonnés s'entraînent au hasard (c'est neutre) | ne pas leur choisir de compétence |
| Niveau 9 → 10 plus lent | Ahtola SKA9 | test du taux (§3) |
| Work Ethic | Attribut caché qui accélère l'entraînement [G:Training] | non lisible en base : **il me manque** ; on le déduit du taux (Lubowitz 75 contre Stone 18) |
| Coachs spéciaux | Seules les spéciales du **head** jouent en match ; elles n'agissent pas sur l'entraînement. Eye For Talent (Lisowsky head, Gschwend) : meilleur joueur de 25 ans et moins +1 chaque match — **Papež, Kabát, Yokoyama, Flink, Spinka (25), Conte (25), Bélanger** éligibles | argument pour Lisowsky head en S28 (Finances) |
| Retraites de coachs | Németh (64) part à 65, Herman (63) à 65 : plus de coach CHK6/DSC6 (Németh) ni REF7/PK8 (Herman) | plan de relève : Finances annexe C. Pour l'entraînement : DSC (Vašák 9, Vaitkus 9) et CHK (Strachan 9) en S28 |
| Compétences sans coach en PRO (plan A) | **SHO, DEF, POS, STK** (STK : Bondar 4) | pas de joueur PRO concerné sauf Spinka (SHO), Papež (DEF), Nokelainen (DEF), Jaworski (SHO) |
| Coachs de gardien | Aucun gardien PRO n'a de compétence libre à part Kovalev END4 : les coachs de gardien (Herman REF7, Németh GLO5, Lisowsky PAD9) ne servent pas à l'entraînement | ne pas les garder pour ça ; leur valeur est en match (somme) |

## 8. Delta et conseils ajoutés
C-043 à C-046 ajoutés à `outputs/hockeynation/learnings.md`.

---

## ANNEXE A — Compétences libres des 8 PRO et 14 FRM (source : snapshots 10-25, `*` = plafonné)
PRO : Kabát SKA2 END2 PWR5 SHO8* PAS8 DEF9* CHK7* DSC3 · Papež SKA7* END6* PWR7* SHO7* PAS8* DEF3 CHK4* DSC7* FOF8* · Spinka SKA9* END7* PWR8* SHO3 PAS5* DEF5* CHK10* DSC3 FOF5* · Lubowitz SKA4 END4* PWR5 SHO9* PAS8* DEF7* CHK4* DSC4* FOF6* · Stone SKA5 END8* PWR7* SHO7* PAS7 DEF4* CHK6 DSC3 FOF5* · Bélanger SKA3 END5 PWR7* SHO9* PAS7* DEF4* CHK4 DSC3 FOF5* · Kovalev REF5* END4 POS6* PAD6* GLO5* BLO8* STK10* · Carpentier tout libre.
## ANNEXE B — Cas de Plan B détaillé
Si Bondar refuse au jour 3 : head Lisowsky (SKA6 PAS8 CHK5 DSC4 POS5 PAD9, supervise 9), assistant Mei à la place de Baier (SKA4 END7 SHO6 PAS5 PAD4 STK5). Saisie : Kabát SKA (Lisowsky 6) ; Lubowitz SKA, Stone SKA, Bélanger SKA (Lisowsky) ; Spinka SHO (Mei 6) ; Kovalev END (Mei 7) ; Hateboer FOF (Németh 4) ; Jaworski SHO (Mei 6) ; Papež DEF (aucun). Seule différence avec le plan A : Spinka SHO au lieu de DSC, Kovalev END7 au lieu de 8, Hateboer FOF4 au lieu de 7.
## ANNEXE C — Aucune validation par le jeu
Les clés de poste sont une hypothèse (`gold.hn_position_keys`). Le seul moyen de la vérifier : comparer au jour 14 la note PRO des joueurs qui ont gagné une compétence clé (Lubowitz SKA, Kabát SKA) avec celle de ceux qui en ont gagné une non clé (Gmür PWR). Si les notes montent autant, l'hypothèse est fausse et le critère « clé » tombe.
