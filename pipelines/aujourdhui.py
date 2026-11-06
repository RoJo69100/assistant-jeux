"""Que faire aujourd'hui BasketVibe, sans modèle ni agent (refonte v3, lot L2).

Exécute en lecture seule (executer() de sql.py) les étapes 1, 4, 5 et 6 du skill basketvibe-aujourdhui,
puis rend un tableau par catégorie au format de forme.py (Priorité | Catégorie | Action), triés par heure limite.

Usage :
  python -I pipelines/aujourdhui.py basketvibe [--jour AAAA-MM-JJ]
Rejeu (--jour) : seules les vues qui savent lire un jour passé sont rejouées ; toutes les autres, qui lisent
current_date ou now(), répondent « rejeu non disponible pour <vue> ». Chaque exécution ajoute une ligne à
docs/refonte-v3/journal-aujourdhui.md. Une donnée absente s'écrit « il me manque X — export Y ».
"""
import argparse
import datetime as dt
import importlib.util
import sys
import time
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
JOURNAL = RACINE / "docs/refonte-v3/journal-aujourdhui.md"
PASTILLE = {1: "🟥 URGENT", 2: "🟧 IMPORTANT", 3: "🟩 SUIVI"}
ORDRE_CAT = ["Exports", "Composition", "Tactique", "Entraînement", "Transferts", "Finances", "Personnel"]
CATEGORIE_FORME = {"Exports": "Export", "Personnel": "Finances"}  # catégories fixes de forme.py
CAT_AGENDA = {"ligue": "Tactique", "amical": "Composition", "entraînement": "Entraînement",
              "transfert": "Transferts", "export": "Exports", "saison": "Composition"}
CAT_ALERTE = {"blessure": "Composition", "fatigue": "Composition", "forme": "Composition",
              "finances": "Finances", "transferts": "Transferts", "export": "Exports"}
MAX_COL = 8  # colonnes d'une vue affichées en « clé=valeur »
# Registre outputs/basketvibe/fait-<jour>.md (skill deja-fait) : écran de bv_exports_state ou catégorie
# d'agenda -> mots qui, présents dans une ligne du registre, retirent l'action du plan (« Déjà fait »).
MOTS_FAIT = {
    "Mes enchères": ("mes enchères",),
    "Amical : tactique du match": ("export de l'amical",),
    "Personnel": ("personnel",),
    "Finances": ("finances",),
    "Entraînement": ("entraînement",),
    "Académie": ("académie",),
    "Marché (enchères)": ("transferts en cours", "marché"),
    "Match de ligue : aperçu": ("aperçu",),
    "ligue": ("saisie de la ligue",),
    "amical": ("saisie de l'amical",),
}

REQUETES = {
    "gold.bv_agenda": "select day, at_time, priority, category, action from gold.bv_agenda "
                      "where day <= current_date + 1 order by day, at_time, priority",
    "gold.bv_exports_state": "select ordre, ecran, pour_quoi, dernier_paris, age_h, statut from gold.bv_exports_state order by ordre",
    "gold.bv_daily_alerts": "select priority, category, alert from gold.bv_daily_alerts order by priority limit 30",
    "gold.bv_finance_health": "select * from gold.bv_finance_health limit 3",
    "gold.bv_finance_projection": "select * from gold.bv_finance_projection limit 3",
    "gold.bv_position_summary": "select * from gold.bv_position_summary limit 10",
    "gold.bv_roster_now": "select name, position, age, form, fatigue, injury_return_on from gold.bv_roster_now order by name limit 20",
    "gold.bv_next_opponents": "select * from gold.bv_next_opponents limit 3",
    "gold.bv_market_bargains": "select * from gold.bv_market_bargains limit 5",
    "gold.bv_market_price_ref": "select * from gold.bv_market_price_ref limit 5",
    "gold.bv_personnel_status": "select * from gold.bv_personnel_status limit 10",
    "apercus": "select distinct match_day from gold.bv_saisie_adversaires "
               "where kind in ('ligue', 'coupe') and match_day >= current_date",
    "derniere_vente": "select max(sold_on) as derniere from gold.bv_transfer_history",
}
# Vues rejouables sur un jour passé : requête de remplacement avec le paramètre {jour}.
REJEU = {
    "derniere_vente": "select max(sold_on) as derniere from gold.bv_transfer_history where sold_on <= '{jour}'",
}


def charger_sql():
    spec = importlib.util.spec_from_file_location("sqlmod", Path(__file__).resolve().parent / "sql.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def lire_tout(executer, jour=None):
    """{nom: (colonnes, lignes) | None | 'rejeu'} ; None = lecture impossible, message dans erreurs."""
    donnees, erreurs, n = {}, {}, 0
    for nom, sql in REQUETES.items():
        if jour:
            if nom not in REJEU:
                donnees[nom] = "rejeu"
                continue
            sql = REJEU[nom].format(jour=jour)
        try:
            donnees[nom] = executer(sql)
            n += 1
        except SystemExit as e:  # sql.py termine par sys.exit(message)
            donnees[nom], erreurs[nom] = None, str(e)
            n += 1
        except Exception as e:  # noqa: BLE001 - une vue en échec ne doit pas arrêter le plan
            donnees[nom], erreurs[nom] = None, f"{type(e).__name__}: {e}"
            n += 1
    return donnees, erreurs, n


def lignes_de(donnees, nom):
    d = donnees.get(nom)
    if not d or d == "rejeu":
        return []
    cols, lignes = d
    return [dict(zip(cols, l)) for l in lignes]


def manque(donnees, erreurs, nom, export):
    """Texte « il me manque … » si la vue n'est pas lisible, sinon None."""
    if donnees.get(nom) == "rejeu":
        return f"rejeu non disponible pour {nom}"
    if donnees.get(nom) is None:
        return f"il me manque {nom} ({erreurs.get(nom, 'illisible')[:60]}) — export {export}"
    return None


def kv(ligne):
    return ", ".join(f"{k}={'' if v is None else v}" for k, v in list(ligne.items())[:MAX_COL])


def heure(v):
    return None if v is None else str(v)[:5]


def lire_fait(jour):
    """Texte du registre du jour en minuscules (apostrophes droites), vide s'il n'existe pas."""
    f = RACINE / "outputs/basketvibe" / f"fait-{jour.isoformat()}.md"
    return f.read_text(encoding="utf-8").lower().replace("’", "'") if f.exists() else ""


def deja(fait, cle):
    return any(m in fait for m in MOTS_FAIT.get(cle, ()))


def plan(donnees, erreurs, jour, maintenant, fait=""):
    """Liste de (catégorie, priorité 1-3, heure 'HH:MM' | None, action) ; catégorie « Déjà fait » pour le registre."""
    out = []
    # 1. Agenda (aujourd'hui, et demain avant 10:00 après 18:00 : règle d'horizon du skill, étape 1)
    m = manque(donnees, erreurs, "gold.bv_agenda", "Équipe (aperçu, joueurs)")
    if m:
        out.append(("Exports", 2, None, m))
    for r in lignes_de(donnees, "gold.bv_agenda"):
        d = r["day"] if isinstance(r["day"], dt.date) else dt.date.fromisoformat(str(r["day"])[:10])
        h = heure(r["at_time"])
        if d == jour or (d == jour + dt.timedelta(days=1) and maintenant.hour >= 18 and h and h < "10:00"):
            if deja(fait, r["category"]):
                out.append(("Déjà fait", 3, h, r["action"]))
                continue
            out.append((CAT_AGENDA.get(r["category"], "Composition"), int(r["priority"]), h, r["action"]))
    # 4. Exports en retard + aperçu + historique des transferts
    m = manque(donnees, erreurs, "gold.bv_exports_state", "tous les écrans")
    if m:
        out.append(("Exports", 2, None, m))
    etat = {r["ecran"]: r for r in lignes_de(donnees, "gold.bv_exports_state")}
    for r in etat.values():
        if not str(r["statut"]).endswith("à jour"):
            if deja(fait, r["ecran"]):
                out.append(("Déjà fait", 3, None, f"{r['ecran']} (registre du jour)"))
                continue
            age ="jamais exporté" if r["age_h"] is None else f"dernier export il y a {int(r['age_h'])} h"
            out.append(("Exports", 1 if "jamais" in str(r["statut"]) else 2, None,
                        f"Exporte {r['ecran']} ({age}) — sert à : {r['pour_quoi']}"))
    ligues = [r for r in lignes_de(donnees, "gold.bv_agenda") if r["category"] == "ligue"]
    apercus = {str(r["match_day"])[:10] for r in lignes_de(donnees, "apercus")}
    if donnees.get("apercus") is None:
        out.append(("Exports", 2, None, manque(donnees, erreurs, "apercus", "Match de ligue : aperçu")))
    for r in ligues:
        d = str(r["day"])[:10]
        if jour <= dt.date.fromisoformat(d) <= jour + dt.timedelta(days=2) and d not in apercus:
            out.append(("Exports", 1, "19:30", f"Exporte l'aperçu du match de ligue du {d[8:]}/{d[5:7]} "
                        f"(aucune ligne adverse en base) — {r['action'].split(' contre ')[-1]}"))
    vente = lignes_de(donnees, "derniere_vente")
    derniere = vente[0]["derniere"] if vente else None
    if donnees.get("derniere_vente") is None:
        out.append(("Exports", 2, None, manque(donnees, erreurs, "derniere_vente", "Historique global des transferts")))
    elif derniere is None or dt.date.fromisoformat(str(derniere)[:10]) < jour - dt.timedelta(days=1):
        out.append(("Exports", 2, None, "Exporte l'historique global des transferts depuis "
                    f"{'le début' if derniere is None else str(derniere)[:10]} (référence de prix à mettre à jour)"))
    # 5. Alertes
    m = manque(donnees, erreurs, "gold.bv_daily_alerts", "Équipe (aperçu, joueurs)")
    if m:
        out.append(("Composition", 2, None, m))
    for r in lignes_de(donnees, "gold.bv_daily_alerts"):
        cat = CAT_ALERTE.get(r["category"])
        if cat and cat != "Exports":  # les exports en retard viennent déjà de bv_exports_state
            out.append((cat, int(r["priority"]), None, r["alert"]))
    # 6. Bilan du club : chiffres lus, sans décision (aucun modèle)
    for nom, cat, export in [("gold.bv_finance_health", "Finances", "Finances"),
                             ("gold.bv_finance_projection", "Finances", "Finances"),
                             ("gold.bv_position_summary", "Composition", "Équipe (aperçu, joueurs)"),
                             ("gold.bv_next_opponents", "Composition", "Classement"),
                             ("gold.bv_personnel_status", "Personnel", "Personnel")]:
        m = manque(donnees, erreurs, nom, export)
        if m:
            out.append((cat, 3, None, m))
            continue
        for r in lignes_de(donnees, nom):
            if nom == "gold.bv_next_opponents" and r.get("match_day") is not None \
                    and dt.date.fromisoformat(str(r["match_day"])[:10]) < jour:
                continue  # la vue peut garder un match déjà joué : on ne rend que les matchs à venir
            out.append((cat, 3, None, f"{nom.split('.')[1]} : {kv(r)}"))
    m = manque(donnees, erreurs, "gold.bv_roster_now", "Équipe (aperçu, joueurs)")
    if m:
        out.append(("Composition", 3, None, m))
    marche = etat.get("Marché (enchères)")
    m = manque(donnees, erreurs, "gold.bv_market_bargains", "Marché (enchères)")
    if m:
        out.append(("Transferts", 2, None, m))
    elif marche is None or not str(marche["statut"]).endswith("à jour"):
        out.append(("Transferts", 2, None, "il me manque un Marché de moins de 24 h — export Marché (enchères)"))
    else:
        for r in lignes_de(donnees, "gold.bv_market_bargains"):
            out.append(("Transferts", 2, None, f"bonne affaire : {kv(r)}"))
        if donnees.get("gold.bv_market_price_ref") is None:
            out.append(("Transferts", 3, None, "il me manque gold.bv_market_price_ref — export Historique des transferts"))
    return out


def rendre(lignes, jour, erreurs=None):
    """Tableaux Markdown : « Exports à faire aujourd'hui » d'abord, puis une catégorie par tableau."""
    def tri(l):
        return (l[2] is None, l[2] or "", l[1])

    texte = [f"# Que faire aujourd'hui BasketVibe — {jour.isoformat()}", ""]
    for cat in ORDRE_CAT:
        sel = sorted((l for l in lignes if l[0] == cat), key=tri)
        if not sel:
            continue
        titre = "Exports à faire aujourd'hui" if cat == "Exports" else cat
        texte += [f"## {titre}", "", "| Priorité | Catégorie | Action |", "|---|---|---|"]
        for _, prio, h, action in sel:
            a = (f"{h} — " if h else "") + str(action).replace("|", "/").replace("\n", " ")
            texte.append(f"| {PASTILLE[min(max(prio, 1), 3)]} | {CATEGORIE_FORME.get(cat, cat)} | {a} |")
        texte.append("")
    faits = [l[3] for l in lignes if l[0] == "Déjà fait"]
    if faits:  # skill deja-fait : liste, jamais une demande
        texte += ["Déjà fait (registre du jour) : " + " ; ".join(faits), ""]
    if erreurs:
        texte.append("Vues illisibles : " + "; ".join(f"{k} ({v[:60]})" for k, v in erreurs.items()))
    return "\n".join(texte)


def journaliser(jour, secondes, requetes):
    if not JOURNAL.exists():
        JOURNAL.write_text("# Journal de durée de `aujourdhui.py` (une ligne par exécution)\n\n"
                           "| Date | Jour du plan | Durée (s) | Requêtes |\n|---|---|---|---|\n", encoding="utf-8")
    with JOURNAL.open("a", encoding="utf-8") as f:
        f.write(f"| {dt.datetime.now().strftime('%Y-%m-%d %H:%M')} | {jour} | {secondes:.1f} | {requetes} |\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("jeu")
    ap.add_argument("--jour", help="AAAA-MM-JJ : rejeu d'un jour passé quand la vue le permet")
    a = ap.parse_args()
    if a.jeu != "basketvibe":
        sys.exit("aujourdhui.py : seul basketvibe est branché (lot L2)")
    jour = dt.date.fromisoformat(a.jour) if a.jour else dt.date.today()
    maintenant = dt.datetime.now()
    debut = time.time()
    sqlmod = charger_sql()
    donnees, erreurs, n = lire_tout(sqlmod.executer, a.jour)
    sys.stdout.reconfigure(encoding="utf-8")
    rendu = rendre(plan(donnees, erreurs, jour, maintenant, lire_fait(jour)), jour, erreurs)
    print(rendu)
    if not a.jour:  # instantané quotidien (écrasé si relancé le même jour) : remplace le rejeu
        fichier = RACINE / "outputs/basketvibe" / f"aujourdhui-{jour.isoformat()}.md"
        fichier.parent.mkdir(parents=True, exist_ok=True)
        fichier.write_text(f"<!-- généré le {maintenant.strftime('%Y-%m-%d %H:%M')} -->\n{rendu}\n", encoding="utf-8")
    nonrej = [k for k, v in donnees.items() if v == "rejeu"]
    if nonrej:
        print("\n" + "\n".join(f"rejeu non disponible pour {k}" for k in nonrej))
    journaliser(a.jour or "aujourd'hui", time.time() - debut, n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
