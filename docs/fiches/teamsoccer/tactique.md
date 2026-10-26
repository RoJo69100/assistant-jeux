# Team Soccer — fiche Tactique

Lue par l'agent `tactique` après `commun.md`. Case E3 de la checklist Team Soccer.

## Skills à lire
- `.claude/skills/teamsoccer-match/SKILL.md` (formations, mode Simple et presets, mode Avancé, style, moteur v3, banc et remplacements, bots, moral)
- `.claude/skills/teamsoccer-joueurs/SKILL.md` (sous-rôles, Forme, talents et météo, cartons)

## Règles propres au jeu
1. **Tout enregistrer au moins 2 h avant le coup d'envoi** (match pré-calculé) [F:2026-06-28 Admin-Dev]. Donne l'heure limite en heure de Paris (`lineup_deadline_paris`). Un match de 13:50 se prépare la veille au soir.
2. Choix à rendre : formation (6), style d'équipe (Très défensif → Très offensif ; ampleur contradictoire dans le skill), 11 joueurs à leur sous-rôle naturel, consignes par zone en mode Avancé, banc de 6 avec rôle couvert, remplacements programmés.
3. **Forme** : un titulaire fatigué joue moins bien dès la 1re minute ; un remplaçant entre avec tout son plafond [F:2026-10-18 Admin-Dev]. Préfère un remplaçant en forme à un titulaire à Forme < 60.
4. Talent : vérifier la météo (−20 % sur toutes les compétences pour la météo qui le pénalise) [skill joueurs].
5. Contre un bot : il joue Neutre, compétences réduites ; profite-en pour reposer les joueurs fatigués ou suspendus à 2 jaunes.

## Données
- `gold.ts_upcoming` : prochains matchs, adversaire, `opponent_rating` / `my_rating`, rang, `lineup_saved`, `saved_formation`, `lineup_deadline_paris`.
- `silver.ts_players` : compétences, `forme`, `zone`, `injury_days`, `suspended`, `yellow_cards`.
- `silver.ts_match_lineups` (par match) et `silver.ts_lineups` (compositions par défaut) : `formation`, `play_style`, `player_positions` / `positions` (emplacement 0–10 → `player_id`), `player_orders` (consignes par joueur), `bench` (`subs`, `slots` avec `coverRole`, `changes` : minute, condition, entrant, sortant).
- Consignes de l'API, en espagnol : zones `ultradef`, `def`, `media`, `ofensiva`, `finalizacion` ; actions `pasar` (passer), `despejar` (dégager), `regatear` (dribbler), `centrar` (centrer) ; cibles `defensas`, `mediocentros`, `delanteros`. Traduis-les en français dans le livrable.
- `outputs/teamsoccer/learnings.md` dès qu'il existe.

## Livrable
Pour chaque match à venir des deux clubs : formation, style, onze (emplacement → joueur), consignes clés, banc et remplacements, plan B (blessure, carton), heure limite d'enregistrement.

## Règles de consignes par poste et par zone (2026-10-23)
Base : [skill teamsoccer-match § Avancé] 5 zones (Ultra défensive, Défensive, Médiane, Offensive, Finition) ; actions dégager, passer, dribbler, centrer, tirer ; consigne cohérente avec la meilleure compétence ×1,10, incohérente ×0,90 ; bonus de poste dans la zone naturelle (DC défensive ×1,15 Défense ; milieu au milieu ×1,10 ; attaquant en Finition ×1,15 Finition et Tête ; ailier qui centre ×1,20 Centres ; milieu qui tire ×1,05 Finition). Les tableaux ci-dessous sont **déduits** de ces multiplicateurs, pas des règles du jeu : à confirmer au fil des matchs.

| Poste | Ultra déf. | Défensive | Médiane | Offensive | Finition |
|---|---|---|---|---|---|
| Défenseur central | dégager | passer (milieu) | passer | passer | passer (jamais dribbler : ×0,90) |
| Latéral | dégager | passer | dribbler si Conduite ≥ 70, sinon passer | centrer si Centres ≥ 70, sinon passer | centrer |
| Milieu | passer | passer | passer ou dribbler selon la meilleure des deux (Passe/Conduite) | passer vers l'attaquant | tirer si Finition ≥ 60 (×1,05), sinon passer |
| Ailier | passer | passer | dribbler | centrer (×1,20) ou dribbler | tirer |
| Attaquant | passer | passer | passer | dribbler puis tirer | tirer (×1,15) |

Règle de choix : pour chaque joueur et chaque zone, l'action = la compétence la plus haute parmi celles qui servent l'action (Passe → passer, Conduite → dribbler, Centres → centrer, Finition → tirer), sauf dans la zone Ultra défensive (dégager). Les défenseurs et milieux qui « dribblent puis tirent » privent les attaquants de ballons [F:2026-09-15 PIPO68].

## Emplacements (confirmé par l'utilisateur, 2026-10-23)
- Défense à 4 : emplacements 1 et 4 = latéraux, 2 et 3 = centraux. Milieu à 3 : 1 latéral, 1 central, 1 latéral. Les centraux ne centrent pas (ils passent) ; seuls les latéraux et les ailiers centrent.
- Gardien : une seule consigne (dégager). Aucune consigne en zone de Finition pour les défenseurs ni le gardien.

## Données absentes enregistrées (2026-10-23)
- **Départage à 60** : plusieurs joueuses de Ben Ahmed ont Passe = Conduite = Centres = Finition = 60. Il me manque une règle de choix ; voici comment on l'obtient ensemble : saisir « passer » (action par défaut du poste), puis comparer les pertes de balle après le match (`gold.ts_match_plays`) et tester « dribbler » si elles sont trop nombreuses.
- **Remplaçant et consignes** : il me manque si un entrant reprend les consignes du sortant ; voici comment on l'obtient ensemble : après le premier remplacement réel, lire l'onglet Avancé de la page du match et le noter ici.
- **Numéros d'emplacement des formations à 5 défenseurs (1-5-4-1)** : déduits, non vus ; voici comment on l'obtient ensemble : choisir la formation à l'écran et relever le numéro de chaque case.
- **Convention des tableaux nommés** : Défensive = passer pour tous ; Médiane et Offensive = meilleure compétence d'action ; Finition seulement milieux, ailiers, attaquants ; centraux ni centrer ni dribbler. Les consignes de Chomelix pour Adrien Roux, Lucas David et Robert suivent la logique de poste, pas strictement la meilleure compétence : décision de l'utilisateur en attente.
