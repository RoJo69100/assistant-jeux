"""Que faire aujourd'hui BasketVibe, sans modèle ni agent (refonte v3, lots L2 et L3).

Même plan que le skill basketvibe-aujourdhui : au plus 8 lignes `HH:MM — action — détail (source)` triées par heure
limite, une ligne « Autres points », une ligne « Garder » (décisions « ne rien changer », en demi-ligne) et la ligne
finale « Exports à faire aujourd'hui : … ». Lit en lecture seule les vues gold (executer() de sql.py), la décision
d'achat ouverte (learn.decision) et les fichiers du jour (aujourdhui_sources.py : briefs tactique, registre fait,
dossier, police, learnings). Critères : docs/refonte-v3/journal-aujourdhui.md.

Usage :
  python -I pipelines/aujourdhui.py basketvibe [--jour AAAA-MM-JJ]
Rejeu (--jour) : seules les vues qui savent lire un jour passé sont rejouées ; toutes les autres, qui lisent
current_date ou now(), répondent « rejeu non disponible pour <vue> ». Chaque exécution ajoute une ligne à
docs/refonte-v3/journal-aujourdhui.md. Une donnée absente s'écrit « il me manque X — export Y ».
Règles de décision : docs/attentes/regles-decision-basketvibe.yaml (EFF-1/5, TRF-1/4, FIN-1/5) ; une règle que
le YAML ne porte pas est marquée « (à valider) ».
"""
import argparse
import datetime as dt
import importlib.util
import re
import sys
import textwrap
import time
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python -I n'ajoute pas le dossier du script
import aujourdhui_sources as src  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent
BASE = RACINE / "outputs/basketvibe"
JOURNAL = RACINE / "docs/refonte-v3/journal-aujourdhui.md"
ACTIONS_MAX = 5  # + « Autres points » + « Garder » + « Exports » = 8 lignes au plus
CAT_ALERTE = {"blessure": "Composition", "fatigue": "Composition", "forme": "Composition",
              "finances": "Finances", "transferts": "Transferts", "export": "Exports"}
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
    "gold.bv_position_summary": "select * from gold.bv_position_summary limit 10",
    "gold.bv_market_bargains": "select name, position, ps, ref_n, ref_reliable, bid_ceiling_resale, resale_margin_p25, "
                               "ends_paris from gold.bv_market_bargains order by resale_margin_p25 desc nulls last limit 5",
    "gold.bv_market_candidates": "select name, position, ps, would_rank_in_slot, enters_top8, current_price, ends_paris "
                                 "from gold.bv_market_candidates where enters_top8 order by gain_vs_my_second desc nulls last limit 5",
    "gold.bv_personnel_status": "select * from gold.bv_personnel_status limit 10",
    "capacite": "select capacite_invest from gold.finance_health where game = 'basketvibe'",
    "joueurs_declin": "select name, age from gold.bv_roster_now where age >= 31 order by age desc",
    "decisions_achat": "select id, label, hypothesis from learn.decision where game = 'basketvibe' and domain = 'achat' "
                       "and status in ('proposed', 'accepted') and eval_after >= now() and decided_at >= now() - interval '3 days' order by id",
    # enchères décidées : fin à venir (ouvertes) ou finie depuis moins de 4 jours (résultat à lire, PB7)
    "encheres_ouvertes": "select name, ends_at at time zone 'Europe/Paris' as fin_paris from core.market_listing "
                         "where game = 'basketvibe' and not is_mine and ends_at > now() - interval '4 days' and ends_at < now() + interval '4 days'",
    "transferts_recents": "select t.name, t.settled_at, t.to_team, (t.to_team_id = m.team_id) as achete from silver.bv_transfers t "
                          "cross join silver.bv_my_team m where t.entry_type = 'transfer' and t.settled_at >= now() - interval '6 days' "
                          "order by t.settled_at desc limit 300",
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


def heure(v):
    return None if v is None else str(v)[:5]


def lire_fait(jour):
    """Texte du registre du jour en minuscules (apostrophes droites), vide s'il n'existe pas."""
    f = BASE / f"fait-{jour.isoformat()}.md"
    return f.read_text(encoding="utf-8").lower().replace("’", "'") if f.exists() else ""


def lire_sources(donnees, jour, base=BASE):
    """Fichiers du jour (aujourdhui_sources.py) et décisions d'achat ouvertes de la base."""
    return {"tactique": src.lire_tactique(base, jour), "restes": src.lire_restes(base, jour),
            "cibles": src.lire_cibles(lignes_de(donnees, "decisions_achat"), lignes_de(donnees, "encheres_ouvertes"), base, jour),
            "conseils": src.lire_conseils(base, jour), "saisies": src.lire_saisies(base, jour)}


def deja(fait, cle):
    return any(m in fait for m in MOTS_FAIT.get(cle, ()))


def norm(s):
    return "".join(c for c in unicodedata.normalize("NFKD", str(s).lower()) if not unicodedata.combining(c))


def meme_match(a, b):
    """Deux noms d'adversaire désignent le même club : même premier mot, sans accent."""
    return bool(a) and bool(b) and norm(a).split()[0] == norm(b).split()[0]


def montant(n):
    return f"{int(n):,}".replace(",", " ")


def propre(s):
    """Texte sur une ligne, sans coupure : une ligne longue est repliée à l'affichage par plier()."""
    return str(s).replace("|", "/").replace("\n", " ")


def plier(texte, largeur=100):
    """Replie chaque ligne sur plusieurs lignes d'affichage (suite en retrait) ; un montant « 150 000 » ne se coupe pas."""
    sortie = []
    for l in texte.splitlines():
        l = re.sub(r"(?<=\d) (?=\d{3}\b)", " ", l)
        morceaux = textwrap.wrap(l, largeur, subsequent_indent="    ", break_long_words=False, break_on_hyphens=False)
        sortie += [m.replace(" ", " ") for m in morceaux] or [""]
    return "\n".join(sortie)


def jour_fr(d):
    return f"{src.JOURS[d.weekday()]} {d:%d/%m}"


def vrai(v):
    return str(v).lower() in ("t", "true", "1", "vrai", "oui")


def regrouper(reglages):
    """[('Agress. 1','Dang'), ('Agress. 1','Albano'), ('Tir 1','Albano')] -> « Agress. 1 : Dang, Albano ; Tir 1 : Albano »."""
    par = {}
    for r, nom in reglages:
        par.setdefault(r, []).append(nom)
    return " ; ".join(f"{r} : {', '.join(n)}" for r, n in par.items())


def enchere_terminee(c, fin, donnees, erreurs):
    """Ligne d'une décision d'achat dont l'enchère est finie : résultat lu dans silver.bv_transfers (PB7), jamais écrit."""
    titre = f"Enchère sur {c['nom']} ({c['poste']}) terminée le {fin:%d/%m}"
    m = manque(donnees, erreurs, "transferts_recents", "Historique global des transferts")
    if m:
        return f"{titre} : {m}"
    trouves = []
    for r in lignes_de(donnees, "transferts_recents"):
        if norm(c["nom"]) in norm(r["name"]):
            quand = dt.datetime.fromisoformat(str(r["settled_at"])[:19])
            if quand >= fin - dt.timedelta(days=1):
                trouves.append((abs((quand - fin).total_seconds()), r))
    if not trouves:
        return f"{titre} : résultat lu dans silver.bv_transfers : aucune ligne (export Historique global des transferts)"
    r = min(trouves, key=lambda x: x[0])[1]
    verdict = "acheté" if vrai(r["achete"]) else f"non acheté, parti à {r['to_team']}"
    return f"{titre} : {verdict} (résultat lu dans silver.bv_transfers)"


def plan(donnees, erreurs, jour, maintenant, fait="", sources=None):
    """{'actions': [(limite|None, priorité 1-3, action, détail, source)], 'exports': [texte], 'garder': [texte],
    'infos': [texte]} ; infos = enchères terminées, une ligne chacune, rangées dans « Autres points »."""
    A, exports, garder, infos = [], [], [], []
    S = sources or {}
    restes = list(S.get("restes", []))

    def ajoute(limite, prio, action, detail="", source=""):
        A.append((limite, prio, action, detail, source))

    # 1. Matchs à venir : brief tactique du jour (verrou, tests), registre « reste à corriger »
    couverts = []
    for t in S.get("tactique", []):
        limite = dt.datetime.combine(t["date"], dt.time.fromisoformat(t["verrou"])) if t["date"] and t["verrou"] else None
        reste = next((r for r in restes if meme_match(r["match"], t["match"])), None)
        saisie = next((s for s in S.get("saisies", []) if s["date"] == t["date"] and meme_match(s["match"], t["match"])), None)
        quand = jour_fr(t["date"]) if t["date"] else "date inconnue"
        if t["type"] == "ligue":
            titre = f"Ligue {t['manche'] or ''} {'à' if t['lieu'] == 'extérieur' else 'contre'} {t['match']}".replace("  ", " ")
        else:
            titre = f"Amical contre {t['match']}"
        if reste and reste["reglages"]:
            etat, prio = f"corrige à l'écran {len(reste['reglages'])} réglages ({regrouper(reste['reglages'])})", 1
        elif deja(fait, t["type"]) or saisie:
            etat, prio = "", 1  # saisie déclarée faite (registre du jour ou d'un jour antérieur) : la ligne reste, pour l'heure limite et les conditions du test
        else:
            etat, prio = "saisis la tactique maintenant", 1
        detail = f"heure limite du verrou {t['verrou'] or 'inconnue'}"
        if t["preuves"]:
            detail += " ; le test est perdu si : " + " ; ".join(propre(p.rstrip(".")) for p in t["preuves"])
        if t["vieux"]:
            detail += f" ; brief vieux de {t['age']} jours : relance l'agent tactique"
        ajoute(limite, prio, f"{titre} ({quand})" + (f" : {etat}" if etat else ""), detail,
               t["fichier"] + (", " + reste["fichier"] if reste else ""))
        couverts.append(t["match"])
        if reste:
            restes.remove(reste)
    for r in restes:  # reste à faire sans brief du jour
        limite = dt.datetime.combine(r["date"], dt.time.fromisoformat(r["heure"])) if r["date"] and r["heure"] else None
        ajoute(limite, 1, f"{r['match'] or 'Match'} : corrige à l'écran {len(r['reglages'])} réglages ({regrouper(r['reglages'])})",
               "", r["fichier"])
        couverts.append(r["match"])

    # 2. Enchères décidées : montant maximum, fin d'enchère, police avant l'enchère
    for c in S.get("cibles", []):
        pol = "police faite" if c["police"] else "police d'abord (aucune trace de police du jour)"
        fin = c["fin"]
        if fin is not None and fin <= maintenant:  # enchère finie : plus une action, le résultat se lit en base (PB7)
            infos.append(enchere_terminee(c, fin, donnees, erreurs))
            continue
        detail = (f"fin {jour_fr(fin.date())} {fin:%H:%M}" if fin
                  else "fin d'enchère absente de la base : export Marché (enchères)")
        ajoute(fin, 1, f"Enchère sur {c['nom']} ({c['poste']}) : maximum {montant(c['max'])}, {pol}", detail,
               "décision d'achat ouverte, " + ("dossier du jour" if c["dossier"] else "dossier absent : python pipelines/dossier.py basketvibe achat"))

    # 3. Conseils arrivant à échéance
    for c in S.get("conseils", []):
        ajoute(None, 3, f"Conseil {c['id']} à juger au plus tard le {c['echeance']:%d/%m}", propre(c["conseil"]), "learnings.md")

    # 4. Agenda (aujourd'hui, et demain avant 10:00 après 18:00) : ce que les briefs ne couvrent pas déjà
    m = manque(donnees, erreurs, "gold.bv_agenda", "Équipe (aperçu, joueurs)")
    if m:
        ajoute(None, 2, m)
    for r in lignes_de(donnees, "gold.bv_agenda"):
        d = r["day"] if isinstance(r["day"], dt.date) else dt.date.fromisoformat(str(r["day"])[:10])
        h = heure(r["at_time"])
        if not (d == jour or (d == jour + dt.timedelta(days=1) and maintenant.hour >= 18 and h and h < "10:00")):
            continue
        if r["category"] in ("ligue", "amical") and any(norm(c).split()[0] in norm(r["action"]) for c in couverts if c):
            continue  # la ligne du brief est plus complète
        if r["category"] == "export" and d != jour:
            continue  # export d'après-match de demain : pas une action d'aujourd'hui
        if deja(fait, r["category"]):
            continue
        ajoute(dt.datetime.combine(d, dt.time.fromisoformat(h)) if h else None, int(r["priority"]), r["action"], "", "gold.bv_agenda")

    # 5. Exports en retard + aperçu + historique des transferts (ligne finale)
    m = manque(donnees, erreurs, "gold.bv_exports_state", "tous les écrans")
    if m:
        exports.append(m)
    etat = {r["ecran"]: r for r in lignes_de(donnees, "gold.bv_exports_state")}
    # Mes enchères : la page est vide (et jamais envoyée) sans enchère d'achat en cours ; fin inconnue = peut-être en cours (PB6)
    encheres_en_cours = any(c["fin"] is None or c["fin"] > maintenant for c in S.get("cibles", []))
    for r in etat.values():
        if r["ecran"] == "Mes enchères" and not encheres_en_cours:
            continue
        if not str(r["statut"]).endswith("à jour") and not deja(fait, r["ecran"]):
            exports.append(f"{r['ecran']} ({'jamais exporté' if r['age_h'] is None else str(int(r['age_h'])) + ' h'})")
    ligues = [r for r in lignes_de(donnees, "gold.bv_agenda") if r["category"] == "ligue"]
    apercus = {str(r["match_day"])[:10] for r in lignes_de(donnees, "apercus")}
    if donnees.get("apercus") is None:
        exports.append(manque(donnees, erreurs, "apercus", "Match de ligue : aperçu"))
    for r in ligues:
        d = str(r["day"])[:10]
        if jour <= dt.date.fromisoformat(d) <= jour + dt.timedelta(days=2) and d not in apercus and not deja(fait, "Match de ligue : aperçu"):
            exports.append(f"aperçu du match de ligue du {d[8:]}/{d[5:7]} (aucune ligne adverse en base)")
    vente = lignes_de(donnees, "derniere_vente")
    derniere = vente[0]["derniere"] if vente else None
    if donnees.get("derniere_vente") is None:
        exports.append(manque(donnees, erreurs, "derniere_vente", "Historique global des transferts"))
    elif derniere is None or dt.date.fromisoformat(str(derniere)[:10]) < jour - dt.timedelta(days=1):
        exports.append("historique global des transferts depuis " + ("le début" if derniere is None else str(derniere)[:10]))

    # 6. Alertes (les exports en retard viennent déjà de bv_exports_state)
    m = manque(donnees, erreurs, "gold.bv_daily_alerts", "Équipe (aperçu, joueurs)")
    if m:
        ajoute(None, 2, m)
    for r in lignes_de(donnees, "gold.bv_daily_alerts"):
        cat = CAT_ALERTE.get(r["category"])
        if cat and cat != "Exports":
            ajoute(None, int(r["priority"]), r["alert"], "", "gold.bv_daily_alerts")

    # 7. Décisions par secteur (étape 6 du skill) : une ligne si la règle du YAML se déclenche, sinon « Garder »
    m = manque(donnees, erreurs, "gold.bv_position_summary", "Équipe (aperçu, joueurs)")
    pos = lignes_de(donnees, "gold.bv_position_summary")
    marche_frais = etat.get("Marché (enchères)") is not None and str(etat["Marché (enchères)"]["statut"]).endswith("à jour")
    decides = [norm(c["nom"]) for c in S.get("cibles", [])]  # déjà décidés (plafond de la décision) : pas de 2e ligne

    cap = lignes_de(donnees, "capacite")  # règle E8 : capacité d'investissement moins les dépenses déjà décidées
    reste_cap = float(cap[0]["capacite_invest"]) - sum(c["max"] for c in S.get("cibles", [])) if cap else None

    def libre(r):
        return not any(n in norm(r["name"]) for n in decides)

    def finance(prix):  # prix inconnu ou capacité illisible : on ne tranche pas, la cible reste proposée
        return reste_cap is None or prix is None or float(prix) <= reste_cap

    if m:
        ajoute(None, 3, m)
    elif pos:
        faible = min(pos, key=lambda r: float(r["ps_avg"]))
        minces = [r for r in pos if int(r["depth"]) <= 2]
        cands = [r for r in lignes_de(donnees, "gold.bv_market_candidates")
                 if vrai(r["enters_top8"]) and str(r["would_rank_in_slot"]) == "1" and r["position"] == faible["position"]
                 and libre(r) and finance(r["current_price"])] if marche_frais else []
        cible = minces[0] if minces else faible if cands else None
        if cible:
            x = round(float(cible["ps_max"]) + 1, 1)
            nom = f" : {cands[0]['name']} (PS {cands[0]['ps']})" if cands else ""
            ajoute(None, 2, f"Acheter un {cible['position']} de note ≥ {str(x).replace('.', ',')}{nom}",
                   f"poste {cible['position']} : profondeur {cible['depth']}, PS moyen {cible['ps_avg']}", "gold.bv_position_summary")
        else:
            garder.append(f"effectif, acheter : seuil non atteint (le poste le plus faible, {faible['position']} PS {faible['ps_avg']}, "
                          f"a assez de joueurs : {faible['depth']} contre 2 au plus pour un poste mince)")
        declin = lignes_de(donnees, "joueurs_declin")
        if donnees.get("joueurs_declin") is None:
            ajoute(None, 3, manque(donnees, erreurs, "joueurs_declin", "Équipe (aperçu, joueurs)"))
        elif declin:
            ajoute(None, 2, f"Mets {declin[0]['name']} en vente ({declin[0]['age']} ans, déclin chaque semaine)",
                   "31 ans ou plus", "gold.bv_roster_now")
        else:
            garder.append("effectif, vendre : rien de vendable (aucun joueur de 31 ans ou plus, âge du déclin)")
        garder.append("effectif, vendre pour profit : règle non écrite — à valider (seuil de déclenchement non validé)")
        garder.append("effectif, jeunes : règle non écrite — à valider (le script ne sait pas dire si un match de ligue est gagné d'avance)")
    m = manque(donnees, erreurs, "gold.bv_finance_health", "Finances")
    fh = lignes_de(donnees, "gold.bv_finance_health")
    if m:
        ajoute(None, 3, m)
    elif fh:
        res = float(fh[0]["weekly_result_est"])
        if res < 0:
            charge = max(("personnel", float(fh[0]["weekly_personnel"])), ("académie", float(fh[0]["weekly_academy"])), key=lambda x: x[1])
            ajoute(None, 1, f"Réduis le poste {charge[0]} ({montant(charge[1])} par semaine)",
                   f"résultat hebdomadaire estimé {montant(res)}", "gold.bv_finance_health")
        else:
            garder.append(f"finances : seuil non atteint (résultat hebdo estimé +{montant(res)}, la réduction de charges commence sous 0)")
    m = manque(donnees, erreurs, "gold.bv_market_bargains", "Marché (enchères)")
    if m:
        ajoute(None, 2, m)
    elif not marche_frais:
        garder.append("transferts : pas d'enchère nouvelle, l'export du Marché a plus de 24 h")
    else:
        bonnes = [r for r in lignes_de(donnees, "gold.bv_market_bargains")
                  if vrai(r["ref_reliable"]) and float(r["resale_margin_p25"] or 0) > 0 and int(r["ref_n"] or 0) >= 5 and libre(r)
                  and finance(r["bid_ceiling_resale"])][:2]
        for r in bonnes:
            fin = dt.datetime.fromisoformat(str(r["ends_paris"])[:19]) if r.get("ends_paris") else None
            ajoute(fin, 2, f"Enchère maximale {montant(r['bid_ceiling_resale'])} sur {r['name']} ({r['position']}, PS {r['ps']})",
                   f"marge de revente p25 {montant(r['resale_margin_p25'])}", "gold.bv_market_bargains")
        if not bonnes:
            garder.append("transferts : aucune affaire fiable qui tienne dans ce que le club peut investir après les enchères déjà décidées "
                          "(capacité restante (réserve de sécurité à valider)"
                          + (f" : {montant(reste_cap)}" if reste_cap is not None else " illisible") + ")")
    m = manque(donnees, erreurs, "gold.bv_personnel_status", "Personnel")
    pers = lignes_de(donnees, "gold.bv_personnel_status")
    if m:
        ajoute(None, 3, m)
    elif pers:
        garder.append("Personnel (" + ", ".join(f"{r['role']} {r['hired']}/{r['slots']}" for r in pers)
                      + ", semaine du " + str(pers[0].get("week", "?"))[:10] + ") : règle de personnel non tranchée, à valider")
    return {"actions": A, "exports": exports, "garder": garder, "infos": infos}


def rendre(res, jour, erreurs=None):
    """Au plus 8 lignes : 5 actions triées par heure limite, Autres points, Garder, Exports à faire aujourd'hui."""
    maxi = dt.datetime.max
    rang = sorted(res["actions"], key=lambda a: (a[0] is None, a[1], a[0] or maxi))
    vues, reste = rang[:ACTIONS_MAX], rang[ACTIONS_MAX:]
    lignes = []
    for limite, _, action, detail, source in sorted(vues, key=lambda a: (a[0] is None, a[0] or maxi, a[1])):
        t = f"{limite:%H:%M}" if limite else "--:--"
        lignes.append(f"{t} — {action}" + (f" — {detail}" if detail else "") + (f" ({source})" if source else ""))
    autres = [propre(a[2]) for a in reste] + list(res.get("infos", [])) + [f"vue illisible {k}" for k in (erreurs or {})]
    if autres:
        lignes.append(f"Autres points ({len(autres)}) : " + " ; ".join(autres))
    if res["garder"]:
        lignes.append("Garder : " + " ; ".join(res["garder"]))
    lignes.append("Exports à faire aujourd'hui : " + (" ; ".join(res["exports"]) if res["exports"] else "aucun"))
    return "\n".join(lignes)


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
    rendu = plier(rendre(plan(donnees, erreurs, jour, maintenant, lire_fait(jour), lire_sources(donnees, jour)), jour, erreurs))
    print(rendu)
    if not a.jour:  # instantané quotidien (écrasé si relancé le même jour) : remplace le rejeu
        fichier = BASE / f"aujourdhui-{jour.isoformat()}.md"
        fichier.parent.mkdir(parents=True, exist_ok=True)
        fichier.write_text(f"<!-- généré le {maintenant.strftime('%Y-%m-%d %H:%M')} -->\n{rendu}\n", encoding="utf-8")
    nonrej = [k for k, v in donnees.items() if v == "rejeu"]
    if nonrej:
        print("\n" + "\n".join(f"rejeu non disponible pour {k}" for k in nonrej))
    journaliser(a.jour or "aujourd'hui", time.time() - debut, n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
