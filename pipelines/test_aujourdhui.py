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
        "gold.bv_finance_health": (["balance", "weekly_result_est", "weekly_personnel", "weekly_academy"], [(279666, 108847, 60000, 100000)]),
        "gold.bv_position_summary": (["position", "depth", "ps_avg", "ps_max"], [
            ("PG", 3, 49.4, 56.2), ("SG", 4, 46.4, 51.6), ("C", 3, 49.4, 52.4)]),
        "gold.bv_market_bargains": (["name", "position", "ps", "ref_n", "ref_reliable", "bid_ceiling_resale",
                                     "resale_margin_p25", "ends_paris"], [
            ("Martin", "PG", 57.0, 9, True, 120000, 40000, "2026-11-07T10:00:00"),
            ("Yuma Fujita", "C", 55.5, 9, True, 735722, 700000, "2026-11-08T03:50:00")]),
        "gold.bv_market_candidates": (["name", "position", "ps", "would_rank_in_slot", "enters_top8", "current_price", "ends_paris"], []),
        "gold.bv_personnel_status": (["week", "role", "hired", "slots"], [("2026-11-02", "médecin", 2, 2), ("2026-11-02", "marketing", 0, 2)]),
        "joueurs_declin": (["name", "age"], []),
        "decisions_achat": (["id", "label", "hypothesis"], [(d["id"], d["label"], d["hypothesis"]) for d in DECISIONS]),
        "encheres_ouvertes": (["name", "fin_paris"], [(e["name"], e["fin_paris"]) for e in ENCHERES]),
        "transferts_recents": (["name", "settled_at", "to_team", "achete"], []),
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
    yield "D1 capacité restante = solde − enchères ouvertes, sans réserve (PB8)", "réserve" not in t \
        and "(capacité restante : 29 666)" in t
    mince = figees(**{"gold.bv_position_summary": (["position", "depth", "ps_avg", "ps_max"], [("PG", 2, 49.4, 56.2), ("SG", 4, 46.4, 51.6)])})
    yield "D1 EFF-1 : poste mince = acheter un PG de note ≥ 57,2", "Acheter un PG de note ≥ 57,2" in texte(mince)
    rouge = figees(**{"gold.bv_finance_health": (["weekly_result_est", "weekly_personnel", "weekly_academy"], [(-5000, 60000, 100000)])})
    yield "D1 FIN-1 : résultat négatif = réduire le plus gros poste", "Réduis le poste académie (100 000" in texte(rouge)
    yield "D1 TRF-1 : affaire fiable = enchère maximale", "Enchère maximale 120 000 sur Martin" in texte(figees())
    yield "D1 capacité restante (solde 279 666 − 250 000 d'enchères ouvertes) trop faible = affaire abandonnée", \
        "Martin" not in t and "tienne dans le solde moins les enchères encore ouvertes" in t and "(capacité restante : 29 666)" in t
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
    # PB6 : Mes enchères jamais en ligne Export sans enchère d'achat dont la fin est à venir
    cibles9 = src.lire_cibles(DECISIONS, ENCHERES, ESSAI9, JOUR9)  # Fujita et Stankevičius ont fini le 08/11
    retard = figees(**{"gold.bv_agenda": (AGENDA[0], []), "gold.bv_exports_state": (
        ["ordre", "ecran", "pour_quoi", "dernier_paris", "age_h", "statut"],
        [(9, "Mes enchères", "ventes", None, 119, "🟧 à refaire"), (13, "Personnel", "staff", None, 80, "🟧 à refaire")])})
    t6 = auj.rendre(auj.plan(retard, {}, JOUR9, TOT, "", {"cibles": cibles9}), JOUR9)
    yield "PB6 09/11 : aucune ligne Mes enchères (enchères finies le 08/11)", "Mes enchères" not in t6
    yield "PB6 les autres exports en retard restent demandés", "Personnel (80 h)" in t6
    ouvertes = [dict(c, fin=dt.datetime(2026, 11, 10, 3, 50)) for c in cibles9]
    yield "PB6 une enchère dont la fin est à venir : Mes enchères demandé", "Mes enchères (119 h)" in auj.rendre(
        auj.plan(retard, {}, JOUR9, TOT, "", {"cibles": ouvertes}), JOUR9)
    inconnue = [dict(c, fin=None) for c in cibles9]
    yield "PB6 fin d'enchère inconnue : Mes enchères demandé (peut-être en cours)", "Mes enchères (119 h)" in auj.rendre(
        auj.plan(retard, {}, JOUR9, TOT, "", {"cibles": inconnue}), JOUR9)
    yield "PB6 aucune décision d'achat : aucune ligne Mes enchères", "Mes enchères" not in auj.rendre(
        auj.plan(retard, {}, JOUR9, TOT, "", {"cibles": []}), JOUR9)
    # PB7 : une enchère terminée n'est plus une action ; le résultat se lit dans silver.bv_transfers
    resultats = (["name", "settled_at", "to_team", "achete"], [
        ("Yuma Fujita", "2026-11-08T02:51:00+00:00", "San Jacobo", False),
        ("Bronius Stankevičius", "2026-11-08T02:47:00+00:00", "Toronto Moose", False),
        ("Bronius Stankevičius", "2026-10-04T09:05:00+00:00", "FC Dąb", False)])
    d7 = figees(**{"gold.bv_agenda": (AGENDA[0], []), "transferts_recents": resultats})
    t7 = auj.rendre(auj.plan(d7, {}, JOUR9, TOT, "", {"cibles": cibles9}), JOUR9)
    yield "PB7 09/11 : plus de ligne d'action pour Fujita ni Stankevičius (ni montant maximum, ni police)", \
        not any(re.match(r"^(\d\d:\d\d|--:--) — ", l) and ("Fujita" in l or "Stankevi" in l) for l in t7.splitlines()) \
        and "maximum 150 000" not in t7 and "police d'abord" not in t7
    autres7 = next(l for l in t7.splitlines() if l.startswith("Autres points"))
    yield "PB7 Fujita : terminée le 08/11, non acheté, résultat lu dans silver.bv_transfers", \
        "Fujita (C) terminée le 08/11 : non acheté, parti à San Jacobo (résultat lu dans silver.bv_transfers)" in autres7
    yield "PB7 Stankevičius : le transfert récent, pas celui du 04/10", \
        "Stankevičius (SF) terminée le 08/11 : non acheté, parti à Toronto Moose" in autres7 and "FC Dąb" not in t7
    achete = figees(**{"gold.bv_agenda": (AGENDA[0], []), "transferts_recents": (resultats[0], [
        ("Yuma Fujita", "2026-11-08T02:51:00+00:00", "San Jacobo", True)])})
    yield "PB7 acheté par mon équipe : dit « acheté »", "Fujita (C) terminée le 08/11 : acheté (résultat lu" in auj.rendre(
        auj.plan(achete, {}, JOUR9, TOT, "", {"cibles": cibles9}), JOUR9)
    yield "PB7 aucune ligne en base : le dit, sans inventer", "aucune ligne (export Historique global des transferts)" in auj.rendre(
        auj.plan(figees(**{"gold.bv_agenda": (AGENDA[0], [])}), {}, JOUR9, TOT, "", {"cibles": cibles9}), JOUR9)
    yield "PB7 vue illisible : « il me manque transferts_recents »", "il me manque transferts_recents" in auj.rendre(
        auj.plan(figees(**{"gold.bv_agenda": (AGENDA[0], []), "transferts_recents": None}), {"transferts_recents": "boum"},
                 JOUR9, TOT, "", {"cibles": cibles9}), JOUR9)
    # PB8 : capacité = solde − enchères encore ouvertes (une enchère finie ne retient plus d'argent), jamais de réserve
    bargains9 = (["name", "position", "ps", "ref_n", "ref_reliable", "bid_ceiling_resale", "resale_margin_p25", "ends_paris"], [
        ("Martin", "PG", 57.0, 9, True, 120000, 40000, "2026-11-09T21:00:00")])  # fin ce soir : encore une action
    d8 = figees(**{"gold.bv_agenda": (AGENDA[0], []), "gold.bv_market_bargains": bargains9})
    t8_finies = auj.rendre(auj.plan(d8, {}, JOUR9, TOT, "", {"cibles": cibles9}), JOUR9)
    t8_ouvertes = auj.rendre(auj.plan(d8, {}, JOUR9, TOT, "", {"cibles": ouvertes}), JOUR9)
    yield "PB8 enchères finies : rien n'est retenu, l'affaire de 120 000 tient dans le solde (279 666)", \
        "Enchère maximale 120 000 sur Martin" in t8_finies
    yield "PB8 enchères ouvertes (250 000) : capacité 29 666, l'affaire de 120 000 est écartée", \
        "Martin" not in t8_ouvertes and "(capacité restante : 29 666)" in t8_ouvertes
    sans_solde = figees(**{"gold.bv_agenda": (AGENDA[0], []), "gold.bv_finance_health": (
        ["weekly_result_est", "weekly_personnel", "weekly_academy"], [(108847, 60000, 100000)])})
    yield "PB8 solde illisible : capacité dite illisible, affaire non écartée", "(capacité restante illisible)" in auj.rendre(
        auj.plan(sans_solde, {}, JOUR9, TOT, "", {"cibles": cibles9}), JOUR9) or "Martin" in auj.rendre(
        auj.plan(sans_solde, {}, JOUR9, TOT, "", {"cibles": cibles9}), JOUR9)
    yield "PB8 le mot « réserve » n'apparaît dans aucune sortie", \
        not any("réserve" in x for x in (t, t8_finies, t8_ouvertes, auj.rendre(auj.plan(sans_solde, {}, JOUR9, TOT, "", {}), JOUR9)))
    # PB9 : une action dont le verrou est passé n'est plus « à faire maintenant »
    matin = dt.datetime(2026, 11, 9, 9, 18)
    S9 = {"tactique": tactique9, "saisies": []}
    t9_tot = auj.rendre(auj.plan(vide, {}, JOUR9, TOT, "", S9), JOUR9)
    t9_matin = auj.rendre(auj.plan(vide, {}, JOUR9, matin, "", S9), JOUR9)
    yield "PB9 à 06:00 : la ligne amical de 07:45 est présente", any(l.startswith("07:45") and "Garden City" in l for l in t9_tot.splitlines())
    yield "PB9 à 09:18 : la ligne amical de 07:45 est absente", "Garden City" not in t9_matin and not any(l.startswith("07:45") for l in t9_matin.splitlines())
    yield "PB9 à 09:18 : la ligue de 19:45 reste", any(l.startswith("19:45") and "Naked Spartans" in l for l in t9_matin.splitlines())
    yield "PB9 à 20:00 : la ligue de 19:45 est absente aussi", "Naked Spartans" not in auj.rendre(
        auj.plan(vide, {}, JOUR9, dt.datetime(2026, 11, 9, 20, 0), "", S9), JOUR9)
    agenda9 = figees(**{"gold.bv_agenda": (AGENDA[0], [
        (JOUR9, "07:45", 1, "amical", "Avant 07:45 : preset amical sur le match contre Garden City (domicile)"),
        (JOUR9, "19:30", 2, "export", "Avant 19:45 si possible : exporter la page Preview du match J4")])})
    ta = auj.rendre(auj.plan(agenda9, {}, JOUR9, matin, "", {}), JOUR9)
    yield "PB9 ligne d'agenda sans brief : verrou 07:45 passé, absente à 09:18 ; l'export de 19:30 reste", \
        "preset amical" not in ta and "19:30 — Avant 19:45 si possible" in ta
    yield "PB9 la même ligne d'agenda est présente à 06:00", "preset amical" in auj.rendre(auj.plan(agenda9, {}, JOUR9, TOT, "", {}), JOUR9)
    reste9 = {"restes": [{"match": "Garden City", "date": JOUR9, "heure": "07:45", "reglages": [("Tir 1", "Albano")], "texte": "", "fichier": "fait.md"}]}
    yield "PB9 réglage à corriger au verrou passé : absent à 09:18, présent à 06:00", \
        "Garden City" not in auj.rendre(auj.plan(vide, {}, JOUR9, matin, "", reste9), JOUR9) \
        and "Garden City : corrige à l'écran 1 réglages" in auj.rendre(auj.plan(vide, {}, JOUR9, TOT, "", reste9), JOUR9)
    finie = figees(**{"gold.bv_agenda": (AGENDA[0], []), "gold.bv_market_bargains": (bargains9[0], [
        ("Zhang", "PG", 55.1, 9, True, 120000, 541500, "2026-11-08T19:55:44"),   # fin hier soir : plus une action
        ("Martin", "PG", 57.0, 9, True, 120000, 40000, "2026-11-09T21:00:00")])})
    tf = auj.rendre(auj.plan(finie, {}, JOUR9, matin, "", {}), JOUR9)
    yield "PB9 enchère du Marché finie hier soir : plus de ligne ; celle de ce soir reste", \
        "Zhang" not in tf and "21:00 — Enchère maximale 120 000 sur Martin" in tf
    yield "PB9 fin d'enchère du Marché inconnue : l'affaire reste proposée", "Enchère maximale 120 000 sur Zhang" in auj.rendre(
        auj.plan(figees(**{"gold.bv_agenda": (AGENDA[0], []), "gold.bv_market_bargains": (bargains9[0], [
            ("Zhang", "PG", 55.1, 9, True, 120000, 541500, None)])}), {}, JOUR9, matin, "", {}), JOUR9)
    ref = dt.datetime(2026, 11, 9, 10, 28)
    yield "PB9 défaut inchangé : jour et heure de Paris", auj.reperes(None, None, ref) == (JOUR9, ref)
    yield "PB9 --maintenant 09:18 : même jour, heure imposée", auj.reperes(None, "09:18", ref) == (JOUR9, matin)
    yield "PB9 --jour : jour imposé, heure de Paris", auj.reperes("2026-11-06", None, ref) == (dt.date(2026, 11, 6), ref)
    try:
        auj.reperes(None, "neuf heures", ref)
        refus = False
    except SystemExit as e:
        refus = "HH:MM" in str(e)
    yield "PB9 --maintenant illisible : refus qui dit le format", refus
    hp = auj.heure_paris_naive()
    yield "PB9 l'heure vient de heure_paris.py : datetime sans fuseau", isinstance(hp, dt.datetime) and hp.tzinfo is None
    yield "PB7 enchère encore ouverte : reste une action", "Enchère sur Fujita (C) : maximum 150 000" in auj.rendre(
        auj.plan(d7, {}, JOUR9, TOT, "", {"cibles": ouvertes}), JOUR9)

    # R3 : Mes enchères « optionnel » (sans page récente) n'est jamais demandé
    optionnel = figees(**{"gold.bv_agenda": (AGENDA[0], []), "gold.bv_exports_state": (
        ["ordre", "ecran", "pour_quoi", "dernier_paris", "age_h", "statut"],
        [(9, "Mes enchères", "ventes", None, 120, "🟩 optionnel"), (13, "Personnel", "staff", None, 80, "🟧 à refaire")])})
    en_cours = [dict(c, fin=dt.datetime(2026, 11, 10, 3, 50)) for c in cibles9]  # enchère ouverte : PB6 ne filtre pas
    tr3 = auj.rendre(auj.plan(optionnel, {}, JOUR9, TOT, "", {"cibles": cibles9}), JOUR9)
    yield "R3 Mes enchères non demandé : « 🟩 optionnel » sans enchère ouverte (absent)", "Mes enchères" not in tr3
    yield "R3 les autres écrans en retard restent demandés", "Personnel (80 h)" in tr3
    tr3b = auj.rendre(auj.plan(optionnel, {}, JOUR9, TOT, "", {"cibles": en_cours}), JOUR9)
    yield "R3 Mes enchères avec enchère ouverte et page de 120 h (présent)", "Mes enchères (120 h)" in tr3b
    # R5 : déclarations par clé `[clé=…]`, registres des 7 derniers jours
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "briefs").mkdir()
        for f in (ESSAI9 / "briefs").glob("*.md"):
            (tmp / "briefs" / f.name).write_text(f.read_text(encoding="utf-8"), encoding="utf-8")

        def registre(jour_fichier, *lignes):
            (tmp / f"fait-{jour_fichier}.md").write_text("\n".join(lignes) + "\n", encoding="utf-8")

        def garden(cles):
            r = auj.rendre(auj.plan(vide, {}, JOUR9, TOT, "", {"tactique": tactique9, "cles": cles}), JOUR9)
            return next(l for l in r.splitlines() if "Garden City" in l)
        registre("2026-11-08", "- [10:34 UTC] [clé=Garden City 09/11] Amical Garden City : composition et consignes faites — source : déclaré par l'utilisateur")
        cles = src.lire_cles(tmp, JOUR9)
        yield "R5 la clé du 08/11 est lue : Garden City, 09/11", [(c["nom"], c["date"], c["jour"]) for c in cles] == [("Garden City", JOUR9, dt.date(2026, 11, 8))]
        yield "R5 sans aucun mot connu du registre, la clé seule retire « saisis la tactique » (déclarée le 08/11, reconnue le 09/11)", \
            "saisis la tactique" not in garden(cles) and "heure limite du verrou 07:45" in garden(cles)
        yield "R5 sans la clé : « saisis la tactique maintenant » (contrôle)", "saisis la tactique maintenant" in garden([])
        registre("2026-11-08", "- [10:34 UTC] [clé=Garden City 14/11] Amical : composition faite")
        yield "R5 clé datée d'un autre jour : le match du 09/11 reste à saisir", "saisis la tactique maintenant" in garden(src.lire_cles(tmp, JOUR9))
        registre("2026-11-08", "- [10:34 UTC] [clé=Garden City] Amical : composition faite")
        yield "R5 clé sans date : valable pour un match des 7 jours suivants", "saisis la tactique" not in garden(src.lire_cles(tmp, JOUR9))
        registre("2026-11-08", "- [10:34 UTC] [clé=Garden City 09/11] reste à corriger : Tir 1 : Albano")
        yield "R5 une ligne « reste à … » n'est jamais une déclaration faite", src.lire_cles(tmp, JOUR9) == []
        registre("2026-11-08", "- [clé=Garden City 09/11] Amical : composition faite")
        yield "R5 registre de 7 jours : lu le 14/11, ignoré le 15/11", \
            len(src.lire_cles(tmp, dt.date(2026, 11, 14))) == 1 and src.lire_cles(tmp, dt.date(2026, 11, 15)) == []
        yield "R5 registre du lendemain d'un jour futur : jamais lu", src.lire_cles(tmp, dt.date(2026, 11, 7)) == []
        # écran déclaré par clé : même jour seulement
        registre("2026-11-09", "- [08:00 UTC] [clé=Personnel] Export Personnel — source : déclaré par l'utilisateur")
        registre("2026-11-08", "- [08:00 UTC] [clé=Finances] Export Finances — source : déclaré par l'utilisateur")
        retard9 = figees(**{"gold.bv_agenda": (AGENDA[0], []), "gold.bv_exports_state": (
            ["ordre", "ecran", "pour_quoi", "dernier_paris", "age_h", "statut"],
            [(13, "Personnel", "staff", None, 80, "🟧 à refaire"), (10, "Finances", "semaine", None, 80, "🟧 à refaire")])})
        tc = auj.rendre(auj.plan(retard9, {}, JOUR9, TOT, "", {"cles": src.lire_cles(tmp, JOUR9)}), JOUR9)
        yield "R5 écran déclaré aujourd'hui par clé (Personnel) : non redemandé", "Personnel (80 h)" not in tc
        yield "R5 écran déclaré hier par clé (Finances) : redemandé, la base fait foi", "Finances (80 h)" in tc
    yield "R5 repli : l'ancienne correspondance par mots garde son effet sans clé", \
        "Personnel (80 h)" not in auj.rendre(auj.plan(retard9, {}, JOUR9, TOT, "- [10:00 utc] export personnel", {"cles": []}), JOUR9) \
        and "Personnel (80 h)" in auj.rendre(auj.plan(retard9, {}, JOUR9, TOT, "", {"cles": []}), JOUR9)
    yield from cas_etape5a()


ETAT_VIDE = (["ordre", "ecran", "pour_quoi", "dernier_paris", "age_h", "statut"], [])
COLS_AM = ["rule_id", "prio", "alerte"]


def plan5a(**remplace):
    """Plan du 09/11 à 06:00 sur une base sans agenda ni export en retard, plus les sources de l'étape 5a."""
    d = figees(**{"gold.bv_agenda": (AGENDA[0], []), "gold.bv_exports_state": ETAT_VIDE,
                  "gold.bv_daily_alerts": (["priority", "category", "alert"], [])})
    d.update(remplace)
    return auj.rendre(auj.plan(d, {}, JOUR9, TOT, "", {}), JOUR9)


def cas_etape5a():
    # A1 : alertes de domaine « match »
    dernier = (2, "Dernier match exporté : 08/11 (amical, L 94-96 contre New York City Cyclones)")
    t = plan5a(alertes_match=(COLS_AM, [("dernier_match",) + dernier]))
    yield "A1 dernier match : ligne « Analyse : » (présent)", "Analyse : Dernier match exporté : 08/11" in t
    t = plan5a(alertes_match=(COLS_AM, [("coupe_sans_resultat", 2, "Match de coupe joué non exporté : J2 du 08/11")]))
    yield "A1 coupe jouée non exportée : dans la ligne Exports (présent)", \
        "Match de coupe joué non exporté : J2 du 08/11" in t.splitlines()[-1]
    box = (ETAT_VIDE[0], [(6, "Match de ligue : box", "match", None, 30, "🟧 à refaire")])
    t = plan5a(alertes_match=(COLS_AM, [("ligue_sans_resultat", 2, "Match de ligue joué non exporté : J4 du 07/11")]),
               **{"gold.bv_exports_state": box})
    yield "A1 ligue non exportée et écran box déjà demandé : pas de doublon", \
        "Match de ligue : box (30 h)" in t and "non exporté" not in t
    t = plan5a(alertes_match=(COLS_AM, [("ligue_sans_resultat", 2, "Match de ligue joué non exporté : J4 du 07/11")]))
    yield "A1 ligue non exportée sans écran box demandé : dans la ligne Exports", "Match de ligue joué non exporté : J4 du 07/11" in t
    t = plan5a(alertes_match=(COLS_AM, []))
    yield "A1 aucune alerte de match (absent)", "Analyse :" not in t and "non exporté" not in t
    yield "A1 alertes illisibles : « il me manque »", "il me manque alertes_match" in plan5a(alertes_match=None)
    # A2 : défaite de ligue ou de coupe -> analyste ce soir
    COLS_OBJ = ["day", "competition_kind", "opponent", "objectif", "raison", "rule_id", "defaites_d_affilee"]
    COLS_OFF = ["day", "competition_kind", "opponent", "my_result"]
    serie = (COLS_OBJ, [(JOUR9, "ligue", "Naked Spartans", "corriger", "2 défaites d'affilée", "serie", 2)])
    perdu = (COLS_OFF, [(dt.date(2026, 11, 7), "ligue", "Póvoa Riptide", "L")])
    t = plan5a(objectifs=serie, dernier_officiel=perdu)
    l = next((x for x in t.splitlines() if "analyste" in x), "")
    yield "A2 série de 2 défaites de ligue : « lance l'agent analyste ce soir » (présent)", \
        "Analyse : lance l'agent analyste ce soir" in l and "2 défaites d'affilée" in l and "Póvoa Riptide, 07/11" in l
    t = plan5a(objectifs=(COLS_OBJ, []), dernier_officiel=(COLS_OFF, [(dt.date(2026, 11, 8), "coupe", "Ploppers", "L")]))
    yield "A2 défaite de coupe sans série : même ligne", "lance l'agent analyste ce soir" in t and "défaite de coupe" in t
    t = plan5a(objectifs=(COLS_OBJ, []), dernier_officiel=(COLS_OFF, [(dt.date(2026, 11, 7), "ligue", "Póvoa Riptide", "W")]))
    yield "A2 dernier match officiel gagné (absent)", "analyste" not in t
    d = figees(**{"gold.bv_agenda": (AGENDA[0], []), "gold.bv_exports_state": ETAT_VIDE,
                  "gold.bv_daily_alerts": (["priority", "category", "alert"], [])}, objectifs=serie, dernier_officiel=perdu)
    t = auj.rendre(auj.plan(d, {}, JOUR9, TOT, "", {"analyste": dt.date(2026, 11, 8)}), JOUR9)
    yield "A2 défaite déjà analysée (brief analyste plus récent) : absent", "analyste" not in t
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "briefs").mkdir()
        for n in ("2026-11-05-analyste.md", "2026-10-24-analyse-defaite-j21.md", "2026-11-10-analyste.md", "2026-11-08-tactique.md"):
            (Path(tmp) / "briefs" / n).write_text("x", encoding="utf-8")
        yield "A2 lecteur : dernier brief analyste daté d'au plus le jour", src.lire_analyste(tmp, JOUR9) == dt.date(2026, 11, 5)
    t = plan5a(alertes_match=(COLS_AM, [("dernier_match", 2, "Dernier match exporté : 07/11 (ligue, L 80-90 contre Póvoa Riptide)")]),
               objectifs=serie, dernier_officiel=perdu)
    yield "A1/A2 même match : une seule ligne Analyse", sum("Analyse :" in x for x in t.splitlines()) == 1
    t = plan5a(alertes_match=(COLS_AM, [("dernier_match",) + dernier]))
    yield "A2 amical perdu seul (dernier match amical) : pas d'analyste", "analyste" not in t


def cas_base():
    """R4, sur la base (option --base) : un type de page sans lecteur sort en alerte, un type lu n'en porte pas."""
    spec = importlib.util.spec_from_file_location("sqlmod", DOSSIER / "sql.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cols, lignes = mod.executer("select type_page, lu_par_silver, alerte from gold.bv_couverture_pages")
    par = {l[0]: dict(zip(cols, l)) for l in lignes}
    yield "R4 base : /api/v1/teams/<id>/tactics reçu, aucun lecteur silver : « page reçue, non lue »", \
        par.get("/api/v1/teams/<id>/tactics", {}).get("alerte") == "page reçue, non lue"
    yield "R4 base : /api/v1/teams/<id>/academy lu par silver, sans alerte", \
        par.get("/api/v1/teams/<id>/academy", {}).get("lu_par_silver") == "oui" and par["/api/v1/teams/<id>/academy"]["alerte"] is None
    yield "R4 base : friendlies lue par gold seulement, signalée comme telle", \
        par.get("/api/v1/teams/<id>/friendlies", {}).get("alerte") == "lue par gold seulement"
    yield "R4 base : toute ligne sans lecteur porte une alerte", all(v["alerte"] for v in par.values() if v["lu_par_silver"] == "non")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    echecs = 0
    jeux = list(cas()) + (list(cas_base()) if "--base" in sys.argv else [])
    for nom, ok in jeux:
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    n = len(jeux)
    print(f"{n - echecs}/{n}")
    sys.exit(1 if echecs else 0)
