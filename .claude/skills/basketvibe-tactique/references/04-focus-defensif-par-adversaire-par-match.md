## Focus défensif par adversaire (par match) [M§6.6]
- Se règle sur la page du match (Tactics à côté de Preview), joueur adverse par joueur adverse. Verrouillé 15 min avant le coup d'envoi.
- **Sans plan sauvegardé, tous les adversaires sont marqués pareil.**

| Niveau | Lock | Intense | Normal | Light | Give up |
|---|---|---|---|---|---|
| Poids de marquage | 2,00 | 1,55 | 1,00 | 0,62 | 0,22 |

- Plus de focus : le joueur tire moins et, quand il tire, est mieux défendu. Ses coéquipiers récupèrent des tirs.
- **Hit** : Lock ou Intense sur le vrai scoreur (celui sur qui passe l'attaque) → l'adversaire perd nettement. **Even** : sur un cinq équilibré → le score bouge peu. **Miss** : Lock sur un meneur passeur → les autres ont des tirs plus faciles, l'adversaire peut marquer plus.
- Effet typique sur le % de réussite du scoreur visé : Intense contre Normal −2 à −4 pts ; Lock contre Intense −2 à −4 pts ; de Give up à Lock +12 à +16 pts d'écart.
- Conseils du manuel : verrouiller le scoreur, pas le meneur qui distribue ; compenser par Light ou Give up sur les joueurs peu utilisés ; toujours sauvegarder avant le verrouillage.
- [v4, tous les matchs : amical, coupe, ligue ; confirmé par l'utilisateur le 2026-10-30] Nouvelle zone de focus défensif par joueur adverse : **Rim** (son 2P% −3 % environ, son 3P% jusqu'à +5 %), **Perimeter** (son 3P% −3 % environ, son 2P% jusqu'à +5 %), **Neutral** (comme avant). Le compromis est volontairement inégal [News 2026-10-19]. À vérifier : `silver.bv_match_tactics` capte-t-il ce champ ?
- [Export] Dans le plan sauvegardé exporté (page du match), un focus défensif **Lock** est écrit `off` ; confirmé à l'écran pour deux joueurs de Žirmūnai (J20) [Utilisateur 2026-10-21, learnings L-018]. Les autres niveaux sont écrits par leur nom.
- **Échelle à l'écran : 1 à 5** = Give up, Light, Normal, Intense, Lock (3 = Normal, valeur sans plan sauvegardé). Saisir le chiffre. [M§6.6.1 ; échelle confirmée par l'utilisateur le 2026-10-23]
- **Nombre de joueurs en Intense/Lock** : le manuel ne fixe aucun plafond. Il conseille « un ou deux » joueurs forts en Lock/Intense, compensés par Light/Give up sur le banc [M§6.6.5]. Les poids sont moyennés sur l'effectif adverse et décalent des tirs vers les coéquipiers [M§6.6.3]. Effet de plusieurs 4/5 en même temps sur les autres joueurs : non documenté, voir tests L-012 / C-040 du journal.
- Écart d'effet typique sur le joueur visé : un cran plus facile sur le scoreur clé ≈ +2 à +7 points de FG% ; Intense contre Normal et Lock contre Intense ≈ 2 à 4 points chacun [M§6.6.4].
- **En amical, un grand écart de compétence au même poste ajoute à l'effet du focus** ; en ligue et en coupe l'effet de compétence reste plus petit [M§6.6.3].

### Defensive area (tous les matchs depuis le moteur v4, confirmé par l'utilisateur le 2026-10-30) [M§6.6.2]
- Second curseur par joueur adverse, à côté du focus : **Perimeter – Middle – Rim**. Middle = aucun décalage (défaut). Elle existe aussi en ligue et en coupe (confirmation de l'utilisateur le 2026-10-30 ; le champ `area_step` est dans l'export de coupe) : toujours la régler et l'afficher pour chaque adversaire.
- ✅ V-20261027-3 CONFIRMÉE par l'utilisateur le 2026-10-30 (la zone existe en coupe et en ligue) ; texte d'origine : (un seul texte, non testé à l'époque) : le recap du 27/10 liste la zone parmi les changements du v4 « actif dans chaque match » sans la mention « amicaux seulement » [News 2026-10-27]. Elle est peut-être ouverte en ligue et en coupe : à constater sur l'écran tactique de la coupe du 28/10 ou de la ligue du 02/11 ; d'ici là, ne pas la régler en ligue. Valeurs : Rim −3 % de 2P% adverse mais jusqu'à +5 % de 3P% ; Perimeter −3 % de 3P% mais jusqu'à +5 % de 2P% ; Neutral = 0.
- Elle change le **% de réussite**, pas le nombre de tirs. Perimeter : tirs à 3 pts plus difficiles, tirs à 2 pts plus faciles. Rim : l'inverse.
- Ampleur : à l'extrême, tirs défendus ≈ −3 points, tirs ouverts ≈ +5 points ; un cran hors du milieu = la moitié.
- Annonce complète [News 2026-10-19, « v4 engine wraps up: injury tuning and defensive focus areas »] : réglage par joueur adverse dans la tactique du match (**amicaux seulement pour l'instant**). **Rim** : −3 % environ de 2P% adverse, mais jusqu'à +5 % de 3P%. **Perimeter** : −3 % environ de 3P%, mais jusqu'à +5 % de 2P%. **Neutral** : comme avant. Le déséquilibre est voulu : « décaler le focus à l'aveugle comporte un vrai risque, par exemple un grand qui tire à 3 ». [M§6.6.2] : la ligue et les coupes ne l'utilisent pas ; « for now » laisse penser à une extension future (à surveiller). Pas de plan sauvegardé : tous les adversaires sont marqués pareil.
- Avis de joueurs (non vérifiés) : « les intérieurs tirent environ 10 fois plus à 2 qu'à 3, on peut régler Rim à l'aveugle sur eux » [Com 2026-10-20, marekb9231, polska] ; avec seulement des fourchettes de compétences adverses, le choix reste « une loterie » [Com 2026-10-20, gulon84, polska].
- Utilité : à tester en amical pour la saison 2 ; non applicable en ligue (saison 1).

