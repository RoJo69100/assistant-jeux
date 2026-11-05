---
name: teamsoccer-aujourdhui
description: Team Soccer — que faire aujourd'hui : plan du jour pour les deux clubs depuis l'agenda et les alertes. Pour tout « que faire », « reprenons » ou plan du soir.
---

# Team Soccer — que faire aujourd'hui

Sources : `gold.ts_agenda` et `gold.ts_daily_alerts` (`sql/gold/018_ts_agenda.sql`), prochains matchs `gold.ts_upcoming`, derniers briefs `outputs/teamsoccer/briefs/`, conseils ouverts `outputs/teamsoccer/learnings.md`. Rythme : skill teamsoccer-saison (lundi 00:05 finances, vendredi entraînement, 1 révélation d'académie par jour, un amical par semaine) ; composition enregistrée au moins 2 h avant le coup d'envoi [skill teamsoccer-match].

## Méthode (coût minimal : pas d'agent, deux requêtes)
0. **Avant toute requête et avant le premier rendu du plan** : charge le skill `deja-fait` et lis `outputs/teamsoccer/fait-AAAA-MM-JJ.md` du jour ; ce qui est fait ne sort pas du plan.
0 bis. **Vues à jour** : `python -I pipelines/rafraichir_avant_soir.py --attendre` (150 s au plus) ; si la réponse n'est pas « à jour », le plan sort quand même, avec l'heure du dernier rafraîchissement.
1. `select day_label, team, priority, category, action from gold.ts_agenda` puis `select priority, team, category, alert from gold.ts_daily_alerts order by priority, team` via `python -I pipelines/sql.py` (ou connecteur `Supabase`, `project_id = smkariminvfityondmmc`).
2. L'utilisateur n'agit que **le soir après 19:00** : l'agenda le respecte déjà (une limite de composition avant 19:00 — par exemple un match de 13:50 — tombe la veille au soir). Ne donne jamais de liste sur la journée.
3. Les jours de match viennent des données, pas de la règle « mardi et samedi » : Ben Ahmed Donkey joue le lundi et le jeudi à 19:30, Chomelix Cows le mardi et le samedi à 13:50 [Obs, `silver.ts_matches`, 2026-10-20].
4. Pour chaque action, ajoute le détail concret du dernier brief concerné, sans relancer d'agent : composition (`*-tactique*.md`), enchères (`*-transferts.md`), entraînement (`*-entrainement.md`), solde, stade et HPC (`*-finances*.md`), révélations (`*-academie.md`), conseils `C-nnn` ouverts.
5. Préparation au plus tôt (CLAUDE.md) : si les données utiles sont exportées, propose de préparer aussi les compositions des jours suivants (`gold.ts_upcoming`), avec « à refaire si : Forme, blessure, adversaire ».
6. Brief de plus de 3 jours sur un sujet du soir (la Forme change chaque vendredi) : dis-le et propose l'agent.
7. Si le calendrier (`matches`) a plus de 24 h dans `gold.ts_daily_alerts`, l'agenda peut être faux : demande l'export de la page Matchs des deux clubs.
8. « Match de type inconnu » (ni ligue, ni coupe, ni amical dans l'API, souvent la nuit) : ne devine pas ce que c'est ; demande de regarder la page Matchs.

## Format de réponse
- **Format validé le 2026-10-31** : un tableau par club, une ligne par joueur, colonnes `Emplacement | Joueur | Ultra déf. | Défensive | Médiane | Offensive | Finition` (consigne + cible → milieux / attaquants / défenseurs / ailiers). L'emplacement est le poste exact de l'écran : **DL / DC / DR** en défense, **ML / MC / MR** au milieu (jamais « DEF » ou « MIL »), déduit de l'ordre des emplacements de `player_positions` (1-4 = DL, DC, DC, DR ; milieu 5-7 = ML, MC, MR ou 5-8 = ML, MC, MC, MR), à vérifier une fois sur l'écran. **Toutes les colonnes remplies** (aucune cellule « — » : Ultra déf. = Dégager, Défensive = Passer → cible, Finition = Tirer pour tous, GB Dégager partout), lues dans `player_orders` du match après l'export de l'utilisateur ; je signale les écarts et un joueur à la fois titulaire et sur le banc. Banc de 6 qui couvre GB, DC, MC, AC. Adversaire inconnu : une ligne.
- **Pas d'heures** : écris « Ce soir : » puis **au plus 6 puces simples**, dans l'ordre logique (exports, compositions des prochains matchs, académie, agents), en nommant le club, sans `HH:MM`, sans « avant », « après » ni « il est … ».
- Puis les alertes de priorité 1, une ligne chacune.
- Pas de ligne « Exports de ce soir » ni de « puis / après » ; un export figure dans le tableau seulement s'il est à faire maintenant.
- Une composition à enregistrer se rend **complète** : formation, style, onze par emplacement 0–10 dans l'ordre de l'écran (GB, DEF, MIL, ATT), consignes des 5 zones par joueur, banc de 6, ligne « Remplacements programmés » (aucun + raison, ou minute / sortant / entrant). Chaque « Passer » porte sa cible obligatoire (défenseurs / milieux / attaquants). Jamais le onze seul. Cows ET Donkey (R-12).
- Pas de règle de jeu sans source ; pas de recommandation nouvelle : seulement ce que les briefs ont validé. Si une décision manque, propose l'agent (Tactique, Match, Académie, Finances, Entraînement, Transferts), avec le jeu et le club dans la demande.
