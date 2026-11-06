"""Test de pipelines/aujourdhui_hockeynation.py sur le relevé figé du 2026-11-06 (sans réseau ni base).

Jeu d'essai : pipelines/jeu_essai/hockeynation/2026-11-06/ (8 requêtes du jour, registre, journal des enseignements).
Un cas par critère H1 à H6 de docs/refonte-v3/journal-aujourdhui.md ; les cas « deux matchs sans équipe » et « lineup à
18 cases vides » sont fabriqués ici à partir du relevé (la base du jour n'en contient pas).
Lancer : python -I pipelines/test_aujourdhui_hockeynation.py   (code 1 si un cas se trompe)
"""
import datetime as dt
import json
import re
import sys
from pathlib import Path

DOSSIER = Path(__file__).resolve().parent
sys.path.insert(0, str(DOSSIER))
import aujourdhui_hockeynation as hn  # noqa: E402
import forme  # noqa: E402

JOUR = dt.date(2026, 11, 6)
ESSAI = DOSSIER / "jeu_essai" / "hockeynation" / "2026-11-06"
FAIT = hn.lire_fait(JOUR, base=ESSAI)
LEARNINGS = (ESSAI / "learnings.md").read_text(encoding="utf-8")
DEPUIS = dt.date(2026, 11, 4)


def charger():
    brut = json.loads((ESSAI / "donnees.json").read_text(encoding="utf-8"))
    return {n: (v["cols"], [tuple(r) for r in v["rows"]]) for n, v in brut.items()}


def modifier(d, nom, fonction):
    cols, rows = d[nom]
    lst = [dict(zip(cols, r)) for r in rows]
    fonction(lst)
    d[nom] = (cols, [tuple(x[c] for c in cols) for x in lst])
    return d


def ajoute_divers(d, k, v):
    return modifier(d, "divers", lambda l: l.append({"k": k, "v": json.dumps(v, ensure_ascii=False)}))


def plan(d, fait=None, depuis=DEPUIS):
    return hn.plan_du_jour(d, JOUR, FAIT if fait is None else fait, LEARNINGS, depuis)


def lignes_table(texte, debut):
    """Lignes de données du tableau dont l'en-tête commence par `debut`."""
    out, dans = [], False
    for l in texte.splitlines():
        if l.startswith("| " + debut):
            dans = True
            continue
        if dans and l.startswith("|---"):
            continue
        if dans and l.startswith("|"):
            out.append([c.strip() for c in l.strip("|").split("|")])
        elif dans:
            break
    return out


def h1():
    base = charger()
    a, faire = hn.bloc_exports(base, FAIT, JOUR, hn.lignes(base, "jeux"))
    yield "H1 : tout est à jour, aucun export demandé", a == [] and faire == []
    d = modifier(charger(), "divers", lambda l: [x.update(v=x["v"].replace("🟩 à jour", "🟧 à refaire")) for x in l if x["k"] == "export" and "Roster" in x["v"]])
    a, faire = hn.bloc_exports(d, [], JOUR, hn.lignes(d, "jeux"))
    yield "H1 : Roster à refaire et absent du registre = demandé", faire == ["Roster"] and "Exporte Roster" in a[0][1]
    a, faire = hn.bloc_exports(d, FAIT, JOUR, hn.lignes(d, "jeux"))
    yield "H1 : Roster à refaire mais cité refait dans le registre = jamais redemandé", faire == []
    d = modifier(charger(), "jeux", lambda l: [x for x in l if x["equipe"] == "PRO" and x["my_result"]][-1].update(detail=False))
    a, faire = hn.bloc_exports(d, [], JOUR, hn.lignes(d, "jeux"))
    yield "H1 : page du dernier match PRO absente = demandée", any(f.startswith("page du match PRO") for f in faire)
    a, faire = hn.bloc_exports(d, FAIT, JOUR, hn.lignes(d, "jeux"))
    yield "H1 : l'export des matchs du registre couvre les pages de match", faire == []
    fait_change = FAIT + ["- [23:00 utc] entraînement modifié : nouveaux choix saisis"]
    a, faire = hn.bloc_exports(charger(), fait_change, JOUR, hn.lignes(charger(), "jeux"))
    yield "H1 : Training demandé si son journal est plus vieux que le dernier changement", "Training" in faire
    a, faire = hn.bloc_exports(charger(), FAIT, JOUR, hn.lignes(charger(), "jeux"))
    yield "H1 : Training non demandé sans changement plus récent", "Training" not in faire


def h2():
    d = charger()
    s = hn.bloc_scouts(d, FAIT)
    yield "H2 : une ligne par scout (6)", len(s) == 6 and len({x[0] for x in s}) == 6
    yield "H2 : la cible est sans rapport", all(x[5] == 0 for x in s)

    def uden(l):
        l.append({"scout": "Patrik Táborský", "categorie": "A poste + nation", "rang": 1, "joueur": "Kevin Uden", "poste": "C", "nation": "Netherlands", "rapports": 0})

    d2 = modifier(charger(), "cibles", uden)
    yield "H2 : Uden est la cible quand rien ne le retire", [x for x in hn.bloc_scouts(d2, []) if x[0] == "Patrik Táborský"][0][1].endswith("Kevin Uden")
    ligne = "- [15:25 utc] kevin uden déjà scouté : à retirer des cibles — source : déclaré par l'utilisateur"
    yield "H2 : « déjà scouté » du registre retire la cible", not [x for x in hn.bloc_scouts(d2, [ligne]) if "Uden" in x[1]]
    d3 = ajoute_divers(charger(), "declare", {"name": "Kevin Uden", "detail": "déjà scouté", "kind": "x"})
    d3 = modifier(d3, "cibles", uden)
    yield "H2 : une déclaration en base retire aussi la cible", not [x for x in hn.bloc_scouts(d3, []) if "Uden" in x[1]]


def h3():
    d = charger()
    jeux = hn.lignes(d, "jeux")
    attendu = len([j for j in jeux if j["my_result"] and j["equipe"] in hn.EQUIPES and hn.vers_date(j["scheduled_at"]) > DEPUIS])
    tab, defs, reg, inc = hn.bloc_matchs(d, JOUR, DEPUIS, dt.date(2026, 10, 25))
    yield "H3 : une ligne par match joué des 4 équipes depuis le dernier passage", len(tab) == attendu and attendu >= 4
    yield "H3 : les 4 équipes sont présentes", {r[0].split(" ")[0] for r in tab} >= set(hn.EQUIPES)
    yield "H3 : résultat en mot, jamais le score brut", all(r[2] in ("Victoire", "Défaite") for r in tab) and not any(re.search(r"(?<![\d-])\d{1,2}-\d{1,2}(?![\d-])", " ".join(r[:3])) for r in tab)
    yield "H3 : « mérité ou non » donne le nombre de matchs de la comparaison", all(re.search(r"sur \d+ matchs|indéterminé", r[3]) for r in tab)
    yield "H3 : FRM, U21, U17 marqués « expérience sans notre choix »", all("expérience sans notre choix" in r[0] for r in tab if not r[0].startswith("PRO"))
    yield "H3 : chaque défaite a oui / non / indéterminé et oui / non pour la structure", len(defs) == len([r for r in tab if r[2] == "Défaite"]) and all(
        re.match(r"(oui|non|indéterminé)", x[3]) and re.match(r"(oui|non)", x[4]) for x in defs)
    yield "H3 : un taux indéterminé affiche son intervalle", all("IC95" in x[3] for x in defs if x[3].startswith("indéterminé"))
    # deux matchs sans équipe (jours 10 et 11) : fabriqués en vidant l'équipe de deux matchs PRO réels

    def vide(l):
        for x in l:
            if x["equipe"] == "PRO" and re.search(r"Forest Hills|Helsinki", x["home"] + x["away"]):
                x["equipe"] = None

    def vide_detail(l):
        ids = {j["game_id"] for j in hn.lignes(d2, "jeux") if j["equipe"] is None}
        for x in l:
            if x["game_id"] in ids:
                x["team_level"] = None

    d2 = modifier(charger(), "jeux", vide)
    d2 = modifier(d2, "details", vide_detail)
    tab2, defs2, _, inc2 = hn.bloc_matchs(d2, JOUR, dt.date(2026, 11, 1), dt.date(2026, 10, 25))
    inconnus = [r for r in tab2 if r[0] == "équipe inconnue"]
    yield "H3 : les deux matchs sans équipe sont des lignes « équipe inconnue »", len(inconnus) == 2 and inc2
    yield "H3 : aucun match ignoré quand l'équipe est inconnue", len(tab2) >= len(tab) - 0 and all(r[2] in ("Victoire", "Défaite") for r in inconnus)
    # jugement : oui, non, indéterminé
    m = {"game_id": "x", "my_result": "L", "bn": 0, "tn": 40, "bo": 3, "te": 20, "xn": 3.0, "xe": 1.0}
    gb = (30, 250, 220, 250, 5)  # réalisation moyenne 12 %, arrêts moyens 88 %
    yield "H3 : volume pour nous et réalisation décelablement basse = « oui »", hn.juge_match(m, gb, None)[1].startswith("oui")
    m2 = {"game_id": "y", "my_result": "L", "bn": 1, "tn": 20, "bo": 4, "te": 40, "xn": 1.0, "xe": 3.0}
    yield "H3 : dominé en xG et en tirs = « non »", hn.juge_match(m2, gb, None)[1].startswith("non")
    m3 = {"game_id": "z", "my_result": "L", "bn": 2, "tn": 20, "bo": 3, "te": 20, "xn": 2.0, "xe": 2.5}
    yield "H3 : le reste = « indéterminé » avec l'intervalle", hn.juge_match(m3, gb, None)[1].startswith("indéterminé") and "IC95" in hn.juge_match(m3, gb, None)[1]


def h4():
    d = charger()
    p = plan(d)
    yield "H4 : aucun déclencheur = bloc tactique absent", p["motifs"] == [] and not any(a[1] == "Tactique" for a in p["actions"])

    def vides(l):
        for k in range(18):
            l.append({"k": "case", "v": json.dumps({"lineup": "A", "line": f"L{k}", "slot": "C", "joueur": None, "controle": "vide"})})

    d2 = modifier(charger(), "divers", vides)
    p2 = plan(d2)
    yield "H4 : lineup à 18 cases vides = tactique déclenchée", any("18 case(s)" in m for m in p2["motifs"]) and any(a[1] == "Tactique" for a in p2["actions"])
    d3 = ajoute_divers(charger(), "controle", {"controle": "hors poste", "valeur": 2, "etat": "à corriger"})
    yield "H4 : un joueur hors poste déclenche la tactique", any("hors poste" in m for m in plan(d3)["motifs"])
    ancien = hn.TESTS["pp_pk"]
    hn.TESTS["pp_pk"] = (ancien[0], 4, ancien[2])
    try:
        yield "H4 : un test arrivé à échéance déclenche la tactique", any("test arrivé à échéance" in m for m in plan(charger())["motifs"])
    finally:
        hn.TESTS["pp_pk"] = ancien

    def deux_defaites(l):
        frm = [x for x in l if x["equipe"] == "FRM" and x["game_type"] == "League" and x["my_result"]]
        for x in frm[-2:]:
            x["my_result"] = "L"

    yield "H4 : deux défaites de suite d'une équipe déclenchent la tactique", any("deux défaites de suite" in m for m in plan(modifier(charger(), "jeux", deux_defaites))["motifs"])
    fait = FAIT + ["- [17:00 utc] lineup modifiée : nouveau montage"]
    yield "H4 : lineup exportée plus vieille que le dernier changement = déclenchée", any("plus vieille" in m for m in plan(charger(), fait)["motifs"])
    d4 = modifier(charger(), "divers", lambda l: [x.update(v=json.dumps({"cap_space": -250000, "salary_cap": 57500000})) for x in l if x["k"] == "cap"])
    p4 = plan(d4)
    yield "H4 : plafond négatif = première ligne 🟥, seule alerte hors plan", p4["actions"][0][0] == "🟥 URGENT" and p4["temps1"].split("\n")[2].startswith("| Priorité")


def h5():
    d = charger()
    ent = hn.bloc_entrainement(d)
    yield "H5 : un tableau par équipe, les 4 équipes", all(ent[eq] for eq in hn.EQUIPES)
    yield "H5 : aucune compétence plafonnée proposée", not any("plafonn" in str(c[2]).lower() for eq in ent.values() for c in eq)
    yield "H5 : le joueur sans compétence ouverte est en fin de liste, sans coach", all(c[0] == "fin de liste" and c[3] == "" for eq in ent.values() for c in eq if c[2] == "aucune compétence ouverte")
    ordres = [c[0] for c in ent["PRO"] if isinstance(c[0], int)]
    yield "H5 : l'ordre de choix est croissant", ordres == sorted(ordres) and ordres[0] == 1
    t2 = plan(d)["temps2"]
    yield "H5 : le rendu a un tableau par équipe dans l'ordre PRO, FRM, U21, U17", [t2.find(f"Ordre de choix {eq}") for eq in hn.EQUIPES] == sorted(t2.find(f"Ordre de choix {eq}") for eq in hn.EQUIPES) and -1 not in [t2.find(f"Ordre de choix {eq}") for eq in hn.EQUIPES]


def h6():
    d = charger()
    p = plan(d)
    texte = p["temps1"] + "\n" + p["temps2"]
    yield "H6 : le rendu passe forme.py", forme.fautes_de(texte, "hockeynation") == []
    yield "H6 : aucun code interne (règle, saison, vue)", not re.search(r"\b[LC]-\d{3}\b|\bS2[67]\b|\bgold\.|\bsilver\.|\bhn_", texte)
    yield "H6 : le registre est dit en mots", "réalisation, pas volume" in texte and "L-001" not in texte
    yield "H6 : en_mots retire les codes", hn.en_mots("L-018 Kovalev P3 en S27 / S26") == "Kovalev P3 en saison en cours / saison précédente"
    yield "H6 : Rendu en deux temps, temps 1 se termine par la consigne « actions »", "Dis « actions » pour passer au temps 2." in p["temps1"]
    yield "H6 : dernière ligne = exports à faire aujourd'hui (aucun si tout est à jour)", p["temps1"].splitlines()[-1] == "Exports à faire aujourd'hui : aucun"
    d2 = modifier(charger(), "divers", lambda l: [l.append({"k": "case", "v": json.dumps({"controle": "vide"})}) for _ in range(3)])
    acts = plan(d2)["temps2"].split("Ordre de choix")[0]
    yield "H6 : au plus 5 actions dans le temps 2", len([r for r in lignes_table(acts, "Priorité")]) <= hn.ACTIONS_MAX


def h7():
    yield "H7 : le relevé figé contient les 8 requêtes", set(charger()) == set(hn.REQUETES) and len(hn.REQUETES) <= 8
    yield "H7 : le relevé date du 2026-11-06", (ESSAI / "fait-2026-11-06.md").exists() and (ESSAI / "learnings.md").exists()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    echecs = total = 0
    for groupe in (h1, h2, h3, h4, h5, h6, h7):
        for nom, ok in groupe():
            total += 1
            echecs += not ok
            print(("OK " if ok else "ECHEC "), nom)
    print(f"{total - echecs}/{total}")
    sys.exit(1 if echecs else 0)
