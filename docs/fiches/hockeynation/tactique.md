# Hockey Nation — fiche Tactique (lignes PRO)

Lue par l'agent `tactique` après `commun.md`.

## Skills
`hockeynation-match-calendrier` (lignes, pénalités, gardiens, mises au jeu), `hockeynation-joueurs`, `hockeynation-adversaires`.

## Rendu fixe (2026-10-29, « à chaque fois le même export, le même résultat »)
Le rendu tactique n'est plus rédigé à la main : on lit les vues, dans cet ordre, et on affiche les tableaux tels quels.
1. `gold.hn_tactique_effectif_poste` : **tous les joueurs PRO par poste** (C, LW, RW, LD, RD, G) avec note, END, FOF, rôles occupés ou RÉSERVE.
2. `gold.hn_tactique_rendu` : la lineup cible dans l'ordre de l'écran, un tableau par bloc : Lignes et paires D · Gardiens · Power play · Infériorité 4 hommes · Infériorité 3 hommes · 4 contre 4 · Gardien retiré · Rôles. Colonne `dans_le_jeu` = écart avec la dernière lineup exportée (🟥 case vide, 🟧 à changer).
3. `gold.hn_tactique_plan_rendu` : plan de jeu cible contre plan saisi.
4. `gold.hn_tactique_controle` : toutes les lignes doivent être `ok` avant de rendre.
Lineups B et C = copie exacte de A (rôle inconnu).

## Changer la lineup (après chaque étude de matchs)
- `UPDATE gold.hn_tactique_cible` (une ligne = un poste d'une unité ; `motif` à jour) et `gold.hn_tactique_plan`.
- Une ligne dans `gold.hn_tactique_journal` : changement, raison, test (mesure + date), résultat quand il est connu.
- Reporter la modification dans un fichier `sql/gold/0xx_hn_tactique_vN.sql` (la base seule ne se versionne pas).
- Règles de choix : END d'abord en L1/L2 (seuils L1 7+, L2 6+, D1 8+, D2 6+, G1 7+, tolérance −1) ; PP = SHO+PAS+SKA avec un FOF 7+ par unité ; PK = DEF+CHK+SKA+PWR ; un joueur une fois par type d'unité ; postes tenus sans −20 %.
- `silver.hn_lineups` ne lit que le dernier export (corrigé le 2026-10-29 : une case vidée dans le jeu restait remplie par un ancien export).

## Données
- `silver.hn_lineups`, `gold.hn_player_fit`, `silver.hn_players` (END, FOF, DSC, compétences), `gold.hn_position_keys`.

## Il me manque
- Le sens exact de 0/1/2 pour chaque réglage (lu dans l'ordre des libellés, voir mémoire `reference-hn-plan-de-jeu-libelles`) : à confirmer par un changement test.
- Capitaine et assistants : attributs cachés (leadership), non lisibles ; choix par expérience, aucun écart affiché.

## Livrable
1. Lignes A, B, C poste par poste, **joueur au poste où ses talents collent** ; aucun joueur hors de ses postes (−20 %).
2. Deux meilleurs FOF parmi les attaquants (mises au jeu).
3. Gardien titulaire et remplaçant ; nombre de matchs d'affilée avant fatigue (= END).
4. Lignes FRM, U21, U17 automatiques : seul levier = poste principal (« Swap position »).

## Rendu figé et objectif (2026-10-29, « ne change jamais le rendu »)
- Le rendu (tableaux, ordre, colonnes, pastilles, « jeu : X » entre parenthèses) ne change plus : mêmes vues, mêmes blocs, même ordre à chaque fois.
- Objectif permanent : **la meilleure tactique possible**, et la meilleure équipe possible. Chaque passage Transferts / Effectif / Match compare l'équipe à `gold.hn_tactique_effectif_poste` : une cible d'achat ou d'échange se juge sur ce qu'elle change dans la lineup (poste, END, FOF, PP/PK), puis la lineup cible est mise à jour (procédure ci-dessus).
- Lineup v2 saisie par l'utilisateur le 2026-10-29 (déclaré) ; à vérifier au prochain export des lineups (`gold.hn_tactique_controle`).
