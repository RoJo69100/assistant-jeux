# Priorités pour faire progresser Chomelix Cow

Sources : skills sixzeroleague-joueurs, -match, -entrainement, -club, -communaute ; briefs du 2026-10-20 ; `learnings.md`. L'ordre est un **avis** : du moins cher au plus cher, du plus sûr au moins sûr. Le jeu est en alpha et les résultats restent très aléatoires [Dev chat] : aucune conclusion sur 3 matchs.

## 1. Une composition valide et des remplaçants (gratuit)
- La composition enregistrée sert à tous les matchs [W:Match] ; un remplaçant par rôle [W:Injuries]. Moins de 7 joueurs aptes = forfait 15-0 [W:Competitions].
- Hors poste = pénalité sur les compétences d'attaque, de défense et de gardien, pas sur le physique ; ampleur **non documentée** (« légère », non chiffrée) [W:Attributes].
- [Obs 2026-10-20] LW (Lefebvre) et RB (Roger) n'ont aucun remplaçant naturel ; les autres rôles en ont un (`gold.sz_lineup_natural`). Arrières et pivots sont bien plus exposés aux blessures que les ailiers [W:Injuries] : le RB sans doublure est le risque le plus réel (avis).

## 2. Le focus d'entraînement (gratuit, effet mesuré)
- « Le focus bat la dispersion » [W:Training]. Viser les compétences clés du rôle où le joueur joue (voir profils-roles.md). Plafond 100 ; sans plafond caché [W:Attributes].
- L'éthique de travail (1 à 100, fixe) décide du rendement [W:Training]. [Obs 2026-10-20] sur la compétence ciblée : environ 1,4 à 1,8 point par cycle à éthique 61-78, 0,7 à éthique 2-5 (`silver.sz_player_cycles`) ; le skill ne chiffre pas de rendement.
- Intensité d'équipe Light, Normal, High : plus haut = progrès plus rapides mais plus de blessures et plus longues (~3 matchs, parfois 6) [W:Training, Injuries]. Gain de High : **non documenté**. Brief du 2026-10-20 : rester en Normal (effectif de 12, deux rôles sans doublure).
- Les jeunes (≤ 20 ans) ont le bonus complet [W:Training] : c'est ainsi qu'un petit club rattrape un riche.

## 3. Les transferts (peu d'argent, forte variance)
- Prix de départ 1 000 €, palier 1 000 €, frais de mise en vente 500 € non remboursés [W:Transfers]. Le salaire se compte en plus du prix (revu entre les saisons [W:Finances]).
- Prix constatés [Obs 2026-10-18, un seul export, aucun prix final] : joueurs de champ de note 11 à 13 vus entre 4 000 et 6 000 € ; notes 7 à 9 souvent invendues. Indice faible.
- Un naturel à note égale vaut plus qu'un hors-poste, la note de rôle étant calculée avant la pénalité [Obs SQL 2026-10-18].
- Éviter les 33 ans et plus : retraite possible [W:Retirement] ; un joueur qui annonce sa retraite ne peut plus être vendu [W:Transfers].

## 4. L'argent et les infrastructures
- Les salaires sont le poste principal de dépenses et ne changent qu'entre les saisons ; l'entraînement les augmente pour la saison suivante [W:Finances].
- **Arena et Fan Shop sont les seules infrastructures qui rapportent** ; le coût monte plus vite que le revenu [W:Infrastructure]. Le jeu affiche les semaines de remboursement du niveau suivant [W:Infrastructure].
- [Obs 2026-10-20] Remboursement estimé (`gold.sz_infrastructure_payback`) : Fan Shop 7 en 10,8 à 27,7 cycles, Arena 7 en 18,5 cycles. Brief Finances : Fan Shop 7, pas l'Arena 7, avec une réserve de 5 500 € (avis). Aucun des deux ne se rembourse avant la fin de la saison.
- Le sponsor se choisit entre deux saisons ; re-signer le même sponsor fait perdre la prime de signature [Dev chat]. Le meilleur choix dépend du nombre de victoires attendues (calcul du brief Finances, à refaire à l'intersaison avec les offres réelles).
- Training Facilities : plus de progression et emplacements de formation de rôle aux niveaux 5, 10, 15, 20 ; Youth Academy : meilleurs prospects [W:Infrastructure]. Rendement chiffré : `silver.sz_infrastructure_levels` ; retour sur investissement **non calculé**.

## 5. Former un 2e rôle (lent)
- 2 saisons (36 journées), 3 rôles au maximum, 150 € par cycle observé, annulation sans remboursement ; le joueur garde ses rôles [W:Training, Dev chat, Obs API 2026-10-18]. Le rôle de départ est définitif [Com chat, Fundador23].
- [Obs] Un seul emplacement ouvert (Training Facilities 6) : Blanc, gardien, apprend RW. Brief Entraînement : ne pas y toucher ; candidats futurs pour RB puis LW, confiance faible.

## 6. La relève U18
- Elle sert surtout à remplacer les retraités [W:U18]. Signer un prospect donne un joueur de 18 ans complet, mais il doit encore s'entraîner pour progresser [W:U18]. Compétences dévoilées avant signature : 2 / 4 / 6 / 8 aux niveaux d'académie 3 / 8 / 13 / 18 [W:U18].
- Effectif de 30 au maximum [W:U18, Transfers]. Aucun retraité à anticiper cette saison [Obs 2026-10-20].

## Discipline (à surveiller, non prouvé)
Marquage d'abord, puis Anticipation et Duels, réduisent fautes et exclusions [Com chat, Antarez ; W:Attributes]. [Obs] Exclusions en ligue : 15 contre 13 pour l'adversaire sur 3 matchs, sans lien démontré avec le résultat (L-002).
