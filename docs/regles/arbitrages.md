# Arbitrages entre règles contradictoires — 2026-11-03

Une ligne par conflit, décision datée. Les huit premiers viennent de l'annexe A du plan ; les suivants ont été trouvés pendant le triage (`triage.md`).

| # | Conflit | Décision (2026-11-03) |
|---|---|---|
| 1 | « Tout lire en ENTIER » (L19, CM-31) contre le coût | Complétude par requête : tout le thème via `kb.py` ou une vue, avec « N affichées / N total » ; jamais un corpus entier en contexte. |
| 2 | « Je tranche » (CM-26, R-8) contre « laisser l'utilisateur arbitrer » (anciennes L19, L8) | Je tranche. L'utilisateur n'est sollicité que pour une action irréversible (plan §0.4) ou le budget d'un backfill. |
| 3 | Plafond 20 agents/semaine et 3 par passage contre `police`, `analyste`, `decideur` | Plafond appliqué par `orchestre.py` (5.1). Exceptions : `police` (script d'abord), `analyste` sur défaite. |
| 4 | A-10 « initiative multi-jeux » (CM-29d, L82) contre « un jeu par session » | A-10 supprimé comme comportement de session. La propagation passe par `core` (phase 1). |
| 5 | R-9 « vérifié avant d'être dit » contre le coût des agents de vérification | Vérification programmatique (`verifier_rendu.py`, 5.3) ; en attendant, la requête du tour (contrôle c). |
| 6 | « Lire `regles-apprises.md` au début » (L26) contre le budget de contexte | Remplacé par le hook de début de session : titres des règles actives et 3 exports en retard. |
| 7 | Règle d'or + exception transferts + R-1 (CM-20, CM-21) | Une seule formulation dans `CLAUDE.md`, implémentée dans `gold.agenda` ; l'exception transferts est un champ de la vue. |
| 8 | Hook `police` bloquant les « mots d'aveu » en discussion de conception | Garder H4 ; chaque faux positif ajoute un cas à `test_police.py`. |
| 9 | « Chaîne complète dès l'arrivée des exports » (L79) contre « agent seulement sur nouveauté » (CM-41.12) et le plafond | La nouveauté et le plafond l'emportent. L79 supprimée. |
| 10 | `rappel_debut.py` et la rétro disent « horizon contrôlé par les hooks », or aucun hook ne le contrôle (`forme.py` ne bloque que « rien à faire ») | L'horizon est une règle E sans code : écrit le 2026-11-03 : `controle.py` f bloque un report dans la cellule Action d'un plan (« demain matin », « plus tard »…) ; un match de demain saisi ce soir reste autorisé. La phrase du rappel est supprimée avec la refonte du hook de début de session. |
| 11 | « Le plafond d'agents justifie la décision remise à plus tard » (L130) contre « décision rendue aujourd'hui » (R-1, CM-21) | La décision est rendue aujourd'hui ; le plafond limite les agents, pas la décision (elle sort de `gold.*` et de `rapport_jour.py`). |
| 12 | SZ « compo de demain » (L140) contre l'horizon « aujourd'hui seulement » (CM-21) | Pas de conflit : la composition d'un match de demain se saisit aujourd'hui, ce qui est autorisé. L140 reste une règle de jeu SZ. |
| 13 | Numérotation en double dans `regles-apprises.md` (13 à 31 existent deux fois) et deux « 5. » dans `attentes.md` §4 | Les règles sont désormais identifiées par leur ligne (`triage.md`) ; la numérotation de §4 sera corrigée avec l'archivage. |
| 14 | Agents « retirés » encore cités (`lecteur-exports`, `verificateur`, `effectif`, `finances`, `optimisation`) dans L116, L117, L87, L93 et `CLAUDE.md` | Les règles qui ne servent qu'à eux sont D ; leur fond est repris par une vue gold (`exports_nouvelles_cles`, `roster_bilan`, `finance_policy`). |
