"""Test de pipelines/que_faire_blocs.py (étape 5n), sur des données figées, sans réseau ni base.
Lancer : python -I pipelines/test_que_faire_blocs.py   (code 1 si un cas se trompe)
"""
import ast
import datetime as dt
import importlib.util
import os
import re
import sys
import tempfile
from pathlib import Path
from zoneinfo import ZoneInfo

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
    yield from cas_bloc_1()
    yield from cas_blocs_2_3()


J = dt.date(2026, 11, 10)
# une action par bloc que classer() peut produire (les blocs 5 et 6 n'ont aucune action dans plan() : leurs lignes viennent de bloc_5 et bloc_6)
PAR_BLOC = {
    0: "Réexporte l'aperçu : l'effectif adverse a pu changer",
    2: "Amical contre Opper Cards (mardi) : saisis la tactique maintenant",
    3: "Ligue J5 contre Naked Spartans (mercredi) : saisis la tactique maintenant",
    4: "Vendre Dupont : économie 5 000 par semaine",
    7: "Analyse : défaite du 09/11",
    8: "Finances : solde projeté au 30/11 de 100 000",
    9: "Académie, rapport du 05/11 : 2 prospects ; cote inconnue",
    10: "Un texte que personne ne connaît",
}


def cas_bloc_1():
    auj_ = (dt.datetime(2026, 11, 10, 19, 45), 1, "Ligue J4 contre Naked Spartans (mardi) : saisis la tactique maintenant", "", "s")
    dem = (dt.datetime(2026, 11, 11, 19, 45), 2, "Ligue J5 contre Brest (mercredi) : saisis la tactique maintenant", "", "s")
    t = "\n".join(qfb.bloc_1([auj_, dem], J))
    yield "test_bloc_1_deux_sections : titres", "Aujourd'hui" in t and "Demain (préparé aujourd'hui)" in t
    i_dem = t.index("Demain (préparé aujourd'hui)")
    yield "test_bloc_1_deux_sections : J en Aujourd'hui, J+1 en Demain", t.index("Naked Spartans") < i_dem < t.index("Brest")
    yield "test_bloc_1_pastilles", "🟥 URGENT" in t and "🟧 IMPORTANT" in t

    toutes = [(None, 2, texte, "", "s") for texte in PAR_BLOC.values()]
    lignes = qfb.bloc_1(toutes, J)
    for n, texte in PAR_BLOC.items():
        cherche = [l for l in lignes if texte[:25] in l]
        yield f"test_bloc_1_liste_toutes_les_actions : bloc {n}", len(cherche) == 1 and f"→ bloc {n}" in cherche[0]

    vide = qfb.bloc_1([], J)
    tv = "\n".join(vide)
    yield "test_bloc_1_jamais_vide", "🟩 SUIVI" in tv and "→ bloc 0" in tv and "tout est traité" in tv
    yield "test_bloc_1_vide_passe_forme", forme.fautes_tableaux(tv, "basketvibe") == []

    horaires = [(dt.datetime(2026, 11, 10, 19, 45), 1, "Avant 19:45 : vérifier le preset de ligue et régler le focus", "", "s"),
                (None, 2, "Avant 07:45 : preset amical sur le match contre Opper Cards", "", "s"),
                (None, 2, "Après l'amical (~08:55) : exporter la page du match", "", "s"),
                (None, 3, "Avant dimanche 04:00 : vérifier et sauvegarder les choix d'entraînement", "", "s")]
    th = "\n".join(qfb.bloc_1(horaires, J))
    yield "test_bloc_1_sans_heure", re.search(r"\d\d:\d\d", th) is None and "preset amical" in th and "exporter la page du match" in th
    yield "test_bloc_1_passe_forme", forme.fautes_tableaux(t + "\n" + "\n".join(lignes) + "\n" + th, "basketvibe") == []

    seul = "\n".join(qfb.bloc_1([auj_], J))
    yield "test_bloc_1_section_vide_omise", "Demain" not in seul and "rien" not in seul.lower() and "Naked Spartans" in seul

    avec_consigne = [(None, 1, "Composition J4 contre X : lance l'agent tactique (aperçu du 09/11 en base)", "", "s"),
                     (None, 2, "Vendre Dupont : économie 5 000 par semaine", "", "s")]
    tc = "\n".join(qfb.bloc_1(avec_consigne, J))
    yield "test_bloc_1_sans_commande", qfb.INTERDITS.search(tc) is None and "Vendre Dupont" in tc
    barre = "\n".join(qfb.bloc_1([(None, 2, "Vendre A | B : économie", "", "s")], J))
    yield "test_bloc_1_barre_verticale_neutralisee", forme.fautes_tableaux(barre, "basketvibe") == [] and len([l for l in barre.splitlines() if "Vendre" in l][0].split("|")) == 5


# ---- 5n T3 : blocs 2 et 3 --------------------------------------------------------------------------------------
JOUR_T = dt.date(2026, 11, 10)
MAINT = dt.datetime(2026, 11, 10, 14, 39)
PARIS = ZoneInfo("Europe/Paris")
EN_TETE = "| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Min | Off. focus | Rôle | Tir | Agress. |\n|---|---|---|---|---|---|---|---|---|---|---|---|\n"
JOUEURS = (EN_TETE + "| Richard | PG | PG | PG | PG | PG | — | 36 | 1 | 1 | 3 | 1 |\n| Bonnet | SG | SG | SG | — | — | — | 24 | 5 | 5 | 5 | 1 |\n"
           "| Gimenez | SF | SF | — | SF | SF | SF | 36 | 4 | 3 | 3 | 1 |\n| Albano | PF | — | PF | PF | — | — | 24 | 3 | 3 | 3 | 1 |\n"
           "| Fournier | C | C | — | — | — | — | 12 | 2 | 2 | 1 | 1 |\n")
ANTICIP = ("\nAnticipation (hypothèse) : Gimenez porte 31 % des tirs à 3 points ; si le focus 5 tombe sur lui, plan B : Bonnet tireur principal.\n")


def brief_amical(adv="Opper Cards", anticipation=True):
    return (f"# Tactique AMICAL mer. 11/11 08:00 (verrou 07:45), DOMICILE contre {adv}\n\n## 2. Consignes\n" + JOUEURS
            + "\n## 3. Adversaires\n| Adversaire | Poste | Focus (1-5) | Zone |\n|---|---|---|---|\n| Roze | PG | 3 Normal | Perimeter (1) |\n"
            + (ANTICIP if anticipation else ""))


def brief_ligue(adv="Naked Spartans", anticipation=True):
    return (f"# Tactique ligue J5 : {adv} (domicile, mer. 11/11 20:00, verrou 19:45)\n\n## 1. Fiche\n" + JOUEURS
            + "\n## 2. Adversaires\n| Adversaire | Poste | Focus (1-5) | Zone |\n|---|---|---|---|\n| Zwoliński | PF | 4 Intense | Middle (3) |\n"
            + (ANTICIP if anticipation else ""))


def dossier(*fichiers):
    """Dossier de briefs temporaire ; chaque fichier = (nom, texte, heure de production à Paris | None)."""
    d = Path(tempfile.mkdtemp())
    (d / "briefs").mkdir()
    for nom, texte, quand in fichiers:
        f = d / "briefs" / nom
        f.write_text(texte, encoding="utf-8")
        if quand:
            ts = quand.replace(tzinfo=PARIS).timestamp()
            os.utime(f, (ts, ts))
    return d


def T(cols, rows):
    return (cols, rows)


CAL = ["day", "competition_kind", "opponent", "coup_envoi_paris", "verrou_paris"]
AM_11 = ("2026-11-11", "amical", "Opper Cards", "2026-11-11T08:00:00", "2026-11-11T07:45:00")
LG_11 = ("2026-11-11", "ligue", "Naked Spartans", "2026-11-11T20:00:00", "2026-11-11T19:45:00")
APERCU_COLS = ["fixture_id", "competition_kind", "round_no", "day", "opponent", "capture_paris", "adverse"]


def donnees_t(calendrier=(AM_11, LG_11), capture="2026-11-10T09:00:00", **plus):
    d = {"calendrier": T(CAL, list(calendrier)),
         "amical_reglage": T(["fixture_id", "match_day", "opponent", "agress_cran", "primary_quarts", "tir_cran4_joueurs"], []),
         "apercus_matchs": T(APERCU_COLS, [(7, "ligue", 5, "2026-11-11", "Naked Spartans", capture, "Zwolinski,Buczek")]),
         "gold.bv_exports_state": T(["ordre", "ecran", "pour_quoi", "dernier_paris", "age_h", "statut"],
                                    [(1, "Équipe (aperçu, joueurs)", "x", "2026-11-10T08:00:00", 6, "🟩 à jour")]),
         "gold.bv_daily_alerts": T(["priority", "category", "alert"], []),
         "fatigue_avant_match": T(["kind", "match_day", "opponent", "joueur", "minutes", "defense_tier", "sat_fatigue", "zone_verte"], []),
         "transferts_recents": T(["name", "settled_at", "to_team", "achete"], []),
         "fatigue_amical": T(["match_day", "joueur", "minutes_am", "agress", "stamina", "fatigue_ajoutee"],
                             [("2026-11-11", "Gimenez", 36, 1, 53, 0.5), ("2026-11-11", "Bonnet", 24, 1, 52, 0.4)])}
    d.update(plus)
    return d


def cas_blocs_2_3():
    S = {"experiences": None}
    sans_test = lambda *a, **k: None  # noqa: E731
    yield "test_requete_fatigue_amical_existe", "fatigue_amical" in auj.REQUETES and "0.019" in auj.REQUETES["fatigue_amical"]

    # --- bloc 2
    l, c = qfb.bloc_2(donnees_t(calendrier=(LG_11,)), S, JOUR_T, MAINT, base=dossier())
    yield "test_aucun_amical", l == ["aucun amical programmé aujourd'hui ni demain"] and c == []

    b_jour = dossier(("2026-11-10-tactique-amical.md", brief_amical(), None))
    l, c = qfb.bloc_2(donnees_t(), S, JOUR_T, MAINT, base=b_jour)
    t2 = "\n".join(l)
    yield "test_amical_rend_le_brief_du_jour", "| Gimenez |" in t2 and "Agress." in t2 and c == [] and "préparation" not in t2
    yield "test_amical_verrou_et_heure_limite", "07:45" in t2
    yield "test_amical_jamais_pas_de_blessure", "pas de blessure" not in t2.lower() and "sans blessure" not in t2.lower()
    yield "test_anticipation_affichee_avec_brief_du_jour : bloc 2", "Anticipation (hypothèse) :" in t2 and "plan B" in t2
    yield "test_amical_fatigue_ajoutee_jour_de_ligue : jour de ligue", "fatigue ajoutée" in t2.lower() and "Gimenez" in t2.lower().replace("gimenez", "Gimenez")
    l_autre, _ = qfb.bloc_2(donnees_t(calendrier=(AM_11, ("2026-11-12", "ligue", "Naked Spartans", "2026-11-12T20:00:00", "2026-11-12T19:45:00"))),
                            S, JOUR_T, MAINT, base=b_jour)
    yield "test_amical_fatigue_ajoutee_jour_de_ligue : hors jour de ligue", "fatigue ajoutée" not in "\n".join(l_autre).lower()
    yield "test_blocs_2_3_passent_forme : bloc 2", forme.fautes_tableaux(t2, "basketvibe") == [] and forme.fautes_de(t2, "basketvibe") == []
    yield "test_bloc_2_sans_commande", qfb.INTERDITS.search(t2) is None

    # test en cours nommé
    E1 = {"id": "E1", "niveaux": {"A": "agressivité 3", "B": "agressivité 5"}, "joue": {"A": {"agress_cran": 2}, "B": {"agress_cran": 4}}}
    reel = qfb.auj.test_en_cours
    qfb.auj.test_en_cours = lambda *a, **k: (E1, "B", False)
    try:
        lt, _ = qfb.bloc_2(donnees_t(), S, JOUR_T, MAINT, base=b_jour)
    finally:
        qfb.auj.test_en_cours = reel
    tt = "\n".join(lt)
    yield "test_amical_reglage_teste_nomme", "test E1 niveau B : agressivité 5" in tt and "{'5'}" not in tt \
        and {x[11] for x in composition_lignes(tt)} == {"5"}

    # brief d'hier seulement : jamais repris
    b_hier = dossier(("2026-11-09-tactique-amical.md", brief_amical(), None))
    l, c = qfb.bloc_2(donnees_t(), S, JOUR_T, MAINT, base=b_hier)
    t = "\n".join(l)
    yield "test_amical_jamais_le_dernier_amical", "| Gimenez |" not in t and "composition de l'amical en préparation" in t and len(c) == 1 \
        and "lancer l'agent tactique" in c[0] and qfb.INTERDITS.search(t) is None
    yield "test_amical_jamais_pas_de_blessure : en préparation", "pas de blessure" not in t.lower() and "sans blessure" not in t.lower()
    for mot in ("21 ans", "un seul réglage", "titulaires protégés", "minutes réparties", "jamais reprise du dernier amical"):
        yield f"test_amical_consigne_cite_la_regle : {mot}", mot in c[0]
    yield "test_anticipation_dans_les_consignes : bloc 2", "décisions de l'adversaire" in c[0] and "hypothèse" in c[0]
    yield "test_anticipation_dans_les_consignes : constante", "décisions de l'adversaire" in qfb.ANTICIPATION and "hypothèse" in qfb.ANTICIPATION

    # brief du jour sans ligne d'anticipation : signalé, consigne pour la compléter
    b_sans = dossier(("2026-11-10-tactique-amical.md", brief_amical(anticipation=False), None))
    l, c = qfb.bloc_2(donnees_t(), S, JOUR_T, MAINT, base=b_sans)
    yield "test_anticipation_absente_du_brief_signalee", "Anticipation (hypothèse) : absente du brief" in "\n".join(l) and len(c) == 1 \
        and "décisions de l'adversaire" in c[0]

    # --- bloc 3
    l, c = qfb.bloc_3(donnees_t(capture=None), S, JOUR_T, MAINT, base=dossier())
    t = "\n".join(l)
    yield "test_ligue_apercu_absent", "donnée manquante : exporte l'aperçu du match de ligue du 11/11" in t and qfb.INTERDITS.search(t) is None and c == []

    l, c = qfb.bloc_3(donnees_t(), S, JOUR_T, MAINT, base=dossier())
    t = "\n".join(l)
    yield "test_ligue_apercu_sans_fiche_met_la_consigne_en_session", len(c) == 1 and "lancer l'agent tactique" in c[0] and "composition en préparation" in t \
        and qfb.INTERDITS.search(t) is None
    yield "test_anticipation_dans_les_consignes : bloc 3", "décisions de l'adversaire" in c[0] and "hypothèse" in c[0]

    b_hier = dossier(("2026-11-09-tactique.md", brief_ligue(), datetime_paris(2026, 11, 9, 20)))
    l, c = qfb.bloc_3(donnees_t(), S, JOUR_T, MAINT, base=b_hier)
    t = "\n".join(l)
    yield "test_ligue_fiche_d_hier_pas_a_jour", "| Gimenez |" not in t and len(c) == 1 and "composition en préparation" in t

    avant = dossier(("2026-11-10-tactique.md", brief_ligue(), datetime_paris(2026, 11, 10, 8, 30)))  # avant l'aperçu de 09:00
    l, c = qfb.bloc_3(donnees_t(), S, JOUR_T, MAINT, base=avant)
    yield "test_ligue_fiche_du_jour_produite_avant_l_apercu_pas_a_jour", "| Gimenez |" not in "\n".join(l) and len(c) == 1

    avant_equipe = dossier(("2026-11-10-tactique.md", brief_ligue(), datetime_paris(2026, 11, 10, 9, 30)))  # après l'aperçu, avant l'export Équipe de 10:00
    d_eq = donnees_t(**{"gold.bv_exports_state": T(["ordre", "ecran", "pour_quoi", "dernier_paris", "age_h", "statut"],
                                                   [(1, "Équipe (aperçu, joueurs)", "x", "2026-11-10T10:00:00", 4, "🟩 à jour")])})
    l, c = qfb.bloc_3(d_eq, S, JOUR_T, MAINT, base=avant_equipe)
    yield "test_ligue_fiche_produite_avant_le_dernier_export_equipe_pas_a_jour", "| Gimenez |" not in "\n".join(l) and len(c) == 1

    a_jour = dossier(("2026-11-10-tactique.md", brief_ligue(), datetime_paris(2026, 11, 10, 11)))
    l, c = qfb.bloc_3(donnees_t(), S, JOUR_T, MAINT, base=a_jour)
    t3 = "\n".join(l)
    yield "test_ligue_fiche_a_jour : tableaux et pas de consigne", "| Gimenez |" in t3 and "Zwoliński" in t3 and c == []
    yield "test_anticipation_affichee_avec_brief_du_jour : bloc 3", "Anticipation (hypothèse) :" in t3 and "plan B" in t3
    yield "test_blocs_2_3_passent_forme : bloc 3", forme.fautes_tableaux(t3, "basketvibe") == [] and forme.fautes_de(t3, "basketvibe") == []
    yield "test_bloc_3_sans_commande", qfb.INTERDITS.search(t3) is None

    l, c = qfb.bloc_3(donnees_t(apercus_matchs=T(APERCU_COLS, []), calendrier=(AM_11,)), S, JOUR_T, MAINT, base=dossier())
    yield "test_bloc_3_aucun_match", "aucun match de ligue ou de coupe dans les trois prochains jours" in "\n".join(l) and c == []

    # --- vérification J-1, blocs 2 et 3
    alertes = T(["priority", "category", "alert"], [(1, "blessure", "Marc Gimenez blessé, retour le 12/11"),
                                                  (2, "fatigue", "Paul Bonnet : fatigue 73 (hors zone verte)"),
                                                  (2, "forme", "Zoé Inconnue : forme 1 (attaque −11 %)")])
    ftg = T(["kind", "match_day", "opponent", "joueur", "minutes", "defense_tier", "sat_fatigue", "zone_verte"],
            [("ligue", "2026-11-11", "Naked Spartans", "Albano", 24, 2, 31.0, 20)])
    vendus = T(["name", "settled_at", "to_team", "achete"], [("Luc Richard", "2026-11-09T12:00:00", "Autre club", False),
                                                           ("Marc Fournier", "2026-11-09T13:00:00", "Mon club", True)])
    dj = donnees_t(**{"gold.bv_daily_alerts": alertes, "fatigue_avant_match": ftg, "transferts_recents": vendus})
    for nom, fonction, base_ in (("bloc 2", qfb.bloc_2, b_jour), ("bloc 3", qfb.bloc_3, a_jour)):
        l, _ = fonction(dj, S, JOUR_T, MAINT, base=base_)
        ecarts = [x for x in l if x.startswith("Écart J-1")]
        for joueur, motif in (("Gimenez", "blessé"), ("Bonnet", "fatigue"), ("Albano", "fatigue"), ("Richard", "vendu")):
            trouve = [x for x in ecarts if joueur in x]
            yield f"test_j_moins_1_signale_blesse_fatigue_vendu : {nom} : {joueur}", len(trouve) == 1 and motif in trouve[0]
        yield f"test_j_moins_1 : {nom} : ni Fournier acheté ni joueur absent du tableau", not any("Fournier" in x or "Inconnue" in x for x in ecarts)
        yield f"test_j_moins_1 : {nom} : écarts passent forme", forme.fautes_de("\n".join(l), "basketvibe") == []
    yield "test_j_moins_1_aucun_ecart", qfb.verifier_j_moins_1(JOUEURS, donnees_t()) == []
    yield "test_j_moins_1_forme_basse", any("Gimenez" in x for x in qfb.verifier_j_moins_1(JOUEURS, donnees_t(**{"gold.bv_daily_alerts": T(
        ["priority", "category", "alert"], [(2, "forme", "Marc Gimenez : forme 2 (attaque −8 %)")])})))


def composition_lignes(texte):
    for cols, lignes in forme.tableaux(texte):
        if cols and cols[0] == "joueur":
            return lignes
    return []


def datetime_paris(a, m, j, h=0, mi=0):
    return dt.datetime(a, m, j, h, mi)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    echecs = 0
    jeux = list(cas())
    for nom, ok in jeux:
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    print(f"{len(jeux) - echecs}/{len(jeux)}")
    sys.exit(1 if echecs else 0)
