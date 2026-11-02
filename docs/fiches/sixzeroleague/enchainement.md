# Six Zero League — enchaînement export → agents

Règle générale : `CLAUDE.md`, section « Enchaînement automatique ». Après « exports faits », je vérifie l'arrivée dans `bronze.raw_pages` / silver, je donne le compte rendu, puis je lance les agents de cette table **un par un, sans demander**. Briefs dans `outputs/sixzeroleague/briefs/` ; je te rends 3 à 5 lignes par brief, avec ce qu'il faut saisir.

Rythme : 2 journées par jour, entraînement et transferts réglés chaque soir [skill sixzeroleague-communaute].

| Export reçu | Agents lancés, dans l'ordre | Ce que tu reçois, prêt à saisir |
|---|---|---|
| Match (journée jouée) | Match → Tactique (journées suivantes) | Match : explication chiffrée, conseils `C-nnn` contrôlés. Tactique : voir ci-dessous |
| Calendrier / classement | Tactique | Composition des 2 prochaines journées |
| Équipe (joueurs) avec blessé ou suspendu | Tactique | Composition corrigée, remplaçant sans pénalité si possible |
| Entraînement (cycle de 2 journées) | Entraînement | Intensité d'équipe (Light / Normal / High), focus par joueur, 2e rôle à former |
| Finances | Finances | Voir « Finances » ci-dessous |
| Académie U18 (nouveau choix toutes les 8 journées) | Académie | Prospect à prendre, scouting |
| Marché des transferts | Transferts | Voir « Transferts » ci-dessous |
| Chat du jeu / News | Veille | Propositions de modification de skills, **à valider par toi** |

## Tactique : contenu obligatoire
- **Sept de départ** rôle par rôle : gardien, demi-centre, arrière gauche, arrière droit, ailier gauche, ailier droit, pivot.
- **Remplaçant** pour chaque rôle.
- **Formations** attaque et défense.
- Prochain adversaire : rang, bilan, bot ou humain, 0 à 2 changements justifiés.
- Blessés et suspendus (cartons, exclusions) : qui manque, qui remplace.
- « À refaire si : blessure, suspension, adversaire. »

## Transferts : contenu obligatoire
- 3 à 5 annonces pour nos rôles faibles, ou le joueur demandé : intérêt, prix, **enchère maximale**, coût total (frais, salaire).
- Nos joueurs : vendre maintenant / fin de saison / garder (âge, rôle, salaire, retraite).
- **Jamais d'enchère ni de vente lancée sans ton accord.**

## Finances : contenu obligatoire
- Perte ou gain sur le dernier cycle et la prévision, cause chiffrée ; masse salariale et marge.
- Sponsor (si changement possible) : les 3 offres comparées sur la saison.
- Infrastructures : laquelle améliorer et quand (décision en attente : Fan Shop 7 ou Arena 7).

## Quand rien n'est lancé
- Export absent ou périmé : je le dis et je ne lance pas l'agent.
- Plusieurs exports : ordre Match → Effectif → Tactique → Entraînement → Finances → Académie → Transferts → Veille.
