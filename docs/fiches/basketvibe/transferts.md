# BasketVibe — fiche Transferts

Lue par l'agent `transferts` après `commun.md`. Contenu repris de l'agent BasketVibe validé (checklist BasketVibe, partie E).

## Skills à lire
- `.claude/skills/basketvibe-transferts/SKILL.md`
- `.claude/skills/basketvibe-economie/SKILL.md` (salaires, solde)
- `.claude/skills/basketvibe-communaute/SKILL.md` (prix constatés)
- `.claude/skills/basketvibe-entrainement/SKILL.md` (âge, potentiel)

## Règles propres au jeu
1. **Prix de référence, du plus fiable au moins fiable** :
   - `gold.bv_market_price_known` : ventes conclues dont on connaît le PS (peu nombreuses) ;
   - `gold.bv_market_price_ref` : médiane et quartiles par âge et poste sur 21 jours, compétences inconnues, donc très dispersés ;
   - prix constatés sur Discord [Com].
   Dis toujours combien de ventes comparables tu as. Avec moins de 5, la confiance est faible.
2. **Argent** : la somme des enchères maximales en cours ne peut pas dépasser le solde [M§10.3]. Lis `gold.bv_finance_projection` (solde, projection de fin de saison) avant de conseiller un achat. Compte le **salaire hebdomadaire** de la recrue (`est_weekly_salary`, barème [M§10.2]), pas seulement le prix.

## Données
- `gold.bv_market_candidates` : joueurs en vente au dernier export du marché. PS, moyenne des compétences, meilleur emplacement (`best_slot`, `best_fit`, taille comprise), `would_rank_in_slot` (son rang parmi mes joueurs à cet emplacement), `enters_top8` (fait-il monter le TS [M§2.2]), salaire estimé, statut d'âge, prix actuel, nombre d'enchères, fin de l'enchère (heure de Paris), médiane des ventes comparables, et les 8 compétences.
- `gold.bv_sell_candidates` : mes joueurs. Âge, PS, salaire, potentiel estimé (`gold.bv_potential_estimate`), projection (`trend_s3`, `ps_s1`, `ps_s2`), minutes en ligue sur les 4 derniers matchs, rang à leur meilleur emplacement, déjà en vente ou non, alerte d'âge, `available_players` (il en faut 9 pour vendre [M§11.1]).
- `gold.bv_slot_fit` et `outputs/basketvibe/briefs/*-tactique.md` (dernier) : la rotation réelle (unité A, unité B, banc). Une recrue n'a d'intérêt que si elle **entre dans la rotation** ou **comble un trou** (ex. : 2e intérieur remplaçant au PF / C, voir le plan B du brief tactique).
- `silver.bv_transfers` / `silver.bv_transfer_auctions` : détail si besoin.

## Livrable
### 1. Joueur donné ou marché du jour (case E13)
Pour chaque joueur étudié (celui demandé, ou les 3 à 5 meilleurs du marché pour mon effectif) :
- **Intérêt** : quel emplacement, quelle unité, qui il remplace, gain de `fit`, effet sur le TS, âge (progression ou déclin [M§8.5]).
- **Prix** : correct, cher ou bonne affaire, d'après les références (règle 4), avec le nombre de comparables.
- **Enchère maximale conseillée** : le montant et son calcul. Rappelle le mécanisme : enchère maximale automatique, anti-snipe de 3 min, phase finale à l'aveugle, prix final = de quoi battre le 2e maximum [M§11.3]. Signale l'heure de fin.
- **Coût total** : prix + salaire × semaines restantes, plus la saison suivante.
- Les joueurs libres partent à 10 000 [M§11.4] : souvent le meilleur rapport qualité-prix pour un remplaçant.

### 2. Joueurs à vendre et moment de la vente (case E14)
Classe mes joueurs : **vendre maintenant**, **vendre en fin de saison**, **garder**. Critères :
- l'âge (29 : dernière saison de progression ; 30 : plus rien ; 31+ : déclin chaque semaine [M§8.5]) ;
- le potentiel (un jeune à potentiel élevé ne se vend pas) ;
- la place dans la rotation et le salaire par point de PS ;
- la valeur de marché.
**Moment** : la vente dure environ 2 jours et ne s'annule pas ; garder 9 joueurs disponibles ; la taxe est de 5 % [M§11.1]. Tiens compte du calendrier (matchs à jouer, maintien) et de la fin de saison (salaires recalculés, +1 an [skill saison]).

### 3. Conseils suivis
Ajoute chaque achat ou vente conseillé dans la section Conseils de `outputs/basketvibe/learnings.md` (ID `C-nnn`, critère vérifiable : joueur présent ou absent de `gold.bv_roster_now`, `on_transfer_list`).

## Sortie propre au jeu
- En tête du brief : les **actions à faire** (enchère, montant maximum, heure limite ; mise en vente, prix de départ).
- Si l'export du marché date de plus de 24 h, demande un nouvel export (les enchères bougent vite).
