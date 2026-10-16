# Game Assistant — assistant de gestion de clubs (jeux de management sportif)

Réponds en français, court et précis. Si tu ne sais pas, dis-le. Ne devine jamais une règle de jeu : cite le skill ou la source.

## Objectif
Aider le propriétaire à gagner sur ses jeux de management en ligne. Pilote : **BasketVibe**.
La checklist `docs/checklist-basketvibe.md` définit le périmètre : le travail est fini quand tout est coché.
Coche une case uniquement quand son critère est vérifié, et note la date.

## Architecture
- **Collecte** : un script Tampermonkey par jeu (`userscripts/<jeu>.user.js`) exporte le JSON de la page ouverte par l'utilisateur et l'envoie dans Supabase. Jamais de robot qui navigue seul, jamais de requête supplémentaire vers le site du jeu.
- **Discord** : export géré par l'utilisateur ; fichiers déposés dans `data/discord/<jeu>/`, puis importés en bronze par `pipelines/import_discord.py`.
- **Données** : Supabase (Postgres), schémas `bronze` (JSON brut daté, jamais modifié), `silver` (vues/tables par jeu), `gold` (vues d'analyse et d'alertes). Les calculs se font en SQL, pas dans le LLM.
- **Connaissance** : skills par jeu dans `.claude/skills/<jeu>-<domaine>/SKILL.md`. Chaque fait est sourcé (manuel, devlog, Discord + date). Toute modification de skill proposée par l'agent veille doit être validée par l'utilisateur.
- **Agents** : par domaine dans `.claude/agents/` (effectif, match, tactique, entrainement, academie, transferts, finances-personnel, veille). Ils lisent Supabase via MCP et chargent le skill du jeu concerné.
- **Sorties** : `outputs/<jeu>/` — wiki, journal des enseignements (`learnings.md`), briefs datés.

## Arborescence
```
.claude/agents/        agents par domaine
.claude/skills/        skills par jeu
userscripts/           scripts Tampermonkey
sql/bronze|silver|gold migrations et vues SQL
pipelines/             Python (import Discord, utilitaires)
samples/<jeu>/         pages HTML enregistrées (ignoré par Git)
data/discord/<jeu>/    exports Discord (ignoré par Git)
outputs/<jeu>/         wiki, learnings, briefs
docs/                  checklist et décisions
```

## Règles
- Secrets dans `.env` (jamais commité). `samples/`, `data/` et `.env` sont dans `.gitignore`.
- Python 3.12, dépendances dans `requirements.txt`.
- Une modification = un commit avec un message clair.
- Coût : ne jamais relire tout l'historique brut ; travailler sur les vues gold et le delta du jour.

## Sources BasketVibe
- Manuel officiel : https://www.basketvibe.com/guide
- Devlog : https://www.basketvibe.com/devlog
- Discord : exports dans `data/discord/basketvibe/`
