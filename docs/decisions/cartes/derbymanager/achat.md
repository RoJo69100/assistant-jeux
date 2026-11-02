# Carte derbymanager — achat (enchère, joueur libre, scouting avant enchère ; deux clubs)

Sources lues : commit 6fd098a (2026-11-02)

Écrite le 2026-11-02 (`resume.md`, skill `derbymanager-club` § Transferts, `-effectif-entrainement` § Scouting ; connaissance § 7, § 8, § 9 ; learnings). Règles : chaque rendu propose un achat nommé (prix, finançable avec `capacite_invest` et `marge_salaire_jour`) ou la raison chiffrée ; jamais d'enchère sans accord ; un bloc par club.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-DM.txt:20 | acheter un joueur ? | var. 1, 6 |
| :40 | base « ce type vaut ce prix » | var. 4 |
| :41 | étudier le marché, acheter / revendre | var. 1, 9 |
| :43 | scouter ce joueur ? | var. 3 |

## Rendu (figé)
1. Marché filtré sur une fourchette de prix trop basse ou ancien : « 🟥 URGENT · Export · exporte le marché filtré <fourchette> ».
2. Un tableau par club : `| Priorité | Cible | Poste | Âge | Tier | Note au poste (bas–milieu) | Notre dernier titulaire | Gain sûr | Prix | Salaire / jour | Scouté (niveau) | Finançable (caisse et marge salariale) |`.
3. Une ligne par cible : pourquoi, ce qui prouvera l'erreur.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Cibles | `select club, name, vendeur, pos, age, tier, price, salary, cles_vues, note_min, note_milieu, dernier_titulaire, gain_milieu, gain_sur from gold.dm_marche_notes order by club, gain_sur desc limit 20` (**ne pas lire `gold.dm_marche_postes`**) | Gain sûr = bas de fourchette au-dessus de notre dernier titulaire | `resume.md` § Vues prêtes | aucun gain sûr à 0,3-7,5 M (L-004) |
| 2 | Filtre de l'export | `silver.dm_market` (prix min / max vus) | L'export suit le filtre de prix de l'écran | L-004 ; `resume.md` § Pièges | |
| 3 | Scouting | — | Scouter au moins une fois pour voir prix et exigences et enchérir ; 3 scouts gratuits par jour, stock de 20 ; niveaux 0-3, −1 par semaine ; 3e scout = stats de match | connaissance § 7, § 8 | |
| 4 | Prix de référence | `select tier, ages, n, p25, mediane, p75, salaire_moy from gold.dm_prix_reference` | « No bargains, prices correlate to quality » ; « oldies are really worth it » : Solid 31+ médiane 8,0 M contre 11,1 M à 24-27 ans | dev 2026-02-07, 2026-10-05 ; reprise 2026-10-31 § 2 | |
| 5 | Salaire et prime | `salary` | Prime de signature : 0 pour un joueur du pays, 500 k minimum sinon ; « 1 k de salaire = 100 k de prime » ; offrir un peu plus, le premier enchérisseur est préféré | connaissance § 7 | |
| 6 | Argent | `select club, money, flux_jour_estime, salaries_committed, salary_cap, marge_salaire_jour, capacite_invest from gold.dm_finances_bilan` | Prix + frais > `capacite_invest` moins dépenses déjà décidées (Tactic 8 M) ou salaire > `marge_salaire_jour` = abandon | `resume.md` § Ce que l'utilisateur attend | QoS 22 983 477, marge 703 k/jour (02/11 21:50) ; reste 14,98 M après Tactic |
| 7 | Frais | — | Solidarity fee : 5 % à l'équipe formatrice + 5 % au joueur | connaissance § 7 (2026-09-06) | |
| 8 | Décision du joueur | — | Jusqu'à 3 jours ; à la 4e offre la 3e meilleure peut être rejetée | connaissance § 7 | |
| 9 | Équilibre d'effectif | `gold.dm_effectif` (âges) | 5 vieux / 5 au pic / 5 en progression / 5 de l'école | dev 2025-05-16 | |
| 10 | Pièges | — | Acheter un blessé sans le voir ; plafond salarial faux jusqu'au lundi après changement de saison | connaissance § 13 | |
| 11 | Avis des amis | connaissance § 7 | 2 bons joueurs plutôt que 7 moyens | dev (connaissance § 7) | |
| 12 | Comparer au bon titulaire | `gold.dm_marche_notes.dernier_titulaire` | La vue compare au plus faible joueur de la ligne (307 D : Labourd 8,6) ; le gain réel se calcule contre le titulaire que la cible remplace (Desagnat 12,6) | police 2026-11-02 | Mansfield 11,8 / 15,5 (−0,8 / +2,9), Alex 12,8 / 15,1 (+0,2 / +2,5) |
| 13 | Marché exporté | `gold.dm_marche_notes` (302 lignes par club) | Prix 0,2 à 8,1 M (export 547 du 01/11 ; 307 du 30/10) ; 8-20 M absent | police 2026-11-02 | 547 : aucun gain sûr (max −0,9) ; 307 : 18 gains sûrs > 0 |
| 14 | Colonne FEES (page transferts) ➕ | bronze `transfers` : regex `prix:: x frais:: y salaire:: z` sur le HTML nettoyé | Frais moyens 22,6 % du prix (médiane 21,5 %, 10-60 %) ; ≈ 0,136 × prix + 16,9 × salaire/jour ; « 1 k = 100 k de prime » ne s'y retrouve pas | police achat 2026-11-02 21:58 (354 lignes, export 21:50) | Mansfield ≈ 0,58 M, Benigno ≈ 1,6 M, Sheridan ≈ 1,2 M |
| 15 | Limite de 25 (achat) ➕ | `select count(*) from gold.dm_effectif where club='Queen of the South'` | Seule la promotion de l'école est bloquée à 25 ; « attendu 18 à 25 » (dev 2023-05-02) ; blocage de l'achat : non trouvé, à tester en posant l'offre | connaissance §6 ; Discord part3 2023-05-02 | 547 = 25 (Almgren inclus) |
| 16 | Contrat de la cible ➕ | fiche `players_id` (« Until … N days left » / « Daily rolling contract ») | Contrat à 0 jour ou roulant = joueur bientôt listé, prix −10-15 % ; exigences peuvent monter pendant la décision (offre rejetée si salaire trop juste) | connaissance §7 ; Discord 2024-06-07 | Mansfield 0 j ; Sheridan roulant ; Benigno 89 j |
| 17 | Mentor de la cible ➕ | fiche `players_id` : « highly experienced (tactic +3) » | Mentor = installation de groupe (10 pts = demi-étoile), −1 point au transfert ; ne justifie pas un achat sans gain sûr | connaissance §5 | Benigno tactic +3 (GK) |
| 18 | Enchère maximale ➕ | — | Offre maximale posée en premier = non battable ; plafond conseillé 110 % du prix affiché sous le p25 de `dm_prix_reference` ; salaire = demande + ~10 k ; prime ≥ 500 k hors pays | connaissance §7 (2025-09-08, 2026-08-13) | Mansfield 3,85 M / 16 k/j |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|
| L-004 | Exporter une fourchette de prix plus haute avant de conclure « aucune cible » | 2026-11-02 | à contrôler (C-005) |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
