---
name: hockeynation-contrats-finances
description: Règles Hockey Nation sur l'argent — plafond salarial PRO, cap space, paies (jours 8-42), pénalités de dépassement, rachats (moitié du restant), prolongations avec l'agent (humeur, frais, durée par âge), contrats ELC (50 % moins chers) et Farm, rétrogradations, libérations, agents libres (Frenzy, ELC, 5 offres), règles par équipe PRO/FRM/U21. À charger pour juger une prolongation, un rachat, une signature ou l'effet d'un échange sur le plafond.
---

# Hockey Nation — contrats et finances

Sources : **[G:Finances]**, **[G:U21 Team]**, **[G:Farm Team]**, **[G:Free Agents]** (guide du 30/09/2026, lu le 2026-10-23).

## Plafond salarial (PRO)
- Plafond de départ 50 M$, varie chaque saison par multiples de 100 000 $, d'1 M$ au plus. Annonces : jour 1 (hausse ou baisse), jour 28 (fourchette), jour 57 (valeur officielle).
- S26 : 57,2 M$ ; S27 : 57,5 M$ (`silver.hn_finances.salary_cap_projection`).
- Cap space = plafond − salaire total payé en fin de saison. **Ne jamais passer sous zéro** : plus de signature, échanges refusés s'ils ajoutent du salaire, **−30 % aux compétences en match officiel** ; toujours dépassé en fin de saison = faillite et GM renvoyé.
- Paie quotidienne pendant la saison régulière, jours 8 à 42.

## Rachat (buyout)
- Le joueur part tout de suite ; pénalité = **moitié du salaire restant**, répartie sur les années restantes.
- Interdit si l'effectif PRO tombe sous 12 attaquants, 6 défenseurs, 2 gardiens (sauf dépassement du plafond), si le coût est nul, ou pour un agent libre signé dans sa 1re saison.
- **Calcul [Obs, 2026-10-29, tiré de la règle ci-dessus ; `buyout-info` revenu vide pour Lauper, à confirmer à l'écran]** : la pénalité totale = ½ du salaire restant, répartie à parts égales sur les années restantes, donc le plafond n'est soulagé que de **50 % du salaire chaque saison** (Lauper 3 250 000 $ jusqu'en S29 : paie 4 875 000 $ au total, 1 625 000 $ par saison en S27, S28, S29 ; soulage 1 625 000 $ par saison). Un échange soulage 100 % : à préférer pour descendre sous le plafond. Rachat = joueur parti tout de suite ; vérifier le minimum de 2 gardiens avant.
- **Échanges et plafond négatif [G:Finances]** : un échange qui ajoute du salaire est refusé tant que le cap space est négatif.

## Prolongation (agent)
- Seulement pendant la **dernière année** de contrat. 1re proposition immédiate, les suivantes en 2 à 6 jours (réponse garantie à la dernière mise à jour de la saison, et juste après un échange).
- Salaire demandé : note en début de saison, plafond, générosité de l'agent, **humeur** (happy → neutral → unhappy, +3 à 5 % de frais), salaire actuel, niveau de la ligue (ligue 3.x ou plus bas : +1 % dès 55, +3 % dès 70, +5 % dès 80).
- Durée : 1-5 ans à 22 ans ou moins, 1-7 ans de 23 à 29 ans, 1-3 ans à 30 ans et plus. Redemander risque une offre pire. Humeur remise à « happy » après un échange.

## Jeunes : ELC et Farm
- **Correction de l'utilisateur, 2026-10-25 [U]** : un U21 peut être monté directement en FRM ou en PRO, même avant 21 ans ; à 21 ans il monte automatiquement. Le texte du guide ci-dessous (ELC après la fenêtre I, Farm à 21 ans avec effet à 22 ans) est donc à ne pas opposer à l'utilisateur. Discord confirme que les U21 s'appellent en équipe supérieure (« call up », #general, 2026-09-13). À vérifier à l'écran : prix du contrat et jour d'effet.
- U21 → PRO : **ELC 3 ans, 50 % moins cher** ; signable après la fermeture de la fenêtre I, effet la saison suivante [guide, contredit par [U] ci-dessus].
- FRM → PRO : ELC jusqu'à 24 ans (durée selon l'âge et la fenêtre : 3 ans à 18-21 ans ; 22 ans → 3 ans avant la fenêtre I, 2 ans après ; 23 ans → 2 puis 1 ; 24 ans → 1 an, avant la fenêtre I seulement). 25 ans et plus : négociation, à conclure **avant la fin de saison** sinon il part. FRM de 25+ ans noté 70+ : demande lui-même un contrat PRO au jour 1.
- Contrat Farm : sans salaire, durée indéfinie, signable **seulement à 21 ans**, effet à 22 ans. Un U21 non signé part à 22 ans.
- Contrats PRO signés : actifs la saison suivante ; « Activate Now » possible avant la fermeture de la fenêtre I.
- Rétrograder : seulement un joueur sous ELC (vers U21 s'il a 21 ans ou moins) ; plus de salaire PRO pendant ce temps ; 3 jours avant de le rappeler ; interdit après le jour 35 ; **impossible pour un joueur signé comme agent libre**.
- FRM : 30 joueurs et 30 contrats au maximum ; au-delà en début de saison, libérations **au hasard** (plus de 15 attaquants, 8 défenseurs ou 3 gardiens).

## Agents libres
- Offres du jour 1 au jour 35, salaire entre 90 % et 200 % de la demande ; 5 offres au maximum en même temps. Frenzy au jour 3 (offres jusqu'à 1 h avant).
- Le joueur ne regarde que les 3 meilleures offres ; chaque dollar compte. Demandes −5 à 10 % en début de saison, révisées jours 10, 20, 30.
- ELC possible pour un agent libre de 24 ans ou moins noté 69 ou moins, seulement si personne ne lui offre de contrat PRO.

## Vues
`silver.hn_finances`, `silver.hn_expiring` (agent, humeur, demande), `silver.hn_players` (`salary`, `contract_to`, `elc`, `frm`, `next_salary`), `gold.hn_cap_outlook` (engagements par saison, rachats, cap space S+1).

## [Veille 2026-10-29] Mises à jour (V-20261029-1, -2, -3, -4, -12)
- **S27 (25/10/2026)** : Contract Year Special (actif quand il reste 1 an au contrat actif, même après prolongation anticipée, seulement pour les joueurs qui ont la compétence), FA ELC, Coach Development Boost, Agent Rework partie 1. **S28 (+63 jours, ~27/12/2026)** : activation des favors d'agents et **plancher salarial de 50 %** ; base de calcul non publiée. [Discord #general, hnadmin, 2026-10-25 06:46 et 2026-10-22 04:29 ; V-2]
- **ELC d'agent libre — hypothèse ⚠️** : un joueur écrit « ovr max 69 » (note maximale possible), notre texte dit « noté 69 ou moins » ; 1re saison 3-way, 2e et 3e 2-way. Avis de joueur non confirmé par hnadmin : vérifier à l'écran avant de bâtir un plan sur la note actuelle. [Discord #general, gordie_79, 2026-10-25 14:49-14:51 ; V-1]
- **Rachat** : le reste du salaire de la saison en cours est effacé, le futur est remplacé par un salaire de rachat, le coût baisse si on attend (hnadmin, 2025-07-02). Le plafond est libéré **immédiatement à l'action** (hnadmin, 2026-07-22 07:21, contexte du message non vu). L'écart avec « moitié du restant » se lève par le chiffre affiché à l'écran. [Discord #general ; V-3]
- **Échanges** : l'allègement du plafond et les pénalités s'appliquent dès l'**approbation** du trade, pas à la fin du traitement. [Discord #general, hnadmin, 2026-03-12 06:41 ; V-4]
- **Frenzy S27 (repères de prix, avis)** : Raymond Baker (LD/RD) 4 ans 9 050 000 $ (Odesa) ; Borer (min 81) demande 5,5 M × 5 ; les agents libres signés pendant la Frenzy disparaissent de la recherche avant l'annonce. Agents : réponse instantanée au début d'une négociation, humeur remise à « happy » après un échange, réponse garantie à la dernière mise à jour de la saison (hnadmin, 2026-04-22 et 2026-06-17). [Discord #events, .coleh, 2026-10-27 19:12-19:18 ; V-12]
