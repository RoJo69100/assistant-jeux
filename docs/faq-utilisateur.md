# FAQ — travailler avec Claude

## Commencer la journée
1. `/clear` si la session précédente est finie. Une session = un jeu.
2. Règle `/effort low` et `/model sonnet` (medium seulement pour lancer les agents d'analyse).
3. Fais tes exports du jour (BasketVibe : un amical chaque jour, vérifier tous les exports).
4. Écris une phrase : « [jeu] : j'ai fait [exports / composition / transfert] ». Claude vérifie en base et note dans `outputs/<jeu>/fait-AAAA-MM-JJ.md`.
5. Demande « que faire aujourd'hui sur [jeu] ». Claude répond avec le plan en SQL (agenda, alertes, registre), sans agent inutile.

## Quand tu vois un problème
| Situation | Dis ceci | Ce que Claude doit faire |
|---|---|---|
| Erreur de fait (nom, chiffre, résultat) | « Erreur : [ce qui est faux], preuve : [ce que tu vois] » | Revérifier en base (`my_result`), corriger, chercher d'autres lignes touchées |
| Il redemande ce que tu as déjà fait | « Déjà fait : [quoi] » | Le noter dans `fait-…`, ne plus le redemander |
| Réponse floue (« si », « peut-être ») | « Aucun flou : nomme-les » | Joueur par joueur, chiffres, une seule action |
| Trop long / fouilli | « Synthèse » | Un tableau par jeu, 🟥🟧🟩, détail dans les briefs |
| Conseil qui a échoué | « Le conseil C-nnn a échoué : [résultat] » | Le consigner dans `learnings.md`, proposer un autre levier (jamais le même deux fois) |
| Il affirme sans avoir lu | « Ouvre le fichier avant de répondre » | Lire le script / la vue / le brief, puis répondre |
| Bug de données (score, ligne en trop) | « Bug : [où], [attendu] vs [obtenu] » | Requête de preuve, puis correction SQL (conception, Opus) |
| Tu es en colère ou ça se répète | « Rétro » | Lancer l'agent `retro`, qui met à jour `docs/retro/regles-apprises.md` |

## Fin de session
- Une tâche finie = un commit. Puis `/clear`.
- Si la session a été longue ou si quelque chose t'a énervé : « Rétro » avant le `/clear`.
