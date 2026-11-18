"""Tests figés de fin_etape.py (critère T4), sur des dépôts temporaires : python -I pipelines/test_fin_etape.py"""

import contextlib
import io
import subprocess
import sys
import tempfile
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
from fin_etape import rapport  # noqa: E402

CFG = ["-c", "commit.gpgsign=false", "-c", "user.name=test", "-c", "user.email=test@test"]


def g(cwd, *args) -> str:
    return subprocess.run(["git", *CFG, *args], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


def depot(racine: Path) -> tuple[Path, Path]:
    """origin.git + clone avec pipelines/test_a.py (« 3/3 ») et test_b.py (sans sortie), main poussé."""
    origine, travail = racine / "origin.git", racine / "travail"
    g(racine, "init", "--bare", "-b", "main", str(origine))
    g(racine, "clone", str(origine), str(travail))
    g(travail, "checkout", "-b", "main")
    (travail / "pipelines").mkdir()
    (travail / "pipelines" / "test_a.py").write_text("print('OK x')\nprint('3/3')\n", encoding="utf-8")
    (travail / "pipelines" / "test_b.py").write_text("x = 1\n", encoding="utf-8")
    g(travail, "add", ".")
    g(travail, "commit", "-m", "base")
    g(travail, "push", "-u", "origin", "main")
    return origine, travail


def lancer(travail) -> tuple[int, str]:
    tampon = io.StringIO()
    with contextlib.redirect_stdout(tampon):
        code = rapport(travail)
    return code, tampon.getvalue()


def etat_git(travail) -> tuple[str, str, str]:
    return g(travail, "rev-parse", "HEAD"), g(travail, "rev-parse", "origin/main"), g(travail, "status", "--short")


def cas_a_jour(racine):
    _, travail = depot(racine)
    code, out = lancer(travail)
    return code == 0 and "branche : main" in out and "commits d'avance sur origin/main : 0" in out \
        and "(propre)" in out and "HEAD dans origin/main : oui" in out


def cas_en_avance(racine):
    _, travail = depot(racine)
    g(travail, "checkout", "-b", "session")
    (travail / "n.txt").write_text("n", encoding="utf-8")
    g(travail, "add", ".")
    g(travail, "commit", "-m", "nouveau")
    code, out = lancer(travail)
    return code == 1 and "commits d'avance sur origin/main : 1" in out and "nouveau" in out \
        and "HEAD dans origin/main : NON" in out


def cas_statut_court(racine):
    _, travail = depot(racine)
    (travail / "sale.txt").write_text("x", encoding="utf-8")
    code, out = lancer(travail)
    return code == 0 and "?? sale.txt" in out


def cas_tests(racine):
    _, travail = depot(racine)
    _, out = lancer(travail)
    return "test_a.py : 3/3" in out and "test_b.py : (aucune sortie)" in out


def cas_ligne_de_forme(racine):
    """17/11 : la ligne d'un test est sa dernière ligne N/N (stdout) si elle existe, jamais un message stderr ; sans N/N, repli sur la dernière ligne."""
    _, travail = depot(racine)
    (travail / "pipelines" / "test_c.py").write_text(
        "import sys\nprint('3 requêtes sur 4 en échec', file=sys.stderr)\nprint('OK x')\nprint('282/282')\nprint('fin sans forme')\n", encoding="utf-8")
    (travail / "pipelines" / "test_d.py").write_text("import sys\nprint('vert')\nprint('message', file=sys.stderr)\n", encoding="utf-8")
    _, out = lancer(travail)
    return "test_c.py : 282/282" in out and "test_c.py : 3 requêtes" not in out and "test_d.py : message" in out


def cas_test_rouge(racine):
    """18/11 : un test rouge (N/M avec N < M, ou code retour non nul) fait sortir fin_etape.py avec un code non nul, même à jour."""
    _, travail = depot(racine)
    (travail / "pipelines" / "test_r.py").write_text("print('ECHEC x')\nprint('504/505')\n", encoding="utf-8")
    code_n, out_n = lancer(travail)
    (travail / "pipelines" / "test_r.py").write_text("import sys\nprint('5/5')\nsys.exit(1)\n", encoding="utf-8")
    code_c, _ = lancer(travail)
    (travail / "pipelines" / "test_r.py").write_text("print('5/5')\n", encoding="utf-8")
    code_v, _ = lancer(travail)
    return code_n != 0 and "tests rouges : 1" in out_n and code_c != 0 and code_v == 0


def cas_lecture_seule(racine):
    _, travail = depot(racine)
    (travail / "sale.txt").write_text("x", encoding="utf-8")
    avant = etat_git(travail)
    lancer(travail)
    return etat_git(travail) == avant


CAS = [
    ("à jour : code 0, 0 commit d'avance", cas_a_jour),
    ("en avance : code 1, commit listé", cas_en_avance),
    ("git status --short affiché", cas_statut_court),
    ("dernière ligne de chaque test_*.py", cas_tests),
    ("ligne N/N de stdout plutôt qu'un message stderr", cas_ligne_de_forme),
    ("test rouge : code non nul", cas_test_rouge),
    ("lecture seule : HEAD, origin/main, statut inchangés", cas_lecture_seule),
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
