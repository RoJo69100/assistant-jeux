"""Évaluation des décisions échues (refonte v2, étape 3.3).

Lit gold.decisions_a_evaluer, mesure la prédiction, écrit learn.outcome et fait évoluer la leçon liée :
  confirmations ≥ lecon_valider sans contradiction → validated ; ≥ lecon_regle → hard_rule proposée (affichée, non appliquée) ;
  contradictions ≥ lecon_retirer → retired + learn.error ouverte (conseil à réécrire, attentes A-7).
Seuils : core.game_params, game = '_tous'.
Mesures :
  my_result : les N premiers matchs joués (hors amicaux) de l'équipe après la décision ; moins de N → en attente
  sql       : la requête de lecture, une valeur numérique comparée au seuil
Usage : python -I pipelines/evaluer_decisions.py [--essai]   (--essai : mesure et affiche, n'écrit rien)
"""

import argparse
import json
import operator
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from decision import ATTENDU_RESULTAT, ATTENDU_VALEUR  # noqa: E402
from sql import url_ro  # noqa: E402

OPS = {">=": operator.ge, "<=": operator.le, ">": operator.gt, "<": operator.lt, "=": operator.eq}
SEUILS_DEFAUT = {"lecon_valider": 3, "lecon_regle": 5, "lecon_retirer": 2}


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


def mesurer(cur, d: dict) -> tuple[str | None, dict]:
    pred = d["prediction"]
    if pred["metric"] == "my_result":
        n = pred["fenetre_matchs"]
        cur.execute("select my_result from core.fixture where game = %s and team_id is not distinct from %s"
                    " and played and my_result is not null and competition_kind <> 'amical'"
                    " and coalesce(scheduled_at, day::timestamptz) > %s"
                    " order by coalesce(scheduled_at, day::timestamptz) limit %s",
                    (d["game"], d["team_id"], d["decided_at"], n))
        res = [r[0] for r in cur.fetchall()]
        if len(res) < n:
            return None, {"matchs": res, "attendus": n}
        return verdict_resultats(res, pred["attendu"]), {"matchs": res}
    cur.execute(pred["requete"])
    ligne = cur.fetchone()
    valeur = next(iter(ligne.values())) if ligne else None  # curseur en dict_row
    return verdict_valeur(valeur, pred["attendu"]), {"valeur": None if valeur is None else float(valeur)}


def main(argv=None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    a = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    a.add_argument("--essai", action="store_true")
    args = a.parse_args(argv)
    import psycopg
    from psycopg.rows import dict_row

    with psycopg.connect(url_ro(), connect_timeout=15, row_factory=dict_row) as c, c.cursor() as cur:
        cur.execute("select key, value::text::int as v from core.game_params where game = '_tous' and key like 'lecon_%'")
        seuils = {**SEUILS_DEFAUT, **{r["key"]: r["v"] for r in cur.fetchall()}}
        cur.execute("select * from gold.decisions_a_evaluer order by id")
        decisions = cur.fetchall()
        for d in decisions:
            verdict, observe = mesurer(cur, d)
            if verdict is None:
                print(f"⏳ D-{d['id']} en attente : {observe}")
                continue
            print(f"{'✅' if verdict == 'confirmed' else '❌' if verdict == 'contradicted' else '⚪'} D-{d['id']} {verdict} {observe}")
            if args.essai:
                continue
            cur.execute("insert into learn.outcome (decision_id, observed, verdict) values (%s, %s, %s)",
                        (d["id"], json.dumps(observe), verdict))
            if not d["lesson_id"] or verdict == "inconclusive":
                continue
            cur.execute("select * from learn.lesson where id = %s", (d["lesson_id"],))
            l = cur.fetchone()
            if not l:
                print(f"  ⚠️ leçon {d['lesson_id']} introuvable")
                continue
            n_for = l["n_for"] + (verdict == "confirmed")
            n_against = l["n_against"] + (verdict == "contradicted")
            statut, message = statut_lecon(l["status"], n_for, n_against, seuils)
            cur.execute("update learn.lesson set n_for = %s, n_against = %s, status = %s,"
                        " promoted_at = case when %s <> status then now() else promoted_at end,"
                        " source_decisions = array_append(source_decisions, %s) where id = %s",
                        (n_for, n_against, statut, statut, d["id"], l["id"]))
            if message:
                print(f"  → {l['id']} : {message}")
            if statut == "retired" and l["status"] != "retired":
                cur.execute("insert into learn.error (game, description, recurrence, enforcement, guard_ref)"
                            " values (%s, %s, %s, 'sql', 'garde.py : leçon retirée bloquée')",
                            (l["game"], f"Leçon {l['id']} contredite {n_against} fois : {l['claim']}", n_against))
        if not decisions:
            print("Aucune décision à évaluer.")
        if args.essai:
            c.rollback()
    return 0


if __name__ == "__main__":
    sys.exit(main())
