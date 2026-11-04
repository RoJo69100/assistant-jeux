# Dossier hardwood — composition — 2026-11-04 — carte + nouveau

1. **Carte** `docs/decisions/cartes/hardwood/composition.md` : lis-la en entier. Chaque variable y a son endroit et son check : lance ses requêtes (groupées, colonnes choisies, `LIMIT`) et remplis les valeurs du jour. Ne relis pas les sources déjà notées.
2. **Nouveau depuis le commit d0cfdca** (ci-dessous) : à lire en entier. Une ligne qui change une règle, un avis ou un seuil → modifie le check de la carte (cite la source et la date) ; une variable nouvelle → ajoute une ligne.
3. **Joueur ou réglage absent de la carte** : recherche ciblée sur son nom dans tout l'historique (`--mots`, fichier `-cible.txt`).
4. **Fin** : carte à jour (valeurs, checks, sources), commit, puis `python pipelines/dossier.py hardwood composition --marquer`.

## 0. Cœur commun `docs/decisions/cartes/_core/composition.md` (valeurs calculées le 2026-11-04)

| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| C1 | Prochain match | `select day, competition_kind, round_no, opponent, home, scheduled_at at time zone 'Europe/Paris' as coup_envoi_paris from core.fixture where game = 'hardwood' and not played and day >= current_date order by day, scheduled_at nulls last limit 5` | Match d'aujourd'hui ou de demain : se prépare aujourd'hui | CLAUDE.md, inviolable 3 | aucune ligne |
| C2 | Joueurs du dernier relevé | `select position, name, age, rating, form, fatigue, injured, suspended, day from core.player_daily where game = 'hardwood' and day = (select max(day) from core.player_daily where game = 'hardwood') order by position, rating desc limit 40` | Forme et fatigue en échelle 0–1 (échelle du jeu : `core.game_params` echelle_*) | `docs/attentes/jeux/<jeu>.yaml` core | position=C, name=Fred Howell, age=19, rating=37.9, form=, fatigue=, injured=False, suspended=False, day=2026-11-04 ; position=C, name=Dale Wallace, age=20, rating=37.5, form=, fatigue=, injured=False, suspended=False, day=2026-11-04 ; position=C, name=Larry Chance, age=19, rating=32.9, form=, fatigue=, injured=False, suspended=False, day=2026-11-04 ; position=C, name=Darnel McCleary, age=19, rating=28.9, form=, fatigue=, injured=False, suspended=False, day=2026-11-04 ; position=PF, name=Dustin Barbieri, age=22, rating=45.7, form=, fatigue=, injured=False, suspended=False, day=2026-11-04 ; … |
| C3 | Alertes joueurs | `select prio, domaine, alerte from gold.daily_alerts where game = 'hardwood' and domaine in ('blessure', 'fatigue', 'forme', 'tactique', 'effectif') order by prio limit 15` | Blessé ou hors zone : jamais titulaire sans raison écrite | `core.alert_rule` | ⚠ erreur : canceling statement due to statement timeout |
| C4 | Classement | `select rank, team_label, played, points, wins, losses, gf, ga, is_mine from core.standing where game = 'hardwood' and day = (select max(day) from core.standing where game = 'hardwood') order by rank limit 20` | Force de l'adversaire lue au classement et à ses résultats | `docs/decisions/variables.md` § composition | ⚠ erreur : canceling statement due to statement timeout |
| C5 | Bilan de la saison | `select competition_kind, my_result, count(*) as n, round(avg(my_score), 1) as pour, round(avg(opp_score), 1) as contre from core.fixture where game = 'hardwood' and my_result is not null group by 1, 2 order by 1, 2 limit 12` | Ce qui a marché / échoué : voir learnings du jeu | `outputs/<jeu>/learnings.md` | aucune ligne |
| C6 | Agenda du jour | `select at_time, priority, category, action from gold.agenda where game = 'hardwood' and day = current_date order by at_time limit 10` | Heure limite du réglage | `core.agenda_rule` | aucune ligne |
| C7 | Exports à refaire | `select ecran, statut, age_h from gold.exports_state where game = 'hardwood' and statut <> '🟩 à jour' order by ordre limit 15` | Effectif ou tactique périmé : « exporte » avant la saisie | `core.export_rule` | ecran=Statistics, statut=🟧 à refaire, age_h=126 ; ecran=Recruiting, statut=🟧 à refaire, age_h=55 ; ecran=Prospect Search (région), statut=🟧 à refaire, age_h=121 ; ecran=Conference, statut=🟧 à refaire, age_h=85 ; ecran=Rankings, statut=🟧 à refaire, age_h=126 ; … |

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
### `.claude/skills/hardwood-aujourdhui/SKILL.md` — 1 lignes ajoutées, 1 sur le sujet
description: Hardwood — que faire aujourd'hui : plan du jour depuis l'agenda et les alertes. Pour tout « que faire », « reprenons » ou plan du soir.

### `.claude/skills/hardwood-recrutement/SKILL.md` — 15 lignes ajoutées, 15 sur le sujet
description: Recrutement Hardwood : types de recrues, points (2 par jour, plafond 45), offres, niveaux d'intérêt, engagements, facteurs, régions, phrases du scout. Pour choisir, contacter ou abandonner une recrue.
Ce fichier est un index : le contenu est dans `references/`. Lis seulement la section utile à la question ; chaque fichier reprend telle quelle une section de l'ancien SKILL.md (contenu inchangé).
| Fichier | Section |
| `references/00-introduction.md` | Introduction et sources |
| `references/01-types-de-recrues.md` | Types de recrues [R:Recruiting] |
| `references/02-points-et-contacts.md` | Points et contacts [R:Contacts, Recruiting Calendar] [D] |
| `references/03-offres-interet-engagement.md` | Offres, intérêt, engagement [R:Scholarship Offers, Commitments] |
| `references/04-facteurs-de-reussite.md` | Facteurs de réussite [R:Recruiting Success Factors] |
| `references/05-evaluation-du-scout.md` | Évaluation du scout [A] |
| `references/06-arrivee-des-recrues.md` | Arrivée des recrues [A] |
| `references/07-repartir-les-contacts.md` | Répartir les contacts [A] |
| `references/08-methode-des-bons-managers.md` | Méthode des bons managers [G] [D] |
| `references/09-tableau-pret.md` | Tableau prêt |
| `references/10-recrues-en-deux-temps-2026-10-30-sql-gol.md` | Recrues en deux temps (2026-10-30, `sql/gold/046_hw_recrue_fiches.sql`) |
| `references/11-inconnu.md` | Inconnu |

### `.claude/skills/hardwood-recrutement/references/00-introduction.md` — 3 lignes ajoutées, 2 sur le sujet
## Introduction et sources
Sources : **[R:Rubrique]** = manuel officiel (capturé le 2026-10-30). **[D]** = Discord, veille du 2026-10-30 (`outputs/hardwood/veille/v-recrutement.md`, statut entre parenthèses). **[G]** = guide d'un joueur (Google Doc fourni par l'utilisateur). **[A]** = document d'aide de l'utilisateur (`data/manual/hardwoord/Aide docs.txt`, 2026-10-30). **[E]** = nos exports.

### `.claude/skills/hardwood-recrutement/references/01-types-de-recrues.md` — 9 lignes ajoutées, 8 sur le sujet
## Types de recrues [R:Recruiting]
| Type | Recrutable | S'engage | Arrive comme |
|---|---|---|---|
| Lycée (HS FR → SR) | dès 14 ans | en SR (dès la **mise à jour 5**) | freshman, 4 ans d'éligibilité |
| JuCo (JC FR → SO) | dès 18 ans | en JC SO (plus tard que les lycéens) | junior, **2 ans** d'éligibilité |
| International | 1 seule saison, à 17 ans | dans l'année (plus tard) | freshman |
- À la mise à jour 53, un non-engagé signe chez une équipe qui lui a offert une bourse, part en JuCo, devient walk-on ou arrête.
- **Il n'y a pas de transferts** : tout le renouvellement passe par ici [D (confirmé Steve, 2021)].

### `.claude/skills/hardwood-recrutement/references/02-points-et-contacts.md` — 6 lignes ajoutées, 5 sur le sujet
## Points et contacts [R:Contacts, Recruiting Calendar] [D]
- Un gros versement au début de la saison (≈ 29 au flip), puis **2 points par mise à jour** : ≈ 130-135 par saison [G] [D (confirmé)].
- **Plafond : 45 points en réserve.** À la fin de la saison, les points au-delà de 10 sont **divisés par deux**.
- Aucune limite de dépense par jour ni par prospect. Sur les **jeunes classes (FR, SO, JR), un plafond souple** réduit l'effet des gros contacts.
- Coût observé pour atteindre « Low » : 2 à 7 contacts dans l'État ou la région, 10 à 15 en dehors ou à l'international. Medium coûte environ 4 fois plus, High environ 7 fois [D (en doute : un seul joueur, 2026-03)].

### `.claude/skills/hardwood-recrutement/references/03-offres-interet-engagement.md` — 6 lignes ajoutées, 5 sur le sujet
## Offres, intérêt, engagement [R:Scholarship Offers, Commitments]
- Pas d'engagement sans **offre de bourse**. Offrir ne coûte rien [D]. **Retirer une offre remet à zéro** le travail fait sur ce joueur ; impossible une fois qu'il est engagé.
- Notre intérêt est affiché finement : None, Low, Low+, Low++, Medium, Medium+, Medium++, High, High+, High++, Very High. **Celui des concurrents est arrondi** (un « Medium » peut valoir Medium++) : on ne sait jamais si on mène vraiment.
- L'engagement est **probabiliste** : le plus haut intérêt n'est pas une garantie, d'où l'utilité d'un plan B.
- Une fois les bourses de la saison suivante toutes attribuées, aucun autre engagement n'est possible.

### `.claude/skills/hardwood-recrutement/references/04-facteurs-de-reussite.md` — 6 lignes ajoutées, 5 sur le sujet
## Facteurs de réussite [R:Recruiting Success Factors]
- **Niveau de conférence** : en **Division 3, attirer des 4 et 5 étoiles est très difficile** ; en D2, les 5 étoiles.
- Prestige ; **durée du contact** (contacter tôt aide) ; note Recruiting du coach ; **géographie** (bonus dans l'État et la région) ; **temps de jeu offert** (un effectif plein de jeunes bien notés fait fuir) ; **redshirt de joueurs bien notés** (les élites fuient) ; une part de hasard.
- L'intérêt chute après une **descente de conférence** ou un **renvoi du head coach**.
- Notre région : **USA Central = Illinois, Indiana, Missouri, Ohio, West Virginia**. Eureka est dans l'Illinois [R:Recruiting Regions] [E].

### `.claude/skills/hardwood-recrutement/references/05-evaluation-du-scout.md` — 18 lignes ajoutées, 17 sur le sujet
## Évaluation du scout [A]
**[A]** = document d'aide fourni par l'utilisateur le 2026-10-30 (`data/manual/hardwoord/Aide docs.txt` : tableau épinglé sur Discord, conseils d'un ancien). Table en base : `silver.hw_ref_scout_phrases` (remplace `public.hardwood_ref_scouting_ranges`, fausse par endroits : « good shooter » 13-19, « sluggish » 0-6, « below average ball handler » 0-2).
| Compétence | Phrase → plafond probable |
|---|---|
| IS | dominating post 18-20 · very good post 15-18 · good post 13-17 · above average post moves 11-14 |
| OS | excellent shooter 15-20 · good shooter 13-16 · above average shooter 11-17 · « does not have much of a shooting touch » = bas (non chiffré) |
| Rng | really be a long-range shooter 10-20 |
| Reb | monster on the boards 15-20 · decent rebounder 13-16 · **never a good rebounder 0-8** |
| IQ | really smart 14-20 · smart 13-18 · **prone to mental mistakes 0-7** |
| Défense | great all-around defensive **IDef + PDef = 22-36** · good all-around 14-31 · never a good perimeter (ou interior) defender 0-10 |
| Pass | skilled passer with exceptional court vision 14-20 · skilled passer 12-16 |
| Hnd | really good ball handler 15-20 · decent 11-16 · below average 0-12 |
| Spd | quick as lightning 19-20 · very quick 15-18 · speedy 12-16 · **always a bit sluggish 0-9** |
- Autres phrases : « troubled kid » et « isn't much of a student » = environ 50/50 de perdre la recrue à la fin de son année HS SR (jamais en université / part en JuCo) ; « may choose to play overseas » = international, 50/50 ; « eager to commit early » = s'engage dans la 1re moitié de saison s'il a des contacts ; « would prefer to play close to home » = bonus de région ; « will flourish in a fast pace offense » = Pace positif.
- Plafond de SI selon le potentiel : `silver.hw_ref_potential_caps` (pot 9 → 126-139 … pot 17 → 238-251, soit 14 × pot à 14 × pot + 13) [A].
- L'évaluation ne change pas d'une année de lycée à l'autre ; une nouvelle évaluation arrive au passage en JuCo [G].
- Regarder la croissance de la taille d'année en année : un joueur qui grandit tard peut encore atteindre sa taille projetée [G].

### `.claude/skills/hardwood-recrutement/references/06-arrivee-des-recrues.md` — 5 lignes ajoutées, 4 sur le sujet
## Arrivée des recrues [A]
- **HS** : seul un lycéen **HS SR** s'engage ; il arrive **FR** (4 ans). Un HS JR ne s'engagera que dans 2 saisons.
- **JC** : un junior college s'engage en **JC SO** et arrive **JR** (2 ans d'éligibilité).
- Prendre **3 à 4 recrues par classe** (pas 2), dont **au moins un grand** (PF/C) ; garder des plans B, et chercher en fin de saison des « pépites » bon marché [A].

### `.claude/skills/hardwood-recrutement/references/07-repartir-les-contacts.md` — 7 lignes ajoutées, 6 sur le sujet
## Répartir les contacts [A]
- Plus de contacts sur les mieux notés (étoiles, SI) : les autres équipes les chassent fort.
- Dans la région, peu de contacts suffisent pour prendre la tête et la reprendre : pas besoin de grosse avance.
- Recrue pressée (« eager to commit early ») : il suffit d'être en tête au moment du sprint. Recrue qui attend : il faut une grosse avance, sinon les équipes qui ont perdu leurs cibles nous rattrapent.
- Concurrence : si seules des D3 sans propriétaire la suivent, dépenser ailleurs ; une D1 avec propriétaire est un vrai rival. En fin de saison, vérifier si les rivaux n'ont plus de bourses libres : ils ne peuvent plus la prendre.
- Les montées de conférence relèvent l'intérêt des HS FR-JR et JC FR après la saison, les descentes le baissent (effet de montée plus fort, petit échantillon).

### `.claude/skills/hardwood-recrutement/references/08-methode-des-bons-managers.md` — 7 lignes ajoutées, 6 sur le sujet
## Méthode des bons managers [G] [D]
- **Une cible principale à 45-60 points, plus deux secondaires pour 20 à 30 points au total.** Jamais 6 recrues à la fois avec 135 points.
- Rester dans l'État ou la région, éviter les duels High contre High. Repère [G] : dans l'État, une cible est jouable si 2 équipes au plus sont sur elle ; hors région, si aucune.
- **Garder environ 10 points au flip** (ils sont reportés entiers). Prendre de l'avance sur les JR et SO.
- Viser une recrue qui atteindra 110-115 de SI après redshirt ; sinon, elle ne servira pas longtemps [G].
- Rythme d'effectif conseillé : 2 à 4 recrues par classe, avec 2 ou 3 bourses qui se libèrent chaque saison.

### `.claude/skills/hardwood-recrutement/references/09-tableau-pret.md` — 3 lignes ajoutées, 2 sur le sujet
## Tableau prêt
`gold.hw_recruit_board` (prospects de la recherche + nos suivis) : verdict cible / cible hors région / secondaire / dur / futur / écarter, `rang` dans le verdict, `besoin` = poste d'un boursier qui part, plafond de SI, équipes intéressées et à High, notre intérêt et notre offre, bourses libres et points.

### `.claude/skills/hardwood-recrutement/references/10-recrues-en-deux-temps-2026-10-30-sql-gol.md` — 4 lignes ajoutées, 3 sur le sujet
## Recrues en deux temps (2026-10-30, `sql/gold/046_hw_recrue_fiches.sql`)
1. `gold.hw_recrues_a_ouvrir` : prospects engageables du board (cible, cible hors région, secondaire) sans page joueur en base. Donner **au moins 15 noms** à ouvrir : beaucoup sont rejetés une fois la page lue (demande de l'utilisateur).
2. `gold.hw_recrue_fiches` : une ligne par page ouverte. Note /5 au meilleur poste jouable (listé dans Positions, Grand ≥ 1,95 m), même barème que `gold.hw_roster_notes` : `note_now` (actuel) et `note_plafond` (potentiel + milieu des phrases du scout), `boursiers_devant` = nos boursiers qui restent et sont mieux notés, `cles_non_dites` = compétences clés sans phrase (plafond pris à l'actuel), `phrases_hors_ref` à ajouter à `silver.hw_ref_scout_phrases`. Verdict [H] : 🟥 offrir / 🟧 réserve / rejeter, risque 50/50 signalé.

### `.claude/skills/hardwood-recrutement/references/11-inconnu.md` — 2 lignes ajoutées, 2 sur le sujet
## Inconnu
Coût exact par classe (HS FR à JC), taille et durée du malus de redshirt, seuils des étoiles, heure de réouverture après le flip.

### `.claude/skills/hardwood-regles/SKILL.md` — 16 lignes ajoutées, 15 sur le sujet
description: Hardwood, règles : conférences, montée/descente, calendrier, effectif, compétences 0-20, potentiel, coaching, fatigue, blessures, redshirt, coachs, prestige. Pour une règle, un calendrier ou un joueur.
Ce fichier est un index : le contenu est dans `references/`. Lis seulement la section utile à la question ; chaque fichier reprend telle quelle une section de l'ancien SKILL.md (contenu inchangé).
| Fichier | Section |
|---|---|
| `references/00-introduction.md` | Introduction et sources |
| `references/01-structure.md` | Structure [R:Conference Structure, Conference, Tournaments] |
| `references/02-calendrier-d-une-saison.md` | Calendrier d'une saison [R:Games, Schedule] [D] |
| `references/03-effectif.md` | Effectif [R:Team Roster, Walk-Ons] |
| `references/04-joueurs.md` | Joueurs [R:Players] |
| `references/05-entrainement.md` | Entraînement [R:Player Development] |
| `references/06-fatigue-overwork-blessures.md` | Fatigue, Overwork, blessures [R:Fatigue, Overwork, Injuries] |
| `references/07-redshirt.md` | Redshirt [R:Red Shirting] |
| `references/08-coachs.md` | Coachs [R:Head Coaches, Assistant Coaches] |
| `references/09-classements.md` | Classements [R:Ratings] |
| `references/10-ce-qui-reste-inconnu.md` | Ce qui reste inconnu |

### `.claude/skills/hardwood-regles/references/00-introduction.md` — 3 lignes ajoutées, 2 sur le sujet
## Introduction et sources
Sources : **[R:Rubrique]** = manuel officiel `onlinecollegebasketball.org/rules`, capturé le 2026-10-30 (`bronze.raw_pages` page_type `rules`). **[D]** = Discord, veille du 2026-10-30 (`outputs/hardwood/veille/`, statut entre parenthèses). **[A]** = document d'aide de l'utilisateur (`data/manual/hardwoord/Aide docs.txt`, 2026-10-30 : tableaux épinglés sur Discord et conseils d'un ancien). **[E]** = constaté dans nos exports. **[H]** = hypothèse à confirmer. **[U]** = règle de l'utilisateur.

### `.claude/skills/hardwood-regles/references/01-structure.md` — 5 lignes ajoutées, 4 sur le sujet
## Structure [R:Conference Structure, Conference, Tournaments]
- Pyramide : 1 conférence de niveau I, 2 de niveau II, 4 de niveau III, etc. ; 16 équipes par conférence. Division 1 = niveaux I à IV, Division 2 = niveau V, Division 3 = niveau VI.
- **Les 3 premiers montent, les 6 derniers descendent**, sur le **classement de conférence de la saison régulière** ; égalité départagée à la différence de points.
- Nous : Eureka Red Devils (#940), conférence **VI.26 (Division 3)**, descendue le 03/09/2054 [E].

### `.claude/skills/hardwood-regles/references/02-calendrier-d-une-saison.md` — 16 lignes ajoutées, 15 sur le sujet
## Calendrier d'une saison [R:Games, Schedule] [D]
| Phase | Matchs | Compte pour |
|---|---|---|
| Exhibitions | 3 [E] | rien (minutes de développement seulement) ; ne comptent pas dans la limite de redshirt |
| Hors conférence | 10 | RPI, SOS, sélection au tournoi |
| Conférence | 30 (aller-retour) | classement, titre, montée/descente |
| Playoffs de conférence | jusqu'à 4 (16 équipes, élimination directe) | vainqueur qualifié d'office au tournoi de sa division |
| Tournoi de division | 64 équipes, jusqu'à 6 matchs (mars) | titre ; sélection RPI + niveau + rang en conférence |
| Invitational | groupes de 4 puis 4 vainqueurs | équipes non qualifiées ; ne compte pas pour le redshirt |
- **1 match par jour réel**, simulé vers 9 h (heure du Pacifique), soit 17 h-18 h à Paris [E : « @ 9:00 am »]. Saison ≈ 56 jours réels [D (confirmé)].
- **Coaching (progression) : jeudi et dimanche matin, heure du Pacifique** [R:Players].
- Recrutement : 53 mises à jour, une après chaque journée [R:Recruiting Calendar].
- Le passage de saison (« flip ») dure 12 à 24 h ; tout est gelé, recrutement compris (« dead period » depuis 2026-06) [D (confirmé)].
- Matchs de rivalité : 4 adversaires hors conférence au choix ; mode de programmation Up / Down / Any [R:Non-Conference Scheduling].
- **Pas d'argent, pas de budget, pas de transferts** : l'arène limite seulement les spectateurs [R:Arena] [D (confirmé)].

### `.claude/skills/hardwood-regles/references/03-effectif.md` — 5 lignes ajoutées, 4 sur le sujet
## Effectif [R:Team Roster, Walk-Ons]
- **13 joueurs boursiers au maximum**, plus des walk-ons (non boursiers) qu'on ne choisit pas. 4 ans d'éligibilité, plus 1 an de redshirt possible.
- **Walk-ons [U, 2026-10-30]** : jamais exportés (pas de page joueur) ni proposés dans le depth chart ; leurs minutes freinent le développement des jeunes boursiers [D (stromstar 2025-02)]. Le roster suffit pour les voir ; `gold.hw_depth_suggest.walk_on_meilleur` signale seulement un walk-on nettement meilleur qu'un boursier.
- Inactif plus de 35 jours = équipe perdue [R:Activation].

### `.claude/skills/hardwood-regles/references/04-joueurs.md` — 12 lignes ajoutées, 11 sur le sujet
## Joueurs [R:Players]
- 14 compétences de 0 à 20 : attaque IS (tir intérieur), OS (tir extérieur, **et lancers francs**), Rng (portée), Fin (finition) ; défense Reb, IDef, PDef ; jeu IQ, Pass, Hnd, Drv ; physique Str, Spd, Sta. Plus taille, poids, envergure et détente, qui ne sont pas dans le SI.
- **Skill Index (SI)** = somme des compétences. **Potentiel** = mesure des plafonds, avec une part d'incertitude.
- Chaque compétence a une base et un plafond ; la valeur actuelle monte avec le **coaching** (surtout chez les jeunes) et **l'expérience** (chaque minute jouée, plus une base pour la présence à l'entraînement).
- **Valeurs affichées = estimation, jusqu'à ±20 % de la vraie valeur** ; elles se précisent avec les matchs et peuvent donc baisser à l'affichage sans vraie baisse.
- Pas de compétence cachée, mais des valeurs fixes cachées pèsent un peu sur certaines actions.
- Plafond de SI ≈ 14 × potentiel + 0 à 13 (pot 10 → 140-153) [D (confirmé par plusieurs joueurs, pas par Steve)] [A : tableau pot 9-17] ; table `silver.hw_ref_potential_caps`.
- **Compétences clés par poste [A]** : PG = IQ, Pass, Hnd, Spd ; SG = OS, Spd ; SF = OS, défense complète (IDef + PDef), Spd, plus grand que PG et SG ; PF et C = IS, Reb, grand. Un ancien juge « acceptable » une compétence clé à **13 ou plus** [A]. Note par poste : `gold.hw_player_pos_scores` (0,6 × moyenne des clés + 0,4 × SI/14, pondération [H]).
- Postes : le poste principal est celui où le joueur a le plus d'expérience, pas forcément son meilleur. Majuscule = poste maîtrisé, minuscule = en apprentissage ; on gagne l'expérience d'un poste en y jouant, exhibitions comprises.
- La taille et le physique changent en grandissant : la taille projetée n'est qu'une estimation.
- Déclin vers 30 ans : ne touche pas les joueurs universitaires.

### `.claude/skills/hardwood-regles/references/05-entrainement.md` — 4 lignes ajoutées, 3 sur le sujet
## Entraînement [R:Player Development]
- Un **focus principal et un focus secondaire** reçoivent plus de coaching à chaque mise à jour. S'y ajoutent **8 entraînements additionnels** au petit effet : Post Moves, Shooting, Foul Shooting, Ball Handling & Passing, Video / Film Work (IQ), Defense, Fitness (stamina), Strength Training. Sans effet sur les recrues déjà engagées.
- L'essentiel de la progression vient du coaching général et du poste joué en match.

### `.claude/skills/hardwood-regles/references/06-fatigue-overwork-blessures.md` — 6 lignes ajoutées, 5 sur le sujet
## Fatigue, Overwork, blessures [R:Fatigue, Overwork, Injuries]
- Fatigue en match selon les minutes ; une stamina haute la réduit. Elle touche tout le jeu et l'effort défensif en fin de match. Niveaux affichés dans le box score : -, Lght, Mod, Hvy [E].
- **Overwork** : un joueur proche de **40 min par match** ou qui joue souvent fatigué **perd de l'efficacité jusqu'à la fin de la saison**. La feuille de match indique « Overworked » [E].
- Fatigue [A] : elle baisse la qualité du joueur pendant le match et augmente le risque de blessure, mais **les joueurs sont reposés entre deux matchs** : inutile de réduire ses minutes au match suivant. Le risque s'accumule seulement si on le fatigue sans cesse.
- Tout joueur qui joue peut se blesser, et la fatigue augmente le risque [D (confirmé Steve)]. Un blessé est noté « +N » jours [E]. Aucune suspension en cours de saison [D (en doute : rien trouvé)].

### `.claude/skills/hardwood-regles/references/07-redshirt.md` — 6 lignes ajoutées, 5 sur le sujet
## Redshirt [R:Red Shirting]
- Joueur boursier et non senior, **5 matchs au plus** (hors conférence, conférence, playoffs, tournoi ; exhibitions et invitational exclus), minutes illimitées dans ces 5 matchs. Un seul redshirt par carrière.
- Il faut **cocher la case Red Shirt dans Game Management avant la fin de saison**. Cochée tôt, le moteur limite le joueur à 5 matchs. Le plus sûr : cocher, retirer le joueur du depth chart et des Game Plans, Playing Time à 0.
- Le redshirt ne ralentit pas la progression ; il coûte de l'intérêt chez les recrues 4-5 étoiles [R:Recruiting Success Factors] [D (confirmé)].
- [A] Le redshirt prend effet **après** la saison (case laissée cochée → RS FR la saison suivante) ; plusieurs joueurs peuvent être redshirtés. Dans `silver.hw_management.red_shirt` : « oui » = cochée, « non » = possible, « impossible » = case grisée (senior, déjà RS ou plus de 5 matchs).

### `.claude/skills/hardwood-regles/references/08-coachs.md` — 9 lignes ajoutées, 8 sur le sujet
## Coachs [R:Head Coaches, Assistant Coaches]
- Notes : Offense, Defense, Game Tactics (surtout en fin de match), Recruiting, Motivation (momentum), Player Development. Salaire minimum 500 000 $. Déclin du head coach entre 55 et 70 ans.
- **3 assistants** qui renforcent le head coach selon leurs points forts (pas une simple moyenne). Un assistant part vers un poste de head coach au-delà de **1 M$ de salaire ou 50 ans**.
- **Un recrutement de coach par jour réel.** Les assistants ne se remplacent qu'**avant la saison de conférence ou après la saison**.
- **Renvoyer le head coach fait chuter l'intérêt des recrues en cours** (pas celles déjà engagées). Changer d'assistant a un petit effet, positif si le nouveau recrute mieux.
- Nous [E] : head coach Darius McNair, 67 ans (âge de déclin), Off 10, Def 13, Tac 0, Dev 11, Mot 11, **Rec 3**, 2,6 M$.
- **Lire la page d'un coach (phrases → note) [A]** : Offense 14+ good, 11-13 above average, 10 rien, 0-9 below average · Defense 15+ good, 11-14 above average, 10 rien, 0-9 below average · Tactics 15+ « excellent X's and O's » (pas toujours affiché à 15), 12-14 good, 0-11 rien · Development 15+ excellent teacher, 12-14 good teacher, 9-11 rien, 0-8 poor · Motivation 15+ great, 12-14 good, 0-11 rien · Recruiting (avant l'effet de l'âge) 15+ excellent, 13-14 good, 11-12 decent, 5-10 rien, 0-9 poor (chevauchement : un 9 peut porter « poor »).
- Tableau prêt : `gold.hw_coach_board` (notre staff contre les 5 meilleurs libres de moins de 55 ans : total, Rec, Dev).

### `.claude/skills/hardwood-regles/references/09-classements.md` — 3 lignes ajoutées, 2 sur le sujet
## Classements [R:Ratings]
- Rating : force estimée selon les victoires. **RPI** : bilan + force du calendrier, il sélectionne le tournoi. SOS : force du calendrier. **TPI** : moyenne pondérée des SI des 10 meilleurs joueurs (les 5 premiers comptent double). Prestige : titres et matchs de tournoi, bonus de recrutement. Fan Mood : affluence. Alumni Mood : pèse sur le renvoi du coach par les bots.

### `.claude/skills/hardwood-regles/references/10-ce-qui-reste-inconnu.md` — 2 lignes ajoutées, 2 sur le sujet
## Ce qui reste inconnu
Formule du RPI, ampleur exacte du malus hors poste, bonus du terrain, effet chiffré de la fatigue et de l'Overwork, formule des assistants (« Game Engine Algorithm Discussion : To Do » dans le manuel).

### `.claude/skills/hardwood-tactique/SKILL.md` — 12 lignes ajoutées, 12 sur le sujet
description: Hardwood, match : Game Plan, depth chart, Pace, Inside/Outside, Man/Zone/Pressure, substitutions, ajustements de mi-temps, Game Management, feuille de match. Pour régler un match ou lire un adversaire.
Ce fichier est un index : le contenu est dans `references/`. Lis seulement la section utile à la question ; chaque fichier reprend telle quelle une section de l'ancien SKILL.md (contenu inchangé).
| Fichier | Section |
| `references/00-introduction.md` | Introduction et sources |
| `references/01-game-plan.md` | Game Plan [R:Game Strategy, Depth Chart & Game Plan] |
| `references/02-game-tactics.md` | Game Tactics [R:Setting Up Your Game Tactics] [E] |
| `references/03-game-management-par-joueur.md` | Game Management, par joueur [R:Game Management Settings] [E] |
| `references/04-methode-d-un-ancien.md` | Méthode d'un ancien [A] |
| `references/05-ce-que-dit-la-communaute.md` | Ce que dit la communauté [D] |
| `references/06-lire-un-match-feuille-game-id.md` | Lire un match (feuille /game/<id>) [E] |
| `references/07-tableaux-prets.md` | Tableaux prêts |
| `references/08-inconnu.md` | Inconnu |

### `.claude/skills/hardwood-tactique/references/00-introduction.md` — 3 lignes ajoutées, 2 sur le sujet
## Introduction et sources
Sources : **[R:Rubrique]** = manuel officiel (capturé le 2026-10-30). **[D]** = Discord, veille du 2026-10-30 (`outputs/hardwood/veille/v-tactique.md`, statut entre parenthèses). **[A]** = document d'aide de l'utilisateur (`data/manual/hardwoord/Aide docs.txt`, 2026-10-30). **[E]** = nos exports (vues `silver.hw_tactics`, `hw_management`, `hw_games`, `hw_game_teams`, `hw_game_box`).

### `.claude/skills/hardwood-tactique/references/01-game-plan.md` — 4 lignes ajoutées, 3 sur le sujet
## Game Plan [R:Game Strategy, Depth Chart & Game Plan]
- **Chaque match peut avoir son propre Game Plan** (lien « (set) » du calendrier) = un depth chart + des Game Tactics avec ajustements. Sans plan spécifique, le **plan par défaut** s'applique ; il sert aussi de point de départ à chaque plan de match.
- Depth chart : les 5 titulaires (tous différents) en haut, puis les remplaçants ; un même joueur peut doubler deux postes. Le moteur remplit les trous dans l'ordre **PG, C, PF, SF, SG**.

### `.claude/skills/hardwood-tactique/references/02-game-tactics.md` — 20 lignes ajoutées, 18 sur le sujet
## Game Tactics [R:Setting Up Your Game Tactics] [E]
| Réglage | Valeurs | Effet |
|---|---|---|
| Pace | -5 à +5 | + = plus vite, plus de transition, moins de temps de possession |
| Inside/Outside Emphasis | I, i, ~, o, O | I = cherche les tirs intérieurs, O = extérieurs |
| Zone % / Pressure % | 0 à 100 par pas de 5 | le reste = individuelle (Man-to-Man). Zone : PG, SG, SF dehors, PF et C dedans [R:Glossary] |
| Extend | -5 à +5 (NC = inchangé à la mi-temps) | + = défense étendue vers l'arc, - = resserrée sous le panier ; elle dérive pendant le match selon les réussites adverses |
| Substitution Mode | Mass, Staggered A, B, C | voir ci-dessous |
- **Ajustements de mi-temps : 5 au plus**, chacun avec un déclencheur (Point differential, Points in the paint, 3-pointers made, Personal fouls, Opponent points in the paint, Opponent 3-pointers made) et un seuil bas et/ou haut (-25 à +25). **Seul le premier qui remplit son critère s'applique.**
- Lire les seuils [A : Neph, Discord 2022-04-09] : le seuil décrit la condition ; « Lower ≥ X » = « si la valeur est au moins X », « Upper ≤ X » = « au plus X ». Exemples : Opponent points in the paint, Lower ≥ (valeur jugée dominante) → Extend −3 ; Opponent 3-pointers made, Lower ≥ 6 → Extend +2. Les deux seuils ensemble servent aux tranches de Point differential : ≤ −20 · −19 à −1 · 0 à 10 · ≥ 11.
### Repos des titulaires (minutes restantes dans la mi-temps) [R]
| Mode | Repos |
|---|---|
| Mass | tous entre la 7e et la 15e minute |
| Staggered A | C 18-11 ; PG et SF 15-8 ; SG et PF 12-5 |
| Staggered B | **PG et C 18-11** ; SG et PF 12-5 ; SF 15-8 (garde les postes clés occupés par les meilleurs) |
| Staggered C | repos courts : C 18-15 et 12-9 ; PF 15-12 et 6-3 ; SF 12-6 ; SG 18-15 et 6-3 ; PG 15-12 et 9-6 |
Le repos dépend aussi du Playing Time de chaque joueur.

### `.claude/skills/hardwood-tactique/references/03-game-management-par-joueur.md` — 10 lignes ajoutées, 9 sur le sujet
## Game Management, par joueur [R:Game Management Settings] [E]
| Réglage | Valeurs | Effet |
|---|---|---|
| Green Light | x, --, -, (neutre), +, ++ | fréquence de tir ; x = ne tire jamais |
| Offensive Positioning | I, i, (neutre), o, O | où il joue. Arrière ou ailier en I : coupe vers le panier et évite l'arc. Grand en o/O : joue dehors (stretch-4). Influe aussi sur le rebond offensif |
| Playing Time | 0 à 40 min (1 à 15 « non recommandé ») | 40 ≈ tout le match ; **32 = moyen** ; 25 = plus bas conseillé ; **minimum 15 pour un titulaire** ; ignoré en prolongation ; 0 pour un redshirt |
| Foul Trouble Hook | none, slow, average, quick | vitesse de sortie en cas de fautes |
| Red Shirt | case à cocher | voir `hardwood-regles` |
- Nous, le 30/10 [E] : les 20 joueurs ont tous 32 min, average, Green Light et positionnement au neutre ; c'est le réglage par défaut, jamais personnalisé.

### `.claude/skills/hardwood-tactique/references/04-methode-d-un-ancien.md` — 7 lignes ajoutées, 6 sur le sujet
## Méthode d'un ancien [A]
- **Le talent des joueurs compte plus que la tactique** : partir des réglages par défaut, observer quelques matchs, puis ajuster un réglage à la fois.
- Pace : plus de possessions favorisent l'équipe la plus forte ; moins de possessions augmentent la part de hasard, donc aident la plus faible. Plus rapide = plus de fatigue.
- Équipe lente : pas de Pace élevé ni de pressing. Mauvais défenseurs : pas beaucoup d'individuelle. Faible dehors et dedans : ni Extend + ni −. Petite, pas longue ni intelligente : la zone ne marche pas bien. Nourrir l'intérieur si nos meilleurs marqueurs sont des IS.
- Gagner maintenant ou développer : les minutes des jeunes boursiers les font progresser ; un jeune titulaire coûte des matchs cette saison.
- Les 5 repos de Mass / Staggered A-B-C sont dans un tableau minute par minute (image du doc) : voir le tableau « Repos des titulaires » ci-dessous.

### `.claude/skills/hardwood-tactique/references/05-ce-que-dit-la-communaute.md` — 7 lignes ajoutées, 6 sur le sujet
## Ce que dit la communauté [D]
- Pressure fait plus de fautes que Man, et Man plus que Zone ; le consensus est de mélanger les trois (confirmé par plusieurs joueurs).
- La zone est une seule zone (de type 3-2), sans 2-3 ni 1-3-1 (consensus 2026-01, sans réponse de Steve).
- Avant 2026, Extend négatif par défaut. **Le 2026-08-23, Steve a modifié Extend et le spacing** (scoring intérieur plus dur, plus d'ouvertures dehors) : tout conseil plus ancien est à retester.
- Les tirs à 3 points ont été relevés début 2026 (réglage de Steve).
- Pace et Foul Hook sont les deux grands leviers des fautes ; la taille pèse beaucoup dans le moteur.

### `.claude/skills/hardwood-tactique/references/06-lire-un-match-feuille-game-id.md` — 7 lignes ajoutées, 6 sur le sujet
## Lire un match (feuille /game/<id>) [E]
- **Notre tactique demandée** (1re mi-temps, 2e mi-temps ou « No Change ») → `silver.hw_games`.
- **Défense réellement jouée par les deux équipes** : % Man, Zone, Pressure, 2nd Chance, Transition, Intentional Foul, et Extend au début, à la mi-temps et à la fin → `silver.hw_game_teams`. **C'est notre seule lecture de la tactique adverse** : on ne voit pas ses réglages.
- Efficacité par zone : au cercle, intérieur, mi-distance, à 3 points (réussis/tentés) ; SI pondéré et TPI des deux équipes ; blessés ; joueurs en Overwork.
- Box score → `silver.hw_game_box` : poste joué, minutes, tirs, OFG (tirs de l'adversaire direct), +/-, DIST (distance moyenne de tir), PITP, FBP, FD, **fatigue** (-, Lght, Mod, Hvy).
- Pour préparer un adversaire : ses matchs précédents (défense mesurée, efficacité par zone) et ses SI/TPI.

### `.claude/skills/hardwood-tactique/references/07-tableaux-prets.md` — 4 lignes ajoutées, 3 sur le sujet
## Tableaux prêts
- `gold.hw_depth_suggest` : depth chart proposé (boursiers valides, ordre de remplissage du moteur PG, C, PF, SF, SG ; colonnes `actuel`, `controle`, `walk_on_meilleur`).
- `gold.hw_season_games` (match par match : notre tactique, efficacité par zone nous/eux, défense adverse mesurée, SI pondéré) et `gold.hw_vd_compare` (victoires contre défaites, toute la saison).

### `.claude/skills/hardwood-tactique/references/08-inconnu.md` — 2 lignes ajoutées, 2 sur le sujet
## Inconnu
Bonus du terrain (réel d'après les joueurs, non chiffré), poids exact de la vitesse, de l'IQ et de la taille, effet des notes Game Tactics et Motivation du coach, algorithme des remplacements (« To Do » dans le manuel).

### `outputs/hardwood/learnings.md` — 12 lignes ajoutées, 1 sur le sujet
| C-003 | 2026-10-30 | Depth chart SG et C titulaires selon `gold.hw_depth_suggest` | `select depth, pos, propose, actuel, controle from gold.hw_depth_suggest` : `controle` = ok | appliqué (SG, C titulaires) | SG Adkins ✔, C Howell ✔. Reste 🟧 : PF titulaire Barbieri blessé (proposé Young), C remplaçant Chance (proposé McCleary) |

## Nouveau — Discord / chat
- rien de nouveau.

## Du jour
- registre : `outputs/hardwood/fait-2026-11-04.md`
- exports : `bronze.raw_pages` where game = 'hardwood' and captured_at >= '2026-11-04'

## Couverture (à remplir)
| Source | trouvés | lus | retenus | écartés (pourquoi) |
|---|---|---|---|---|
| carte (variables) | | | | |
| nouveau règles | | | | |
| nouveau Discord/chat | | | | |
