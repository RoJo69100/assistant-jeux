"""Test du palier 5 de la revue hebdo BasketVibe : « adversaire plus fort » prédit-il le résultat de ligue ? (lot L3c)

Critères fixés avant le calcul (docs/refonte-v3/journal.md, section L3c) : E = 0,3 point par match, au moins 20 matchs
avec un classement antérieur, part de prédictions justes (hors équivalent) au moins 10 points au-dessus de la base
naïve « toujours victoire ». Force = points marqués / (victoires + défaites) au dernier relevé de
silver.bv_standings_weekly STRICTEMENT antérieur au match. Lecture seule (executer() de sql.py).

Usage : python -I pipelines/palier5_test.py
"""
import importlib.util
import sys
from pathlib import Path

E = 0.3
MIN_MATCHS = 20
MARGE_REQUISE = 0.10  # 10 points de pourcentage au-dessus de la base naïve

SQL_MATCHS = ("select match_day, opponent, my_result from gold.bv_match_report "
              "where competition = 'league' and my_result in ('W', 'L') order by match_day")
SQL_CLASSEMENT = ("select team, day, wins, losses, points_for, is_mine, club_strength "
                  "from silver.bv_standings_weekly order by day")


def jour(v) -> str:
    return str(v)[:10]


def ppm(ligne):
    """Points marqués par match, ou None sans match joué."""
    matchs = (ligne["wins"] or 0) + (ligne["losses"] or 0)
    return None if not matchs or ligne["points_for"] is None else ligne["points_for"] / matchs


def dernier_avant(releves, date):
    """Dernier relevé dont le jour est strictement antérieur à `date` (aucune donnée postérieure au match)."""
    avant = [r for r in releves if jour(r["day"]) < jour(date)]
    return max(avant, key=lambda r: jour(r["day"])) if avant else None


def predire(nous, eux, e=E):
    ecart = round(nous - eux, 9)  # arrondi : 100,3 − 100,0 doit valoir 0,3 pile
    if ecart >= e:
        return "W"
    if -ecart >= e:
        return "L"
    return "="


def evaluer(matchs, classement, e=E):
    """(lignes, sans_classement) ; une ligne = dict avec date, adversaire, nous, eux, prediction, reel, issue."""
    par_equipe, moi = {}, []
    for r in classement:
        (moi if r["is_mine"] else par_equipe.setdefault(r["team"], [])).append(r)
    lignes, sans = [], []
    for m in matchs:
        r_nous, r_eux = dernier_avant(moi, m["match_day"]), dernier_avant(par_equipe.get(m["opponent"], []), m["match_day"])
        p_nous, p_eux = (ppm(r_nous) if r_nous else None), (ppm(r_eux) if r_eux else None)
        if p_nous is None or p_eux is None:
            sans.append(m)
            continue
        pred = predire(p_nous, p_eux, e)
        issue = "équivalent" if pred == "=" else ("juste" if pred == m["my_result"] else "faux")
        lignes.append({"date": jour(m["match_day"]), "adversaire": m["opponent"], "nous": p_nous, "eux": p_eux,
                       "prediction": pred, "reel": m["my_result"], "issue": issue})
    return lignes, sans


def bilan(lignes, sans):
    n = len(lignes)
    juste = sum(l["issue"] == "juste" for l in lignes)
    faux = sum(l["issue"] == "faux" for l in lignes)
    equiv = sum(l["issue"] == "équivalent" for l in lignes)
    base = sum(l["reel"] == "W" for l in lignes) / n if n else None
    part = juste / (juste + faux) if juste + faux else None
    if n < MIN_MATCHS:
        verdict = f"non mesurable : {n} match(s) avec classement antérieur, il en faut {MIN_MATCHS}"
    elif part is not None and base is not None and part >= base + MARGE_REQUISE:
        verdict = "utilisable avec confiance faible"
    else:
        verdict = "non utilisable"
    return {"n": n, "sans_classement": len(sans), "juste": juste, "faux": faux, "equivalent": equiv,
            "part_justes": part, "base_naive": base, "verdict": verdict}


def rendre(lignes, b):
    sortie = ["| date | adversaire | nos points/match | les siens | prédiction | résultat réel | |", "|---|---|---|---|---|---|---|"]
    nom = {"W": "victoire", "L": "défaite", "=": "équivalent"}
    for l in lignes:
        sortie.append(f"| {l['date']} | {l['adversaire']} | {l['nous']:.1f} | {l['eux']:.1f} | {nom[l['prediction']]} | "
                      f"{nom[l['reel']]} | {l['issue']} |")
    pct = lambda v: "n/a" if v is None else f"{100 * v:.1f} %"  # noqa: E731
    sortie += ["", f"n (avec classement antérieur) = {b['n']} ; sans classement antérieur = {b['sans_classement']} ; "
               f"justes = {b['juste']}, faux = {b['faux']}, équivalents = {b['equivalent']}",
               f"part de prédictions justes (hors équivalent) = {pct(b['part_justes'])} ; "
               f"base naïve (toujours victoire) = {pct(b['base_naive'])} ; E = {E}",
               f"verdict : {b['verdict']}"]
    return "\n".join(sortie)


def charger_sql():
    spec = importlib.util.spec_from_file_location("sqlmod", Path(__file__).resolve().parent / "sql.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def dicts(res):
    cols, lignes = res
    return [dict(zip(cols, l)) for l in lignes]


def main() -> int:
    executer = charger_sql().executer
    matchs, classement = dicts(executer(SQL_MATCHS)), dicts(executer(SQL_CLASSEMENT))
    lignes, sans = evaluer(matchs, classement)
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"matchs de ligue lus : {len(matchs)} ; relevés de classement lus : {len(classement)}")
    print(rendre(lignes, bilan(lignes, sans)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
