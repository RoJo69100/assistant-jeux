# Six Zero League — fiche Finances, sponsor et infrastructures

Lue par l'agent `finances` après `commun.md`. Cases E7 (finances, sponsor) et E8 (infrastructures) de la checklist SixZero League. **Pas de personnel dans ce jeu** : la partie personnel de l'agent devient « infrastructures ».

## Skills à lire
- `.claude/skills/sixzeroleague-club/SKILL.md` (finances, sponsor, infrastructures)
- `.claude/skills/sixzeroleague-match/SKILL.md` (multiplicateurs par division, primes de ligue et de coupe)
- `.claude/skills/sixzeroleague-communaute/SKILL.md` (§ 4 : re-signer = pas de prime de signature)

## Règles propres au jeu
1. Un cycle (2 journées) = une « semaine » financière ; 9 cycles par saison, environ 1 match à domicile par cycle ; hors saison, ni recettes ni entretien. Ce sont les hypothèses en tête de `sql/gold/013_sz_gold.sql` : rappelle-les.
2. Salaires revus seulement entre les saisons : les progrès de l'entraînement alourdissent la masse salariale de la saison suivante [W:Finances].
3. Sponsor : règles du skill club § Sponsor ; prime de signature perdue si on re-signe le même [Dev chat].
4. Infrastructures : seules l'Arena et le Fan Shop rapportent ; coûts et entretien suivent la division [W:Infrastructure]. Training Facilities et Youth Academy se jugent sur la progression et la relève, pas en remboursement.
5. Fan Shop : 1,6 × (leader) à 0,7 × (dernier) selon le classement [Dev chat, devlog 0.5.7] : la projection doit dépendre de la place en ligue. Les coûts de niveau sont cachés volontairement ; ne les déduis que de `silver.sz_infrastructure_levels`. Training Facilities +0,04 par niveau : incertain [Dev chat, 2026-10-19].

## Données
- `silver.sz_finances` : par jour, `balance`, sponsor actuel (`sponsor_weekly`, `sponsor_win_bonus`, `sponsor_can_choose`, `sponsor_offers`), prévision du cycle (`fc_revenue`, `fc_expenses`, `fc_wages`, `fc_net`, `fc_home_fixtures`), dernier rapport (`last_week`, `last_net`, `last_report`).
- `silver.sz_infrastructure_levels` : chaque niveau des 4 installations (effet, entretien, coût depuis le niveau actuel, déblocage).
- `gold.sz_infrastructure_payback` : Arena et Fan Shop, 4 niveaux au-dessus de l'actuel, gain net par cycle (min / max) et cycles de remboursement (`payback_cycles_best`, `payback_cycles_worst`).
- `gold.sz_finance_cycles` : résultat de chaque cycle réglé (recettes par poste, primes, entretien, dépenses d'infrastructure, transferts).
- `gold.sz_finance_projection` : solde de fin de saison sans prime de victoire (`end_balance_no_wins`) et avec les victoires au rythme actuel (`end_balance_with_wins`), `wages_pct_revenue`, `sponsor_can_choose`.

## Livrable
1. **Alerte** : le club perd-il de l'argent sur le dernier cycle et sur la prévision ? Cause chiffrée.
2. **Masse salariale** : `fc_wages` / `fc_revenue`, marge avant le rouge.
3. **Sponsor** (si `sponsor_can_choose`) : comparer les 3 offres sur la saison (fixe × cycles restants + prime de victoire × victoires attendues + prime de signature).
4. **Infrastructures** : quelle installation améliorer et quand, d'après le remboursement en cycles et la trésorerie. Décision en attente au 2026-10-18 : Fan Shop 7 ou Arena 7.

## Sortie propre au jeu
- Fichier : `outputs/sixzeroleague/briefs/AAAA-MM-JJ-finances.md`. En tête : l'alerte (ou « pas d'alerte ») et les actions.
- Si `silver.sz_finances.day` est antérieur au dernier cycle, demande l'export de la page Finances.
