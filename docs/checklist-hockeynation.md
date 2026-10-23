# Checklist Hockey Nation (hockey sur glace)

Adaptée des checklists BasketVibe et SixZero League le 2026-10-23 (4e jeu). Le travail est terminé quand tout est coché. Parties E et F : chaque case est un test validé par l'utilisateur. Spécificités : 4 équipes (PRO, FRM, U21, U17) aux droits différents, plafond salarial, contrats longs, draft et scouting, coachs à former.

## A. Fondations
- [x] Bronze commun, `game = 'hockeynation'` (vérifié le 2026-10-23 : 265 captures, 35 types de page)
- [x] Script `userscripts/hockeynation.user.js` installé (vérifié le 2026-10-23 : v0.1.0, captures API + guide)
- [x] Discord importé (vérifié le 2026-10-23 : 154 464 messages, 5 salons)

## B. Collecte
- [x] Effectifs des 4 équipes, talents, contrats (vérifié le 2026-10-23 : 84 joueurs)
- [x] Finances PRO, plafond, rachats, contrats qui expirent (vérifié le 2026-10-23 : plafond S27 57,5 M$)
- [x] Coachs du club et marché des coachs (vérifié le 2026-10-23 : 16 coachs)
- [x] Entraînement et journal (vérifié le 2026-10-23)
- [x] Lignes PRO (vérifié le 2026-10-23)
- [x] Matchs, classement (vérifié le 2026-10-23 : 128 matchs)
- [x] Échanges et marché (vérifié le 2026-10-23)
- [x] Draft : classes des 3 ligues de nos choix, choix, scouts, budget (vérifié le 2026-10-23 : 300 joueurs, 5 choix)
- [x] Guide complet (vérifié le 2026-10-23 : 21 rubriques)
- [ ] Lignes FRM, U21, U17 ; fiche détaillée d'un coach ; fiche contrat d'un joueur ; /version-history
- [ ] Exports d'un adversaire (effectif, coachs, matchs)

## C. Modèle de données
- [x] Silver : 22 vues `hn_*` (vérifié le 2026-10-23 : `sql/silver/015_hn_base.sql`)
- [x] Gold : talents vs poste `hn_player_fit` (vérifié le 2026-10-23 : 8 joueurs PRO/FRM en contre-emploi au poste principal)
- [x] Gold : tableau de draft `hn_draft_board` (vérifié le 2026-10-23 : 3 ligues, 53 repérés dans la nôtre)
- [x] Gold : plafond par saison `hn_cap_outlook` (vérifié le 2026-10-23 : S27 engagés 55,2 M$ + rachat 0,67 M$, cap space 1,63 M$)
- [x] Gold : coachs `hn_coach_board`, calendrier `hn_calendar`, alertes `hn_daily_alerts` (vérifié le 2026-10-23)
- [ ] Gold : valeur d'un échange (avant/après : âge, talents, cap space)
- [ ] Gold : progression par joueur entre deux relevés
- [ ] Silver/gold : équipes adverses

## D. Skills
- [x] 6 skills `hockeynation-*` écrits depuis le guide, chaque fait sourcé [G:Rubrique] (2026-10-23)
- [ ] Hypothèse des compétences clés par poste confirmée (Discord ou observation)
- [ ] Validés par l'utilisateur

## E. Agents (fiche `docs/fiches/hockeynation/`, 2026-10-23)
- [ ] Effectif : bilan par poste et par équipe, doubles postes, vieillissement
- [ ] Finances-personnel : plafond, prolongations, coachs, scouts
- [ ] Académie : draft, U21 (ELC, Farm, départ), Import Draft
- [ ] Entraînement : compétence et coach par joueur PRO/FRM, ordre de choix
- [ ] Tactique : lignes A/B/C, mises au jeu, gardiens
- [ ] Transferts : verdict d'échange, joueurs à vendre, agents libres
- [ ] Match : explication et journal des enseignements
- [ ] Étude des adversaires

## F. Routine
- [ ] « Que faire aujourd'hui » Hockey Nation (agenda par jour de saison)
- [ ] Première chaîne d'agents complète en medium + Sonnet
