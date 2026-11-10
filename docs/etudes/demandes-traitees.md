# Demandes d'export traitées

Lu par `pipelines/que_faire_blocs.py` (`lire_etudes`) : toute ligne « Pour comprendre le Match Engine, j'ai besoin de : … » d'une étude dont le début (après les deux-points) figure dans la première colonne est ignorée, aux blocs 0 et 6 du « que faire ». Statuts qui ignorent la demande : `fait`, `écartée` (tout autre statut la laisse active). Les études ne sont pas modifiées.

Colonne « question liée » : l'identifiant de la question de la carte de faisabilité (ex. `3b`) ; `—` si aucune. Pour un statut `fait`, `etat_etude` écrit « export reçu le JJ/MM, étude à lancer » à la place du verdict de la carte (la date est celle de la colonne `date`).

| début de la demande | statut | date | question liée | raison |
|---|---|---|---|---|
| exporte la page Effectif les jours de ligue entre l'amical de 8 h | écartée | 2026-11-10 | 1a | fatigue d'amical déjà mesurée |
| exporte la page effectif (compétences des joueurs) chaque jour de match, avant le match | écartée | 2026-11-10 | — | demande sur des groupes v3 clos |
| exporte la page des réglages utilisés de l'amical du 29/10 | fait | 2026-11-10 | — | exporté par l'utilisateur |
| exporte la page Équipe (effectif) des clubs de tête du classement | fait | 2026-11-10 | 3b | exporté par l'utilisateur, ingérée dans silver.bv_club_roster (384 lignes, dernière capture le 10/11) |
| exporte la page Entraînement chaque semaine | écartée | 2026-11-10 | 5a | remplacée par les demandes datées du samedi et du lundi du bloc 0 (traitement le dimanche) |
