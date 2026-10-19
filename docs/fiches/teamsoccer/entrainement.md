# Team Soccer — fiche Entraînement

Lue par l'agent `entrainement` après `commun.md`. Case E5 de la checklist Team Soccer.

## Skills à lire
- `.claude/skills/teamsoccer-entrainement/SKILL.md` (gymnase, âge, physique, Forme et intensité, entraîneurs)
- `.claude/skills/teamsoccer-joueurs/SKILL.md` (compétences clés par poste, Forme)

## Règles propres au jeu
1. Une compétence et une intensité (0–100 %) par joueur ; **mise à jour le vendredi** : seul compte le réglage en place à ce moment [F:2026-07-20 PIPO68]. Verdict chaque vendredi soir (après l'export), réglage modifiable toute la semaine.
2. **Forme selon l'intensité** à chaque vendredi : 100 % −10, 90 % −6, 80 % −4, 70 % −2, 60 % 0, 50 % +6, ≤ 40 % +10 (30 ans et plus : −2 de plus à 80–100 %) [F:2026-06-27 Admin-Dev]. Arbitre progrès contre Forme en regardant les matchs de la semaine suivante.
3. **Physique** : depuis fin septembre 2026 il ne monte plus seul, il faut l'entraîner [F:2026-10-09 PIPO68]. **Endurance ≤ 30 → seul l'entraînement d'Endurance est possible** [P:Entraînement].
4. Âge : pleins gains à 16–17 ans, moins jusqu'à 27, rien ou perte dès 28. Inutile de pousser l'intensité d'un joueur de 28 ans et plus pour la technique.
5. Les barèmes chiffrés du forum datent de la BETA (le multiplicateur a été réduit le 2026-09-13) : **mesure les gains réels** avant d'en tirer une règle.
6. Entraîneur : niveau 1 (« poor ») pour les deux clubs ; le niveau 2 coûte 1 000 000 $, impossible tant que le solde est négatif [skill entraînement, club].

## Données
- `silver.ts_training` : par joueur `training_type`, `intensity`, `last_trained_type`, progression fractionnaire (`skill_progress`, `stamina_progress`, `pace_progress`) et dernier gain (`last_change`, `stamina_last_change`, `pace_last_change`).
- `gold.ts_player_progress` : écarts entre deux relevés (`d_ovr`, `d_forme`, `d_<compétence>`), avec le réglage actuel. Vide tant qu'il n'y a qu'un relevé (2026-10-19).
- `silver.ts_players` : `age`, `forme`, compétences ; `gold.ts_upcoming` pour les matchs de la semaine.

## Livrable
1. **Fiche de saisie** par club : joueur → compétence, intensité, garder ou changer.
2. **Verdict** du vendredi : gains mesurés par âge et intensité, variation de Forme, joueurs à reposer.
3. Alerte : Endurance ≤ 35, Forme < 60, joueurs de 28 ans et plus encore à haute intensité.

## Sortie propre au jeu
- Sans relevé postérieur au dernier vendredi, demande l'export des pages Effectif et Entraînement des deux clubs.
