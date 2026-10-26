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

## Règles de données et de chiffrage (ajoutées le 2026-10-24)
- **Solde réel** = `silver.sz_finances.balance` (dernier jour), pas le `closing_balance` de `gold.sz_finance_cycles` : un achat d'infrastructure fait après le règlement n'apparaît que dans `since_last_report` (le 2026-10-24, 6 645 affiché, 3 045 réel après Youth Academy 3 -> 4 à 3 600 €). Toujours lire `current_level` avant de dire « monter ».
- Prochain choix : compare `rounds_until_next_pick` au nombre de matchs joués par nous (`silver.sz_standings.played`), pas à la journée en cours ; ne pas annoncer une journée sans ce calcul.
- Les compétences du prospect se tirent à la signature au niveau de l'académie : acheter le niveau **avant** de signer, pas après.
- `weekly_maintenance` = entretien par cycle (2 journées) ; 9 cycles par saison. Coût multi-saisons = achat + supplément d'entretien x 9 x saisons.
- Gain d'un niveau d'académie : moyenne supposée 9 + 1,5 x niveau par compétence (tirage uniforme **supposé**, un seul cas Dupont ; à confirmer avec les prospects réellement signés). Training Facilities : l'effet d'un niveau est de +0,06 de rendement (supposé linéaire sur les points gagnés).
- Autres clubs : l'API ne donne ni infrastructures ni compétences (overall nul), seulement nom, note, âge, rôle, retraite. Toute comparaison de niveau d'infrastructure entre clubs est **non mesurable** tant qu'une page d'un rival n'affiche pas ces niveaux (à vérifier à l'écran). Pour âge et rôles : ouvrir `/teams/<id>/players` des 9 clubs de la ligue.
- Tirage d'un prospect cohérent avec un **milieu de plage** : niv. 5 = 16,5 ; 7 = 19,5 ; 9 = 22,5 ; 10 = 24 (exact). Témoins : Stoik niv. 10 « tirage moyen 24 » (C:0e6ced), Squidward niv. 7 « 19 et 23 », pierrottingchrist_29708 niv. 7-8 « vers 20 » ; Fournier (niv. 5) 17. **Hypothèse (4 observations), pas une règle.** Retard mesuré contre les autres clubs : niv. 5 contre 9-10 = **+6 à +7,5 points par compétence en moyenne par prospect** ; chiffrer toute montée avec les coûts cumulés (`upgrade_cost_from_current` est cumulé : depuis le niv. 5, niv. 8 = 18 900 €, à confirmer à l'écran). [Com chat, C:6aa782, 0e6ced ; D:L258-265 ; SQL ; V-20261026-19]

## Livrable
1. **Prospect à signer** (ou attendre) : rôle, compétences dévoilées comparées aux compétences clés du rôle, besoin de l'effectif.
2. **Youth Academy** : monter maintenant ou non (coût, compétences dévoilées en plus, effet sur les prochains prospects).

## Sortie propre au jeu
- Si `silver.sz_u18.day` est périmé ou si `rounds_until_next_pick` est arrivé à 0, demande l'export de la page Équipe → U18.
