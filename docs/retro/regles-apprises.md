# Règles apprises (à lire en début de session — mises à jour par la rétro de fin de session)

Format : une ligne par règle, la plus récente en haut. Une règle déjà violée deux fois remonte en tête et passe en `CLAUDE.md`.

## 2026-10-27 (soir)
42. Vitesse : agents → `docs/fiches/<jeu>/resume.md` au lieu de 4 fichiers ; 3 agents au plus ; tableau de données = vue gold sans agent ; vérification = requête du même tour ou `synthese`, `verificateur` seulement sans l'un ni l'autre (CLAUDE.md « Vitesse »). À mesurer au prochain passage avec `optimisation` contre `outputs/optimisation/2026-10-27-basketvibe.md`.
41. Rendu de saisie BasketVibe = `select * from gold.bv_saisie_joueurs` / `gold.bv_saisie_adversaires` (filtre `kind`, `match_day`, `order by ordre`), sans agent. Coût mesuré en fin de session par l'agent `optimisation` (`pipelines/mesure_session.py`) ; mesure du 27/10 : 85 min, contexte max 108 %, 9 agents = 8,2 M tokens relus, `basketvibe.yaml` relu par 8 agents.
39. Budget par jeu : 23 jeux ne tiennent pas si un jeu coûte 27 % du contexte et 1 h. Cible : un rendu de saisie = 1 requête SQL + 1 tableau, sans agent ; agents seulement pour décider ; jamais plus de 3 agents par passage ; `/compact` dès 15 % ; estimation de durée annoncée = durée tenue (j'avais dit 15–20 min, réel 60 min : cause = 7 agents en série qui relisent les mêmes fichiers).
40. Contexte : je dis moi-même « /compact maintenant » dès ~15 % de contexte ou après un gros rendu, avec la raison (chaque message relit tout le contexte et coûte plus cher). Oublié le 27/10 jusqu'à 27 % : RÉCIDIVE de CLAUDE.md « Tokens ».
38. Tactique : joueurs et adversaires dans l'ordre de l'écran (par poste PG-SG-SF-PF-C, puis alphabétique ; l'ordre brut du JSON est alphabétique global, faux), et tableau défensif par adversaire avec focus ET zone (R-10 complété). Oublier la zone dans l'amical et ranger par poste = RÉCIDIVE de 35.
37. Les agents sont liés : un désaccord entre deux briefs (Match vs Effectif sur les 48 minutes) se tranche par moi avec la source avant de rendre, et je n'inverse pas ma position sans fait nouveau. Si la tâche est un tableau de données déjà en base, je le fais moi-même en SQL (5 minutes) plutôt que d'enchaîner 7 agents (45 minutes, 27 % du budget).
36. Réserve d'argent = sorties moins recettes certaines de la même période (pas deux semaines de charges à recettes nulles) ; l'argent qui dort n'est pas un conseil : chaque passage Finances nomme un usage chiffré (A-3).
35. Tactique = tableau joueur × quart-temps avec toutes les colonnes (R-10) ; l'amical aussi (config du 2026-10-27). RÉCIDIVE de la règle 3 de rendu.
34. Avant tout « que faire » pour un match : lire la ligne du type de match dans `docs/attentes/jeux/<jeu>.yaml` (BasketVibe amical = `saisie: non, preset: non`) et le plan de tests ouvert dans `learnings.md` (C-063 : area Perimeter/Rim/Middle par amical). Jamais reprendre `gold.bv_agenda` (« preset amical ») ni demander l'export Preview d'un amical (RÉCIDIVE des règles 8, 29, 30).
33. Un utilisateur qui exporte beaucoup attend la chaîne complète (lecteur → Match → Effectif → Finances → Tactique → Transferts) sans que je m'arrête après le sponsor et la veille ; lancer la chaîne dès l'arrivée des exports.

## 2026-10-26 (fin de nuit)
31. Ce que je fais pour un jeu, je le vérifie pour les autres dans la même session et je l'étends sans demander (base des transferts faite pour BasketVibe seul alors que la mémoire disait « par jeu » ; « tu as tout, prends l'initiative »). Règle A-10 de `attentes.md`.

## 2026-10-26 (nuit) — les règles de rendu vivent désormais dans `docs/attentes/attentes.md` (R-1 à R-9, A-1 à A-9)
30. Une consigne de l'utilisateur s'écrit là où les agents la lisent (`attentes.md` ou config du jeu), jamais seulement en mémoire (preset d'amical redemandé après avoir été noté).
29. Une alerte sans action ne s'affiche pas ; horizon = maintenant + demain si annoncé (RÉCIDIVE de la règle 20 → R-1, R-2).
28. L'agent économie décide de l'usage de l'argent avant Transferts ; une réserve se justifie par les sorties certaines (A-3).
27. Une remarque sur un jeu va dans `attentes.md` par défaut ; dans la config du jeu seulement si elle nomme une mécanique propre au jeu.

## 2026-10-26 (soir)
26. Avant tout lancement d'agent : demander `/effort medium` si je ne sais pas que la session y est (RÉCIDIVE de la règle CLAUDE.md « Agents d'analyse » ; vérificateur et lecteur lancés sans l'avoir demandé).
24. Au « reprenons » : relire les briefs du jour et le registre `fait-…` avant l'agenda ; jamais répondre depuis `gold.*_agenda` seul.
23. Plan ou liste de plus de 5 lignes = `verificateur` avant de répondre (récidive de la règle CLAUDE.md « Vérificateur » : 3 réponses sans lui, 4 erreurs).
22. Avant d'écrire « pas de donnée » ou « absent » : chercher dans tous les exports, y compris `data/chat/`, et dans le dernier export bronze (pas seulement silver).
25. Un investissement se juge contre la situation du club : Fan Shop (revenu lié au classement, 6e/10) ou Arena avant la Youth Academy en retard n'a pas de sens ; relire le « pourquoi » d'un plan avant de le relayer, même venu de `decideur` + `verificateur`.
21. Avant de dire qu'une décision n'a pas d'obstacle : relire la section « Réglage exact » du brief concerné ; une dérogation à un `C-nnn` se déclare et décale ses critères de réfutation. `captured_at` est en UTC : heure Paris via `at time zone 'Europe/Paris'`.

## 2026-10-25 (à lire en premier)
20. « Que faire » = seulement ce qui est faisable maintenant. Jamais d'export de match ni d'action « après le match » dans « Reste à faire » : je les annonce quand le match est joué (RÉCIDIVE de « pas de temporalité »).
19. Six Zero League : une seule tactique par défaut pour tous les matchs ; on ne choisit pas de compo par match. `gold.sz_agenda` répète « tactique pour J14 / J15 » : ne pas la reprendre telle quelle, la tactique du jour couvre les matchs suivants.

## 2026-10-24 (bilan de fin de journée)
18. Conseil d'une catégorie échoué deux fois = nouveau levier nommé, jamais « ne rien changer » (RÉCIDIVE ; agent Match). Compter les échecs dans `learnings.md` avant d'écrire.
17. Série de 3 défaites ou plus : le brief propose un changement chiffré de composition ou de tactique.
16. Une vue de résultat se teste sur un match non joué (`bv_matches.my_result` donne `L` si le score est NULL, bug B1).
15. Expliquer un script ou une vue = l'ouvrir et citer la ligne (RÉCIDIVE de la règle 6, à monter dans `CLAUDE.md` avec la règle 17 de début de session).
14. Les `C-nnn` se prennent après le plus grand ID du fichier (BV a deux C-046).
13. Trou de données (Team Soccer `ts_match_lineups`) : une seule demande, avec le geste exact, puis les conseils dépendants sont marqués « non vérifiable ».

## 2026-10-24 (matin)
1. Résultat d'un match = `my_result` / `is_mine`, jamais le score brut.
2. Tout solde se recoupe avec la dernière ligne de dépenses ; sinon « non recoupé ».
3. Un rang se lit avec sa date et son club ; le rang de l'adversaire n'est pas le nôtre.
4. Un conseil d'achat m'engage : je le suis (acheté ? vendu ?). Un revirement se déclare avec son plan de sortie chiffré.
5. Une hypothèse de l'utilisateur qui contredit le guide : je le dis tout de suite, avant de produire un tableau.
6. Avant de dire « absent de la base » : comparer `captured_at` des exports à l'heure du passage ; lancer `lecteur-exports`.
7. Les options d'un écran (select, énumérations) sont des données : `lecteur-exports` les compare aux fiches.
8. Jamais redemander un preset, un export ou une action du registre `fait-…`.
9. Transferts : ouvrir par les cibles nommées (poste faible → candidats, prix, heure de fin), pas par les ventes ; réclamer un export marché frais s'il a plus de 24 h.
10. Un match n'est jamais expliqué seul : le comparer à tous les matchs de la saison, lire la tactique adverse, et dire ce qui sépare victoires et défaites.
11. Un jeu par session, un agent seulement sur nouvel export, résumé de 10 lignes.
12. Plan du jour : lire l'horloge de Paris avant ; aucune échéance passée.
