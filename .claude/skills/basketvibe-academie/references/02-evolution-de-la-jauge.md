## Évolution de la jauge [M§4.2]
- Plus on investit, plus elle monte, mais de moins en moins vite près du sommet. **0 investi = −5 par semaine.**
- 100 000 par semaine maintient 100 %. 50 000 plafonne vers **89 %** (à 100 %, −5 par semaine). 20 000 fait **baisser** une jauge à 25 % (vers ~21 %).
- À 99 %, tout investissement positif amène à 100 % exactement.
- Départ de 0 % à 100 000 par semaine : 20, 37, 52, 64, 74, 82, 89, 94, 97, 99, 100 % (11 semaines, 1,1 M). À 50 000 : 12, 23, 33, 42, 50, 58, 65, 71, 76, 80, 83, 85, 87, 88, 89 %.
- V-20261108-8 [Dev 2026-11-05, #polska] : une jauge à 100 % ne **promet** pas 3 étoiles, c'est une chance ; le tirage « purement aléatoire » pourrait poser problème (cas extrême : 2 blessures par match). ⚠️ À vérifier : un joueur rapporte que la page Académie prédit 85 % → 88 % pour 100 000, alors que le manuel donne 82 % → 89 % ; le développeur : « je vais vérifier » [Dev 2026-11-01, #academy] ; la News du 2026-11-01 ajuste l'écran pour que les prévisions ne se chevauchent plus à haut niveau d'académie. Comparer `gold.bv_academy_gauge_projection` à la prochaine jauge exportée avant d'investir. Avis (non règle) : à 100 %, un 17 ans à 400 points de compétences vaut mieux qu'un 16 ans à 370 [Com 2026-11-05, grobarbrate].
- Départ de 50 % à 100 000 par semaine : 63, 73, 82, 89, 94, 97, 99, 100 % (8 semaines).

