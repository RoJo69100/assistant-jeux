# Rétro 2026-10-31 — BasketVibe, compo de l'amical du 01/11

Session courte : compo + test, rendu une fois refusé par le hook `forme.py`, puis validé (« c'est fait »).

| # | Ce qui s'est passé | Cause racine | Règle corrective (où) |
|---|---|---|---|
| 1 | Premier rendu bloqué par le hook : colonne « Min » au lieu de « Minutes », adversaires en une ligne, plan sans tableau Priorité/Catégorie/Action | Je me suis fié à la mémoire `feedback-amical-compo-test` (« une ligne les 12 ») sans relire `pipelines/forme.py`, qui exige une ligne par joueur | 63 : avant tout rendu tactique, relire le format de `forme.py` ; la mémoire amical est alignée sur le hook (mémoire corrigée) |
| 2 | « Granada : noms pas en base » écrit avant toute requête | Affirmation d'absence sans recherche (règle « aucun flou », récidive de vérification) ; vérifié ensuite : aucune page d'aperçu de Granada en base, seulement club/schedule/notifications | 64 : chercher (`bronze.raw_pages ilike '%<adversaire>%'`) avant d'écrire « pas en base » |
| 3 | `gold.bv_zone_jouee` donne Middle pour Calije alors que la zone saisie était Rim : la vue lit l'export d'avant la saisie | La vue lit l'export, pas le plan réellement sauvegardé ; verdict C-100 appuyé sur la déclaration | 65 : signalé dans le brief ; tâche de conception (Opus) : lire la zone dans l'export du match joué, pas dans l'aperçu |
| 4 | Brief écrit sans lire d'abord l'export du match de coupe du jour | Dernier export 10:52, coupe à 18:00 : fatigue des dix supposée | Dit dans la réponse ; le test lit le match après export |

## Ce qui a bien marché
- Tableau joueur × quart-temps repris de `gold.bv_saisie_joueurs` sans réinventer ; test unique (zone) ; C-100 clos avec chiffres (L 95-131, 2P % adverse 63,8 %) et C-104 ouvert avec critère de réfutation.
- Registre `fait-2026-10-31.md` et commit dès « c'est fait ».

## À faire (conception, Opus)
- Vue gold : zone réellement jouée (export du match terminé) pour fiabiliser les tests de zone.
