# Lecteur d'exports - Six Zero League - 2026-10-30, lot 08:20 a 08:46 UTC (09:46 Paris)

## 1. Inventaire (bronze, depuis 08:00 UTC : 32 lignes)
| page_type (script) | nb | nature reelle | lu par silver ? | ce qu'on en tire |
|---|---|---|---|---|
| app_transfers | 12 | `/transfers` (marche, 52 annonces, `myBids` vide) ; `/seasons/current` ; effectifs adverses `/teams/{f5831a4b..., 57a27f7c...}/players` (17 joueurs chacun) + `player-stats` ; DOM marche ; negociations SignalR | marche oui (`silver.sz_transfer_listings`) ; saison, effectifs adverses, player-stats : non | marche a jour |
| app_team | 2 | DOM effectif (16 joueurs) + `/notifications/mine` | DOM : non (silver lit `/teams/mine/players`, absent du lot) | effectif inchange |
| app_competitions | 5 | `/cups/current` (finie), `/leagues/6c8d...` (Vanadium div 5) , notifications | `/leagues` non ; `my-competition` oui | saison terminee |
| app_overview | 6 | `/seasons/current/my-competition`, chat `/chat/messages`, negociations | classement/calendrier oui ; chat oui | Vanadium : 18/18, 5e, 19 pts |
| app_club_infrastructure | 1 | DOM niveaux (aucun upgrade abordable) | non (silver lit `/infrastructure/mine`, dernier 29/10) | Arene 7, Training 6, Academie 6, Fan shop 9 |
| app_national-teams | 6 | `/national-teams` (+ `mine`, France `players` et `trophies` vides `[]`), DOM | non | election ouverte, France rang 2, note 23 |

Aucun `/teams/mine/players`, `/finances/mine`, `/infrastructure/mine` dans ce lot : le dernier roster API est du 29/10 08:46 UTC. Le DOM app_team (08:46:34 UTC) le remplace pour nom/poste/ovr/age/salaire/statut, mais pas pour les competences.

## 2. Changements depuis le lot du 29/10 (roster 29/10 08:46 UTC vs DOM 30/10 08:46 UTC)
- Roster : 16 joueurs identiques, 0 parti, 0 arrive. Ages identiques (pas de +1, la saison n'est pas rouverte). Salaires identiques. Ovr identiques (Fournier 17, Lefebvre 14, Roger/Dupont/Bourgeois 11, Denis 8...). Aucun blesse, suspendu ou retraite dans le DOM (colonne STATUS vide sauf Denis).
- Frederic Denis (CB, 27 ans, ovr 8, 95 EUR) : toujours EN VENTE, mise a prix 1 000, 0 offre. Ma vente reste ouverte.
- Solde : 1 559 EUR (notifications et DOM). Aucune amelioration d'infrastructure abordable (Arene 7 500, Training 6 200, Academie 6 200).
- Marche : 52 annonces contre 30 le 29/10 (09:12 UTC) ; 22 nouvelles, 0 disparue, 16 encheres modifiees. Mes encheres (`myBids`) : aucune.
- Notifications : tactique complete, composition non auto-remplie, pas de choix de sponsor ni de pick U18, pas de prochain match, rapport d'entrainement du 28/10 17:17 UTC.
- Calendrier saison : Cup final complete (28/10) ; `Off-season` 29/10 12:00 UTC encore "pending" ; `Managers take office` 30/10 12:00 UTC (13:00 Paris) en attente.

## 3. Valeurs brutes que silver ne lit pas
Roster (DOM, 30/10) : GK Blanc 27 ans ovr 9 (145), GK Bourgeois 31 ovr 11 (150) ; CB Simon 20 ovr 10 (105), CB Denis 27 ovr 8 (95, en vente), CB Fournier 19 ovr 17 (150) ; LB A. Bertin 27 ovr 10 (100), LB Leroy 25 ovr 9 (80) ; RB Barros 31 ovr 10 (110), RB Roger 28 ovr 11 (110) ; LW Sundberg 30 ovr 10 (95), LW Lefebvre 28 ovr 14 (130) ; RW G. Bertin 26 ovr 9 (95), RW Dupont 19 ovr 11 (115), RW Lemaire 23 ovr 9 (95) ; P Benoit 20 ovr 10 (100), P Chevalier 25 ovr 9 (90). Masse salariale lue : 1 820 EUR/semaine.

Marche, meilleures annonces (silver les lit aussi) : Schmid LB 19 ans ovr 18 (165 ; offre 17 000 par AL Ahly1907 ; suivante 18 000) ; Kolodziej P 19 ovr 17 (150 ; depart 18 000, sans offre) ; Farinha CB 19 ovr 15 (140 ; 15 000) ; Bohm LB 31 ovr 13 ; Henriques LW 18 ovr 13 (125 ; depart 8 000, sans offre). Au-dessus de mon ovr: Schmid, Kolodziej, Farinha sont plus forts que mon meilleur de poste sauf CB Fournier 17. Tous inabordables : solde 1 559 EUR (mise minimale la moins chere hors 1 000 : ovr 8-9 sans interet, aucun achat chiffre justifie).

Elections nationales : `/national-teams/mine` -> France rang 2, note 23, `election.open = true`, candidats dont FC bresse (dudumomo) ; `votePending=false` dans les notifications.

## 4. Classement errone du script
| page_type | contenu reel | critere |
|---|---|---|
| app_overview | SignalR `chat/negotiate`, `/chat/messages`, `my-competition` | `source_url` |
| app_team | `/notifications/mine` (+ DOM effectif) | `source='dom'` = fiche ; sinon notifications |
| app_competitions | `/notifications/mine`, `/cups/current`, `/leagues/{id}`, negociations | `source_url` |
| app_transfers | marche + `/seasons/current` + effectifs adverses + `player-stats` adverses | `source_url` ; effectif adverse = `/teams/{uuid}/players` avec uuid different de 5b564d16 |
| app_national-teams | `/national-teams`, `mine`, `trophies`, `players`, notifications | `source_url` |
(`page_typee_reelle` non ajoute dans `docs/attentes/jeux/sixzeroleague.yaml` ; aucune section "Options observees" trouvee dans docs : a faire par l'agent principal.)

Nouveautes : aucune option de choix nouvelle dans ce lot ; deux sources non lues par silver a mentionner : `/seasons/current` (steps, dates des phases : Off-season, Managers take office) et `/teams/{uuid}/players` des deux clubs adverses f5831a4b (premier joueur Oscar Reis) et 57a27f7c (premier joueur Ksawery Sikora). Effet inconnu : pour les effectifs adverses, mesure = comparaison ovr par poste avec mon roster.

## 5. Reste a exporter (aujourd'hui, apres 13:00 Paris)
- Ecran Team > Players (pour `/teams/mine/players`) : competences, ages et ovr apres la prise de fonction.
- Ecran Club > Finances (pour `/finances/mine`) : le dernier solde API date du 30/10 06:53 UTC.
- Ecran Team > U18 : seulement si "Managers take office" ouvre un pick (`u18PickAvailable` est faux a 08:41 UTC).
