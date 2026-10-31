"""Test du hook pipelines/forme.py : un cas valide et un cas fautif par format.

Lancer : python pipelines/test_forme.py   (code 1 si un cas se trompe)
"""

import sys

sys.path.insert(0, str(__file__.rsplit("pipelines", 1)[0] + "pipelines"))
import forme  # noqa: E402

PLAN_OK = """| Priorité | Catégorie | Action |
|---|---|---|
| 🟥 URGENT | Composition | Saisir la compo du match contre BC Calije. |
| 🟩 SUIVI | Export | Exporter la page du match. |
"""
PLAN_KO = """| Priorité | Catégorie | Action |
|---|---|---|
| URGENT | Compo | rien à faire |
"""
ENTR_TOUS_OK = """| Joueur | Principale | Secondaire |
|---|---|---|
| Albano | Rebounding | Defense |
| Baron | Passing | Defense |
| Bernard | Rebounding | Athleticism |
| Bonnet | Defense | Ball handling |
| Boyer | Passing | Ball handling |
| Dang | Three point | Defense |
| Durand | Two point | Defense |
| Fournier | Rebounding | Defense |
| Gimenez | Two point | Three point |
| Henry | Three point | Two point |
| Klein | Rebounding | Defense |
| Leclerc | Three point | Defense |
| Lecomte | Defense | Athleticism |
| Lefebvre | Defense | Athleticism |
| Legrand | Rebounding | Defense |
| Richard | Passing | Defense |
| Ungureanu | Rebounding | Passing |
"""
ENTR_CHANGE_OK = """| Joueur | Actuel | À mettre |
|---|---|---|
| Baron | Passing / Defense | Passing / Ball handling |
| Henry | Three point / Two point | Two point / Three point |
"""
ENTR_DESORDRE = """| Joueur | Actuel | À mettre |
|---|---|---|
| Henry | Three point / Two point | Two point / Three point |
| Baron | Passing / Defense | Passing / Ball handling |
"""
ENTR_SANS_CHANGEMENT = """| Joueur | Actuel | À mettre |
|---|---|---|
| Baron | Passing / Defense | Passing / Defense |
"""
ENTR_PARTIEL = """| Joueur | Principale | Secondaire |
|---|---|---|
| Albano | Rebounding | Defense |
| Baron | Passing | Defense |
"""
TACT_OK = """| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Minutes | Off. focus | Rôle | Tir | Agress. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baron | PG | x | x | x | x | x | 30 | 3 | a | b | c |
| Henry | SG | x | x | x | x | x | 30 | 3 | a | b | c |
| Gimenez | SF | x | x | x | x | x | 30 | 3 | a | b | c |
| Albano | PF | x | x | x | x | x | 30 | 3 | a | b | c |
| Bernard | C | x | x | x | x | x | 30 | 3 | a | b | c |
"""
TACT_KO = """| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Minutes | Off. focus | Rôle | Tir | Agress. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bernard | C | x | x | x | x | x | 30 | 3 | a | b | c |
| Baron | PG | x | x | x | x | x | 30 | 3 | a | b | c |
"""
ADV_OK = """| Adversaire | Poste | Focus défensif (1–5) | Zone |
|---|---|---|---|
| Brun | PG | 4 | Perimeter |
| Girard | PG | 3 | Middle |
| Lacroix | C | 5 | Rim |
"""
ADV_KO = """| Adversaire | Poste | Focus défensif (1–5) | Zone |
|---|---|---|---|
| Brun, Girard | PG | 4 | Perimeter |
| Lacroix | C | 7 | Haut |
"""
HW_OK = """| Réglage | Actuel | À mettre |
|---|---|---|
| Pace | 50 | 60 |
| Inside/Outside Emphasis | 40 | 50 |
| Zone % | 20 | 30 |
| Pressure % | 10 | 10 |
| Extend | Off | On |
"""
HW_KO = """| Réglage | Actuel | À mettre |
|---|---|---|
| Extend | Off | On |
| Pace | 50 | 60 |
"""
REC_OK = """| Priorité | Poste (qui part) | Cible | Remplaçant 1 | Remplaçant 2 |
|---|---|---|---|---|
| 1 | PG | Sturgeon | A | B |
| 2 | SG | Simon | A | B |
| 3 | Grand | Woodling | A | B |
| 4 | SF | Tolliver | A | B |
"""
REC_KO = """| Priorité | Poste | Cible | Remplaçant 1 | Remplaçant 2 |
|---|---|---|---|---|
| 1 | PG | Sturgeon (High) | A | B |
| 2 | SG | Simon | A | B |
| 3 | Grand | Woodling | A | B |
"""
TS_OK = """Chomelix Cows
| Empl. | Ultra déf. | Défensive | Médiane | Offensive | Finition |
|---|---|---|---|---|---|
| ATT | Passer aux attaquants | x | x | x | x |
Ben Ahmed Donkey : idem.
Remplacements programmés : aucun.
"""
TS_KO = """Chomelix Cows
| Empl. | Ultra déf. | Défensive | Médiane | Offensive | Finition |
|---|---|---|---|---|---|
| ATT | Passer | x | x | x | x |
"""
HN_OK = """| Poste | Joueur | Note | Endurance | FOF |
|---|---|---|---|---|
| C | X | 70 | 8 | 6 |
"""
HN_KO = """| Poste | Joueur | Note |
|---|---|---|
| C | X | 70 |
"""
TEXTE_KO = "J'ai pas tout lu, ce sera pour plus tard."

CAS = [
    ("plan ok", PLAN_OK, True), ("plan ko", PLAN_KO, False),
    ("entraînement tous ok", ENTR_TOUS_OK, True), ("entraînement changements ok", ENTR_CHANGE_OK, True),
    ("entraînement désordre", ENTR_DESORDRE, False), ("entraînement sans changement", ENTR_SANS_CHANGEMENT, False),
    ("entraînement partiel « tous »", ENTR_PARTIEL, False),
    ("tactique ok", TACT_OK, True), ("tactique ko", TACT_KO, False),
    ("adversaires ok", ADV_OK, True), ("adversaires ko", ADV_KO, False),
    ("hardwood tactique ok", HW_OK, True), ("hardwood tactique ko", HW_KO, False),
    ("hardwood recrues ok", REC_OK, True), ("hardwood recrues ko", REC_KO, False),
    ("team soccer ok", TS_OK, True), ("team soccer ko", TS_KO, False),
    ("hn effectif ok", HN_OK, True), ("hn effectif ko", HN_KO, False),
    ("texte avec interdit", TEXTE_KO, False),
    ("texte sans tableau", "Voilà, c'est fait.", True),
]

if __name__ == "__main__":
    echecs = 0
    for nom, texte, attendu in CAS:
        fautes = forme.fautes_de(texte)
        ok = (not fautes) == attendu
        echecs += not ok
        print(("✅" if ok else "❌"), nom, "" if ok else f"— {fautes}")
    print(f"{len(CAS) - echecs}/{len(CAS)}")
    sys.exit(1 if echecs else 0)
