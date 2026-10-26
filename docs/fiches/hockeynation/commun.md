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

## Options observées (lecteur d'exports, 2026-10-25)
| Nouveauté | Où | Valeur actuelle | Effet |
|---|---|---|---|
| Saison 27 phase `regular` | `season-current`, `season-phase` | 27 / regular (depuis ~09:22 UTC) | Fenêtres de la fiche (« fermées jusqu'au jour 1 S27 ») à réviser : agents libres open jusqu'au 2026-11-28 20:00 UTC |
| Fenêtre échanges | `trade-center/trade-window` | timestamp 2026-11-28 20:00 UTC | sens à confirmer (fin de fenêtre ?) |
| Statut de prolongation | `player/<id>/contract-extension-talks`, `new-extension-offer` | Bélanger : 3 ans, 1 870 000, mood happy, `waiting_for_gm` / `waiting_for_agent` | effet inconnu : à tester une option à la fois, mesure = réponse de l'agent après contre-offre |
| Humeur du joueur | même endpoint | `happy` | effet inconnu |
| Scouting : assignations | `scouting-assignments` | 2 missions (duration 1 et 2 jours) | effet inconnu : mesure = scouted_times de la classe |
| Candidatures scouts / coachs | `office/scout-applications`, `coach-applications` | canHire true | recrutement possible |
| Position limits / pick preferences | `draft-center/draft-position-limits`, `draft-pick-preferences` | 5 picks, ordre inconnu, tirage 2026-12-26 20:00 | effet inconnu |
| Puck / raffle | `puck-overview`, `raffle-event-result` | solde 1 204 pucks, tirage 2026-10-25 20:00 UTC | hors gestion de club |
| Staff PRO | `hn_club_staff` | head coach Byström (41, sans spécial) | Aalst parti, à évaluer par Finances/Entraînement |
| Silver : pièges (corrigés le 2026-10-25, `sql/silver/021`, `sql/gold/021`) | `hn_players` = dernier roster de chaque équipe seulement (absents dans `hn_players_gone`) ; `hn_draft_class.season` et `gold.hn_draft_board.season` (filtrer la saison de la draft) ; `gold.hn_cap_outlook` commence à la saison en cours | — | — |
| Nouvelles vues (2026-10-25) | `silver.hn_extension_offers`, `hn_scouting_assignments`, `hn_scout_applications`, `hn_coach_applications`, `hn_league_team_ratings` | — | Coach Center : le script 0.2.0 signale les pages manquantes (bouton rouge ⚠) |

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
- Correction du 2026-10-23 (agent Académie, sources [G:U21 Team], [G:Farm Team], [G:Teams]) : il n'y a pas de négociation en U21. Le GM signe un ELC PRO (après la fenêtre I) ou un contrat Farm (à 21 ans seulement, effet à 22 ans) ; un U21 non signé part à 22 ans. La négociation existe pour les FRM de 25 ans et plus. Les draftés et les 2 U17 non draftables arrivent en U21 à 18 ans ; un U17 draftable est pris par un autre club.
- Le calendrier « négociations ouvertes le jour 1, validées jours 4-5 » (dit par l'utilisateur) est introuvable dans le guide : non vérifié.
- « Contre-emploi » (gold.hn_player_fit) = aucun des 2 talents forts du joueur n'est une compétence clé de son poste (hypothèse de `gold.hn_position_keys`, non confirmée par le jeu).

## Précisions de l'utilisateur du 2026-10-23 (soir)
- Négociation FRM : la demande de contrat (ex. Vollmer, 1,56 M$ sur 5 ans) n'est qu'une étape pour décider de garder ou non un joueur FRM. Pour renvoyer un FRM, le seul moyen est de négocier avec lui puis de ne pas le prolonger : il part. Un FRM en négociation dont le GM ne répond pas ne part pas (il reste, comme les autres FRM).
- Finances : aucune évolution dans le temps ; seul compte le cap space à respecter avec les salaires PRO.
- Stan Aalst (head coach PRO) prend sa retraite en début de saison S27.
- Vocabulaire : ne pas dire « vendre » pour un échange ; dire « échanger ». Échanger Hateboer et Jaworski dégrade la ligne : toujours vérifier la ligne avant/après.
- Scouts : à recruter ensemble en début de saison, selon la classe de draft.
- Toujours raisonner en **20 joueurs par équipe : 4 C / 4 LW / 4 RW / 3 LD / 3 RD / 2 G** (3 paires de défenseurs ; correction du 2026-10-23, remplace « 2 LD / 2 RD »). Lignes complètes pour PRO, FRM, U21, U17.

## Fenêtres (2026-10-23)
- Les échanges et les montées FRM→PRO sont fermés jusqu'au **jour 1 de S27** : ne jamais mettre en « aujourd'hui » une action qui dépend d'une fenêtre fermée ou d'un état S27 (lineup avec Nokelainen, Hateboer, Jaworski ; échanges Pålsson, Munk, Carpentier, Hongisto). Le plan B d'entraînement attend l'embauche des coachs.
- Les 4 clubs étudiés (Leszno, Seoul, Miami, Jessup) sont dans l'autre ligue : **équipes de comparaison seulement** [U, 2026-10-25] ; ne jamais leur proposer d'échange. Les partenaires d'échange viennent du Trade Center (export à jour).
- **Jugement d'un joueur** [U, 2026-10-25] : jamais la note seule, ni « meilleur de l'équipe ». Dire s'il est fort et s'il peut le devenir, d'après ses compétences spéciales, l'importance de ses compétences dans la ligne (rôle, unités PP/PK, endurance) et la cohésion avec ses coéquipiers de ligne. Aucune règle de cohésion n'est documentée (guide, Discord) : travailler par compléments de talents (passeur + tireur) et par spéciales collectives (Team Player, Telepathy…), en hypothèse testable.
- **Montées d'U21** [U, 2026-10-25] : un U21 peut être monté en FRM ou en PRO à tout âge ; il monte automatiquement à 21 ans.

## Consignes tactique (2026-10-23, après la v1)
- **Aucun nouveau joueur dans une lineup** : on n'en reçoit que par agent libre ou échange (difficile, non garanti). Une lineup se bâtit sur nos joueurs actuels moins ceux qui partent (contrat fini non prolongé, échange voulu, draft). Les cibles d'échange vont dans un tableau séparé, jamais dans la lineup. Ne pas parler de Baier ; Mráz et Jenko ne servent que de cible d'échange.
- Montées en PRO : candidats du **FRM et de l'U21** (U21 : pas de négociation, ELC actif la saison suivante).
- Équipes spéciales à saisir : PP1, PP2, PK1, PK2, PK 3 hommes 1 et 2, 4 contre 4 L1 et L2 (un joueur une fois par type).
- Coach pick order : liste ordonnée pour chaque équipe (PRO, FRM, U21, U17).
- Endurance : seuils Discord (talonflame1, 2026-04-04) L1 7+, L2 6+, D1 8+, D2 6+, G1 7+, tolérés à −1 ; le temps de glace est fixé par la ligne, l'END fait baisser la condition.
