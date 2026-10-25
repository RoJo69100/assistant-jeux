---
name: hockeynation-compositions-trades
description: Méthode Hockey Nation pour construire les 4 équipes (PRO, FRM, U21, U17) avec montées, descentes et sorties, puis choisir les échanges avec de vrais joueurs en comptant les salaires dans le bon ordre. À charger avant tout rendu de rosters, de lineups ou de trades.
---

# Hockey Nation — compositions et échanges

Sources : [U] consignes de l'utilisateur du 2026-10-25 ; [G:Teams], [G:Farm Team], [G:U21 Team], [G:Trades] via les skills joueurs / contrats-finances ; [Discord, #general, 2026-03-26] (une équipe peut dépasser 20 joueurs) ; `outputs/hockeynation/briefs/2026-10-25-transferts.md`.

## Rendu des rosters [U]
- Un tableau par équipe, **dans l'ordre de jeu** : L1 à L4 (LW – C – RW), D1 à D3 (LD – RD), G1 puis G2. Réserve hors lineup en dessous.
- Tags : **TOP** meilleur du poste, **CE** contre-emploi (à remplacer), **TRADER**, **VIDE** si le poste est vide. Jamais de colonne « trou / à améliorer ».
- Un joueur annoncé « monte » apparaît dans l'équipe d'arrivée. Tableau des mouvements : monte / descend / sort, avec la condition.
- Cible : 12 attaquants (4 C, 4 LW, 4 RW), 6 défenseurs (3 LD, 3 RD), 2 G. Les doubles postes (Stone, Yokoyama LW/RW ; Blednov, Flink RW/C) comblent un poste, jamais deux.

## Règles de mouvement
- **Aucun maximum de 20 en PRO** n'est documenté ; les surplus restent en réserve jusqu'à leur échange. FRM : 30 joueurs maximum.
- Seuls les joueurs sous **ELC** peuvent redescendre ; les autres ne partent que par échange, rachat ou libération.
- U21 → FRM ou PRO : possible à tout âge [U, 2026-10-25] (montée automatique à 21 ans) ; un U21 en trop peut donc combler un VIDE du FRM. Lire le prix du contrat à l'écran.
- Les 4 clubs de comparaison (Leszno, Jessup, Miami, Seoul) ne sont jamais des partenaires d'échange [U]. Pas de nom d'échange sans export Trade Center à jour.
- Tag « TOP » supprimé : décrire la force réelle du joueur (note, spéciales, rôle, cohésion, potentiel) et non son rang dans l'équipe.
- Monter un FRM en PRO : choisir **les meilleurs par poste** selon la lineup à compléter ; son salaire n'est connu qu'à l'écran de contrat. Ne jamais dire « sous négociation » à l'utilisateur : dire « prix à lire à l'écran ».

## Salaires : ordre des opérations
1. Marge = plafond − engagé (`gold.hn_cap_outlook`, S27 : 1 630 000 au 10-25). Jamais négative.
2. D'abord ce qui libère du salaire (sortants), puis ce qui en coûte (montées, arrivées). Un départ avant la 1re paie (11-01) libère 100 % du salaire.
3. Un échange passe un comité de 21 votants (24 h) : prévoir 2 à 3 jours ; dernier jour sûr d'envoi avant la paie.
4. Donner pour chaque échange : joueurs et salaires des deux côtés, Δ marge, lineup avant → après (note, END, verdict talents).
5. Noms réels uniquement, tirés de `silver.hn_league_players` / `silver.hn_market_players` (donner la date de l'export) ; marché de plus de 24 h = première ligne « exporte le marché ». Agents libres 30+ ans à 70+ demandent environ 4 000 000 et plus : hors marge.

## Contrôle
Avant de rendre : 20 joueurs par équipe, VIDE marqués, aucun joueur annoncé « monte » absent de l'équipe d'arrivée, marge ≥ 0 à chaque étape.
