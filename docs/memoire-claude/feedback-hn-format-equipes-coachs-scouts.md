---
name: feedback-hn-format-equipes-coachs-scouts
description: "Hockey Nation — format imposé pour rosters, coachs et scouts (tableaux par poste, match skills d'abord, jeunes coachs, scouts nommés), plus rappel d'utiliser règles et Discord"
metadata:
  node_type: memory
  type: feedback
  originSessionId: a6a6af01-9d37-4493-819e-15d2dc04d3dd
  modified: 2026-10-25T15:14:29.049Z
---

Hockey Nation, demandes du 2026-10-25 (l'utilisateur était mécontent : « je n'ai rien compris », « tu n'utilises presque jamais les règles ou les exports Discord »).

- **Rosters** : pour les 4 équipes, un tableau par équipe avec les postes et les joueurs nommés ; écrire VIDE si vide, CONTRE-EMPLOI si contre-emploi (= à remplacer), TOP JOUEUR, À TRADER. Jamais de colonne « trou / à améliorer ».
- **Coachs** : le critère est les **compétences de match** (OFP, DFP, BAT, PP, PK ; celles du head comptent double), pas l'entraînement. Donner par équipe et par coach : garder ou remplacer, et par quel coach nommé. Toujours inclure des **jeunes coachs à potentiel** (forts sur 2 compétences de match, peu d'expérience). Plafonds : U17 note 54 / expérience Average ; U21 note 69 / Very Good ; vérifier s'il existe une limite en FRM (non trouvée le 10-25).
- **Scouts** : tableau « prends ce scout » avec, pour chaque scout, les joueurs nommés qu'il scoute le plus vite (poste et nation identiques = durée la plus courte). Un pick = 20 rangs (pick 1 = 1-20, pick 2 = 21-40…).
- **Limite de roster** : aucun maximum de 20 en PRO n'est documenté (Discord : « more than 20 players on the roster » est possible) ; ne pas retarder une signature pour « libérer une place ».
- Chercher d'abord dans les skills, le guide et `bronze.discord_messages` (colonnes `posted_at`, `payload->>'content'`) avant de dire qu'une règle manque.

- **Corrections du 2026-10-25 (soir)** : les U21 montent en FRM/PRO à tout âge (auto à 21 ans) ; Leszno, Jessup, Miami, Seoul = équipes de comparaison, jamais partenaires d'échange ; plus de tag « TOP/meilleur de l'équipe » : juger la force réelle et l'avenir d'un joueur par ses compétences spéciales, son rôle dans la ligne et la cohésion de ligne, pas par la note seule.

**Why:** réponse précédente jugée illisible, centrée sur l'entraînement alors que le critère était le match, et sans utiliser les règles.
**How to apply:** HN, tout rendu d'équipe, de coach ou de scout suit ce format. Voir [[feedback-hn-4-equipes-format]] et [[feedback-aucun-flou-noms-et-donnees]].
