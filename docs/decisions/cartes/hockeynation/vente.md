# Carte hockeynation — vente (échange sortant, rachat, libération, non-prolongation)

Sources lues : commit 0000000 (2026-11-02)

Écrite le 2026-11-02 (fiche `transferts.md`, `finances.md`, skills `hockeynation-contrats-finances`, `-compositions-trades`, `-joueurs`). Règles : dire « échanger », jamais « vendre » ; FRM : ouvrir une négociation sans prolonger = il part ; U21 : ELC ou Farm à 21 ans, sinon départ à 22 ans ; équipe résultante à 20.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:168 | beaucoup d'argent / axes à améliorer | var. 5, 6 |

## Rendu (figé)
`| Priorité | Joueur | Équipe | Poste | Âge | Note | Potentiel min–max | Classe / futur | Remplaçant interne | Contrat (salaire, fin) | Option (échange / rachat / départ) | Cap space après | Moment |`, puis l'équipe résultante à 20 (VIDE signalé). Une ligne par joueur : pourquoi, et ce qui prouvera l'erreur.

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Candidats au départ | `select team_level, name, poste, age, rating, pot_min, pot_max, classe, futur, fit from gold.hn_player_potential where futur = 'VIRER' or classe = 'Nul' order by team_level limit 20` | Futur VIRER ou contre-emploi sans poste tenable | skill `hockeynation-potentiel-joueurs` | |
| 2 | Rôle dans la lineup | `select poste, joueur, roles, nb_roles from gold.hn_tactique_effectif_poste where joueur = '<nom>'` | Un titulaire L1-L2, PP ou PK ne part que remplacé (nommé) | fiche tactique § Rendu figé et objectif | |
| 3 | Remplaçant interne | `gold.hn_depth_chart` (même poste, `ord` suivant, FRM et U21 compris) | Écart de note et verdict talents du remplaçant | `resume.md` § Règles | |
| 4 | Rachat ou échange | `select name, saisons_restantes, rachat_total, rachat_par_saison, soulage_rachat, soulage_echange, cap_space_si_rachat, cap_space_si_echange, rachat_possible from gold.hn_buyout_calc where name = '<nom>'` | Rachat interdit pour un agent libre de la saison ; coût du rachat baisse si on attend (« moitié du restant » non confirmé : lire l'écran) ; plafond libéré à l'action | hnadmin 2025-07-02, 2026-07-22 | Eskelinen racheté, 1 285 000 $/saison S27-S29 (`silver.hn_declared`) |
| 5 | Fin de contrat | `select name, age, rating, main_position, agent, talk_status, agent_mood, asked_salary, asked_years from silver.hn_expiring order by rating desc limit 15` | Humeur remise à « happy » après un échange ; réponse garantie à la dernière mise à jour de saison ; Contract Year Special actif à 1 an | hnadmin 2026-04-22, 2026-10-22 | |
| 6 | Valeur d'échange | `select name, age, rating, position, verdict, salary, contract_to, cap_space_apres from gold.hn_trade_value where own and name = '<nom>'` | Barème note minimale → tour de draft (avis) ; cap dump : < 1 M = 4e tour… 7-10 M = 1er (avis) ; peu de preneurs de cap dumps (seany148 en prend) | talonflame1 2026-04-14 ; #trade 2026-10 | |
| 7 | Moment | `gold.hn_today` | Départ avant la paie (jour 8, puis chaque paie jours 8-42) libère le salaire ; fenêtre I ferme jour 35 | `resume.md` § Saison 27 ; skill contrats-finances | |
| 8 | U21 de 21 ans | `select * from gold.hn_daily_alerts limit 20` (U21 sans contrat) | ELC PRO ou Farm, sinon départ à 22 ans sans rien | `resume.md` § Règles | |
| 9 | FRM de 25 ans et plus | `silver.hn_expiring` (route `contract-talks-farm-players`) | Sans négociation il reste ; ouvrir sans prolonger = il part | `resume.md` § Règles | |
| 10 | Souhaits de l'utilisateur | fiche transferts § Livrable 2 (2026-10-23 : Pålsson, Burns, Carpentier ; garder Kabát, Koukal) ; `resume.md` (Carpentier ne peut pas bouger) | Le registre `fait-` et `resume.md` l'emportent sur la fiche (Carpentier bloqué) | [U] 2026-10-29 | |
| 11 | Avis des amis | connaissance § Échanges, § Contrats ; `connaissance-C-2026-trade-events.md` | — | connaissance | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
