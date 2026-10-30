---
name: hardwood-regles
description: Règles Hardwood (Online College Basketball) — pyramide de conférences, montée/descente, calendrier (exhibitions, 10 hors conférence, 30 de conférence, playoffs, tournois D1/D2/D3, invitational), effectif (13 bourses + walk-ons), compétences 0-20, Skill Index, potentiel, valeurs affichées ±20 %, coaching deux fois par semaine, entraînement additionnel, expérience, fatigue, Overwork, blessures, redshirt, coachs (head + 3 assistants), RPI/TPI/prestige, pas de finances ni de transferts. À charger pour toute question de règle, de calendrier, d'évaluation d'un joueur ou de coach.
---

# Hardwood — règles générales

Sources : **[R:Rubrique]** = manuel officiel `onlinecollegebasketball.org/rules`, capturé le 2026-10-30 (`bronze.raw_pages` page_type `rules`). **[D]** = Discord, veille du 2026-10-30 (`outputs/hardwood/veille/`, statut entre parenthèses). **[A]** = document d'aide de l'utilisateur (`data/manual/hardwoord/Aide docs.txt`, 2026-10-30 : tableaux épinglés sur Discord et conseils d'un ancien). **[E]** = constaté dans nos exports. **[H]** = hypothèse à confirmer. **[U]** = règle de l'utilisateur.

## Structure [R:Conference Structure, Conference, Tournaments]
- Pyramide : 1 conférence de niveau I, 2 de niveau II, 4 de niveau III, etc. ; 16 équipes par conférence. Division 1 = niveaux I à IV, Division 2 = niveau V, Division 3 = niveau VI.
- **Les 3 premiers montent, les 6 derniers descendent**, sur le **classement de conférence de la saison régulière** ; égalité départagée à la différence de points.
- Nous : Eureka Red Devils (#940), conférence **VI.26 (Division 3)**, descendue le 03/09/2054 [E].

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

## Effectif [R:Team Roster, Walk-Ons]
- **13 joueurs boursiers au maximum**, plus des walk-ons (non boursiers) qu'on ne choisit pas. 4 ans d'éligibilité, plus 1 an de redshirt possible.
- **Walk-ons [U, 2026-10-30]** : jamais exportés (pas de page joueur) ni proposés dans le depth chart ; leurs minutes freinent le développement des jeunes boursiers [D (stromstar 2025-02)]. Le roster suffit pour les voir ; `gold.hw_depth_suggest.walk_on_meilleur` signale seulement un walk-on nettement meilleur qu'un boursier.
- Inactif plus de 35 jours = équipe perdue [R:Activation].

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

## Entraînement [R:Player Development]
- Un **focus principal et un focus secondaire** reçoivent plus de coaching à chaque mise à jour. S'y ajoutent **8 entraînements additionnels** au petit effet : Post Moves, Shooting, Foul Shooting, Ball Handling & Passing, Video / Film Work (IQ), Defense, Fitness (stamina), Strength Training. Sans effet sur les recrues déjà engagées.
- L'essentiel de la progression vient du coaching général et du poste joué en match.

## Fatigue, Overwork, blessures [R:Fatigue, Overwork, Injuries]
- Fatigue en match selon les minutes ; une stamina haute la réduit. Elle touche tout le jeu et l'effort défensif en fin de match. Niveaux affichés dans le box score : -, Lght, Mod, Hvy [E].
- **Overwork** : un joueur proche de **40 min par match** ou qui joue souvent fatigué **perd de l'efficacité jusqu'à la fin de la saison**. La feuille de match indique « Overworked » [E].
- Fatigue [A] : elle baisse la qualité du joueur pendant le match et augmente le risque de blessure, mais **les joueurs sont reposés entre deux matchs** : inutile de réduire ses minutes au match suivant. Le risque s'accumule seulement si on le fatigue sans cesse.
- Tout joueur qui joue peut se blesser, et la fatigue augmente le risque [D (confirmé Steve)]. Un blessé est noté « +N » jours [E]. Aucune suspension en cours de saison [D (en doute : rien trouvé)].

## Redshirt [R:Red Shirting]
- Joueur boursier et non senior, **5 matchs au plus** (hors conférence, conférence, playoffs, tournoi ; exhibitions et invitational exclus), minutes illimitées dans ces 5 matchs. Un seul redshirt par carrière.
- Il faut **cocher la case Red Shirt dans Game Management avant la fin de saison**. Cochée tôt, le moteur limite le joueur à 5 matchs. Le plus sûr : cocher, retirer le joueur du depth chart et des Game Plans, Playing Time à 0.
- Le redshirt ne ralentit pas la progression ; il coûte de l'intérêt chez les recrues 4-5 étoiles [R:Recruiting Success Factors] [D (confirmé)].
- [A] Le redshirt prend effet **après** la saison (case laissée cochée → RS FR la saison suivante) ; plusieurs joueurs peuvent être redshirtés. Dans `silver.hw_management.red_shirt` : « oui » = cochée, « non » = possible, « impossible » = case grisée (senior, déjà RS ou plus de 5 matchs).

## Coachs [R:Head Coaches, Assistant Coaches]
- Notes : Offense, Defense, Game Tactics (surtout en fin de match), Recruiting, Motivation (momentum), Player Development. Salaire minimum 500 000 $. Déclin du head coach entre 55 et 70 ans.
- **3 assistants** qui renforcent le head coach selon leurs points forts (pas une simple moyenne). Un assistant part vers un poste de head coach au-delà de **1 M$ de salaire ou 50 ans**.
- **Un recrutement de coach par jour réel.** Les assistants ne se remplacent qu'**avant la saison de conférence ou après la saison**.
- **Renvoyer le head coach fait chuter l'intérêt des recrues en cours** (pas celles déjà engagées). Changer d'assistant a un petit effet, positif si le nouveau recrute mieux.
- Nous [E] : head coach Darius McNair, 67 ans (âge de déclin), Off 10, Def 13, Tac 0, Dev 11, Mot 11, **Rec 3**, 2,6 M$.
- **Lire la page d'un coach (phrases → note) [A]** : Offense 14+ good, 11-13 above average, 10 rien, 0-9 below average · Defense 15+ good, 11-14 above average, 10 rien, 0-9 below average · Tactics 15+ « excellent X's and O's » (pas toujours affiché à 15), 12-14 good, 0-11 rien · Development 15+ excellent teacher, 12-14 good teacher, 9-11 rien, 0-8 poor · Motivation 15+ great, 12-14 good, 0-11 rien · Recruiting (avant l'effet de l'âge) 15+ excellent, 13-14 good, 11-12 decent, 5-10 rien, 0-9 poor (chevauchement : un 9 peut porter « poor »).
- Tableau prêt : `gold.hw_coach_board` (notre staff contre les 5 meilleurs libres de moins de 55 ans : total, Rec, Dev).

## Classements [R:Ratings]
- Rating : force estimée selon les victoires. **RPI** : bilan + force du calendrier, il sélectionne le tournoi. SOS : force du calendrier. **TPI** : moyenne pondérée des SI des 10 meilleurs joueurs (les 5 premiers comptent double). Prestige : titres et matchs de tournoi, bonus de recrutement. Fan Mood : affluence. Alumni Mood : pèse sur le renvoi du coach par les bots.

## Ce qui reste inconnu
Formule du RPI, ampleur exacte du malus hors poste, bonus du terrain, effet chiffré de la fatigue et de l'Overwork, formule des assistants (« Game Engine Algorithm Discussion : To Do » dans le manuel).
