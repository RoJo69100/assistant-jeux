# Six Zero League — Transferts — 2026-11-01

Brief amont lu : `2026-11-01-finances.md` (capacite_invest = 0 €). Données : `silver.sz_transfer_listings` et `silver.sz_api /transfers` du 2026-11-01 07:28 UTC (marché de 9 h, à rafraîchir avant 21:00), `gold.sz_effectif_bilan`, `gold.sz_role_report` (as_of 2026-10-31).

## Correction à la règle du brief Finances
« Les annonces ne se résolvent qu'à l'intersaison » est **périmé**. Gazelle, chat 2026-10-29 20:57 UTC : « The current transfers only end at the last round of the first day of the season ». Saison 4 lancée le 31/10 (Gazelle 13:31 UTC), 1re manche le 01/11. Les 67 annonces de l'export portent toutes `settle_after_round` = 2 : **règlement après la manche 2 d'aujourd'hui (21:00 Paris)**. Restent vrais : annulation impossible (Gazelle 2026-10-27 09:16 UTC), règlement ensuite toutes les 2 journées. Sources corrigées : `connaissance.md` 6.14b, skill `sixzeroleague-club`, `resume.md`. Inconnu : si une annonce posée maintenant se règle aussi ce soir (cherché dans : chat, wiki skill club, `settle_after_round` ; on le réunit en exportant le marché après une mise en vente).

## Décision (une seule)
**Ne mets personne en vente et n'enchéris sur personne aujourd'hui. Frédéric Denis reste en vente à 1 000 €. Le niveau 7 de la Youth Academy se paie dès que le solde affiché atteint 6 200 € (prévu après le cycle de demain).**

## (1) Ventes et enchères ouvertes
| Élément | État | Source |
|---|---|---|
| Frédéric Denis, CB 8, 27 ans, salaire 95 | en vente, départ 1 000 €, 0 enchère, réglé après la manche 2 de ce soir ; frais 500 € déjà payés | `silver.sz_transfer_listings` 01/11 |
| Gabriel Bertin | pas en vente (toujours dans l'effectif, RW3, 0 match) : la vente du 27/10 n'a jamais été lancée | `gold.sz_effectif_bilan` |
| Mes enchères | aucune (`myBids` = []) | `/transfers` 01/11 |
| Historique récent | arrivées Barros et Sundberg à 1 000 € ; aucun départ | `/teams/mine/transfers` 31/10 |

## (2) Une vente qui comble les ~1 245 € ? Non
- Seuls surplus : Denis (CB3) et Bertin (RW3). Les 14 autres sont titulaires ou l'unique remplaçant de leur rôle : aucun à vendre sans abîmer le sept.
- Denis à 1 000 (au mieux) : manque encore ~245 €. Bertin à 1 000 : net 500 € (frais 500). **Les deux ensemble, vendus au prix de départ, donneraient 4 955 + 1 000 + 500 = 6 455 €** (marge 255). Mais comparables du marché : aucun joueur de note 8-9 sans enchère n'est parti (Zambrano GK 8, Ruiz GK 8, Palma LW 9, Winter RB 9, Kristiansen RW 9 : 0 enchère). Denis a sans doute peu de chances, Bertin encore moins à ≥ 1 000 €.
- Mettre Bertin en vente = 500 € perdus à coup probable (invendu). Les 500 € font passer le solde après le 2e cycle de 8 351 à ~7 851 : le niveau 7 reste payable demain soir, mais l'espérance de gain est négative. **Décision : pas de mise en vente de Bertin.** Ce qui prouvera que j'avais tort : Denis réglé ce soir à ≥ 1 000 € ET solde > 6 200 € après le cycle (alors acheter le niveau 7 tout de suite).

## (3) Cibles nommées (aucun achat : capacite_invest = 0 €)
Poste faible = ceux où les clés sont basses (`gold.sz_role_report` : LB clés 11,3 ; P 11,5 ; GK 13,8).
| Cible | Poste | Prix (prochaine enchère) | Gain chiffré | Finançable | Solde nécessaire |
|---|---|---|---|---|---|
| Stefan Böhm, 31 ans, éthique 97 | LB | 2 000 (1 enchère à 1 000) ; salaire 125 | note 10 -> 13, clés 11,3 -> 16,0 vs Alain Bertin | non (solde 1 559) | 2 000 + réserve niveau 7 : 8 200 € |
| Moritz König, 24 ans | P | 4 000, 0 enchère ; salaire 120 | note 10 -> 12, clés 11,5 -> 14,0 vs Benoit | non | 10 200 € |
| Sreten Nedeljković, 19 ans | GK | 10 000, 0 enchère ; salaire 220 | note 11 -> 18, mais clés 13,8 -> 15,6 seulement | non | 16 200 € |
Écartés : Nélson Matos GK 12 (clés 11,8 < 13,8 de Bourgeois), Sascha Schmid LB 18 (20 000 déjà misés), Kołodziej P 17 (19 000). Toutes ces annonces se règlent ce soir : elles ne seront plus achetables demain ; je ne propose donc rien à surveiller. Après le niveau 7 (solde ~2 150), le LB à ~2 000 redevient finançable seulement sur une annonce future, à rechercher à l'export suivant. Confiance faible (note ≠ clés, effet sur le résultat non prouvé).

## (4) Enchères du marché à suivre
Aucune à suivre : les 67 se règlent ce soir. Seul repère utile pour la suite : prix réglés (Transfer history) à relever demain pour calibrer Denis et les LB/P.

## Conseils suivis
Aucun achat ni vente conseillé aujourd'hui : rien à ajouter à `learnings.md`. Denis (vente du 27/10, C déjà existante) reste ouvert jusqu'au règlement de ce soir.
