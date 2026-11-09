---
name: basketvibe-aujourdhui
description: BasketVibe — que faire aujourd'hui : plan du jour depuis gold.bv_agenda et les alertes, avec les exports en retard. Pour tout « que faire », « reprenons » ou plan du jour.
---

# BasketVibe — que faire aujourd'hui

Sources : `gold.bv_agenda` (calcul SQL de l'agenda) + les derniers briefs des agents (`outputs/basketvibe/briefs/`). Rythme de la semaine : skill basketvibe-saison [M§1.3]. Routine d'export de l'utilisateur : mémoire (après chaque match ; dimanche après 04:00 : Entraînement + Finances + Personnel).

## Méthode depuis le 09/11 : le script d'abord (Porte BasketVibe, critères PB1 à PB3 de `docs/refonte-v3/journal-aujourdhui.md`)
1. **Première action, avant toute requête et tout autre outil** : `python -I pipelines/aujourdhui.py basketvibe`. Le script lit lui-même le registre du jour, les vues gold, les briefs et la décision d'achat ouverte. Affiche sa sortie **telle quelle** : sans reformulation, sans tableau, sans ajout dans ses lignes.
2. **Complément, une ligne chacun, sous la sortie du script** (jusqu'à l'étape 5 du plan) :
   - (a) matchs joués depuis le dernier passage, résultat par `my_result` : `gold.bv_match_report` ; pour un match de ligue joué et non exporté, `silver.bv_fixtures` ;
   - (b) académie, seulement si un rapport est arrivé depuis le dernier passage ;
   - (c) aperçu adverse et brief tactique du prochain match de ligue ou de coupe : `gold.bv_saisie_adversaires` et dernier `*-tactique.md` ; sinon la ligne « brief manquant ».
3. **Hooks** : la réponse passe `forme.py` et `controle.py` sans que leurs règles changent. Si un hook rejette, corrige seulement la ligne rejetée et note le rejet dans le tableau « Rejets de hooks » du journal.
4. **Registre « déjà fait »** : ce que l'utilisateur déclare (export fait, réglage saisi) s'inscrit dans `outputs/basketvibe/fait-AAAA-MM-JJ.md` (skill `deja-fait`) ; le script le lit au passage suivant.
5. **Porte** : chaque jour, demande à l'utilisateur ses quatre lignes (verdict, il manquait, en trop, faux) et inscris-les telles quelles dans le tableau « Retours de la Porte » du journal, sans les interpréter.

## Ancienne méthode — remplacée par le script depuis le 09/11, utilisée seulement pour le complément ci-dessus (coût minimal : pas d'agent, quelques requêtes)
0. **Avant toute requête et avant le premier rendu du plan** : charge le skill `deja-fait` et lis `outputs/basketvibe/fait-AAAA-MM-JJ.md` du jour ; ce qui est fait ne sort pas du plan.
1. Heure actuelle (Paris) = la ligne « Heure de Paris » injectée à chaque message (hook `pipelines/heure_paris.py`) ou `python -I pipelines/heure_paris.py` ; jamais `date` du shell (UTC, 2026-11-07), ni `at time zone` par sql.py (bloqué par Cloudflare en https, 2026-11-07). Lis `select * from gold.bv_agenda where day <= current_date + 1` via `python -I pipelines/sql.py` (ou connecteur `Supabase`, `project_id = smkariminvfityondmmc`). Garde les actions d'aujourd'hui encore à venir ; après 18:00, ajoute celles de demain avant 10:00.
2. Pour chaque action, ajoute **le détail concret** pris dans le dernier brief concerné (sans relancer d'agent) :
   - ligue : cinqs, consignes et focus défensif → dernier `*-tactique.md` (fiche de saisie, mise à jour éventuelle en bas du brief) ;
   - amical : ligne Composition chaque jour (cinq de ligue à 0 minute, jeunes, agressivité 1 : plan du dernier brief) ; aucune donnée adverse ni Preview ni analyse (arbitrage 15) ; export de la page du match après coup ;
   - enchères qui se terminent aujourd'hui ou cette nuit : tableau ACTIONS du dernier `*-transferts.md` (montant maximum, heure limite). `gold.bv_agenda` ne connaît que **mes ventes**, pas mes enchères d'achat : lis-les dans le brief ;
   - entraînement (samedi soir) : fiche de saisie du dernier `*-entrainement.md` ;
   - personnel ou finances : actions datées du dernier `*-finances.md`.
3. Vérifie la fraîcheur : si un brief a plus de 3 jours pour un sujet du jour (ex. tactique avant un match de ligue), dis-le et propose de relancer l'agent concerné.
4. Signale les exports attendus que je n'ai pas reçus (ex. page du dernier match joué absente de `silver.bv_matches`). **Toujours** lire `select ecran, dernier_paris, age_h, statut from gold.bv_exports_state` dans le même tour que l'agenda : chaque ligne « à refaire » devient une ligne Export du plan. En plus, à chaque tour (2026-11-05) :
   - **Aperçu du prochain match de ligue ou de coupe** si `gold.bv_saisie_adversaires` n'a aucune ligne pour lui (visible dès J-2 ; jamais pour un amical) ;
   - **Historique global des transferts** si `select max(sold_on) from gold.bv_transfer_history` date d'avant hier : demander les ventes depuis cette date, pour mettre à jour la référence de prix `gold.bv_market_price_ref` par delta ; puis Marché et Mes enchères, lus par `gold.bv_market_bargains` (sans agent).

5. Lis `select * from gold.bv_daily_alerts order by priority` : blessés, fatigue hors zone verte, forme ≤ 2, finances, joueurs disponibles, exports en retard, dernier match exporté, match joué non exporté.
6. **Bilan du club, chaque soir, sans agent** (2026-11-05, demande de l'utilisateur : « je ne devrais pas avoir à poser la question ») — une requête chacune, puis une décision par secteur, tranchée :
   - Finances : `gold.bv_finance_health` (solde, résultat hebdo, salaires en % des recettes) et `gold.bv_finance_projection` (solde de fin de saison) ;
   - Effectif : `gold.bv_position_summary` (poste le plus faible), `gold.bv_roster_now` (âge, déclin), `gold.bv_next_opponents` (notre note d'équipe contre celle de la ligue) → « acheter un <poste> de note ≥ X », « vendre Y » ou « garder » ;
   - Transferts (ligne chaque jour, 2026-11-07) : `gold.bv_market_bargains` contre `gold.bv_market_price_ref` si le Marché a moins de 24 h, sinon ligne Export ; le plafond d'une enchère se donne seulement quand elle se termine (le prix monte), avant cela la cible seule ;
   - Personnel : `gold.bv_personnel_status` ; export Personnel si `gold.bv_exports_state` le dit « à refaire » ;
   - Entraînement : le samedi soir (cycle), sinon rien.
   Une ligne « garder » n'est pas écrite (aucune ligne « rien à faire ») ; elle va dans le commentaire en une demi-ligne.

## Brief du matin (case F7)
Si la demande est faite **le matin** (avant 12:00) ou si l'utilisateur demande « le brief » : écris aussi `outputs/basketvibe/briefs/AAAA-MM-JJ-quotidien.md`, qui regroupe en une page :
1. **Aujourd'hui** : la liste horodatée (format ci-dessous).
2. **Alertes** : `gold.bv_daily_alerts`, une ligne chacune, avec l'action à faire (ex. fatigue > 20 → le sortir d'un quart-temps, voir l'agent Tactique).
3. **Hier** : derniers matchs exportés (`gold.bv_match_report`, 24 h) en une ligne chacun.
4. **Conseils ouverts** qui arrivent à échéance aujourd'hui ou demain (section Conseils de `outputs/basketvibe/learnings.md`).
5. **Agents à relancer** : ceux dont l'export d'entrée est arrivé depuis leur dernier brief (match, entraînement, académie, transferts, veille) ; effectif et finances : je relis leurs vues gold moi-même (plus d'agent depuis le 2026-11-02).
Pas plus d'une page ; pas de nouvelle recommandation, seulement ce que les briefs ont validé.

## Fin de saison 1 (2026) [détail dans basketvibe-saison]
- Du 27/10 au 01/11 : amicaux quotidiens, pas de ligue ; ligue en v4 dès le 02/11 [Dev 2026-10-18/22, News 2026-10-19].

## Format de réponse
- **Au plus 8 lignes**, triées par heure : `HH:MM — action — détail (source)`.
- Mets en tête ce qui a une **heure limite** (verrouillage, fin d'enchère).
- Termine par une ligne « Exports à faire aujourd'hui : … ».
- Pas de règle de jeu sans source. Une recommandation nouvelle est permise si elle sort d'une vue gold citée (étape 6) ; sinon seulement ce que les briefs ont validé. Agent seulement pour un cas que les vues ne tranchent pas.
