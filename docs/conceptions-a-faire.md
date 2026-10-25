# Conceptions à faire

Chantiers de conception en attente (à lancer sur Opus, retour sur Sonnet après le commit).

## Issus de la rétro du 2026-10-24 (`outputs/retro/2026-10-24.md`)

| Priorité | Chantier | État |
|---|---|---|
| 🟥 URGENT | B1 : `silver.bv_matches.my_result` = L sur match sans score + règle 15 (test sur match non joué) | Fait le 2026-10-25 (`sql/silver/018`), test = 0 ligne, ligue 9V-12D |
| 🟧 IMPORTANT | B2 : `silver.sz_matches` ligne orpheline (13 lignes / 12 journées), `match_day` = jour de capture | À faire, ouvrir le brut d'abord |
| 🟧 IMPORTANT | B5 : `silver.hn_games` mélange les 4 équipes → colonne `team_level` ou `gold.hn_pro_games` | À faire |
| 🟧 IMPORTANT | Agent Match : compter les échecs d'un même conseil avant de rédiger ; 3 défaites = changement chiffré (règles 13-14) | À faire (`.claude/agents/match.md`) |
| 🟧 IMPORTANT | B3 : `silver.ts_match_lineups` vide depuis le 21/10, page composition captée ? | Test sur la composition d'Ajax (26/10) |
| 🟩 SUIVI | Numérotation `C-nnn` sans doublon (règle 17) | À faire |
| 🟩 SUIVI | B4 : phrase fausse en tête de `outputs/teamsoccer/learnings.md` | À faire (suppression simple) |

## Export en un clic piloté par Supabase (demandé le 2026-10-24)

Idée de l'utilisateur : un script Tampermonkey lit dans Supabase ce qu'il faut exporter aujourd'hui (journée, transferts, joueurs, etc.), fait les exports, puis écrit « export fait » dans une table ; un déclencheur lance ensuite les agents sans intervention.

| Partie | Contenu | Règle du projet |
|---|---|---|
| 1. Plan du jour | Checklist des exports lue dans Supabase et affichée sur la page | Compatible |
| 2. Suivi automatique | Chaque export coche sa ligne dans une table Supabase | Compatible |
| 3. Un clic, tout s'exporte | Le script récupère lui-même les autres pages | Interdit par « jamais de requête supplémentaire vers le site du jeu » |

**Décision de l'utilisateur (2026-10-24)** : si la partie 3 n'est pas possible, ne pas faire les parties 1 et 2. Chantier gardé ici, non lancé.

**À lever pour reprendre** : la règle « pas de requête supplémentaire » (décision de l'utilisateur) et la vérification des conditions d'utilisation du jeu concerné (non faite).

**Reste à vérifier si repris** : déclencheur automatique des agents sur « export fait » (tâche planifiée ou RemoteTrigger), non vérifié.
