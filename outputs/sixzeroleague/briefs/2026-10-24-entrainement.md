# Six Zero League — brief Entraînement, 2026-10-24 (cycle 6 réglé à 22:13 Paris ; prochain cycle le 25 au soir)

Briefs amont lus : Match, Effectif, Finances-personnel, Académie (2026-10-24). Sources : `gold.sz_training_progress`, `silver.sz_player_cycles` (après cycle 6, 2026-10-24 20:13 UTC), `silver.sz_players` (export du 2026-10-24 20:15 UTC), `silver.sz_training_plan`, `silver.sz_role_training`, `gold.sz_role_report`. Règles : skill `sixzeroleague-entrainement` [W:Training, W:Injuries], `sixzeroleague-joueurs` [W:Attributes].

## En tête
- **Il me manque : le plan saisi après le cycle 6.** Le dernier relevé du plan (`/teams/mine/training`) et de la formation de rôle date du 2026-10-23 12:39 UTC ; l'export du 24 n'a apporté que le rapport (`/training/report`, 20:15 UTC). On le réunit comme ça : ouvrir Équipe → Training et vérifier à l'écran les 15 lignes (surtout Blanc, voir plus bas), puis ré-exporter la page.
- **Un seul changement à saisir : Blanc passe en Gardien / Handling.** Les 14 autres lignes et l'intensité ne bougent pas.
- **Date limite : avant 21:00 Paris le 25/10** (le cycle se règle après le match de 21:00 [Dev chat]).
- **Verdict C-007 (brief du 23)** : Barros (Technique) appliqué (15→16 au cycle 6) ; formation de Blanc annulée (emplacement 1 sans joueur au relevé du 23) ; **focus de Blanc non appliqué** : au cycle 6 il a encore gagné Contrôle du ballon 11→12 (0 point clé de gardien, 5 points sur 5 cycles).

## Fiche de saisie (avant 21:00 Paris le 25/10)
| Réglage | Valeur | Action |
|---|---|---|
| Intensité d'équipe | Normal | Garder |
| Sébastien Blanc (GK, 26) | Gardien / Handling | **Changer** (était Attaque / Contrôle du ballon) |
| Formation de rôle | emplacement 1 libre | Ne rien lancer (voir § 4) |
| Les 14 autres | inchangés (tableau § 2) | Garder |

## 1. Intensité : Normal (confiance moyenne)
- Faits : 15 joueurs, 0 blessé, 0 suspendu, 2 joueurs par rôle (briefs Effectif). CB le plus mince : Simon 10, Denis 8, aucun troisième CB (`gold.sz_role_report`). Cycle 6 : 12 points dont 11 sur des compétences clés (`gold.sz_training_progress`).
- Règle : High = progrès plus rapides mais blessures plus nombreuses et plus longues (~3 matchs, parfois 6) ; un club qui s'entraîne dur a besoin d'un effectif plus profond [W:Training, W:Injuries]. Le skill ne chiffre pas le gain de High.
- Avis : Normal. Une blessure de Simon (CB) laisserait Denis 8 seul au poste ; les 6 exclusions de J11 n'ont pas de lien connu avec l'intensité. Light n'a pas de raison d'être : personne à ménager.

## 2. Verdict par joueur (cycle 6, `gold.sz_training_progress`, `silver.sz_players`)
Âge : bonus jusqu'à 20 ans, nul à 25, baisse dès 28, déclin physique dès 30 au changement de saison, saison suivante vers le 27/10 [W:Training]. Le skill ne donne aucun chiffre ; la progression fractionnaire est celle de `silver.sz_players.training_progress`.
| Joueur (rôle, âge, éthique) | Focus saisi (relevé du 23) | Cycle 6 | Point suivant | Verdict |
|---|---|---|---|---|
| Simon (CB, 19, 22) | Attaque / Passe | Passe 5→6 | Passe 0,98 | Garder (bonus jeune, CB le plus mince) |
| Denis (CB, 26, 3) | Attaque / Passe | 0 | Passe 0,80 | Garder |
| Bourgeois (GK, 30, 26) | Gardien / Placement | 0 | Placement 0,86 | Garder (déclin physique au changement de saison, ses clés de but ne sont pas physiques) |
| **Blanc (GK, 26, 48)** | Attaque / Contrôle du ballon | Contrôle du ballon 11→12 (hors clé) | Prise de balle 0,57 ; Réflexes 0,57 | **Changer : Gardien / Handling** |
| A. Bertin (LB, 26, 32) | Attaque / Passe | Passe 12→13 | Passe 0,39 | Garder |
| Leroy (LB, 24, 29) | Attaque / Tir | Tir 10→11 | Tir 0,35 | Garder |
| Roger (RB, 27, 78) | Attaque / Passe | Passe 12→14 (2 points) | Passe 0,51 | Garder, meilleur rendement |
| Barros (RB, 30, 24) | Attaque / Technique | Technique 15→16 | Technique 0,32 | Garder (appliqué, effet visible) |
| Lefebvre (LW, 27, 2) | Attaque / Tir | Tir 17→18 | Tir 0,50 | Garder (28 ans à la prochaine saison : baisse du gain) |
| Sundberg (LW, 29, 28) | Attaque / Tir | 0 | Tir 0,95 | Garder (point imminent ; 30 ans à la prochaine saison) |
| Dupont (RW, 18, 1) | Attaque / Tir | Tir 20→21 | Tir 0,74 | Garder |
| G. Bertin (RW, 25, 61) | Physique / Vitesse | Vitesse 14→15 | Vitesse 0,65 | Garder |
| Lemaire (RW, 22, 19) | Attaque / Tir | Tir 13→14 | Tir 0,38 | Garder |
| Benoit (P, 19, 40) | Attaque / Tir | Tir 7→8 | Tir 0,77 | Garder (bonus jeune) |
| Chevalier (P, 24, 5) | Physique / Force | 0 | Force 0,91 | Garder (point imminent) |
- Les 14 joueurs hors Blanc suivent leur focus : 11 points sur 11 clés au cycle 6, aucun focus mal choisi par rapport au rôle. Sans point ce cycle : Denis, Bourgeois, Sundberg, Chevalier, avec 0,80 à 0,95 en réserve sur leur focus : ce n'est pas un retard.
- Éthique : non modifiable [W:Training], pas un motif de changer un focus (Lefebvre 2 gagne autant que Roger 78 sur ce cycle).

### Blanc : Gardien / Handling (confiance moyenne)
- Faits : 5 points sur 5 cycles en Contrôle du ballon (5→12), tous hors clés de gardien ; clés actuelles Handling 8, Un contre un 14, Réflexes 15, Placement 4, Relance 4 (`gold.sz_role_report`). Il est GK2 (note 9) derrière Bourgeois 11, 30 ans.
- Règle : le focus bat la dispersion ; une compétence ciblée gagne son point plus vite [W:Training]. Pas de rendement décroissant : choisir une compétence parce qu'elle est basse ne la rend pas moins chère [Dev chat 2026-10-19]. Le skill ne dit pas quelle clé pèse le plus dans la note.
- Choix : Handling parce que c'est une clé de GK où il a déjà 0,57 de progression (avec Réflexes, 0,57) : le point arrive au plus tôt. Alternative équivalente : Réflexes. Confiance moyenne : c'est le gardien de relève (Bourgeois 30 ans), la progression de sa note compte pour les 2 prochaines saisons.

## 3. CB le plus mince et 6 exclusions de J11
- CB : Simon 10 (19 ans), Denis 8 (26 ans). Le rôle ne se renforce pas par l'entraînement ce soir : Simon gagne déjà un point de Passe par cycle (4→5→6), Denis a 0,80 sur sa Passe. On ne les change pas.
- Exclusions : Simon 9 en 12 apparitions (0,75), Dupont 3 en 4, Leroy 4 en 3 (1,33), Lemaire 7 en 8 (brief Effectif). Règle : Marquage et Duels = moins de fautes [W:Attributes] ; Contrôle du ballon = moins de fautes de zone et techniques. Simon : Duels 20, Contrôle du ballon 19, **Marquage 6** ; Leroy : Marquage 1, Duels 15.
- Décision : **garder Simon sur Passe ce cycle** (Passe 0,98 : le point de la semaine est quasi acquis, c'est une clé de CB). Au rapport du 25 au soir, si Simon est à Passe 7, **passer Simon sur Défense / Marquage** (cycle du 26) et mesurer ses exclusions sur 3 matchs. Confiance faible : un point de Marquage ne garantit aucun effet chiffrable ; aucun skill ne donne l'ampleur [Com chat, Antarez : Marquage puis Anticipation et Duels]. Leroy (LB2) : ne pas changer, 3 apparitions seulement.

## 4. Formation de rôle (emplacement 1 libre, 150 par cycle)
- Faits : Training Facilities 6, emplacement 1 libre, 2e à 10 (`silver.sz_role_training` du 2026-10-23, pas de relevé plus récent). Durée 36 journées soit 18 cycles = 2 saisons, ~2 700 au total ; annuler ne rembourse rien ; le rôle de départ est définitif [W:Training, Dev chat]. Solde 6 645, cycle à +3 133 (brief Finances).
- Candidat unique : Gilbert Lemaire (RW3, 22 ans), CB 10 avant pénalité contre 8 pour Denis (`silver.sz_players.role_overalls`) ; Roger et Barros sont CB 11 mais jouent RB/RB2 et déclinent (27, 30 ans).
- **Décision : ne pas lancer.** Raisons : (1) la note 10 est avant la pénalité de hors-poste (commun.md) : la formation ne vaut que quand elle finit, en saison 4, et le gain est de 1 à 2 points sur le CB2 seulement ; (2) c'est le même raisonnement que celui qui a fait annuler la formation de Blanc le 23 ; (3) le brief Finances ne conseille aucune dépense non rentable cette saison. À rouvrir seulement si Simon est blessé deux fois ou si l'académie ne livre aucun CB après J14.

## 5. Conseils suivis
- C-007 : statut mis à jour (Blanc non appliqué, le reste appliqué).
- C-016 ajouté dans `outputs/sixzeroleague/learnings.md` (Blanc Gardien / Handling ; Normal ; pas de formation).

## Limites
- Plan saisi après le cycle 6 non relevé (voir En tête). Gain de High et montant du déclin à 30 ans inconnus du skill ; pas de potentiel caché dans le skill : aucune estimation.
