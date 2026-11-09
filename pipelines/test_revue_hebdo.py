"""Tests figés de pipelines/revue_hebdo.py (étape 6a, R2 à R7 et R1) : données factices, aucune base.

Lancer : python -I pipelines/test_revue_hebdo.py   (code 1 si un cas se trompe)
"""
import datetime as dt
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import revue_hebdo as r  # noqa: E402

JOUR = dt.date(2026, 11, 15)  # dimanche
LUNDI = dt.date(2026, 11, 9)


def txt(lignes):
    return "\n".join(lignes)


def cas():
    # R2 : décisions
    v = lambda dom, verdict, req="select opp_fg2_pct from gold.bv_match_report": \
        {"domain": dom, "verdict": verdict, "metric": "sql", "requete": req}
    verdicts = [v("tactique", "contradicted"), v("tactique", "confirmed", "select defense_tier from gold.bv_match_player_lines")] \
        + [v("composition", "contradicted")] * 7 + [v("composition", "confirmed")] * 3
    d = txt(r.sec_decisions(verdicts, [{"id": 1, "domain": "achat"}]))
    yield "R2 présent : composition 7 contredits sur 10 = 70 % (n = 10)", "| composition | 3 | 7 | 0 | 0 | effet 10, exécution 0 | 70 % (n = 10) |" in d
    yield "R2 présent : tactique sous 10 verdicts = n insuffisant, 1 exécution", \
        "| tactique | 1 | 1 | 0 | 0 | effet 1, exécution 1 | n insuffisant (n = 2) |" in d
    yield "R2 présent : décision en attente comptée dans son domaine", "| achat | 0 | 0 | 0 | 1 |" in d
    yield "R2 absent : aucune décision ni verdict = n = 0, pas de tableau", \
        "(n = 0)" in txt(r.sec_decisions([], [])) and "| Domaine" not in txt(r.sec_decisions([], []))
    yield "R2 absent : table illisible = donnée manquante", "donnée manquante" in txt(r.sec_decisions(None, []))

    # R3 : leçons
    L = [{"id": "L-1", "status": "hypothesis", "n_for": 0, "n_against": 2, "derniere_mesure": None},
         {"id": "L-2", "status": "hypothesis", "n_for": 1, "n_against": 0, "derniere_mesure": "2026-11-10T08:00:00"},
         {"id": "L-3", "status": "validated", "n_for": 7, "n_against": 1, "derniere_mesure": None}]
    l = txt(r.sec_lecons(L, JOUR, {"jour": "08/11", "n_against": 1}))
    yield "R3 présent : états comptés (hypothèse 2, validée 1, n = 3)", "hypothèse 2 ; validée 1 (n = 3)" in l
    yield "R3 présent : « contre » ajoutés = 3 − 1 = 2 depuis l'instantané", "depuis l'instantané du 08/11 : 2 (total 3)" in l
    yield "R3 présent : hypothèse bloquée (aucune mesure) listée, la mesurée il y a 5 jours non", \
        "depuis 14 jours : 1 sur 2 (L-1)" in l
    l0 = txt(r.sec_lecons(L, JOUR, None))
    yield "R3 absent : pas d'instantané précédent", "pas d'instantané précédent (total actuel 3)" in l0
    yield "R3 absent : aucune hypothèse bloquée", "depuis 14 jours : 0 sur 1" in txt(r.sec_lecons(L[1:], JOUR, None))

    # R4 : matchs
    M = [{"match_day": "2026-11-10", "competition": "league", "opponent": "A|B", "my_result": "L", "my_pts": 80,
          "opp_pts": 90, "margin": -10},
         {"match_day": "2026-11-11", "competition": "friendly", "opponent": "C", "my_result": "W", "my_pts": 100,
          "opp_pts": 96, "margin": 4}]
    m = txt(r.sec_matchs(M))
    yield "R4 présent : une ligne par match, résultat my_result, « | » échappé", \
        "| 10/11 | league | A\\|B | L | 80-90 | -10 |" in m and "| 11/11 | friendly | C | W | 100-96 | +4 |" in m
    yield "R4 présent : marge moyenne −3,0 (n = 2), compte par compétition", \
        "Marge moyenne : -3,0 (n = 2) ; par compétition : friendly 1 ; league 1" in m
    yield "R4 présent et absent : matchs mal prédits = donnée manquante", \
        "aucune prédiction de marge en base" in m and "aucune prédiction de marge en base" in txt(r.sec_matchs([]))
    yield "R4 absent : 0 match (n = 0)", "0 match exporté cette semaine (n = 0)" in txt(r.sec_matchs([]))

    # R5 : expériences
    X = {"file": [{"id": "E1", "amicaux_vises": 4, "joue": {"A": {"agress_cran": 2}}, "ordre": ["A"]}],
         "faits": [{"id": "E1", "niveau": "A", "cle": {"nom": "Alpha", "date": dt.date(2026, 11, 12), "jour": LUNDI,
                                                         "fichier": "f"}, "jour": LUNDI, "fichier": "f"}],
         "debut": dt.date(2026, 11, 10)}
    J = [{"fixture_id": "f1", "match_day": "2026-11-12", "opponent": "Alpha BC", "agress_cran": 2,
          "primary_quarts": 0, "tir_cran4_joueurs": 0}]
    e = txt(r.sec_experiences(X, J, JOUR))
    yield "R5 présent : E1 1 vérifié sur 4 ; dimanche : étude « non calculé »", \
        "E1 1 vérifié sur 4" in e and "non calculé" in e
    e0 = txt(r.sec_experiences(X, [], LUNDI))
    yield "R5 absent : réglage non exporté = 0 vérifié ; lundi : pas de ligne de l'étude", \
        "E1 0 vérifié sur 4" in e0 and "étude" not in e0
    yield "R5 absent : fichier d'expériences illisible = donnée manquante", "donnée manquante" in txt(r.sec_experiences(None, J, JOUR))

    # S2 (6b) : clé `lecons` du fichier d'expériences réel
    vrai = r.src.lire_experiences(Path(tempfile.gettempdir()) / "aucun-registre", LUNDI)
    lec = {e["id"]: e.get("lecons") for e in vrai["file"]}
    yield "S2 présent : E1 relie L-004, L-008, L-011#2, L-015, L-021 ; E2 relie L-002, L-020, L-025", \
        lec["E1"] == ["L-004", "L-008", "L-011#2", "L-015", "L-021"] and lec["E2"] == ["L-002", "L-020", "L-025"]
    yield "S2 absent : E3 et E4 sans leçon (liste vide, clé présente)", lec["E3"] == [] and lec["E4"] == []

    # S3 (6b) : expériences à conclure
    X4 = {"file": [{"id": "E1", "amicaux_vises": 2, "joue": {"A": {"agress_cran": 2}}, "ordre": ["A"],
                    "lecons": ["L-004", "L-008"]},
                   {"id": "E3", "amicaux_vises": 1, "joue": {}, "ordre": ["A"], "lecons": []}],
          "faits": [{"id": i, "niveau": "A", "cle": {"nom": n, "date": dt.date(2026, 11, d), "jour": LUNDI, "fichier": "f"},
                     "jour": LUNDI, "fichier": "f"} for i, n, d in (("E1", "Alpha", 11), ("E1", "Bravo", 12), ("E3", "Charlie", 13))],
          "debut": dt.date(2026, 11, 10)}
    J4 = [{"fixture_id": f"f{d}", "match_day": f"2026-11-{d}", "opponent": f"{n} BC", "agress_cran": 2,
           "primary_quarts": 0, "tir_cran4_joueurs": 0} for n, d in (("Alpha", 11), ("Bravo", 12), ("Charlie", 13))]
    c = txt(r.sec_a_conclure(X4, J4))
    yield "S3 présent : « verdict à produire : E1, n = 2, leçons L-004, L-008 »", \
        "verdict à produire : E1, n = 2, leçons L-004, L-008" in c
    yield "S3 présent, sans leçon : E3 dit « leçon à créer »", "verdict à produire : E3, n = 1, leçons aucune (leçon à créer" in c
    c0 = txt(r.sec_a_conclure(X4, J4[:1]))
    yield "S3 absent (E1 à 1 sur 2, E3 non exporté) : « aucune expérience à conclure »", \
        "aucune expérience à conclure (0 sur 2" in c0 and "verdict à produire" not in c0
    yield "S3 absent : réglage non conforme (cran 4 au lieu de 2) = pas de verdict pour E1", \
        "E1" not in txt(r.sec_a_conclure(X4, [dict(j, agress_cran=4) for j in J4[:2]]))

    # R6 : données
    d6, n = r.sec_donnees([{"non_lus": 90, "types": 126}], {"jour": "08/11", "non_lus": 93})
    yield "R6 présent : 90 non lus sur 126, écart −3 avec l'instantané", \
        n == 90 and "90 sur 126 ; écart avec l'instantané du 08/11 : -3" in txt(d6)
    yield "R6 absent : pas d'instantané précédent", "pas d'instantané précédent" in txt(r.sec_donnees([{"non_lus": 90, "types": 126}], None)[0])
    yield "R6 absent : vue illisible = donnée manquante", "donnée manquante" in txt(r.sec_donnees(None, None)[0])

    # R7 : paramètres
    PB = ("## X\n### Paramètres écrits à la main (règle 5)\n\n| Paramètre | Valeur | Où |\n|---|---|---|\n"
          "| Âge de déclin | 31 ans | a.py |\n| Poste mince | profondeur ≤ 2 | b.py |\n\n## Étape 6\n| Autre | x | y |\n")
    P = r.lire_parametres(PB)
    yield "R7 lecteur : 2 paramètres, tableau suivant ignoré", [p[0] for p in P] == ["Âge de déclin", "Poste mince"]
    p7 = txt(r.sec_parametres(P, [{"key": "age_declin", "value": 31, "source": "skill", "verified_on": "2026-11-03"}]))
    yield "R7 présent : clé connue = date et source", "| Âge de déclin | 31 ans | 2026-11-03 (skill) |" in p7
    yield "R7 absent : sans clé = jamais calculé", "| Poste mince | profondeur ≤ 2 | jamais calculé |" in p7 \
        and "1 sur 2 jamais calculés" in p7
    yield "R7 absent : tableau absent du playbook = donnée manquante", "donnée manquante" in txt(r.sec_parametres([], []))

    # V4 (6c) : version du moteur et décisions ouvertes d'une version antérieure
    VE = [{"version": "v3", "competition_kind": "ligue", "start_date": "2026-09-07", "end_date": "2026-10-26"},
          {"version": "v5", "competition_kind": "amical", "start_date": "2026-10-28", "end_date": None},
          {"version": "v4", "competition_kind": "ligue", "start_date": "2026-11-02", "end_date": None}]
    OU = [{"id": 7, "jour": "2026-10-30"}, {"id": 9, "jour": "2026-11-01"}, {"id": 12, "jour": "2026-11-05"}]
    cles = sorted(r.cle_version(x) for x in VE)
    v4, k4 = r.lignes_version(VE, OU, LUNDI, {"jour": "02/11", "versions": cles})
    yield "V4 présent : « ligue v4, amical v5 ; décisions ouvertes d'une version antérieure : 2 », sans liste", \
        len(v4) == 1 and "Version du moteur : ligue v4, amical v5 ; décisions ouvertes d'une version antérieure : 2 (avant le 02/11)" in v4[0] \
        and k4 == cles
    VE5 = VE + [{"version": "v5", "competition_kind": "ligue", "start_date": "2026-11-15", "end_date": None}]
    VE5[2] = dict(VE5[2], end_date="2026-11-14")
    v5, _ = r.lignes_version(VE5, OU, JOUR, {"jour": "08/11", "versions": cles})
    yield "V4 présent : nouvelle ligne de version = liste des conseils ouverts d'avant, rien de marqué", \
        "ligue v5, amical v5 ; décisions ouvertes d'une version antérieure : 3" in v5[0] and len(v5) == 2 \
        and "Nouvelle version ligue v5 (depuis le 15/11) : conseils ouverts d'avant (3) : 7, 9, 12 ; rien n'est marqué" in v5[1]
    v0, _ = r.lignes_version(VE5, OU, JOUR, {"jour": "08/11", "n_against": 1})
    yield "V4 absent : instantané précédent sans clé de versions = aucune liste", len(v0) == 1
    vm, km = r.lignes_version(None, OU, JOUR, None)
    yield "V4 absent : table illisible = donnée manquante, aucune clé", "donnée manquante" in vm[0] and km is None

    # R1 et instantané
    yield "R1 page coupée à 60 lignes, la dernière le dit", \
        len(r.borner(["x"] * 70)) == 60 and "11 lignes de plus" in r.borner(["x"] * 70)[-1]
    yield "R1 page courte inchangée", r.borner(["x"] * 5) == ["x"] * 5
    with tempfile.TemporaryDirectory() as tmp:
        for j, n_ag in (("2026-11-01", 0), ("2026-11-08", 1), ("2026-11-14", 5), ("2026-11-15", 9)):
            (Path(tmp) / f"instantane-{j}.json").write_text(json.dumps({"n_against": n_ag, "non_lus": 90}), encoding="utf-8")
        p = r.precedent_instantane(tmp, JOUR)
        yield "Instantané présent : celui d'il y a 7 jours ou plus (08/11), pas celui de la veille ni du jour", \
            p["jour"] == "08/11" and p["n_against"] == 1
        yield "Instantané absent : aucun avant le jour", r.precedent_instantane(tmp, dt.date(2026, 11, 1)) is None


if __name__ == "__main__":
    resultats = list(cas())
    echecs = [n for n, ok in resultats if not ok]
    for n, ok in resultats:
        print(("OK " if ok else "ECHEC "), n)
    print(f"{len(resultats) - len(echecs)}/{len(resultats)}")
    sys.exit(1 if echecs else 0)
