# Gabarit « que faire » — BasketVibe

Ce que l'utilisateur attend de la réponse du jour. Document en blocs, organisé par jour (aujourd'hui, demain), sans heures, sauf l'heure limite du verrou dans la ligne de composition.

**Règle générale** : un bloc contient des données réelles ou une ligne « donnée manquante : exporte X pour l'obtenir ». Jamais un bloc absent. Jamais une commande à lancer par l'utilisateur.

Producteurs possibles : **script** (pipelines/), **agent** (.claude/agents/), **Claude de session** (requête + raisonnement du tour), **export** (page ouverte par l'utilisateur, collecte passive).

---

## Bloc 0 — Exports d'abord

- **Contenu** : liste de ce qui manque et, pour chaque export, ce qu'il débloque.
  - Marché (plusieurs pages) → cibles et prix du bloc 4.
  - Aperçu du prochain match de ligue ou de coupe → bloc 3 (composition, focus défensif par adversaire).
  - Match du jour → blocs 6, 7.
  - Amical → blocs 2, 6.
  - Équipe → blocs 2, 3.
  - Académie, Finances, Personnel, Entraînement, quand la fiche est plus vieille que le dernier export → bloc 8, 9.
  - Exports de l'étude du bloc 5 (classement, calendrier, matchs et joueurs adverses, tactiques adverses).
- **Donnée nécessaire** : date de la dernière page reçue par type (bronze) comparée à la date de la fiche/vue gold correspondante.
- **Qui la produit** : script (état des exports, gold) ; l'export lui-même vient de l'utilisateur.

## Bloc 1 — À faire aujourd'hui, puis demain

- **Contenu** : tableau priorité (🟥/🟧/🟩 + mot) | catégorie | action. Deux sections : Aujourd'hui, Demain (préparé aujourd'hui, jamais reporté).
- **Donnée nécessaire** : agenda, alertes, verrous de composition.
- **Qui la produit** : script (gold.bv_agenda, alertes) ; Claude de session pour l'assemblage.

## Bloc 2 — Composition de l'amical

- **Contenu** : tableau poste par poste dans l'ordre de l'écran : joueur | quarts | agressivité | focus offensif | focus de tir | rôle | valeurs d'écran. Puis zone et focus défensif. Test en cours nommé. Heure limite du verrou dans la ligne.
- **Donnée nécessaire** : effectif et forme (Équipe), adversaire, expériences amicales (`docs/attentes/experiences-amicales-basketvibe.yaml`), règles de décision.
- **Qui la produit** : script (vue de saisie gold) + agent tactique ; export Équipe + amical par l'utilisateur.

## Bloc 3 — Composition de la ligue ou de la coupe

- **Contenu** : même tableau, très précis, avec le focus défensif par adversaire, dès que l'aperçu adverse est en base. Vérification à J-1 (tout écart avec l'état de l'effectif signalé).
- **Donnée nécessaire** : aperçu du prochain match (adversaire, effectif adverse, tactique adverse si exposée), effectif, forme, fatigue.
- **Qui la produit** : agent tactique + vue gold ; export aperçu adverse par l'utilisateur.

## Bloc 4 — Transferts

- **Contenu** : cibles du Marché sur les prochaines 24 h (nom, poste, note, prix, plafond, fin d'enchère) ; conseils sur les recrues ; ventes ; mes enchères en cours.
- **Donnée nécessaire** : pages Marché (plusieurs), effectif, solde, enchères en cours.
- **Qui la produit** : agent transferts + vue gold ; export Marché par l'utilisateur ; `police` seulement au-dessus du seuil de gros montant.

## Bloc 5 — Les meilleurs et les failles du jeu (priorité absolue)

- **Contenu** :
  1. Pourquoi les meilleures équipes sont les meilleures.
  2. Pourquoi les meilleures tactiques.
  3. Pourquoi les meilleurs joueurs.
  4. Comparaison haut contre reste du classement, avec n et intervalle.
  5. Failles repérées.
  6. Ce que nous devons changer.
- **Donnée nécessaire** : matchs détaillés de toutes les équipes (pas seulement la nôtre), statistiques joueurs adverses, tactiques adverses, classement hebdomadaire.
- **Qui la produit** : requêtes SQL (silver) + agent analyste ; exports par l'utilisateur (classement, calendrier, matchs d'autres équipes, joueurs).

## Bloc 6 — Match Engine

- **Contenu** : une ligne par jour « matchs ajoutés depuis hier : n (ligue, amical), total en base n, étude relancée le JJ/MM » ; avancement des expériences ; prochaine hypothèse ; exports manquants pour mieux comprendre le moteur, classés par apport.
- **Donnée nécessaire** : compte de matchs par jour et par type, état des expériences, date de la dernière étude.
- **Qui la produit** : script (compte en base) + Claude de session ; agent match pour les hypothèses.

## Bloc 7 — Analyse détaillée

- **Contenu** : après une défaite de ligue ou de coupe ; le dimanche, tous les matchs de la semaine : quart par quart, tirs par zone, fautes, minutes et fatigue, hypothèses confirmées ou infirmées, ce qui change.
- **Donnée nécessaire** : stats de match par quart et par joueur, tirs par zone, minutes, fatigue.
- **Qui la produit** : agent analyste (défaite) ; agent match (hebdomadaire) ; export du match par l'utilisateur.

## Bloc 8 — Économie

- **Contenu** : l'argent ne doit pas stagner. Investissable aujourd'hui ; usages classés par rendement mesuré (joueurs, académie, entraînement, personnel) ; solde qui dort signalé.
- **Donnée nécessaire** : solde, recettes, salaires, rendements mesurés par usage.
- **Qui la produit** : script (vue gold finances) + Claude de session ; export Finances.

## Bloc 9 — Académie, personnel, entraînement

- **Contenu** : pour chacun : état, décision du jour, prochaine échéance, préparation faite avant l'échéance.
- **Donnée nécessaire** : pages Académie, Personnel, Entraînement ; calendrier des échéances.
- **Qui la produit** : agents académie et entraînement + vue gold ; exports de l'utilisateur.

## Bloc 10 — À valider par l'utilisateur

- **Contenu** : décisions qui exigent son accord écrit (achat, vente, enchère) et choix qu'une requête ne peut pas trancher.
- **Donnée nécessaire** : liste des propositions en attente.
- **Qui la produit** : Claude de session.
