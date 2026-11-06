"""Test de chargement des agents de .claude/agents/ (N11, rétro du 2026-11-06 : un « : » non cité dans
`description` a cassé 8 agents, signalés « introuvables »).

Contrôles par fichier : en-tête YAML lisible, `name` = nom du fichier, `description` texte non vide, `tools`
et `model` présents. Puis chaque type cité dans la section Agents de CLAUDE.md a son fichier.
Lancer : python pipelines/test_agents.py   (code 1 si un agent ne se charge pas ; aussi au pre-commit)
"""

import re
import sys
from pathlib import Path

import yaml

RACINE = Path(__file__).resolve().parent.parent
AGENTS = RACINE / ".claude" / "agents"
MODELES = {"sonnet", "opus", "haiku", "inherit"}


def entete(texte: str) -> dict:
    m = re.match(r"---\r?\n(.*?)\r?\n---", texte, re.S)
    if not m:
        raise ValueError("pas d'en-tête --- … ---")
    d = yaml.safe_load(m.group(1))
    if not isinstance(d, dict):
        raise ValueError("en-tête qui n'est pas un dictionnaire")
    return d


def fautes(chemin: Path) -> list[str]:
    try:
        d = entete(chemin.read_text(encoding="utf-8"))
    except (ValueError, yaml.YAMLError) as e:
        return [f"YAML illisible ({str(e).splitlines()[0]}) — mets `description` entre guillemets"]
    f = []
    if d.get("name") != chemin.stem:
        f.append(f"name « {d.get('name')} » ≠ nom du fichier")
    if not isinstance(d.get("description"), str) or not d["description"].strip():
        f.append("description absente ou pas du texte")
    if not d.get("tools"):
        f.append("tools absent")
    if d.get("model") not in MODELES:
        f.append(f"model « {d.get('model')} » hors {sorted(MODELES)}")
    return f


def types_claude_md() -> list[str]:
    texte = (RACINE / "CLAUDE.md").read_text(encoding="utf-8")
    m = re.search(r"Types propres dans `\.claude/agents/` \(([^)]*)\)", texte)
    return [t.strip() for t in m.group(1).split(",")] if m else []


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    echecs = 0
    for chemin in sorted(AGENTS.glob("*.md")):
        f = fautes(chemin)
        echecs += bool(f)
        print(("✅" if not f else "❌"), chemin.stem, "" if not f else "— " + " ; ".join(f))
    for t in types_claude_md():
        if not (AGENTS / f"{t}.md").exists():
            echecs += 1
            print("❌", t, "— cité dans CLAUDE.md, fichier absent")
    print(f"{echecs} échec(s)")
    sys.exit(1 if echecs else 0)
