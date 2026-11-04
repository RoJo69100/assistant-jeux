# Conception à faire (prochaines sessions `/model opus`)

Demandé par l'utilisateur le 2026-11-04 après la session SixZero League : plus d'agent pour ce que des données de base et une vue gold tranchent. Un agent seulement pour un cas que les vues ne tranchent pas, ou au plus une fois par semaine.

## 1. Contrôle d'entraînement (vue gold, tous les jeux, SixZero League d'abord)
- Pour chaque joueur : focus attendu (compétence clé du poste, niveau, âge) contre focus réellement saisi.
- Source du plan saisi : HTML `app_team` le plus récent dans `bronze.raw_pages` (`silver.sz_training_plan` est périmé depuis le 2026-10-26, `sz_role_training` depuis le 2026-10-23).
- Sortie : « rien à faire » si tout correspond, sinon seulement les écarts, avec la saisie exacte ; plus intensité et blessés.
- Remplace l'agent `entrainement` après chaque cycle ; l'agent ne reste que pour le bilan hebdomadaire.
- Cas déclencheur : Ramiro Rincón (LB) en « All skills » sans focus, repéré à la main le 2026-11-04.

## 2. Table de référence des prix de transferts (vue gold, tous les jeux)
- Une ligne par poste × tranche d'âge × tranche de note : prix médian, prix de départ, part des annonces réglées, nombre d'observations.
- Construite sur l'historique des transferts déjà en base, puis mise à jour par delta à chaque export du marché ou de « Mes transferts ».
- Sortie : pour chaque annonce du jour, « sous le prix / dans la norme / au-dessus » et l'enchère maximale, sans agent.
- À vérifier d'abord : ce qui existe déjà (`silver.sz_transfer_listings`, historique) avant de créer une table.
- Remplace l'agent `transferts` pour le marché du jour.

## 3. Règle commune
- Un état attendu et un état saisi, comparés en SQL ; l'écart est la seule action proposée. Zéro écart = zéro ligne dans le plan.
- Voir [[feedback-effectif-questions-vue-gold-systematique]] : vue gold dès qu'un gain de temps existe.
