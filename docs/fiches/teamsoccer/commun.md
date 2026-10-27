# Team Soccer — fiche commune (tous les agents)

Lue en premier par chaque agent, avant la fiche de son domaine (`docs/fiches/teamsoccer/<agent>.md`). Rédigée le 2026-10-19. Les règles changent souvent (20 annonces de l'admin entre août et octobre 2026) : en cas de doute, la veille passe d'abord.

## Identité
- Identifiant : `teamsoccer` (bronze : `game = 'teamsoccer'` ; vues `silver.ts_*`, `gold.ts_*`). Football, teamsoccer.org. Monnaie : $.
- **Deux clubs, deux économies séparées** — toujours préciser lequel, et traiter les deux si la demande ne dit rien :
  - `team_id = 18` **Chomelix Cows** (équipe première), Division I, série 119.
  - `team_id = 15858` **Ben Ahmed Donkey** (équipe féminine, Women's TS League, liée au Premium), Division III, série 1956.
- Zones de poste : GB, DEF, MIL, ATT (`position` de l'API : GK / DEF / MID / FWD). Le sous-rôle (DC, LAT, WB, MD, MC, ML, MO, AC, DR) se lit avec le tableau du skill joueurs ; `second_skill` n'en est qu'un indice.
- **La Forme** (`forme`, 0–100, colonne `fitness` de l'API) multiplie chaque action par 0,70 + 0,30 × Forme / 100 [F:2026-06-27 Admin-Dev]. Elle ne bouge qu'à l'entraînement du vendredi. C'est l'arbitrage central du jeu.

## Sources et codes de citation
- `[G:Rubrique]` guide officiel > `[F:date pseudo]` forum (Admin-Dev = le développeur, Admin-PIPO68 = l'administrateur ; les autres = avis) > `[P:Page]` écran du jeu > `[Obs]` nos données (`[Obs SQL date]`).
- Skills : `.claude/skills/teamsoccer-joueurs|match|entrainement|club|saison|communaute/SKILL.md` (validés par l'utilisateur le 2026-10-19). Pas de Discord.

## Rythme (skill teamsoccer-saison)
- Saison de 9 semaines : ligue de 8, 14 journées (semaines 1 à 7), barrages en semaine 8, repos en semaine 9. Saison 3 en cours : ligue du 2026-10-12 au 2026-11-28 (`gold.ts_season_calendar`).
- Ligue : Chomelix Cows le **mardi et le samedi 13:50** (Paris), Ben Ahmed Donkey le **lundi et le jeudi 19:30** (`gold.ts_upcoming`). Coupes en semaine.
- **Vendredi** : entraînement (et Forme). **Lundi 00:05** (heure du site) : finances de la semaine. **Chaque jour** : 3 révélations d'académie par club.
- **Composition à enregistrer au moins 2 h avant le coup d'envoi** (match pré-calculé) [skill teamsoccer-match] : `gold.ts_upcoming.lineup_deadline_paris`.
- Un match de 13:50 se prépare **la veille** (composition enregistrée 2 h avant au plus tard).

## Pièges communs
- L'API renvoie des réponses partielles ; les vues silver fusionnent la dernière valeur de chaque colonne. Vérifie toujours `as_of` / `day` et demande l'export s'il est périmé.
- Certaines valeurs sont des libellés au lieu de nombres (`coach_level_label` = « poor », `team_spirit_label` = « Normal », `form_label` = « Good » ou « 5 »).
- Solde négatif : pas de faillite, mais ni achat, ni stade, ni entraîneur [skill teamsoccer-club].
- Bots : compétences ×0,90 et Gardien/Finition encore réduits ; ils perdent plus de 90 % de leurs matchs [skill teamsoccer-match].

## État des données (2026-10-19)
- Silver (`sql/silver/012_ts_base.sql`) : `ts_api`, `ts_me`, `ts_teams`, `ts_my_teams`, `ts_player_snapshots`, `ts_players`, `ts_training`, `ts_finances`, `ts_stadiums`, `ts_matches`, `ts_match_lineups`, `ts_lineups`, `ts_standings` (recalculé depuis les matchs), `ts_transfer_listings`, `ts_my_bids`, `ts_youth_academies`, `ts_youth_players`, `ts_hpc`, `ts_news`, `ts_forum_posts`.
- Gold (`sql/gold/016_ts_gold.sql`) : `ts_season_calendar`, `ts_squad_report`, `ts_player_progress`, `ts_finance_status`, `ts_stadium_payback`, `ts_academy`, `ts_hpc_status`, `ts_upcoming`.
- Pas encore captés : notes des joueurs et rapport détaillé des matchs (checklist B4), cercles de constance du manager (B6). Un seul relevé des joueurs (2026-10-19) : `ts_player_progress` sera vide jusqu'au prochain export après le vendredi.

## Ordre des agents et briefs du jour (règle du 2026-10-22)
Un agent ne rend jamais un retour incomplet parce qu'un autre agent n'est pas encore passé. Ordre : Veille (si nouvelle source) → Match → Effectif → Finances-personnel → Académie → Entraînement → Tactique → Transferts (dernier). Chaque agent lit d'abord les briefs du jour (`outputs/teamsoccer/briefs/AAAA-MM-JJ-<domaine>.md`) des agents placés avant lui ; seuls les agents sans dépendance entre eux tournent en parallèle. Avant d'écrire « donnée non relevée », cherche dans ces briefs ; sinon, dis quel export manque en tête du résumé. Un agent en aval qui contredit un agent en amont l'écrit en tête de son résumé (relance à faire).

## Sorties
- Briefs : `outputs/teamsoccer/briefs/AAAA-MM-JJ-<domaine>.md` (une section par club).
- Journal : `outputs/teamsoccer/learnings.md` (enseignements `L-nnn`, conseils `C-nnn`) ; à créer au premier match analysé, sur le modèle de `outputs/basketvibe/learnings.md`.
- Veille : `outputs/teamsoccer/veille/`.

## Options observées (lecteur-exports, 2026-10-25)
- Champs bruts non lus par silver, effet inconnu (à tester, mesure = résultat des révélations / matchs) : `login_streak` (19 le 2026-10-25), `daily_reveal_count` / `fully_revealed_count` (académie 376 : 15 jeunes entièrement révélés), `eliminated_in_round` (coupe), `reward` / `page_key` (récompense « foros »).
- POST de révélation d'académie (`skill_name`, `skill_value`, `daily_reveal_count`) : en bronze (`dashboard_youth-scout`), non lus par silver ; max 3 jeunes distincts par club et par jour, reset 01:00 UTC.
- Aucun `<select>` / `<option>` dans les HTML du marché et de l'académie.
- 2026-10-27 : champs bruts non lus, effet inconnu (mesure = résultat de match / Forme) : `is_admin_match` (Ajax–Cows 2080875 = true, `competition` inconnue dans silver), `is_promotion`, `time_changed`, `room_challenge_id`, `custom_tournament_id`, `team_morale` (75), `team_spirit` (Normal), `shirt_color`, `name_changed`, `hotlists`, `season_yellow_cards`, `injured_at`.
- Une composition de match n'arrive en base que par l'export de la page composition / match ; `dashboard_squad` n'en contient pas.
