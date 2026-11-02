# Carte sixzeroleague — composition (tactique par défaut : formations, direction, agressivité, 7 titulaires + remplaçants)

Sources lues : commit 4bd592f (2026-11-02)

Écrite le 2026-11-02 (fiche `tactique.md`, `resume.md`, skills `sixzeroleague-match`, `-joueurs`, `-communaute` ; connaissance § 1, § 2, « Ce qui change nos décisions » ; learnings). Règles : R-4 (saisie dans l'ordre de l'écran : formations, direction, agressivité, puis rôle → titulaire → remplaçant GK, CB, LB, RB, LW, RW, P) ; une seule tactique par défaut pour tous les matchs, refaite seulement si un joueur change ; pas d'amical : une nouveauté se teste en ligue, une option à la fois (A-6).

## Lignes de la liste couvertes
| Ligne | Texte court | Variable(s) |
|---|---|---|
| chose-a-faire.txt:61 | coupe / ligue : paramètres de chacune | var. 1 |
| :96 | quelles tactiques | var. 3-6 |
| :97 | tableau : poste, formations, direction, agressivité, remplacements | Rendu |
| :98 | ordres de match | var. 9 |
| :99 | stratégie selon nos matchs contre cet adversaire | var. 2 |
| :100 | stratégie selon toute la saison, blessés, réussite | var. 7, 8, 11 |
| :160 | même ordre que l'écran | Rendu |

## Rendu (figé)
1. `select ordre, reglage, valeur, export_le from gold.sz_saisie_reglages order by ordre` → `| Réglage | Valeur à saisir | Dans le jeu |` (formation d'attaque, formation de défense, direction, agressivité).
2. `select role_tactique, poste, ordre, joueur, role_joueur, note_au_poste, controle, meilleur_naturel, suggestion from gold.sz_saisie_tactique order by ordre` → `| Rôle | Titulaire | Note au rôle | Remplaçant | Contrôle |` dans l'ordre GK, CB, LB, RB, LW, RW, P.
3. Contrôle SQL rendu : 7 joueurs différents, aucun blessé ni suspendu, remplaçants différents des titulaires et jamais remplaçants à deux postes.
4. Heure limite : prochain coup d'envoi (13:00 ou 21:00 Paris ; coupe 17:00).

## Variables
| # | Variable | Où la lire | Check | Source du check | Dernière valeur |
|---|---|---|---|---|---|
| 1 | Prochain match | `select today, etape_du_jour, prochain_match, intersaison from gold.sz_today` ; `silver.sz_fixtures` | Ligue 13:00 et 21:00, coupe 17:00 (terrain neutre, sans avantage du terrain) ; même tactique pour tous | `resume.md` § Rythme ; fiche match § 2 | |
| 2 | Adversaire | `select journee, adversaire, domicile, rang_adv, bot, bilan_vnd, bp, bc, forme_adv, nos_confrontations from gold.sz_adversaires limit 3` ; tactique adverse : `teams.tactics` du match | 2e rencontre : chaque adversaire déjà vu nous a battus de plus (−8,2 en moyenne) ; `teams.tactics` souvent vide : exporter le match juste après le coup de sifflet | L-025 ; `resume.md` § Pièges | |
| 3 | Formation d'attaque | `gold.sz_saisie_reglages` | 5-1 = meilleur contre une défense 6-0 ; 4-2 = sans CB (incompatible avec un CB atout comme Fournier), bon seulement contre 3-3 | Gazelle 2026-10-24 (connaissance 1.3, 1.6) ; L-029 | 5-1 |
| 4 | Formation de défense | idem | Aucune source ne dit quelle défense contre un 5-1 ; 3-2-1 / 3-3 pressent plus ; un ailier y défend hors poste | connaissance 1.3, 1.11 | 6-0 |
| 5 | Direction | idem | right-center : 52 tirs par match contre ~42, part CB + P 52 % ; « left/right + centre » = CB et P attaquent le plus, sans chiffre d'effet | L-031 ; connaissance 1.7 | right-center (C-043) |
| 6 | Agressivité | idem | Effet non documenté ; discipline = cause de défaite (exclusions → 7 m adverses) | connaissance 1.13 ; L-002, L-010, L-012 | Normal |
| 7 | Joueur au rôle | `gold.sz_lineup_natural`, `gold.sz_slot_options` (`no_penalty`, `rating_before_penalty`) | Hors-poste : −20 % attaque, −10 % défense, joueur de champ au but −20 % ; la pénalité de défense suit la place défensive ; `role_overalls` calculé avant pénalité | Gazelle 2026-10-13 (2.1) ; connaissance 1.8 | |
| 8 | Blessés, suspendus | `silver.sz_players` (`injured`, `suspended`) | Rouge direct = 1 match à l'écran (2 journées si rapport d'arbitre, devlog 0.5.7) ; blessure 1-6 matchs | fiche tactique § Contraintes ; connaissance 2.7, 7.1 | |
| 9 | Remplaçants et ordres | `silver.sz_tactics` (`kind`) | Remplacement automatique **uniquement** sur blessure ou rouge, une entrée par match ; pas de « rotation » ; ordres de match sans remplacement (« not yet ») | connaissance 2.14b, 2.14d, 1.12 ; L-013, L-016, L-032 | |
| 10 | 7 m | — | Tiré automatiquement par le meilleur tireur sur le terrain : ne pas proposer de tireur | Gazelle 2026-10-20 (2.3) ; L-006 | |
| 11 | Toute la saison | `select * from gold.sz_vd_comparatif` | Défaites perdues en 1re mi-temps (−4,5) et dans les 15 premières minutes (−3,6), liées au solde d'exclusions (r = 0,75) | `resume.md` § Pièges ; L-028, L-007, L-004 | |
| 12 | Efficacité par poste | `silver.sz_match_players` | Pivot stable ~73 % ; LW en baisse depuis J10 (Lefebvre) ; Fournier CB 56,8 % | L-026, L-021, L-033, L-030, L-020 | |
| 13 | Forces de l'équipe | — | « Jouer selon les forces de son équipe plutôt que contrer » | Gazelle (1.4) | |
| 14 | Avis des amis | connaissance § 1, § 2, § 7 | Pour moins de jaunes / 2 min : Marquage, puis Anticipation et Duels (avis) | Antarez 2026-10-16 (7.3) | |

## Checks appris
| L-nnn | Check | Ajouté le | Résultat depuis |
|---|---|---|---|
| L-004 | Fins de match perdues (4 des 5 derniers buts) | 2026-11-02 | à surveiller (L-032) |
| L-006 | 7 m : tireur automatique, nos 7 m décisifs dans les matchs serrés | 2026-11-02 | confirmé |
| L-007 | Départ lent à l'extérieur | 2026-11-02 | confirmé (L-028) |
| L-013 | Aucun remplaçant entré sans blessure ni rouge | 2026-11-02 | confirmé |
| L-016 | Mêmes 7 titulaires, deux défaites de −10 : cause non isolée | 2026-11-02 | à surveiller |
| L-020 | Denis CB meilleur tireur récent (58 %) | 2026-11-02 | vendu (27/10) |
| L-021 | Lefebvre LW : exclusions et tir en baisse | 2026-11-02 | confirmé (L-033) |
| L-024 | Mêmes réglages des deux côtés J13-J15 : la tactique ne départage pas | 2026-11-02 | à surveiller |
| L-026 | Pivot efficace et stable, LW en baisse | 2026-11-02 | confirmé |
| L-028 | 15 premières minutes = l'écart, lié aux exclusions | 2026-11-02 | à surveiller |
| L-029 | Contres des formations (devlog 0.6.1, Gazelle) | 2026-11-02 | source |
| L-030 | Fournier CB 56,8 % | 2026-11-02 | à surveiller (C-039, C-047) |
| L-031 | right-center : plus de tirs, plus de CB + P | 2026-11-02 | à surveiller (2 matchs) |
| L-032 | Fins de match : 29-44 en 5 matchs, aucun remplaçant | 2026-11-02 | à surveiller |
| L-033 | Lefebvre 0/5 hors 7 m | 2026-11-02 | à surveiller (C-042, C-048) |

## Historique des changements de checks
| Date | Check | Avant → après | Pourquoi |
|---|---|---|---|
