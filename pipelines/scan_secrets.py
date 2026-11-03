"""Garde anti-fuite : refuse un commit qui contient un secret ou un gros fichier.

Usage : python -I pipelines/scan_secrets.py [--all]
Sans option : fichiers indexés (git diff --cached). Avec --all : tous les fichiers suivis.
Code de sortie 1 si un motif ou un fichier de plus de 5 Mo est trouvé.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_OCTETS = 5 * 1024 * 1024
MOTIFS = [
    ("JWT", re.compile(r"eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}")),
    ("clé Supabase secrète", re.compile(r"sb_secret_[A-Za-z0-9_-]{10,}")),
    ("jeton Discord/ingestion", re.compile(r"(DISCORD_TOKEN|INGEST_TOKEN)[ \t]*=[ \t]*['\"]?[A-Za-z0-9._-]{8,}")),
    ("mot de passe en base", re.compile(r"postgres(?:ql)?://[^\s:@]+:[^\s@]{4,}@")),
]
IGNORER = {"pipelines/scan_secrets.py", "pipelines/test_scan_secrets.py"}


def fichiers(tous):
    cmd = ["git", "ls-files"] if tous else ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"]
    sortie = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return [l for l in sortie.splitlines() if l and l not in IGNORER]


def verifier(chemin):
    p = ROOT / chemin
    if not p.is_file():
        return []
    problemes = []
    if p.stat().st_size > MAX_OCTETS:
        problemes.append(f"{chemin} : fichier de plus de 5 Mo")
        return problemes
    try:
        texte = p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return problemes
    for nom, motif in MOTIFS:
        if motif.search(texte):
            problemes.append(f"{chemin} : {nom}")
    return problemes


def main():
    tous = "--all" in sys.argv
    problemes = [m for f in fichiers(tous) for m in verifier(f)]
    for m in problemes:
        print("REFUSÉ -", m)
    sys.exit(1 if problemes else 0)


if __name__ == "__main__":
    main()
