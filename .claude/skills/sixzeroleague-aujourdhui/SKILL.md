---
name: sixzeroleague-aujourdhui
description: Six Zero League — que faire aujourd'hui : plan du jour depuis gold.sz_agenda et le calendrier frais. Pour tout « que faire », « reprenons » ou plan du soir.
---

# Six Zero League — que faire aujourd'hui

Sources : `gold.sz_agenda` et `gold.sz_daily_alerts` (`sql/gold/015_sz_agenda.sql`), calendrier officiel `silver.sz_schedule` (endpoint `/seasons/current`), derniers briefs `outputs/sixzeroleague/briefs/`. Rythme : skill sixzeroleague-communaute § 1 (ligue 13:00 et 21:00, coupe ~17:00, cycle réglé chaque soir après 21:00, annonces closes au coup d'envoi suivant [Dev chat]).

## Garde-fou obligatoire (2026-11-02, règle apprise 69 : plan faux lu d'un calendrier périmé)
0. AVANT toute réponse : `select round, opponent, venue, kickoff_paris, status, captured_at from silver.sz_schedule where i_play and competition in ('league','cup') order by scheduled_at limit 6`, puis le registre `outputs/sixzeroleague/fait-*.md` du jour et de la veille. Si `captured_at` a plus de 12 h : première et seule ligne = « exporte le calendrier (League) », rien d'autre avant. Le match à préparer = le prochain `pending` dont `kickoff_paris` est encore à venir aujourd'hui ; jamais le lendemain. Les libellés de `gold.sz_agenda` et `sz_daily_alerts` ne se reprennent jamais tels quels. Victoire sur tapis vert (forfait) : ni export de match ni agent Match.

## Méthode (coût minimal : pas d'agent, deux requêtes)
0. **Avant toute requête et avant le premier rendu du plan** : charge le skill `deja-fait` et lis `outputs/sixzeroleague/fait-AAAA-MM-JJ.md` du jour ; ce qui est fait ne sort pas du plan.
0 bis. **Vues à jour** : `python -I pipelines/rafraichir_avant_soir.py --attendre` (150 s au plus) ; si la réponse n'est pas « à jour », le plan sort quand même, avec l'heure du dernier rafraîchissement.
1. `select day_label, at_time, category, action from gold.sz_agenda` puis `select priority, category, alert from gold.sz_daily_alerts order by priority` via `python -I pipelines/sql.py` (ou connecteur `Supabase`, `project_id = smkariminvfityondmmc`).
2. L'utilisateur agit **maintenant**, quand il demande : donne les actions du jour, sans « ce soir » ni liste horodatée (un match de 13:00 ou 17:00 se prépare la veille). « Après un match » seulement quand l'action en dépend vraiment.
3. Pour chaque action, ajoute le détail concret du dernier brief concerné, sans relancer d'agent : composition (`*-tactique.md`), enchères (`*-transferts.md`), fiche d'entraînement (`*-entrainement.md`), sponsor et infrastructures (`*-finances.md`), conseils ouverts `C-nnn` (`outputs/sixzeroleague/learnings.md`).
4. Un brief de plus de 2 jours sur un sujet du soir (une saison dure 9 à 11 jours) : dis-le et propose l'agent.
5. Si `silver.sz_schedule.captured_at` a plus de 24 h, l'agenda peut être faux : demande l'export de la page League.

## Règles de l'utilisateur (2026-10-25)
- **Compo du prochain match = première ligne du plan (correction du 2026-10-31)** : si un match a lieu demain (ou si aucun n'est encore joué dans la nouvelle saison), la première ligne Composition nomme le match (journée, adversaire, domicile/extérieur, heure) et donne la saisie complète : réglages lus dans `gold.sz_saisie_reglages` (formations, places, direction, agressivité : JAMAIS recopiés d'un ancien brief) puis poste par poste dans `gold.sz_saisie_tactique`, même si elle est identique à celle en place : l'utilisateur ne peut agir que le jour même. Jamais « rien à faire » quand un match tombe le lendemain. Une saisie unique reste valable pour plusieurs matchs d'affilée tant qu'aucun joueur ne change, mais je la rappelle et la contrôle (blessés, suspendus) chaque jour de match.
- Aucune action « après le match » (export de match, Finances, Entraînement post-cycle) dans la liste : je la demande une fois le match joué.

## Format de réponse
- **Pas d'heures** : l'utilisateur fait tout quand il peut ; un match raté n'est pas grave. Écris « Aujourd'hui : » puis **au plus 6 puces simples** dans l'ordre logique (exports, tactique des prochains matchs, agents), sans `HH:MM`, sans « avant », « après » ni « il est … ».
- Puis les alertes de priorité 1, une ligne chacune.
- Termine par « Exports du jour : … ».
- Pas de règle de jeu sans source ; pas de recommandation nouvelle : seulement ce que les briefs ont validé. Si une décision manque, propose l'agent.
