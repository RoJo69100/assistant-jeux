# Académie BasketVibe — rapport du 19/11 (brief du 2026-11-23, 17:29 Paris)

Sources : `gold.bv_academy_prospects` (rapport du 19/11 09:00 Paris), capture de la page Académie du 23/11 15:45 (page 73541, `refined_skill_brackets` et `potential_bucket`), `silver.bv_academy_weekly`. L'utilisateur peut avoir agi depuis. Chat : `gold.bv_academy_chat` depuis le 19/11 = 0 ligne. Brief amont : aucun requis par la config ; aucun brief académie du 19/11 trouvé avant celui-ci.

## Décision (en tête)
| Prospect | Décision | Pourquoi |
|---|---|---|
| Quentin Besson (PG, 17 ans) | **Ignorer** | Test lu : Decent. Hors règle « très gros potentiel » (17/11). |
| Damien Roussel (PG, 16 ans) | **Ignorer** (je tranche l'« à juger ») | Test lu : High, taille 177 cm dans la plage PG, mais PS au poste 41,95–51,95 : sous le plus faible PG (45,2) en bas de fourchette, sous Boyer (48,7) et Richard (56,8) au milieu. Ne « correspond » pas aux meilleures caractéristiques du poste. |
| Lenny Gauthier (PF, 16 ans) | **Ignorer** | Test lu : Decent. Hors règle. |
| Investissement | **Garder 100 000 / sem.** | Jauge 92 % → vers 100 % (bonus potentiel). À sauvegarder avant le jeudi 26/11 09:00 (prochain rapport 26/11). |
| Signature | **Aucune** | Aucun prospect à signer aujourd'hui. |

## Verdict par prospect
| Prospect | Poste | Potentiel testé | Verdict |
|---|---|---|---|
| Quentin Besson | PG | decent | ignorer |
| Damien Roussel | PG | high | ignorer |
| Lenny Gauthier | PF | decent | ignorer |

## 1. Prospects (faits : `gold.bv_academy_prospects`, capture 23/11)
| Prospect | Poste | Âge | Taille | TSP min–max | Compétences clés du poste (fourchettes 20 pts) | P(High) jauge 92 % | Verdict |
|---|---|---|---|---|---|---|---|
| Besson | PG | 17 | 184 | 274–434 | 2 pts 37–57, 3 pts 34–54, passes 35–55, dribble 32–52 ; PS mid 43,7 | 28,7 % (test : Decent) | ignorer |
| Roussel | PG | 16 | 177 | 271–431 | 2 pts 35–55, 3 pts 35–55, passes 35–55, dribble 35–55 ; PS mid 43,7 | 28,7 % (test : **High**) | ignorer |
| Gauthier | PF | 16 | 194 | 247–407 | 2 pts 30–50, déf. 35–55, rebond 17–37, athl. 28–48 ; PS mid 40,2 | 28,7 % (test : Decent) | ignorer |

Probabilités : `gold.bv_academy_potential_odds` (jauge actuelle 92 : Low 2,3 / Decent 68,9 / High 28,7 %, potentiel moyen 6,54) [M§4.2].

## 2. Roussel en détail (le seul High)
- **Faits** : test (fourchettes de 10 pts, capture 23/11) : 2 pts 44–54, 3 pts 45–55, déf. 35–45, passes 43–53, dribble 45–55, rebond 43–53, endurance 35–45, athl. 45–55. PS PG (poids `gold.bv_ps_weight` : 0,15 ×5, rebond 0,05, athl. 0,10, endurance 0,10) = **41,95 à 51,95** (calcul sur les bornes du test).
- Nos PG (`gold.bv_roster_now`) : Richard 56,8 (25 ans), Boyer 48,7 (20 ans), Baron 45,2 (17 ans, junior signé). Poste PG : 3 joueurs (`gold.bv_position_summary`).
- **Règle** (utilisateur, 17/11, `docs/regles-utilisateur.md`) : signer si très gros potentiel + meilleures caractéristiques du poste + bonne taille. Potentiel : oui (High). Taille : oui (177, plage 172–187). Caractéristiques : **non** : même la borne haute (51,95) n'atteint pas Richard et le milieu (≈ 47) ne dépasse que Baron. Aucun seuil chiffré de l'utilisateur ; le seuil du code (18/11, posé par Claude, contestable : bas ≥ PS le plus faible du poste, haut ≥ meilleur − 5) donne aussi « ignorer » (41,95 < 45,2 ; 51,95 ≥ 51,8 seulement en haut).
- **Coût d'une signature** [M§4.2] : jauge 92 → 46 %, puis 5 semaines à 100 000 pour revenir ≈ 92 % (`gold.bv_academy_gauge_projection`, 100 000 : 59,2 / 70,0 / 78,8 / 86,2 / 92,0), soit des rapports moins bons ; irréversible. Ce qu'on obtiendrait : un PG de plus, au niveau de Baron, à 5 pts de Richard.
- **Avis (confiance moyenne)** : un High à 16 ans a de la marge, mais son profil est plat (35–55 partout, défense/endurance basses) ; ignorer coûte zéro et garde la jauge pour un High mieux profilé (43,9 % de High à 100 %, table [M§4.2]).
- **Ce qui prouverait que j'avais tort** : si l'utilisateur fixe un seuil de PS plus bas que 45 pour « meilleures caractéristiques », Roussel redevient signable ; à écrire dans `docs/regles-utilisateur.md`.

## 3. Investissement
| Jauge | Investissement/sem. | Projection | Décision |
|---|---|---|---|
| 92 % (`silver.bv_academy_weekly`, semaines 16/11 et 23/11) | 100 000 | ≈ 100 % au prochain rapport (+ ≈ 8 pts/sem. observés : 79 → 86 → 92) ; hypothèse de `sql/gold/010_bv_academy.sql` | **Garder 100 000**. Coût 8 semaines : 800 000. Solde 1 496 859, résultat hebdo estimé +151 849 (`gold.bv_finance_health`). Date limite : jeudi 26/11 09:00. |

À 100 % le bonus porte P(High) de 28,7 % à 43,9 % [M§4.2] : c'est le moment de viser un seul prospect solide, pas de signer un profil moyen.

## 4. Autres points
- Jusqu'à 25 000 par test : aucun test à lancer aujourd'hui (les trois du 19/11 sont lus).
- Aucune somme > 250 000 engagée : police non requise.
- Anselmo Albano : non concerné par l'académie (consigne : ne pas le faire jouer ; vente au plan).

## 5. Conseil suivi
C-135 ajouté à `outputs/basketvibe/learnings.md`.
