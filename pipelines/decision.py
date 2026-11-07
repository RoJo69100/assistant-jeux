"""Journal de décisions (refonte v2, étape 3.2) : un conseil = une ligne de learn.decision.

Une décision sans prédiction mesurable est refusée (attentes A-7, R-8).
Prédictions acceptées (JSON) :
  {"metric": "my_result", "fenetre_matchs": 3, "attendu": "W>=2"}
      sur les N prochains matchs de l'équipe (hors amicaux) ; attendu = W|D|L suivi de >=, <= ou = et d'un entier ≤ N
  {"metric": "sql", "requete": "select …", "attendu": ">= 10"}
      une requête de lecture qui rend une seule valeur numérique ; attendu = opérateur (>=, <=, >, <, =) et nombre
La charte du club validée (core.club_strategy) est copiée dans strategy_snapshot.

Usage :
  python -I pipelines/decision.py new <jeu> <domaine> --label … --hypothese … --prediction '<json>'
                                       --evaluer-le AAAA-MM-JJ [--equipe ID] [--preuve '<json liste>']
                                       [--lecon L-nnn] [--sujet NOM]   (refus si la leçon est retirée)
  python -I pipelines/decision.py statut <id> accepted|rejected|done|expired [--note …]
  python -I pipelines/decision.py liste [<jeu>]
"""

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python -I n'ajoute pas le dossier du script
from sql import (DEBUT_OK, ECRITURE, auth_refusee, executer, marquer_pg_refuse, rpc_post,  # noqa: E402
                 transport, url_ro)

DOMAINES = ("composition", "tactique", "entrainement", "academie", "achat", "vente",
            "finances", "infrastructure", "personnel")
STATUTS = ("accepted", "rejected", "done", "expired")
ATTENDU_RESULTAT = re.compile(r"^([WDL])(>=|<=|=)(\d+)$")
ATTENDU_VALEUR = re.compile(r"^(>=|<=|>|<|=)\s*(-?\d+(?:[.,]\d+)?)$")
SCHEMA_PREDICTION = """--prediction : objet JSON, une des deux formes (clés exactes) :
  {"metric": "my_result", "fenetre_matchs": 1, "attendu": "W>=1"}
      N prochains matchs hors amicaux ; attendu = W|D|L, puis >=, <= ou =, puis un entier ≤ N
  {"metric": "sql", "requete": "select count(*) from …", "attendu": ">= 1"}
      lecture (select / with) qui rend une seule valeur ; attendu = >=, <=, >, < ou =, puis un nombre
Guillemets simples dans la requête : sous bash, '"'"'texte'"'"'."""


def valider_prediction(pred: object) -> str | None:
    """Rend None si la prédiction est mesurable, sinon la raison du refus."""
    if not isinstance(pred, dict):
        return "la prédiction doit être un objet JSON"
    metric = pred.get("metric")
    attendu = str(pred.get("attendu", "")).replace(" ", "")
    if metric == "my_result":
        n = pred.get("fenetre_matchs")
        if not isinstance(n, int) or isinstance(n, bool) or n < 1:
            return "fenetre_matchs doit être un entier ≥ 1"
        m = ATTENDU_RESULTAT.match(attendu)
        if not m:
            return "attendu doit être W, D ou L suivi de >=, <= ou = et d'un entier (ex. W>=2)"
        if int(m.group(3)) > n:
            return f"attendu {attendu} impossible sur {n} match(s)"
        return None
    if metric == "sql":
        req = str(pred.get("requete", ""))
        if not DEBUT_OK.match(req) or ECRITURE.search(req):
            return "requete doit être une lecture (select / with), sans écriture"
        if not ATTENDU_VALEUR.match(str(pred.get("attendu", "")).strip()):
            return "attendu doit être un opérateur et un nombre (ex. >= 10)"
        return None
    return "metric doit être my_result ou sql"


def valider_date(texte: str, aujourdhui: dt.date) -> str | None:
    try:
        d = dt.date.fromisoformat(texte)
    except ValueError:
        return "evaluer-le doit être une date AAAA-MM-JJ"
    if d <= aujourdhui:
        return "evaluer-le doit être dans le futur"
    return None


def _connexion():
    import psycopg
    return psycopg.connect(url_ro(), connect_timeout=15)


def _bascule_https(e: Exception) -> bool:
    """Postgres refuse l'authentification : témoin posé et HTTPS forcé pour ce processus (sinon l'erreur remonte)."""
    if not auth_refusee(e):
        return False
    marquer_pg_refuse()
    os.environ["SQL_TRANSPORT"] = "https"
    return True


def cmd_new(a) -> int:
    try:
        pred = json.loads(a.prediction)
    except json.JSONDecodeError as e:
        print(f"❌ prédiction illisible : {e}")
        return 1
    try:
        preuve = json.loads(a.preuve)
    except json.JSONDecodeError as e:
        print(f"❌ preuve illisible : {e}")
        return 1
    erreurs = [x for x in (valider_prediction(pred), valider_date(a.evaluer_le, dt.date.today())) if x]
    if not isinstance(preuve, list):
        erreurs.append("preuve doit être une liste JSON")
    if erreurs:
        print("❌ décision refusée : " + " ; ".join(erreurs))
        if valider_prediction(pred):
            print(SCHEMA_PREDICTION)
        return 1
    if a.lecon:
        a.lecon = a.lecon if ":" in a.lecon else f"{a.jeu}:{a.lecon}"  # ids migrés : <jeu>:L-nnn
    eval_apres = dt.datetime.combine(dt.date.fromisoformat(a.evaluer_le), dt.time(12, 0)).astimezone()
    if transport() == "https":  # cloud : écriture par la fonction public.decision_ecrire (POST, clé de service)
        rep = rpc_post("decision_ecrire", {"p": {"op": "new", "jeu": a.jeu, "equipe": a.equipe, "domaine": a.domaine,
                                                 "label": a.label, "hypothese": a.hypothese, "prediction": pred,
                                                 "eval_after": eval_apres.isoformat(), "preuve": preuve,
                                                 "lecon": a.lecon, "sujet": a.sujet}})
        if not rep.get("ok"):
            print(f"❌ décision refusée : {rep.get('erreur')}")
            return 1
        print(f"✅ décision D-{rep['id']} enregistrée (proposée) ; charte : {'copiée' if rep.get('charte') else 'aucune validée'}")
        _marquer(a)
        return 0
    try:
        return _new_pg(a, pred, preuve, eval_apres)
    except Exception as e:  # noqa: BLE001 - psycopg.OperationalError, importé à la demande
        if not _bascule_https(e):
            raise
        return cmd_new(a)


def _new_pg(a, pred, preuve, eval_apres) -> int:
    with _connexion() as c, c.cursor() as cur:
        if a.lecon:
            cur.execute("select status from learn.lesson where id = %s", (a.lecon,))
            ligne = cur.fetchone()
            if not ligne:
                print(f"❌ décision refusée : leçon {a.lecon} introuvable")
                return 1
            if ligne[0] == "retired":
                print(f"❌ décision refusée : la leçon {a.lecon} est retirée (contredite) — conseil à réécrire (A-7)")
                return 1
        cur.execute("select to_jsonb(s) - 'game' - 'team_id' from core.club_strategy s"
                    " where game = %s and team_id is not distinct from %s and valide_le is not null",
                    (a.jeu, a.equipe))
        ligne = cur.fetchone()
        cur.execute("insert into learn.decision (game, team_id, domain, label, hypothesis, prediction, eval_after,"
                    " evidence, strategy_snapshot, lesson_id, sujet)"
                    " values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning id",
                    (a.jeu, a.equipe, a.domaine, a.label, a.hypothese, json.dumps(pred),
                     eval_apres, json.dumps(preuve), json.dumps(ligne[0]) if ligne else None, a.lecon, a.sujet))
        print(f"✅ décision D-{cur.fetchone()[0]} enregistrée (proposée) ; charte : {'copiée' if ligne else 'aucune validée'}")
    _marquer(a)
    return 0


def _marquer(a) -> None:
    try:  # trace lue par le hook police (H3) quand la commande n'est pas dans la session
        marque(a.jeu, a.domaine).write_text(dt.datetime.now().isoformat(), encoding="utf-8")
    except OSError:
        pass


def marque(jeu: str, domaine: str, jour: dt.date | None = None) -> Path:
    """Fichier témoin d'une décision enregistrée aujourd'hui (hook police, H3)."""
    import tempfile
    return Path(tempfile.gettempdir()) / f"claude-decision-{jeu}-{domaine}-{(jour or dt.date.today()).isoformat()}"


def cmd_statut(a) -> int:
    if transport() == "https":
        rep = rpc_post("decision_ecrire", {"p": {"op": "statut", "id": a.id, "statut": a.statut, "note": a.note}})
        if not rep.get("ok"):
            print(f"❌ décision D-{a.id} introuvable")
            return 1
        print(f"✅ D-{a.id} : {a.statut}")
        return 0
    try:
        with _connexion() as c, c.cursor() as cur:
            cur.execute("update learn.decision set status = %s, user_note = coalesce(%s, user_note) where id = %s",
                        (a.statut, a.note, a.id))
            if cur.rowcount != 1:
                print(f"❌ décision D-{a.id} introuvable")
                return 1
    except Exception as e:  # noqa: BLE001
        if not _bascule_https(e):
            raise
        return cmd_statut(a)
    print(f"✅ D-{a.id} : {a.statut}")
    return 0


def cmd_liste(a) -> int:
    _, lignes = executer("select id, game, domain, status, eval_after::date, label from learn.decision"
                         " where %s::text is null or game = %s order by id desc limit 30", (a.jeu, a.jeu))
    for i, jeu, dom, st, ev, label in lignes:
        print(f"D-{i}\t{jeu}\t{dom}\t{st}\t{ev}\t{label}")
    return 0


def main(argv=None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sp = p.add_subparsers(dest="cmd", required=True)
    n = sp.add_parser("new", epilog=SCHEMA_PREDICTION, formatter_class=argparse.RawDescriptionHelpFormatter)
    n.add_argument("jeu")
    n.add_argument("domaine", choices=DOMAINES)
    n.add_argument("--label", required=True)
    n.add_argument("--hypothese", required=True)
    n.add_argument("--prediction", required=True, help="objet JSON mesurable (schéma ci-dessous)")
    n.add_argument("--evaluer-le", required=True)
    n.add_argument("--equipe")
    n.add_argument("--preuve", default="[]")
    n.add_argument("--lecon", help="leçon L-nnn sur laquelle repose la décision (refus si retirée)")
    n.add_argument("--sujet", help="joueur, cible ou réglage visé (revirements : garde.py)")
    s = sp.add_parser("statut")
    s.add_argument("id", type=int)
    s.add_argument("statut", choices=STATUTS)
    s.add_argument("--note")
    li = sp.add_parser("liste")
    li.add_argument("jeu", nargs="?")
    a = p.parse_args(argv)
    return {"new": cmd_new, "statut": cmd_statut, "liste": cmd_liste}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
