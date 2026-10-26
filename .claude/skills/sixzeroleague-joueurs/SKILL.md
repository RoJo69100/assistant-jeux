---
name: sixzeroleague-joueurs
description: Règles Six Zero League (handball) sur les joueurs — 7 rôles (gardien, demi-centre, arrières, ailiers, pivot), 20 compétences de 1 à 100 en 4 groupes (Physique, Attaque, Défense, Gardien) et ce que fait chacune, compétences clés par rôle, échelle des notes, taille, main forte, hors-poste, blessures (durée, remplaçants, jeu en infériorité, forfait), retraite. À charger pour évaluer un joueur, choisir le sept de départ, les remplaçants ou gérer blessures et départs.
---

# Six Zero League — joueurs

Sources : **[W:Rubrique]** = wiki officiel, lu le 2026-10-18 (voir sixzeroleague-match). « Si une règle n'est pas écrite, elle n'est pas appliquée » [W:Introduction].

## Rôles [W:Players]
| Rôle | Mission |
|---|---|
| Gardien (GK) | Arrêts, arrêts propres (sans renvoi), relance |
| Demi-centre (CB) | Meneur : construit l'attaque au centre, fait circuler |
| Arrières gauche / droit (LB / RB) | Tireurs de loin, depuis les 9 m dans les demi-espaces |
| Ailiers gauche / droit (LW / RW) | Attaquants de couloir rapides : vont aux 6 m, convertissent les occasions proches |
| Pivot (P) | Joueur de ligne : tient sa place aux 6 m et finit sous pression |
Chaque rôle offensif a une position défensive associée [W:The game]. Effectif : 10 au départ, de 7 à 30 [W:Team, Transfers].

## Les 20 compétences (1 à 100, sans plafond caché) [W:Attributes]
| Groupe | Compétence | Effet |
|---|---|---|
| Physique | Agilité | Battre son défenseur vers les 6 m ; intercepter proprement sans faute |
| | Vitesse | Vitesse de déplacement en jeu (50 = base) : déborder, premier sur les ballons libres, montée vers les 6 m |
| | Force | Le pivot tient sa place et finit sous pression ; plus solide en défense directe |
| | Détente (Jumping) | Conversion des tirs en suspension (9 m et 6 m), contres |
| | Endurance | Peu d'endurance = plus d'erreurs et moins d'efficacité à mesure que le match avance |
| Attaque | Passe | Moins de passes ratées ou interceptées |
| | Tir | **Compétence de finition principale** : cadrage, conversion, envie de tirer ; compte pour désigner le tireur de 7 m |
| | Contrôle du ballon | Moins de fautes de zone et techniques, plus dur à voler ; le pivot garde mieux le ballon |
| | Jeu sans ballon | Démarquage : plus d'occasions de tir, plus souvent servi |
| | Technique | Précision, moins de poteaux, moins de mauvaises passes, provoque plus de fautes ; compte pour le tir de 7 m |
| Défense | Marquage | Défense directe : stoppe la montée aux 6 m, interceptions, moins de fautes |
| | Contre | Arrête les tirs avant le but (avec détente et anticipation) |
| | Anticipation | Lit le jeu : interceptions, contres, coupe les montées |
| | Duels | Gagne les 50/50 : interceptions, bloque pivot et montées, moins de fautes |
| | Récupération | Premier sur les ballons perdus, rebonds, déviations |
| Gardien | Réflexes | Compétence d'arrêt principale dans le jeu |
| | Un contre un | Clé sur les 7 m, secondaire aux 6 m |
| | Prise de balle | Garde le ballon au lieu de lâcher des rebonds dangereux |
| | Relance | Meilleures relances, moins interceptées |
| | Placement | Couvre plus de but : tirs adverses moins cadrés |
Un joueur de champ utilise Physique, Attaque et Défense ; un gardien Physique et Gardien.

## Compétences clés par rôle [W:Attributes]
| Rôle | À rechercher |
|---|---|
| Demi-centre | Passe, Technique, Jeu sans ballon, Tir (engagement et jets francs passent par lui) |
| Arrières | Tir, Détente, Technique, Passe |
| Ailiers | Vitesse, Agilité, Tir, Contrôle du ballon |
| Pivot | Force, Contrôle du ballon, Jeu sans ballon, Tir |
| Gardien | Réflexes, Un contre un, Placement, Prise de balle, Relance (toutes) |

## Comment les compétences jouent [W:Attributes, Match]
- Elles inclinent les probabilités des moments clés (tirs, passes, interceptions, arrêts), sans jamais décider seules. En duel, les deux notes comptent : deux joueurs forts s'annulent.
- **Taille** : avantage pour gardiens, arrières, demi-centres et pivots (plus grand = plus d'avantage ; plus petit que la moyenne coûte un peu).
- **Main forte** : ailiers et arrières jouent mieux du côté de leur main forte.
- **Hors poste** : affaiblit un peu les compétences d'attaque, de défense et de gardien ; pas les compétences physiques. Chiffres : **−20 % en attaque, −10 % en défense** ; un joueur de champ au but : **−20 %** ; les compétences physiques ne baissent jamais [Dev chat, Discord #chat 2026-10-13 11:41 et 16:28 ; chat jeu 2026-10-20 23:21]. Avis : un rôle appris supprime la pénalité (voir sixzeroleague-entrainement).
- Les 7 m sont tirés par le meilleur tireur et technicien sur le terrain.
- **Échelle des notes** (compétences, note générale, force de club, même échelle) : 1–14 Grassroots · 15–29 Amateur · 30–44 Semi-pro · 45–59 Professional · 60–74 Elite · 75–89 World class · 90–100 Legendary. La note générale dépend des compétences, mais aussi de la taille et de la main forte face au côté de jeu [Dev chat, Discord #chat 2026-09-23 12:30] ; elle n'est donc pas la simple moyenne des compétences.
- Statistiques et compétences d'un joueur : privées, sauf s'il est sur le marché [W:Players, Transfers].

## Blessures [W:Injuries]
- En match : sur un contact (faute, duel, tir sous pression). **Arrières, pivots et leurs défenseurs** sont bien plus exposés que les ailiers et les gardiens. À l'entraînement : plus l'intensité est haute, plus le risque et la durée augmentent (en High, environ 3 matchs d'absence, parfois 6).
- Durée : **1 à 6 matchs du club**, le plus souvent 1 ou 2. Comptée sur les matchs du club (ligue et coupe). Reportée sur la saison suivante.
- **Remplaçants** : un par rôle (onglet Tactique). Le remplaçant du rôle entre ; sinon un autre ; un gardien remplaçant ne joue dans le champ qu'en dernier recours. Les places vides sont remplies automatiquement par des joueurs valides ; chaque remplaçant n'entre qu'une fois.
- **À court de joueurs** : défense moins bonne, moins d'espaces et de tirs en attaque (passe, technique, contrôle et physique intacts) ; l'équipe en surnombre marque plus facilement. Jamais de forfait pour une blessure pendant le match.
- Pendant la convalescence : badge rouge, le joueur disparaît de la liste des disponibles ; un remplaçant valide prend sa place dans la composition, puis il revient automatiquement.
- Moins de 7 joueurs aptes → forfait 15–0 [W:Competitions].

## Âge et retraite [W:Retirement, Players, Training]
- L'âge augmente seulement **à la fin d'une saison de ligue**.
- Retraite envisagée **à partir de 33 ans** : chance à chaque anniversaire, croissante (à 33 ans presque tous continuent ; fin de la trentaine, la plupart arrêtent). Après l'annonce : **une saison complète de plus**, badge orange R, toujours sélectionnable et entraînable ; un joueur qui a annoncé sa retraite ne peut pas être vendu [W:Transfers].
- Progression et déclin selon l'âge : voir sixzeroleague-entrainement.

## [Obs] Nos données
- Le 2026-10-18 : effectif de 12 joueurs (Chomelix Cow), composition 7/7, formations attaque 5-1 / défense 6-0 (page Équipe → Tactique). API : `/api/teams/mine/players`, `/api/teams/mine/tactics/default`.
- [Obs 2026-10-18, utilisateur] Dans l'écran Tactique, un joueur placé hors de son poste apparaît **en orange** (pénalité de hors-poste visible). L'API donne une note par rôle (`roleOveralls`) non affichée à l'écran ; à son poste naturel elle est égale à la note générale. L'écran n'affiche pas de note, seulement l'alerte « out of position » (bulle orange). [Obs SQL 2026-10-18] `roleOveralls` est calculé **avant** la pénalité de hors-poste : son écart à la moyenne des compétences des groupes du rôle est le même au poste naturel (−0,4) et hors poste (−0,3), corrélation 0,92. Une composition hors poste vaut donc moins que la somme de ces notes (pénalité « légère » [W:Attributes], non chiffrée).
- La liste affiche une note (OVR) de 7 à 13 et des salaires de 75 à 145 € : niveau « Grassroots » en début de jeu.

## [Veille 2026-10-26] Mise à jour (V-20261026-2)
- Hors-poste : -20 % sur les compétences d attaque quand le joueur attaque hors poste, -10 % sur celles de défense quand il défend hors poste ; si deux joueurs permutent, les deux sont pénalisés ; le physique n est pas touché ; handicap plus visible chez les équipes fortes [Dev chat, Gazelle, 2026-10-24 12:43 à 13:03 UTC ; V-20261026-2].
- Hors-poste en **défense** (complète la puce ci-dessus) : la pénalité dépend de la **place défensive** du joueur, pas de sa place d'attaque. Le slot LB défend par défaut une demi-place, le pivot défend au centre : un P placé LB en attaque perd **12,5 %** sur ses compétences de défense ; placé sur une place centrale de l'onglet Défense, **aucune pénalité**. Les places centrales sont pour **CB et P** ; le CB peut en plus jouer à l'extérieur (corrigé le 2026-10-24 13:44). ⚠️ **12,5 % contredit le « 10 % en défense » (2026-10-13 et 2026-10-24) : non tranché**, hypothèse : la pénalité suit la distance entre places. [Dev chat, Gazelle, D:L304, L325, L329-331 ; V-20261026-11]
