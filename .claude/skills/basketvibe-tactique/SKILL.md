---
name: basketvibe-tactique
description: Règles BasketVibe de la tactique et du moteur de match — cinq par quart-temps, emplacements PG–C, depth chart, consignes par joueur (passe/tir, focus offensif, focus de tir, agressivité défensive), focus défensif par adversaire, presets, verrouillage, quelles compétences pèsent sur chaque action. À charger pour construire ou ajuster une tactique, analyser un match ou expliquer un résultat.
---

# BasketVibe — tactique et moteur de match

Sources : **[M§x]** = manuel officiel https://www.basketvibe.com/guide (lu le 2026-10-16). Le manuel donne des directions, pas tous les coefficients cachés [M§9.8]. Ne pas inventer de chiffres.

## Composition [M§6.2]
- 5 joueurs **par quart-temps** (Q1–Q4) plus la prolongation (OT), chacun sur un emplacement fixe PG, SG, SF, PF, C. Un joueur peut jouer un quart-temps et pas le suivant.
- Le moteur ignore le libellé de poste : seuls comptent l'**emplacement**, la **taille par rapport à l'emplacement** et le physique (table d'efficacité dans basketvibe-joueurs [M§6.2.1]).
- L'emplacement règle aussi la portée au rebond et les duels défensifs [M§6.2].
- Le manuel cite deux remplacements forcés pendant un quart-temps : 6 fautes ou blessure. Sinon, le cinq change au début de chaque quart-temps selon la grille [M§6.2].
- [Obs] Nos play-by-play contiennent aussi des événements `substitution_foul_trouble` (2 dans le match du 14/10) : le moteur sort parfois un joueur chargé de fautes. Le manuel n'en parle pas ; règle non documentée.
- Rappel : à partir de 36 minutes dans le match, −20 % sur tout (basketvibe-joueurs [M§5.7]). Les rotations par quart-temps sont le levier pour l'éviter.
- ⚠️ **Moteur v4 (ligue en saison 2)** : fatigue plus punitive (jusqu'à −50 % à 80) et duels 1 contre 1 plus marqués, ce qui donne plus d'impact à la tactique ; les fautes suivent l'agressivité défensive [News 2026-10-11 / 16 / 17]. Détail dans basketvibe-communaute. Une tactique de saison 2 doit gérer la fatigue d'un match à l'autre, pas seulement les 36 min. Le v4 sera activé dans tous les types de match juste après la saison 1, sans autre changement prévu au moteur [News 2026-10-19].
  - V-20261027-1/-2/-4 : v4 actif en ligue, coupe et amical depuis le 27/10 [News 2026-10-27]. Fatigue identique en attaque et défense : 0 / −4 / −15 / −30 / −50 % à fatigue 0 / 20 / 40 / 60 / 80 ; au-delà de 80, non précisé (hypothèse : −50 %). Blessures : Soft = 60 % et Medium soft = 80 % du risque neutre ; +40 % au Q4 au-delà de 36 min ; cinq meilleurs 48 min en Regular ou Aggressive coûtent des points et des joueurs. Duels : un ~80 bat nettement un ~40 (attaque et défense) ; bots un peu plus faibles. Fautes plus réalistes pour un défenseur en Lock (sens non précisé, hypothèse : mesurer les fautes en focus 5). Moteur v5 annoncé, sans date.
- [v4, amicaux] Risque de blessure : soft ×0,60, medium soft ×0,80 ; +40 % au-delà de 36 min au dernier quart-temps (détail dans basketvibe-joueurs) [News 2026-10-19].

## Depth chart [M§6.2.2]
- Pour chaque poste, liste ordonnée de 5 remplaçants maximum ; un joueur peut figurer sur plusieurs listes. Valable pour tout le club, indépendant des presets.
- Utilisé avant le coup d'envoi (blessé, doublon, place vide) et pendant le match (6 fautes, blessure).
- Si la liste du poste est épuisée : le joueur valide dont le poste est le plus proche sur l'échelle PG→C. Plusieurs postes à remplir : ordre C → PF → SF → SG → PG.
- Sans depth chart sauvegardé : uniquement l'échelle PG→C.
- Banc court : un remplaçant déjà très utilisé jouera quand même (~40 min possibles) ; le jeu ne plafonne pas les minutes.

## Consignes par joueur (pour tout le match) [M§6.3]
1. **Passe ou tir** : 5 crans, de passeur à scoreur. Oriente qui tire ; ce n'est pas un bonus de compétence.
2. **Focus offensif** : 5 crans, de Low à Primary en passant par Normal. Part relative de l'attaque qui passe par lui (dernière passe, tir, pertes de balle). Exemple : deux scoreurs, l'un Primary et l'autre Normal → le Primary tente ~1/3 de tirs en plus.
3. **Focus de tir** : 5 crans, de 2 pts à 3 pts. Au maximum ~2 tirs à 3 pour 1 tir à 2 ; toute l'équipe au maximum plafonne à ~50 % de tirs à 3.
4. **Agressivité défensive** : 0 soft · 2 équilibrée (défaut) · 4 agressive.

| | Soft (0) | Équilibrée (2) | Agressive (4) |
|---|---|---|---|
| Défense en duel direct | ~−14 | 0 | ~+14 |
| Défense moyenne des 5 | ~−4,4 | 0 | ~+4,4 |
| Tirs adverses provoquant une faute | ~12 % | ~16,5 % | ~21 % |
| Fatigue après match | ×0,75 | ×1,00 | ×1,65 |
| Risque de blessure | ×0,85 | ×1,00 | ×2,00 |

- Les fautes dépendent de l'agressivité **moyenne des 5 sur le terrain** ; la fatigue, de l'agressivité de chaque joueur.
- Ordre de grandeur, à niveaux égaux (~70) : adversaire à ~53 % aux tirs en soft contre ~48 % en agressif. Soit ~4–5 points encaissés de plus en soft qu'en équilibré, et ~3–4 de moins en agressif.
- ⚠️ **Moteur v4 (ligue à partir de la saison 2) : risque de blessure retouché** [News 2026-10-19]. Par rapport à une défense neutre : **Soft ×0,60** (v3 : ×0,85), **Medium soft ×0,80** (v3 : ×0,95). Les valeurs Neutre, Medium aggressive et Aggressive ne sont pas annoncées (le tableau v3 ci-dessus reste la seule référence). **Au-delà de 36 min, +40 % de risque de blessure au dernier quart** pour ce joueur. Effet annoncé : 48 min en Soft ≈ inchangé (0,60 × 1,40 = 0,84) ; 5×48 en défense normale ou agressive = « far more injuries ». Dernier message du dev : plus de changement prévu pour le v4. Interprétation (confiance moyenne) : la News étiquette ces deux points « v4, friendlies only », or les amicaux n'ont pas de blessure [M§1.2] ; ils visent donc la ligue v4. Texte de la News relu en base (`gold.bv_veille_feed`, 2026-10-19) le 2026-10-23.
- Le moteur respecte les consignes : il ne redirige pas le ballon vers le joueur en forme [M§6.3].

## Focus défensif par adversaire (par match) [M§6.6]
- Se règle sur la page du match (Tactics à côté de Preview), joueur adverse par joueur adverse. Verrouillé 15 min avant le coup d'envoi.
- **Sans plan sauvegardé, tous les adversaires sont marqués pareil.**

| Niveau | Lock | Intense | Normal | Light | Give up |
|---|---|---|---|---|---|
| Poids de marquage | 2,00 | 1,55 | 1,00 | 0,62 | 0,22 |

- Plus de focus : le joueur tire moins et, quand il tire, est mieux défendu. Ses coéquipiers récupèrent des tirs.
- **Hit** : Lock ou Intense sur le vrai scoreur (celui sur qui passe l'attaque) → l'adversaire perd nettement. **Even** : sur un cinq équilibré → le score bouge peu. **Miss** : Lock sur un meneur passeur → les autres ont des tirs plus faciles, l'adversaire peut marquer plus.
- Effet typique sur le % de réussite du scoreur visé : Intense contre Normal −2 à −4 pts ; Lock contre Intense −2 à −4 pts ; de Give up à Lock +12 à +16 pts d'écart.
- Conseils du manuel : verrouiller le scoreur, pas le meneur qui distribue ; compenser par Light ou Give up sur les joueurs peu utilisés ; toujours sauvegarder avant le verrouillage.
- [v4, amicaux pour l'instant] Nouvelle zone de focus défensif par joueur adverse : **Rim** (son 2P% −3 % environ, son 3P% jusqu'à +5 %), **Perimeter** (son 3P% −3 % environ, son 2P% jusqu'à +5 %), **Neutral** (comme avant). Le compromis est volontairement inégal [News 2026-10-19]. À vérifier : `silver.bv_match_tactics` capte-t-il ce champ ?
- [Export] Dans le plan sauvegardé exporté (page du match), un focus défensif **Lock** est écrit `off` ; confirmé à l'écran pour deux joueurs de Žirmūnai (J20) [Utilisateur 2026-10-21, learnings L-018]. Les autres niveaux sont écrits par leur nom.
- **Échelle à l'écran : 1 à 5** = Give up, Light, Normal, Intense, Lock (3 = Normal, valeur sans plan sauvegardé). Saisir le chiffre. [M§6.6.1 ; échelle confirmée par l'utilisateur le 2026-10-23]
- **Nombre de joueurs en Intense/Lock** : le manuel ne fixe aucun plafond. Il conseille « un ou deux » joueurs forts en Lock/Intense, compensés par Light/Give up sur le banc [M§6.6.5]. Les poids sont moyennés sur l'effectif adverse et décalent des tirs vers les coéquipiers [M§6.6.3]. Effet de plusieurs 4/5 en même temps sur les autres joueurs : non documenté, voir tests L-012 / C-040 du journal.
- Écart d'effet typique sur le joueur visé : un cran plus facile sur le scoreur clé ≈ +2 à +7 points de FG% ; Intense contre Normal et Lock contre Intense ≈ 2 à 4 points chacun [M§6.6.4].
- **En amical, un grand écart de compétence au même poste ajoute à l'effet du focus** ; en ligue et en coupe l'effet de compétence reste plus petit [M§6.6.3].

### Defensive area (amicaux seulement) [M§6.6.2]
- Second curseur par joueur adverse, à côté du focus : **Perimeter – Middle – Rim**. Middle = aucun décalage (défaut). Ni la ligue ni les coupes ne l'utilisent.
- ⚠️ V-20261027-3 (hypothèse, un seul texte, non testé) : le recap du 27/10 liste la zone parmi les changements du v4 « actif dans chaque match » sans la mention « amicaux seulement » [News 2026-10-27]. Elle est peut-être ouverte en ligue et en coupe : à constater sur l'écran tactique de la coupe du 28/10 ou de la ligue du 02/11 ; d'ici là, ne pas la régler en ligue. Valeurs : Rim −3 % de 2P% adverse mais jusqu'à +5 % de 3P% ; Perimeter −3 % de 3P% mais jusqu'à +5 % de 2P% ; Neutral = 0.
- Elle change le **% de réussite**, pas le nombre de tirs. Perimeter : tirs à 3 pts plus difficiles, tirs à 2 pts plus faciles. Rim : l'inverse.
- Ampleur : à l'extrême, tirs défendus ≈ −3 points, tirs ouverts ≈ +5 points ; un cran hors du milieu = la moitié.
- Annonce complète [News 2026-10-19, « v4 engine wraps up: injury tuning and defensive focus areas »] : réglage par joueur adverse dans la tactique du match (**amicaux seulement pour l'instant**). **Rim** : −3 % environ de 2P% adverse, mais jusqu'à +5 % de 3P%. **Perimeter** : −3 % environ de 3P%, mais jusqu'à +5 % de 2P%. **Neutral** : comme avant. Le déséquilibre est voulu : « décaler le focus à l'aveugle comporte un vrai risque, par exemple un grand qui tire à 3 ». [M§6.6.2] : la ligue et les coupes ne l'utilisent pas ; « for now » laisse penser à une extension future (à surveiller). Pas de plan sauvegardé : tous les adversaires sont marqués pareil.
- Avis de joueurs (non vérifiés) : « les intérieurs tirent environ 10 fois plus à 2 qu'à 3, on peut régler Rim à l'aveugle sur eux » [Com 2026-10-20, marekb9231, polska] ; avec seulement des fourchettes de compétences adverses, le choix reste « une loterie » [Com 2026-10-20, gulon84, polska].
- Utilité : à tester en amical pour la saison 2 ; non applicable en ligue (saison 1).

## Presets et verrouillage [M§6.4, §6.5, §1.1]
- Jusqu'à 5 presets nommés ; un actif pour la ligue, un pour les amicaux, un pour les coupes.
- Plan d'un match précis : preset, cinq et consignes propres à ce match + focus défensif. Le depth chart reste celui du club.
- Verrouillage 15 min avant le coup d'envoi (ligue 19:45). Le plan sauvegardé en dernier est utilisé.
- Tactique incomplète impossible : 5 joueurs différents par segment, consignes pour chaque joueur. Sans tactique sauvegardée : composition par défaut avec consignes neutres.
- Depuis le rapport d'un match terminé : « Save as preset » enregistre les cinq et les consignes (pas le focus défensif).

## Avantage du terrain [M§6.1]
Petit bonus de compétence à domicile et meilleure chance de gagner l'entre-deux du premier quart-temps.

## Quelles compétences pour quelle action [M§7.1]
| Action | Compétences utilisées |
|---|---|
| Lancers francs | Deux points (2/3), Trois points (1/3) |
| Tirs à 2 mi-distance | Deux points, qualité de la passe |
| Tirs à 3 | Trois points, qualité de la passe |
| Tirs à 2 au cercle | Deux points, Athlétisme (+ taille, poids), qualité de la passe |
| Défense intérieure | Défense, Athlétisme (+ taille, poids) |
| Défense extérieure | Défense, Athlétisme |
| Rebonds | Rebond, Athlétisme (+ taille, emplacement) |
| Interceptions | Défense, Athlétisme |
| Contres | Défense, Athlétisme (+ taille) |
| Éviter les pertes en dribble | Dribble, Athlétisme |
| Éviter les pertes sur passe | Passe, Athlétisme |
| Passes décisives | Passe, Dribble |
| Qui attaque la raquette | Dribble, Deux points |

L'endurance n'intervient dans aucune action [M§7.1].

Profils de joueur (compétences principales → secondaires) [M§7.1] :
| Profil | Principales | Secondaires |
|---|---|---|
| Shooteur en attente du ballon (spot-up) | Trois points, Défense | Deux points |
| Scoreur arrière / ailier | Trois points, Dribble | Deux points, Passe |
| Meneur passeur | Passe, Dribble | Deux points, Trois points |
| Pénétrateur | Dribble, Deux points | Athlétisme |
| Scoreur mi-distance | Deux points | — |
| Intérieur finisseur | Deux points, Rebond | Défense, Athlétisme |
| Rebondeur / dur au mal | Rebond, Défense | Deux points, Athlétisme |
| Défenseur extérieur | Défense | Athlétisme, Dribble |
| 3-and-D | Trois points, Défense | Athlétisme, Deux points |
| Intérieur shooteur | Trois points, Deux points | Rebond, Défense |

Par emplacement (attaque principale / défense principale) [M§7.1] : PG Dribble+Passe / Défense · SG Trois points+Deux points / Défense · SF Deux points+Trois points / Défense · PF Deux points / Défense+Rebond · C Deux points+Rebond / Défense+Rebond. L'athlétisme est secondaire partout.

## Déroulé d'une possession [M§7.3]
Chaque possession se termine par un tir, une perte de balle ou des lancers francs. Après un rebond offensif, le rebondeur a la priorité pour la seconde chance, en général au cercle et sans passe.

## Lecture de nos données
- `silver.bv_match_tactics` : tactique réellement jouée (cinq par quart-temps, consignes, focus défensif).
- `gold.bv_match_trends` : tendances sur les 5 et 10 derniers matchs, de mon côté et du côté adverse.
- Le PS adverse n'est visible que pour les joueurs en vente ; sinon les compétences adverses sont en tranches [M§2.2, §4].
