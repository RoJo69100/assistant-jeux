---
name: feedback-format-tactique-parfait
description: "Format de rendu tactique validé \"absolument parfait\" par l'utilisateur le 2026-10-27 — à reproduire à chaque fois, ordre de l'export, focus défensif + zone par adversaire en tableau"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 51ef3928-8819-4dda-b574-79832ad90f33
  modified: 2026-10-30T09:32:45.436Z
---

Format validé (27/10 soir, « absolument PARFAIT, tu dois faire ça à chaque fois ») : un tableau joueur × quart-temps (poste, Q1–Q4, Prol., minutes, Off. focus, Rôle, Tir, Agress.), puis un second tableau **par adversaire** avec focus défensif 1–5 ET defensive area, les deux dans le même tableau.

**Why:** l'utilisateur veut saisir sans réfléchir ; le 27/10 j'avais oublié la zone défensive dans l'amical et listé les adversaires en vrac.
**How to apply:**
- Joueurs ET adversaires dans l'ordre de l'écran : par poste PG, SG, SF, PF, C, puis alphabétique dans le poste (ex. adversaires PG : Brun, Girard, Leclerc, Rousseau). Pas l'ordre brut du JSON (alphabétique global), pas regroupés par valeur.
- Dire « /compact maintenant » moi-même dès ~15 % de contexte (l'utilisateur paie chaque relecture du contexte).
- Tableau défensif : colonnes Adversaire | Poste | Focus défensif (1–5) | Zone (Rim/Middle/Perimeter), **une ligne par joueur** (Gautier, Jourdan, Lacroix…), pour coupe, ligue et amical. Jamais regroupé par valeur de focus, jamais « zone amical seulement ».
- **Récidive du 2026-10-30** : j'ai regroupé par focus et écrit que la zone n'existe qu'en amical. L'utilisateur : « Rim existe, nouveauté du nouveau engine, à mettre présent partout ». Un champ `area_step` dans l'export de coupe prouve que la zone existe. Avant de rendre une tactique, relire ce fichier et recopier `gold.bv_saisie_adversaires`.
- Si l'ordre ou les noms adverses manquent en base : le dire en une ligne et donner l'export à faire, jamais « tu lis à l'écran ».
- Pas de preset d'amical, pas de « si ». Voir [[feedback-rendu-demain-seulement]].
