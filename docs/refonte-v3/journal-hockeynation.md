# Journal Hockey Nation — charte et skill « que faire aujourd'hui » (2026-11-06)

## Critères d'acceptation (écrits avant le reste)

- **C1** Le skill nomme chaque vue citée et chacune existe : pour chaque vue, `select 1 from <vue> limit 1` via `python -I pipelines/sql.py`, sortie collée dans le rapport.
- **C2** Le plan quotidien est exactement 5 blocs : 1 exports en retard · 2 scouts · 3 matchs joués des 4 équipes · 4 tactique PRO si déclenchée · 5 entraînement des joueurs.
- **C3** Aucune ligne transferts, finances ni Trade Center, sauf l'alerte plafond salarial négatif.
- **C4** Chaque règle de test porte « ce qui prouvera que j'avais tort » et une échéance en matchs.
- **C5** Aucune valeur nouvelle sans la marquer « (à valider) ».

## Correction du 2026-11-06 : critères M1 à M4 (écrits avant la modification)

- **M1** Le bloc 3 produit une ligne par match joué des 4 équipes, victoire ou défaite : résultat (`my_result`), « mérité ou non » (tirs et xG contre réalisation et arrêts, comparés à la moyenne de la saison de l'équipe), et la règle L-nnn que ce match confirme ou contredit (pour/contre), sinon « aucune règle concernée ».
- **M2** Une section « Registre du Match Engine » dit où les pour/contre s'inscrivent (`outputs/hockeynation/learnings.md`), qui les met à jour (Claude, une fois par semaine, avec la revue des matchs) et qu'un compteur automatique viendra dans un lot suivant.
- **M3** Le bloc 5 cite la requête qui prouve que l'entraînement saisi est en base et sa date ; sinon il ajoute l'export Training au bloc 1 pour ce cas seulement.
- **M4** Un match d'une des 3 équipes non PRO (lignes automatiques) est marqué « expérience sans notre choix » dans le registre.
