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
