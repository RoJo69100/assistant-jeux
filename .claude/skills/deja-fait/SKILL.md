---
name: deja-fait
description: AVANT tout plan ou « que faire » : vérifie ce qui est déjà fait (exports en base, briefs du jour, réglages, déclarations de l'utilisateur) pour ne jamais redemander une action accomplie.
---

# Déjà fait — ne jamais redemander

L'utilisateur déteste qu'on lui redemande ce qu'il a déjà fait. Avant toute liste d'actions, je vérifie, jeu par jeu, et je ne garde que le reste à faire.

## 1. Registre de ce que l'utilisateur dit avoir fait
- Fichier : `outputs/<jeu>/fait-AAAA-MM-JJ.md` (créé au premier ajout du jour). Une ligne par action : `- [HH:MM UTC] <action> — source : <déclaré par l'utilisateur | vérifié en base>`.
- Dès que l'utilisateur écrit « j'ai fait / j'ai exporté / j'ai réglé … », j'ajoute la ligne (Edit/Write), puis je vérifie quand c'est possible (§ 2).
- **Clé obligatoire** (lue par `pipelines/aujourdhui.py` sur les 7 derniers registres) : chaque ligne porte `[clé=<écran ou match>]` juste après l'heure, ex. `- [10:34 UTC] [clé=Garden City 09/11] Saisie de l'amical …` ou `- [10:10 UTC] [clé=Personnel] Export Personnel …`. Écran = nom exact de l'écran de `gold.bv_exports_state` (valable le jour même seulement, la base fait foi ensuite). Match = adversaire suivi de la date du match `JJ/MM` (sans date : valable 7 jours). Une ligne « reste à corriger / à faire » ne porte jamais de clé. Sans clé, l'ancienne correspondance par mots reste en repli.
- Une action déclarée mais non vérifiable (réglage d'écran absent de la base) reste notée **faite** : je ne la redemande pas ; je dis seulement « non vérifiable en base » une fois.

## 2. Vérifications (une requête chacune, colonnes choisies, `LIMIT`)
| Action | Preuve |
|---|---|
| Export reçu | `bronze.raw_pages` : `max(captured_at)` par `page_type` pour `game = '<jeu>'` depuis minuit (heure de Paris) |
| Match exporté et analysé | `silver.*_matches` du match **et** `outputs/<jeu>/briefs/AAAA-MM-JJ-match.md` |
| Tactique / preset réglé | `silver.*_tactics` (Six Zero) ; BasketVibe : brief tactique du jour + export Preview |
| Entraînement réglé | `silver.*_training_plan`, `silver.sz_role_training` du jour |
| Infrastructure achetée | `silver.sz_infrastructure_levels` : niveau actuel du jour |
| Agent déjà passé | `outputs/<jeu>/briefs/AAAA-MM-JJ-<agent>.md` existe et est plus récent que le dernier export concerné |
| Veille faite | `outputs/<jeu>/veille/etat.md` (date « lu jusqu'au ») |

## 3. Règle de décision
1. Pour chaque action candidate : preuve trouvée (§ 2) ou ligne du registre (§ 1) → **ne pas la proposer** ; je l'inscris dans une ligne « Déjà fait » (jamais en demande).
2. Un agent n'est relancé que si un export **plus récent que son brief** est arrivé (nouveau match, nouveau relevé d'équipe, blessure ou suspension nouvelle) ; je dis lequel.
3. Une action n'est reproposée que si le fait a changé depuis (nouveau match, nouveau cycle) ; j'écris alors ce qui a changé.
4. En cas de doute entre « fait » et « pas fait », je cherche une preuve en base ou dans les briefs avant de poser une question ; je ne demande à l'utilisateur qu'en dernier recours.

## 4. Sortie
Toujours en deux blocs courts : **Déjà fait** (liste, avec la preuve en deux mots) puis **Reste à faire** (tableau action / dépend de, sans horaires). Si le reste à faire est vide, je le dis en une phrase.
