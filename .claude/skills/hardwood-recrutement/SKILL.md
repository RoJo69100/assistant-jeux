---
name: hardwood-recrutement
description: Règles et méthode Hardwood du recrutement — types de recrues (lycée, JuCo, international), points de recrutement (2 par jour, gros versement au début, plafond 45, report 10 + moitié), offres de bourse, niveaux d'intérêt (Low à Very High), engagements probabilistes (à partir de la mise à jour 5), facteurs (niveau de conférence, prestige, durée du contact, coach, géographie, temps de jeu, redshirt des 4-5 étoiles), régions, phrases du scout et plafonds, méthode des bons managers. À charger pour choisir, contacter ou abandonner une recrue, ou répartir les points.
---

# Hardwood — recrutement

Sources : **[R:Rubrique]** = manuel officiel (capturé le 2026-10-30). **[D]** = Discord, veille du 2026-10-30 (`outputs/hardwood/veille/v-recrutement.md`, statut entre parenthèses). **[G]** = guide d'un joueur (Google Doc fourni par l'utilisateur). **[A]** = document d'aide de l'utilisateur (`data/manual/hardwoord/Aide docs.txt`, 2026-10-30). **[E]** = nos exports.

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

## Arrivée des recrues [A]
- **HS** : seul un lycéen **HS SR** s'engage ; il arrive **FR** (4 ans). Un HS JR ne s'engagera que dans 2 saisons.
- **JC** : un junior college s'engage en **JC SO** et arrive **JR** (2 ans d'éligibilité).
- Prendre **3 à 4 recrues par classe** (pas 2), dont **au moins un grand** (PF/C) ; garder des plans B, et chercher en fin de saison des « pépites » bon marché [A].

## Répartir les contacts [A]
- Plus de contacts sur les mieux notés (étoiles, SI) : les autres équipes les chassent fort.
- Dans la région, peu de contacts suffisent pour prendre la tête et la reprendre : pas besoin de grosse avance.
- Recrue pressée (« eager to commit early ») : il suffit d'être en tête au moment du sprint. Recrue qui attend : il faut une grosse avance, sinon les équipes qui ont perdu leurs cibles nous rattrapent.
- Concurrence : si seules des D3 sans propriétaire la suivent, dépenser ailleurs ; une D1 avec propriétaire est un vrai rival. En fin de saison, vérifier si les rivaux n'ont plus de bourses libres : ils ne peuvent plus la prendre.
- Les montées de conférence relèvent l'intérêt des HS FR-JR et JC FR après la saison, les descentes le baissent (effet de montée plus fort, petit échantillon).

## Méthode des bons managers [G] [D]
- **Une cible principale à 45-60 points, plus deux secondaires pour 20 à 30 points au total.** Jamais 6 recrues à la fois avec 135 points.
- Rester dans l'État ou la région, éviter les duels High contre High. Repère [G] : dans l'État, une cible est jouable si 2 équipes au plus sont sur elle ; hors région, si aucune.
- **Garder environ 10 points au flip** (ils sont reportés entiers). Prendre de l'avance sur les JR et SO.
- Viser une recrue qui atteindra 110-115 de SI après redshirt ; sinon, elle ne servira pas longtemps [G].
- Rythme d'effectif conseillé : 2 à 4 recrues par classe, avec 2 ou 3 bourses qui se libèrent chaque saison.

## Tableau prêt
`gold.hw_recruit_board` (prospects de la recherche + nos suivis) : verdict cible / cible hors région / secondaire / dur / futur / écarter, `rang` dans le verdict, `besoin` = poste d'un boursier qui part, plafond de SI, équipes intéressées et à High, notre intérêt et notre offre, bourses libres et points.

## Recrues en deux temps (2026-10-30, `sql/gold/046_hw_recrue_fiches.sql`)
1. `gold.hw_recrues_a_ouvrir` : prospects engageables du board (cible, cible hors région, secondaire) sans page joueur en base. Donner **au moins 15 noms** à ouvrir : beaucoup sont rejetés une fois la page lue (demande de l'utilisateur).
2. `gold.hw_recrue_fiches` : une ligne par page ouverte. Note /5 au meilleur poste jouable (listé dans Positions, Grand ≥ 1,95 m), même barème que `gold.hw_roster_notes` : `note_now` (actuel) et `note_plafond` (potentiel + milieu des phrases du scout), `boursiers_devant` = nos boursiers qui restent et sont mieux notés, `cles_non_dites` = compétences clés sans phrase (plafond pris à l'actuel), `phrases_hors_ref` à ajouter à `silver.hw_ref_scout_phrases`. Verdict [H] : 🟥 offrir / 🟧 réserve / rejeter, risque 50/50 signalé.

## Inconnu
Coût exact par classe (HS FR à JC), taille et durée du malus de redshirt, seuils des étoiles, heure de réouverture après le flip.
