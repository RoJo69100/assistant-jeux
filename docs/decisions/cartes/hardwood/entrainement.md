# Carte hardwood — entrainement (Development : focus principal, secondaire, entraînements additionnels)

Sources lues : commit d0cfdca (2026-11-02)

Écrite le 2026-11-02 (`resume.md`, skill `hardwood-regles` ; veille `v-joueurs-entrainement.md` ; learnings). Coaching (progression) jeudi et dimanche matin (Pacifique). Saisie dans l'ordre de l'écran Development.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire-hardwood.txt:26 | caractéristiques et entraînement additionnel | var. 1-3 |
| :27 | suivre le progrès | var. 4 |
| :18 | toutes les caractéristiques | var. 1 |

## Rendu (figé)
`| Joueur | Poste | Classe | SI → plafond | Compétences clés du poste (valeur) | Focus principal | Focus secondaire | Entraînement additionnel | Progrès dernière mise à jour | Garder / changer |`.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Compétences et plafond | `select name, pos, class, si, pot, si_cap_min, si_cap_max, marge_max, best_pos, progres_derniere_maj from gold.hw_effectif where not walk_on order by marge_max desc limit 20` | Plafond ≈ 14 × potentiel à +13 ; travailler une compétence clé du poste ; valeurs affichées ±20 % | v-recrutement § 4 ; `resume.md` § Pièges | |
| 2 | Compétences clés | fiche académie § Règles 1 | PG = IQ, Pass, Hnd, Spd ; SG = OS, Spd ; SF = OS, défense, Spd ; Grand = IS, Reb ; vitesse et IQ grandissent peu | v-joueurs § 1 | |
| 3 | Réglage actuel | `silver.hw_development` | Focus principal / secondaire, entraînements additionnels ; Overwork à surveiller | skill règles | |
| 4 | Progrès | `progres_derniere_maj` ; `silver.hw_development` | Une baisse affichée n'est pas une vraie baisse (±20 %) ; les valeurs convergent avec les matchs joués | v-joueurs § 1 | |
| 5 | Expérience de poste | graphe de développement | 0-3 par poste, s'acquiert en jouant (exhibitions comprises) | v-joueurs § 1 | |
| 6 | Coachs | carte `finances` var. 1 | Compétences de développement des coachs | skill règles § Coachs | |
| 7 | Avis des amis | v-joueurs § 1 | Force lente au lycée puis plus rapide | v-joueurs § 1 | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis | Statut (base) |
| --- | --- | --- | --- | --- |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
