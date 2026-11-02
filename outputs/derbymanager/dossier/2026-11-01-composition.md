# Dossier derbymanager — composition — 2026-11-01

À lire **en entier**, puis remplir la grille `docs/decisions/variables.md` § `composition` et le tableau Couverture. Mots : tactic, lineup, line-up, rotation, minutes, fatigue, focus, preset, depth, formation, tactique, composition, consigne

## 1. Règles (skills à lire en entier)
- `.claude/skills/derbymanager-club/SKILL.md`
- `.claude/skills/derbymanager-effectif-entrainement/SKILL.md`
- `.claude/skills/derbymanager-regles/SKILL.md`
- `.claude/skills/derbymanager-tactique/SKILL.md`
- fiches : `docs/fiches/derbymanager/resume.md`

## 2. Avis des amis — connaissance (toutes les lignes sur le sujet)
### `outputs/derbymanager/veille/connaissance.md` — 0 lignes

## 3. Avis des amis — Discord / chat bruts
- 246 lignes (dont 0 avec un mot précis) → `outputs/derbymanager/dossier/2026-11-01-composition-discord.txt`, **à lire en entier**.
- 3938 lignes à un seul mot générique → `outputs/derbymanager/dossier/2026-11-01-composition-discord-faible.txt` : relancer avec `--mots` précis pour les remonter.
- Avant « absent » : `bronze.discord_messages` et le chat en base (`silver.sz_api` pour Six Zero League).

## 4. Chiffres (à interroger, toute la saison)
- vues gold citées par le résumé : `gold.dm_effectif`, `gold.dm_entrainement`, `gold.dm_entrainement_plan`, `gold.dm_exports_etat`, `gold.dm_finances_bilan`, `gold.dm_joueurs`, `gold.dm_marche_notes`, `gold.dm_marche_postes`, `gold.dm_matchs`, `gold.dm_poste_scores`, `gold.dm_prix_reference`, `gold.dm_saison_bilan`, `gold.dm_tirs_profil`, `gold.dm_verdict_joueurs`
- exports du jour : `bronze.raw_pages` where game = 'derbymanager' and captured_at >= '2026-11-01'
- registre : `outputs/derbymanager/fait-2026-11-01.md`

## 5. Couverture (à remplir par l'agent)
| Source | trouvés | lus | retenus | écartés (pourquoi) |
|---|---|---|---|---|

## 6. Carte (pour ne plus jamais tout relire)
- `docs/decisions/cartes/derbymanager/composition.md` n'existe pas : écris-la (modèle `docs/decisions/cartes/MODELE.md`) — chaque variable, l'endroit exact où tu l'as trouvée (requête, fichier § section) et son check. Commit, puis `python pipelines/dossier.py derbymanager composition --marquer`. Les prochaines fois, seul le nouveau sera lu.
