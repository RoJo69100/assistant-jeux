"""Évaluation des décisions échues (refonte v2, étape 3.3 ; HTTPS depuis la refonte v3, étape 5b-2).

Lit gold.decisions_a_evaluer, mesure la prédiction, écrit learn.outcome et fait évoluer la leçon liée :
  confirmations ≥ lecon_valider sans contradiction → validated ; ≥ lecon_regle → hard_rule proposée (affichée, non appliquée) ;
  contradictions ≥ lecon_retirer → retired + learn.error ouverte (conseil à réécrire, attentes A-7).
Seuils : core.game_params, game = '_tous'.
Mesures :
  my_result : les N premiers matchs joués (hors amicaux) de l'équipe après la décision ; moins de N → en attente.
              Un match sans heure (scheduled_at vide) compte si son jour est ≥ la date de Paris de la décision.
  sql       : la requête de lecture, une valeur numérique comparée au seuil ; valeur vide → en attente (jamais « inconclusive »)
Un résultat « inconclusive » ancien est remplacé par le nouveau verdict (sql/learn/005_evaluer_reevaluable.sql).
Transport : lectures par sql.py (HTTPS en cloud) ; écriture par la fonction public.evaluer_ecrire (POST, clé de service),
qui insère le résultat et met à jour la leçon dans une seule transaction (sql/learn/004_evaluer_ecrire_https.sql).
Usage : python -I pipelines/evaluer_decisions.py [--essai]   (--essai : mesure et affiche, n'écrit rien)
"""

import argparse
import datetime as dt
import json
import operator
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
from decision import ATTENDU_RESULTAT, ATTENDU_VALEUR  # noqa: E402
from sql import executer, litteral, rpc_post  # noqa: E402

OPS = {">=": operator.ge, "<=": operator.le, ">": operator.gt, "<": operator.lt, "=": operator.eq}
SEUILS_DEFAUT = {"lecon_valider": 3, "lecon_regle": 5, "lecon_retirer": 2}
PARIS = ZoneInfo("Europe/Paris")


def verdict_resultats(resultats: list[str], attendu: str) -> str:
    """resultats : W/D/L des N matchs de la fenêtre ; attendu : ex. W>=2."""
    m = ATTENDU_RESULTAT.match(attendu.replace(" ", ""))
    lettre, op, n = m.group(1), m.group(2), int(m.group(3))
    return "confirmed" if OPS[op](resultats.count(lettre), n) else "contradicted"


def verdict_valeur(valeur, attendu: str) -> str:
    if valeur is None:
        return "inconclusive"
    m = ATTENDU_VALEUR.match(attendu.strip())
    return "confirmed" if OPS[m.group(1)](float(valeur), float(m.group(2).replace(",", "."))) else "contradicted"


def statut_lecon(statut: str, n_for: int, n_against: int, seuils: dict) -> tuple[str, str | None]:
    """Nouveau statut et message éventuel (proposition de règle dure, retrait)."""
    if statut == "retired":
        return statut, None
    if n_against >= seuils["lecon_retirer"]:
        return "retired", f"{n_against} contradictions : leçon retirée, conseil à réécrire"
    if n_against == 0 and n_for >= seuils["lecon_regle"] and statut != "hard_rule":
        return "validated", f"{n_for} confirmations sans contradiction : règle dure à proposer à l'utilisateur"
    if n_against == 0 and n_for >= seuils["lecon_valider"] and statut == "hypothesis":
        return "validated", f"{n_for} confirmations sans contradiction : leçon validée"
    return statut, None


def instant(v) -> dt.datetime | None:
    """timestamptz lu en Postgres (datetime) ou en HTTPS (chaîne ISO)."""
    if v is None or v == "":
        return None
    return v if isinstance(v, dt.datetime) else dt.datetime.fromisoformat(str(v))


def jour(v) -> dt.date:
    return v if isinstance(v, dt.date) and not isinstance(v, dt.datetime) else dt.date.fromisoformat(str(v)[:10])


def dans_fenetre(jour_match, scheduled_at, decided_at) -> bool:
    """Match postérieur à la décision : heure connue → après decided_at ; heure vide → jour ≥ date de Paris de la décision."""
    decide = instant(decided_at)
    heure = instant(scheduled_at)
    if heure is not None:
        return heure > decide
    return jour(jour_match) >= decide.astimezone(PARIS).date()


def fenetre_resultats(matchs: list[tuple], decided_at, n: int) -> list[str]:
    """matchs : (jour, scheduled_at, my_result) triés ; rend les N premiers résultats de la fenêtre."""
    return [r for j, h, r in matchs if dans_fenetre(j, h, decided_at)][:n]


def charge_ecriture(d: dict, verdict: str, observe: dict, lecon: dict | None, seuils: dict) -> tuple[dict, str | None]:
    """Corps de public.evaluer_ecrire et message éventuel sur la leçon. Sans leçon (ou verdict non concluant) : lecon = null."""
    p = {"decision_id": d["id"], "observed": observe, "verdict": verdict, "lecon": None}
    if not lecon or verdict == "inconclusive":
        return p, None
    n_for = lecon["n_for"] + (verdict == "confirmed")
    n_against = lecon["n_against"] + (verdict == "contradicted")
    statut, message = statut_lecon(lecon["status"], n_for, n_against, seuils)
    erreur = (f"Leçon {lecon['id']} contredite {n_against} fois : {lecon['claim']}"
              if statut == "retired" and lecon["status"] != "retired" else None)
    p["lecon"] = {"id": lecon["id"], "n_for_avant": lecon["n_for"], "n_against_avant": lecon["n_against"],
                  "n_for": n_for, "n_against": n_against, "statut": statut, "erreur": erreur}
    return p, message


def lire(sql: str) -> list[dict]:
    cols, lignes = executer(sql)
    return [dict(zip(cols, l)) for l in lignes]


def json_de(v):
    return json.loads(v) if isinstance(v, str) else v


def mesurer(d: dict) -> tuple[str | None, dict]:
    pred = d["prediction"]
    if pred["metric"] == "my_result":
        n = pred["fenetre_matchs"]
        equipe = "" if d["team_id"] is None else f" and team_id = {litteral(str(d['team_id']))}"
        date_paris = instant(d["decided_at"]).astimezone(PARIS).date().isoformat()
        lignes = lire("select day, scheduled_at, my_result from core.fixture"
                      f" where game = {litteral(d['game'])}{equipe}"
                      " and played and my_result is not null and competition_kind <> 'amical'"
                      f" and day >= {litteral(date_paris)}::date"
                      " order by coalesce(scheduled_at, day::timestamptz), day")
        res = fenetre_resultats([(l["day"], l["scheduled_at"], l["my_result"]) for l in lignes], d["decided_at"], n)
        if len(res) < n:
            return None, {"matchs": res, "attendus": n}
        return verdict_resultats(res, pred["attendu"]), {"matchs": res}
    lignes = lire(pred["requete"])
    valeur = next(iter(lignes[0].values())) if lignes else None
    return issue_valeur(valeur, pred["attendu"], pred["requete"])


def issue_valeur(valeur, attendu: str, requete: str) -> tuple[str | None, dict]:
    """D1 (étape 5b-3) : une valeur vide n'est pas un verdict ; la décision reste en attente avec la donnée qui manque."""
    if valeur is None:
        return None, {"valeur": None, "manque": f"aucune valeur rendue par : {requete}"}
    return verdict_valeur(valeur, attendu), {"valeur": float(valeur)}


def a_ecrire(verdict: str | None) -> bool:
    """Seul un verdict conclusif s'écrit dans learn.outcome (jamais « inconclusive », D1)."""
    return verdict in ("confirmed", "contradicted")


def main(argv=None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    a = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    a.add_argument("--essai", action="store_true")
    args = a.parse_args(argv)
    seuils = {**SEUILS_DEFAUT, **{l["key"]: int(l["v"]) for l in lire(
        "select key, value::text as v from core.game_params where game = '_tous' and key like 'lecon_%'")}}
    decisions = lire("select id, game, team_id, decided_at, prediction, lesson_id from gold.decisions_a_evaluer order by id")
    erreurs = 0
    for d in decisions:
        d["prediction"] = json_de(d["prediction"])
        verdict, observe = mesurer(d)
        if not a_ecrire(verdict):
            print(f"⏳ D-{d['id']} en attente : {observe}")
            continue
        print(f"{'✅' if verdict == 'confirmed' else '❌'} D-{d['id']} {verdict} {observe}")
        lecon = None
        if d["lesson_id"]:
            ls = lire(f"select id, status, n_for, n_against, claim from learn.lesson where id = {litteral(d['lesson_id'])}")
            lecon = ls[0] if ls else None
            if not lecon:
                print(f"  ⚠️ leçon {d['lesson_id']} introuvable : résultat écrit sans leçon")
        p, message = charge_ecriture(d, verdict, observe, lecon, seuils)
        if message:
            print(f"  → {lecon['id']} : {message}")
        if args.essai:
            continue
        rep = rpc_post("evaluer_ecrire", {"p": p})
        if not rep.get("ok"):
            erreurs += 1
            print(f"  ❌ non écrit : {rep.get('erreur')}")
    if not decisions:
        print("Aucune décision à évaluer.")
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
