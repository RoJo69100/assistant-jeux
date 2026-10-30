---
name: derbymanager-regles
description: Règles Derby Manager (football, derbymanager.com, DM2 bêta) — saison de 30 matchs et ~35 jours, divisions D1-D4 par pays, nouvelles ligues S26 (Écosse 8 équipes, sans relégation), coupes (NC, AC, CC), primes de victoire et de fin de saison, avantage du terrain, joueurs et compétences renommées, tiers, âge et retraite, forme, condition, blessures, sharpness, satisfaction et temps de jeu, Team Spirit, réputation du manager, licenciement. À charger pour toute question de règle, de calendrier, d'évaluation d'un joueur ou de risque de licenciement.
---

# Derby Manager — règles générales

Sources : veille complète du 2026-10-30 (`outputs/derbymanager/veille/connaissance.md`, fusion de partie-A/B/C). `dev` = compte `derbymanager` (le développeur). Statut « confirmé » sauf mention. Le plus récent l'emporte. Jamais deviner : une règle absente ici = « il me manque X ».

## Calendrier et compétitions
- Saison = 30 matchs de ligue (ligue de 16 équipes en D4 Italie) — #italy 2024-07-20 / 2024-06-03, dev.
- Saison ≈ 35 jours réels (annonces IFA 2026-07-17, 08-21, 09-25, 10-30) — #france IFA ; #quick-questions 2026-08-15 randykeys — confirmé.
- Lundi : nouvelle saison générée ; mercredi : premiers matchs ; dernier match samedi (finale CC) — #england 2025-09-02, dev.
- Pré-saison de 5 jours (2026-09-25) : +20 % de condition, blessures réduites de 5, 2 amicaux ; condition non remise à 100 % — #quick-questions 2026-09-25, dev.
- 4 divisions par pays, 5 pays jouables (Angleterre, Espagne, Italie, France, Allemagne), ~450 bots — #italy 2026-03-15 / 2025-07-31, dev.
- **S26 (2026-09-28)** : Pays-Bas, Portugal, Belgique, Écosse, une seule D1, « no relegations (for now) » ; Écosse = 8 équipes qui se rencontrent 4 fois (28 matchs) — #updates 2026-09-28, dev.
- Nouvelles ligues : « Better than d2, but not d1 level », moins d'argent et de réputation ; seuls 3 clubs vont en coupe internationale — #belgium 2026-10-01 / 10-08, dev.
- Montée : 4 places observées en D2 — #discussion 2025-02-10, dev — complété (une observation).
- Coupes : NC, AC, CC ; pas de coupe de ligue ; CC en groupes de 8 équipes (2 matchs contre « strong », 2 contre « weak »), 4 premiers en élimination, jusqu'à 8 matchs — #updates 2025-07-02, dev ; #italy 2025-08-23, dev.
- Départage : différence de buts, buts marqués, puis aléatoire — #italy 2025-03-13, dev.
- Avantage du terrain : jusqu'à 10 % par joueur (~5 % en moyenne), ligue seulement, **aucun en coupe** — #discussion 2026-02-14, dev ; #england 2026-09-16, dev.
- Amicaux : existent depuis avril 2026, aléatoires, « training, experiment with formations » ; effets sur satisfaction non expliqués — #quick-questions 2026-06-15, dev — complété.
- Pas de tactiques programmées : on règle la formation du match du jour — #discussion 2026-07-28, dev.
- 3 jaunes = 1 rouge ; rouge = 2 matchs de suspension — #updates 2025-09-08, dev.

## Primes et récompenses
- Victoire par division (D4/D3/D2/D1) : 200 k / 300 k / 500 k / 800 k ; moitié pour un nul ; 1,2 M en NC et AC ; 2 M en CC — #updates 2025-05-20, dev. En D4 : 200 k + ~120 k à domicile (#quick-questions 2026-10-03, dev). Étiquette exacte des 800 k (prime ou droits TV) = en doute.
- Fin de saison : seuls les 4 premiers de chaque division reçoivent 20 M / 10 M / 5 M / 2,5 M ; pots NC 10 M, AC 10 M, CC 20 M — #updates 2025-05-20, dev.
- CC : 28 M si 8 victoires (6 minimum pour la coupe) + ~3 M d'affluence par match — #discussion 2025-09-19, dev.

## Joueurs et attributs
- Compétences (noms 2026-04-05) : set pieces → reaction ; crossing → ball control ; dribbling → technique ; long shots → accuracy ; finishing → shooting ; centre = passing + accuracy — #updates 2026-04-04/05, dev. Pressing → anticipation (2025-07-02) ; anticipation → creativity (2024-08-24).
- Gardien : 5 compétences utiles (handling, positioning, agility, aerial, reaction/set pieces) — #discussion 2025-06-03, dev.
- Tier d'un joueur = rang relatif (meilleur 10, 50e 9, 250e 8) ; world class 9,01-10, elite 7,01-9,0 — #general 2025-03-31, dev. Seuils inférieurs : inconnus.
- Tier d'équipe : 1re équipe en popularité = 10, 50e = 9 ; fixe revenus et plafond — #discussion 2026-08-22, dev.
- Hors poste : même ligne = petite pénalité, autre ligne = grosse ; ~5-10 matchs pour bien jouer un nouveau poste ; GK et champ non échangeables — #quick-questions 2025-07-31, dev ; #italy 2024-06-13, dev.
- Effectif : minimum 18 non listés ; 442 demande ~19 joueurs ; 2 GK ; limite de 25 pour promouvoir de l'école ; 16 joueurs de 12,5 M valent mieux que 20 de 10 M — #discussion 2025-01-08, dev ; #discussion 2026-06-28, dev ; #quick-questions 2026-08-19, dev.
- Âge : natural fitness maximale ~26 ans ; baisses fréquentes de 28 à 34 ans ; pas de prolongation à 37+ ; max 38 ; âge réel caché ±3 ans — #quick-questions 2025-02-04, dev ; #updates 2024-07-16, dev ; #belgium 2026-10-08, dev.
- Gain ou perte maximum d'une compétence : ±1 par jour — #discussion 2025-06-11, dev.
- Traits : 10 spécialistes, 5 leaders (Tenacious, Influential, Determined, Hard-working, Relentless), 11 personnalités — #discussion 2026-10-01, dev.

## Forme, condition, sharpness
- **Forme (2026-10-21)** : monte quand il joue, baisse quand il ne joue pas, vitesse variable — #updates 2026-10-21, dev. Cycle 1-20 de 2024 : contredit.
- Condition = fatigue longue. Fatigue = énergie courte par action, récupère de 25 % par minute ; chaque cumul égal à la condition actuelle = −1 % de condition ; **chaque option tactique cochée = −1 % de condition à tous** — #updates 2026-10-18, dev.
- Perte de condition = pourcentage de la condition restante (à 50 %, il perd 1 % au lieu de 2 %) ; un joueur à 100 % peut perdre ~7 % par match — #inconnu 2026-10-19, dev.
- Récupération : +3 %/jour ; Low +4 %, Medium +3 %, High +2 % selon l'intensité ; blessé +4 % — #updates 2025-10-15, dev ; #discussion 2025-10-21, dev.
- Blessure : chance = condition manquante (70 % ⇒ 30 %) ; base non nulle à 100 % ; durée courte (moyenne 2,3-2,5 jours) ; chaque blessure raccourcie d'un match ; l'écran montre la condition seule (2026-10-25) — #quick-questions 2025-01-24, dev ; #updates 2026-10-25, dev.
- Sharpness = forme + club fit + autres modificateurs, légèrement aléatoire ; le cœur à l'écran = le visage probable — #quick-questions 2026-09-06, dev ; #italy 2025-08-06, dev. Ancienne sharpness « jouer régulièrement » : contredit.
- Les GK perdent peu de condition — #inconnu 2026-10-30, dev.
- Au-dessus de 80 % = « ok to play » ; le dev garde ses joueurs entre 80 et 93 % — #france 2024-12-18, dev — avis.

## Satisfaction, temps de jeu, Team Spirit
- **Temps de jeu attendu** : Key 75 %, First team 60 %, Rotation 40 %, Backup 25 % des matchs (20 matchs : 15, 12, 8, 5) — #general 2026-08-20, dev. Ancien « Key saute 1 match sur 6 » : contredit.
- 3 plaintes : temps de jeu, équipe (entraînement + « trop bon pour le club »), contrat (salaire + statut) — #updates 2026-08-22, dev.
- Pénalité seulement s'il joue ; transfer-listé depuis ≥ 24 h = annulée ; blessé/suspendu n'accumule pas — #quick-questions 2026-08-17 / 2026-09-29, dev.
- Nouveau contrat : satisfaction remise à 75 % si plus basse ; attentes réinitialisées — #quick-questions 2026-09-21/22, dev.
- **Team Spirit** : leaders (≤ 10) +1 % TS, plaintes −3 % ; regulars 0, −2 % ; fringe/outsiders −1 %, −1 % ; plage 75-110 % ; TS 96 % ⇒ puissance ×0,96 à chaque action ; l'école compte (≈ −1 % par jeune) — #updates 2026-08-16/22, dev ; #quick-questions 2026-09-25 / 2026-08-19, dev.
- Visage rouge : joue sans courir, effets multiplicatifs — #italy 2025-01-13/15, dev.
- Prolongation bloquée si les 3 plaintes sont actives ou si « far above your level » — #updates 2026-08-22, dev.

## Manager, réputation, licenciement
- Réputation du manager : départ 200, converge vers celle du club, ne dépend que de la position en ligue ; aucun effet sur les matchs — #quick-questions 2026-04-02, dev ; #france 2024-12-18, dev.
- Boost : +5 par saison dans le club (max 50) + 10 % de la hausse de popularité — #updates 2025-03-31, dev.
- Offres de club : 21 jours dans le club ; on ne rejoint pas l'équipe quittée récemment — #quick-questions 2026-03-24, dev ; #general 2026-09-11, dev.
- Licenciement : un avertissement d'abord, **3 avertissements = viré**, remis à 0 si on réussit ; ~7 places sous l'attente = viré en ~4 semaines ; attente basée sur la réputation — #quick-questions 2026-09-23, dev ; #italy 2025-10-15, dev ; #updates 2024-07-15, dev.
- Manager inactif viré après ~2 semaines (« last sign in » mis à jour à chaque sauvegarde de formation) — #discussion 2024-06-29, dev ; #quick-questions 2026-06-11, dev.

## Pièges
- Plafond salarial affiché faux jusqu'au lundi après un changement de saison — #updates 2025-05-24, dev.
- Les « 12 places » de D1 (2025) et les 16 équipes de D4 ne sont pas conciliées : vérifier le nombre d'équipes de la ligue dans la base — en doute.
- Écosse : aucune relégation « for now » ; ne pas appliquer les règles de montée/descente des autres ligues sans vérification.
- Repos de pré-saison : le réglage d'entraînement précédent est mémorisé, vérifier l'intensité après la pré-saison — #quick-questions 2026-09-25, dev.
- Les notes de match montent si l'équipe gagne ; le xG affiché n'est pas la vérité du match.
- Colonnes d'écran non définies par la veille : ne pas les interpréter (voir glossaire de `connaissance.md`).
- Aucune source ne nomme « Queen of the South » : les règles propres à ce club sont à lire dans la base, pas ici.
