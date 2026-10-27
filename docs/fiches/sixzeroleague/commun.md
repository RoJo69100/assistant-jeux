# Six Zero League — fiche commune (tous les agents)

Lue en premier par chaque agent, avant la fiche de son domaine (`docs/fiches/sixzeroleague/<agent>.md`). Rédigée le 2026-10-19 ; le jeu est en **alpha** [W:Competitions] et change vite.

## Identité
- Identifiant : `sixzeroleague` (bronze : `game = 'sixzeroleague'` ; vues `silver.sz_*`, `gold.sz_*`). Handball.
- Notre club : Chomelix Cow, ligue Vanadium, 5e division, 10 clubs, 18 journées (`silver.sz_standings`, 2026-10-18).
- Rôles (codes de l'API) : GK gardien, CB demi-centre, LB / RB arrières, LW / RW ailiers, P pivot. Compétences de 1 à 100 [W:Attributes].
- Pas de forme, pas de personnel, pas de jauge d'académie : ne transpose aucune règle de BasketVibe.

## Sources et codes de citation
- `[W:Rubrique]` wiki officiel (« si une règle n'est pas écrite, elle n'est pas appliquée » [W:Introduction]) > `[Dev chat]` Gazelle, le développeur > `[Com chat, pseudo]` joueur (avis, jamais une règle) > `[Obs]` nos observations (`[Obs SQL date]`, `[Obs utilisateur date]`).
- Skills : `.claude/skills/sixzeroleague-match|joueurs|entrainement|club|communaute/SKILL.md`. Discord du jeu : exports dans `data/discord/SixZeroLeague/` (canaux #dev-log et #chat, `[Dev chat]` pour Gazelle/gazellemag, `[Com chat]` pour les autres) ; chat global dans `data/chat/sixzeroleague/` et `silver.sz_api` '/chat/messages' (correction du 2026-10-23, veille V-20261023-4).

## Rythme (skill sixzeroleague-communaute § 1)
- Une « semaine » du jeu = **2 journées de ligue** : finances, entraînement, blessures et transferts se règlent ensemble [W:Finances]. On l'appelle **cycle**.
- **2 journées par jour** : 13:00 et 21:00 (Paris) ; le cycle se règle **chaque soir après le match de 21:00** [Dev chat]. Coupe 17:00 (Paris) [Dev chat, 2026-10-18 : 16:00 Lisbonne] ; un joueur dit 17:00 Lisbonne, non confirmé.
- Saison = 9 à 11 jours ; **+1 an pour les joueurs à chaque saison** [Dev chat] : bonus jeune, déclin et retraite arrivent vite en temps réel. Hors saison, aucun cycle ne passe.
- Une recommandation donne toujours sa **date limite en heure de Paris** (en général : avant 21:00 le jour même).

## Pièges communs
- **Hors-poste** : l'écran l'affiche en orange, sans note ; `role_overalls` de l'API est calculé **avant** la pénalité [Obs SQL 2026-10-18]. Une note hors poste n'est donc pas comparable à une note au poste.
- Bots selon la division, bien plus faibles qu'une équipe humaine forte [Dev chat] ; résultats encore très aléatoires [Dev chat] : prudence sur les conclusions.
- Confidentialité : ne jamais afficher `ownerUsername` (e-mail des autres managers).
- Montants en euros entiers ; revenus, coûts et entretien multipliés par la division (pas les salaires) [W:Competitions].

## État des données (2026-10-19)
- Silver (`sql/silver/010_sz_base.sql`) : `sz_api`, `sz_my_team`, `sz_player_snapshots`, `sz_players`, `sz_tactics`, `sz_training_plan`, `sz_training_changes`, `sz_role_training`, `sz_finances`, `sz_infrastructure_levels`, `sz_standings`, `sz_fixtures`, `sz_transfer_listings`, `sz_u18`.
- Gold (`sql/gold/013_sz_gold.sql`) : `sz_infrastructure_payback`, `sz_lineup_natural`, `sz_slot_options`.
- Silver des matchs (`sql/silver/011_sz_matches.sql`, 2026-10-19) : `sz_matches`, `sz_match_players`, `sz_match_incidents`.
- Cycles (`sql/gold/014_sz_cycles.sql`, 2026-10-19) : `silver.sz_player_cycles` (relevé des joueurs rattaché au dernier cycle réglé), `gold.sz_role_report` (bilan par rôle), `gold.sz_training_progress` (points par cycle et par joueur), `gold.sz_finance_cycles` (résultat de chaque cycle) et `gold.sz_finance_projection` (fin de saison). `weekNumber` repart à 1 chaque saison : un cycle s'identifie par `applied_at`.
- Calendrier et agenda (`sql/gold/015_sz_agenda.sql`, 2026-10-19) : `silver.sz_schedule` (heure officielle de chaque journée de ligue et tour de coupe, mon adversaire), `gold.sz_agenda` (plan du soir), `gold.sz_daily_alerts`. Skill `sixzeroleague-aujourdhui`.
- Aucune capture après le 2026-10-18 au moment de la rédaction : vérifie toujours la date du dernier relevé (`day`, `as_of`) et demande l'export si elle est périmée.

## Ordre des agents et briefs du jour (règle du 2026-10-22)
Un agent ne rend jamais un retour incomplet parce qu'un autre agent n'est pas encore passé. Ordre : Veille (si nouvelle source) → Match → Effectif → Infrastructures (lire `silver.sz_infrastructure_levels` et `silver.sz_finances.since_last_report` : montées déjà payées, ex. Youth Academy 4 → 5 le 2026-10-26 ; règle du 2026-10-26, l'agent Finances disait « dépense inconnue » faute de les avoir lues) → Finances-personnel → Académie (U18) → Entraînement → Tactique → Transferts (dernier). Chaque agent lit d'abord les briefs du jour (`outputs/sixzeroleague/briefs/AAAA-MM-JJ-<domaine>.md`) des agents placés avant lui ; seuls les agents sans dépendance entre eux tournent en parallèle. Avant d'écrire « donnée non relevée », cherche dans ces briefs ; sinon, dis quel export manque en tête du résumé. Un agent en aval qui contredit un agent en amont l'écrit en tête de son résumé (relance à faire).

## Sorties
- Briefs : `outputs/sixzeroleague/briefs/AAAA-MM-JJ-<domaine>.md`.
- Journal : `outputs/sixzeroleague/learnings.md` (enseignements `L-nnn`, conseils `C-nnn`) ; à créer au premier match analysé, sur le modèle de `outputs/basketvibe/learnings.md`.
- Veille : `outputs/sixzeroleague/veille/`.

## Options de tactique observées à l'écran (déclaré par l'utilisateur, 2026-10-24)
- Formation d'attaque : 5-1 ou 4-2 (nouveau).
- Formation de défense : 6-0, 5-1, 3-2-1 ou 3-3 (nouveau).
- Direction d'attaque : mixed, left, right, centre, left + centre, right + centre, left-right.
- Remplace « 5-1 / 6-0 seules disponibles » [Dev chat, 2026-10-10], périmé. Effets connus (qualitatifs) : voir `outputs/sixzeroleague/veille/connaissance.md` § 1 (contres 1.3, 4-2 sans CB 1.6, hors-poste défensif 1.8). Direction d'attaque : effet **non chiffré** (écran : « left/right + centre » = CB et P attaquent le plus). À relever dans l'export du match (`teams.tactics`, rempli seulement pour J12 : aggression normal, attackDirection mixed). [V-20261026-23, corrige « aucune source n'indique l'effet »]

## Repères infrastructures des autres clubs (chat du jeu en base, 2026-10-26)
Source : `silver.sz_api` `/chat/messages`. Avant d'écrire « pas de donnée » sur un autre club, chercher là et dans `data/discord/SixZeroLeague/`, `data/chat/sixzeroleague/`.
| Club (joueur) | Date | Arena | Training Facilities | Youth Academy | Fan Shop |
|---|---|---|---|---|---|
| Stoik | 2026-10-21 | 7 | 1 | **10** | **10** |
| martin | 2026-10-22 | 9 | 6 | 2 | 1 |
| pierrottingchrist_29708 (Discord) | 2026-10-20 | ? | ? | 9 | ? |
| Nous | 2026-10-27 | 7 | 6 | 6 | 9 |
- Stoik : Youth Academy 10 = prospects aux compétences 10 à 38, moyenne d'un tirage ≈ 24 de note ; il a tiré un pivot à 26 (2026-10-21 et 2026-10-23). Il conseille le Fan Shop quand on est bien classé (2026-10-23). Notre Fournier (17) sort d'une académie niveau 5.
- Retard mesuré : Youth Academy 5 contre 9–10 chez deux clubs ; Arena et Fan Shop au niveau des autres. Training Facilities 6 : au niveau de martin, très au-dessus de Stoik.
