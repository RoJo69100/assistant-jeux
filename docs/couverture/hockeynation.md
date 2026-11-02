# Registre de couverture — Hockey Nation

Créé le 2026-11-02 (plan de conception iso BasketVibe, `docs/decisions/variables.md` § Mise en route). Hockey Nation n'a pas de liste propre dans `docs/chose-a-faire*.txt` : ce registre couvre le bloc « Tous jeux » (`docs/chose-a-faire.txt`, lignes 160-177) et les règles Hockey Nation de CLAUDE.md et de `docs/fiches/hockeynation/resume.md`. Statuts : ✅ répondu · 🔧 mécanisme fait, limite connue · ❌ manque, avec le plan. Les découvertes (facteurs que l'utilisateur ne connaît peut-être pas) sont en lignes `+N`.

Cartes : `docs/decisions/cartes/hockeynation/<type>.md` (composition, defaite, achat, vente, entrainement, academie, finances).

## Tous jeux
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| 160 | Même ordre que l'écran pour la saisie | carte `composition` § Rendu (`gold.hn_tactique_rendu order by ordre`, ordre de l'écran Lineups) ; carte `entrainement` § Rendu | ✅ |
| 161 | Meilleures caractéristiques de chaque joueur | `gold.hn_tactique_effectif_poste`, `gold.hn_player_fit`, `gold.hn_player_potential` ; cartes `composition` var. 2-3, `achat` var. 2-3 | ✅ |
| 162 | Actions claires, aujourd'hui seulement | CLAUDE.md § Horizon ; rendu des cartes | ✅ |
| 163 | Pas de « si », vérifications tout le temps | R-5 ; hooks `pipelines/police.py` et `forme.py` (HN 4 équipes) ; checks chiffrés des cartes | ✅ |
| 164 | Réponses simples, mise en forme | rendu des cartes ; un tableau par équipe (PRO, FRM, U21, U17) | ✅ |
| 165 | Des tableaux | rendu des cartes | ✅ |
| 166 | Tout vérifier, apprendre de ses erreurs | `outputs/hockeynation/learnings.md` (L-001 à L-016) ; § Checks appris des cartes | ✅ |
| 167 | Pas d'hypothèse sans vérifier | statut confirmé / en doute de la connaissance ; [H] dans `gold.hn_position_keys` | 🔧 compétences clés par poste encore hypothèse [H] |
| 168 | Beaucoup d'argent : que faire, axes à améliorer | carte `finances` var. 1-2, 6-8 (cap space, coachs) + carte `achat` | ✅ |
| 169 | Beaucoup de défaites : prendre une action | carte `defaite` var. 11 + `analyste` / `decideur` | ✅ |
| 170 | Nouveauté : tester en amical, sinon proposer comment | carte `composition` var. 12 (amicaux jouables, pénalité de poste active, pas d'expérience) | ✅ |
| 171 | Chaque règle parfaite, mine d'or étudiée à 100 % | lecture intégrale Discord du 2026-10-29 (`connaissance-A/B/C`, ≈ 380 faits, 46 propositions appliquées) | 🔧 sens exact des réglages du plan de jeu à confirmer par test |
| 172 | Quel export chaque jour, quoi faire après | `gold.hn_exports_state`, `gold.hn_today`, `gold.hn_daily_alerts`, `outputs/hockeynation/exports-a-faire.md` | ✅ |
| 173 | Ordre logique des actions, dépendances | `docs/attentes/jeux/hockeynation.yaml` § dependances ; `resume.md` § Ordre des agents | ✅ |
| 174 | Mettre à jour agents/skills à chaque nouveauté | veille → skills ; `dossier.py` rend le nouveau depuis le commit de la carte | ✅ |
| 175 | Retour des joueurs expérimentés Discord | connaissance ; variable « avis des amis » de chaque carte | ✅ |
| 176 | Facteurs cachés révélés dans les discussions | lignes `+N` ci-dessous | ✅ |
| 177 | Export incomplet : le dire, je le refais | `gold.hn_exports_state`, `gold.sante_collecte`, `gold.exports_nouvelles_cles` ; « il me manque X, fais l'export Y » | 🔧 `gold.exports_nouvelles_cles` à appliquer en base |

## Règles Hockey Nation (CLAUDE.md, resume.md)
| Ligne | Demande | Réponse | Statut |
|---|---|---|---|
| H1 | 4 équipes, un bloc chacune, 20 joueurs (4 C / 4 LW / 4 RW / 3 LD / 3 RD / 2 G) | rendu des cartes `composition`, `achat`, `vente`, `academie` ; hook `forme.py` (HN 4 équipes) | ✅ |
| H2 | Talents fort/faible contre le poste d'abord | `gold.hn_player_fit`, `gold.hn_draft_board` ; check des cartes | ✅ |
| H3 | Tout ajout de joueur = équipe résultante à 20 | cartes `achat` § Rendu 3, `academie` § Rendu 4 | ✅ |
| H4 | Effet sur le plafond de toute opération | `gold.hn_trade_value`, `gold.hn_buyout_calc`, `gold.hn_cap_outlook` ; cartes `achat` var. 5, `finances` var. 1-2 | ✅ |
| H5 | Lignes FRM/U21 réellement alignées | ❌ absentes de la base (`club_lineups` = PRO) ; on les réunit par l'export d'une page de match FRM ou U21 jouée | ❌ plan : export d'un match FRM et U21 |

## Découvertes (facteurs cachés)
| Ligne | Fait | Source | Où il sert |
|---|---|---|---|
| +1 | Lineup saisie moins d'1 h avant le match = risque de −30 % aux compétences | hnadmin 2025-07-10 | carte `composition` var. 1 |
| +2 | Le « coach rating » d'équipe = score des compétences de match, pas la note affichée du coach | hnadmin 2026-10-29 | cartes `finances` var. 8, `defaite` var. 8 |
| +3 | Mise au jeu : un bon FOF par ligne suffit, pas forcément le centre | talonflame1 2026-04-04 | carte `composition` var. 5 |
| +4 | En amical la pénalité de mauvais poste s'applique, pas celle du plafond | d0ghouse 2026-10-28 | carte `composition` var. 12 |
| +5 | Rachat : coût qui baisse si on attend ; plafond libéré tout de suite | hnadmin 2025-07-02, 2026-07-22 | carte `vente` var. 4 |
| +6 | S28 : plancher salarial de 50 % (base non publiée) | hnadmin 2026-10-25 | cartes `achat` var. 6, `finances` var. 2 |
| +7 | Capitaine : aucun effet mesuré sur nos résultats | L-009 | carte `composition` var. 10 |
| +8 | Gardien END bas : arrêts plus faibles en 3e période | L-016 ; talonflame1 2026-04-04 | cartes `composition` var. 4, `defaite` var. 3 |
