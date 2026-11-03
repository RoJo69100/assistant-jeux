---
name: retro-session
description: Rétro de fin de session (tous les jeux) : erreurs de Claude, cause racine, règle corrective dans outputs/retro/ et docs/regles/actives.md. À charger en début de session, en fin de session ou si l'utilisateur dit « tu ne t'améliores pas ».
---

# Rétro de session

## Début de session (obligatoire, 30 secondes)
Lis `docs/regles/actives.md` et applique-les. Si une règle a déjà été violée deux fois (la rétro le dit), elle passe dans `CLAUDE.md`.

## Fin de session (avant `/clear`, ou à la demande)
1. Relis les reproches de l'utilisateur dans la conversation (colère, « pourquoi », « tu redemandes », « je te l'ai déjà dit »), les corrections d'agents (« contradiction », « CORRECTION EN TÊTE ») et les erreurs que le vérificateur ou l'utilisateur a relevées.
2. Pour chaque point : ce qui s'est passé · cause racine (une phrase : donnée non lue, hypothèse non vérifiée, agent non lancé, format…) · règle corrective et où elle vit (`CLAUDE.md`, fiche du jeu, fichier d'agent, skill).
3. Écris `outputs/retro/AAAA-MM-JJ.md` (tableau, plus « ce qui a bien marché »), puis ajoute les nouvelles règles en tête de `docs/regles/actives.md` (une ligne chacune au format `Quand <déclencheur> → <action vérifiable>` ; si la règle a déjà récidivé, classe E : écris aussi le code ou la vue, sinon note `hook à écrire` ; 40 lignes au plus, supprime les doublons).
4. Si une règle demande une modification d'agent ou de skill, applique-la tout de suite quand elle tient en quelques lignes ; sinon, signale-la comme tâche de conception (Opus).
5. Termine par trois lignes à l'utilisateur : ce que j'ai mal fait, ce que j'ai corrigé, ce que je ferai différemment demain.
