"""Test de pipelines/aujourdhui.py sur des données figées (sans réseau ni base).

Lancer : python pipelines/test_soir.py   (code 1 si un cas se trompe)
"""
import datetime as dt
import importlib.util
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("soir", Path(__file__).resolve().parent / "aujourdhui.py")
soir = importlib.util.module_from_spec(spec)
spec.loader.exec_module(soir)
spec_f = importlib.util.spec_from_file_location("forme", Path(__file__).resolve().parent / "forme.py")
forme = importlib.util.module_from_spec(spec_f)
spec_f.loader.exec_module(forme)

JOUR = dt.date(2026, 11, 6)
SOIR = dt.datetime(2026, 11, 6, 19, 0)


def figees(**remplace):
    d = {
        "gold.bv_agenda": (["day", "at_time", "priority", "category", "action"], [
            (JOUR, "19:45", 1, "ligue", "Avant 19:45 : régler le focus défensif du match J3 contre Póvoa (domicile)"),
            (JOUR, "20:50", 2, "export", "Après le match (~20:50) : exporter la page du match J3"),
            (JOUR + dt.timedelta(days=3), "04:30", 1, "export", "trop loin"),
        ]),
        "gold.bv_exports_state": (["ordre", "ecran", "pour_quoi", "dernier_paris", "age_h", "statut"], [
            (1, "Équipe (aperçu, joueurs)", "effectif", None, 5, "🟩 à jour"),
            (8, "Marché (enchères)", "cibles", None, 30, "🟧 à refaire"),
            (13, "Personnel", "staff", None, None, "🟥 jamais"),
        ]),
        "gold.bv_daily_alerts": (["priority", "category", "alert"], [
            (2, "fatigue", "Dupont : fatigue 25 (hors zone verte)"),
            (3, "export", "Finances : dernier export il y a 8 jour(s)"),
        ]),
        "gold.bv_finance_health": (["solde", "weekly_result_est"], [(1000, -50)]),
        "gold.bv_finance_projection": (["solde_fin"], [(900,)]),
        "gold.bv_position_summary": (["position", "n"], [("PG", 3)]),
        "gold.bv_roster_now": (["name"], [("Dupont",)]),
        "gold.bv_next_opponents": (["opponent"], [("Póvoa",)]),
        "gold.bv_market_bargains": (["name", "prix"], [("Martin", 5000)]),
        "gold.bv_market_price_ref": (["position", "median"], [("PG", 6000)]),
        "gold.bv_personnel_status": (["role", "hired"], [("coach", 1)]),
        "apercus": (["match_day"], []),
        "derniere_vente": (["derniere"], [(dt.date(2026, 11, 3),)]),
    }
    d.update(remplace)
    return d


def texte(donnees, erreurs=None):
    return soir.rendre(soir.plan(donnees, erreurs or {}, JOUR, SOIR), JOUR, erreurs)


def cas():
    t = texte(figees())
    lignes = soir.plan(figees(), {}, JOUR, SOIR)
    yield "exports en tête", t.index("## Exports à faire aujourd'hui") < t.index("## Composition")
    yield "agenda : jour courant gardé", "focus défensif du match J3" in t
    yield "agenda : jour lointain écarté", "trop loin" not in t
    yield "export en retard nommé", "Exporte Marché (enchères) (dernier export il y a 30 h)" in t
    yield "jamais exporté = URGENT", any(l[1] == 1 and "Personnel" in l[3] and "jamais" in l[3] for l in lignes)
    yield "aperçu demandé (aucune ligne adverse)", "Exporte l'aperçu du match de ligue du 06/11" in t
    yield "historique des transferts demandé (vente du 03/11)", "Exporte l'historique global des transferts depuis 2026-11-03" in t
    yield "alerte export non doublée", "Finances : dernier export il y a 8" not in t
    yield "marché périmé : pas de bonne affaire", "il me manque un Marché de moins de 24 h" in t and "bonne affaire" not in t
    ok = figees()
    ok["gold.bv_exports_state"] = (ok["gold.bv_exports_state"][0], [(8, "Marché (enchères)", "cibles", None, 3, "🟩 à jour")])
    yield "marché frais : bonne affaire lue", "bonne affaire : name=Martin" in texte(ok)
    yield "heure : 19:30 avant 19:45 dans Exports", t.index("19:30") < t.index("20:50")
    yield "donnée absente", "il me manque gold.bv_finance_health" in texte(figees(**{"gold.bv_finance_health": None}), {"gold.bv_finance_health": "boum"})
    yield "rejeu non disponible", "rejeu non disponible pour gold.bv_agenda" in texte(figees(**{"gold.bv_agenda": "rejeu"}))
    yield "après 18:00 : demain avant 10:00 ajouté", "tôt demain" in texte(figees(**{"gold.bv_agenda": (
        ["day", "at_time", "priority", "category", "action"],
        [(JOUR + dt.timedelta(days=1), "04:30", 1, "export", "tôt demain")])}))
    opp = (["match_day", "opponent"], [(dt.date(2026, 11, 4), "Passé FC"), (dt.date(2026, 11, 7), "Futur BC")])
    to = texte(figees(**{"gold.bv_next_opponents": opp}))
    yield "adversaire : match passé non rendu", "Passé FC" not in to and "Futur BC" in to
    fait = "- [13:47 utc] mes enchères — source : déclaré\n- [13:47 utc] saisie de la ligue à póvoa — source : déclaré\n"
    ef = figees()
    ef["gold.bv_exports_state"] = (ef["gold.bv_exports_state"][0], [(9, "Mes enchères", "ventes", None, 51, "🟧 à refaire")])
    tf = soir.rendre(soir.plan(ef, {}, JOUR, SOIR, fait), JOUR)
    yield "registre : export déjà fait non redemandé", "Exporte Mes enchères" not in tf and "Mes enchères (registre du jour)" in tf
    yield "registre : saisie de ligue faite retirée du plan", "| 🟥 URGENT | Tactique | 19:45" not in tf and "Déjà fait (registre du jour)" in tf
    yield "sans registre : rien retiré", "Exporte Mes enchères" in soir.rendre(soir.plan(ef, {}, JOUR, SOIR), JOUR)
    # format de forme.py : chaque tableau rendu passe le contrôle du plan
    fautes = []
    for cols, lg in forme.tableaux(t):
        if cols[:2] == ["priorite", "categorie"]:
            fautes += forme.plan(cols, lg)
    yield "format forme.py (pastilles, catégories)", not fautes


if __name__ == "__main__":
    echecs = 0
    for nom, ok in cas():
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    n = sum(1 for _ in cas())
    print(f"{n - echecs}/{n}")
    sys.exit(1 if echecs else 0)
