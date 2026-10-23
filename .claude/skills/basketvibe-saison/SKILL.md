---
name: basketvibe-saison
description: Règles BasketVibe du calendrier et de la compétition — rythme de la semaine (matchs, entraînement, académie, salaires), ligue de 12, classement et départages, promotion/relégation, coupes, amicaux, fuseaux horaires. À charger pour toute question « quand », « combien de matchs », « qui monte/descend », ou pour planifier la routine.
---

# BasketVibe — saison, calendrier, compétitions

Sources : **[M§x]** = manuel officiel https://www.basketvibe.com/guide, lu en entier le 2026-10-16 (copie locale `data/manual/basketvibe/guide-2026-10-16.md`). **[Obs]** = constaté dans nos données bronze. Ne rien affirmer qui ne soit pas ici ou dans une source citée.

## Rythme de la semaine
| Quand | Quoi | Source |
|---|---|---|
| Lun, Mer, Sam 19:45 (heure de la ligue) | Verrouillage de la tactique du match (15 min avant) | [M§1.3] |
| Lun, Mer, Sam 20:00 | Matchs de ligue, puis diffusion live ~48 min | [M§1.1, §1.3] |
| Jour d'amical 07:45 / 08:00 (fuseau de l'hôte) | Verrouillage / coup d'envoi amical | [M§1.3] |
| Jeudi 09:00 | Jour de l'académie : investissement débité, force mise à jour, nouveau rapport du scout | [M§1.3, §4.2] |
| Dimanche minuit (calendrier mondial, même instant partout) | Entraînement, salaires, sponsor, bonus homegrown, forme | [M§1.3] |
| Chaque minuit | Récupération de la fatigue | [M§5.6] |

- Europe = heure d'Europe centrale [M§1.3].
- [Obs] Les entraînements de recent-runs sont horodatés dimanche 02:00 UTC = 04:00 à Paris (6 semaines vérifiées le 2026-10-16). La « minuit du calendrier mondial » ne correspond donc pas à minuit à Paris.

## Ligue et saison
- 12 équipes par ligue, 22 journées, un match par journée, ~8 semaines réelles [M§2, Intro].
- Points : victoire 2, défaite jouée 1, défaite par forfait 0. Pas de match nul (prolongations jusqu'à un vainqueur) [M§2, §9.1].
- Forfait = victoire 20–0 pour l'adversaire si un club ne peut aligner 5 joueurs éligibles ; ni fatigue, ni expérience, ni play-by-play [M§9.1].
- Départage à égalité de points, dans l'ordre : confrontations directes (bilan V-D puis différence de points entre les clubs à égalité, réappliqué au sous-groupe) → différence de points sur la saison → points marqués → points encaissés (moins = mieux) → ancienneté du club → étape déterministe [M§2.1].
- Échelle régionale : 1 ligue tier 1, 4 en tier 2, 16 en tier 3 [M§2.1].
- Fin de saison : 4 promus (vainqueur de chacune des 4 ligues filles), 4 relégués (places 9 à 12), répartis par tirage au sort entre les ligues filles [M§2.1].
- Primes de classement en fin de saison : voir basketvibe-economie [M§10.1.4].
- Inactivité 45 jours → compte fermé au changement de saison [M§2.1].
- Nouvelle saison : forme remise à 6, fatigue à 0, popularité à 70 %, salaires recalculés, +1 an d'âge, retraite à la fin de la saison des 38 ans [M§5.5, §5.6, §10.1.1, §10.2, §4].

## Fin de la saison 1 → saison 2 (dates 2026)
- **Dernière journée de ligue : lundi 26/10.** Le changement de saison a lieu **dans la nuit du 26 au 27/10** ; les ligues neuves sont visibles **mardi 27/10** [Dev 2026-10-18 et 2026-10-22, general : « Last round is on Monday and season rollover will happen in the night. So Tuesday we will have fresh leagues » ; Dev 2026-10-10 : « le changement de saison a lieu le jour de la dernière journée »]. ⚠️ Une réponse du dev du 2026-10-10 (« Yes ») à une question qui plaçait le changement au dimanche 1/11 est ambiguë ; les messages du 18 et du 22/10 tranchent.
- **Une semaine sans match de ligue** ensuite ; premier match de la saison 2 un lundi, donc **lundi 02/11** (déduit : « toujours un lundi » [Dev 2026-10-18]). Le dev prévoit des **coupes nationales rapides à matchs quotidiens pendant cette pause** (8 ou 16 équipes par pays ; les autres dans une « other-cup » ; l'automatisation reste à écrire) [Dev 2026-10-18 et 2026-10-20, general]. Règles de fatigue et d'expérience de ces coupes : inconnues, voir l'annonce de l'édition [M§3.3].
- Forme et fatigue repartent à 6 et 0 [Dev 2026-10-22, general ; M§5.5, §5.6]. **L'académie ne se remet pas à zéro** [Dev 2026-10-18, general]. Tout le monde prend +1 an au changement de saison [M§4].
- Conséquences pour la semaine : le **dimanche 25/10** est le dernier entraînement de la saison 1 (un joueur de 29 ans y progresse encore ; il aura 30 ans ensuite et ne progresse plus [M§8.5], déduction) ; le **jeudi 29/10** est le premier rapport d'académie de la saison 2 (le dernier de la saison 1 était le jeudi 22/10 [Com 2026-10-22/23, grillanza, italia ; non confirmé mot pour mot par le dev]). Les salaires sont recalculés en fin de saison [M§10.2] : date exacte du premier prélèvement recalculé non documentée.
- Ménage entre les saisons : comptes inactifs (45 jours) retirés (~100 sur ~600) ; les 2es des ligues inférieures comblent les places vides, force d'équipe pour départager s'il manque une place [Dev 2026-10-11 et 2026-10-18, general]. 2 promus au lieu d'1 : en discussion, rien de décidé.

## Indicateurs de force
- **PS** (force joueur), **TS** (moyenne PS des 8 meilleurs du roster de 12, blessés compris), **LH** (moyenne des TS de la ligue sans le club le plus faible). Détail des poids dans basketvibe-joueurs [M§2.2].
- La barre de chances avant match (Club → Next game) utilise les 8 meilleurs disponibles, la forme récente et l'avantage du terrain, sans la tactique. Ce n'est pas le TS [M§2.2].

## Coupes
- Élimination directe, réservées aux clubs humains, inscription automatique. Les plus forts (TS) sont exemptés du 1er tour si le nombre d'équipes n'est pas une puissance de 2 [M§3.2].
- **Le plus faible reçoit** [M§3.2].
- Règles par défaut : pas de prime de match, pas de billetterie, pas de blessure, **ni fatigue ni expérience** — sauf si l'édition l'annonce autrement (Inbox → BasketVibe) [M§3.3].

## Amicaux
- Hors classement. Expérience et fatigue ≈ **1/10** d'un match de ligue pour les mêmes minutes. **Aucune blessure.** Même recette billetterie pour les deux clubs (≈ 6 % d'un match de ligue à domicile), popularité inchangée [M§1.2, §10.1.1].
- Maximum 10 amicaux programmés. Annulation possible jusqu'à 48 h avant [M§1.2].
- Usage typique selon le manuel : tester des compositions et des tactiques sans risque [M§1.2].

## Matchs (structure)
- 4 quart-temps, possessions alternées calibrées pour 48 minutes. Fin de match serrée (≤ 6 points au 4e QT ou en prolongation) jouée comme un vrai finish (fautes volontaires, tirs à 3) [M§9.1].
- 6 fautes personnelles = exclusion. Bonus d'équipe : une fois la 5e faute d'équipe du quart-temps atteinte, les fautes suivantes envoient l'adversaire aux lancers. Avant, environ la moitié des fautes sur tir sont des fautes de tir (lancers), les autres des fautes simples [M§9.2, §6.3].
- Le classement, la popularité et la billetterie se mettent à jour après la fenêtre live [M§9.5].
- Variance : un match isolé peut surprendre ; les tendances se lisent sur plusieurs matchs [M§9.8].
