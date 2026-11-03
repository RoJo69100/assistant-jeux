## Joueurs [R:Players]
- 14 compétences de 0 à 20 : attaque IS (tir intérieur), OS (tir extérieur, **et lancers francs**), Rng (portée), Fin (finition) ; défense Reb, IDef, PDef ; jeu IQ, Pass, Hnd, Drv ; physique Str, Spd, Sta. Plus taille, poids, envergure et détente, qui ne sont pas dans le SI.
- **Skill Index (SI)** = somme des compétences. **Potentiel** = mesure des plafonds, avec une part d'incertitude.
- Chaque compétence a une base et un plafond ; la valeur actuelle monte avec le **coaching** (surtout chez les jeunes) et **l'expérience** (chaque minute jouée, plus une base pour la présence à l'entraînement).
- **Valeurs affichées = estimation, jusqu'à ±20 % de la vraie valeur** ; elles se précisent avec les matchs et peuvent donc baisser à l'affichage sans vraie baisse.
- Pas de compétence cachée, mais des valeurs fixes cachées pèsent un peu sur certaines actions.
- Plafond de SI ≈ 14 × potentiel + 0 à 13 (pot 10 → 140-153) [D (confirmé par plusieurs joueurs, pas par Steve)] [A : tableau pot 9-17] ; table `silver.hw_ref_potential_caps`.
- **Compétences clés par poste [A]** : PG = IQ, Pass, Hnd, Spd ; SG = OS, Spd ; SF = OS, défense complète (IDef + PDef), Spd, plus grand que PG et SG ; PF et C = IS, Reb, grand. Un ancien juge « acceptable » une compétence clé à **13 ou plus** [A]. Note par poste : `gold.hw_player_pos_scores` (0,6 × moyenne des clés + 0,4 × SI/14, pondération [H]).
- Postes : le poste principal est celui où le joueur a le plus d'expérience, pas forcément son meilleur. Majuscule = poste maîtrisé, minuscule = en apprentissage ; on gagne l'expérience d'un poste en y jouant, exhibitions comprises.
- La taille et le physique changent en grandissant : la taille projetée n'est qu'une estimation.
- Déclin vers 30 ans : ne touche pas les joueurs universitaires.

