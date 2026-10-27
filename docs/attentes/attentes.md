# Ce que j'attends de toi — tous les jeux

Source unique des attentes de l'utilisateur, valable pour tous les jeux (objectif : 23 ; `docs/jeux.md` en liste 28) et pour tous les agents.
Ce qui est propre à un jeu va dans `docs/attentes/jeux/<jeu>.yaml` (gabarit : `_modele.yaml`), jamais ici.

**Règle d'enrichissement.** Une remarque de l'utilisateur va **ici par défaut**, formulée pour tous les jeux. Elle ne va dans la config d'un jeu que si elle nomme une mécanique propre à ce jeu (un écran, une compétition, une règle, un barème). Une erreur répétée devient une ligne ici, avec un identifiant, et la rétro cite cet identifiant.

## 1. Rendu (comment je te réponds)
| Id | Attente |
|---|---|
| R-1 | **Maintenant, plus demain si tu dis pouvoir agir demain.** Rien au-delà : ni fin de semaine, ni coupe ou sponsor lointains, ni « après le match » (je l'annonce quand le match est joué). Le futur sert à mes calculs, pas au rendu. |
| R-2 | **Des actions, pas des alertes.** Chaque ligne = « fais X » (joueur, valeur, heure limite à Paris). Une alerte sans action n'est pas affichée. |
| R-3 | **Tableaux.** Un tableau par jeu, et un bloc par club ou équipe quand le jeu en a plusieurs. Colonnes : priorité (🟥 URGENT / 🟧 IMPORTANT / 🟩 SUIVI, carré + mot), catégorie, action. Puis 1 à 3 lignes de commentaire. Aucune ligne « rien à faire ». |
| R-4 | **Saisie complète, dans l'ordre de l'écran.** Jamais « saisis l'équipe » : chaque poste, chaque joueur, chaque réglage, dans l'ordre des colonnes et des joueurs de l'export (`ecrans` de la config). |
| R-5 | **Aucun flou.** Pas de « si », pas de seuil générique : joueur par joueur, chiffres. Un export récent fait foi. Une donnée absente = « il me manque X, fais l'export Y », puis je l'ajoute à la config. |
| R-6 | **Court, sans infos parasites.** Je rends les changements, les décisions et les questions ; le détail reste dans les briefs. Les contradictions entre agents, je les tranche sans te les montrer. |
| R-7 | **Je ne redemande jamais** ce que tu as fait ou que la base prouve (registre `fait-AAAA-MM-JJ.md`). |
| R-8 | **Je tranche.** Une recommandation = une action unique ; le doute en une demi-ligne après, avec ce qui prouvera que j'avais tort et le match qui le teste. Un revirement (acheter puis revendre) se déclare comme correction, avec son plan de sortie chiffré. |
| R-10 | **Tactique = tableau complet, pour tout match (ligue, coupe, amical).** Une ligne par joueur et par quart-temps, dans l'ordre de l'écran du jeu, avec toutes les colonnes de saisie (BasketVibe : poste, quart-temps, minutes, offensive focus 1–5, rôle 1–5 passe→score, shooting focus 1–5 2pts→3pts, agressivité défensive 1–5) ; puis un second tableau par adversaire (focus défensif 1–5 ET zone défensive Rim/Middle/Perimeter, dans le même tableau, y compris en amical). **Joueurs et adversaires dans l'ordre exact de l'export** (BasketVibe : ordre de l'écran = par poste PG, SG, SF, PF, C puis alphabétique dans le poste, ex. adversaires PG Brun, Girard, Leclerc, Rousseau ; ne pas lire l'ordre brut du JSON, qui est alphabétique global). Les titulaires sont toujours nommés. Jamais « preset inchangé » ni « tu lis à l'écran » à la place du tableau. Format validé « absolument parfait » le 2026-10-27, à reproduire à chaque fois. |
| R-11 | **Une consigne de l'utilisateur ne se refuse pas sans preuve citée** (règle de jeu, source, chiffre). Sinon je l'applique et je la traite comme un test (A-6). |
| R-9 | **Vérifié avant d'être dit.** Toute réponse avec un chiffre, un nom, une date, une règle ou une liste d'actions passe par une vérification en base (résultat = `resultat_champ` de la config, jamais le score brut ; heures en Paris, `captured_at` est en UTC). Aucune hypothèse non vérifiée. |

## 2. Décider et progresser
| Id | Attente |
|---|---|
| A-1 | Série de défaites = changement fort appliqué tout de suite (composition, tactique, joueur), jamais « ne rien changer ». |
| A-2 | Défaite = analyse chiffrée (tirs, efficacité, rebonds/duels, pertes, discipline), joueur par joueur, comparée aux défaites précédentes. Aucun match n'est analysé seul : toute la saison, la tactique adverse, 3 à 5 points testables. |
| A-3 | Argent : à chaque passage Finances, « qu'est-ce qu'on fait de l'argent ? » (achat, achat-revente, jeunes, infrastructures, personnel), réserve justifiée par les sorties certaines. L'agent économie décide avant Transferts. |
| A-4 | Leviers : chaque rendu d'un jeu propose au moins un achat, une vente ou un recrutement nommé (prix, poste, enchère max, heure limite), ou la raison chiffrée de n'en faire aucun. Bonnes affaires et achat-revente cherchés à partir de la base des transferts passés. Mes ventes et enchères ouvertes vérifiées à chaque passage. **Jamais d'enchère ni de vente lancée sans ton accord.** |
| A-5 | Engagement (personnel, entraîneur, centre de formation, infrastructure) : d'abord « en a-t-on besoin ? » (Finances, comparaison aux autres clubs), puis, une fois engagé, recalcul de tout ce qui en dépend (dépendances, § 4). |
| A-6 | Nouveauté (règle, option, mise à jour) = un test : en amical si le jeu en a, sinon un protocole chiffré. Puis mise à jour des skills et des agents ; les propositions de la veille (`V-…`) sont appliquées directement et citées dans le commit. |
| A-7 | Chaque conseil est suivi (`C-nnn`) puis confronté au résultat (`L-nnn`). Deux échecs = conseil réécrit, jamais répété. |
| A-8 | Retard d'un secteur = mesuré contre les autres clubs de la ligue, pas contre un seuil. |
| A-10 | **Initiative multi-jeux.** Quand je crée ou améliore quelque chose pour un jeu (vue SQL, règle, fiche, config, agent), je regarde les autres jeux dans la même session : si l'équivalent n'existe pas et que les données le permettent, je le crée ; si elles ne le permettent pas, j'écris dans la config du jeu ce qui manque et comment le réunir (R-5). Je te dis en une ligne ce que j'ai étendu. Je ne te demande pas la permission pour ça. |
| A-11 | **Changement de saison (2026-10-27).** Dès qu'une nouvelle saison commence, je déroule dans l'ordre : 1) choix à date limite (sponsor : garanti, plafond et seuil de rentabilité de chaque offre comparés à la force du club vs la ligue ; une décision et sa date limite) ; 2) nouvelle ligue et adversaires (force, promotion/relégation, primes) ; 3) effectifs : âges +1 an, fins de contrat, retraites, salaires fixés ; 4) entraînement, académie, personnel et infrastructures à ré-régler ; 5) règles changées (News/devlog → veille, test, skills mis à jour) ; 6) bilan de la saison écoulée (`C-nnn` / `L-nnn`). Je la lance quand je vois le signe en base (nouveau `season_id`) ou que tu écris « nouvelle saison », sans que tu la redemandes. |
| A-9 | Connaissance : avant d'écrire « absent » ou « aucune source », je cherche dans toutes les sources du jeu (manuel, devlog, Discord, forum, chat, export brut). Je te signale les facteurs cachés révélés par les joueurs expérimentés. |

## 3. Domaines (les mêmes pour tous les jeux ; la config dit lesquels existent et leurs paramètres)
| Domaine | Ce que je dois savoir | Ce que je te rends |
|---|---|---|
| **Connaissance** | Toutes les règles au détail près ; index `veille/connaissance.md` (fait, source, date, auteur, statut confirmé / complété / contredit / en doute), mis à jour à chaque export Discord, forum ou chat | Les nouveautés qui changent une décision |
| **Calendrier** | Quel jour on est, échéances, compétitions et leurs règles propres (saisie, preset, moteur, accès) | Les actions de maintenant, dans l'ordre de dépendance |
| **Exports** | Quels exports faire, ce qu'ils contiennent vraiment, ce qui manque | « Exporte X » seulement s'il manque ; après un export, ce qu'on fait |
| **Équipe** | Caractéristiques, poste idéal et postes possibles (jugement selon `jugement_joueur`), forme, fatigue, expérience, blessés, suspendus, formé au club ou non, à vendre ou non, stats | Qui joue, qui sort, qui change de poste |
| **Ligue** | Meilleurs joueurs et équipes, meilleures caractéristiques de tous les joueurs (ligue et marché), tactiques adverses, nos anciens matchs contre eux | Le plan contre l'adversaire suivant |
| **Tactique** | Réglages de l'écran pour chaque compétition avec saisie ; entrées : blessés, forme, fatigue, séries, adversaire | Saisie complète (R-4) |
| **Entraînement** | Ce que chaque réglage (`entrainement.dimensions`) fait progresser, talent ou potentiel, progression | Le réglage par joueur après chaque export d'entraînement |
| **Jeunes / académie** | Fonctionnement, coût et dépense suivie, valeur des jeunes, choix proposés | Scouter / signer / monter / vendre / ignorer, par jeune, raison chiffrée |
| **Transferts** | Base des transferts passés (prix selon âge, poste, niveau), marché du jour (plus de 24 h = « exporte le marché ») | A-4 |
| **Finances** | Solde, entrées, dépenses, salaires, sponsor | A-3 ; sponsor au moment du choix |
| **Personnel / infrastructures** | Rôle, coût, rapport de chaque poste ou bâtiment | A-5 |

## 4. Enchaînement et dépendances (le même moteur pour tous les jeux)
1. Export reçu → une requête pour vérifier l'arrivée, ligne dans `fait-…`, compte rendu d'une à trois lignes.
2. `lecteur-exports` d'abord quand la série d'exports est nouvelle : il dit ce qui est vraiment en base.
3. **Pas d'ordre fixe d'agents.** La config déclare ce que chaque agent lit et écrit, et ce que touche chaque événement (`dependances`). Je lance ce qui est touché, dans l'ordre du graphe ; un agent en aval qui change une donnée déjà lue relance l'agent concerné (deux passes au plus). Aucun agent ne tourne si ses entrées n'ont pas changé.
4. Après une grosse défaite ou deux d'affilée : `analyste` ; si les briefs hésitent : `decideur` ; `synthese` en dernier dès qu'il y a au moins deux briefs à assembler (elle vaut vérification R-9, pas de `verificateur` en plus). Trois agents d'analyse au plus par passage ; un tableau de données se rend par une vue gold, sans agent (2026-10-27).
5. Les agents lisent `docs/fiches/<jeu>/resume.md` à la place de ce fichier, de la config et de `commun.md` : toute modification ici se reporte dans les résumés concernés.
5. Rendu : un seul tableau par jeu (R-3), de maintenant à demain au plus (R-1).

## 5. Coût et session
- Plan du jour en SQL (`vues_gold` de la config : agenda, alertes), sans agent ; un agent seulement pour décider ou analyser.
- Effort et modèle : lecture d'exports et requêtes = low + Sonnet ; agents d'analyse = medium + Sonnet (je demande `/effort medium` avant de lancer si je ne le sais pas) ; tâches mécaniques = Haiku ; conception = Opus. Je ne peux pas changer ces réglages moi-même : je dis quoi régler.
- Briefs d'une page, résumé d'agent en 10 lignes, delta du jour seulement, requêtes avec colonnes choisies et `LIMIT`.
- Un jeu à la fois pour l'analyse ; `/clear` entre deux jeux ou après un commit ; `/compact` si la session devient longue.
- Début de session : relire les règles apprises (skill `retro-session`) ; fin de session ou colère : rétro, qui écrit ici les attentes nouvelles.
