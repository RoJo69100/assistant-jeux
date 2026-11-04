# Carte derbymanager — vente (liste de transfert, libération, fin de contrat, prolongation ; deux clubs)

Sources lues : commit 87dc954 (2026-11-02)

Écrite le 2026-11-02 (`resume.md`, skill `derbymanager-club` § Transferts, § Contrats ; connaissance § 4, § 7). Règles : jamais de vente sans accord ; une vente identifiée reste ouverte jusqu'à exécution ; un bloc par club.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-DM.txt:33 | ce joueur est-il à vendre | var. 1, 2 |
| :42 | faut-il vendre nos joueurs | var. 1-7 |

## Rendu (figé)
Un tableau par club : `| Priorité | Joueur | Poste | Âge | Note au poste | Rang à son poste | Statut (Key…Backup) | Satisfaction temps de jeu | Contrat (jours) | Salaire / jour | Prix | Option (lister / libérer / prolonger / laisser partir) |`.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Candidats | `select club, ligne, rang_ligne, name, pos, age, note_poste, temps_jeu_satisf_pct, statut_contrat, temps_jeu_attendu_pct, statut_vestiaire from gold.dm_verdict_joueurs order by club, ligne, rang_ligne limit 60` | Trop de joueurs à un poste = plaintes : vendre ; outsider = −1 % de team spirit | `resume.md` § Règles qui décident ; connaissance § 4 | |
| 2 | Contrat | `select club, name, contract_days, salary, price from gold.dm_effectif order by contract_days limit 20` | Mise en vente possible sous 85 jours de contrat ; libération gratuite à 70 jours ou moins sous un seuil de valeur ; contrat expiré = reste, très mécontent, entraînement 0 % | connaissance § 7 | |
| 3 | Satisfaction | `temps_jeu_satisf_pct` | Transfer-listé depuis 24 h = insatisfaction annulée ; nouveau contrat remet la satisfaction à 75 % | connaissance § 4 | |
| 4 | Prolongation | `contract_days` | Bloquée si mécontent, trop bon pour le tier, ou ne peut plus s'entraîner ; renégocier ~1,5 an après la signature | connaissance § 4 | Neufeld, Bjerg à prolonger (C-003) |
| 5 | Ce qui se vend | `price` | GK facilement ; M et D à partir de 2-4 M ; F à partir de 4 M ; sous 1 M difficile ; plus longtemps listé, plus les bots regardent | connaissance § 7 | |
| 6 | Valeur qui baisse | `gold.dm_entrainement` (`price_change`) | Un joueur qui ne s'entraîne pas perd de la valeur, surtout les vieux | dev 2026-10-08 | |
| 7 | Effectif minimum | `select club, count(*) from gold.dm_effectif group by 1` | Sous 18 joueurs : risque, le jeu promeut de l'école | connaissance § 13 | |
| 8 | Avis des amis | connaissance § 7 | Un jeune ex-école vendu rend 5 % de frais à l'équipe | connaissance § 6 | |
| 9 | Listable aujourd'hui ? | `gold.dm_effectif.contract_days` | Listable seulement si `contract_days` < 85 (strict) ; ≥ 18 joueurs non listés. Le brouillon du 02/11 listait à tort Allan (87 j, 547) et Ohara (102 j, 307) | connaissance § 7 (2025-09-08) ; police 2026-11-02 | Listables : Vidales 68, King 80, Wilmot 45 (547) ; McCulloch 4, Aponte 5, Vargas 38 (307) |
| 10 | Mentors à ne pas vendre | `gold.dm_verdict_joueurs.mentor` | Un mentor retraité donne des points d'installations ; vendre un mentor retire son apport au groupe (voir carte entrainement var. 12) | connaissance § 5 ; police 2026-11-02 | 547 : Cooper, Tavernost, Vicomte, Hadjidj, Vidales ; 307 : Ohara, Charbonnier |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis | Statut (base) |
| --- | --- | --- | --- | --- |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
