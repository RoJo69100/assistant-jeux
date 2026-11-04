# Dossier hockeynation — composition — 2026-11-04 — carte + nouveau

1. **Carte** `docs/decisions/cartes/hockeynation/composition.md` : lis-la en entier. Chaque variable y a son endroit et son check : lance ses requêtes (groupées, colonnes choisies, `LIMIT`) et remplis les valeurs du jour. Ne relis pas les sources déjà notées.
2. **Nouveau depuis le commit d1eaf11** (ci-dessous) : à lire en entier. Une ligne qui change une règle, un avis ou un seuil → modifie le check de la carte (cite la source et la date) ; une variable nouvelle → ajoute une ligne.
3. **Joueur ou réglage absent de la carte** : recherche ciblée sur son nom dans tout l'historique (`--mots`, fichier `-cible.txt`).
4. **Fin** : carte à jour (valeurs, checks, sources), commit, puis `python pipelines/dossier.py hockeynation composition --marquer`.

## 0. Cœur commun `docs/decisions/cartes/_core/composition.md` (valeurs calculées le 2026-11-04)

| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| C1 | Prochain match | `select day, competition_kind, round_no, opponent, home, scheduled_at at time zone 'Europe/Paris' as coup_envoi_paris from core.fixture where game = 'hockeynation' and not played and day >= current_date order by day, scheduled_at nulls last limit 5` | Match d'aujourd'hui ou de demain : se prépare aujourd'hui | CLAUDE.md, inviolable 3 | day=2026-11-04, competition_kind=ligue, round_no=, opponent=Little Rock Hitmen U17, home=False, coup_envoi_paris=2026-11-04 23:00:00 ; day=2026-11-05, competition_kind=ligue, round_no=, opponent=New Mexico Ogres U21, home=False, coup_envoi_paris=2026-11-05 00:00:00 ; day=2026-11-05, competition_kind=ligue, round_no=, opponent=Oudega Hûnekop Flyers, home=True, coup_envoi_paris=2026-11-05 17:00:00 ; day=2026-11-05, competition_kind=ligue, round_no=, opponent=Dallas Goats U21, home=True, coup_envoi_paris=2026-11-05 18:45:00 ; day=2026-11-05, competition_kind=ligue, round_no=, opponent=Not Fast J… |
| C2 | Joueurs du dernier relevé | `select position, name, age, rating, form, fatigue, injured, suspended, day from core.player_daily where game = 'hockeynation' and day = (select max(day) from core.player_daily where game = 'hockeynation') order by position, rating desc limit 40` | Forme et fatigue en échelle 0–1 (échelle du jeu : `core.game_params` echelle_*) | `docs/attentes/jeux/<jeu>.yaml` core | position=C, name=Alexander de Bruin, age=31, rating=72, form=, fatigue=, injured=, suspended=, day=2026-11-04 ; position=C, name=Vladislav Papež, age=24, rating=70, form=, fatigue=, injured=, suspended=, day=2026-11-04 ; position=C, name=Kamil Chromý, age=32, rating=57, form=, fatigue=, injured=, suspended=, day=2026-11-04 ; position=C, name=Petr Hrdlička, age=20, rating=56, form=, fatigue=, injured=, suspended=, day=2026-11-04 ; position=C, name=Alfréd Višňovský, age=22, rating=54, form=, fatigue=, injured=, suspended=, day=2026-11-04 ; … |
| C3 | Alertes joueurs | `select prio, domaine, alerte from gold.daily_alerts where game = 'hockeynation' and domaine in ('blessure', 'fatigue', 'forme', 'tactique', 'effectif') order by prio limit 15` | Blessé ou hors zone : jamais titulaire sans raison écrite | `core.alert_rule` | ⚠ erreur : canceling statement due to statement timeout |
| C4 | Classement | `select rank, team_label, played, points, wins, losses, gf, ga, is_mine from core.standing where game = 'hockeynation' and day = (select max(day) from core.standing where game = 'hockeynation') order by rank limit 20` | Force de l'adversaire lue au classement et à ses résultats | `docs/decisions/variables.md` § composition | ⚠ erreur : canceling statement due to statement timeout |
| C5 | Bilan de la saison | `select competition_kind, my_result, count(*) as n, round(avg(my_score), 1) as pour, round(avg(opp_score), 1) as contre from core.fixture where game = 'hockeynation' and my_result is not null group by 1, 2 order by 1, 2 limit 12` | Ce qui a marché / échoué : voir learnings du jeu | `outputs/<jeu>/learnings.md` | competition_kind=amical, my_result=W, n=2, pour=3.5, contre=2.0 ; competition_kind=ligue, my_result=L, n=51, pour=2.9, contre=4.8 ; competition_kind=ligue, my_result=W, n=81, pour=4.8, contre=2.4 ; competition_kind=playoff, my_result=L, n=6, pour=2.8, contre=4.7 ; competition_kind=playoff, my_result=W, n=2, pour=2.5, contre=1.0 |
| C6 | Agenda du jour | `select at_time, priority, category, action from gold.agenda where game = 'hockeynation' and day = current_date order by at_time limit 10` | Heure limite du réglage | `core.agenda_rule` | aucune ligne |
| C7 | Exports à refaire | `select ecran, statut, age_h from gold.exports_state where game = 'hockeynation' and statut <> '🟩 à jour' order by ordre limit 15` | Effectif ou tactique périmé : « exporte » avant la saisie | `core.export_rule` | ecran=Office > Salary cap, statut=🟧 à refaire, age_h=99 ; ecran=Trade Center > offres, statut=🟧 à refaire, age_h=149 ; ecran=Trade Center > recherche, statut=🟧 à refaire, age_h=191 ; ecran=Lineups PRO, statut=🟧 à refaire, age_h=108 ; ecran=Training (journal), statut=🟧 à refaire, age_h=149 ; … |

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
### `.claude/skills/hockeynation-adversaires/SKILL.md` — 1 lignes ajoutées, 1 sur le sujet
description: Hockey Nation, adversaires : exports à faire sur une équipe adverse, lecture de sa force (talents vs poste, coachs, gardiens, plafond). Avant un match important ou une série de playoffs.

### `.claude/skills/hockeynation-coachs-entrainement/SKILL.md` — 13 lignes ajoutées, 12 sur le sujet
description: Hockey Nation, coachs et entraînement : 3 types de coachs, compétences, head coach, plafonds U17/U21, embauche, entraînement quotidien et maxings. Pour recruter un coach ou régler l'entraînement PRO/FRM.
Ce fichier est un index : le contenu est dans `references/`. Lis seulement la section utile à la question ; chaque fichier reprend telle quelle une section de l'ancien SKILL.md (contenu inchangé).
| Fichier | Section |
|---|---|
| `references/00-introduction.md` | Introduction et sources |
| `references/01-coachs.md` | Coachs |
| `references/02-choix-des-coachs-consigne-de-l-utilisate.md` | Choix des coachs (consigne de l'utilisateur, 2026-10-25 ; [Discord, #general, 2025-12-24]) |
| `references/03-embauche-renvoi-retraite.md` | Embauche, renvoi, retraite |
| `references/04-entrainement.md` | Entraînement |
| `references/05-vues.md` | Vues |
| `references/06-mise-a-jour-v-20261029-5.md` | [Veille 2026-10-29] Mise à jour (V-20261029-5) |
| `references/07-coachs-et-entrainement-v-a-13-a-a-15-v-b.md` | [Veille intégrale 2026-10-29] Coachs et entraînement (V-A-13 à A-15, V-B-2, V-C-9) |

### `.claude/skills/hockeynation-coachs-entrainement/references/00-introduction.md` — 3 lignes ajoutées, 2 sur le sujet
## Introduction et sources
Sources : **[G:Coaches]**, **[G:Training]** (guide du 30/09/2026, lu le 2026-10-23).

### `.claude/skills/hockeynation-coachs-entrainement/references/01-coachs.md` — 10 lignes ajoutées, 9 sur le sujet
## Coachs
- Types : réguliers (compétences plafonnées entre 4 et 10, 3 compétences spéciales), intérimaires (3-5, aucune spéciale, remplacent un poste vide), amateurs (équipes nationales).
- Staff par équipe : 1 head coach + 3 assistants. Le head coach supervise 9 joueurs à l'entraînement, un assistant 6.
- **6 compétences d'entraînement** au hasard parmi les 15 compétences de joueur (1 à 3 de gardien : 60 % en ont 1, 30 % 2, 10 % 3 ; un ancien gardien en a 3).
- **5 compétences de match** : OFP jeu offensif à 5 contre 5 (mieux avec une note offensive élevée), DFP jeu défensif (note défensive), BAT duels (note physique), PP supériorité, PK infériorité. **Celles du head coach comptent double.**
- Compétences spéciales : 3, débloquées à des niveaux d'expérience secrets (1re entre Bad et Average, 2e entre Solid et Very Good, 3e entre Excellent et Elite). **Seules celles du head coach jouent en match.** Utiles : Eye For Talent (meilleur joueur de 25 ans ou moins +1), Shining Star, Commander, Meditation, First/Second/Third Period.
- Progression : un coach employé progresse chaque jour ; un coach sans emploi ne progresse pas. Plafond en U17 : note 54 et expérience Average ; en U21 : note 69 et Very Good. Au-delà, il ne progresse plus.
- Expérience : par match officiel, plus vite en PRO qu'en FRM, U21 ou U17 (ex. None → Awful = 31 matchs PRO à domicile, 40 en U17).
- **Former un jeune coach** [U] : l'embaucher en U17 (le guide conseille de remplir l'U17 d'abord), le promouvoir quand il atteint le plafond. Promotion sans retour possible, seulement vers un poste tenu par un intérimaire, jusqu'au jour 35.

### `.claude/skills/hockeynation-coachs-entrainement/references/02-choix-des-coachs-consigne-de-l-utilisate.md` — 5 lignes ajoutées, 4 sur le sujet
## Choix des coachs (consigne de l'utilisateur, 2026-10-25 ; [Discord, #general, 2025-12-24])
- Le critère est la **somme des 5 compétences de match** (OFP+DFP+BAT+PP+PK), le head comptant double ; l'entraînement vient après. PRO : la meilleure note de match tout en gardant les compétences d'entraînement utiles. FRM : jeunes coachs à potentiel. U21 : meilleur entraînement sans note de match nulle. U17 : jeunes coachs à développer, ou plafonnés à 54.
- Toujours proposer des jeunes coachs à potentiel : âge ≤ 45, expérience ≤ 3, au moins 2 compétences de match à 7 ou plus. Promotion U17/U21 → FRM/PRO quand ils sont plafonnés [Discord, #general, 2026-02-17].
- Limite d'expérience en FRM : non trouvée dans le guide ni dans Discord (10-25) ; à tester à l'offre.

### `.claude/skills/hockeynation-coachs-entrainement/references/03-embauche-renvoi-retraite.md` — 7 lignes ajoutées, 6 sur le sujet
## Embauche, renvoi, retraite
- Embauche du jour 1 au jour 35 (fin de la fenêtre I) ; jusqu'à 12 offres par jour (une par poste) ; réponse au début de la journée suivante, rien le 1er jour.
- Le coach choisit la **meilleure offre** : PRO > FRM > U21 > U17, puis head coach > assistant au même niveau ; à égalité, tirage au sort.
- Contrat permanent, salaire non public, hors plafond salarial.
- Protégé du renvoi pendant sa 1re saison au club. Renvoi immédiat ensuite (intérimaire à la place).
- Retraite à 65 ans ; un coach libre peut se retirer après 1 à 3 saisons sans club. Anciens joueurs de 38 ans et plus : peuvent postuler comme coach.

### `.claude/skills/hockeynation-coachs-entrainement/references/04-entrainement.md` — 6 lignes ajoutées, 5 sur le sujet
## Entraînement
- Quotidien, une compétence à la fois. Réglable en PRO et FRM seulement ; U21 et U17 entraînent une compétence au hasard, sans bonus ni malus.
- Chaque joueur choisit le coach le plus fort dans la compétence qu'il travaille, dans l'**ordre de choix** réglable (sinon aléatoire). Sans coach compétent : aucun bonus.
- Vitesse : âge (effet maximal dès 25 ans), niveau actuel (9 → 10 plus lent), Work Ethic, **niveau du coach dans la compétence** (effet fort). Le journal d'entraînement (`silver.hn_training_log`, `training_rate`) montre le coach choisi et la vitesse.
- Plafond atteint : le joueur passe à une compétence au hasard. Déclin dès 32 ans, les coachs n'y peuvent rien.

### `.claude/skills/hockeynation-coachs-entrainement/references/05-vues.md` — 3 lignes ajoutées, 2 sur le sujet
## Vues
`silver.hn_coaches`, `silver.hn_free_coaches`, `gold.hn_coach_board` (`match_sum` = OFP+DFP+BAT+PP+PK, `skills_open` = compétences encore sous leur plafond, `years_to_retire`), `silver.hn_training_log`.

### `.claude/skills/hockeynation-coachs-entrainement/references/06-mise-a-jour-v-20261029-5.md` — 4 lignes ajoutées, 3 sur le sujet
## [Veille 2026-10-29] Mise à jour (V-20261029-5)
- Le **rating d'équipe des coachs est un score calculé des compétences de match**, pas la note affichée du coach (cas du 29/10 : remplacement d'un intérimaire 43 → rating 57 puis 61). [Discord #general, hnadmin, 2026-10-29 11:49]
- Un coach à Puck Battling 80+ renforce les joueurs aux bonnes compétences physiques mais ne comble pas les faiblesses (avis du modérateur d0ghouse, 2026-08-24 20:04). Les compétences du head coach restent doubles après S27 (avis gordie_79, 2026-10-25). Coach Development Boost (S27) : effet exact non publié.

### `.claude/skills/hockeynation-coachs-entrainement/references/07-coachs-et-entrainement-v-a-13-a-a-15-v-b.md` — 6 lignes ajoutées, 6 sur le sujet
## [Veille intégrale 2026-10-29] Coachs et entraînement (V-A-13 à A-15, V-B-2, V-C-9)
- **Marché de coachs (depuis S17)** : marché ouvert ; une offre réussie renvoie automatiquement le coach en place (pas besoin de le renvoyer d'abord) ; le coach choisit la meilleure offre de poste (PRO > FRM > U21 > U17, puis head > assistant) et refuse un poste trop bas ; un coach renvoyé revient aussitôt dans le pool ; 2 jours de recherche. **Une seule offre de head coach par jour** (kenvald 2026-08-25) ; empiler les offres sur le n° 1 du marché fait perdre les autres bons coachs (avis). Remplace la réponse « début de la journée suivante ». [hnadmin 2025-01-02, 2025-02-04 ; d0ghouse 2025-04-10 ; V-A-13, C-9]
- **Spéciales par parcours** : coach U17 seul = max 1 spéciale, U21 = max 2, PRO = max 3 [d0ghouse 2024-03-24]. Arrêt de l'expérience et arrêt des compétences sont séparés ; un pop peut dépasser le plafond (U17 54, U21 69).
- **Places d'entraînement** : un head coach prend 9 joueurs, un assistant 6 ; une fois ses places remplies, il n'est plus choisissable (segi_3554 2024-03-29). Candidatures des jours 1-35 : 1 + intérimaires, plafonné à 10 (erzac 2024-03-25, formule d'avant le FRM, à revérifier). Anciens joueurs : coach dès 38 ans, scout dès 36 ans. Pool « Coaches → Tracker → Fired ». À vérifier à l'écran : « 12 offres par jour » du skill contre « 11/16 » cité par talonflame1 (2025-04-10). [V-B-2]
- **Spécialiser les coachs** : la note d'équipe des coachs est une moyenne de formule type OVR ; spécialiser par catégorie (OFP / DFP / BAT / PP / PK) donne une meilleure note ; chaque note booste les joueurs de ce type et ne comble pas les faiblesses : privilégier la catégorie où nos joueurs sont forts (croiser avec `gold.hn_coach_options`). [d0ghouse 2025-09-17, 2026-08-24 ; V-A-14]
- **Vitesse d'entraînement** : depuis S12 le « 100 % » du journal vaut ≈ 1,5 × l'ancien ; dépend de l'âge, du niveau (bas niveaux plus vite), de Work Ethic et du coach ; attaquants > défenseurs > gardiens ; U21 : entraînement aléatoire, même vitesse qu'en PRO. [hnadmin 2024-03-24 ; d0ghouse 2024-04-09, 2025-10-17 ; V-A-15]

### `.claude/skills/hockeynation-compositions-trades/SKILL.md` — 1 lignes ajoutées, 1 sur le sujet
description: Hockey Nation : construire les 4 équipes (PRO, FRM, U21, U17) avec montées, descentes et sorties, puis choisir les échanges en comptant les salaires. Avant tout rendu de rosters, lineups ou trades.

### `.claude/skills/hockeynation-contrats-finances/SKILL.md` — 14 lignes ajoutées, 13 sur le sujet
description: Hockey Nation, argent : plafond salarial, paies, pénalités, rachats, prolongations, contrats ELC et Farm, agents libres. Pour juger une prolongation, un rachat, une signature ou un échange.
Ce fichier est un index : le contenu est dans `references/`. Lis seulement la section utile à la question ; chaque fichier reprend telle quelle une section de l'ancien SKILL.md (contenu inchangé).
| Fichier | Section |
|---|---|
| `references/00-introduction.md` | Introduction et sources |
| `references/01-plafond-salarial-pro.md` | Plafond salarial (PRO) |
| `references/02-rachat-buyout.md` | Rachat (buyout) |
| `references/03-prolongation-agent.md` | Prolongation (agent) |
| `references/04-jeunes-elc-et-farm.md` | Jeunes : ELC et Farm |
| `references/05-agents-libres.md` | Agents libres |
| `references/06-vues.md` | Vues |
| `references/07-mises-a-jour-v-20261029-1-2-3-4-12.md` | [Veille 2026-10-29] Mises à jour (V-20261029-1, -2, -3, -4, -12) |
| `references/08-contrats-plafond-agents-v-a-8-a-a-12-a-2.md` | [Veille intégrale 2026-10-29] Contrats, plafond, agents (V-A-8 à A-12, A-24, V-B-4, V-C-3 à C-5, C-12) |

### `.claude/skills/hockeynation-contrats-finances/references/00-introduction.md` — 3 lignes ajoutées, 2 sur le sujet
## Introduction et sources
Sources : **[G:Finances]**, **[G:U21 Team]**, **[G:Farm Team]**, **[G:Free Agents]** (guide du 30/09/2026, lu le 2026-10-23).

### `.claude/skills/hockeynation-contrats-finances/references/01-plafond-salarial-pro.md` — 6 lignes ajoutées, 5 sur le sujet
## Plafond salarial (PRO)
- Plafond de départ 50 M$, varie chaque saison par multiples de 100 000 $, d'1 M$ au plus. Annonces : jour 1 (hausse ou baisse), jour 28 (fourchette), jour 57 (valeur officielle).
- S26 : 57,2 M$ ; S27 : 57,5 M$ (`silver.hn_finances.salary_cap_projection`).
- Cap space = plafond − salaire total payé en fin de saison. **Ne jamais passer sous zéro** : plus de signature, échanges refusés s'ils ajoutent du salaire, **−30 % aux compétences en match officiel** ; toujours dépassé en fin de saison = faillite et GM renvoyé.
- Paie quotidienne pendant la saison régulière, jours 8 à 42.

### `.claude/skills/hockeynation-contrats-finances/references/02-rachat-buyout.md` — 6 lignes ajoutées, 5 sur le sujet
## Rachat (buyout)
- Le joueur part tout de suite ; pénalité = **moitié du salaire restant**, répartie sur les années restantes.
- Interdit si l'effectif PRO tombe sous 12 attaquants, 6 défenseurs, 2 gardiens (sauf dépassement du plafond), si le coût est nul, ou pour un agent libre signé dans sa 1re saison.
- **Calcul [Obs, 2026-10-29, tiré de la règle ci-dessus ; `buyout-info` revenu vide pour Lauper, à confirmer à l'écran]** : la pénalité totale = ½ du salaire restant, répartie à parts égales sur les années restantes, donc le plafond n'est soulagé que de **50 % du salaire chaque saison** (Lauper 3 250 000 $ jusqu'en S29 : paie 4 875 000 $ au total, 1 625 000 $ par saison en S27, S28, S29 ; soulage 1 625 000 $ par saison). Un échange soulage 100 % : à préférer pour descendre sous le plafond. Rachat = joueur parti tout de suite ; vérifier le minimum de 2 gardiens avant.
- **Échanges et plafond négatif [G:Finances]** : un échange qui ajoute du salaire est refusé tant que le cap space est négatif.

### `.claude/skills/hockeynation-contrats-finances/references/03-prolongation-agent.md` — 5 lignes ajoutées, 4 sur le sujet
## Prolongation (agent)
- Seulement pendant la **dernière année** de contrat. 1re proposition immédiate, les suivantes en 2 à 6 jours (réponse garantie à la dernière mise à jour de la saison, et juste après un échange).
- Salaire demandé : note en début de saison, plafond, générosité de l'agent, **humeur** (happy → neutral → unhappy, +3 à 5 % de frais), salaire actuel, niveau de la ligue (ligue 3.x ou plus bas : +1 % dès 55, +3 % dès 70, +5 % dès 80).
- Durée : 1-5 ans à 22 ans ou moins, 1-7 ans de 23 à 29 ans, 1-3 ans à 30 ans et plus. Redemander risque une offre pire. Humeur remise à « happy » après un échange.

### `.claude/skills/hockeynation-contrats-finances/references/04-jeunes-elc-et-farm.md` — 9 lignes ajoutées, 8 sur le sujet
## Jeunes : ELC et Farm
- **Correction de l'utilisateur, 2026-10-25 [U]** : un U21 peut être monté directement en FRM ou en PRO, même avant 21 ans ; à 21 ans il monte automatiquement. Le texte du guide ci-dessous (ELC après la fenêtre I, Farm à 21 ans avec effet à 22 ans) est donc à ne pas opposer à l'utilisateur. Discord confirme que les U21 s'appellent en équipe supérieure (« call up », #general, 2026-09-13). À vérifier à l'écran : prix du contrat et jour d'effet.
- U21 → PRO : **ELC 3 ans, 50 % moins cher** ; signable après la fermeture de la fenêtre I, effet la saison suivante [guide, contredit par [U] ci-dessus].
- FRM → PRO : ELC jusqu'à 24 ans (durée selon l'âge et la fenêtre : 3 ans à 18-21 ans ; 22 ans → 3 ans avant la fenêtre I, 2 ans après ; 23 ans → 2 puis 1 ; 24 ans → 1 an, avant la fenêtre I seulement). 25 ans et plus : négociation, à conclure **avant la fin de saison** sinon il part. FRM de 25+ ans noté 70+ : demande lui-même un contrat PRO au jour 1.
- Contrat Farm : sans salaire, durée indéfinie, signable **seulement à 21 ans**, effet à 22 ans. Un U21 non signé part à 22 ans.
- Contrats PRO signés : actifs la saison suivante ; « Activate Now » possible avant la fermeture de la fenêtre I.
- Rétrograder : seulement un joueur sous ELC (vers U21 s'il a 21 ans ou moins) ; plus de salaire PRO pendant ce temps ; 3 jours avant de le rappeler ; interdit après le jour 35 ; **impossible pour un joueur signé comme agent libre**.
- FRM : 30 joueurs et 30 contrats au maximum ; au-delà en début de saison, libérations **au hasard** (plus de 15 attaquants, 8 défenseurs ou 3 gardiens).

### `.claude/skills/hockeynation-contrats-finances/references/05-agents-libres.md` — 5 lignes ajoutées, 4 sur le sujet
## Agents libres
- Offres du jour 1 au jour 35, salaire entre 90 % et 200 % de la demande ; 5 offres au maximum en même temps. Frenzy au jour 3 (offres jusqu'à 1 h avant).
- Le joueur ne regarde que les 3 meilleures offres ; chaque dollar compte. Demandes −5 à 10 % en début de saison, révisées jours 10, 20, 30.
- ELC possible pour un agent libre de 24 ans ou moins noté 69 ou moins, seulement si personne ne lui offre de contrat PRO.

### `.claude/skills/hockeynation-contrats-finances/references/06-vues.md` — 3 lignes ajoutées, 2 sur le sujet
## Vues
`silver.hn_finances`, `silver.hn_expiring` (agent, humeur, demande), `silver.hn_players` (`salary`, `contract_to`, `elc`, `frm`, `next_salary`), `gold.hn_cap_outlook` (engagements par saison, rachats, cap space S+1).

### `.claude/skills/hockeynation-contrats-finances/references/07-mises-a-jour-v-20261029-1-2-3-4-12.md` — 7 lignes ajoutées, 6 sur le sujet
## [Veille 2026-10-29] Mises à jour (V-20261029-1, -2, -3, -4, -12)
- **S27 (25/10/2026)** : Contract Year Special (actif quand il reste 1 an au contrat actif, même après prolongation anticipée, seulement pour les joueurs qui ont la compétence), FA ELC, Coach Development Boost, Agent Rework partie 1. **S28 (+63 jours, ~27/12/2026)** : activation des favors d'agents et **plancher salarial de 50 %** ; base de calcul non publiée. [Discord #general, hnadmin, 2026-10-25 06:46 et 2026-10-22 04:29 ; V-2]
- **ELC d'agent libre — hypothèse ⚠️** : un joueur écrit « ovr max 69 » (note maximale possible), notre texte dit « noté 69 ou moins » ; 1re saison 3-way, 2e et 3e 2-way. Avis de joueur non confirmé par hnadmin : vérifier à l'écran avant de bâtir un plan sur la note actuelle. [Discord #general, gordie_79, 2026-10-25 14:49-14:51 ; V-1]
- **Rachat** : le reste du salaire de la saison en cours est effacé, le futur est remplacé par un salaire de rachat, le coût baisse si on attend (hnadmin, 2025-07-02). Le plafond est libéré **immédiatement à l'action** (hnadmin, 2026-07-22 07:21, contexte du message non vu). L'écart avec « moitié du restant » se lève par le chiffre affiché à l'écran. [Discord #general ; V-3]
- **Échanges** : l'allègement du plafond et les pénalités s'appliquent dès l'**approbation** du trade, pas à la fin du traitement. [Discord #general, hnadmin, 2026-03-12 06:41 ; V-4]
- **Frenzy S27 (repères de prix, avis)** : Raymond Baker (LD/RD) 4 ans 9 050 000 $ (Odesa) ; Borer (min 81) demande 5,5 M × 5 ; les agents libres signés pendant la Frenzy disparaissent de la recherche avant l'annonce. Agents : réponse instantanée au début d'une négociation, humeur remise à « happy » après un échange, réponse garantie à la dernière mise à jour de la saison (hnadmin, 2026-04-22 et 2026-06-17). [Discord #events, .coleh, 2026-10-27 19:12-19:18 ; V-12]

### `.claude/skills/hockeynation-contrats-finances/references/08-contrats-plafond-agents-v-a-8-a-a-12-a-2.md` — 10 lignes ajoutées, 10 sur le sujet
## [Veille intégrale 2026-10-29] Contrats, plafond, agents (V-A-8 à A-12, A-24, V-B-4, V-C-3 à C-5, C-12)
- **Rachat — écart guide/staff** : la ligne « moitié du salaire restant » vient du guide ; le staff ne la confirme nulle part (hnadmin 2023-06-10, 2025-07-02 : restant de la saison effacé, futur remplacé par un salaire de rachat qui **diminue si on attend**). Lire le chiffre de l'écran (`buyout-info`) avant décision ; « moitié » = hypothèse. Rachat interdit si le PRO passe sous 12 attaquants / 6 défenseurs / 2 gardiens, sauf dépassement du plafond (d0ghouse 2025-01-28). [V-A-8]
- **Cap Space** : un seul chiffre depuis 2025, qui inclut les échanges approuvés ; −30 % si négatif plus d'1 h avant le match (d0ghouse 2025-09-03 ; hnadmin 2025-04-16, 2025-07-10). [V-A-7]
- **Demande de salaire** : fonction de la note au **début de saison** (pas les sauts en cours de saison), du plafond, de l'avidité et de l'humeur de l'agent ; un joueur n'accepte **pas plus de −3 % par année de contrat** (−12 % à 4 saisons) ; prolonger tôt coûte plus cher (plafond en hausse). [hnadmin 2023-09-18, 2024-01-14 ; d0ghouse 2026-04-22 ; V-A-9]
- **Agents libres** : seules les 3 meilleures offres comptent (cotes pondérées au dollar) ; décision 1-48 h après la 1re offre ; offres déposées jusqu'à la date limite traitées à la mise à jour **suivante** ; sous le plafond, 5 offres possibles quel que soit le montant. Offre minimale = **90 % de la demande** (3,51 M → 3,159 M) ; demande calculée sur le niveau actuel ; ne pas offrir un chiffre rond (égalité d'offres, avis). [hnadmin 2023-12-21, 2025-07-10 ; d0ghouse 2025-07-06 ; diamond_ace 2026-07-14 ; V-A-10, C-12]
- **Fin de contrat** : équipe active → la plupart partent en agence libre, seuls ceux sans saison complète ni 15 matchs de carrière (12 gardiens) prennent leur retraite ; équipe inactive → seuls les joueurs de sélection avec saison complète ; un prospect drafté par un bot n'est jamais éligible ; retraite en FA après 3 saisons. Sources des FA : équipes humaines inactives ou en faillite avec ≥ 50 matchs ; les équipes CPU ne libèrent personne. [hnadmin 2025-01-02, 2026-04-20 ; d0ghouse 2024-12-01 ; gordie_79 2022-02-28 ; V-A-11, B-4]
- **Farm / ELC** : Farm signable à 21 ans, effet à 22 ; pas d'ELC la même saison qu'un Farm ; ELC seul contrat multi-voies : 3 ans (18-21), 2 ans (22-23), 1 an (24), prix = 50 % de la demande à la note du début de la saison de signature ; rétrogradation limitée aux ELC (pas aux FA), salaire en pause, repos 3 jours, effet à la mise à jour suivante. [hnadmin 2025-03-08 à 2025-06-13 ; V-A-12, B-4]
- **Humeur de l'agent** : libellés qui varient (happy → neutral → unhappy/angry) ; neutral = 50 % de chances de +3-5 % de frais, unhappy/angry = +3-5 % à chaque offre ; remise à happy après un échange. [hnadmin 2023-10-06 ; d0ghouse 2023-01-28, 2024-03-26 ; V-A-24]
- **Hypothèses (avis)** : un joueur laissé partir puis repris en FA redemande beaucoup plus (gardien 59 : 780 k$ → 1 820 000 $) — prix de 2023, à retester [talonflame1 2023-07-17 ; V-B-4] ; **un agent libre signé est intransférable pendant la saison** (rjs_lu_ridware_rangers 2023-05-14 ; heymelo27 2026-04-14), à confirmer avant tout plan « signer puis échanger » [V-C-3] ; un joueur FRM qui atteint 70 OVR lance lui-même ses négociations (roadiculous 2026-02-15 ; jakkysosa 2026-06-21) [V-C-5].
- **Agents S27** : traits (rapide/paresseux, stable/lunatique, généreux/avide) et capacités (*Remove One Year*, *Bridge & Anchor Deal*, *Make Peace*, *Money Saver*). ⚠️ Deux joueurs disent que les « favors » servent déjà, hnadmin annonce leur activation en S28 : tester sur un joueur avant de compter dessus. [jakkysosa 2026-10-25 ; seany148, .coleh 2026-10-27 ; V-C-4]

### `.claude/skills/hockeynation-draft-scouting/SKILL.md` — 1 lignes ajoutées, 1 sur le sujet
description: Hockey Nation, draft et scouting : classes de 100, 10 choix, pré-instructions, Import Draft, scouts (8 max, budget 300 000 $), rapports. Pour préparer une draft ou organiser le scouting.

### `.claude/skills/hockeynation-joueurs/SKILL.md` — 14 lignes ajoutées, 13 sur le sujet
description: Hockey Nation, joueurs : équipes et contrôle du GM, compétences 0-10, plafonds, talents fort/faible, double poste, expérience, âge, déclin, retraite. Pour évaluer un joueur, une ligne ou un échange.
Ce fichier est un index : le contenu est dans `references/`. Lis seulement la section utile à la question ; chaque fichier reprend telle quelle une section de l'ancien SKILL.md (contenu inchangé).
| Fichier | Section |
|---|---|
| `references/00-introduction.md` | Introduction et sources |
| `references/01-les-4-equipes.md` | Les 4 équipes [G:Teams] |
| `references/02-competences.md` | Compétences [G:Players] |
| `references/03-talents-la-lecture-prioritaire.md` | Talents : la lecture prioritaire [U, 2026-10-23] |
| `references/04-competences-speciales.md` | Compétences spéciales [G:Players] |
| `references/05-attributs-caches-experience-capitaine.md` | Attributs cachés, expérience, capitaine |
| `references/06-age.md` | Âge [G:Players, Training] |
| `references/07-mises-a-jour-v-20261029-6-7.md` | [Veille 2026-10-29] Mises à jour (V-20261029-6, -7) |
| `references/08-ovr-speciales-declin-experience-potentie.md` | [Veille intégrale 2026-10-29] OVR, spéciales, déclin, expérience, potentiel (V-A-1 à A-4, A-22, A-23, A-25, V-B-1, B-6, V-C-6 à C-8) |

### `.claude/skills/hockeynation-joueurs/references/00-introduction.md` — 3 lignes ajoutées, 2 sur le sujet
## Introduction et sources
Sources : **[G:Rubrique]** = guide officiel (mis à jour le 30/09/2026, lu le 2026-10-23, `bronze.raw_pages` page_type `guide`). **[U]** = règle de l'utilisateur. **[H]** = hypothèse à confirmer.

### `.claude/skills/hockeynation-joueurs/references/01-les-4-equipes.md` — 9 lignes ajoutées, 8 sur le sujet
## Les 4 équipes [G:Teams]
| Équipe | Âges | Ce que le GM contrôle |
|---|---|---|
| PRO | tous | tout : coachs, échanges, contrats PRO, rachats, rétrogradations, entraînement, lignes A/B/C et plan de jeu |
| FRM (Farm, depuis 04/2025) | 22+ en pratique | coachs, entraînement complet, contrats ; lignes automatiques ; 30 joueurs et 30 contrats Farm au maximum |
| U21 | 18-21 | draft (5 choix), échanges, contrats ELC ou Farm, libération ; **pas d'entraînement réglable**, lignes automatiques |
| U17 | 15-17 | rien de plus que les coachs ; 7 jeunes de 15 ans par saison, 5 draftables, 2 non draftables (NDE, dont 1 via l'Import Draft) |
Lignes FRM, U21, U17 : construites sur le **poste principal** d'abord ; le 2e poste ne sert que pour combler. « Swap position » échange poste principal et secondaire à tout moment (PRO, FRM, U21) [G:Lineups].

### `.claude/skills/hockeynation-joueurs/references/02-competences.md` — 6 lignes ajoutées, 5 sur le sujet
## Compétences [G:Players]
- Patineurs, 0 à 10 : SKA patinage, END endurance, PWR puissance, SHO tir, PAS passe (principale source d'occasions), DEF défense (« crucial » pour empêcher les occasions), CHK mise en échec (récupérer le palet), DSC discipline, FOF mises au jeu (attaquants seulement).
- Gardiens : REF réflexes, END (nombre de matchs avant fatigue), POS placement, PAD jambières, BLO bloqueur, GLO mitaine, STK canne (arrêt le moins fréquent).
- Seul un **niveau entier** compte en match ; les points partiels ne servent à rien [G:Training].
- Plafond (maxing) propre à chaque compétence, entre 4 et 10 (3 à 5 pour les amateurs). `max: true` = plafond atteint ; le joueur entraîne alors une compétence au hasard [G:Training].

### `.claude/skills/hockeynation-joueurs/references/03-talents-la-lecture-prioritaire.md` — 7 lignes ajoutées, 6 sur le sujet
## Talents : la lecture prioritaire [U, 2026-10-23]
- Talents = les **2 compétences au plus fort potentiel** et **la plus faible** [G:Scouting].
- Compétences clés par poste [H, tiré des définitions] : C = SHO, PAS, SKA, FOF ; LW/RW = SHO, PAS, SKA ; LD/RD = DEF, CHK, SKA ; G = REF, POS, PAD, BLO, GLO (`gold.hn_position_keys`).
- Verdict (`gold.hn_player_fit`, `gold.hn_draft_board`) : **idéal** = 2 talents forts clés et talent faible hors clés ; **correct** = 1 talent fort clé ; **contre-emploi** = aucun. Exemple de l'utilisateur : un ailier aux talents DEF + CHK ne nous intéresse pas.
- Double poste : vérifier les deux postes ; Blednov (RW/C, talents DEF + FOF) est « correct » au centre et « contre-emploi » à l'aile (2026-10-23).
- Mauvais poste en ligne = **−20 %** sur les compétences [G:Lineups].

### `.claude/skills/hockeynation-joueurs/references/04-competences-speciales.md` — 3 lignes ajoutées, 2 sur le sujet
## Compétences spéciales [G:Players]
0 à 3 par joueur. Les plus utiles à suivre : Inspire, Tactician, Team Player (effets collectifs), Powerplay Specialist, Penalty Killer, Second Wind, Brick Wall (gardien), Goalie Tandem (2 gardiens). Late Bloomer : débloquée à 25 ans.

### `.claude/skills/hockeynation-joueurs/references/05-attributs-caches-experience-capitaine.md` — 5 lignes ajoutées, 4 sur le sujet
## Attributs cachés, expérience, capitaine
- Work Ethic (effort à l'entraînement, varie chaque jour) et Leadership (capitanat) [G:Players].
- Expérience 0 (None) à 10 (Elite), gagnée en match officiel : 100 % en PRO, 75 % FRM, 50 % U21, 25 % U17 ; pas en amical. Ex. None → Awful = 25 matchs PRO, 34 FRM, 50 U21, 100 U17 [G:Competitions].
- Capitaine choisi sur expérience + leadership ; « Veteran Leadership » aide à gagner les duels : à ne pas sous-estimer dans une équipe jeune [G:Lineups].

### `.claude/skills/hockeynation-joueurs/references/06-age.md` — 6 lignes ajoutées, 5 sur le sujet
## Âge [G:Players, Training]
- Entraînement un peu moins efficace avec l'âge, effet maximal dès 25 ans.
- Déclin possible dès 32 ans sur les compétences plafonnées (sauf DSC), maximal vers 35-39 ; les coachs n'y changent rien.
- Retraite annoncée dès 35 ans (jour 1), effective en fin de saison ; pic de probabilité à 39.
- Recrue (rookie) : 23 ans ou moins et 10 matchs PRO au plus.

### `.claude/skills/hockeynation-joueurs/references/07-mises-a-jour-v-20261029-6-7.md` — 4 lignes ajoutées, 3 sur le sujet
## [Veille 2026-10-29] Mises à jour (V-20261029-6, -7)
- **Compétences clés par poste — hypothèse [H] complétée, avis de joueur** : SHO et PAS = buts ; SKA et PWR = possession du palet ; CHK et DEF = défense ; DSC = pénalités prises ; FOF : un bon joueur de mise au jeu par ligne suffit, pas forcément le centre. PWR serait donc à ajouter à SKA pour C/LW/RW/D, à tester sur les lignes avant de modifier `gold.hn_position_keys` (rendu tactique figé). [Discord #general, talonflame1, 2026-04-04 ; V-6]
- **Gardiens** : END = nombre de matchs avant fatigue, titulaire 7+ ; STK est la compétence la moins utilisée ; un gardien à END bas arrive à ~60 % de condition en 3e période (avis talonflame1, 2026-04-04). La perte de condition pèse relativement plus sur les hautes compétences (d0ghouse, 2025-12-03). [V-7]

### `.claude/skills/hockeynation-joueurs/references/08-ovr-speciales-declin-experience-potentie.md` — 9 lignes ajoutées, 9 sur le sujet
## [Veille intégrale 2026-10-29] OVR, spéciales, déclin, expérience, potentiel (V-A-1 à A-4, A-22, A-23, A-25, V-B-1, B-6, V-C-6 à C-8)
- **OVR joueur (hnadmin 2022-09-28)** : moyenne des compétences où chaque niveau au-dessus de la moyenne compte deux fois ; décimales gardées, arrondi à la fin ; l'expérience n'est pas comptée. Exemple : 4 compétences à 4 et 4 à 8 → somme 48, excédent 8 → (48 + 8) / 8 = 7 → OVR 70. La formule « (somme + excédents) / n » est une déduction de l'exemple : vérifier sur un joueur de l'effectif avant de modifier `gold.hn_potential`. [V-A-1]
- **Spéciales (règles chiffrées)** : *Equalizer* annule une spéciale adverse au hasard (deux Equalizers = les deux spéciales d'un joueur) ; ordre : Equalizers, puis Telepathy, puis les autres ; *Telepathy* copie une spéciale que le joueur n'a pas (jamais Equalizer ni une annulée) ; *Team Player* +2 par joueur quand 5 jouent ensemble (+10) ; *Inspire* : un seul bonus actif à la fois par joueur ; *Patriot* : +1 à une compétence au hasard d'un compatriote, une fois par match, ne se cumule pas ; *Mr Game Five* +1 à toutes les compétences, *Playoff Beard* +1 à deux ; cumul : gardiens +9, défenseurs +10, attaquants +11 ; *Agitator* : −1 DSC au mieux noté adverse (jamais sous 0) ; *Goalie Tandem* : l'autre gardien reçoit +2 sur la meilleure compétence du premier (hasard entre ex æquo, tirée au début du match) ; les deux gardiens doivent l'avoir (avis avakael 2026-04-16). Questions sans réponse : +1 Patriot sur une compétence à 10 ? Patriot d'un gardien remplaçant ? [hnadmin / d0ghouse 2022-2025 ; V-A-2, B-6, C-8]
- **Déclin** : seules les compétences **plafonnées** déclinent ; DSC ne décline jamais ; chaque jour une compétence est tirée au hasard et, si elle est en déclin, ajoute des points de déclin (1 en déclin sur 8 = 12,5 % par jour) ; dépend de l'âge (max à 35 ans) et du poste (attaquants > défenseurs > gardiens) ; l'entraînement accumulé n'y change rien. [hnadmin 2023-04-20, 2023-11-10 ; V-A-3]
- **Expérience** : gagnée selon le niveau de la compétition (PRO 100 %, FRM 75 %, U21 50 %, U17 25 %), pas selon le temps de glace ; gardien : titulaire remplacé 100 %, remplaçant qui entre 100 %, remplaçant qui ne joue pas 25 %. **Capitaine** : leadership caché **fixe** + expérience ; un joueur nommé A ou C avec des coéquipiers plus expérimentés révèle un fort leadership ; seuls les 3 titulaires du capitanat en profitent. [d0ghouse 2022-09-06, 2023-08-15, 2025-08-16 ; hnadmin 2025-02-17 ; segi_3554 2024-08-16 ; V-A-4, B-1, B-6]
- **Potentiel** : minimum et maximum se déduisent des talents (2 plus forts, 1 plus faible) ; compétences plafonnées visibles (pucs rouges) ; plancher 4 (3 pour les amateurs, plafond 3-5) ; aucun rapport de scout n'indique le potentiel. [hnadmin 2022-04-11, 2024-03-24 ; d0ghouse 2022-07-30, 2025-07-08 ; V-A-25]
- **Rating d'équipe (avis, rétro-ingénierie de valyxn 2026-05-09, non confirmée)** : OFF = SHO + PAS ; DEF = DEF + CHK ; PHY = SKA + END + PWR ; DSC et FOF ne comptent pas — complète l'hypothèse [H] de `gold.hn_position_keys` (PWR et END). [V-C-6]
- **Blessures — hypothèse** : aucune n'est implémentée à notre connaissance ; proposées en 2023 (9 par saison, 25 % majeures), rejetées par un vote de la communauté (2023-07 → 2024-04), hnadmin a dit qu'elles pouvaient être annulées ; ne bâtir aucun plan dessus. [.coleh 2023-07-04 ; hnadmin 2023-03-24, 2023-04-17 ; fishyicee 2026-02-19 ; V-A-23, B-1, C-7]
- **Comptes inactifs** : non connecté depuis 28 jours = marqué à supprimer (suppression au changement de saison) ; Mode vacances +28 jours ; leurs choix de draft et joueurs suivent les règles des bots. [hnadmin 2026-02-10, 2026-07-21 ; V-A-22]

### `.claude/skills/hockeynation-match-calendrier/SKILL.md` — 11 lignes ajoutées, 11 sur le sujet
description: Hockey Nation, matchs et saison : ligues, 30 matchs, playoffs, lignes A/B/C, pénalités, fatigue des gardiens, amicaux, calendrier de 63 jours. Pour composer les lignes, analyser un match ou dater une action.
Ce fichier est un index : le contenu est dans `references/`. Lis seulement la section utile à la question ; chaque fichier reprend telle quelle une section de l'ancien SKILL.md (contenu inchangé).
| Fichier | Section |
| `references/00-introduction.md` | Introduction et sources |
| `references/01-competitions.md` | Compétitions |
| `references/02-lignes-pro.md` | Lignes (PRO) |
| `references/03-calendrier-63-jours-gold-hn-calendar.md` | Calendrier (63 jours) — `gold.hn_calendar` |
| `references/04-echanges.md` | Échanges [G:Trades] |
| `references/05-vues.md` | Vues |
| `references/06-mises-a-jour-v-20261029-8-9.md` | [Veille 2026-10-29] Mises à jour (V-20261029-8, -9) |
| `references/07-condition-plan-de-jeu-plafond-amicaux-v.md` | [Veille intégrale 2026-10-29] Condition, plan de jeu, plafond, amicaux (V-A-5 à A-7, A-21, V-B-3, V-C-13) |

### `.claude/skills/hockeynation-match-calendrier/references/00-introduction.md` — 3 lignes ajoutées, 2 sur le sujet
## Introduction et sources
Sources : **[G:Competitions]**, **[G:Lineups]**, **[G:Trades]**, **[G:Calendar]** (guide du 30/09/2026, lu le 2026-10-23).

### `.claude/skills/hockeynation-match-calendrier/references/01-competitions.md` — 6 lignes ajoutées, 5 sur le sujet
## Compétitions
- 15 ligues : 1 (niveau 1), 2, 4, 8 ; 20 équipes en 2 conférences (Est, Ouest).
- 30 matchs en 35 jours : 18 dans la conférence, 10 contre l'autre conférence, 2 contre le **rival** (1er et dernier match). Top 4 de chaque conférence en playoffs, séries au meilleur des 5.
- Les 2 finalistes montent, les 2 derniers de chaque conférence descendent.
- Amicaux : jours 1-7 et 43-63, un par jour ; FRM, U21, U17 seulement pour les comptes premium ; pas d'expérience gagnée.

### `.claude/skills/hockeynation-match-calendrier/references/02-lignes-pro.md` — 10 lignes ajoutées, 9 sur le sujet
## Lignes (PRO)
- 3 lignes A, B, C (A par défaut) ; modifiables jusqu'à 1 h avant le match. Lignes invalides corrigées automatiquement (amateurs si besoin).
- Pénalités (cumul plafonné à 30 %) : **mauvais poste −20 %** ; gardien fatigué −20 % ; chaque amateur −5 % pour toute l'équipe ; dépassement des dépenses −30 % (hors amicaux).
- Condition : 100 % au départ, baisse à chaque présence selon END ; une condition de 80 % = compétences à 80 %. Une grosse mise en échec retire 1 à 3 % non récupérables.
- Gardien : perd de la condition à chaque tir ; **fatigué** après autant de matchs d'affilée que son END (saison régulière seulement) : il ne peut pas débuter le suivant. Remplacé automatiquement si fatigué, ou mené de 3 buts en 1re période, 4 en 2e, 5 en 3e, ou 3 buts encaissés à moins de 60 % d'arrêts (jamais dans les 5 dernières minutes).
- Mises au jeu : les 2 attaquants avec le meilleur FOF, surtout le meilleur.
- Capitaine et assistants : expérience + leadership caché ; le leadership des vétérans aide à gagner les duels.
- Bagarres : les moins disciplinés ; issue selon PWR et expérience ; une victoire donne un bonus temporaire ; plus fréquentes contre le rival.
- Tirs au but : les meilleurs tireurs, le meilleur en premier.

### `.claude/skills/hockeynation-match-calendrier/references/03-calendrier-63-jours-gold-hn-calendar.md` — 17 lignes ajoutées, 16 sur le sujet
## Calendrier (63 jours) — `gold.hn_calendar`
| Jour | Événement |
|---|---|
| 1 | âge +1, draftés en U21, fenêtre I et agents libres ouverts, plafond annoncé en hausse ou baisse |
| 3 | Frenzy des agents libres, 1res réponses des coachs |
| 4 | début du scouting |
| 8 | 1re journée, 1re paie |
| 10, 20, 30 | demandes des agents libres révisées |
| 28 | fourchette du plafond suivant |
| 35 | **fermeture fenêtre I et agents libres (21:00 CET)** : effectifs gelés, fin des embauches de coachs et des activations de contrat |
| 42 / 43 | dernière journée, dernière paie / fin de saison régulière |
| 44 | playoffs |
| 49 | Import Draft |
| 51 → 61 | fenêtre II (21:00 CET) ; un joueur reçu en fenêtre I ne peut pas y être échangé |
| 57 | plafond officiel de la saison suivante |
| 63 | Youth Draft (pré-instructions 1 h avant) |

### `.claude/skills/hockeynation-match-calendrier/references/04-echanges.md` — 5 lignes ajoutées, 4 sur le sujet
## Échanges [G:Trades]
- PRO, U21 et choix de draft échangeables, après les avoir marqués disponibles ; un agent libre signé ne s'échange pas dans sa 1re saison.
- Chaque échange accepté passe devant un comité de 21 votants (24 h, décision finale) ; traité à la 2e mise à jour quotidienne ; échanges de choix seuls traités tout de suite.
- Équipe au-dessus du plafond : aucun échange qui augmente sa masse salariale.

### `.claude/skills/hockeynation-match-calendrier/references/05-vues.md` — 3 lignes ajoutées, 2 sur le sujet
## Vues
`silver.hn_lineups`, `silver.hn_games`, `silver.hn_game_detail`, `silver.hn_standings`, `silver.hn_trades`, `silver.hn_market_players`, `gold.hn_calendar`, `gold.hn_daily_alerts`.

### `.claude/skills/hockeynation-match-calendrier/references/06-mises-a-jour-v-20261029-8-9.md` — 4 lignes ajoutées, 3 sur le sujet
## [Veille 2026-10-29] Mises à jour (V-20261029-8, -9)
- **Lignes** : une modification est prise en compte tout de suite, mais **au moins 1 h avant le match**, sinon risque de −30 % aux compétences (hnadmin, 2025-07-10). **Amical** : la pénalité de mauvais poste s'applique, seule la pénalité de plafond est désactivée, et le mauvais poste ne touche que le joueur concerné (d0ghouse, 2026-10-28 11:06/12:59). Les amicaux ne donnent pas d'expérience (krusher_kev, 2026-10-05, avis). [Discord #general ; V-8]
- **Capitaine** : leadership + expérience, limité à 3 joueurs (C + 2 A), plus d'expérience est mieux (d0ghouse, 2026-08-24 19:32). Le temps de glace maximal des défenseurs a été réduit dans une version passée (date non précisée) ; « tout joueur peut jouer 25-30 min quel que soit END » (d0ghouse, 2026-05-11 20:27, portée à vérifier). [Discord #general ; V-9]

### `.claude/skills/hockeynation-match-calendrier/references/07-condition-plan-de-jeu-plafond-amicaux-v.md` — 8 lignes ajoutées, 8 sur le sujet
## [Veille intégrale 2026-10-29] Condition, plan de jeu, plafond, amicaux (V-A-5 à A-7, A-21, V-B-3, V-C-13)
- **Condition** : mise à jour après chaque présence pour un patineur, toutes les 30 s pour un gardien ; une grosse mise en échec subie ne se récupère pas à l'entracte ; END bas = plus de condition perdue (≈ 60 % à la fin des 20 min). **Gardiens** : chaque match joué, même partiel, réduit le compteur de fatigue de 1 ; remplaçant qui joue = un repos mais fatigue un match plus tôt ; END 0 ou 1 = un seul match ; reposés et sans fatigue en playoffs. [hnadmin 2022-02-21, 2025-04-30 ; d0ghouse 2022-07-31, 2023-11-21, 2025-11-10 ; V-A-5]
- **Temps de glace des défenseurs** : réduit (≈ 2 min pour la 1re paire au patch du 2024-09-09, réduit avant le 2024-05-13) et perte de condition augmentée ; hnadmin 2026-10-28 : le facteur décroissant est « peut-être trop agressif », il va le retoucher — suivre le prochain patch. [V-A-5, B-3]
- **Plan de jeu** : une instruction vaut pour l'unité sur la glace (ex. L2 + paire 3) ; « Against » cible une ligne adverse ; en cas de conflit **la dernière instruction de la liste gagne** ; « Def Pair 1 » sans précision = toutes les combinaisons. Aucun effet chiffré des réglages n'a été donné. [hnadmin 2025-06-16 ; d0ghouse 2022-08-16, 2023-04-01 ; V-A-6]
- **Plafond et match** : les matchs sont simulés 1 h avant avec les lignes de cet instant (postes vides remplis par des joueurs hors lignes) ; amicaux sans pénalité de plafond depuis S9 (en 2023 elle s'appliquait aux amicaux de pré-saison) ; coût journalier d'un échange = différence des salaires totaux / 35 jours de paie. Amateurs : −5 % de toutes les compétences par amateur (guide cité 2024-10-01). [d0ghouse 2025-09-03, 2026-10-28 ; hnadmin 2023-08-23 ; V-A-7, B-3]
- **UA Cup** : équipe copiée (autres ID) ; les lignes A, B, C sont copiées à la fermeture des inscriptions (jour 36), A par défaut ; tout changement du PRO après le jour 36 n'est pas repris. [hnadmin 2025-09-25, 2026-03-31 ; V-A-21]
- **Amicaux de pré-saison S23 (avis jakkysosa 2026-02-15)** : PRO jours 1 et 7, FRM jours 2, 4, 5, 6, 7, U21 jours 1, 3, 4, 5, 7 ; à comparer à `gold.hn_calendar` S27. Non tranché : rétrograder dans l'heure avant un match pour redevenir positif ; moment exact de la libération de plafond après rétrogradation. [V-C-13]
- **Stats** : des buts attendus (xG) existent (stillnoah75 2026-03-02), à chercher dans `silver.hn_game_detail`. [V-C-7]

### `.claude/skills/hockeynation-potentiel-joueurs/SKILL.md` — 1 lignes ajoutées, 1 sur le sujet
description: Hockey Nation : calculer le potentiel d'un joueur (note min et max) depuis ses compétences plafonnées et ses talents, puis le classer. Pour juger un trade, un prospect, un U21 ou un choix de draft.

### `docs/attentes/jeux/hockeynation.yaml` — 11 lignes ajoutées, 10 sur le sujet
core:   # refonte v2 phase 1 : entités branchées (adapt.hockeynation_<entité>) ; limites = colonnes nulles par construction
player_daily:  { limites: [form, fatigue, morale, injured, suspended, contract_end, market_value] }   # pas de forme ; condition en match seulement ; blessures non implémentées (hypothèse) ; fin de contrat en saison (extras)
fixture:       { limites: [round_no] }                                     # numéro de journée non exporté (extras.season_day)
standing:      { limites: [draws] }                                        # règle des points et prolongations non sourcée (extras.ot)
finance_daily: { limites: [balance, income, expenses, capacite_invest] }   # économie au plafond salarial, pas de trésorerie
market_listing: { limites: [ends_at, price, starting_price, bids, seller_id] }  # agents libres (salaire) et trade block : ni enchère ni prix
academy_prospect: { limites: [potential_min, potential_max] }              # classe de draft de ma ligue ; potentiel calculé par le skill, pas affiché
staff:         { limites: [] }                                             # coachs (note, pas de salaire) + scouts (salaire par jour, pas de note)
training_plan: { limites: [focus_secondary, intensity] }                   # une compétence par jour ; pas d'intensité
season:        { limites: [] }                                             # jour 1 = fermeture de la fenêtre I − 34 jours [G:Calendar], comme gold.hn_today

### `outputs/hockeynation/learnings.md` — 13 lignes ajoutées, 5 sur le sujet
| L-018 | 2026-11-04 | Kovalev P3 .900 (45/50) sur J8-J11 contre .868 en S26 : le recul de L-016 tient sur J8 seul. Kovalev a démarré les 4 matchs d'affilée (END 4) : fatigue attendue pour J12. | 4 | à surveiller (L-016 affaibli) | `silver.hn_game_detail` (periods, boxscore) ; `hockeynation-match-calendrier` (02-lignes-pro) |
| C-016 | 2026-10-23 | Ne pas faire le Swap Blednov RW→C (inutile en PRO) ; garder Kovalev SG / Lauper BG sans réglage (rotation automatique) | `select main_position from silver.hn_players where name='Slava Blednov'` = RW ; en S27 Lauper démarre 1 match après 4 départs d'affilée de Kovalev (S26 observé : Lauper démarre après 3 ou 4 départs, jours 11, 16, 22, 28, 32, 38) | remplacé par C-062 (pour J12) | — |
| C-059 | 2026-11-02 | Avant Deadwood (03/11 00:45) : PP1 LW Hakkarainen (valeur 24) à la place de Bélanger (19), Bélanger en PP2 LW ; reste de la lineup et plan de jeu inchangés | `select line, slot, joueur from gold.hn_saisie_lignes where lineup='A' and line in ('PP1','PP2') and slot='LW'` ; échec si PP < 20 % ET < 1 tir par minute de PP sur 5 matchs de ligue (J8 : 1/3, 4 tirs en 251 s ; S26 20,7 %) | **non appliqué (2026-11-04)** : `gold.hn_saisie_lignes` PP1 LW = Bélanger, PP2 LW = Hakkarainen | motif affaibli : PP 5/21 (23,8 %) sur J8-J11 ; reste ouvert, pas repoussé |
| C-060 | 2026-11-02 | Kovalev démarre contre Deadwood (pas de changement de gardien) ; seuil : save % en P3 | `periods` + `boxscore` de `silver.hn_game_detail` : P3 de Kovalev >= .880 sur 5 matchs de ligue (S26 .868, J8 .714) ; sinon C-061 prioritaire | appliqué (Kovalev SG J8-J11) | trop tôt : P3 .900 (45/50) sur 4 matchs ; J12 sera Lauper (C-062) |
| C-062 | 2026-11-04 | Gardiens de la lineup A pour J12 Oudega (05/11 17:00 Paris) : SG Lauper, BG Kovalev (Kovalev a démarré J8 à J11, END 4 = fatigué) ; remplace C-016 pour ce match | `select joueur, slot from gold.hn_saisie_lignes where lineup='A' and line='G'` : SG = Lauper ; `silver.hn_game_detail` J12 : Lauper toi > 0 et arrêts >= .871 (S26, 5 matchs complets) | ouvert | — |

## Nouveau — Discord / chat
- rien de nouveau.

## Du jour
- brief : `outputs/hockeynation/briefs/2026-11-04-match.md`
- registre `fait-` : absent
- exports : `bronze.raw_pages` where game = 'hockeynation' and captured_at >= '2026-11-04'

## Couverture (à remplir)
| Source | trouvés | lus | retenus | écartés (pourquoi) |
|---|---|---|---|---|
| carte (variables) | | | | |
| nouveau règles | | | | |
| nouveau Discord/chat | | | | |
