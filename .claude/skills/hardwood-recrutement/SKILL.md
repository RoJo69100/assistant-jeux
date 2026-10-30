---
name: hardwood-recrutement
description: Règles et méthode Hardwood du recrutement — types de recrues (lycée, JuCo, international), points de recrutement (2 par jour, gros versement au début, plafond 45, report 10 + moitié), offres de bourse, niveaux d'intérêt (Low à Very High), engagements probabilistes (à partir de la mise à jour 5), facteurs (niveau de conférence, prestige, durée du contact, coach, géographie, temps de jeu, redshirt des 4-5 étoiles), régions, phrases du scout et plafonds, méthode des bons managers. À charger pour choisir, contacter ou abandonner une recrue, ou répartir les points.
---

# Hardwood — recrutement

Sources : **[R:Rubrique]** = manuel officiel (capturé le 2026-10-30). **[D]** = Discord, veille du 2026-10-30 (`outputs/hardwood/veille/v-recrutement.md`, statut entre parenthèses). **[G]** = guide d'un joueur (Google Doc fourni par l'utilisateur). **[E]** = nos exports.

## Types de recrues [R:Recruiting]
| Type | Recrutable | S'engage | Arrive comme |
|---|---|---|---|
| Lycée (HS FR → SR) | dès 14 ans | en SR (dès la **mise à jour 5**) | freshman, 4 ans d'éligibilité |
| JuCo (JC FR → SO) | dès 18 ans | en JC SO (plus tard que les lycéens) | junior, **2 ans** d'éligibilité |
| International | 1 seule saison, à 17 ans | dans l'année (plus tard) | freshman |
- À la mise à jour 53, un non-engagé signe chez une équipe qui lui a offert une bourse, part en JuCo, devient walk-on ou arrête.
- **Il n'y a pas de transferts** : tout le renouvellement passe par ici [D (confirmé Steve, 2021)].

## Points et contacts [R:Contacts, Recruiting Calendar] [D]
- Un gros versement au début de la saison (≈ 29 au flip), puis **2 points par mise à jour** : ≈ 130-135 par saison [G] [D (confirmé)].
- **Plafond : 45 points en réserve.** À la fin de la saison, les points au-delà de 10 sont **divisés par deux**.
- Aucune limite de dépense par jour ni par prospect. Sur les **jeunes classes (FR, SO, JR), un plafond souple** réduit l'effet des gros contacts.
- Coût observé pour atteindre « Low » : 2 à 7 contacts dans l'État ou la région, 10 à 15 en dehors ou à l'international. Medium coûte environ 4 fois plus, High environ 7 fois [D (en doute : un seul joueur, 2026-03)].

## Offres, intérêt, engagement [R:Scholarship Offers, Commitments]
- Pas d'engagement sans **offre de bourse**. Offrir ne coûte rien [D]. **Retirer une offre remet à zéro** le travail fait sur ce joueur ; impossible une fois qu'il est engagé.
- Notre intérêt est affiché finement : None, Low, Low+, Low++, Medium, Medium+, Medium++, High, High+, High++, Very High. **Celui des concurrents est arrondi** (un « Medium » peut valoir Medium++) : on ne sait jamais si on mène vraiment.
- L'engagement est **probabiliste** : le plus haut intérêt n'est pas une garantie, d'où l'utilité d'un plan B.
- Une fois les bourses de la saison suivante toutes attribuées, aucun autre engagement n'est possible.

## Facteurs de réussite [R:Recruiting Success Factors]
- **Niveau de conférence** : en **Division 3, attirer des 4 et 5 étoiles est très difficile** ; en D2, les 5 étoiles.
- Prestige ; **durée du contact** (contacter tôt aide) ; note Recruiting du coach ; **géographie** (bonus dans l'État et la région) ; **temps de jeu offert** (un effectif plein de jeunes bien notés fait fuir) ; **redshirt de joueurs bien notés** (les élites fuient) ; une part de hasard.
- L'intérêt chute après une **descente de conférence** ou un **renvoi du head coach**.
- Notre région : **USA Central = Illinois, Indiana, Missouri, Ohio, West Virginia**. Eureka est dans l'Illinois [R:Recruiting Regions] [E].

## Évaluation du scout
- Une phrase de l'évaluation fixe une fourchette ou un plafond pour une compétence. Exemples : « Will always be a bit sluggish » = vitesse 6 au plus ; « Could be a dominating post player » = IS 18-20. Table : `public.hardwood_ref_scouting_ranges` [D (principe confirmé, valeurs non vérifiées une à une : la table d'origine est épinglée sur Discord, absente de l'export)].
- L'évaluation ne change pas d'une année de lycée à l'autre ; une nouvelle évaluation arrive au passage en JuCo [G].
- Regarder la croissance de la taille d'année en année : un joueur qui grandit tard peut encore atteindre sa taille projetée [G].

## Méthode des bons managers [G] [D]
- **Une cible principale à 45-60 points, plus deux secondaires pour 20 à 30 points au total.** Jamais 6 recrues à la fois avec 135 points.
- Rester dans l'État ou la région, éviter les duels High contre High. Repère [G] : dans l'État, une cible est jouable si 2 équipes au plus sont sur elle ; hors région, si aucune.
- **Garder environ 10 points au flip** (ils sont reportés entiers). Prendre de l'avance sur les JR et SO.
- Viser une recrue qui atteindra 110-115 de SI après redshirt ; sinon, elle ne servira pas longtemps [G].
- Rythme d'effectif conseillé : 2 à 4 recrues par classe, avec 2 ou 3 bourses qui se libèrent chaque saison.

## Inconnu
Coût exact par classe (HS FR à JC), taille et durée du malus de redshirt, seuils des étoiles, heure de réouverture après le flip.
