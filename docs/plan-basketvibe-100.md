# Plan BasketVibe à 100 % (17/11/2026)

À lire chez toi : tout tourne dans le cloud. Il te faut le navigateur (jeu + Tampermonkey) et claude.ai/code (sessions du dépôt, environnement « Assistant-jeux »).

## Où on en est (pourcentages = jugement de Claude, pas mesurés)
Collecte 75 · Base 70 · Plan du jour 70 · Agents 50 · Apprentissage 20 · Match Engine 35 · Réutilisation 0.
Fait : moteur d'état par événement, table état → agent, routine quotidienne (10:40 Paris, publie sur la branche claude/passage-quotidien), fiches de match à la nouvelle forme, exports périodiques, règles d'offres, de ventes, de preset et de personnel, docs/regles-utilisateur.md.
Autres jeux au 17/11 (Collecte / Base / Règles / Plan / Match Engine / Auto) : Hockey Nation 45/60/85/55/45/0 ; TeamSoccer 45/35/65/10/5/0 ; SixZeroLeague 45/40/65/10/5/0 ; Hardwood 40/35/60/10/0/0 ; DerbyManager 45/35/25/0/0/0. Gelés jusqu'à l'étape 6.

## Ta journée (10 minutes)
1. Après 10:40, le tableau est dans claude.ai/code/routines, « BasketVibe passage quotidien », dernière exécution (ou dans la notification).
2. Fais les lignes : exports, écrans à sauvegarder avant l'échéance (le lien de la fiche est dans la ligne). Ligue et coupe : preset de l'adversaire d'abord. Amical : pas de preset.
3. Juge chaque ligne : juste / fausse / manquante / inutile (une phrase si fausse).
4. Colle ce jugement dans une session du dépôt avec le prompt « Verdict du jour » (en bas).
Si la routine échoue (ligne « git : » ou « agent X non lancé ») : colle sa réponse dans une session.

## Étape 1 — Ce soir et demain
- [ ] Amical Union Heidelberg : saisir selon outputs/basketvibe/briefs/2026-11-17-tactique-amical.md avant le 18/11 07:45, puis exporter la page du match.
- [ ] Exporter le Marché (toutes les pages), l'historique global des transferts et la page Personnel.
- [ ] Ligue C.B.Granada (18/11, verrou 19:45) : preset de l'adversaire, exporter l'aperçu, saisir selon la fiche.
- [ ] Session : prompt « règle de personnel » (marketing 0, psychologues selon la forme) s'il n'est pas encore passé.

## Étape 2 — Trois journées jugées (critère : 3 jours de suite sans ligne fausse)
- [ ] Chaque jour : ta journée ci-dessus ; chaque ligne fausse devient un test le jour même (prompt « Verdict du jour »).
- [ ] Après la 3e journée sans ligne fausse : le plan du jour est à 100 %.

## Étape 3 — Collecte et base (en parallèle, environ 1 heure à toi au total)
- [ ] Installer ou mettre à jour le script Tampermonkey : https://raw.githubusercontent.com/RoJo69100/assistant-jeux/main/userscripts/basketvibe.user.js ; vérifier : pas de bouton rouge, « Dernière capture il y a X h » inférieur à 24 h dans le plan (jamais testé dans un vrai Tampermonkey).
- [ ] 7 jours sans trou de capture.
- [ ] Sauvegarde du bronze : suivre docs/sauvegarde.md (dépôt privé et jeton, jeton d'export, 4 secrets, copier docs/sauvegarde-workflow.yml vers .github/workflows/). Critère : une sauvegarde hebdomadaire reçue.
- [ ] Session : fin_etape.py doit échouer quand un test est rouge (aujourd'hui il sort 0 même avec un test rouge).
- [ ] Session : lecteur du résultat de test d'académie, après le premier test réel d'un prospect (exporter la page où le résultat s'affiche).
- [ ] Session, basse priorité : 8 numéros de migration en double et un outil qui applique les migrations dans l'ordre.

## Étape 4 — Match Engine (plusieurs semaines : dépend des matchs et de tes exports)
- [ ] Chaque match de ligue : exporter la page (Details, Stats par quart, Play-by-play). Chaque journée : le Classement des 3 ligues.
- [ ] Une fois : dire si le jeu affiche les réglages utilisés par l'adversaire (oui/non ; si oui, exporter la page).
- [ ] Amicaux E1 : saisir la fiche (agressivité 3), exporter après.
- [ ] Session : prompt « Étude Match Engine » après chaque série d'exports.
Critère : chaque expérience E1 à E5 a un verdict (confirmé ou infirmé) avec son nombre de matchs, et la fiche tactique cite les règles confirmées.

## Étape 5 — Mesure dans le jeu (optionnel, une session)
Trois chiffres par semaine dans le plan : rang en ligue, force moyenne des 7 joueurs de rotation, trésorerie. À défaut d'un autre choix de l'utilisateur, ceux-là.

## Étape 6 — Réutilisation pour les autres jeux (après l'étape 2)
- [ ] Session de conception : contrat par jeu du moteur d'état (vue d'état, section de config, fiches, agents, routine) et check-list « nouveau jeu ».
- [ ] Porter Hockey Nation en 2 sessions (preuve de réutilisation), puis TeamSoccer et SixZeroLeague, puis Hardwood, puis DerbyManager.

## Prompts à coller (sessions du dépôt, /model sonnet /effort medium)
### Verdict du jour
```
Aucun texte entre les appels d'outil. Réponse finale : 5 lignes au plus. Plafond : 30 appels d'outil, 20 requêtes SQL. Ce prompt tient lieu de conception (voie courte).
Verdict de l'utilisateur sur le tableau du jour (BasketVibe) : <colle ici une ligne par ligne du tableau : juste / fausse / manquante / inutile, plus une phrase si fausse>.
Pour chaque ligne fausse, manquante ou inutile : (1) cause dans le code ou la config (chiffres issus d'une requête), (2) un test écrit d'abord qui échoue, (3) le correctif, (4) docs/regles-utilisateur.md si c'est une règle nouvelle. Un commit par ligne. Puis fusion_main.py et fin_etape.py. Réponse : nombre de lignes corrigées, et au plus UNE question à l'utilisateur.
```
### Étude Match Engine
```
Aucun texte entre les appels d'outil. Réponse finale : 5 lignes au plus. Plafond : 30 appels d'outil, 60 requêtes SQL. Ce prompt tient lieu de conception (voie courte).
Relance l'étude du Match Engine de BasketVibe (celle du bloc 6 du plan, « étude du 16/11 ») avec les matchs entrés en base depuis. Mets à jour l'avancement de E1 à E5. Liste les exports encore nécessaires, un par ligne, avec la raison. Ne change aucune règle sans verdict chiffré (n et critère).
```

## Règles de travail
- Une session = un jeu. Toute règle nouvelle de l'utilisateur va dans docs/regles-utilisateur.md.
- Aucun achat, vente ou enchère sans accord écrit de l'utilisateur ; au-dessus de 250 000, dossier puis agent police.
- Pas d'infrastructure sans effet visible le lendemain.
