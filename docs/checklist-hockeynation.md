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
- [x] Lignes FRM, U21, U17 (non réglables par le GM : calculées par `gold.hn_depth_chart`), fiches coach (31 fiches `/coach/:id`, dont Pavel Vašák), contrats (partie Contract de la fiche joueur) (vérifié le 2026-10-23) ; reste /version-history
- [x] Exports d'adversaires : Leszno Bulls, Seoul Pilots, Miami Maidiacs, Jessup Baldos (effectif + staff) (vérifié le 2026-10-23)

## C. Modèle de données
- [x] Silver : 22 vues `hn_*` (vérifié le 2026-10-23 : `sql/silver/015_hn_base.sql`)
- [x] Gold : talents vs poste `hn_player_fit` (vérifié le 2026-10-23 : 8 joueurs PRO/FRM en contre-emploi au poste principal)
- [x] Gold : tableau de draft `hn_draft_board` (vérifié le 2026-10-23 : 3 ligues, 53 repérés dans la nôtre)
- [x] Gold : plafond par saison `hn_cap_outlook` (vérifié le 2026-10-23 : S27 engagés 55,2 M$ + rachat 0,67 M$, cap space 1,63 M$)
- [x] Gold : coachs `hn_coach_board`, calendrier `hn_calendar`, alertes `hn_daily_alerts` (vérifié le 2026-10-23)
- [x] Gold : valeur d'un échange `hn_trade_value` (vérifié le 2026-10-23 : 169 joueurs ; Pålsson cédé = cap space S27 1,63 → 4,91 M$)
- [ ] Gold : progression par joueur entre deux relevés (`hn_player_progress` créée le 2026-10-23, vide tant qu'il n'y a qu'un jour de relevés)
- [x] Silver/gold : équipes adverses `hn_league_players`, `hn_club_compare`, `hn_coach_specials`, `hn_special_skills` (vérifié le 2026-10-23 : 5 clubs comparés)

## D. Skills
- [x] 6 skills `hockeynation-*` écrits depuis le guide, chaque fait sourcé [G:Rubrique] (2026-10-23)
- [x] Hypothèse des compétences clés par poste confirmée (2026-10-23 : Discord talonflame1/a_ferk 2026-04-04 + guide ; écarts à corriger au recalage : PWR manque aux attaquants, FOF n'est pas clé du centre, END gardien 7+ ; voir skill `hockeynation-adversaires`)
- [x] Validés par l'utilisateur (2026-10-23, « je valide TOUT »)

## E. Agents (fiche `docs/fiches/hockeynation/`, 2026-10-23)
- [x] Effectif : bilan par poste et par équipe, doubles postes, vieillissement (briefs validés par l'utilisateur le 2026-10-23)
- [x] Finances-personnel : plafond, prolongations, coachs, scouts (validé le 2026-10-23)
- [x] Académie : draft, U21 (ELC, Farm, départ), Import Draft (validé le 2026-10-23)
- [x] Entraînement : compétence et coach par joueur PRO/FRM, ordre de choix (validé le 2026-10-23)
- [x] Tactique : lignes, unités spéciales, Extra Attacker, ordre des coachs (validé le 2026-10-23 ; lignes B et C PRO à exporter)
- [x] Transferts : abandonné par l'utilisateur le 2026-10-23 (« ça ne sert à rien », pas d'export du marché) ; les cibles d'échange viennent de l'agent Tactique
- [x] Match : explication et journal des enseignements (33 matchs, validé le 2026-10-23)
- [x] Étude des adversaires (brief `2026-10-23-adversaires.md`, 4 clubs de l'autre ligue ; schedules et Team Ratings à exporter pour aller plus loin)

## F. Routine
- [ ] « Que faire aujourd'hui » Hockey Nation (agenda par jour de saison)
- [ ] Première chaîne d'agents complète en medium + Sonnet
