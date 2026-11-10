"""Test de pipelines/que_faire_blocs.py (étape 5n), sur des données figées, sans réseau ni base.
Lancer : python -I pipelines/test_que_faire_blocs.py   (code 1 si un cas se trompe)
"""
import ast
import importlib.util
import sys
from pathlib import Path

DOSSIER = Path(__file__).resolve().parent
sys.path.insert(0, str(DOSSIER))
import forme  # noqa: E402
import que_faire_blocs as qfb  # noqa: E402

spec = importlib.util.spec_from_file_location("aujourdhui", DOSSIER / "aujourdhui.py")
auj = importlib.util.module_from_spec(spec)
spec.loader.exec_module(auj)

# Cas où classer() peut tomber dans le défaut (10, "Question") : aucun, la liste blanche est vide.
LISTE_BLANCHE: tuple = ()

# Valeurs que prennent les variables placées en tête (ou seules) dans un appel ajoute(), relevées dans aujourdhui.py.
# Une variable absente de cette table fait échouer test_classer_couvre_chaque_ajoute : il faut la décrire ici.
ECHANTILLONS = {
    "titre": ["Ligue J4 contre Naked Spartans", "Ligue J4 à Naked Spartans", "Coupe contre Naked Spartans", "Amical contre Opper Cards"],
    "r['match'] or 'Match'": ["Naked Spartans", "Match"],
    "tete": ["Académie, rapport du 05/11 : Dupont (PG, 17 ans, TSP 40-60)", "Acheter un PG de note ≥ 60"],
    "ent[1]": ["Entraînement (fin du cycle dimanche 04:00) : corrige 2 écarts à l'écran",
               "Entraînement (fin du cycle dimanche 04:00) : il me manque la fiche de l'agent Entraînement",
               "Entraînement (fin du cycle dimanche 04:00) : il me manque l'export Entraînement"],
    "r['action']": ["Avant 07:45 : preset amical sur le match contre Opper Cards (saisir la tactique)",
                    "Avant dimanche 04:00 : vérifier et sauvegarder les choix d'entraînement",
                    "Après l'amical (~08:55) : exporter la page du match",
                    "Avant 19:45 si possible : exporter la page Preview du match de ligue",
                    "Après le match (~20:50) : exporter la page du match J6 (puis l'aperçu suivant)",
                    "Après 04:00 : exporter Entraînement, Finances et Personnel",
                    "Après 09:00 : exporter la page Académie (nouveau rapport du jeudi)",
                    "Avant 19:45 : vérifier le preset de ligue et régler le focus défensif"],
    "r['alert']": ["Dupont blessé, retour le 12/11", "Dupont : fatigue 73 (hors zone verte)",
                   "Dupont : forme 2 (attaque −8 %)", "Semaine type déficitaire : -1200 par semaine",
                   "Match de ligue joué non exporté : J5 du 06/11"],
}


def _manque_exemple(nom, export):
    return auj.manque({}, {}, nom, export)


def textes_des_appels():
    """[(ligne, [textes possibles])] : le premier argument de texte de chaque appel ajoute( de aujourdhui.py."""
    arbre = ast.parse((DOSSIER / "aujourdhui.py").read_text(encoding="utf-8"))
    manques = []
    for n in ast.walk(arbre):
        if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "manque" and len(n.args) == 4 \
                and all(isinstance(a, ast.Constant) for a in n.args[2:]):
            manques.append(_manque_exemple(n.args[2].value, n.args[3].value))
    sortie = []
    for n in ast.walk(arbre):
        if not (isinstance(n, ast.Call) and getattr(n.func, "id", "") == "ajoute" and len(n.args) >= 3):
            continue
        a = n.args[2]
        while isinstance(a, ast.BinOp):  # f"{titre} (…)" + (…) : on classe d'après la tête
            a = a.left
        if isinstance(a, ast.Constant):
            sortie.append((n.lineno, [a.value]))
        elif isinstance(a, ast.JoinedStr):
            premier = a.values[0]
            tetes = ["X"]
            if isinstance(premier, ast.FormattedValue):
                cle = ast.unparse(premier.value)
                tetes = ECHANTILLONS.get(cle, [None])
                reste = a.values[1:]
            else:
                tetes, reste = [""], a.values
            suite = "".join(v.value if isinstance(v, ast.Constant) else "X" for v in reste)
            sortie.append((n.lineno, [None if t is None else t + suite for t in tetes]))
        elif isinstance(a, ast.Call) and getattr(a.func, "id", "") == "manque":
            sortie.append((n.lineno, [_manque_exemple(a.args[2].value, a.args[3].value)]))
        else:
            cle = ast.unparse(a)
            if cle == "m":
                sortie.append((n.lineno, manques))
            else:
                sortie.append((n.lineno, ECHANTILLONS.get(cle, [None])))
    return sortie


def cas():
    yield "test_manque_format", qfb.manque("l'aperçu du match de ligue du 11/11") == "donnée manquante : exporte l'aperçu du match de ligue du 11/11"
    yield "test_manque_avec_deblocage", qfb.manque("Marché", "bloc 4") == "donnée manquante : exporte Marché (bloc 4)"

    for texte in ("lance l'agent tactique", "relance l'agent analyste", "puis python -I pipelines/sql.py", "exécute le script",
                  "voir pipelines/aujourdhui.py", "Python"):
        yield f"test_interdits_attrape : {texte}", qfb.INTERDITS.search(texte) is not None
    for texte in ("lancer l'agent", "relancer le script", "exécuter la requête", "pour relancer"):
        yield f"test_interdits_attrape_les_infinitifs : {texte}", qfb.INTERDITS.search(texte) is not None
    for texte in ("défaite du 09/11 : analyse non faite, lancée dans ce passage", "étude à jour au 09/11", "exporté hier",
                  "le lancement de la saison", "les lanceurs"):
        yield f"test_interdits_laisse_passer : {texte}", qfb.INTERDITS.search(texte) is None

    appels = textes_des_appels()
    yield "test_classer_couvre_chaque_ajoute : au moins 30 appels relevés", len(appels) >= 30
    for ligne, textes in appels:
        for t in textes:
            if t is None:
                yield f"test_classer_couvre_chaque_ajoute : ligne {ligne} : variable non décrite dans ECHANTILLONS", False
                continue
            bloc, cat = qfb.classer(t)
            ok = (bloc, cat) != (10, "Question") or t in LISTE_BLANCHE
            yield f"test_classer_couvre_chaque_ajoute : ligne {ligne} : {t[:60]} -> {bloc} {cat}", ok and 0 <= bloc <= 10

    attendus = {
        "Composition J4 contre Naked Spartans : lance l'agent tactique (aperçu du 09/11 en base)": (3, "Composition"),
        "Composition : minutes aux jeunes, amical contre X (lundi)": (2, "Composition"),
        "Réexporte l'aperçu : l'effectif adverse a pu changer": (0, "Export"),
        "Analyse : lance l'agent analyste ce soir": (7, "Analyse"),
        "Finances : solde projeté au 30/11 de 100 000": (8, "Finances"),
        "Vendre Dupont : économie 5 000 par semaine": (4, "Transferts"),
        "Enchère maximale 100 000 sur Dupont (PG, PS 60)": (4, "Transferts"),
        "Académie, rapport du 05/11 : 2 prospects ; cote inconnue": (9, "Académie/Draft"),
        "Entraînement (fin du cycle dimanche 04:00) : corrige 2 écarts à l'écran": (9, "Entraînement"),
        "Amical contre Opper Cards (lundi) : saisis la tactique maintenant": (2, "Composition"),
        "Ligue J4 contre Naked Spartans (lundi) : saisis la tactique maintenant": (3, "Composition"),
        "il me manque gold.bv_finance_health (illisible) — export Finances": (8, "Finances"),
        "il me manque gold.bv_market_bargains (illisible) — export Marché (enchères)": (4, "Transferts"),
        "il me manque alertes_match (illisible) — export page du dernier match": (7, "Analyse"),
        "Après 04:00 : exporter Entraînement, Finances et Personnel": (0, "Export"),
    }
    for texte, attendu in attendus.items():
        yield f"test_classer_attendu : {texte[:60]}", qfb.classer(texte) == attendu
    yield "test_classer_inconnu_va_en_question", qfb.classer("Un texte que personne ne connaît") == (10, "Question")
    yield "test_classer_categories_de_forme", all(
        forme.norm(qfb.classer(t)[1]) in forme.CATEGORIES for t in attendus)

    # séparer : les consignes destinées à Claude sortent de l'affichage
    prop = (None, 1, "Composition J4 contre X : lance l'agent tactique (aperçu du 09/11 en base)", "", "src")
    rel = (None, 1, "Composition J4 contre X : composition adverse changée : relance l'agent tactique", "entrés : A", "src")
    cmd = (None, 2, "Entraînement : corrige 2 écarts", "relance l'agent entraînement", "src")
    py = (None, 3, "Revue", "python -I pipelines/revue_hebdo.py", "src")
    nette = (None, 2, "Vendre Dupont : économie 5 000 par semaine", "remplaçant Martin", "src")
    aff, sess = qfb.separer([prop, rel, cmd, py, nette])
    yield "test_separer_met_les_consignes_en_session : actions à consigne retirées", nette in aff and prop not in aff and rel not in aff
    yield "test_separer_met_les_consignes_en_session : 4 consignes", len(sess) == 4 and all(isinstance(s, str) for s in sess)
    yield "test_separer_garde_l_action_sans_la_commande_du_detail", any(a[2] == cmd[2] and a[3] == "" for a in aff) and "relance l'agent entraînement" in sess
    yield "test_separer_aucune_commande_dans_l_affichage", all(not qfb.INTERDITS.search(a[2] + " " + a[3]) for a in aff)
    yield "test_separer_liste_vide", qfb.separer([]) == ([], [])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    echecs = 0
    jeux = list(cas())
    for nom, ok in jeux:
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    print(f"{len(jeux) - echecs}/{len(jeux)}")
    sys.exit(1 if echecs else 0)
