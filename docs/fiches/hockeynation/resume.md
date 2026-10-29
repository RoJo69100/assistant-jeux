# Hockey Nation — résumé pour les agents (remplace attentes.md + hockeynation.yaml + commun.md)

Lu par chaque agent **à la place** de `docs/attentes/attentes.md`, `docs/attentes/jeux/hockeynation.yaml` et `docs/fiches/hockeynation/commun.md`. N'ouvre ces trois fichiers que si ta tâche touche une ligne marquée « → source ». Mis à jour dans le même commit que toute modification de ces trois fichiers (écrit le 2026-10-29).

## Jeu
- `hockeynation`, préfixe `hn_` (bronze `game = 'hockeynation'`). Club **Chomelix Cows**, 4 équipes : **PRO** (lignes, unités spéciales, entraînement, échanges, contrats, coachs, scouts, draft), **FRM** (poste principal, entraînement, négociation des 25 ans et plus), **U21** (montée, ELC ou contrat Farm à 21 ans), **U17** (poste principal). Lignes FRM/U21/U17 automatiques (`gold.hn_depth_chart`).
- Toujours **20 joueurs par équipe : 4 C / 4 LW / 4 RW / 3 LD / 3 RD / 2 G**, un bloc par équipe dans chaque rendu. Tout ajout de joueur = équipe résultante à 20 (talents vs poste, VIDE).
- Ligue de 20 (2 conférences, 4 niveaux), 30 matchs, playoffs au meilleur des 5. Résultat = `silver.hn_games` côté `*_is_mine`, jamais le score brut.
- Heures en Paris (`captured_at` en UTC). Sources : `[G:Rubrique]` guide > `[Discord, salon, date]` > `[Obs]` ; `[U]` règle de l'utilisateur, `[H]` hypothèse. Skills `hockeynation-*`.

## Saison 27 (calendrier : `gold.hn_today`, `gold.hn_calendar`)
| Jour | Date | Quoi |
|---|---|---|
| 1 | 25/10 | début S27, fenêtre I et agents libres ouverts |
| 4 | 28/10 | début des missions de scouting |
| 8 | 01/11 | 1er match de ligue, 1re paie (un départ avant la paie libère 100 % du salaire) |
| 35 | 28/11 21:00 | fermeture fenêtre I : effectifs gelés, dernières embauches de coachs |
| 42 / 44 | 05/12 / 07/12 | dernière journée / playoffs |
| 49–54 | 12/12–17/12 | Import Draft |
| 63 | 26/12 21:00 | draft (pré-instructions 1 h avant) |
- Un échange passe un comité de 21 votants (≈ 24 h) puis la mise à jour quotidienne : compter 2 à 3 jours.

## Règles propres au jeu
- **Talents d'abord** [U] : un joueur se juge sur ses talents forts/faible contre son poste (`gold.hn_player_fit` : idéal / correct / contre-emploi, hypothèse `gold.hn_position_keys`), puis spéciales, rôle dans la ligne (PP/PK, END), plafonds, note, stats. Jamais la note seule.
- **Plafond** : seuls les contrats PRO comptent ; cap space jamais négatif (−30 % en match). Tout échange, signature ou prolongation donne l'effet avant/après sur `silver.hn_cap_now` et `gold.hn_cap_outlook`.
- **Pénalités** : joueur hors poste −20 % ; case vide ou joueur parti = amateur, −5 % d'équipe chacun.
- **Endurance** (Discord talonflame1, 04/04/2026) : L1 7+, L2 6+, D1 8+, D2 6+, G1 7+, tolérés à −1.
- **FRM** : un FRM sans négociation reste ; ouvrir une négociation sans prolonger = il part. **U21** : pas de négociation ; ELC PRO ou Farm à 21 ans, sinon départ à 22 ans.
- **Échanges** : dire « échanger », jamais « vendre ». Partenaires = Trade Center ; jamais Leszno, Seoul, Miami, Jessup (comparaison seulement). Aucun nouveau joueur dans une lineup avant son arrivée : les cibles vont dans un tableau à part.
- **Coachs** : head compte double ; jugés sur les compétences de match (OFP DFP BAT PP PK) et leurs spéciales ; retraite à 65 ans.

## Écrans (ordre de saisie)
- Lineups PRO A, B, C : L1–L4 (LW, C, RW), paires D1–D3 (LD, RD), G (titulaire, remplaçant), PP1, PP2, PK1, PK2, PK 3 hommes 1–2, 4 contre 4 L1–L2, EXT. Un joueur une seule fois par type d'unité.
- Plan de jeu : tempo, mentalité, agressivité, retrait du gardien, durée des présences, pression (libellés des échelles encore à lire).
- Coach pick order par équipe ; Training PRO / FRM : compétence + coach par joueur.

## Vues prêtes (lis-les avant de calculer toi-même ; colonnes choisies, `LIMIT`)
- **Routine** : `gold.hn_today` (jour de saison), `gold.hn_daily_alerts` (rouge d'abord), `gold.hn_exports_state` (fraîcheur de chaque export, statut 🟩/🟧/🟥).
- **Saisie** : `gold.hn_saisie_lignes` (lignes enregistrées, `order by lineup, ordre`, colonne `controle` : joueur parti, hors poste).
- **Effectif et marché** : `silver.hn_players` (dernier roster ; partis dans `hn_players_gone`), `gold.hn_player_fit`, `gold.hn_depth_chart`, `silver.hn_trade_offers` (offres reçues / envoyées en cours), `silver.hn_market_players`, `gold.hn_trade_value`, `gold.hn_league_player_fit`, `gold.hn_club_compare`.
- **Argent et staff** : `silver.hn_cap_now`, `gold.hn_cap_outlook`, `silver.hn_expiring`, `silver.hn_extension_offers`, `gold.hn_coach_board`, `gold.hn_coach_specials`, `silver.hn_club_staff`, `silver.hn_coach_applications`.
- **Draft** : `gold.hn_draft_board` (filtrer la saison), `silver.hn_draft_picks`, `silver.hn_scouts`, `silver.hn_scouting_budget`, `silver.hn_scouting_assignments`, `silver.hn_scout_applications`.
- **Matchs** : `silver.hn_games`, `silver.hn_game_detail`, `silver.hn_standings`.

## Ordre des agents (tu lis les briefs du jour `outputs/hockeynation/briefs/AAAA-MM-JJ-<domaine>.md` de ceux avant toi)
Veille → Match → Effectif → Finances-personnel → Académie → Entraînement → Tactique → Transferts. Un agent en aval qui contredit un agent en amont l'écrit en tête de son résumé. Trois agents d'analyse au plus par passage.

## Ce que l'utilisateur attend (condensé ; → source : `docs/attentes/attentes.md`)
- **Horizon : aujourd'hui seulement**. Toute action se fait aujourd'hui ; un match de demain se prépare aujourd'hui ; une échéance lointaine se règle maintenant ou n'est pas mentionnée.
- **Rendu** : tableau 🟥 URGENT / 🟧 IMPORTANT / 🟩 SUIVI · catégorie · action « fais X » (joueur, valeur) ; saisie complète dans l'ordre de l'écran ; aucun « si », aucun seuil générique ; donnée manquante = « il me manque X, fais l'export Y » ; ne jamais redemander ce que `outputs/hockeynation/fait-AAAA-MM-JJ.md` ou la base prouvent ; une décision, le doute en une demi-ligne avec ce qui prouvera l'erreur ; tout chiffre vérifié en base.
- **Décider** : chaque rendu contient un levier (échange nommé, montée, signature) ou la raison chiffrée de n'en faire aucun ; série de défaites = changement fort ; défaite = analyse chiffrée contre toute la saison ; conseils `C-nnn` → `L-nnn` dans `outputs/hockeynation/learnings.md`.
- **Coût** : brief d'une page, résumé de 10 lignes, delta du jour seulement.

## Pièges connus
- `silver.hn_trades` = échanges **conclus** de la ligue (Trade Tracker) ; nos offres en cours sont dans `silver.hn_trade_offers` (dernier export seulement).
- `hn_scouts` / `hn_scouting_budget` ne bougent que si l'utilisateur exporte Scouting : regarder la date du relevé avant d'écrire « 2 scouts ».
- `gold.hn_today.day1` se déduit de la fermeture de la fenêtre I (jour 35) : à revoir à l'ouverture de la fenêtre II (jour 51).
- Lignes enregistrées : un `player_id` sans nom = joueur parti (le jeu met un amateur).
