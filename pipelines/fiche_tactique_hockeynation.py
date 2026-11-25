"""Fiche tactique Hockey Nation d'une équipe : tableau complet à recopier dans l'écran Lineups (lecture seule, sans modèle).

Équipes : bloc `equipes` de docs/attentes/jeux/hockeynation.yaml (PRO, ISL, ISL21, HUA ; ids dans match_engine_etat.EQUIPES_ID).
Sources lues (silver.hn_api) : dernier roster de l'équipe, dernier export Lineups (s'il existe), pages de calendrier
(prochain match). Verrouillage = coup d'envoi − 1 h (lignes prises en compte au moins 1 h avant, sinon −30 % ;
skill hockeynation-match-calendrier, 06-mises-a-jour et 07-condition-plan-de-jeu).

Règles de choix (toutes citées dans la fiche) :
- lignes et paires : postes listés du joueur seulement (hors poste −20 %, 02-lignes-pro) ; note décroissante ; seuils d'endurance
  L1 7+, L2 6+, D1 8+, D2 6+, G1 7+ tolérés à −1 (Discord talonflame1 2026-04-04, docs/attentes/jeux/hockeynation.yaml `seuils`) ;
  amateurs (−5 % pour l'équipe) et joueurs sans note lue en dernier recours ;
- jeu de puissance : SHO + PAS + SKA (Discord a_ferk, c0ntrail 2026-07-19), +1 SHO/PAS si Powerplay Specialist ;
- infériorité : DEF + CHK + SKA + PWR (guide, Players), +1 chacune si Penalty Killer ; le registre du 25/11 confirme sur 268
  équipes-matchs que l'infériorité pèse sur le résultat (PK 75,8 % en défaite, 87,0 % en victoire) ;
- 4 contre 4 : SKA + PAS + SHO ; gardien retiré : SHO + PAS ; un joueur une seule fois par type (PP, PK4, PK3, 4 contre 4) ;
- PRO : seuls les réglages que le registre soutient changent (infériorité) ; le reste garde la saisie du jeu.

Usage : python -I pipelines/fiche_tactique_hockeynation.py <PRO|ISL|ISL21|HUA> [--jour AAAA-MM-JJ] [--ecrire]
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import match_engine_etat as me  # noqa: E402
import sql as sqlmod  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent
BRIEFS = RACINE / "outputs/hockeynation/briefs"
ID = {v: k for k, v in me.EQUIPES_ID.items()}
NOM = {"PRO": "PRO (Chomelix Cows)", "ISL": "équipe nationale d'Islande", "ISL21": "Islande U21 (nationale)", "HUA": "Huaraz Lamas (tournoi)"}
FICHIER = {"PRO": "pro", "ISL": "islande", "ISL21": "islande-u21", "HUA": "huaraz-lamas"}
EXPORT_LINEUPS = {"PRO": "l'onglet Lineups de l'équipe PRO", "ISL": "l'onglet Lineups de l'équipe nationale (Iceland)",
                  "ISL21": "l'onglet Lineups de l'équipe nationale U21 (Iceland U21)",
                  "HUA": "l'onglet Lineups de l'équipe de tournoi Huaraz Lamas (page de l'équipe dans Queens League: Nine Lives)"}
SEUIL_END = {"L1": 7, "L2": 6, "D1": 8, "D2": 6, "G1": 7}
TOLERANCE = 1
PLAN = {"tempo": ("tempo", ["lent", "normal", "rapide"]), "mentality": ("mentalité", ["défensive", "équilibrée", "offensive"]),
        "aggression": ("agressivité", ["calme", "normale", "agressive"]), "puckPressure": ("pression sur le palet", ["légère", "normale", "forte"]),
        "shiftLength": ("durée des présences", ["courte (35-40 s)", "normale (41-49 s)", "longue (50-55 s)"]),
        "pullGoalie1": ("retrait du gardien à 1 but", ["jamais", "parfois", "toujours"]),
        "pullGoalie2": ("retrait du gardien à 2 buts", ["jamais", "parfois", "toujours"])}  # libellés : resume.md § Plan de jeu
UNITES = [("PP1", ["C", "LW", "RW", "D", "ANY"]), ("PP2", ["C", "LW", "RW", "D", "ANY"]),
          ("PK4-1", ["FW1", "FW2", "LD", "RD"]), ("PK4-2", ["FW1", "FW2", "LD", "RD"]),
          ("PK3-1", ["FW", "LD", "RD"]), ("PK3-2", ["FW", "LD", "RD"]),
          ("4V4-1", ["FW1", "FW2", "LD", "RD"]), ("4V4-2", ["FW1", "FW2", "LD", "RD"]), ("EXT", ["FW1", "FW2"])]
LIBELLE_UNITE = {"PP1": "jeu de puissance 1", "PP2": "jeu de puissance 2", "PK4-1": "infériorité 1 (4 joueurs)",
                 "PK4-2": "infériorité 2 (4 joueurs)", "PK3-1": "infériorité à 3, unité 1", "PK3-2": "infériorité à 3, unité 2",
                 "4V4-1": "4 contre 4, unité 1", "4V4-2": "4 contre 4, unité 2", "EXT": "gardien retiré"}

Q_ROSTER = """select body from silver.hn_api where route in ('/team/:id/roster', '/user-tournament-team/:id/roster')
 and endpoint like '%{id}%' order by captured_at desc limit 1"""
Q_LINEUPS = "select captured_at, body from silver.hn_api where route = '/team/:id/lineups' and endpoint like '%{id}%' order by captured_at desc limit 1"
Q_CAL = """select body from silver.hn_api where route in ('/club/:id/game-overview', '/team/:id/schedule', '/nation/:id/game-overview',
 '/user-tournament-team/:id/game-overview') and captured_at > now() - interval '3 days' and body::text like '%{id}%' order by captured_at desc limit 6"""


def _json(x):
    return json.loads(x) if isinstance(x, str) else x


def joueurs_de(roster):
    """[{id, nom, postes, note, comp, ...}] depuis le corps d'un roster (players[] ou liste)."""
    pl = roster.get("players", roster) if isinstance(roster, dict) else roster
    res = []
    for p in pl:
        comp = {s["id"]: s.get("lvl") for s in p.get("skills", [])}
        res.append({"id": p["id"], "nom": f"{p['firstname']} {p['lastname']}", "postes": p.get("positions") or [],
                    "note": p.get("rating"), "comp": comp, "amateur": bool(p.get("amateur")), "goalie": bool(p.get("goalie")),
                    "fatigue": p.get("tiredness"), "fatigue_bloque": bool(p.get("tired")),
                    "speciales": [s["id"] for s in p.get("specialSkills") or []]})
    return res


def c(j, k):
    return j["comp"].get(k) or 0


def valeur(j, critere):
    bonus_pp = 1 if "powerplay-specialist" in j["speciales"] else 0
    bonus_pk = 1 if "penalty-killer" in j["speciales"] else 0
    if critere == "PP":
        return c(j, "SHO") + c(j, "PAS") + c(j, "SKA") + 2 * bonus_pp
    if critere == "PK":
        return c(j, "DEF") + c(j, "CHK") + c(j, "SKA") + c(j, "PWR") + 4 * bonus_pk
    if critere == "4V4":
        return c(j, "SKA") + c(j, "PAS") + c(j, "SHO")
    return c(j, "SHO") + c(j, "PAS")  # EXT


def ordre_ligne(j, seuil):
    """Clé de tri : vrai joueur noté d'abord, note ensuite, seuil d'endurance (toléré à −1) pour départager ; un joueur sous
    le seuil est signalé (confiance faible), pas écarté : la lineup PRO validée le 29/10 garde Seppälä (END 4) en D1."""
    fiable = j["note"] is not None and not j["amateur"]
    return (fiable, j["note"] or 0, seuil is None or c(j, "END") >= seuil - TOLERANCE)


def composer(joueurs, en_place=None):
    """{(ligne, poste): joueur} pour G, L1-L4, paires D, unités spéciales. en_place : {(ligne, poste): nom} du jeu ;
    à valeur égale, le joueur déjà en place garde la case (aucun changement sans gain)."""
    en_place = en_place or {}
    pris, out = set(), {}
    patineurs = [j for j in joueurs if not j["goalie"]]
    gardiens = sorted([j for j in joueurs if j["goalie"] and j["note"] is not None],
                      key=lambda j: (not j["fatigue_bloque"], not j["amateur"], c(j, "END") >= SEUIL_END["G1"] - TOLERANCE, j["note"]), reverse=True)
    if gardiens:
        out[("G", "SG")] = gardiens[0]
    if len(gardiens) > 1:
        out[("G", "BG")] = gardiens[1]
    for ligne, seuil_f, seuil_d in (("L1", "L1", "D1"), ("L2", "L2", "D2"), ("L3", None, None), ("L4", None, None)):
        for poste in ("C", "LW", "RW") + (("LD", "RD") if ligne != "L4" else ()):
            seuil = SEUIL_END.get(seuil_d if poste in ("LD", "RD") else seuil_f) if (seuil_d or seuil_f) else None
            cand = [j for j in patineurs if poste in j["postes"] and j["id"] not in pris]
            if not cand:
                continue
            best = max(cand, key=lambda j: (ordre_ligne(j, seuil), en_place.get((ligne, poste)) == j["nom"]))
            out[(ligne, poste)] = best
            pris.add(best["id"])
    dans_lignes = [j for j in patineurs if j["id"] in pris]
    avants = [j for j in dans_lignes if set(j["postes"]) & {"C", "LW", "RW"}]
    defs = [j for j in dans_lignes if set(j["postes"]) & {"LD", "RD"}]
    for type_, unites, crit in (("PP", ("PP1", "PP2"), "PP"), ("PK4", ("PK4-1", "PK4-2"), "PK"), ("PK3", ("PK3-1", "PK3-2"), "PK"),
                                ("4V4", ("4V4-1", "4V4-2"), "4V4"), ("EXT", ("EXT",), "EXT")):
        utilises = set()
        for u in unites:
            for slot in dict(UNITES)[u]:
                if slot in ("LD", "RD"):
                    pool = [j for j in defs if slot in j["postes"]]
                elif slot == "D":
                    pool = defs
                elif slot in ("C", "LW", "RW"):
                    pool = [j for j in avants if slot in j["postes"]]
                elif slot == "ANY":
                    pool = dans_lignes
                else:  # FW, FW1, FW2
                    pool = avants
                pool = [j for j in pool if j["id"] not in utilises]
                if pool:
                    best = max(pool, key=lambda j: (valeur(j, crit), j["nom"] in {v for (uu, _), v in en_place.items() if uu == u}, j["note"] or 0))
                    out[(u, slot)] = best
                    utilises.add(best["id"])
    return out


def lineup_jeu(corps, joueurs):
    """{(ligne, poste): nom} de la lineup A exportée ; None si l'export est vide ou absent."""
    if not corps:
        return None
    a = next((l for l in corps if l.get("id") == "A"), None)
    if not a or not any(a.get("lines", {}).values()):
        return None
    noms = {j["id"]: j["nom"] for j in joueurs}
    res = {(ligne, poste): noms.get(pid, f"joueur hors roster ({pid[:8]})") for ligne, s in a["lines"].items() for poste, pid in s.items()}
    res["gameplan"] = a.get("gameplan")
    return res


def prochain(cal_bodies, team_id, maintenant):
    """(datetime UTC du coup d'envoi, adversaire, type) du prochain match de l'équipe, ou None."""
    vus = []
    for b in cal_bodies:
        for g in _json(b) if isinstance(_json(b), list) else []:
            t = g.get("teams") or {}
            ids = {(t.get("home") or {}).get("id"), (t.get("away") or {}).get("id")}
            if team_id in ids and g.get("status") == "upcoming":
                quand = me._dt(g["scheduledAt"])
                if quand > maintenant:
                    autre = t["away"] if (t.get("home") or {}).get("id") == team_id else t["home"]
                    vus.append((quand, f"{autre.get('city', '')} {autre.get('nickname', '')}".strip(), g.get("type")))
    return min(vus) if vus else None


def paris(d):
    try:
        from zoneinfo import ZoneInfo
        return d.astimezone(ZoneInfo("Europe/Paris"))
    except Exception:  # noqa: BLE001 - tzdata absent : heure d'hiver
        return d.astimezone(dt.timezone(dt.timedelta(hours=1)))


def raison_ligne(j, ligne, poste):
    seuil_nom = ("D1" if ligne == "L1" else "D2" if ligne == "L2" else None) if poste in ("LD", "RD") else (ligne if ligne in ("L1", "L2") else None)
    end = c(j, "END")
    txt = f"note {j['note']}, END {end}" + (f" (seuil {seuil_nom} {SEUIL_END[seuil_nom]}+, toléré à −1)" if seuil_nom else "")
    if j["amateur"]:
        txt += " ; amateur (−5 % pour l'équipe) : aucun joueur noté à ce poste"
    if seuil_nom and end < SEUIL_END[seuil_nom] - TOLERANCE:
        txt += " ; sous le seuil : condition plus vite perdue, garder s'il reste le meilleur du poste"
    return txt


def confiance_ligne(j, ligne, poste):
    seuil_nom = ("D1" if ligne == "L1" else "D2" if ligne == "L2" else None) if poste in ("LD", "RD") else (ligne if ligne in ("L1", "L2") else None)
    if j["note"] is None or j["amateur"] or (seuil_nom and c(j, "END") < SEUIL_END[seuil_nom] - TOLERANCE):
        return "faible"
    return "moyenne"


def raison_unite(j, u):
    crit = "PP" if u.startswith("PP") else "PK" if u.startswith("PK") else "4V4" if u.startswith("4V4") else "EXT"
    form = {"PP": "SHO+PAS+SKA", "PK": "DEF+CHK+SKA+PWR", "4V4": "SKA+PAS+SHO", "EXT": "SHO+PAS"}[crit]
    sp = [s for s in j["speciales"] if s in ("powerplay-specialist", "penalty-killer")]
    return f"{form} = {valeur(j, crit)}" + (f" (dont {', '.join(sp)})" if sp else "") + f", END {c(j, 'END')}"


def fiche(eq, roster, lineups_corps, lineups_quand, cal, maintenant, jour, classement=None):
    joueurs = joueurs_de(roster)
    jeu = lineup_jeu(lineups_corps, joueurs)
    ideal = composer(joueurs, {k: v for k, v in (jeu or {}).items() if k != "gameplan"})
    pro = eq == "PRO"
    nx = prochain(cal, ID[eq], maintenant)
    l = [f"# Hockey Nation — fiche tactique {NOM[eq]} du {jour}", ""]
    if pro and classement:  # en tête du plan PRO (consigne du 25/11)
        l += [classement, ""]
    if nx:
        verrou = nx[0] - dt.timedelta(hours=1)
        l.append(f"Prochain match : **{paris(nx[0]):%d/%m/%Y %H:%M} (heure de Paris)**, {nx[2]}, contre {nx[1]}. "
                 f"Verrouillage : **{paris(verrou):%d/%m/%Y %H:%M}** (lignes prises en compte au moins 1 h avant, sinon −30 % ; skill hockeynation-match-calendrier).")
    else:
        l.append("Prochain match : inconnu (aucune page de calendrier de l'équipe exportée depuis 3 jours).")
    l.append("")
    if jeu is None:
        l.append(f"**Lineups absent ou vide** : la fiche est la composition idéale d'après le roster ({len(joueurs)} joueurs). "
                 f"Exporte {EXPORT_LINEUPS[eq]} pour que la colonne « dans le jeu » soit remplie.")
        if eq == "ISL21":
            l.append("L'équipe est marquée gérée par l'IA (`bot: true`) dans l'export de l'équipe nationale : je ne sais pas si l'écran te laisse saisir ses lignes.")
        l.append("")
    else:
        l.append(f"Lineup A lue dans l'export Lineups du {paris(me._dt(lineups_quand)):%d/%m %H:%M}. 🔁 = case à changer.")
        l.append("")
    if pro:
        l.append("PRO : seuls changent les réglages que le registre du Match Engine soutient (infériorité : confirmé sur 268 équipes-matchs) ; "
                 "lignes, jeu de puissance, 4 contre 4 et plan de jeu gardent la saisie du jeu (aucune règle du registre ne soutient de changement ; "
                 "durée des présences courte : aucun effet décelable, on garde).")
        l.append("")
    l += ["| poste | dans le jeu aujourd'hui | à saisir | raison en une phrase | confiance |", "|---|---|---|---|---|"]

    def rang(ligne, poste, j_ideal, raison, conf, garder_jeu=False):
        actuel = jeu.get((ligne, poste)) if jeu else None
        if garder_jeu and actuel:
            a_saisir, raison, conf = actuel, "garder : le registre ne soutient aucun changement de cette case", "moyenne"
        else:
            a_saisir = j_ideal["nom"] if j_ideal else "case vide (aucun joueur du poste)"
        change = (actuel or "") != a_saisir
        marque = "🔁 " if change and jeu is not None else ""
        l.append(f"| {marque}{ligne} {poste} | {actuel or ('—' if jeu is not None else 'inconnu')} | {a_saisir} | {raison} | {conf} |")

    l += ["| **Gardiens** | | | | |"]
    for poste, lib in (("SG", "titulaire"), ("BG", "remplaçant")):
        j = ideal.get(("G", poste))
        r = f"note {j['note']}, END {c(j, 'END')}" + (", fatigué (ne peut pas débuter)" if j and j["fatigue_bloque"] else "") if j else "aucun gardien"
        rang("G", f"{poste} ({lib})", j, r, "moyenne") if False else None
        actuel = jeu.get(("G", poste)) if jeu else None
        a_saisir = actuel if (pro and actuel) else (j["nom"] if j else "case vide")
        raison = "garder : le registre ne soutient aucun changement de cette case" if pro and actuel else r
        marque = "🔁 " if jeu is not None and (actuel or "") != a_saisir else ""
        l.append(f"| {marque}G {lib} | {actuel or ('—' if jeu is not None else 'inconnu')} | {a_saisir} | {raison} | moyenne |")
    for ligne in ("L1", "L2", "L3", "L4"):
        l.append(f"| **Ligne {ligne[1]} (attaque{' + paire D' if ligne != 'L4' else ''})** | | | | |")
        for poste in ("LW", "C", "RW") + (("LD", "RD") if ligne != "L4" else ()):
            j = ideal.get((ligne, poste))
            rang(ligne, poste, j, raison_ligne(j, ligne, poste) if j else "aucun joueur du poste", confiance_ligne(j, ligne, poste) if j else "faible", garder_jeu=pro)
    for u, slots in UNITES:
        l.append(f"| **{LIBELLE_UNITE[u].capitalize()}** | | | | |")
        for s in slots:
            j = ideal.get((u, s))
            garder = pro and not u.startswith("PK")
            conf = "faible" if j and c(j, "END") <= 3 else "moyenne"
            rang(u, s, j, raison_unite(j, u) if j else "aucun joueur", conf, garder_jeu=garder)
    # Rôles (automatiques ou cachés) et réglages d'équipe
    l.append("| **Rôles** | | | | |")
    fof = sorted([j for j in joueurs if not j["goalie"] and j["note"] is not None], key=lambda j: c(j, "FOF"), reverse=True)[:2]
    sho = sorted([j for j in joueurs if not j["goalie"] and j["note"] is not None], key=lambda j: c(j, "SHO"), reverse=True)[:3]
    liste = lambda js, k: ", ".join("%s %s %s" % (j["nom"], k, c(j, k)) for j in js)  # noqa: E731 (f-string imbriqué refusé avant 3.12)
    l.append(f"| mises au jeu | automatique | rien à saisir ({liste(fof, 'FOF')}) | le jeu prend les 2 attaquants au meilleur FOF sur la glace (02-lignes-pro) | solide |")
    l.append(f"| tirs au but | automatique | rien à saisir ({liste(sho, 'SHO')}) | le jeu prend les meilleurs tireurs (02-lignes-pro) | solide |")
    l.append("| capitaine et assistants | caché | rien à saisir | expérience et leadership caché, non lisibles dans l'export (resume.md) | — |")
    l.append("| **Réglages d'équipe (plan de jeu, lineup A)** | | | | |")
    gp = (jeu or {}).get("gameplan") or {}
    for k, (lib, val) in PLAN.items():
        actuel = gp.get(k)
        act_txt = val[actuel] if isinstance(actuel, int) and 0 <= actuel < len(val) else ("—" if jeu is not None else "inconnu")
        cible = actuel if actuel is not None else 1
        raison = ("garder : le test du registre ne montre aucun effet décelable (arrêts 89,8 % en court contre 88,6 % en référence)"
                  if k == "shiftLength" and pro else "garder la valeur du jeu : aucune règle du registre ne porte sur ce réglage"
                  if actuel is not None else "valeur médiane : aucune règle du registre ne porte sur ce réglage")
        l.append(f"| {lib} | {act_txt} | {val[cible]} | {raison} | {'moyenne' if k == 'shiftLength' and pro else 'faible'} |")
    l += ["", "Lineups B et C : copie de la lineup A. Un joueur n'apparaît qu'une fois par type (jeu de puissance, infériorité à 4, "
          "infériorité à 3, 4 contre 4). Poids exacts des compétences dans les unités spéciales : non publiés (formules sourcées en tête du script "
          "`pipelines/fiche_tactique_hockeynation.py`)."]
    return "\n".join(l), ideal, jeu


Q_CLASSEMENT = """select captured_at, body from silver.hn_api where route = '/league/:id/standings' and body::text like '%{id}%'
 order by captured_at desc limit 1"""
MATCHS_SAISON = 30  # 30 matchs de ligue ; top 4 de chaque conférence en playoffs (skill hockeynation-match-calendrier, 01-competitions)
PLACES_PLAYOFFS = 4


def en_tete_classement(corps, quand, team_id):
    """Ligne « rang, points, matchs restants, écart à la ligne des playoffs » de la conférence de l'équipe."""
    for g in (corps or {}).get("groups", []):
        e = g["standing"]["entries"]
        moi = next((x for x in e if x["id"] == team_id), None)
        if not moi:
            continue
        ligne = sorted(e, key=lambda x: x["pos"])[PLACES_PLAYOFFS - 1]
        ecart = moi["pts"] - ligne["pts"]
        noms = {t["id"]: f"{t.get('city', '')} {t.get('nickname', '')}".strip() for t in corps.get("teams", [])}
        pos_txt = f"{moi['pos']}e de la conférence {g['title']}"
        cible = (f"{-ecart} point(s) derrière la 4e place ({noms.get(ligne['id'])}, {ligne['pts']} pts, {ligne['gp']} matchs)"
                 if ecart < 0 else f"{ecart} point(s) d'avance sur la 5e place" if moi["pos"] <= PLACES_PLAYOFFS else
                 f"à égalité de points avec la 4e place ({noms.get(ligne['id'])})")
        return (f"**Classement (relevé du {paris(me._dt(quand)):%d/%m %H:%M})** : {pos_txt}, {moi['pts']} points "
                f"({moi['won']} V, {moi['lost']} D, {moi['ot']} prol.), {moi['gp']} matchs joués, {MATCHS_SAISON - moi['gp']} restants ; "
                f"ligne des playoffs (top {PLACES_PLAYOFFS}) : {cible}.")
    return "Classement : non lu (aucun export de classement de la ligue contenant l'équipe)."


def lire(eq):
    tid = ID[eq]
    cols, r = sqlmod.executer(Q_ROSTER.format(id=tid))
    roster = _json(r[0][0]) if r else {"players": []}
    cols, r = sqlmod.executer(Q_LINEUPS.format(id=tid))
    lu, quand = (_json(r[0][1]), r[0][0]) if r else (None, None)
    cols, r = sqlmod.executer(Q_CAL.format(id=tid))
    return roster, lu, quand, [x[0] for x in r]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("equipe", choices=list(FICHIER))
    ap.add_argument("--jour")
    ap.add_argument("--ecrire", action="store_true")
    a = ap.parse_args()
    jour = a.jour or dt.date.today().isoformat()
    roster, lu, quand, cal = lire(a.equipe)
    classement = None
    if a.equipe == "PRO":
        cols, r = sqlmod.executer(Q_CLASSEMENT.format(id=ID["PRO"]))
        classement = en_tete_classement(_json(r[0][1]), r[0][0], ID["PRO"]) if r else en_tete_classement(None, None, ID["PRO"])
    txt, _, _ = fiche(a.equipe, roster, lu, quand, cal, dt.datetime.now(dt.timezone.utc), jour, classement)
    sys.stdout.reconfigure(encoding="utf-8")
    print(txt)
    if a.ecrire:
        f = BRIEFS / f"{jour}-tactique-{FICHIER[a.equipe]}.md"
        f.write_text(txt + "\n", encoding="utf-8")
        print(f"\nÉcrit : {f.relative_to(RACINE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
