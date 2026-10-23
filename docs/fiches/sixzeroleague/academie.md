# Six Zero League — fiche Académie U18

Lue par l'agent `academie` après `commun.md`. Case E9 de la checklist SixZero League.

## Skills à lire
- `.claude/skills/sixzeroleague-entrainement/SKILL.md` (§ Académie U18, § L'âge)
- `.claude/skills/sixzeroleague-club/SKILL.md` (§ Infrastructures : Youth Academy)
- `.claude/skills/sixzeroleague-joueurs/SKILL.md` (compétences clés par rôle, retraite)

## Règles propres au jeu (skill entraînement § Académie U18)
1. 2 prospects fixes jusqu'à ce qu'on en signe un ; nouveau choix toutes les 8 journées de ligue ; signature à 18 ans, compétences tirées au niveau actuel de l'académie.
2. Compétences dévoilées avant signature selon le niveau de l'académie ; monter le niveau pendant une offre en dévoile plus sur les 2 mêmes prospects.
2bis. Plage des compétences selon le niveau : 1-20 (niv. 1), 2-22 (niv. 2), 9-36 (niv. 9) [Com chat, 2026-10-20]. Formule min = niveau, max = 18 + 2 × niveau : **vérifiée le 2026-10-23 sur `silver.sz_infrastructure_levels` pour les niveaux 1 à 20** (niv. 20 = 20-58) ; confiance bonne. Le prospect étranger (2 % au niv. 5 à 9, 4 % au niv. 10, 6 % au 15, 8 % au 20 d'après les mêmes données) ne sert qu'aux futures sélections nationales [Dev chat, 2026-10-20].
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
