# Derby Manager — reprise du 2026-10-31 (tout ce qui a été compris et reste à faire)

Écrit le 2026-10-30 à la demande de l'utilisateur : « garde tout, on creuse demain ». Sources : `gold.dm_verdict_joueurs`, `gold.dm_entrainement_plan`, `silver.dm_player_tips` (infobulles du jeu), `outputs/derbymanager/veille/connaissance.md`, `docs/fiches/derbymanager/resume.md` (glossaire des colonnes).

## 1. Question ouverte n°1 : « je n'arrive pas à faire remonter la condition »
L'utilisateur tourne l'équipe en permanence et la condition ne remonte pas. **À comprendre demain, avant tout autre conseil.**

Constat en base (Queen of the South, fin de saison 26) : la **condition est correcte, 83 à 100 %** (Bock 83, Neufeld 85, Arneberg 85, Ludig 85, … Vigerie 100). Ce qui est bas, c'est la **forme (FRM)** : Bjerg 13, Kjer 21, Vigerie 26, Schultze 30, Bock 32, Connelly 34, Ludig 37. Hypothèse n°1 : l'utilisateur parle de la **forme** (ou du cœur SHA), pas de la condition. À lui demander : quelle colonne, quel joueur, quelle valeur.

Règles connues sur la condition (sources : infobulles + Discord, voir `connaissance.md`) :
- Récupération par nuit : LOW +4 %, MED +3 %, HIGH +2 %. Les intensités actuelles sont HIGH pour 10 joueurs → récupèrent le moins vite.
- Chaque option tactique cochée (Pressing, Counters, Through balls, Run with ball) = −1 % de condition pour tous, à chaque match.
- FIT (natural fitness 0-3) = vitesse de perte de condition par match. Bock, Cooper = 0.
- Risque de blessure ≈ condition manquante ; jouer au-dessus de 80 %.
- Banc avec statut CON : remplace un joueur sous 80 %.
- La **forme** ne remonte qu'en jouant (monte à chaque match joué, baisse à chaque match manqué) : tourner l'équipe la fait baisser pour ceux qui ne jouent pas. Le **cœur (SHA)** suit la forme et la satisfaction. **Tourner l'équipe tout le temps est donc probablement la cause** : personne ne cumule assez de matchs pour que la forme monte. À tester.
- Fin de saison : une semaine de pause, la condition est remise à zéro [H, à vérifier dans `connaissance.md`].

À faire demain : interroger `connaissance.md` (thème condition/forme) et Discord pour un chiffre exact de gain de forme par match, puis lui répondre colonne par colonne.

## 2. Sens des codes (déjà expliqué à l'utilisateur)
- **SUB** : AUTO mélange · RAT « Judge by ratings » (remplace un titulaire dont la note est ≥ 0,5 sous la moyenne ou < 6,5) · CON « Preserve condition » (remplace sous 80 %) · DEV « Give training time » (fait entrer un jeune pour ses minutes) · IMP « Is important player » (entre en priorité si l'équipe ne gagne pas) · EMR « Only in emergency » (blessure seulement, par ex. 2e gardien).
- **Colonnes** : CON condition · SHA cœur (Confident > Reliable > Inconsistent > Volatile) · FRM forme · PT satisfaction de temps de jeu (attente Key 75 %, First team 60 %, Rotation 40 %, Backup 25 %) · STA vestiaire (Leader +1 % de team spirit, Regular 0, Outsider −1 % ; plainte −3/−2/−1 %) · BU/PBU capacité 1-20 de construire / empêcher · POT chance du tier suivant · FIT perte de condition · EXP régularité · TR « a/b » (a > b ⇒ plus d'entraînement) · SKILL niveau relatif.
- **Scouting** : 3 par jour gratuits, stock de 20 ; obligatoire avant d'enchérir ; niveaux 0-3 qui baissent d'un cran par semaine. Noté dans `connaissance.md`.
- **Vieux joueurs** : à acheter (« oldies are really worth it », dev 2026-10-05). « Solid » 31 ans et plus : médiane 8,0 M contre 11,1 M à 24-27 ans. Équilibre conseillé 5 vieux / 5 au pic / 5 en progression / 5 de l'école.

## 3. Queen of the South (547) — plan rendu le 30/10
- Compo 5-4-1 : GK Vigerie · DL FB Cáceres · DLC LD Connelly · DC CD Pilot · DRC LD de Tavernost · DR FB Kelly · ML DWG Neufeld · MLC HM Forrest · MRC DLP Vicomte · MR DWG Bjerg · FC CF Eliassen. Capitaine Vicomte. Banc : Vidales EMR · Ludig CON · Bock DEV · Linden DEV · Allan RAT. Schultze et Ndiaga blessés.
- Curseurs : ligne Low, passes Direct, jeu Wide, tirs From box, têtes au milieu ; seule l'option Counters.
- Entraînement : D → Anticipation, M → First Touch, F → First Touch, GK → Reaction. Intensités : Connelly HIGH, Pilot MED, Vidales MED, Arneberg MED, Schultze LOW.
- Installations : payer les 8 M manquants (niveau 17). Doute : le dev dit « l'effectif avant les installations ». Décision prise : installations (9 plaintes).
- Transferts : liste Vidales et King ; prolonger Neufeld (40 j) et Bjerg (46 j) ; promouvoir Almgren ; scouter Mansfield (DC, 3,5 M), Jaén (MC, 6,2 M), Maillard (FC, 4,9 M) ; viser un « Solid » de 29-31 ans vers 8 M.
- Budget : 20,4 M − 8 M = 12,4 M ; marge salariale 634 k par jour.
- Bilan saison 26 : 7e/8, 2 V 4 N 26 D (9-80), xG 0,43 pour / 2,62 contre, 3,3 tirs pour / 16,7 contre. Le conseil attend la 6e place. Pas de relégation.

## 4. Marmandes (307)
Zéro export. À faire : pages d'équipe (Squad, Training), Matches, Finances, Facilities, School, Market. Puis le même travail qu'au point 3.

## 5. Ce qui manque encore
| Manque | Comment le réunir |
|---|---|
| Marmandes complet | exporter toutes les pages du club 307 |
| Marché 8-20 M | filtrer le prix 8-20 M sur l'écran Market, exporter |
| Adversaires | exporter `/teams/<id>` de Celtic, Rangers, Hearts et des autres + leurs matchs (vue gold « stratégie par adversaire » à concevoir) |
| Calendrier saison 27 | exporter Competitions / Matches |
| Effet chiffré d'un niveau d'installations | le dev ne le donne pas ; chercher dans Discord |
| Gain de forme / condition par match | chercher dans Discord (voir point 1) |

## 6. Nettoyage base en attente d'accord de l'utilisateur
Supprimer `gold.dm_marche_postes` (défectueuse) et `gold.dm_joueurs` (première version). Ne pas les lire.

## 7. Côté Claude
- Gros travail de conception : prochaine étape probable = vue gold adversaires, vue gold condition/forme (par joueur : condition, forme, intensité, FIT, minutes jouées), vue Marmandes.
- La session est repassée sur Sonnet : rappeler `/model opus` avant toute conception SQL.
