# BasketVibe — fiche Académie

Lue par l'agent `academie` après `commun.md`. Contenu repris de l'agent BasketVibe validé (checklist BasketVibe, partie E).

## Skills à lire
- `.claude/skills/basketvibe-academie/SKILL.md` (règles complètes)
- `.claude/skills/basketvibe-entrainement/SKILL.md` (le potentiel multiplie la progression)
- `.claude/skills/basketvibe-economie/SKILL.md` (homegrown, salaires)
- `.claude/skills/basketvibe-communaute/SKILL.md` (prix des jeunes, conseils sur les tests)

## Règles propres au jeu
1. Les projections de jauge reposent sur l'**hypothèse** écrite en tête de `sql/gold/010_bv_academy.sql` : rappelle-la.
2. La signature est irréversible et coûte la moitié de la jauge [M§4.2] : sois explicite sur cet arbitrage.
3. Fin de saison 1 : pas de recrutement avant le jeudi 29/10 sauf prospect exceptionnel (le junior vieillit d'un an au changement de saison du 27/10 ; l'académie ne se remet pas à zéro [Dev 2026-10-18]) ; ne cite pas l'avis « 90 suffit » [Com 2026-10-22/23, italia], contraire à [M§4.2] : 27,3 % contre 43,9 % de High (`gold.bv_academy_potential_odds`, vérifié le 2026-10-23). Investissement à sauvegarder avant jeudi 29/10 09:00.

## Données
- `silver.bv_academy_weekly` : jauge, investissement, date du rapport et du prochain.
- `gold.bv_academy_prospects` : prospects du dernier rapport. Poste, taille, fourchettes par compétence (fenêtre d'environ 20 points), TSP minimum et maximum, PS estimé au poste (milieu des fourchettes × poids [M§2.2]).
- `gold.bv_academy_potential_odds` : probabilité d'un potentiel Low (1–3), Decent (4–7) ou High (8–10) et potentiel moyen attendu, à la jauge actuelle et à 60, 80, 90 et 100 % [M§4.2].
- `gold.bv_academy_gauge_projection` : jauge sur 8 semaines selon l'investissement (100 000, 50 000, 0), sans signature ou après une signature (jauge divisée par 2).
- `gold.bv_potential_estimate` / `gold.bv_roster_now` : nos juniors déjà signés (Bernard 10, Baron 8, Leclerc 8 d'après la mesure du 18/10 ; Lecomte 5). Ils servent de **référence de ce qu'un bon prospect devient**.
- `gold.bv_finance_health` / `gold.bv_finance_s2_projection` : capacité à financer 100 000 par semaine et un test à 25 000.
- `gold.bv_market_price_ref` (tranche 16–17 ans) et le skill communauté : ce que coûte un jeune équivalent sur le marché (valeur d'une signature).
- `gold.bv_slot_fit` / dernier brief tactique : l'effectif et la place qu'aurait un junior (roster, minutes pour l'expérience et le homegrown [M§10.1.3]).

## Livrable
### 1. Les 3 prospects : tester, signer ou ignorer
Pour chacun : poste et taille (taille de recrutement à 16 ans [M§5.2] et croissance jusqu'à 22 ans), fourchette de TSP et PS estimé comparés à nos juniors au même âge, probabilités de potentiel à la jauge du rapport.
- **Tester** (25 000) : seulement si le résultat peut changer la décision. Un test donne une fourchette de 10 points par compétence et une catégorie de potentiel [M§4.2].
- **Signer** : si l'espérance (potentiel × profil × besoin de l'effectif) vaut la perte de la moitié de la jauge, donc des rapports suivants moins bons.
- **Ignorer** : laisser monter la jauge vers 90–100 %, où la probabilité d'un High passe d'environ 7 % à 27–44 %.
- Rappel : **un seul prospect par rapport** ; un nouveau rapport arrive chaque jeudi.

### 2. Investissement hebdomadaire
Garder, baisser ou monter (0 à 100 000), avec la projection de jauge, le coût sur 8 semaines, la date à laquelle la jauge atteint 90 %, et le moment où signer. À sauvegarder **avant le jeudi 09:00** [M§4.2].

### 3. Conseils suivis
Ajoute chaque décision conseillée dans la section Conseils de `outputs/basketvibe/learnings.md` (ID `C-nnn`, critère vérifiable : `silver.bv_academy_weekly`, nouveau junior dans `gold.bv_roster_now`).

## Sortie propre au jeu
- En tête du brief : la **décision** pour chaque prospect et l'**investissement**, avec la date limite.
- Après chaque export d'académie : lis le chat (`gold.bv_academy_chat`, depuis le dernier rapport) en entier, voir la carte `docs/decisions/cartes/basketvibe/academie.md` § Après chaque export d'académie.
- Si le rapport en base est périmé (un nouveau rapport est sorti depuis jeudi 09:00), dis-le et demande l'export de la page Académie.

- Juniors signés de l'académie (homegrown), donnés par l'utilisateur le 2026-10-24 : Baron, Leclerc, Bernard. Les minutes de ligue de ces trois rapportent 200 par minute (plafond 40 000 par semaine) [M§10.1.3] ; à vérifier sur l'écran Académie à chaque signature.
