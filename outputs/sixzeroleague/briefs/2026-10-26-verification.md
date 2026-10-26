# Six Zero League — vérification 2026-10-26 (J16 à 21:00 Paris)

Preuves : `bronze.raw_pages` 17921 / 17923 / 17956 / 17961 (19:22-19:27 UTC), briefs du jour, `data/discord/SixZeroLeague/discord_SixZeroLeague_part1.txt`, `silver.sz_infrastructure_levels`.

| # | Affirmation | Verdict | Correction |
|---|---|---|---|
| 1 | Fournier CB titulaire, tactique 17921 | **Juste** | Titulaires : GK Bourgeois, CB Fournier, LB A. Bertin, RB Roger, LW Lefebvre, RW Dupont, P Benoit. Attaque 5-1, défense 6-0, mixed, agressivité normal, `autoFilled` false, `orders` vide. L'export MONTRE les remplaçants (`substitutes`) : GK Blanc, CB Simon, LB Leroy, RB Barros, LW Sundberg, RW G. Bertin, P Chevalier. Absents du banc : Denis (CB) et Lemaire (RW). Places de défense : P=CR, CB=CL, LB=HL, RB=HR, LW=OR, RW=OL. |
| 2 | Attributs Fournier (17923) | **Juste** | Les 8 valeurs concordent : Duels 26, Marquage 23, Passe 23, Anticipation 16, Tir 11, Technique 18, éthique 90, salaire 150. Âge 18, note 17. À ajouter : Un contre un 26, Prise de balle (Handling) 26, Force 19. |
| 3a | Rien ne s'oppose à « right + centre » dès J16 | **Faux** | Le brief Analyste §6 levier 1 (C-040) l'exclut explicitement : « pas J16 : le test Fournier CB titulaire (C-038/C-039) occupe J16-J17 ; deux changements à la fois ne se lisent pas ». Tactique C-039 juge Fournier sur J16+J17 (tir < 40 %, exclusions, fautes). Mettre la direction dès J16 mélange les deux tests. La source Gazelle (lignes 324-331) ne s'y oppose pas, mais elle ne donne aucun effet chiffré. Si tu passes outre, dis-le comme une dérogation à C-040 et déplace les critères de réfutation (efficacité < 50 %, part du centre < 38 %) sur J16-J18. Mon avis : garder J17-J18. |
| 3b | « right + centre » existe à l'écran | **Non vérifiable en direct** | Citation d'un joueur, ligne 324 : « Left + Center or Right + Center ... CB and P will attack the most ». Ligne 327 : Gazelle confirme que le choix existe. Les exports du jour ne l'ont jamais pris : `attackDirection` en base vaut `mixed` (3 relevés) et `left-center` (1 relevé). La valeur technique `right-center` n'a jamais été vue. Aucun skill ne parle de directions (grep vide). À confirmer en ouvrant l'écran ; l'option précise (right + centre) reste à voir. |
| 4a | « Stoik » absent de `data/discord/SixZeroLeague/` | **Juste, mais partiel** | Absent de ce dossier (un seul fichier). Il existe dans `data/chat/sixzeroleague/export_2310.txt` (21 occurrences, flags nationaux, ligue 8), rien sur les infrastructures. |
| 4b | pierrottingchrist_29708, Youth Academy 9, 20/10 ; niveau 7-8 -> joueurs ~20 | **Juste** | 20/10 09:02 : « with level 7-8 academy players seems to be around level 20 » ; 09:05 : il achète le niveau 9 (pour son prochain choix du soir) ; 14:14 : précise « level 20 » = note générale, et que le niveau 9 affiche « U18 prospect skills 9 to 36, scout 4 skills, 2 % foreign ». Nuance : au 20/10 09:05 il achète le 9, il ne l'a pas encore à 09:02. |
| 4c | squidwardfrommegamind académie montée tôt | **Juste** | 11/10 18:34 : « spent my whole balance on my academy instantly » ; 20/10 06:18 : niveau 7, « dumped my whole opening budget into it ». Résultats : pivot 23, ailier 19 et 22 (12/10, 16/10, 19/10). |
| 4d | Gazelle 11/10 revenus Arena d'abord | **Juste** | 11/10 18:31 : l'Arena est l'infrastructure de revenu principale devant le Fan Shop ; 18:41 : « invest on revenue infrastructure first ». |
| 4e | Nos niveaux Arena 7, Training Facilities 6, Youth Academy 5, Fan Shop 9 | **Juste** | `silver.sz_infrastructure_levels` au 2026-10-26 : Arena 7, TrainingFacilities 6, YouthAcademy 5, FanShop 9. Arena niveau 8 : 7 500 €, solde actuel 1 843 €. |
| 5 | Décalage de fuseau dans `captured_at` | **Faux : aucun décalage** | `captured_at` est en UTC (`+00`). Les 20:30/20:37 Paris sont justes : au 26/10/2026 Paris est en UTC+1 (heure d'hiver depuis le 25/10), donc 19:37 UTC = 20:37 Paris. Les exports de 19:22-19:27 UTC = 20:22-20:28 Paris. J16 = 21:00 Paris = 20:00 UTC. La page 17956 (capture 19:27:18 UTC) affiche « Round 16 in 32m », soit coup d'envoi à ~19:59 UTC : cohérent. Au moment de la requête (19:38 UTC) il restait ~22 min. |

## Corrections à appliquer
1. Dire à l'utilisateur : direction « right + centre » en J17-J18, pas en J16 (C-040) ; sinon dérogation assumée et critères décalés.
2. Donner le banc J16 nommé : Blanc, Simon, Leroy, Barros, Sundberg, G. Bertin, Chevalier ; Denis et Lemaire hors feuille de match.
3. Ne pas dire que l'option « right + centre » est vue à l'écran : seule la citation Discord (lignes 324-327) l'atteste.
4. « Stoik » : préciser qu'il est dans `data/chat/sixzeroleague/export_2310.txt`, sans lien avec les infrastructures.

## Erreurs récurrentes (learnings)
- L-nnn : avant d'annoncer qu'une décision n'a pas d'obstacle, relire la section « Réglage exact » du brief concerné (ici C-040 : exclusion de J16 écrite).
- L-nnn : tout fuseau se vérifie avec `now()` et `at time zone 'Europe/Paris'` ; `captured_at` est en UTC, Paris = UTC+1 depuis le 25/10/2026.
- Fiche du jeu : `attackDirection` observé seulement `mixed` et `left-center` ; ajouter `right-center` dès qu'un export le montre.
