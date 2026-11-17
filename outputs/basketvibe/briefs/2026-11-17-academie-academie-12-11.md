# Brief académie BasketVibe — mardi 17/11/2026 (14:07 Paris)

Rapport lu : jeudi 12/11 09:00 Paris (`gold.bv_academy_prospects`, scout_report_at 2026-11-12 08:00 UTC), toujours le dernier en base (`silver.bv_academy_weekly` : semaine 09/11, jauge 86 %, investissement 100 000, prochain rapport 19/11). L'utilisateur a pu agir depuis. Aucun achat, aucune signature, aucun test exécuté par moi : je propose.
Brief amont : `2026-11-13-academie.md` (même rapport) relu ; ses chiffres sont repris et revérifiés ci-dessous.

## Décision (à exécuter aujourd'hui)
- **Tester les 3 prospects (75 000) : NON.** Aucun test ne peut changer la décision : aucun des trois ne bat un titulaire ni nos juniors au même âge, même en haut de fourchette.
- **Signer : personne.** Une signature coûte la moitié de la jauge (86 → 43 %) [M§4.2] et ne comble aucun trou.
- **Investissement : garder 100 000.** Vérifier avant jeudi 19/11 09:00 que la valeur sauvegardée est bien 100 000.
- Police : non requise (aucune somme > 250 000 engagée).

## Prospects
| Prospect | Poste / âge / taille | TSP min–max, PS mi-fourchette | Écart avec l'effectif au poste | Verdict |
|---|---|---|---|---|
| Gabriel Bertrand | PF, 17, 197 cm | 260–420, PS 42,8 | PF : Lefebvre 63,2, Legrand 49,6, Albano 47,9 (`gold.bv_roster_now`). Sous les trois ; ≈ Leclerc à 17 ans (41,6 → 42,3) d'après le brief du 13/11 (`silver.bv_player_daily`) | **Ignorer** |
| Oscar Guillaume | PF, 16, 198 cm | 219–379, PS 37,8 | Sous Baron (43,1) et Leclerc (40,9) à 16 ans ; athlétisme 23-43 faible | **Ignorer** |
| Noé Deschamps | SF, 16, 190 cm | 236–396, PS 39,4 | SF : Gimenez 60,2, Durand 43,7 ; sous Durand de 4 points, défense 23-43 faible pour un SF | **Ignorer** |

Fourchettes par compétence : `gold.bv_academy_prospects` (fenêtre ≈ 20 points). PS = milieu des fourchettes × poids [M§2.2] : estimation, ±10 par compétence possible.

## Coût d'une signature (fait + règle)
- Jauge divisée par 2 : 86 → 43 % [M§4.2] ; retour à 90 % en ≈ 5 semaines à 100 000 (`gold.bv_academy_gauge_projection`, scénario « après une signature »). P(High) ≈ 25 % à 86 % contre ≈ 5 % à 43 % (`gold.bv_academy_potential_odds`).
- Homegrown : 200 par minute de ligue, plafond 40 000 par semaine [M§10.1.3]. Réel : `homegrown_last_week` = 4 800 au 16/11 (`gold.bv_finance_health`), soit ≈ 24 minutes. Un prospect à PS 38-43 ne jouerait pas devant Durand ni les PF : revenu ≈ 0 pour un salaire estimé de 12 500 à 15 750 par semaine (interpolation [M§10.2]).
- Finances : solde 1 291 868, résultat hebdomadaire estimé +140 631 (`gold.bv_finance_health`, 16/11). Un test serait finançable, mais inutile.

## Investissement
| Jauge | Investissement | Projection | Décision |
|---|---|---|---|
| 86 % (rapport du 12/11) | 100 000 par semaine | 90 % puis 100 % en ≈ 3 semaines sans signer ; P(High) 25 % → 44 % à 100 % (`gold.bv_academy_potential_odds`) | **Garder 100 000** ; coût sur 8 semaines 800 000 |

Moment de signer (avis) : un prospect qui bat un titulaire au poste, avec jauge ≥ 90-100 %. Ne cite pas « 90 suffit » (contraire à [M§4.2]).

## Chat académie
`gold.bv_academy_chat` lu (15 derniers messages, jusqu'au 08/11) : rien après le rapport du 12/11 ; sans effet sur la décision (anecdotes de tirages, aucune règle nouvelle).

## Doutes
1. PS estimé sur une fenêtre de 20 points et potentiel caché inconnu. Preuve que j'ai tort : un test révélant un High, ou un prospect dont le haut de fourchette dépasse Durand/Albano.
2. Revente très dispersée à PS égal (21 000 à 950 000 d'après le brief du 13/11, `bv_transfer_history`) : signer pour revendre n'est pas prouvé rentable ; je ne le recommande pas.
3. Salaires interpolés ; Guillaume est hors table (< 40).

## Conseil suivi
C-126 ajouté à `outputs/basketvibe/learnings.md` (critère : `silver.bv_academy_weekly`, `gold.bv_roster_now`).
