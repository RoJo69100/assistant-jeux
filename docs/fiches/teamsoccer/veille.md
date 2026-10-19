# Team Soccer — fiche Veille

Lue par l'agent `veille` après `commun.md`. Case E10 de la checklist Team Soccer. Pas de Discord : la veille lit les **annonces de l'admin** (page Communauté) et le **forum**.

## Skills à lire
- `.claude/skills/teamsoccer-communaute/SKILL.md` (chronologie des changements, contradictions, bugs récurrents)
- les autres `.claude/skills/teamsoccer-*/SKILL.md` touchés par les messages lus

## Règles propres au jeu
1. Hiérarchie : guide `[G]` > Admin-Dev et Admin-PIPO68 (`is_admin`) `[F:date pseudo]` > modérateurs (`admin_level` 2 à 4) et joueurs (avis).
2. Les règles changent souvent et les annonces les annoncent : lis **toutes** les annonces nouvelles et tous les messages des administrateurs ; pour les autres, seulement ceux qui touchent une règle, un horaire ou un chiffre.
3. Delta : `outputs/teamsoccer/veille/etat.md` (date « lu jusqu'au » ; le créer au premier passage). Lu jusqu'au 2026-10-19 pour le forum (skill communauté) ; les 20 annonces anglaises du 2026-08-18 au 2026-10-18 ont été captées le 2026-10-19 et **pas encore intégrées** aux skills (dont formes, physique, académie, blessures, Haute Performance) : premier passage à faire sur elles.

## Données
- `silver.ts_news` : `news_id`, `created_at`, `title`, `content` (HTML léger).
- `silver.ts_forum_posts` : `created_at`, `username`, `is_admin`, `admin_level`, `thread_title`, `content`. Filtre `created_at > <lu jusqu'au>`, colonnes choisies, `LIMIT`.
- Guide : `bronze.raw_pages` (`page_type = 'dashboard_help'`, `source = 'dom'`), seulement si une nouvelle capture existe.

## Livrable
`outputs/teamsoccer/veille/AAAA-MM-JJ.md` : résumé, propositions `V-AAAAMMJJ-n` (skill visé, texte prêt à coller avec sa source, type ajout / correction / contradiction ⚠️, impact sur les agents ou les vues SQL, priorité), à surveiller. Puis mise à jour de `etat.md`. Ne modifie jamais un skill toi-même.

## Sortie propre au jeu
- Si rien de nouveau n'est en base, demande d'ouvrir la page Communauté et le forum avec le script actif.
