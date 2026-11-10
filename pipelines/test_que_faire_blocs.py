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
    yield from cas_contrat_brief()
    yield from cas_produit_le()
    yield from cas_bloc_4()
    yield from cas_t5()
    yield from cas_t6()
    yield from cas_a1()
    yield from cas_r3()
    yield from cas_a2()
    yield from cas_a6()


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


ADVERSAIRES = "\n## Adversaires\n| Adversaire | Poste | Focus (1-5) | Zone |\n|---|---|---|---|\n| Roze | PG | 3 Normal | Perimeter (1) |\n"


def brief_depuis_la_consigne(consigne):
    """Fabrique un brief en ne suivant que le texte de la consigne : nom de fichier, première ligne exacte, tableau de saisie,
    puis une ligne qui commence par la formule exacte donnée par la consigne. Renvoie (nom du fichier, texte)."""
    nom = re.search(r"outputs/basketvibe/briefs/(\S+?\.md)", consigne)
    ligne = re.search(r"première ligne exactement « ([^»]+) »", consigne)
    debut = re.search(r"commençant exactement par « (Anticipation \(hypothèse\) :) »", consigne)
    if not (nom and ligne and debut):
        return None, None
    texte = (ligne.group(1) + "\n\n## Saisie\n" + JOUEURS + ADVERSAIRES
             + "\n" + debut.group(1) + " Gimenez porte 31 % des tirs à 3 points ; si le focus 5 tombe sur lui, plan B : Bonnet tireur principal.\n")
    return nom.group(1), texte


def cas_contrat_brief():
    S = {"experiences": None}
    # --- consignes : nom de fichier, première ligne, formule de l'anticipation (amical)
    _, c = qfb.bloc_2(donnees_t(), S, JOUR_T, MAINT, base=dossier())
    yield "test_contrat_brief : bloc 2 lancement : nom du fichier amical", "outputs/basketvibe/briefs/2026-11-10-tactique-amical.md" in c[0]
    yield "test_contrat_brief : bloc 2 lancement : première ligne exacte", "première ligne exactement « Amical contre Opper Cards (11/11) »" in c[0]
    yield "test_contrat_brief : bloc 2 lancement : formule de l'anticipation", "« Anticipation (hypothèse) : »" in c[0] and "plan B" in c[0]
    yield "test_contrat_brief : bloc 2 lancement : tableau de saisie", "tableau de saisie" in c[0]
    yield "test_contrat_brief : constante ANTICIPATION", "« Anticipation (hypothèse) : »" in qfb.ANTICIPATION and "plan B" in qfb.ANTICIPATION
    # relance quand la ligne d'anticipation manque : même contrat
    b_sans = dossier(("2026-11-10-tactique-amical.md", brief_amical(anticipation=False), None))
    _, c_rel = qfb.bloc_2(donnees_t(), S, JOUR_T, MAINT, base=b_sans)
    yield "test_contrat_brief : bloc 2 relance : nom du fichier et formule", len(c_rel) == 1 \
        and "outputs/basketvibe/briefs/2026-11-10-tactique-amical.md" in c_rel[0] and "« Anticipation (hypothèse) : »" in c_rel[0]

    # --- bloc 2 de bout en bout : un brief fabriqué à partir du texte de la consigne est lu par brief_du_jour, composer_amical, anticipation_du_brief
    nom, texte = brief_depuis_la_consigne(c[0])
    yield "test_contrat_brief : bloc 2 : la consigne se laisse lire", nom == "2026-11-10-tactique-amical.md" and texte is not None
    base = dossier((nom, texte, None)) if nom else dossier()
    f = qfb.brief_du_jour(base, JOUR_T, True, "Opper Cards")
    yield "test_contrat_brief : bloc 2 : brief_du_jour le trouve", f is not None and f.name == nom
    yield "test_contrat_brief : bloc 2 : adversaire_du_titre lit la première ligne", qfb.comp.adversaire_du_titre((texte or "\n").splitlines()[0]) == "Opper Cards"
    tab = qfb.comp.composer_amical(f, None) if f else None
    yield "test_contrat_brief : bloc 2 : composer_amical rend le tableau", tab is not None and "| Gimenez |" in tab
    ant = qfb.anticipation_du_brief(f) if f else qfb.ABSENTE
    yield "test_contrat_brief : bloc 2 : anticipation_du_brief la lit", ant != qfb.ABSENTE and ant.startswith("Anticipation (hypothèse) : ") and "plan B" in ant
    l, c2 = qfb.bloc_2(donnees_t(), S, JOUR_T, MAINT, base=base)
    t = "\n".join(l)
    yield "test_contrat_brief : bloc 2 : le bloc rend le brief, sans nouvelle consigne", "| Gimenez |" in t and "plan B" in t and c2 == []

    # --- bloc 3, ligue de bout en bout (J<n> : <adversaire> (JJ/MM))
    _, c3 = qfb.bloc_3(donnees_t(), S, JOUR_T, MAINT, base=dossier())
    yield "test_contrat_brief : bloc 3 lancement : nom du fichier ligue", "outputs/basketvibe/briefs/2026-11-10-tactique.md" in c3[0] \
        and "tactique-amical" not in c3[0]
    yield "test_contrat_brief : bloc 3 lancement : première ligne exacte", "première ligne exactement « J5 : Naked Spartans (11/11) »" in c3[0]
    yield "test_contrat_brief : bloc 3 lancement : formule de l'anticipation", "« Anticipation (hypothèse) : »" in c3[0] and "plan B" in c3[0]
    nom3, texte3 = brief_depuis_la_consigne(c3[0])
    yield "test_contrat_brief : bloc 3 : la consigne se laisse lire", nom3 == "2026-11-10-tactique.md" and texte3 is not None
    base3 = dossier((nom3, texte3, datetime_paris(2026, 11, 10, 11))) if nom3 else dossier()
    f3 = qfb.brief_du_jour(base3, JOUR_T, False, "Naked Spartans")
    yield "test_contrat_brief : bloc 3 : brief_du_jour le trouve", f3 is not None and f3.name == nom3
    yield "test_contrat_brief : bloc 3 : adversaire_du_titre lit la première ligne", qfb.comp.adversaire_du_titre((texte3 or "\n").splitlines()[0]) == "Naked Spartans"
    ant3 = qfb.anticipation_du_brief(f3) if f3 else qfb.ABSENTE
    yield "test_contrat_brief : bloc 3 : anticipation_du_brief la lit", ant3 != qfb.ABSENTE and ant3.startswith("Anticipation (hypothèse) : ")
    l3, c33 = qfb.bloc_3(donnees_t(), S, JOUR_T, MAINT, base=base3)
    t3 = "\n".join(l3)
    yield "test_contrat_brief : bloc 3 : le bloc rend le brief, sans nouvelle consigne", "| Gimenez |" in t3 and "plan B" in t3 and c33 == []

    # --- coupe sans numéro de manche : « Coupe contre <adversaire> (JJ/MM) », lue par adversaire_du_titre
    coupe = donnees_t(apercus_matchs=T(APERCU_COLS, [(8, "coupe", None, "2026-11-11", "Naked Spartans", "2026-11-10T09:00:00", "Zwolinski")]))
    _, cc = qfb.bloc_3(coupe, S, JOUR_T, MAINT, base=dossier())
    yield "test_contrat_brief : coupe : première ligne exacte", len(cc) == 1 and "première ligne exactement « Coupe contre Naked Spartans (11/11) »" in cc[0] \
        and "outputs/basketvibe/briefs/2026-11-10-tactique.md" in cc[0]
    nomc, textec = brief_depuis_la_consigne(cc[0])
    basec = dossier((nomc, textec, datetime_paris(2026, 11, 10, 11))) if nomc else dossier()
    fc = qfb.brief_du_jour(basec, JOUR_T, False, "Naked Spartans")
    yield "test_contrat_brief : coupe : brief_du_jour le trouve", fc is not None
    lc, c_c = qfb.bloc_3(coupe, S, JOUR_T, MAINT, base=basec)
    yield "test_contrat_brief : coupe : le bloc rend le brief", "| Gimenez |" in "\n".join(lc) and c_c == []

    # --- relance du bloc 3 (ligne d'anticipation absente) : même contrat
    b3_sans = dossier(("2026-11-10-tactique.md", brief_ligue(anticipation=False), datetime_paris(2026, 11, 10, 11)))
    _, c3r = qfb.bloc_3(donnees_t(), S, JOUR_T, MAINT, base=b3_sans)
    yield "test_contrat_brief : bloc 3 relance : nom du fichier et formule", len(c3r) == 1 \
        and "outputs/basketvibe/briefs/2026-11-10-tactique.md" in c3r[0] and "« Anticipation (hypothèse) : »" in c3r[0]


def cas_produit_le():
    """C2 : produit_le = heure de commit du brief (git log -1 --format=%ct), mtime seulement si le fichier n'est pas suivi."""
    import subprocess
    d = Path(tempfile.mkdtemp())
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t",
               GIT_COMMITTER_DATE="2026-11-09T20:00:00+01:00", GIT_AUTHOR_DATE="2026-11-09T20:00:00+01:00")

    def git(*a):
        return subprocess.run(["git", "-C", str(d), *a], env=env, capture_output=True, text=True)
    git("init", "-q")
    git("config", "commit.gpgsign", "false")
    (d / "briefs").mkdir()
    suivi = d / "briefs" / "2026-11-10-tactique.md"
    suivi.write_text(brief_ligue(), encoding="utf-8")
    git("add", "briefs/2026-11-10-tactique.md")
    ok = git("commit", "-q", "-m", "brief").returncode == 0
    yield "test_produit_le : le commit de test est créé", ok
    maintenant = dt.datetime.now().timestamp()
    os.utime(suivi, (maintenant, maintenant))  # mtime récent, commit ancien
    yield "test_produit_le : fichier suivi = heure du commit (20:00 Paris le 09/11)", qfb.produit_le(suivi) == dt.datetime(2026, 11, 9, 20, 0)
    yield "test_produit_le : mtime récent mais commit ancien : pas à jour", not qfb.fiche_a_jour(suivi, dt.datetime(2026, 11, 10, 9, 0), None)
    yield "test_produit_le : commit postérieur à l'aperçu : à jour", qfb.fiche_a_jour(suivi, dt.datetime(2026, 11, 9, 19, 0), None)

    # A5 : suivi mais modifié sans commit = mtime (le brief réécrit dans la journée est « produit » à sa dernière écriture)
    suivi.write_text(brief_ligue() + "\nAnticipation (hypothèse) : ajoutée après le commit.\n", encoding="utf-8")
    ts_m = datetime_paris(2026, 11, 10, 11).replace(tzinfo=PARIS).timestamp()
    os.utime(suivi, (ts_m, ts_m))
    yield "test_produit_le : suivi mais modifié sans commit = mtime (11:00 Paris)", qfb.produit_le(suivi) == dt.datetime(2026, 11, 10, 11, 0)
    yield "test_produit_le : suivi modifié sans commit, mtime après l'aperçu : à jour", qfb.fiche_a_jour(suivi, dt.datetime(2026, 11, 10, 9, 0), None)
    git("add", "briefs/2026-11-10-tactique.md")
    yield "test_produit_le : suivi, modification indexée mais non commitée = mtime", qfb.produit_le(suivi) == dt.datetime(2026, 11, 10, 11, 0)
    git("commit", "-q", "-m", "brief réécrit")
    yield "test_produit_le : modification commitée = heure du nouveau commit", qfb.produit_le(suivi) == dt.datetime(2026, 11, 9, 20, 0)

    libre = d / "briefs" / "2026-11-10-tactique-amical.md"
    libre.write_text(brief_amical(), encoding="utf-8")
    ts = datetime_paris(2026, 11, 10, 11).replace(tzinfo=PARIS).timestamp()
    os.utime(libre, (ts, ts))
    yield "test_produit_le : fichier non suivi = mtime (11:00 Paris)", qfb.produit_le(libre) == dt.datetime(2026, 11, 10, 11, 0)
    yield "test_produit_le : fichier non suivi, mtime après l'aperçu : à jour", qfb.fiche_a_jour(libre, dt.datetime(2026, 11, 10, 9, 0), None)

    hors = Path(tempfile.mkdtemp()) / "x.md"  # hors de tout dépôt git
    hors.write_text("x", encoding="utf-8")
    os.utime(hors, (ts, ts))
    yield "test_produit_le : hors dépôt git = mtime", qfb.produit_le(hors) == dt.datetime(2026, 11, 10, 11, 0)


# ---- 5n T4 : bloc 4 -------------------------------------------------------------------------------------------
PRIX_COLS = ["ps_band", "age_band", "n", "p25", "median", "p75", "last_sale"]
PRIX = T(PRIX_COLS, [(45, "22-25", 32, 10187.5, 93888.5, 201249.75, "2026-11-08"), (40, "22-25", 20, 251, 4375.5, 31000.25, "2026-11-07"),
                     (35, "22-25", 2, 1050, 1100, 1150, "2026-11-08"), (45, "≤21", 37, 440000, 721000, 1543500, "2026-11-08")])
ANN_COLS = ["auction_id", "name", "position", "age", "ps", "price_now", "ends_paris", "heures", "gain_vs_my_second", "enters_top8"]
ANN = T(ANN_COLS, [("a1", "Paul Aubert", "PG", 23, 47.0, 50000, "2026-11-11T09:00:00", 5.5, 2.1, True),
                   ("a2", "Luc Brun", "SG", 24, 46.0, 120000, "2026-11-11T10:00:00", 6.5, -1.0, False),
                   ("a3", "Marc Cler", "PF", 22, 36.0, 500, "2026-11-11T11:00:00", 7.5, -3.0, False),
                   ("a4", "Yan Dole", "C", 25, 47.0, 60000, "2026-11-11T12:00:00", 8.5, 0.4, False),
                   ("a5", "Eli Ferrand", "SF", 31, 52.0, 1000, "2026-11-11T13:00:00", 9.5, 1.0, False)])
# « vendre » (gold.bv_sell_candidates) et « gold.bv_sell_replacement » sont lues séparément (en parallèle) et jointes par nom dans le module :
# leur jointure en SQL dépassait le délai (mesuré le 10/11 : chaque vue ~4,7 s, jointure 18 s puis statement timeout).
VENTE = T(["player_id", "name", "position", "age", "ps", "salary", "best_slot", "rank_in_slot", "league_min_last4", "on_transfer_list"],
          [("p1", "Maël Bernard", "C", 18, 47.8, 17303, "PF", 5, 0.0, False), ("p2", "Léo Lefebvre", "PF", 29, 63.1, 31803, "PF", 1, 35.1, False),
           ("p3", "Nolan Baron", "PG", 17, 44.5, 16691, "PG", 7, 0.0, False), ("p4", "Sacha Leclerc", "SG", 17, 42.3, 13767, "SG", 11, 0.0, True),
           ("p5", "Zoé Sansremplaçant", "C", 30, 49.0, 20000, "C", 6, 3.0, False)])
REMPL = T(["player_id", "name", "best_slot", "fit_best", "replacement_name", "replacement_fit", "gap", "weekly_salary", "on_transfer_list", "available",
           "available_players"],
          [("p1", "Maël Bernard", "PF", 47.6, "Anselmo Albano", 47.5, 0.1, 17303, False, True, 14),
           ("p2", "Léo Lefebvre", "PF", 62.8, "Hadrien Gimenez", 58.6, 4.2, 31803, False, True, 14),
           ("p3", "Nolan Baron", "PG", 44.2, "Jonathan Durand", 43.9, 0.3, 16691, False, True, 9),
           ("p4", "Sacha Leclerc", "SG", 42.2, "Nolan Baron", 40.9, 0.2, 13767, True, True, 14)])
JOUR_J = dt.date(2026, 11, 10)


def donnees_4(**plus):
    d = {"prix_cases": PRIX, "annonces_24h": ANN, "vendre": VENTE, "gold.bv_sell_replacement": REMPL,
         "annonces_export": T(["n"], [(20,)]),
         "gold.bv_exports_state": T(["ordre", "ecran", "pour_quoi", "dernier_paris", "age_h", "statut"],
                                    [(3, "Marché (enchères)", "x", "2026-11-10T10:13:00", 5, "🟩 à jour")])}
    d.update(plus)
    return d


def ligne_de(lignes, nom):
    return next((l for l in lignes if l.startswith("|") and nom in l), "")


def cas_bloc_4():
    t = "\n".join(qfb.bloc_4(donnees_4(), {}, 300000, 1.0))
    # table des prix : une ligne par case
    cases = [l for l in t.splitlines() if re.match(r"\| (≤21|22-25|26-29|30\+) \| \d\d ", l)]
    yield "test_table_prix_une_ligne_par_case", len(cases) == 4
    yield "test_table_prix_colonnes", all(x in t for x in ("Prix bas", "Médian", "Prix haut", "Dernière vente", "93 888", "08/11"))
    yield "test_requetes_bloc_4_existent", all(k in auj.REQUETES for k in ("prix_cases", "annonces_24h", "vendre", "annonces_export"))

    # achetable : prix <= médiane de la case, case fiable, dans la capacité restante
    L = t.splitlines()
    yield "test_achetable_sous_la_mediane : oui", re.search(r"\| oui \|\s*$", ligne_de(L, "Paul Aubert")) is not None
    yield "test_achetable_sous_la_mediane : au-dessus de la médiane = non", "non (prix au-dessus de la médiane" in ligne_de(L, "Luc Brun")
    yield "test_achetable_sous_la_mediane : case non fiable = non", "non (case peu fiable" in ligne_de(L, "Marc Cler")
    yield "test_achetable_sous_la_mediane : case sans référence = non", "non (case sans référence" in ligne_de(L, "Eli Ferrand")
    petit = "\n".join(qfb.bloc_4(donnees_4(), {}, 40000, 1.0)).splitlines()
    yield "test_achetable_sous_la_mediane : capacité insuffisante = non", "non (au-dessus de la capacité restante" in ligne_de(petit, "Paul Aubert")
    inconnue = "\n".join(qfb.bloc_4(donnees_4(), {}, None, 1.0)).splitlines()
    yield "test_achetable : capacité illisible = non", "non (capacité restante illisible" in ligne_de(inconnue, "Paul Aubert")
    yield "test_annonces_colonnes", all(x in t for x in ("Prix actuel", "Médiane de la case", "Plafond", "Gain pour mon cinq", "Achetable", "dans 5,5 h"))
    yield "test_annonces_triees_par_fin", t.index("Paul Aubert") < t.index("Luc Brun") < t.index("Yan Dole")

    # aucune annonce dans les 24 h : phrase exacte de la revue ciblée 1
    vide = "\n".join(qfb.bloc_4(donnees_4(annonces_24h=T(ANN_COLS, [])), {}, 300000, 1.0))
    yield "test_aucune_annonce_24h", "aucune annonce du Marché ne se termine dans les 24 h (export du 10/11, 20 annonces)" in vide \
        and "donnée manquante" not in vide.split("Qui vendre")[0]

    # déduplication entre les pages
    doublon = T(ANN_COLS, list(ANN[1][:1]) * 2 + [ANN[1][1]])
    td = "\n".join(qfb.bloc_4(donnees_4(annonces_24h=doublon), {}, 300000, 1.0))
    yield "test_deduplication_des_pages", td.count("Paul Aubert") == 1 and td.count("Luc Brun") == 1

    # qui vendre
    V = t.splitlines()
    yield "test_vendre_vendable_et_necessaire : écart dans la tolérance = vendable", "vendable" in ligne_de(V, "Maël Bernard") \
        and "nécessaire" not in ligne_de(V, "Maël Bernard")
    yield "test_vendre_vendable_et_necessaire : écart > tolérance = nécessaire avec la raison", \
        "nécessaire (écart de force 4,2 supérieur à la tolérance 1,0)" in ligne_de(V, "Léo Lefebvre")
    yield "test_vendre_vendable_et_necessaire : 8 disponibles après la vente = nécessaire", \
        "nécessaire (il ne resterait que 8 joueurs disponibles, 9 requis)" in ligne_de(V, "Nolan Baron")
    yield "test_vendre_deja_en_vente", "déjà en vente" in ligne_de(V, "Sacha Leclerc")
    yield "test_vendre_prix_attendu_de_la_case", "721 000" in ligne_de(V, "Maël Bernard") and "—" in ligne_de(V, "Léo Lefebvre")
    yield "test_vendre_colonnes", all(x in t for x in ("Salaire", "Rang au poste", "Minutes", "Remplaçant", "Écart", "Verdict"))
    sans_tol = "\n".join(qfb.bloc_4(donnees_4(), {}, 300000, None))
    yield "test_vendre_tolerance_inconnue", "tolérance de vente inconnue" in sans_tol and "| vendable" not in sans_tol

    # vue illisible : le bloc ne plante pas, la ligne dit laquelle
    ill = "\n".join(qfb.bloc_4(donnees_4(prix_cases=None, annonces_24h=None, vendre=None), {}, 300000, 1.0))
    yield "test_bloc_4_vue_illisible", all(f"donnée manquante : vue {v} illisible" in ill for v in ("prix_cases", "annonces_24h", "vendre"))
    ill2 = "\n".join(qfb.bloc_4(donnees_4(**{"gold.bv_sell_replacement": None}), {}, 300000, 1.0))
    yield "test_bloc_4_vue_illisible : remplaçants", "donnée manquante : vue gold.bv_sell_replacement illisible" in ill2 and "Maël Bernard" not in ill2.split("Qui vendre")[-1]
    # A4 : jointure par player_id, deux homonymes ne se mélangent pas
    hom_c = T(["player_id", "name", "position", "age", "ps", "salary", "best_slot", "rank_in_slot", "league_min_last4", "on_transfer_list"],
              [("h1", "Jean Dupont", "PG", 25, 50.0, 20000, "PG", 3, 10.0, False), ("h2", "Jean Dupont", "C", 25, 50.0, 21000, "C", 4, 5.0, False)])
    hom_r = T(["player_id", "name", "best_slot", "fit_best", "replacement_name", "replacement_fit", "gap", "weekly_salary", "on_transfer_list", "available", "available_players"],
              [("h1", "Jean Dupont", "PG", 50.0, "Remplaçant Un", 49.5, 0.5, 20000, False, True, 14),
               ("h2", "Jean Dupont", "C", 50.0, "Remplaçant Deux", 40.0, 10.0, 21000, False, True, 14)])
    th = [l for l in qfb.bloc_4(donnees_4(vendre=hom_c, **{"gold.bv_sell_replacement": hom_r}), {}, 300000, 1.0) if "Jean Dupont" in l]
    yield "test_vendre_jointure_par_player_id_homonymes", len(th) == 2 and "Remplaçant Un" in th[1 if "| PG |" in th[1] else 0] \
        and any("| PG |" in l and "Remplaçant Un" in l and "vendable" in l and "nécessaire" not in l for l in th) \
        and any("| C |" in l and "Remplaçant Deux" in l and "nécessaire (écart de force 10,0" in l for l in th)
    yield "test_vendre_requetes_exposent_player_id", "player_id" in auj.REQUETES["vendre"] and "player_id" in auj.REQUETES["gold.bv_sell_replacement"]
    yield "test_vendre_sans_remplacant", "nécessaire (aucun remplaçant au poste)" in ligne_de(V, "Zoé Sansremplaçant")

    # lignes d'enchères et d'achats déjà produites par le plan : gardées, sans heure
    plan = [(None, 2, "Enchère maximale 100 000 sur Dupont (PG, PS 60)", "plafond de revente ; fin 11/11 09:30", "s")]
    tp = "\n".join(qfb.bloc_4(donnees_4(), {}, 300000, 1.0, actions=plan))
    yield "test_bloc_4_garde_les_lignes_du_plan", "Enchère maximale 100 000 sur Dupont" in tp and re.search(r"\d\d:\d\d", tp) is None

    yield "test_bloc_4_sans_commande", qfb.INTERDITS.search(t) is None and qfb.INTERDITS.search(tp) is None
    yield "test_bloc_4_passe_forme", forme.fautes_tableaux(t, "basketvibe") == [] and forme.fautes_de(t, "basketvibe") == [] \
        and forme.fautes_de(vide, "basketvibe") == []
    yield "test_bloc_4_sans_heure", re.search(r"\d\d:\d\d", t) is None


# ---- 5n T5 : blocs 0 et 6 ---------------------------------------------------------------------------------------
DEMANDE_A = "Pour comprendre le Match Engine, j'ai besoin de : exporte la page Effectif chaque jour de match, parce que le relevé manque."
DEMANDE_B = "Pour comprendre le Match Engine, j'ai besoin de : exporte la page des réglages utilisés vue côté adversaire, parce que le focus adverse est absent."
DEMANDE_C = "Pour comprendre le Match Engine, j'ai besoin de : exporte la page Équipe des clubs de tête, parce que leurs compétences manquent."
DEMANDE_INVALIDE = "Pour comprendre le Match Engine, j'ai besoin de : exporte une page issue d'une étude invalidée, parce que fuite."
ETUDE_OK = ("# Réussite à 3 points (2026-11-08)\n\n**Question** : x ?\n\n| groupe | n tirs | n matchs | estimé | IC 95 % | méthode | verdict |\n|---|---|---|---|---|---|---|\n"
            "| v3 ligue | 127 | 5 | +6,2 pts | - | - | indéterminé : n trop petit (< 8 matchs) |\n"
            "| v4 amical | 313 | 12 | +6,81 pts | [+3,92 ; +8,88] | bootstrap | association présente |\n\n## Export demandé\n- " + DEMANDE_A + "\n")
ETUDE_PLUS_RECENTE = ETUDE_OK.replace("2026-11-08", "2026-11-09").replace("+6,81 pts", "+7,00 pts").replace(DEMANDE_A, DEMANDE_B)
ETUDE_INVALIDEE = ("# Tirs au cercle (2026-11-10)\n\n> **T1 invalidé, fuite.** Produit par un lancement qui a lu le fichier des interdits.\n\n**Question** : y ?\n\n"
                   "Pour comprendre le Match Engine, j'ai besoin de : " + DEMANDE_INVALIDE.split(" : ", 1)[1] + "\n")
CARTE = ("# Carte de faisabilité BasketVibe (2026-11-10)\n\n| Question | n disponible | n requis | délai | Verdict |\n|---|---|---|---|---|\n"
         "| 3a force du club et victoires | 36 équipes | 4 | 0 | faisable maintenant |\n"
         "| 3b pourquoi les premiers le sont | 1 équipe | - | - | bloquée par : exporte la page Équipe des clubs de tête |\n\n## Export demandé\n- " + DEMANDE_C + "\n")


def etudes_de(textes):
    """textes : {nom de fichier : texte} -> lire_etudes sur un dossier temporaire."""
    d = Path(tempfile.mkdtemp())
    for nom, texte in textes.items():
        (d / nom).write_text(texte, encoding="utf-8")
    return qfb.lire_etudes(d)


MATCHS = T(["day", "competition_kind", "n"], [("2026-10-20", "ligue", 2), ("2026-11-01", "coupe", 1), ("2026-11-08", "amical", 1),
                                              ("2026-11-09", "ligue", 1), ("2026-11-09", "amical", 1), ("2026-11-10", "amical", 1)])
# A3 : « matchs ajoutés » = pages de match captées pour la première fois depuis hier (une ligne par match de chez nous, jour de première capture)
CAPTES = T(["kind", "premiere_jour"], [("match", "2026-11-09"), ("friendly", "2026-11-09"), ("cup", "2026-11-10"), ("friendly", "2026-10-30")])
# A7 : matchs d'autres clubs (finis, sans fixture chez nous) : jour de première capture de leur page (None si jamais captée)
AUTRES = T(["premiere_jour"], [("2026-11-09",), ("2026-10-30",), ("2026-10-30",)])
OBJ_COLS = ["day", "competition_kind", "opponent", "objectif", "raison", "rule_id", "defaites_d_affilee"]
SERIE3 = T(OBJ_COLS, [("2026-11-11", "ligue", "BC KIT", "corriger", "serie", "serie", 3)])


def donnees_t5(heb=None, **plus):
    avant = lambda h: (MAINT - dt.timedelta(hours=h)).isoformat()  # noqa: E731
    heb = heb if heb is not None else [("standings_teams", avant(100)), ("standings_players", avant(170)), ("standings_transfers", avant(10)),
                                       ("club_adverse", avant(200))]
    d = donnees_t(exports_hebdo=T(["page_type", "derniere_paris"], heb),
                  captures_marche=T(["captures", "annonces", "derniere_paris"], [(1, 20, "2026-11-09T23:18:35")]),
                  matchs_ajoutes=MATCHS, matchs_captes=CAPTES, matchs_autres=AUTRES, amical_reglage=T(["fixture_id", "match_day", "opponent", "agress_cran", "primary_quarts", "tir_cran4_joueurs"], []),
                  objectifs=SERIE3)
    d.update(plus)
    return d


def cas_t5():
    # --- lire_etudes
    et = etudes_de({"2026-11-10-tirs-cercle.md": ETUDE_INVALIDEE, "2026-11-08-trois-points.md": ETUDE_OK, "2026-11-09-trois-points.md": ETUDE_PLUS_RECENTE,
                    "2026-11-10-carte-faisabilite.md": CARTE, "test-data-scientist.md": "# pas daté\n", "interdits-t1.txt": "x"})
    sujets = {(e["sujet"], str(e["date"])) for e in et}
    yield "test_lire_etudes_ignore_invalidee", ("tirs-cercle", "2026-11-10") not in sujets and not any(DEMANDE_INVALIDE in e["demandes"] for e in et)
    yield "test_lire_etudes_plus_recente_par_sujet", sujets == {("trois-points", "2026-11-09"), ("carte-faisabilite", "2026-11-10")}
    yield "test_lire_etudes_ignore_les_fichiers_sans_date", all(e["sujet"] not in ("test-data-scientist", "interdits-t1") for e in et)
    tp = next(e for e in et if e["sujet"] == "trois-points")
    yield "test_lire_etudes_verdicts_et_resultat", "association présente" in tp["verdicts"] and tp["resultat"] == {"estime": "+7,00 pts", "ic": "[+3,92 ; +8,88]"}
    yield "test_lire_etudes_demandes_telles_quelles", tp["demandes"] == [DEMANDE_B]
    carte = next(e for e in et if e["sujet"] == "carte-faisabilite")
    yield "test_lire_etudes_carte_reconnue_et_lue", carte["carte"] is True and tp["carte"] is False and carte["demandes"] == [DEMANDE_C] \
        and ("3b pourquoi les premiers le sont", "bloquée par : exporte la page Équipe des clubs de tête") in [tuple(x) for x in carte["lignes"]]
    yield "test_date_derniere_etude_hors_carte", qfb.date_derniere_etude(et) == dt.date(2026, 11, 9) \
        and qfb.date_derniere_etude([carte]) is None and qfb.date_derniere_etude([]) is None
    yield "test_lire_etudes_dossier_absent", qfb.lire_etudes(Path(tempfile.mkdtemp()) / "inexistant") == []

    # --- etude_a_lancer
    ok = qfb.etude_a_lancer
    yield "test_etude_a_lancer_trois_defaites", ok(3, dt.date(2026, 11, 10), dt.date(2026, 11, 8), 1) is True
    yield "test_etude_pas_lancee_sans_nouveau_match", ok(3, dt.date(2026, 11, 10), dt.date(2026, 11, 8), 0) is False
    yield "test_etude_a_lancer_dimanche", ok(0, dt.date(2026, 11, 15), dt.date(2026, 11, 8), 2) is True
    yield "test_etude_pas_lancee_dimanche_etude_recente", ok(0, dt.date(2026, 11, 15), dt.date(2026, 11, 10), 2) is False
    yield "test_etude_pas_lancee_dimanche_sans_nouveau_match", ok(0, dt.date(2026, 11, 15), dt.date(2026, 11, 8), 0) is False
    yield "test_etude_pas_lancee_un_mardi_sans_defaites", ok(1, dt.date(2026, 11, 10), dt.date(2026, 11, 1), 4) is False
    yield "test_etude_pas_lancee_deux_fois_le_meme_jour", ok(3, dt.date(2026, 11, 10), dt.date(2026, 11, 10), 2) is False
    yield "test_etude_pas_lancee_deux_fois_le_meme_jour : carte du jour", ok(3, dt.date(2026, 11, 10), dt.date(2026, 11, 8), 2, etude_du_jour=True) is False
    yield "test_etude_a_lancer_sans_etude_encore", ok(3, dt.date(2026, 11, 10), None, 5) is True

    # --- bloc 0
    res = {"exports": ["Équipe (aperçu, joueurs) (30 h)", "historique global des transferts depuis 2026-11-05", "aperçu du match de ligue du 11/11 (aucune ligne adverse en base)"],
           "actions": [(None, 2, "Après 04:00 : exporter Entraînement, Finances et Personnel", "", "s"), (None, 2, "Vendre Dupont : économie", "", "s")]}
    t0 = "\n".join(qfb.bloc_0(donnees_t5(), res, et, JOUR_T, MAINT))
    L0 = t0.splitlines()
    yield "test_bloc_0_cite_le_bloc_debloque", all("→ bloc" in l for l in L0 if l.startswith("- ")) and len(L0) >= 6
    yield "test_bloc_0_cite_le_bloc_debloque : valeurs", "exporte Équipe (aperçu, joueurs) (30 h) → bloc 3" in t0 \
        and "exporte historique global des transferts depuis 2026-11-05 → bloc 4" in t0 and "exporter Entraînement, Finances et Personnel → bloc 9" in t0
    yield "test_bloc_0_une_action_hors_export_absente", "Vendre Dupont" not in t0
    yield "test_bloc_0_apercu_absent_par_match", "donnée manquante : exporte l'aperçu du match de ligue du 11/11 → bloc 3" in "\n".join(
        qfb.bloc_0(donnees_t5(**donnees_t(capture=None)), {"exports": [], "actions": []}, [], JOUR_T, MAINT)) and t0.count("l'aperçu du match de ligue du 11/11") == 0
    ill = "\n".join(qfb.bloc_0(donnees_t5(apercus_matchs=None), {"exports": [], "actions": []}, [], JOUR_T, MAINT))
    yield "test_bloc_0_apercu_illisible", "donnée manquante : exporte l'aperçu du prochain match de ligue ou de coupe → bloc 3" in ill
    yield "test_bloc_0_marche_affiche_le_compte_sans_seuil", "Marché : 1 capture, 20 annonces vues depuis 24 h (dernière le 09/11) → bloc 4" in t0
    yield "test_bloc_0_exports_hebdomadaires : 100 h non réclamé", "Équipes de la ligue" not in t0 and "Transferts de la ligue" not in t0
    yield "test_bloc_0_exports_hebdomadaires : 170 h réclamé", "exporte l'onglet Joueurs de la ligue (dernier export il y a 170 h) → blocs 5 et 6" in t0
    m51 = "\n".join(qfb.bloc_0(donnees_t5(), {"exports": ["Marché (enchères) (51 h)"], "actions": []}, [], JOUR_T, MAINT))
    yield "test_bloc_0_marche_perime (R4)", "- donnée manquante : exporte le Marché (plusieurs pages) (dernier export il y a 51 h) → bloc 4" in m51 \
        and "Marché (enchères)" not in m51
    mj = "\n".join(qfb.bloc_0(donnees_t5(), {"exports": ["Marché (enchères) (jamais exporté)"], "actions": []}, [], JOUR_T, MAINT))
    yield "test_bloc_0_marche_jamais_exporte (R4)", "- donnée manquante : exporte le Marché (plusieurs pages) (jamais exporté) → bloc 4" in mj
    yield "test_bloc_0_marche_a_jour_pas_de_demande (R4)", "exporte le Marché" not in "\n".join(qfb.bloc_0(donnees_t5(), {"exports": [], "actions": []}, [], JOUR_T, MAINT))
    vieux = "\n".join(qfb.bloc_0(donnees_t5(heb=[("standings_teams", (MAINT - dt.timedelta(hours=1)).isoformat()), ("standings_transfers", (MAINT - dt.timedelta(hours=900)).isoformat())]),
                                 {"exports": [], "actions": []}, [], JOUR_T, MAINT))
    yield "test_bloc_0_onglet_transferts_jamais_reclame (déjà dans l'historique global)", "Transferts de la ligue" not in vieux \
        and all(pt != "standings_transfers" for pt, _ in qfb.HEBDO) and "standings_transfers" not in auj.REQUETES["exports_hebdo"]
    yield "test_bloc_0_exports_hebdomadaires : jamais capturé réclamé", "exporte l'onglet Blessés de la ligue (jamais exporté) → blocs 5 et 6" in t0
    yield "test_bloc_0_exports_hebdomadaires : pages club réclamées", "exporte une page /c/<club> d'un club adverse (dernier export il y a 200 h) → blocs 5 et 6" in t0
    # R2 (test réécrit : l'ancien attendait le texte complet de la demande au bloc 0) : forme courte au bloc 0, texte complet au bloc 6 seulement
    yield "test_bloc_0_demandes_courtes", "- exporte la page des réglages utilisés vue côté adversaire (étude du 09/11) → bloc 6" in t0 \
        and "- exporte la page Équipe des clubs de tête (étude du 10/11) → bloc 6" in t0 and "parce que" not in t0 and "Pour comprendre" not in t0 \
        and DEMANDE_A not in t0 and DEMANDE_INVALIDE not in t0
    yield "test_demande_courte : coupe avant « parce que », sans ponctuation finale", qfb.demande_courte(DEMANDE_B) == "exporte la page des réglages utilisés vue côté adversaire" \
        and qfb.demande_courte("exporte X, parce que y") == "exporte X" and qfb.demande_courte("exporte X.") == "exporte X" \
        and qfb.demande_courte(PREFIXE_DEMANDE + "exporte la page Z (si le jeu l'affiche), parce que a") == "exporte la page Z (si le jeu l'affiche)"
    yield "test_bloc_6_garde_le_texte_complet_des_demandes", f"{DEMANDE_B} (étude du 09/11)" in "\n".join(qfb.bloc_6(donnees_t5(), et, JOUR_T)[0])
    yield "test_bloc_0_aucune_etude_aucune_demande", "Pour comprendre" not in "\n".join(qfb.bloc_0(donnees_t5(), {"exports": [], "actions": []}, [], JOUR_T, MAINT))
    yield "test_bloc_0_sans_commande_ni_heure", qfb.INTERDITS.search(t0) is None and re.search(r"\d\d:\d\d", t0) is None
    toutes = "\n".join(qfb.bloc_0(donnees_t5(heb=[(p, (MAINT - dt.timedelta(hours=1)).isoformat()) for p in
                                                  ("standings_teams", "standings_players", "standings_injuries", "standings_transfers", "club_adverse")]),
                                  {"exports": [], "actions": []}, [], JOUR_T, MAINT))
    yield "test_bloc_0_tout_a_jour_n_est_pas_vide", "aucun export à refaire" in toutes and "donnée manquante" not in toutes
    yield "test_bloc_0_vue_illisible", "donnée manquante : vue exports_hebdo illisible" in "\n".join(
        qfb.bloc_0(donnees_t5(exports_hebdo=None, captures_marche=None), {"exports": [], "actions": []}, [], JOUR_T, MAINT)) \
        and "donnée manquante : vue captures_marche illisible" in "\n".join(
        qfb.bloc_0(donnees_t5(exports_hebdo=None, captures_marche=None), {"exports": [], "actions": []}, [], JOUR_T, MAINT))
    yield "test_requete_matchs_captes_existe", "matchs_captes" in auj.REQUETES and "min(p.captured_at)" in auj.REQUETES["matchs_captes"] \
        and "bronze.raw_pages" in auj.REQUETES["matchs_captes"]
    yield "test_requetes_t5_existent", all(k in auj.REQUETES for k in ("captures_marche", "matchs_ajoutes", "exports_hebdo"))

    # --- bloc 6
    jour = dt.date(2026, 11, 10)
    etu = etudes_de({"2026-11-08-trois-points.md": ETUDE_OK, "2026-11-10-carte-faisabilite.md": CARTE})
    l6, c6 = qfb.bloc_6(donnees_t5(), etu, jour)
    t6 = "\n".join(l6)
    yield "test_bloc_6_ligne_quotidienne", l6[0] == "matchs ajoutés : 4 (ligue 2, amical 1 ; autres clubs 1) · 10 en base · étude à jour au 08/11, 3 de nos matchs pas encore étudiés ; 1 d'autres clubs" \
        and "appris" not in t6 and "relancée" not in t6
    yield "test_bloc_6_la_carte_ne_compte_ni_pour_la_date_ni_pour_k", "étude à jour au 08/11, 3 de nos matchs pas encore étudiés ; 1 d'autres clubs" in l6[0]
    yield "test_bloc_6_ligne_sans_etude", qfb.bloc_6(donnees_t5(), [], jour)[0][0] == "matchs ajoutés : 4 (ligue 2, amical 1 ; autres clubs 1) · 10 en base · aucune étude encore, 7 de nos matchs pas encore étudiés ; 3 d'autres clubs"
    yield "test_bloc_6_ligue_comprend_la_coupe", qfb.bloc_6(donnees_t5(matchs_captes=T(["kind", "premiere_jour"], [("cup", "2026-11-09"), ("cup", "2026-11-10"), ("match", "2026-11-10")])),
                                                           etu, jour)[0][0].startswith("matchs ajoutés : 4 (ligue 3, amical 0 ; autres clubs 1)")
    yield "test_demandes_recopiees_des_etudes : bloc 6", f"{DEMANDE_A} (étude du 08/11)" in t6 and f"{DEMANDE_C} (étude du 10/11)" in t6
    yield "test_demandes_recopiees_des_etudes : aucune étude", all("Pour comprendre" not in l for l in qfb.bloc_6(donnees_t5(), [], jour)[0])
    yield "test_bloc_6_consigne_session", len(c6) == 1 and "data-scientist" in c6[0] and "v4 ligue, v5 amical" in c6[0] and "horizon aujourd'hui" in c6[0]
    yield "test_bloc_6_consigne_nomme_la_question_indeterminee", "trois-points" in c6[0]
    yield "test_bloc_6_consigne_arriere_plan", "en arrière-plan" in c6[0] and "n'attends pas son résultat" in c6[0] \
        and "au plus une fois par jour" in c6[0] and "étude lancée, résultat attendu" in c6[0] and qfb.MARQUEUR_ETUDE_LANCEE in c6[0]
    l6d, c6d = qfb.bloc_6(donnees_t5(), etu, jour, None, f"- 15:55 {qfb.MARQUEUR_ETUDE_LANCEE} sur trois-points")
    yield "test_bloc_6_etude_lancee_registre : plus de consigne, ligne « étude lancée, résultat attendu »", c6d == [] and "étude lancée, résultat attendu" in l6d
    yield "test_bloc_6_etude_lancee_registre : la première ligne reste la ligne quotidienne", l6d[0].startswith("matchs ajoutés : ")
    l6e, c6e = qfb.bloc_6(donnees_t5(), etu, jour, None, "- export fait")
    yield "test_bloc_6_registre_sans_lancement : consigne maintenue, pas de ligne « étude lancée »", len(c6e) == 1 and "étude lancée, résultat attendu" not in l6e
    l6b, c6b = qfb.bloc_6(donnees_t5(matchs_ajoutes=T(["day", "competition_kind", "n"], [("2026-11-08", "amical", 1)])), etu, jour)
    yield "test_etude_pas_lancee_sans_nouveau_match : bloc 6", c6b == [] and "0 de nos matchs pas encore étudiés ; 1 d'autres clubs" in l6b[0]
    l6c, c6c = qfb.bloc_6(donnees_t5(objectifs=T(OBJ_COLS, [("2026-11-11", "ligue", "BC KIT", "corriger", "serie", "serie", 1)])), etu, jour)
    yield "test_etude_pas_lancee_un_mardi_sans_defaites : bloc 6", c6c == []
    dim = dt.date(2026, 11, 15)
    l6d, c6d = qfb.bloc_6(donnees_t5(objectifs=T(OBJ_COLS, [])), etu, dim)
    yield "test_etude_a_lancer_dimanche : bloc 6", len(c6d) == 1
    etu_j = etudes_de({"2026-11-10-trois-points.md": ETUDE_OK})
    l6e, c6e = qfb.bloc_6(donnees_t5(matchs_ajoutes=T(["day", "competition_kind", "n"], [("2026-11-10", "ligue", 1)])), etu_j, jour)
    yield "test_etude_pas_lancee_deux_fois_le_meme_jour : bloc 6", c6e == []
    carte_seule = etudes_de({"2026-11-10-carte-faisabilite.md": CARTE})
    l6f, c6f = qfb.bloc_6(donnees_t5(), carte_seule, jour)
    yield "test_bloc_6_la_carte_du_jour_ne_bloque_pas_le_lancement", len(c6f) == 1
    yield "test_bloc_6_sans_commande_ni_heure", qfb.INTERDITS.search(t6) is None and re.search(r"\d\d:\d\d", t6) is None
    yield "test_bloc_6_passe_forme", forme.fautes_tableaux(t6, "basketvibe") == [] and forme.fautes_de(t6, "basketvibe") == []
    # A3 : ce qui compte est la première capture de la page, pas le jour du match ; une page captée plus tôt n'est pas « ajoutée »
    joues_hier = T(["day", "competition_kind", "n"], [("2026-11-09", "ligue", 1), ("2026-11-09", "amical", 1)])
    anciennes = T(["kind", "premiere_jour"], [("match", "2026-10-20"), ("friendly", "2026-10-20")])
    yield "test_matchs_ajoutes_page_captee_plus_tot_non_comptee", qfb.bloc_6(donnees_t5(matchs_ajoutes=joues_hier, matchs_captes=anciennes), etu, jour)[0][0] \
        .startswith("matchs ajoutés : 1 (ligue 0, amical 0 ; autres clubs 1) · 5 en base")
    yield "test_matchs_ajoutes_page_captee_hier_pour_un_match_ancien_comptee", qfb.bloc_6(donnees_t5(matchs_ajoutes=joues_hier, matchs_captes=T(["kind", "premiere_jour"], [("match", "2026-11-09")])),
                                                                                         etu, jour)[0][0].startswith("matchs ajoutés : 2 (ligue 1, amical 0 ; autres clubs 1)")
    yield "test_matchs_ajoutes_fenetre_hier", qfb.bloc_6(donnees_t5(matchs_captes=T(["kind", "premiere_jour"], [("match", "2026-11-08"), ("friendly", "2026-11-09")])),
                                                        etu, jour)[0][0].startswith("matchs ajoutés : 2 (ligue 0, amical 1 ; autres clubs 1)")
    l_ill = qfb.bloc_6(donnees_t5(matchs_captes=None), etu, jour)[0][0]
    yield "test_matchs_ajoutes_vue_illisible", l_ill.startswith("matchs ajoutés : donnée manquante : vue matchs_captes illisible · 10 en base · étude à jour au 08/11, 3 de nos matchs pas encore étudiés ; 1 d'autres clubs")
    # A7 : autres clubs dans la ligne ; k et le déclencheur ne comptent que nos matchs
    yield "test_matchs_autres_clubs_dans_la_ligne", qfb.bloc_6(donnees_t5(), etu, jour)[0][0] == "matchs ajoutés : 4 (ligue 2, amical 1 ; autres clubs 1) · 10 en base · étude à jour au 08/11, 3 de nos matchs pas encore étudiés ; 1 d'autres clubs"
    yield "test_matchs_autres_clubs_zero", "autres clubs 0) · 7 en base" in qfb.bloc_6(donnees_t5(matchs_autres=T(["premiere_jour"], [])), etu, jour)[0][0]
    yield "test_matchs_autres_clubs_jamais_captes_comptes_en_base_pas_ajoutes", "autres clubs 0) · 8 en base" in qfb.bloc_6(
        donnees_t5(matchs_autres=T(["premiere_jour"], [(None,)])), etu, jour)[0][0]
    yield "test_matchs_autres_clubs_vue_illisible", qfb.bloc_6(donnees_t5(matchs_autres=None), etu, jour)[0][0].startswith(
        "matchs ajoutés : 3 (ligue 2, amical 1 ; autres clubs donnée manquante : vue matchs_autres illisible) · 7 en base · étude à jour au 08/11, 3 de nos matchs pas encore étudiés")
    seuls_autres = donnees_t5(matchs_ajoutes=T(["day", "competition_kind", "n"], [("2026-11-08", "amical", 1)]), matchs_autres=T(["premiere_jour"], [("2026-11-10",)] * 5))
    l_a, c_a = qfb.bloc_6(seuls_autres, etu, jour)
    yield "test_matchs_autres_clubs_ne_declenchent_pas_l_etude_et_hors_de_k", c_a == [] and "0 de nos matchs pas encore étudiés ; 5 d'autres clubs" in l_a[0]
    yield "test_requete_matchs_autres_existe", "matchs_autres" in auj.REQUETES and "silver.bv_matches" in auj.REQUETES["matchs_autres"] and "not exists" in auj.REQUETES["matchs_autres"]
    yield "test_bloc_6_vue_illisible", "donnée manquante : vue matchs_ajoutes illisible" in "\n".join(qfb.bloc_6(donnees_t5(matchs_ajoutes=None), etu, jour)[0])

    # avancement des expériences et prochaine hypothèse
    exp = {"debut": "2026-11-10", "faits": [], "file": [{"id": "E1", "reglage": "agressivité défensive", "niveaux": {"A": "agressivité 3", "B": "agressivité 5"},
                                                           "joue": {"A": {"agress_cran": 2}, "B": {"agress_cran": 4}}, "ordre": ["A", "B", "A", "B"], "amicaux_vises": 4}]}
    l6g, _ = qfb.bloc_6(donnees_t5(), etu, jour, experiences=exp)
    t6g = "\n".join(l6g)
    yield "test_bloc_6_avancement_et_prochaine_hypothese", "E1 : 0 vérifié sur 4" in t6g and "prochaine hypothèse : E1" in t6g


# ---- 5n T6 : blocs 5, 7 à 10 et assemblage ---------------------------------------------------------------------
PHRASE_SANS_ETUDE = "étude pas encore commencée, carte de faisabilité à faire"
OFFICIEL_COLS = ["day", "competition_kind", "opponent", "my_result"]
RES_VIDE = {"actions": [], "exports": [], "garder": [], "infos": [], "capacite": None}


def donnees_t6(**plus):
    d = donnees_t5(**donnees_4())
    d.update({"tolerance_vente": T(["value"], [("1.0",)]), "dernier_officiel": T(OFFICIEL_COLS, [("2026-11-09", "ligue", "Naked Spartans", "L")])})
    d.update(plus)
    return d


def res_t6():
    return {"actions": [(None, 1, "Composition J5 contre Naked Spartans : lance l'agent tactique (aperçu du 10/11 en base)", "", "s"),
                        (None, 2, "Analyse : lance l'agent analyste ce soir", "", "s"),
                        (None, 2, "Analyse : défaite du 09/11 contre Naked Spartans, 3 défaites d'affilée", "", "s"),
                        (None, 1, "Finances : solde projeté au 30/11 de 100 000, sous une semaine de salaires (30 000)", "cause : charges", "s"),
                        (None, 2, "Entraînement (fin du cycle dimanche 04:00) : corrige 2 écarts à l'écran", "", "s"),
                        (None, 2, "Académie, rapport du 05/11 : 2 prospects ; cote inconnue", "", "s"),
                        (None, 2, "Enchère maximale 100 000 sur Dupont (PG, PS 60)", "fin 11/11 09:30", "s"),
                        (None, 2, "Vendre Maël Bernard : économie 17 303 par semaine", "", "s")],
            "exports": ["Équipe (aperçu, joueurs) (30 h)"], "infos": [], "capacite": 300000,
            "garder": ["effectif, vendre pour profit : règle non écrite — à valider (seuil de déclenchement non validé)",
                       "Personnel (Coach 1/1) : règle de personnel non tranchée, à valider", "finances : seuil non atteint (résultat hebdo estimé +9 000)"]}


def cas_t6():
    S = {"experiences": None, "analyste": None}
    etu = etudes_de({"2026-11-08-trois-points.md": ETUDE_OK, "2026-11-10-carte-faisabilite.md": CARTE})

    # --- états d'étude
    yield "test_etat_etude_sans_etude", qfb.etat_etude([], 5) == PHRASE_SANS_ETUDE and qfb.etat_etude([], 8) == PHRASE_SANS_ETUDE \
        and qfb.etat_etude([], 9) == PHRASE_SANS_ETUDE
    e5 = qfb.etat_etude(etu, 5)
    yield "test_etat_etude_lit_la_carte : faisable et bloquée", "3a force du club et victoires : faisable maintenant" in e5 \
        and "3b pourquoi les premiers le sont : bloquée par : exporte la page Équipe des clubs de tête" in e5 and "10/11" in e5
    yield "test_etat_etude_lit_la_carte : bloc sans question", "ne couvre pas ce bloc" in qfb.etat_etude(etu, 8) and "carte de faisabilité à faire" not in qfb.etat_etude(etu, 8)
    reel = dict(qfb.SUJET_BLOC)
    qfb.SUJET_BLOC["trois-points"] = 5
    try:
        e5r = qfb.etat_etude(etu, 5)
    finally:
        qfb.SUJET_BLOC.clear()
        qfb.SUJET_BLOC.update(reel)
    yield "test_etat_etude_dernier_resultat", e5r == "dernier résultat du 08/11 : +6,81 pts [+3,92 ; +8,88]"
    yield "test_table_sujet_bloc_vide_en_5n", qfb.SUJET_BLOC == {}
    yield "test_aucun_reporte", all("report" not in x.lower() for b in (qfb.bloc_5(etu), qfb.bloc_5([]), qfb.bloc_8([], etu), qfb.bloc_9([], []))
                                    for x in b)
    yield "test_bloc_5_une_ligne", qfb.bloc_5([]) == [PHRASE_SANS_ETUDE]

    # --- bloc 7 : la ligne d'état est toujours là
    defaite = donnees_t6()
    l = qfb.bloc_7([], defaite)
    yield "test_bloc_7_ligne_d_etat_toujours : défaite non analysée", l[0] == "défaite du 09/11 : analyse non faite, lancée dans ce passage"
    yield "test_bloc_7_ligne_d_etat_toujours : défaite analysée", qfb.bloc_7([], defaite, analyste=dt.date(2026, 11, 9))[0] == "défaite du 09/11 : analyse faite"
    gagne = donnees_t6(dernier_officiel=T(OFFICIEL_COLS, [("2026-11-09", "ligue", "Naked Spartans", "W")]))
    yield "test_bloc_7_ligne_d_etat_toujours : aucune défaite", qfb.bloc_7([], gagne)[0] == "aucune défaite de ligue ou de coupe non analysée"
    yield "test_bloc_7_ligne_d_etat_toujours : vue illisible", qfb.bloc_7([], donnees_t6(dernier_officiel=None))[0] == "donnée manquante : vue dernier_officiel illisible"
    l7 = qfb.bloc_7(res_t6()["actions"], defaite)
    yield "test_bloc_7_puis_les_lignes_du_plan", l7[0].startswith("défaite du") and any("défaite du 09/11 contre Naked Spartans, 3 défaites" in x for x in l7) \
        and not any("lance l'agent" in x for x in l7)

    # --- blocs 8 et 9
    l8 = qfb.bloc_8(res_t6()["actions"], etu, res_t6()["garder"])
    yield "test_bloc_8_etat_puis_lignes", l8[0] == qfb.etat_etude(etu, 8) and any("solde projeté au 30/11" in x for x in l8)
    yield "test_bloc_8_sans_ligne_constat_ou_vide", any("finances : seuil non atteint" in x for x in qfb.bloc_8([], [], ["finances : seuil non atteint (résultat hebdo estimé +9 000)"])) \
        and any("aucune règle de finances déclenchée" in x for x in qfb.bloc_8([], [], []))
    l9 = qfb.bloc_9(res_t6()["actions"], etu)
    yield "test_bloc_9_etat_puis_lignes", l9[0] == qfb.etat_etude(etu, 9) and any("corrige 2 écarts" in x for x in l9) and any("Académie, rapport" in x for x in l9) \
        and re.search(r"\d\d:\d\d", "\n".join(l9)) is None
    yield "test_bloc_9_sans_ligne", any("aucune règle d'académie, de personnel ou d'entraînement déclenchée" in x for x in qfb.bloc_9([], []))

    # --- bloc 10
    r = res_t6()
    l10 = "\n".join(qfb.bloc_10(r["actions"], r["garder"]))
    yield "test_bloc_10_propositions_a_valider_par_ecrit", "à valider par écrit : Enchère maximale 100 000 sur Dupont" in l10 and "à valider par écrit : Vendre Maël Bernard" in l10 \
        and re.search(r"\d\d:\d\d", l10) is None
    yield "test_bloc_10_regles_non_tranchees", "vendre pour profit" in l10 and "Personnel (Coach 1/1)" in l10 and "seuil non atteint" not in l10
    yield "test_bloc_10_jamais_vide", qfb.bloc_10([], []) == ["- aucune décision n'attend ton accord écrit"]
    besoin = [(None, 2, "Acheter un SF de note ≥ 61,0 : aucune annonce au poste SF dans le Marché du 09/11 (annonces encore ouvertes de l'export)", "", "s")]
    cible = [(None, 2, "Acheter un PG de note ≥ 60 : Dupont (PS 61) : 50 000 à l'export, plafond de besoin 90 000, à valider", "", "s")]
    yield "test_bloc_10_un_besoin_sans_annonce_n_est_pas_une_proposition", qfb.bloc_10(besoin, []) == ["- aucune décision n'attend ton accord écrit"] \
        and "à valider par écrit : Acheter un PG" in "\n".join(qfb.bloc_10(cible, []))

    # --- assemblage
    texte, consignes = qfb.rendre_blocs(r, donnees_t6(), {}, JOUR_T, MAINT, S, etudes=etu, base=dossier())
    pos = [texte.find(f"## Bloc {n} — ") for n in range(11)]
    yield "test_onze_blocs_dans_l_ordre", all(p >= 0 for p in pos) and pos == sorted(pos)
    vide_texte, vide_cons = qfb.rendre_blocs(RES_VIDE, {}, {}, JOUR_T, MAINT, S, etudes=[], base=dossier())
    yield "test_aucun_bloc_absent", all(f"## Bloc {n} — " in vide_texte for n in range(11)) and isinstance(vide_cons, list)
    yield "test_aucun_bloc_vide : chaque bloc a au moins une ligne", all(len(b.split("\n", 1)[1].strip()) > 0 for b in vide_texte.split("## Bloc ")[1:])
    yield "test_consignes_de_session_collectees", any("lancer l'agent tactique" in c or "lance l'agent tactique" in c for c in consignes) \
        and any("lance l'agent analyste" in c for c in consignes) and not any(c in texte for c in consignes)
    yield "test_aucun_mot_interdit_dans_tout_le_rendu", qfb.INTERDITS.search(texte) is None and qfb.INTERDITS.search(vide_texte) is None
    yield "test_aucune_heure_dans_le_rendu_sauf_le_verrou", all(re.search(r"\d\d:\d\d", l) is None or "verrou" in l for l in texte.splitlines())
    yield "test_rendu_passe_forme_et_controle", forme.fautes_de(texte, "basketvibe") == [] and forme.fautes_de(vide_texte, "basketvibe") == [] \
        and __import__("controle").reports(texte) == []
    yield "test_rendu_bloc_1_et_bloc_4_dedans", "→ bloc 4" in texte and "Table des prix" in texte and "Qui vendre" in texte

    # revue ciblée 5 : vue illisible = ligne dans le bloc concerné, le script ne plante pas
    r_ill = dict(res_t6(), actions=res_t6()["actions"] + [(None, 3, "il me manque gold.bv_finance_health (timeout) — export Finances", "", "s")])
    t_ill, _ = qfb.rendre_blocs(r_ill, donnees_t6(**{"gold.bv_finance_health": None}), {"gold.bv_finance_health": "timeout"}, JOUR_T, MAINT, S, etudes=etu, base=dossier())
    bloc8 = t_ill.split("## Bloc 8 — ")[1].split("## Bloc 9 — ")[0]
    yield "test_vue_illisible_ne_plante_pas", "donnée manquante : vue gold.bv_finance_health illisible" in bloc8 and "il me manque gold.bv_finance_health" not in bloc8
    t_ill2, _ = qfb.rendre_blocs(res_t6(), donnees_t6(prix_cases=None, matchs_ajoutes=None, exports_hebdo=None, dernier_officiel=None),
                                 {"prix_cases": "x", "matchs_ajoutes": "x", "exports_hebdo": "x", "dernier_officiel": "x"}, JOUR_T, MAINT, S, etudes=etu, base=dossier())
    yield "test_vue_illisible_dans_chaque_bloc", all(f"donnée manquante : vue {v} illisible" in t_ill2 for v in ("prix_cases", "matchs_ajoutes", "exports_hebdo", "dernier_officiel"))


# ---- A1 : demandes traitées (docs/etudes/demandes-traitees.md) -----------------------------------------------------
PREFIXE_DEMANDE = "Pour comprendre le Match Engine, j'ai besoin de : "
DEMANDES_REELLES = {
    "effectif_ligue": PREFIXE_DEMANDE + "exporte la page Effectif les jours de ligue entre l'amical de 8 h et le match de 20 h, puis après le match de ligue, parce que les 4 intervalles manquent.",
    "effectif_match": PREFIXE_DEMANDE + "exporte la page effectif (compétences des joueurs) chaque jour de match, avant le match, parce que les tirs à 3 points de v3 ligue n'ont pas de relevé.",
    "reglages_29_10": PREFIXE_DEMANDE + "exporte la page des réglages utilisés de l'amical du 29/10 (Chomelix Cow contre BC Statyba Telsiai), parce que c'est le seul amical v5 sans réglages en base.",
}
DEMANDE_RESTANTE = PREFIXE_DEMANDE + "exporte la page Équipe des clubs de tête du classement, parce que leurs compétences manquent."
TRAITEES = ("| début de la demande | statut | date | raison |\n|---|---|---|---|\n"
            "| exporte la page Effectif les jours de ligue entre l'amical de 8 h | écartée | 2026-11-10 | fatigue d'amical déjà mesurée |\n"
            "| exporte la page effectif (compétences des joueurs) chaque jour de match, avant le match | écartée | 2026-11-10 | demande sur des groupes v3 clos |\n"
            "| exporte la page des réglages utilisés de l'amical du 29/10 | fait | 2026-11-10 | exporté par l'utilisateur |\n")


def etude_avec(*demandes):
    return "# Étude (2026-11-10)\n\n**Question** : x ?\n\n## Export demandé\n" + "".join(f"- {d}\n" for d in demandes)


TRAITEES_Q = ("| début de la demande | statut | date | question liée | raison |\n|---|---|---|---|---|\n"
              "| exporte la page Équipe (effectif) des clubs de tête du classement | fait | 2026-11-10 | 3b | ingérée dans silver.bv_club_roster |\n"
              "| exporte la page Entraînement chaque semaine | écartée | 2026-11-10 | 5a | remplacée par les demandes du samedi et du lundi |\n")


def cas_r3():
    """R3 : colonne « question liée » de demandes-traitees.md ; une question dont la demande est « fait » : « export reçu le JJ/MM, étude à lancer »."""
    et = etudes_de({"2026-11-10-carte-faisabilite.md": CARTE, "demandes-traitees.md": TRAITEES_Q})
    e5 = qfb.etat_etude(et, 5)
    yield "test_r3_question_fait : 3b affiche « export reçu le 10/11, étude à lancer »", "3b pourquoi les premiers le sont : export reçu le 10/11, étude à lancer" in e5 \
        and "bloquée par" not in e5
    yield "test_r3_question_fait : 3a, sans demande traitée, garde son verdict", "3a force du club et victoires : faisable maintenant" in e5
    et2 = etudes_de({"2026-11-10-carte-faisabilite.md": CARTE, "demandes-traitees.md": TRAITEES_Q.replace("| fait |", "| écartée |")})
    yield "test_r3_question_ecartee : le verdict de la carte reste", "bloquée par : exporte la page Équipe des clubs de tête" in qfb.etat_etude(et2, 5)
    et3 = etudes_de({"2026-11-10-carte-faisabilite.md": CARTE, "demandes-traitees.md": TRAITEES_Q.replace("| 3b |", "| — |")})
    yield "test_r3_sans_question_liee : verdict inchangé", "bloquée par" in qfb.etat_etude(et3, 5)
    yield "test_r3_demande_toujours_ignoree_avec_la_nouvelle_colonne", etudes_de({"2026-11-10-sujet.md": etude_avec(
        PREFIXE_DEMANDE + "exporte la page Équipe (effectif) des clubs de tête du classement, parce que x.", DEMANDE_RESTANTE),
        "demandes-traitees.md": TRAITEES_Q})[0]["demandes"] == [DEMANDE_RESTANTE]
    yield "test_r3_sans_fichier : verdict inchangé", "bloquée par" in qfb.etat_etude(etudes_de({"2026-11-10-carte-faisabilite.md": CARTE}), 5)
    # fichier réel
    reel = qfb.lire_etudes()
    texte = (qfb.DOSSIER_ETUDES / "demandes-traitees.md").read_text(encoding="utf-8")
    yield "test_r3_fichier_reel : colonne « question liée » et les deux lignes", "| question liée |" in texte \
        and "exporte la page Équipe (effectif) des clubs de tête du classement | fait | 2026-11-10 | 3b |" in texte \
        and "exporte la page Entraînement chaque semaine | écartée | 2026-11-10 | 5a |" in texte
    yield "test_r3_fichier_reel : bloc 5, 3b « export reçu le 10/11, étude à lancer »", "3b pourquoi les premiers le sont (compétences, tactique) : export reçu le 10/11, étude à lancer" in qfb.etat_etude(reel, 5)
    yield "test_r3_fichier_reel : plus de demande « page Équipe des clubs de tête » ni « Entraînement chaque semaine »", not any(
        d.startswith(PREFIXE_DEMANDE + x) for e in reel for d in e["demandes"] for x in ("exporte la page Équipe (effectif) des clubs de tête", "exporte la page Entraînement chaque semaine"))


def cas_a1():
    for cle, demande in DEMANDES_REELLES.items():
        et = etudes_de({"2026-11-10-sujet.md": etude_avec(demande, DEMANDE_RESTANTE), "demandes-traitees.md": TRAITEES})
        yield f"test_demande_traitee_ignoree : {cle}", len(et) == 1 and et[0]["demandes"] == [DEMANDE_RESTANTE]
    et = etudes_de({"2026-11-10-sujet.md": etude_avec(*DEMANDES_REELLES.values(), DEMANDE_RESTANTE), "demandes-traitees.md": TRAITEES})
    yield "test_demande_traitee_ignoree : les trois ensemble, une seule reste", et[0]["demandes"] == [DEMANDE_RESTANTE]
    sans = etudes_de({"2026-11-10-sujet.md": etude_avec(*DEMANDES_REELLES.values())})
    yield "test_demande_traitee_sans_fichier_rien_n_est_ignore", len(sans[0]["demandes"]) == 3
    en_cours = TRAITEES.replace("| fait |", "| en cours |")
    yield "test_demande_traitee_statut_inconnu_non_ignore", len(etudes_de({"2026-11-10-sujet.md": etude_avec(DEMANDES_REELLES["reglages_29_10"]),
                                                                        "demandes-traitees.md": en_cours})[0]["demandes"]) == 1
    yield "test_demandes_traitees_n_est_pas_une_etude", all(e["sujet"] != "demandes-traitees" for e in etudes_de({"demandes-traitees.md": TRAITEES}))
    # bloc 0 et bloc 6 : la demande traitée n'est plus réclamée
    t0 = "\n".join(qfb.bloc_0(donnees_t5(), {"exports": [], "actions": []}, et, JOUR_T, MAINT))
    l6, _ = qfb.bloc_6(donnees_t5(), et, dt.date(2026, 11, 10))
    yield "test_demande_traitee_absente_des_blocs_0_et_6", qfb.demande_courte(DEMANDE_RESTANTE) in t0 and "l'amical du 29/10" not in t0 + "\n".join(l6) \
        and "les jours de ligue entre" not in t0 and "exporte la page effectif (compétences" not in t0
    # fichier réel du dépôt
    reel = qfb.lire_etudes()
    toutes = [d for e in reel for d in e["demandes"]]
    yield "test_fichier_reel_demandes_traitees_present", (qfb.DOSSIER_ETUDES / "demandes-traitees.md").is_file()
    yield "test_etudes_reelles_sans_les_trois_demandes", not any(d.startswith(PREFIXE_DEMANDE + x) for d in toutes for x in (
        "exporte la page Effectif les jours de ligue entre l'amical de 8 h", "exporte la page effectif (compétences des joueurs) chaque jour de match, avant le match",
        "exporte la page des réglages utilisés de l'amical du 29/10")) and len(toutes) >= 1


# ---- A2 : bloc 0, page Entraînement la veille et le lendemain du traitement (dimanche) --------------------------
def etat_entrainement(dernier):
    """gold.bv_exports_state avec l'écran Entraînement exporté à `dernier` (None : jamais)."""
    lignes = [(11, "Entraînement", "x", dernier, 52, "🟩 à jour")] if dernier else []
    return T(["ordre", "ecran", "pour_quoi", "dernier_paris", "age_h", "statut"], lignes)


def demande_entrainement(jour, dernier, heure=(15, 0)):
    maint = dt.datetime.combine(jour, dt.time(*heure))
    d = donnees_t5(**{"gold.bv_exports_state": etat_entrainement(dernier)})
    return [l for l in qfb.bloc_0(d, {"exports": [], "actions": []}, [], jour, maint) if "Entraînement" in l]


def cas_a2():
    skill = (DOSSIER.parent / ".claude/skills/basketvibe-entrainement/references/01-fonctionnement.md").read_text(encoding="utf-8")
    yield "test_entrainement_jour_de_traitement_lu_dans_le_skill", "le **dimanche à minuit" in skill and qfb.JOUR_TRAITEMENT_ENTRAINEMENT == 6
    # veille (samedi 14/11) : dernier export le 08/11
    sam = demande_entrainement(dt.date(2026, 11, 14), "2026-11-08T11:08:00")
    yield "test_entrainement_veille_du_traitement", len(sam) == 1 and "veille du traitement" in sam[0] and "dimanche 15/11" in sam[0] \
        and sam[0].startswith("- donnée manquante : exporte la page Entraînement aujourd'hui") and sam[0].endswith("→ blocs 9 et 6")
    yield "test_entrainement_veille_deja_exportee_aujourd_hui", demande_entrainement(dt.date(2026, 11, 14), "2026-11-14T09:00:00") == []
    # lendemain (lundi 16/11) : dernier export avant le traitement de dimanche 04:00
    lun = demande_entrainement(dt.date(2026, 11, 16), "2026-11-14T18:00:00")
    yield "test_entrainement_lendemain_du_traitement", len(lun) == 1 and "lendemain du traitement" in lun[0] and "dimanche 15/11" in lun[0] \
        and lun[0].endswith("→ blocs 9 et 6")
    yield "test_entrainement_lendemain_export_apres_le_traitement", demande_entrainement(dt.date(2026, 11, 16), "2026-11-15T10:00:00") == []
    yield "test_entrainement_lendemain_export_pile_avant_le_traitement", len(demande_entrainement(dt.date(2026, 11, 16), "2026-11-15T03:59:00")) == 1
    # les autres jours : rien
    yield "test_entrainement_autres_jours_rien", all(demande_entrainement(dt.date(2026, 11, j), "2026-11-08T11:08:00") == [] for j in (10, 11, 12, 13, 15, 17))
    # jamais exporté : réclamé la veille et le lendemain
    yield "test_entrainement_jamais_exporte", len(demande_entrainement(dt.date(2026, 11, 14), None)) == 1 and len(demande_entrainement(dt.date(2026, 11, 16), None)) == 1
    # la date du traitement est la même pour la veille et le lendemain (deux dates)
    yield "test_entrainement_les_deux_dates", sam[0].count("15/11") == 1 and lun[0].count("15/11") == 1 and "14/11" not in lun[0]
    yield "test_entrainement_sans_commande_ni_heure", all(qfb.INTERDITS.search(x) is None and re.search(r"\d\d:\d\d", x) is None for x in sam + lun)


# ---- A6 : budget de durée du script ------------------------------------------------------------------------------
def cas_a6():
    racine = DOSSIER.parent
    plan = (racine / "docs/refonte-v3/plan-5n-que-faire.md").read_text(encoding="utf-8")
    conception = (racine / "docs/refonte-v3/conception-5n-que-faire.md").read_text(encoding="utf-8")
    yield "test_budget_du_script_30_s", qfb.BUDGET_SECONDES == 30
    yield "test_parallele_inchange", auj.PARALLELE == 8
    yield "test_plan_dit_30_s", "Durée du script : au plus 30 s" in plan and "au plus 15 s" not in plan
    yield "test_conception_dit_30_s", "30 s" in conception and "les 15 s actuelles" not in conception
    yield "test_journal_donne_la_raison_du_budget", "Budget du script : 30 s" in (racine / "docs/refonte-v3/journal-aujourdhui.md").read_text(encoding="utf-8")


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
