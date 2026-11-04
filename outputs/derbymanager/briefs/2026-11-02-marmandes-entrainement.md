# Marmandes (307) — Entraînement, début de saison — 2026-11-02

Base : exports 307 du 2026-11-02 21:59 UTC (`silver.dm_training`, `silver.dm_training_groups`, `silver.dm_facilities`, `gold.dm_verdict_joueurs`, `gold.dm_entrainement_plan`). Les briefs du 31/10 sont périmés et ne sont pas utilisés. Police : à passer avant rendu (obligatoire, non lancée par moi).

## Fiche de saisie — écran Training (à faire aujourd'hui)
| Priorité | Groupe | Actuel | Fais | Base |
|---|---|---|---|---|
| 🟥 URGENT | DEF | Marking | **Anticipation** | `dm_entrainement_plan` : Anticipation 7,5 (la plus basse, niveau Decisions = 3, écart 4,5) ; Marking 15,7 déjà haut |
| 🟥 URGENT | MID | Passing | **Anticipation** | Technique et Anticipation à égalité 8,4 (Decisions = 3, écart 5,4) ; départage Anticipation : le choix 307 de la carte var. 11, [H] |
| 🟥 URGENT | FWD | Shooting | **Agility** | Agility 10,4 (Movement = 4, écart 6,4) contre Accuracy 11,6 (Decisions = 5, écart 6,6) ; Shooting 12,6 |
| 🟩 SUIVI | GK | Aerial | **garder Aerial** | Aerial 11,0 (Movement = 4, écart 6,5) contre Reaction 10,0 (Tactic = 1, écart 9) ; carte var. 11 |
Règle [H] de la carte var. 11 : écart le plus petit parmi les compétences basses (sources : dev 2025-06-29 P×(F+C), 2025-07-02 optimum niveau = compétence, connaissance § 5). Niveaux de groupe : tec 1 partout, dec 3 (FWD 5), mov 4 (`silver.dm_training_groups`). Installations niveau 14, « Local » (`silver.dm_facilities`), upgrade à 7 M : cela explique tec 1.

## Intensité joueur par joueur
**Il me manque l'état réel de l'écran : `intensity` est nul pour 20/20 en base (cherché dans : `silver.dm_training`, `gold.dm_verdict_joueurs`, `gold.dm_entrainement`).** Même cause que la carte var. 13 (pill « REST » entre saisons) ; sur 547 l'utilisateur a noté ce soir que l'intensité n'est pas modifiable en début de saison. Fais : essaie de saisir les valeurs ci-dessous ; si l'écran refuse, ne force rien et dis-le (je l'enregistre).
Règle : Low 50 % (+4 % récup.), Med 100 % (+3 %), High 150 % (+2 %) — dev 2025-10-15 (connaissance § 5). Valeurs = `intensite_conseillee` de la vue (logique du calcul de la vue non relue : [H]). Tous en condition 100, forme 0, TR atteint (`ne_s_entraine_pas` faux pour tous).

| Groupe | HIGH | MED | LOW |
|---|---|---|---|
| GK | N. Lafleur (20, pot 3), M. Comonfort (19, pot 3) | — | — |
| DEF | B. Desagnat (19, pot 3), M. Schmitz (19, pot 3), A. Labourd (18), H. Hardt (17, pot 3) | Y. Messimy (25), S. La Ferrière (26) | — |
| MID | N. Taddei (20, pot 3), C. Lévêque (20), C. Lerch (21), F. Bodian (23), C. Toussaint (18) | B. Cave (21, pot 0), C. Cleary (28, pot 0) | — |
| FWD | B. Vasilev (23), G. Luzerne (18, pot 3) | A. McCulloch (25), A. Vargas (25) | B. Ohara (31, pot 1, mentor) |
Base : `gold.dm_verdict_joueurs.intensite_conseillee` (jeunes pot 3 = HIGH ; pot 0 ou vieux = MED/LOW). Pot 0 : Cave et Cleary ne progressent pas, MED suffit.

## Points à connaître
- Contrats : Desagnat et McCulloch n'ont plus que 2 jours (`contract_days`) ; Lafleur 17 j, Lerch 19 j. Entraîner HIGH un joueur qui part est perdu : décision de prolongation hors périmètre de cet agent.
- Vasilev (Key) : temps de jeu satisfait 0 % pour 75 % attendus (`dm_verdict_joueurs`) : à aligner demain ; sans minutes (TR 4 j) il ne s'entraîne pas pleinement (dev 2026-10-25).
- Surplus FWD : Vargas, Ohara (verdict « vendre »). Ohara est le mentor (F decisions, carte var. 12) : le vendre retire ~+2 à dec FWD.
- Jeunes « amical + banc DEV » (Hardt, Luzerne, Comonfort, Lerch, Toussaint) : un jeune qui ne joue pas ne progresse pas (dev 2026-10-25) → les faire jouer à l'amical de demain, sinon HIGH est inutile.
- Gains/pertes : 0/0 pour 20/20 (début de saison), aucun verdict de gain possible. Premier contrôle : 2026-11-09.

## Ce qui prouvera que j'avais tort
- DEF Anticipation / MID Anticipation / FWD Agility : si la somme `gained` du groupe au 2026-11-09 (`gold.dm_entrainement where team_id=307`) n'est pas supérieure à la perte `lost`, ou si la compétence visée n'a pas bougé, revenir à la compétence la plus basse suivante (DEF Positioning, FWD Accuracy).
- Intensités : un jeune HIGH sans minutes jouées au 2026-11-09 (`jours_sans_match` > `tr_exigence`) → passer MED.

## Conseils à ajouter dans learnings (non écrits, pas de commit demandé)
- C-011 (2026-11-02) : 307 D → Anticipation, M → Anticipation, F → Agility, GK → Aerial ; critère : `select groupe, entrainement_groupe, sum(gained), sum(lost) from gold.dm_entrainement where team_id=307 group by 1,2` au 2026-11-09 ; C-007 (réglages 547 du 31/10, hypothèse) ne vise pas 307.
