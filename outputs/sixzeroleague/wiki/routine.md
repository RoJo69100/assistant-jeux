# Routine Six Zero League

Tout se fait **le soir**. Sources : skills sixzeroleague-communaute § 1 (rythme), -match (composition par défaut), -entrainement, -club, -aujourdhui. Pas d'heure imposée à l'utilisateur : un match raté n'est pas grave, mais les matchs de 13:00 et 21:00 se préparent la veille ou le soir même.

## Le rythme du jeu
- **2 journées de ligue par jour** : 13:00 et 21:00 Paris [Com chat, 97777ali ; confirmé Dev chat]. Coupe vers 17:00 ou 18:00 Paris, horaire incertain [Dev chat, Com chat].
- Une « semaine » du jeu = 2 journées terminées : finances, entraînement, blessures et transferts se règlent ensemble [W:Finances, Training, Transfers]. On l'appelle **cycle** ; en pratique **un par jour**, après le match de 21:00 [Dev chat].
- Le cycle ne tourne que pendant une saison de ligue ; hors saison aucun cycle ne passe [W:Training].
- **La composition enregistrée sert à tous les matchs** tant qu'on ne la change pas : pas de composition par match [W:Match].

## Chaque soir
| Action | Pourquoi |
|---|---|
| Vérifier blessés et suspendus (Équipe → Players), exporter si besoin | Un blessé ou un rouge direct vide un poste ; rouge direct = suspension au match suivant [W:Match, Injuries] |
| **Enregistrer la composition** (Équipe → Tactique) avant le prochain match | La composition par défaut sert aux matchs de 13:00 où l'on n'est pas là [W:Match]. Contrôle SQL du brief tactique : 7 titulaires distincts, 0 blessé, 0 hors-poste |
| Régler l'**entraînement** (intensité, focus par joueur) avant le match de 21:00 | Le cycle se règle après ce match [Dev chat] ; un changement de focus joue au cycle suivant [W:Training] |
| Poser les **enchères** (marché) avant 21:00 | Règlement de toutes les annonces toutes les 2 journées [W:Transfers] ; impossible de vendre ou libérer pendant un match de ligue de son équipe [W:Transfers] |
| Après le match de 21:00 : **exporter** League, Équipe → Training, Finances/Club, puis agents Match, Entraînement, Finances | Vérifier les gains du cycle et le solde. Un brief de plus de 2 jours sur le sujet du soir est périmé (skill aujourdhui § Méthode) |
| Après un match : agent Match | Journal `learnings.md` ; seuil de confirmation d'un enseignement : 3 matchs de ligue dans le même sens [fiche match] |

## Chaque saison (9 à 11 jours) [Dev chat]
- **18 journées** de ligue, ligue de 10 clubs, matchs aller et retour [W:Competitions] ; 9 jours à 2 journées par jour, jusqu'à 11 s'il y a beaucoup d'équipes en coupe [Dev chat].
- **Coupe** : élimination directe pour les clubs humains ; un tour se joue entre les deux journées d'une « semaine » [W:Competitions].
- **Fin de saison** : un admin clôture puis lance la suivante (montées, descentes) [W:Competitions]. Le champion monte, les **3 derniers descendent** [W:Competitions].
- **Entre deux saisons** : choisir le sponsor (changement une fois par saison, entre deux saisons seulement) [W:Sponsors] ; les salaires sont revus [W:Finances] ; **+1 an pour tous les joueurs** [Dev chat].
- **Académie U18** : un nouveau choix toutes les 8 journées de ligue terminées, soit environ tous les 4 jours [W:U18] ; export de l'onglet U18 à chaque nouveau choix.
- Saison en cours : J1 le 2026-10-19 [Obs, `silver.sz_schedule`] ; calendrier à lire dans `silver.sz_schedule` (si `captured_at` a plus de 24 h, exporter la page League).

## Ce qui n'existe pas
Pas de forme, pas de moral, pas de personnel, pas de jauge d'académie [fiche commun]. Pas de réglage d'agressivité : prévu plus tard [Dev chat]. Pas d'enchère maximale automatique : chaque enchère est manuelle [W:Transfers].
