"""Test de pipelines/aujourdhui.py et aujourdhui_sources.py sur des données figées (sans réseau ni base).

Jeu d'essai : pipelines/jeu_essai/2026-11-06/ (copie des briefs, du registre, des learnings et du dossier du 06/11).
Critères L1-L4, F1-F2, D1 : docs/refonte-v3/journal-aujourdhui.md.
Lancer : python pipelines/test_aujourdhui.py   (code 1 si un cas se trompe)
"""
import datetime as dt
import importlib.util
import re
import sys
import tempfile
from pathlib import Path

DOSSIER = Path(__file__).resolve().parent
sys.path.insert(0, str(DOSSIER))
spec = importlib.util.spec_from_file_location("aujourdhui", DOSSIER / "aujourdhui.py")
auj = importlib.util.module_from_spec(spec)
spec.loader.exec_module(auj)
src = auj.src

JOUR = dt.date(2026, 11, 6)
SOIR = dt.datetime(2026, 11, 6, 19, 0)
ESSAI = DOSSIER / "jeu_essai" / "2026-11-06"
JOUR9 = dt.date(2026, 11, 9)  # jeu d'essai du 09/11 : briefs et registre du 08/11 (critères PB5 à PB9)
ESSAI9 = DOSSIER / "jeu_essai" / "2026-11-09"
TOT = dt.datetime(2026, 11, 9, 6, 0)
FAIT = (ESSAI / "fait-2026-11-06.md").read_text(encoding="utf-8").lower().replace("’", "'")
DECISIONS = [{"id": 1076, "label": "Enchères 07-08/11 : Fujita C (max 150 000) et Stankevičius SF (max 100 000)",
              "hypothesis": "Un C de PS 55,5 améliore le titulaire Fournier (52,4)"}]
ENCHERES = [{"name": "Yuma Fujita", "fin_paris": "2026-11-08T03:50:46.834"},
            {"name": "Bronius Stankevičius", "fin_paris": "2026-11-08T03:46:12.027"}]
AGENDA = (["day", "at_time", "priority", "category", "action"], [
    (JOUR, "20:50", 2, "export", "Après le match (~20:50) : exporter la page du match J3"),
    (JOUR + dt.timedelta(days=1), "07:45", 1, "amical", "Avant 07:45 : preset amical sur le match contre Knight Jays (domicile)"),
    (JOUR + dt.timedelta(days=1), "08:55", 3, "export", "Après l'amical (~08:55) : exporter la page du match"),
    (JOUR + dt.timedelta(days=3), "04:30", 1, "export", "trop loin"),
])


def figees(**remplace):
    d = {
        "gold.bv_agenda": AGENDA,
        "gold.bv_exports_state": (["ordre", "ecran", "pour_quoi", "dernier_paris", "age_h", "statut"], [
            (1, "Équipe (aperçu, joueurs)", "effectif", None, 5, "🟩 à jour"),
            (8, "Marché (enchères)", "cibles", None, 3, "🟩 à jour"),
            (13, "Personnel", "staff", None, None, "🟥 jamais"),
            (9, "Mes enchères", "ventes", None, 51, "🟧 à refaire"),
        ]),
        "gold.bv_daily_alerts": (["priority", "category", "alert"], [
            (2, "fatigue", "Dupont : fatigue 25 (hors zone verte)"),
            (3, "export", "Finances : dernier export il y a 8 jour(s)"),
        ]),
        "gold.bv_finance_health": (["weekly_result_est", "weekly_personnel", "weekly_academy"], [(108847, 60000, 100000)]),
        "gold.bv_position_summary": (["position", "depth", "ps_avg", "ps_max"], [
            ("PG", 3, 49.4, 56.2), ("SG", 4, 46.4, 51.6), ("C", 3, 49.4, 52.4)]),
        "gold.bv_market_bargains": (["name", "position", "ps", "ref_n", "ref_reliable", "bid_ceiling_resale",
                                     "resale_margin_p25", "ends_paris"], [
            ("Martin", "PG", 57.0, 9, True, 120000, 40000, "2026-11-07T10:00:00"),
            ("Yuma Fujita", "C", 55.5, 9, True, 735722, 700000, "2026-11-08T03:50:00")]),
        "gold.bv_market_candidates": (["name", "position", "ps", "would_rank_in_slot", "enters_top8", "current_price", "ends_paris"], []),
        "gold.bv_personnel_status": (["week", "role", "hired", "slots"], [("2026-11-02", "médecin", 2, 2), ("2026-11-02", "marketing", 0, 2)]),
        "capacite": (["capacite_invest"], [(279666,)]),
        "joueurs_declin": (["name", "age"], []),
        "decisions_achat": (["id", "label", "hypothesis"], [(d["id"], d["label"], d["hypothesis"]) for d in DECISIONS]),
        "encheres_ouvertes": (["name", "fin_paris"], [(e["name"], e["fin_paris"]) for e in ENCHERES]),
        "apercus": (["match_day"], []),
        "derniere_vente": (["derniere"], [(dt.date(2026, 11, 5),)]),
    }
    d.update(remplace)
    return d


def sources_essai(base=ESSAI):
    return {"tactique": src.lire_tactique(base, JOUR), "restes": src.lire_restes(base, JOUR),
            "cibles": src.lire_cibles(DECISIONS, ENCHERES, base, JOUR), "conseils": src.lire_conseils(base, JOUR)}


def texte(donnees, erreurs=None, fait="", sources=None, maintenant=SOIR):
    return auj.rendre(auj.plan(donnees, erreurs or {}, JOUR, maintenant, fait, sources), JOUR, erreurs)


def cas():
    S = sources_essai()
    t = texte(figees(), fait=FAIT, sources=S)
    lignes = t.splitlines()
    # L1 : briefs tactique du jour
    yield "L1 ligue : Póvoa 19:45", any(l.startswith("19:45") and "Póvoa" in l for l in lignes)
    yield "L1 amical : Knight Jays 07:45", any(l.startswith("07:45") and "Knight Jays" in l for l in lignes)
    yield "L1 tests « prouvera que j'avais tort » lus", "Faux si" in t and "Test 1" in t
    yield "L1 les 3 conditions du Test 1 en entier", \
        "Test 1 (Lefebvre Q1-Q2-Q4) : Q2 inférieur à −5 ou Q3 inférieur à +3 ou rebond offensif sous 9" in t
    yield "L1 les 2 conditions de l'amical en entier", "Faux si opp_fg2_pct > 53,4 %" in t \
        and "Faux si Dang, Albano ou Ungureanu commettent plus de fautes que le reste du cinq ou si opp_ft_rate dépasse celui de la ligue" in t
    povoa = next(l for l in lignes if "Póvoa" in l)
    yield "L1 Póvoa : heure limite et conditions, ni « rien à ressaisir » ni « saisie déclarée faite »", \
        "heure limite du verrou 19:45" in povoa and "Test 1" in povoa and "ressaisir" not in t and "saisie déclarée" not in t \
        and "saisis la tactique" not in t
    yield "L1 sans registre : saisie demandée", "saisis la tactique maintenant" in texte(figees(), sources=S)
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "briefs").mkdir()
        vieux = (ESSAI / "briefs" / "2026-11-06-tactique.md").read_text(encoding="utf-8").replace("sam. 07/11", "ven. 06/11")
        (Path(tmp) / "briefs" / "2026-11-01-tactique.md").write_text(vieux, encoding="utf-8")
        tv = src.lire_tactique(tmp, JOUR)
        yield "L1 brief de 5 jours pour un match du jour : signalé", len(tv) == 1 and tv[0]["vieux"] and tv[0]["age"] == 5 \
            and "vieux de 5 jours" in texte(figees(), sources={"tactique": tv})
        yield "L1 brief absent : lecteur vide", src.lire_tactique(tmp + "/inexistant", JOUR) == []
    # L2 : cibles d'achat
    yield "L2 Fujita 150 000", any("Fujita" in l and "150 000" in l for l in lignes)
    yield "L2 Stankevičius 100 000", any("Stankevičius" in l and "100 000" in l for l in lignes)
    yield "L2 police absente : police d'abord", sum("police d'abord" in l for l in lignes) == 2
    yield "L2 aucune cible ni source ne montre un numéro de décision", not re.search(r"\bD-\d+", t)
    yield "L2 fin d'enchère en tête de ligne (03:50)", any(l.startswith("03:50") and "Fujita" in l for l in lignes)
    yield "L2 pas de 2e ligne (bonne affaire) sur une cible décidée", t.count("Fujita") == 1
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "police-2026-11-06.md").write_text("police faite", encoding="utf-8")
        c = src.lire_cibles(DECISIONS, ENCHERES, tmp, JOUR)
        yield "L2 police du jour présente : police faite", all(x["police"] for x in c) \
            and "police faite" in texte(figees(), sources={"cibles": c})
    # L3 : registre « reste à corriger »
    yield "L3 quatre réglages à corriger", "4 réglages" in t
    yield "L3 réglages regroupés", "Agress. 1 : Dang, Albano, Ungureanu ; Tir 1 : Albano" in t
    yield "L3 la saisie déclarée n'est pas seulement retirée", sum("Knight Jays" in l for l in lignes) == 1
    # L4 : conseils à échéance
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "learnings.md").write_text(
            "| C-900 | 2026-11-05 | Juger Fuchs | Test après le match du 07/11 | ouvert | |\n"
            "| C-901 | 2026-11-05 | Autre | Test le 07/11 | **appliqué** | |\n"
            "| C-902 | 2026-11-05 | Loin | Test le 20/11 | ouvert | |\n", encoding="utf-8")
        cs = src.lire_conseils(tmp, JOUR)
        yield "L4 conseil ouvert à échéance demain lu, les autres écartés", [c["id"] for c in cs] == ["C-900"]
        yield "L4 conseil dans le plan", "C-900" in texte(figees(), sources={"conseils": cs}) or "C-900" in texte(figees(), sources={"conseils": cs})
    # F1 : format
    yield "F1 au plus 8 lignes", len(lignes) <= 8
    yield "F1 chaque ligne d'action : HH:MM — action", all(re.match(r"^(\d\d:\d\d|--:--) — ", l) for l in lignes
                                                           if not l.startswith(("Autres points", "Garder", "Exports à faire")))
    yield "F1 dernière ligne = exports", lignes[-1].startswith("Exports à faire aujourd'hui :")
    yield "F1 aucune ligne clé=valeur", not re.search(r"\w+=\S+", t)
    heures = [l[:5] for l in lignes if re.match(r"^\d\d:\d\d", l)]
    yield "F1 triées par échéance complète (06/11 20:50, 07/11 07:45 et 19:45, 08/11 03:46 et 03:50)", \
        heures == ["20:50", "07:45", "19:45", "03:46", "03:50"]
    beaucoup = [(dt.datetime(2026, 11, 6, 20, i), 2, f"action {i}", "", "") for i in range(7)]
    tb = auj.rendre({"actions": beaucoup, "exports": [], "garder": []}, JOUR).splitlines()
    yield "F1 surplus dans « Autres points », toujours 8 lignes au plus", len(tb) <= 8 and tb[-2].startswith("Autres points (2)")
    # F2 : Personnel
    yield "F2 Personnel étiqueté Personnel", "Personnel (médecin 2/2" in t
    # D1 : décisions par secteur
    yield "D1 poste le plus faible : garder en demi-ligne, pas en ligne", \
        "Garder : effectif, acheter : seuil non atteint (le poste le plus faible, SG" in t \
        and not any(l.startswith(("--:--", "0", "1", "2")) and "effectif" in l for l in lignes)
    yield "D1 finances : garder si résultat hebdo positif", "finances : seuil non atteint (résultat hebdo estimé +108 847" in t
    garder = next(l for l in lignes if l.startswith("Garder"))
    yield "D1 Garder dit pourquoi, secteur par secteur (rien de vendable, règle non écrite, seuil non atteint)", \
        "vendre : rien de vendable" in garder and "vendre pour profit : règle non écrite — à valider" in garder \
        and "jeunes : règle non écrite — à valider" in garder and "seuil non atteint" in garder
    vieux = figees(**{"joueurs_declin": (["name", "age"], [("Vétéran", 33)])})
    yield "D1 joueur de 31 ans ou plus : vendre", "Mets Vétéran en vente (33 ans" in texte(vieux) \
        and "rien de vendable" not in texte(vieux)
    yield "D1 capacité restante suivie de la réserve à valider", "Capacité restante (réserve de sécurité à valider)" not in t \
        and "capacité restante (réserve de sécurité à valider) : 29 666" in t
    mince = figees(**{"gold.bv_position_summary": (["position", "depth", "ps_avg", "ps_max"], [("PG", 2, 49.4, 56.2), ("SG", 4, 46.4, 51.6)])})
    yield "D1 EFF-1 : poste mince = acheter un PG de note ≥ 57,2", "Acheter un PG de note ≥ 57,2" in texte(mince)
    rouge = figees(**{"gold.bv_finance_health": (["weekly_result_est", "weekly_personnel", "weekly_academy"], [(-5000, 60000, 100000)])})
    yield "D1 FIN-1 : résultat négatif = réduire le plus gros poste", "Réduis le poste académie (100 000" in texte(rouge)
    yield "D1 TRF-1 : affaire fiable = enchère maximale", "Enchère maximale 120 000 sur Martin" in texte(figees())
    yield "D1 E8 : capacité restante (279 666 − 250 000 décidés) trop faible = affaire abandonnée", \
        "Martin" not in t and "ce que le club peut investir après les enchères déjà décidées" in t and ": 29 666)" in t
    perime = figees(**{"gold.bv_exports_state": (["ordre", "ecran", "pour_quoi", "dernier_paris", "age_h", "statut"],
                                                 [(8, "Marché (enchères)", "cibles", None, 30, "🟧 à refaire")])})
    tp = texte(perime)
    yield "D1 TRF-4 : Marché périmé = pas d'enchère, ligne Export", "Marché (enchères) (30 h)" in tp and "Martin" not in tp
    # Lisibilité : ni coupure par « … », ni code interne, une ligne longue passe sur plusieurs lignes d'affichage
    alerte = figees(**{"gold.bv_daily_alerts": (["priority", "category", "alert"], [
        (1, "blessure", "Gimenez blessé : absent 3 jours, retire-le du cinq de départ avant le verrou")])})
    ta = texte(alerte, fait=FAIT, sources=S)
    autres = next((l for l in ta.splitlines() if l.startswith("Autres points")), "")
    yield "Alerte : un joueur blessé s'affiche en entier dans « Autres points »", \
        "Gimenez blessé : absent 3 jours, retire-le du cinq de départ avant le verrou" in autres
    interne = re.compile(r"\b(EFF|FIN|TRF)-\d|\bE8\b|\bD-\d+|\bL-\d+")
    sortie = [t, ta, texte(mince), texte(rouge), texte(perime)]
    yield "Aucun code interne dans la sortie", not any(interne.search(x) for x in sortie)
    yield "Aucune ligne coupée par « … »", not any("…" in x for x in sortie)
    pl = auj.plier(ta)
    yield "Repli : lignes d'affichage de 100 caractères au plus, rien perdu", \
        all(len(l) <= 100 for l in pl.splitlines()) and len(pl.splitlines()) > len(ta.splitlines()) \
        and re.sub(r"\s+", " ", pl) == re.sub(r"\s+", " ", ta)
    yield "Repli : un montant ne se coupe pas", "150 000" in pl and "100 000" in pl
    # comportements conservés
    ap = texte(figees(), sources=S)
    yield "export en retard nommé dans la ligne finale", "Mes enchères (51 h)" in ap and "Personnel (jamais exporté)" in ap
    yield "registre : export déjà fait non redemandé", "Mes enchères" not in t and "Personnel (jamais" not in t
    yield "agenda : jour lointain écarté", "trop loin" not in t
    yield "agenda : export d'après-match de demain écarté", "08:55" not in t
    yield "agenda : export du jour gardé", "20:50 — Après le match" in ap
    yield "alerte export non doublée", "Finances : dernier export il y a 8" not in t
    yield "aperçu demandé (aucune ligne adverse)", "aperçu du match de ligue du 06/11" in texte(figees(**{"gold.bv_agenda": (
        AGENDA[0], [(JOUR, "19:45", 1, "ligue", "Avant 19:45 : focus du match J3 contre Póvoa")])}))
    yield "historique des transferts demandé (vente du 03/11)", "historique global des transferts depuis 2026-11-03" in texte(
        figees(**{"derniere_vente": (["derniere"], [(dt.date(2026, 11, 3),)])}))
    yield "donnée absente", "il me manque gold.bv_finance_health" in texte(
        figees(**{"gold.bv_finance_health": None}), {"gold.bv_finance_health": "boum"})
    yield "rejeu non disponible", "rejeu non disponible pour gold.bv_agenda" in texte(figees(**{"gold.bv_agenda": "rejeu"}))
    yield "après 18:00 : demain avant 10:00 ajouté", "tôt demain" in texte(figees(**{"gold.bv_agenda": (
        AGENDA[0], [(JOUR + dt.timedelta(days=1), "04:30", 1, "entraînement", "tôt demain")])}))
    yield "avant 18:00 : demain non ajouté", "tôt demain" not in texte(figees(**{"gold.bv_agenda": (
        AGENDA[0], [(JOUR + dt.timedelta(days=1), "04:30", 1, "entraînement", "tôt demain")])}), maintenant=dt.datetime(2026, 11, 6, 12, 0))
    # PB5 : une saisie déclarée dans un registre antérieur retire l'action de saisie
    vide = figees(**{"gold.bv_agenda": (AGENDA[0], [])})
    saisies = src.lire_saisies(ESSAI9, JOUR9)
    yield "PB5 la ligne de 10:34 UTC du 08/11 est lue : Garden City, 09/11", \
        [(s["match"], s["date"]) for s in saisies] == [("Garden City", JOUR9)]
    tactique9 = src.lire_tactique(ESSAI9, JOUR9)
    avec = auj.rendre(auj.plan(vide, {}, JOUR9, TOT, "", {"tactique": tactique9, "saisies": saisies}), JOUR9)
    sans = auj.rendre(auj.plan(vide, {}, JOUR9, TOT, "", {"tactique": tactique9, "saisies": []}), JOUR9)
    garden = next(l for l in avec.splitlines() if "Garden City" in l)
    yield "PB5 Garden City : la ligne reste (verrou, test) sans « saisis la tactique »", \
        garden.startswith("07:45") and "heure limite du verrou 07:45" in garden and "saisis la tactique" not in garden
    yield "PB5 sans la déclaration : « saisis la tactique » pour Garden City", \
        "saisis la tactique maintenant" in next(l for l in sans.splitlines() if "Garden City" in l)
    yield "PB5 la ligue non déclarée (Naked Spartans) reste à saisir", \
        "saisis la tactique maintenant" in next(l for l in avec.splitlines() if "Naked Spartans" in l)
    yield "PB5 une saisie datée d'un jour passé n'est pas retenue", \
        src.lire_saisies(ESSAI9, dt.date(2026, 11, 10)) == []


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    echecs = 0
    for nom, ok in cas():
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    n = sum(1 for _ in cas())
    print(f"{n - echecs}/{n}")
    sys.exit(1 if echecs else 0)
