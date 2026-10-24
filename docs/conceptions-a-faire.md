# Conceptions à faire

Chantiers de conception en attente (à lancer sur Opus, retour sur Sonnet après le commit).

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
