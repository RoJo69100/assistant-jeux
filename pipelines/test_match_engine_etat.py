"""Test de pipelines/match_engine_etat.py sur un jeu d'essai figé (sans connexion à la base).

Lancer : python -I pipelines/test_match_engine_etat.py   (code 1 si un cas se trompe)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import match_engine_etat as me  # noqa: E402


def match(i, res, bn, bo, tn=30, te=30, ppn=2, ppe=2, ppgn=0, ppge=0, jour="2026-09-01", type_="League", niveau="PRO"):
    return {"game_id": f"g{i}", "team_level": niveau, "game_type": type_, "jour": jour, "my_result": res, "bn": bn, "bo": bo,
            "tn": tn, "te": te, "xn": 3.0, "xe": 2.0, "gvn": 8, "ppn": ppn, "ppe": ppe, "ppgn": ppgn, "ppge": ppge, "shge": 0,
            "fow": 20, "fol": 10, "s12": 20, "g12": 1, "s3": 10, "g3": 3, "capitaine": "Seppälä"}


# 4 défaites (nous 3/30 = 10 %, eux 6/30 = 20 %) et 2 victoires, dont un match sans ppAttempts adverse.
MS = [match(i, "L", 3, 6, ppge=1) for i in range(4)] + [match(10, "W", 5, 2), match(11, "W", 4, 1, ppe=None)]
GARDIENS = [{"game_id": f"g{i}", "nom": "Kovalev", "toi": 3600, "arrets": 24, "tirs": 30, "buts": 6} for i in range(4)] + \
           [{"game_id": "g10", "nom": "Kovalev", "toi": 3600, "arrets": 28, "tirs": 30, "buts": 2}]
JOUEURS = [{"nom": "Conte", "res": "L", "n": 4, "buts": 0, "tirs": 20, "diff": -2, "pim": 4},
           {"nom": "Conte", "res": "W", "n": 2, "buts": 4, "tirs": 20, "diff": 6, "pim": 0},
           {"nom": "Spinka", "res": "L", "n": 4, "buts": 1, "tirs": 20, "diff": 0, "pim": 0}]
DSC = {"Gordon Conte": 3, "Perry Spinka": 8}


def par_regle(lignes):
    return {l["regle"].split(" ")[0]: l for l in lignes}


def cas():
    r = par_regle(me.evaluer(MS, GARDIENS, JOUEURS, DSC))
    l1 = r["L-001"]
    yield "L-001 : 4 défaites, toutes moins réalistes que l'adversaire", (l1["n"], l1["pour"], l1["contre"]) == (4, 4, 0)
    yield "confiance faible sous la moitié de n requis (4 sur 10)", l1["confiance"] == "faible"
    yield "L-001 : taux comparés, intervalles qui se chevauchent = indéterminé", l1["verdict"].startswith("indéterminé : n trop petit (IC95")
    l6 = r["L-006"]
    yield "L-006 : un match sans ppAttempts est écarté, pas compté 0", "1 match(s) écarté(s)" in l6["mesure"]
    yield "L-002 : 24/30 = .800 sous .870 dans 4 défaites sur 4", (r["L-002"]["pour"], r["L-002"]["contre"]) == (4, 0)
    yield "L-008 : DSC lu par nom de famille (Conte 3, Spinka 8)", "(1 joueurs)" in r["L-008"]["mesure"]
    yield "L-011 : descriptif, jamais de verdict", r["L-011"]["verdict"].startswith("descriptif")
    yield "L-005 : une branche non lue, verdict partiel", r["L-005"]["verdict"].startswith("partiel")


def wilson():
    yield "Wilson : 6 buts sur 26 supériorités contre le seuil PP = indéterminé", me.v_seuil(6, 26, me.SEUIL_PP, "au-dessus").startswith("indéterminé : n trop petit (IC95")
    yield "Wilson : 6 sur 26 contre 23 % = indéterminé aussi", me.v_seuil(6, 26, 0.23, "au-dessus").startswith("indéterminé")
    yield "Wilson : 60 sur 100 contre 20,7 % = confirmé", me.v_seuil(60, 100, me.SEUIL_PP, "au-dessus") == "confirmé"
    yield "Wilson : 5 sur 100 contre 20,7 % = infirmé", me.v_seuil(5, 100, me.SEUIL_PP, "au-dessus") == "infirmé"
    yield "Wilson : arrêts 800 sur 1000 sous .870 = confirmé", me.v_seuil(800, 1000, 0.87, "sous") == "confirmé"
    yield "écart : 10 % contre 40 % sur 100 = confirmé", me.v_ecart((10, 100), (40, 100)) == "confirmé"
    yield "écart : sens inverse = infirmé", me.v_ecart((40, 100), (10, 100)) == "infirmé"
    yield "écart : « sans écart » jamais confirmé par un chevauchement", me.v_ecart((10, 20), (11, 20), "sans_ecart").startswith("indéterminé")
    yield "un seul seuil PP, avec sa source", me.SEUILS["pp"][0] == 0.207 and "L-006" in me.SEUILS["pp"][1]


def retraites():
    carte = "| L-009 | Capitaine | 2026-11-02 | infirmé S26 | ⛔ retirée — ne plus appliquer |\n| L-004 | FOF | x | y | ✅ validée |"
    yield "retirées : L-009 lue dans la carte (⛔)", me.retirees([carte]) == {"L-009"}
    yield "retirées : « retirée » dans une table d'enseignements", me.retirees(["| L-012 | x | y | retirée | z |"]) == {"L-012"}
    yield "retirées : une phrase hors tableau ne compte pas", me.retirees(["Le capitaine L-009 est retirée du texte"]) == set()
    ms = MS
    avec = me.rapport(ms, GARDIENS, JOUEURS, DSC)
    sans = me.rapport(ms, GARDIENS, JOUEURS, DSC, retirees={"L-009"})
    yield "règle retirée : L-009 mesurée sans le filtre", "L-009 capitaine" in avec
    yield "règle retirée : L-009 ni mesurée ni affichée avec le filtre", "L-009" not in sans


def glace():
    vide = me.temps_de_glace([], {"jours": 1, "premier": "2026-11-06", "dernier": "2026-11-06"})
    yield "temps de glace : sans lineup, une seule ligne non mesurable", len(vide) == 1 and vide[0].startswith("non mesurable : il manque la lineup en vigueur")
    lignes = me.temps_de_glace([{"game_id": "g1", "jour": "2026-11-04", "line": x, "toi": s, "joueurs": 5}
                                for x, s in (("L1", 1200), ("L2", 905), ("L3", 700), ("L4", 300))], {"jours": 3, "premier": "a", "dernier": "b"})
    yield "temps de glace : une ligne par match, m:ss", any("| 2026-11-04 | 20:00 | 15:05 | 11:40 | 5:00 |" == l for l in lignes)


def seuils():
    yield "confiance : 4/10 faible", me.confiance(4, 10) == "faible"
    yield "confiance : 5/10 moyenne", me.confiance(5, 10) == "moyenne"
    yield "confiance : 10/10 solide", me.confiance(10, 10) == "solide"
    yield "verdict : jamais confirmé sous solide", me.verdict(9, 1, "moyenne") == "à surveiller (penche pour)"
    yield "verdict : confirmé en solide", me.verdict(9, 1, "solide") == "confirmé"
    yield "verdict : infirmé en solide", me.verdict(1, 9, "solide") == "infirmé"
    yield "verdict : égalité indécise", me.verdict(3, 3, "solide") == "indécis"
    yield "verdict : zéro match", me.verdict(0, 0, "faible") == "aucun match"


def rapport():
    txt = me.rapport(MS + [match(20, "L", 1, 2, niveau="FRM", jour="2026-11-02")], GARDIENS, JOUEURS, DSC)
    yield "rapport : équipes non PRO marquées expérience sans notre choix", "expérience sans notre choix" in txt
    yield "rapport : non mesurable écrit avec ce qui manque", "non mesurable : il manque l'heure de saisie par match" in txt
    nm = [l.split(" | ") for l in txt.splitlines() if "non mesurable" in l]
    yield "rapport : aucune ligne non mesurable chiffrée", bool(nm) and all(set(c[1:7]) <= {"—"} for c in nm)
    yield "rapport : pas de ligne à zéro match hors PRO", not any("expérience" in l and "aucun match" in l for l in txt.splitlines())


def tous_les_matchs():
    """25/11 : registre sur tous les matchs (deux observations par match, autres clubs inclus) et test shift length."""
    import yaml
    y = yaml.safe_load((Path(__file__).resolve().parent.parent / "docs/attentes/jeux/hockeynation.yaml").read_text(encoding="utf-8"))
    yield "EQUIPES_ID couvre les équipes du yaml", set(me.EQUIPES_ID.values()) == {e["id"] for e in y["equipes"]}
    yield "ids du yaml = EQUIPES_ID (équipes hors club)", all(me.EQUIPES_ID.get(e["game_id"]) == e["id"] for e in y["equipes"] if e.get("game_id"))
    yield "Q_TOUS lit les deux côtés sans filtre « à nous »", "cross join (values ('home', 'away'), ('away', 'home'))" in me.Q_TOUS and "is_mine or" not in me.Q_TOUS_M
    tous = [dict(m, game_id=f"t{i}/home", team_level="autres clubs", game_type="Tournament") for i, m in enumerate(MS)]
    txt = me.rapport(MS, GARDIENS, JOUEURS, DSC, tous=tous, gardiens_tous=[])
    yield "rapport : ligne « tous les matchs » avec autres clubs", "tous les matchs (6 matchs, 6 équipes-matchs, autres clubs inclus)" in txt
    yield "rapport : plus de regroupement FRM+U21+U17 quand tous est fourni", "FRM+U21+U17" not in txt
    r = par_regle(me.evaluer(tous, [], [], {}, complet=False, tous_types=True, propres=False))
    yield "tous_types : un match de tournoi compte", r["L-001"]["n"] == 4
    yield "propres=False : ni PP de la saison ni Kovalev", not ({"L-019", "L-016", "L-018", "L-017"} & set(r))
    rel = [("2026-10-23T10:00:00+00:00", 1), ("2026-10-31T10:00:00+00:00", 0), ("2026-11-25T10:00:00+00:00", 0)]
    yield "réglage fixé : encadré par deux relevés égaux", me.reglage_fixe("2026-11-10T18:00:00+00:00", rel) == 0
    yield "réglage non prouvé : relevés différents autour", me.reglage_fixe("2026-10-28T18:00:00+00:00", rel) is None
    yield "réglage non prouvé : avant le premier relevé", me.reglage_fixe("2026-09-01T18:00:00+00:00", rel) is None
    pm = [{"scheduled_at": f"2026-11-{j:02d}T18:00:00+00:00", "bo": 3, "te": 30, "xe": 3.0} for j in range(1, 21)] + \
         [{"scheduled_at": f"2026-09-{j:02d}T18:00:00+00:00", "bo": 3, "te": 30, "xe": 3.0} for j in range(1, 11)]
    t = "\n".join(me.test_shift(rel, pm))
    yield "test shift : 20 matchs court prouvés", "| court | 20 |" in t
    yield "test shift : référence d'avant le premier relevé marquée NON prouvée", "référence NON prouvée" in t and "| 10 |" in t
    yield "test shift : sans groupe normal prouvé, verdict indéterminé", "Verdict : indéterminé : un des deux réglages" in t
    yield "poisson_ic : 64 buts en 20 matchs", tuple(round(x, 2) for x in me.poisson_ic(64, 20)) == (3.2, 2.42, 3.98)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    echecs = total = 0
    for groupe in (cas, wilson, retraites, glace, seuils, rapport, tous_les_matchs):
        for nom, ok in groupe():
            total += 1
            echecs += not ok
            print(("OK " if ok else "ECHEC "), nom)
    print(f"{total - echecs}/{total}")
    sys.exit(1 if echecs else 0)
