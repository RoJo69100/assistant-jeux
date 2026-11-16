# Pages reçues depuis 30 jours et non lues par une vue silver (état du 16/11/2026)

Source : `gold.couverture_pages`, alerte « page reçue, non lue », les 25 types les plus fréquents par jeu. Aucune valeur de payload lue : seulement les clés de premier niveau de la dernière capture du type.
Registre : `core.page_reader` semé le 16/11 depuis les littéraux (route ou `page_type`) des vues silver de chaque jeu (`sql/core/031`).
**Limite connue** : une vue qui lit une page par motif d'URL, par texte ou par filtre non littéral n'est pas détectée. Les types `dom:` de DerbyManager, Hardwood et Team Soccer (ex. `dom:teams_id_squad-tab`, `dom:dashboard_squad`) sont probablement lus à tort « non lus ». À confirmer au tri.
Pour ignorer exprès : `insert into core.page_ignore (game, motif, raison) values ('<jeu>', '^<regex du type>$', '<raison>')`. Rien n'est décidé ici.

Bilan après les lecteurs gold de l'étape 4 (types avec décision / types reçus ; captures avec décision / captures ; décision = lecteur silver ou gold, ou motif ignoré exprès, aucun ignoré pour l'instant) : basketvibe 34/128 ; 1641/3241 · derbymanager 27/47 ; 250/426 · hardwood 12/38 ; 829/923 · hockeynation 39/216 ; 996/3260 · sixzeroleague 17/60 ; 464/1474 · teamsoccer 20/112 ; 2212/3205.
Les tableaux ci-dessous datent d'avant l'étape 4 : ne sont plus « non lus » les `setpiece` de DerbyManager, `dom:players_id`, `dom:schedule_id` (Hardwood), `/api/infrastructure/mine` et `/api/teams/mine/transfers` (SixZero League), `dom:dashboard_match-viewer_id` (Team Soccer).

Clés (premier niveau de la charge utile) :
- **A** DM dom : `club, club_from, club_name, fields, html, tables, team_id, text, title`
- **B** DM api : `body, club, club_from, club_name, method, status, team_id`, puis les clés de `body`
- **C** HW dom : `fields, html, tables, text, title`
- **D** HN/SZ/TS dom : `html, tables, text, title`
- **E** HN/SZ/TS api : `body, method, status`, puis les clés de `body` (vide = `body` non objet)

## derbymanager

| type de page | n | dernier | clés |
|---|---:|---|---|
| `dom:players_id` | 51 | 06/11 | A |
| `dom:teams_id_squad-tab` | 36 | 06/11 | A |
| `dom:teams_id_overview-tab` | 26 | 06/11 | A |
| `dom:matches_id_end-tab` | 20 | 06/11 | A |
| `dom:teams_id_news-tab` | 19 | 06/11 | A |
| `dom:teams_id_training-tab` | 19 | 06/11 | A |
| `dom:players_id_contract` | 14 | 06/11 | A |
| `/players/<n>/setpiece/attack/box` | 8 | 03/11 | B ; body: alert, value |
| `dom:news` | 8 | 06/11 | A |
| `/players/<n>/setpiece/defence/box` | 7 | 03/11 | B ; body: alert, value |
| `dom:managers_id` | 6 | 03/11 | A |
| `dom:teams_id_matches` | 6 | 06/11 | A |
| `/players/<n>/setpiece/defence/default` | 5 | 02/11 | B ; body: alert, value |
| `/players/<n>/setpiece/fk/default` | 5 | 03/11 | B ; body: alert, value |
| `/players/<n>/setpiece/sub/development` | 5 | 03/11 | B ; body: alert, value |
| `/players/<n>/setpiece/attack/default` | 4 | 02/11 | B ; body: alert, value |
| `/players/<n>/setpiece/captain/default` | 3 | 03/11 | B ; body: alert, value |
| `/players/<n>/setpiece/pen/default` | 3 | 03/11 | B ; body: alert, value |
| `/players/<n>/setpiece/sub/rating` | 3 | 03/11 | B ; body: alert, value |
| `/teams/<n>/matches.json` | 3 | 06/11 | B ; body: fallback, matches, season, team, territory, v… |
| `dom:teams_id_development` | 3 | 01/11 | A |
| `/managers/messages/seen` | 2 | 30/10 | B ; body: alert |
| `/players/<n>/setpiece/corner/default` | 2 | 03/11 | B ; body: alert, value |
| `/players/<n>/setpiece/corner/priority` | 2 | 03/11 | B ; body: alert, value |
| `/players/<n>/setpiece/fk/priority` | 2 | 03/11 | B ; body: alert, value |

## hardwood (25 premiers sur 27)

| type de page | n | dernier | clés |
|---|---:|---|---|
| `dom:prospect_id` | 23 | 07/11 | C |
| `dom:schedule_id` | 15 | 07/11 | C |
| `dom:prospect_results` | 13 | 07/11 | C |
| `dom:prospect_search` | 11 | 07/11 | C |
| `dom:conference_id` | 6 | 07/11 | C |
| `dom:management` | 6 | 02/11 | C |
| `dom:game_plan_id` | 4 | 02/11 | C |
| `dom:news_id` | 4 | 07/11 | C |
| `dom:alerts` | 3 | 06/11 | C |
| `dom:game_plan_id_dc` | 3 | 02/11 | C |
| `dom:coach_search` | 2 | 30/10 | C |
| `dom:coaches_id` | 2 | 01/11 | C |
| `dom:statistics_id_c` | 2 | 30/10 | C |
| `dom:user_input` | 2 | 30/10 | C |
| `dom:arena_id` | 1 | 30/10 | C |
| `dom:champions` | 1 | 30/10 | C |
| `dom:coach_id` | 1 | 30/10 | C |
| `dom:coaching_news` | 1 | 01/11 | C |
| `dom:game_action` | 1 | 30/10 | C |
| `dom:guide` | 1 | 30/10 | C |
| `dom:hall_of_fame_id` | 1 | 30/10 | C |
| `dom:help` | 1 | 30/10 | C |
| `dom:history_id` | 1 | 30/10 | C |
| `dom:home` | 1 | 30/10 | C |
| `dom:rankings` | 1 | 30/10 | C |

## hockeynation

| type de page | n | dernier | clés |
|---|---:|---|---|
| `/api/club/<id>` | 146 | 08/11 | E ; body: bananas, data, hasCoachingStaff, hasHallOfFame |
| `/api/free-agent-center/frenzy-event/live` | 126 | 27/10 | E ; body: data |
| `/api/club/<id>/coach-pick-order` | 121 | 06/11 | E ; body: data |
| `/api/coach/<id>/jobs` | 116 | 04/11 | E ; body: data, pagination |
| `dom:coach_id` | 113 | 01/11 | D |
| `/api/coach/<id>/season-stats` | 105 | 04/11 | E ; body: data |
| `/api/coach/<id>/last-games` | 98 | 04/11 | E ; body: data |
| `/api/coach/<id>/news` | 91 | 01/11 | E ; body: data, pagination |
| `/api/coach/<id>/career-stats` | 90 | 04/11 | E ; body: data |
| `/api/notifications` | 83 | 08/11 | E ; body: liveGames, messages, news, nextTrackedGame, tradeOffers, world |
| `dom:game_id` | 76 | 08/11 | D |
| `/api/game/live-scores` | 71 | 08/11 | E ; body: data |
| `/api/team/<id>/related` | 71 | 07/11 | E ; body: data |
| `/api/player-info/<id>` | 61 | 08/11 | E ; body: data |
| `/api/user` | 48 | 08/11 | E ; body: activatedAt, currency, federation, frmLeague, frmTeamId, giftBalance, goalHorns, id, isPrem… |
| `/api/world/version` | 38 | 07/11 | E ; body: version |
| `dom:guide` | 38 | 23/10 | D |
| `/api/club/<id>/news` | 37 | 08/11 | E ; body: data, pagination, team |
| `/api/club/<id>/league-group-standing` | 34 | 08/11 | E ; body: data |
| `/api/club/<id>/scoring-leaders` | 32 | 08/11 | E ; body: data |
| `/api/club/<id>/ratings` | 29 | 04/11 | E ; body: data |
| `dom:club_roster_id` | 28 | 07/11 | D |
| `/api/club/<id>/season-salary` | 24 | 04/11 | E ; body: projectedSeasonSalary, salaryCap |
| `/api/player/<id>/call-up-for-national-team` | 23 | 04/11 | E ; body: status |
| `/api/player/<id>/news` | 22 | 29/10 | E ; body: data, pagination |

## sixzeroleague

| type de page | n | dernier | clés |
|---|---:|---|---|
| `/hubs/chat/negotiate` | 176 | 08/11 | E ; body: availableTransports, connectionId, connectionToken, negotiateVersion |
| `/hubs/competitions/negotiate` | 172 | 08/11 | E ; body: availableTransports, connectionId, connectionToken, negotiateVersion |
| `/api/notifications/mine` | 148 | 08/11 | E ; body: balance, latestEventAt, lineupAutoFilled, liveMatches, nationalTeam, nextKickoff, sponsor |
| `/api/chat/messages` | 102 | 08/11 | E (body non objet) |
| `dom:app_team` | 58 | 08/11 | D |
| `/hubs/transfers/negotiate` | 44 | 07/11 | E ; body: availableTransports, connectionId, connectionToken, negotiateVersion |
| `dom:app_competitions` | 41 | 08/11 | D |
| `/api/leagues/<id>` | 35 | 08/11 | E ; body: currentRound, division, leagueId, maxTeams, name, promotionPlaces, relegationPlaces, round… |
| `dom:app_wiki` | 27 | 18/10 | D |
| `/api/teams/mine/live-match` | 21 | 24/10 | E ; body: awayPenalties, awayScore, awayTeamId, awayTeamName, clockSeconds, homePenalties, homeScor… |
| `/api/infrastructure/mine` | 19 | 07/11 | E ; body: balance, facilities |
| `/api/seasons/current/teams/<id>/player-stats` | 15 | 08/11 | E (body non objet) |
| `/api/world-cup/current` | 15 | 07/11 | E ; body: championCountry, currentRound, entrants, entries, groupRounds, groups, knockoutSize, match… |
| `/api/seasons/current/teams/<id>/competition` | 13 | 04/11 | E ; body: currentRound, division, leagueId, maxTeams, name, promotionPlaces, relegationPlaces, round… |
| `/api/world-cup/current/live` | 13 | 04/11 | E ; body: groups, matches |
| `/api/health` | 12 | 07/11 | E ; body: status |
| `/api/teams/<id>/trophies` | 12 | 04/11 | E (body non objet) |
| `/api/teams/<id>` | 11 | 04/11 | E ; body: country, id, isBot, logoIcon, logoShape, name, ownerId, ownerUsername, primaryColor, rating… |
| `dom:app_transfers` | 11 | 07/11 | D |
| `/api/teams/<id>/favourite-tactics` | 10 | 08/11 | E ; body: aggression, attackDirection, attackFormation, defenseFormation |
| `dom:app_club_infrastructure` | 10 | 07/11 | D |
| `/api/profiles/me` | 6 | 02/11 | E ; body: role, username |
| `/api/teams/<id>/players` | 6 | 30/10 | E (body non objet) |
| `/api/teams/mine/transfers` | 6 | 31/10 | E ; body: arrivals, departures |
| `dom:app_club` | 6 | 31/10 | D |

## teamsoccer

| type de page | n | dernier | clés |
|---|---:|---|---|
| `/rest/v1/forum_post_likes` | 191 | 31/10 | E (body non objet) |
| `/rest/v1/tsc_magics` | 57 | 04/11 | E (body non objet) |
| `/rest/v1/manager_topwebgames_votes` | 47 | 04/11 | E (body non objet) |
| `/rest/v1/manager_mc_stats` | 46 | 04/11 | E (body non objet) |
| `/rest/v1/forums` | 34 | 04/11 | E (body non objet) |
| `/rest/v1/player_league_stats_per_match` | 31 | 04/11 | E (body non objet) |
| `/rest/v1/group_members` | 30 | 29/10 | E (body non objet) |
| `/rest/v1/rpc/count_unread_messages` | 30 | 29/10 | E (body non objet) |
| `/rest/v1/meta` | 26 | 29/10 | E (body non objet) |
| `/rest/v1/room_forum_threads` | 26 | 29/10 | E (body non objet) |
| `/rest/v1/rpc/reveal_youth_skill` | 25 | 04/11 | E ; body: daily_reveal_count, player_id, skill_name, skill_value |
| `/rest/v1/cup_tournaments` | 24 | 02/11 | E (body non objet) |
| `/rest/v1/leagues_regions` | 23 | 29/10 | E (body non objet) |
| `/rest/v1/team_visits` | 20 | 31/10 | E (body non objet) |
| `dom:dashboard_match-viewer_id` | 20 | 31/10 | D |
| `/rest/v1/official_match_history` | 19 | 04/11 | E (body non objet) |
| `/rest/v1/cup_participants` | 18 | 04/11 | E (body non objet) |
| `/rest/v1/match_halftime_changes` | 18 | 31/10 | E (body non objet) |
| `dom:dashboard_squad` | 18 | 04/11 | D |
| `dom:dashboard_youth-scout` | 18 | 04/11 | D |
| `dom:dashboard_transfers` | 17 | 04/11 | D |
| `dom:dashboard_finances` | 16 | 04/11 | D |
| `dom:dashboard_forums` | 16 | 27/10 | D |
| `dom:dashboard_stadium` | 14 | 04/11 | D |
| `/rest/v1/forum_translations` | 13 | 31/10 | E (body non objet) |

## basketvibe (ajouté à l'étape 4 ; clés : **E** pour l'API, **F** = `tables, text, title` pour le DOM)

| type de page | n | dernier | clés |
|---|---:|---|---|
| `/api/v1/leagues/<id>` | 110 | 16/11 | E ; body: country_code, last_round_number, league_id, league_name, league_short_code, le… |
| `dom:unknown` | 106 | 16/11 | F |
| `dom:match` | 95 | 16/11 | F |
| `/api/v1/clubs/<slug>/schedule` | 78 | 16/11 | E ; body: active_enrollments, cup_fixtures, fixtures, friendlies, from_ymd, league_timez… |
| `/api/v1/clubs/<slug>/season-history` | 77 | 16/11 | E ; body: league_id, league_name, league_short_code, rows, team_id, team_name |
| `/api/v1/clubs/<slug>/season-roster` | 70 | 16/11 | E ; body: players, season_id, season_index |
| `/api/v1/leagues/<id>/seasons/<id>/fixtures/round/<n>` | 68 | 16/11 | E ; body: fixtures, match_day, round_number, season_id, team_country_codes, team_kits, te… |
| `/api/v1/clubs/<slug>/head-to-head` | 67 | 16/11 | E ; body: filters, league_timezone, matches, opponent_country_code, opponent_kit, oppone… |
| `/api/v1/teams/<id>/tactics` | 66 | 16/11 | E ; body: active_cup_preset_id, active_friendly_preset_id, active_league_preset_id, ac… |
| `/api/v1/teams/<id>/notifications` | 56 | 16/11 | E ; body: notifications, total |
| `/api/v1/leagues/<id>/seasons` | 55 | 16/11 | E ; body: seasons |
| `/api/v1/leagues/<id>/chat/sync` | 53 | 10/11 | E ; body: messages, server_time, unread_count |
| `dom:friendly` | 44 | 16/11 | F |
| `/api/v1/clubs/<slug>/seasons` | 41 | 16/11 | E ; body: current_season_id, seasons |
| `/api/v1/teams/<id>/notifications/unread-count` | 39 | 16/11 | E ; body: unread_count |
| `/api/v1/clubs/<slug>/trophies` | 38 | 16/11 | E ; body: cup_rows, rows, team_id, team_name |
| `/api/v1/watchlist/clubs` | 38 | 16/11 | E ; body: clubs |
| `/api/v1/teams/<id>/league-fixtures` | 33 | 16/11 | E ; body: fixtures, team_labels |
| `/api/v1/teams/<id>` | 25 | 11/11 | E ; body: arena_name, away_kit_text_color, country_code, home_kit_text_color, kit_logo_… |
| `/api/v1/leagues/<id>/seasons/<id>/rounds/<n>/best-five` | 23 | 16/11 | E ; body: mvp_player_id, round_complete, round_number, season_id, slots |
| `/api/v1/teams/<id>/cup-fixtures` | 20 | 13/11 | E ; body: active_enrollments, cup_fixtures |
| `/api/v1/teams/<id>/friendlies/invites` | 20 | 16/11 | E ; body: booked, invite |
| `/api/v1/news/has-new` | 18 | 12/11 | E ; body: has_new |
| `/api/v1/onboarding/status` | 17 | 11/11 | E ; body: completed_task_count, eligible, journey_active, journey_skipped, levels, next_… |
| `/api/v1/players/<id>/season-profile` | 17 | 16/11 | E ; body: achievements, averages, bests, career, friendly_statistics, games_played, lates… |
