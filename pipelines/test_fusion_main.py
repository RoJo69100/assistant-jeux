"""Tests figés de fusion_main.py (critère T3), sur des dépôts temporaires : python -I pipelines/test_fusion_main.py"""

import contextlib
import io
import subprocess
import sys
import tempfile
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
from fusion_main import fusion  # noqa: E402

CFG = ["-c", "commit.gpgsign=false", "-c", "user.name=test", "-c", "user.email=test@test"]


def g(cwd, *args) -> str:
    r = subprocess.run(["git", *CFG, *args], cwd=cwd, capture_output=True, text=True, check=True)
    return r.stdout.strip()


def commit(cwd, nom: str) -> str:
    (Path(cwd) / f"{nom}.txt").write_text(nom, encoding="utf-8")
    g(cwd, "add", ".")
    g(cwd, "commit", "-m", nom)
    return g(cwd, "rev-parse", "HEAD")


def depot(racine: Path) -> tuple[Path, Path]:
    """origin.git (nu) + clone de travail sur la branche « session », main poussé."""
    origine, travail = racine / "origin.git", racine / "travail"
    g(racine, "init", "--bare", "-b", "main", str(origine))
    g(racine, "clone", str(origine), str(travail))
    g(travail, "checkout", "-b", "main")
    commit(travail, "base")
    g(travail, "push", "-u", "origin", "main")
    g(travail, "checkout", "-b", "session")
    return origine, travail


def distant(origine: Path) -> str:
    return g(origine, "rev-parse", "refs/heads/main")


def lancer(travail, essai=False) -> tuple[int, str]:
    tampon = io.StringIO()
    with contextlib.redirect_stdout(tampon):
        code = fusion(travail, essai)
    return code, tampon.getvalue()


def cas_fast_forward(racine):
    origine, travail = depot(racine)
    tete = commit(travail, "t1")
    code, out = lancer(travail)
    return code == 0 and distant(origine) == tete and "avant : HEAD" in out and "après : HEAD" in out \
        and g(travail, "rev-parse", "main") == tete


def cas_essai(racine):
    origine, travail = depot(racine)
    avant = distant(origine)
    commit(travail, "t1")
    code, out = lancer(travail, essai=True)
    return code == 0 and distant(origine) == avant and "Essai : rien n'est poussé." in out


def cas_divergent(racine):
    origine, travail = depot(racine)
    commit(travail, "t1")
    autre = racine / "autre"
    g(racine, "clone", str(origine), str(autre))
    commit(autre, "concurrent")
    g(autre, "push", "origin", "main")
    avant, statut = distant(origine), g(travail, "status", "--short")
    code, out = lancer(travail)
    return code == 1 and distant(origine) == avant and "fast-forward" in out and statut == g(travail, "status", "--short")


def cas_a_jour(racine):
    origine, travail = depot(racine)
    avant = distant(origine)
    code, out = lancer(travail)
    return code == 0 and distant(origine) == avant and "Déjà à jour" in out


def cas_sans_forcage(_racine):
    source = (ICI / "fusion_main.py").read_text(encoding="utf-8")
    return "--force" not in source and '"-f"' not in source and "+HEAD" not in source


CAS = [
    ("fast-forward : main avance et est poussé", cas_fast_forward),
    ("--essai : rien n'est poussé", cas_essai),
    ("divergent : refus, rien ne change", cas_divergent),
    ("déjà à jour : aucun push", cas_a_jour),
    ("jamais de forçage dans le source", cas_sans_forcage),
]


def main() -> int:
    echecs = 0
    for nom, cas in CAS:
        with tempfile.TemporaryDirectory() as d:
            try:
                ok = cas(Path(d))
            except subprocess.CalledProcessError as e:
                ok = False
                print(e.stderr)
        echecs += not ok
        print("OK " if ok else "ECHEC ", nom)
    print(f"{len(CAS) - echecs}/{len(CAS)}")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
