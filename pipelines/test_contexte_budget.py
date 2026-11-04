"""Test de pipelines/contexte_budget.py : calcul des jetons, dette figée, dépassement.

Lancer : python pipelines/test_contexte_budget.py   (code 1 si un cas se trompe)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import contexte_budget as cb  # noqa: E402

CAS = [
    ("jetons 360 car. = 100", cb.jetons("x" * 360) == 100),
    ("corps sans frontmatter", cb.corps("---\nname: a\n---\nBonjour") == "Bonjour"),
    ("description + nom", cb.description("---\nname: a\ndescription: b c\n---\nx") == "a: b c"),
    ("fichier sous budget", cb.verifie({"f.md": (900, 1000)}, {}, {}) == []),
    ("fichier au-dessus", len(cb.verifie({"f.md": (1100, 1000)}, {}, {})) == 1),
    ("dette tolère sans grossir", cb.verifie({"f.md": (1100, 1000)}, {}, {"f.md": 1100}) == []),
    ("dette qui grossit", len(cb.verifie({"f.md": (1101, 1000)}, {}, {"f.md": 1100})) == 1),
    ("session au-dessus", len(cb.verifie({}, {"bv": 6100}, {})) == 1),
    ("session dette", cb.verifie({}, {"bv": 6100}, {"session:bv": 6100}) == []),
]

if __name__ == "__main__":
    echecs = 0
    for nom, ok in CAS:
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    print(f"{len(CAS) - echecs}/{len(CAS)}")
    sys.exit(1 if echecs else 0)
