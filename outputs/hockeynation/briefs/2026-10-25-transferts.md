# Hockey Nation — brief Transferts du 2026-10-25 (S27, jour 1)

Lus : agent `transferts`, `commun.md` + fiche `transferts.md`, briefs du jour effectif / finances / academie / tactique / lecteur-exports (entrainement : non lu, hors sujet échanges), registre `fait-2026-10-25`, règles apprises, skills contrats-finances et match-calendrier (§ Échanges). Vues : `silver.hn_league_players` (jour 2026-10-25 = nos 4 équipes ; jour **2026-10-23 = les 4 clubs cibles**), `silver.hn_market_players` (jour 2026-10-23), `silver.hn_trades` (10 échanges du 10-15 au 10-21, 0 à nous), `silver.hn_league_team_ratings` (10-25), `silver.hn_draft_picks`, `gold.hn_cap_outlook`.
Codes : `[G:...]` guide via skills ; `[Obs]` observation ; `[H]` hypothèse ; `[U]` règle de l'utilisateur. Verdict talents = `gold.hn_position_keys` (hypothèse non confirmée par le jeu), recalculé en SQL pour les joueurs adverses (idéal = 2 talents forts clés, correct = 1, contre-emploi = 0).

## 0. Corrections et contradictions (lire d'abord)
| Point | Verdict | Preuve |
|---|---|---|
| Tactique plan A garde **Burns** (LD, D2/D3) | **Burns est sur la liste d'échange du jeu** (`on_trade_block` = true, PRO). Même cas : **Pålsson** (PRO), **Juras** (FRM, LD 67) et **Hongisto** (U21). Burns ne doit partir que si un LD arrive (Gavran) : sinon LD = Seppälä + Munk seulement. Correction de C-021 (10-23 : « Burns contre Mráz/Jenko ») : Burns reste. **Plan de sortie** : retirer Burns de la liste aujourd'hui (geste §6) | `silver.hn_league_players` 10-25 |
| Effectif/Finances : « Hateboer et Jaworski montent » (🟥) | **Devient conditionnel** : si Schoen + Kristensen (ailiers droits) arrivent, ils n'ont plus de place et leurs contrats (≈ 3 120 000 [H]) sont économisés. S'ils n'arrivent pas au 10-29, on les monte (repli, §5) | calcul §3 |
| Tactique : « Munk ne s'échange pas sans LD de remplacement » | **Respecté** : Munk ne part qu'après l'arrivée de Gavran (offre 4 en 2e vague) | Tactique §7 |
| Tactique cible 4 : « Schoen contre Eskelinen + Carpentier » | **Changé** : Eskelinen + Carpentier + Juras servent à Gavran ; Schoen et Kristensen s'obtiennent avec Munk + une pioche | §2 |
| Tactique/Effectif : Mráz « correct » | **Idéal** : SKA et CHK sont ses 2 talents forts, tous deux clés du D | SQL ci-dessus |
| Tactique : Jenko « correct, faible POS clé » | **Idéal** : REF et GLO sont ses 2 talents forts, tous deux clés du G ; la faiblesse POS reste une clé | SQL |
| Ventes ouvertes de l'utilisateur | **Aucun échange à nous dans `hn_trades`** (10 échanges de la ligue, 0 avec Chomelix). Rien n'est vendu : Pålsson, Burns, Juras, Hongisto sont toujours sur la liste, aucune offre reçue ou acceptée en base | `silver.hn_trades` |

## 1. Première ligne
🟥 **URGENT, Export : exporte le marché.** Le marché en base date du **2026-10-23** (plus de 24 h, avant le passage en S27) ; les clubs cibles n'ont pas d'export du 10-25 (8 clubs lus sur les 4 le 10-23) ; la liste des agents libres date aussi du 10-23. Geste exact : Transfers > Trade Center > onglet *Players* (tri note décroissante, toutes les pages) puis onglet *Trade block* ; ensuite Transfers > Free agents (toutes les pages) ; ensuite, sur chaque club cible (Leszno Bulls, Jessup Baldos, Miami Maidiacs, Seoul Pilots), la page *Roster*. Je travaille quand même ci-dessous sur les données du 10-23 : **tout joueur au contrat « fin S26 » (ct = 26) est expiré, non utilisable avant la ré-exportation** ; je n'ai gardé que les contrats allant au moins jusqu'en S27.

## 2. Résumé d'une page : cibles nommées (règle 20)
Cap PRO S27 : plafond 57 500 000, engagé 55 870 000, marge **1 630 000** (`gold.hn_cap_outlook` + `silver.hn_finances`). Somme des notes de la lineup (12 attaquants + 6 défenseurs + G1, [calcul], méthode du brief Tactique) : aujourd'hui (plan B) **1261**, plan A (Hateboer, Jaworski, Nokelainen montés, 3 sortants échangés) **1296**.

| Priorité | Catégorie | Action unique |
|---|---|---|
| 🟥 URGENT | Export | Exporte Trade Center + Free agents + 4 rosters cibles (§1). Sans cela, chaque offre ci-dessous est à vérifier à l'écran avant d'être envoyée. |
| 🟥 URGENT | Transferts | **Offre 1 (Leszno Bulls) : Flink contre Sallijs Bagatskis** (C 28 ans, 73, SHO CHK / DSC, correct, 2 550 000 jusqu'en S29, sur leur liste). Marge 1 630 000 → 3 200 000 (+1 570 000). C4 70 → 73, END 5 → 7. À envoyer aujourd'hui. |
| 🟥 URGENT | Transferts | **Offre 2 (Jessup Baldos) : Conte contre Andreas Kellermann** (LW/C 28 ans, 73, END PAS / CHK, correct, 2 350 000 jusqu'en S28, END 9). Note égale, verdict contre-emploi → correct, END 4 → 9 en L2, marge +1 480 000. |
| 🟥 URGENT | Transferts | **Offre 3 (Miami Maidiacs) : Eskelinen + Carpentier + Juras (FRM) contre Sandro Gavran** (LD/RD 22 ans, 72, END SHO / PAS, END 9, 1 440 000 jusqu'en S28, contre-emploi par la liste mais DEF 8 SKA 7). D1 Seppälä END 4 → Gavran END 9, marge +1 765 000 (Juras ne compte pas dans le plafond). Si refus : retirer Juras, ajouter la pioche du tour 5. |
| 🟥 URGENT | Transferts | **Offre 4 (Leszno Bulls) : Munk + pioche tour 4 contre Marcus Schoen + Theo Kristensen** (RW 28 ans 73 END 10 correct, 2 200 000 S29 ; RW/LW 22 ans 69 SKA SHO idéal, 1 050 000 S28). Marge +3 030 000 − pioche. À envoyer **après** l'arrivée de Gavran (Munk = LD de rechange). RW L2 : Lubowitz END 4 → Schoen END 10. |
| 🟧 IMPORTANT | Transferts | **Offre 5 (Miami Maidiacs) : Lauper + pioche tour 2 contre Bogomir Jenko** (G 26 ans, 81, REF GLO / POS, idéal, 3 080 000, **fin S27**, END 8). G1 71 → 81 (+10, le plus gros gain unique), END 4 → 8. Marge +170 000. Jamais la pioche du tour 1 (Jenko est une location jusqu'à son extension). |
| 🟧 IMPORTANT | Transferts | **Offre 6 (Jessup Baldos) : Kabát + Pålsson (+ pioche tour 3 si refus) contre Ernest Mráz** (RD 28 ans, 84, SKA CHK / PWR, idéal, 3 850 000 jusqu'en S28, END 9). RD1 71 → 84 ; D3 reste 68 (Nokelainen). Marge +1 590 000. Confiance faible (valeur de Mráz pour le comité inconnue). |
| 🟧 IMPORTANT | Transferts | Retirer **Burns** de la liste d'échange (correction §0) ; laisser **Pålsson** (échange prévu, offre 6) ; **Juras** reste sur la liste mais devient la monnaie de l'offre 3 : ne pas le brader seul. |
| 🟧 IMPORTANT | Académie/Draft | Échanger **Öhgren** (U21 LW 21 ans, 50), **Arhosuo** (RD 44), **Daněk** (LW 40) contre n'importe quelle pioche ou prospect avant le 12-26 : sans contrat Farm, ils partent à 22 ans pour rien (§7). |
| 🟩 SUIVI | Transferts | Agents libres : **ne pas participer au Frenzy du jour 3 (10-27)** : marge 1 630 000, aucun libre noté 70+ ne demande moins de 3 900 000 (liste du 10-23). Revoir les demandes aux révisions des jours 10, 20, 30 (11-03, 11-13, 11-23) avec la marge libérée par les offres 1 à 6. |

Résultat attendu si les 6 offres passent : lineup **1350** (+54 contre le plan A, +89 contre aujourd'hui), marge S27 **6 430 000** après l'ELC de Nokelainen, 20 joueurs, VIDE 0 (§3). Si seules les offres 1 à 4 passent : **1324** (+28), marge 5 475 000, soit 4 670 000 après l'ELC de Nokelainen (Pålsson reste alors en D, sans Mráz).

**Fenêtre et calendrier** : échanges et agents libres ouverts jusqu'au 2026-11-28 20:00 UTC (sens du timestamp à confirmer). Un échange accepté passe un comité de 21 votants (24 h) puis la 2e mise à jour quotidienne [G:Trades] : prévoir 2 à 3 jours. **Dernier jour sûr pour envoyer : 2026-10-28** (traité avant la 1re paie du jour 8 = 11-01 : un départ avant la paie libère 100 % du salaire, Finances §3a). Les échanges de choix seuls sont traités tout de suite. Dans les 10 échanges de la ligue, le comité a donné 7 voix pour dans 8 cas, 5 dans 1 cas, 3 dans 1 cas : aucun refus visible en base (ce que `hn_trades` contient = échanges acceptés [H], pas les refus).

## 3. Effet sur le plafond et sur la lineup, offre par offre
Méthode : une offre à la fois, dans l'ordre, la marge ne descend jamais sous 0. Salaires = `silver.hn_league_players` (10-23 pour les adverses, [H] inchangés en S27 pour ct ≥ 27).

| # | Je donne (salaire, fin) | Je reçois (salaire, fin) | Δ marge S27 | Marge après | Δ S28 | Lineup : avant → après |
|---|---|---|---|---|---|---|
| départ | | | | 1 630 000 | engagé 42 345 000 | |
| 1 | Flink (4 120 000, S30) | Bagatskis (2 550 000, S29) | +1 570 000 | 3 200 000 | −1 570 000 | C4 70 (contre-emploi aux 2 postes, END 5) → 73 (correct, END 7) : +3 |
| 2 | Conte (3 830 000, S28) | Kellermann (2 350 000, S28) | +1 480 000 | 4 680 000 | −1 480 000 | LW L2 73 contre-emploi END 4 → 73 correct END 9 : 0 de note, END +5 |
| 3 | Eskelinen (2 570 000, S29) + Carpentier (635 000, S28) + Juras (FRM, 0) | Gavran (1 440 000, S28) | +1 765 000 | 6 445 000 | −1 765 000 | D1 LD Seppälä 73 (END 4) → Gavran 72 (END 9) et Seppälä en D2 (END 4 contre seuil 6 : −2 au lieu de −4) |
| 4 | Munk (2 280 000, S28) + pioche T4 | Schoen (2 200 000, S29) + Kristensen (1 050 000, S28) | −970 000 | 5 475 000 | −970 000 | RW L2 Lubowitz 65 (END 4) → Schoen 73 (END 10) : +8 ; RW L3 Hateboer 60 → Kristensen 69 : +9 |
| 5 | Lauper (3 250 000, S29) + pioche T2 | Jenko (3 080 000, S27) | +170 000 | 5 645 000 | −3 250 000 (Jenko expire : extension à négocier) | G1 71 → 81 : +10 ; G2 Lauper 69 → Kovalev 71 |
| 6 | Kabát (2 160 000, S31) + Pålsson (3 280 000, S27) | Mráz (3 850 000, S28) | +1 590 000 | 7 235 000 | −2 160 000 + 3 850 000 | RD1 Nokelainen 68 → Mráz 84 : +16 en D1, D3 = Nokelainen 68 (inchangé) |
| ELC | Nokelainen (RD 23 ans, 68) monté du FRM | 805 000 [Obs : 3 ELC PRO à 805 000] | −805 000 | **6 430 000** | +805 000 | requis dans tous les scénarios (RD3) |
| | | Hateboer + Jaworski **non montés** | économie ≈ 3 120 000 [H] | inclus | | RW couverts par Schoen + Kristensen + Spinka + Lubowitz |

**Engagement S28** : 42 345 000 − (4 120 000 + 3 830 000 + 2 570 000 + 635 000 + 2 280 000 + 3 250 000 + 2 160 000) + (2 550 000 + 2 350 000 + 1 440 000 + 2 200 000 + 1 050 000 + 3 850 000) + 805 000 = **37 745 000** (−4 600 000) ; S29 : 21 900 000 → ≈ 14 550 000. Plafond S28 non publié (annonce du 11-21). Marge de prolongation : Seppälä et Blednov à 4 400 000 chacun, Bélanger 1 870 000, Jenko [H : 4 500 000 ?] rentrent largement.

**Lineup après les 6 offres** (20 joueurs : 4 C / 4 LW / 4 RW / 3 LD / 3 RD / 2 G, **VIDE : 0**) :
| Ligne | LW | C | RW |
|---|---|---|---|
| L1 | Yokoyama 69 | de Bruin 72 | Spinka 72 |
| L2 | Kellermann 73 (END 9) | Papež 70 | Schoen 73 (END 10) |
| L3 | Stone 65 | Blednov 74 | Kristensen 69 |
| L4 | Bélanger 60 | Bagatskis 73 | Lubowitz 65 |
| Paire D | LD | RD |
|---|---|---|
| D1 | Gavran 72 (END 9) | Mráz 84 (END 9) |
| D2 | Seppälä 73 (END 4, point faible restant) | Marquardt 71 |
| D3 | Burns 66 | Nokelainen 68 |
| G | Jenko 81 (END 8) | Kovalev 71 |
Somme : attaquants 835 (plan A 813), défenseurs 434 (412), G1 81 (71) = **1350**. Variantes : offres 1-4 seulement (Jenko, Mráz absents) : 835 + 418 + 71 = **1324** ; avec Lauper et Kovalev en place et Pålsson (RD 68) à la place de Mráz, les RD sont Marquardt, Nokelainen, Pålsson/Kabát. Après chaque échange acquis, le brief Tactique re-saisit la lineup (PP/PK/4v4 à refaire : Schoen, Kellermann, Gavran, Mráz changent les unités).

## 4. Chaque cible : fiche, verdict, prix, repli
Données `silver.hn_league_players` 10-23 (S26), à ré-exporter. « Valeur pour le comité » : **inconnue** (aucune donnée de refus en base) ; les repères de prix viennent des 10 échanges de la ligue (§5).

| # | Cible (club) | Âge, poste | Note | Talents fort / faible | Verdict (hyp.) | END | Spéc. | Salaire, fin | Gain chiffré | Confiance | Repli si l'offre échoue |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Bagatskis** (Leszno, liste d'échange) | 28, C | 73 | SHO CHK / DSC | correct | 7 | 0 | 2 550 000, S29 | C4 +3, cap +1 570 000 | moyenne (il est proposé par le club) | **Hunter** (Seoul, 23, C/LW 71, END FOF / SKA, correct, FOF 9, END 7, 1 120 000, fin S27) : C4 +1, cap +3 000 000, mises au jeu 6 → 9 ; extension à négocier |
| 2 | **Kellermann** (Jessup) | 28, LW/C | 73 | END PAS / CHK | correct | 9 | 0 | 2 350 000, S28 | verdict contre → correct, END +5, cap +1 480 000 | moyenne-faible | garder Conte (73, 3 830 000) ; chercher un LW 70+ SHO/PAS/SKA dans le nouvel export (Pirttijärvi Miami 34 ans 71 idéal 3 510 000 S27, 3 spéciales : repli à vérifier) |
| 3 | **Gavran** (Miami) | 22, LD/RD | 72 | END SHO / PAS | contre-emploi (7/8 compétences plafonnées, DEF 8, SKA 7, END 9) | 9 | 0 | 1 440 000, S28 | D1 END +5, cap +1 765 000 | moyenne-faible (pas sur la liste) | **Gilbert Kohler** (Leszno, 25, LD 69, DEF CHK / DSC, **idéal**, END 6, 2 spéciales, 2 670 000, S31) : verdict idéal mais contrat de 5 ans à 2 670 000 ; ou **Hjalmar Kellman** (Miami, liste, 29, LD 66 idéal, 2 200 000, S28) |
| 4a | **Schoen** (Leszno) | 28, RW | 73 | END SHO / CHK | correct | 10 | 2 | 2 200 000, S29 | RW L2 +8, END +6 | moyenne-faible | **Ellefsen** (Miami, liste, 33, RW 76 correct SHO CHK / DSC, END 7, 4 730 000, S27) : +11 sur Lubowitz mais 4 730 000 de salaire |
| 4b | **Kristensen** (Leszno) | 22, RW/LW | 69 | SKA SHO / FOF | **idéal** | 5 | 1 | 1 050 000, S28 | RW L3 +9 sur Hateboer, 22 ans | faible (jeune, bon marché : le club le garde) | promouvoir Hateboer (RW 60 idéal) et Jaworski (63) |
| 5 | **Jenko** (Miami) | 26, G | 81 | REF GLO / POS | **idéal** (faible POS = clé) | 8 | 2 | 3 080 000, **S27** | G1 +10, END +4 | **faible** | garder Kovalev (71) ; **Conn** (Jessup, liste, 28, G 65, 1 490 000, S29) n'est pas une amélioration : écarté |
| 6 | **Mráz** (Jessup) | 28, RD | 84 | SKA CHK / PWR | **idéal** | 9 | 0 | 3 850 000, S28 | RD1 +16 | **faible** | **Beaudry** (Jessup, 27, RD 78 idéal SKA DEF / SHO, END 7, 2 spéciales, 4 590 000, S29) : +10, cap −2 430 000 sur le même paquet ; ou **Deursen** (Leszno, liste, 32 ans, 75, ct. 26 expiré : à revérifier) |

Autres C et ailiers rencontrés et **non retenus** (talents) : Kariya (Jessup, C 28 ans, 78, END DSC / PWR, **contre-emploi**, END 9, 2 spéciales, 2 010 000, S28) : +8 de note et −2 110 000 de salaire sur Flink, mais contre-emploi [U] ; il devient le **test** de l'hypothèse (tableau §8, T-B) et non un achat. Martens (Leszno, C 33 ans 79, 5 671 000, S27) : trop cher. Cho (Seoul, liste, C 69 contre-emploi). Aliev (Miami C 70 contre). Mrkvička (Seoul, RD 88, 34 ans, 7 610 000, liste) : hors marge, 34 ans. Davis (Seoul, G 86, 6 300 000, S31) : hors marge.

Prix de repli (rachat si l'achat déçoit [G:Finances], moitié du restant) : Bagatskis 3 825 000 sur 3 ans ; Kellermann 2 350 000 sur 2 ans ; Gavran 1 440 000 ; Schoen 3 300 000 ; Kristensen 1 050 000 ; Jenko 1 540 000 ; Mráz 3 850 000. Un joueur reçu en fenêtre I ne se rééchange pas en fenêtre II (fiche) : l'issue d'un mauvais achat est le rachat, pas la revente.

## 5. Pioches de draft S27 (tours 1 à 5) et monnaie d'échange
Faits : nos 5 choix S27, un par tour, ligue a40e48a8, `original_team` NULL, ordre inconnu (`overall_rank` NULL) ; en S26 nous étions 55 / 75 / 95 (15e de chaque tour). Les S28 n'apparaissent pas en base (guide : 10 choix sur 2 saisons ; Académie : export Draft > My picks S28).
Repères des 10 échanges de la ligue (`silver.hn_trades`) :
| Date | Donné | Reçu | Lecture |
|---|---|---|---|
| 10-21 | Green Bay : C 31 ans 80, 6 000 000 (+ 6 120 000 en S27-S28) | Roswell : pioche **tour 1 S27** | un tour 1 = un 80 de 31 ans |
| 10-21 | Miami : pioche **tour 5 S27** | Mississauga : RD U21 21 ans, 55 | un tour 5 = un prospect de 55 |
| 10-20 | Riverside : RW 34 ans 69 (expire) + tour 4 S27 | Baie-comeau : tour 2 S27 | un tour 2 = un 69 de 34 ans + un tour 4 |
| 10-20 | Richmond : RW/LW 29 ans 69 + prospects FRM 53, U21 51, G 56 | Essen : RW 34 ans 74 + LW 27 ans 69 | des prospects FRM/U21 servent de monnaie |
| 10-19 | Wilhelmsburg : 5 pioches (T1 S26, T1+T2+T2+T3 S27) | Parkland : LW 24 ans 73, 3 790 000 jusqu'en S30 | cinq pioches = un 73 de 24 ans |
| 10-18 | Sherbrooke : tour 3 S26 | Mississauga : RD 31 ans 72, 4 130 000 | un tour 3 = un 72 de 31 ans |
| Tous | `salary_impact` = 0 pour les deux clubs dans les 10 cas, même quand les salaires diffèrent | | champ non fiable pour le plafond |
Affectation de nos pioches (décision) : **tour 1 et tour 2** gardés pour la draft (Duguay, Klose, Dunn au tour 1, Adams au tour 2, Académie) **sauf le tour 2 dans l'offre 5 (Jenko)** ; **tour 3** = renfort de l'offre 6 (Mráz), **tour 4** = offre 4 (Schoen + Kristensen), **tour 5** = offre 3 (Gavran). Une pioche ne s'ajoute qu'au 2e envoi, après un refus du comité : on commence sans. **Tension avec Académie** : le tour 2 sert à Adams (RD 52, idéal) ; coût de l'offre 5 = ne plus avoir Adams garanti. Jugement : G1 +10 pèse plus qu'un RD de 48 qui jouera en S29 au mieux.
Pas d'échange de pioches S28 possible tant que l'export My picks S28 manque.

## 6. Gestes exacts à l'écran
1. Transfers > Trade Center : exporter (§1).
2. Roster PRO : cocher **Burns** > retirer de la liste. Cocher *disponible* (Available for trade) Flink, Conte, Eskelinen, Carpentier, Munk, Lauper, Kabát, Pålsson (déjà), Juras (déjà). Les joueurs adverses ne se « marquent » pas : ouvre leur fiche > *Propose trade*.
3. Envoyer les offres **1, 2, 3 aujourd'hui** (3 clubs différents ou indépendants), attendre le comité (24 h), puis 4 (après Gavran), 5 et 6 le 10-27 (dernier jour sûr : 10-28).
4. Chaque lendemain : relire `gold.hn_cap_outlook` (marge ≥ 0) et le roster PRO.
5. Ne signer l'ELC de Nokelainen **qu'après** l'offre 6 si Mráz arrive ; sinon avant le 10-31 comme prévu (Finances).

## 7. Ce que tu as pu oublier
| Point | Constat | Action |
|---|---|---|
| Prospects qui partent pour rien | Öhgren (LW 50), Arhosuo (RD 44), Daněk (LW 40) n'ont pas de contrat : départ à 22 ans (S28). Cooper, Krejčí, Drouin vont en Farm. Les prospects servent de monnaie (échange du 10-20 : G 56, U21 51, FRM 53) | proposer Öhgren + Arhosuo + Daněk dans l'offre 4 ou 6 à la place d'une pioche ; un joueur non tradable n'apparaît pas : les 24 U21 sont `tradable` = true |
| Excédents à nous | U21 : Barrett (LW 42), Hawkins (RW 36), Signer (G 39) ; U17 : Marchenko (RD 38) | compléments gratuits (même méthode) |
| Juras (FRM LD 67, 26 ans, sans salaire) | déjà sur la liste ; Effectif le garde ; c'est notre seule monnaie à note ≥ 66 sans effet de plafond | Offre 3 ; sa perte coûte 0 en lineup (Koukal 58, von Arx 55 couvrent FRM) |
| Hongisto (U21 RW 20 ans, 49) | sur la liste, contre-emploi | l'ajouter en complément de l'offre 4 si refus |
| Ellefsen (Miami, RW 76, 33 ans, 4 730 000, S27) | sur la liste d'échange du club : seule aile 75+ avec contrat S27 ; salaire trop lourd tant que les offres 1 à 4 ne sont pas passées | à reconsidérer après l'offre 4 si Schoen est refusé |
| Rachat vs échange | Eskelinen : rachat 3 855 000 sur 3 ans contre 2 570 000/an libérés par un échange (Finances §3a) | échange d'abord |
| Séquence cap | marge 1 630 000 : aucune offre entrante ne dépasse la marge restante ; ordre 1 → 2 → 3 puis 4 respecte cela (offre 4 : −970 000 sur 6 445 000) | ne jamais envoyer 4 avant 3 |
| Seppälä/Blednov (expirants) | Seppälä 73 (32 ans) : Gavran puis Mráz le rendent moins critique ; prolongation 1 an ≤ 4 400 000 (Finances) reste vraie | pas de changement |
| Flink et Conte : « talents faibles, note haute » | valeur d'échange maximale maintenant (Flink 24 ans 70 ; Conte 25 ans 73) | offres 1 et 2 |
| FRM : excédents/surplus | FRM compte 22 | pas de lien avec le plafond [commun.md] |

## 8. Tests (confiance faible : ce qui prouvera que j'avais tort, date)
| Test | Mesure | J'ai tort si | Date |
|---|---|---|---|
| T-A Kellermann (correct) remplace Conte (contre-emploi) à note égale | points/match de Kellermann en L2 contre Conte en S26 + 5 matchs | points/match de Kellermann < ceux de Conte sur les 5 premiers matchs S27 (boxscore) | 5e match de ligue (≈ 2026-11-05) |
| T-B hypothèse « contre-emploi » (`hn_position_keys`) | Kariya (C 78 contre-emploi) acheté **seulement si** T-A et les tests Effectif (Conte, Flink, Eskelinen) donnent « contre-emploi = mauvais » | si Conte/Flink font mieux que la médiane de leur poste, l'hypothèse tombe et Kariya (2 010 000) devient l'achat prioritaire en C | 5e match |
| T-C Jenko | % d'arrêts de Jenko sur ses 5 premiers départs contre Kovalev S26 | % d'arrêts < Kovalev S26 ou négociation de son extension > 4 500 000 [H] | 5e départ |
| T-D Gavran en D1 | plus/moins et TOI de Gavran | plus/moins < −1/match sur 10 matchs | 10e match (≈ 2026-11-10) |
| T-E Mráz | note stable 84 ; plus/moins | note < 82 après 10 matchs | 10e match |
Le plan de sortie de chaque achat est le rachat de la ligne « prix de repli » §4 ; aucun achat n'est irréversible avant le 11-28.

## 9. Il me manque (à réunir ensemble)
| Donnée | Comment |
|---|---|
| Trade Center S27 (tous les joueurs, liste d'échange, prospects U21/FRM) | Transfers > Trade Center, toutes les pages, aujourd'hui (§1) |
| Agents libres actuels et leur demande | Transfers > Free agents, toutes les pages |
| Contrats S27 des 4 clubs cibles (les « fin S26 » ont expiré) | page *Roster* de Leszno, Jessup, Miami, Seoul |
| Valeur d'un joueur pour le comité de 21 votants | non publiée : la mesurer sur les 6 offres (accepté / refusé, nombre de voix) et l'enregistrer dans la fiche |
| Nos pioches S28 | Draft > My picks, onglet S28 |
| Salaire réel de Hateboer et Jaworski | Contract talks (Effectif/Finances) |
| Si une offre peut contenir des joueurs FRM / U21 sans contrat | l'écran d'offre le dit : essayer avec Öhgren |

## 10. Conseils ajoutés à `learnings.md`
C-053 à C-058 (offres 1 à 6).
