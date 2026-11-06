---
name: hockeynation-aujourdhui
description: Hockey Nation — que faire aujourd'hui : plan du jour en 5 blocs (exports, scouts, matchs joués des 4 équipes, tactique PRO si déclenchée, entraînement). Pour tout « que faire », « reprenons » ou plan du jour.
---

# Hockey Nation — que faire aujourd'hui

**/compact dès 15 % de contexte restant.**

But et règles : `docs/attentes/charte-hockeynation.md`. Faits du jeu : `docs/fiches/hockeynation/resume.md`. Cartes : `docs/decisions/cartes/hockeynation/composition.md` et `defaite.md`. Leçons : `outputs/hockeynation/learnings.md`. Temps de lecture : 7 minutes pour tout le jeu (fixé, ne pas le redemander).

## Méthode (pas d'agent, quelques requêtes)
0. Charge le skill `deja-fait` et lis `outputs/hockeynation/fait-AAAA-MM-JJ.md` du jour : ce qui est fait ne sort pas du plan.
1. `select * from gold.hn_today` (jour de saison), `select * from gold.hn_daily_alerts order by prio` via `python -I pipelines/sql.py`.
2. Les cinq blocs ci-dessous, dans cet ordre, **et rien d'autre**, rendus **en deux temps** :
   - **Temps 1 « Lire »** : blocs 1 (exports), 2 (scouts) et 3 (analyse des matchs). Il se termine par la ligne **« Dis "actions" pour passer au temps 2. »** ; aucune saisie n'est demandée avant.
   - **Temps 2 « Agir »** (sur « actions ») : blocs 4 (tactique PRO, si déclenchée) et 5 (entraînement). **Au plus 5 actions par message, une saisie à la fois** ; l'utilisateur dit « fait » pour passer à la suivante, et je donne alors la suivante (jamais la liste entière d'un coup).
3. Aucune ligne transferts, finances ni Trade Center. Seule exception : si `silver.hn_cap_now` donne un cap space négatif (−30 % en match, `resume.md`), une ligne « 🟥 URGENT · plafond négatif ». Les échéances du calendrier restent dans `gold.hn_today` / `resume.md`, pas dans le plan.

## Les 5 blocs

### 1. Exports en retard
`select ecran, dernier_paris, age_h, statut from gold.hn_exports_state` + `fait-<jour>.md`. Garder trois exports seulement : **Roster** (PRO, FRM, U21, U17), **page du match d'avant de chacune des 4 équipes** (absente de `silver.hn_games` / `silver.hn_game_detail` = à exporter), **Scouting staff**. Les lignes Salary cap, Trade Center et Coaching staff ne sont pas demandées ici ; Training seulement dans le cas du bloc 5 (entraînement saisi absent de la base). Chaque export « à refaire » = une ligne Export.

### 2. Scouts
Un tableau, **une ligne par scout avec sa cible** : `gold.hn_scout_liste` (top poste+nation / poste / nation, joueurs nommés et rang), `gold.hn_scout_targets` (tous les joueurs à repérer par scout), `gold.hn_scout_board` (embauchés + candidats). Rendu en tableau, jamais en puces (`resume.md`, rendu scouts [U, 2026-10-29]). Relevé Scouting daté d'avant 24 h : ligne Export du bloc 1.

### 3. Matchs joués des 4 équipes (PRO, FRM, U21, U17)
- **Une ligne par match joué des 4 équipes, victoire ou défaite** (matchs depuis le dernier passage, `fait-<jour>.md`) : `| Équipe | Match | Résultat | Mérité ou non | Règle L-nnn pour/contre |`.
  - Résultat : `silver.hn_games` colonne `my_result`, jamais le score brut (`select game_id, team_level, season_day, game_type, my_result from silver.hn_games where my_result is not null order by scheduled_at desc limit 12`).
  - **Mérité ou non** : tirs et xG (`teams->'home'->'stats'` et `teams->'away'->'stats'` de `silver.hn_game_detail`, clés `shots`, `xGoalsF`…, côté domicile ou extérieur selon `home` de `silver.hn_games` ; carte `defaite.md` var. 2 et 6) contre réalisation et arrêts du match, chacun comparé à la **moyenne de la saison de la même équipe** ; la colonne « Mérité ou non » affiche le nombre de matchs de la comparaison (« non mérité, sur n matchs ») ; volume supérieur mais réalisation et arrêts inférieurs = « non mérité » (hasard), l'inverse aussi pour une victoire.
  - **Règle L-nnn** : celle de `outputs/hockeynation/learnings.md` que ce match confirme (pour) ou contredit (contre), écrite « L-001 pour » ; sinon « aucune règle concernée ». Le pour/contre s'inscrit dans le registre (charte, § Registre du Match Engine).
  - Match FRM, U21 ou U17 : marqué « expérience sans notre choix » (lignes automatiques).
  - **Numérotation** : « match n° k » (k = rang du match de ligue de l'équipe cette saison, plus la date) ; jamais « J11 » tiré de `season_day`, qui est le jour de saison et non la journée de ligue. Les amicaux sont comptés à part. Comparaison : ligue de la saison en cours seule.
  - **Profondeur obligatoire par match** (carte `defaite.md` rendu 1 à 3) : tirs par période et xG, PP (buts / occasions) et PK (buts encaissés / occasions adverses) avec `summary.scoring.strength` et `teams.*.stats.ppAttempts`, pertes et prises, PIM, gardien (arrêts / tirs subis, %, nom) et joueurs (points, +/- ≤ −2, PIM ≥ 4) dans `silver.hn_game_detail.boxscore`. Par équipe, un tableau des joueurs de la saison : matchs, TOI, buts, passes, tirs, +/-, PIM, pertes, prises, fatigue max. Lire la lineup contre ces chiffres avant de répondre « on ne change rien ».
- **Analyse des unités — pour chaque match PRO** (pas FRM, U21, U17), un tableau par unité : L1, L2, L3, L4, paires D1/D2/D3, gardien, PP1, PP2, PK1, PK2, 4 contre 4 : `| Unité | Temps de glace | Tirs pour | Tirs contre | Buts pour | Buts contre | Fonctionnelle : oui/non, preuve |`.
  - **Coût : au plus 6 appels pour tout le bloc 3** (une requête par unité de mesure, sur tous les matchs d'un coup, pas une par match) : (1) composition `silver.hn_lineups` (`day`, `lineup`, `line`, `slot`, `player_id`) reliée au match par la date ; (2) `boxscore` par joueur (`toi`, `shots`, `goals`, `assists`, `diff`, `pim`) ; (3) `events` types `Shot` (`shooter`, `goalie`, `teamId`) et `Goal` (`scorer`, `strength`, `teamId`) ; (4) `summary.scoring[].strength` (EVEN / PP / SH) ; (5) `teams.*.stats` (`ppAttempts`, `ppGoals`, `penaltyTotal`, `shots`, `xGoalsFor`) ; (6) gardien : arrêts / tirs subis.
  - **Ce qui se mesure** (vérifié le 2026-11-06 sur `silver.hn_game_detail`) : temps de glace, tirs, buts, passes, +/- et PIM **par joueur** (`boxscore`), donc par unité en additionnant les joueurs de l'unité (`silver.hn_lineups`) ; tirs et buts **pour** par unité via le tireur / buteur de chaque événement ; PP et PK en bloc (force `PP` / `SH` des buts, `ppAttempts`, `ppGoals`) ; gardien (tirs `goalie` de chaque événement `Shot`).
  - **Ce qui ne se mesure pas** : `events` ne dit pas quels joueurs sont sur la glace, et `boxscore` ne donne ni changements ni temps par unité. Donc, **écrit tel quel dans la case, jamais inventé** : « non mesurable : il manque les joueurs sur la glace à chaque tir » pour les tirs et buts **contre** d'une unité L / D ; « non mesurable : PP1 et PP2 ne sont pas séparées dans la force du but (seulement PP) » pour PP1 / PP2 et PK1 / PK2 pris séparément (le temps par unité = somme des `toi` de ses joueurs, à titre d'ordre de grandeur, dit comme tel) ; le 4 contre 4 : « non mesurable » sauf buts marqués avec la force 4v4 s'il apparaît dans `summary.scoring`. Le +/- d'un joueur est le seul chiffre « contre » disponible : le citer comme indice, pas comme preuve d'unité.
  - **Verdict « fonctionnelle »** : « oui » ou « non » seulement avec une preuve mesurée ; sinon « indéterminé : non mesurable ». **Les buts attendus (xG) et la possession ne suffisent jamais à conclure une défaite** : ils servent à la colonne « Mérité ou non », pas au verdict d'une unité.
- Pour chaque défaite en plus : l'échelle de la charte (composition → tactique → force relative → hasard), variables de la carte `defaite.md` (var. 2 à 9), et la ligne finale **« pouvait-on gagner : oui ou non, pourquoi »**.
- **Changer la structure : oui ou non, avec preuve** — la preuve est un chiffre de la carte `defaite.md` (réalisation, arrêts, PK, hors poste) comparé à la saison. Hasard prouvé (L-001, L-007) = « non, on ne change pas ».
- Deux défaites de suite d'une équipe : agent `analyste` d'office (charte). FRM, U21, U17 : une défaite ne s'analyse que si la page du match est exportée (carte `defaite.md` var. 13) ; sinon ligne Export au bloc 1.

### 4. Tactique PRO — seulement si déclenchée
Déclencheurs (charte) : (a) lineup exportée d'avant le dernier changement (`gold.hn_exports_state`, ligne Lineups PRO) ; (b) case vide, hors poste, joueur parti (`select * from gold.hn_tactique_controle`, `gold.hn_saisie_lignes` où `controle <> 'ok'`) ; (c) un test arrive à échéance ; (d) deux défaites de suite (bloc 3) ; (e) nouveau joueur (`silver.hn_players`). Aucun déclencheur = bloc absent, pas de ligne « rien à faire ».
Si déclenchée : rendu **figé du 2026-10-29**, tel quel, via `gold.hn_tactique_effectif_poste`, `gold.hn_tactique_rendu`, `gold.hn_tactique_plan_rendu`, `gold.hn_tactique_controle` (carte `composition.md` § Rendu, étapes 1 à 6). Lineups B et C = copie de A. Prochain match et heure limite : `gold.hn_adversaires` (lineup saisie 1 h avant au moins).

**Règles de test** (un réglage à la fois ; chacune avec ce qui prouvera l'erreur et son échéance en matchs, C4) :
| Test | Ce qui prouvera que j'avais tort | Échéance |
|---|---|---|
| Plan de jeu : shift length short (depuis 2026-10-29, `resume.md`) | la L1 encaisse plus de buts qu'avant le test (carte `composition.md` var. 9) → retour à normal | 10 matchs |
| PP1/PP2, un seul changement à la fois | taux de PP sous 20,7 % (S26, L-006) sur la période | 5 matchs (à valider) |
| Infériorités PK, un seul changement à la fois | taux de PK sous 70 % (niveau des défaites S26, L-006) | 5 matchs (à valider) |
Amical seulement quand un de ces tests est ouvert (carte `composition.md` var. 12).

### 5. Entraînement des joueurs
**Preuve que l'entraînement saisi est en base** : `select team_level, count(*) joueurs, max(captured_at) as saisi_le from silver.hn_training_log group by team_level` (dernier journal saisi, par équipe) et `select team_level, count(*) from gold.hn_training_plan group by team_level` (plan lu). Citer la date `saisi_le` dans la ligne du bloc. Si une équipe (PRO ou FRM) n'a aucune ligne ou une date d'avant le dernier changement connu d'entraînement (`fait-<jour>.md`), ajouter **dans ce cas seulement** la ligne Export « Training » au bloc 1.
`select * from gold.hn_player_potential` (tous nos joueurs : potentiel min–max, classe Fort / Solide / Moyen / Nul ↑, futur PRO / FRM / VIRER, adéquation au poste). Règles d'entraînement : skill `hockeynation-coachs-entrainement` et `hockeynation-potentiel-joueurs`. Aucune règle chiffrée nouvelle sans « (à valider) ».
**Rendu : un tableau par équipe, PRO, FRM, U21, U17, jamais mélangés, avec l'ordre de choix en première colonne** (`gold.hn_training_plan`, colonne `ordre`) : c'est la liste que l'utilisateur ressaisit dans l'écran Coach pick order, possible pour les 4 équipes. Tous les joueurs de l'équipe y figurent, les plafonnés en fin de liste. L'ordre n'est pas âge puis note : marge de progression attendue d'abord, puis âge, puis note (`sql/gold/033_hn_training_plan.sql`), et il ne joue que si un coach dépasse sa capacité (head 9 joueurs, assistant 6, `01-coachs.md`) : vérifier la charge de chaque coach avec le plan proposé.
Compétence et coach par joueur : PRO et FRM seulement (U21 et U17 : compétence au hasard, seul l'ordre se règle). **Une compétence plafonnée ne s'entraîne pas** : avant toute proposition, lister les compétences OUVERTES de chaque joueur (roster `silver.hn_api` route `/team/:id/roster`, `skills[]` où `max` est faux, comme `gold.hn_training_plan`) et ne choisir que parmi elles. Par compétence ouverte : niveau, clé du poste ou non (`gold.hn_position_keys`), talent fort, meilleur coach de l'équipe (`/club/:id/coaching-staff`) ; sans coach compétent, aucun bonus. Un joueur qui n'a qu'une compétence ouverte, ou dont la seule ouverte n'a pas de coach, ne change pas. `gold.hn_training_plan` donne déjà le meilleur choix : un changement proposé doit battre ce choix sur une compétence ouverte, sinon on garde.

**Avant les propositions : l'ordre de choix de chaque équipe, à vérifier par l'utilisateur.** Un tableau par équipe (PRO, FRM, U21, U17) : `| Ordre | Joueur | Coach de la ligne |` (`gold.hn_training_plan`, colonnes `ordre` et coach ; U21 et U17 : l'ordre seul compte, coach affiché s'il existe). Puis seulement les propositions de changement. **Jamais une compétence déjà au plafond du joueur** (`max` vrai) : si aucune compétence ouverte, le joueur est en fin de liste sans proposition.

## Format de réponse
- Un tableau par équipe quand le bloc le demande ; sinon `🟥 / 🟧 / 🟩 · bloc · action « fais X »`. Aucune ligne « rien à faire ». Le doute en une demi-ligne, avec ce qui prouvera l'erreur.
- Pas de règle de jeu sans source.
- Dernière ligne : **« Exports à faire aujourd'hui : … »**.
