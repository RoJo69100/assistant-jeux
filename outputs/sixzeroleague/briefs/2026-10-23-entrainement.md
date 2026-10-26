# Six Zero League — brief Entraînement du 2026-10-23

**Corrigé le 2026-10-23 :** la décision sur la formation RW de Blanc **change** : de « continuer » à « annuler » (confiance faible à moyenne). Le motif « RW 11 sans pénalité, 2 à 3 points de plus que le RW2 » ne valait qu'une fois la formation finie : la note 11 est calculée avant la pénalité de hors-poste (`silver.sz_players.role_overalls`, brief Effectif corrigé § 3 et ligne « Corrigé le 2026-10-23 (2) », brief Tactique § 3). Fin de formation : 11/36 journées faites (`silver.sz_role_training`, 2026-10-23), 25 restantes ; la saison compte 18 journées (`commun.md`, `silver.sz_standings`) et on est à J9-J10, donc 8 journées finissent cette saison (19/36), le reste tombe vers la J17 de la saison 3. Blanc compte pour 0 au RW cette saison, et le RW est déjà tenu par 3 joueurs au poste (Dupont 11, G. Bertin 9, Lemaire 8). Les 150 par cycle restants (~12,5 cycles, ~1 875) ne sont pas dépensés (brief Finances). Les erreurs : « Blanc RW 11 » comparé comme si le poste était au poste ; avantage compté pour cette saison. Le reste du brief est inchangé.

**Export manquant : le rapport du cycle du 21/10 (semaine 3).** `gold.sz_training_progress` n'a que les cycles du 19, 20 et 22/10 ; des points intermédiaires manquent (ex. Bourgeois Positioning 5→6, Simon Passing 2→3). Non bloquant, non récupérable. Le cycle de ce soir (semaine 5, après J10 à 21:00) sera à exporter : Équipe → Training après 21:00.
**Contradiction avec les briefs amont :** aucune sur les faits. Deux nuances : (1) Effectif écrit « un focus par joueur » : Teodoro Barros n'a **aucune ligne dans le plan** au relevé du 2026-10-23 (14 joueurs sur 15, `silver.sz_training_plan`) ; (2) Effectif juge le RW de Blanc de faible intérêt : sa note au rôle RW est 11 (`silver.sz_players.role_overalls`), égale à Dupont, contre 9 et 8 pour G. Bertin et Lemaire. Pas de brief Veille.
Briefs amont lus : Match, Effectif (corrigé), Finances-personnel, Académie.

## Fiche de saisie (avant 21:00 Paris aujourd'hui)
| Réglage | Valeur | Action |
|---|---|---|
| Intensité d'équipe | Normal | Garder |
| Teodoro Barros (RB, 30 ans) | Attaque / Technique | **À régler** (aucun focus aujourd'hui) |
| Formation de rôle Blanc → RW | 11/36, 150 par cycle | **Annuler** (Équipe → Training → formation de rôle), voir § 4 |
| Sébastien Blanc (GK) | Attaque / Contrôle du ballon | **Changer** après l'annulation : Gardien (compétence à choisir parmi ses clés GK les plus faibles, non lues ici). Contrôle du ballon n'avait de sens que pour l'aile |
| Emmanuel Bourgeois (GK) | Gardien / Placement | Garder |
| Aurélien Simon (CB) | Attaque / Passe | Garder |
| Frédéric Denis (CB) | Attaque / Passe | Garder |
| Alain Bertin (LB) | Attaque / Passe | Garder |
| Guillaume Leroy (LB) | Attaque / Tir | Garder |
| Nicolas Roger (RB) | Attaque / Passe | Garder |
| Jordan Lefebvre (LW) | Attaque / Tir | Garder |
| Nils Sundberg (LW) | Attaque / Tir | Garder |
| Denis Dupont (RW) | Attaque / Tir | Garder |
| Gabriel Bertin (RW) | Physique / Vitesse | Garder |
| Gilbert Lemaire (RW) | Attaque / Tir | Garder |
| Alexandre Benoit (P) | Attaque / Tir | Garder |
| Benoît Chevalier (P) | Physique / Force | Garder |
Un seul changement : Barros. Source : `silver.sz_training_plan` (2026-10-23).

## 1. Intensité d'équipe : rester à Normal (confiance moyenne)
Faits : Normal ; 15 joueurs valides, aucun blessé ni suspendu (`silver.sz_players`). Cycles du 19, 20 et 22/10 : 12, 11 et 15 points au total, 9, 10 et 14 sur des compétences clés du rôle ; gain de note générale 2, 2 et 0 (`gold.sz_training_progress`).
Règles : High = progrès plus rapides, mais plus de blessures et plus longues (~3 matchs, parfois 6) ; « un club qui s'entraîne dur a besoin d'un effectif plus profond » [W:Training, W:Injuries]. Le skill ne chiffre pas le gain de High : je ne peux pas dire s'il compense le risque.
Avis : un seul remplaçant naturel par rôle (Effectif), arrières et pivots les plus exposés [W:Injuries], 2e place à jouer contre Pretok (J9) : un blessé de plus coûterait plus que quelques points d'avance. Les 5 cycles restants (23 au 27/10) ne justifient pas de monter. Je suis l'avis d'Effectif. Light n'a pas de raison d'être : pas de blessé à ménager.

## 2. Verdict par joueur (cycles du 19, 20 et 22/10 ; `gold.sz_training_progress`, `silver.sz_players`)
Gain attendu : le skill ne donne aucun chiffre de gain par âge ou éthique ; la référence est donc l'équipe (environ 1 point par cycle sur le focus quand le joueur progresse). Éthique de travail (`silver.sz_players.work_ethic`) : Roger 78 → 5 points, G. Bertin 61 → 4, Leroy 29 → 4 ; Dupont 1, Lefebvre 2, Denis 3 → 0, 2 et 3 points. L'éthique décide du rendement [W:Training], mais n'est pas modifiable : ne pas changer un focus à cause d'elle.
| Joueur | Focus | Points (clés) | Progression en cours | Verdict |
|---|---|---|---|---|
| Roger (RB) | Passe 11 | 5 (5) | — | Garder, meilleur rendement |
| G. Bertin (RW) | Vitesse 12 | 4 (4) | — | Garder |
| Leroy (LB2) | Tir 9 | 4 (4) | — | Garder |
| A. Bertin (LB) | Passe 12 | 3 (3) | Tir 0,16 | Garder (Tir 7 est sa clé la plus faible, 0/4 en J8 sur un seul match : pas de motif de changer) |
| Benoit (P) | Tir 7 | 3 (3) | — | Garder (Force 5 reste faible, voir Chevalier) |
| Bourgeois (GK) | Placement 7 | 3 (3) | Un contre un 0,69 ; Prise de balle 0,60 | Garder |
| Denis (CB2) | Passe 5 | 3 (3) | — | Garder |
| Lemaire (RW3) | Tir 12 | 3 (2) | — | Garder (2 points hors clé avant le 20/10, focus déjà corrigé) |
| Blanc (GK) | Contrôle du ballon 10 | 3 (0 comme GK) | Prise de balle 0,57 | Corrigé : changer pour un focus Gardien si la formation est annulée (§ 4) |
| Simon (CB) | Passe 4 | 2 (2) | Anticipation 0,87 | Garder |
| Chevalier (P2) | Force 10 | 2 (2) | — | Garder |
| Lefebvre (LW) | Tir 17 | 2 (1) | — | Garder (focus passé de Jeu sans ballon, hors clé, à Tir le 22/10) |
| Sundberg (LW2) | Tir 9 | 1 (1) | — | Garder, trop peu de cycles pour juger |
| Dupont (RW) | Tir 19 | 0 | **Tir 0,913** | Garder : le point tombe au prochain cycle ; éthique 1 |
| Barros (RB2) | aucun | 0 | Technique 0,70 ; Passe 0,61 | **Régler un focus** (voir ci-dessous) |
Retard : Dupont (0 point en 3 cycles, éthique 1) et Sundberg (1 point). Aucun cas de focus mal choisi par rapport au rôle.

### Barros : régler Attaque / Technique (confiance faible)
Faits : 30 ans, éthique 24, aucun focus ; l'effort est donc réparti sur les 20 compétences (progressions de 0,08 par compétence). Compétences clés de RB : Tir 6, Détente 13, Technique 14, Passe 10. Il est RB2 (note 10, comme Roger), sans minutes.
Règles : « le focus bat la dispersion » ; gain hebdomadaire réduit dès 28 ans [W:Training].
Avis : Technique est la clé de RB la plus proche du prochain point (0,70) et Passe suit (0,61) : un focus lui donne un gain rapide. Impact attendu faible (joueur de banc, déclin à venir). Alternative : Attaque entière.

## 3. Déclin physique à 30 ans (fin de saison vers le 27/10)
Règle [W:Training] : perte de compétences physiques à chaque changement de saison dès 30 ans (une part de chacune des 5, plus grande avec l'âge) ; « continuer à entraîner un joueur âgé lui fait garder l'essentiel ». Le skill ne donne **aucun montant** : je ne chiffre pas la perte. Il ne dit pas non plus si le déclin frappe à l'arrivée à 30 ans ou à partir de 30 ans déjà révolus : le cas de Sundberg (29 → 30) est donc incertain.
| Joueur | Physique actuel (Vitesse / Force / Détente / Endurance) | Effet pour la note |
|---|---|---|
| Bourgeois (GK, 30) | 11 / 1 / 11 / 11 | Faible : ses clés de gardien (Réflexes 13, Un contre un 11, Placement 7, Prise de balle 16, Relance 18) ne sont pas physiques. |
| Barros (RB, 30) | 19 / 4 / 13 / 15 | Détente (clé RB) touchée ; il est remplaçant. |
Avis (confiance faible) : ne rien changer pour Bourgeois, son focus Gardien garde ce qui compte au but ; aucun moyen de compenser les 5 compétences physiques d'un coup par un focus unique. Surveiller après le changement de saison : relire `silver.sz_players` (Bourgeois, Barros, Sundberg) et chiffrer la perte réelle, qui servira de repère. Le risque se rapporte plus aux deux saisons à venir qu'à la fin de saison ; la relève GK est à chercher à l'U18 (brief Académie, offre après J15 le 26/10).

## 4. Formation de rôle de Blanc (GK → RW) : annuler (corrigé le 2026-10-23, confiance faible à moyenne)
**Correctif :** l'avis ci-dessous (« continuer ») est remplacé par « annuler ». Faits ajoutés : gain RW nul cette saison (formation à 19/36 en fin de saison, fin vers la J17 de la saison 3, Blanc 28 ans, gains réduits dès 28 [W:Training]) ; RW déjà couvert à 3 au poste (Effectif § RW) ; un Blanc RW 11 n'apporterait que +2 sur G. Bertin et +3 sur Lemaire, en 3e rôle de réserve derrière Dupont ; solde 5 235, prévision +3 306 par cycle (brief Finances). Les 11 journées déjà faites sont perdues (rien remboursé, reprise non décrite) : c'est un coût déjà payé, il ne pèse pas dans le choix. Le vrai poste faible à 2 saisons est GK (Effectif § 4), où Blanc est déjà GK2. Contre l'annulation : décision difficile à défaire ; si l'argent n'est pas un frein, continuer reste défendable. Source de la règle : skill sixzeroleague-entrainement (« Formation à un 2e rôle »).

Texte d'origine (conservé, avis périmé) :
## 4 bis. Formation de rôle de Blanc (GK → RW) : continuer (confiance faible)
Faits (`silver.sz_role_training`, `silver.sz_players`, `silver.sz_finances` via briefs) : 11 / 36 journées, 150 par cycle, Training Facilities 6 (emplacement 1 pris, 2e au niveau 10). Reste 25 journées, environ 12,5 cycles, ~1 875 non encore payés. Blanc : 0 minute en 9 matchs (GK2). Notes au rôle avant pénalité : Blanc RW 11 (LW 11), Dupont RW 11, G. Bertin RW 9, Lemaire RW 8. Compétences clés d'ailier de Blanc : Vitesse 20, Agilité 16, Tir 17, Contrôle du ballon 10.
Règles : formation sans pénalité de hors-poste ensuite, le joueur garde ses rôles, annuler ne rembourse rien [W:Training, Dev chat]. Pénalité hors poste « légère », non chiffrée [W:Attributes].
| Option | Coût | Ce qu'on obtient |
|---|---|---|
| Continuer | 150 par cycle, ~1 875 jusqu'à la fin (au-delà de cette saison) | Blanc RW 11 sans pénalité : 2 à 3 points de plus que le RW2 (9) et le RW3 (8) ; un joueur de banc inutilisé devient utile |
| Annuler | 0 ensuite, rien remboursé, 11 journées perdues (reprise éventuelle non décrite) | Dépenses du cycle 2 140 au lieu de 2 290 (brief Finances) |
Avis : continuer. Raisons : (1) la dépense n'est pas bloquante : 150 par cycle sur une prévision de +3 306, et ~19 500 de capacité en fin de saison (brief Finances) ; (2) Blanc est aujourd'hui le seul joueur de banc sans minutes que la formation transforme en vrai deuxième choix à un poste ; (3) le choix est réversible : attendre un cycle coûte 150 au plus, annuler plus tard reste possible. Contre : l'effet n'arrive qu'après 12,5 cycles, soit en saison 3 avec Blanc à 28 ans (gains réduits dès 28), et rien ne dit qu'il jouera RW. Si l'argent devient le frein (rien avant la fin de saison, brief Finances), annuler est le premier levier. Le skill ne dit pas si la formation avance et se paie hors saison : à vérifier au prochain relevé. Option à étudier plus tard, hors décision du jour : le 2e emplacement (niveau 10) pour un CB, Lemaire ayant une note CB de 10 contre 8 pour Denis (`role_overalls`) ; non conseillé tant que le solde est bas.

## Conseils suivis
- C-007 ajouté puis corrigé le 2026-10-23 dans `outputs/sixzeroleague/learnings.md` (intensité Normal, formation de Blanc annulée, focus de Blanc et de Barros).
- C-005 (Finances, formation de Blanc) : tranché côté sportif par ce brief, statut inchangé (ouvert).
- Conseils d'entraînement antérieurs ouverts : aucun.

## Limites
- Cycle du 21/10 non exporté ; projection de fin de saison non chiffrée (montant du déclin et gain de High inconnus du skill).
- Pas de notion de potentiel caché dans le skill : aucune estimation de potentiel.
- Progressions fractionnaires lues sur `silver.sz_players.training_progress` du 2026-10-23, avant le cycle de ce soir.
