# Charte Hockey Nation (2026-11-06)

Les faits du jeu sont dans `docs/fiches/hockeynation/resume.md` ; les cartes `docs/decisions/cartes/hockeynation/composition.md` et `defaite.md` portent les variables et les checks ; les leçons sont dans `outputs/hockeynation/learnings.md` (L-nnn). Cette charte ne les recopie pas.

## But
- **Premier : comprendre le Match Engine** pour les 4 équipes : PRO Chomelix Cows, FRM Ben Ahmed Donkey, U21 Mjóifjörður Sheep, U17 Martigny Saint Bernard. Les 3 autres équipes servent à apprendre pour la PRO.
- **Objectif sportif : 1er au classement** pour les 4 équipes.

## Hors périmètre du plan quotidien
- Transferts, finances, Trade Center, horizon long : jamais dans le plan quotidien.
- Seule alerte : **plafond salarial négatif** (−30 % en match, `resume.md` § Règles propres au jeu).
- Les échéances calendrier (fermeture de fenêtre jour 35, Import Draft jours 49–54, draft jour 63, offres de coachs) restent dans le calendrier par jour de saison (`gold.hn_today`, `resume.md` § Saison 27), pas dans le plan quotidien.

## Temps de lecture
7 minutes pour tout Hockey Nation. Valeur fixée par l'utilisateur : ne plus la demander.

## Tactique PRO : pas tous les jours
Elle n'est proposée que si l'un des cinq déclencheurs est vrai :
- (a) la lineup exportée date d'avant le dernier changement ;
- (b) case vide, joueur hors poste ou joueur parti (`gold.hn_tactique_controle`) ;
- (c) un test arrive à échéance ;
- (d) deux défaites de suite ;
- (e) nouveau joueur dans l'effectif.

## Tests
- Un réglage à la fois.
- Durée : **10 matchs** pour le plan de jeu (échéance déjà posée : shift length short, `resume.md`) ; **5 matchs** pour PP1/PP2 et les infériorités (à valider).
- Chaque test porte « ce qui prouvera que j'avais tort » et son échéance en matchs (C4) ; sans les deux, pas de test.
- Amical seulement quand un test est ouvert (carte composition, var. 12).
- **Défaite grave** = deux défaites de suite d'une même équipe (4 équipes) → analyse immédiate (`analyste`). Sinon une revue par semaine de tous les matchs.

## Registre du Match Engine
- **Où** : les pour/contre de chaque règle s'inscrivent dans `outputs/hockeynation/learnings.md` (§ Enseignements, colonnes Matchs et Statut des L-nnn). Une règle nouvelle prend le prochain L-nnn.
- **Qui** : Claude, **une fois par semaine**, avec la revue des matchs : il reprend les lignes « L-nnn pour/contre » du bloc 3 des plans de la semaine et met à jour les compteurs et le statut.
- **Plus tard** : un compteur automatique des pour/contre viendra dans un lot suivant ; d'ici là, le compte est tenu à la main.
- **Match d'une équipe non PRO** (FRM, U21, U17 : lignes automatiques) : inscrit avec la mention **« expérience sans notre choix »** ; il apprend le moteur de match mais ne juge pas nos réglages.

## Échelle d'une défaite
Dans cet ordre, on s'arrête à la première cause prouvée :
1. **Composition** : joueur hors poste, case vide, lineup saisie moins d'1 h avant le match (carte composition, var. 1, 2, 11).
2. **Tactique** : plan de jeu, unités spéciales (carte defaite, var. 4, 9).
3. **Force relative** : `gold.hn_club_compare`, coach rating (carte defaite, var. 8).
4. **Hasard** : réalisation et arrêts, règles L-001 et L-007.

Chaque défaite se termine par « **pouvait-on gagner : oui ou non, pourquoi** ». Il n'y a pas de blessures dans ce jeu : ne pas en chercher (`resume.md`, veille Discord du 2026-10-29).
