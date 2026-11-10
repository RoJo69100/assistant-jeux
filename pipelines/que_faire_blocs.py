"""Le « que faire » BasketVibe en 11 blocs (étape 5n), gabarit : docs/attentes/gabarit-que-faire-basketvibe.md.

Plan : docs/refonte-v3/plan-5n-que-faire.md. Ce module range les actions de aujourdhui.plan() dans les blocs 0 à 10
et rend le document. Règle commune : un bloc vide s'écrit « donnée manquante : exporte <écran> », jamais une commande.
"""
import datetime as dt
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import aujourdhui as auj  # noqa: E402
import composition as comp  # noqa: E402
import forme  # noqa: E402
import heure_paris  # noqa: E402

# Mots entiers qui sont une commande à l'utilisateur ; un participe (« lancée dans ce passage ») n'en est pas une.
INTERDITS = re.compile(r"(?<!\w)(?:lance|relance|exécute|lancer|relancer|exécuter|python)(?!\w)|pipelines/", re.IGNORECASE)

# Consignes destinées à Claude (pas à l'utilisateur) : elles sortent de l'affichage.
CONSIGNE = re.compile(r"(?:lance|relance|lancer|relancer) l'agent|python -I", re.IGNORECASE)

# Catégories de forme.CATEGORIES (sans accents) -> texte affiché.
AFFICHAGE = {"composition": "Composition", "tactique": "Tactique", "entrainement": "Entraînement", "transferts": "Transferts",
             "academie/draft": "Académie/Draft", "finances": "Finances", "export": "Export", "question": "Question",
             "analyse": "Analyse"}
assert set(AFFICHAGE) == set(forme.CATEGORIES)

# « il me manque <vue> (<erreur>) — export <écran> » : le bloc se déduit de l'écran demandé.
MANQUE_ECRAN = [("Finances", 8, "finances"), ("Marché", 4, "transferts"), ("Personnel", 9, "finances"),
                ("Académie", 9, "academie/draft"), ("Entraînement", 9, "entrainement"),
                ("page du dernier match", 7, "analyse")]

# (motif, bloc, catégorie) : première règle qui correspond au début du texte (ou à la forme indiquée) ; ordre = priorité.
REGLES = [
    (r"Entraînement \(", 9, "entrainement"),
    (r"Composition : minutes aux jeunes", 2, "composition"),
    (r"Composition ", 3, "composition"),
    (r"Réexporte l'aperçu", 0, "export"),
    (r"rejeu non disponible", 0, "export"),
    (r"Analyse : ", 7, "analyse"),
    (r"Finances : ", 8, "finances"),
    (r"Réduis le poste", 8, "finances"),
    (r"Semaine type déficitaire", 8, "finances"),
    (r"Vendre ", 4, "transferts"),
    (r"Mets .+ en vente", 4, "transferts"),
    (r"Enchère (?:sur|maximale) ", 4, "transferts"),
    (r"Acheter un ", 4, "transferts"),
    (r"Académie, rapport", 9, "academie/draft"),
    (r"Boucle d'apprentissage", 7, "analyse"),
    (r"Conseil \S+ à juger", 7, "analyse"),
    (r"Revue de la semaine", 7, "analyse"),
    (r"Amical contre ", 2, "composition"),
    (r"(?:Ligue|Coupe) ", 3, "composition"),
    (r"Sors ", 3, "composition"),
    (r"[^:]{1,80} : corrige à l'écran \S+ réglages", 3, "composition"),
    (r".+ blessé, retour le", 3, "composition"),
    (r".+ : fatigue \d", 3, "composition"),
    (r".+ : forme \d", 3, "composition"),
    (r"Match de ligue joué non exporté", 0, "export"),
    # actions de gold.bv_agenda
    (r"Avant .+? : preset amical", 2, "composition"),
    (r"Avant .+? : vérifier le preset de ligue", 3, "composition"),
    (r"Avant .+? : vérifier et sauvegarder les choix d'entraînement", 9, "entrainement"),
    (r"(?:Avant|Après) .+ : exporter ", 0, "export"),
]


def manque(export: str, debloque: str = "") -> str:
    """Ligne d'un bloc vide : « donnée manquante : exporte <écran> » (+ « (<ce que ça débloque>) »)."""
    return f"donnée manquante : exporte {export}" + (f" ({debloque})" if debloque else "")


def classer(action: str) -> tuple:
    """(numéro de bloc, catégorie affichée) d'après le début du texte d'une action de aujourdhui.plan()."""
    texte = action.strip()
    if texte.startswith("il me manque"):
        ecran = texte.rsplit("export ", 1)[-1]
        for mot, bloc, cat in MANQUE_ECRAN:
            if mot.lower() in ecran.lower():
                return bloc, AFFICHAGE[cat]
        return 0, AFFICHAGE["export"]
    for motif, bloc, cat in REGLES:
        if re.match(motif, texte):
            return bloc, AFFICHAGE[cat]
    return 10, AFFICHAGE["question"]


def separer(actions: list) -> tuple:
    """(actions affichables, consignes de session).

    Une action (limite, prio, action, détail, source) dont le texte est une consigne à Claude (« lance l'agent … »,
    « python -I … ») sort de l'affichage et va dans les consignes. Si seul le détail en contient une, l'action reste
    affichée avec un détail vide et le détail va dans les consignes."""
    affichables, consignes = [], []
    for a in actions:
        limite, prio, texte, detail, source = a
        if CONSIGNE.search(texte):
            consignes.append(texte + (f" — {detail}" if detail else ""))
        elif detail and CONSIGNE.search(detail):
            consignes.append(detail)
            affichables.append((limite, prio, texte, "", source))
        else:
            affichables.append(a)
    return affichables, consignes


PASTILLE = {1: "🟥 URGENT", 2: "🟧 IMPORTANT", 3: "🟩 SUIVI"}
PREFIXE_HEURE = re.compile(r"^(?:Avant|Après)\b.*? : ")
HEURE = re.compile(r"\s*\(?~?\d{1,2}:\d{2}\)?")
LIGNE_VIDE = "tout est traité côté actions ; détail des blocs 0 à 10 ci-dessous"


def sans_heure(texte: str) -> str:
    """Retire les heures HH:MM d'une action (le bloc 1 n'en porte aucune) ; « Avant 07:45 : » devient vide."""
    return HEURE.sub("", PREFIXE_HEURE.sub("", texte)).replace("  ", " ").strip()


def _ligne_plan(prio: int, texte: str) -> str:
    bloc, cat = classer(texte)
    court = sans_heure(texte).replace("|", "/")
    court = court if len(court) <= 150 else court[:149].rstrip() + "…"
    return f"| {PASTILLE.get(prio, PASTILLE[3])} | {cat} | {court} → bloc {bloc} |"


def _tableau(titre: str, actions: list) -> list:
    rangees = sorted(actions, key=lambda a: (a[1], a[0] is None, a[0] or dt.datetime.max))
    return [f"**{titre}**", "", "| Priorité | Catégorie | Action |", "|---|---|---|"] \
        + [_ligne_plan(a[1], a[2]) for a in rangees] + [""]


def bloc_1(actions: list, jour: dt.date) -> list:
    """Bloc 1 : « Aujourd'hui » puis « Demain (préparé aujourd'hui) », tableaux Priorité | Catégorie | Action, sans heures.

    Toutes les actions affichables y figurent, chacune avec « → bloc N » (le détail reste dans son bloc). Une action dont
    la limite tombe après `jour` va en « Demain » ; sinon en « Aujourd'hui ». Jamais vide."""
    affichables, _ = separer(actions)
    ajd = [a for a in affichables if not (a[0] is not None and a[0].date() > jour)]
    dem = [a for a in affichables if a[0] is not None and a[0].date() > jour]
    sortie = []
    if ajd:
        sortie += _tableau("Aujourd'hui", ajd)
    if dem:
        sortie += _tableau("Demain (préparé aujourd'hui)", dem)
    if not sortie:
        sortie = ["| Priorité | Catégorie | Action |", "|---|---|---|", f"| {PASTILLE[3]} | {AFFICHAGE['analyse']} | {LIGNE_VIDE} → bloc 0 |", ""]
    return sortie


# ---- Blocs 2 et 3 : compositions -------------------------------------------------------------------------------

BASE = comp.BASE
# Texte commun aux consignes de session des blocs 2 et 3 (amical, ligue et coupe).
ANTICIPATION = ("anticipe les décisions de l'adversaire contre nous : pour chacun de nos joueurs, le focus défensif et la zone qu'un adversaire "
                "appliquerait selon la même règle que la nôtre (parts de tirs, 2P/3P de nos joueurs, gold.bv_match_player_lines) ; compose pour "
                "rester solide si le focus tombe sur notre meilleur tireur (plan B) ; hypothèse signalée comme telle, aucune donnée sur les focus "
                "adverses en base ; sous le tableau de saisie, écris une ligne commençant exactement par « Anticipation (hypothèse) : » "
                "avec le plan B nommé")


def contrat_brief(jour: dt.date, amical: bool, adversaire: str, date_match: dt.date, manche=None, genre: str = "ligue") -> tuple:
    """(chemin du brief, première ligne) que l'agent tactique doit écrire pour que le script le retrouve :
    `brief_du_jour` exige le nom daté du jour, `adversaire_du_titre` lit l'adversaire dans la première ligne."""
    chemin = f"outputs/basketvibe/briefs/{jour.isoformat()}-tactique{'-amical' if amical else ''}.md"
    jj = f"{date_match:%d/%m}"
    if amical:
        return chemin, f"Amical contre {adversaire} ({jj})"
    if manche and genre == "ligue":
        return chemin, f"J{manche} : {adversaire} ({jj})"
    return chemin, f"{genre.capitalize()} contre {adversaire} ({jj})"


def consigne_brief(jour: dt.date, amical: bool, adversaire: str, date_match: dt.date, manche=None, genre: str = "ligue") -> str:
    """Fin de consigne commune aux lancements et relances des blocs 2 et 3 : fichier, première ligne, tableau, anticipation."""
    chemin, ligne = contrat_brief(jour, amical, adversaire, date_match, manche, genre)
    return f"écris le brief dans {chemin}, première ligne exactement « {ligne} », puis le tableau de saisie ; " + ANTICIPATION


LIGNE_ANTICIPATION = re.compile(r"^[\s>*-]*\**\s*(Anticipation \(hypothèse\)\s*:.*?)\**\s*$", re.M)
ABSENTE = "Anticipation (hypothèse) : absente du brief du jour"


def _heure_commit(fichier):
    """Horodatage (epoch) du dernier commit qui touche le fichier ; None si le fichier n'est pas suivi, hors dépôt git ou git absent."""
    f = Path(fichier).resolve()
    try:
        r = subprocess.run(["git", "-C", str(f.parent), "log", "-1", "--format=%ct", "--", f.name],
                           capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    sortie = r.stdout.strip()
    return int(sortie) if r.returncode == 0 and sortie.isdigit() else None


def produit_le(fichier) -> dt.datetime:
    """Heure de Paris (naïve) à laquelle le brief a été produit : celle de son dernier commit (`git log -1 --format=%ct`, un
    `git checkout` ne la change pas) ; la date de dernière écriture seulement si le fichier n'est pas suivi."""
    ts = _heure_commit(fichier)
    if ts is None:
        ts = os.path.getmtime(fichier)
    return heure_paris.paris(dt.datetime.fromtimestamp(ts, dt.timezone.utc)).replace(tzinfo=None)


def brief_du_jour(base, jour: dt.date, amical: bool, adversaire: str):
    """Chemin du brief tactique **daté du jour** (`AAAA-MM-JJ-tactique[-amical].md`) dont le titre nomme l'adversaire ; None sinon.
    Un brief d'un autre jour n'est jamais renvoyé."""
    f = Path(base or BASE) / "briefs" / f"{jour.isoformat()}-tactique{'-amical' if amical else ''}.md"
    if not f.is_file() or f.stat().st_size == 0:
        return None
    lignes = f.read_text(encoding="utf-8").splitlines()
    return f if lignes and auj.meme_match(comp.adversaire_du_titre(lignes[0]), adversaire) else None


def dernier_export_equipe(donnees):
    """Heure de Paris du dernier export de l'écran Équipe (gold.bv_exports_state) ; None si inconnue."""
    for r in auj.lignes_de(donnees, "gold.bv_exports_state"):
        if forme.norm(str(r["ecran"])).startswith("equipe") and r.get("dernier_paris"):
            return auj.en_heure(r["dernier_paris"])
    return None


def fiche_a_jour(fichier, apercu, export_equipe) -> bool:
    """Brief produit après l'aperçu adverse en base et après le dernier export de l'équipe (la date du jour est contrôlée par brief_du_jour)."""
    bornes = [x for x in (apercu, export_equipe) if x is not None]
    return all(produit_le(fichier) >= x for x in bornes)


def anticipation_du_brief(fichier) -> str:
    m = LIGNE_ANTICIPATION.search(Path(fichier).read_text(encoding="utf-8"))
    return m.group(1).strip() if m else ABSENTE


def _virgule(x) -> str:
    return f"{float(x):.1f}".replace(".", ",")


def verifier_j_moins_1(tableau: str, donnees) -> list:
    """Une ligne « Écart J-1 » par joueur du tableau de saisie signalé blessé, en forme basse ou hors zone verte de fatigue
    (gold.bv_daily_alerts), dont la fatigue projetée dépasse la zone verte (fatigue_avant_match) ou vendu depuis
    (transferts_recents où achete est faux). Compare à l'effectif du jour."""
    noms = []
    for cols, lignes in forme.tableaux(tableau):
        if cols and cols[0] == "joueur" and forme.idx(cols, "q1") >= 0:
            noms = [l[0].replace("*", "").strip() for l in lignes if l and l[0].strip()]
            break

    def est(cellule, complet):
        c, p = forme.norm(cellule), forme.norm(complet)
        return bool(c) and (c == p or c == p.split()[-1])

    sortie = []
    for r in auj.lignes_de(donnees, "gold.bv_daily_alerts"):
        if r.get("category") not in ("blessure", "fatigue", "forme"):
            continue
        m = re.match(r"(.+?)(?: blessé,| : )", r["alert"])
        for n in noms:
            if m and est(n, m.group(1)):
                sortie.append(f"Écart J-1 : {n} — {r['alert']}")
    for r in auj.lignes_de(donnees, "fatigue_avant_match"):
        for n in noms:
            if est(n, r["joueur"]):
                sortie.append(f"Écart J-1 : {n} — fatigue projetée {_virgule(r['sat_fatigue'])} au match de {r['kind']} du "
                              f"{auj.en_date(r['match_day']):%d/%m} contre {r['opponent']} (zone verte {r['zone_verte']})")
    for r in auj.lignes_de(donnees, "transferts_recents"):
        if auj.vrai(r.get("achete")):
            continue
        for n in noms:
            if est(n, r["name"]):
                sortie.append(f"Écart J-1 : {n} — vendu le {auj.en_date(r['settled_at']):%d/%m} ({r['to_team']})")
    return sortie


def bloc_2(donnees, S, jour: dt.date, maintenant: dt.datetime, base=None) -> tuple:
    """Bloc 2 : composition de l'amical, choisie le jour même (brief tactique du jour). (lignes affichées, consignes de session)."""
    am = auj.prochain_amical(donnees, jour, maintenant)
    if am is None:
        return ["aucun amical programmé aujourd'hui ni demain"], []
    test = auj.test_en_cours((S or {}).get("experiences"), am, auj.lignes_de(donnees, "amical_reglage"))
    quand = auj.jour_fr(am["date"])
    entete = f"Amical contre {am['match']} ({quand}), heure limite du verrou {am['limite']:%H:%M}"
    f = brief_du_jour(base, jour, True, am["match"])
    tableau = comp.composer_amical(f, test)
    if tableau is None:
        consigne = (f"lancer l'agent tactique (BasketVibe, amical du {am['date']:%d/%m}, horizon aujourd'hui) : composition de l'amical selon la "
                    "fiche tactique §2 bis, dans l'ordre : minutes aux jeunes de 21 ans ou moins (21 ans), un seul réglage testé "
                    f"({auj.texte_test(*test[:2]) if test else 'aucun test en cours'}), titulaires protégés si ligue le soir "
                    "(fatigue ajoutée de fatigue_amical) ; minutes réparties entre les joueurs ; chiffres cités, hypothèses signalées ; "
                    "jamais reprise du dernier amical ni du dernier brief ; minutes par joueur dans le tableau ; " + consigne_brief(jour, True, am["match"], am["date"]))
        return [entete, "", "composition de l'amical en préparation"], [consigne]
    lignes, consignes = [entete, "", tableau, ""], []
    ant = anticipation_du_brief(f)
    lignes.append(ant)
    if ant == ABSENTE:
        consignes.append(f"relancer l'agent tactique (BasketVibe, amical du {am['date']:%d/%m}, horizon aujourd'hui) : ajouter au brief du jour "
                         "la ligne « Anticipation (hypothèse) : … » avec le plan B nommé ; " + consigne_brief(jour, True, am["match"], am["date"]))
    lignes.append(f"Test en cours (un seul réglage à la fois) : {auj.texte_test(*test[:2])}" if test else "Test en cours : aucun")
    if any(r["competition_kind"] == "ligue" and auj.en_date(r["day"]) == am["date"] for r in auj.lignes_de(donnees, "calendrier")):
        du_jour = [r for r in auj.lignes_de(donnees, "fatigue_amical") if auj.en_date(r["match_day"]) == am["date"]]
        lignes.append("Fatigue ajoutée aux titulaires de la ligue du soir : "
                      + " ; ".join(f"{r['joueur']} +{_virgule(r['fatigue_ajoutee'])}" for r in du_jour) if du_jour
                      else manque("l'amical saisi (page du match)", "fatigue ajoutée aux titulaires de la ligue du soir"))
    lignes += verifier_j_moins_1(tableau, donnees)
    return lignes, consignes


def _matchs_ligue_coupe(donnees, jour, maintenant):
    """Matchs de ligue ou de coupe des 3 prochains jours, verrou non passé, avec les heures de capture de l'aperçu adverse."""
    matchs = {}
    for r in auj.lignes_de(donnees, "apercus_matchs"):
        m = matchs.setdefault(r["fixture_id"], {"kind": r["competition_kind"], "manche": r.get("round_no"), "jour": auj._jour(r["day"]),
                                                "adv": r["opponent"], "captures": []})
        if r.get("capture_paris"):
            m["captures"].append(auj.en_heure(r["capture_paris"]))
    sortie = []
    for m in matchs.values():
        m["limite"] = auj.verrou_calendrier(donnees, m["jour"], m["adv"])
        if m["jour"] >= jour and not (m["limite"] is not None and m["limite"] < maintenant):
            sortie.append(m)
    return sorted(sortie, key=lambda m: (m["jour"], m["adv"]))


def bloc_3(donnees, S, jour: dt.date, maintenant: dt.datetime, base=None) -> tuple:
    """Bloc 3 : composition de la ligue ou de la coupe, séparée de l'amical (elle exige l'aperçu adverse).
    Aperçu absent -> « donnée manquante » ; aperçu sans fiche à jour -> consigne de session ; fiche à jour -> tableaux + J-1."""
    if donnees.get("apercus_matchs") in (None, "rejeu"):
        return [manque("l'aperçu du prochain match de ligue ou de coupe", "bloc 3")], []
    matchs = _matchs_ligue_coupe(donnees, jour, maintenant)
    if not matchs:
        return ["aucun match de ligue ou de coupe dans les trois prochains jours"], []
    lignes, consignes = [], []
    for m in matchs:
        genre = "ligue" if m["kind"] == "ligue" else "coupe"
        jj = f"{m['jour']:%d/%m}"
        manche = f" J{m['manche']}" if m["manche"] and genre == "ligue" else ""
        entete = (f"{genre.capitalize()}{manche} contre {m['adv']} ({auj.jour_fr(m['jour'])})"
                  + (f", heure limite du verrou {m['limite']:%H:%M}" if m["limite"] else ""))
        lignes += [entete, ""]
        if not m["captures"]:
            lignes += [manque(f"l'aperçu du match de {genre} du {jj}", "bloc 3"), ""]
            continue
        f = brief_du_jour(base, jour, False, m["adv"])
        tableau = comp.composer(m["adv"], base or BASE, jour, False) if f and fiche_a_jour(f, max(m["captures"]), dernier_export_equipe(donnees)) else comp.AUCUNE
        if tableau == comp.AUCUNE:
            lignes += ["composition en préparation", ""]
            consignes.append(f"lancer l'agent tactique (BasketVibe, {genre} contre {m['adv']} du {jj}, horizon aujourd'hui) : composition et focus défensif "
                             "par adversaire d'après l'aperçu adverse en base et l'effectif du jour ; chiffres cités, hypothèses signalées ; " + consigne_brief(jour, False, m["adv"], m["jour"], m["manche"], genre))
            continue
        ant = anticipation_du_brief(f)
        lignes += [tableau, "", ant]
        if ant == ABSENTE:
            consignes.append(f"relancer l'agent tactique (BasketVibe, {genre} contre {m['adv']} du {jj}, horizon aujourd'hui) : ajouter au brief du jour "
                             "la ligne « Anticipation (hypothèse) : … » avec le plan B nommé ; " + consigne_brief(jour, False, m["adv"], m["jour"], m["manche"], genre))
        lignes += verifier_j_moins_1(tableau, donnees) + [""]
    return lignes, consignes


# ---- Bloc 4 : transferts (prix, qui acheter, qui vendre) ------------------------------------------------------

TRANCHES = ["≤21", "22-25", "26-29", "30+"]
CASE_FIABLE_N = 5  # même seuil que le reste du script (ref_n >= 5, aujourdhui.py)


def vue_illisible(nom: str) -> str:
    """Ligne d'un bloc dont la vue n'a pas pu être lue (revue ciblée 5)."""
    return f"donnée manquante : vue {nom} illisible"


def tranche_age(age) -> str:
    a = int(float(age))
    return "≤21" if a <= 21 else "22-25" if a <= 25 else "26-29" if a <= 29 else "30+"


def palier_note(ps) -> int:
    return int(float(ps) // 5 * 5)


def _virg(x, d: int = 1) -> str:
    return f"{float(x):.{d}f}".replace(".", ",")


def _cases(donnees) -> dict:
    return {(int(float(r["ps_band"])), r["age_band"]): r for r in auj.lignes_de(donnees, "prix_cases")}


def _table_prix(donnees) -> list:
    lignes = ["**Table des prix (ventes conclues, par tranche d'âge et palier de note de 5)**", "",
              "| Âge | Note (dès) | Ventes | Prix bas (p25) | Médian | Prix haut (p75) | Dernière vente |", "|---|---|---|---|---|---|---|"]
    for r in sorted(auj.lignes_de(donnees, "prix_cases"), key=lambda r: (TRANCHES.index(r["age_band"]) if r["age_band"] in TRANCHES else 9,
                                                                         int(float(r["ps_band"])))):
        lignes.append(f"| {r['age_band']} | {int(float(r['ps_band']))} | {int(float(r['n']))} | {auj.montant(r['p25'])} | {auj.montant(r['median'])} | "
                      f"{auj.montant(r['p75'])} | {auj.en_date(r['last_sale']):%d/%m} |")
    return lignes + [""]


def _export_marche(donnees):
    for r in auj.lignes_de(donnees, "gold.bv_exports_state"):
        if forme.norm(str(r["ecran"])).startswith("marche") and r.get("dernier_paris"):
            return auj.en_heure(r["dernier_paris"])
    return None


def _achetable(r, cases, capacite):
    """(plafond, achetable) d'une annonce : prix <= médiane de sa case (case fiable) et <= capacité restante."""
    prix = float(r["price_now"])
    case = cases.get((palier_note(r["ps"]), tranche_age(r["age"])))
    if case is None:
        return None, "non (case sans référence de prix)"
    mediane = float(case["median"])
    plafond = mediane if capacite is None else min(mediane, float(capacite))
    if int(float(case["n"])) < CASE_FIABLE_N:
        return plafond, f"non (case peu fiable : {int(float(case['n']))} ventes)"
    if prix > mediane:
        return plafond, "non (prix au-dessus de la médiane de la case)"
    if capacite is None:
        return plafond, "non (capacité restante illisible)"
    if prix > float(capacite):
        return plafond, "non (au-dessus de la capacité restante)"
    return plafond, "oui"


def _table_annonces(donnees, capacite) -> list:
    titre = ["**Qui acheter (annonces du Marché qui se terminent dans les 24 h)**", ""]
    vues, annonces = set(), []
    for r in auj.lignes_de(donnees, "annonces_24h"):
        if r["auction_id"] not in vues:  # la même annonce vue sur deux pages compte une fois
            vues.add(r["auction_id"])
            annonces.append(r)
    if not annonces:
        quand = _export_marche(donnees)
        n = next((int(float(r["n"])) for r in auj.lignes_de(donnees, "annonces_export")), None)
        precis = ", ".join(x for x in ((f"export du {quand:%d/%m}" if quand else ""), (f"{n} annonces" if n is not None else "")) if x)
        return titre + ["aucune annonce du Marché ne se termine dans les 24 h" + (f" ({precis})" if precis else ""), ""]
    cases = _cases(donnees)
    lignes = titre + ["| Nom | Poste | Âge | Note | Prix actuel | Médiane de la case | Plafond | Fin | Gain pour mon cinq | Achetable |",
                      "|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(annonces, key=lambda r: float(r["heures"])):
        plafond, verdict = _achetable(r, cases, capacite)
        case = cases.get((palier_note(r["ps"]), tranche_age(r["age"])))
        gain = r.get("gain_vs_my_second")
        lignes.append(f"| {r['name']} | {r['position']} | {int(float(r['age']))} | {_virg(r['ps'])} | {auj.montant(r['price_now'])} | "
                      f"{auj.montant(case['median']) if case else '—'} | {auj.montant(plafond) if plafond is not None else '—'} | "
                      f"dans {_virg(r['heures'])} h | {('+' if float(gain) > 0 else '') + _virg(gain) if gain is not None else '—'} | {verdict} |")
    return lignes + [""]


def _verdict_vente(r, tolerance):
    if auj.vrai(r.get("on_transfer_list")):
        return "déjà en vente"
    if tolerance is None:
        return "inconnu (tolérance de vente inconnue)"
    if r.get("gap") is None:
        return "nécessaire (aucun remplaçant au poste)"
    if float(r["gap"]) > float(tolerance):
        return f"nécessaire (écart de force {_virg(r['gap'])} supérieur à la tolérance {_virg(tolerance)})"
    restent = int(float(r["available_players"])) - (1 if auj.vrai(r.get("available")) else 0)
    if restent < auj.DISPONIBLES_APRES_VENTE:
        return f"nécessaire (il ne resterait que {restent} joueurs disponibles, {auj.DISPONIBLES_APRES_VENTE} requis)"
    return "vendable"


def _table_vente(donnees, tolerance) -> list:
    lignes = ["**Qui vendre (joueurs vendables et s'ils sont nécessaires)**", "",
              "| Nom | Poste | Âge | Note | Salaire hebdomadaire | Rang au poste | Minutes (4 derniers matchs de ligue) | Remplaçant | "
              "Écart de force | Prix attendu (médiane de la case) | Verdict |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    cases = _cases(donnees)
    rempl = {forme.norm(r["name"]): r for r in auj.lignes_de(donnees, "gold.bv_sell_replacement")}
    rangees = []
    for c in auj.lignes_de(donnees, "vendre"):
        r = dict(c, **{k: v for k, v in rempl.get(forme.norm(c["name"]), {}).items() if k not in c})  # remplaçant, écart, disponibles
        verdict = _verdict_vente(r, tolerance)
        case = cases.get((palier_note(r["ps"]), tranche_age(r["age"])))
        if case is None:
            prix = "—"
        elif int(float(case["n"])) < CASE_FIABLE_N:
            prix = "— (case peu fiable)"
        else:
            prix = auj.montant(case["median"])
        minutes = _virg(r["league_min_last4"]) if r.get("league_min_last4") is not None else "—"
        rangees.append((verdict != "vendable", -float(r["salary"]),
                        f"| {r['name']} | {r['position']} | {int(float(r['age']))} | {_virg(r['ps'])} | {auj.montant(r['salary'])} | "
                        f"{int(float(r['rank_in_slot']))} ({r['best_slot']}) | {minutes} | {r.get('replacement_name') or '—'} | "
                        f"{_virg(r['gap']) if r.get('gap') is not None else '—'} | {prix} | {verdict} |"))
    return lignes + [l for _, _, l in sorted(rangees)] + [""]


def bloc_4(donnees, erreurs, capacite, tolerance, actions=()) -> list:
    """Bloc 4 : table des prix, annonces des 24 h avec « achetable », qui vendre avec « vendable » / « nécessaire »,
    puis les lignes de transferts déjà produites par plan() (enchères, achats, mises en vente), sans heure.
    Une proposition reste une proposition : rien n'est acheté ni vendu sans l'accord écrit de l'utilisateur (bloc 10)."""
    sortie = []
    for noms, fabrique in ((("prix_cases",), lambda: _table_prix(donnees)),
                           (("annonces_24h",), lambda: _table_annonces(donnees, capacite)),
                           (("vendre", "gold.bv_sell_replacement"), lambda: _table_vente(donnees, tolerance))):
        illisibles = [n for n in noms if donnees.get(n) in (None, "rejeu")]
        sortie += [vue_illisible(n) for n in illisibles] + [""] if illisibles else fabrique()
    if tolerance is None and donnees.get("vendre") not in (None, "rejeu"):
        sortie += ["tolérance de vente inconnue (core.game_params.vente_tolerance_force) : aucun joueur n'est déclaré vendable", ""]
    affichables, _ = separer(list(actions))
    deja = [a for a in affichables if classer(a[2])[0] == 4]
    if deja:
        sortie += ["**Enchères, achats et ventes déjà proposés**", ""]
        sortie += ["- " + sans_heure(a[2]) + (f" — {sans_heure(a[3])}" if a[3] else "") for a in deja] + [""]
    return sortie
