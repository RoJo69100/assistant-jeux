# Question 3 BasketVibe : force du club, victoires, et ce qui distingue les clubs de tête (2026-11-11)

**Question 3a** : la force d'un club est-elle associée à sa part de victoires en ligue ?
**Question 3b** : à force égale, quelles compétences ou quels traits de l'effectif sont associés aux victoires ? Et la tactique ?

**Mesure.** Unité : le club. Variable : la part de victoires en ligue, soit victoires / (victoires + défaites), prise dans le dernier relevé de `silver.bv_standings_weekly` de chaque club (saison en cours). Exposition : `club_strength` du même relevé. Pour 3b : les compétences de `silver.bv_club_roster`, prises au milieu de la fourchette affichée, moyenne pondérée par les minutes par match (`min_avg`). Effet minimal qui compterait : 10 points de part de victoires par écart type.

**Population.** Les 35 clubs de `silver.bv_club_roster` (notre club n'y est pas). 4 matchs de ligue par club, soit 140 équipes-matchs. Ces clubs jouent 72 matchs distincts, répartis dans 3 ligues (12, 11 et 12 clubs ; les ligues sont reconstruites à partir du calendrier).

**Groupe moteur.** Tous les matchs sont dans le groupe v4 ligue : `groupe()` le donne pour les 72 matchs, tous joués à partir du 02/11. *Hypothèse* : les deux autres ligues utilisent le même moteur que la nôtre.

**Victoires.** Elles viennent du classement. Aucun score brut n'est utilisé. `my_result` n'existe que pour nos propres matchs.

**Bootstrap.** Par clubs, 2 000 tirages, graine 20261111.

## Résultats retenus

| # | classe | groupe | n clubs / équipes-matchs / matchs | estimé | IC 95 % | méthode | verdict |
|---|---|---|---|---|---|---|---|
| 1 | ÉTABLI | v4 ligue | 35 / 140 / 72 | +0,164 de part de victoires par +1 ET de force (ET = 2,83 points de force), soit +0,058 par point | [+0,099 ; +0,321] | bootstrap par clubs | association présente |
| 1' | ÉTABLI (contrôle) | v4 ligue | 35 / 140 / 72 | à l'intérieur d'une même ligue : +0,174 | [+0,118 ; +0,346] ; permutation de la force dans chaque ligue (5 000 tirages) : p = 0,0008 | bootstrap par clubs et permutation | association présente |
| 1'' | ÉTABLI (sensibilité) | v4 ligue | 34 / 136 / 72 (sans KK Glen Johnson, force 42,8) | +0,150 par ET | [+0,058 ; +0,230] | bootstrap par clubs | association présente |
| 2 | ÉTABLI | v4 ligue | 35 / 140 / 72 | force relative (force du club − force moyenne de ses 4 adversaires) : +0,150 par ET | [+0,106 ; +0,257] | bootstrap par clubs | association présente |
| 2' | — | v4 ligue | 35 / 140 / 72 | force adverse, à force propre égale : −0,174 par ET | [−0,402 ; +0,051] | régression multiple, bootstrap par clubs | indéterminé : n trop petit |
| 3 | HYPOTHÈSE | v4 ligue | 35 / 140 / 72 (356 joueurs) | taille moyenne pondérée par les minutes, à force égale : +0,129 par +1 ET (2,07 cm) | [+0,019 ; +0,247] ; sans KK Glen Johnson : +0,114 [+0,004 ; +0,243] | régression multiple, bootstrap par clubs | association présente, mais fragile (15 variables testées) |
| 4 | — | v4 ligue | 35 / 140 / 72 | à force égale, aucune des 8 compétences ne se détache (pente partielle de −0,077 à +0,087) | les 8 IC contiennent 0 (défense : [−0,052 ; +0,221]) | régression multiple, bootstrap par clubs | indéterminé : n trop petit |
| 4' | — | v4 ligue | 5 clubs à 4-0 contre 30 | écart de force : +1,90 point | [−0,17 ; +3,72] | bootstrap par clubs | indéterminé : n trop petit |
| 5 | IMPOSSIBLE | — | tactique : 55 lignes dans `silver.bv_match_tactics`, toutes de 1 équipe (la nôtre) | — | — | — | donnée absente |

### ÉTABLI
- **R1. La force est associée aux victoires.**
  - La force du club (`club_strength`) est associée à la part de victoires, dans l'ensemble des clubs comme à l'intérieur d'une même ligue.
  - Le résultat résiste au retrait du club le plus faible, qui pèse beaucoup sur la pente.
  - Le coefficient de Spearman vaut +0,487, IC [+0,167 ; +0,740] (bootstrap par clubs).
- **R2. L'association tient en force relative.**
  - La force moyenne des adversaires varie peu d'un club à l'autre (écart type 1,31 contre 2,83 pour la force propre). Elle est peu corrélée à la force propre (r = −0,26).
  - Le calendrier des 4 premières journées ne crée donc pas l'association.
  - L'effet propre de la force adverse (coefficient négatif, le sens attendu) reste indéterminé.
- **Descriptif, sans test.** La force du club suit de près les compétences de l'effectif : r = +0,88 avec la moyenne des milieux de fourchette pondérée par les minutes (+0,70 avec les 5 joueurs les plus utilisés). C'est pour cette raison qu'en 3b, une fois la force contrôlée, il reste peu de variation à expliquer.

### HYPOTHÈSE
- **H1. Taille.** *Hypothèse* : à force égale, les effectifs plus grands (taille pondérée par les minutes) gagnent davantage.
  - Recoupement par requête : 197,3 cm en moyenne pour les clubs à 0 victoire (4 clubs) ; 199,6 ; 200,7 ; 200,7 ; 201,9 cm pour les clubs à 1, 2, 3 et 4 victoires.
  - Pourquoi ce n'est pas établi :
    - 15 variables ont été testées, ce qui donne environ 0,8 faux positif attendu ;
    - la borne basse de l'IC est proche de 0 ;
    - confusion probable : la composition par postes (plus de pivots) et le rebond.
  - Ce qui la confirmerait : la même pente partielle, avec une borne basse nettement au-dessus de 0, à 8 matchs par club ou plus (classement de la fin novembre).
  - Ce qui l'infirmerait : un IC qui contient 0 sur ces mêmes données.
- **H1 bis. Expérience.** Pente partielle −0,074 [−0,149 ; −0,007]. Le sens est contraire à l'intuition, et il y a beaucoup de tests : je la classe comme faux positif probable, à revoir avec le même critère que H1.
- **Simples, sans contrôle de la force.** La défense (+0,162 [+0,081 ; +0,249]) et le rebond (+0,109 [+0,007 ; +0,204]) sont associés aux victoires. Ces deux associations disparaissent une fois la force contrôlée : elles passent par la force du club (corrélation de 0,79 entre défense et force). On ne peut pas dire laquelle des compétences fait la force.

### IMPOSSIBLE avec les données actuelles
- **Tactique des clubs de tête.** `silver.bv_match_tactics` ne contient que nos réglages (55 lignes, 1 équipe). Aucun réglage d'un autre club n'est observé.
- **Compétences exactes.** 347 joueurs sur 356 ne sont visibles qu'en fourchette (largeur médiane 19 points). L'erreur de mesure atténue toute pente par compétence. *Hypothèse* : le jeu n'affiche les valeurs exactes qu'à leur propriétaire ; si c'est le cas, aucun export ne lève cette limite.
- **Modèle match par match** (qui bat qui, force contre force). Le vainqueur d'un match entre deux autres clubs ne se lit que dans le score brut, qui est exclu. Le classement n'a été relevé jour par jour que pour notre ligue, et à la seule 4e journée.

## Sources (exécutées ce tour)
- `python -I pipelines/etudes/q3_force_victoires.py 2000 20261111 0` : population complète, tous les chiffres des sections 3a et 3b. Le script est jetable et non commité ; il peut être supprimé.
- `python -I pipelines/etudes/q3_force_victoires.py 2000 20261111 50` : contrôle de sensibilité sans KK Glen Johnson.
- Requêtes `sql.py` :
  - colonnes de `silver.bv_club_roster`, `silver.bv_standings_weekly`, `gold.bv_league_top_players` et `silver.bv_matches` (`information_schema`) ;
  - inventaire de `bv_club_roster` : 35 clubs, 384 lignes, 364 en dernière capture, du 06/11 au 10/11, visibilité bracket ou full ;
  - fourchettes de `two_point` ;
  - relevés du classement par jour ;
  - jointure du classement avec les effectifs (36 équipes ; seule la nôtre n'a pas d'effectif) ;
  - `silver.bv_matches` et `silver.bv_fixtures` par compétition et statut (72 matchs de ligue terminés) ;
  - recoupement de la taille moyenne par nombre de victoires.

## Limites
- **Dépendance.** Le bootstrap par clubs traite les clubs comme indépendants. Or chaque match donne une victoire à un club et une défaite à un autre, et les victoires d'une ligue ont une somme fixe. La permutation à l'intérieur de chaque ligue sert de contrôle (p = 0,0008).
- **Bruit.** Avec 4 matchs, le bruit binomial d'une part de victoires vaut 0,25 (écart type), pour un écart type observé de 0,32 entre clubs. La plus grande partie de la variation des victoires est du hasard.
- **Moment des mesures.** La force et les effectifs sont relevés du 06/11 au 11/11, et non au jour de chaque match. Les transferts récents ne sont pas datés ici.
- **Minutes endogènes.** La pondération par les minutes dépend des choix de l'entraîneur adverse, et donc en partie des résultats.
- **Confusions probables en 3b.**
  - Colinéarité entre compétences (jusqu'à r = 0,61 entre `ball_handling` et `stamina`) et avec la force.
  - Composition par postes.
  - Tactique adverse non observée.
  - Les clubs sont tous humains (`is_human`) : il n'y a pas de contraste entre humains et robots.
- Aucun chiffre global toutes versions : un seul groupe (v4 ligue) est concerné.

## Export demandé
- Pour comprendre le Match Engine, j'ai besoin de : exporte la page des réglages utilisés d'un match entre deux autres clubs, ou d'un de nos matchs vue côté adversaire, si le jeu l'affiche. Parce que la tactique (`player_directives`, `defensive_focus`) des autres clubs est absente : `silver.bv_match_tactics` ne contient qu'1 équipe. *Hypothèse* : cette page existe. Sinon, la partie tactique de 3b reste hors d'atteinte.
- Pour comprendre le Match Engine, j'ai besoin de : exporte la page Classement des trois ligues après chaque journée, parce que le vainqueur de chaque match entre deux autres clubs manque hors score brut. L'écart de victoires d'un relevé à l'autre, croisé avec `silver.bv_fixtures`, donnerait qui a battu qui, sans utiliser de score. Aujourd'hui, le classement n'est relevé jour par jour que pour notre ligue.
