# Six Zero League — résumé pour les agents (remplace attentes.md + sixzeroleague.yaml + commun.md)

Lu par chaque agent **à la place** de `docs/attentes/attentes.md`, `docs/attentes/jeux/sixzeroleague.yaml` et `docs/fiches/sixzeroleague/commun.md`. N'ouvre ces trois fichiers que si ta tâche touche une ligne marquée « → source ». Mis à jour dans le même commit que toute modification de ces trois fichiers (2026-10-27).

## Jeu
- `sixzeroleague`, préfixe `sz_` (bronze `game = 'sixzeroleague'`). Handball, **alpha** : résultats très aléatoires, règles qui changent vite [Dev chat]. Un club : **Chomelix Cow**, ligue Vanadium, 5e division, 10 clubs, 18 journées. Heures affichées en Paris (`captured_at` en UTC).
- Résultat d'un match = `silver.sz_matches.result` (W/L/D, déjà de notre point de vue), jamais le score brut.
- Rôles : GK, CB, LB, RB, LW, RW, P. 20 compétences de 1 à 100. **Pas de forme, pas de personnel, pas de jauge d'académie, pas d'amical** : ne transpose rien de BasketVibe.
- Sources : `[W:Rubrique]` wiki > `[Dev chat]` Gazelle > `[Com chat, pseudo]` (avis) > `[Obs]`. Connaissance : `outputs/sixzeroleague/veille/connaissance.md` ; Discord `data/discord/SixZeroLeague/` ; chat `data/chat/sixzeroleague/` + `silver.sz_api` `/chat/messages`.
- Confidentialité : ne jamais afficher `ownerUsername` (e-mail des autres managers).

## Rythme et compétitions
| Quoi | Quand (Paris) | Saisie |
|---|---|---|
| Ligue | chaque jour 13:00 et 21:00, verrou au coup d'envoi | une seule tactique par défaut pour tous les matchs ; on ne la refait que si un joueur change |
| Coupe | jours de coupe 17:00 [Dev chat 2026-10-18] | même tactique |
| Cycle (finances, entraînement, blessures, transferts) | chaque soir après 21:00 (2 journées = 1 cycle) | entraînement avant le cycle suivant |
| Choix U18 | toutes les 8 journées (2 prospects) | signer / ignorer |
| Fin de saison | tous les 9 à 11 jours | +1 an pour tous ; salaires fixés ; sponsor changeable une fois (re-signer = pas de prime) |
- **Corrigé 2026-10-29 (V-20261029-4)** : les annonces de transfert en cours ne se résolvent qu'à la **prochaine intersaison**, sans annulation possible ; ne lance aucune annonce à retirer [Dev chat Gazelle 2026-10-28].
- **0.6.2 (2026-10-28)** : Coupe du monde 19:00 Paris (sélectionneurs seulement) ; la saison 3 s'est finie le 2026-10-28 (finale de coupe) ; intersaison en cours, date de la saison 4 inconnue ; l'aperçu et le rapport de match montrent les tactiques favorites des deux camps (à relever) ; aucun changement de moteur [V-20261029-1, -2, -9].
- Revenus, coûts, entretien × division (pas les salaires) [W:Competitions].

## Écrans (ordre de saisie)
- Tactique : formation d'attaque `5-1` / `4-2` (sans CB) ; défense `6-0` / `5-1` / `3-2-1` / `3-3` ; direction `mixed`, `left`, `right`, `centre`, `left + centre`, `right + centre`, `left-right` ; agressivité `Light` / `Normal` / `Hard`. Places défensives : par défaut sauf test justifié.
- Composition : rôle → titulaire → remplaçant, ordre GK, CB, LB, RB, LW, RW, P ; 7 joueurs différents, un remplaçant par rôle.
- Entraînement : intensité d'équipe Light / Normal / High ; focus par joueur (groupe ou compétence) ; formation de rôle (2 saisons, 3 rôles max, rôle initial définitif).
- Le 7 m est tiré automatiquement par le meilleur tireur : ne propose pas de tireur [Dev chat 2026-10-20]. Rouge direct = 1 match de suspension [Obs 2026-10-23].

## Pièges
- **Hors-poste** (orange à l'écran) : −20 % attaque, −10 % défense, joueur de champ au but −20 % [Dev chat 2026-10-13] ; `role_overalls` est calculé **avant** la pénalité [Obs SQL 2026-10-18].
- `weekNumber` repart à 1 chaque saison : un cycle s'identifie par `applied_at`.
- Infrastructures déjà payées : lis `silver.sz_infrastructure_levels` et `silver.sz_finances.since_last_report` avant d'écrire « dépense inconnue ». Niveaux au 2026-10-27 : Arena 7, Training Facilities 6, **Youth Academy 6**, Fan Shop 9 ; solde 31 € (déclaré).
- Retard mesuré contre les autres clubs (→ source `commun.md` § Repères infrastructures) : Youth Academy 6 contre 9–10 chez Stoik et pierrottingchrist.
- **Remplacements (veille 2026-10-27)** : automatiques, **uniquement sur blessure ou rouge** (un remplaçant par rôle, une entrée par match) [W:Match, W:Injuries ; SQL 18 matchs] ; aucune règle de fatigue ni de rotation ; ne propose jamais de « faire tourner ». Nos défaites se perdent en **1re mi-temps** (−4,5 en moyenne), pas en 2e (−1,0) ; J17 : menés 16-19 à la pause (à l'extérieur), 2e MT 13-14.
- **Vente / libération** : effectif 7 minimum, 30 maximum (nous : 16) ; 500 € de frais ; pas pendant un match de ligue ; règlement toutes les 2 journées [W:Transfers]. Le mécanisme exact du minimum n'est pas documenté.
- Tactique adverse : `teams.tactics` du match souvent vide → demander l'export du match juste après le coup de sifflet.

## Vues prêtes (lis-les avant de calculer toi-même)
`gold.sz_agenda`, `gold.sz_daily_alerts`, `gold.sz_effectif_bilan` (rang au poste, titulaire / doublure / surplus, salaire, temps de jeu : base du verdict effectif), `gold.sz_vd_comparatif` (moyennes W / D / L et écart W-L : base de toute analyse victoires/défaites), `gold.sz_lineup_natural`, `gold.sz_slot_options`, `gold.sz_role_report`, `gold.sz_training_progress`, `gold.sz_finance_cycles`, `gold.sz_finance_projection`, `gold.sz_infrastructure_payback` ; matchs : `silver.sz_matches`, `silver.sz_match_players`, `silver.sz_match_incidents` ; aussi `silver.sz_schedule`, `sz_standings`, `sz_players`, `sz_tactics`, `sz_transfer_listings`, `sz_u18`. Requêtes : colonnes choisies et `LIMIT`.

## Exports
- `page_type` en bronze = écran ouvert, pas contenu : classer par `source_url`. Sources non lues par silver et options observées : → source `commun.md` § Options observées (lecteur-exports seulement).

## Ordre des agents (tu lis les briefs du jour `outputs/sixzeroleague/briefs/AAAA-MM-JJ-<domaine>.md` de ceux avant toi)
Veille (si nouvelle source) → Match → Effectif → Finances-personnel (couvre les infrastructures) → Académie → Entraînement → Tactique → Transferts (dernier). Déclencheurs : → source `sixzeroleague.yaml` § dependances. Un agent aval qui contredit un amont l'écrit en tête de son résumé.

## Ce que l'utilisateur attend (condensé ; → source : `docs/attentes/attentes.md`)
- **Rendu** : maintenant + demain seulement, sans heures (R-1) ; des actions « fais X » avec joueur et valeur (R-2) ; tableau 🟥 URGENT / 🟧 IMPORTANT / 🟩 SUIVI · catégorie · action (R-3) ; saisie complète dans l'ordre de l'écran : formations, direction, agressivité, puis rôle → titulaire → remplaçant (R-4) ; aucun « si », aucun seuil générique, donnée manquante = « il me manque X, fais l'export Y » (R-5) ; court (R-6) ; ne jamais redemander ce que `outputs/sixzeroleague/fait-AAAA-MM-JJ.md` ou la base prouvent (R-7) ; une décision, le doute en une demi-ligne avec ce qui prouvera l'erreur (R-8) ; tout chiffre vérifié en base (R-9).
- **Décider** : série de défaites = changement fort (A-1) ; défaite = analyse chiffrée joueur par joueur contre toute la saison (A-2) ; Finances dit quoi faire de l'argent (A-3) ; chaque rendu propose un achat / une vente nommé·e avec prix, **jamais d'enchère ni de vente lancée sans accord** (A-4) ; pas d'amical : une nouveauté se teste par protocole chiffré en ligue (A-6) ; conseils `C-nnn` → `L-nnn` dans `outputs/sixzeroleague/learnings.md`, deux échecs = conseil réécrit (A-7) ; retard mesuré contre les autres clubs (A-8) ; chercher dans toutes les sources avant « absent » (A-9).
- **Coût** : brief d'une page, résumé de 10 lignes, delta du jour seulement.
