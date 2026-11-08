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

### Moteur v5 : amicaux seulement depuis le 28/10 (V-20261108-5)
- [News 2026-10-28] Plus de 20 s d'inaction en fin de quart-temps ; tirs au buzzer et tirs de demi-terrain ou de tout le terrain en fin de quart, à pourcentage plus bas ; plus de possession de plus de 24 s dans le play-by-play.
- **Dans le money-time, les dernières actions du match vont aux joueurs au focus offensif le plus élevé.**
- Étend à chaque quart-temps le travail v4 sur le 4e ; déploiement dans tous les matchs « vers le milieu de la saison », sans date.
- Impact : amical = v5, ligue = v4 jusqu'au déploiement. Ne pas mélanger leurs tendances.

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

