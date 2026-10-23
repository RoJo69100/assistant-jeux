# Hockey Nation — fiche commune (tous les agents)

Lue en premier par chaque agent, avant la fiche de son domaine (`docs/fiches/hockeynation/<agent>.md`). Rédigée le 2026-10-23.

## Identité
- Identifiant : `hockeynation` (bronze : `game = 'hockeynation'` ; vues `silver.hn_*`, `gold.hn_*`). Hockey sur glace.
- Notre club : 4 équipes, PRO, FRM, U21, U17 (`silver.hn_my_teams`). Saison 26, phase post au 2026-10-23 ; saison = 63 jours (`gold.hn_calendar`).
- Contexte et vision de l'utilisateur : `data/contexte/HN_contexte.txt` (line-up très jeune, vendre les vieux, bien drafter, juger échanges et extensions, étude des adversaires).
- Postes : C, LW, RW, LD, RD, G ; certains joueurs ont 2 postes (principal + secondaire).

## Règles propres au jeu (à appliquer dans chaque livrable)
- **Talents d'abord** [règle de l'utilisateur, 2026-10-23] : tout joueur se juge sur ses talents fort/faible contre son poste (`gold.hn_player_fit`, `gold.hn_draft_board` : idéal / correct / contre-emploi), puis sa note, ses plafonds, ses spéciales, ses stats. Un ailier aux talents DEF + CHK ne nous intéresse pas.
- **Double poste** : intéressant ; dire à quel poste les talents collent (ex. Blednov : correct au centre, contre-emploi à l'aile).
- Plafond salarial : jamais de cap space négatif (−30 % en match, faillite) ; toute idée d'échange ou d'extension donne son effet sur `gold.hn_cap_outlook`.
- Ce qui est réglable dépend de l'équipe (skill hockeynation-joueurs § Les 4 équipes) : pas d'entraînement réglable en U21/U17, lignes auto hors PRO.

## Sources et codes de citation
- `[G:Rubrique]` guide officiel (30/09/2026) > `[Discord, salon, date]` (#general, #events, #trade, #france, #game-tools ; 154 464 messages importés, `bronze.discord_messages`) > `[Obs]` nos observations. `[U]` = règle de l'utilisateur. `[H]` = hypothèse.
- Skills : `.claude/skills/hockeynation-joueurs|coachs-entrainement|contrats-finances|draft-scouting|match-calendrier|adversaires/SKILL.md`.

## État des données (2026-10-23)
- Silver (`sql/silver/015_hn_base.sql`) : `hn_api`, `hn_season`, `hn_nations`, `hn_my_teams`, `hn_skill()`, `hn_player_snapshots`, `hn_players`, `hn_finances`, `hn_expiring`, `hn_coaches`, `hn_free_coaches`, `hn_training_log`, `hn_lineups`, `hn_games`, `hn_game_detail`, `hn_standings`, `hn_trades`, `hn_market_players`, `hn_draft_class`, `hn_draft_picks`, `hn_scouts`, `hn_scouting_budget`.
- Gold (`sql/gold/019_hn_gold.sql`) : `hn_position_keys`, `hn_player_fit`, `hn_draft_board`, `hn_cap_outlook`, `hn_coach_board`, `hn_calendar`, `hn_daily_alerts`.
- Manques connus (`outputs/hockeynation/exports-a-faire.md`) : lignes FRM/U21/U17 (automatiques), fiches détaillées des coachs, fiche contrat d'un joueur, adversaires. Toujours vérifier `day` / `as_of`.

## Ordre des agents et briefs du jour
Veille (si nouvelle source) → Match → Effectif → Finances-personnel (contrats, plafond, coachs, scouts) → Académie (draft, U17, U21) → Entraînement → Tactique → Transferts (dernier). Chaque agent lit les briefs du jour (`outputs/hockeynation/briefs/AAAA-MM-JJ-<domaine>.md`) des agents placés avant lui et le registre `outputs/hockeynation/fait-AAAA-MM-JJ.md`. Un agent en aval qui contredit un agent en amont l'écrit en tête de son résumé.

## Sorties
- Briefs : `outputs/hockeynation/briefs/AAAA-MM-JJ-<domaine>.md`. Journal : `outputs/hockeynation/learnings.md` (C-nnn, L-nnn), créé au premier match analysé. Veille : `outputs/hockeynation/veille/`.
- Couleurs : 🟥 URGENT, 🟧 IMPORTANT, 🟩 SUIVI devant chaque action ; verdict nommé, joueur par joueur.

## Lignes des équipes que le GM ne gère pas (consigne du 2026-10-23)
- Le GM ne règle les lignes que de la PRO. Pour les autres équipes (FRM, U21, U17 et adversaires), la composition idéale est **4 LW / 4 RW / 4 C / 2 LD / 2 RD / 2 G** : elle dit quel joueur joue. Lezno Bulls (meilleure équipe du jeu, très loin devant) sert d'équipe de référence.
- Il n'y a pas de fiche contrat : le contrat d'un joueur est dans la partie Contract de sa fiche.
- Un coach se juge sur ses compétences spéciales (ex. Pavel Vasak, marché : Commander, Master Agitator) : lire le bonus exact avant un recrutement ou un échange.

## Négociations de fin de saison (consigne du 2026-10-23)
- Seuls les contrats de l'équipe PRO comptent pour le plafond ; un contrat FRM n'a aucun impact.
- Un joueur FRM en négociation (page contract-talks-farm-players : ex. Vollmer, 1 560 000 $ sur 5 ans) **part de l'équipe si le GM ne fait rien** ; les autres joueurs FRM n'ont pas besoin de négociation pour rester.
- Les U21 en négociation montent en FRM ou en PRO selon le choix du GM ; les U17 montent en U21. À vérifier dans le guide (U21 Team / Farm Team).
- Les négociations ouvrent le jour 1 de la saison et sont validées vers le jour 4 ou 5 (déclaré par l'utilisateur, non vérifié).
- « Contre-emploi » (gold.hn_player_fit) = aucun des 2 talents forts du joueur n'est une compétence clé de son poste (hypothèse de `gold.hn_position_keys`, non confirmée par le jeu).
