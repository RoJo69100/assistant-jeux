# Vérification du brief Décideur 2026-10-26 (SZL)

| Affirmation | Verdict | Correction |
|---|---|---|
| Solde 1 843 €, -4 300 Youth Academy 4→5 | Juste | `silver.sz_finances` 2026-10-26 |
| Coûts cumulés YA depuis niv. 5 : 6 = 5 200, 7 = 11 400, 8 = 18 900, 9 = 27 900, 10 = 38 600 ; entretien 455 au niv. 10 | Juste | `silver.sz_infrastructure_levels` |
| Fan Shop 9→10 = 5 400 ; Arena 8 = 7 500 | Juste | idem |
| Solde 1 843 → 4 767 (cycle 8) → 5 041 (cycle 9, J17-J18 à l'extérieur) | Juste | 4 767 = +2 924 ; 5 041 = +274 (revenu sans match à domicile, -2 650). `gold.sz_finance_projection` (7 691) est faux ici : il compte 1 match à domicile au cycle 9 |
| Plan : Fan Shop 10 fin du cycle 1 (solde ≈ 2 700), Youth Academy 7 vers le cycle 4 (solde ≈ 1 000) | Tenable | 5 041 + ≈ 3 100 = 8 141 - 5 400 = ≈ 2 700. Puis +3 300/cycle : ≈ 12 600 en fin de cycle 4 ≥ 11 400, reste ≈ 1 200. Marge faible : un cycle à 2 matchs à l'extérieur (-2 650) décale à 5 |
| Fan Shop 10 : +266/cycle, 20 cycles de retour | Faux | +286 brut (1 474 → ≈ 1 760 à la 6e place), +241 net d'entretien (+45) : 19 cycles brut / 22 net |
| Seuil « revenu Fan Shop ≈ 1 919 » | Faux | ≈ 1 760 à place égale |
| Retard académie : niv. 5 = 16,5 contre Stoik 10 = 24, pierrottingchrist_29708 9 = 22,5 ; niv. 7 = 19,5 | Juste | milieux des fourchettes (5-28, 10-38, 9-36, 7-32) ; Stoik et pierrottingchrist : joueurs (chat/Discord), observation |
| Trident : 13 080 contre 11 550 Yarrow à 4 victoires, Trident devant jusqu'à 8 | Juste, avec réserve | Yarrow 11 550 exclut la prime de signature de 1 070 ; son renouvellement est non vérifié |
| Parts de tirs J10-J15 : centre 48/85 = 56,5 %, droite 47,3 %, gauche 37,3 %, LW 10/34 = 29,4 % | Juste mais mal étiqueté | Ce sont des efficacités. Parts des 245 tirs : centre 34,7 %, droite 38,0 %, gauche 27,3 %. Le centre était déjà à 56,9 % avant J10 |
| C-043 à C-046 de `learnings.md` | Juste | cohérents avec le brief (C-043 dérogation à C-040, C-044 plan infra, C-045 Trident, C-046 retrait C-035/C-036) |
| « right-center jamais vu en base » | Nuancé | L'option « Right + centre » est dans le menu de l'export app_team du 2026-10-24 ; la valeur dans `teams.tactics` n'a jamais été vue. Son effet reste non vérifié (texte de l'écran cité par un joueur seulement) |
| Série : 6 matchs sans victoire, 7 victoires en 15, J16 domicile, J17-J18 extérieur | Juste | `silver.sz_matches`, `silver.sz_schedule` |
| Dernier export tactique = 17921 | Incomplet | 17951, 17956, 17961 (19:27 UTC) sont postérieurs, sans `attackDirection`, non relus |
| Fournier +7 au CB, Passe 23, éthique 90, Endurance 32,8 % / 32,0 % | Non vérifié | hors périmètre demandé |

## Recommandations de mise à jour des fiches
- Fiche finances : `gold.sz_finance_projection` suppose 1 match à domicile par cycle ; à corriger avec `silver.sz_schedule` quand les derniers matchs sont à l'extérieur.
- Fiche commun : le menu app_team contient `right-center` (observé le 2026-10-24).
- Étiqueter « efficacité » ou « part » à chaque pourcentage de tirs par zone.
