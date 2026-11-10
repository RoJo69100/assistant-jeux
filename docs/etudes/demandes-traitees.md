# Demandes d'export traitées

Lu par `pipelines/que_faire_blocs.py` (`lire_etudes`) : toute ligne « Pour comprendre le Match Engine, j'ai besoin de : … » d'une étude dont le début (après les deux-points) figure dans la première colonne est ignorée, aux blocs 0 et 6 du « que faire ». Statuts qui ignorent la demande : `fait`, `écartée` (tout autre statut la laisse active). Les études ne sont pas modifiées.

| début de la demande | statut | date | raison |
|---|---|---|---|
| exporte la page Effectif les jours de ligue entre l'amical de 8 h | écartée | 2026-11-10 | fatigue d'amical déjà mesurée |
| exporte la page effectif (compétences des joueurs) chaque jour de match, avant le match | écartée | 2026-11-10 | demande sur des groupes v3 clos |
| exporte la page des réglages utilisés de l'amical du 29/10 | fait | 2026-11-10 | exporté par l'utilisateur |
