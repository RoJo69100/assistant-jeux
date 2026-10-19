---
name: sixzeroleague-aujourdhui
description: Six Zero League — « que faire aujourd'hui / ce soir » : plan du soir (tactique avant les matchs, exports avant et après 21:00, matchs du lendemain à préparer la veille, agents à lancer) et alertes du jour (blessés, rôle sans remplaçant, finances, sponsor, académie, exports en retard). À utiliser pour « que faire sur SixZero », « le plan du soir », « le brief » de Six Zero League.
---

# Six Zero League — que faire aujourd'hui

Sources : `gold.sz_agenda` et `gold.sz_daily_alerts` (`sql/gold/015_sz_agenda.sql`), calendrier officiel `silver.sz_schedule` (endpoint `/seasons/current`), derniers briefs `outputs/sixzeroleague/briefs/`. Rythme : skill sixzeroleague-communaute § 1 (ligue 13:00 et 21:00, coupe ~17:00, cycle réglé chaque soir après 21:00, annonces closes au coup d'envoi suivant [Dev chat]).

## Méthode (coût minimal : pas d'agent, deux requêtes)
1. `select day_label, at_time, category, action from gold.sz_agenda` puis `select priority, category, alert from gold.sz_daily_alerts order by priority` via `mcp__supabase__execute_sql`.
2. L'utilisateur n'agit que **le soir après 19:00** : l'agenda le respecte déjà (un match de 13:00 ou 17:00 se prépare la veille au soir, son export se fait le soir). Ne donne jamais de liste sur la journée.
3. Pour chaque action, ajoute le détail concret du dernier brief concerné, sans relancer d'agent : composition (`*-tactique.md`), enchères (`*-transferts.md`), fiche d'entraînement (`*-entrainement.md`), sponsor et infrastructures (`*-finances.md`), conseils ouverts `C-nnn` (`outputs/sixzeroleague/learnings.md`).
4. Un brief de plus de 2 jours sur un sujet du soir (une saison dure 9 à 11 jours) : dis-le et propose l'agent.
5. Si `silver.sz_schedule.captured_at` a plus de 24 h, l'agenda peut être faux : demande l'export de la page League.

## Format de réponse
- **Pas d'heures** : l'utilisateur fait tout le soir, quand il peut ; un match raté n'est pas grave. Écris « Ce soir : » puis **au plus 6 puces simples** dans l'ordre logique (exports, tactique des prochains matchs, agents), sans `HH:MM`, sans « avant », « après » ni « il est … ».
- Puis les alertes de priorité 1, une ligne chacune.
- Termine par « Exports de ce soir : … ».
- Pas de règle de jeu sans source ; pas de recommandation nouvelle : seulement ce que les briefs ont validé. Si une décision manque, propose l'agent.
