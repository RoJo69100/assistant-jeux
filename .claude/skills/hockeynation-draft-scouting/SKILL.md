---
name: hockeynation-draft-scouting
description: Règles Hockey Nation sur la draft et le scouting — classes de 100 joueurs par ligue PRO, rang, steals et busts, 10 choix (2 saisons), ordre inverse du classement, pré-instructions (3 cibles, repli, limites de position, 1 h avant), Import Draft ; scouts (8 au maximum, budget 300 000 $ par saison, salaires, durée des missions selon chef, poste, nationalité, rang), 3 rapports successifs. À charger pour préparer une draft, organiser le scouting ou juger un choix de draft dans un échange.
---

# Hockey Nation — draft et scouting

Sources : **[G:Draft]**, **[G:Scouting]**, **[G:Calendar]** (guide du 30/09/2026, lu le 2026-10-23). **[U]** = règle de l'utilisateur.

## Draft
- Chaque ligue PRO a sa classe : les 100 joueurs draftables des U17 de ses équipes. Rang 1 à 100 calculé sur la note au jour 1 : il y a des « steals » (sous-classés) et des « busts ».
- Nos propres U17 sont entièrement visibles ; les autres doivent être repérés.
- 10 choix : tours 1 à 5 de la saison et de la suivante ; échangeables. Ordre = inverse du classement final de la ligue.
- Pré-instructions : jusqu'à **3 cibles** ; repli = « Pick Top Ranked Available » (notre classement de draft) ou « Pick By Position » ; **limites de position par ligue** (ex. gardien = 1). Clôture **1 h avant** la draft, jour 63.
- Import Draft : 2 semaines avant (jour 49), 6 joueurs de 14 ans révélés, 1 à choisir avant la fin de saison (sinon au hasard) ; il rejoint l'U17, non draftable, puis l'U21 à 18 ans.
- Lecture d'un prospect [U, 2026-10-23] : talents fort/faible contre le poste avant tout (skill hockeynation-joueurs § Talents), puis compétences visibles et plafonds, compétences spéciales, puis stats (buts, assists). `gold.hn_draft_board`.

## Scouting
- Staff : 1 head scout (obligatoire, sinon aucune mission n'avance) + jusqu'à 7 assistants ; 10 candidats par jour ; contrat permanent reconduit chaque saison.
- Budget : +300 000 $ par saison, reliquat reporté. Salaires : head scout 1 500 $/jour, assistant 1 000 $/jour, payés jours 4 à 63 (60 jours). Budget épuisé = scouting arrêté.
- Missions du jour 4 au jour 63, 1 à 5 jours : base 1 jour (head scout) ou 2 (assistant) ; **+1 jour** si le poste demandé n'est pas son poste préféré ; **+1** si la nationalité demandée n'est pas la sienne ; **+1** pour un rang dans les 2 premiers tours (sauf joueur nommé).
- Rapports (3 au maximum par joueur) : 1er = note + talents ; 2e = 3 à 5 compétences (3 gardien, 4 défenseur, 5 attaquant) + nombre de compétences spéciales ; 3e = tout le reste.
- Renvoi immédiat = 5 jours de salaire d'indemnité (sauf scouts d'origine) ; ou fin de reconduction gratuite en fin de saison.
- Leçon S26 [Obs 2026-10-23] : les classes des ligues de nos choix venus d'autres équipes (74, 93) n'avaient aucun joueur repéré. En S27, nommer des joueurs de ces ligues (pas de pénalité de rang pour un joueur nommé).

## Vues
`silver.hn_draft_class`, `silver.hn_draft_picks` (préférences), `gold.hn_draft_board` (ligue, talents vs poste, état du scouting), `silver.hn_scouts`, `silver.hn_scouting_budget`.

## [Veille 2026-10-29] Mise à jour (V-20261029-10)
- **Pré-instructions** : sans cible principale, la sim suit le classement pré-draft du GM combiné aux besoins de poste réglés (d0ghouse, 2026-10-24 10:46). **U17** : chaque saison 7 jeunes de 15 ans, on en choisit un, les 6 autres reçoivent un poste pour qu'aucun poste ne manque (5 draftables dans 3 saisons, 2 non draftables joignent l'U21) (hnadmin, 2026-09-19). [Discord #general]

## [Veille intégrale 2026-10-29] Draft et scouting (V-A-16 à A-18, V-B-5, V-C-10, C-11)
- **Priorité des pré-instructions** : limites de position (par ligue) > cibles principales (de haut en bas) > classement du GM + repli ; on peut réordonner les 100 joueurs. [hnadmin 2022-09-29, 2025-12-27 ; V-A-16]
- **Équipes inactives / bots (inactifs depuis 28 jours)** : choisissent au hasard parmi les 20 meilleurs restants, cotes décroissantes (≈ 20 % pour le n° 1, 15 % pour le n° 2, avis talonflame1) ; le meilleur disponible est pris dans ≈ 17 % des cas (d0ghouse 2023-07-06) : un joueur classé 2-6 peut tomber, ne jamais conclure « j'aurai le n° 5 » ; toujours plusieurs cibles de repli. Lire le **MIN** du joueur, pas le MAX. [V-A-16, C-11]
- **Steals / busts (S14+)** : les « classiques » (mal classés exprès) et les vrais (démarrent bas puis progressent longtemps, ou déjà presque maxés) ; lecture = compétences plafonnées + talents + 3 rapports + plusieurs jours de journal ; beaucoup de joueurs de bas tours prennent leur retraite avant de maxer. Avis : les choix hors top 10 sont peu fiables depuis la réforme du 2024-03-24 (furysk, c0ntrail 2024-12-30), « trop tôt pour dire » (gordie_79). [d0ghouse 2024-05-05, 2026-04-18 ; V-A-17, B-5]
- **U17** : 7 jeunes par saison (5 draftables, 2 non draftables dont l'import) ; le choix libre est l'import ; les 6 autres reçoivent un poste pour qu'aucun poste ne manque ; les prospects de notre U17 vont à notre draft quelle que soit la ligue. [hnadmin 2026-09-19 ; d0ghouse 2025-05-30 ; V-A-18]
- **Scouts** : le budget de scouting s'accumule (peu de scouts les saisons de montée, plus avant une saison riche en choix) ; un head scout qui prend sa retraite sans qu'on le voie fait perdre une partie du budget : surveiller son statut à chaque ouverture. Scouting 2.0 actif depuis ~2023-04 ; scouts en tranches de rang (11-30, 31-50…) quand on tombe tard (avis). [trunkxolotl 2026-06-17 ; talonflame1 2026-04-16 ; V-B-5, C-10]
