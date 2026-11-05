# Plan v3 — moteur de décision multi-jeux (version consolidée du 2026-11-05)

À copier dans le dépôt sous `docs/refonte-v3/plan.md`, avec un journal neuf `docs/refonte-v3/journal.md`. **Ce fichier est le seul plan à suivre.** Il remplace `docs/refonte-v2/plan-reprise.md` et le brouillon v3 du matin. Les phases 0 à 4 de `docs/refonte-v2/plan.md` restent acquises (collecte, `core`, `learn`, `kb`).

Comment l'utiliser : une session = un bloc `S<n>` du § 8. Claude lit le bloc, `docs/refonte-v3/journal.md` et rien d'autre, exécute, prouve, commite, met à jour le journal, puis `/clear`.

## 1. Objectif et critères de réussite

**Ce que veut l'utilisateur** (ses mots, 2026-11-05) : chaque soir, pour chaque jeu, un « que faire » complet — composition, tactique, entraînement, transferts, académie, finances, stade, personnel — fondé sur des faits : tables de référence, deltas depuis la veille, historique des matchs. Une analyse qui explique **pourquoi** on gagne ou on perd (tactique, joueur, force de l'adversaire). Un système qui apprend, ne répète pas les mêmes compositions sans raison, sait en quelle phase de saison on est, et s'étend facilement à d'autres clubs et d'autres jeux. Un modèle appelé seulement quand il apporte quelque chose.

**La réussite se mesure à la qualité de décision, pas au coût en tokens.**

| # | Mesure | Cible |
|---|---|---|
| Q1 | Catégories rendues par jeu un soir de match | Toutes celles du calendrier, avec un « si » |
| Q2 | Durée d'un soir par jeu | Moins de 10 minutes |
| Q3 | Appels au modèle par jeu et par soir | 0 sans événement ; 6 à 8 par semaine au plus |
| Q4 | Décisions avec prédiction mesurable | 100 % |
| Q5 | Décisions évaluées dans leur fenêtre | Plus de 80 % |
| Q6 | Lignes de `ref.*` modifiées par des résultats | Quelques-unes par semaine |
| Q7 | « Inchangé » sans preuve par les options ni test nommé | 0 |
| Q8 | Défaites avec revue causale | 100 % |
| Q9 | Même composition recopiée plusieurs jours sans raison chiffrée | 0 (alerte) |
| Q10 | Export demandé en tête du plan du soir | 0 |
| Q11 | Lignes de tes listes « chose à faire » (`docs/chose-a-faire*.txt`, `docs/chose-a-DM.txt`) répondues **dans le rendu du soir** quand elles sont dues (§ 5.12) | 100 % ; un ✅ de `docs/couverture` ne suffit pas |
| Q12 | Pour chacun des 6 jeux : preuves P1 à P4 et tests du soir tous ✅, ou ⏳ et ⛔ expliqués (§ 8 bis) | 6 jeux sur 6, aucun ❌ sans repli appliqué |

## 2. Décisions déjà prises (ne pas les rouvrir)

| Décision | Source |
|---|---|
| Jeu de départ : BasketVibe | Utilisateur, 2026-11-05 (« je confirme tout ») |
| Accord écrit pour séparer, dans `CLAUDE.md` inviolable 3, l'horizon d'**action** (aujourd'hui) et l'horizon de **raisonnement** (la saison). Texte exact : Annexe C | Utilisateur, 2026-11-05 |
| Charte remplie pour 11 équipes (§ 3) | Utilisateur, 2026-11-05 |
| Team Soccer, équipes 1 et 2 : les jeunes jouent quand il n'y a plus rien à jouer | Utilisateur, 2026-11-05 (« fais tourner les jeunes ») |
| Exports **ciblés par le calendrier de chaque jeu** (ce qui s'est passé depuis le dernier export de l'écran), pas par un âge maximal ; jamais « tous les exports de tous les jeux » (§ 5.2 bis) | Utilisateur, 2026-11-05 |
| Tables de référence : première version validée par l'utilisateur en tableau, une fois | Utilisateur, 2026-11-05 |
| Exports manquants : l'utilisateur les fait (liste donnée par S3) | Utilisateur, 2026-11-05 |
| Aucun nouveau hook : ce qui doit être garanti est fait dans `soir.py` | Ce plan |
| Aucun achat, vente ni enchère sans accord écrit | `CLAUDE.md` inviolable 2 |
| Collecte passive seulement (Tampermonkey) ; exports Discord manuels | `CLAUDE.md` inviolable 1 |
| Plan Supabase gratuit : pas de sauvegarde automatique, quota à surveiller | Journal v2 |

## 3. La charte des 11 équipes (réponses de l'utilisateur, traduites)

| Jeu · équipe | Objectif | Horizon (valeur technique) | Minutes aux jeunes si rien à jouer | Vendre pour profit | Intouchables / à vendre |
|---|---|---|---|---|---|
| BasketVibe · Chomelix | titre | `3_saisons` (« maintenant et moyen terme ») | oui | oui | aucun, « la meilleure équipe » |
| Six Zero League | titre | `long_terme` | oui | oui | aucun |
| Hardwood | titre | `long_terme` | oui | **non : pas de ventes, du recrutement** | aucun |
| Team Soccer · équipe 1 | titre | `3_saisons` | oui | oui | aucun |
| Team Soccer · équipe 2 | titre | `3_saisons` | oui | oui | aucun |
| Hockey Nation · PRO, FRM, U21, U17 (4 équipes) | titre | `3_saisons` | **sans objet** (les jeunes sont déjà dans U21 et U17) | **non : pas de ventes, des échanges** | échanges « à voir plus tard » |
| Derby Manager · QOS | **maintien** | `long_terme` | oui | oui | aucun, « les meilleurs jeunes » |
| Derby Manager · Marmandes | titre | `maintenant` (« court terme ») | oui | oui | aucun, « les meilleurs joueurs » |

Déductions déjà actées, avec leur source :
- Hockey Nation : domaines exclus en saison = finances, plafond salarial, staff d'entraîneurs ; le travail porte sur les matchs et le scouting (utilisateur, 2026-11-04, rétro `outputs/retro/2026-11-04.md`, mémoire `feedback-hn-matchs-scouts-pas-finances`).
- Hockey Nation et Hardwood : l'action « vente » n'est jamais proposée. Les échanges de Hockey Nation ne sont pas traités tant que l'utilisateur ne les décrit pas.
- « Aucun intouchable » veut dire que le moteur peut proposer de vendre n'importe qui, **toujours sans exécution sans accord écrit**.

**À confirmer (aucun ne bloque S0 à S4 ; le premier est demandé avant S7) :**
1. **Hockey Nation : en cas de conflit de promotion** (monter un U21 en PRO affaiblit U21, alors que l'objectif est le titre pour les quatre), qui a priorité ? Valeur proposée : PRO, puis FRM, puis U21, puis U17.
2. **Temps disponible par soir et par jeu** (en minutes). Sans réponse, le plan du soir est classé mais pas coupé.
3. **Tests tactiques en match de ligue.** Valeur par défaut : amicaux seulement.
4. **Perte nette tolérée sur les transferts en 4 semaines.** Claude propose un montant par équipe à partir des recettes observées, dans un tableau à valider.
5. **Derby Manager : rattacher QOS et Marmandes à leurs identifiants de club** (547 et 307 dans la base) : Claude les lit dans l'adaptateur et te montre la correspondance avant d'insérer.

## 4. Architecture

### 4.1 Principes
1. **Le code garantit, les tables savent, le modèle juge les cas limites.**
2. **Une décision part d'une situation, d'options et d'un objectif** ; elle sort avec une prédiction mesurable et ce qui prouverait l'erreur ; elle est jugée après coup.
3. **Le savoir est dans des tables, pas dans de la prose** : source, confiance, nombre d'observations, date de validité sur chaque ligne.
4. **On compare, on ne relit pas** : aujourd'hui contre hier et contre la référence. Zéro écart, zéro ligne.
5. **Donnée vieille ou absente = confiance abaissée et nommée**, jamais une demande d'export en tête du plan.
6. **Pas d'apprentissage sur une observation.** Indice dès 3, règle dès 5 (paramètres à ajuster).
7. **Pas de nouveau contrôle avant le moteur** (la leçon du 04/11).

### 4.2 Vue d'ensemble
```
  COLLECTE (existant)  bronze → silver → core (adaptateurs)         CONNAISSANCE kb (Discord, forums, manuels)
        │                                                                   │ valeurs de départ, patchs
        ▼                                                                   ▼
  ┌──────────────────────────── QUOTIDIEN, sans modèle ─────────────────────────────┐
  │ DÉTECTEURS     deltas du jour contre hier et contre ref.*  → gold.signal        │
  │ ÉTAT DU CLUB   phase de saison · objectif · probabilités · 7 indices de santé   │
  │ SITUATIONS     catalogue de cas reconnus (stade, argent, trou à un poste…)      │
  │ MODULES        un par domaine : options chiffrées → choix → prédiction          │
  └──────────────┬─────────────────────────────────────────────┬────────────────────┘
                 │ cas ambigu / événement                       │ toujours
                 ▼                                              ▼
       RAISONNEUR (1 appel borné par jeu)        RENDU par script + verifier_rendu.py
                 └──────────► learn.decision (prédiction, date d'évaluation) ◄────────┘
                                        │
  APRÈS CHAQUE MATCH : revue causale → learn.match_review → learn.hypothesis / experiment
                                        │
  CHAQUE SEMAINE : RÉVISEUR relit résultats et hypothèses → propose les changements de ref.*
                                        ▼
                         ref.* mis à jour, versionné, diff montré
```

### 4.3 Cadences et rôle du modèle
| Cadence | Ce qui tourne | Modèle |
|---|---|---|
| Chaque soir, par jeu | Fraîcheur, deltas, évaluation des décisions échues, état du club, situations, modules, rendu, vérification | Non par défaut ; un appel du raisonneur au plus si un déclencheur est vrai |
| Après chaque match | Revue causale en SQL | Non ; le raisonneur écrit le récit seulement pour une défaite, une surprise ou une série |
| Chaque semaine | `semaine.py` : mise à jour de `ref.*`, bilan « sommes-nous sur la bonne voie ? » | Oui, un réviseur par jeu |
| Chaque saison, ou sur demande | Charte, paramètres de jeu, nouveaux leviers | Oui, avec l'utilisateur |

Déclencheurs du raisonneur (liste fermée, un appel par jeu et par soir au plus) : défaite ou résultat contraire à l'attendu non expliqué ; deux options sous la marge ; montant supérieur au seuil de gros montant de la charte ; deux affirmations `kb` contradictoires pour la même décision ; situation absente de `ref.*` ; série de 2 défaites ou plus.

## 5. Les composants

### 5.1 Tables de référence (schéma `ref`)
Colonnes communes : `source` (id `kb.claim` ou « observé chez nous »), `confidence`, `n_obs`, `valid_from`, `valid_to`, `version`. Rien n'est supprimé : une ligne remplacée est fermée.

| Table | Contenu | Départ | Mise à jour hebdomadaire |
|---|---|---|---|
| `ref.training_focus` | Poste × âge × note → compétences à travailler, priorité, intensité | `kb` thème entraînement + skills | Gain réel contre gain attendu par joueur |
| `ref.player_score` | Poids des statistiques par poste et capacités spéciales : **score maison** (scouts Hockey Nation) | Skills + `kb` | Corrélation avec les performances |
| `ref.price_benchmark` | Poste × âge × note → p25, médiane, p75, part réglée, `n_obs` | Historique des transferts en base | Delta à chaque export du marché |
| `ref.team_need` (vue) | Besoins par poste de **mon** effectif | Calcul quotidien | — |
| `ref.tactic_effect` | Réglage × contexte (adversaire plus fort / égal / plus faible, domicile, type de compétition) → V/N/D, écart moyen | `kb`, puis nos matchs | Recalcul après chaque match |
| `ref.expected_result` | Écart de force → probabilités de V/N/D | Prudent (plat, confiance basse) | Recalibrage hebdomadaire |
| `ref.academy_profile` | Ce qu'est un bon prospect par poste | `kb` + nos promotions | Résultats des promus |
| `ref.health_threshold` | Seuils des indices de santé | Sourcés ou « à calibrer » | Revue du réviseur |
| `ref.action_handler` | Ligne d'agenda → module de décision | Données | Quand l'agenda change |

### 5.2 Détecteurs de deltas (quotidien, SQL) → `gold.signal`
Colonnes : jeu, domaine, entité, gravité, preuve, action suggérée, **empreinte** (pas de répétition), statut `ouvert | fait | ignoré`. Le registre `fait-AAAA-MM-JJ.md` devient le statut des signaux.

| Détecteur | Compare | Produit |
|---|---|---|
| Marché | Annonces contre `price_benchmark` et `team_need` | Sous le prix et comble un besoin ; mon joueur vaut plus que sa référence ; enchère maximale |
| Effectif | Progression, blessures, forme, contrats | Joueur en retrait, blessé, fin de contrat |
| Entraînement | Focus saisi contre `training_focus` | Seulement les écarts, avec la saisie exacte |
| Matchs | Nouveaux résultats | Déclenche la revue causale |
| Classement | `season_context` d'hier contre aujourd'hui | Changement d'objectif |
| Finances | Solde contre capacité moins dépenses engagées | Montant disponible |
| Stade (si le jeu en a un) | Affluence contre capacité sur N matchs | Plein ou vide : prix, agrandissement |
| Fraîcheur | Dernier export par écran | Confiance abaissée par domaine |

### 5.2 bis Le calendrier de chaque jeu : source unique de l'agenda et des exports
Les données n'arrivent que quand tu ouvres une page : les exports restent nécessaires, mais **ciblés par ce qui s'est passé dans le jeu**, pas par un âge maximal. Le `max_age_h` actuel de `core.export_rule` (24 h, 72 h, 168 h) est un reste des anciennes vues : il ne sait pas qu'un entraînement tombe le dimanche à 04:00 ou qu'un rapport d'académie sort le jeudi. Il ne reste que comme **filet de sécurité** pour un écran dont aucun événement n'est connu.

**`core.game_event`** : une ligne par événement récurrent ou daté du jeu. Colonnes : jeu, `event_id`, déclencheur (`match`, `jour_semaine`, `tous_les_jours`, `jour_saison`, `tous_les_n_jours`, `fenetre`, `fin_saison`, `date`), heure et fuseau, type de compétition, **effet** (ce que le jeu fait : « entraînement appliqué, salaires prélevés »), **écrans modifiés** (liens vers `core.export_rule`), **action de l'utilisateur** (catégorie, priorité, phrase modèle, reprises de `agenda_rule`), **verrou** (heure limite de saisie), source, statut `sourcé | à sourcer`.

Exemples, tirés de ce que tu as déjà dit et des profils :
- BasketVibe, dimanche 04:00 : entraînement, salaires, personnel facturé → écrans Équipe, Entraînement, Finances, Personnel. Jeudi 09:00 : rapport d'académie → écran Académie. Lundi, mercredi, samedi 20:00 : match → résultat, box, classement.
- Hockey Nation : missions de scouting chaque jour du jour 4 au jour 63 → écran scouting après chaque mission (`office_scouting`).
- Team Soccer : vendredi, entraînement et forme ; lundi 00:05, finances ; chaque jour, une révélation d'académie par club (01:00 UTC).
- Six Zero League : chaque soir après 21:00, cycle réglé (finances, entraînement, blessures, transferts ; 2 journées = 1 cycle).
- Hardwood : chaque jour match à 9:00 heure du Pacifique ; jeudi et dimanche, coaching ; après chaque journée, mise à jour du recrutement.

**Règles dérivées :**
1. Un écran est **périmé** si son dernier export est antérieur au dernier événement qui le modifie. Il est **frais** sinon, même s'il a six jours (les finances de BasketVibe exportées dimanche matin restent valables le mercredi ; elles sont périmées dès dimanche 04:00 suivant).
2. Un écran est **utile ce soir** s'il nourrit une action due ce soir, ou si une situation ouverte en dépend (le marché, seulement si un achat ou une vente est ouvert).
3. `gold.exports_needed` = périmé **et** utile → « Exporte X : l'événement Y a eu lieu à Z, il sert à W ». Un écran frais n'est jamais redemandé.
4. `core.agenda_rule` devient une lecture de `core.game_event` : **une seule source** pour « quand décider » et « quand les données changent ».
5. **Le plan du soir ne dépend jamais de cette liste** : s'il manque une donnée, la décision sort avec une confiance plus basse, nommée, et les exports utiles sont proposés après le plan.
6. Un événement que personne n'a sourcé est marqué `à sourcer` et listé en question à l'utilisateur. Jamais inventé.

### 5.3 Intelligence de situation
**État du club** (`core.club_state`, une ligne par équipe et par soir) : phase de saison, objectif, probabilités de saison, sept indices de 0 à 100 avec leurs causes.

| Indice | Calculé à partir de | Exemple de cause montrée |
|---|---|---|
| Effectif | Profondeur par poste, âge, blessés, contrats | « Trou à l'aile gauche » |
| Forme sportive | Résultats contre attendu | « 3 défaites, 2 attendues » |
| Finances | Trésorerie contre réserve, masse salariale contre plafond, bilan net des transferts, recettes | « −X sur les transferts en 4 semaines » |
| Jeunesse | Prospects par poste et âge | « Aucun gardien en formation » |
| Infrastructure | Niveaux contre référence, remplissage du stade | « Stade plein 5 matchs sur 5 » |
| Personnel | Niveaux contre référence, coût contre apport | « Entraîneur sous la référence, budget excédentaire » |
| Connaissance | Fraîcheur des exports, confiance des références | « Marché : dernier export il y a 3 jours » |

Un indice qui n'existe pas dans un jeu est absent, pas à zéro.

**Phase de saison** (`core.season_phase`, une ligne par jeu et par phase ; phases et déclencheurs tirés de `core.season` et du profil du jeu, « à sourcer » si inconnus) :

| Phase | Liste de contrôle |
|---|---|
| Début de saison | Audit complet : contrats, masse salariale contre plafond, budget, personnel, infrastructures, effectif par poste, jeunes, objectif et charte, prix des billets |
| Jour lambda | Agenda du jour et signaux ouverts : entraînement, match, tactique, marché |
| Fenêtre de transferts | Marché élargi, ventes et achats classés par bilan attendu |
| Mi-saison | Décisions contre prédictions ; objectif ajusté si l'écart l'impose |
| Dernière ligne droite | Probabilités de titre ou de maintien ; rotation et jeunes si l'objectif est acquis |
| Post-saison | Contrats, retraites, académie, sponsors, bilan de saison et leçons |

**Catalogue de situations** (`core.situation_rule`, généralise `agenda_rule` et `alert_rule`) : jeu (nul = tous), condition SQL, diagnostic, module, priorité, source.

| Situation | Détection | Réponse |
|---|---|---|
| Entraînement dû | Agenda | Écarts contre `training_focus` |
| Match ce soir | Agenda et verrouillage | Composition, tactique, « si » |
| Stade plein ou vide | Affluence contre capacité | Prix, agrandissement, selon charte et rendement |
| Recettes sous l'attendu | Recettes contre projection | Cause puis action |
| Trop de défaites | Échelle de diagnostic | Test tactique, besoin de transfert chiffré, ou rien si attendu |
| Pertes sur transferts | Bilan net 4 semaines au-dessus de la tolérance | Gel des achats, candidats à la vente |
| Masse salariale au-dessus du plafond | Salaires contre revenus | Non-renouvellement ou vente, classés |
| Trésorerie sous la réserve | Solde contre réserve | Vente ou arrêt des dépenses |
| Excédent | Capacité d'investissement | Investissements classés par rendement attendu |
| Personnel à recruter ou remplacer | Niveau contre référence et budget | Candidat, coût, gain attendu |
| Trou ou surplus à un poste | `team_need` | Achat, promotion, vente |
| Contrat qui se termine | Date de fin | Prolonger, vendre avant, laisser partir |
| Bonne affaire | Prix contre `price_benchmark` | Enchère maximale ; revente si la charte l'autorise |
| Mise à jour du jeu | Message officiel (§ 5.9) | Références concernées « à revalider », skills à réviser listés |
| Sponsor à choisir ou à changer (si le jeu en a) | Revenus et conditions du sponsor actuel contre les alternatives | Meilleur sponsor chiffré, sous réserve des règles de changement du jeu |
| Une action dépend d'une autre | `core.action_dependency` (ex. vendre avant d'acheter ; export « Recent changes » avant l'analyse d'entraînement ; composition avant le verrou) | Ordre imposé dans le plan du soir |

**Échelle de diagnostic quand l'équipe perd** (la première marche qui explique la série arrête l'échelle) : 1 attendu ? (adversaire nettement plus fort → rien à corriger, on le dit) · 2 disponibilité (titulaires absents ou hors poste) · 3 tactique contre ce type d'adversaire · 4 joueurs contre leur niveau · 5 structure (trou à un poste, effectif vieillissant → **besoin de transfert** : poste, note minimale, prix maximal selon charte et capacité) · 6 contrainte financière (vente préalable ou jeunes). Sortie : cause dominante, action d'aujourd'hui, preuve de l'erreur.

**Argent.** Registre des transferts `learn.transfer_ledger` (prix d'achat, date, rendement mesuré, prix de revente) : bilan net, rendement par poste et âge, alimente `price_benchmark`. Investissements (joueur, personnel, infrastructure) comparés au même critère : gain attendu par unité d'argent, avec la confiance de l'estimation.

**Priorisation du soir.** Score = gain attendu × urgence ÷ temps de saisie ; plan classé, coupé au temps disponible ; le reste reste un signal ouvert, jamais un « demain » dans le plan.

**Probabilités de saison.** Titre ou maintien acquis : calcul exact des points restants. Sinon simulation depuis `ref.expected_result` (probabilité de titre, de podium, de maintien). L'objectif du match en dépend. Fiabilité affichée.

### 5.4 Modules de décision (un par domaine)
Forme commune : **entrée** (situation, objectif, signaux du domaine, `ref.*`, leçons validées par `garde.py`) → **options** (réglage actuel et 1 à 3 alternatives, avec effet attendu, confiance, source) → **choix** (meilleur score ; sous la marge, déclencheur du raisonneur) → **quota d'exploration** (quand aucune option n'a d'avantage prouvé : un test nommé ; « inchangé » refusé s'il n'est pas prouvé par les options) → **sortie** (une action, un « si » chiffré, une prédiction mesurable, ce qui prouverait l'erreur) → **écriture** dans `learn.decision` par le module lui-même.

| Module | Options viennent de | Mesure de succès |
|---|---|---|
| Composition | Effectif, score maison, forme, fatigue, objectif (gagner, ménager, former) | Résultat contre `expected_result` |
| Tactique | `tactic_effect` pour ce contexte | Écart de buts, résultat contre attendu |
| Entraînement | `training_focus` contre saisie, gain mesuré | Gain par joueur contre attendu |
| Transferts | Signaux du marché, `team_need`, capacité, charte | Rendement après N matchs, bilan du registre |
| Académie | `academy_profile` contre prospects | Promotions réussies |
| Finances | Projection en 3 scénarios (prudent, central, favorable) | Solde de fin de saison contre projection |
| Stade, infrastructure, personnel (si le jeu les a) | Situations du catalogue, rendement attendu | Recettes, remplissage, niveau gagné par unité d'argent |

### 5.5 Analyse de match causale, hypothèses, expériences
Après chaque match, en SQL, `learn.match_review` calcule : **attendu** (`expected_result`) · **disponibilité** (titulaires absents, hors poste) · **tactique contre cet adversaire** (`tactic_effect`, avec `n_obs`) · **joueurs contre leur moyenne mobile** · **forme et fatigue** · **statistiques d'équipe quand elles existent** (existent au moins pour BasketVibe, `silver.bv_match_stats_team`, et Team Soccer, `ts_match_detail` ; les autres jeux : inventaire S3) · **verdict** : conforme à l'attendu, sous-performance ou sur-performance, avec facteurs dominants. Une donnée absente = « non mesurable ».

`learn.hypothesis` : énoncé testable (« ballon long contre une équipe plus forte → résultat inférieur à l'attendu »), contexte, observations pour et contre ; statut `proposée → en test → indice (n ≥ 3) → règle (n ≥ 5) → contredite`.
`learn.experiment` : le module lance un test nommé, en alternance avec le réglage de base, dans le même type de compétition et contre des adversaires de force comparable (les amicaux sont les terrains naturels ; les matchs de ligue seulement si la charte l'autorise).
**Raisonneur** : sur défaite, surprise ou série, reçoit la revue calculée (pas le Discord brut), écrit le récit, propose hypothèses et test ; sortie en JSON rangée en base.
**Limite** : avec un match par jour au mieux, 3 à 5 observations prennent des jours ou des semaines ; les valeurs de départ viennent de `kb`.

### 5.6 Orchestrateur : `soir.py <jeu>` et `semaine.py <jeu>`
```
soir.py :
 1 fraîcheur : dernier export par écran → confiance par domaine
 2 détecteurs : deltas → gold.signal
 3 évaluation des décisions échues → learn.outcome
 4 revues causales des matchs terminés depuis hier
 5 état du club : phase, objectif, probabilités, indices
 6 situations reconnues + agenda du soir → modules de décision, priorisés au temps disponible
 7 escalade : si un déclencheur est vrai → UN appel du raisonneur (paquet de 3 à 5 k jetons, JSON)
 8 écriture automatique dans learn.decision
 9 rendu par script, dans l'ordre de l'écran du jeu
10 vérification : chaque nom, chiffre, date existe dans le paquet ; aucune vente ou achat sans accord ; horizon d'action = aujourd'hui
11 ops.run : durée, appels au modèle, catégories rendues
semaine.py : recalcul de ref.* depuis résultats et kb ; réviseur (1 appel) ; diff proposé ; validation de l'utilisateur pour prix, objectifs, charte
```

### 5.7 Mémoire et apprentissage
`décision (prédiction) → résultat → comparaison → hypothèse confirmée ou contredite → ref.* mis à jour (versionné) → options de demain changées`. Évaluation automatique au début de `soir.py`. Promotion : indice dès 3, règle dès 5, retrait au 2e échec (déjà codé dans `garde.py`). Les 352 conseils migrés sans métrique sont réécrits avec une métrique ou classés « non évaluables ». Tes corrections deviennent des lignes `learn.user_preference` appliquées par le code (ex. « Hockey Nation : pas de finances en saison »).

### 5.8 Rendu et contrôle (légers)
Le tableau est **fabriqué** par script ; `forme.py` fabrique le format, ne rejette plus après coup. `verifier_rendu.py` contrôle noms, chiffres, dates. La police ne sert qu'aux achats, ventes et enchères au-dessus du seuil, plafonnée à 12 appels et 3 minutes (dépassement : brouillon avec « police partielle : manque X »). `CLAUDE.md` inviolable 3 : texte de l'Annexe C.

### 5.9 Connaissance : forums, chats, Discord
Principe : **code partout, modèle une fois par lot**.
| Étape | Fait par | Fréquence |
|---|---|---|
| 1. Collecte Discord | Export manuel (DiscordChatExporter) des seuls salons utiles (annonces, notes de version, stratégie, aide), incrémental depuis la dernière date | Hebdomadaire ; tout de suite après une mise à jour du jeu ; historique complet une seule fois |
| 1 bis. Forum, chat du jeu | Userscript passif : la page du fil que **tu ouvres** part en base | Quand tu lis ; un passage hebdomadaire sur les fils clés |
| 2. Filtre sans modèle | Code : salon utile, auteur officiel ou fiable (`kb.author_reliability`), chiffres, glossaire du jeu, réactions, doublons, regroupement question-réponse, récence | À chaque import |
| 3. Extraction | Un lot de 50 messages à l'agent `veille` en JSON strict, sur les seuls candidats, avec accord écrit sur le budget (`kb_estimer`) | Hebdomadaire ou au seuil de volume ; pas quotidien |
| 4. Confiance | `kb.recompute_confidence` + vérification par nos données (`kb_verify`) + résultats des hypothèses | Automatique |
| 5. Utilisation | `kb_search` par thème avec compteur, jamais l'historique brut | À chaque décision, sans agent |
| 6. Mise à jour du jeu | Message officiel avec « patch », « nerf », « buff », « changed » ou note de version : alerte, extraction immédiate, `ref.*` dépendantes « à revalider », confiance des anciennes affirmations abaissée | Dès l'import |
| 7. Ce que tu ne sais peut-être pas | Chaque semaine : affirmations `kb` de confiance élevée qui **ne figurent ni dans le profil, ni dans les skills, ni dans `ref.*`** (facteur caché dévoilé dans une discussion, retour d'un joueur expérimenté) | Hebdomadaire, dans le bilan de `semaine.py` |
Je ne conseille pas d'automatiser l'export Discord avec un jeton d'utilisateur (contraire aux conditions de Discord). Le volume réel après filtre est inconnu : `kb_estimer` le donne avant de fixer le budget.

### 5.10 Chaque jeu est spécifique
`docs/attentes/jeux/<jeu>.yaml` reçoit `capacites` (stade, personnel, infrastructure, académie, marché, finances en saison : oui ou non), `phases`, `fenetres`. Les situations sont **filtrées par capacité** : un jeu sans stade ne reçoit jamais de règle de stade. Le spécifique non sourcé est listé « à sourcer » avec l'écran à exporter. Les modules ne changent pas d'un jeu à l'autre ; les paramètres (`core.game_params`, `ref.*`, profil) changent.

### 5.11 Ajouter un club ou un jeu
**Un club dans un jeu déjà suivi** (moins d'une session) : une ligne dans `core.my_team`, une ligne de charte, ses exports dans `core.export_rule`. Les adaptateurs sont déjà par `team_id`. Preuve : `contrat_core.py` vert et un soir complet.
**Un jeu** (kit en 7 étapes, `nouveau_jeu.py` génère les squelettes) : 1 profil depuis `_modele.yaml` · 2 userscript depuis le gabarit · 3 adaptateur généré depuis le contrat de `core` · 4 lignes `export_rule`, `agenda_rule`, `alert_rule` · 5 inventaire des données · 6 valeurs de départ de `ref.*` depuis `kb` et les manuels · 7 trois soirs de test.
**Ce qui change d'un jeu à l'autre, et où ça vit.** Les jeux sont très différents ; le plan ne le nie pas. Les différences sont rangées dans des **données**, pas dans le moteur :

| Ce qui diffère | Exemples | Où ça vit | Effort réel pour un nouveau jeu |
|---|---|---|---|
| Calendrier | Heures de match, verrouillage des compositions, cycle d'entraînement, fenêtres de transferts, journées de paie | `rythme` du profil, `core.agenda_rule`, `core.season_phase` | Moyen : à sourcer jeu par jeu |
| Écrans et données | Quelles pages existent, quels champs, quels identifiants | Adaptateur `sql/adapters/<jeu>.sql`, `core.export_rule` | **Le plus gros** : c'est là que la différence entre jeux est la plus forte |
| Règles et paramètres | Points par victoire, relégation, barèmes d'entraînement, prix | `core.game_params`, graines de `ref.*` depuis `kb` | Moyen à fort : dépend de la connaissance disponible |
| Capacités | Stade, personnel, infrastructure, académie, marché | `capacites` du profil | Faible |
| Saisie et rendu | Ordre de l'écran, colonnes, compositions par quart-temps ou par lignes | `ecrans` du profil, rendu par script | Moyen |

Ce qui ne change **pas** : le moteur du soir, les modules, la revue de match, les tables `learn` et `kb`, le rendu, la mesure. « Facile » veut donc dire **« on ne réécrit pas le moteur »**, pas « sans effort » : le travail est surtout l'adaptateur, le calendrier et les règles du jeu. Le test de contrat (`contrat_core.py`) dit ce qui manque au lieu de laisser deviner.

**Familles.** Basket, hockey, hand, volley, football, football américain, baseball : modèle actuel de `core`. Tennis et auto : nouvelles entités (pilote, course, réglages de voiture ; joueur, tournoi) et nouveau module, famille par famille. Estimation indicative, non vérifiée : 1 à 2 sessions pour un jeu d'une famille traitée, 3 à 4 pour une nouvelle famille.

### 5.12 Tes listes « chose à faire » : chaque ligne reçoit une réponse
Tes listes (`docs/chose-a-faire.txt`, `docs/chose-a-DM.txt`, `docs/chose-a-faire-hardwood.txt`) sont la **spécification** du système. `docs/couverture/<jeu>.md` les suit déjà ligne par ligne (au 2026-11-05 : 262 ✅, 30 🔧, 7 ❌ sur les 6 jeux). Un ✅ y veut dire « un artefact existe ». Le plan ajoute ce qui manquait : **la ligne est répondue dans le rendu du soir quand elle est due** (mesure Q11).

| Type de ligne | Exemple | Répondue par |
|---|---|---|
| « Comprendre X » | effet de la forme, de la fatigue, du mentor, des badges | Une ligne `kb` ou `ref.*` avec source, confiance et `n_obs` ; « compris » = confiance au-dessus du seuil, sinon hypothèse à tester |
| « Connaître X » | solde, salaires, joueurs blessés | Une vue, lue chaque soir par le détecteur ou l'état du club |
| « Savoir si X » | joueur à vendre, stade à agrandir, bon à son poste | Une situation du catalogue (§ 5.3), avec sa preuve |
| « Choisir / Définir X » | caractéristique à entraîner, tactique, sponsor | Un module de décision (§ 5.4) |
| « Tous jeux » | ordre identique à l'écran, pas de « si » vague, une action claire, tester une nouveauté, dire ce qui manque | Rendu par script, `verifier_rendu.py`, quota d'exploration, § 5.2 bis |

**Contrôle par le code** : `pipelines/couverture_check.py` (dans `recette.py`) vérifie que chaque ligne de tes listes a une ligne dans `docs/couverture/<jeu>.md`, que chaque ✅ pointe vers un fichier, une vue ou une table qui existe, et, dès S7, que la ligne apparaît dans le rendu du soir quand son événement du calendrier est dû. Une ligne sans réponse fait échouer la recette.

**Les lignes ouvertes d'aujourd'hui, par cause** (identifiants de `docs/couverture`) :

| Cause | Lignes | Traitées par |
|---|---|---|
| Stats de la ligue, meilleurs joueurs des autres équipes | BasketVibe 7, Derby Manager 7, Hardwood 7, Six Zero League 62, Team Soccer 110 | Exports ciblés (S3b) puis vue par jeu (G1 à G5) |
| Migration `exports_nouvelles_cles` non appliquée | Derby Manager 177, Hardwood 177, Hockey Nation 177, Six Zero League 177, Team Soccer 177 | S3 (une migration) |
| Analyse match par match, apprendre de ses erreurs | Derby Manager 166, Hardwood 166, Team Soccer 163 | S8 |
| Projection de fin de saison et de finances | Derby Manager 21, Team Soccer 125 | S9 |
| Base « ce type vaut ce prix » | Six Zero League 86, Team Soccer 138 | S5, puis G |
| Réglages encore en hypothèse, à tester | BasketVibe 171, Derby Manager 32, 67, 171, Hardwood 20, 170, Hockey Nation 167, 171, Six Zero League 98, Team Soccer 171 | Expériences (S8) ; questions seulement si la recherche (§ 7 règle 10) ne trouve rien |
| Suspensions : aucune règle trouvée | BasketVibe 33, Derby Manager 35 | Recherche Discord (S3b), puis question |
| Donnée absente | BasketVibe 42 (export « Recent changes »), Hockey Nation H5 (lignes FRM et U21), Team Soccer 112 (badges), 117, 130 | Exports ciblés ; capture d'écran pour les badges |
| Calendrier et dépendances | Derby Manager 5, 173 | S3b |

## 6. Existant : gardé, réutilisé, retiré
| Existant | Sort |
|---|---|
| `bronze`, `silver`, `core`, adaptateurs, `sql.py`, sauvegardes | **Gardé** |
| `gold.agenda`, `core.agenda_rule`, `gold.exports_state`, `season_context`, `match_objective`, `club_strategy` | **Réutilisé** ; vues lentes matérialisées (S4) |
| `learn.*`, `decision.py`, `evaluer_decisions.py`, `garde.py` | **Réutilisé**, branché sur les modules |
| `kb.*`, `kb.py`, `kb_search`, `kb_ingest.py` | **Réutilisé** (valeurs de départ de `ref.*`) |
| `docs/conception-a-faire.md` §§ 1 à 3 | **Devient** `ref.training_focus`, `ref.price_benchmark` et détecteurs |
| Police obligatoire par type, lecture « en entier », couverture à 4 colonnes | **Retiré** |
| Agents `decideur`, `synthese`, chaîne d'agents par jeu | **Retirés** (raisonneur) |
| Règles de statu quo (« XI stable », « ne change pas un réglage qui marche ») | **Transformées** en option « garder » en concurrence |
| Règles S1 à S5 et hooks « à écrire » | **Non écrits** (couverts par `soir.py`) |
| Parité 7 jours | **Close sur l'état actuel** ; anciennes vues supprimées au fur et à mesure |

## 7. Règles d'exécution pour Claude
1. Un bloc par session, `/clear` après le commit. Design en `/model opus`, ensuite `/model sonnet`.
2. **Aucune case cochée sans preuve** : la sortie de la commande ou de la requête est collée dans le journal.
3. **Aucun autre plan, analyse ou rétro de plus de 30 lignes** : le journal suffit.
4. **Aucun nouveau hook.** Si un contrôle manque, c'est `soir.py` ou `verifier_rendu.py`.
5. `CLAUDE.md` : une seule modification, l'inviolable 3 (Annexe C). Rien d'autre sans accord écrit.
6. Jamais d'achat, de vente ni d'enchère. Jamais `drop policy` par le connecteur (N3).
7. Un commit par modification ; commit et push en deux appels (N2).
8. Chaque table nouvelle porte `source`, `confidence`, `n_obs` quand c'est un savoir.
9. Une donnée absente est dite « non mesurable » ; on ne l'invente pas.
10. **Chercher avant de demander.** Avant toute question à l'utilisateur (calendrier, règle, donnée), chercher dans cet ordre : profil du jeu et skills, `outputs/<jeu>/veille/connaissance.md`, `kb` (`kb.py`, `kb_search`), messages Discord, forum et chat en base, `docs/couverture/<jeu>.md`. La question cite où on a cherché (« cherché dans : … ») et ce qui manque exactement.
11. **Les preuves doivent être rejouables** : le journal contient la commande ou la requête exacte et sa sortie, pour qu'un audit externe (§ 8 bis P7) puisse les refaire. Un test de la phase P dont le critère n'est pas écrit avant le lancement est invalide.

## 8. Plan d'exécution par sessions
Les durées sont indicatives, non mesurées. Chaque session doit laisser quelque chose de visible le soir.

| Session | Modèle | Contenu | Preuve de fin | Ce que tu vois le soir |
|---|---|---|---|---|
| **S0 — Remise à plat** (~1 h) | Sonnet | Les 5 branches distantes autres que `main` sont à 0 commit en avance : les supprimer **avec ton accord** ; `pip install -r requirements.txt` au démarrage cloud (règle N1) ; `CLAUDE.md` inviolable 3 (Annexe C) ; journal v3 créé, `plan-reprise.md` marqué « remplacé » | `git branch -r` ne liste que `main` ; `sql.py` marche dans une session cloud neuve | Rien de changé, base propre |
| **S1 — Désarmer le contrôle** (1 session) | Opus | `police.py` H1 et H2 limités aux achats, ventes, enchères au-dessus du seuil ; agent `police` plafonné (12 appels, 3 min, deltas seulement) ; `controle.py` f limité à la colonne Action, bloc « Si » et « Plan de saison » autorisés ; `forme.py` accepte le bloc « Si » ; `deja-fait` chargé avant le plan ; journal manuel de durée ; tests mis à jour | `test_police`, `test_forme`, `test_controle` verts ; un tour réel BasketVibe de moins de 15 minutes, 0 police hors transfert | Soirées plus courtes dès ce soir |
| **S2 — Charte et capacités** (1 session) | Opus | Migration `sql/core/013` : colonnes de charte (Annexe A), `core.my_team`, règle « former » basée sur `minutes_jeunes_si_rien_a_jouer` ; 11 lignes de l'Annexe A (identifiants lus dans les adaptateurs, correspondance Derby Manager montrée avant insertion) ; `capacites`, `phases` dans les 6 profils (« à sourcer » si inconnu) | `select count(*) from core.club_strategy` = 11 ; test : un titre acquis sur BasketVibe produit l'objectif « former » dans `gold.match_objective` | Charte lue par le système |
| **S3 — Inventaire des données** (1 session) | Sonnet (medium) | Part de `docs/couverture/<jeu>.md` (ne repart pas de zéro) ; ajoute `pipelines/couverture_check.py` ; migration `exports_nouvelles_cles` appliquée (5 jeux) ; par jeu × domaine (match, entraînement, marché, jeunes, finances, stade, personnel, infrastructure) : exploitable / partiel / absent ; `ops.data_inventory` ; `docs/couverture/donnees-exploitables.md` ; liste des écrans à exporter, par jeu (provisoire : la liste ciblée sortira de S3b) | Tableau 6 jeux × 8 domaines complet ; liste d'exports remise à l'utilisateur | **Ta liste d'exports** (Hardwood : Recruiting, Development, Conference, Rankings, Statistics ; BasketVibe : Personnel ; autres selon l'inventaire) |
| **S3b — Calendrier de chaque jeu** (2 sessions : trois jeux chacune) | Opus | `core.game_event` (§ 5.2 bis) ; reprise du `rythme` des profils, des règles d'agenda existantes (BasketVibe, Team Soccer, Hockey Nation) et des skills ; migration de l'ancienne vue `gold.sz_agenda` (Six Zero League) ; **Derby Manager et Hardwood construits depuis les skills, la mémoire et tes réponses** ; pour chaque événement : heure, effet, écrans modifiés, action, verrou, source ; `agenda_rule` lue depuis `game_event` ; `gold.exports_needed` ; ordre de recherche avant toute question (règle 10 du § 7) ; liste des « à sourcer », avec où on a cherché, remise à l'utilisateur | Pour chaque jeu : tous les événements du `rythme` du profil sont présents ; rejoué sur un jour passé, `gold.exports_needed` donne une liste cohérente et ne redemande aucun écran frais ; chaque « à sourcer » est listé | Une liste d'exports **courte et justifiée**, et des questions précises sur le calendrier pour les trous |
| **S4 — Vues rapides** (1 session) | Opus | `core.*`, `season_context`, `match_objective`, `daily_alerts` matérialisés, rafraîchis après chaque arrivée de page ; taille de la base contre le quota gratuit | Les 3 vues répondent en moins de 2 s ; 0 timeout dans un dossier de test | Plus d'erreurs de délai |
| **P — Preuves P1 à P4** (1 à 2 sessions, juste après S1) | Opus | `pipelines/preuves.py` : les quatre tests du § 8 bis en rejeu sur l'historique, **sur les 6 jeux**, avec un statut ✅ ❌ ⏳ ⛔ par jeu et par preuve ; résultats chiffrés dans `docs/refonte-v3/preuves.md` | Les quatre résultats écrits avec chiffres ; pour chaque échec, le repli appliqué au plan | **La décision d'élargir ou de réduire S5 à S9**, sur du mesuré |
| **S5 — Références BasketVibe et rejeu du passé** (1 à 2 sessions) | Opus | Schéma `ref` ; `training_focus`, `player_score`, `price_benchmark`, `team_need` (graines `kb` + historique) ; **rejeu sur des jours passés** (`core.player_daily_asof`) : les tables auraient-elles bien conseillé ? ; tableau de validation pour toi | Rapport de rejeu ; tables avec `n_obs` et confiance ; **tu valides en tableau** | Un tableau à lire et corriger |
| **S6 — Détecteurs, état du club, situations** (1 à 2 sessions) | Opus | Détecteurs du § 5.2 ; `core.club_state` (indices) ; `core.season_phase` ; `core.situation_rule` (14 situations du § 5.3 pour BasketVibe) ; `learn.transfer_ledger` | `gold.signal` non vide sur les données du jour ; un `club_state` par soir ; chaque situation du catalogue testée sur un cas passé | Signaux et indices de santé |
| **S7 — Modules et `soir.py` v0, sans modèle** (2 sessions) | Opus | Modules entraînement, transferts, composition, stade, finances ; `soir.py` v0 ; `ops.run` ; rendu par script ; `verifier_rendu.py` ; quota d'exploration | **Mode ombre les 5 premiers soirs** (`soir.py` en parallèle de ton déroulé habituel, comparaison à l'aveugle : tu préfères le script ou c'est équivalent 4 soirs sur 5, § 8 bis P5), puis **7 soirs d'affilée sur BasketVibe** : au moins 4 catégories, moins de 10 minutes, 0 agent, `learn.decision` qui augmente | **Le plan du soir complet, sans agent** |
| **T — Recette v3 et rétro automatique** (1 session, après S7) | Opus | `pipelines/recette_soir.py` ; `pipelines/retro_auto.py` ; champ `rendu_cle` et échéance ajoutés aux Qn des 6 fichiers `docs/attentes/tests/<jeu>.yaml` (les 814 lignes sont conservées) ; appel depuis `soir.py` | Un soir réel produit la grille ✅ ❌ ⏳ ⛔ et une rétro de 30 lignes au plus ; **un échec injecté** (une catégorie due volontairement omise) est détecté ; la même omission deux soirs est marquée récidive | Une rétro automatique chaque soir, plus de rétro à écrire |
| **S8 — Analyse causale** (2 sessions) | Opus | `ref.expected_result`, `learn.match_review`, `learn.hypothesis`, `learn.experiment`, module tactique, échelle de diagnostic | Après 5 matchs : chaque défaite a une revue avec facteurs ; une hypothèse suivie avec `n_obs` ; un test nommé en cours | « Pourquoi on a perdu » |
| **S9 — Probabilités de saison et besoin de transfert** (1 session) | Opus | Simulation depuis `expected_result` ; objectif du match lié aux probabilités ; module transfert sur « structure » avec poste, note, prix | Probabilités affichées avec leur fiabilité ; un besoin de transfert chiffré sur un cas passé | « J20/25, 97 % de titre → jeunes » |
| **S10 — Raisonneur et réviseur** (1 à 2 sessions) | Opus | Paquet de contexte, JSON de sortie, déclencheurs du § 4.3 ; `semaine.py` avec diff | Un soir de défaite : 1 appel, récit rangé en base ; un lundi : diff de `ref.*` produit | Bilan hebdomadaire |
| **S11 — Boucle fermée** (en continu) | Opus puis Sonnet | Évaluation au démarrage ; conseils migrés réécrits ; effet des leçons dans les options ; `learn.user_preference` | `learn.outcome` supérieur à 0 sous 3 jours ; une ligne de `ref.*` change à cause d'un résultat | Le système change d'avis sur preuve |
| **K — Connaissance** (1 à 2 sessions, peut démarrer après S2) | Opus (design) puis Sonnet | Import des Discord de Derby Manager et de Hardwood dans `bronze.discord_messages` (lus le 2026-10-30 mais absents de la base) ; reprise du backfill BasketVibe (lots 4 à 9) et Hockey Nation (49 761 messages, environ 1,5 M de jetons : **accord écrit sur le budget requis**) ; filtre en code, `kb.author_reliability`, détection de mise à jour, lot hebdomadaire | Un import réel réduit les messages à extraire (chiffre mesuré) ; une mise à jour simulée marque des `ref.*` « à revalider » | Moins de bruit, alerte de patch |
| **G1 à G5 — Extension, un jeu par session** | Opus puis Sonnet | Ordre : Team Soccer (2 équipes), Hockey Nation (4 équipes, conflit de promotion, scouting, sans finances ni ventes), Six Zero League, Derby Manager (QOS maintien et jeunes, Marmandes titre court terme), Hardwood (recrutement, sans ventes) ; profil, graines `ref.*`, situations filtrées par capacité | Même preuve que S7 et S8 pour chaque jeu | Les 6 jeux au même niveau |
| **N — Nouveaux jeux** | Opus | `nouveau_jeu.py` et kit du § 5.11 | Trois soirs de test sur un jeu pilote de la famille | Un jeu de plus |

## 8 bis. Phase P — preuves avant de construire

Principe : chaque incertitude technique du plan est transformée en **test sur ton historique réel**, avec un critère de réussite écrit **avant** de lancer le test, et un plan de repli. Ces tests ne construisent rien de durable : ce sont des analyses en rejeu (`core.player_daily_asof`, historique des matchs, des enchères, de l'entraînement). Résultats chiffrés dans `docs/refonte-v3/preuves.md`. **Si un test échoue, on applique le repli au plan avant de continuer** ; on ne construit pas sur un pari.

| # | Question | Méthode (en rejeu, sans regarder l'avenir) | Réussite | Si échec : repli |
|---|---|---|---|---|
| P1 | Peut-on estimer un **résultat attendu** assez bien pour dire « défaite attendue » ? | Pour chaque match passé de Hockey Nation (247), BasketVibe (70) et Team Soccer (57) : force = points par match avant le match (classement) et, si disponible, notes de l'effectif. Prédire V/N/D avec un modèle simple appris sur les matchs précédents seulement (glissant) ; comparer à une base naïve (taux de victoire à domicile) sur la perte logarithmique et le taux de réussite | Meilleur que la base naïve sur au moins 2 jeux sur 3 | Aucun verdict « attendu / sous-performance » : la revue causale se limite à la disponibilité, à la tactique et aux joueurs ; « attendu » reste « non mesurable » |
| P2 | Peut-on prévoir un **gain d'entraînement** par poste, âge et focus ? | BasketVibe : gains hebdomadaires de compétences (`bv_skill_progress_weekly`, `bv_training_gains_exact`). Prédire la semaine suivante depuis les semaines précédentes ; comparer au gain moyen naïf | Erreur absolue moyenne plus faible que la base naïve | Le module entraînement se limite au contrôle des écarts (focus saisi contre `ref.training_focus`) et aux **tests nommés** ; aucun « gain attendu » affiché |
| P3 | La **table de prix** prédit-elle le prix réglé ? | BasketVibe (952 enchères vues) et Team Soccer (annonces) : pour chaque annonce passée, prédire le prix final avec les seules annonces antérieures ; comparer à la médiane globale | Erreur plus faible que la médiane globale **et** l'intervalle p25–p75 contient le prix final dans 40 à 60 % des cas (50 % attendu) | `ref.price_benchmark` marquée « indicatif », pas d'enchère maximale calculée ; seulement des alertes « sous la médiane » |
| P4 | Le moteur peut-il **détecter un vrai effet** (tactique, entraînement) avec si peu de matchs, sans fausses alertes ? | Simulation : injecter dans l'historique un effet connu (réglage qui ajoute un écart de buts fixé) et un réglage sans effet ; rejouer le suivi d'hypothèses sur des saisons simulées au rythme réel de chaque jeu | Détecte l'effet injecté dans au moins 80 % des saisons simulées ; fausses alertes sous 10 % | On relève le seuil (indice dès 5, règle dès 8) ; le test donne **le nombre de matchs réellement nécessaires par jeu**, affiché au lieu de promettre plus |
| P5 | Un **plan sans agent** est-il aussi bon que celui d'aujourd'hui ? | Mode ombre en S7 : `soir.py` v0 tourne en parallèle de ton déroulé habituel pendant 5 soirs ; comparaison à l'aveugle | Tu préfères le plan du script ou tu le juges équivalent au moins 4 soirs sur 5, et toutes les catégories dues sont rendues | Retour à l'agent pour les catégories où le script est plus pauvre ; le script garde ce qu'il fait mieux |
| P6 | La vue **exports ciblés** sort-elle la bonne liste ? | En S3b : rejouer le soir du 04/11 avec une vérité connue : Hardwood n'avait que Schedule, game_id et Roster | Liste = exactement Recruiting, Development, Conference, Rankings, Statistics ; aucun écran frais redemandé pour BasketVibe | Ajustement des événements du calendrier jusqu'à la bonne liste |
| P7 | Les preuves des sessions sont-elles **vraies** ? | **Audit externe** : après S1, S4, S7 et S8, tu me renvoies le dépôt ; je recontrôle les preuves du journal contre les fichiers, les commits et les journaux collés | Chaque case cochée a une preuve vérifiable | Case décochée, session reprise |
| P8 | Mes **estimations** de durée tiennent-elles ? | Mesurer la durée réelle de S0 et S1, puis recalibrer les estimations du § 8 | Écart inférieur à 50 % | Le plan est ré-estimé avec les durées mesurées |

### Les tests tournent sur les 6 jeux, avec un statut honnête
`pipelines/preuves.py <jeu>` ou `--tous` exécute P1 à P4 sur chaque jeu et donne **un statut par jeu et par preuve** :
- ✅ **passe** : critère atteint ;
- ❌ **échoue** : le repli du tableau est appliqué et noté ;
- ⏳ **pas assez de données** : nombre d'observations actuel, date estimée pour atteindre le seuil, repli provisoire ;
- ⛔ **sans objet** : capacité absente (Hardwood n'a ni transferts ni finances : P3 ⛔).

**« Tout passe » veut dire** : pour chaque jeu, aucune preuve sans statut, aucun ❌ sans repli appliqué, et le **mode du moteur** de ce jeu (complet ou réduit) correspond aux statuts. Un jeu avec un ⏳ tourne en mode réduit, affiché comme tel, jusqu'à ce que le test passe. Je ne peux pas promettre ✅ partout : certains jeux ont peu d'historique, et le test le dira au lieu de le cacher.

### Recette v3 : tests de soirée et rétro automatique
**Ce qui existe déjà et que tu avais construit** : `docs/attentes/tests/<jeu>.yaml` (6 fichiers, 814 lignes : pour chaque jeu, « nouvelle saison » et « chaque jour » Q1 à Qn, avec critère, vues et lignes de `docs/couverture` couvertes) et `pipelines/recette.py`. **Limites constatées dans le dépôt** :
1. `recette.py` contrôle la **structure** (fichiers présents, vues citées existantes dans `sql/`, lignes de couverture rattachées à un test) ;
2. avec `--reponse`, elle contrôle le **texte** d'une réponse (mots interdits, pastilles, horizon), pas que chaque Qn est rendu avec du contenu ;
3. les critères des Qn sont écrits en prose, donc non vérifiables par le code ;
4. `--reponse` n'est branchée à aucun hook ni à la routine du soir (seul `recette.py --tous` figure dans `CLAUDE.md`).
Résultat : une recette qui peut rester verte pendant qu'un soir ne rend que des compositions (le 04/11).

**Ce que fait la v3** :
1. **On garde les 814 lignes** : chaque Qn reçoit un champ `rendu_cle` (la clé de la sortie structurée de `soir.py` qui doit exister et être non vide) et une condition d'échéance tirée du calendrier (`core.game_event`) ;
2. `pipelines/recette_soir.py <jeu>` compare, pour le soir, les Qn **dus** aux clés réellement rendues, et vérifie : durée, appels au modèle, export demandé en tête, « inchangé » sans preuve ni test nommé, composition recopiée plusieurs jours ;
3. elle est appelée par `soir.py` à la fin (pas un hook : un appel du script) ;
4. `pipelines/retro_auto.py` écrit `outputs/retro/AAAA-MM-JJ-recette.md` : par jeu ✅ ❌ ⏳ ⛔ ; pour chaque échec, une **cause classée** (donnée absente · règle absente · bug de module · export manquant · limite du modèle), une **correction proposée** (ligne de `ref.*`, règle de situation, correctif de code) et la **récidive** (même échec deux soirs : `learn.error_occurrence`, qui existe déjà) ;
5. la rétro fait 30 lignes au plus ; tu ne l'écris pas, tu la lis ;
6. **un jeu entre « en service » quand ses tests du soir passent 7 soirs de suite**, ou que chaque échec restant a un statut expliqué.

P1 à P4 se lancent juste après S1 (ils n'ont besoin que de l'historique) et décident de la taille de S5 à S9. P5 est la porte de sortie de S7, P6 celle de S3b, P7 et P8 sont continus.

**Ce que ça change pour ma confiance** : sur P1 à P4, je ne sais pas aujourd'hui si ça passera. Après ces tests, je saurai exactement ce que le moteur sait faire sur tes jeux, ce qu'il ne sait pas, et le plan sera ajusté en conséquence. Je ne promettrai alors que ce qui est mesuré.

## 9. Ce que tu fais chaque soir, selon l'étape
| Étape | Toi | Tu demandes |
|---|---|---|
| Avant S7 (maintenant) | Exports des jeux, puis tu joues comme aujourd'hui | « exports faits » ; tu signales ce qui cloche avec « Erreur : … preuve : … » |
| Après S1 | Idem, avec moins d'attente | — |
| Après S5 | Une fois : valider le tableau des références | « Voilà mes corrections » |
| Après S7 (BasketVibe) | Exports, puis lire le plan du soir, saisir en jeu dans l'ordre de l'écran | « exports faits » ; « Fait : X » ; « Rétro » si quelque chose t'a gêné |
| Chaque lundi, après S10 | Lire le bilan et valider les gros changements | « Bilan de la semaine » |
| Chaque semaine | Export Discord incrémental ; la sauvegarde du dimanche 21 h doit avoir tourné (PC allumé) | « kb : lot suivant » (après accord sur le budget) |

## 10. Risques et hypothèses non vérifiées
1. **Peu d'observations** : les hypothèses mûrissent lentement ; la confiance est affichée, pas supposée.
2. **Données inégales selon les jeux** : statistiques de match connues pour BasketVibe et Team Soccer seulement. Un jeu pauvre en données aura une analyse causale réduite (S3 le dit avant d'investir).
3. **Tables de référence imparfaites au départ** : tracées, corrigibles par toi dans un tableau, rejouées sur le passé avant mise en service.
4. **`ref.expected_result` fragile au début** : verdict « sous-performance » à faible confiance tant que la calibration est courte.
5. **Sur-ajustement** : une règle tirée de 5 matchs peut être du hasard ; le réviseur voit `n_obs` et la contre-épreuve.
6. **Quota Supabase gratuit** : les tables matérialisées doivent être surveillées (S4).
7. **Les modules tactique et transferts sont le point dur** : d'où un jeu pilote, avec preuve, avant extension.
8. **Les réponses de charte ont deux points ouverts** (priorité de promotion à Hockey Nation, identifiants Derby Manager) : § 3.
9. **Ce plan n'était pas testé.** Les risques techniques majeurs sont maintenant testés avant construction (phase P, § 8 bis), chacun avec un critère de réussite et un repli. Critère d'arrêt : si S7 ne donne pas 7 soirs conformes, on corrige S7 avant S8.
10. **Mon propre biais** : j'ai déjà écrit un plan qui privilégiait les contrôles et le coût. Le contrôle qualité de ce plan est donc la mesure Q1 à Q10 sur de vrais soirs, pas sa cohérence sur le papier.

## Annexe A — Charte : colonnes et lignes à insérer (S2)

Colonnes ajoutées (migration `sql/core/013`, rien n'est supprimé) :
```sql
alter table core.club_strategy
  add column if not exists objectif_saison text check (objectif_saison in ('titre','podium','milieu','maintien','developpement')),
  add column if not exists minutes_jeunes_si_rien_a_jouer boolean,          -- null = non répondu ou sans objet : règle « former » inactive
  add column if not exists tests_en_ligue boolean default false,
  add column if not exists max_tests_simultanes int default 1,
  add column if not exists budget_transferts_net_saison numeric,
  add column if not exists perte_transferts_toleree_4sem numeric,
  add column if not exists seuil_gros_montant_pct numeric,
  add column if not exists posture_infrastructure text check (posture_infrastructure in ('investir','maintenir','ne_pas_toucher')),
  add column if not exists posture_personnel text check (posture_personnel in ('investir','maintenir','ne_pas_toucher')),
  add column if not exists temps_soir_min int,
  add column if not exists intouchables text[],
  add column if not exists a_vendre text[],
  add column if not exists domaines_exclus text[],
  add column if not exists actions_exclues text[];

create table if not exists core.my_team (
  game text not null, team_id text not null, nom text, niveau text, groupe text,
  primary key (game, team_id)
);
```
La règle `titre_former` et `rien_former` de `core.objective_rule` passe de `charte_horizons` à `minutes_jeunes_si_rien_a_jouer is true`.

Lignes (les `team_id` sont lus dans `core.player_daily` avant insertion ; `valide_le = '2026-11-05'`) :

| game | équipe | objectif_saison | horizon | minutes_jeunes | vendre_pour_profit | domaines_exclus | actions_exclues | note |
|---|---|---|---|---|---|---|---|---|
| basketvibe | Chomelix | titre | 3_saisons | true | true | — | — | « la meilleure équipe » |
| sixzeroleague | (mon équipe) | titre | long_terme | true | true | — | — | |
| hardwood | (mon équipe) | titre | long_terme | true | false | — | vente | recrutement seulement |
| teamsoccer | équipe 1 | titre | 3_saisons | true | true | — | — | « fais tourner les jeunes » (2026-11-05) |
| teamsoccer | équipe 2 | titre | 3_saisons | true | true | — | — | « fais tourner les jeunes » (2026-11-05) |
| hockeynation | PRO, FRM, U21, U17 (4 lignes, `groupe` commun) | titre | 3_saisons | **null** (sans objet) | false | finances, plafond salarial, staff d'entraîneurs | vente | échanges à voir plus tard ; priorité de promotion : question ouverte |
| derbymanager | QOS | maintien | long_terme | true | true | — | — | « les meilleurs jeunes » |
| derbymanager | Marmandes | titre | maintenant | true | true | — | — | « les meilleurs joueurs » |

## Annexe B — Esquisses de tables (non exécutées, à adapter à `core`)
```sql
create table ref.training_focus (
  game text, position text, age_min int, age_max int, rating_min int, rating_max int,
  attribute text, priority int, intensity text,
  source text, confidence numeric, n_obs int, valid_from date, valid_to date, version int);
create table ref.price_benchmark (
  game text, position text, age_band text, rating_band text,
  p25 numeric, median numeric, p75 numeric, settled_share numeric, n_obs int, valid_from date, valid_to date);
create table ref.tactic_effect (
  game text, setting text, value text, opp_strength text, venue text, competition_kind text,
  wins int, draws int, losses int, avg_goal_diff numeric, confidence numeric, valid_from date);
create table gold.signal (
  game text, domain text, entity_id text, severity text, evidence jsonb,
  suggested_action text, fingerprint text, status text, seen_on date);
create table core.club_state (
  game text, team_id text, day date, phase text, objectif text, probas jsonb, indices jsonb, causes jsonb,
  primary key (game, team_id, day));
create table core.situation_rule (
  rule_id text primary key, game text, condition_sql text, diagnostic text, module text,
  priorite int, capacite_requise text, source text);
create table learn.match_review (
  game text, fixture_id text, expected jsonb, availability jsonb, tactic jsonb,
  player_deltas jsonb, team_stats jsonb, verdict text, dominant_factors text[], reviewed_on date);
create table learn.hypothesis (
  id bigint generated always as identity, game text, statement text, context jsonb,
  n_for int, n_against int, status text, created_on date);
create table learn.experiment (
  id bigint generated always as identity, game text, hypothesis_id bigint, variable text,
  variant_a text, variant_b text, metric text, starts_on date, ends_on date, status text);
create table learn.transfer_ledger (
  game text, team_id text, player_id text, bought_on date, price numeric, sold_on date, sold_price numeric,
  perf_after_n jsonb, roi numeric);
create table ops.run (
  game text, run_on date, started_at timestamptz, seconds int,
  llm_calls int, categories_rendered text[], escalations text[]);
```

## Annexe C — Texte de `CLAUDE.md`, inviolable 3 (accord de l'utilisateur du 2026-11-05)
> 3. **Horizon d'action = aujourd'hui.** L'utilisateur n'agit que le soir même : aucune *action* n'est reportée (« demain », « le 29 », « après le prochain match »). Le *raisonnement* peut porter sur la saison (objectif, « si », projection financière) à condition de finir par l'action d'aujourd'hui. Un match de demain se prépare aujourd'hui. Exception : les transferts (cibles, enchères) se disent toujours.

## Annexe D — Prompt de lancement pour Claude
> Lis `docs/refonte-v3/plan.md` (§ 7 d'abord) et `docs/refonte-v3/journal.md`. Exécute **uniquement** le bloc de session `S<n>` du § 8 que je t'indique, dans l'ordre. Avant de commencer, annonce en 5 lignes : ce que tu vas faire, les fichiers touchés, la preuve de fin. À la fin : colle la preuve dans le journal, commite, pousse (en deux appels), dis `/clear`. Ne rédige aucun autre plan ni rétro de plus de 30 lignes. N'ajoute aucun hook. Si une donnée manque, dis « non mesurable » ; n'invente pas.
