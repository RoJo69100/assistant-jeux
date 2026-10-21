# BasketVibe — enchaînement export → agents

Règle générale : `CLAUDE.md`, section « Enchaînement automatique ». Après « exports faits », je vérifie l'arrivée dans `bronze.raw_pages` / silver, je donne le compte rendu, puis je lance les agents de cette table **un par un, sans demander**. Chaque agent écrit son brief dans `outputs/basketvibe/briefs/` ; je te rends 3 à 5 lignes par brief, avec ce qu'il faut saisir dans le jeu.

| Export reçu | Agents lancés, dans l'ordre | Ce que tu reçois, prêt à saisir |
|---|---|---|
| Match (ligue, coupe ou amical) | Match → Tactique (prochain match) | Match : pourquoi gagné/perdu, chiffres, conseils `C-nnn` contrôlés. Tactique : voir « Tactique » ci-dessous |
| Preview / calendrier (prochain adversaire) | Tactique | Tactique complète pour ce match |
| Effectif (Roster) avec blessure ou forme changée | Tactique (si un match est à venir) | Tactique corrigée, plan B du blessé |
| Entraînement (dimanche après 04:00) | Entraînement | Verdict garder/changer par joueur, réglages principal/secondaire, potentiel estimé |
| Finances (dimanche) | Finances-personnel | Voir « Finances » ci-dessous |
| Académie (rapport du jeudi 09:00) | Académie | Tester / signer / ignorer / attendre par prospect, investissement de la semaine |
| Transferts (marché du jour ou joueur précis) | Transferts | Voir « Transferts » ci-dessous |
| News / Discord | Veille | Propositions de modification de skills, **à valider par toi** |

## Tactique : contenu obligatoire
- **Cinqs** Q1, Q2, Q3, Q4, OT × PG, SG, SF, PF, C.
- **Consignes par joueur** : passe ↔ tir, focus offensif, focus de tir, agressivité défensive, avec libellé de l'écran et cran.
- **Depth chart** : 2 ou 3 remplaçants par emplacement.
- **Focus défensif** par joueur adverse (Intense / Lock / Normal / Light / Give up) ; en amical v4, la zone Rim / Perimeter / Neutral.
- Blessés et plan B ; rappel : re-sélectionner le preset sur chaque match déjà planifié.
- « À refaire si : forme, blessure, fatigue, adversaire. »
- Amical quotidien : preset amical (jeunes, tests v4, fatigue) [mémoire basketvibe-daily-friendlies].

## Transferts : contenu obligatoire
- Par joueur : emplacement, qui il remplace, prix (correct / cher / affaire), **enchère maximale** chiffrée, heure de fin, coût total (prix + salaires).
- Mes joueurs : vendre maintenant / fin de saison / garder, en gardant 9 disponibles.
- **Jamais d'enchère ni de vente lancée sans ton accord** : l'agent conseille, tu décides.

## Finances : contenu obligatoire
- Le club perd-il de l'argent, cause chiffrée ; marge de masse salariale ; capacité d'investissement maintenant et en saison 2.
- Personnel poste par poste (médecins, kinés, psychologues, marketing) : recruter / garder / virer, coût et gain.
- Homegrown : ce que rapportent les minutes des juniors.

## Quand rien n'est lancé
- Export absent ou périmé : je le dis et je ne lance pas l'agent.
- Plusieurs exports : ordre Match → Effectif → Tactique → Entraînement → Finances → Académie → Transferts → Veille.
