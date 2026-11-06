"""Fige le jeu d'essai de aujourdhui_hockeynation.py : les 8 requêtes du jour, telles que la base les rend, en JSON.

Écrit pipelines/jeu_essai/hockeynation/<jour>/donnees.json, fait-<jour>.md et learnings.md (copies du registre et du journal
des enseignements). À lancer une seule fois par jour figé : python -I pipelines/figer_jeu_essai_hockeynation.py 2026-11-06
Les cas des tests (deux matchs sans équipe, lineup à 18 cases vides) sont fabriqués dans les tests à partir de ce relevé.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import aujourdhui_hockeynation as hn  # noqa: E402
import sql as sqlmod  # noqa: E402


def main() -> int:
    jour = sys.argv[1]
    sortie = Path(__file__).resolve().parent / "jeu_essai" / "hockeynation" / jour
    sortie.mkdir(parents=True, exist_ok=True)
    donnees, erreurs, _ = hn.lire_tout(sqlmod.executer)
    if erreurs:
        sys.exit(f"vues illisibles : {erreurs}")
    brut = {nom: {"cols": list(cols), "rows": [list(r) for r in rows]} for nom, (cols, rows) in donnees.items()}
    (sortie / "donnees.json").write_text(json.dumps(brut, ensure_ascii=False, default=str), encoding="utf-8")
    for source, nom in ((hn.BASE / f"fait-{jour}.md", f"fait-{jour}.md"), (hn.BASE / "learnings.md", "learnings.md")):
        shutil.copyfile(source, sortie / nom)
    print(f"{len(brut)} requêtes figées dans {sortie}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
