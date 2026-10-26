# Six Zero League — fiche Veille

Lue par l'agent `veille` après `commun.md`. Sources : chat global (base + `data/chat/sixzeroleague/`), Discord (`data/discord/SixZeroLeague/`, y compris le devlog des mises à jour 0.5.7 à 0.6.0), wiki.

## Skills à lire
- tous les `.claude/skills/sixzeroleague-*/SKILL.md` concernés par les messages lus

## Règles propres au jeu
1. Hiérarchie : wiki `[W:Rubrique]` > développeur `[Dev chat]` (Gazelle) > joueurs `[Com chat, pseudo]`.
2. Delta : `etat.md` donne une date par source (chat jeu, Discord #chat, Discord #dev-log, wiki). Les exports de `data/chat/sixzeroleague/` et `data/discord/SixZeroLeague/` qui ne sont pas listés dans `etat.md` sont à lire en entier ; la base reprend le chat du jeu (100 derniers messages par canal), donc vérifier les doublons par `createdAt`. Le chat collé le 2026-10-18 est déjà intégré au skill communauté.
3. Coût : lis tous les messages du développeur ; pour les joueurs, seulement ceux qui touchent une règle, un horaire ou un chiffre.
4. **`outputs/sixzeroleague/veille/connaissance.md` est tenu à jour à chaque export (section « Delta ») et lu par tous les agents avant toute conclusion « aucune source »** (règle du 2026-10-26 : les agents écrivaient « aucune source » alors que l'info était dans le Discord ou le chat). Il indexe par thème tout ce que disent Gazelle (développeur), le wiki et les joueurs, avec source, date, auteur et statut (CONFIRMÉ / COMPLÉTÉ / CONTREDIT ⚠️ / EN DOUTE). Alias connu : « Urban Fox » = Gazelle.

## Données
- `silver.sz_api` avec `endpoint = '/chat/messages'` (chat global capturé par le script ; pas encore de vue silver dédiée) : lis le JSON `body` en SQL, colonnes choisies et `LIMIT`.
- Wiki : `bronze.raw_pages` (`game = 'sixzeroleague'`, `page_type = 'app_wiki'`). Ne le relis que si une nouvelle version a été capturée, et seulement les rubriques modifiées (exception au « jamais bronze » : pas de vue silver du wiki).

## Livrable
`outputs/sixzeroleague/veille/AAAA-MM-JJ.md` : résumé, propositions `V-AAAAMMJJ-n` (skill visé, texte prêt à coller avec sa source, type ajout / correction / contradiction ⚠️, impact sur les agents ou les vues SQL, priorité), à surveiller. Puis mise à jour de `etat.md`.

## Sortie propre au jeu
- Si aucun nouveau message n'est en base, demande d'ouvrir le chat du jeu avec le script actif (ou de coller le chat).
