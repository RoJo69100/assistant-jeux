"""Relie le registre « fait » aux décisions (refonte v3, étape 5b-3, critère D4).

Une ligne de `outputs/<jeu>/fait-AAAA-MM-JJ.md` peut porter `[décision=<id>]` (en plus de `[clé=…]`) quand la saisie
déclarée vient d'une décision ouverte. Ce script lit les registres des 7 derniers jours (date de Paris) et passe à `done`,
par `python -I pipelines/decision.py statut <id> done`, chaque décision citée qui est encore `proposed`.
Jamais de correspondance floue : seul l'identifiant écrit dans la ligne compte. Une ligne « reste à … » est ignorée.
Identifiant inconnu, d'un autre jeu, déjà `done` ou dans un autre statut : signalé, rien n'est écrit.
Usage : python -I pipelines/relier_faits.py <jeu> [--essai]   (--essai : liste sans écrire)
"""

import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from heure_paris import paris  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent
DECISION = re.compile(r"\[décision=(\d+)\]", re.I)
RESTE = re.compile(r"reste à", re.I)
REGISTRE = re.compile(r"^fait-(\d{4}-\d{2}-\d{2})\.md$")
FENETRE = 7  # jours relus, aujourd'hui compris


def lire_references(base: Path, jour: dt.date, fenetre: int = FENETRE) -> list[dict]:
    """{id, fichier, ligne} pour chaque `[décision=<id>]` d'une ligne faite des `fenetre` derniers registres."""
    res = []
    for f in sorted(Path(base).glob("fait-*.md")):
        m = REGISTRE.match(f.name)
        if not m:
            continue
        j = dt.date.fromisoformat(m.group(1))
        if j > jour or (jour - j).days >= fenetre:
            continue
        res += references_lignes(f.name, f.read_text(encoding="utf-8").splitlines())
    return res


def references_lignes(fichier: str, lignes: list[str]) -> list[dict]:
    res = []
    for n, l in enumerate(lignes, 1):
        if RESTE.search(l):
            continue
        for d in DECISION.finditer(l):
            res.append({"id": int(d.group(1)), "fichier": fichier, "ligne": n})
    return res


def plan(refs: list[dict], decisions: dict[int, tuple[str, str]], jeu: str) -> list[dict]:
    """decisions : id → (statut, jeu) lus en base. Rend une action par identifiant distinct :
    a_faire = True seulement pour une décision du jeu encore « proposed »."""
    vus, res = set(), []
    for r in refs:
        if r["id"] in vus:
            continue
        vus.add(r["id"])
        statut, jeu_d = decisions.get(r["id"], (None, None))
        if statut is None:
            raison = "identifiant inconnu"
        elif jeu_d != jeu:
            raison = f"décision d'un autre jeu ({jeu_d})"
        elif statut != "proposed":
            raison = f"déjà {statut}"
        else:
            raison = None
        res.append({**r, "statut": statut, "a_faire": raison is None, "raison": raison})
    return res


def lire_decisions(ids: list[int]) -> dict[int, tuple[str, str]]:
    from sql import executer
    if not ids:
        return {}
    _, lignes = executer("select id, status, game from learn.decision where id in (" + ", ".join(map(str, ids)) + ")")
    return {int(i): (st, g) for i, st, g in lignes}


def main(argv=None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    a = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    a.add_argument("jeu")
    a.add_argument("--essai", action="store_true")
    args = a.parse_args(argv)
    jour = paris().date()
    refs = lire_references(RACINE / "outputs" / args.jeu, jour)
    actions = plan(refs, lire_decisions(sorted({r["id"] for r in refs})), args.jeu)
    if not actions:
        print("Aucune ligne [décision=<id>] dans les registres des 7 derniers jours.")
        return 0
    erreurs = 0
    for x in actions:
        source = f"{x['fichier']}:{x['ligne']}"
        if not x["a_faire"]:
            print(f"— D-{x['id']} ({source}) : {x['raison']}, rien écrit")
            continue
        if args.essai:
            print(f"→ D-{x['id']} ({source}) : proposed → done (essai, rien écrit)")
            continue
        r = subprocess.run([sys.executable, "-I", str(RACINE / "pipelines" / "decision.py"), "statut", str(x["id"]), "done",
                            "--note", f"relier_faits : {source}"], capture_output=True, text=True, encoding="utf-8")
        print(f"→ D-{x['id']} ({source}) : {(r.stdout or r.stderr).strip()}")
        erreurs += r.returncode != 0
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
