# Décisions importantes : dossier complet et variables obligatoires (tous jeux)

Créé le 2026-10-31 (l'utilisateur : « avant que j'aie une information importante, tu compiles TOUTES les informations nécessaires… pas "j'ai pas tout lu, il me manquait des données" »).

Une **décision importante** = achat, vente, enchère ; composition de ligue, coupe ou playoffs ; analyse d'une défaite ; entraînement de la semaine ; signature ou renvoi (académie, draft, coach, personnel) ; dépense d'infrastructure ou de finances. Les tableaux de routine tirés d'une vue gold (amical, agenda, état des exports) n'en sont pas.

## Les trois sources, toujours ensemble
| Source | Où | Ce qu'on en tire |
|---|---|---|
| **Règles** | skills `.claude/skills/<jeu>-*`, manuel, devlog, News | le mécanisme (pourquoi ça marche) |
| **Avis des amis** | `outputs/<jeu>/veille/connaissance*.md`, `data/discord/<Jeu>/`, `data/chat/<jeu>/`, chat en base | l'expérience des autres managers et du développeur, statut confirmé / contredit / en doute |
| **Chiffres** | vues gold du jeu (`docs/fiches/<jeu>/resume.md` § Vues prêtes), bronze du jour, `learnings.md` | la mesure, sur **toute la saison**, et nos conseils passés (C-nnn → L-nnn) |

## Étapes (dans l'ordre, sans en sauter)
1. **Dossier** : `python pipelines/dossier.py <jeu> <type> [--mots "nom joueur,mot clé"]` → `outputs/<jeu>/dossier/AAAA-MM-JJ-<type>.md` (+ `…-discord.txt` avec **toutes** les lignes trouvées). Il liste les skills à lire, chaque ligne de `connaissance` sur le sujet, chaque message Discord/chat trouvé, les briefs du jour, les learnings, le registre `fait-`.
2. **Lecture intégrale** : l'agent (ou moi) lit le dossier **en entier** et le fichier Discord **en entier**, puis interroge les vues gold citées.
3. **Grille** : chaque variable du type ci-dessous reçoit une valeur et sa source. Une variable vide se cherche (SQL, bronze brut, Discord, chat) avant d'être déclarée absente.
4. **Tableau « Couverture »** en fin de brief : `Source | éléments trouvés | lus | retenus | écartés (pourquoi)`. Lus = trouvés, sinon le brief n'est pas fini.
5. **Police** : l'agent `police` contrôle la grille et la couverture, complète lui-même ce qui manque, puis la décision est rendue.

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

### `academie` (académie, draft, scouting, jeunes)
Chaque prospect : compétences, fourchettes, potentiel estimé, âge · règles du jeu (coût, effet d'un recrutement, probabilités) · besoin de l'effectif par poste · budget · comparaison aux académies des autres clubs · avis des amis · ce qui prouvera l'erreur.

### `finances` (infrastructure, personnel, sponsor, dépense)
Solde, revenus et dépenses par semaine, salaires · capacité d'investissement moins dépenses décidées · rentabilité selon les règles du jeu · niveau des autres clubs de la ligue (retard mesuré) · rang et série de résultats · alternative avec le même argent (achat, autre infrastructure) · avis des amis · ce qui prouvera l'erreur.
