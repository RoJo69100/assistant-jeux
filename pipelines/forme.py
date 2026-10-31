"""Hook Stop : refuse un plan « que faire » qui sort du format fixe.

Se déclenche seulement si la réponse contient un tableau dont l'en-tête commence par « Priorité ».
Contrôles : colonnes Priorité | Catégorie | Action ; chaque ligne commence par pastille carrée + mot
(🟥 URGENT / 🟧 IMPORTANT / 🟩 SUIVI) ; catégorie dans la liste fixe ; aucune ligne « rien à faire » ;
aucun interdit des tests docs/attentes/tests/*.yaml. Le texte entre « », "" ou `` est ignoré.
Règle : CLAUDE.md « Règles universelles de rendu » 1-2. Une seule relance (stop_hook_active).
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
PASTILLES = ["🟥 URGENT", "🟧 IMPORTANT", "🟩 SUIVI"]
CATEGORIES = ["composition", "tactique", "entrainement", "transferts", "academie/draft", "finances",
              "export", "question", "analyse"]
CITATION = re.compile(r"«[^»]*»|\"[^\"]*\"|“[^”]*”|`[^`]*`")
VIDE = re.compile(r"rien a faire|rien de special|aucune action")


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower().replace("’", "'"))
    return "".join(c for c in s if not unicodedata.combining(c))


def interdits() -> list[str]:
    vals = []
    for f in (RACINE / "docs/attentes/tests").glob("*.yaml"):
        for m in re.finditer(r"^interdits:\s*\[(.*)\]\s*$", f.read_text(encoding="utf-8"), re.M):
            vals += [a or b.strip() for a, b in re.findall(r'"([^"]*)"|([^,"]+)', m.group(1)) if a or b.strip()]
    return vals


def last_text(path: str) -> str:
    try:
        lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return ""
    for line in reversed(lines):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("type") != "assistant":
            continue
        parts = e.get("message", {}).get("content", [])
        text = "\n".join(p.get("text", "") for p in parts if isinstance(p, dict) and p.get("type") == "text")
        if text.strip():
            return text
    return ""


def fautes_de(text: str) -> list[str]:
    lignes = [l.strip() for l in text.splitlines() if l.strip().startswith("|")]
    entetes = [i for i, l in enumerate(lignes) if norm(l).startswith("| priorite")]
    if not entetes:
        return []
    fautes = []
    for i in entetes:
        cols = [c.strip() for c in norm(lignes[i]).strip("|").split("|")]
        if cols[:3] != ["priorite", "categorie", "action"]:
            fautes.append("colonnes attendues : Priorité | Catégorie | Action")
        for l in lignes[i + 2:]:
            if l.startswith("|---") or not l.startswith("|"):
                break
            cells = [c.strip() for c in l.strip("|").split("|")]
            if not any(cells[0].startswith(p) for p in PASTILLES):
                fautes.append(f"ligne sans pastille carrée + mot : {cells[0][:30]}")
            if len(cells) > 1 and norm(cells[1]) not in CATEGORIES:
                fautes.append(f"catégorie hors liste : {cells[1][:30]}")
            if VIDE.search(norm(l)):
                fautes.append("ligne « rien à faire »")
    n = norm(CITATION.sub(" ", text))
    fautes += [f"interdit : {i}" for i in interdits() if norm(i) in n]
    return list(dict.fromkeys(fautes))


def main() -> int:
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    data = json.load(sys.stdin)
    if data.get("stop_hook_active"):
        return 0
    text = data.get("last_assistant_message") or last_text(data.get("transcript_path", ""))
    fautes = fautes_de(CITATION.sub(lambda m: m.group(0) if "|" in m.group(0) else " ", text))
    if not fautes:
        return 0
    print(json.dumps({"decision": "block", "reason": (
        "Forme : plan hors format (" + " ; ".join(fautes) + "). Réécris-le : tableau Priorité | Catégorie | "
        "Action, chaque ligne commençant par 🟥 URGENT / 🟧 IMPORTANT / 🟩 SUIVI, catégories fixes "
        "(Composition, Tactique, Entraînement, Transferts, Académie/Draft, Finances, Export, Question, Analyse), "
        "aucune ligne « rien à faire », aucun interdit.")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
