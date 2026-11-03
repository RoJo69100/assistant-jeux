---
name: hockeynation-compositions-trades
description: Hockey Nation : construire les 4 équipes (PRO, FRM, U21, U17) avec montées, descentes et sorties, puis choisir les échanges en comptant les salaires. À charger avant tout rendu de rosters, lineups ou trades.
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

## [Veille 2026-10-29] Avis de marché (V-20261029-11, jamais une règle)
- Valeur d'échange par note minimale (talonflame1, 2026-04-14) : 80+ = 1er tour, 70-79 = 1er, 60-70 = 2e, 60-64 = 3e, 55-60 = 4e, < 55 = 5e. Cap dump par salaire jeté : < 1 M = 4e, 1-2 M = 3e, 2-4,5 M = 2e, 4,5-7 M = 2e + 3e, 7-10 M = 1er. Marché S27 : surplus de U21 (30 à 35 joueurs par club), demande pour U21 C/RW/LD, RD de tête et gardiens U21. [Discord #general et #trade, 2026-10-24 à 10-29]

## [Veille intégrale 2026-10-29] Échanges : délais et avis de marché (V-A-20, V-B-7, V-C-1, C-2)
- **Règles (staff)** : traitement à la 2e mise à jour quotidienne après l'acceptation ; échanges de choix seuls : instantanés ; en fenêtre II, un joueur reçu en fenêtre I ne peut pas être échangé ; les FA signés ne sont pas échangeables dans leur 1re saison (avis, à confirmer) ; une équipe en playoffs ne peut pas échanger ; le plafond se libère à l'approbation, l'effet sur les paies est le salaire total / 35 jours. [hnadmin 2022-03-01, 2023-09-19, 2024-01-18 ; d0ghouse 2025-09-03 ; V-A-20]
- **Avis de valeur (jamais une règle)** : modificateurs d'un tour — plus pour spéciales, joueur de 18-20 ans non plafonné, gardien élite ; moins pour 35 ans et plus, contrat expirant en fenêtre II sans prolongation signée, équipe déjà au-dessus du plafond, gardien titulaire non PRO ; en général sans cumul. Fenêtre I : 2 × 5e = 4e, 2 × 4e = 3e, 2 × 3e = 2e, 2 × 2e = 1er. Cap dump de 10 M et plus = 1er tour et plus ; les années restantes du joueur jeté comptent. Repères 2023 : cap dump 2-3 M$ = 2e tour, joueur plafonné ≈ 2e, 1ers tours « collants ». [talonflame1, _pignon_ 2026-04-14 ; V-B-7, C-1] À comparer avec `gold.hn_trade_value`.
- **Pratique de la trade board (avis, ≥ 6 joueurs)** : toujours écrire un commentaire qui explique l'échange (le comité ne voit que le suivi : joueur, variation de salaire, compte nouveau ou non — mr.president13 2024-07-17) ; la première offre fixe le ton ; éviter les équipes « New user » (presque toujours refusées) ; un joueur déverrouillé dans le Trade Center n'est pas forcément à vendre : confirmer par message. Définition officielle du « cap dump » et seuil de la board : absents, ne pas fonder un échange dessus. [roadiculous 2026-02-09 ; beanz6969 2026-04-20 ; V-C-2]
