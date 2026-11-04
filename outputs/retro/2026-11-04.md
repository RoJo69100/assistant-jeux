# Rétro 2026-11-04 — refonte v2, règles d'export Derby Manager (conception, aucun jeu joué)

| Erreur | Cause racine | Règle / emplacement |
|---|---|---|
| `git push -q` refusé, commit bloqué avec | RÉCIDIVE de la rétro du 2026-11-03 (même erreur). La leçon n'était que dans `outputs/retro/2026-11-03.md`, ni dans `actives.md` ni dans `CLAUDE.md` : non relue au démarrage. Le hook `garde_push.py` a joué son rôle. Commit chaîné au push : un refus bloque les deux. | N2 dans `docs/regles/actives.md` (commit et push en deux appels). Pas de montée dans `CLAUDE.md` : un hook bloque déjà. |
| `psycopg` absent : `sql.py`, `recette.py`, `*_parite.py` inutilisables en cloud | `requirements.txt` listait `psycopg[binary]` mais rien ne l'installe au démarrage cloud ; aucun contournement documenté | N1 dans `docs/regles/actives.md`. Tâche de conception (Opus) : ajouter `pip install -r requirements.txt` au SessionStart de `.claude/settings.json`, ou un repli du script sur le connecteur. |
| Ligne de parité écrite à la main dans `parite-exports.log` | Conséquence du point précédent ; la comparaison elle-même (0 écart, 15/15) est faite via le connecteur, mais le journal ne distingue pas manuel et script | N1 : marquer `(manuel, script non exécuté)` ; relancer le script dès que psycopg est installé. |

## Ce qui a bien marché
Prochaine étape déduite du journal, comparaison chiffrée par requête, un commit, poussée vérifiée après relance.
