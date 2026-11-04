# Dossier derbymanager — composition — 2026-11-04 — carte + nouveau

1. **Carte** `docs/decisions/cartes/derbymanager/composition.md` : lis-la en entier. Chaque variable y a son endroit et son check : lance ses requêtes (groupées, colonnes choisies, `LIMIT`) et remplis les valeurs du jour. Ne relis pas les sources déjà notées.
2. **Nouveau depuis le commit c03238b** (ci-dessous) : à lire en entier. Une ligne qui change une règle, un avis ou un seuil → modifie le check de la carte (cite la source et la date) ; une variable nouvelle → ajoute une ligne.
3. **Joueur ou réglage absent de la carte** : recherche ciblée sur son nom dans tout l'historique (`--mots`, fichier `-cible.txt`).
4. **Fin** : carte à jour (valeurs, checks, sources), commit, puis `python pipelines/dossier.py derbymanager composition --marquer`.

## 0. Cœur commun `docs/decisions/cartes/_core/composition.md` (valeurs calculées le 2026-11-04)

| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| C1 | Prochain match | `select day, competition_kind, round_no, opponent, home, scheduled_at at time zone 'Europe/Paris' as coup_envoi_paris from core.fixture where game = 'derbymanager' and not played and day >= current_date order by day, scheduled_at nulls last limit 5` | Match d'aujourd'hui ou de demain : se prépare aujourd'hui | CLAUDE.md, inviolable 3 | aucune ligne |
| C2 | Joueurs du dernier relevé | `select position, name, age, rating, form, fatigue, injured, suspended, day from core.player_daily where game = 'derbymanager' and day = (select max(day) from core.player_daily where game = 'derbymanager') order by position, rating desc limit 40` | Forme et fatigue en échelle 0–1 (échelle du jeu : `core.game_params` echelle_*) | `docs/attentes/jeux/<jeu>.yaml` core | position=DC, name=Y. Messimy, age=25, rating=, form=, fatigue=, injured=, suspended=, day=2026-11-04 ; position=DC, name=J. Pilot, age=30, rating=, form=, fatigue=, injured=, suspended=, day=2026-11-04 ; position=DC, name=J. Mansfield, age=22, rating=, form=, fatigue=, injured=, suspended=, day=2026-11-04 ; position=DC, name=F. Schultze, age=18, rating=, form=, fatigue=, injured=, suspended=, day=2026-11-04 ; position=DC, name=H. Hardt, age=17, rating=, form=, fatigue=, injured=, suspended=, day=2026-11-04 ; … |
| C3 | Alertes joueurs | `select prio, domaine, alerte from gold.daily_alerts where game = 'derbymanager' and domaine in ('blessure', 'fatigue', 'forme', 'tactique', 'effectif') order by prio limit 15` | Blessé ou hors zone : jamais titulaire sans raison écrite | `core.alert_rule` | ⚠ erreur : canceling statement due to statement timeout |
| C4 | Classement | `select rank, team_label, played, points, wins, losses, gf, ga, is_mine from core.standing where game = 'derbymanager' and day = (select max(day) from core.standing where game = 'derbymanager') order by rank limit 20` | Force de l'adversaire lue au classement et à ses résultats | `docs/decisions/variables.md` § composition | ⚠ erreur : canceling statement due to statement timeout |
| C5 | Bilan de la saison | `select competition_kind, my_result, count(*) as n, round(avg(my_score), 1) as pour, round(avg(opp_score), 1) as contre from core.fixture where game = 'derbymanager' and my_result is not null group by 1, 2 order by 1, 2 limit 12` | Ce qui a marché / échoué : voir learnings du jeu | `outputs/<jeu>/learnings.md` | competition_kind=amical, my_result=D, n=2, pour=1.5, contre=1.5 ; competition_kind=amical, my_result=L, n=2, pour=0.0, contre=3.0 ; competition_kind=coupe, my_result=L, n=2, pour=1.0, contre=2.5 ; competition_kind=coupe, my_result=W, n=1, pour=5.0, contre=3.0 ; competition_kind=ligue, my_result=D, n=12, pour=0.8, contre=0.8 ; … |
| C6 | Agenda du jour | `select at_time, priority, category, action from gold.agenda where game = 'derbymanager' and day = current_date order by at_time limit 10` | Heure limite du réglage | `core.agenda_rule` | aucune ligne |
| C7 | Exports à refaire | `select ecran, statut, age_h from gold.exports_state where game = 'derbymanager' and statut <> '🟩 à jour' order by ordre limit 15` | Effectif ou tactique périmé : « exporte » avant la saisie | `core.export_rule` | ecran=Finances, statut=🟧 à refaire, age_h=48 ; ecran=Graduates, statut=🟥 jamais, age_h= ; ecran=Classement de la ligue, statut=🟧 à refaire, age_h=47 |

### Couverture de `docs/decisions/variables.md` § composition
| Variable obligatoire | Où |
|---|---|
| Adversaire : forces, résultats de la saison | C1, C4 ; effectif et tactique lue : carte du jeu |
| Forme, fatigue, blessures, suspensions | C2, C3 |
| Minutes lourdes | carte du jeu (stats de match) |
| Fit poste par poste, réglages dans l'ordre de l'écran | carte du jeu (rendu figé) |
| Règles du moteur | skill tactique du jeu |
| Ce qui a marché / échoué | C5 + learnings du jeu |
| Avis des amis, ce qui prouvera l'erreur | dossier et rendu |

La carte du jeu ci-dessous est le **delta** : ses variables s'ajoutent au cœur ; une variable qui répète une variable C renvoie à son numéro.

## Nouveau — règles, fiches, connaissance, learnings
- rien de nouveau.

## Nouveau — Discord / chat
- rien de nouveau.

## Du jour
- registre : `outputs/derbymanager/fait-2026-11-04.md`
- exports : `bronze.raw_pages` where game = 'derbymanager' and captured_at >= '2026-11-04'

## Couverture (à remplir)
| Source | trouvés | lus | retenus | écartés (pourquoi) |
|---|---|---|---|---|
| carte (variables) | | | | |
| nouveau règles | | | | |
| nouveau Discord/chat | | | | |
