# Six Zero League — fiche commune (tous les agents)

Lue en premier par chaque agent, avant la fiche de son domaine (`docs/fiches/sixzeroleague/<agent>.md`). Rédigée le 2026-10-19 ; le jeu est en **alpha** [W:Competitions] et change vite.

## Identité
- Identifiant : `sixzeroleague` (bronze : `game = 'sixzeroleague'` ; vues `silver.sz_*`, `gold.sz_*`). Handball.
- Notre club : Chomelix Cow, ligue Vanadium, 5e division, 10 clubs, 18 journées (`silver.sz_standings`, 2026-10-18).
- Rôles (codes de l'API) : GK gardien, CB demi-centre, LB / RB arrières, LW / RW ailiers, P pivot. Compétences de 1 à 100 [W:Attributes].
- Pas de forme, pas de personnel, pas de jauge d'académie : ne transpose aucune règle de BasketVibe.

## Sources et codes de citation
- `[W:Rubrique]` wiki officiel (« si une règle n'est pas écrite, elle n'est pas appliquée » [W:Introduction]) > `[Dev chat]` Gazelle, le développeur > `[Com chat, pseudo]` joueur (avis, jamais une règle) > `[Obs]` nos observations (`[Obs SQL date]`, `[Obs utilisateur date]`).
- Skills : `.claude/skills/sixzeroleague-match|joueurs|entrainement|club|communaute/SKILL.md`. Pas de Discord pour ce jeu.

## Rythme (skill sixzeroleague-communaute § 1)
- Une « semaine » du jeu = **2 journées de ligue** : finances, entraînement, blessures et transferts se règlent ensemble [W:Finances]. On l'appelle **cycle**.
- **2 journées par jour** : 13:00 et 21:00 (Paris) ; le cycle se règle **chaque soir après le match de 21:00** [Dev chat]. Coupe vers 17:00–18:00 (Paris) ⚠️ horaire incertain.
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
- Aucune capture après le 2026-10-18 au moment de la rédaction : vérifie toujours la date du dernier relevé (`day`, `as_of`) et demande l'export si elle est périmée.

## Sorties
- Briefs : `outputs/sixzeroleague/briefs/AAAA-MM-JJ-<domaine>.md`.
- Journal : `outputs/sixzeroleague/learnings.md` (enseignements `L-nnn`, conseils `C-nnn`) ; à créer au premier match analysé, sur le modèle de `outputs/basketvibe/learnings.md`.
- Veille : `outputs/sixzeroleague/veille/`.
