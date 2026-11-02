# Décisions importantes : dossier complet et variables obligatoires (tous jeux)

Créé le 2026-10-31 (l'utilisateur : « avant que j'aie une information importante, tu compiles TOUTES les informations nécessaires… pas "j'ai pas tout lu, il me manquait des données" »).

Une **décision importante** = achat, vente, enchère ; composition de ligue, coupe ou playoffs ; analyse d'une défaite ; entraînement de la semaine ; signature ou renvoi (académie, draft, coach, personnel) ; dépense d'infrastructure ou de finances. Les tableaux de routine tirés d'une vue gold (amical, agenda, état des exports) n'en sont pas.

## Les trois sources, toujours ensemble
| Source | Où | Ce qu'on en tire |
|---|---|---|
| **Règles** | skills `.claude/skills/<jeu>-*`, manuel, devlog, News | le mécanisme (pourquoi ça marche) |
| **Avis des amis** | `outputs/<jeu>/veille/connaissance*.md`, `data/discord/<Jeu>/`, `data/chat/<jeu>/`, chat en base | l'expérience des autres managers et du développeur, statut confirmé / contredit / en doute |
| **Chiffres** | vues gold du jeu (`docs/fiches/<jeu>/resume.md` § Vues prêtes), bronze du jour, `learnings.md` | la mesure, sur **toute la saison**, et nos conseils passés (C-nnn → L-nnn) |

## Carte : on cherche une fois, on garde (2026-10-31)
L'utilisateur : « si la première fois il a trouvé l'information à un endroit, il faut qu'il sache que l'information est là et qu'il la garde ; il ne faut pas relire à chaque fois tout ; s'il y a du nouveau dans la règle, il modifie ce check ». C'est **le cœur du projet** : décider mieux avec le temps, pour moins cher.

- `docs/decisions/cartes/<jeu>/<type>.md` (modèle `cartes/MODELE.md`) : pour chaque variable, **où la lire** (requête SQL exacte ou fichier § section), **le check** (règle, seuil chiffré, sens), **sa source**, la dernière valeur. Plus les checks appris des matchs (`L-nnn`) et l'historique des changements de checks.
- **Pas de carte** : `dossier.py` compile tout (étapes ci-dessous) et l'agent écrit la carte à la fin.
- **Carte présente** : `dossier.py` rend la carte + **seulement le nouveau** depuis le commit noté (« Sources lues ») : lignes ajoutées aux skills, fiches, config, connaissance, learnings, Discord/chat, y compris non commitées. L'agent lance les requêtes de la carte, lit le nouveau en entier, modifie un check si le nouveau change une règle, ajoute une variable apprise, puis commit et `--marquer`. Un joueur absent de la carte : `--mots "<nom>"` fait une recherche ciblée dans tout l'historique.
- **Apprendre des matchs** : chaque `L-nnn` qui touche un type devient un check de sa carte ; un check contredit deux fois par les résultats est réécrit (historique daté). Ainsi la carte s'améliore à chaque match au lieu de tout relire.
- `--complet` recompile tout : seulement si la carte est fausse ou sur demande.

## Mise en route d'un jeu = le gros travail, une seule fois (2026-10-31)
L'utilisateur : « on commence BEAUCOUP à l'ajout d'un jeu, c'est là que tout se fait ; après, consommation ». À l'ajout (ou à la remise à niveau) d'un jeu, en Opus :
1. **Veille intégrale** : tout le Discord, le forum, le chat, le manuel, le devlog → `outputs/<jeu>/veille/connaissance.md` et les skills.
2. **Registre de couverture** `docs/couverture/<jeu>.md` : **chaque ligne** de la liste de l'utilisateur pour ce jeu (`docs/chose-a-faire*.txt`, `docs/chose-a-DM.txt`, bloc « Tous jeux ») → `| fichier:n° | ligne | réponse (carte § variable, vue gold, skill §) | statut ✅ répondu / 🔧 mécanisme fait / ❌ manque + comment le réunir |`. Les choses nouvelles trouvées en veille (facteur caché, règle découverte) y sont **ajoutées** comme lignes `+N`.
3. **Mécanismes** : une vue gold par tableau qui reviendra, une carte par type de décision (variables, check, rendu figé, lignes couvertes).
4. Le jeu est « prêt » quand aucune ligne du registre n'est ❌ sans plan. Ensuite, au quotidien, seulement carte + nouveau.

## Étapes sans carte (première fois), dans l'ordre, sans en sauter
1. **Dossier** : `python pipelines/dossier.py <jeu> <type> [--mots "nom joueur,mot clé"]` → `outputs/<jeu>/dossier/AAAA-MM-JJ-<type>.md` (+ `…-discord.txt` avec **toutes** les lignes trouvées). Il liste les skills à lire, chaque ligne de `connaissance` sur le sujet, chaque message Discord/chat trouvé, les briefs du jour, les learnings, le registre `fait-`.
2. **Lecture intégrale** : l'agent (ou moi) lit le dossier **en entier** et le fichier Discord **en entier**, puis interroge les vues gold citées.
3. **Grille** : chaque variable du type ci-dessous reçoit une valeur et sa source. Une variable vide se cherche (SQL, bronze brut, Discord, chat) avant d'être déclarée absente.
4. **Tableau « Couverture »** en fin de brief : `Source | éléments trouvés | lus | retenus | écartés (pourquoi)`. Lus = trouvés, sinon le brief n'est pas fini.
5. **Police** : l'agent `police` contrôle la grille et la couverture, complète lui-même ce qui manque, puis la décision est rendue.
6. **Carte** : l'agent écrit `docs/decisions/cartes/<jeu>/<type>.md` (où il a trouvé chaque variable, le check), commit, `python pipelines/dossier.py <jeu> <type> --marquer`.

Seule phrase admise pour un manque réel : « il me manque X — cherché dans : <liste des sources> — on le réunit comme ça : <export précis> ». Interdits : « pas tout lu », « lu à moitié », « non lu », « non relevé », « échantillon », « pas eu le temps », « à lire plus tard » (bloqués par le hook `pipelines/police.py`).

## Variables obligatoires par type
Valeurs nommées (joueur, prix, date), jamais un seuil générique.

### `achat` (achat, enchère, agent libre)
Joueur, âge, poste et fit au poste (vue fit du jeu) · compétences clés du poste vs notre titulaire et notre remplaçant · potentiel / plafond · forme, fatigue, blessures · salaire et durée de contrat · prix demandé, prix des ventes comparables (base des transferts) · `capacite_invest` moins dépenses déjà décidées · taxe et règles d'enchère (skill transferts) · revente possible (délai, valeur) · avis des amis sur ce profil ou ce poste · effet sur l'effectif minimum · ce qui prouvera l'erreur et le match qui le teste.

### `vente` (vente, libération)
Joueur, âge, minutes jouées sur la saison, rôle dans les victoires/défaites · remplaçant interne et écart de niveau · valeur marché et ventes comparables · salaire économisé · taxe, délai, effectif minimum · déclin (âge) ou progression attendue · avis des amis · ce qui prouvera l'erreur.

### `composition` (ligue, coupe, playoffs)
Adversaire : effectif, forces, tactique lue, résultats de la saison · nos joueurs : forme, fatigue, minutes lourdes, blessures, suspensions · fit poste par poste · réglages complets dans l'ordre de l'écran (voir fiche du jeu) · règles du moteur concernées (skill tactique) · ce qui a marché / échoué cette saison (gold V/D, learnings) · avis des amis sur ce réglage · ce qui prouvera l'erreur.

### `defaite` (analyse d'une défaite)
Score via `my_result`/`is_mine` · tirs, efficacité par zone, rebonds, pertes, fautes, joueur par joueur · comparaison à toutes les défaites et victoires de la saison · tactique adverse lue · nos réglages du match · fatigue et minutes · conseils C-nnn appliqués et leur effet · règles du moteur qui expliquent l'écart · avis des amis sur la même situation · 3 à 5 corrections testables nommées et chiffrées.

### `entrainement`
Chaque joueur : âge, potentiel, compétences sous/au-dessus des seuils du poste, gains des semaines passées · règles de progression (skill entraînement) · objectifs de l'effectif (qui doit progresser pour quel poste) · risque (blessure, intensité, fatigue) · avis des amis sur les choix d'entraînement · ce qui prouvera l'erreur (gain mesuré, semaine).

### `academie` (académie, draft, scouting, jeunes, recrutement)
Chaque prospect : compétences, fourchettes, potentiel estimé, âge · règles du jeu (coût, effet d'un recrutement, probabilités) · besoin de l'effectif par poste · budget · comparaison aux académies des autres clubs · avis des amis · ce qui prouvera l'erreur.
Recrutement (Hardwood, 2026-11-02) : en plus, pour chaque cible et remplaçant : compétences clés du poste et phrases du scout · taille (grand ≥ 2,02 m) · note actuelle → plafond · nombre d'équipes intéressées (jamais High) · points disponibles et coût · offres déjà faites (registre `fait-`) · poste du boursier qui part.

### `finances` (infrastructure, personnel, sponsor, dépense)
Solde, revenus et dépenses par semaine, salaires · capacité d'investissement moins dépenses décidées · rentabilité selon les règles du jeu · niveau des autres clubs de la ligue (retard mesuré) · rang et série de résultats · alternative avec le même argent (achat, autre infrastructure) · avis des amis · ce qui prouvera l'erreur.
