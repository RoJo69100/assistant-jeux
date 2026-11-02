# BasketVibe — fiche Finances et personnel

Lue par l'agent `finances` après `commun.md`. Contenu repris de l'agent BasketVibe validé (checklist BasketVibe, partie E).

## Skills à lire
- `.claude/skills/basketvibe-economie/SKILL.md`
- `.claude/skills/basketvibe-saison/SKILL.md` (calendrier, fin de saison)
- `.claude/skills/basketvibe-joueurs/SKILL.md` (blessures, forme : effet du personnel)
- `.claude/skills/basketvibe-communaute/SKILL.md` (conseils sur le personnel, revenus des amicaux)

## Règles propres au jeu
1. Les projections reposent sur des **hypothèses écrites en tête de `sql/gold/007_bv_finance.sql`** : rappelle-les.
2. Arrondis à 1 000 près dans le texte.

## Données
- `gold.bv_finance_health` : semaine type actuelle. Solde, popularité, charges fixes (salaires, personnel, académie), recettes récurrentes estimées (sponsor, billetterie : 11 matchs à domicile sur 8 semaines, un amical à domicile par jour, homegrown), résultat hebdomadaire estimé, part des salaires dans les recettes, argent disponible et engagé dans les enchères.
- `gold.bv_finance_season_rates` : cumul de la saison par catégorie (résumé du jeu) et nombre de dimanches de paie écoulés, d'où les moyennes par semaine réelles.
- `gold.bv_finance_weekly_result` : résultat par semaine à partir des transactions. Seules les 20 dernières transactions sont visibles à chaque export : signale-le si une semaine est incomplète (`complete` = false).
- `gold.bv_finance_projection` : fin de la saison en cours. `gold.bv_finance_s2_projection` : saison 2 (8 semaines), prime de classement si le rang est conservé, réserve de sécurité (2 semaines de charges), `investable_now_end_s1` (ce qu'on peut engager sans passer sous la réserve).
- `gold.bv_personnel_status` : postes occupés, coût, effet unitaire et effet actuel.
- `gold.bv_sell_candidates` / `gold.bv_market_candidates` : salaires des joueurs et des recrues possibles. Brief transferts du jour pour les enchères en cours.
- `silver.bv_finance_transactions` : détail (type de recette ou de dépense).

## Livrable
### 1. Alerte (case E15)
- **Le club perd-il de l'argent ?** Sur la dernière semaine complète et sur la semaine type. Si oui, la **cause** : la catégorie qui a le plus bougé (salaires après des recrues, billetterie en baisse avec la popularité, amicaux non programmés, homegrown perdu…), chiffrée.
- Signale aussi les risques à venir : enchères engagées, salaires recalculés en fin de saison [M§10.2], popularité basse.

### 2. Masse salariale (case E16)
- Salaires / recettes récurrentes (`salaries_pct_of_income`) et résultat hebdomadaire. Soutenable si le résultat reste positif sans compter les ventes de joueurs. Dis jusqu'où elle peut monter (en salaire hebdomadaire supplémentaire) avant que la semaine type passe dans le rouge.
- **Homegrown** [M§10.1.3] : 200 par minute de ligue des juniors de l'académie (plafond 40 000 par semaine). Chiffre ce que rapporteraient ou coûteraient leurs minutes dans la rotation de l'agent Tactique.

### 3. Capacité d'investissement (case E17)
- Ce qu'on peut engager **maintenant** (enchères) et **en saison 2** (académie, personnel, recrues), en gardant la réserve de sécurité.
- Académie : relis `.claude/skills/basketvibe-academie/SKILL.md` pour le rapport entre investissement et progression de la jauge. Ne recommande pas de montant sans cette règle.

### 4. Personnel poste par poste (case E18)
Pour médecins, kinés, psychologues et marketing : **recruter, garder ou virer**, avec le coût hebdomadaire, le gain attendu (règle [M§4.3]) et le moment.
- Facturation au maximum de la semaine [M§4.3].
- Les kinés comptent au coup d'envoi ; les médecins peuvent être embauchés après une blessure [Dev 2026-09-14].
- Les psychologues n'agissent que le dimanche (tirage de forme) ; la forme est remise à 6 en début de saison [M§5.5].
- Le marketing réduit la perte de popularité en cas de défaite à domicile [M§10.1.1] : à mettre en rapport avec les matchs à domicile restants.

### 5. Conseils suivis
Ajoute chaque conseil dans la section Conseils de `outputs/basketvibe/learnings.md` (ID `C-nnn`, critère vérifiable : `gold.bv_personnel_status`, `gold.bv_finance_health`).

## Sortie propre au jeu
- Fichier : `outputs/basketvibe/briefs/AAAA-MM-JJ-finances.md`.
- En tête du brief : **l'alerte** (ou « pas d'alerte ») et les **actions** (personnel à embaucher ou renvoyer, avec la date ; plafond d'enchères).
- Si l'export Finances date de plus d'une semaine, demande-le.

## Données manquantes enregistrées (2026-10-26)
- Jauge d'académie, personnel, solde et masse salariale des 11 autres clubs : absents des exports (`standings[]` : rang, force, `manager_*`). À réunir : demander dans le Discord (academy/general), consigner dans `outputs/basketvibe/veille/connaissance.md` (thème finances/académie, daté).
- Facturation du personnel : maximum atteint dans la semaine entre deux prélèvements du dimanche 02:30 (observé le 25/10 : 85 000 pour 2 marketing virés le 18/10 après 02:30 + 4 kinés). Virer avant 02:30 pour économiser la semaine suivante.
- `gold.bv_finance_projection` double-compte le match à domicile du jour tant que `bv_fixtures` garde le match « scheduled » : recalculer à la main (solde actuel + prime) en attendant.
