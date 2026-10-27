---
name: teamsoccer-joueurs
description: Règles Team Soccer (football, teamsoccer.org) sur les joueurs — 10 compétences, sous-rôles (GB, DC, LAT, WB, MD, MC, ML, MO, AC, DR) et leur calcul, OVR pondéré, compétences clés par poste, Forme (0–100) et son effet en match, endurance et fatigue en match, talents spéciaux et météo, blessures, cartons et suspensions, âge et vieillissement, valeur et salaire, effectif de 16 à 24. À charger pour évaluer un joueur, choisir son poste, expliquer une performance, gérer la forme, les blessures ou les suspensions.
---

# Team Soccer — joueurs

Sources : **[G:Rubrique]** = guide officiel (page Aide, version française, captée le 2026-10-19 ; nouvelle page Aide annoncée le 2026-09-20). **[F:date auteur]** = forum global anglais ; seuls les messages des administrateurs (Admin-Dev = développeur, Admin-PIPO68) valent règle, et le forum dit lui-même que seuls le forum global et les annonces sont fiables [F:2026-10-11 PIPO68]. **[P:Page]** = texte d'une page du jeu capté le 2026-10-19. **[Obs]** = nos données. Tout ce qui date d'avant le 2026-07-07 vient de la BETA (remise à zéro complète ce jour-là) : à manier avec prudence. Voir aussi teamsoccer-communaute.

## Les 10 compétences [G:Commencer à jouer] [F:2026-08-25 Admin-Dev]
| Nom dans le jeu (FR) | API | Rôle dans le moteur [G:Moteur de match] |
|---|---|---|
| Gardien de but | `goalkeeper` | Duel de tir face à la Finition |
| Défense | `defense` | Duel contre la Conduite de l'adversaire |
| Contrôle (du ballon) | `ball_control` | Réception d'une passe, duels au pied |
| Passe | `passing` | Facilité de contrôle pour le receveur |
| Centres | `crosses` | Centres devant le but |
| Conduite (ex-« Dribble », renommée le 2026-08-27, même effet) | `dribbling` | Duel contre la Défense, avancer avec le ballon |
| Coup de tête | `heading` | Duels aériens |
| Définition / Finition | `finishing` | Tir face au Gardien |
| Endurance | `stamina` | Physique : baisse de rendement au fil du match |
| Vitesse | `pace` | Physique : arriver le premier sur un ballon, peut renverser un duel |
- Compétences de 0 à 100 avec décimales ; on peut toutes les monter à 100 [F:2026-05-03 Admin-Dev]. L'OVR n'utilise que la **partie entière** : les décimales (+0,X / −0,X) ne comptent qu'au passage à l'entier suivant [P:Entraînement].
- Physique (Endurance, Vitesse) requis à tous les postes de champ [G:Commencer à jouer] ; « les compétences physiques sont l'attribut le plus important » [F:2026-05-01 Admin-Dev].
- Pas de système d'expérience : un jeune de 16 ans a la même probabilité de carton qu'un joueur de 24 ans [F:2026-10-14 PIPO68].

## Poste naturel : sous-rôles [G:Effectif — Notes et positions]
- Pas de poste fixe : le manager place qui il veut [F:2026-05-17 Admin-Dev].
- Seules **4 compétences définissent le poste** : Gardien, Défense, Conduite, Finition. La plus haute donne la zone (GB / défenseur / milieu / attaquant) ; la **2e plus haute** des compétences pertinentes donne le sous-rôle. Tête, Passe, Centres et Contrôle ne sont jamais principales, même plus hautes.
- 10 sous-rôles : **GB** gardien · **DC** défenseur central · **LAT** latéral · **WB** piston · **MD** milieu défensif · **MC** milieu central · **ML** milieu latéral · **MO** milieu offensif · **AC** avant-centre (spécialiste de la tête) · **DR** attaquant dribbleur. Dans l'API, `position` ne donne que GK / DEF / MID / FWD [Obs].
- Exemple donné par l'admin : Défense 1re puis Contrôle 2e = latéral [F:2026-06-24 Admin-Dev].
- Outil de placement conseillé par le jeu : feuille « Best Player Position Tool » (BPP/Tool) [G:Commencer à jouer] [F:2026-04-29 Admin-Dev].

## Compétences clés par poste [G:Commencer à jouer 2.1]
Par ordre de priorité, secondaires entre parenthèses.
| Poste | Compétences | Mission |
|---|---|---|
| Gardien | Gardien, Contrôle, (Passe) | Arrêter les tirs |
| Défenseur central | Défense, Contrôle, (Tête, Passe, Conduite) | Arrêter les attaquants, dégager |
| Arrière latéral | Défense, Contrôle, (Passe, Conduite) | Fermer les flancs |
| Latéral offensif (piston) | Défense, Contrôle, (Centres, Conduite) | Défendre le flanc et centrer |
| Milieu défensif | Conduite, (Contrôle, Défense, Passe) | Aider la défense, distribuer |
| Milieu | Conduite, (Contrôle, Passe, Défense) | Défense et attaque |
| Ailier | Conduite, (Contrôle, Centres, Passe) | Centrer et passer depuis l'aile |
| Milieu offensif | Conduite, (Contrôle, Passe, Finition) | Passes décisives et tirs |
| Avant-centre (Tête) | Finition, Contrôle, (Tête) | Marquer de la tête sur centre |
| Avant-centre (Conduite) | Finition, Contrôle, (Conduite) | Dribbler et tirer |
- La version du forum (2026-04-29, BETA) ajoute Vitesse et parfois Endurance en secondaire : gardien (Endurance), défenseurs et milieux (Vitesse), ailier et milieu (Endurance).

## OVR [G:Effectif — Notes et positions]
**OVR = (1 × Principale + 0,5 × Étoile + 0,2 × Secondaire 1 + 0,2 × Secondaire 2) / 1,9**, selon le sous-rôle **naturel** ; les 6 autres compétences n'y entrent pas.
- Exemple : MC avec Conduite 100, Passe 92, Défense 81, Contrôle 71,4 → (100 + 46 + 14,28 + 16,2) / 1,9 = 92,9 → **93**.
- Le guide ne détaille pas quelles compétences sont « Étoile » et « Secondaires » pour chaque sous-rôle ; l'admin renvoie au guide sans répondre [F:2026-09-23 PIPO68]. À déduire de nos données (régression sur `rating`) avant de s'en servir.
- L'OVR est affiché seulement : il ne change pas les capacités du joueur [F:2026-05-08 Admin-Dev]. Le classement d'équipe (`team_rating`) n'est pas une moyenne simple des 18 [F:2026-06-25 Admin-Dev].

## Notes de match [G:Effectif — 3] [F:2026-10-14 PIPO68]
- Note de 0,5 à 10 (pas de 0,5) à la fin du match, calculée dans le **sous-rôle naturel** : jouer hors poste baisse la note. Depuis octobre 2026, échelle décimale 0–10 (avant : 0–5 étoiles), matchs passés recalculés.
- Échelle : 8,5–10 Élite · 7–8 Professionnel · 5,5–6,5 Compétitif · 0,5–5 Amateur.
- La note tient compte du poste joué, du soutien des coéquipiers proches (note de zone) et des événements du match.

## Forme (0–100) — la clé du rendement
**Effet en match** [F:2026-06-27 Admin-Dev] : chaque action est multipliée par **0,70 + 0,30 × Forme / 100** (duels, tirs, passes, tacles ; pas le gardien sur penalty). Forme 100 → ×1,00 · 80 → ×0,94 · 60 → ×0,88 · 40 → ×0,82 · 30 → ×0,79. Effet dès la 1re minute : un joueur à 100 avec Forme 50 joue comme 85 [F:2026-08-28 Admin-Dev].
**Plafond et fatigue en match** (moteur v3, 2026-10-18) [F:2026-10-18 Admin-Dev] :
- La Forme d'avant-match fixe un plafond (Forme 60 → 88 %). Le joueur entre à 100 % de ce plafond, titulaire ou remplaçant.
- Toutes les 5 minutes jouées, son pourcentage baisse selon son **Endurance**. Sur 90 minutes : environ −9 points avec Forme 100, −16 avec Forme 60. Un remplaçant frais entre avec tout son plafond.
- Indicateur de force en direct à côté de chaque joueur dans le rapport v3.
**Évolution de la Forme** : seulement à l'entraînement hebdomadaire, jamais en match (officiel ou amical) [F:2026-06-30 Admin-Dev]. Table par intensité dans teamsoccer-entrainement. Minimum 30, maximum 100 ; un nouveau joueur commence à 85.
- **Fin de saison** : réponses contradictoires (« reste telle quelle » 2026-07-03 Admin-Dev ; « elle repart » 2026-09-14 PIPO68 ; « non, pas de remise à zéro » 2026-10-11 PIPO68). Dernière réponse : **pas de remise à zéro**. À vérifier au changement de saison avec nos exports.
- [Obs] Dans l'API `players`, `fitness` (0–100 : 98, 84, 46…) correspond vraisemblablement à la Forme, et `form` est un libellé (« Good », « 5 »). À confirmer avec la page Effectif.

## Talents spéciaux [G:Académie des Jeunes] [F:2026-04-29 Admin-Dev]
7 % des jeunes de l'académie ont un talent ; Magique 3 %. Visible seulement à la montée en équipe première [F:2026-09-22 PIPO68].
| Talent | Effet | Valeur | Météo qui le pénalise (−20 % sur toutes ses compétences) |
|---|---|---|---|
| 🏋️ Performance | Entraînement ×2 | ×3 | Ensoleillé ☀️ (garde le bonus d'entraînement) |
| ⚽ Buteur | Finition ×1,3 en match | ×3 | Vent 💨 (perd aussi le ×1,3) |
| 🛡️ Bouclier | Défense ×1,3 en match | ×3 | Pluie 🌧️ (perd aussi le ×1,3) |
| 👸 Idole | Affluence ×1,5 à domicile — il suffit qu'il soit dans l'effectif, même sans jouer [F:2026-05-18, 2026-07-06 Admin-Dev] | ×3 | Neige ❄️ (garde le bonus d'affluence) |
| 🪄 Magique | Les 4 talents | ×5 | Aucune |
- **Tous les talents disparaissent à 32 ans.** Avec un talent, regarder la météo du match avant de l'aligner.

## Blessures [G:Blessures] [F:2026-08-13 PIPO68]
- En match, durée de 1 à 7 jours ; badge avec jours restants dans l'Effectif et la fiche. Décompte automatique une fois par jour (vers 03:00). Un blessé ne peut pas être aligné.
- Pas de blessure en amical [F:2026-09-07 Admin-Dev]. Depuis le 2026-09-17, les blessures dépendent de la Forme du joueur (annonce 103). V-20261019-6 : elles n'arrivent que sur un tacle dur ou un duel physique ; le joueur plaqué risque une blessure, de 1 à 7 jours, une seule par match. Avant le 2026-09-17 la chance était de 1 % fixe ; changement proposé : Forme 100 = 0 % ; 85 = 0,20 % ; 70 = 0,40 % ; 50 = 0,58 % ; 40 = 0,76 % ; ≤ 30 = 1,00 %, linéaire entre ces points. Hypothèse : le texte est écrit « proposed change », application non confirmée par un message séparé (la FAQ dit que la condition physique joue).
- Remplacement d'un blessé : automatique poste pour poste si le banc est configuré (voir teamsoccer-match).

## Cartons et suspensions [F:2026-08-13 PIPO68]
- Rouge direct ou 2 jaunes = expulsion. Rouge = suspendu ; **3 jaunes cumulés = suspendu**. Suspension levée après le match de ligue suivant (compteur de jaunes remis à 0).
- Au 2026-08-13, seuls les cartons (et blessures) des matchs de **ligue** étaient enregistrés ; correction proposée pour tous les matchs officiels, application non confirmée. Cartons en sélection nationale sans effet en club [F:2026-09-14 PIPO68]. Pas de carton reporté depuis un amical.

## Âge et vieillissement
- +1 an par saison pour l'équipe première [F:2026-05-08 Admin-Dev]. Les jeunes encore à l'académie ne vieillissent pas [F:2026-09-28 PIPO68] (contredit par le programme de changement de saison, question restée sans réponse le 2026-10-01).
- Progression et déclin par âge : voir teamsoccer-entrainement (gain réduit dès 23 ans, perte à partir de 29–30 ans).

## Valeur et salaire
- **Valeur de la fiche** = prix payé par la banque TeamSoccer et prix de départ maximal d'une enchère. Changement de valeur au plus tous les 7 jours [G:Valeur des joueurs].
- Formule du guide : valeur de base = somme des compétences × 100, puis × âge (18 ans ×10, 19 ×8, 20 ×6, 21 ×5, 22 ×4, 23 ×3, 24 ×2, 25 ×1, 26 ×0,8, 27 ×0,6, 28 ×0,5, 29 ×0,3, 30+ ×0,1). **Ne correspond pas à nos données** [Obs : un 21 ans et un 26 ans de même niveau valent tous deux 1 158 502 $]. Depuis le 2026-07-12, la valeur est « fondée sur les compétences, l'OVR et le poste » [F:2026-07-12 Admin-Dev]. Talent : valeur ×3, Magique ×5.
- **Salaire hebdomadaire ≈ 1 % de la valeur** [Obs : 16 000 $ pour 1 600 026 $, 9 035 $ pour 903 450 $]. Le guide ne parle pas des salaires ; ils sont la ligne « Wages » des Finances.

## Effectif [G:Finances] [F:2026-04-29 Admin-Dev]
- **16 minimum, 24 maximum**, enchères en cours comprises [F:2026-10-18 Admin-Dev]. À 24, impossible d'enchérir ou de monter un jeune. Le guide dit qu'on ne peut dépenser que « avec plus de 16 joueurs ».
- Temple de la renommée : le joueur continue à jouer ; ses compétences y sont figées au moment de l'entrée, donc à faire en fin de carrière [F:2026-06-21 PIPO68].

## [Obs] Nos données
- API (`/rest/v1/players`) : compétences, `rating` (OVR), `position`, `form`, `fitness`, `talent`, `value`, `wage`, `injury_days_remaining`, `is_suspended`, `season_yellow_cards`, statistiques officielles.
