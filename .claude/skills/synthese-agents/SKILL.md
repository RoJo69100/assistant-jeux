---
name: synthese-agents
description: Format obligatoire du rendu après une chaîne d'agents ou un plan « que faire » : un tableau par jeu, priorités 🟥/🟧/🟩, saisies poste par poste, analyses chiffrées, tests avec preuve contraire. À charger avant de rendre compte.
---

# Synthèse des agents — format du rendu

Règle de l'utilisateur (2026-10-24) : « je veux les infos importantes : changement de composition, d'entraînement ou d'autre chose, les analyses, les questions ; des catégories et des couleurs ; un tableau par jeu, ne mélange pas ; sois TRÈS précis ». Règles universelles dans `CLAUDE.md`.

## 1. Ordre des blocs
Un bloc par jeu, dans l'ordre des échéances les plus proches. Team Soccer : un sous-bloc par club (Chomelix Cows, Ben Ahmed Donkey). Hockey Nation : par équipe concernée (PRO, FRM, U21, U17).

## 2. Contenu d'un bloc
1. **Corrections** (s'il y en a) : une ligne par chiffre que j'avais donné faux, avec la bonne valeur. En tête, jamais cachées.
2. **Tableau d'actions** : `Priorité | Catégorie | Action précise | Échéance`.
   - Priorité : 🟥 URGENT (échéance proche ou perte réelle) · 🟧 IMPORTANT · 🟩 SUIVI ; carré **et** mot ; rouge d'abord.
   - Catégorie (fixe) : Composition · Tactique · Entraînement · Transferts · Académie/Draft · Finances · Export · Question · Test.
   - Aucune ligne « rien à faire », aucune action déjà faite (registre `fait-…`).
3. **Fiche de saisie** pour toute ligne Composition / Tactique / Entraînement : tableau poste par poste (ou joueur par joueur) avec chaque réglage de l'écran (formation, consignes, focus 1–5, agressivité, minutes par période, remplaçants, remplacements programmés ; ou principale/secondaire, intensité). Seulement les changements si le reste est déjà saisi, en le disant (« les 14 autres : inchangés »).
4. **Analyse** (après un match, surtout une défaite) : tableau `Constat | Chiffre` de 4 à 8 lignes : par période, joueurs clés, adversaire, ce qui sépare nos victoires de nos défaites. Lien vers le brief détaillé.
5. **Tests** : pour chaque conseil de confiance faible : `Test | Ce qui prouvera que c'est faux | Date du match qui le teste`.
6. **Il me manque** : une ligne par donnée absente, avec l'écran exact à ouvrir.

## 3. Interdits
- « Saisis l'équipe », « voir le brief » à la place des valeurs.
- Un résultat lu dans le score brut (toujours `my_result`).
- Une décision forte bâtie sur une hypothèse (compétences clés supposées, tirage supposé) sans la marquer Test.
- Un conseil qui contredit un conseil précédent (ex. acheter puis revendre) sans le dire en Correction avec la raison et le plan de sortie (vente impossible → libération, coût chiffré).
- Plus de 3 lignes de commentaire après un tableau.

## 4. Leviers d'amélioration
Chaque bloc de jeu contient au moins une ligne Transferts ou Académie/Draft nommée (joueur, poste, prix, enchère maximale, heure de fin) ou la raison chiffrée de n'en proposer aucune. Les ventes ouvertes de l'utilisateur sont vérifiées (vendu ? prix ? retiré ?) à chaque passage.
