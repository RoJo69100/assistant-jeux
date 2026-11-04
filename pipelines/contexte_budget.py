"""Budget de contexte (refonte v2, 0.5) : tokens ≈ caractères / 3,6.

Usage : python -I pipelines/contexte_budget.py [--figer] [--json]
Budgets (échec si dépassé) : CLAUDE.md 2 500 · actives.md 1 500 · agent 1 500 · resume.md 1 000 · corps de SKILL.md 1 000 ·
total « session de jeu » 6 000 (CLAUDE.md + actives.md + sortie du hook de début + descriptions des skills + resume.md du jeu).
Dette connue : docs/regles/budget-dette.json fige la taille actuelle des fichiers déjà trop gros ; ils ne peuvent plus grossir.
`--figer` réécrit ce fichier avec les tailles actuelles (à utiliser seulement pour constater une dette, jamais pour la creuser).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
CAR_PAR_JETON = 3.6
BUDGET = {"claude": 2500, "actives": 1500, "agent": 1500, "resume": 1000, "skill": 1000, "session": 6000}
DETTE = RACINE / "docs" / "regles" / "budget-dette.json"


def jetons(texte: str) -> int:
    return round(len(texte) / CAR_PAR_JETON)


def lire(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def corps(texte: str) -> str:
    m = re.match(r"^---\n.*?\n---\n(.*)$", texte, re.S)
    return m.group(1) if m else texte


def description(texte: str) -> str:
    nom = re.search(r"(?m)^name:\s*(.*)$", texte)
    d = re.search(r"(?m)^description:\s*(.*)$", texte)
    return f"{nom.group(1) if nom else ''}: {d.group(1) if d else ''}"


def hook_debut() -> str:
    r = subprocess.run([sys.executable, "-I", str(RACINE / "pipelines" / "rappel_debut.py")],
                       capture_output=True, encoding="utf-8", errors="replace", cwd=RACINE)
    return r.stdout


def mesures(racine: Path = RACINE) -> tuple[dict, dict]:
    """(fichiers, sessions) : fichiers = {chemin: (jetons, budget)}, sessions = {jeu: jetons}."""
    f = {}
    f["CLAUDE.md"] = (jetons(lire(racine / "CLAUDE.md")), BUDGET["claude"])
    f["docs/regles/actives.md"] = (jetons(lire(racine / "docs/regles/actives.md")), BUDGET["actives"])
    for a in sorted((racine / ".claude/agents").glob("*.md")):
        f[a.relative_to(racine).as_posix()] = (jetons(lire(a)), BUDGET["agent"])
    resumes = {}
    for r in sorted((racine / "docs/fiches").glob("*/resume.md")):
        t = jetons(lire(r))
        f[r.relative_to(racine).as_posix()] = (t, BUDGET["resume"])
        resumes[r.parent.name] = t
    desc = 0
    for s in sorted((racine / ".claude/skills").glob("*/SKILL.md")):
        txt = lire(s)
        desc += jetons(description(txt))
        f[s.relative_to(racine).as_posix()] = (jetons(corps(txt)), BUDGET["skill"])
    fixe = f["CLAUDE.md"][0] + f["docs/regles/actives.md"][0] + jetons(hook_debut()) + desc
    sessions = {jeu: fixe + t for jeu, t in resumes.items()}
    return f, sessions


def verifie(fichiers: dict, sessions: dict, dette: dict) -> list[str]:
    fautes = []
    for chemin, (t, b) in fichiers.items():
        if t > max(b, dette.get(chemin, 0)):
            fautes.append(f"{chemin} : {t} jetons (budget {b}, toléré {dette.get(chemin, b)})")
    for jeu, t in sessions.items():
        cle = f"session:{jeu}"
        if t > max(BUDGET["session"], dette.get(cle, 0)):
            fautes.append(f"{cle} : {t} jetons (budget {BUDGET['session']}, toléré {dette.get(cle, BUDGET['session'])})")
    return fautes


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    fichiers, sessions = mesures()
    dette = json.loads(DETTE.read_text(encoding="utf-8")) if DETTE.exists() else {}
    if "--figer" in sys.argv:
        nouv = {c: t for c, (t, b) in fichiers.items() if t > b}
        nouv.update({f"session:{j}": t for j, t in sessions.items() if t > BUDGET["session"]})
        DETTE.write_text(json.dumps(nouv, indent=1, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
        print(f"dette figée : {len(nouv)} entrées -> {DETTE.relative_to(RACINE).as_posix()}")
        return 0
    if "--json" in sys.argv:
        print(json.dumps({"fichiers": {c: t for c, (t, _) in fichiers.items()}, "sessions": sessions}, ensure_ascii=False, indent=1))
        return 0
    trop = {c: (t, b) for c, (t, b) in fichiers.items() if t > b}
    print(f"fichiers mesurés : {len(fichiers)} ; au-dessus du budget : {len(trop)} (dette)")
    for c, (t, b) in sorted(trop.items(), key=lambda x: -x[1][0])[:12]:
        print(f"  {t:>6} / {b}  {c}")
    print("session de jeu (jetons, budget 6000) : " + ", ".join(f"{j} {t}" for j, t in sorted(sessions.items())))
    fautes = verifie(fichiers, sessions, dette)
    for x in fautes:
        print("❌ " + x)
    print("✅ budget respecté (hors dette figée)" if not fautes else f"{len(fautes)} dépassement(s)")
    return 1 if fautes else 0


if __name__ == "__main__":
    sys.exit(main())
