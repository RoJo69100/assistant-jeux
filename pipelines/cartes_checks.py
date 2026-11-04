"""« Checks appris » des cartes de décision : colonne « Statut (base) » générée depuis learn.lesson (refonte v2, 3.5).

Pour chaque carte docs/decisions/cartes/<jeu>/<type>.md, la table « ## Checks appris » garde ses colonnes
écrites à la main (L-nnn, Check, Ajouté le, Résultat depuis) ; la dernière colonne, « Statut (base) », est
réécrite à partir de public.learn_export : validée (n pour / m contre), règle dure, hypothèse, retirée.
Une L-nnn inconnue de la base est une erreur (code 1).
Usage : python -I pipelines/cartes_checks.py [jeux …] [--check]   (--check : n'écrit rien, code 1 si une carte change)
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from migrer_learnings import JEUX, RACINE, cellules  # noqa: E402

COLONNE = "Statut (base)"
REF = re.compile(r"\bL-\d{3}[a-z]?\b")


def libelle(l: dict) -> str:
    s = l["status"]
    if s == "validated":
        return f"✅ validée ({l['n_for']} pour / {l['n_against']} contre)"
    if s == "hard_rule":
        return f"✅ règle dure ({l['n_for']} pour)"
    if s == "retired":
        return "⛔ retirée — ne plus appliquer"
    return "hypothèse"


def statuts(base: dict) -> dict[str, dict]:
    """L-nnn → leçon ; pour un identifiant en double (« #2 »), la dernière version l'emporte."""
    res = {}
    for l in base["lessons"]:
        res[l["id"].split(":", 1)[-1].split("#")[0]] = l
    return res


def regenerer(texte: str, lecons: dict[str, dict]) -> tuple[str, list[str]]:
    out, erreurs, dans = [], [], False
    for ligne in texte.splitlines():
        if ligne.startswith("## "):
            dans = ligne.startswith("## Checks appris")
        if dans and ligne.startswith("|"):
            c = cellules(ligne)
            if c[-1] == COLONNE or (c and c[-1].startswith("---") and len(c) == 5):
                c = c[:-1]
            if c[0] == "L-nnn":
                c.append(COLONNE)
            elif set(c[0]) <= set("-: "):
                c.append("---")
            else:
                refs = REF.findall(c[0])
                inconnues = [r for r in refs if r not in lecons]
                erreurs += inconnues
                c = c[:4] if len(c) > 4 else c
                c.append(" / ".join(libelle(lecons[r]) if r in lecons else "❓ inconnue" for r in refs) or "—")
            ligne = "| " + " | ".join(c) + " |"
        out.append(ligne)
    return "\n".join(out) + ("\n" if texte.endswith("\n") else ""), erreurs


def main(argv=None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("jeux", nargs="*", default=[])
    p.add_argument("--check", action="store_true")
    a = p.parse_args(argv)
    from export_learnings_md import lire_base
    code = 0
    for jeu in a.jeux or JEUX:
        d = RACINE / f"docs/decisions/cartes/{jeu}"
        if not d.is_dir():
            continue
        lecons = statuts(lire_base(jeu))
        changees, erreurs = [], []
        for carte in sorted(d.glob("*.md")):
            texte = carte.read_text(encoding="utf-8")
            neuf, err = regenerer(texte, lecons)
            erreurs += [f"{carte.stem}:{e}" for e in err]
            if neuf != texte:
                changees.append(carte.stem)
                if not a.check:
                    carte.write_text(neuf, encoding="utf-8")
        ok = not erreurs and not (a.check and changees)
        code |= not ok
        print(("✅ " if ok else "❌ ") + f"{jeu} : " + (f"{'à régénérer' if a.check else 'régénérées'} : "
              f"{', '.join(changees)}" if changees else "cartes à jour")
              + (f" — leçons inconnues : {', '.join(erreurs)}" if erreurs else ""))
    return code


if __name__ == "__main__":
    sys.exit(main())
