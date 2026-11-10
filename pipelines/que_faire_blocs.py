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

# Budget de durée du script complet (lecture + plan + rendu) : 30 s depuis A6 (16,7 s mesurés le 10/11 avec 40 requêtes) ; PARALLELE inchangé.
BUDGET_SECONDES = 30

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
    """Horodatage (epoch) du dernier commit qui touche le fichier ; None si le fichier n'est pas suivi, modifié sans commit (A5), hors dépôt git ou git absent."""
    f = Path(fichier).resolve()
    try:
        r = subprocess.run(["git", "-C", str(f.parent), "log", "-1", "--format=%ct", "--", f.name],
                           capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    sortie = r.stdout.strip()
    if r.returncode != 0 or not sortie.isdigit():
        return None
    try:  # A5 : suivi mais modifié (ou indexé) sans commit : le contenu lu n'est pas celui du commit, on prend la date d'écriture
        etat = subprocess.run(["git", "-C", str(f.parent), "status", "--porcelain", "--", f.name], capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    return None if etat.returncode != 0 or etat.stdout.strip() else int(sortie)


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
    rempl = {str(r["player_id"]): r for r in auj.lignes_de(donnees, "gold.bv_sell_replacement")}  # A4 : par player_id, pas par nom (homonymes)
    rangees = []
    for c in auj.lignes_de(donnees, "vendre"):
        r = dict(c, **{k: v for k, v in rempl.get(str(c["player_id"]), {}).items() if k not in c})  # remplaçant, écart, disponibles
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


# ---- Blocs 0 et 6 : exports et Match Engine -------------------------------------------------------------------

DOSSIER_ETUDES = Path(__file__).resolve().parent.parent / "docs" / "etudes"
ETUDE_NOM = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)\.md$")
DEMANDE = "Pour comprendre le Match Engine, j'ai besoin de :"
SUJET_CARTE = "carte-faisabilite"  # ajustement b : lue par etat_etude, mais ni date de dernière étude ni k
SANS_VALEUR = ("", "-", "—")
SEUIL_HEBDO_H = 168  # un export hebdomadaire n'est réclamé qu'au-delà d'une semaine
HEBDO = [("standings_teams", "l'onglet Équipes de la ligue"), ("standings_players", "l'onglet Joueurs de la ligue"),
         ("standings_injuries", "l'onglet Blessés de la ligue"),
         ("club_adverse", "une page /c/<club> d'un club adverse")]
# Mot d'un export -> bloc qu'il débloque ; le premier mot rencontré dans le texte décide.
BLOC_DE = [("aperçu", 3), ("Équipe", 3), ("Effectif", 3), ("amical", 2), ("page du match", 7), ("Match de", 7), ("Marché", 4),
           ("Mes enchères", 4), ("transferts", 4), ("Finances", 8), ("Personnel", 9), ("Académie", 9), ("Entraînement", 9)]


FICHIER_TRAITEES = "demandes-traitees.md"
STATUTS_TRAITES = ("fait", "ecartee")  # normalisés (sans accent) ; tout autre statut laisse la demande active


def demandes_traitees(dossier) -> list:
    """Débuts normalisés des demandes d'export déjà traitées (fait ou écartée) dans demandes-traitees.md du dossier
    (colonnes : début de la demande | statut | date | raison) ; liste vide sans fichier."""
    f = Path(dossier) / FICHIER_TRAITEES
    if not f.is_file():
        return []
    debuts = []
    for cols, lignes in forme.tableaux(f.read_text(encoding="utf-8")):
        ist = forme.idx(cols, "statut")
        if ist < 0 or not cols or "debut" not in cols[0]:
            continue
        debuts += [forme.norm(l[0]) for l in lignes if len(l) > ist and forme.norm(l[ist]) in STATUTS_TRAITES and l[0].strip()]
    return debuts


def questions_exportees(dossier) -> dict:
    """{identifiant de question de la carte (ex. « 3b ») : date de l'export} pour les lignes de demandes-traitees.md de statut `fait`
    dont la colonne « question liée » n'est pas vide ni « — » (R3)."""
    f = Path(dossier) / FICHIER_TRAITEES
    if not f.is_file():
        return {}
    sortie = {}
    for cols, lignes in forme.tableaux(f.read_text(encoding="utf-8")):
        ist, iq, idate = forme.idx(cols, "statut"), forme.idx(cols, "question"), forme.idx(cols, "date")
        if min(ist, iq, idate) < 0:
            continue
        for l in lignes:
            if len(l) > max(ist, iq, idate) and forme.norm(l[ist]) == "fait" and l[iq].strip() not in SANS_VALEUR:
                try:
                    sortie[l[iq].strip().lower()] = dt.date.fromisoformat(l[idate].strip())
                except ValueError:
                    continue
    return sortie


def _etude(fichier: Path, date: dt.date, sujet: str, texte: str, traitees=()) -> dict:
    verdicts, lignes, resultat = [], [], None
    for cols, rangees in forme.tableaux(texte):
        iv, ie, ic = forme.idx(cols, "verdict"), forme.idx(cols, "estim", "pente"), forme.idx(cols, "ic 95")
        if iv < 0:
            continue
        for r in rangees:
            if len(r) > iv:
                verdicts.append(r[iv])
                lignes.append((r[0], r[iv]))
                if resultat is None and ie >= 0 and ic >= 0 and len(r) > max(ie, ic) and r[ic] not in SANS_VALEUR:
                    resultat = {"estime": r[ie], "ic": r[ic]}
    demandes = []
    for l in texte.splitlines():
        s = re.sub(r"^\s*[-*]\s+", "", l).strip()
        corps = forme.norm(s[len(DEMANDE):]).strip() if s.startswith(DEMANDE) else None
        if corps is not None and not any(corps.startswith(t) for t in traitees):
            demandes.append(s)
    return {"fichier": fichier.name, "date": date, "sujet": sujet, "carte": sujet == SUJET_CARTE, "verdicts": verdicts,
            "lignes": lignes, "resultat": resultat, "demandes": demandes}


def lire_etudes(dossier=DOSSIER_ETUDES) -> list:
    """Une entrée par fichier `AAAA-MM-JJ-<sujet>.md` de docs/etudes/ dont l'en-tête (6 premières lignes) ne dit pas « invalidé » ;
    le plus récent par sujet. Triées de la plus récente à la plus ancienne. Dossier absent : liste vide."""
    dossier = Path(dossier)
    if not dossier.is_dir():
        return []
    gardes, traitees, exportees = {}, demandes_traitees(dossier), questions_exportees(dossier)
    for f in sorted(dossier.glob("*.md")):
        m = ETUDE_NOM.match(f.name)
        if not m:
            continue
        texte = f.read_text(encoding="utf-8")
        if "invalid" in " ".join(texte.splitlines()[:6]).lower():
            continue
        e = _etude(f, dt.date.fromisoformat(m.group(1)), m.group(2), texte, traitees)
        e["exportees"] = exportees
        if e["sujet"] not in gardes or e["date"] > gardes[e["sujet"]]["date"]:
            gardes[e["sujet"]] = e
    return sorted(gardes.values(), key=lambda e: (e["date"], e["sujet"]), reverse=True)


def date_derniere_etude(etudes):
    """Date du dernier fichier d'étude, hors carte de faisabilité (jamais `git log`) ; None sans étude."""
    return max((e["date"] for e in etudes if not e["carte"]), default=None)


def etude_a_lancer(defaites_d_affilee: int, jour: dt.date, derniere_etude, k: int, etude_du_jour=None) -> bool:
    """3 défaites de suite en ligue ou en coupe, ou dimanche avec une dernière étude de plus de 6 jours, et dans les deux cas au moins
    un match en base joué après la dernière étude (k >= 1) ; jamais deux fois le même jour (dernière étude datée du jour ; la carte de faisabilité ne compte pas)."""
    if etude_du_jour is None:
        etude_du_jour = derniere_etude == jour
    if etude_du_jour or k < 1:
        return False
    if defaites_d_affilee >= 3:
        return True
    return jour.weekday() == 6 and (derniere_etude is None or (jour - derniere_etude).days > 6)


def _demandes(etudes) -> list:
    """(demande, date de l'étude), recopiées telles quelles, la plus récente d'abord, sans doublon."""
    vues, sortie = set(), []
    for e in etudes:
        for d in e["demandes"]:
            if d not in vues:
                vues.add(d)
                sortie.append((d, e["date"]))
    return sortie


# Entraînement : traité une fois par semaine le dimanche à minuit sur le calendrier mondial, soit 04:00 à Paris
# (skill basketvibe-entrainement, references/01-fonctionnement.md l. 2) ; weekday() : lundi = 0, dimanche = 6.
JOUR_TRAITEMENT_ENTRAINEMENT = 6
HEURE_TRAITEMENT_ENTRAINEMENT = dt.time(4, 0)


def demande_entrainement(donnees, jour: dt.date) -> list:
    """Demande d'exporter la page Entraînement la veille (samedi) et le lendemain (lundi) du traitement du dimanche. Chaque demande
    n'est écrite que le jour même (horizon = aujourd'hui) : le samedi si la page n'a pas été exportée aujourd'hui, le lundi si le
    dernier export précède le traitement (dimanche 04:00). Écran absent de gold.bv_exports_state : jamais exporté."""
    if donnees.get("gold.bv_exports_state") in (None, "rejeu"):
        return []
    dernier = next((auj.en_heure(r["dernier_paris"]) for r in auj.lignes_de(donnees, "gold.bv_exports_state")
                    if forme.norm(str(r["ecran"])).startswith("entrainement") and r.get("dernier_paris")), None)
    veille, lendemain = (JOUR_TRAITEMENT_ENTRAINEMENT - 1) % 7, (JOUR_TRAITEMENT_ENTRAINEMENT + 1) % 7
    quand = None
    if jour.weekday() == veille and (dernier is None or dernier.date() < jour):
        quand = ("veille", jour + dt.timedelta(days=1))
    elif jour.weekday() == lendemain:
        traitement = jour - dt.timedelta(days=1)
        if dernier is None or dernier < dt.datetime.combine(traitement, HEURE_TRAITEMENT_ENTRAINEMENT):
            quand = ("lendemain", traitement)
    if quand is None:
        return []
    precision = f"{quand[0]} du traitement du dimanche {quand[1]:%d/%m}"
    ecran = "la page Entraînement aujourd'hui"
    return [f"- {manque(ecran, precision)} → blocs 9 et 6"]


def bloc_de_export(texte: str, defaut: int = 0) -> int:
    bas = texte.lower()
    trouves = [(bas.find(mot.lower()), bloc) for mot, bloc in BLOC_DE if mot.lower() in bas]
    return min(trouves)[1] if trouves else defaut


def demande_courte(demande: str) -> str:
    """Forme courte d'une demande d'étude pour le bloc 0 : sans « Pour comprendre le Match Engine, j'ai besoin de : », coupée avant
    « , parce que », sans point final (R2). Le texte complet reste au bloc 6."""
    t = demande[len(DEMANDE):] if demande.startswith(DEMANDE) else demande
    return re.split(r",?\s+parce que\b", t.strip(), maxsplit=1)[0].strip().rstrip(".;")


def bloc_0(donnees, res, etudes, jour: dt.date, maintenant: dt.datetime) -> list:
    """Bloc 0 : ce qu'il faut exporter, chaque ligne avec le bloc qu'elle débloque. Contrôle par match (aperçu de ligue ou de coupe,
    page du match joué, amical), Marché (nombre de captures, sans seuil), exports hebdomadaires de l'étude (plus de 168 h, mesurés par
    page_type), puis les demandes des études, recopiées telles quelles. Jamais une commande."""
    lignes, a_faire = [], []

    def export(texte, bloc):
        a_faire.append(f"- {texte if texte.startswith(('il me manque', 'rejeu non', 'donnée manquante')) else manque(texte)} → bloc {bloc}")

    for t in res.get("exports", []):
        if t.startswith("Marché (enchères) ("):  # R4 : « exporte le Marché (plusieurs pages) (dernier export il y a N h) »
            age = t[len("Marché (enchères) ("):-1]
            export("le Marché (plusieurs pages) (" + (age if age == "jamais exporté" else f"dernier export il y a {age}") + ")", 4)
        elif not t.startswith("aperçu du match de"):  # l'aperçu se contrôle match par match, ci-dessous
            export(t, bloc_de_export(t, 3))
    if donnees.get("apercus_matchs") in (None, "rejeu"):
        export("l'aperçu du prochain match de ligue ou de coupe", 3)
    else:
        for m in _matchs_ligue_coupe(donnees, jour, maintenant):
            if not m["captures"]:
                export(f"l'aperçu du match de {'ligue' if m['kind'] == 'ligue' else 'coupe'} du {m['jour']:%d/%m}", 3)
    affichables, _ = separer(res.get("actions", []))
    for a in affichables:
        if classer(a[2])[0] == 0:
            export(sans_heure(a[2]), bloc_de_export(a[2], 0))
    a_faire += demande_entrainement(donnees, jour)

    if donnees.get("captures_marche") in (None, "rejeu"):
        lignes.append(vue_illisible("captures_marche"))
    else:
        r = next(iter(auj.lignes_de(donnees, "captures_marche")), {})
        c, m = int(float(r.get("captures") or 0)), int(float(r.get("annonces") or 0))
        quand = f" (dernière le {auj.en_heure(r['derniere_paris']):%d/%m})" if r.get("derniere_paris") else ""
        lignes.append(f"- Marché : {c} capture{'s' if c > 1 else ''}, {m} annonce{'s' if m > 1 else ''} "
                      f"vue{'s' if m > 1 else ''} depuis 24 h{quand} → bloc 4")

    if donnees.get("exports_hebdo") in (None, "rejeu"):
        lignes.append(vue_illisible("exports_hebdo"))
    else:
        derniers = {r["page_type"]: r.get("derniere_paris") for r in auj.lignes_de(donnees, "exports_hebdo")}
        for pt, libelle in HEBDO:
            d = derniers.get(pt)
            age = (maintenant - auj.en_heure(d)).total_seconds() / 3600 if d else None
            if age is None or age > SEUIL_HEBDO_H:
                a_faire.append(f"- {manque(libelle, 'jamais exporté' if age is None else f'dernier export il y a {int(age)} h')} → blocs 5 et 6")

    demandes = [f"- {demande_courte(d)} (étude du {date:%d/%m}) → bloc 6" for d, date in _demandes(etudes)]  # R2 : forme courte ; le texte complet est au bloc 6
    sortie = list(dict.fromkeys(a_faire))
    if not sortie:
        sortie = ["- aucun export à refaire : toutes les pages suivies sont à jour"]
    return sortie + lignes + demandes


def defaites_suite(donnees) -> int:
    """Défaites d'affilée en ligue ou en coupe (gold.match_objective, même valeur sur chaque ligne)."""
    vals = [int(float(r["defaites_d_affilee"])) for r in auj.lignes_de(donnees, "objectifs") if r.get("defaites_d_affilee") is not None]
    return max(vals, default=0)


# Phrase que Claude inscrit dans le registre du jour (fait-AAAA-MM-JJ.md) en lançant l'agent data-scientist en arrière-plan : le script
# ne redemande pas le lancement et écrit « étude lancée, résultat attendu » (au plus un lancement par jour, résultat non attendu).
MARQUEUR_ETUDE_LANCEE = "étude data-scientist lancée"


def bloc_6(donnees, etudes, jour: dt.date, experiences=None, fait: str = "") -> tuple:
    """Bloc 6 : Match Engine. (lignes affichées, consignes de session). Première ligne :
    « matchs ajoutés : n (ligue a, amical b ; autres clubs c) · N en base · étude à jour au JJ/MM, k de nos matchs pas encore étudiés ; c d'autres clubs » (R5). n = matchs dont la
    page de match a été captée pour la première fois depuis hier (A3, bronze.raw_pages) ; a et b : nos matchs (« ligue » comprend la coupe) ;
    c : matchs d'autres clubs (A7). N inclut les matchs d'autres clubs ; k (joués après la dernière étude) et le déclencheur de l'étude ne
    comptent que nos matchs (core.fixture) ; la carte de faisabilité ne compte ni pour la date ni pour k."""
    lignes, consignes = [], []
    derniere, k = date_derniere_etude(etudes), None
    if donnees.get("matchs_ajoutes") in (None, "rejeu"):
        lignes.append(vue_illisible("matchs_ajoutes"))
    else:
        rangees = [(auj.en_date(r["day"]), r["competition_kind"], int(float(r["n"]))) for r in auj.lignes_de(donnees, "matchs_ajoutes")]
        total = sum(n for _, _, n in rangees)
        k = sum(n for d, _, n in rangees if derniere is None or d > derniere)
        nos = total
        veille = jour - dt.timedelta(days=1)
        autres_ok = donnees.get("matchs_autres") not in (None, "rejeu")
        autres = auj.lignes_de(donnees, "matchs_autres") if autres_ok else []
        # R5 : « k de nos matchs pas encore étudiés ; c d'autres clubs » (c = matchs d'autres clubs dont la page a été captée pour la première
        # fois après la dernière étude, ou jamais étudiés s'il n'y a pas d'étude) ; vue illisible : déjà dite dans la première partie de la ligne
        c_etude = sum(1 for r in autres if r.get("premiere_jour") and (derniere is None or auj.en_date(r["premiere_jour"]) > derniere))
        reste = f"{k if derniere else nos} de nos matchs pas encore étudiés" + (f" ; {c_etude} d'autres clubs" if autres_ok else "")
        suite = f"étude à jour au {derniere:%d/%m}, {reste}" if derniere else f"aucune étude encore, {reste}"
        total += len(autres)  # A7 : N inclut les matchs d'autres clubs ; k (ci-dessus) et le déclencheur restent ceux de nos matchs
        if donnees.get("matchs_captes") in (None, "rejeu"):
            ajoutes = vue_illisible("matchs_captes")
        else:  # A3 : pages de match captées pour la première fois depuis hier (et non matchs joués depuis hier)
            neuves = [r["kind"] for r in auj.lignes_de(donnees, "matchs_captes") if auj.en_date(r["premiere_jour"]) >= veille]
            a, b = sum(1 for t in neuves if t != "friendly"), sum(1 for t in neuves if t == "friendly")
            if autres_ok:
                c = sum(1 for r in autres if r.get("premiere_jour") and auj.en_date(r["premiere_jour"]) >= veille)
                ajoutes = f"{a + b + c} (ligue {a}, amical {b} ; autres clubs {c})"
            else:
                ajoutes = f"{a + b} (ligue {a}, amical {b} ; autres clubs {vue_illisible('matchs_autres')})"
        lignes.append(f"matchs ajoutés : {ajoutes} · {total} en base · {suite}")
    lignes += [f"{d} (étude du {date:%d/%m})" for d, date in _demandes(etudes)]

    prochaine = None
    if experiences and experiences.get("file"):
        v = auj.verifier(experiences, auj.lignes_de(donnees, "amical_reglage"))
        lignes.append("Avancement des expériences : " + " ; ".join(auj.texte_avancement(e, v[e["id"]]) for e in experiences["file"]))
        e = next((e for e in experiences["file"] if v[e["id"]]["verifies"] < int(e["amicaux_vises"])), None)
        prochaine = f"{e['id']} — {e['reglage']}" if e else None
        lignes.append(f"prochaine hypothèse : {prochaine}" if prochaine else "prochaine hypothèse : file d'expériences terminée")

    if k is not None and etude_a_lancer(defaites_suite(donnees), jour, derniere, k):
        ouverte = next((e for e in etudes if not e["carte"] and any("indéterminé" in x or "donnée absente" in x for x in e["verdicts"])), None)
        question = f"{ouverte['sujet']} (étude du {ouverte['date']:%d/%m})" if ouverte else (prochaine or "prochaine hypothèse de la file d'expériences")
        if MARQUEUR_ETUDE_LANCEE in fait.lower().replace("’", "'"):
            lignes.append("étude lancée, résultat attendu")
        else:
            consignes.append(f"lancer l'agent data-scientist (BasketVibe, horizon aujourd'hui) en arrière-plan (un lancement a duré plus de 19 minutes) "
                             f"sur la question ouverte : {question} ; n'attends pas son résultat ; au plus une fois par jour : inscris d'abord "
                             f"« {MARQUEUR_ETUDE_LANCEE} à HH:MM » dans le registre du jour outputs/basketvibe/fait-AAAA-MM-JJ.md, puis affiche "
                             "« étude lancée, résultat attendu » sous le bloc 6 ; "
                             "ne demande un export que pour les groupes de moteur encore ouverts (v4 ligue, v5 amical)")
    return lignes, consignes


# ---- Blocs 5, 7, 8, 9, 10 et assemblage ------------------------------------------------------------------------

SUJET_BLOC: dict = {}  # sujet d'étude -> bloc (5, 8 ou 9) ; vide en 5n, remplie en 5o quand les études de ces blocs existent
QUESTIONS_BLOC = {5: ("3",), 8: ("2", "4"), 9: ("5",)}  # chiffre initial des questions de la carte de faisabilité rattachées au bloc
VUES_BLOC = {8: ("gold.bv_finance_health", "gold.bv_finance_projection"),
             9: ("gold.bv_personnel_status", "prospects", "cote_potentiel", "gold.bv_saisie_entrainement")}
TITRES = ["Exports d'abord", "À faire aujourd'hui, puis demain", "Composition de l'amical", "Composition de la ligue ou de la coupe",
          "Transferts", "Les meilleurs et les failles du jeu", "Match Engine", "Analyse détaillée", "Économie",
          "Académie, personnel, entraînement", "À valider par l'utilisateur"]
PROPOSITION = re.compile(r"Vendre |Mets .+ en vente|Enchère (?:sur|maximale) |Acheter un ")


def etat_etude(etudes, bloc: int) -> str:
    """État de l'étude d'un bloc (5, 8 ou 9) : dernier résultat d'une étude rattachée au bloc (table SUJET_BLOC), sinon ce que la carte
    de faisabilité dit des questions du bloc (faisable ou bloquée par : exporte X), sinon « étude pas encore commencée ». Jamais « reporté »."""
    for e in etudes:
        if not e["carte"] and SUJET_BLOC.get(e["sujet"]) == bloc and e["resultat"]:
            return f"dernier résultat du {e['date']:%d/%m} : {e['resultat']['estime']} {e['resultat']['ic']}"
    carte = next((e for e in etudes if e["carte"]), None)
    if carte is None:
        return "étude pas encore commencée, carte de faisabilité à faire"
    questions = [(q, v) for q, v in carte["lignes"] if q[:1] in QUESTIONS_BLOC.get(bloc, ())]
    if not questions:
        return f"étude pas encore commencée (la carte de faisabilité du {carte['date']:%d/%m} ne couvre pas ce bloc)"
    exportees = carte.get("exportees", {})  # R3 : demande « fait » liée à la question : l'export est arrivé, l'étude reste à lancer

    def verdict(q, v):
        d = exportees.get(q.split()[0].lower()) if q.split() else None
        return f"export reçu le {d:%d/%m}, étude à lancer" if d else v
    return f"carte de faisabilité du {carte['date']:%d/%m} : " + " ; ".join(f"{q} : {verdict(q, v)}" for q, v in questions)


def bloc_5(etudes) -> list:
    return [etat_etude(etudes, 5)]


def _lignes_plan(actions, n: int, erreurs=()) -> list:
    """Lignes de plan() rangées dans le bloc n, inchangées (sans heure) ; une ligne « il me manque <vue> » dont la vue est
    déjà signalée illisible par le bloc n'est pas répétée."""
    affichables, _ = separer(list(actions))
    return ["- " + sans_heure(a[2]) + (f" — {sans_heure(a[3])}" if a[3] else "") for a in affichables
            if classer(a[2])[0] == n and not any(a[2].startswith(f"il me manque {v} ") for v in erreurs)]


def bloc_7(actions, donnees, analyste=None) -> list:
    """Bloc 7 : toujours une ligne d'état en tête (dernière défaite de ligue ou de coupe, analyse faite ou non), puis les lignes du plan."""
    if donnees.get("dernier_officiel") in (None, "rejeu"):
        etat = vue_illisible("dernier_officiel")
    else:
        o = auj.lignes_de(donnees, "dernier_officiel")
        if o and str(o[0]["my_result"]) == "L":
            d = auj.en_date(o[0]["day"])
            etat = f"défaite du {d:%d/%m} : " + ("analyse faite" if analyste is not None and analyste >= d else "analyse non faite, lancée dans ce passage")
        else:
            etat = "aucune défaite de ligue ou de coupe non analysée"
    return [etat] + _lignes_plan(actions, 7)


def _bloc_economie_ou_vie(actions, etudes, bloc: int, constats, vide: str, erreurs) -> list:
    illisibles = [vue_illisible(v) for v in VUES_BLOC[bloc] if v in erreurs]
    lignes = _lignes_plan(actions, bloc, erreurs)
    sortie = [etat_etude(etudes, bloc)] + [f"- {x}" for x in illisibles] + lignes
    if not lignes and not illisibles:
        sortie += [f"- {c}" for c in constats] or [f"- {vide}"]
    return sortie


def bloc_8(actions, etudes, garder=(), erreurs=()) -> list:
    """Bloc 8 : état de l'étude, lignes de finances du plan inchangées ; sans ligne, le constat chiffré de `garder` (finances)."""
    return _bloc_economie_ou_vie(actions, etudes, 8, [g for g in garder if g.lower().startswith("finances")],
                                 "aucune règle de finances déclenchée", erreurs)


def bloc_9(actions, etudes, garder=(), erreurs=()) -> list:
    """Bloc 9 : état de l'étude, lignes d'académie, de personnel et d'entraînement du plan inchangées."""
    return _bloc_economie_ou_vie(actions, etudes, 9, [], "aucune règle d'académie, de personnel ou d'entraînement déclenchée", erreurs)


def bloc_10(actions, garder) -> list:
    """Bloc 10 : propositions d'achat, de vente et d'enchère qui attendent l'accord écrit, puis les règles « à valider » du jour."""
    affichables, _ = separer(list(actions))
    sortie = [f"- à valider par écrit : {sans_heure(a[2])}" for a in affichables
              if PROPOSITION.match(a[2]) and "aucune annonce" not in a[2]]  # « Acheter un X : aucune annonce » est un besoin, rien à valider
    sortie += [f"- {g}" for g in garder if "à valider" in g or "non tranchée" in g]
    return sortie or ["- aucune décision n'attend ton accord écrit"]


def rendre_blocs(res, donnees, erreurs, jour: dt.date, maintenant: dt.datetime, S, etudes=None, base=None, fait: str = "") -> tuple:
    """(texte des blocs 0 à 10, consignes de session). Les consignes (lancer un agent) ne sont jamais dans le texte. Une vue
    illisible donne une ligne « donnée manquante : vue <nom> illisible » dans son bloc, sans faire échouer le rendu."""
    S = S or {}
    etudes = lire_etudes() if etudes is None else etudes
    erreurs = erreurs or {}
    actions, garder = res.get("actions", []), res.get("garder", [])
    tol = next((r["value"] for r in auj.lignes_de(donnees, "tolerance_vente")), None)
    tol = float(tol) if tol not in (None, "") else None
    b2, c2 = bloc_2(donnees, S, jour, maintenant, base)
    b3, c3 = bloc_3(donnees, S, jour, maintenant, base)
    b6, c6 = bloc_6(donnees, etudes, jour, S.get("experiences"), fait)
    blocs = [bloc_0(donnees, res, etudes, jour, maintenant), bloc_1(actions, jour), b2, b3,
             bloc_4(donnees, erreurs, res.get("capacite"), tol, actions), bloc_5(etudes), b6,
             bloc_7(actions, donnees, S.get("analyste")), bloc_8(actions, etudes, garder, erreurs), bloc_9(actions, etudes, garder, erreurs),
             bloc_10(actions, garder)]
    texte = []
    for n, (titre, lignes) in enumerate(zip(TITRES, blocs)):
        texte += [f"## Bloc {n} — {titre}", ""] + list(lignes) + [""]
    return "\n".join(texte).rstrip() + "\n", separer(actions)[1] + c2 + c3 + c6
