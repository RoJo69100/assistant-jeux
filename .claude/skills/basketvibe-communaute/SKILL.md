---
name: basketvibe-communaute
description: Ce que disent le Discord BasketVibe (lu en entier le 2026-10-16, 2 624 messages du 31/05 au 09/10/2026 ; delta du 09/10 au 23/10 lu le 2026-10-23, en base) et les News de l'admin (lues jusqu'au 2026-10-22 : moteur v4 en ligue après la saison 1, fatigue plus punitive, duels plus marqués, blessures v4, potentiel de ses joueurs visible) — précisions du développeur, versions du moteur, conseils et observations de la communauté, prix du marché constatés, contradictions avec le manuel. Chaque point est daté et sourcé. À charger en complément des skills de règles, pour les conseils pratiques, ou quand le manuel est muet.
---

# BasketVibe — communauté et développeur (Discord)

## Comment lire cette skill
- **[Dev aaaa-mm-jj, salon]** = vachacz, développeur unique du jeu : quasi officiel, mais ça peut changer.
- **[Com aaaa-mm-jj, auteur, salon]** = un joueur : opinion ou expérience, **pas une règle**.
- **[News aaaa-mm-jj]** = annonce officielle de l'admin sur la page News du jeu (`silver.bv_news`, lue le 2026-10-18) : vaut une règle pour la version de moteur qu'elle cite.
- **Le manuel l'emporte** en cas de contradiction ; les écarts sont signalés ⚠️.
- **Reset du monde le 2026-09-06** (saison 1 depuis le 07/09). Ce qui date d'**avant** porte sur la bêta : souvent périmé, marqué 🕰️.
- Source brute : `bronze.discord_messages` (export du 2026-10-16).

## 1. Moteur de match : versions et calibrage
- **Moteur** : la ligue reste en **v3 jusqu'à la dernière journée de la saison 1 (lundi 26/10)** ; le **v4 est activé dans tous les types de matchs juste après la saison 1**, et le dev ne prévoit **plus aucun changement du v4** [News 2026-10-19 ; Dev 2026-09-30]. Un amical (v4) ne prédit donc plus la ligue v3 aujourd'hui, mais prédit la ligue de la saison 2. Ne pas mélanger les tendances v3 et v4 : couper `gold.bv_match_trends` à la date du changement. (Le v3 tourne en ligue depuis la journée 12 [Dev 2026-09-30 / 2026-10-04, release-notes + engine].)

### Moteur v4 : changements annoncés (amicaux seulement en saison 1, **ligue en saison 2**)
À prendre en compte pour préparer la saison 2. Les amicaux depuis le 11/10 tournent déjà avec ces réglages.
- **Fatigue plus punitive, une seule échelle pour l'attaque et la défense** : fatigue 0 → 0 % ; 20 → −4 % ; 40 → −15 % ; 60 → −30 % ; 80 → −50 % [News 2026-10-17].
  - ⚠️ C'est plus dur que le tableau du manuel (v3 : attaque −3 / −10 / −20 / −40 % à 20 / 40 / 60 / 100 ; défense plus faible encore) [M§5.6].
  - Simulations miroir de l'admin (équipe fraîche contre la même fatiguée à 20 / 40 / 60 / 80) : **+1,7 / +7,4 / +11,5 / +15,3 points** pour l'équipe fraîche.
  - But annoncé : décourager le « 5 × 48 min » (les bots sur ce réglage gagnaient trop) [News 2026-10-17].
- **Duels 1 contre 1 plus marqués** : le v3 resserrait les gros écarts de compétences ; en v4, un défenseur à ~80 pèse plus contre un attaquant à ~40, et inversement. « La tactique a plus de place et plus d'impact. » Les équipes bots (≈ 10 points de compétences sous les humains) perdent 1,5 à 4,5 points par match de plus [News 2026-10-16].
- **Fautes** : leur répartition suit maintenant l'agressivité défensive (manquait en v3). Avec un **Lock**, le défenseur direct provoque moins de fautes, puisqu'une partie des tirs du joueur visé part chez ses coéquipiers [News 2026-10-11].

### Autres annonces (toutes versions)
- **Changement de poste d'un senior** sur sa fiche, dans la plage permise par sa taille [News 2026-10-14]. Complète le manuel (libellé modifiable dès 22 ans [M§4]).
- **Primes de fin de saison** confirmées : 1er 400k, 2e 300k, 3e 200k, 4e 100k, 5e–8e 50k, 9e–12e rien [News 2026-10-14]. Concorde avec le manuel §10.1.4.
- Les tests de potentiel sur le marché n'apparaissent plus comme des achats dans Finances [News 2026-10-14].
- Logos : option « Remove solid background » (Settings) pour un fond transparent ; logos prédéfinis désormais transparents [News 2026-10-20].
- Mises à jour du 2026-10-19/20 (potentiel révélé, blessures et focus Rim/Perimeter en amical, Best fives, amicaux hors succès) : détail dans basketvibe-joueurs, -tactique, -saison et -academie.
- Trophées pour les 3 premiers de chaque ligue et pour le finaliste de la coupe ; partage de l'historique d'entraînement dans le chat ; le play-by-play affiche le remplacement d'un joueur indisponible par le depth chart [News 2026-10-11].
- Les poids du PS sont **indicatifs**. Le moteur joue possession par possession avec les compétences, pas avec ces pourcentages [Dev 2026-09-17, engine].
- Pénalité au-delà de 36 min : 8 % → 10 % → 12,5 % → **20 %** (le 2026-09-13). Le manuel indique 20 % [Dev, release-notes]. La communauté trouve que les équipes à « 5 × 48 min » gagnent encore trop souvent [Com 2026-09-12, grobarbrate/faraone85, engine].
- Le dev simule un match 1 000 fois pour mesurer la chance (exemple : 68 % de chances de gagner, et défaite quand même). **Un match isolé ne prouve rien** [Dev 2026-06-27 / 2026-08-24, general].
- Tirs à 3 : plafonnés à **50 % des tirs** pour un joueur réglé « tout à 3 pts » [Dev 2026-08-24]. Le plafond par joueur a été relevé le 2026-09-16 (détails non publiés) [Dev, release-notes].
- Dernier passeur choisi selon le poste et le rôle ; sa passe améliore le tir assisté [Dev 2026-08-24], ce que confirme le manuel §5.1.4.
- Fin de match serrée : fautes volontaires de l'équipe menée (v3) [Dev 2026-09-09].
- Le libellé de poste n'a aucun effet, seule la taille sur l'emplacement compte ; entre 200 et 205 cm en PG, la baisse est linéaire [Dev 2026-09-10, help].
- Complément (V-20261023-10) : le libellé de poste n'a **aucun effet sur le match** (seules comptent la taille et la corpulence par rapport à l'emplacement) [Com 2026-10-21, elemke. (GM), general, relu en base ; Dev 2026-09-10, help]. Il sert (1) à l'éligibilité aux récompenses de poste (top 5 de journée et de saison) [Com 2026-10-21, marekb9231, general ; non recoupé en base] ; (2) au **PS affiché**, qui dépend des poids du poste [M§2.2] : un joueur est passé de PS 51 à 52 en passant de PG à SG [Com 2026-10-15, foo_13, ex-yugo] — **observation isolée, confiance faible**. Seniors seulement (juniors : pas encore) [Dev 2026-10-10 et 2026-10-17, general].

### Autres éléments (faible priorité, V-20261023-14)
- Autres annonces [News 2026-10-20, relue en base] : onglet League « Best fives » (dont un meilleur cinq U21) ; les amicaux ne comptent plus pour les succès de joueur ; logos : option « Remove solid background » et logos prédéfinis transparents. [News 2026-10-22, relue en base] : onglet Schedule « Matches » (l'ancien « Combined ») par défaut ; stats de tir dans l'ordre FT%, 2P%, 3P% ; ORB/DRB ajoutés ; premier jet d'un outil d'analyse d'équipe, qui fera partie d'un futur pack Supporter en 2027 ; correctif : sauvegarde des tactiques sur mobile (lineup OT manquant).
- V-20261027-8 [News 2026-10-22, 2026-10-25] : stats en FT%, 2P%, 3P% partout ; ORB et DRB ajoutés à REB ; classements de ligue limités aux joueurs ayant joué au moins 50 % des matchs ; notes privées de joueur (effacées au transfert), filtres rapides du marché, affluence dans Schedule. Impact : l'ordre des colonnes de tirs a changé, vérifier les scripts d'export et la lecture FT/2P/3P.
- V-20261027-2 [News 2026-10-27] : v4 actif en ligue, coupe et amical depuis le 27/10 ; duels plus marqués (un ~80 bat nettement un ~40), bots plus faibles ; moteur v5 de micro-améliorations annoncé, sans date. Détail dans basketvibe-tactique.
- Le dev peut rejouer un match 1 000 fois : une défaite avec 96 % de chances de victoire est un cas rare, « sous observation » [Dev 2026-10-11, engine]. Idée de « rejouer N fois pour voir le taux de victoire » (réservée aux matchs de ligue) envisagée, sans date [Dev 2026-10-11, engine].
- Équipes inactives : leur tactique par défaut (cinq fixes sur 48 min) bat encore des équipes de jeunes en v3 ; plusieurs joueurs l'ont constaté [Com 2026-10-13/21, carlomtlopes/dollarius/arodrigues84, portugal et italia] (avis) ; le v4 devrait corriger (fatigue, +40 % de blessures au-delà de 36 min, hypothèse).
- Avis : en défense normale, un joueur à 48 min avec une fatigue < 30 ne se remarque presque pas (v3) [Com 2026-10-09, heldermoreno, portugal] ; ⚠️ contredit par les chiffres du v4 [News 2026-10-17] : pour la saison 2, ne plus s'y fier.
- Grandir : les joueurs disent +4 cm par saison jusqu'à 21 ans (max 15 cm de 16 à 21 ans) [Com 2026-10-13/17, chanceler/grobarbrate/montabelas] ; ⚠️ le skill academie et le manuel disent « jusqu'à 22 ans » [M§5.2] : le manuel fait foi.
- Outil tiers cité par le dev (depth chart) : https://www.onlinesportmanagers.com/tools/basket-vibe-depth-chart-tool/ [Dev 2026-10-13, general] ; extensions de navigateur de joueurs : sources non vérifiées.
- Récupération de fatigue : confirmée par le manuel (0,5 + 10 % de la fatigue du moment ; l'endurance ne joue pas sur la récupération) [M§5.6 ; Com 2026-10-23, grillanza, italia].
- V-20261030-1 [Release-notes vachacz 2026-08-07 et 2026-09-28] : +/- et PER ajoutés le 2026-08-07 (écrans match, effectif, profil joueur) ; **PER remplacé par EVAL le 2026-09-28**, utilisé aussi pour le MVP et le meilleur cinq (anciens MVP recalculés) ; League > Players : filtre de tirs minimal pour FG% et 3P% (seuil tronqué dans l'export) ; le développeur note que les équipes à 5 × 48 min dominent le « top 5 de la saison ». EVAL est l'indice de performance du jeu : ne plus citer PER.
- Médecins : 1 médecin = 7–8 jours pour 10 jours de blessure ; 2 médecins = 5 jours [Com 2026-10-21, isr_shay/elemke., general, relu en base] : cohérent avec −25 % chacun [M§4.3]. Question ouverte : un joueur dont la date de retour tombe le dimanche d'entraînement s'entraîne-t-il ? « On croit que oui, pas sûr » [Com 2026-10-21, uthred9751, italia] — à tester avec `gold.bv_training_gains_exact`.

## 2. Tactique
- **Agressivité défensive** = « arme à double tranchant » : un match plus fort, payé en fatigue. On peut jouer soft pour se permettre un match agressif ensuite [Dev 2026-09-19, engine].
  - Retours de joueurs : l'agressif « ne paie pas pour l'instant », ils restent en équilibré en ligue et en coupe, au minimum en amical [Com 2026-09-22, tankre1792 / grillanza, italia].
- **Focus défensif** : erreurs rapportées par les joueurs. « Give up » sur un pivot → il en a marqué 48 [Com 2026-09-09, tankre1792, italia]. Délaisser un joueur qui n'avait jamais joué → puni [Com 2026-09-13, grillanza, italia]. Trop concentrer le focus est contre-productif [Com 2026-09-22, uthred9751]. C'est le cas « Miss » du manuel §6.6.
- Tactique de match = preset + focus. Si on modifie un preset, il faut **le re-sélectionner sur chaque match déjà planifié**, sinon l'ancienne version est utilisée [Com 2026-09-05, grobarbrate/vortexraijin, help].
- Les joueurs observent qu'une tactique soignée fait gagner. Exemple : défaite contre le dernier sans tactique, alors que le moteur donnait 68 % de victoire [Com+Dev 2026-08-24, general].

## 3. Joueurs, entraînement, potentiel
- **Les compétences sont stockées avec des décimales** [Dev 2026-08-02]. Les juniors de l'académie et les effectifs de départ commencent **sans décimales** [Dev 2026-09-13, help].
- **Expérience** : elle monte de façon linéaire, mais son effet ne l'est pas. **Les 10 premiers points comptent plus que ceux de 80 à 90** [Dev 2026-08-02, general].
- **S'entraîner ne demande pas de jouer** : tout le monde s'entraîne chaque semaine, quelles que soient ses minutes [Dev 2026-09-21, help ; manuel §8].
- Pas de plafond caché par compétence : on peut monter jusqu'à 99, de plus en plus lentement [Dev 2026-09-08, help].
- Potentiel identique quel que soit le pays [Dev 2026-09-08]. Joueurs libres : potentiel tiré **au hasard entre 3 et 9** [Dev 2026-09-07, help].
- Un junior « 3 étoiles » de 16 ans gagne **18 à 24 points de compétence par saison** selon son potentiel [Dev 2026-09-24, help] ; cohérent avec le manuel §8.3.
- Lire le potentiel dans les progrès (méthode des joueurs) :
  - « 3 étoiles » = potentiel 8–10 [Com 2026-09-06, help ; manuel §4.2].
  - Un +2 sur la compétence principale en une semaine (16–18 ans) indique au moins un potentiel moyen, pas forcément 10 [Com 2026-08-16, dcarra / random_player_123].
  - +2 principale et +1 secondaire dès la première semaine → potentiel 10 très probable [Com 2026-09-24, pilipinas].
  - Il faut **4–5 entraînements** pour une estimation fiable [Com 2026-09-01, dcarra, italia].
  - Les décimales cachées faussent ces lectures. Nos valeurs précises (`*_exact`) donnent une mesure bien meilleure.
- **Potentiel de nos propres joueurs visible depuis le 2026-10-20** : il s'affiche dans la fiche et y reste [News 2026-10-20 : « Reveal your own player's potential in his profile, and it stays visible to you »]. Les fiches des nouveaux juniors d'académie restent visibles (nouveaux seulement) [News 2026-10-20] ; les anciens tests d'académie ne sont pas récupérés [Dev 2026-10-18, general].
  - ⚠️ **Contradiction** : le manuel §11 (lu 2026-10-23, résumé) parle encore de « Unknown » avant test ; la News du 2026-10-20 dit l'inverse. La News est plus récente ; le manuel peut être en retard.
  - **Constat dans nos données (2026-10-23)** : la page joueur de Chomelix Cow (joueur de notre effectif), capturée le 2026-10-22 13:33 UTC, affiche « Potential ★★☆ — Decent potential », soit une **tranche** (pas un nombre) ; aucun test de 25 000 pour ce joueur dans les transactions exportées. Un test a été payé pour un autre joueur (Dang, 2026-10-19), avant la News. Le champ de la fiche `potential_reveal_available: true` existe aussi dans le JSON d'une page joueur. Format confirmé pour **un seul joueur** : à confirmer sur d'autres fiches. `gold.bv_potential_estimate` n'a pas de `potential_est` au 2026-10-23 (15 lignes, 0 gain mesuré pour la semaine du 2026-10-18) : la comparaison est impossible pour l'instant.
- Endurance sous 40 jugée « inutile » [Com 2026-08-13, grobarbrate, reset] : opinion. Selon le manuel, l'endurance ne joue que sur la fatigue et les blessures.
- Garder tout le monde **sous 15 de fatigue** → une seule blessure sur une saison [Com 2026-08-23, random_player_123, general] : expérience individuelle, cohérente avec le manuel §9.3.
- Pivots : monter le rebond jusqu'à 80 avec la défense, car le ralentissement devient fort au-delà [Com 2026-10-06, .doman/kotryk, polska]. Contre-avis : l'athlétisme aide à la fois le rebond, la défense et l'attaque [Com 2026-10-08, marekb9231].
- Un grand pivot athlétique et bon rebondeur marque beaucoup même avec peu de tir à 2 [Com 2026-09-14, carlomtlopes, portugal].
- 🕰️ « Stage de présaison » : petit bonus d'entraînement des jeunes au changement de saison [Dev 2026-07-21]. Date d'avant la refonte de l'entraînement (2026-08-10), **non confirmé aujourd'hui**.

## 4. Académie
- Le rapport est tiré **après** la mise à jour du jeudi. Exemple : si la jauge passe de 99 à 100 %, le rapport bénéficie déjà du bonus des 100 % [Dev 2026-09-28, polska] ; conforme au manuel §4.2.
- Stratégie répandue : **ne pas signer en fin de saison**. Monter à 100 % et faire le premier recrutement au début de la saison suivante, car tout le monde vieillit en même temps au changement de saison [Com 2026-10-08, giovannidziadzia / .doman, academy ; Com 2026-07-12, br0kh3n].
- Ne signer qu'un 3 étoiles après test, sauf compétences exceptionnelles. Un 17 ans 3 étoiles reste derrière un 16 ans 3 étoiles [Com 2026-09-12/13, carlomtlopes, portugal].
- Le test à 25 000 « vaut le coup » (≈ 1,5 amical de recette) [Com 2026-09-10, .doman, academy].
- ⚠️ « Attendre 100 % ne sert à rien par rapport à 90 % » [Com 2026-10-22/23, grillanza/dixi2499, italia ; avis non retrouvé mot pour mot en base] : **contredit le manuel** [M§4.2] : probabilité d'un potentiel 8–10 = 27,3 % à 90 %, 43,9 % à 100 % (P10 : 3,5 % → 10,7 % [M§4.2]). Chiffres 27,3 et 43,9 vérifiés dans `gold.bv_academy_potential_odds` le 2026-10-23. Le manuel fait foi.
- Fin de saison 1 : ne pas signer avant le changement de saison (27/10) ; le prochain rapport est celui du jeudi 29/10 [Com 2026-10-22/23, italia ; Dev 2026-10-18 : l'académie ne se remet pas à zéro]. Consensus d'avis (le junior de 16 ans a 17 ans au changement de saison ; signer fait perdre la moitié de la jauge) ; certains ont tiré quand même (17 ans PS 51 tiré à l'académie 100 %, « 50/50 ») [Com 2026-10-22, dcarra/grillanza/allymcinally, academy et italia].
- Observation isolée : avec test, le PS réel est tombé en haut de la fourchette estimée (51 pour une estimation 47,6, min 42,6, max 52,6) : un cas, pas une règle [Com 2026-10-22, isr_shay, academy].
- Les valeurs de départ maximales confirment le tableau du skill academie : au-dessus de 90 %, 55 maximum par compétence à 16 ans, 57 à 17 ans [Com 2026-10-12, grillanza, italia ; M§4.2]. La page Académie du jeu indique la jauge projetée [Com 2026-10-23, grillanza, italia].
- ⚠️ « 71 000 investis font progresser la jauge autant que 100 000 » [Com 2026-09-13, nhegas12, portugal] : **non vérifié**, contraire aux tableaux du manuel §4.2. À tester avec `silver.bv_academy_weekly`.

## 5. Économie et personnel
- **Amicaux = revenu important** : ~17 000–20 000 par amical pour chaque club [Com 2026-09-05, lolek5232, help ; Obs : 20 150 le 2026-10-16]. Le dev le confirme : « jouer des amicaux reste financièrement important » [Dev 2026-08-21, economy]. Sans blessure, avec 1/10 de fatigue et d'expérience : idéal pour faire jouer les jeunes.
- Match de ligue à domicile : **250 000 à 400 000** selon la popularité [Dev 2026-09-05, help].
- Personnel = **un compromis, pas « tout prendre et oublier »** [Dev 2026-08-28, general].
  - Médecins : **on peut les embaucher après une blessure**, ils agissent à partir du jour d'embauche [Dev 2026-09-14, help]. Facturation = maximum de la semaine, donc ~10 000 par médecin et par semaine d'usage (manuel §4.3.6).
  - Kinés : comptés **au coup d'envoi**, à embaucher **avant** les matchs.
  - Conseil répandu : médecins et kinés seulement en cas de blessures ; le marketing utile si on perd souvent à domicile [Com 2026-09-12, carlomtlopes / chanceler, portugal].
- Solde négatif : interdiction d'enchérir ; restrictions possibles sur le personnel et l'académie [Dev 2026-09-12, help ; manuel §10.3].
- Pas de limite de taille d'effectif, à part le coût des salaires [Dev 2026-09-12, help].
- Sponsor : 6 contrats au choix **à partir de la saison 2**, version « tout ou rien » retirée, écarts réduits [Dev 2026-10-02, economy].
- ⚠️ Prime de titre : « 200 000 » [Dev 2026-09-27, help] → le manuel actuel dit **400 000** (§10.1.4). Le manuel fait foi.
- Salaires non linéaires et revenus selon le niveau de la ligue : **envisagés pour plus tard** [Dev 2026-08-27, economy]. Le dev « peut gonfler l'économie si elle est trop serrée » [Dev 2026-08-28].
- Alternance domicile/extérieur non garantie : début de saison inégal en recettes, mais 11 domicile / 11 extérieur sur la saison [Com 2026-09-11, italia].

## 6. Marché des transferts
- Prix constatés en saison 1 [Com, italia 2026-09-11 / pilipinas 2026-09-24 / lietuva 2026-09-22] :
  - 16 ans PS 40 ≈ **300 000** ; PS 42 ≈ **500 000**. Prix doublés en 2 semaines début septembre.
  - Jeunes à fort potentiel : **1 à 2 M+**.
  - « Même les mauvais jeunes partent à des prix délirants » (lietuva 22/09).
  - Bêta : stars à 1,5–2,5 M.
- Fin de saison 1 (avis, non vérifiés sauf mention) : PF PS 63 vendu 2,3 M le 22/09 puis 4,0 M ; 16 ans PG > 3 M (20/10) ; une enchère à 3,5 M citée comme la plus chère [Com 2026-10-17, carlomtlopes, portugal] ; 3,5 M n'ont pas suffi pour un 16 ans (Mercier, 20/10, grillanza, italia) ; prix « presque doublés en 2–3 semaines » ; 60–80 % des transactions observées seraient des reventes avec plus-value [Com 2026-10-14/20/22, dcarra/uthred9751/grillanza/dollarius, italia ; sakota0, portugal]. **Contrôle en base (2026-10-23)** : `gold.bv_market_price_known` (89 ventes du 16 au 22/10) a pour maximum 2 894 063 (SF 17 ans PS 49,7, le 21/10) ; les 3,5 M et 4,0 M ne s'y trouvent pas (hors fenêtre ou enchère non terminée). Références du dev (12/10) : 18 ans PS 45 = 100 000 ; 19 ans PS 49 = 380 000 ; 16 ans PS 44 = 660 000 [Dev 2026-10-12, general ; non recoupé en base].
- Une partie de la communauté attend les prix plus bas pendant la pause entre saisons, d'autres pensent qu'ils vont monter : avis opposés, aucune donnée [Com 2026-10-21/22, italia].
- Taxe dégressive sur les reventes rapides : idée d'un joueur, à l'étude, non décidée (voir basketvibe-transferts) [Dev 2026-10-22, economy].
- Conseil : acheter des jeunes vite, avant que les prix montent encore [Com 2026-10-08, .doman, academy].
- Joueurs libres post-reset : TSP entre 360 et 420 [Dev 2026-08-14], potentiel 3–9 [Dev 2026-09-07]. Départ à 10 000 (manuel §11.4).
- Taxe de 5 % (anti-revente rapide), délai avant revente ramené à **7 jours** [Dev 2026-07-29 / 2026-09-14] ; conforme au manuel §11.1.

## 7. Coupes
- ⚠️ Coupe de septembre 2026 : « **25 % de fatigue et d'expérience** » [Com 2026-09-12, dcarra, italia]. Par défaut, le manuel dit 0 (§3.3) : **chaque édition annonce ses propres règles** (Inbox → BasketVibe). Vérifier avant chaque coupe.
- Bug signalé (2026-09-18) : en coupe, le preset amical était pris par défaut ; depuis, il existe un preset coupe [Dev 2026-09-19].

## 8. À venir (non joué, ne pas en tenir compte pour les règles)
Moteur v4 en ligue en saison 2 ; zone de défense et « fréquence de pénétration » à l'étude ; équipes nationales et coupe mondiale ; contrats de sponsor ; salaires non linéaires [Dev, engine/economy/general].
