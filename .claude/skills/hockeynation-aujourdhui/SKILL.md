---
name: hockeynation-aujourdhui
description: Hockey Nation — que faire aujourd'hui : plan du jour en 5 blocs (exports, scouts, matchs joués des 4 équipes, tactique PRO si déclenchée, entraînement). Pour tout « que faire », « reprenons » ou plan du jour.
---

# Hockey Nation — que faire aujourd'hui

But et règles : `docs/attentes/charte-hockeynation.md`. Faits du jeu : `docs/fiches/hockeynation/resume.md`. Cartes : `docs/decisions/cartes/hockeynation/composition.md` et `defaite.md`. Leçons : `outputs/hockeynation/learnings.md`. Temps de lecture : 7 minutes pour tout le jeu (fixé, ne pas le redemander).

## Méthode (pas d'agent, quelques requêtes)
0. Charge le skill `deja-fait` et lis `outputs/hockeynation/fait-AAAA-MM-JJ.md` du jour : ce qui est fait ne sort pas du plan.
1. `select * from gold.hn_today` (jour de saison), `select * from gold.hn_daily_alerts order by prio` via `python -I pipelines/sql.py`.
2. Les cinq blocs ci-dessous, dans cet ordre, **et rien d'autre**.
3. Aucune ligne transferts, finances ni Trade Center. Seule exception : si `silver.hn_cap_now` donne un cap space négatif (−30 % en match, `resume.md`), une ligne « 🟥 URGENT · plafond négatif ». Les échéances du calendrier restent dans `gold.hn_today` / `resume.md`, pas dans le plan.

## Les 5 blocs

### 1. Exports en retard
`select ecran, dernier_paris, age_h, statut from gold.hn_exports_state` + `fait-<jour>.md`. Garder trois exports seulement : **Roster** (PRO, FRM, U21, U17), **page du match d'avant de chacune des 4 équipes** (absente de `silver.hn_games` / `silver.hn_game_detail` = à exporter), **Scouting staff**. Les lignes Salary cap, Trade Center, Training et Coaching staff ne sont pas demandées ici. Chaque export « à refaire » = une ligne Export.

### 2. Scouts
Un tableau, **une ligne par scout avec sa cible** : `gold.hn_scout_liste` (top poste+nation / poste / nation, joueurs nommés et rang), `gold.hn_scout_targets` (tous les joueurs à repérer par scout), `gold.hn_scout_board` (embauchés + candidats). Rendu en tableau, jamais en puces (`resume.md`, rendu scouts [U, 2026-10-29]). Relevé Scouting daté d'avant 24 h : ligne Export du bloc 1.

### 3. Matchs joués des 4 équipes (PRO, FRM, U21, U17)
- Résultat : `silver.hn_games` colonne `my_result`, jamais le score brut (`select game_id, team_level, season_day, game_type, my_result from silver.hn_games where my_result is not null order by scheduled_at desc limit 12`).
- Pour chaque défaite : l'échelle de la charte (composition → tactique → force relative → hasard), variables de la carte `defaite.md` (var. 2 à 9), et la ligne finale **« pouvait-on gagner : oui ou non, pourquoi »**.
- **Changer la structure : oui ou non, avec preuve** — la preuve est un chiffre de la carte `defaite.md` (réalisation, arrêts, PK, hors poste) comparé à la saison. Hasard prouvé (L-001, L-007) = « non, on ne change pas ».
- Deux défaites de suite d'une équipe : agent `analyste` d'office (charte). FRM, U21, U17 : une défaite ne s'analyse que si la page du match est exportée (carte `defaite.md` var. 13) ; sinon ligne Export au bloc 1.
- Sans défaite : une revue par semaine de tous les matchs, pas de ligne quotidienne.

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
`select * from gold.hn_player_potential` (tous nos joueurs : potentiel min–max, classe Fort / Solide / Moyen / Nul ↑, futur PRO / FRM / VIRER, adéquation au poste). Une ligne par joueur dont l'entraînement saisi ne colle pas à son poste ou à son potentiel ; règles d'entraînement : skill `hockeynation-coachs-entrainement` et `hockeynation-potentiel-joueurs`. Entraînement PRO / FRM seulement (écran Training, `resume.md` § Écrans). Aucune règle chiffrée nouvelle sans « (à valider) ».

## Format de réponse
- Un tableau par équipe quand le bloc le demande ; sinon `🟥 / 🟧 / 🟩 · bloc · action « fais X »`. Aucune ligne « rien à faire ». Le doute en une demi-ligne, avec ce qui prouvera l'erreur.
- Pas de règle de jeu sans source.
- Dernière ligne : **« Exports à faire aujourd'hui : … »**.
