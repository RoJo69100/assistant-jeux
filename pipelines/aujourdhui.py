"""Que faire aujourd'hui BasketVibe, sans modèle ni agent (refonte v3, lots L2 et L3).

Même plan que le skill basketvibe-aujourdhui : au plus 8 lignes `HH:MM — action — détail (source)` triées par heure
limite, une ligne « Autres points », une ligne « Garder » (décisions « ne rien changer », en demi-ligne) et la ligne
finale « Exports à faire aujourd'hui : … ». Lit en lecture seule les vues gold (executer() de sql.py), la décision
d'achat ouverte (learn.decision) et les fichiers du jour (aujourdhui_sources.py : briefs tactique, registre fait,
dossier, police, learnings). Critères : docs/refonte-v3/journal-aujourdhui.md.

Usage :
  python -I pipelines/aujourdhui.py basketvibe [--jour AAAA-MM-JJ] [--maintenant HH:MM]
L'heure et le jour viennent de pipelines/heure_paris.py (jamais de l'horloge du shell) ; une action dont le verrou est passé n'est
plus proposée. --maintenant HH:MM impose l'heure pour les tests : ni instantané, ni ligne de durée.
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
FENETRE = 7  # jours : durée de validité d'une clé de match sans date (R5)
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
    "gold.bv_finance_health": "select * from gold.bv_finance_health limit 3",  # balance = solde ; capacité = solde − enchères ouvertes
    "gold.bv_position_summary": "select * from gold.bv_position_summary limit 10",
    "gold.bv_market_bargains": "select name, position, ps, ref_n, ref_reliable, bid_ceiling_resale, resale_margin_p25, "
                               "ends_paris from gold.bv_market_bargains order by resale_margin_p25 desc nulls last limit 5",
    "gold.bv_market_candidates": "select name, position, ps, would_rank_in_slot, enters_top8, current_price, ends_paris "
                                 "from gold.bv_market_candidates where enters_top8 order by gain_vs_my_second desc nulls last limit 5",
    "gold.bv_personnel_status": "select * from gold.bv_personnel_status limit 10",
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
    # A1 : alertes de domaine « match » (dernier match, ligue ou coupe jouée non exportée) ; coupe_sans_resultat
    # n'existe que dans gold.daily_alerts (core.alert_rule), pas dans gold.bv_daily_alerts
    "alertes_match": "select rule_id, prio, alerte from gold.daily_alerts where game = 'basketvibe' and domaine = 'match' order by prio",
    # A2 et A3 : objectif des matchs des 7 prochains jours (règle serie, titre, rien) et dernier match officiel joué
    "objectifs": "select day, competition_kind, opponent, objectif, raison, rule_id, defaites_d_affilee "
                 "from gold.match_objective where game = 'basketvibe' order by day",
    "dernier_officiel": "select day, competition_kind, opponent, my_result from core.fixture where game = 'basketvibe' "
                        "and played and my_result is not null and competition_kind <> 'amical' "
                        "order by day desc, scheduled_at desc nulls last limit 1",
    # J5 (étape 5c) : verrou des matchs à venir depuis scheduled_at (fuseau lu dans la page), heure de Paris
    "calendrier": "select day, competition_kind, opponent, scheduled_at at time zone 'Europe/Paris' as coup_envoi_paris, "
                  "(extras ->> 'verrou_at')::timestamptz at time zone 'Europe/Paris' as verrou_paris from core.fixture "
                  "where game = 'basketvibe' and not played and scheduled_at is not null "
                  "and day between current_date - 1 and current_date + 7 order by scheduled_at",
    # H6 (étape 5d) : règles d'agenda de ligue à heure écrite, avec leur décalage relatif au coup d'envoi
    "regles_agenda": "select rule_id, category, to_char(heure, 'HH24:MI') as heure, decalage_min from core.agenda_rule "
                     "where game = 'basketvibe' and competition_kind = 'ligue' and actif and heure is not null "
                     "and decalage_min is not null",
    # K3 (étape 5e) : dernier rapport du scout, cote du potentiel à la jauge actuelle, valeur d'un High et coût du test
    "prospects": "select scout_report_at at time zone 'Europe/Paris' as rapport_paris, slot, name, position, age, tsp_min, tsp_max "
                 "from gold.bv_academy_prospects order by slot",
    "cote_potentiel": "select academy_score, p_high_8_10 from gold.bv_academy_potential_odds where label = 'jauge actuelle'",
    "valeurs_academie": "select key, value from core.game_params where game = 'basketvibe' "
                        "and key in ('academie_valeur_high', 'academie_cout_test')",
    # L3 (étape 5f) : remplaçant au même poste (force fit), écart et salaire ; tolérance de force lue dans core.game_params
    "gold.bv_sell_replacement": "select name, best_slot, fit_best, replacement_name, replacement_fit, gap, weekly_salary, "
                                "on_transfer_list, available, available_players from gold.bv_sell_replacement",
    "tolerance_vente": "select value from core.game_params where game = 'basketvibe' and key = 'vente_tolerance_force'",
    # M3 (étape 5g) : réglage réellement joué par amical (page « réglages utilisés »), pour vérifier les expériences
    "amical_reglage": "select fixture_id, match_day, opponent, agress_cran, primary_quarts, tir_cran4_joueurs "
                      "from gold.bv_amical_reglage where match_day >= current_date - 120",
    # K4 (étape 5e) : décisions échues à mesurer, et décisions encore « proposed » (faits du registre à relier)
    "a_evaluer": "select count(*) as n from gold.decisions_a_evaluer where game = 'basketvibe'",
    "decisions_proposees": "select id, status, game from learn.decision where game = 'basketvibe' and status = 'proposed'",
    # A4 : solde projeté en fin de saison
    "gold.bv_finance_projection": "select season_end, balance_end_projected, tickets_left, sponsor_left, costs_left "
                                  "from gold.bv_finance_projection limit 1",
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


PARALLELE = 8  # requêtes simultanées (K1, étape 5e) : elles sont indépendantes ; l'ordre du résultat reste celui de REQUETES


def lire_tout(executer, jour=None):
    """{nom: (colonnes, lignes) | None | 'rejeu'} ; None = lecture impossible, message dans erreurs.
    Les requêtes partent en parallèle (K1) ; donnees et erreurs sont remplis dans l'ordre de REQUETES."""
    from concurrent.futures import ThreadPoolExecutor

    def une(sql):
        try:
            return executer(sql), None
        except SystemExit as e:  # sql.py termine par sys.exit(message)
            return None, str(e)
        except Exception as e:  # noqa: BLE001 - une vue en échec ne doit pas arrêter le plan
            return None, f"{type(e).__name__}: {e}"

    a_lire = {}
    for nom, sql in REQUETES.items():
        if jour:
            if nom not in REJEU:
                continue
            sql = REJEU[nom].format(jour=jour)
        a_lire[nom] = sql
    with ThreadPoolExecutor(max_workers=PARALLELE) as pool:
        futurs = {nom: pool.submit(une, sql) for nom, sql in a_lire.items()}
    donnees, erreurs = {}, {}
    for nom in REQUETES:
        if nom not in futurs:
            donnees[nom] = "rejeu"
            continue
        donnees[nom], err = futurs[nom].result()
        if err is not None:
            erreurs[nom] = err
    return donnees, erreurs, len(futurs)


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
            "conseils": src.lire_conseils(base, jour), "saisies": src.lire_saisies(base, jour),
            "cles": src.lire_cles(base, jour), "analyste": src.lire_analyste(base, jour),
            "experiences": src.lire_experiences(base, jour), "refs_decisions": lire_refs_decisions(base, jour)}


def lire_refs_decisions(base, jour):
    """K4 : `[décision=<id>]` des registres des 7 derniers jours (lecteur de relier_faits.py, sans écriture)."""
    import relier_faits
    return relier_faits.lire_references(Path(base), jour)


def deja(fait, cle):
    return any(m in fait for m in MOTS_FAIT.get(cle, ()))


def declare(fait, cles, jour, nom):
    """Écran ou catégorie déclaré fait aujourd'hui : clé du registre du jour (R5), sinon l'ancienne correspondance par mots."""
    return any(c["jour"] == jour and c["date"] is None and norm(c["nom"]) == norm(nom) for c in cles) or deja(fait, nom)


def cle_match(cles, match, date):
    """Déclaration par clé d'un match à venir (R5) : même adversaire ; la date de la clé est celle du match, sans date
    la déclaration vaut pour un match des 7 jours suivant le registre."""
    for c in cles:
        if not meme_match(c["nom"], match):
            continue
        if c["date"] is not None:
            if c["date"] == date:
                return c
        elif date is None or c["jour"] <= date <= c["jour"] + dt.timedelta(days=FENETRE):
            return c
    return None


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


def en_date(v):
    return v if isinstance(v, dt.date) and not isinstance(v, dt.datetime) else dt.date.fromisoformat(str(v)[:10])


def verrou_calendrier(donnees, date, match):
    """Verrou (heure de Paris) du match `match` le `date` d'après core.fixture.scheduled_at (étape 5c, J5) ;
    None si le calendrier n'a pas d'heure pour ce match : l'appelant garde alors l'heure du brief."""
    if not date:
        return None
    for r in lignes_de(donnees, "calendrier"):
        if en_date(r["day"]) == date and meme_match(r["opponent"], match):
            v = r.get("verrou_paris") or r.get("coup_envoi_paris")
            if v:
                return v if isinstance(v, dt.datetime) else dt.datetime.fromisoformat(str(v)[:19])
    return None


def en_heure(v):
    return v if isinstance(v, dt.datetime) else dt.datetime.fromisoformat(str(v)[:19])


def recaler(donnees, d, h, category, action):
    """H6 : ligne d'agenda de ligue à heure écrite -> (limite, action) recalées sur le coup d'envoi du match de ligue
    du jour `d` (core.fixture) + decalage_min de core.agenda_rule ; coup d'envoi inconnu ou règle sans décalage :
    (None, action), l'appelant garde l'heure écrite."""
    regles = lignes_de(donnees, "regles_agenda")
    ce = next((r["coup_envoi_paris"] for r in lignes_de(donnees, "calendrier")
               if r["competition_kind"] == "ligue" and en_date(r["day"]) == d and r.get("coup_envoi_paris")), None)
    if not regles or ce is None or not any(r["heure"] == h and r["category"] == category for r in regles):
        return None, action
    nouvelles = {r["heure"]: en_heure(ce) + dt.timedelta(minutes=int(r["decalage_min"])) for r in regles}
    texte = re.sub(r"\b\d{2}:\d{2}\b", lambda m: f"{nouvelles[m.group(0)]:%H:%M}" if m.group(0) in nouvelles else m.group(0), action)
    return nouvelles[h], texte


def prochain_amical(donnees, jour, maintenant):
    """H3 : premier amical d'aujourd'hui ou de demain dans core.fixture dont le verrou n'est pas passé :
    {'match', 'date', 'limite'} ; None sinon."""
    for r in lignes_de(donnees, "calendrier"):
        d = en_date(r["day"])
        v = r.get("verrou_paris") or r.get("coup_envoi_paris")
        if r["competition_kind"] == "amical" and d in (jour, jour + dt.timedelta(days=1)) and v and en_heure(v) >= maintenant:
            return {"match": r["opponent"], "date": d, "limite": en_heure(v)}
    return None


def _jour(v):
    return v if isinstance(v, dt.date) else dt.date.fromisoformat(str(v)[:10])


def conforme(regle, r):
    """M3 : le réglage joué `r` (ligne de gold.bv_amical_reglage) respecte la règle `joue` du niveau ; règle vide : oui."""
    for k, v in (regle or {}).items():
        if k == "agress_cran" and r.get("agress_cran") != v:
            return False
        if k == "tir_cran4_min" and (r.get("tir_cran4_joueurs") or 0) < v:
            return False
        if k == "primary_quarts_min" and (r.get("primary_quarts") or 0) < v:
            return False
    return True


def verifier(experiences, joues, exclus=()):
    """M3-M4 : {id: {'verifies', 'attente', 'ecarts'}} pour les faits déclarés (hors `exclus`).
    Match d'un fait : celui de sa clé, sinon le premier amical joué le jour du registre ou le lendemain.
    Vérifié = match exporté dont le réglage joué respecte `joue` ; écart = réglage différent ; attente = match non
    exporté ou pas encore joué. Un amical joué avant `debut` ne compte pas (M4) ; un match compte une fois."""
    res = {e["id"]: {"verifies": 0, "attente": 0, "ecarts": []} for e in (experiences or {}).get("file", [])}
    if not experiences:
        return res
    debut = experiences.get("debut")
    regles = {e["id"]: e.get("joue") or {} for e in experiences["file"]}
    lignes = sorted(({**r, "jour": _jour(r["match_day"])} for r in joues or []), key=lambda r: r["jour"])
    vus = set()
    for f in experiences["faits"]:
        if f in exclus or f["id"] not in res:
            continue
        c = f["cle"]
        if c:
            r = next((r for r in lignes if cle_match([c], r["opponent"], r["jour"])), None)
            quand = c["date"] or f["jour"]
        else:
            r = next((r for r in lignes if f["jour"] <= r["jour"] <= f["jour"] + dt.timedelta(days=1)), None)
            quand = f["jour"]
        if debut and ((r and r["jour"] < debut) or (not r and quand < debut)):
            continue  # M4 : amical d'avant le test, ne compte pour aucune expérience
        if r is None:
            res[f["id"]]["attente"] += 1
            continue
        if (f["id"], r["fixture_id"]) in vus:
            continue
        vus.add((f["id"], r["fixture_id"]))
        if conforme(regles[f["id"]].get(f["niveau"]), r):
            res[f["id"]]["verifies"] += 1
        else:
            res[f["id"]]["ecarts"].append(f"{r['opponent']} {r['jour']:%d/%m}")
    return res


def _pluriel(n, mot):
    return f"{n} {mot}" + ("s" if n > 1 else "")


def texte_avancement(e, v):
    """M3 : « E1 : 1 vérifié sur 4, 1 déclaré non vérifié (match à exporter) », écarts signalés."""
    t = f"{e['id']} : {_pluriel(v['verifies'], 'vérifié')} sur {e['amicaux_vises']}"
    if v["attente"]:
        t += f", {v['attente']} déclaré{'s' if v['attente'] > 1 else ''} non vérifié{'s' if v['attente'] > 1 else ''}" \
             " (match à exporter)"
    if v["ecarts"]:
        t += f", réglage joué ≠ réglage du test ({', '.join(v['ecarts'])})"
    return t


def faits_ici(experiences, amical):
    return [f for f in experiences["faits"] if f["cle"] and cle_match([f["cle"]], amical["match"], amical["date"])]


def test_en_cours(experiences, amical, joues=()):
    """H1-H2 : (expérience, niveau, déjà saisi) du test à jouer sur `amical`, None si aucune expérience en cours (H4).
    Les expériences passent dans l'ordre du fichier ; un fait dont la clé désigne cet amical ne le fait pas avancer :
    il dit l'amical saisi à ce niveau. M3 (5g) : la suivante démarre quand la précédente a `amicaux_vises` amicaux
    vérifiés (réglage joué conforme dans `joues`) ; le niveau suit les vérifiés et les déclarés en attente, pas les écarts."""
    if not experiences or not amical:
        return None
    ici = faits_ici(experiences, amical)
    v = verifier(experiences, joues, exclus=ici)
    for e in experiences["file"]:
        fait = next((f for f in ici if f["id"] == e["id"]), None)
        if fait:
            return e, fait["niveau"], True
        if v[e["id"]]["verifies"] < int(e["amicaux_vises"]):
            ordre = e["ordre"]
            return e, ordre[(v[e["id"]]["verifies"] + v[e["id"]]["attente"]) % len(ordre)], False
    return None


def texte_test(e, niveau):
    nom = f"test {e['id']}" + (f" niveau {niveau}" if len(e["niveaux"]) > 1 else "")
    return f"{nom} : {e['niveaux'].get(niveau, niveau)}"


def alertes_match(donnees, erreurs, fait, cles, jour, A, exports, ajoute):
    """A1 : dernier match -> ligne « Analyse : … » ; ligue ou coupe jouée non exportée -> ligne Exports, sans doublon.
    Source absente du jeu de données (anciens tests) : rien ; illisible : « il me manque »."""
    if "alertes_match" not in donnees:
        return
    m = manque(donnees, erreurs, "alertes_match", "page du dernier match")
    if m:
        ajoute(None, 3, m)
        return
    for r in lignes_de(donnees, "alertes_match"):
        texte = propre(r["alerte"])
        if r["rule_id"] == "dernier_match":
            jm = re.search(r"\d{2}/\d{2}", texte)
            if jm and any(a[2].startswith("Analyse : lance l'agent analyste") and jm.group(0) in a[3] for a in A):
                continue  # la ligne analyste porte déjà ce match (A2)
            # priorité 3 : un constat, pas une action ; il ne doit pas chasser une action du plan (A6)
            ajoute(None, 3, f"Analyse : {texte}", "", "gold.daily_alerts")
        elif r["rule_id"] in ("ligue_sans_resultat", "coupe_sans_resultat"):
            if r["rule_id"] == "ligue_sans_resultat" and (any(e.startswith("Match de ligue : box") for e in exports)
                                                         or declare(fait, cles, jour, "Match de ligue : box")):
                continue  # l'écran box du match de ligue est déjà demandé ou déclaré fait
            if texte not in exports:
                exports.append(texte)


def defaite_officielle(donnees, erreurs, brief_analyste, ajoute):
    """A2 (arbitrage 15) : dernier match de ligue ou de coupe joué perdu, plus récent que le dernier brief analyste
    -> une ligne « Analyse : lance l'agent analyste ce soir » ; série de `gold.match_objective` (règle serie) dite en clair.
    Amicaux exclus par la requête. Source absente du jeu de données : rien."""
    if "dernier_officiel" not in donnees:
        return
    m = manque(donnees, erreurs, "dernier_officiel", "page du dernier match")
    if m:
        ajoute(None, 2, m)
        return
    o = lignes_de(donnees, "dernier_officiel")
    if not o or str(o[0]["my_result"]) != "L":
        return
    d = en_date(o[0]["day"])
    if brief_analyste is not None and brief_analyste >= d:
        return  # défaite déjà analysée
    serie = [r for r in lignes_de(donnees, "objectifs") if r["rule_id"] == "serie"]
    quoi = (f"{serie[0]['defaites_d_affilee']} défaites d'affilée en ligue ou coupe" if serie
            else f"défaite de {o[0]['competition_kind']}")
    vu = f"dernier brief analyste du {brief_analyste:%d/%m}" if brief_analyste else "aucun brief analyste"
    ajoute(None, 2, "Analyse : lance l'agent analyste ce soir",
           f"{quoi} (dernière : {o[0]['opponent']}, {d:%d/%m}, {o[0]['competition_kind']}) ; {vu}",
           "core.fixture" + (", gold.match_objective" if serie else ""))


REGLES_JEUNES = ("titre", "titre_former", "rien", "rien_former")  # core.objective_rule : titre acquis, rien à jouer


def minutes_jeunes(donnees, erreurs, ajoute, garder):
    """A3 : titre acquis ou rien à jouer (règle de gold.match_objective, pas l'objectif seul : `tester` sort aussi de la
    règle amical) -> ligne Composition « minutes aux jeunes » ; sinon demi-ligne « Garder ». Source absente : rien."""
    if "objectifs" not in donnees:
        return
    m = manque(donnees, erreurs, "objectifs", "Classement")
    if m:
        ajoute(None, 3, m)
        return
    r = next((r for r in lignes_de(donnees, "objectifs") if r["rule_id"] in REGLES_JEUNES), None)
    if r is None:
        garder.append("effectif, jeunes : ni titre acquis ni rien à jouer sur les 7 prochains jours (gold.match_objective)")
        return
    ajoute(None, 2, f"Composition : minutes aux jeunes, {r['competition_kind']} contre {r['opponent']} ({jour_fr(en_date(r['day']))})",
           propre(r["raison"]), "gold.match_objective")


def solde_projete(donnees, erreurs, fh, ajoute):
    """A4 : ligne Finances si le solde projeté de fin de saison est négatif ou inférieur à une semaine de masse salariale
    (`weekly_salaries` de gold.bv_finance_health, aucun seuil écrit à la main), avec la cause. Source absente : rien."""
    if "gold.bv_finance_projection" not in donnees:
        return
    m = manque(donnees, erreurs, "gold.bv_finance_projection", "Finances")
    if m:
        ajoute(None, 3, m)
        return
    p = next(iter(lignes_de(donnees, "gold.bv_finance_projection")), None)
    if p is None or p.get("balance_end_projected") is None or fh.get("weekly_salaries") is None:
        return
    fin, semaine = float(p["balance_end_projected"]), float(fh["weekly_salaries"])
    if fin >= 0 and fin >= semaine:
        return
    recettes = float(p["tickets_left"] or 0) + float(p["sponsor_left"] or 0)
    charge = max((("salaires", fh.get("weekly_salaries")), ("personnel", fh.get("weekly_personnel")),
                  ("académie", fh.get("weekly_academy"))), key=lambda x: float(x[1] or 0))
    ajoute(None, 1, f"Finances : solde projeté au {str(p['season_end'])[8:10]}/{str(p['season_end'])[5:7]} de {montant(fin)}, "
                    f"sous une semaine de salaires ({montant(semaine)})",
           f"cause : charges restantes {montant(p['costs_left'] or 0)} contre recettes restantes {montant(recettes)} ; "
           f"plus grosse charge : {charge[0]} ({montant(charge[1] or 0)} par semaine)",
           "gold.bv_finance_projection, gold.bv_finance_health")


DISPONIBLES_APRES_VENTE = 9  # L3 (étape 5f, règle de l'utilisateur) : joueurs disponibles qui doivent rester après une vente


def vendre_remplacable(donnees, ajoute):
    """L3 (étape 5f) : « Vendre X » si un joueur a au même poste un remplaçant d'écart de force (fit) au plus égal à la
    tolérance de core.game_params.vente_tolerance_force, n'est pas déjà en vente et laisse au moins 9 joueurs disponibles ;
    plusieurs candidats : le plus gros salaire. Tolérance absente ou aucun candidat : aucune ligne."""
    tol = next((r["value"] for r in lignes_de(donnees, "tolerance_vente")), None)
    if tol in (None, ""):
        return
    tol = float(tol)
    ok = [r for r in lignes_de(donnees, "gold.bv_sell_replacement")
          if r.get("gap") is not None and r.get("weekly_salary") is not None and not vrai(r.get("on_transfer_list"))
          and float(r["gap"]) <= tol
          and int(r["available_players"]) - (1 if vrai(r.get("available")) else 0) >= DISPONIBLES_APRES_VENTE]
    if not ok:
        return
    r = max(ok, key=lambda r: float(r["weekly_salary"]))
    fr = lambda x: str(round(float(x), 1)).replace(".", ",")
    ajoute(None, 2, f"Vendre {r['name']} : économie {montant(r['weekly_salary'])} par semaine, remplaçant {r['replacement_name']} "
                    f"au poste {r['best_slot']}, écart {fr(r['gap'])}",
           f"force au poste {fr(r['fit_best'])} contre {fr(r['replacement_fit'])}, tolérance {fr(tol)} "
           f"(core.game_params.vente_tolerance_force)", "gold.bv_sell_replacement")


VALEURS_ACADEMIE = {"academie_valeur_high": "valeur d'un High", "academie_cout_test": "coût du test"}
INCONNUES_ACADEMIE = {"academie_valeur_high": "valeur d'un High inconnue", "academie_cout_test": "coût du test inconnu"}


def academie(donnees, erreurs, cles, maintenant, ajoute):
    """K3 : à l'arrivée d'un rapport du scout (moins de 7 jours, aucune clé `[clé=Académie]` au registre depuis), une ligne
    par prospect, même sous 100 % de jauge. Verdict « tester » si P(High) × valeur d'un High dépasse le coût du test, sinon
    « ignorer » (espérance, à valider) ; les deux montants viennent de core.game_params. L5 (étape 5f) : une donnée
    manque → UNE ligne pour tout le rapport (« n prospects ; valeur d'un High inconnue »), pas une par prospect.
    « signer » demande le résultat d'un test, absent de la base : jamais rendu. Vue absente ou rapport ancien : rien."""
    pros = lignes_de(donnees, "prospects")
    if not pros:
        return
    rapport = en_heure(pros[0]["rapport_paris"])
    if not (maintenant - dt.timedelta(days=FENETRE) < rapport <= maintenant):
        return
    if any(norm(c["nom"]) == "academie" and c["jour"] >= rapport.date() for c in cles):
        return
    cote = lignes_de(donnees, "cote_potentiel")
    vals = {r["key"]: r["value"] for r in lignes_de(donnees, "valeurs_academie")}
    manquants = ([] if cote else ["gold.bv_academy_potential_odds"]) \
        + [f"core.game_params.{k}" for k in VALEURS_ACADEMIE if vals.get(k) in (None, "")]
    if manquants:
        inconnues = ([] if cote else ["cote du potentiel inconnue"]) \
            + [t for k, t in INCONNUES_ACADEMIE.items() if vals.get(k) in (None, "")]
        n = len(pros)
        ajoute(None, 3, f"Académie, rapport du {rapport:%d/%m} : {n} prospect{'s' if n > 1 else ''} ; {', '.join(inconnues)}",
               f"donnée manquante : {', '.join(manquants)}", "gold.bv_academy_prospects")
        return
    for p in pros:
        tete = f"Académie, rapport du {rapport:%d/%m} : {p['name']} ({p['position']}, {p['age']} ans, TSP {p['tsp_min']}-{p['tsp_max']})"
        ph = float(cote[0]["p_high_8_10"])
        gain, cout = ph / 100 * float(vals["academie_valeur_high"]), float(vals["academie_cout_test"])
        verdict = "tester" if gain > cout else "ignorer"
        ajoute(None, 2, f"{tete} : {verdict}",
               f"P(High) {str(ph).replace('.', ',')} % × valeur d'un High {montant(vals['academie_valeur_high'])} = {montant(gain)} "
               f"contre test {montant(cout)} (règle d'espérance, à valider)", "gold.bv_academy_potential_odds, core.game_params")


def boucle(donnees, refs, ajoute):
    """K4 : « n décisions à mesurer, m faits à relier » si n + m > 0 ; n = gold.decisions_a_evaluer, m = identifiants
    `[décision=<id>]` des registres des 7 derniers jours (relier_faits.lire_references) encore « proposed » en base.
    Lecture seule : les commandes qui écrivent sont citées, jamais lancées. Une source illisible compte 0."""
    import relier_faits
    a_mesurer = sum(int(r["n"]) for r in lignes_de(donnees, "a_evaluer"))
    ouvertes = {int(r["id"]): (r["status"], r["game"]) for r in lignes_de(donnees, "decisions_proposees")}
    a_relier = sum(1 for r in relier_faits.plan(refs or [], ouvertes, "basketvibe") if r["a_faire"])
    if a_mesurer + a_relier == 0:
        return
    pl = lambda n, s, p: f"{n} {s if n < 2 else p}"
    ajoute(None, 3, f"Boucle d'apprentissage : {pl(a_mesurer, 'décision à mesurer', 'décisions à mesurer')}, "
                    f"{pl(a_relier, 'fait à relier', 'faits à relier')}",
           "python -I pipelines/evaluer_decisions.py ; python -I pipelines/relier_faits.py basketvibe",
           "gold.decisions_a_evaluer, registres fait-<jour>.md")


def plan(donnees, erreurs, jour, maintenant, fait="", sources=None):
    """{'actions': [(limite|None, priorité 1-3, action, détail, source)], 'exports': [texte], 'garder': [texte],
    'infos': [texte]} ; infos = enchères terminées, une ligne chacune, rangées dans « Autres points »."""
    A, exports, garder, infos = [], [], [], []
    S = sources or {}
    restes = list(S.get("restes", []))
    cles = S.get("cles", [])

    def ajoute(limite, prio, action, detail="", source=""):
        A.append((limite, prio, action, detail, source))

    # 1. Matchs à venir : brief tactique du jour (verrou, tests), registre « reste à corriger »
    couverts = []
    # 1 bis (5d, H3) : test de la file d'expériences sur le prochain amical (aujourd'hui ou demain, core.fixture)
    am = prochain_amical(donnees, jour, maintenant)
    joues = lignes_de(donnees, "amical_reglage")
    test = test_en_cours(S.get("experiences"), am, joues)
    apres = ""
    if test:
        e, niveau, _ = test
        apres = f"{texte_test(e, niveau)} (remplace l'agressivité du brief pour ce match)" if e["id"] == "E1" \
            else f"{texte_test(e, niveau)} (remplace ce réglage du brief pour ce match)"
        avance = texte_avancement(e, verifier(S.get("experiences"), joues)[e["id"]])  # M3 : déclarés, vérifiés, écarts
        apres_exports = "après le match exporte : " + ", ".join(e.get("export_requis") or []) + " ; " + avance
    for t in S.get("tactique", []):
        cal = verrou_calendrier(donnees, t["date"], t["match"])
        verrou = f"{cal:%H:%M}" if cal else t["verrou"]  # scheduled_at de core.fixture d'abord, sinon l'heure du brief
        limite = cal or (dt.datetime.combine(t["date"], dt.time.fromisoformat(t["verrou"])) if t["date"] and t["verrou"] else None)
        reste = next((r for r in restes if meme_match(r["match"], t["match"])), None)
        if limite is not None and limite < maintenant:  # verrou passé : plus une action à faire maintenant (PB9)
            couverts.append(t["match"])
            if reste:
                restes.remove(reste)
            continue
        saisie = next((s for s in S.get("saisies", []) if s["date"] == t["date"] and meme_match(s["match"], t["match"])), None)
        quand = jour_fr(t["date"]) if t["date"] else "date inconnue"
        if t["type"] == "ligue":
            titre = f"Ligue {t['manche'] or ''} {'à' if t['lieu'] == 'extérieur' else 'contre'} {t['match']}".replace("  ", " ")
        elif t["type"] == "coupe":
            titre = f"Coupe contre {t['match']}"
        else:
            titre = f"Amical contre {t['match']}"
        if reste and reste["reglages"]:
            etat, prio = f"corrige à l'écran {len(reste['reglages'])} réglages ({regrouper(reste['reglages'])})", 1
        elif deja(fait, t["type"]) or saisie or cle_match(cles, t["match"], t["date"]):
            etat, prio = "", 1  # saisie déclarée faite (registre du jour ou d'un jour antérieur) : la ligne reste, pour l'heure limite et les conditions du test
        else:
            etat, prio = "saisis la tactique maintenant", 1
        detail = f"heure limite du verrou {verrou or 'inconnue'}"
        if test and t["type"] == "amical" and t["date"] == am["date"] and meme_match(t["match"], am["match"]):
            detail = f"{apres} ; {detail} ; {apres_exports}"
            test = None  # ligne du test posée sur celle du brief
        if t["preuves"]:
            detail += " ; le test est perdu si : " + " ; ".join(propre(p.rstrip(".")) for p in t["preuves"])
        if t["vieux"]:
            detail += f" ; brief vieux de {t['age']} jours : relance l'agent tactique"
        ajoute(limite, prio, f"{titre} ({quand})" + (f" : {etat}" if etat else ""), detail,
               t["fichier"] + (", " + reste["fichier"] if reste else ""))
        couverts.append(t["match"])
        if reste:
            restes.remove(reste)
    if test:  # amical sans brief du jour : la ligne vient de core.fixture et du fichier d'expériences
        e, niveau, saisi = test
        etat = f"{texte_test(e, niveau)} saisi" if saisi else f"saisis le {texte_test(e, niveau)}"
        ajoute(am["limite"], 1, f"Amical contre {am['match']} ({jour_fr(am['date'])}) : {etat}",
               f"heure limite du verrou {am['limite']:%H:%M} ; réglage du test à la place de celui du brief ; {apres_exports}",
               "docs/attentes/experiences-amicales-basketvibe.yaml, core.fixture")
        couverts.append(am["match"])
    for r in restes:  # reste à faire sans brief du jour
        limite = dt.datetime.combine(r["date"], dt.time.fromisoformat(r["heure"])) if r["date"] and r["heure"] else None
        couverts.append(r["match"])
        if limite is not None and limite < maintenant:  # verrou passé (PB9)
            continue
        ajoute(limite, 1, f"{r['match'] or 'Match'} : corrige à l'écran {len(r['reglages'])} réglages ({regrouper(r['reglages'])})",
               "", r["fichier"])

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
        cal, r["action"] = recaler(donnees, d, h, r["category"], r["action"])  # H6 : coup d'envoi + décalage
        h = f"{cal:%H:%M}" if cal else h
        if not (d == jour or (d == jour + dt.timedelta(days=1) and maintenant.hour >= 18 and h and h < "10:00")):
            continue
        if r["category"] in ("ligue", "amical") and any(norm(c).split()[0] in norm(r["action"]) for c in couverts if c):
            continue  # la ligne du brief est plus complète
        if r["category"] == "export" and d != jour:
            continue  # export d'après-match de demain : pas une action d'aujourd'hui
        if r["category"] in ("ligue", "amical", "coupe") and h and dt.datetime.combine(d, dt.time.fromisoformat(h)) < maintenant:
            continue  # verrou de saisie passé (PB9)
        if declare(fait, cles, jour, r["category"]):
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
        statut = str(r["statut"])
        if r["ecran"] == "Mes enchères" and statut.endswith("optionnel"):
            # R3 : « optionnel » vaut seulement sans enchère ouverte ; avec une enchère ouverte, page de plus de 24 h = à refaire
            statut = "🟧 à refaire" if r["age_h"] is None or r["age_h"] > 24 else "🟩 à jour"
        if not statut.endswith(("à jour", "optionnel")) and not declare(fait, cles, jour, r["ecran"]):
            exports.append(f"{r['ecran']} ({'jamais exporté' if r['age_h'] is None else str(int(r['age_h'])) + ' h'})")
    ligues = [r for r in lignes_de(donnees, "gold.bv_agenda") if r["category"] == "ligue"]
    apercus = {str(r["match_day"])[:10] for r in lignes_de(donnees, "apercus")}
    if donnees.get("apercus") is None:
        exports.append(manque(donnees, erreurs, "apercus", "Match de ligue : aperçu"))
    for r in ligues:
        d = str(r["day"])[:10]
        if jour <= dt.date.fromisoformat(d) <= jour + dt.timedelta(days=2) and d not in apercus and not declare(fait, cles, jour, "Match de ligue : aperçu"):
            exports.append(f"aperçu du match de ligue du {d[8:]}/{d[5:7]} (aucune ligne adverse en base)")
    vente = lignes_de(donnees, "derniere_vente")
    derniere = vente[0]["derniere"] if vente else None
    if donnees.get("derniere_vente") is None:
        exports.append(manque(donnees, erreurs, "derniere_vente", "Historique global des transferts"))
    elif derniere is None or dt.date.fromisoformat(str(derniere)[:10]) < jour - dt.timedelta(days=1):
        exports.append("historique global des transferts depuis " + ("le début" if derniere is None else str(derniere)[:10]))

    defaite_officielle(donnees, erreurs, S.get("analyste"), ajoute)

    # 6. Alertes (les exports en retard viennent déjà de bv_exports_state)
    m = manque(donnees, erreurs, "gold.bv_daily_alerts", "Équipe (aperçu, joueurs)")
    if m:
        ajoute(None, 2, m)
    for r in lignes_de(donnees, "gold.bv_daily_alerts"):
        cat = CAT_ALERTE.get(r["category"])
        if cat and cat != "Exports":
            ajoute(None, int(r["priority"]), r["alert"], "", "gold.bv_daily_alerts")
    alertes_match(donnees, erreurs, fait, cles, jour, A, exports, ajoute)
    academie(donnees, erreurs, cles, maintenant, ajoute)
    boucle(donnees, S.get("refs_decisions"), ajoute)

    # 7. Décisions par secteur (étape 6 du skill) : une ligne si la règle du YAML se déclenche, sinon « Garder »
    m = manque(donnees, erreurs, "gold.bv_position_summary", "Équipe (aperçu, joueurs)")
    pos = lignes_de(donnees, "gold.bv_position_summary")
    marche_frais = etat.get("Marché (enchères)") is not None and str(etat["Marché (enchères)"]["statut"]).endswith("à jour")
    decides = [norm(c["nom"]) for c in S.get("cibles", [])]  # déjà décidés (plafond de la décision) : pas de 2e ligne

    # Capacité (PB8, décision de l'utilisateur du 09/11) : solde moins les enchères encore ouvertes, sans réserve de sécurité.
    solde = next((r.get("balance") for r in lignes_de(donnees, "gold.bv_finance_health")), None)
    ouvertes = [c for c in S.get("cibles", []) if c["fin"] is None or c["fin"] > maintenant]
    reste_cap = float(solde) - sum(c["max"] for c in ouvertes) if solde is not None else None

    def libre(r):
        return not any(n in norm(r["name"]) for n in decides)

    def pas_finie(r):  # une enchère du Marché dont la fin est passée n'est plus une action (PB9) ; fin inconnue : reste proposée
        fin = r.get("ends_paris")
        return not fin or dt.datetime.fromisoformat(str(fin)[:19]) > maintenant

    def finance(prix):  # prix inconnu ou capacité illisible : on ne tranche pas, la cible reste proposée
        return reste_cap is None or prix is None or float(prix) <= reste_cap

    if m:
        ajoute(None, 3, m)
    elif pos:
        faible = min(pos, key=lambda r: float(r["ps_avg"]))
        minces = [r for r in pos if int(r["depth"]) <= 2]
        cands = [r for r in lignes_de(donnees, "gold.bv_market_candidates")
                 if vrai(r["enters_top8"]) and str(r["would_rank_in_slot"]) == "1" and r["position"] == faible["position"]
                 and libre(r) and finance(r["current_price"]) and pas_finie(r)] if marche_frais else []
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
        vendre_remplacable(donnees, ajoute)
        garder.append("effectif, vendre pour profit : règle non écrite — à valider (seuil de déclenchement non validé)")
        if "objectifs" not in donnees:  # A3 : sans gold.match_objective (anciens jeux de données), l'ancienne demi-ligne
            garder.append("effectif, jeunes : règle non écrite — à valider (le script ne sait pas dire si un match de ligue est gagné d'avance)")
    minutes_jeunes(donnees, erreurs, ajoute, garder)
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
        solde_projete(donnees, erreurs, fh[0], ajoute)
    m = manque(donnees, erreurs, "gold.bv_market_bargains", "Marché (enchères)")
    if m:
        ajoute(None, 2, m)
    elif not marche_frais:
        garder.append("transferts : pas d'enchère nouvelle, l'export du Marché a plus de 24 h")
    else:
        bonnes = [r for r in lignes_de(donnees, "gold.bv_market_bargains")
                  if vrai(r["ref_reliable"]) and float(r["resale_margin_p25"] or 0) > 0 and int(r["ref_n"] or 0) >= 5 and libre(r)
                  and finance(r["bid_ceiling_resale"]) and pas_finie(r)][:2]
        for r in bonnes:
            fin = dt.datetime.fromisoformat(str(r["ends_paris"])[:19]) if r.get("ends_paris") else None
            ajoute(fin, 2, f"Enchère maximale {montant(r['bid_ceiling_resale'])} sur {r['name']} ({r['position']}, PS {r['ps']})",
                   f"marge de revente p25 {montant(r['resale_margin_p25'])}", "gold.bv_market_bargains")
        if not bonnes:
            garder.append("transferts : aucune affaire fiable qui tienne dans le solde moins les enchères encore ouvertes "
                          "(capacité restante"
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


def journaliser(jour, secondes, requetes, quand=None):
    if not JOURNAL.exists():
        JOURNAL.write_text("# Journal de durée de `aujourdhui.py` (une ligne par exécution)\n\n"
                           "| Date | Jour du plan | Durée (s) | Requêtes |\n|---|---|---|---|\n", encoding="utf-8")
    with JOURNAL.open("a", encoding="utf-8") as f:
        f.write(f"| {(quand or heure_paris_naive()).strftime('%Y-%m-%d %H:%M')} | {jour} | {secondes:.1f} | {requetes} |\n")


def heure_paris_naive():
    """Heure de Paris (pipelines/heure_paris.py, jamais l'horloge du shell, UTC en cloud), sans fuseau pour les comparaisons."""
    from heure_paris import paris
    return paris().replace(tzinfo=None)


def reperes(jour_arg, maintenant_arg, ref):
    """(jour du plan, heure de référence) : `ref` = heure de Paris ; `--jour` change le jour, `--maintenant HH:MM` l'heure (PB9)."""
    jour = dt.date.fromisoformat(jour_arg) if jour_arg else ref.date()
    if maintenant_arg:
        try:
            h = dt.time.fromisoformat(maintenant_arg)
        except ValueError:
            sys.exit(f"aujourdhui.py : --maintenant attend HH:MM, reçu « {maintenant_arg} »")
        return jour, dt.datetime.combine(jour, h.replace(second=0, microsecond=0))
    return jour, ref


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("jeu")
    ap.add_argument("--jour", help="AAAA-MM-JJ : rejeu d'un jour passé quand la vue le permet")
    ap.add_argument("--maintenant", help="HH:MM : heure de référence pour les tests (rien n'est écrit) ; défaut : l'heure de Paris")
    a = ap.parse_args()
    if a.jeu != "basketvibe":
        sys.exit("aujourdhui.py : seul basketvibe est branché (lot L2)")
    ref = heure_paris_naive()
    jour, maintenant = reperes(a.jour, a.maintenant, ref)
    debut = time.time()
    sqlmod = charger_sql()
    donnees, erreurs, n = lire_tout(sqlmod.executer, a.jour)
    sys.stdout.reconfigure(encoding="utf-8")
    rendu = plier(rendre(plan(donnees, erreurs, jour, maintenant, lire_fait(jour), lire_sources(donnees, jour)), jour, erreurs))
    print(rendu)
    if not a.jour and not a.maintenant:  # instantané quotidien (écrasé si relancé le même jour) : ni rejeu ni simulation d'heure
        fichier = BASE / f"aujourdhui-{jour.isoformat()}.md"
        fichier.parent.mkdir(parents=True, exist_ok=True)
        fichier.write_text(f"<!-- généré le {maintenant.strftime('%Y-%m-%d %H:%M')} -->\n{rendu}\n", encoding="utf-8")
    nonrej = [k for k, v in donnees.items() if v == "rejeu"]
    if nonrej:
        print("\n" + "\n".join(f"rejeu non disponible pour {k}" for k in nonrej))
    if not a.maintenant:
        journaliser(a.jour or "aujourd'hui", time.time() - debut, n, ref)
    return 0


if __name__ == "__main__":
    sys.exit(main())
