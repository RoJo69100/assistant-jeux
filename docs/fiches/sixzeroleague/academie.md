# Six Zero League — fiche Académie U18

Lue par l'agent `academie` après `commun.md`. Case E9 de la checklist SixZero League.

## Skills à lire
- `.claude/skills/sixzeroleague-entrainement/SKILL.md` (§ Académie U18, § L'âge)
- `.claude/skills/sixzeroleague-club/SKILL.md` (§ Infrastructures : Youth Academy)
- `.claude/skills/sixzeroleague-joueurs/SKILL.md` (compétences clés par rôle, retraite)

## Règles propres au jeu (skill entraînement § Académie U18)
1. 2 prospects fixes jusqu'à ce qu'on en signe un ; nouveau choix toutes les 8 journées de ligue ; signature à 18 ans, compétences tirées au niveau actuel de l'académie.
2. Compétences dévoilées avant signature selon le niveau de l'académie ; monter le niveau pendant une offre en dévoile plus sur les 2 mêmes prospects.
3. Effectif de 30 au maximum. L'académie sert surtout à remplacer les retraités.
4. Ni test payant, ni jauge, ni investissement hebdomadaire : ne reprends pas la méthode BasketVibe.

## Données
- `silver.sz_u18` : `available`, `squad_full`, `rounds_until_next_pick`, `prospects` (JSON : rôle, compétences dévoilées).
- `silver.sz_infrastructure_levels` (Youth Academy) : niveau actuel, coût du suivant.
- `silver.sz_players` : rôles sans relève, joueurs proches de la retraite (`retiring`, âge).

## Livrable
1. **Prospect à signer** (ou attendre) : rôle, compétences dévoilées comparées aux compétences clés du rôle, besoin de l'effectif.
2. **Youth Academy** : monter maintenant ou non (coût, compétences dévoilées en plus, effet sur les prochains prospects).

## Sortie propre au jeu
- Si `silver.sz_u18.day` est périmé ou si `rounds_until_next_pick` est arrivé à 0, demande l'export de la page Équipe → U18.
