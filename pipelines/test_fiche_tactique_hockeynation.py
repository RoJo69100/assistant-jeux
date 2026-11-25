"""Test de pipelines/fiche_tactique_hockeynation.py sur un roster d'essai (sans connexion à la base).

Lancer : python -I pipelines/test_fiche_tactique_hockeynation.py   (code 1 si un cas se trompe)
"""
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fiche_tactique_hockeynation as ft  # noqa: E402


def joueur(i, postes, note, end=6, **comp):
    base = {"END": end, "SKA": 5, "PWR": 5, "SHO": 5, "PAS": 5, "DEF": 5, "CHK": 5, "DSC": 5, "FOF": 5}
    base.update(comp)
    return {"id": f"p{i}", "firstname": "J", "lastname": str(i), "positions": postes, "rating": note,
            "skills": [{"id": k, "lvl": v} for k, v in base.items()], "specialSkills": []}


def roster():
    pl, i = [], 0
    for poste, n in (("C", 4), ("LW", 4), ("RW", 4), ("LD", 3), ("RD", 3)):
        for k in range(n):
            pl.append(joueur(i, [poste], 70 - 3 * k, end=8 - k))
            i += 1
    pl[0]["skills"] = [{"id": "END", "lvl": 3}, {"id": "DEF", "lvl": 10}, {"id": "CHK", "lvl": 10}, {"id": "SKA", "lvl": 10}, {"id": "PWR", "lvl": 10}]
    pl.append({**joueur(98, ["G"], 75, end=8), "goalie": True})
    pl.append({**joueur(99, ["G"], 65, end=8), "goalie": True})
    pl.append({**joueur(97, ["C"], 30), "amateur": True})
    return {"players": pl}


def cas():
    js = ft.joueurs_de(roster())
    ideal = ft.composer(js)
    noms = {k: v["nom"] for k, v in ideal.items()}
    yield "gardien titulaire = meilleure note", noms[("G", "SG")] == "J 98"
    yield "chaque joueur de ligne est à un poste listé", all(p in v["postes"] for (l, p), v in ideal.items() if l in ("L1", "L2", "L3", "L4"))
    yield "aucun joueur deux fois dans les lignes", len({v["id"] for (l, _), v in ideal.items() if l in ("L1", "L2", "L3", "L4")}) == \
        len([1 for (l, _) in ideal if l in ("L1", "L2", "L3", "L4")])
    yield "l'amateur ne joue pas quand un joueur noté existe", "J 97" not in {v["nom"] for (l, _), v in ideal.items() if l.startswith("L")}
    for type_, unites in (("PP", ("PP1", "PP2")), ("PK4", ("PK4-1", "PK4-2")), ("PK3", ("PK3-1", "PK3-2")), ("4V4", ("4V4-1", "4V4-2"))):
        ids = [v["id"] for (u, _), v in ideal.items() if u in unites]
        yield f"{type_} : un joueur une seule fois par type", len(ids) == len(set(ids))
    yield "infériorité : le meilleur DEF+CHK+SKA+PWR des avants en PK4-1", noms[("PK4-1", "FW1")] == "J 0"
    # à valeur égale, le joueur en place garde la case
    js2 = [j for j in js]
    en_place = {("PK4-1", "RD"): "J 16"}
    i2 = ft.composer(js2, en_place)
    yield "égalité : le joueur déjà en place reste", i2[("PK4-1", "RD")]["nom"] in ("J 16", "J 15") and \
        (ft.valeur(i2[("PK4-1", "RD")], "PK") > ft.valeur(next(j for j in js2 if j["nom"] == "J 16"), "PK") or i2[("PK4-1", "RD")]["nom"] == "J 16")
    corps = {"teams": [{"id": "a", "city": "A", "nickname": "x"}, {"id": "b", "city": "B", "nickname": "y"}],
             "groups": [{"title": "East", "standing": {"entries": [
                 {"id": f"t{k}", "pos": k + 1, "pts": 40 - 2 * k, "gp": 21, "won": 1, "lost": 1, "ot": 0} for k in range(4)] + [
                 {"id": "moi", "pos": 5, "pts": 33, "gp": 21, "won": 9, "lost": 7, "ot": 5}]}}]}
    t = ft.en_tete_classement(corps, "2026-11-25T12:00:00+00:00", "moi")
    yield "classement : rang, points, matchs restants", "5e de la conférence East, 33 points" in t and "9 restants" in t
    yield "classement : écart à la 4e place", "1 point(s) derrière la 4e place" in t
    cal = [[{"status": "upcoming", "scheduledAt": "2026-11-25T22:30:00.000000Z", "type": "League",
             "teams": {"home": {"id": "x", "city": "Forest Hills", "nickname": "Rangers"}, "away": {"id": ft.ID["PRO"]}}}]]
    nx = ft.prochain(cal, ft.ID["PRO"], dt.datetime(2026, 11, 25, 12, tzinfo=dt.timezone.utc))
    yield "prochain match lu, adversaire nommé", nx and nx[1] == "Forest Hills Rangers"
    txt, _, _ = ft.fiche("HUA", roster(), None, None, [], dt.datetime(2026, 11, 25, 12, tzinfo=dt.timezone.utc), "2026-11-25")
    yield "sans Lineups : dit en tête et nomme la page à exporter", "Lineups absent ou vide" in txt and "Exporte l'onglet Lineups" in txt
    yield "fiche : colonnes demandées", "| poste | dans le jeu aujourd'hui | à saisir | raison en une phrase | confiance |" in txt
    yield "fiche : plus de « rendu figé » ni de lien", "figé" not in txt and "http" not in txt
    yield "fiche : toutes les sections", all(s in txt for s in ("Gardiens", "Ligne 1", "Ligne 4", "Jeu de puissance 2", "Infériorité 2",
                                                               "Infériorité à 3", "4 contre 4", "Gardien retiré", "Rôles", "Réglages d'équipe"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    jeux = list(cas())
    echecs = 0
    for n, ok in jeux:
        echecs += not ok
        print("OK " if ok else "ECHEC ", n)
    print(f"{len(jeux) - echecs}/{len(jeux)}")
    sys.exit(1 if echecs else 0)
