# Hockey Nation — fiche Académie (draft, U17, U21)

Lue par l'agent `academie` après `commun.md`.

## Skills
`hockeynation-draft-scouting`, `hockeynation-joueurs`, `hockeynation-contrats-finances` (§ Jeunes : ELC et Farm).

## Données
- `gold.hn_draft_board` (toutes les classes exportées, talents vs poste, état du scouting), `silver.hn_draft_picks` (nos choix et pré-instructions).
- `silver.hn_players` filtré `team_level in ('U17','U21')`, `gold.hn_player_fit`.
- `gold.hn_daily_alerts` (U21 de 21 ans sans contrat).

## Livrable
1. **Draft** (jour 63) : 3 cibles par choix, repli, limites de position, talents à l'appui ; ligues de nos choix venus d'autres équipes à scouter.
2. **U21** : par joueur de 21 ans, ELC, contrat Farm ou départ ; candidats à l'ELC après la fenêtre I.
3. **U17** : nos draftables (tout visible) et ceux à garder via la draft.
4. **Import Draft** (jours 49-55) : le meilleur des 6 révélés, talents vs poste.
