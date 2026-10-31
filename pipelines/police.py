"""Hook Stop / SubagentStop : refuse une réponse qui avoue une lecture incomplète.

Lit la dernière réponse (de la session ou de l'agent) et la bloque si elle contient une phrase
interdite (« pas tout lu », « non relevé »…) ou un manque (« il me manque ») sans la preuve
« cherché dans : … ». Le texte entre « », "" ou `` est ignoré (citations de règles).
Règle : docs/decisions/variables.md. Une seule relance par réponse (stop_hook_active).
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

INTERDITS = [
    "pas tout lu", "pas encore lu", "non lu", "je n'ai pas lu", "pas pu lire", "lu a moitie",
    "lu partiellement", "partiellement lu", "lecture partielle", "non releve", "pas releve",
    "pas eu le temps", "survol", "lu un echantillon", "sur un echantillon", "a lire plus tard",
    "reste a lire", "non exploite", "pas exploite", "les premiers messages", "pas tout parcouru",
]
MANQUE = re.compile(r"il me manqu|donnees? manquantes?|manque de donnees|faute de donnees")
PREUVE = "cherche dans"
CITATION = re.compile(r"«[^»]*»|\"[^\"]*\"|“[^”]*”|`[^`]*`")


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower().replace("’", "'"))
    return "".join(c for c in s if not unicodedata.combining(c))


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


def main() -> int:
    data = json.load(sys.stdin)
    if data.get("stop_hook_active"):
        return 0
    text = data.get("last_assistant_message") or last_text(
        data.get("agent_transcript_path") or data.get("transcript_path", ""))
    n = norm(CITATION.sub(" ", text))
    fautes = [p for p in INTERDITS if p in n]
    if MANQUE.search(n) and PREUVE not in n:
        fautes.append("« il me manque » sans « cherché dans : <sources> »")
    if not fautes:
        return 0
    print(json.dumps({"decision": "block", "reason": (
        "Police : réponse incomplète (" + " ; ".join(fautes) + "). Ne rends pas cette réponse : lis ce qui "
        "reste (dossier `python pipelines/dossier.py <jeu> <type>`, Discord/chat, connaissance, vues gold, "
        "bronze brut), complète chaque variable de docs/decisions/variables.md, puis réécris la réponse. "
        "Un manque réel s'écrit : « il me manque X — cherché dans : … — on le réunit comme ça : … ».")},
        ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
