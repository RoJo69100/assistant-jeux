# Quel entraînement selon le poste et l'âge

Sources : skill basketvibe-entrainement [M§8.2–8.5], basketvibe-joueurs (poids du PS [M§2.2]), basketvibe-tactique (compétences par emplacement [M§7.1]), conseils de la communauté [Com]. La décision de la semaine vient de l'agent Entraînement (`gold.bv_training_options`, `gold.bv_potential_estimate`).

## Les règles qui décident
- Principale **+1,0**, secondaire **+0,5** par semaine, multipliées par le potentiel, l'âge et le niveau [M§8.2].
- **Ralentissement** : ×0,88 à 75, ×0,75 à 80, ×0,50 à 90 [M§8.4]. Monter une compétence de 40 à 60 rapporte bien plus que de 80 à 85.
- 0 progression à 30 ans, déclin dès 31 [M§8.5]. Un joueur blessé ne s'entraîne pas [M§8].
- Changer coûte peu, mais il faut **4 à 5 semaines** pour juger un choix [Com 2026-09-01].

## Par poste (emplacement réellement joué)
| Poste | Principale (ordre de préférence) | Secondaire | À éviter |
|---|---|---|---|
| **PG** | Passe, Dribble | Défense, 3 pts | Rebond (poids 5 au PS) |
| **SG** | 3 pts, 2 pts | Défense, Athlétisme | Rebond, Passe |
| **SF** | 2 pts, 3 pts | Défense, Athlétisme | — |
| **PF** | Rebond, 2 pts | Défense, Athlétisme | 3 pts si le joueur ne tire pas |
| **C** | Rebond (jusqu'à ~80 [Com 2026-10-06]), 2 pts | Défense, Athlétisme (aide rebond, défense et finition [Com 2026-10-08]) | 3 pts, Passe |

**Endurance** : n'agit pas en match [M§7.1] ; +1 point ≈ −0,7 % de fatigue par match (calcul SQL du 18/10) : rarement prioritaire, même en v4.

## Par âge
| Âge | Stratégie |
|---|---|
| **16–18** | Construire la compétence majeure du poste en principale jusqu'à 70–75, puis passer à la suivante (plan « une compétence jusqu'à 80, puis la suivante » [M§8.6]). Les gains sont les plus forts : ne pas gaspiller une semaine |
| **19–24** | Compléter le profil de l'emplacement où il joue réellement ; éviter les compétences au-delà de 80 |
| **25–29** | Peu de gain : viser la compétence qui change un duel (défense de l'emplacement, ou le tir de son rôle) |
| **30+** | Inutile [M§8.5] : laisser tel quel |

## Exemple : Maël Bernard (17 ans, C, potentiel 10)
Rebond en principale (+2,20 par semaine mesuré le 18/10), athlétisme en secondaire. Quand le rebond approchera 70–75 (dans 3 à 4 semaines), passer le 2 pts en principale (brief entraînement du 18/10).
