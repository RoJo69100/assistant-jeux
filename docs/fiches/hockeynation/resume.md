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
- Plan de jeu : mentality (defensive/balanced/offensive), puck pressure (light/normal/heavy), tempo (slow/normal/fast), aggression (calm/normal/aggressive), shift length (short 35-40 s / normal 41-49 s / long 50-55 s), pull goalie 1 et 2 buts de retard (never/sometimes/always). Libellés : mémoire `reference-hn-plan-de-jeu-libelles`.
- Coach pick order par équipe ; Training PRO / FRM : compétence + coach par joueur.

## Vues prêtes (lis-les avant de calculer toi-même ; colonnes choisies, `LIMIT`)
- **Routine** : `gold.hn_today` (jour de saison), `gold.hn_daily_alerts` (rouge d'abord), `gold.hn_exports_state` (fraîcheur de chaque export, statut 🟩/🟧/🟥).
- **Décisions (sans agent)** : `gold.hn_player_potential` (tous nos joueurs : potentiel min/max, classe Fort / Solide / Moyen / Nul ↑, futur PRO / FRM / VIRER, fit ; fonction `gold.hn_potential(skills, talents, rating)` aussi pour un joueur adverse), `gold.hn_scout_priority` (candidats scouts du jour classés sur notre classe de draft, hors postes et nations déjà couverts, G exclus), `gold.hn_coach_options` (meilleur coach libre par poste de coach, gain d'équipe, head ×2, plafonds U17 54 / U21 69), `gold.hn_buyout_calc` (rachat contre échange : coût, effet sur le cap space, rachat interdit pour les agents libres de la saison).
- **Scouts et coachs (2026-10-29)** : `gold.hn_scout_targets` (à chaque passage scouts : lister **tous** les joueurs à repérer par chacun de nos scouts, catégories A poste+nation / B poste / C nation, plus les 6 premiers du classement d'abord), `gold.hn_coach_potential` (min/max des 5 compétences de match, tout est plafonné chez Strobel et Graf donc min = max ; max théorique tant que rien n'est plafonné), `gold.hn_coach_options` exclut les coachs arrivés cette saison (non remplaçables).
- **Rendu [U, 2026-10-29, colère]** : tout résultat **en tableau, un tableau par équipe** (PRO, FRM, U21, U17), jamais en puces. Toujours d'abord la **liste complète de tous les joueurs** de chaque équipe (note, potentiel min–max, classe, futur, adéquation, END, contrat, place), puis les compositions à 20, puis le roster **A+1** (saison suivante : contrats finis, 22 ans en U21, draft en U17, postes qui manquent). Scouts : le but est de **couvrir le plus de joueurs possible** (`gold.hn_scout_coverage` = par scout poste+nation / poste / nation / total, `gold.hn_scout_priority` = candidats classés par joueurs NOUVEAUX couverts) ; un coach arrivé par offre cette saison (`firstSeason`) ne se remplace pas, un intérimaire oui (Ahn).
- **Tableaux prêts [U, 2026-10-29]** : `gold.hn_scout_board` (TOUS les scouts, embauchés + candidats : top poste+nation / poste / nation / total / nouveaux), `gold.hn_coach_candidats` (xp, marge, droits U17/U21). Faits déclarés par l'utilisateur et pas encore exportés (scouts embauchés, joueurs bloqués, offres de coachs) : `silver.hn_declared`, à alimenter à chaque « j'ai fait X ». **Règles coachs [U]** : U17 = note ≤ 54 ET expérience ≤ 4 (Average), on cherche 2 talents forts de match (OFP DFP BAT PP PK) et la plus grande marge ; U21 = note ≤ 69 ET expérience ≤ 7 (Very Good), donc ni Vrábel (xp 10) ni Majeský (xp 9) ; Strobel en PRO (offre envoyée). **Jasiński [U]** ne peut pas bouger non plus (reste PRO).
- **Carpentier [U]** n'est pas un des 4 agents libres : il ne peut pas bouger (reste en PRO). Les 4 agents libres sont Hakkarainen, Kaneda, Dosymkhanov, Jasiński.
- **Mouvements entre équipes [U, 2026-10-29]** : les 4 agents libres de la Frenzy du 27/10 (Hakkarainen, Kaneda, Dosymkhanov, Jasiński) peuvent être déplacés entre PRO / FRM / U21 / U17 ; le guide dit l'inverse (rétrogradation interdite pour un agent libre) : tester sur un joueur avant de bâtir le plan sur les quatre. Les compositions se refont poste par poste, 20 titulaires par équipe (2 G, 4 C, 4 LW, 4 RW, 3 LD, 3 RD), le surplus avec sa destination.
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

- **Rendu scouts [U, 2026-10-29]** : à « on fait quoi Hockey Nation », afficher `gold.hn_scout_liste` EN TABLEAU (une ligne par scout, colonnes top poste+nation / poste / nation avec les joueurs nommés et leur rang) puis `gold.hn_scout_board`. Jamais « pour voir la liste, requête X ». Rachat Eskelinen fait (pénalité 1 285 000 $ par saison S27-S29, dans `silver.hn_declared`).

- **Tactique PRO, rendu FIGÉ [U, 2026-10-29, « ne change jamais le rendu », « TRÈS satisfait »]** : toujours lire `gold.hn_tactique_effectif_poste` (tous les joueurs par poste), `gold.hn_tactique_rendu` (lignes, gardiens, PP1/PP2, PK4, PK3, 4v4, EXT, rôles, « (jeu : X) », 🟥 case vide / 🟧 à changer), `gold.hn_tactique_plan_rendu`, `gold.hn_tactique_controle`, et les afficher tels quels. Objectif permanent : meilleure tactique et meilleure équipe possibles ; trades, effectif et analyse de matchs se jugent sur leur effet dans la lineup cible (procédure de mise à jour : `docs/fiches/hockeynation/tactique.md`). Capitaine et assistants = cachés. Lineup v2 saisie le 29/10 ; shift length short = test (revenir à normal si la L1 encaisse plus de buts après 10 matchs).

- **Veille Discord 2026-10-29 (V-20261029-1 à 12, rapport `outputs/hockeynation/veille/2026-10-29.md`)** : toute lineup se saisit **au moins 1 h avant le match** (sinon risque de −30 %, hnadmin) ; en amical la pénalité de mauvais poste s'applique ; le rating d'équipe d'un coach est un score calculé des compétences de match, pas sa note affichée ; l'allègement du plafond est immédiat à l'action de rachat et à l'approbation d'un échange ; S28 (~27/12) = plancher salarial 50 % (base non publiée) ; ELC d'agent libre = « ovr max 69 » (avis, à vérifier à l'écran) ; PWR/FOF dans les compétences clés = hypothèse à tester, vues non modifiées.
- **Lecture intégrale Discord 2026-10-29 (46 propositions V-A/B/C appliquées aux skills ; index `outputs/hockeynation/veille/connaissance*.md`, à lire avant d'écrire « aucune source »)** : rachat = « moitié du restant » du guide NON confirmé par le staff (coût décroissant avec l'attente, lire l'écran) ; un seul Cap Space (−30 % si négatif > 1 h avant le match) ; formule d'OVR (excédents comptés deux fois, déduction à vérifier) ; spéciales chiffrées dans `hockeynation-joueurs` ; coachs : marché ouvert, une offre de head coach par jour, spécialiser par catégorie ; agent libre signé = probablement intransférable la saison (avis) ; pas de blessures dans le jeu ; favors d'agents : S27 ou S28 en désaccord, tester avant de compter dessus.
