# Marmandes (307) — Tactique — amical Everton (3 nov 11:00, ext., 13e EN3) + ligue du 5 nov

Base : `gold.dm_effectif`, `gold.dm_verdict_joueurs`, `silver.dm_tactic`, `gold.dm_setpieces` (exports 307 du 2026-11-02 21:59 UTC, 20 joueurs), `gold.dm_saison_bilan`, `gold.dm_matchs`, `gold.dm_tirs_profil`, `gold.dm_adversaires`. Le brouillon du 31/10 est périmé et non utilisé. Police : à passer avant rendu (non lancée par moi). Tout le monde : condition 100, forme 0, aucune blessure (`gold.dm_setpieces.blessure` nul pour 20/20). Charbonnier et Aponte ne sont plus dans la base.

## Fiche de saisie — écran Squad (à faire aujourd'hui, amical Everton)
**Formation : 343** (base : `gold.dm_saison_bilan`, ligue 343 = 8 matchs 3V 4N 1D, xG contre 0,79, 5,5 tirs contre ; 352 = 22 matchs 5V 4N 13D, xG contre 1,88, 11,6 tirs contre ; 352 aux 2 amicaux 0V 2N). Réserve : les 343 ont été joués avec une force d'équipe plus haute (108-121 contre 52-74 au 352, `gold.dm_matchs.force_nous`) : confiance moyenne. Les 5 derniers matchs de ligue en 352 : L L W L L.

| Poste | Rôle | Joueur | Note | Cœur |
|---|---|---|---|---|
| GK | GK | M. Comonfort (19, pot 3) | 11,4 | Volatile |
| DLC | LD | B. Desagnat (19, pot 3) | 12,8 | Volatile |
| DC | CD | Y. Messimy | 14,0 | Volatile |
| DRC | LD | M. Schmitz (19, pot 3) | 9,4 | Volatile |
| ML | DWG | C. Lerch (21, pot 3) | 9,7 | Volatile |
| MLC | CM | N. Taddei (20, pot 3) | 12,3 | Volatile |
| MRC | DLP | C. Lévêque (20, pot 3) | 11,2 | Volatile |
| MR | DWG | F. Bodian (23, pot 3) | 9,0 | Volatile |
| FLC | FN | A. Vargas | 12,3 | Volatile |
| FC | CF | B. Vasilev (Key) | 13,5 | Volatile |
| FRC | FN | G. Luzerne (18, pot 3) | 10,2 | Volatile |

Rôles : seuls ceux déjà saisis et lus dans `gold.dm_effectif.slot` (GK, LD, CD, DWG, CM, DLP, CF, FN) ; le choix par poste 343 est une hypothèse. Notes = `gold.dm_verdict_joueurs.note_poste`.

| Curseur | Valeur | Base |
|---|---|---|
| Defensive line | 1 | `silver.dm_tactic` (1), laissé : 343 à 0,79 xG contre |
| Pass preference | 0 (Short) | idem (0) |
| Pass focus | 1 | idem (1) |
| Shooting | 1 | idem (1) |
| Headers | 1 | idem (1) ; test Headers 2 non fait ce soir (amical = une seule chose testée : 343 + jeunes) |

Options : **Counters coché**, Pressing / Through balls / Run with ball décochés. Base : `gold.dm_tirs_profil` counter = 45 tirs, 8,09 xG, 15,6 % de conversion (2e source de tirs hors CPA) ; coût −1 % de condition (`resume.md`). Pas d'option en base (`silver.dm_tactic` n'a pas ces colonnes) : « il me manque les cases actuelles, cherché dans : `silver.dm_tactic`, `gold.dm_matchs.counters` » ; fais comme ci-dessus.

| Banc | Joueur | Statut |
|---|---|---|
| S1 | N. Lafleur (GK) | EMR |
| S2 | H. Hardt (DC, 17) | DEV |
| S3 | C. Toussaint (MC, 18) | DEV |
| S4 | A. Labourd (DLC, 18) | DEV |
| S5 | B. Ohara (FCR, 31) | RAT |
Base : DEV = temps de jeu à un jeune, EMR = blessure seulement, RAT = note < 6,5 (`connaissance.md` § 11). Au repos : Cave, Cleary, La Ferrière (rien à entraîner : pot 0 / adultes), McCulloch.

**Set pieces** (saisie : « PRI » = preneur prioritaire ; DEF/ATT = default ou box ; retire les anciens PRI)
| PEN | FK | COR | DEF box | ATT box | Capitaine |
|---|---|---|---|---|---|
| Vargas (rang_penalty 1, finition 17) | Vargas (rang_coup_franc 1, précision 17) | Lévêque (rang_corner 2 ; Cave, rang 1, au repos) | Messimy, Schmitz | Luzerne (rang_surface 1), Vasilev (3) | Schmitz (rang_capitaine 4 ; Cleary 1, Ohara 2, Cave 3 au repos) |
À décocher : PEN Bodian, FK Cave et Schmitz, FK/COR/PEN Lévêque sauf COR, capitaine Lafleur. Placements DEF/ATT box = hypothèse (C-010 de 547 ; base : contre set piece 129 tirs, 106 en surface, 55 de la tête, 24 buts, `gold.dm_tirs_profil`).

## Contrats de 2 jours
- **Desagnat joue** : contrat valide au coup d'envoi (2 j, `gold.dm_effectif.contract_days`), jeune pot 3 en HIGH ; il me manque l'heure exacte d'expiration (cherché dans : `dm_effectif`, `connaissance.md`). Sa prolongation n'est pas dans `fait-2026-11-02.md`.
- **McCulloch ne joue pas** : il part, aucun gain d'entraînement ; Luzerne (pot 3) prend sa place.

## Adversaire et focus défensif
Everton (13e EN3) et Liège (1er BE1) ne sont pas dans `gold.dm_adversaires` (ligue D4 seulement) : il me manque effectif, tirs et tactique adverses, cherché dans : `gold.dm_adversaires`, `silver.dm_fixtures`, `gold.dm_matchs`. Export à faire : page Équipe d'Everton. L'écran Squad n'a pas de focus défensif ; le seul levier défensif est Defensive line (1).

## Ligue 5 nov — Raon-l'Étape (11e, domicile)
Fiche : nos résultats D 0-0, W 1-0 ; xG concédé 0,47 (`gold.dm_adversaires`), donc peu de buts : on garde la défense 343 de 0,79 xG contre. Desagnat et McCulloch (2 j) sont absents du XI : contrat échu le 5 sauf prolongation, aucune en base.
GK Lafleur ; DLC La Ferrière (LD), DC Messimy (CD), DRC Schmitz (LD) ; ML Taddei (DWG), MLC Cave (CM), MRC Lévêque (DLP), MR Cleary (DWG) ; FLC Vargas (FN), FC Vasilev (CF), FRC Ohara (FN). Curseurs 1 / 0 / 1 / 1 / 1, Counters coché. Banc : S1 Comonfort EMR, S2 Lerch DEV, S3 Bodian RAT, S4 Luzerne DEV, S5 Hardt DEV. Set pieces : PEN Vargas, FK Vargas, COR Cave, capitaine Cleary, DEF box Messimy + Schmitz, ATT box Vasilev + Ohara. Base : notes et rangs de `gold.dm_verdict_joueurs` / `gold.dm_setpieces`. Compo à ré-exporter après l'amical.

## Contrôle SQL (lectures du tour)
11 titulaires distincts + 5 remplaçants distincts, tous dans `gold.dm_effectif` ; condition 100 ≥ 80 ; blessure nulle ; Vasilev (Key, 0 % de temps de jeu) titulaire ; 5 jeunes pot 3 titulaires (Desagnat, Schmitz, Lerch, Taddei, Lévêque, Bodian, Luzerne = 7) et 3 en banc DEV.

## Ce qui prouvera que j'avais tort
- 343 : xG contre > 1,4 ou plus de 10 tirs contre à Everton (352 saison : 10,0 tirs, `gold.dm_saison_bilan`) — match du 2026-11-03.
- Jeunes : un titulaire pot 3 avec moins de 20 min jouées (`gold.dm_effectif`, apps) — 2026-11-03.
- Counters : 0 tir de counter à Everton (`gold.dm_matchs.counters` = 0) → décocher.

Conseils ajoutés dans `outputs/derbymanager/learnings.md` : C-012, C-013.
