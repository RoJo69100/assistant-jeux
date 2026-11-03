# Triage des règles — refonte v2, étape 0.3-A (2026-11-03)

Sources triées : `CLAUDE.md` (CM-nn), `docs/attentes/attentes.md` (R-n, A-n), `docs/retro/regles-apprises.md` (Lnn = **ligne** du fichier au commit `35b50a7`, le numéro de la règle entre parenthèses ; les numéros 13 à 31 existent deux fois, la ligne les distingue). **Rien n'est supprimé ni déplacé par ce fichier** : les destinations sont appliquées en 0.3-C/D/E.

**Classes** : **E** enforce (code) · **S** scope (un jeu ou un domaine) · **K** keep (≤ 15, prose) · **D** delete (doublon, contredite, obsolète).
**Enforcement** : `existant : X` = déjà bloqué ou fourni par X ; `à écrire : X (étape)` = fichier du plan ; `—` = rien. Une règle E sans code existant reste dans `actives.md` en attendant (colonne « interim »).

## 1. `CLAUDE.md`

| id | résumé | classe | destination | enforcement |
|---|---|---|---|---|
| CM-01 | Français court ; ne jamais deviner une règle de jeu, citer la source | K | actives (K1) | — |
| CM-02 | Travail fini quand la checklist est cochée, avec critère et date | S | `docs/checklist-<jeu>.md` | — |
| CM-03 | Collecte passive Tampermonkey, jamais de robot ni requête vers le jeu | K | actives (K2) | pas de code ; interdit §0.4 du plan |
| CM-04 | Discord importé en bronze par `import_discord.py`, fichiers non versionnés | S | carte du dépôt | existant : `.gitignore`, `scan_secrets.py` |
| CM-05 | Bronze/silver/gold ; calculs en SQL, pas dans le LLM | S | carte du dépôt | — |
| CM-06 | Skills par jeu, faits sourcés ; propositions `V-…` appliquées avec citation au commit | S | `.claude/agents/veille.md`, A-6 | — |
| CM-07 | Liste des agents, 5 retirés, plafond 20/semaine, donner le jeu | E | `.claude/agents/`, `ops.agent_run` | à écrire : `orchestre.py` (5.1) ; liste des retirés = D |
| CM-08 | `resume.md` obligatoire par jeu, mis à jour avec attentes/config | E | `docs/fiches/<jeu>/resume.md` | à écrire : `contexte_budget.py` vérifie l'existence (0.5) |
| CM-09 | Attentes générales + config YAML du jeu, la config l'emporte | S | `docs/attentes/` | — |
| CM-10 | Sorties dans `outputs/<jeu>/` | S | carte du dépôt | — |
| CM-11 | Arborescence du dépôt | S | carte du dépôt (CLAUDE.md, 8 lignes) | — |
| CM-12 | Secrets dans `.env` ; `samples/`, `data/discord/`, `data/chat/` ignorés | E | `.gitignore` | existant : `scan_secrets.py` + pre-commit (0.2) |
| CM-13 | Deux PC : mémoire copiée dans `docs/memoire-claude/`, commit et push | K | actives (K9) | existant : hook `git pull` ; copie mémoire à écrire (hook, hors phase 0) |
| CM-14 | Python 3.13, dépendances dans `requirements.txt` | S | `requirements.txt` | — |
| CM-15 | Une modification = un commit au message clair | K | actives (K4) | — |
| CM-16 | Coût : ne jamais relire l'historique brut, travailler sur gold et delta | E | `pipelines/sql.py` | à écrire : `sql.py` (0.4) |
| CM-17 | Une tâche par session, `/clear` après commit, `/compact` quand long, requêtes avec LIMIT | K | actives (K5) | existant : H5 de `police.py` (rappel rétro) ; `sql.py` ajoute le LIMIT (0.4) |
| CM-18 | Session et agents en Sonnet ; conception = rappel `/model opus` puis `/model sonnet` | E | hook | existant : `controle.py` contrôle a |
| CM-19 | « Que faire » = actions maintenant par jour ; BV a un amical chaque jour | S | `gold.agenda`, `resume.md` BV | à écrire : `gold.agenda` générique (1.4) |
| CM-20 | Règle d'or : seulement le faisable maintenant ; exception transferts | E | `gold.agenda` (champ `exception_transfert`) | à écrire : `gold.agenda` (1.4) ; annexe A |
| CM-21 | Horizon aujourd'hui seulement ; achat contrôlé contre `capacite_invest` moins l'engagé | E | `forme.py`, `gold.buy_targets` | **aucun hook aujourd'hui** (voir arbitrage 10) ; à écrire : mots « demain », dates futures dans un plan (`forme.py`, 0.3-bis) ; `buy_targets` (2.4) |
| CM-22a | Ordre de lancement selon `dependances` du YAML, briefs amont transmis | E | `orchestre.py` | à écrire : 5.1 |
| CM-22b | Type d'agent propre, jamais `general-purpose` + « lis le fichier » ; aucune demande libre | E | hook | à écrire : contrôle sur les appels `Agent` dans `controle.py` (0.3-bis) |
| CM-22c | `police` obligatoire avant achat, vente, composition, défaite, finances… | E | `police.py` | existant : H1/H2 |
| CM-22d | Défaite en base lance `analyste` ; deux défaites lancent `decideur` | E | `orchestre.py` | à écrire : 5.1 (+ `match_objective` 2.2) |
| CM-22e | Avant `/clear` ou après 5 échanges : `retro` + `mesure_session.py` | E | hook | existant : H5 |
| CM-23 | Après un export : vérifier l'arrivée, compte rendu 1 à 3 lignes, proposer l'agent | D | doublon de `attentes.md` §4.1 | — |
| CM-24 | Agents d'analyse en medium + Sonnet, refus de tout autre réglage | E | agents (`model: sonnet`), `orchestre.py` | existant : frontmatter ; annonce du réglage à écrire (5.4) |
| CM-25 | Skill `deja-fait` avant tout plan ; registre `fait-AAAA-MM-JJ.md` | E | hook | existant : `controle.py` contrôle b |
| CM-26 | Je tranche : une action unique, le doute en une demi-ligne | E | hook | existant : `controle.py` contrôle d |
| CM-27 | Plus de `verificateur` ; plan à partir d'une requête du tour | D | obsolète (agent retiré) ; fond repris par CM-28 | existant : contrôle c |
| CM-28 | Aucun chiffre, nom, date non vérifié ; vérification au moindre coût (requête du tour, `synthese` si ≥ 2 briefs) | E | `verifier_rendu.py` | existant : `controle.py` contrôle c ; complet à écrire (5.3) |
| CM-29a | Un tableau de données = une vue gold, zéro agent | E | `rapport_jour.py` | à écrire : 5.5 |
| CM-29b | Trois agents au plus par passage, 20 par semaine | E | `orchestre.py` | à écrire : 5.1 ; annexe A |
| CM-29c | Annoncer la durée avant de lancer des agents | D | sans valeur mesurable | — |
| CM-29d | Créer la vue gold dès qu'un gain existe, sur tous les jeux (= A-10) | D | contredit « un jeu par session » ; propagation par `core` | annexe A |
| CM-29e | Effectif à chaque passage : verdict par poste, vente ouverte jusqu'à exécution ; V/D sur toute la saison | S | cartes `_core/{vente,achat,defaite}` | à écrire : `gold.roster_bilan`, `gold.sell_candidates` (1.4, 2.4) |
| CM-30 | Chercher dans toutes les sources avant « absent » ; `connaissance.md` par thème, veille à chaque export | E | `kb.py` | à écrire : `kb.py` compteur (4.4) ; interim = actives |
| CM-31 | Dossier complet avant décision importante : `dossier.py`, cartes, `--marquer` | E | `dossier.py`, `garde.py` | existant : H1/H2 ; « lire en ENTIER » remplacé par P3 (annexe A) |
| CM-32 | Aucun flou : les données en base, je les lis et nomme | D | doublon de R-5 | — |
| CM-33 | Chaque conseil `C-nnn` confronté au résultat `L-nnn`, deux échecs = réécrit | E | `learn.*` | à écrire : 3.1–3.3 ; interim K10 |
| CM-34 | Réglage effort/modèle : je dis quoi régler (table low/medium/Haiku/Opus) | E | `orchestre.py` | à écrire : annonce (5.4) |
| CM-35 | Tableau court + 1 à 3 lignes ; focus défensif 1–5 | E | `forme.py` | existant |
| CM-36 | Pastilles 🟥 URGENT / 🟧 IMPORTANT / 🟩 SUIVI, pastille + mot | E | `forme.py` | existant |
| CM-37 | Team Soccer : deux clubs partout | E | `forme.py` H3 | existant |
| CM-38 | Hockey Nation : 4 équipes, talents d'abord | E | `forme.py` H3 ; S `resume.md` HN | existant |
| CM-39.1 | Synthèse, pas de déluge | E | hook | existant : `controle.py` contrôle e |
| CM-39.2 | Un tableau par jeu, catégories fixes, aucune ligne « rien à faire » | E | `forme.py` | existant |
| CM-39.3 | Saisie d'équipe complète, poste par poste, ordre de l'écran | E | `forme.py` | existant |
| CM-39.4 | Défaite = analyse détaillée, joueur par joueur, comparée à la saison | S | carte `_core/defaite` | — |
| CM-39.5 | Chaque rapport : un levier nommé (achat/vente/recrutement) ou la raison de n'en faire aucun | S | cartes `_core/{achat,vente}` (= A-4) | à écrire : `gold.buy_targets` (2.4) |
| CM-39.6 | Retard mesuré contre la ligue (= A-8) | S | carte `_core/finances` | — |
| CM-39.7 | Résultat = `my_result` / `is_mine`, jamais le score brut | E | `core.fixture.my_result` | à écrire : 1.1 ; interim actives |
| CM-39.8 | HN : tout ajout de joueurs = équipe résultante complète | S | `resume.md` HN | existant : `forme.py` H3 |
| CM-39.9 | Chaîne d'agents limitée aux agents déclenchés, `synthese` en dernier | E | `orchestre.py` | à écrire : 5.1 |
| CM-39.10 | Confiance faible = test ; décision forte porte « ce qui prouvera que j'avais tort » ; revirement signalé | E | JSON de 2.5, `garde.py` | à écrire : 2.5, 3.4 |
| CM-39.11 | Ventes et enchères ouvertes vérifiées à chaque passage | E | `gold.engaged_spend` | à écrire : 2.4 |
| CM-40.17 | Début de session : charger `retro-session`, appliquer les règles apprises | E | `rappel_debut.py` | existant ; sortie réduite aux titres actifs (0.3-D) |
| CM-40.18 | Fin de session : proposer la rétro | E | `police.py` H5 | existant |
| CM-40.19 | Analyse de match jamais seule (saison, tactique adverse, 3–5 points testables) | S | carte `_core/defaite` (= A-2) | — |
| CM-40.20 | Brief Transferts ouvert par des cibles nommées ; marché > 24 h = « exporte le marché » | S | carte `_core/achat` | à écrire : `buy_targets` (2.4) |
| CM-41.12 | Un agent ne tourne que si un export plus récent que son brief est arrivé | E | `orchestre.py` (hash) | à écrire : 5.1 |
| CM-41.13 | Plan du jour en SQL, sans agent | E | `rapport_jour.py` | à écrire : 5.5 |
| CM-41.14 | Un jeu par session, `/clear` entre deux jeux | K | actives (K5) | existant : H5 |
| CM-41.15 | Briefs plafonnés : une page, résumé d'agent 10 lignes | E | `contexte_budget.py` | à écrire : 0.5 (budget brief) |
| CM-41.16 | État des exports d'abord en SQL, clés nouvelles ajoutées à `commun.md` | E | `gold.exports_state` | existant : `gold.*_exports_state`, `sante_collecte`, `exports_nouvelles_cles` ; générique 1.4 |
| CM-42 | Écrire les fichiers avec Write, jamais par heredoc | E | hook PreToolUse | à écrire : refuser `Bash` avec heredoc d'écriture de fichier (0.3-bis) ; interim actives |
| CM-43 | Sources BasketVibe (manuel, devlog, Discord) | S | `resume.md` BV, `kb` | — |

## 2. `docs/attentes/attentes.md` (reste la source des exigences ; `actives.md` ne la recopie pas)

| id | résumé | classe | destination | enforcement |
|---|---|---|---|---|
| R-1 | Aujourd'hui seulement ; jamais « demain » comme étape | E | `forme.py`, `gold.agenda` | voir CM-21 |
| R-2 | Des actions, pas des alertes | E | `gold.agenda` | à écrire : 1.4 |
| R-3 | Un tableau par jeu, colonnes priorité/catégorie/action | E | `forme.py` | existant |
| R-4 | Saisie complète dans l'ordre de l'écran | E | `forme.py` | existant |
| R-5 | Aucun flou, pas de « si », donnée absente = « exporte Y » | K | actives (K6) | — |
| R-6 | Court, contradictions entre agents tranchées sans les montrer | E | hook | existant : contrôle e |
| R-7 | Ne jamais redemander ce que l'utilisateur a fait | E | registre `fait-…`, `rapport_jour.py` | existant : contrôle b ; complet 5.5 |
| R-8 | Je tranche, preuve contraire et date du test | E | hook, JSON 2.5 | existant : contrôle d ; preuve : 2.5 |
| R-9 | Vérifié avant d'être dit | E | `verifier_rendu.py` | voir CM-28 |
| R-10 | Tactique = tableau joueur × Q + adversaires (focus ET zone), ordre de l'export | E | `forme.py` | existant |
| R-11 | Consigne de l'utilisateur jamais refusée sans preuve citée | K | actives (K7) | — |
| R-12 | Team Soccer, composition : deux clubs, 5 zones, banc, remplacements, cible de « Passer » | E | `forme.py` ts-compo | existant |
| A-1 | Série de défaites = changement fort tout de suite | E | `gold.match_objective` (objectif `corriger`) | à écrire : 2.2 |
| A-2 | Défaite = analyse chiffrée, saison entière, 3–5 points testables | S | carte `_core/defaite` | — |
| A-3 | Argent : chaque passage dit quoi faire de l'argent, réserve justifiée | E | `gold.finance_policy` | à écrire : 2.4 |
| A-4 | Un levier nommé par rapport ; **jamais d'enchère ni de vente sans accord** | K | actives (K3) pour l'accord ; S cartes achat/vente | accord : pas de code |
| A-5 | Engagement : d'abord « en a-t-on besoin ? » puis recalcul des dépendances | S | cartes `_core/finances` | — |
| A-6 | Nouveauté = test (amical sinon protocole chiffré) ; `V-…` appliquées | S | `agents/veille.md` | — |
| A-7 | Conseil suivi `C-nnn`, confronté `L-nnn`, deux échecs = réécrit | E | `learn.*` | à écrire : 3.3 (= CM-33) |
| A-8 | Retard mesuré contre la ligue | S | carte `_core/finances` | — |
| A-9 | Chercher dans toutes les sources avant « absent » | E | `kb.py` | à écrire : 4.4 (= CM-30) |
| A-10 | Initiative multi-jeux dans la même session | D | contredit « un jeu par session » | annexe A |
| A-11 | Changement de saison : déroulé en 6 points | S | carte `_core/saison` (à créer) ; déclencheur `season_id` | à écrire : `orchestre.py` événement « nouvelle saison » (5.1) |

## 3. `docs/retro/regles-apprises.md`

| id | résumé | classe | destination | enforcement |
|---|---|---|---|---|
| L1 | (HN 29/10) tableaux par équipe, listes affichées, coachs par xp, joueurs bloqués lus dans `hn_declared` | S | `resume.md` HN | existant : `forme.py` H3 |
| L7 | (82) contradiction de moins de 5 lignes corrigée dans le tour | D | remplacée par `arbitrages.md` | — |
| L8 | (81) une règle ne m'ordonne jamais de demander ; je décide | D | doublon CM-26 | existant : contrôle d |
| L9 | (80) conception : 5 lignes, zéro identifiant interne | E | hook | existant : contrôle e |
| L12 | (79) lire les règles globales ; liste G1–G12 au démarrage | E | `rappel_debut.py` | existant ; remplacé par titres actifs + 3 exports en retard (0.3-D) |
| L13 | (77) `dossier.py` à chaque décision, la carte d'abord | E | `police.py` H1 | existant |
| L14 | (78) « je ne peux pas » interdit sans preuve ou commande | E | hook | à écrire : mots dans `controle.py` (0.3-bis) |
| L15 | (76b) règle globale > résumé de jeu | K | actives (K8) | — |
| L18 | (76) MCP non authentifié = état de session à autoriser, réessayer au début | S | `rappel_debut.py` (texte gardé) | existant |
| L19 | (75) tout lire en ENTIER, pas de grep partiel | E | `kb.py`, compteur | remplacée par P3 (annexe A) ; à écrire : 4.4 |
| L22 | (74) mot interdit des tests = expression, pas préfixe | S | `docs/attentes/tests/` | existant : `recette.py` |
| L23 | (73) supprimer les `dossier/<date>-*` créés par un test | E | tests | à écrire : tests de `dossier.py` en répertoire temporaire (0.3-bis) |
| L24 | (72) requête de carte écrite après lecture des colonnes de la vue | E | `test_vues.py` | à écrire : 7 |
| L25 | (71) 6 jeux enchaînés = 29,6 M relus ; `/clear` entre jeux | K | actives (K5) | existant : H5 |
| L26 | (70) même la conception commence par les règles apprises | D | remplacée par le hook de démarrage | existant : `rappel_debut.py` |
| L29 | (69) calendrier frais (< 12 h) avant tout plan ; statut lu dans le calendrier ; forfait sans export | E | `gold.agenda` (colonne fraîcheur) | à écrire : 1.4 / 5.5 ; détail SZ en S `resume.md` SZ |
| L31 | (68) HN : jamais Trade Center ; lire `resume.md` [U] et `raw_pages` 3 h avant de lister des exports | S | `resume.md` HN | — |
| L32 | (67) page « absente » : regarder la dernière capture brute (Cloudflare) | S | `commun.md` HN | — |
| L33 | (66) lire `pg_get_viewdef` avant « la vue ne fait pas X » ; TS : croiser l'export du jour | S | carte TS composition | à écrire : `test_vues.py` (7) |
| L36 | (65) `bv_zone_jouee` lit l'export d'avant la saisie | S | carte BV tactique ; adaptateur BV (1.2) | — |
| L37 | (64) avant « pas en base » sur un adversaire : requête `ilike` | S | carte BV tactique (= A-9) | — |
| L38 | (63) relire `forme.py` avant rendu tactique | D | le hook bloque | existant : `forme.py` |
| L41 | (62) TS compo : colonnes remplies, DL/DC/DR, état lu dans `player_orders` | S | `resume.md` TS | existant : `forme.py` ts-compo |
| L42 | (61) match demain = donner la saisie complète depuis `hn_tactique_rendu` | S | `resume.md` HN | existant : `forme.py` |
| L43 | (60) numéro de match ≠ jour de saison | S | `resume.md` HN ; `core.fixture.round_no` (1.1) | — |
| L44 | (59) pénalité −20 % = colonne `poste` de `hn_tactique_rendu` | S | `resume.md` HN | — |
| L45 | (58) réponse d'offre lue dans `club_news` et diff `hn_club_staff` | S | `resume.md` HN | — |
| L46 | (57) vue de décision testée sur le cas limite connu | E | fixtures | à écrire : `tests/fixtures` (7) |
| L47 | ((forme)) catégories de plan fixes | E | `forme.py` | existant |
| L50 | (56) coachs U17/U21 : `hn_coach_potential`, gain ≥ 5 | S | `resume.md` HN | — |
| L51 | (55) vue de marché = dernier export seulement | S | `resume.md` HN ; test vues | à écrire : 7 |
| L52 | (54) TS : dépense décidée soldée par comparaison de solde ; semaine exceptionnelle non projetée | S | carte TS finances ; `gold.engaged_spend` (2.4) | — |
| L53 | (53) TS « que faire » : compo complète, seulement le faisable maintenant | S | `resume.md` TS | existant : `forme.py` |
| L56 | (52) fin de journée : lister d'abord quels jeux ont eu des briefs | D | doublon R-7 | — |
| L57 | (51) Discord jamais lu en entier : première passe intégrale | E | `kb` backfill | à écrire : 4.3 |
| L58 | (50) priorité entraînement/draft/scouts = marge de progression | S | cartes HN entraînement, académie | — |
| L59 | (49) scouts : couvrir le maximum de joueurs, liste donnée | S | carte HN académie | — |
| L60 | (48) coach faible : plan B nommé dans la même réponse | S | carte HN transferts | — |
| L61 | (47) « les 4 » : compter `hn_declared`, un tableau par équipe | S | `resume.md` HN | existant : `forme.py` H3 |
| L64 | (43) saisie BV depuis `gold.bv_saisie_*`, zone de l'export | S | carte BV tactique | existant : `forme.py` |
| L65 | (44) amical = composition de test, un seul test ; tableau adversaires « les 12 » | S | `basketvibe.yaml` | — |
| L66 | (45) ne jamais demander l'export Preview d'un amical | S | `basketvibe.yaml` | — |
| L67 | (46) « 0 ligne » en silver n'est pas une absence ; lire `bv_fixture_api` | S | carte BV tactique (= A-9) | — |
| L70 | (42) vitesse : `resume.md`, 3 agents, vue gold sans agent | D | doublon CM-29 | — |
| L71 | (41) saisie BV = `select * from gold.bv_saisie_*` | D | doublon L64 | — |
| L72 | (39) budget par jeu : un rendu = 1 requête + 1 tableau | D | objectif M4 du plan | — |
| L73 | (40) proposer `/compact` à ~15 % de contexte | K | actives (K5) | — |
| L74 | (38) tactique : ordre de l'écran, focus ET zone | E | `forme.py` | existant |
| L75 | (37) désaccord entre briefs tranché par moi avec la source | D | doublon CM-26 / R-6 | — |
| L76 | (36) réserve = sorties moins recettes certaines ; l'argent qui dort n'est pas un conseil | E | `gold.finance_policy` | à écrire : 2.4 |
| L77 | (35) tactique = tableau joueur × Q, aussi en amical | E | `forme.py` | existant |
| L78 | (34) lire la ligne du type de match dans le YAML et le plan de tests ouvert | S | `basketvibe.yaml` ; `gold.agenda` (1.4) | — |
| L79 | (33) chaîne complète dès l'arrivée des exports | D | contredit plafond 3 agents et « sur nouveauté » | annexe A |
| L82 | (31) étendre aux autres jeux sans demander | D | = A-10 | annexe A |
| L85 | (30) une consigne s'écrit dans `attentes.md`/YAML, pas seulement en mémoire | D | doublon de l'en-tête d'`attentes.md` | — |
| L86 | (29) alerte sans action non affichée ; horizon | E | `gold.agenda` | à écrire : 1.4 (= R-2) |
| L87 | (28) agent économie décide avant Transferts | D | agent retiré ; fond = L76 | — |
| L88 | (27) remarque d'un jeu → `attentes.md` par défaut | D | doublon de l'en-tête d'`attentes.md` | — |
| L91 | (26) demander `/effort medium` avant tout agent | E | `orchestre.py` | à écrire : 5.4 (= CM-24) |
| L92 | (24) au « reprenons » : relire briefs et `fait-…` avant l'agenda | E | `rapport_jour.py` | à écrire : 5.5 (= R-7) |
| L93 | (23) plan de plus de 5 lignes = `verificateur` | D | agent retiré | — |
| L94 | (22) avant « absent » : chercher dans tous les exports et `data/chat/` | E | `kb.py` | à écrire : 4.4 (= A-9) |
| L95 | (25) un investissement se juge contre la situation du club | S | carte `_core/finances` | — |
| L96 | (21) relire « Réglage exact » ; dérogation à un `C-nnn` déclarée ; `captured_at` en UTC → Paris | E | `core` (`day` Paris) ; `learn.decision` | à écrire : 1.1, 3.2 |
| L99 | (20) « que faire » = seulement le faisable maintenant | E | `gold.agenda` | = CM-20 |
| L100 | (19) SZ : une tactique par défaut ; ne pas reprendre l'agenda tel quel | S | `resume.md` SZ | — |
| L103 | (18) conseil échoué 2 fois = nouveau levier nommé | E | `learn.lesson` (retired) | à écrire : 3.3 |
| L104 | (17) 3 défaites ou plus : changement chiffré | E | `gold.match_objective` | à écrire : 2.2 (= A-1) |
| L105 | (16) vue de résultat testée sur un match non joué | E | fixtures | à écrire : 7 |
| L106 | (15) expliquer un script = l'ouvrir et citer la ligne | D | couvert par CM-28 / R-9 | — |
| L107 | (14) `C-nnn` pris après le plus grand ID | E | `learn.decision` (id auto) | à écrire : 3.2 |
| L108 | (13) trou de données TS `ts_match_lineups` : une demande avec le geste exact | S | `resume.md` TS | — |
| L111 | (1) résultat = `my_result` / `is_mine` | E | `core.fixture.my_result` | = CM-39.7 |
| L112 | (2) tout solde recoupé avec la dernière ligne de dépenses | E | `gold.finance_health` | à écrire : 1.4 |
| L113 | (3) un rang se lit avec sa date et son club | E | `core.standing` | à écrire : 1.1 |
| L114 | (4) conseil d'achat engage ; revirement déclaré avec plan de sortie | E | `garde.py` | à écrire : 3.4 |
| L115 | (5) hypothèse de l'utilisateur contredisant le guide : le dire tout de suite | D | absorbée par R-11 | — |
| L116 | (6) avant « absent » : comparer `captured_at`, lancer `lecteur-exports` | D | agent retiré ; fond = A-9 | — |
| L117 | (7) options d'écran = données, comparées par `lecteur-exports` | D | agent retiré ; remplacé par `gold.exports_nouvelles_cles` | existant |
| L118 | (8) jamais redemander un preset, un export, une action du registre | E | registre `fait-…` | = R-7 |
| L119 | (9) Transferts : cibles nommées d'abord, export marché frais s'il a > 24 h | S | carte `_core/achat` | à écrire : 2.4 |
| L120 | (10) un match jamais expliqué seul | S | carte `_core/defaite` (= A-2) | — |
| L121 | (11) un jeu par session, un agent sur nouvel export, résumé de 10 lignes | D | doublon CM-17, CM-41 | — |
| L122 | (12) plan du jour : lire l'horloge de Paris | E | `core` (`day` Paris) | à écrire : 1.1 |
| L123 | (13) V/D comparées + questions d'effectif posées seul | S | cartes `_core/defaite`, `_core/vente` (= CM-29e) | — |
| L124 | (14) score partiel remis de notre point de vue | E | `core.fixture` (`my_score`) | à écrire : 1.1 |
| L125 | (15) aucune action au-delà d'aujourd'hui | E | = CM-21 | voir CM-21 |
| L126 | (16) achat non finançable : contrôle `capacite_invest` moins l'engagé | E | `gold.buy_targets` | à écrire : 2.4 |
| L127 | (17) à chaque `youth-scout` : compter les jeunes complets | S | carte `_core/academie` | — |
| L128 | (18) verdict sur jeunes : heure de l'export donnée, export frais | S | carte `_core/academie` ; fraîcheur 1.4 | — |
| L129 | (19) jeune jugé sur compétences nommées, pas sur un OVR | S | carte `_core/academie` | — |
| L130 | (20) le plafond d'agents ne justifie pas « prochaine étape » | D | contredit l'orchestrateur ; la décision sort de `rapport_jour` | annexe A |
| L131 | (21) proposer `/compact` après 8 agents ou 30 échanges | D | absorbée par K5 | — |
| L133 | (22) champ présent dans un export = fonction existante ; adversaires une ligne par joueur | S | `kb` BV ; `forme.py` | existant : `forme.py` |
| L135 | (23) 3e récidive format tactique BV ; relancer `raw_pages` avant « absent » | S | carte BV tactique | existant : `forme.py` |
| L136 | (24) anticiper le focus défensif adverse sur nos joueurs | S | carte BV composition | — |
| L137 | (25) ne pas changer la compo gagnante sans preuve chiffrée | S | carte BV composition | — |
| L138 | (26) rotation : « Minutes lourdes » ET quart-temps des matchs en base | S | carte BV composition | — |
| L140 | (27) SZ : match demain = « Composition : … » saisie complète | S | `resume.md` SZ | compatible avec R-1 (se prépare aujourd'hui) |
| L141 | (28) SZ : saisie lue dans `gold.sz_saisie_reglages` | S | `resume.md` SZ | — |
| L143 | (29) BV : transfert traité dans le même tour (`bv_market_bargains`, `bv_market_candidates`) | S | carte BV achat | à écrire : `buy_targets` (2.4) |
| L145 | (TS) export de match non joué : vérifier `status = 'finished'` | S | `resume.md` TS ; `core.fixture.played` (1.1) | — |
| L147 | (30) Hardwood : décision écrite tout de suite ; tableau Réglage/Actuel/À mettre | S | `resume.md` HW | existant : `forme.py` hw-tactique ; décision : `learn.decision` (3.2) |
| L149 | (31) usage des agents : type propre, `police`, `analyste` | E | = CM-22 | voir CM-22 |

## 4. Comptage et K retenues

K (10 sur 15 permis) : K1 CM-01 · K2 CM-03 · K3 A-4 (accord) · K4 CM-15 · K5 CM-17 + L25 + L73 + CM-41.14 · K6 R-5 · K7 R-11 · K8 L15 · K9 CM-13 · K10 CM-33 (interim jusqu'à 3.3).
Les règles E sans code existant et les plus violées (CM-21 horizon, CM-39.7 `my_result`, CM-42 heredoc, L14 « je ne peux pas ») restent en tête de `actives.md` jusqu'à leur code (0.3-bis ou phases 1 à 5).
