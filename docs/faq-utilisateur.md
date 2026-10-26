# FAQ — travailler avec Claude (tous les jeux)

À interroger : « FAQ : [ta question] ». Claude répond depuis ce fichier et l'enrichit quand une question n'y est pas (une ligne, datée). Attentes de fond : `docs/attentes/attentes.md` ; config d'un jeu : `docs/attentes/jeux/<jeu>.yaml`.

## La routine la plus rapide (2026-10-26)
| Étape | Toi | Claude |
|---|---|---|
| 1. Le soir | « Demain je peux / je ne peux pas » | Ne parle que de ce que tu peux faire (R-1) |
| 2. Exports | **Tous les exports de tous les jeux d'un coup**, puis « exports faits » | Vérifie l'arrivée en base, jeu par jeu (une requête), note dans `fait-…` |
| 3. Tour rapide | rien | Un tableau par jeu, tiré du SQL (agenda, alertes, delta), **sans agent** : ce qui est à faire maintenant |
| 4. Analyse | rien | Agents seulement pour les jeux où un événement l'exige (défaite, marché, entraînement, engagement), **un jeu à la fois**, selon les dépendances de la config |
| 5. Saisie | Tu saisis dans le jeu, dans l'ordre de l'écran | Rend la saisie dans l'ordre de l'écran (R-4) |
| 6. Fin | « Rétro » si quelque chose t'a gêné | Écrit la nouvelle attente dans `attentes.md`, commit, `/clear` |

**Pourquoi tout exporter d'un coup ?** Tu n'ouvres chaque jeu qu'une fois, et le tour rapide en SQL coûte peu pour tous les jeux ensemble. L'analyse reste jeu par jeu : mélanger plusieurs jeux dans les agents fait exploser les tokens et les erreurs.

**Quels exports pour chaque jeu ?** Demande « quels exports aujourd'hui ? » : Claude lit `exports` et `rythme` de chaque config et ne cite que ceux qui manquent.

## Réglages
| Tâche | Réglage |
|---|---|
| Exports, tour rapide, commits | `/effort low` + `/model sonnet` |
| Agents d'analyse | `/effort medium` + `/model sonnet` (Claude le demande avant de lancer) |
| Conception (nouveau jeu, vues SQL, refonte) | `/model opus`, retour à Sonnet après le commit |

## Quand tu vois un problème
| Situation | Dis ceci | Ce que Claude fait |
|---|---|---|
| Erreur de fait | « Erreur : [ce qui est faux], preuve : [ce que tu vois] » | Revérifie en base, corrige, cherche les autres lignes touchées |
| Il redemande ce que tu as fait | « Déjà fait : [quoi] » | Le note dans `fait-…`, ne le redemande plus (R-7) |
| Réponse floue, « si », alertes | « Aucun flou » | Joueur par joueur, chiffres, une action par ligne (R-2, R-5) |
| Trop long, infos parasites | « Synthèse » | Un tableau par jeu, maintenant ou demain seulement (R-1, R-6) |
| Une remarque qui vaut pour tous les jeux | La dire une fois, sur n'importe quel jeu | Elle va dans `attentes.md` (global par défaut), pas dans le jeu |
| Une particularité d'un jeu | « Spécificité [jeu] : … » | Elle va dans la config du jeu |
| Conseil échoué | « C-nnn a échoué : [résultat] » | `learnings.md`, autre levier (A-7) |
| Colère ou répétition | « Rétro » | Agent `retro`, nouvelle attente dans `attentes.md` |

## Nouveau jeu
1. `/model opus`. 2. Claude copie `_modele.yaml` en `<jeu>.yaml` et le remplit depuis le manuel et le Discord (veille intégrale). 3. Tu fais un export de chaque page ; Claude complète `ecrans` et `exports`. 4. Retour à Sonnet.
