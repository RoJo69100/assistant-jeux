---
name: hockeynation-potentiel-joueurs
description: Hockey Nation : calculer le potentiel d'un joueur (note min et max) depuis ses compétences plafonnées et ses talents, puis le classer. Pour juger un trade, un prospect, un U21 ou un choix de draft.
---

# Hockey Nation — potentiel d'un joueur

Source : règle de l'utilisateur du 2026-10-25 [U], exemple de calibrage Kabát (RD 22 ans, 68 → minimum 73, maximum 89). Non confirmée par le guide ni par Discord (aucune formule de note publiée) : à garder comme hypothèse calibrée sur un exemple.

## Règle
- Talents = les 2 compétences au plus fort plafond (**fortes**) et la compétence au plus faible plafond (**faible**).
- Une compétence plafonnée (`max: true`, `*`) est définitive.
- **Faible plafond M** : toute autre compétence s'arrête au moins à M. Si la compétence faible n'est pas plafonnée, M ≥ niveau + 1. M est aussi strictement inférieur au plus bas niveau des autres compétences plafonnées (Kabát : CHK plafonné à 7, donc DSC ≤ 6).
- **Plafond fort C** : aucune autre compétence ne dépasse le plus bas des deux talents forts. Un talent fort plafonné à 9 fixe C = 9 ; deux talents forts non plafonnés laissent C = 10.
- **Minimum** : la compétence faible monte à son niveau + 1 si elle n'est pas plafonnée ; les autres non plafonnées montent au moins à M ; les fortes ne bougent pas.
- **Maximum** : la compétence faible monte à (plus bas niveau des autres) − 1 ; les autres montent à C.
- Chaque point de compétence vaut 1 point de note (calibrage Kabát). Ma régression sur 150 joueurs donne plutôt 1,15 (attaquants) à 1,28 (défenseurs) par point avec une erreur de 2 : les minima sont donc prudents. Pour les gardiens le facteur est inconnu (7 compétences) : lire avec réserve.
- Écart connu avec l'exemple : Kabát PAS (talent fort non plafonné, niveau 8) monte à 9 : maximum 90 au lieu de 89.

## Verdict (seuils calés sur notre PRO, 2026-10-25)
Classement par minimum, puis maximum. **Fort** : minimum ≥ 74 ; **Solide** : 68-73 ; **Moyen** : 58-67 ; **Nul** : < 58. Flèche ↑ : maximum ≥ minimum + 15 et joueur de 23 ans ou moins. Maximum au-dessus de 95 : plafond théorique (deux talents forts non plafonnés), jamais atteint tel quel.

## Futur (hypothèse, 2026-10-25)
Colonne ajoutée sur demande de l'utilisateur : où le joueur a sa place. **PRO** = minimum ≥ 64, ou 23 ans et moins avec minimum ≥ 55 et maximum ≥ 80 ; **FRM** = minimum ≥ 52, ou 23 ans et moins avec maximum ≥ 75 ; **VIRER** = le reste. Seuils choisis par moi, à ajuster. `tableau.py` produit le tableau (verdict + futur) à partir de `pot.json`.

## Vérification de l'utilisateur sur Spinka (RW, 72)
L'utilisateur lit minimum 74 et maximum 83. La règle ci-dessus donne 76 et 84 : tir et discipline (3) montent à 5 (+4 points) ; maximum à 9 (+12 points). Le jeu lui-même semble arrondir ou pondérer autrement (écart de 1 à 2 points) : sans formule de note publiée, comparer ces valeurs à l'affichage du jeu quand il existe.

## Quand l'appliquer [U, 2026-10-25]
Toujours pour une recrue (draft, U17 qui arrive, échange, agent libre), et souvent sur demande : états d'équipe, échange, montée, renvoi. Ne pas attendre qu'on le réclame.

## Utilisation
- Script : `potentiel.py` (lit `players.txt`, une ligne par joueur : `équipe|nom|âge|poste|note|compétences avec * si plafonnée|talents forts|talent faible|spéciales`, produit `pot.json`). Exemple de données : `exemple-joueurs-2026-10-25.txt`.
- Requête SQL des lignes : `silver.hn_player_snapshots` (jour le plus récent) ou `silver.hn_league_players` pour un joueur d'une autre équipe.
- Avant tout échange : calculer minimum et maximum du joueur reçu et du joueur donné, puis répondre « vaut le coup / ne vaut pas le coup » avec ces deux chiffres, ses spéciales et son rôle dans la ligne.
- Résultat du 2026-10-25 : `outputs/hockeynation/briefs/2026-10-25-potentiel.md`.
