---
name: basketvibe-aujourdhui
description: « Qu'est-ce que je fais aujourd'hui sur BasketVibe ? » — liste courte et horodatée des actions du jour (et de demain matin si on est le soir) : presets et focus à régler avant les verrouillages, enchères qui se terminent, entraînement à sauvegarder, exports à faire, amicaux à programmer. À charger dès que l'utilisateur demande quoi faire aujourd'hui, ce soir, demain matin, ou « mes tâches BasketVibe ».
---

# BasketVibe — que faire aujourd'hui

Sources : `gold.bv_agenda` (calcul SQL de l'agenda) + les derniers briefs des agents (`outputs/basketvibe/briefs/`). Rythme de la semaine : skill basketvibe-saison [M§1.3]. Routine d'export de l'utilisateur : mémoire (après chaque match ; dimanche après 04:00 : Entraînement + Finances + Personnel).

## Méthode (coût minimal : pas d'agent, quelques requêtes)
1. Heure actuelle (Paris). Lis `select * from gold.bv_agenda where day <= current_date + 1` via `mcp__supabase__execute_sql`. Garde les actions d'aujourd'hui encore à venir ; après 18:00, ajoute celles de demain avant 10:00.
2. Pour chaque action, ajoute **le détail concret** pris dans le dernier brief concerné (sans relancer d'agent) :
   - ligue : cinqs, consignes et focus défensif → dernier `*-tactique.md` (fiche de saisie, mise à jour éventuelle en bas du brief) ;
   - amical : preset amical et test du jour → même brief (plan des amicaux) ;
   - enchères qui se terminent aujourd'hui ou cette nuit : tableau ACTIONS du dernier `*-transferts.md` (montant maximum, heure limite). `gold.bv_agenda` ne connaît que **mes ventes**, pas mes enchères d'achat : lis-les dans le brief ;
   - entraînement (samedi soir) : fiche de saisie du dernier `*-entrainement.md` ;
   - personnel ou finances : actions datées du dernier `*-finances.md`.
3. Vérifie la fraîcheur : si un brief a plus de 3 jours pour un sujet du jour (ex. tactique avant un match de ligue), dis-le et propose de relancer l'agent concerné.
4. Signale les exports attendus que je n'ai pas reçus (ex. page du dernier match joué absente de `silver.bv_matches`).

## Format de réponse
- **Au plus 8 lignes**, triées par heure : `HH:MM — action — détail (source)`.
- Mets en tête ce qui a une **heure limite** (verrouillage, fin d'enchère).
- Termine par une ligne « Exports à faire aujourd'hui : … ».
- Pas de règle de jeu sans source ; pas de recommandation nouvelle : seulement ce que les briefs ont déjà validé. Si une décision manque, propose l'agent à lancer.
