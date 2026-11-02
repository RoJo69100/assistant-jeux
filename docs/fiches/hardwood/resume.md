# Hardwood — résumé pour les agents (remplace attentes.md + hardwood.yaml + commun.md)

Lu par chaque agent **à la place** de `docs/attentes/attentes.md` et `docs/attentes/jeux/hardwood.yaml`. N'ouvre ces fichiers que si ta tâche touche une ligne marquée « → source ». Mis à jour dans le même commit que toute modification de ces fichiers (écrit le 2026-10-30).

## Jeu
- `hardwood`, préfixe `hw_` (bronze `game = 'hardwood'`, `source = 'dom'`). Basket universitaire, onlinecollegebasketball.org. Club **Eureka Red Devils** (#940), conférence **VI.26 (Division 3)**, région de recrutement **USA Central** (Illinois, Indiana, Missouri, Ohio, West Virginia).
- **Pas de finances, pas de transferts, pas d'infrastructures** : les leviers sont le depth chart, la tactique, le Game Management, l'entraînement, le recrutement et les coachs.
- **13 boursiers** + walk-ons. **Walk-ons [U, 2026-10-30]** : jamais exportés (pas de page joueur), jamais proposés dans le depth chart.
- Heures en Paris (`captured_at` en UTC). Match simulé à 9:00 heure du Pacifique. Sources : `[R]` manuel > `[A]` doc d'aide > `[D]` Discord ; `[U]` règle de l'utilisateur, `[H]` hypothèse. Skills `hardwood-regles`, `hardwood-recrutement`, `hardwood-tactique` ; index `outputs/hardwood/veille/connaissance.md`.

## Saison (calendrier : `gold.hw_today`, `silver.hw_schedule`)
| Phase | Quoi |
|---|---|
| 3 exhibitions | **= amicaux** : tests, minutes des jeunes ; ne comptent ni au classement ni au redshirt |
| 10 hors conférence | RPI ; ligue au sens de l'utilisateur (Game Plan de référence) |
| 30 de conférence (à partir du 01/11) | classement : top 3 monte, 6 derniers descendent |
| Playoffs de conférence, tournoi D3, Invitational | **= coupe** : même Game Plan que la ligue |
- Coaching (progression) jeudi et dimanche matin (Pacifique). Recrutement : 53 tours, un après chaque journée, +2 points, plafond 45.
- **Assistants remplaçables seulement avant la saison de conférence ou après la saison** ; un recrutement de coach par jour réel.

## Écrans (ordre de saisie)
1. **Depth Chart** : PG, SG, SF, PF, C × titulaire / 2e / 3e (le moteur remplit PG, C, PF, SF, SG ; un joueur peut doubler deux postes).
2. **Game Tactics** : Pace (−5..+5), Emphasis (I i ~ o O), Zone %, Pressure % (reste = individuelle), Extend (−5..+5), Substitution Mode (Mass, Staggered A/B/C) ; 5 ajustements de mi-temps (seul le premier déclenché s'applique).
3. **Game Management** par joueur : Green Light, Offensive Positioning, Playing Time (titulaire ≥ 15, moyen 32, redshirt 0), Foul Trouble Hook, Red Shirt.
4. Development (focus principal, secondaire, entraînements additionnels), Recruiting (contacts, offres), Coaches.

## Vues prêtes (lis-les avant de calculer ; colonnes choisies, `LIMIT`)
- **Routine** : `gold.hw_today`, `gold.hw_daily_alerts` (rouge d'abord), `gold.hw_exports_state`.
- **Effectif** : `gold.hw_effectif` (tout : compétences, poste, potentiel et plafond de SI, stats, blessure, redshirt, départ en fin de saison, progression, évaluation du scout, walk_on), `gold.hw_player_fit`, `gold.hw_player_pos_scores` (note par poste = 0,6 × compétences clés + 0,4 × SI/14 [H]).
- **Composition** : `gold.hw_depth_suggest` (proposé contre enregistré, `controle`, `walk_on_meilleur`), `silver.hw_depth_chart`, `silver.hw_tactics`, `silver.hw_management`.
- **Matchs** : `gold.hw_season_games` (tactique, efficacité par zone nous/eux, défense adverse mesurée, SI pondéré), `gold.hw_vd_compare`, `silver.hw_game_box` (fatigue, OFG).
- **Recrutement** : `gold.hw_recrues_a_ouvrir` (pages à ouvrir, 15 au moins) → `gold.hw_recrue_fiches` (note /5 actuelle et au plafond, verdict) ; `gold.hw_recruit_board` (verdict, `rang`, `besoin`), `silver.hw_recruiting`, `silver.hw_prospects`, références `silver.hw_ref_scout_phrases`, `silver.hw_ref_potential_caps`.
- **Coachs** : `gold.hw_coach_board`, `silver.hw_coaches`, `silver.hw_coach_market`.
- **Classements** : `silver.hw_standings`, `silver.hw_rankings`.

## Ordre des agents (briefs du jour `outputs/hardwood/briefs/AAAA-MM-JJ-<domaine>.md` de ceux avant toi)
Veille → Match → Effectif → Finances (coachs) → Académie (recrutement) → Entraînement → Tactique. Pas d'agent Transferts (aucun marché). Trois agents d'analyse au plus par passage ; un tableau = une vue gold, zéro agent.

## Ce que l'utilisateur attend (condensé ; → source : `docs/attentes/attentes.md`)
- **Horizon : aujourd'hui seulement**. Le match de demain se prépare aujourd'hui.
- **Rendu recrues [U]** : TOUJOURS 4 lignes, colonnes Priorité · Poste (qui part) · Cible · Remplaçant 1 · Remplaçant 2 ; sans High ; grand ≥ 2,02 m (vérifier height_m) ; recrues déjà prises retirées.
- **Rendu tactique [U]** : tableau Réglage | Actuel | À mettre dans l ordre de l écran : Pace, Inside/Outside Emphasis, Zone %, Pressure %, Extend (Man % = reste).
- **Rendu** : tableau 🟥 URGENT / 🟧 IMPORTANT / 🟩 SUIVI · catégorie · action « fais X » ; saisie complète dans l'ordre de l'écran (depth chart poste par poste, puis Game Tactics, puis Game Management joueur par joueur) ; aucun « si » ; donnée manquante = « il me manque X, fais l'export Y » ; registre `outputs/hardwood/fait-AAAA-MM-JJ.md`.
- **Décider** : chaque rendu contient un levier (recrue nommée, coach nommé, changement de poste) ou la raison chiffrée de n'en faire aucun ; défaite = analyse chiffrée contre toute la saison (`gold.hw_vd_compare`) ; conseils `C-nnn` → `L-nnn` dans `outputs/hardwood/learnings.md`.
- **Amical (exhibition)** : compo de test, pas le cinq de ligue.

## Pièges connus
- Noms abrégés (« E. Corey ») dans les stats, le depth chart et les box scores : joindre au roster par initiale + nom.
- `silver.hw_player_stats` ne compte que les matchs officiels (pas les exhibitions).
- Valeurs affichées ±20 % : une baisse affichée n'est pas une vraie baisse.
- Tables `public.hardwood_*` (hors dépôt) : fourchettes de phrases fausses, ne pas les lire ; utiliser `silver.hw_ref_*`.
- Il manque les **meilleurs joueurs des autres équipes de la ligue** : seule notre page Statistics est exportée. Pour les réunir : exporter `/statistics/<id adverse>` des adversaires de conférence (une page par équipe, au fil des matchs).
