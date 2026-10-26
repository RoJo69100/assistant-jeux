# Six Zero League — fiche Transferts

Lue par l'agent `transferts` après `commun.md`. Case E6 de la checklist SixZero League.

## Skills à lire
- `.claude/skills/sixzeroleague-club/SKILL.md` (§ Marché des transferts, § Finances)
- `.claude/skills/sixzeroleague-joueurs/SKILL.md` (rôles, compétences clés, retraite)
- `.claude/skills/sixzeroleague-entrainement/SKILL.md` (âge)
- `.claude/skills/sixzeroleague-communaute/SKILL.md` (annonces closes au coup d'envoi suivant)

## Règles propres au jeu
1. Frais, paliers, minimum d'effectif, libération et règlement : **uniquement d'après le skill club** ; ne les cite pas de mémoire.
2. Les compétences d'un joueur en vente sont visibles de tous [W:Transfers] : compare-les au rôle sur les 20 compétences.
3. **Salaires** : fixés selon le niveau, revus seulement entre les saisons [W:Finances] ; compte le salaire en plus du prix.
4. Pas de ventes conclues en base : pas de prix de référence. Dis-le et donne une confiance faible.
5. Une enchère dure une semaine du jeu (2 journées) et se règle au coup d'envoi suivant [Dev chat, 2026-09-23 et 2026-10-18]. Un joueur libéré a 10 % de chances de réapparaître en joueur libre [Dev chat, 2026-09-23]. Les stats d'un joueur ne sont visibles que s'il est en vente [devlog 0.5.9].

## Données
- `silver.sz_transfer_listings` : `role`, `age`, `overall`, `wage`, `retiring`, `starting_price`, `current_bid`, `next_bid`, `free_agent`, `seller_is_bot`, `attributes`, `settle_after_round`, `seen_at`.
- `silver.sz_players`, `gold.sz_lineup_natural` : place qu'aurait la recrue, joueurs à vendre.
- `silver.sz_finances` (`balance`, `fc_net`) : de quoi payer.

## Livrable
1. Joueur demandé, ou 3 à 5 meilleures annonces pour nos rôles faibles : intérêt, prix, enchère maximale conseillée (avis), coût total.
2. Nos joueurs : vendre maintenant, en fin de saison, ou garder (âge, rôle, salaire, retraite).

## Sortie propre au jeu
- En tête du brief : les actions (enchère, montant, journée de règlement) et leur date limite.
- Si `seen_at` a plus de 12 h, demande un nouvel export du marché (règlement chaque soir).
