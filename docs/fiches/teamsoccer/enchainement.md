# Team Soccer — enchaînement export → agents

Règle générale : `CLAUDE.md`, section « Enchaînement automatique ». Après « exports faits », je vérifie l'arrivée dans `bronze.raw_pages` / silver, je donne le compte rendu, puis je lance les agents de cette table **un par un, sans demander**, **club par club** (Chomelix Cows, Ben Ahmed Donkey). Briefs dans `outputs/teamsoccer/briefs/` ; je te rends 3 à 5 lignes par brief, avec ce qu'il faut saisir.

Rythme : composition enregistrée au moins 2 h avant le coup d'envoi ; Forme mise à jour le vendredi ; finances le lundi 00:05 [skills teamsoccer-match, teamsoccer-saison].

| Export reçu | Agents lancés, dans l'ordre | Ce que tu reçois, prêt à saisir |
|---|---|---|
| Match (ligue, coupe, amical) | Match → Tactique (prochain match du club) | Match : explication chiffrée, conseils `C-nnn` contrôlés. Tactique : voir ci-dessous |
| Matchs (calendrier) | Tactique, pour chaque match du lendemain sans composition | Composition de chaque match |
| Joueurs avec blessure, 2e jaune ou Forme changée | Tactique (si un match est à venir) | Composition corrigée |
| Entraînement / gymnase (vendredi) | Entraînement | Compétence et intensité par joueur, Forme, entraîneur |
| Finances (lundi) | Finances-personnel | Voir « Finances » ci-dessous |
| Académie (après les 3 révélations du jour) | Académie | Jeunes à révéler ensuite, à monter, à ignorer |
| Marché / enchères | Transferts | Voir « Transferts » ci-dessous |
| Forum / annonces | Veille | Propositions de modification de skills, **à valider par toi** |

## Tactique : contenu obligatoire
- **Formation** (une des 6) et mode (Simple + preset, ou Avancé).
- **Onze** poste par poste avec le sous-rôle (GB, DC, LAT, WB, MD, MC, ML, MO, AC, DR).
- **Style d'équipe**.
- **Consignes par joueur** (mode Avancé), en français, zone par zone : ultra-défense, défense, milieu, attaque, finition ; action (passer, dégager, dribbler, centrer) et cible (défenseurs, milieux, attaquants).
- **Banc** et **remplacements programmés** (minute, qui sort, qui entre) ; changements à la mi-temps.
- Adversaire : bot ou humain, ses barres de secteurs, 0 à 2 changements justifiés.
- Blessés, suspendus, joueurs à 1 jaune ; Forme de chaque titulaire.
- « À refaire si : Forme (vendredi), blessure, carton, adversaire. »

## Transferts : contenu obligatoire
- Par joueur : poste, compétences clés, âge, prix correct ou non, **enchère maximale**, rappel de la limite d'un achat par semaine et du solde.
- Nos joueurs : vendre à la banque ou aux enchères, gain net (commission de 10 %), effet sur la masse salariale ; revente bloquée 7 semaines.
- **Jamais d'enchère ni de vente lancée sans ton accord.**

## Finances : contenu obligatoire
- Pour chaque club : alerte et cause, date estimée du retour au positif.
- Masse salariale soutenable ou non ; capacité d'investissement (entraîneur, places).
- Stade : quelles places acheter, combien, quand ; entretien ; TSCredits du Centre de Haute Performance.

## Quand rien n'est lancé
- Export absent ou périmé : je le dis et je ne lance pas l'agent.
- Plusieurs exports : ordre Match → Effectif → Tactique → Entraînement → Finances → Académie → Transferts → Veille.
