"""Hook PreToolUse Bash : un fichier s'écrit avec l'outil Write, jamais par heredoc (inviolable 8).

Conçu le 2026-11-09 (critère T1, journal-aujourdhui.md « Garde-fous mécaniques »).
Refuse un heredoc (`<<DELIM`, `<<-DELIM`, `<< 'DELIM'`) quand son segment de commande
  - contient une redirection vers un fichier (`>`, `>>`, hors `>&N` et `/dev/null`), ou
  - lance python / cat / tee.
Accepte `git commit -m "$(cat <<'EOF' ... EOF)"` (message de commit, aucun fichier écrit).
Le corps du heredoc n'est jamais analysé (un `>` dans un message de commit ne compte pas).
Tests : test_garde_heredoc.py.
"""

import json
import re
import sys

MESSAGE = "Refusé : heredoc qui écrit un fichier, écris le fichier avec Write."

OUVRANT = re.compile(r"(?<!<)<<(?!<)(-?)[ \t]*(['\"]?)([A-Za-z_][\w.-]*)\2")
COMMIT_SUBST = re.compile(r"\bgit\s+(?:-C\s+\S+\s+)?commit\b.*\$\(\s*cat\s*$")
SEP_GAUCHE = re.compile(r".*(?:;|&&|\|\||\||\$\(|\(|\{|`)")
SEP_DROITE = re.compile(r"(?:;|&|\||\)|`)")
REDIRECTION = re.compile(r">{1,2}(?!&)\s*([^\s;&|()<>]+)")
ECRIVAINS = re.compile(r"^(?:python[\d.]*|py|cat|tee)$")
PREFIXES = {"sudo", "env", "command", "exec", "time", "nohup"}


def ouvrants(commande: str) -> list[tuple[str, int, int]]:
    """(ligne, début, fin) de chaque heredoc, hors corps des heredocs."""
    trouves, attente = [], []
    for ligne in commande.split("\n"):
        if attente:
            delim, tabs = attente[0]
            if (ligne.lstrip("\t") if tabs else ligne).strip() == delim:
                attente.pop(0)
            continue
        for m in OUVRANT.finditer(ligne):
            trouves.append((ligne, m.start(), m.end()))
            attente.append((m.group(3), m.group(1) == "-"))
    return trouves


def mot_commande(texte: str) -> str:
    for jeton in texte.split():
        if "=" in jeton.split("/")[0] or jeton in PREFIXES:
            continue
        if jeton.startswith(">") or jeton.startswith("<"):
            continue
        return jeton.rsplit("/", 1)[-1]
    return ""


def ecrit_fichier(ligne: str, debut: int, fin: int) -> bool:
    gauche, droite = ligne[:debut], ligne[fin:]
    if COMMIT_SUBST.search(gauche):
        return False
    m = SEP_GAUCHE.match(gauche)
    gauche = gauche[m.end():] if m else gauche
    m = SEP_DROITE.search(droite)
    droite = droite[: m.start()] if m else droite
    segment = f"{gauche} {droite}"
    if any(cible != "/dev/null" for cible in REDIRECTION.findall(segment)):
        return True
    mot = mot_commande(gauche) or mot_commande(droite)
    return bool(ECRIVAINS.match(mot))


def verdict(commande: str) -> str | None:
    """Message de refus, ou None si la commande est acceptée."""
    if "<<" not in commande:
        return None
    if any(ecrit_fichier(*o) for o in ouvrants(commande)):
        return MESSAGE
    return None


def main() -> int:
    try:
        entree = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    if entree.get("tool_name") != "Bash":
        return 0
    message = verdict((entree.get("tool_input") or {}).get("command", ""))
    if message:
        sys.stderr.reconfigure(encoding="utf-8")
        print(message, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
