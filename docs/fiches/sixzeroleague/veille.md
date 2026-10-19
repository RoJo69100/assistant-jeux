# Six Zero League — fiche Veille

Lue par l'agent `veille` après `commun.md`. Pas de Discord pour ce jeu : la veille lit le **chat global** du jeu et les mises à jour du wiki.

## Skills à lire
- tous les `.claude/skills/sixzeroleague-*/SKILL.md` concernés par les messages lus

## Règles propres au jeu
1. Hiérarchie : wiki `[W:Rubrique]` > développeur `[Dev chat]` (Gazelle) > joueurs `[Com chat, pseudo]`.
2. Delta : `outputs/sixzeroleague/veille/etat.md` (date « lu jusqu'au » ; le créer au premier passage). Le chat collé le 2026-10-18 est déjà intégré au skill communauté.
3. Coût : lis tous les messages du développeur ; pour les joueurs, seulement ceux qui touchent une règle, un horaire ou un chiffre.

## Données
- `silver.sz_api` avec `endpoint = '/chat/messages'` (chat global capturé par le script ; pas encore de vue silver dédiée) : lis le JSON `body` en SQL, colonnes choisies et `LIMIT`.
- Wiki : `bronze.raw_pages` (`game = 'sixzeroleague'`, `page_type = 'app_wiki'`). Ne le relis que si une nouvelle version a été capturée, et seulement les rubriques modifiées (exception au « jamais bronze » : pas de vue silver du wiki).

## Livrable
`outputs/sixzeroleague/veille/AAAA-MM-JJ.md` : résumé, propositions `V-AAAAMMJJ-n` (skill visé, texte prêt à coller avec sa source, type ajout / correction / contradiction ⚠️, impact sur les agents ou les vues SQL, priorité), à surveiller. Puis mise à jour de `etat.md`.

## Sortie propre au jeu
- Si aucun nouveau message n'est en base, demande d'ouvrir le chat du jeu avec le script actif (ou de coller le chat).
