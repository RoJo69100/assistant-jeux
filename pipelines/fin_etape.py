"""État de fin d'étape, lecture seule : python -I pipelines/fin_etape.py

Conçu le 2026-11-09 (critère T4, journal-aujourdhui.md « Garde-fous mécaniques »).
Imprime : branche, HEAD, origin/main, commits d'avance sur origin/main, `git status --short`,
dernière ligne de sortie de chaque pipelines/test_*.py.
Aucun fetch, aucune écriture git. Code retour 1 si HEAD n'est pas contenu dans origin/main.
Tests : test_fin_etape.py.
"""

import subprocess
import sys
from pathlib import Path


def git(cwd, *args) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8")


def derniere_ligne(cwd, fichier: Path) -> str:
    try:
        r = subprocess.run([sys.executable, "-I", str(fichier)], cwd=cwd, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=300)
    except subprocess.TimeoutExpired:
        return "(délai dépassé)"
    lignes = [l for l in (r.stdout + "\n" + r.stderr).splitlines() if l.strip()]
    fin = lignes[-1].strip() if lignes else "(aucune sortie)"
    return fin if r.returncode == 0 else f"{fin} [code {r.returncode}]"


def rapport(cwd=None) -> int:
    racine = Path(git(cwd, "rev-parse", "--show-toplevel").stdout.strip() or ".")
    head = git(cwd, "rev-parse", "HEAD").stdout.strip()
    om = git(cwd, "rev-parse", "--verify", "--quiet", "refs/remotes/origin/main").stdout.strip()
    print(f"branche : {git(cwd, 'rev-parse', '--abbrev-ref', 'HEAD').stdout.strip()}")
    print(f"HEAD : {head[:12] or '?'}")
    print(f"origin/main : {om[:12] or '?'}")
    avance = git(cwd, "log", "--oneline", f"{om}..HEAD").stdout.strip() if om else ""
    print(f"commits d'avance sur origin/main : {len(avance.splitlines())}")
    if avance:
        print(avance)
    statut = git(cwd, "status", "--short").stdout.rstrip()
    print("git status --short :" + ("\n" + statut if statut else " (propre)"))
    print("tests :")
    for fichier in sorted((racine / "pipelines").glob("test_*.py")):
        print(f"  {fichier.name} : {derniere_ligne(racine, fichier)}")
    contenu = bool(om) and git(cwd, "merge-base", "--is-ancestor", "HEAD", om).returncode == 0
    print("HEAD dans origin/main : " + ("oui" if contenu else "NON"))
    return 0 if contenu else 1


if __name__ == "__main__":
    sys.exit(rapport())
