---
name: hardwood-aujourdhui
description: Hardwood — « que faire aujourd'hui » : prochain match à l'heure de Paris, depth chart à corriger, coach à recruter (fenêtre des assistants), points de recrutement à dépenser, exports en retard. Deux requêtes sur les vues gold, sans agent. À utiliser pour « que faire sur Hardwood », « le plan du jour », « le brief » de Hardwood.
---

# Hardwood — que faire aujourd'hui

Sources : `gold.hw_today`, `gold.hw_daily_alerts`, `gold.hw_exports_state` (`sql/gold/043_hw_gold.sql`), registre `outputs/hardwood/fait-AAAA-MM-JJ.md`, derniers briefs `outputs/hardwood/briefs/`. Règles : skills `hardwood-regles`, `hardwood-tactique`, `hardwood-recrutement`. Résumé : `docs/fiches/hardwood/resume.md`.

## Méthode (pas d'agent)
1. Charger `deja-fait`, lire le registre `fait-` du jour.
2. `select * from gold.hw_today` puis `select niveau, categorie, alerte from gold.hw_daily_alerts`.
3. Pour une alerte Composition : afficher `gold.hw_depth_suggest` en entier (PG, SG, SF, PF, C × rangs), jamais « corrige le depth chart ».
4. Pour une alerte Personnel : `gold.hw_coach_board` et trancher un coach nommé (un seul recrutement par jour réel).
5. Pour une alerte Académie/Draft : `gold.hw_recruit_board where verdict = 'cible' order by rang limit 10` et dire où mettre les points.
6. Un export 🟧/🟥 dans `gold.hw_exports_state` : une ligne « fais l'export X ». Les walk-ons ne s'exportent jamais.

## Format
Un tableau : priorité (🟥 URGENT / 🟧 IMPORTANT / 🟩 SUIVI) · catégorie · action « fais X » (joueur, coach ou recrue nommé). Puis une ligne « Prochain match : <adversaire>, <heure Paris> ». Aucune heure dans les actions, rien pour demain.
