"""Hook PreToolUse / PostToolUse : un push n'est « poussé » que si git le confirme.

Conçu le 2026-11-03 (rétro : `git push -q` échouait faute de suivi distant, sortie non lue, succès supposé).
  PreToolUse   refuse `git push -q` / `--quiet` (la sortie doit rester lisible).
  PostToolUse  après un `git push`, lit `git status -sb` : pas de branche distante suivie ou commits
               en avance = push non confirmé, message renvoyé à Claude (code 2).
Outils surveillés : Bash et PowerShell. Tests : test_garde_push.py.
"""

import json
import re
import subprocess
import sys

PUSH = re.compile(r"\bgit\s+(?:-C\s+\S+\s+)?push\b")
MUET = re.compile(r"\bgit\s+(?:-C\s+\S+\s+)?push\b[^;&|\n]*\s(?:-q|--quiet)\b")


def statut_branche() -> str:
    sortie = subprocess.run(["git", "status", "-sb"], capture_output=True, text=True, encoding="utf-8")
    return sortie.stdout.splitlines()[0] if sortie.stdout else ""


def verdict(evenement: str, commande: str, statut: str | None = None) -> str | None:
    """Message de refus, ou None si rien à signaler."""
    if not PUSH.search(commande):
        return None
    if evenement == "PreToolUse":
        if MUET.search(commande):
            return "Refusé : retire -q/--quiet, la sortie doit être lue."
        return None
    if evenement == "PostToolUse":
        statut = statut_branche() if statut is None else statut
        if "..." not in statut:
            return f"Push non confirmé : aucune branche distante suivie ({statut}). Utiliser `git push -u origin <branche>`."
        if "[ahead" in statut:
            return f"Push non confirmé : {statut}. Ne pas écrire « poussé »."
    return None


def main() -> int:
    try:
        entree = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    if entree.get("tool_name") not in ("Bash", "PowerShell"):
        return 0
    commande = (entree.get("tool_input") or {}).get("command", "")
    message = verdict(entree.get("hook_event_name", ""), commande)
    if message:
        sys.stderr.reconfigure(encoding="utf-8")
        print(message, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
