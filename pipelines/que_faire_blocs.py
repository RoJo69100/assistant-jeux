"""Le « que faire » BasketVibe en 11 blocs (étape 5n), gabarit : docs/attentes/gabarit-que-faire-basketvibe.md.

Plan : docs/refonte-v3/plan-5n-que-faire.md. Ce module range les actions de aujourdhui.plan() dans les blocs 0 à 10
et rend le document. Règle commune : un bloc vide s'écrit « donnée manquante : exporte <écran> », jamais une commande.
"""
import datetime as dt
import os
import re
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
                "adverses en base")
LIGNE_ANTICIPATION = re.compile(r"^[\s>*-]*\**\s*(Anticipation \(hypothèse\)\s*:.*?)\**\s*$", re.M)
ABSENTE = "Anticipation (hypothèse) : absente du brief du jour"


def produit_le(fichier) -> dt.datetime:
    """Heure de Paris (naïve) de dernière écriture du fichier : le moment où le brief a été produit."""
    return heure_paris.paris(dt.datetime.fromtimestamp(os.path.getmtime(fichier), dt.timezone.utc)).replace(tzinfo=None)


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
                    "jamais reprise du dernier amical ni du dernier brief ; minutes par joueur dans le tableau ; " + ANTICIPATION)
        return [entete, "", "composition de l'amical en préparation"], [consigne]
    lignes, consignes = [entete, "", tableau, ""], []
    ant = anticipation_du_brief(f)
    lignes.append(ant)
    if ant == ABSENTE:
        consignes.append(f"relancer l'agent tactique (BasketVibe, amical du {am['date']:%d/%m}, horizon aujourd'hui) : ajouter au brief du jour "
                         "la ligne « Anticipation (hypothèse) : … » avec le plan B nommé ; " + ANTICIPATION)
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
                             "par adversaire d'après l'aperçu adverse en base et l'effectif du jour ; chiffres cités, hypothèses signalées ; " + ANTICIPATION)
            continue
        ant = anticipation_du_brief(f)
        lignes += [tableau, "", ant]
        if ant == ABSENTE:
            consignes.append(f"relancer l'agent tactique (BasketVibe, {genre} contre {m['adv']} du {jj}, horizon aujourd'hui) : ajouter au brief du jour "
                             "la ligne « Anticipation (hypothèse) : … » avec le plan B nommé ; " + ANTICIPATION)
        lignes += verifier_j_moins_1(tableau, donnees) + [""]
    return lignes, consignes
