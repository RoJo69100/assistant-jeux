"""Fusion de la branche courante dans main, en fast-forward seulement, puis push de main.

Conçu le 2026-11-09 (critère T3, journal-aujourdhui.md « Garde-fous mécaniques »).
  python -I pipelines/fusion_main.py           fetch, contrôle, push de HEAD sur main
  python -I pipelines/fusion_main.py --essai   fetch, contrôle, imprime sans pousser
Refuse sans rien changer si origin/main n'est pas un ancêtre de HEAD (branches divergentes).
Jamais de forçage. Imprime avant/après les hashs de HEAD et d'origin/main. Code 0 = main == HEAD.
Tests : test_fusion_main.py.
"""

import subprocess
import sys


def git(cwd, *args) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8")


def sortie(r: subprocess.CompletedProcess) -> None:
    for flux in (r.stdout, r.stderr):
        if flux.strip():
            print(flux.rstrip())


def hash_de(cwd, ref: str) -> str:
    r = git(cwd, "rev-parse", "--verify", "--quiet", ref)
    return r.stdout.strip() if r.returncode == 0 else ""


def etat(cwd, moment: str) -> tuple[str, str]:
    head, om = hash_de(cwd, "HEAD"), hash_de(cwd, "refs/remotes/origin/main")
    print(f"{moment} : HEAD {head[:12] or '?'} | origin/main {om[:12] or '?'}")
    return head, om


def fusion(cwd=None, essai: bool = False) -> int:
    branche = git(cwd, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    print(f"branche : {branche}")
    r = git(cwd, "fetch", "origin")
    sortie(r)
    if r.returncode:
        print("Refusé : git fetch a échoué, rien n'est changé.")
        return 1
    head, om = etat(cwd, "avant")
    if not head or not om:
        print("Refusé : HEAD ou origin/main introuvable, rien n'est changé.")
        return 1
    if head == om:
        print("Déjà à jour : origin/main == HEAD, rien à pousser.")
        return 0
    if git(cwd, "merge-base", "--is-ancestor", om, head).returncode:
        print("Refusé : main ne peut pas avancer en fast-forward (HEAD et origin/main divergent), rien n'est changé.")
        return 1
    commits = git(cwd, "log", "--oneline", f"{om}..{head}").stdout.strip()
    print(f"commits à ajouter à main ({len(commits.splitlines())}) :")
    print(commits)
    if essai:
        print("Essai : rien n'est poussé.")
        return 0
    r = git(cwd, "push", "origin", "HEAD:refs/heads/main")
    sortie(r)
    if r.returncode:
        print("Échec : git push a échoué.")
        return 1
    if branche != "main" and hash_de(cwd, "refs/heads/main"):
        sortie(git(cwd, "fetch", ".", "HEAD:refs/heads/main"))
    r = git(cwd, "fetch", "origin")
    sortie(r)
    head, om = etat(cwd, "après")
    distant = git(cwd, "ls-remote", "origin", "refs/heads/main").stdout.split()
    distant = distant[0] if distant else ""
    print(f"ls-remote origin main : {distant[:12] or '?'}")
    if head == om == distant:
        print("Poussé : origin/main == HEAD.")
        return 0
    print("Push non confirmé : origin/main différent de HEAD.")
    return 1


if __name__ == "__main__":
    sys.exit(fusion(essai="--essai" in sys.argv[1:]))
