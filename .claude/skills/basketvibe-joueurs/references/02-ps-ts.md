## PS / TS [M§2.2]
Seules les 8 compétences comptent (ni forme, ni fatigue, ni taille, ni potentiel). Poids de chaque compétence par poste (le premier libellé du poste sur la carte du joueur) :

| Compétence | PG | SG | SF | PF | C |
|---|---|---|---|---|---|
| Deux points | 15 | 15 | 15 | 15 | 15 |
| Trois points | 15 | 15 | 15 | 10 | 10 |
| Passe | 15 | 10 | 10 | 10 | 10 |
| Dribble | 15 | 15 | 10 | 10 | 10 |
| Défense | 15 | 15 | 15 | 15 | 15 |
| Rebond | 5 | 5 | 10 | 15 | 15 |
| Athlétisme | 10 | 15 | 15 | 15 | 15 |
| Endurance | 10 | 10 | 10 | 10 | 10 |

- Le PS utilise les valeurs précises : il peut différer d'un point du calcul fait sur les chiffres arrondis [M§2.2].
- TS = moyenne du PS des 8 meilleurs du roster (blessés compris) [M§2.2].
- PS visible chez les autres clubs seulement quand le joueur est en vente [M§2.2]. Les compétences adverses apparaissent en tranches (0–20, 21–40, 41–60, 61–80, 81–99) [M§4].
- V-20261030-3 : le TS est recalculé une fois par jour [Dev 2026-09-03 05:27] **et aussi juste après un transfert réglé** [release-notes 2026-09-04] ; après une inscription, le TS du bot est régénéré [2026-09-06]. À vérifier dans `silver` au prochain transfert.
- [Obs] Nos données d'entraînement (`silver.bv_player_daily.*_exact`) donnent les valeurs précises. La valeur affichée = partie entière, vérifié sur 15 joueurs le 2026-10-16.

