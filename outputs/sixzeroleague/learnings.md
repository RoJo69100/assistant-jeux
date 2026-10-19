# Journal des enseignements — Six Zero League (Chomelix Cow)

Tenu par l'agent Match (`.claude/agents/match.md`). Mis à jour après chaque match. Seuil de confirmation : 3 matchs de ligue dans le même sens [fiche match, règle 1 ; Dev chat].

**Dernier match analysé : 2026-10-19 — voleibol aljarafe (ligue J1, domicile, 27-26 V)** (brief `briefs/2026-10-19-match.md`).

## Journal des matchs
| Date | Journée | Adversaire (humain/bot) | Lieu | Score | Résultat | Remarque |
|---|---|---|---|---|---|---|
| 2026-10-19 | J1 ligue | voleibol aljarafe (humain) | domicile | 27-26 | V | mène 14-12 à la mi-temps ; arrêts 23,5 % contre 32,5 % ; 6 exclusions contre 5 ; but adverse à 5 s de la fin |

## Enseignements
<!-- L-nnn · date · enseignement · matchs de ligue à l'appui · statut (à surveiller / confirmé / infirmé) · source -->
| ID | Date | Enseignement | Matchs ligue | Statut | Source |
|---|---|---|---|---|---|
| L-001 | 2026-10-19 | Notre gardien Bourgeois arrête 8 tirs cadrés sur 34 (23,5 %) contre 13 sur 40 (32,5 %) pour le gardien adverse ; à 32,5 %, il aurait pris ~3 buts de moins. Échantillon minuscule. | 1 | à surveiller | `silver.sz_matches`, `silver.sz_match_players` ; [W:Match] (tirages de probabilités) |
| L-002 | 2026-10-19 | Discipline : 6 exclusions (3 joueurs à 2 : Lemaire, Simon, Lefebvre) + 3 jaunes + 8 fautes techniques ; 5 des 6 exclusions tombent entre 18:38 et 25:05 (1re mi-temps), score alors 11-9 puis 13-12 (2 buts pour nous, 3 pour eux). Adversaire : 5 exclusions, 9 fautes techniques : niveau comparable. | 1 | à surveiller | `silver.sz_match_incidents`, `silver.sz_match_players` ; [W:Match] (supériorité = accès aux 6 m), [Com chat, Antarez] |
| L-003 | 2026-10-19 | Plus de volume que l'adversaire (46 tirs contre 37 ; possession 1 945 s contre 1 655 s, soit 54 %) mais moins d'efficacité (58,7 % contre 70,3 %) ; 0 contre pour nous, 4 pour eux. | 1 | à surveiller | `silver.sz_matches` ; [W:Attributes] (Contre) |
| L-004 | 2026-10-19 | 2e mi-temps perdue 13-14 : l'adversaire marque 4 des 5 derniers buts (de 25-22 à 27-26, dernier but à 59:55). | 1 | à surveiller | `silver.sz_match_incidents` |

## Conseils
<!-- C-nnn · date · conseil · critère vérifiable (SQL) · statut (ouvert / appliqué / partiel / non appliqué) · effet constaté -->
| ID | Date | Conseil | Critère vérifiable | Statut | Effet constaté |
|---|---|---|---|---|---|
| C-001 | 2026-10-19 | Garder Bourgeois au but en J2 et J3 (meilleur gardien : note 11 contre 9 pour Blanc) ; ne juger qu'après 3 matchs de ligue — agent Match | `silver.sz_match_players` (`role` = 'GK', `is_mine`) : `name` = Emmanuel Bourgeois aux J2 et J3 ; `save_pct` moyen cumulé via `silver.sz_matches` | ouvert | — |
| C-002 | 2026-10-19 | J2 (avant 21:00 Paris) : test d'échange RW, Gabriel Bertin à la place de Gilbert Lemaire (Lemaire : Marquage 2, Duels 3 ; 2 exclusions, 2 fautes techniques, 1/4 au tir en J1) — confiance faible, un seul match [W:Attributes] — agent Match | `silver.sz_match_players` (J2, `is_mine`) : RW = Gabriel Bertin ; comparer `exclusions` et `technical_fouls` du RW (Lemaire J1 : 2 et 2) | ouvert | — |
