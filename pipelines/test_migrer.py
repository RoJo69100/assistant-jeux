"""Test de migrer_learnings.py et export_learnings_md.py (sans base : la charge parsée sert de « base »).

Lancer : python -I pipelines/test_migrer.py   (code 1 si un cas se trompe)
"""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_learnings_md import exporter  # noqa: E402
from migrer_learnings import RACINE, lire_jeu, statut_conseil, statut_lecon  # noqa: E402


def base(jeu: str) -> dict:
    lecons, conseils = lire_jeu(jeu)
    return {"lessons": lecons, "decisions": conseils}


def aller_retour(jeu: str) -> bool:
    texte, erreurs = exporter(jeu, base(jeu))
    return not erreurs and texte == (RACINE / f"outputs/{jeu}/learnings.md").read_text(encoding="utf-8")


def statut_reecrit() -> bool:
    b = base("hardwood")
    b["lessons"][0]["status"] = "retired"
    texte, _ = exporter("hardwood", b)
    return "infirmé, retirée (learn)" in texte


def nouvelle_lecon() -> bool:
    b = base("hardwood")
    neuve = copy.deepcopy(b["lessons"][0])
    neuve.update(id="hardwood:L-900", claim="test ajout", origine=None, status="validated", n_for=3)
    b["lessons"].append(neuve)
    texte, erreurs = exporter("hardwood", b)
    return not erreurs and "| L-900 | " in texte and "3 pour / 0 contre" in texte


def ligne_manquante() -> bool:
    b = base("hardwood")
    b["lessons"].pop()
    _, erreurs = exporter("hardwood", b)
    return bool(erreurs)


CAS = [
    ("« confirmé » sur 3 matchs → validée", statut_lecon("confirmé", 3), "validated"),
    ("« confirmé » sur 2 matchs → hypothèse", statut_lecon("confirmé", 2), "hypothesis"),
    ("« à surveiller (confirmé…) » → hypothèse", statut_lecon("à surveiller (confirmé en ligue)", 6), "hypothesis"),
    ("« **infirmé** » → retirée", statut_lecon("**infirmé**", 4), "retired"),
    ("« non confirmé » → hypothèse", statut_lecon("non confirmé", 5), "hypothesis"),
    ("« confirmé (lien : infirmé) » → validée", statut_lecon("confirmé (lien avec les résultats : infirmé)", 33),
     "validated"),
    ("conseil « appliqué » → done", statut_conseil("appliqué (2026-10-18)"), "done"),
    ("conseil « non appliqué » → rejected", statut_conseil("non appliqué"), "rejected"),
    ("conseil « ouvert » → proposed", statut_conseil("ouvert"), "proposed"),
    ("conseil « sans objet » → expired", statut_conseil("sans objet"), "expired"),
    *[(f"aller-retour {j}", aller_retour(j), True) for j in
      ("basketvibe", "hockeynation", "teamsoccer", "sixzeroleague", "derbymanager", "hardwood")],
    ("statut changé en base → cellule réécrite", statut_reecrit(), True),
    ("leçon créée en base → ligne ajoutée", nouvelle_lecon(), True),
    ("ligne du fichier absente de la base → erreur", ligne_manquante(), True),
]

if __name__ == "__main__":
    echecs = 0
    for nom, obtenu, attendu in CAS:
        ok = obtenu == attendu
        echecs += not ok
        print(f"{'OK ' if ok else 'ÉCHEC'} {nom}" + ("" if ok else f" : {obtenu!r} au lieu de {attendu!r}"))
    print(f"{len(CAS) - echecs}/{len(CAS)}")
    sys.exit(1 if echecs else 0)
