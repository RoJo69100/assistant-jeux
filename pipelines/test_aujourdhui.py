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
        # phase 0 : un titre sans date ne prouve pas qu'il s'agit de ce match (jamais la fiche du match précédent)
        (Path(tmp) / "briefs" / "2026-11-01-tactique.md").write_text(re.sub(r"\d{2}/\d{2}", "", vieux), encoding="utf-8")
        yield "L1 brief sans date dans le titre : jamais repris", src.lire_tactique(tmp, JOUR) == []
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
    # 5i X2 : une page du Marché ancienne n'est plus cachée ; l'annonce encore ouverte reste, avec l'âge de la page
    yield "D1 TRF-4 (5i) : Marché de 30 h = ligne Export, annonce ouverte gardée avec « page du Marché de 30 h »", \
        "Marché (enchères) (30 h)" in tp and "Martin" in tp and "page du Marché de 30 h : le prix a pu monter" in tp
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
    # instantané du 12/11 : Bērziņš en URGENT avec un gain de -1,8 sur une page du Marché de 28 h ; Torres à 1 de prix de départ avec une
    # « marge » de 1 003 436 ; deux plafonds (726 750 dans l'action, 999 000 dans le tableau du bloc 4)
    cb12 = ["name", "position", "ps", "ref_n", "ref_reliable", "bid_ceiling_resale", "resale_margin_p25", "ends_paris", "price_now"]
    b12 = [("Edgars Bērziņš", "PF", 56.8, 67, True, 726750, 126750, "2026-11-12T22:33:00", 600000),
           ("Hilario Torres", "SG", 55.4, 23, True, 1003438, 1003436, "2026-11-13T09:33:00", 1)]
    ca = ["auction_id", "name", "position", "age", "ps", "price_now", "ends_paris", "heures", "gain_vs_my_second", "enters_top8"]

    def plan12(age_h, gain):
        d = figees(**{"gold.bv_agenda": (AGENDA[0], []), "gold.bv_market_bargains": (cb12, b12),
                      "gold.bv_finance_health": (["balance", "weekly_result_est", "weekly_personnel", "weekly_academy"], [(5000000, 98227, 60000, 100000)]),
                      "gold.bv_exports_state": (["ordre", "ecran", "pour_quoi", "dernier_paris", "age_h", "statut"], [(8, "Marché (enchères)", "cibles", None, age_h, "")]),
                      "annonces_24h": (ca, [(1, "Edgars Bērziņš", "PF", 29, 56.8, 600000, "2026-11-12T22:33:00", 7.7, gain, False)])})
        return auj.plan(d, {}, dt.date(2026, 11, 12), dt.datetime(2026, 11, 12, 14, 51), "", {})
    r12 = plan12(28, -1.8)
    berz = [a for a in r12["actions"] if "Bērziņš" in a[2]]
    yield "X 12/11 gain négatif et page de 28 h : Bērziņš pas URGENT", len(berz) == 1 and berz[0][1] == 2
    yield "X 12/11 gain positif mais page de 28 h : pas URGENT", [a[1] for a in plan12(28, 1.0)["actions"] if "Bērziņš" in a[2]] == [2]
    yield "X 12/11 gain positif et page fraîche, fin aujourd'hui : URGENT", [a[1] for a in plan12(3, 1.0)["actions"] if "Bērziņš" in a[2]] == [1]
    yield "X 12/11 prix de départ ≤ 1 : aucune enchère, « marge non calculable »", not any("Torres" in a[2] for a in r12["actions"]) \
        and any("Hilario Torres" in g and "marge non calculable" in g for g in r12["garder"])
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
    d = figees(**{"gold.bv_agenda": (AGENDA[0], []), "gold.bv_exports_state": ETAT_VIDE,
                  "gold.bv_daily_alerts": (["priority", "category", "alert"], [])}, alertes_match=(COLS_AM, [("dernier_match",) + dernier]))
    a = auj.plan(d, {}, JOUR9, TOT, "", {})["actions"]
    yield "A1/A6 « Dernier match » en priorité 3 (constat, ne chasse pas une action)", \
        [x[1] for x in a if x[2].startswith("Analyse : Dernier")] == [3]
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
    # A3 : titre acquis ou rien à jouer -> minutes aux jeunes
    amical = (JOUR9 + dt.timedelta(days=1), "amical", "Opper Cards", "tester", "amical : tester", "amical", 2)
    rien = (dt.date(2026, 11, 14), "ligue", "BC Gelrode", "former", "rien à jouer (8e sur 12)", "rien_former", 0)
    t = plan5a(objectifs=(COLS_OBJ, [amical, rien]))
    yield "A3 rien à jouer : « minutes aux jeunes » (présent)", \
        "Composition : minutes aux jeunes, ligue contre BC Gelrode (sam. 14/11)" in t and "rien à jouer (8e sur 12)" in t
    t = plan5a(objectifs=(COLS_OBJ, [amical, serie[1][0]]))
    yield "A3 amicaux « tester » et série seulement : aucune ligne jeunes (absent)", \
        "minutes aux jeunes" not in t and "ni titre acquis ni rien à jouer" in t and "règle non écrite — à valider (le script" not in t
    # A4 : solde projeté sous une semaine de masse salariale
    COLS_FH = ["balance", "weekly_result_est", "weekly_salaries", "weekly_personnel", "weekly_academy"]
    fh = (COLS_FH, [(960181, 97137, 294625, 60000, 100000)])
    COLS_PR = ["season_end", "balance_end_projected", "tickets_left", "sponsor_left", "costs_left"]
    t = plan5a(**{"gold.bv_finance_health": fh,
                  "gold.bv_finance_projection": (COLS_PR, [("2026-12-21", 200000, 2800000, 480000, 2727750)])})
    l = next((x for x in t.splitlines() if "solde projeté" in x), "")
    yield "A4 solde projeté 200 000 < une semaine de salaires 294 625 : ligne Finances avec la cause (présent)", \
        "Finances : solde projeté au 21/12 de 200 000, sous une semaine de salaires (294 625)" in t \
        and "cause : charges restantes 2 727 750 contre recettes restantes 3 280 000" in t and "salaires (294 625 par semaine)" in t
    t = plan5a(**{"gold.bv_finance_health": fh,
                  "gold.bv_finance_projection": (COLS_PR, [("2026-12-21", -50000, 0, 0, 500000)])})
    yield "A4 solde projeté négatif : ligne Finances", "solde projeté au 21/12 de -50 000" in t
    t = plan5a(**{"gold.bv_finance_health": fh,
                  "gold.bv_finance_projection": (COLS_PR, [("2026-12-21", 1512431, 2800000, 480000, 2727750)])})
    yield "A4 solde projeté 1 512 431 (base du 09/11) : aucune ligne (absent)", "solde projeté" not in t

    # J5 (étape 5c) : verrou depuis core.fixture.scheduled_at (lignes de la base du 09/11 16:20), sinon heure du brief
    COLS_CAL = ["day", "competition_kind", "opponent", "coup_envoi_paris", "verrou_paris"]
    CAL = (COLS_CAL, [("2026-11-09", "ligue", "Naked Spartans", "2026-11-09T20:00:00", "2026-11-09T19:45:00"),
                      ("2026-11-12", "coupe", "Stare Kotlety", "2026-11-12T20:00:00", "2026-11-12T20:00:00")])
    MIDI = dt.datetime(2026, 11, 9, 12, 0)
    tac = [{"type": "ligue", "match": "Naked Spartans", "date": JOUR9, "verrou": "19:30", "manche": "J4", "lieu": "domicile",
            "preuves": [], "fichier": "briefs/essai.md", "age": 0, "vieux": False},
           {"type": "coupe", "match": "Stare Kotlety", "date": dt.date(2026, 11, 12), "verrou": None, "manche": None,
            "lieu": "domicile", "preuves": [], "fichier": "briefs/essai.md", "age": 0, "vieux": False}]
    vide = figees(**{"gold.bv_agenda": (AGENDA[0], [])})
    def ligne(d, nom):
        return next(l for l in d["actions"] if nom in l[2])
    avec = auj.plan(figees(**{"gold.bv_agenda": (AGENDA[0], []), "calendrier": CAL}), {}, JOUR9, MIDI, "", {"tactique": tac})
    sans = auj.plan(vide, {}, JOUR9, MIDI, "", {"tactique": tac})
    yield "J5 ligue J4 : verrou 19:45 Paris pris dans scheduled_at (le brief disait 19:30)", \
        ligne(avec, "Naked Spartans")[0] == dt.datetime(2026, 11, 9, 19, 45) and "verrou 19:45" in ligne(avec, "Naked Spartans")[3]
    yield "J5 ligue J4 sans scheduled_at : ancienne heure du brief (19:30)", \
        ligne(sans, "Naked Spartans")[0] == dt.datetime(2026, 11, 9, 19, 30) and "verrou 19:30" in ligne(sans, "Naked Spartans")[3]
    yield "J5 coupe 12/11 : limite 20:00 Paris depuis scheduled_at, titre « Coupe contre »", \
        ligne(avec, "Stare Kotlety")[0] == dt.datetime(2026, 11, 12, 20, 0) and ligne(avec, "Stare Kotlety")[2].startswith("Coupe contre")
    yield "J5 coupe sans scheduled_at : verrou inconnu (jamais supposé)", \
        ligne(sans, "Stare Kotlety")[0] is None and "verrou inconnue" in ligne(sans, "Stare Kotlety")[3]

    yield from cas_experiences(COLS_CAL, MIDI)
    yield from cas_academie()
    yield from cas_vente()
    yield from cas_boucle()
    yield from cas_marche_5i()
    yield from cas_composition_5j()
    yield from cas_experience_e5()
    yield from cas_entrainement()
    yield from cas_fatigue()
    yield from cas_revue()


def cas_revue():
    """R8 (étape 6a) : ligne « Revue de la semaine : à lire (…) » le dimanche, rien les autres jours."""
    DIM = dt.date(2026, 11, 15)

    def revue(jour, existe=True):
        p = auj.plan(figees(), {}, jour, dt.datetime.combine(jour, dt.time(10, 0)), "", {"revue_hebdo": existe})
        return [a for a in p["actions"] if a[2].startswith("Revue de la semaine")]

    l = revue(DIM)
    yield "R8 dimanche, présent : une ligne « à lire » avec le chemin de la page", \
        len(l) == 1 and l[0][2] == "Revue de la semaine : à lire (outputs/basketvibe/revue-hebdo-2026-11-15.md)" \
        and l[0][3] == ""
    yield "R8 dimanche, page absente : la ligne dit la commande", \
        "python -I pipelines/revue_hebdo.py basketvibe" in revue(DIM, False)[0][3]
    yield "R8 lundi, absent : aucune ligne de revue", revue(JOUR9) == []
    yield "R8 samedi, absent : aucune ligne de revue", revue(dt.date(2026, 11, 14)) == []


def cas_fatigue():
    """N3 (étape 5h) : « sors X avant le match Y » seulement si la fatigue projetée dépasse la zone verte."""
    COLS = ["kind", "match_day", "opponent", "joueur", "minutes", "defense_tier", "sat_fatigue", "zone_verte"]
    CAL = (["day", "competition_kind", "opponent", "coup_envoi_paris", "verrou_paris"],
           [("2026-11-09", "ligue", "Naked Spartans", "2026-11-09T20:00:00", "2026-11-09T19:45:00")])
    MIDI = dt.datetime(2026, 11, 9, 12, 0)

    def lignes(rows, maintenant=MIDI):
        d = figees(**{"fatigue_avant_match": (COLS, rows), "calendrier": CAL})
        return [a for a in auj.plan(d, {}, JOUR9, maintenant, "", {})["actions"] if a[2].startswith("Sors ")]

    deux = [("ligue", "2026-11-09", "Naked Spartans", "Bernard", 36, 3, 24.6, 20),
            ("ligue", "2026-11-09", "Naked Spartans", "Boyer", 36, 2, 21.2, 20)]
    l = lignes(deux)
    yield "N3 dépassement, présent : une ligne par match, joueurs nommés, verrou du calendrier, zone verte lue", \
        len(l) == 1 and l[0][2] == "Sors Bernard, Boyer avant le match de ligue contre Naked Spartans (lun. 09/11)" \
        and l[0][0] == dt.datetime(2026, 11, 9, 19, 45) and "Bernard 24,6 (36 min, agressivité 4 à l'écran)" in l[0][3] \
        and "zone verte jusqu'à 20" in l[0][3]
    yield "N3 aucun dépassement (vue vide), absent : aucune ligne « Sors »", lignes([]) == []
    yield "N3 verrou passé, absent : aucune ligne « Sors »", lignes(deux, dt.datetime(2026, 11, 9, 20, 0)) == []
    yield "N3 aucun seuil dans le code : la zone verte affichée vient de la vue", \
        "zone verte jusqu'à 25" in lignes([deux[0][:7] + (25,)])[0][3]
    # instantané du 12/11 : « Sors Bonnet, Gimenez, Richard, Lefebvre, Fournier avant le match de coupe contre Stare Kotlety » calculé
    # depuis l'écran non sauvegardé (48 min, agressivité 3 pour tous) ; aucune ligne « Sors », « écran non sauvegardé » à la place
    COLS2 = COLS + ["sauvegarde_match", "ecran_par_defaut"]
    CAL2 = (CAL[0], [("2026-11-12", "coupe", "Stare Kotlety", "2026-11-12T19:15:00", "2026-11-12T19:00:00")])
    coupe = [("coupe", "2026-11-12", "Stare Kotlety", n, 48, 2, 27.0, 20) for n in ("Bonnet", "Gimenez", "Richard", "Lefebvre", "Fournier")]

    def plan12(rows):
        d = figees(**{"fatigue_avant_match": (COLS2, rows), "calendrier": CAL2})
        return auj.plan(d, {}, dt.date(2026, 11, 12), dt.datetime(2026, 11, 12, 14, 51), "", {})["actions"]
    for nom, rows in (("indicateur faux", [r + (False, False) for r in coupe]), ("indicateur absent, écran par défaut", [r + (None, True) for r in coupe])):
        acts = plan12(rows)
        yield f"N3 écran non sauvegardé ({nom}) : aucune ligne « Sors », « écran non sauvegardé » affiché", \
            not any(a[2].startswith("Sors ") for a in acts) \
            and any(a[2] == "Coupe contre Stare Kotlety (jeu. 12/11) : écran non sauvegardé, fatigue projetée non calculée" for a in acts)
    yield "N3 écran sauvegardé : ligne « Sors » gardée", any(a[2].startswith("Sors Bonnet") for a in plan12([r + (True, False) for r in coupe]))
    yield "N3 requête : lit l'indicateur de sauvegarde", "sauvegarde_match" in auj.REQUETES["fatigue_avant_match"] \
        and "ecran_par_defaut" in auj.REQUETES["fatigue_avant_match"]


def cas_entrainement():
    """N2 (étape 5h) : contrôle focus attendu (fiche de l'agent) contre focus saisi, le jour de fin de cycle."""
    SAM = dt.date(2026, 11, 14)  # samedi, isodow 6
    MATIN = dt.datetime(2026, 11, 14, 10, 0)
    REGLE = (["isodow", "heure"], [(6, "23:00")])
    COLS = ["ordre", "nom", "poste", "principale", "secondaire", "export_le"]
    SAISIE = (COLS, [(1, "Albano", "PF", "rebounding", "defense", None), (2, "Baron", "PG", "passing", "defense", None),
                     (3, "Dang", "SG", "three_point", "defense", None)])
    FICHE = {"date": dt.date(2026, 11, 8), "fichier": "briefs/2026-11-08-entrainement.md",
             "joueurs": {"Albano": ("rebounding", "defense"), "Baron": ("passing", "defense"), "Dang": (None, None)}}
    AG = (AGENDA[0], [("2026-11-14", "23:00:00", 2, "entraînement",
                       "Avant dimanche 04:00 : vérifier et sauvegarder les choix d'entraînement")])

    def lignes(saisie=SAISIE, fiche=FICHE, jour=SAM, maintenant=MATIN, regle=REGLE):
        d = figees(**{"gold.bv_agenda": AG, "gold.bv_saisie_entrainement": saisie, "regle_entrainement": regle})
        return [a for a in auj.plan(d, {}, jour, maintenant, "", {"fiche_entrainement": fiche})["actions"]
                if "ntraînement" in a[2]]

    yield "N2 zéro écart, absent : aucune ligne de contrôle, la ligne d'agenda reste", \
        [a[2] for a in lignes()] == ["Avant dimanche 04:00 : vérifier et sauvegarder les choix d'entraînement"]
    ecart = (COLS, [(1, "Albano", "PF", "defense", "defense", None), (2, "Baron", "PG", "passing", "ball_handling", None),
                    (3, "Dang", "SG", "passing", "stamina", None), (4, "Ungureanu", "C", "rebounding", "passing", None)])
    l = lignes(saisie=ecart)
    yield "N2 écarts, présent : une ligne, principale et secondaire attendues, joueur hors fiche, « indifférent » ignoré", \
        len(l) == 1 and l[0][0] == dt.datetime(2026, 11, 14, 23, 0) and "corrige 3 écarts" in l[0][2] \
        and l[0][3] == "Albano : principale Rebond (saisi Défense) ; Baron : secondaire Défense (saisi Dribble) ; " \
                       "Ungureanu : absent de la fiche ; fiche du 08/11" and "Dang" not in l[0][3]
    yield "N2 autre jour que celui de la règle, absent : aucune ligne de contrôle même avec écarts", \
        not any("corrige" in a[2] for a in lignes(saisie=ecart, jour=dt.date(2026, 11, 13), maintenant=dt.datetime(2026, 11, 13, 10)))
    yield "N2 cycle passé (après 23:00), absent : aucune ligne de contrôle", \
        not any("corrige" in a[2] for a in lignes(saisie=ecart, maintenant=dt.datetime(2026, 11, 14, 23, 30)))
    yield "N2 fiche absente, présent : « il me manque la fiche de l'agent Entraînement »", \
        any("il me manque la fiche" in a[2] for a in lignes(fiche=None))
    yield "N2 règle absente, absent : aucune ligne de contrôle", \
        not any("corrige" in a[2] for a in lignes(saisie=ecart, regle=(["isodow", "heure"], [])))
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "briefs").mkdir()
        (Path(tmp) / "briefs" / "2026-11-08-entrainement.md").write_text(
            "| Joueur | Âge | Principale : gain |\n|---|---|---|\n| Baron (PG) | 17 | Passes +1 |\n\n"
            "| Poste | Joueur (âge) | Principale (valeur) | Secondaire (valeur) | Gain |\n|---|---|---|---|---|\n"
            "| PG | Baron (17) | Passes 54,6 | Défense 41,4 | +1,6 |\n| SG | Dang (30) | indifférent (3PT) | indifférent | 0 |\n"
            "| C | Bernard (18) | Rebond 63,2 | Athlétisme 53,6 | +2,2 |\n", encoding="utf-8")
        f = src.lire_fiche_entrainement(tmp, SAM)
        yield "N2 lecteur de fiche, présent : 3 joueurs, libellés traduits, « indifférent » = None", \
            f["joueurs"] == {"Baron": ("passing", "defense"), "Dang": (None, None), "Bernard": ("rebounding", "athleticism")} \
            and f["date"] == dt.date(2026, 11, 8)
        yield "N2 lecteur de fiche, absent (brief postérieur au jour) : None", \
            src.lire_fiche_entrainement(tmp, dt.date(2026, 11, 7)) is None


def cas_experiences(COLS_CAL, MIDI):
    """H7 (étape 5d) : file d'expériences amicales et décalage d'agenda ; cas présent et cas absent pour chacun."""
    with tempfile.TemporaryDirectory() as tmp:
        reg = Path(tmp)

        def exps(*lignes, jour=JOUR9, debut=None):
            """Registre du 08/11 ; `debut` remplace celui du YAML (None : pas de borne M4, cas H7 d'avant 5g)."""
            (reg / "fait-2026-11-08.md").write_text("\n".join(lignes) + "\n", encoding="utf-8")
            x = src.lire_experiences(reg, jour)
            if x is not None:
                x["debut"] = debut
            return x

        AM = {"match": "Opper Cards", "date": dt.date(2026, 11, 10), "limite": dt.datetime(2026, 11, 10, 7, 45)}
        def niveau(x, joues=()):
            t = auj.test_en_cours(x, AM, joues)
            return t and (t[0]["id"], t[1], t[2])
        e1 = lambda n: ["- [08:00 UTC] Saisie de l'amical [expérience=E1:" + "ABAB"[i] + "]" for i in range(n)]
        # M3 (5g) : faits à clé distincte et réglage joué en base (gold.bv_amical_reglage), un club par amical
        CLUBS = ["Alpha", "Bravo", "Charlie", "Delta", "Echo", "Fox", "Golf", "Hotel", "India", "Juliet", "Kilo", "Lima",
                 "Mike", "Nova", "Oscar", "Papa", "Quebec", "Romeo", "Sierra", "Tango", "Ultra", "Victor", "Whisky",
                 "Xray", "Yankee", "Zulu", "Ares", "Bora", "Ceres", "Dune", "Eris", "Faro", "Gaia"]
        def joue(i, cran=0, pq=0, t4=0):
            return {"fixture_id": f"f{i}", "match_day": f"2026-11-{1 + i % 8:02d}", "opponent": f"{CLUBS[i]} BC",
                    "agress_cran": cran, "primary_quarts": pq, "tir_cran4_joueurs": t4}
        def fait(i, exp, niv):
            return f"- [x] [clé={CLUBS[i]} BC {1 + i % 8:02d}/11] [expérience={exp}:{niv}]"
        e1v = lambda n: ([fait(i, "E1", "ABAB"[i]) for i in range(n)], [joue(i, cran=(2, 4)["ABAB"[i] == "B"]) for i in range(n)])
        yield "H7 E1 alternance, absent (aucun fait) : niveau A", niveau(exps()) == ("E1", "A", False)
        yield "H7 E1 alternance, présent : A,B,A,B (1 fait -> B, 2 -> A, 3 -> B)", \
            [niveau(exps(*e1(n)))[1] for n in (1, 2, 3)] == ["B", "A", "B"]
        f3, j3 = e1v(3)
        f4, j4 = e1v(4)
        yield "H7 passage à E2, absent (E1 à 3 vérifiés sur 4) : encore E1", niveau(exps(*f3), j3) == ("E1", "B", False)
        yield "H7 passage à E5 (5j : E5 entre E1 et E2), présent (E1 à 4 vérifiés sur 4) : E5 niveau A", niveau(exps(*f4), j4) == ("E5", "A", False)
        suite = [(i, e, n, kw) for i, (e, n, kw) in enumerate([("E5", "A", {})] * 3 + [("E2", "A", {"t4": 2})] * 3 + [("E3", "A", {"pq": 4})] * 7
                                                              + [("E4", "habituel", {})] * 16, start=4)]
        toutes = f4 + [fait(i, e, n) for i, e, n, _ in suite]
        jt = j4 + [joue(i, **kw) for i, _, _, kw in suite]
        yield "H4 toutes terminées (vérifiées) : aucune expérience en cours", niveau(exps(*toutes), jt) is None
        # M3 : déclarés, vérifiés, écarts
        yield "M3 passage, absent (4 déclarés, aucun exporté) : encore E1, rien ne passe à E2", \
            niveau(exps(*f4), []) == ("E1", "A", False)
        j_ecart = j4[:3] + [joue(3, cran=0)]
        yield "M3 écart, présent (4e amical joué en cran 0 au lieu de 4) : encore E1, niveau B rejoué", \
            niveau(exps(*f4), j_ecart) == ("E1", "B", False)
        av = lambda x, j: auj.texte_avancement(x["file"][0], auj.verifier(x, j)["E1"])
        yield "M3 ligne, présent : « E1 : 1 vérifié sur 4, 1 déclaré non vérifié (match à exporter) »", \
            av(exps(*e1v(2)[0]), e1v(1)[1]) == "E1 : 1 vérifié sur 4, 1 déclaré non vérifié (match à exporter)"
        yield "M3 ligne, absent (rien déclaré) : « E1 : 0 vérifié sur 4 », sans attente ni écart", \
            av(exps(), j4) == "E1 : 0 vérifié sur 4"
        yield "M3 écart, présent : « réglage joué ≠ réglage du test (Delta BC 04/11) »", \
            av(exps(*f4), j_ecart) == "E1 : 3 vérifiés sur 4, réglage joué ≠ réglage du test (Delta BC 04/11)"
        yield "M3 écart, absent (réglages conformes) : aucun « ≠ »", "≠" not in av(exps(*f4), j4)
        yield "M3 sans clé : fait du 08/11 rattaché à l'amical joué le 08 ou le 09", \
            auj.verifier(exps(*e1(1)), [{"fixture_id": "g", "match_day": "2026-11-09", "opponent": "Garden City",
                                         "agress_cran": 2, "primary_quarts": 0, "tir_cran4_joueurs": 0}])["E1"]["verifies"] == 1
        yield "M3 un match compte une fois (deux faits sur le même amical) : 1 vérifié", \
            auj.verifier(exps(fait(0, "E1", "A"), fait(0, "E1", "A")), [joue(0, cran=2)])["E1"]["verifies"] == 1
        # M4 : amical joué avant le début du test
        d10 = dt.date(2026, 11, 10)
        yield "M4 avant le début, présent (amical du 01/11, début 10/11) : ne compte pour rien", \
            auj.verifier(exps(fait(0, "E1", "A"), debut=d10), [joue(0, cran=2)])["E1"] == {"verifies": 0, "attente": 0, "ecarts": []}
        yield "M4 avant le début, absent (sans début) : le même amical compte", \
            auj.verifier(exps(fait(0, "E1", "A")), [joue(0, cran=2)])["E1"]["verifies"] == 1
        yield "M4 YAML : début 2026-11-10", src.lire_experiences(reg, JOUR9)["debut"] == d10
        yield "M4 aucune écriture au registre : fichiers inchangés après vérification", \
            sorted(p.name for p in reg.iterdir()) == ["fait-2026-11-08.md"]
        yield "H7 fichier absent : None, plan sans ligne de test", \
            src.lire_experiences(reg, JOUR9, reg / "absent.yaml") is None and auj.test_en_cours(None, AM) is None
        yield "H7 fichier présent : E1, E5 (5j), E2 à E4 dans l'ordre", [e["id"] for e in exps()["file"]] == ["E1", "E5", "E2", "E3", "E4"]
        yield "H7 ligne « reste à » ignorée, présent : aucun fait", \
            exps("- reste à faire : saisie de l'amical [expérience=E1:A]")["faits"] == []
        yield "H7 ligne « reste à » ignorée, absent (ligne normale) : 1 fait", len(exps(*e1(1))["faits"]) == 1
        deja = exps("- [16:00 UTC] [clé=Opper Cards 10/11] Saisie de l'amical [expérience=E1:A]", jour=JOUR9)
        yield "H2 fait avec la clé du prochain amical : saisi au niveau A, n'avance pas l'expérience", \
            niveau(deja) == ("E1", "A", True)

        CAL = (COLS_CAL, [("2026-11-10", "amical", "Opper Cards", "2026-11-10T08:00:00", "2026-11-10T07:45:00")])
        donnees = figees(**{"gold.bv_agenda": (AGENDA[0], [
            ("2026-11-10", "07:45:00", 1, "amical", "Avant 07:45 : preset amical sur le match contre Opper Cards")]),
            "calendrier": CAL})
        sans_brief = auj.plan(donnees, {}, JOUR9, MIDI, "", {"experiences": exps()})
        l = [a for a in sans_brief["actions"] if "Opper" in a[2]]
        yield "H3 amical sans brief, présent : une ligne E1 niveau A, verrou 07:45 du calendrier, exports après le match", \
            len(l) == 1 and l[0][0] == dt.datetime(2026, 11, 10, 7, 45) \
            and "test E1 niveau A : agressivité 3 à l'écran (cran 2, équilibrée) sur tous les joueurs" in l[0][2] and "verrou 07:45" in l[0][3] \
            and "aperçu, box scores par quart-temps, réglages utilisés, page Équipe du jour" in l[0][3]
        yield "H3 amical sans brief, absent (pas d'amical aujourd'hui ni demain) : aucune ligne de test", \
            not any("test E" in a[2] + a[3] for a in auj.plan(figees(**{"gold.bv_agenda": (AGENDA[0], [])}), {}, JOUR9, MIDI,
                                                                "", {"experiences": exps()})["actions"])
        tac = [{"type": "amical", "match": "Opper Cards", "date": dt.date(2026, 11, 10), "verrou": "07:30", "manche": None,
                "lieu": "domicile", "preuves": [], "fichier": "briefs/2026-11-09-tactique-amical.md", "age": 0, "vieux": False}]
        avec_brief = [a for a in auj.plan(donnees, {}, JOUR9, MIDI, "", {"experiences": exps(), "tactique": tac})["actions"]
                      if "Opper" in a[2]]
        yield "H3 amical avec brief : une seule ligne, celle du brief, qui porte le test à la place de l'agressivité", \
            len(avec_brief) == 1 and "tactique-amical" in avec_brief[0][4] \
            and "test E1 niveau A : agressivité 3 à l'écran (cran 2, équilibrée) sur tous les joueurs (remplace l'agressivité du brief pour ce match)" in avec_brief[0][3]
        yield "M3 plan, présent : la ligne du test porte l'avancement « E1 : 0 vérifié sur 4 »", \
            "E1 : 0 vérifié sur 4" in l[0][3] and "E1 : 0 vérifié sur 4" in avec_brief[0][3]
        cle_ici = "- [16:00 UTC] [clé=Opper Cards 10/11] Saisie de l'amical [expérience=E1:A]"
        l_ici = [a for a in auj.plan(donnees, {}, JOUR9, MIDI, "", {"experiences": exps(cle_ici)})["actions"] if "Opper" in a[2]]
        yield "M3 plan, saisie déclarée pour cet amical : « 1 déclaré non vérifié (match à exporter) »", \
            "E1 : 0 vérifié sur 4, 1 déclaré non vérifié (match à exporter)" in l_ici[0][3]
        yield "H4 fichier absent : plan sans ligne de test, sans plantage", \
            not any("test E" in a[2] + a[3] for a in auj.plan(donnees, {}, JOUR9, MIDI, "", {"experiences": None})["actions"])

    # H6 : règle de ligue à heure écrite recalée sur le coup d'envoi + decalage_min ; sans coup d'envoi, l'heure écrite
    REG = (["rule_id", "category", "heure", "decalage_min"], [("ligue_preview", "export", "19:30", -30),
                                                              ("ligue_preset", "ligue", "19:45", -15),
                                                              ("ligue_export", "export", "20:50", 50)])
    AG = (AGENDA[0], [("2026-11-09", "19:45:00", 1, "ligue", "Avant 19:45 : vérifier le preset de ligue contre Naked Spartans"),
                      ("2026-11-09", "19:30:00", 2, "export", "Avant 19:45 si possible : exporter la page Preview du match J4")])
    tard = (COLS_CAL, [("2026-11-09", "ligue", "Naked Spartans", "2026-11-09T20:30:00", "2026-11-09T20:15:00")])
    avec = auj.plan(figees(**{"gold.bv_agenda": AG, "calendrier": tard, "regles_agenda": REG}), {}, JOUR9, MIDI, "", {})
    sans = auj.plan(figees(**{"gold.bv_agenda": AG, "regles_agenda": REG}), {}, JOUR9, MIDI, "", {})
    def ag(d, mot):
        return next(a for a in d["actions"] if mot in a[2])
    yield "H6 décalage, présent (coup d'envoi 20:30) : preset 20:15, preview 20:00 « Avant 20:15 si possible »", \
        ag(avec, "preset")[0] == dt.datetime(2026, 11, 9, 20, 15) and ag(avec, "preset")[2].startswith("Avant 20:15") \
        and ag(avec, "Preview")[0] == dt.datetime(2026, 11, 9, 20, 0) and ag(avec, "Preview")[2].startswith("Avant 20:15 si")
    yield "H6 décalage, absent (pas de coup d'envoi) : heures écrites 19:45 et 19:30", \
        ag(sans, "preset")[0] == dt.datetime(2026, 11, 9, 19, 45) and ag(sans, "Preview")[0] == dt.datetime(2026, 11, 9, 19, 30) \
        and ag(sans, "preset")[2].startswith("Avant 19:45")


COLS_PROS = ["rapport_paris", "slot", "name", "position", "age", "tsp_min", "tsp_max"]
PROS = (COLS_PROS, [("2026-11-05T09:00:00.849", 0, "Nael Lopez", "PG", 16, 207, 367),
                    ("2026-11-05T09:00:00.849", 1, "Nathan Vidal", "PF", 16, 219, 379),
                    ("2026-11-05T09:00:00.849", 2, "Sacha Aubert", "C", 17, 244, 404)])
COTE = (["academy_score", "p_high_8_10"], [(79, 21.2)])


def cas_academie():
    """K3 (étape 5e) : une ligne par prospect du dernier rapport ; cas présent et cas absent."""
    MIDI9 = dt.datetime(2026, 11, 9, 12, 0)

    def lignes(donnees, cles=()):
        A = []
        auj.academie(donnees, {}, list(cles), MIDI9, lambda *a: A.append(a))
        return A

    vals = lambda h, c: (["key", "value"], [("academie_valeur_high", h), ("academie_cout_test", c)])
    manque = lignes({"prospects": PROS, "cote_potentiel": COTE, "valeurs_academie": (["key", "value"], [])})
    yield "L5 (remplace K3) deux données manquantes : UNE ligne pour le rapport, qui nomme les deux", \
        len(manque) == 1 and manque[0][2] == "Académie, rapport du 05/11 : 3 prospects ; valeur d'un High inconnue, coût du test inconnu" \
        and manque[0][3] == "donnée manquante : core.game_params.academie_valeur_high, core.game_params.academie_cout_test"
    une = lignes({"prospects": PROS, "cote_potentiel": COTE, "valeurs_academie": (["key", "value"], [("academie_cout_test", 25000)])})
    yield "L5 présent : coût du test en base, valeur d'un High absente → « 3 prospects ; valeur d'un High inconnue »", \
        len(une) == 1 and une[0][2] == "Académie, rapport du 05/11 : 3 prospects ; valeur d'un High inconnue" \
        and "coût du test" not in une[0][2] and une[0][1] == 3
    un_seul = lignes({"prospects": (COLS_PROS, PROS[1][:1]), "cote_potentiel": COTE,
                      "valeurs_academie": (["key", "value"], [("academie_cout_test", 25000)])})
    yield "L5 un seul prospect : « 1 prospect » au singulier", \
        len(un_seul) == 1 and "1 prospect ; valeur d'un High inconnue" in un_seul[0][2]
    yield "L5 absent : les deux données en base, aucune ligne « inconnue », une ligne par prospect", \
        (lambda A: len(A) == 3 and not any("inconnu" in a[2] for a in A))(
            lignes({"prospects": PROS, "cote_potentiel": COTE, "valeurs_academie": vals(200000, 25000)}))
    tester = lignes({"prospects": PROS, "cote_potentiel": COTE, "valeurs_academie": vals(200000, 25000)})
    yield "K3 données présentes : « tester » si P(High) × valeur > coût (21,2 % × 200 000 = 42 400 > 25 000)", \
        len(tester) == 3 and all(a[2].endswith(": tester") and "42 400" in a[3] for a in tester)
    ignorer = lignes({"prospects": PROS, "cote_potentiel": COTE, "valeurs_academie": vals(100000, 25000)})
    yield "K3 données présentes : « ignorer » sinon (21 200 < 25 000)", all(a[2].endswith(": ignorer") for a in ignorer)
    yield "K3 absent : aucun rapport en base, aucune ligne", lignes({"prospects": (COLS_PROS, [])}) == [] and lignes({}) == []
    vieux = (COLS_PROS, [("2026-10-29T09:00:00", 0, "X", "PG", 16, 200, 300)])
    yield "K3 absent : rapport de plus de 7 jours, aucune ligne", lignes({"prospects": vieux, "cote_potentiel": COTE}) == []
    cle = {"nom": "Académie", "date": None, "jour": dt.date(2026, 11, 6), "fichier": "fait-2026-11-06.md"}
    yield "K3 absent : décision déclarée au registre ([clé=Académie]) après le rapport, aucune ligne", \
        lignes({"prospects": PROS, "cote_potentiel": COTE}, [cle]) == []
    ancien = dict(cle, jour=dt.date(2026, 11, 4))
    yield "K3 présent : clé Académie antérieure au rapport, la ligne reste (une seule, L5)", len(lignes({"prospects": PROS}, [ancien])) == 1
    # instantané du jeudi 12/11 : rapport du 05/11 en base, nouveau rapport du jour pas encore exporté : aucune ligne d'académie
    def jeudi(donnees, cles=(), quand=dt.datetime(2026, 11, 12, 14, 51)):
        A = []
        auj.academie(donnees, {}, list(cles), quand, lambda *a: A.append(a))
        return A
    j12 = jeudi({"prospects": PROS, "cote_potentiel": COTE})
    yield "Académie jeudi 12/11 : une ligne priorité 2 « décision requise »", len(j12) == 1 and j12[0][1] == 2 \
        and j12[0][2] == "Académie, rapport du jeudi 12/11 : décision requise"
    yield "Académie jeudi sans aucun rapport en base : la ligne reste", len(jeudi({})) == 1
    yield "Académie vendredi 13/11 : aucune ligne", jeudi({"prospects": PROS}, quand=dt.datetime(2026, 11, 13, 9, 0)) == []
    yield "Académie jeudi, décision déclarée au registre du jour : aucune ligne", \
        jeudi({"prospects": PROS}, [dict(cle, jour=dt.date(2026, 11, 12))]) == []


COLS_REMP = ["name", "best_slot", "fit_best", "replacement_name", "replacement_fit", "gap", "weekly_salary",
             "on_transfer_list", "available", "available_players"]
# Extrait de gold.bv_sell_replacement du 2026-11-09 16:25 Paris (4 lignes sur 14)
REMP = [("Maël Bernard", "PF", 47.8, "Anselmo Albano", 47.8, 0.0, 17303, False, True, 14),
        ("Catalin Ungureanu", "C", 48.5, "Maël Bernard", 47.8, 0.7, 19030, False, True, 14),
        ("Sacha Leclerc", "SG", 42.3, "Nolan Baron", 41.1, 1.2, 13767, False, True, 14),
        ("Léo Lefebvre", "PF", 63.1, "Hadrien Gimenez", 58.8, 4.3, 31803, False, True, 14)]
TOL = (["value"], [(1.0,)])


def cas_vente():
    """L3 (étape 5f) : ligne « Vendre X » ; cas présent et cas absent."""
    def lignes(remp, tol=TOL):
        A = []
        auj.vendre_remplacable({"gold.bv_sell_replacement": (COLS_REMP, remp), "tolerance_vente": tol}, lambda *a: A.append(a))
        return A

    un = lignes(REMP)
    yield "L3 présent : une seule ligne, le plus gros salaire sous la tolérance (Ungureanu 19 030, écart 0,7)", \
        len(un) == 1 and un[0][2] == ("Vendre Catalin Ungureanu : économie 19 030 par semaine, remplaçant Maël Bernard "
                                      "au poste C, écart 0,7") and un[0][4] == "gold.bv_sell_replacement"
    yield "L3 présent : la tolérance vient de la base (2,0 → Lefebvre exclu à 4,3, Ungureanu reste)", \
        lignes(REMP, (["value"], [(2.0,)]))[0][2].startswith("Vendre Catalin Ungureanu")
    yield "L3 absent : aucun écart sous la tolérance, aucune ligne", lignes(REMP[2:]) == []
    yield "L3 absent : tolérance absente de core.game_params, aucune ligne", lignes(REMP, (["value"], [])) == [] \
        and (lambda A: (auj.vendre_remplacable({"gold.bv_sell_replacement": (COLS_REMP, REMP)}, lambda *a: A.append(a)), A)[1])([]) == []
    neuf = [r[:9] + (9,) for r in REMP]
    yield "L3 absent : 9 disponibles, 8 après la vente, aucune ligne", lignes(neuf) == []
    dix = [r[:9] + (10,) for r in REMP]
    yield "L3 présent : 10 disponibles, 9 après la vente, la ligne sort", len(lignes(dix)) == 1
    en_vente = [REMP[0], REMP[1][:7] + (True, False, 14)]
    yield "L3 joueur déjà en vente exclu : Bernard (17 303) à la place d'Ungureanu", \
        lignes(en_vente)[0][2].startswith("Vendre Maël Bernard : économie 17 303")
    yield "L3 absent : dernier du poste (aucun remplaçant, écart nul), aucune ligne", \
        lignes([("X", "C", 30.0, None, None, None, 10000, False, True, 14)]) == []


def cas_boucle():
    """K4 (étape 5e) : ligne de compte de la boucle d'apprentissage ; cas présent et cas absent."""
    def lignes(n, proposees, refs):
        A = []
        d = {"a_evaluer": (["n"], [(n,)]), "decisions_proposees": (["id", "status", "game"], [(i, "proposed", "basketvibe") for i in proposees])}
        auj.boucle(d, refs, lambda *a: A.append(a))
        return A

    ref = lambda i: {"id": i, "fichier": "fait-2026-11-09.md", "ligne": 1}
    deux = lignes(2, [1076], [ref(1076)])
    yield "K4 présent : « 2 décisions à mesurer, 1 fait à relier »", \
        len(deux) == 1 and deux[0][2] == "Boucle d'apprentissage : 2 décisions à mesurer, 1 fait à relier"
    yield "K4 présent : fait seul (décision « proposed » citée au registre), 0 à mesurer", \
        lignes(0, [1076], [ref(1076)])[0][2] == "Boucle d'apprentissage : 0 décision à mesurer, 1 fait à relier"
    yield "K4 absent : n = 0 et aucun fait, aucune ligne", lignes(0, [], []) == []
    yield "K4 absent : identifiant du registre déjà done (pas « proposed »), aucune ligne", lignes(0, [], [ref(1070)]) == []
    yield "K4 absent : sources illisibles, aucune ligne", (lambda A: (auj.boucle({}, None, lambda *a: A.append(a)), A)[1])([]) == []
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "fait-2026-11-09.md").write_text("- [x] saisie [décision=1076]\n- reste à faire [décision=1077]\n", encoding="utf-8")
        refs = auj.lire_refs_decisions(tmp, JOUR9)
    yield "K4 registre lu : [décision=1076] pris, ligne « reste à » ignorée", [r["id"] for r in refs] == [1076]


def cas_marche_5i():
    """5i (X2, X3, X4, X6, X8) : Marché ancien, joueur de besoin, deux plafonds ; chaque cas présent et absent."""
    cb = ["name", "position", "ps", "price_now", "ref_n", "ref_reliable", "bid_ceiling_resale", "resale_margin_p25", "ends_paris"]
    cc = ["name", "position", "ps", "would_rank_in_slot", "enters_top8", "current_price", "price_now", "ends_paris", "ref_p75"]
    vieux = (["ordre", "ecran", "pour_quoi", "dernier_paris", "age_h", "statut"],
             [(8, "Marché (enchères)", "cibles", "2026-11-05T13:00:00", 30, "🟧 à refaire")])
    mince = (["position", "depth", "ps_avg", "ps_max"], [("PG", 2, 49.4, 56.2), ("SG", 4, 46.4, 51.6)])

    def plan5i(bargains, candidates, etat=None):
        d = figees(**{"gold.bv_agenda": (AGENDA[0], []), "gold.bv_daily_alerts": (["priority", "category", "alert"], []),
                      "gold.bv_exports_state": etat or vieux, "gold.bv_position_summary": mince,
                      "gold.bv_market_bargains": (cb, bargains), "gold.bv_market_candidates": (cc, candidates)})
        return auj.plan(d, {}, JOUR, SOIR, "", {})

    # X2 : 3 affaires ouvertes (+ 1 au-delà de 3, 1 finie, 1 référence non fiable) sur une page de 30 h
    affaires = [("Martin", "PG", 57.0, 80000, 9, True, 120000, 40000, "2026-11-06T22:00:00"),
                ("Durand", "SG", 50.0, 10000, 9, True, 60000, 50000, "2026-11-07T09:00:00"),
                ("Perrin", "C", 52.0, 5000, 9, True, 50000, 45000, "2026-11-07T10:00:00"),
                ("Quatre", "C", 51.0, 5000, 9, True, 40000, 35000, "2026-11-07T11:00:00"),
                ("Fini", "PG", 55.0, 1000, 9, True, 90000, 89000, "2026-11-06T08:00:00"),
                ("Fragile", "SF", 50.0, 1000, 2, False, 90000, 89000, "2026-11-07T08:00:00")]
    p = plan5i(affaires, [])
    lig = [a for a in p["actions"] if a[2].startswith("Enchère maximale")]
    martin = next((a for a in lig if "Martin" in a[2]), None)
    yield "X2 présent : au plus 3 lignes d'affaire sur une page de 30 h", len(lig) == 3
    yield "X2 présent : nom, poste, PS, plafond de revente, prix à l'export, fin, âge de la page", martin is not None \
        and "Enchère maximale 120 000 sur Martin (PG, PS 57.0)" in martin[2] and "plafond de revente" in martin[3] \
        and "prix à l'export 80 000" in martin[3] and "fin 06/11 22:00" in martin[3] \
        and "page du Marché de 30 h : le prix a pu monter" in martin[3]
    yield "X2 absent : annonce finie et référence non fiable écartées", not any(n in a[2] for a in lig for n in ("Fini", "Fragile"))
    pf = plan5i([affaires[4]], [])
    yield "X2 absent : toutes finies, aucune ligne, la demi-ligne Garder dit le Marché du 05/11", \
        not [a for a in pf["actions"] if a[2].startswith("Enchère maximale")] \
        and any("aucune affaire fiable ouverte dans le Marché du 05/11" in g for g in pf["garder"])
    # X3 : joueur de besoin au poste PG (note ≥ 57,2), capacité 279 666 (solde, aucune enchère ouverte)
    cands = [("Dupuis", "PG", 58.0, 1, True, 100000, 100000, "2026-11-06T21:00:00", 150000),
             ("Borne", "PG", 58.5, 1, True, 200000, 200000, "2026-11-07T10:00:00", 400000),
             ("Cher", "PG", 59.0, 1, True, 300000, 300000, "2026-11-07T10:00:00", 400000),
             ("Bas", "PG", 56.0, 2, True, 1000, 1000, "2026-11-07T10:00:00", 5000),
             ("Ailier", "SF", 60.0, 1, True, 1000, 1000, "2026-11-07T10:00:00", 5000),
             ("Tard", "PG", 60.0, 1, True, 1000, 1000, "2026-11-06T08:00:00", 5000)]
    p3 = plan5i([], cands)
    ach = next((a for a in p3["actions"] if a[2].startswith("Acheter un PG")), None)
    yield "X3 présent : nomme les annonces au poste qui atteignent la note, prix à l'export, fin, plafond de besoin à valider", ach is not None \
        and "Dupuis (PS 58.0) : 100 000 à l'export, fin 06/11 21:00, plafond de besoin 150 000, à valider" in ach[2]
    yield "X3 présent : plafond de besoin borné par la capacité (p75 400 000 → 279 666)", ach is not None and "Borne (PS 58.5) : 200 000 à l'export, fin 07/11 10:00, plafond de besoin 279 666, à valider" in ach[2]
    yield "X3 absent : note non atteinte, autre poste, fin passée, prix au-dessus du plafond", ach is not None \
        and not any(n in ach[2] for n in ("Bas", "Ailier", "Tard", "Cher"))
    frais = (vieux[0], [(8, "Marché (enchères)", "cibles", "2026-11-06T13:00:00", 6, "🟩 à jour")])
    pa = plan5i([], [], frais)
    aucun = next((a for a in pa["actions"] if a[2].startswith("Acheter un PG")), None)
    yield "X3 absent : aucune annonce, Marché à jour : le dit avec la date du Marché", aucun is not None \
        and "aucune annonce au poste PG dans le Marché du 06/11" in aucun[2]
    # R4 : Marché périmé (règle de gold.bv_exports_state) : « Acheter un X : aucune annonce » devient la demande d'export du Marché
    pp = plan5i([], [])
    yield "R4 Marché périmé, aucune annonce : plus de ligne « Acheter un PG », l'export du Marché est demandé", \
        not any(a[2].startswith("Acheter un PG") for a in pp["actions"]) and "Marché (enchères) (30 h)" in pp["exports"]
    pj = plan5i([], [], (vieux[0], [(8, "Marché (enchères)", "cibles", None, None, "🟥 jamais")]))
    yield "R4 Marché jamais exporté, aucune annonce : même demande", not any(a[2].startswith("Acheter un PG") for a in pj["actions"]) \
        and "Marché (enchères) (jamais exporté)" in pj["exports"]
    yield "R4 Marché périmé, des annonces au poste : la ligne reste (annonces à l'export, âge de la page dit)", any(
        a[2].startswith("Acheter un PG") and "Dupuis" in a[2] for a in plan5i([], [("Dupuis", "PG", 58.0, 1, True, 100000, 100000, "2026-11-06T21:00:00", 150000)])["actions"])
    # X4 et X8
    yield "X4 chaque ligne d'enchère dit « fenêtre de mise non mesurée »", all("fenêtre de mise non mesurée : mise près de la fin ; ne dépasse pas le plafond" in a[3]
                                                                            for a in p3["actions"] + p["actions"] if a[2].startswith(("Enchère maximale", "Acheter un PG")) and "annonce" not in a[2])
    yield "X8 affaire : « plafond de revente » seul ; besoin : « plafond de besoin » seul", martin is not None and ach is not None \
        and "plafond de besoin" not in martin[2] + martin[3] and "plafond de revente" not in ach[2] + ach[3]
    # X6 : 8 lignes au plus, les enchères qui finissent aujourd'hui passent en tête
    p6 = plan5i(affaires, cands)
    p6["actions"] += [(dt.datetime(2026, 11, 6, 20, i), 2, f"action {i}", "", "") for i in range(7)]
    t6 = auj.rendre(p6, JOUR)
    yield "X6 8 lignes au plus ; Martin (fin 22:00) et Dupuis (fin 21:00) restent malgré 7 autres actions", \
        len(t6.splitlines()) <= 8 and "Martin" in t6 and "Dupuis" in t6


def cas_composition_5j():
    """5j (Y2, Y3) : lignes de composition d'après les aperçus en base ; cas présent et cas absent."""
    cols = ["fixture_id", "competition_kind", "round_no", "day", "opponent", "capture_paris", "adverse"]
    cal = (["day", "competition_kind", "opponent", "coup_envoi_paris", "verrou_paris"], [
        ("2026-11-09", "ligue", "Naked Spartans", "2026-11-09T20:00:00", "2026-11-09T19:45:00"),
        ("2026-11-10", "ligue", "BC KIT", "2026-11-10T20:00:00", "2026-11-10T19:45:00")])
    matin = dt.datetime(2026, 11, 9, 10, 0)
    brief = lambda jour_b: {"type": "ligue", "match": "Naked Spartans", "manche": "J4", "lieu": "domicile", "date": JOUR9, "verrou": "19:45",
                            "preuves": [], "fichier": f"briefs/{jour_b}-tactique.md", "age": 1, "vieux": False}

    def lignes(rows, S=None, maintenant=matin):
        d = figees(**{"gold.bv_agenda": (AGENDA[0], []), "calendrier": cal, "apercus_matchs": (cols, rows)})
        return auj.plan(d, {}, JOUR9, maintenant, "", S or {})

    def spart(capture, adverse="A,B,C", jour="2026-11-09", adv="Naked Spartans", rang=4):
        return ("f1", "ligue", rang, jour, adv, capture, adverse)

    def a(p, mot):
        return [x for x in p["actions"] if mot in x[2] or mot in x[3]]

    # Y2 : aperçu en base et aucun brief plus récent
    p = lignes([spart("2026-11-08T11:31:58")])
    y2 = a(p, "lance l'agent tactique (aperçu du 08/11 en base)")
    yield "Y2 présent : « Composition J4 contre Naked Spartans : lance l'agent tactique (aperçu du 08/11 en base) », limite = verrou 19:45", \
        len(y2) == 1 and y2[0][2].startswith("Composition J4 contre Naked Spartans") and y2[0][0] == dt.datetime(2026, 11, 9, 19, 45)
    yield "Y2 présent : le plan rendu reste à 8 lignes au plus", len(auj.rendre(p, JOUR9).splitlines()) <= 8
    p2 = lignes([spart("2026-11-08T11:31:58")], {"tactique": [brief("2026-11-08")]})
    yield "Y2 présent : brief du jour de l'aperçu = « Saisis la composition : python -I pipelines/composition.py » dans la ligne du match, pas de relance", \
        not a(p2, "lance l'agent tactique (aperçu") and len(a(p2, "Saisis la composition : python -I pipelines/composition.py \"Naked Spartans\"")) == 1
    p3 = lignes([spart("2026-11-08T11:31:58")], {"tactique": [brief("2026-11-07")]})
    yield "Y2 présent : brief plus ancien que l'aperçu = relance, pas de saisie proposée", \
        len(a(p3, "lance l'agent tactique (aperçu")) == 1 and not a(p3, "Saisis la composition")
    yield "Y2 absent : aperçu absent (aucune capture), aucune ligne de composition", \
        not a(lignes([spart(None)]), "Composition") and not a(lignes([]), "Composition")
    yield "Y2 absent : verrou passé, aucune ligne", not a(lignes([spart("2026-11-08T11:31:58")], maintenant=dt.datetime(2026, 11, 9, 20, 30)), "Composition")
    # Y3 : rappel J-1
    ancien = lignes([spart("2026-11-08T08:00:00")])
    yield "Y3 présent : verrou dans moins de 24 h et aperçu de plus de 24 h = « Réexporte l'aperçu : l'effectif adverse a pu changer »", \
        len(a(ancien, "Réexporte l'aperçu : l'effectif adverse a pu changer")) == 1
    yield "Y3 absent : aperçu de 8 h", not a(lignes([spart("2026-11-09T02:00:00")]), "Réexporte l'aperçu")
    yield "Y3 absent : verrou à plus de 24 h (BC KIT le 10/11 19:45)", not a(lignes([spart("2026-11-06T08:00:00", jour="2026-11-10", adv="BC KIT", rang=5)]), "Réexporte l'aperçu")
    deux = lignes([spart("2026-11-08T08:00:00", "A,B,C"), spart("2026-11-09T02:00:00", "A,B,D")])
    ch = a(deux, "composition adverse changée : relance l'agent tactique")
    yield "Y3 présent : deux aperçus qui diffèrent = « composition adverse changée », entrés D, sortis C", \
        len(ch) == 1 and "entrés : D" in ch[0][3] and "sortis : C" in ch[0][3] and not a(deux, "lance l'agent tactique (aperçu")
    yield "Y3 absent : deux aperçus identiques", not a(lignes([spart("2026-11-08T08:00:00"), spart("2026-11-09T02:00:00")]), "composition adverse changée")
    yield "Y3 absent : un brief daté de la dernière capture en tient compte", \
        not a(lignes([spart("2026-11-08T08:00:00", "A,B,C"), spart("2026-11-09T02:00:00", "A,B,D")], {"tactique": [brief("2026-11-09")]}), "composition adverse changée")
    yield "Y5 plan complet avec composition et rappel : 8 lignes au plus", len(auj.rendre(deux, JOUR9).splitlines()) <= 8


def cas_experience_e5():
    """5j, Y4 : E5 « zone défensive » dans le vrai fichier des expériences, entre E1 et E2 ; E1 écrit ses constantes."""
    exps = src.lire_experiences(ESSAI, JOUR)
    ids = [e["id"] for e in exps["file"]]
    e1, e5 = exps["file"][0], next((e for e in exps["file"] if e["id"] == "E5"), None)
    yield "Y4 présent : E5 placée après E1 et avant E2", ids[:3] == ["E1", "E5", "E2"]
    yield "Y4 présent : E5 alterne Perimeter, Middle, Rim, une zone par niveau, focus 3 constant", e5 is not None \
        and e5["zone"] == {"A": "Perimeter", "B": "Middle", "C": "Rim"} and e5["ordre"] == ["A", "B", "C"] and e5["constants"] == {"focus": 3}
    yield "Y4 présent : E1 écrit zone Perimeter et focus 3 comme constantes", e1["constants"] == {"zone": "Perimeter", "focus": 3}
    termine = {"file": [{**e1, "amicaux_vises": 0}] + exps["file"][1:], "faits": [], "debut": None}
    am = {"match": "Opper Cards", "date": dt.date(2026, 11, 10), "limite": dt.datetime(2026, 11, 10, 7, 45)}
    t = auj.test_en_cours(termine, am, [])
    yield "Y4 présent : E1 terminée, le test suivant est E5 niveau A (pas E2)", t is not None and t[0]["id"] == "E5" and t[1] == "A" \
        and auj.texte_test(t[0], t[1]) == "test E5 niveau A : zone Perimeter (1) sur les adversaires"
    yield "Y4 absent : aucune expérience ne teste le focus défensif par joueur adverse", \
        not any("joueur adverse" in e["reglage"] or "focus défensif" in e["reglage"] for e in exps["file"])
    yield "Y4 absent : fichier d'expériences illisible, aucune expérience (H4)", src.lire_experiences(ESSAI, JOUR, ESSAI / "absent.yaml") is None


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


def cas_t7():
    """5n T7 : sortie du script = blocs 0 à 10, puis séparateur et consignes ; l'instantané n'a ni séparateur ni consigne."""
    res = {"actions": [(None, 1, "Composition J5 contre Naked Spartans : lance l'agent tactique (aperçu du 10/11 en base)", "", "s")],
           "exports": [], "garder": [], "infos": [], "capacite": None}
    jour, maint = dt.date(2026, 11, 10), dt.datetime(2026, 11, 10, 15, 50)
    affichage, instantane = auj.rendre_jour(res, {}, {}, jour, maint, {}, etudes=[], base=ESSAI)
    avant, _, apres = affichage.partition(auj.SEPARATEUR)
    yield "T7 sortie : les 11 blocs sont avant le séparateur", all(f"## Bloc {n} — " in avant for n in range(11))
    yield "T7 sortie : le séparateur est exact", auj.SEPARATEUR == "--- session (à exécuter, ne pas afficher) ---" and affichage.count(auj.SEPARATEUR) == 1
    yield "T7 sortie : la consigne de l'agent tactique est après le séparateur, jamais avant", "lance l'agent tactique" in apres and "lance l'agent tactique" not in avant
    yield "T7 instantané : le rendu sans séparateur ni consigne", auj.SEPARATEUR not in instantane and "lance l'agent tactique" not in instantane \
        and instantane.strip() == avant.strip()
    sans = dict(res, actions=[(None, 1, "Export : page Effectif", "", "s")])
    aff2, inst2 = auj.rendre_jour(sans, {}, {}, jour, maint, {}, etudes=[], base=ESSAI)
    yield "T7 sortie : sans consigne, pas de séparateur", auj.SEPARATEUR not in aff2 and aff2.strip() == inst2.strip()
    source = Path(auj.__file__).read_text(encoding="utf-8")
    yield "T7 main : imprime le rendu en blocs (rendre_jour), plus rendre/plier", "rendre_jour(" in source.split("def main")[1] and "plier(rendre(" not in source


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    echecs = 0
    jeux = list(cas()) + list(cas_t7()) + (list(cas_base()) if "--base" in sys.argv else [])
    for nom, ok in jeux:
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    n = len(jeux)
    print(f"{n - echecs}/{n}")
    sys.exit(1 if echecs else 0)
