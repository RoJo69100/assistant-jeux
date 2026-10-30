# Team Soccer — brief Entraînement du 2026-10-30

Agent Entraînement (medium + Sonnet). Données : export Effectif + Entraînement du 30/10 11:14 Paris (`silver.ts_players`, `silver.ts_training`, `gold.ts_player_progress` 29→30/10, `gold.ts_effectif_bilan`). Brief amont : Match du 30/10 ; delta : brief Entraînement du 24/10 (C-033). Registre `fait-2026-10-30` lu (exports et composition Bresse déjà faits).

## Actions à saisir aujourd'hui
| Priorité | Club | Action |
|---|---|---|
| 🟧 IMPORTANT | Ben Ahmed | **Zainab García (DEF, 16 ans, Défense 90, titulaire)** : passer de Contrôle 70 % à **Défense 70 %**. Gain attendu : +3 Défense par semaine (90 → 93 le 06/11), soit environ +2,8 points de valeur au match par semaine jusqu'à 100 ; Contrôle 23 n'est pas une compétence clé de défenseure. Forme inchangée (−2 à 70 %). |
| 🟩 SUIVI | Les deux | Tous les autres réglages : **garder** (liste ci-dessous). Aucun changement pour les Cows. |
| 🟩 SUIVI | HPC | Pas d'obligation : voir § 4 (décision Premium = utilisateur). |

## 1. Chomelix Cows (18) — décision : aucun changement
Constat de la nuit (PP 29→30/10) : 21 joueurs en base, tous à 70 % sauf Pierre Leroy (0 %). Gains : +3 pour les 14-20 ans et Moreau/Simon (20-21 ans), +2 pour 21-26 ans, **+1 pour Théo Dubois (27 ans)**, Pierre Leroy (32 ans, 0 %) **−2 Défense** (déclin d'âge, hors intensité). Forme −2 pour tous les réglés à 70 % ; Pierre Leroy 100 (0 %, pas de baisse).

| Joueur | Âge | Réglage (gain mesuré) | Décision |
|---|---|---|---|
| Ounahi | 19 | Conduite 70 % (+3) | Garder (Défense 100, Contrôle 100 : le reste monte) |
| Simon / Th. Thomas | 21 | Contrôle 70 % (+3 / +2) | Garder |
| Dubois | 27 | Contrôle 70 % (+1) | Garder (Défense 100 plafonnée, Contrôle 72) |
| R. Thomas (GB) | 23 | Contrôle 70 % (+2) | Garder (Gardien 100) |
| A. Roux, L. David, Robert | 25-26 | Contrôle / Contrôle / Passe 70 % (+2) | Garder (Conduite 100 plafonnée) |
| Moreau, M. David, Bonnet | 20-25 | Contrôle 70 % (+3 / +2 / +2) | Garder (Finition 100 plafonnée) |
| Enzo Roux, Thomas Roux, Thomas David | 16-17 | Défense 88 / Finition 85 / Gardien 92, 70 % (+3) | Garder |
| Jules Leroy, Lefebvre | 17-18 | Conduite 70 % (89 / 76, +3) | Garder |
| A. Thomas, T. Petit | 14 | Conduite 70 % (80 / 75, +3) | Garder |
| Étienne Roux (GB), Hugo Martin (GB) | 14-15 | Gardien 75 (+3) / Endurance 37 (+3) | Garder |
| Pierre Leroy | 32 | Défense 0 % (−2) | Garder (surplus, Forme 100) |

- **Les 11 titulaires ont leur compétence clé à 100** (plafond) : seul le Contrôle (2e compétence) a encore de la marge ; les 70 % ne coûtent que 0,6 point de rendement par semaine (Forme 94 → 92 le 06/11, ×0,982 → ×0,976) contre +2 à +3 de Contrôle. Garder.
- Jeunes à Forme 70 (Enzo Roux, Thomas Roux, Thomas David, Jules Leroy, Lefebvre) → 68 le 06/11 : ils ne sont pas titulaires, on ne touche à rien (décision du 24/10 confirmée).
- Alertes : Endurance ≤ 30 aucun ; ≤ 35 Adrien Thomas 35 et Étienne Roux (GB) 35 (pas de baisse en entraînement technique) ; Forme < 60 aucun ; 28 ans et + à haute intensité aucun. Étienne Roux (ATT) n'est plus à l'effectif (vendu).

## 2. Forme du onze des Cows pour Bresse (31/10 13:50)
**Écart : le onze n'est plus à 96 mais à 94 (−2 pour les 11, attendu à 70 %).** Les 11 enregistrés sont bien les 11 titulaires de `ts_effectif_bilan` (Romain Thomas, Simon, Dubois, Th. Thomas, Ounahi, A. Roux, L. David, Robert, Moreau, Bonnet, M. David) : tous Forme 94, aucun blessé ni suspendu (Adrien Roux 1 jaune). Valeur au match de leur compétence clé 100 : 98,2 (contre 98,8 à 96), soit −0,6 point par titulaire. La Forme ne bouge plus avant le 06/11 : rien à faire, la composition tient. Banc : Thomas David, Jules Leroy, Enzo Roux, Thomas Roux entrent à Forme 70 (compétence clé × 0,91 : 83,7 / 81,0 / 80,1 / 77,4).

## 3. Ben Ahmed Donkey (15858) — décision : un changement (García)
Nuit : seniors 82 → 80 (−2) ; jeunes 86 à 98 (−2). Gains : Müller +3 (Finition 91), J. Yamamoto +2 (89), Fernández +2 (85), Fournier/Taylor +2 (81), Abdel +2 (Gardien 83), Suzuki/Martínez +3 (Conduite 63/65), Kumar/Mansour/Schmidt +2, Girard/Hayashi/Ibe/Shimizu +1 (27-28 ans), García +3 (Contrôle), jeunes +3.
- **García** : seule modification (voir Actions). Test : `last_change` Défense = 3 et Défense 93 au relevé du 06/11 ; preuve que j'avais tort : Défense < 92.
- **Règle C-019 non déclenchée** : les titulaires sont à 80 (seuil ≤ 78 attendu au 06/11) → les titulaires restent à 70 % cette semaine. Müller et J. Yamamoto restent à 70 % tant que Finition < 95.
- Wilson, Shimizu (remplaçantes ATT, Passe 82 / 78, Finition 60) : garder faute de preuve qu'une autre compétence aide plus.
- Alertes : Endurance ≤ 30 aucune, mais **García 31** (marge 1, aucune baisse constatée en technique) ; ≤ 35 Takahashi 34, Kobayashi 36 (Endurance 70 %, +3 chacune) ; Forme < 60 aucune ; 28 ans et + : Hayashi, Ibe à 70 % (vente déjà décidée en amont).

## 4. HPC (TSCredits) — décision : pas d'urgence, choix Premium pour l'utilisateur
Faits (page HPC capturée le 29/10 14:20 UTC, `bronze.raw_pages` ; `gold.ts_hpc_status` est périmée, as_of 19/10) : **50 TSC sur le compte, 0 investi cette saison, 5 semaines restantes, aucun paiement**. Règles [skill entraînement, F:2026-10-10 Admin-Dev] : paiement unique par semaine (0/10/25/50), ouvert le lundi 00:00, **minimum 50 TSC investis pour recevoir le jeune**, aucun remboursement, un seul jeune HPC par saison et par club.
- « 50 manquants pour 50 » est faux pour le seuil : le compte a 50, **un seul paiement de 50 suffit**. Il manque seulement la décision.
- Il me manque : si les 50 TSC sont partagés entre les deux clubs (le champ `account_tsc` laisse penser que oui) et quel club l'export HPC du 29/10 montrait. On l'obtient : ouvrir la page HPC de chaque club et noter « Vos TSCredits ».
- Avis (confiance faible) : si l'utilisateur veut dépenser, c'est **Ben Ahmed** qui en profite le plus (milieu titulaire à 59-65 en Conduite ; les Cows ont déjà 100 à tous les postes clés), compétences à choisir : Conduite, Contrôle, Endurance. Le paiement se fait dans la semaine en cours (fenêtre ouverte depuis lundi 26/10) ; comme l'utilisateur n'agit que le jour même, c'est ce soir ou jamais pour cette semaine.

## Conseils suivis (`learnings.md`)
- C-033 : appliqué (titulaires Cows 94, jeunes 70, Étienne Roux ATT absent) ; critère « jeunes à 72 → 70 » vérifié.
- C-017 : confirmé (Leroy, Lefebvre, A. Thomas +3 en Conduite ; Bonnet, A. Roux, R. Thomas +2 en Contrôle). C-018 : Schmidt Conduite 62 (+2), critère ≥ 69 au 13/11 reste ouvert.
- C-019, C-021 : ouverts (Forme Donkey 80, seuil 78 au 06/11 ; Pierre Leroy −2 Défense, Forme 100).
- Nouveau C-051 : García Défense 70 %.
