# Hockey Nation — fiche Effectif

Lue par l'agent `effectif` après `commun.md`.

## Skills
`hockeynation-joueurs` (talents, postes, âge, déclin), `hockeynation-contrats-finances` (contrats par équipe).

## Données
- `silver.hn_players` : dernier relevé (équipe, âge, note, postes, 15 compétences, plafonds `skills_maxed`, déclin `skills_declining`, talents, spéciales, contrat actif et suivant).
- `gold.hn_player_fit` : verdict talents par joueur et par poste tenable.
- `gold.hn_cap_outlook` : engagements par saison.

## Livrable
1. **Bilan par poste et par équipe** (PRO, FRM, U21) : titulaires, profondeur, verdict talents, âge, fin de contrat. Signale les postes minces (PRO au 2026-10-23 : 2 centres naturels, De Bruin et Papež ; Blednov et Flink en 2e poste).
2. **Doubles postes** : poste où les talents collent le mieux ; proposer un « Swap position » si le poste secondaire est meilleur.
3. **Vieillissement** : joueurs de 30 ans et plus, compétences en déclin, fins de contrat — en lien avec l'objectif d'une line-up jeune.
4. **3 actions** nommées (monter un FRM/U21, échanger, prolonger ou non).
