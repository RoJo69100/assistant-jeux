# Cartes : contrôle des oublis (2026-11-03)

Contrôle des 7 cartes `_core` contre `docs/decisions/variables.md`, puis des 42 cartes de jeu sur ce que la couverture `_core` leur renvoie (« carte du jeu »). Recherche par mots-clés : un « manque » est à confirmer en lisant la carte et le skill du jeu, jamais comblé par supposition.

## Cartes `_core` : corrigé le 2026-11-03
- finances C3 : lisait mon rang seul → classement complet (retard mesuré contre les autres clubs, A-8).
- finances C8 : infrastructures absentes → ligne ajoutée, renvoyée à la carte du jeu tant que `core.facility` n'est pas branchée (TS, SZL, DM).
- vente C8 : « progression attendue » absente → gain sur 7 jours.
- Chaque carte `_core` a sa section « Couverture » (variable obligatoire → C n° ou carte du jeu) ; `dossier.py` la recopie dans le dossier.

## Non applicable (pas un oubli)
| Jeu | Variable | Pourquoi | Source |
|---|---|---|---|
| basketvibe | finances : infrastructure | aucune infrastructure dans les skills BasketVibe | journal refonte v2, 1.2 (vérifié le 2026-11-03) |
| hockeynation | finances : infrastructure, sponsor | économie au plafond salarial, pas de trésorerie | `hockeynation.yaml` (infrastructures : present non ; finance_daily limites) |
| hockeynation | achat : forme de la cible | pas de forme dans le jeu | `hockeynation.yaml` core.player_daily limites (form) |
| hockeynation | achat / vente : taxe, enchère | échanges et agents libres, ni enchère ni prix | `hockeynation.yaml` core.market_listing limites |
| hardwood | achat / vente (marché), finances, sponsor | pas de transferts ni de finances : recrutement universitaire | `hardwood.yaml` (transferts, finances, infrastructures : present non) |

## À vérifier dans une session du jeu (variable obligatoire non trouvée dans la carte)
| Jeu | Carte : variable |
|---|---|
| basketvibe | achat : forme, fatigue, blessures de la cible · entrainement : seuils du poste (ralentissement au-dessus de 70 ?) · finances : rentabilité d'une dépense |
| derbymanager | vente : taxe et délai · defaite : minutes · academie : comparaison aux autres clubs · finances : rentabilité |
| hockeynation | composition / defaite : minutes (temps de glace) · academie : comparaison aux autres clubs · finances : rentabilité |
| sixzeroleague | achat : potentiel, forme de la cible, fit au poste · vente : taxe et délai |
| teamsoccer | achat : potentiel · vente : minutes, rôle, taxe · defaite : minutes · entrainement : potentiel · academie : comparaison aux autres clubs |

Règle : quand la carte d'un jeu est ouverte pour une décision (`dossier.py`), traiter sa ligne ici (variable ajoutée avec sa source, ou « non applicable » avec sa source), puis la rayer.
