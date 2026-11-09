"""Test de pipelines/composition.py (étape 5j, Y1) sur des briefs figés, sans réseau ni base.
Lancer : python -I pipelines/test_composition.py   (code 1 si un cas se trompe)
"""
import datetime as dt
import importlib.util
import sys
import tempfile
from pathlib import Path

DOSSIER = Path(__file__).resolve().parent
sys.path.insert(0, str(DOSSIER))
spec = importlib.util.spec_from_file_location("composition", DOSSIER / "composition.py")
comp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(comp)
import forme  # noqa: E402

JOUR = dt.date(2026, 11, 9)
EN_TETE = "| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Min | Off. focus | Rôle | Tir | Agress. |\n|---|---|---|---|---|---|---|---|---|---|---|---|\n"
# joueurs écrits dans le désordre (C avant PG) : le script doit remettre l'ordre de l'écran PG, SG, SF, PF, C
JOUEURS = (EN_TETE + "| Fournier | C | C | — | — | — | — | 12 | 2 | 2 | 1 | 1 |\n| Richard | PG | PG | PG | PG | PG | — | 36 | 1 | 1 | 3 | 1 |\n"
           "| Bonnet | SG | SG | SG | — | — | — | 24 | 5 | 5 | 5 | 1 |\n| Albano | PF | — | PF | PF | — | — | 24 | 3 | 3 | 3 | 1 |\n"
           "| Gimenez | SF | SF | — | SF | SF | SF | 36 | 4 | 3 | 3 | 1 |\n")
LIGUE = ("# Tactique ligue J4 : Naked Spartans (domicile, lun. 09/11 20:00, verrou 19:45)\n\n## 1. Fiche\n" + JOUEURS
         + "\n## 2. Adversaires\n| Adversaire | Poste | Focus (1-5) | Zone |\n|---|---|---|---|\n| tous les joueurs affichés | PG → C | 3 Normal | Middle (3) |\n"
         "\n## 2 bis. Focus réel\n| Adversaire | Poste | Pts | Focus |\n|---|---|---|---|\n| Zwoliński | PF | 23 pts | 4 Intense |\n"
         "| Biernacki | SG | 26 pts | 5 Lock |\n| Buczek | PG | 11 pts | 3 Normal |\nZone Middle pour les 3.\n")
AMICAL = ("# Tactique AMICAL lun. 09/11 08:00 (verrou 07:45), DOMICILE contre Garden City\n\n## 1. Composition (écran 1)\n| | PG | SG |\n|---|---|---|\n| Q1 | Baron | Leclerc |\n\n"
          "## 2. Consignes\n" + JOUEURS + "\n## 3. Adversaires\n| Adversaire | Poste | Focus (1-5) | Zone |\n|---|---|---|---|\n"
          "| Roze | PG | 3 Normal | Perimeter (1) |\n| Cunanan | C | 3 Normal | Perimeter (1) |\n| Franzoni | SF | 2 Light | Perimeter (1) |\n")
E1 = {"id": "E1", "niveaux": {"A": "agressivité 3", "B": "agressivité 5"}, "joue": {"A": {"agress_cran": 2}, "B": {"agress_cran": 4}},
      "ordre": ["A", "B"], "amicaux_vises": 4, "constants": {"zone": "Perimeter", "focus": 3}}
E5 = {"id": "E5", "niveaux": {"A": "Perimeter", "B": "Middle", "C": "Rim"}, "zone": {"A": "Perimeter", "B": "Middle", "C": "Rim"},
      "ordre": ["A", "B", "C"], "amicaux_vises": 3, "constants": {"focus": 3}}


def base(*fichiers):
    d = Path(tempfile.mkdtemp())
    (d / "briefs").mkdir()
    for nom, texte in fichiers:
        (d / "briefs" / nom).write_text(texte, encoding="utf-8")
    return d


def lignes_tableau(t, premier):
    """Cellules de la 1re colonne du tableau dont l'en-tête commence par `premier`."""
    for cols, lignes in forme.tableaux(t):
        if cols[0].startswith(premier):
            return [l[0] for l in lignes], [l[1] for l in lignes], lignes
    return [], [], []


def cas():
    b = base(("2026-11-08-tactique.md", LIGUE), ("2026-11-08-tactique-amical.md", AMICAL))
    t = comp.composer("Naked Spartans", b, JOUR, False)
    noms, postes, lignes = lignes_tableau(t, "joueur")
    yield "Y1 présent ligue : joueurs dans l'ordre de l'écran PG, SG, SF, PF, C", postes == ["PG", "SG", "SF", "PF", "C"]
    yield "Y1 présent ligue : colonnes de saisie complètes (12) et valeurs de l'écran reprises du brief", \
        all(len(l) == 12 for l in lignes) and lignes[0][:2] == ["Richard", "PG"] and lignes[0][-1] == "1"
    an, ap, al = lignes_tableau(t, "adversaire")
    yield "Y1 présent ligue : dernier tableau des adversaires (focus réel), zone lue sous le tableau, ordre PG→C", \
        an == ["Buczek", "Biernacki", "Zwoliński"] and [l[2] for l in al] == ["3", "5", "4"] and {l[3] for l in al} == {"Middle"}
    yield "Y1 présent : les deux tableaux passent forme.py sans erreur", forme.fautes_de(t, "basketvibe") == []
    # amical : test E1 niveau A (cran 2 → agressivité 3 à l'écran), zone et focus constants nommés sous le tableau
    ta = comp.composer("Garden City", b, JOUR, True, (E1, "A", False))
    _, _, ja = lignes_tableau(ta, "joueur")
    _, _, aa = lignes_tableau(ta, "adversaire")
    yield "Y1 présent amical : agressivité du test (3) pour tous les joueurs, à la place de celle du brief (1)", {l[11] for l in ja} == {"3"}
    yield "Y1 présent amical : zone Perimeter et focus 3 Normal nommés « constant pendant E1 », cellules valides", \
        "zone Perimeter : constant pendant E1" in ta and "focus défensif 3 (Normal) : constant pendant E1" in ta \
        and {l[2] for l in aa} == {"3"} and forme.fautes_de(ta, "basketvibe") == []
    tb = comp.composer("Garden City", b, JOUR, True, (E1, "B", False))
    yield "Y1 présent amical : niveau B = agressivité 5", {l[11] for l in lignes_tableau(tb, "joueur")[2]} == {"5"}
    te = comp.composer("Garden City", b, JOUR, True, (E5, "C", False))
    yield "Y4 présent E5 niveau C : zone Rim du test, focus 3 constant, agressivité du brief gardée", \
        {l[3] for l in lignes_tableau(te, "adversaire")[2]} == {"Rim"} and "zone Rim : réglage du test E5 niveau C" in te \
        and "focus défensif 3 (Normal) : constant pendant E5" in te and {l[11] for l in lignes_tableau(te, "joueur")[2]} == {"1"}
    tn = comp.composer("Garden City", b, JOUR, True, None)
    yield "Y1 amical sans test : valeurs du brief, aucune mention « constant »", "constant pendant" not in tn \
        and {l[3] for l in lignes_tableau(tn, "adversaire")[2]} == {"Perimeter"}
    # absents
    yield "Y1 absent : aucun brief du tout", comp.composer("Opper Cards", b, JOUR, True) == comp.AUCUNE
    yield "Y1 absent : brief d'un autre adversaire", comp.composer("Opper Cards", b, JOUR, False) == comp.AUCUNE
    yield "Y1 absent : brief du mauvais type (un brief de ligue ne sert pas à un amical)", comp.composer("Naked Spartans", b, JOUR, True) == comp.AUCUNE
    yield "Y1 absent : brief daté après le jour demandé", comp.composer("Naked Spartans", b, dt.date(2026, 11, 7), False) == comp.AUCUNE
    sans_adv = base(("2026-11-08-tactique.md", LIGUE.split("## 2.")[0]))
    yield "Y1 absent : brief sans tableau des adversaires = pas de fiche valide", comp.composer("Naked Spartans", sans_adv, JOUR, False) == comp.AUCUNE
    yield "Y1 absent : dossier de briefs vide", comp.composer("Naked Spartans", base(), JOUR, False) == comp.AUCUNE
    reel = comp.composer("Naked Spartans", comp.BASE, JOUR, False)
    yield "Y1 brief réel du 08/11 : 14 joueurs, 13 adversaires, forme.py sans erreur", \
        len(lignes_tableau(reel, "joueur")[2]) == 14 and len(lignes_tableau(reel, "adversaire")[2]) == 13 and forme.fautes_de(reel, "basketvibe") == []


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    echecs = 0
    jeux = list(cas())
    for nom, ok in jeux:
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    print(f"{len(jeux) - echecs}/{len(jeux)}")
    sys.exit(1 if echecs else 0)
