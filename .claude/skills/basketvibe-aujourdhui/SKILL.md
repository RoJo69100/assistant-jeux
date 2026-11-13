---
name: basketvibe-aujourdhui
description: BasketVibe — que faire aujourd'hui : plan du jour en 11 blocs (script pipelines/aujourdhui.py) avec exports en retard, compositions, transferts, Match Engine. Pour tout « que faire », « reprenons » ou plan du jour.
---

# BasketVibe — que faire aujourd'hui

Le script calcule tout (vues gold, briefs, registre « déjà fait », décisions d'achat, études de `docs/etudes/`). Gabarit des 11 blocs : `docs/attentes/gabarit-que-faire-basketvibe.md`. Rythme de la semaine : skill basketvibe-saison [M§1.3].

## Méthode
1. **Première action, avant toute requête et tout autre outil** : `python -I pipelines/aujourdhui.py basketvibe`.
2. **Affiche tel quel tout ce qui précède** la ligne `--- session (à exécuter, ne pas afficher) ---` (blocs 0 à 10) : sans reformulation, sans tableau de ton cru, sans ajout dans ses lignes. Ce qui suit la ligne ne s'affiche jamais.
3. **Exécute les consignes de session** (après le séparateur), dans cet ordre :
   - `lance l'agent tactique` / `lance l'agent analyste` : agent du type propre dans `.claude/agents/`, jamais `general-purpose` ; donne le jeu (BasketVibe) et la règle d'horizon (aujourd'hui) ; au plus 3 agents d'analyse par passage ; annonce le nombre avant de lancer ;
   - `lancer l'agent data-scientist` : **en arrière-plan** (`run_in_background`, un lancement a duré plus de 19 minutes) ; au plus une fois par jour ; inscris d'abord « étude data-scientist lancée à HH:MM » dans `outputs/basketvibe/fait-AAAA-MM-JJ.md` (skill `deja-fait`) ; le « que faire » **n'attend pas son résultat** et affiche « étude lancée, résultat attendu » sous le bloc 6.
4. **Relance le script une fois** après les consignes (le brief écrit par l'agent est alors lu ; le bloc 6 écrit « étude lancée, résultat attendu » grâce au registre) et affiche cette seconde sortie à la place de la première. Pas de troisième passage.
5. **Exports réclamés** : toute ligne « export à faire : … » demande à l'utilisateur de faire l'export ; attends son « fait » avant de conclure sur ce bloc.
6. **Hooks** : la réponse passe `forme.py` et `controle.py` ; si un hook rejette, corrige seulement la ligne rejetée et note le rejet dans le tableau « Rejets de hooks » du journal.
7. **Registre « déjà fait »** : ce que l'utilisateur déclare (export fait, réglage saisi) s'inscrit dans `outputs/basketvibe/fait-AAAA-MM-JJ.md` ; le script le lit au passage suivant.
8. **Porte** : chaque jour, demande à l'utilisateur ses quatre lignes (verdict, il manquait, en trop, faux) et inscris-les telles quelles dans le tableau « Retours de la Porte » de `docs/refonte-v3/journal-aujourdhui.md`.

Le script écrit l'instantané `outputs/basketvibe/aujourdhui-AAAA-MM-JJ.md` (blocs seuls, sans consignes). Les heures viennent de la ligne « Heure de Paris » injectée à chaque message, jamais de `date`.

## Brief du matin (case F7)
Si la demande est faite **le matin** (avant 12:00) ou si l'utilisateur demande « le brief » : écris aussi `outputs/basketvibe/briefs/AAAA-MM-JJ-quotidien.md`, qui regroupe en une page :
1. **Aujourd'hui** : les blocs 1 à 4 du script.
2. **Alertes** : `gold.bv_daily_alerts`, une ligne chacune, avec l'action à faire.
3. **Hier** : derniers matchs exportés (`gold.bv_match_report`, 24 h) en une ligne chacun.
4. **Conseils ouverts** qui arrivent à échéance aujourd'hui ou demain (section Conseils de `outputs/basketvibe/learnings.md`).
5. **Agents à relancer** : ceux dont l'export d'entrée est arrivé depuis leur dernier brief (match, entraînement, académie, transferts, veille) ; effectif et finances : relis les vues gold toi-même (plus d'agent depuis le 2026-11-02).
Pas plus d'une page ; pas de nouvelle recommandation, seulement ce que les briefs ont validé.

## Fin de saison 1 (2026) [détail dans basketvibe-saison]
- Du 27/10 au 01/11 : amicaux quotidiens, pas de ligue ; ligue en v4 dès le 02/11 [Dev 2026-10-18/22, News 2026-10-19].
