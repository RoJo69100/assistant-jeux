# Carte hockeynation — finances (plafond, prolongations, coachs, scouts)

Sources lues : commit d1eaf11 (2026-11-02)

Écrite le 2026-11-02 (fiche `finances.md`, `resume.md` § Scouts et coachs, skills `hockeynation-contrats-finances`, `-coachs-entrainement`, `-draft-scouting` § Scouting ; connaissance § Contrats, § Coachs). Plus d'agent `finances` depuis le 2026-11-02 : je lis ces vues moi-même. Seuls les contrats PRO comptent dans le plafond.

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:168 | beaucoup d'argent : que faire, axes | var. 1, 2, 7 |
| :157 | niveau de l'entraîneur | var. 6, 7 |

## Rendu (figé)
1. `| Saison | Plafond | Engagé | Rachats | Cap space |` (`gold.hn_cap_outlook`), avant / après chaque opération envisagée.
2. Prolongations : `| Joueur | Âge | Note | Pot. min–max | Agent (humeur) | Demande (salaire × ans) | Verdict | Cap space après |`.
3. Coachs : `| Équipe | Head actuel | Somme match | Meilleur candidat | Âge / xp | Gain d'équipe | Droits U17/U21 | Offre en cours |`.
4. Scouts : tableau de la carte `academie` var. 4 (budget restant en tête).

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Cap space actuel | `select captured_at, salary_cap, projected_salary, cap_space from silver.hn_cap_now order by captured_at desc limit 1` | Jamais négatif (−30 % en match si négatif plus d'1 h avant) | skill contrats-finances ; Discord (lecture 2026-10-29) | |
| 2 | Saisons suivantes | `select season, cap_projected, committed, contracts, buyouts, cap_space from gold.hn_cap_outlook order by season limit 4` | S28 : plancher salarial 50 % (base non publiée) | hnadmin 2026-10-25 (en doute) | |
| 3 | Prolongations | `select name, age, rating, main_position, agent, talk_status, agent_mood, asked_salary, asked_years from silver.hn_expiring order by rating desc limit 15` ; `silver.hn_extension_offers` | Durée selon l'âge, frais d'agent ; Bélanger géré par l'utilisateur | skill contrats-finances § Prolongations ; [U] 2026-10-30 | |
| 4 | Rachats | `gold.hn_buyout_calc` | Voir carte `vente` var. 4 | carte vente | Eskelinen 1 285 000 $/saison S27-S29 |
| 5 | Paies | `gold.hn_today` | Paies jours 8-42 ; un départ avant la paie libère le salaire | `resume.md` § Saison 27 | |
| 6 | Coachs : options | `select team_level, head, coach, match_sum, meilleur_candidat, age_candidat, xp_candidat, gain_equipe, saisons_avant_retraite, offre_en_cours from gold.hn_coach_options limit 12` | Head compte double ; embauches jours 1-35 ; un coach arrivé cette saison (`firstSeason`) ne se remplace pas ; retraite à 65 ans ; une offre de head coach par jour | skill coachs-entraînement ; gordie_79 2026-10-25 ; `resume.md` | |
| 7 | Coachs : candidats U17 / U21 | `select coach, age, xp, note, match_sum, marge, talents_forts_de_match, ok_u17, ok_u21, offre_envoyee from gold.hn_coach_candidats order by marge desc limit 15` | U17 : note ≤ 54 et xp ≤ 4, 2 talents forts de match, plus grande marge ; U21 : note ≤ 69 et xp ≤ 7 | [U] 2026-10-29 | |
| 8 | Score d'équipe des coachs | `gold.hn_coach_potential` ; `gold.hn_club_compare` (`hc_match_sum`, `staff_match_sum`) | Coach rating = score des compétences de match, pas la note affichée ; comparer aux autres clubs de la ligue | hnadmin 2026-10-29 ; CLAUDE.md règle 6 | |
| 9 | Scouts : budget | `silver.hn_scouting_budget` (date du relevé) | 300 000 $ par saison, 8 scouts au plus | skill draft-scouting | |
| 10 | Déclarés non exportés | `select * from silver.hn_declared order by 1 desc limit 20` | Le déclaré l'emporte jusqu'au prochain export | `resume.md` § Tableaux prêts | |
| 11 | Avis des amis | connaissance § Contrats / plafond / rachats / agents, § Coachs ; `connaissance-A-staff.md` | Favors d'agents S27 ou S28 (désaccord) : tester avant de compter dessus | lecture Discord 2026-10-29 | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis | Statut (base) |
| --- | --- | --- | --- | --- |
| L-011 | Coach PK adverse supérieur (Ottawa 62 contre 59) : le score de match des coachs pèse en série | 2026-11-02 | à surveiller | hypothèse |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
