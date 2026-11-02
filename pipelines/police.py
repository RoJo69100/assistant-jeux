"""Hook Stop / SubagentStop : refuse une réponse incomplète ou une décision rendue sans preuve.

Contrôles (plan docs/plan-conception-iso-basketvibe.md, étape 0a) :
  aveux  « pas tout lu », « non relevé »… ou « il me manque » sans « cherché dans : … »
         (règle docs/decisions/variables.md) — session et agents.
  H1     décision importante rendue sans dossier du jour : outputs/<jeu>/dossier/<date>-<type>.md
         ou `pipelines/dossier.py <jeu> <type>` lancé dans la session — session seulement.
  H2     décision importante sans trace police : outputs/<jeu>/police-<date>.md qui cite le type.
  H4     discussion de conception (hooks, scripts, refonte) : les aveux ne bloquent plus, sauf si
         la réponse rend aussi une décision de jeu (H1/H2 restent actifs).
  H5     plus de 5 demandes dans la session sans rétro proposée : rappel unique (rétro + optimisation).
Une décision importante = une ligne 🟥 URGENT / 🟧 IMPORTANT d'un tableau de plan dans les catégories
Composition, Tactique, Transferts, Entraînement, Académie/Draft, Finances, ou un tableau de saisie
(tactique, entraînement, adversaires, composition Team Soccer). Le texte entre « », "", `` ou ``` est ignoré.
Une seule relance par réponse (stop_hook_active).
"""

import json
import re
import sys
import tempfile
import unicodedata
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import forme  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent

INTERDITS = [
    "pas tout lu", "pas encore lu", "non lu", "je n'ai pas lu", "pas pu lire", "lu a moitie",
    "lu partiellement", "partiellement lu", "lecture partielle", "non releve", "pas releve",
    "pas eu le temps", "survol", "lu un echantillon", "sur un echantillon", "a lire plus tard",
    "reste a lire", "non exploite", "pas exploite", "les premiers messages", "pas tout parcouru",
]
MANQUE = re.compile(r"il me manqu|donnees? manquantes?|manque de donnees|faute de donnees")
PREUVE = "cherche dans"
CODE = re.compile(r"```.*?```", re.S)
CITATION = re.compile(r"«[^»]*»|\"[^\"]*\"|“[^”]*”|`[^`]*`")
CONCEPTION = re.compile(r"\bconc(ep|oi|ev)|\bhooks?\b|\brefonte\b|plan de conception|\betape 0")

JEUX = {
    "basketvibe": ["basketvibe"],
    "hockeynation": ["hockey nation", "hockeynation"],
    "teamsoccer": ["team soccer", "teamsoccer", "chomelix", "ben ahmed"],
    "sixzeroleague": ["six zero", "sixzero"],
    "derbymanager": ["derby manager", "derbymanager"],
    "hardwood": ["hardwood"],
}
CAT_TYPE = {"composition": "composition", "tactique": "composition", "entrainement": "entrainement",
            "academie/draft": "academie", "finances": "finances"}
VENTE = re.compile(r"\bvend|\bvente\b|\bliber")
SEUIL_H5 = 5


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower().replace("’", "'"))
    return "".join(c for c in s if not unicodedata.combining(c))


def nettoie(text: str) -> str:
    return norm(CITATION.sub(" ", CODE.sub(" ", text)))


def entrees(path: str) -> list[dict]:
    try:
        lignes = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    except (OSError, TypeError):
        return []
    res = []
    for l in lignes:
        try:
            res.append(json.loads(l))
        except ValueError:
            continue
    return res


def last_text(ents: list[dict]) -> str:
    for e in reversed(ents):
        if e.get("type") != "assistant":
            continue
        parts = e.get("message", {}).get("content", [])
        text = "\n".join(p.get("text", "") for p in parts if isinstance(p, dict) and p.get("type") == "text")
        if text.strip():
            return text
    return ""


def demandes(ents: list[dict]) -> list[str]:
    """Messages tapés par l'utilisateur (ni résultats d'outils, ni commandes, ni rappels système)."""
    res = []
    for e in ents:
        if e.get("type") != "user" or e.get("isMeta"):
            continue
        c = e.get("message", {}).get("content")
        if isinstance(c, list):
            if any(isinstance(p, dict) and p.get("type") == "tool_result" for p in c):
                continue
            c = "\n".join(p.get("text", "") for p in c if isinstance(p, dict) and p.get("type") == "text")
        if isinstance(c, str) and c.strip() and not c.lstrip().startswith("<"):
            res.append(c)
    return res


def commandes(ents: list[dict]) -> str:
    """Toutes les entrées d'outils de la session, à plat (pour retrouver dossier.py et le jeu)."""
    morceaux = []
    for e in ents:
        if e.get("type") != "assistant":
            continue
        for p in e.get("message", {}).get("content", []):
            if isinstance(p, dict) and p.get("type") == "tool_use":
                morceaux.append(json.dumps(p.get("input", {}), ensure_ascii=False))
    return "\n".join(morceaux)


def decisions(text: str) -> set[str]:
    """Types de décision importante rendus dans la réponse."""
    types = set()
    for cols, lignes in forme.tableaux(text):
        if not cols or not lignes:
            continue
        j = " ".join(cols)
        if cols[0] == "priorite" and len(cols) > 2 and cols[1] == "categorie":
            for c in lignes:
                if len(c) < 3 or not c[0].replace("*", "").startswith(("🟥", "🟧")):
                    continue
                cat = forme.norm(c[1])
                if cat == "transferts":
                    types.add("vente" if VENTE.search(norm(c[2])) else "achat")
                elif cat in CAT_TYPE:
                    types.add(CAT_TYPE[cat])
        elif cols[0] == "joueur" and (forme.idx(cols, "principale") >= 0 or forme.idx(cols, "a mettre") >= 0):
            types.add("entrainement")
        elif (cols[0] == "joueur" and forme.idx(cols, "q1") >= 0) or "adversaire" in cols[0] \
                or forme.idx(cols, "ultra") >= 0 or ("empl" in j and forme.idx(cols, "finition") >= 0):
            types.add("composition")
    return types


def jeu_de(text: str, cmds: str) -> str | None:
    n = norm(text)
    vus = [j for j, noms in JEUX.items() if any(x in n for x in noms)]
    if len(vus) == 1:
        return vus[0]
    trouves = re.findall(r"outputs[/\\](\w+)[/\\]|game\s*=\s*'(\w+)'|dossier\.py\s+(\w+)", cmds)
    for t in reversed(trouves):
        g = next(x for x in t if x)
        if g in JEUX:
            return g
    return None


def jours() -> list[str]:
    return sorted({date.today().isoformat(), datetime.now(timezone.utc).date().isoformat()})


def dossier_fait(jeu: str, type_: str, cmds: str) -> bool:
    if re.search(rf"dossier\.py\s+{jeu}\s+{type_}\b", cmds):
        return True
    return any((RACINE / f"outputs/{jeu}/dossier/{d}-{type_}.md").exists() for d in jours())


def police_faite(jeu: str, type_: str) -> bool:
    for d in jours():
        p = RACINE / f"outputs/{jeu}/police-{d}.md"
        if p.exists() and type_ in norm(p.read_text(encoding="utf-8", errors="replace")):
            return True
    return False


def h5_du(session: str, nb: int, n: str) -> bool:
    """Rappel de fin de session, une seule fois par session."""
    if nb <= SEUIL_H5 or "retro" in n or not session:
        return False
    marque = Path(tempfile.gettempdir()) / f"claude-police-h5-{re.sub(r'[^A-Za-z0-9_-]', '', session)}"
    if marque.exists():
        return False
    try:
        marque.write_text(date.today().isoformat(), encoding="utf-8")
    except OSError:
        return False
    return True


def fautes_de(text: str, ents: list[dict], principal: bool, session: str = "") -> list[str]:
    n = nettoie(text)
    dem = demandes(ents)
    cmds = commandes(ents)
    types = decisions(text) if principal else set()
    conception = any(CONCEPTION.search(norm(d)) for d in dem)
    f = []
    if not (conception and not types):
        f += [p for p in INTERDITS if p in n]
        if MANQUE.search(n) and PREUVE not in n:
            f.append("« il me manque » sans « cherché dans : <sources> »")
    jeu = jeu_de(text, cmds) if types else None
    for t in sorted(types):
        if not jeu:
            break
        if not dossier_fait(jeu, t, cmds):
            f.append(f"H1 : décision {t} ({jeu}) sans dossier — lance `python pipelines/dossier.py {jeu} {t}`")
        if not police_faite(jeu, t):
            f.append(f"H2 : décision {t} ({jeu}) sans trace police — agent `police`, qui écrit "
                     f"outputs/{jeu}/police-{date.today().isoformat()}.md")
    if principal and h5_du(session, len(dem), n):
        f.append(f"H5 : {len(dem)} demandes dans la session — termine par une ligne qui propose la rétro "
                 "(agent `retro`) et la mesure `python pipelines/mesure_session.py` avant `/clear`")
    return f


def main() -> int:
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    data = json.load(sys.stdin)
    if data.get("stop_hook_active"):
        return 0
    principal = data.get("hook_event_name", "Stop") == "Stop"
    ents = entrees(data.get("transcript_path", ""))
    agent = entrees(data.get("agent_transcript_path", "")) if not principal else ents
    text = data.get("last_assistant_message") or last_text(agent)
    fautes = fautes_de(text, ents, principal, data.get("session_id", ""))
    if not fautes:
        return 0
    if all(x.startswith("H5") for x in fautes):
        raison = "Police : " + fautes[0] + "."
    else:
        raison = ("Police : réponse incomplète (" + " ; ".join(fautes) + "). Ne rends pas cette réponse : "
                  "lance le dossier (`python pipelines/dossier.py <jeu> <type>`), l'agent `police` sur la décision, "
                  "lis ce qui reste (Discord/chat, connaissance, vues gold, bronze brut), complète chaque variable "
                  "de docs/decisions/variables.md, puis réécris la réponse. Un manque réel s'écrit : "
                  "« il me manque X — cherché dans : … — on le réunit comme ça : … ».")
    print(json.dumps({"decision": "block", "reason": raison}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
