"""Réécriture des fiches tactiques du 17/11 dans la nouvelle forme (À saisir, vérifie, exporter, ---, Annexe) : aucune valeur de
saisie ne change. Compare les tableaux d'écran (composition, consignes, adversaires) de la version d'avant
(pipelines/jeu_essai/2026-11-17/fiches-avant/) à la version réécrite (outputs/basketvibe/briefs/), cellule par cellule ; seules les
annotations entre parenthèses de la 1re colonne (« Baron (17 ans) », « Les 12 (noms inconnus…) ») sont retirées.
Lancer : python -I pipelines/test_fiches_forme.py   (code 1 si un cas se trompe)"""
import re
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import composition as comp  # noqa: E402
import forme  # noqa: E402
import que_faire_blocs as qfb  # noqa: E402

AVANT = ICI / "jeu_essai" / "2026-11-17" / "fiches-avant"
APRES = ICI.parent / "outputs" / "basketvibe" / "briefs"
FICHES = ["2026-11-17-tactique-amical.md", "2026-11-17-tactique-amical-bg-bangers.md"]


def _sans_note(c: str) -> str:
    return re.sub(r"\s*\([^)]*\)\s*$", "", c.replace("*", "").strip())


def ecrans(texte: str) -> dict:
    """{« composition » | « consignes » | « adversaires » : lignes} des tableaux d'écran ; 1re colonne sans annotation."""
    res = {}
    for cols, lignes in forme.tableaux(texte):
        if not cols:
            continue
        cle = "consignes" if cols[0] == "joueur" else "adversaires" if "adversaire" in cols[0] else "composition" if "pg" in cols else None
        if cle and cle not in res:
            res[cle] = (tuple(cols), [[_sans_note(l[0])] + [x.replace("*", "").strip() for x in l[1:]] for l in lignes])
    return res


def cas():
    for nom in FICHES:
        avant, apres = (AVANT / nom).read_text(encoding="utf-8"), (APRES / nom).read_text(encoding="utf-8")
        ea, ep = ecrans(avant), ecrans(apres)
        yield f"{nom} : les 3 écrans présents avant et après", set(ea) == set(ep) == {"composition", "consignes", "adversaires"}
        for k in ("composition", "consignes", "adversaires"):
            yield f"{nom} : écran {k}, mêmes colonnes et mêmes valeurs", ea.get(k) == ep.get(k)
        la, lp = comp.lire_fiche(avant), comp.lire_fiche(apres)
        yield f"{nom} : lire_fiche lit la fiche réécrite", lp is not None
        yield f"{nom} : lire_fiche, mêmes valeurs (noms sans annotation)", la is not None and lp is not None \
            and [[_sans_note(r[0])] + r[1:] for r in la[0]] == lp[0] and [[_sans_note(a[0])] + a[1:] for a in la[1]] == lp[1]
        yield f"{nom} : première ligne inchangée", avant.splitlines()[0] == apres.splitlines()[0]
        yield f"{nom} : forme conforme (controle_forme_fiche)", qfb.controle_forme_fiche(apres) == []
        tete = apres.split("\n---\n")[0]
        yield f"{nom} : aucune prose du raisonnement avant ---", "gold." not in tete and "L-0" not in tete


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    jeux = list(cas())
    echecs = 0
    for n, ok in jeux:
        echecs += not ok
        print("OK " if ok else "ECHEC ", n)
    print(f"{len(jeux) - echecs}/{len(jeux)}")
    sys.exit(1 if echecs else 0)
