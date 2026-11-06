"""Que faire aujourd'hui Hockey Nation, sans modèle ni agent (critères H1 à H7 de docs/refonte-v3/journal-aujourdhui.md).

Même plan que le skill hockeynation-aujourdhui, qui fait foi : 5 blocs en deux temps. Lecture seule, 8 requêtes au plus
(executer() de sql.py), 60 secondes au plus. Réutilise match_engine_etat.py (registre des règles, intervalle de Wilson).
  --temps 1  Lire : exports (bloc 1), scouts (bloc 2), matchs joués des 4 équipes (bloc 3)
  --temps 2  Agir : tactique PRO si déclenchée (bloc 4), entraînement (bloc 5), 5 actions au plus
Écrit outputs/hockeynation/aujourdhui-AAAA-MM-JJ.md (les deux temps) et une ligne de durée dans le journal.
Aucun code interne dans le rendu : les règles sont dites en mots.

Usage : python -I pipelines/aujourdhui_hockeynation.py --temps 1|2 [--jour AAAA-MM-JJ] [--depuis AAAA-MM-JJ]
"""
import argparse
import datetime as dt
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python -I n'ajoute pas le dossier du script
import match_engine_etat as me  # noqa: E402
import sql as sqlmod  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent
BASE = RACINE / "outputs/hockeynation"
JOURNAL = RACINE / "docs/refonte-v3/journal-aujourdhui.md"
EQUIPES = ("PRO", "FRM", "U21", "U17")
ACTIONS_MAX = 5
# Tests ouverts : (premier jour, matchs de ligue PRO avant échéance, libellé). PP/PK : date de la décision, à valider (H4c).
TESTS = {
    "plan": (dt.date(2026, 10, 29), 10, "plan de jeu à shift length court : 10 matchs de ligue"),
    "pp_pk": (dt.date(2026, 11, 2), 5, "réglages jeu de puissance et infériorité : 5 matchs de ligue (à valider)"),
}
EXPORTS_UTILES = (("Roster", "roster"), ("Scouting staff", "scouting staff"))
CATEGORIES_SCOUT = {"A poste + nation": 0, "B poste": 1, "C nation": 2}

Q_DIVERS = """
select 'export' as k, to_jsonb(e) as v from gold.hn_exports_state e
union all select 'today', to_jsonb(t) from gold.hn_today t
union all select 'cap', to_jsonb(c) from silver.hn_cap_now c
union all select 'controle', to_jsonb(x) from gold.hn_tactique_controle x
union all select 'case', to_jsonb(l) from gold.hn_saisie_lignes l where l.controle <> 'ok'
union all select 'training', jsonb_build_object('team_level', team_level, 'dernier', max(captured_at), 'joueurs', count(*)) from silver.hn_training_log group by team_level
union all select 'declare', to_jsonb(d) from silver.hn_declared d where d.detail ilike '%déjà scouté%'"""
Q_SCOUTS = "select scout, nb_total from gold.hn_scout_liste order by scout"
Q_CIBLES = "select scout, categorie, rang, joueur, poste, nation, rapports from gold.hn_scout_targets order by scout, categorie, rang"
Q_BOARD = "select scout, poste, nation from gold.hn_scout_board where statut = 'embauché' order by scout"
Q_JEUX = """
select g.game_id, coalesce(g.team_level, (select y.level from silver.hn_my_teams y where y.city || ' ' || y.nickname in (g.home, g.away) limit 1)) as equipe,
 g.game_type, g.scheduled_at, g.my_result, g.home, g.away, g.home_is_mine, (d.game_id is not null) as detail
from silver.hn_games g left join silver.hn_game_detail d using (game_id)
where (g.home_is_mine or g.away_is_mine or exists (select 1 from silver.hn_my_teams y where y.city || ' ' || y.nickname in (g.home, g.away)))
 and g.scheduled_at >= (select day1 from gold.hn_today) order by g.scheduled_at"""
Q_PLAN = "select team_level, ordre, joueur, competence, coach from gold.hn_training_plan order by team_level, ordre"
REQUETES = {"divers": Q_DIVERS, "scouts": Q_SCOUTS, "cibles": Q_CIBLES, "board": Q_BOARD, "details": me.Q_MATCHS,
            "jeux": Q_JEUX, "gardiens": me.Q_GARDIENS, "plan": Q_PLAN}

try:
    from zoneinfo import ZoneInfo
    PARIS = ZoneInfo("Europe/Paris")
except Exception:  # noqa: BLE001 - tzdata absent : heure d'hiver
    PARIS = dt.timezone(dt.timedelta(hours=1))


def vers_dt(x):
    """datetime naïf à l'heure de Paris depuis une date, un datetime ou une chaîne ISO ; None si vide."""
    if x in (None, ""):
        return None
    if isinstance(x, dt.datetime):
        d = x
    elif isinstance(x, dt.date):
        d = dt.datetime.combine(x, dt.time())
    else:
        d = dt.datetime.fromisoformat(str(x).replace("Z", "+00:00"))
    return d.astimezone(PARIS).replace(tzinfo=None) if d.tzinfo else d


def vers_date(x):
    d = vers_dt(x)
    return d.date() if d else None


def lignes(donnees, nom):
    d = donnees.get(nom)
    if not d:
        return []
    cols, rows = d
    return [dict(zip(cols, r)) for r in rows]


def lire_tout(executer):
    """{nom: (colonnes, lignes)}, nombre de requêtes ; une vue illisible donne None, jamais un arrêt."""
    donnees, erreurs = {}, {}
    for nom, sql in REQUETES.items():
        try:
            donnees[nom] = executer(sql)
        except SystemExit as e:
            donnees[nom], erreurs[nom] = None, str(e)[:80]
    return donnees, erreurs, len(REQUETES)


def divers(donnees, k):
    """Objets de la requête « divers » pour la clé k. Le transport HTTPS de sql.py rend une cellule jsonb en chaîne JSON : on la relit."""
    return [json.loads(r["v"]) if isinstance(r["v"], str) else r["v"] for r in lignes(donnees, "divers") if r["k"] == k]


def lire_fait(jour, base=BASE):
    """Lignes du registre fait-<jour>.md en minuscules, apostrophes droites."""
    f = Path(base) / f"fait-{jour.isoformat()}.md"
    return f.read_text(encoding="utf-8").lower().replace("’", "'").splitlines() if f.exists() else []


def fait_dit(fait, *mots):
    """Une ligne du registre cite tous les mots et dit que l'export est refait / exporté."""
    return any(all(m in l for m in mots) and any(v in l for v in ("refait", "exporté", "exporte", "export")) for l in fait)


def heure_fait(ligne, jour):
    """Heure de Paris d'une ligne du registre « [HH:MM UTC] … », None sinon."""
    m = re.search(r"\[(\d{2}):(\d{2}) utc\]", ligne)
    if not m:
        return None
    utc = dt.datetime.combine(jour, dt.time(int(m.group(1)), int(m.group(2))), tzinfo=dt.timezone.utc)
    return utc.astimezone(PARIS).replace(tzinfo=None)


def derniere_ligne(fait, jour, themes, verbes):
    """Heure de la dernière ligne du registre qui cite un des thèmes et un des verbes ; None s'il n'y en a pas."""
    hs = [heure_fait(l, jour) for l in fait if any(t in l for t in themes) and any(v in l for v in verbes)]
    hs = [h for h in hs if h]
    return max(hs) if hs else None


def en_mots(texte):
    """Retire les numéros de règle et les codes de saison du texte rendu."""
    t = re.sub(r"\b[LC]-\d{3}\s*", "", str(texte))
    return re.sub(r"\bS27\b", "saison en cours", re.sub(r"\bS26\b", "saison précédente", t)).strip()


# ---------------------------------------------------------------- bloc 1 : exports

def bloc_exports(donnees, fait, jour, jeux):
    """[(priorité, action)], [export à faire aujourd'hui]. Un export du registre n'est jamais redemandé (H1)."""
    actions, a_faire = [], []
    etat = {e["ecran"]: e for e in divers(donnees, "export")}
    for nom, mot in EXPORTS_UTILES:
        e = next((v for k, v in etat.items() if k.startswith(nom)), None)
        if e is None or fait_dit(fait, mot):
            continue
        if "à refaire" in str(e.get("statut", "")) or (nom == "Scouting staff" and float(e.get("age_h") or 0) > 24):
            actions.append(("🟧 IMPORTANT", f"Exporte {nom} (relevé du {e['dernier_paris'][:16].replace('T', ' ')}, {e['age_h']} h)"))
            a_faire.append(nom)
    pour_pages = {}
    for j in jeux:
        if j.get("my_result") and j.get("equipe") in EQUIPES:
            pour_pages[j["equipe"]] = j  # le plus récent gagne (liste triée par date)
    if not fait_dit(fait, "matchs"):
        for eq in EQUIPES:
            j = pour_pages.get(eq)
            if j and not j.get("detail"):
                actions.append(("🟧 IMPORTANT", f"Exporte la page du match d'avant de {eq} ({vers_date(j['scheduled_at'])}, {adversaire(j)})"))
                a_faire.append(f"page du match {eq}")
    training = {t["team_level"]: t for t in divers(donnees, "training")}
    change = derniere_ligne(fait, jour, ("entraînement", "entrainement", "training"), ("changé", "modifié", "saisi"))
    manque = [eq for eq in ("PRO", "FRM") if eq not in training]
    vieux = [eq for eq, t in training.items() if change and vers_dt(t["dernier"]) < change and eq in ("PRO", "FRM")]
    if (manque or vieux) and not (fait_dit(fait, "training") and not change):
        actions.append(("🟧 IMPORTANT", "Exporte Training (journal d'entraînement plus vieux que le dernier changement : " + ", ".join(manque + vieux) + ")"))
        a_faire.append("Training")
    return actions, a_faire


def adversaire(j):
    return j["away"] if j.get("home_is_mine") else j["home"]


# ---------------------------------------------------------------- bloc 2 : scouts

def bloc_scouts(donnees, fait):
    """[(scout, cible, poste, nation, catégorie, rapports)] : une ligne par scout ; cibles déclarées « déjà scouté » retirées (H2)."""
    retires = {re.sub(r"\s+", " ", d.get("name", "")).lower() for d in divers(donnees, "declare")}
    for l in fait:
        m = re.search(r"\]\s*(.+?)\s+déjà scouté", l)
        if m:
            retires.add(m.group(1).strip())
    res = []
    scouts = [s["scout"] for s in lignes(donnees, "scouts")] or sorted({c["scout"] for c in lignes(donnees, "cibles")})
    cibles = lignes(donnees, "cibles")
    for s in scouts:
        cands = [c for c in cibles if c["scout"] == s and not c.get("rapports") and not any(r and (r in c["joueur"].lower() or c["joueur"].lower() in r) for r in retires)]
        cands.sort(key=lambda c: (CATEGORIES_SCOUT.get(c["categorie"], 9), c["rang"]))
        if cands:
            c = cands[0]
            res.append((s, f"n° {c['rang']} {c['joueur']}", c["poste"], c["nation"], c["categorie"], c["rapports"] or 0))
        else:
            res.append((s, "aucune cible sans rapport", "", "", "", ""))
    return res


# ---------------------------------------------------------------- bloc 3 : matchs joués

def analyse_depuis(learnings, repli):
    """Date du dernier match analysé (en-tête de learnings.md) ; repli si absente."""
    m = re.search(r"Dernier match analysé\s*:\s*(\d{4}-\d{2}-\d{2})", learnings or "")
    return dt.date.fromisoformat(m.group(1)) if m else repli


def moyennes(ms, gardiens_par_match, exclu):
    """Réalisation et arrêts moyens des autres matchs de ligue de l'équipe : (buts, tirs, arrêts, tirs subis, n)."""
    autres = [m for m in ms if m["game_id"] != exclu]
    gb, gt = sum(m["bn"] for m in autres), sum(m["tn"] for m in autres)
    ga = gs = 0
    for m in autres:
        g = gardiens_par_match.get(m["game_id"])
        if g:
            ga, gs = ga + g["arrets"], gs + g["tirs"]
    return gb, gt, ga, gs, len(autres)


def juge_match(m, comparaison, gardien):
    """(mérité, pouvait-on gagner, changer la structure, échelle) en mots, avec n et intervalle (H3a, H3b)."""
    gb, gt, ga, gs, n = comparaison
    if not n or not gt:
        return "indéterminé : aucun autre match de ligue de l'équipe cette saison", "indéterminé : aucun match de comparaison", "non : pas de comparaison", "composition non lue · tactique non mesurable"
    r_moy = gb / gt
    a_moy = ga / gs if gs else None
    r_bas = me.wilson(m["bn"], m["tn"])[1] < r_moy if m["tn"] else False
    arr = (gardien["arrets"], gardien["tirs"]) if gardien and gardien["tirs"] else None
    a_bas = bool(arr and a_moy is not None and me.wilson(*arr)[1] < a_moy)
    r_sous = bool(m["tn"] and m["bn"] / m["tn"] < r_moy)
    a_sous = bool(arr and a_moy is not None and arr[0] / arr[1] < a_moy)
    volume_pour = m["xn"] > m["xe"]
    mesures = f"réalisation {me.pct(m['bn'], m['tn'])} ({me.ic(m['bn'], m['tn'])}) contre {100 * r_moy:.1f} % en moyenne" + \
              (f" ; arrêts {me.pct(*arr)} contre {100 * a_moy:.1f} %" if arr and a_moy is not None else "")
    if m["my_result"] == "L":
        merite = ("non mérité" if volume_pour and (r_sous or a_sous) else "mérité" if not volume_pour else "indéterminé") + f", sur {n} matchs"
    elif m["my_result"] == "W":
        merite = ("non mérité" if not volume_pour and (not r_sous or not a_sous) and (m["bn"] / m["tn"] >= r_moy if m["tn"] else False) else "mérité" if volume_pour else "indéterminé") + f", sur {n} matchs"
    else:
        merite = "indéterminé"
    if m["my_result"] != "L":
        return merite, "", "", ""
    if volume_pour and (r_bas or a_bas):
        gagner = f"oui : xG {m['xn']:.2f} contre {m['xe']:.2f} et {mesures}"
    elif not volume_pour and m["tn"] < m["te"]:
        gagner = f"non : xG {m['xn']:.2f} contre {m['xe']:.2f}, tirs {m['tn']} contre {m['te']}"
    else:
        gagner = f"indéterminé : {mesures}"
    echelle = f"force relative : xG {m['xn']:.2f} contre {m['xe']:.2f} · hasard : {'écart décelable' if (r_bas or a_bas) else 'écart non décelable'} · tactique non mesurable"
    return merite, gagner, "", echelle


def regles_du_match(m, gardien):
    """Règles du registre que ce match soutient (« pour ») ou contredit (« contre »), dites en mots."""
    res = []
    reussite_bas = m["tn"] and m["te"] and m["bn"] / m["tn"] < m["bo"] / m["te"]
    sv = gardien["arrets"] / gardien["tirs"] if gardien and gardien["tirs"] else None
    if m["my_result"] == "L":
        if reussite_bas:
            res.append("réalisation, pas volume : pour")
        if sv is not None and sv < me.SEUIL_GARDIEN_D:
            res.append("gardien sous le seuil d'arrêts : pour")
        if (m.get("ppge") or 0) > 0:
            res.append("défense en infériorité (but adverse en jeu de puissance) : pour")
        if m["fow"] >= m["fol"] and m["fow"] + m["fol"]:
            res.append("mises au jeu sans lien avec le résultat : pour")
    elif m["my_result"] == "W":
        if reussite_bas:
            res.append("réalisation, pas volume : contre")
        if sv is not None and sv < me.SEUIL_GARDIEN_D:
            res.append("gardien sous le seuil d'arrêts : contre")
    return res


def bloc_matchs(donnees, jour, depuis, debut_saison):
    """(lignes du tableau des matchs, lignes des défaites, lignes du registre, alerte matchs sans équipe)."""
    jeux = lignes(donnees, "jeux")
    details = {d["game_id"]: d for d in lignes(donnees, "details")}
    gardiens = {}
    for g in lignes(donnees, "gardiens"):
        if g["tirs"] is not None and g["tirs"] > gardiens.get(g["game_id"], {"tirs": -1})["tirs"]:
            gardiens[g["game_id"]] = g
    saison = {}
    for eq in EQUIPES:
        saison[eq] = [dict(details[j["game_id"]]) for j in jeux if j["equipe"] == eq and j["game_type"] == "League"
                      and j["my_result"] and j["game_id"] in details and vers_date(j["scheduled_at"]) >= debut_saison]
    rangs, amicaux = {}, {}
    for eq in EQUIPES:
        for k, j in enumerate([j for j in jeux if j["equipe"] == eq and j["game_type"] == "League"], 1):
            rangs[j["game_id"]] = k
    for k, j in enumerate([j for j in jeux if j["game_type"] == "Friendly" and (j["home_is_mine"] is not None) and j["equipe"] in EQUIPES], 1):
        amicaux[j["game_id"]] = k
    tableau, defaites, inconnus = [], [], []
    for j in jeux:
        if not j.get("my_result") and j.get("equipe") in EQUIPES:
            continue
        eq = j.get("equipe")
        jouee = bool(j.get("my_result"))
        if eq not in EQUIPES:  # jamais ignoré : ligne « équipe inconnue » (H3)
            if jouee:
                inconnus.append(j)
            continue
        if vers_date(j["scheduled_at"]) <= depuis:
            continue
        d = details.get(j["game_id"])
        etiquette = eq + (" — expérience sans notre choix" if eq != "PRO" else "")
        numero = (f"amical n° {amicaux.get(j['game_id'], '?')}" if j["game_type"] == "Friendly" else f"match n° {rangs.get(j['game_id'], '?')}") + f" du {vers_date(j['scheduled_at'])} contre {adversaire(j)}"
        res = "Victoire" if j["my_result"] == "W" else "Défaite"
        if not d:
            tableau.append((etiquette, numero, res, "détail absent : exporte la page du match", "aucune règle concernée"))
            continue
        d = dict(d)
        pool = [m for m in saison[eq] if m["game_id"] != j["game_id"]]
        merite, gagner, _, echelle = juge_match(d, moyennes(pool, gardiens, j["game_id"]), gardiens.get(j["game_id"]))
        regles = regles_du_match(d, gardiens.get(j["game_id"]))
        tableau.append((etiquette, numero, res, merite, " ; ".join(regles) if regles else "aucune règle concernée"))
        if j["my_result"] == "L":
            derniers = sorted(saison[eq], key=lambda m: str(m["jour"]))[-5:]
            contre_nous = sum(1 for m in derniers if m["xn"] < m["xe"])
            changer = (f"oui : volume contre nous dans {contre_nous} des {len(derniers)} derniers matchs de ligue"
                       if gagner.startswith("non") and contre_nous >= 3 else
                       f"non : volume contre nous dans {contre_nous} des {len(derniers)} derniers matchs de ligue")
            defaites.append((etiquette, numero, echelle, gagner, changer))
    for j in inconnus:
        tableau.append(("équipe inconnue", f"match du {vers_date(j['scheduled_at'])}, {j['home']} contre {j['away']}", "Victoire" if j["my_result"] == "W" else "Défaite", "indéterminé : équipe inconnue, aucune comparaison", "aucune règle concernée"))
    pro = [dict(d) for d in details.values() if d["team_level"] == "PRO"]  # toute la base PRO, saison précédente comprise (comme le registre complet)
    registre = [f"{en_mots(r['regle'])} : {r['verdict']} (n = {r['n']} ; {r['mesure']})" for r in
                me.evaluer(pro, [g for g in lignes(donnees, "gardiens") if g["game_id"] in {m["game_id"] for m in pro}], [], {}, complet=False)
                if re.match(r"L-0(01|02|04|06|19)", r["regle"])]
    return tableau, defaites, [en_mots(x) for x in registre], bool(inconnus)


# ---------------------------------------------------------------- bloc 4 : tactique PRO si déclenchée

def declencheurs(donnees, fait, jour, jeux):
    """Motifs qui déclenchent la tactique PRO (H4) ; liste vide = bloc absent."""
    motifs = []
    etat = {e["ecran"]: e for e in divers(donnees, "export")}
    lineups = vers_dt(etat.get("Lineups PRO", {}).get("dernier_paris"))
    change = derniere_ligne(fait, jour, ("lineup",), ("changée", "modifiée", "changement"))
    if lineups and change and lineups < change:
        motifs.append(f"la lineup exportée ({lineups:%H:%M}) est plus vieille que le dernier changement ({change:%H:%M})")
    # (b) case vide, hors poste, joueur parti : « cases différentes de la cible » n'en est pas un (c'est un écart à saisir)
    hors = [c for c in divers(donnees, "controle") if str(c.get("etat")) != "ok" and re.search(r"introuvable|hors poste|même joueur|vide|parti", str(c.get("controle")))]
    cases = divers(donnees, "case")
    if hors or cases:
        motifs.append(f"{len(cases)} case(s) de la lineup en défaut" + (" ; contrôles : " + ", ".join(str(c.get("controle")) for c in hors) if hors else ""))
    pro = [j for j in jeux if j["equipe"] == "PRO" and j["game_type"] == "League" and j["my_result"]]
    for cle, (debut, n, libelle) in TESTS.items():
        vus = [j for j in pro if vers_date(j["scheduled_at"]) >= debut]
        if len(vus) >= n:
            motifs.append(f"test arrivé à échéance : {libelle} ({len(vus)} matchs joués depuis le {debut})")
    for eq in EQUIPES:
        dern = [j["my_result"] for j in jeux if j["equipe"] == eq and j["game_type"] == "League" and j["my_result"]][-2:]
        if dern == ["L", "L"]:
            motifs.append(f"deux défaites de suite en ligue pour {eq}")
    if any(("nouveau joueur" in l or "monté" in l or "signé" in l) for l in fait):
        motifs.append("nouveau joueur signalé dans le registre du jour")
    return motifs


# ---------------------------------------------------------------- bloc 5 : entraînement

def bloc_entrainement(donnees):
    """{équipe: [(ordre, joueur, compétence, coach)]} lu dans le plan ; sans compétence ouverte = fin de liste, sans proposition (H5)."""
    res = {eq: [] for eq in EQUIPES}
    for r in lignes(donnees, "plan"):
        ouverte = r.get("competence") not in (None, "") and "plafonn" not in str(r["competence"]).lower()
        res.setdefault(r["team_level"], []).append((r["ordre"] if r.get("ordre") is not None else "fin de liste", r["joueur"],
                                                    r["competence"] if ouverte else "aucune compétence ouverte", (r.get("coach") or "") if ouverte else ""))
    return res


# ---------------------------------------------------------------- rendu

def table(entetes, rows):
    out = ["| " + " | ".join(entetes) + " |", "|" + "---|" * len(entetes)]
    return out + ["| " + " | ".join(str(c).replace("|", "/") for c in r) + " |" for r in rows]


def plan_du_jour(donnees, jour, fait, learnings="", depuis=None):
    """Calcule les deux temps. Renvoie {'temps1', 'temps2', 'a_faire', 'inconnus'} (textes déjà rendus)."""
    jeux = lignes(donnees, "jeux")
    today = divers(donnees, "today")
    debut_saison = vers_date(today[0]["day1"]) if today and today[0].get("day1") else dt.date(2026, 10, 25)
    depuis = depuis or analyse_depuis(learnings, jour - dt.timedelta(days=2))
    actions1, a_faire = bloc_exports(donnees, fait, jour, jeux)
    scouts = bloc_scouts(donnees, fait)
    matchs, defaites, registre, inconnus = bloc_matchs(donnees, jour, depuis, debut_saison)
    cap = divers(donnees, "cap")
    urgent = [("🟥 URGENT", "Finances", f"Plafond salarial négatif ({cap[0]['cap_space']:,} $) : −30 % en match tant qu'il l'est".replace(",", " "))] if cap and cap[0].get("cap_space", 0) < 0 else []
    jour_saison = today[0].get("season_day") if today else "?"
    t1 = [f"# Hockey Nation — temps 1 : Lire (jour de saison {jour_saison}, {jour})", ""]
    if urgent:
        t1 += table(["Priorité", "Catégorie", "Action"], urgent) + [""]
    t1 += ["## 1. Exports", ""]
    t1 += table(["Priorité", "Catégorie", "Action"], [(p, "Export", a) for p, a in actions1]) + [""] if actions1 else ["Aucun export en retard parmi Roster, pages de match et Scouting.", ""]
    t1 += ["## 2. Scouts", ""] + table(["Scout", "Cible", "Poste", "Nation", "Catégorie", "Rapports"], scouts) + ["", "## 3. Matchs joués des 4 équipes", ""]
    t1 += table(["Équipe", "Match", "Résultat", "Mérité ou non", "Règle du registre"], matchs) + [""] if matchs else ["Aucun match joué depuis le dernier passage.", ""]
    if defaites:
        t1 += table(["Équipe", "Match perdu", "Échelle", "Pouvait-on gagner", "Changer la structure"], defaites) + [""]
    t1 += (["Registre du Match Engine :"] + [f"- {r}" for r in registre] + [""]) if registre else []
    t1 += ["Dis « actions » pour passer au temps 2.", "Exports à faire aujourd'hui : " + (" ; ".join(a_faire) if a_faire else "aucun")]
    motifs = declencheurs(donnees, fait, jour, jeux)
    plan = bloc_entrainement(donnees)
    acts = list(urgent)
    if motifs:
        acts.append(("🟧 IMPORTANT", "Tactique", "Saisis la lineup PRO selon le rendu figé : " + " ; ".join(motifs)))
    for eq in EQUIPES:
        if plan.get(eq):
            acts.append(("🟧 IMPORTANT", "Entraînement", f"Vérifie et ressaisis l'ordre de choix {eq} ({len(plan[eq])} joueurs, tableau ci-dessous)"))
    ordre = {"🟥 URGENT": 0, "🟧 IMPORTANT": 1, "🟩 SUIVI": 2}
    acts.sort(key=lambda a: ordre[a[0]])
    t2 = [f"# Hockey Nation — temps 2 : Agir ({jour})", ""]
    t2 += table(["Priorité", "Catégorie", "Action"], acts[:ACTIONS_MAX]) + [""]
    if acts[ACTIONS_MAX:]:
        t2 += ["Autres actions (" + str(len(acts) - ACTIONS_MAX) + ") : " + " ; ".join(a[2] for a in acts[ACTIONS_MAX:]), ""]
    if not motifs:
        t2 += []
    for eq in EQUIPES:
        if plan.get(eq):
            t2 += [f"Ordre de choix {eq}", ""] + table(["Ordre", "Joueur", "Compétence", "Coach"], plan[eq]) + [""]
    t2 += ["Exports à faire aujourd'hui : " + (" ; ".join(a_faire) if a_faire else "aucun")]
    return {"temps1": "\n".join(t1), "temps2": "\n".join(t2), "a_faire": a_faire, "inconnus": inconnus, "motifs": motifs, "actions": acts}


def journaliser(etiquette, secondes, requetes):
    with JOURNAL.open("a", encoding="utf-8") as f:
        f.write(f"| {dt.datetime.now().strftime('%Y-%m-%d %H:%M')} | {etiquette} | {secondes:.1f} | {requetes} |\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--temps", type=int, choices=(1, 2), required=True)
    ap.add_argument("--jour", help="AAAA-MM-JJ (par défaut aujourd'hui)")
    ap.add_argument("--depuis", help="AAAA-MM-JJ : matchs joués après cette date (par défaut la date du dernier match analysé)")
    a = ap.parse_args()
    jour = dt.date.fromisoformat(a.jour) if a.jour else dt.date.today()
    debut = time.time()
    donnees, erreurs, n = lire_tout(sqlmod.executer)
    learnings = (BASE / "learnings.md").read_text(encoding="utf-8") if (BASE / "learnings.md").exists() else ""
    res = plan_du_jour(donnees, jour, lire_fait(jour), learnings, dt.date.fromisoformat(a.depuis) if a.depuis else None)
    sys.stdout.reconfigure(encoding="utf-8")
    print(res["temps1"] if a.temps == 1 else res["temps2"])
    if erreurs:
        print("\nVues illisibles : " + " ; ".join(f"{k} ({v})" for k, v in erreurs.items()))
    fichier = BASE / f"aujourdhui-{jour.isoformat()}.md"
    fichier.parent.mkdir(parents=True, exist_ok=True)
    fichier.write_text(f"<!-- généré le {dt.datetime.now():%Y-%m-%d %H:%M} -->\n{res['temps1']}\n\n{res['temps2']}\n", encoding="utf-8")
    secondes = time.time() - debut
    journaliser(f"hockeynation temps {a.temps} ({jour})", secondes, n)
    if secondes > 60:
        print(f"\nDurée {secondes:.1f} s : au-dessus des 60 s du critère")
    return 0


if __name__ == "__main__":
    sys.exit(main())
