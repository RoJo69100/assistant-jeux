# BasketVibe — détails du résumé (lus à la demande)

Suite de `resume.md` : attentes condensées, ordre des agents, pièges connus. Lire quand la tâche touche l'un de ces sujets.

## Ordre des agents (tu lis les briefs du jour `outputs/basketvibe/briefs/AAAA-MM-JJ-<domaine>.md` de ceux avant toi)
Veille → Match → Effectif (moi, vues gold, sans agent depuis le 2026-11-02) → Finances (moi, vues gold, sans agent depuis le 2026-11-02) → Académie / Entraînement (parallèles) → Tactique (lit Match, Effectif, Entraînement) → Transferts (lit Effectif, Finances, Tactique, Académie). Un agent aval qui contredit un amont l'écrit en tête de son résumé.

## Ce que l'utilisateur attend (condensé ; → source : `docs/attentes/attentes.md`)
- **Rendu** : aujourd'hui seulement, le match de demain se prépare aujourd'hui (R-1, CLAUDE.md § Horizon du 2026-10-27) ; des actions « fais X » avec joueur, valeur, heure limite (R-2) ; tableau 🟥 URGENT / 🟧 IMPORTANT / 🟩 SUIVI · catégorie · action (R-3) ; saisie complète dans l'ordre de l'écran (R-4) ; aucun « si », aucun seuil générique, donnée manquante = « il me manque X, fais l'export Y » (R-5) ; court (R-6) ; ne jamais redemander ce que `outputs/basketvibe/fait-AAAA-MM-JJ.md` ou la base prouvent (R-7) ; une décision, le doute en une demi-ligne avec ce qui prouvera l'erreur (R-8) ; tout chiffre vérifié en base (R-9).
- **Tactique (R-10)** : tableau joueur × quart-temps (Joueur, Poste, Q1–Q4, Prol., Min, Off. focus, Rôle, Tir, Agress.) + tableau adversaires (focus 1–5 ET zone), pour ligue, coupe et amical ; jamais « preset inchangé ».
- **Amical, tableau adversaires** : une ligne « les 12 : focus 3, zone X » (pas de noms). Tableau joueurs = format R-10 avec une composition de test ; la vue `gold.bv_saisie_joueurs` donne les réglages du dernier amical enregistré (lacune connue : pas d'export de tactique pour les amicaux du 28 et du 29/10).
- **Décider** : série de défaites = changement fort (A-1) ; défaite = analyse chiffrée joueur par joueur contre toute la saison (A-2) ; Finances dit quoi faire de l'argent (A-3) ; chaque rendu propose un achat / une vente nommé·e avec prix max, **jamais d'enchère ni de vente lancée sans accord** (A-4) ; nouveauté = test en amical (A-6) ; conseils suivis `C-nnn` → `L-nnn` dans `outputs/basketvibe/learnings.md`, deux échecs = conseil réécrit (A-7) ; retard mesuré contre les autres clubs (A-8) ; chercher dans toutes les sources avant « absent » (A-9).
- **Coût** : brief d'une page, résumé de 10 lignes, delta du jour seulement.

## Pièges connus
- Personnel médical : 85 000 au journal le 25/10 contre 60 000 affichés (à confirmer le 01/11).
- Page « academy » parfois en réalité la page finances (26/10).
- Options d'écran observées et non documentées : → source `commun.md` § Options observées (mises à jour par moi depuis `gold.exports_nouvelles_cles`).
  Ajouts du 29/10 : moteur **v5 en amicaux seulement** (annonce du 28/10 : pas de 20 s mortes, tirs de fin de quart ; effet inconnu, mesure = points de Q4 des amicaux) ; compétences adverses de coupe en **fourchettes de 20 points** (`skill_brackets`) ; tactique de coupe enregistrable par match (`/cup-fixtures/<id>/match-tactics`, lue par silver depuis la migration 022) ; zone réellement jouée : `gold.bv_zone_jouee`.
