# Hardwood — fiche Académie (recrutement)

Lue par l'agent `academie` après `resume.md` (Hardwood n'a pas de `commun.md`). Créée le 2026-11-02 (plan de conception, étape 0c : `academie` absorbe le recrutement). Hardwood n'a pas d'académie : la relève vient **seulement** du recrutement (lycée, JuCo, international).

## Skills
`hardwood-recrutement` (points, offres de bourse, niveaux d'intérêt, engagements, facteurs, régions, phrases du scout et plafonds), `hardwood-regles` (effectif de 13 bourses + walk-ons, redshirt, potentiel, valeurs ±20 %).

## Données (vues de `resume.md`, rien d'autre)
- `gold.hw_recrues_a_ouvrir` : pages de recrues à ouvrir et exporter (15 au moins) avant de juger.
- `gold.hw_recrue_fiches` : note /5 actuelle et au plafond, verdict, par recrue dont la page est exportée.
- `gold.hw_recruit_board` : verdict (cible / cible hors région / secondaire / dur / futur / écarter), `rang`, `besoin` (poste d'un boursier qui part).
- `gold.hw_recruit_group_notes`, `gold.hw_roster_notes` : notes par groupe de poste (PF et C = « Grand ») ; note = (niveau SI + adéquation aux compétences clés) / 2, avenir = potentiel [mémoire feedback-hardwood-notes-competences-cles].
- `silver.hw_recruiting` (nos contacts, offres, points), `silver.hw_prospects`, `silver.hw_ref_scout_phrases`, `silver.hw_ref_potential_caps`.

## Règles propres (source entre crochets)
1. **Juger sur les compétences clés du poste et les phrases du scout**, jamais sur le SI seul : SF = OS, défense, Spd ; PG = IQ, Pass, Hnd, Spd ; SG = OS, Spd ; Grand = IS, Reb. Une phrase rédhibitoire (« can never be a good rebounder », « does not have much of a shooting touch ») écarte la recrue [U, 2026-10-30].
2. **Concurrence** : cibler les recrues sans concurrent ou avec une ou deux équipes ; l'intérêt des concurrents est arrondi [skill hardwood-recrutement]. **Jamais de niveau High**, ni en colonne ni en mention [U, feedback-hardwood-pas-de-high].
3. **Au moins un grand**, et un grand mesure **au moins 2,02 m** : contrôler `height_m`, la vue classe « Grand » par poste, pas par taille [U].
4. Une recrue déjà engagée chez nous ou partie ailleurs est retirée ; « Eager to commit early » ne veut pas dire « recrutée » [U, 2026-10-30].
5. Points : +2 par tour, plafond 45, 53 tours [resume.md] ; répartir pour que les 4 cibles restent atteignables, le reste sur les remplaçants.

## Livrable (format figé, contrôlé par `pipelines/forme.py`, format hw-recrues)
1. Tableau de **4 lignes exactement** : `| Priorité | Poste (qui part) | Cible | Remplaçant 1 | Remplaçant 2 |`. Chaque cellule : nom, classe/État, taille, note actuelle → plafond, nombre d'équipes intéressées.
2. Sous le tableau : les points à dépenser aujourd'hui, recrue par recrue (offre de bourse oui/non), et les pages de recrues à exporter (`gold.hw_recrues_a_ouvrir`) si moins de 15 fiches sont lues.
3. Chaque cible : ce qui prouvera l'erreur (engagement ailleurs, plafond plus bas révélé) ; conseil `C-nnn` dans `outputs/hardwood/learnings.md` (à créer s'il manque).
