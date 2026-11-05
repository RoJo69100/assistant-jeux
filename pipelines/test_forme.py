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

# H3 (2026-11-02) : contrôles par jeu
HN4_OK = """Hockey Nation, effectif.
PRO
| Poste | Joueur | Note | Endurance | FOF |
|---|---|---|---|---|
| C | Carpentier | 61 | 70 | 55 |
FRM, U21 et U17 : identiques au relevé.
"""
HN4_KO = """Hockey Nation, effectif PRO.
| Poste | Joueur | Note | Endurance | FOF | Trou |
|---|---|---|---|---|---|
| C | Carpentier | 61 | 70 | 55 | non |
Pour voir la liste, lance la requête.
"""
TS_PLAN_KO = """Team Soccer, Chomelix Cows.
| Priorité | Catégorie | Action |
|---|---|---|
| 🟥 URGENT | Composition | Enregistrer la compo. |
"""
TS_PLAN_OK = TS_PLAN_KO.replace("Chomelix Cows.", "Chomelix Cows puis Ben Ahmed Donkey.")
TS_EMPL_KO = """Team Soccer : Chomelix Cows et Ben Ahmed Donkey.
| Empl. | Joueur | Ultra déf. | Défensive | Médiane | Offensive | Finition |
|---|---|---|---|---|---|---|
| DEF | García | Dégager | Passer → milieux | — | Passer → attaquants | Tirer |
Remplacements programmés : aucun.
"""
SZ_KO = """Six Zero League, tactique.
| Réglage | Valeur |
|---|---|
| Agressivité | Normal |
| Formation attaque | 5-1 |
| Direction | mixed |
"""
SZ_OK = """Six Zero League, tactique.
| Réglage | Valeur |
|---|---|
| Formation attaque | 5-1 |
| Formation défense | 6-0 |
| Direction | mixed |
| Agressivité | Normal |
"""
DM_KO = """Derby Manager.
| Priorité | Catégorie | Action |
|---|---|---|
| 🟥 URGENT | Composition | Marmandes : 4-4-2. |
| 🟧 IMPORTANT | Composition | Queen of the South : 4-3-3. |
"""
DM_OK = """Derby Manager, Queen of the South puis Marmandes.
| Poste | Rôle | Joueur |
|---|---|---|
| DC | CD | Smith |
Remplaçants S1-S5 : Brown (AUTO). Set pieces : PEN Smith, FK Brown, capitaine Smith.
"""
DM_COMPO_KO = DM_OK.replace(" Set pieces : PEN Smith, FK Brown, capitaine Smith.", "")
SI_TITRE = PLAN_OK + """
**Si** :
- on gagne J20, faire tourner les jeunes après le prochain match ;
- on perd, garder le cinq plus tard aussi.
"""
SI_LIGNE = PLAN_OK + "\nSi Baron se blesse, on verra plus tard.\n"
SI_TABLEAU = PLAN_OK + """
| Si | Alors |
|---|---|
| titre acquis | faire tourner les jeunes plus tard |
"""
PLAN_SAISON = """### Plan de saison
Titre visé ; après le prochain match, faire tourner les jeunes.

""" + PLAN_OK
SI_PUIS_INTERDIT = SI_TITRE + "\n### Ce soir\nOn verra plus tard.\n"

CAS = [
    ("plan ok", PLAN_OK, True), ("plan ko", PLAN_KO, False),
    ("entraînement tous ok", ENTR_TOUS_OK, True), ("entraînement changements ok", ENTR_CHANGE_OK, True),
    ("entraînement désordre", ENTR_DESORDRE, False), ("entraînement sans changement", ENTR_SANS_CHANGEMENT, False),
    ("entraînement partiel « tous »", ENTR_PARTIEL, False),
    ("tactique ok", TACT_OK, True), ("tactique ko", TACT_KO, False),
    ("adversaires ok", ADV_OK, True), ("adversaires ko", ADV_KO, False),
    ("hardwood tactique ok", HW_OK, True), ("hardwood tactique ko", HW_KO, False),
    ("tableau Réglage | Valeur (SZL) laissé passer", "| Réglage | Valeur |\n|---|---|\n| Formation d'attaque | 5-1 |\n| Direction | mixed |\n", True),
    ("hardwood recrues ok", REC_OK, True), ("hardwood recrues ko", REC_KO, False),
    ("team soccer ok", TS_OK, True), ("team soccer ko", TS_KO, False),
    ("hn effectif ok", HN_OK, True), ("hn effectif ko", HN_KO, False),
    ("hn 4 équipes ok", HN4_OK, True), ("hn sans 4 équipes, trou, voir la liste", HN4_KO, False),
    ("ts plan deux clubs ok", TS_PLAN_OK, True), ("ts plan un club", TS_PLAN_KO, False),
    ("ts emplacement DEF + cellule vide", TS_EMPL_KO, False),
    ("sz ordre ok", SZ_OK, True), ("sz ordre ko", SZ_KO, False),
    ("dm compo ok", DM_OK, True), ("dm clubs inversés", DM_KO, False), ("dm compo sans set pieces", DM_COMPO_KO, False),
    ("texte avec interdit", TEXTE_KO, False),
    ("texte sans tableau", "Voilà, c'est fait.", True),
    # S1 : blocs « Si » et « Plan de saison » acceptés
    ("bloc Si titré accepté", SI_TITRE, True),
    ("ligne Si accepté", SI_LIGNE, True),
    ("tableau Si | Alors accepté", SI_TABLEAU, True),
    ("bloc Plan de saison accepté", PLAN_SAISON, True),
    ("interdit après la fin du bloc Si", SI_PUIS_INTERDIT, False),
    ("interdit hors bloc", PLAN_OK + "\nOn verra plus tard.\n", False),
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
