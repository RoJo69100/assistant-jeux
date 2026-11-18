# Règles de l'utilisateur (BasketVibe)

Avant toute modification du plan, lire ce fichier. Toute règle nouvelle de l'utilisateur y est ajoutée dans la même session :
date, ses mots, et la clé de `docs/attentes/jeux/basketvibe.yaml` qui la porte (« — » si aucune clé ne la porte).
Contrôle : `python -I pipelines/test_regles_utilisateur.py` (chaque clé citée existe dans le yaml).

| Date | Domaine | Règle (mots de l'utilisateur) | Clé de basketvibe.yaml |
|---|---|---|---|
| 2026-11-17 | Exports | Le plan demande toujours le Marché (toutes les pages) et l'historique global des transferts chaque jour (périmés après 24 h), pour trouver de bonnes offres ; le Personnel une fois par semaine. | `etat_jour.exports_periodiques` |
| 2026-11-17 | Académie | « je signe un prospect quand il a un très gros potentiel, qu'il correspond aux meilleures caractéristiques du poste, qui a la bonne taille, qui a tout ». Résultat du test : à lire plus tard. | `etat_jour.evenements.academie` |
| 2026-11-17 | Preset | En ligue et en coupe, on fait le preset de l'adversaire pour voir ses joueurs, puis on règle la zone et le focus défensif ; en amical on teste joueurs et tactiques, pas de preset. | `competitions.ligue`, `competitions.coupe`, `competitions.amical` |
| 2026-11-17 | Offres | Bonne offre = un joueur pas cher meilleur qu'un des nôtres, ou vraiment pas cher et revendable plus cher. Vendre pour profit = un joueur plus utilisable, vendable à un bon prix. Les seuils sont fixés par Claude, jamais demandés à l'utilisateur. | `offres` |
| 2026-11-17 | Personnel | Règle de personnel du yaml, statut DÉCIDÉE par Claude le 17/11, contestable par l'utilisateur : marketing 0 (clause d'embauche après 2 défaites à domicile supprimée), médecins 2, kinés 4, psychologues 0 si la forme moyenne des joueurs utilisés sur les 4 derniers matchs de ligue ≥ 8, sinon 2 (7,2 le 17/11 → 2) ; le plan n'affiche une ligne Personnel qu'en cas d'écart. | `personnel_propose` (affichage : fonction etat_jour.texte_personnel, pas une clé) |
| 2026-11-18 | Académie | Seuil DÉCIDÉ par Claude le 18/11, contestable par l'utilisateur : « meilleures compétences au poste » = sur la fourchette de PS du test, borne basse ≥ PS du joueur de rotation le plus faible au poste ET borne haute ≥ PS du meilleur joueur au poste − 5 ; potentiel high seulement. Aucun high observé : à recalibrer au premier. | `academie_signature` |
| 2026-11-17 | Méthode | Un traitement global qui agit à chaque fois, jamais un correctif par événement ; une architecture solide qui marche, puis on améliore. | — |
