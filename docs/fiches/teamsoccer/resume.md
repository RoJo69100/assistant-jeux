# Team Soccer — résumé pour les agents (remplace attentes.md + teamsoccer.yaml + commun.md)

Lu par chaque agent **à la place** de `docs/attentes/attentes.md`, `docs/attentes/jeux/teamsoccer.yaml` et `docs/fiches/teamsoccer/commun.md`. N'ouvre ces trois fichiers que si ta tâche touche une ligne marquée « → source ». Mis à jour dans le même commit que toute modification de ces trois fichiers (écrit le 2026-10-27).

## Jeu
- `teamsoccer`, préfixe `ts_` (bronze `game = 'teamsoccer'`). Football, monnaie $. Heures affichées en Paris (`captured_at` en UTC ; heures du jeu = Canaries).
- **Deux clubs, deux économies, deux marchés** — toujours un bloc chacun, jamais un seul :
  - `18` **Chomelix Cows** (équipe première, Division I) : marché **masculin**.
  - `15858` **Ben Ahmed Donkey** (équipe féminine, Women's TS League, Division III) : marché **féminin** (`silver.ts_transfer_listings.market`).
- Résultat d'un match = notre côté (`gold.ts_match_report.result`, `gold.ts_vd_comparatif`), jamais le score domicile–extérieur brut.
- Sources : `[G:Rubrique]` guide > `[F:date pseudo]` forum (Admin-Dev = développeur, Admin-PIPO68 = administrateur) > `[P:Page]` écran > `[Obs]`. Connaissance : `outputs/teamsoccer/veille/connaissance.md` (95 entrées, lue jusqu'au 2026-10-27). Pas de Discord. Skills `teamsoccer-joueurs|match|entrainement|club|saison|communaute`.

## Rythme (→ source : yaml `rythme`)
| Quoi | Quand (Paris) | Saisie |
|---|---|---|
| Ligue Cows | mardi et samedi 13:50 | composition au plus tard 2 h avant |
| Ligue Ben Ahmed | lundi et jeudi 19:30 | idem |
| Coupes | en semaine (`gold.ts_upcoming.lineup_deadline_paris`) | idem |
| Entraînement et Forme | vendredi | réglage par joueur |
| Finances | lundi 00:05 (heure du site) | — |
| Académie | chaque jour, 3 révélations par club (reset 01:00 UTC) | — |
- Saison 3 : ligue du 2026-10-12 au 2026-11-28 (9 semaines : ligue 1–7, barrages 8, repos 9).
- Sans composition enregistrée, le jeu remplit les 11 postes tout seul (jamais de forfait, mais moins bon).

## Juger un joueur (règle du 2026-10-27 : « je m'en fous de l'overall »)
- **Compétence clé du poste** contre l'effectif au même poste, jamais l'OVR : GB Gardien · DEF Défense · MIL Conduite (`dribbling`) · ATT Finition ; Contrôle en 2e partout [skill joueurs § Compétences clés].
- Valeur au match = compétence × (0,70 + 0,30 × Forme/100). La Forme ne bouge qu'au vendredi.
- L'OVR des jeunes estimé par la formule du skill n'est pas fiable (72 estimé contre 64 réel sur les adultes).

## Vues prêtes (lis-les avant de calculer ; une requête, colonnes choisies, `LIMIT`)
| Besoin | Vue |
|---|---|
| Argent disponible pour un achat | `gold.ts_capacite_invest` (solde − 2 semaines de salaires + entretien − dépenses décidées non relevées, table `silver.ts_depenses_decidees`) |
| Places de stade : quel type, combien | `gold.ts_stade_choix` (4 types classés par remboursement, places achetables avec la capacité) |
| Effectif par poste, titulaire / remplaçant / surplus / en vente | `gold.ts_effectif_bilan` |
| Cibles du marché (meilleures que le plus faible titulaire, finançables ou non) | `gold.ts_marche_cibles` |
| Verdict de chaque jeune (MONTER / VENDRE / RÉVÉLER x) | `gold.ts_academie_verdict` |
| Victoires / nuls / défaites comparés sur toute la période | `gold.ts_vd_comparatif` |
| Composition proposée du prochain match (onze + banc de 6, ordre de l'écran) | `gold.ts_saisie_composition` |
| Autres | `gold.ts_upcoming`, `ts_agenda`, `ts_daily_alerts`, `ts_match_report`, `ts_player_match_ratings`, `ts_match_plays`, `ts_finance_status`, `ts_stadium_payback`, `ts_academy`, `ts_hpc_status`, `ts_player_progress`, `ts_season_calendar` |
- Une vue donne les chiffres ; l'agent décide. Si elle contredit le registre `outputs/teamsoccer/fait-AAAA-MM-JJ.md` (action faite après l'export), le registre l'emporte.
- `ts_saisie_composition` ne donne ni les consignes par zone ni les remplacements programmés : c'est le travail de l'agent Tactique.

## Ordre des agents (tu lis les briefs du jour `outputs/teamsoccer/briefs/AAAA-MM-JJ-<domaine>.md` de ceux avant toi)
Veille (si nouvelle source) → Match → Effectif → Finances-personnel → Académie → Entraînement → Tactique → Transferts. Un agent aval qui contredit un amont l'écrit en tête de son résumé.

## Ce que l'utilisateur attend (condensé ; → source : `docs/attentes/attentes.md`, `CLAUDE.md`)
- **Horizon : aujourd'hui seulement.** L'utilisateur n'agit que le jour même, le soir. Jamais « demain », « le 29 », « après le prochain match » comme étape ; un match de demain se prépare aujourd'hui.
- **Rendu** : actions « fais X » avec joueur, valeur, heure limite ; tableau 🟥 URGENT / 🟧 IMPORTANT / 🟩 SUIVI · catégorie · action ; saisie complète dans l'ordre de l'écran ; aucun « si » ; donnée manquante = « il me manque X, fais l'export Y » ; ne jamais redemander ce que `fait-…` ou la base prouvent ; une décision, le doute en une demi-ligne.
- **Finançable d'abord** : un achat n'est proposé que si `capacite_invest` le couvre (règle apprise 16) ; sinon la cible est abandonnée, pas « à surveiller ».
- **Effectif à chaque passage** : verdict par poste (acheter / vendre / garder, joueur nommé, prix) ; une vente identifiée reste ouverte jusqu'à exécution ; jamais d'enchère ni de vente lancée sans accord.
- **Défaite** = analyse chiffrée contre toute la saison (`gold.ts_vd_comparatif`), 3 à 5 points testables ; conseils `C-nnn` → `L-nnn` dans `outputs/teamsoccer/learnings.md`.
- **Export daté** : donne l'heure de l'export avant un verdict (règle apprise 18) ; compte les jeunes complets à chaque export d'académie (règle 17).
- **Coût** : brief d'une page, résumé de 10 lignes, delta du jour seulement.

## Pièges connus
- L'export d'effectif garde les joueurs vendus à la banque jusqu'à la fin de l'enchère (Min-ji Mori le 2026-10-27) : `ts_effectif_bilan.statut = 'en vente'`.
- Deux joueurs différents peuvent porter le même nom (Étienne Roux : gardien 296383 chez les Cows, attaquant 315 vendu) : compare toujours `player_id`.
- Le relevé du stade (`silver.ts_stadiums`) date du 2026-10-19 : l'achat de places du 2026-10-27 (Cows) n'y est pas encore, il est dans `silver.ts_depenses_decidees`.
- Matchs sans détail en base (dont Ajax–Cows 0-4, 2080875, match d'admin) : `ts_vd_comparatif.with_detail` ; il faut exporter la page du match.
- Écart inexpliqué du solde Ben Ahmed au 2026-10-27 (506 299 $) : relevé finances à refaire.
- Champs bruts non lus et options observées : → source `commun.md` § Options observées (lecteur-exports seulement).
