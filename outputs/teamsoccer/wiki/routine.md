# Routine Team Soccer (deux clubs)

Tout se fait **le soir**. Sources : skill teamsoccer-saison (rythme de la semaine), teamsoccer-match (composition 2 h avant), teamsoccer-entrainement (vendredi, académie), teamsoccer-club (lundi). Jours de match observés [Obs, `silver.ts_matches`, 2026-10-20] : **Ben Ahmed Donkey lundi et jeudi en soirée**, **Chomelix Cows mardi et samedi en début d'après-midi**. Un match en journée se prépare donc **la veille au soir** (le match est pré-calculé 2 h avant [F:2026-06-28 Admin-Dev]). Les coupes ajoutent des matchs (mardi, mercredi, jeudi) : l'agenda du soir les lit dans les données.

## Chaque soir
| Action | Pourquoi |
|---|---|
| Se connecter sur les deux clubs | Cercle rouge du moral : 5 jours de suite = 3 points [G:MC] |
| **3 révélations d'académie par club**, puis exporter la page Académie | 3 par jour, au plus 1 par jeune ; remise à zéro dans la nuit [P:Académie]. Une révélation non faite est perdue |
| **Enregistrer la composition** de chaque match qui tombe avant le soir suivant | Sans enregistrement, la composition par défaut s'applique [F:2026-07-18]. Vérifier l'onglet Avancé après enregistrement [F:2026-08-15] |
| **Exporter la page de chaque match joué** (ligue, coupe), puis agent Match | Notes, secteurs, événements → `learnings.md` |
| Exporter le Marché si une enchère est en cours, puis agent Transferts | Prolongation de 2 min sur offre tardive [G] |

## Chaque semaine
| Soir | Action |
|---|---|
| **Dimanche** | Composition de Ben Ahmed pour lundi |
| **Lundi** | Exporter **Finances et Stade** des deux clubs (semaine close dans la nuit) → **contrôler l'entretien du stade** (bug de facturation déjà vu deux fois [F:2026-10-13, 10-19 PIPO68]), puis agent Finances. Limite d'achat remise à zéro (1 achat par semaine [G]). Fenêtre de **paiement HPC** (décision Premium, à l'utilisateur). Composition de Chomelix pour mardi |
| **Mardi** | Export du match de Chomelix ; composition des coupes de mercredi |
| **Mercredi** | Composition de Ben Ahmed pour jeudi. Amicaux bloqués ce jour selon le skill [F:2026-09-08] (mais nos deux clubs ont joué un amical le mercredi 14/10 [Obs] : contradiction à faire trancher par la Veille) |
| **Jeudi** | Export du match de Ben Ahmed. **Régler l'entraînement des deux clubs** (compétence et intensité par joueur) : seul compte le réglage en place à la mise à jour de la nuit [F:2026-07-20 PIPO68]. Baisser l'intensité des joueurs à Forme basse |
| **Vendredi** | Exporter **Effectif et Entraînement** des deux clubs (gains et Forme de la nuit) → agent Entraînement. Composition de Chomelix pour samedi |
| **Samedi** | Export du match de Chomelix |
| Une fois dans la semaine | **Un amical par club** (pas possible tant que le club est en Coupe Nationale [F:2026-09-08]) : tests de poste (ex. Ounahi au but), jeunes, cercle orange du moral, un peu de billetterie |
| Une fois dans la semaine | Une **activité de marché ou d'académie** et un entraînement assigné : cercle bleu du moral [G:MC] |
| Après un export du forum ou des annonces | Agent Veille : propositions de mise à jour des skills, à valider |

## Chaque saison (9 semaines) [G:Compétitions 1]
- **Semaines 1 à 7** : 14 journées de ligue (2 par semaine). Coupes à partir de la semaine 2 (Nationale, Consolation, Masters, Champions).
- **Semaine 8** : barrages de montée/descente aller-retour (hors classement).
- **Semaine 9** : repos, Gala des récompenses le lundi, primes de classement.
- **Fin de saison** : +1 an pour tous [F:2026-05-08] ; Forme : dernière réponse « pas de remise à zéro » [F:2026-10-11 PIPO68], **à vérifier avec nos exports** (checklist D34) ; HPC : si 50 TSC ne sont pas atteints dans la saison, ils sont rendus [F:2026-10-10].
- Saison 3 en cours (début vers le 2026-10-12). Lundis restants et fin estimée : `gold.ts_season_calendar`.
