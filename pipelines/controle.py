"""Hook Stop : contrôleur de sortie des règles globales de CLAUDE.md jusqu'ici non contrôlées par code.

Conçu le 2026-11-02 (rétro du soir, tâche S7 : « le rappel de début de session informe, il ne bloque pas »).
Contrôles sur la réponse finale de la session principale :
  a  modèle     fichiers de conception modifiés dans la session (sql/, .claude/agents/, docs/fiches/,
                pipelines/, .claude/settings.json) sans rappel du modèle : « /model opus » si la session
                n'est pas sur Opus, « /model sonnet » (retour après le commit) si elle l'est.
  b  deja-fait  tableau de plan (Priorité | Catégorie | Action) sans le skill `deja-fait` chargé dans le tour.
  c  preuve     tableau chiffré sans source dans le tour : requête SQL, fichier lu ou agent `synthese`.
  d  tranche    phrase fermée : « veux-tu que », « oui ou non », « à toi de voir », « peut-être »…
  e  concision  réponse de conception de plus de 15 lignes hors tableaux et code, ou identifiant interne
                (R-1, G3, « règle 75 ») dans une réponse de conception.
  f  horizon    plan dont une cellule Action reporte (« demain matin », « la semaine prochaine », « plus tard »…).
  g  preuve     « je ne peux pas » sans « je ne sais pas encore » ni preuve.
  h  agent      agent lancé sans type propre (general-purpose), sauf si la réponse dit « introuvable ».
  i  Write      fichier écrit par heredoc dans le terminal (Bash ou PowerShell).
Le texte entre « », "", `` ou ``` est ignoré. Une seule relance (stop_hook_active). Tests : test_controle.py.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import forme  # noqa: E402
import police  # noqa: E402

CHEMINS_CONCEPTION = re.compile(r"(^|[/\\])(sql|pipelines|\.claude[/\\]agents|docs[/\\]fiches)[/\\]|\.claude[/\\]settings\.json$")
FERMEES = [
    "veux-tu", "voulez-vous", "souhaites-tu", "souhaitez-vous", "tu veux que je", "vous voulez que je",
    "dois-je", "je lance ?", "je continue ?", "oui ou non", "oui/non", "a toi de voir", "a vous de voir",
    "je te laisse choisir", "je te laisse decider", "a toi de choisir", "dis-moi si", "peut-etre",
]
IDENTIFIANT = re.compile(r"\b[RAGHSE]-?\d{1,2}\b")
REGLE_N = re.compile(r"\bregles? (apprises? )?\d{1,3}\b")
SEUIL_LIGNES = 15
CHIFFRE = re.compile(r"\d")
SQL = re.compile(r"\bpsql\b|\bselect\b[\s\S]+\bfrom\b", re.I)
LECTURE = re.compile(r"\b(cat|head|tail|sed|grep|rg|wc)\b")


def tour(ents: list[dict]) -> list[dict]:
    """Entrées depuis la dernière demande tapée par l'utilisateur."""
    debut = 0
    for i, e in enumerate(ents):
        if police.demandes([e]):
            debut = i
    return ents[debut:]


def outils(ents: list[dict]) -> list[tuple[str, dict]]:
    res = []
    for e in ents:
        if e.get("type") != "assistant":
            continue
        for p in e.get("message", {}).get("content", []):
            if isinstance(p, dict) and p.get("type") == "tool_use":
                res.append((p.get("name", ""), p.get("input", {}) or {}))
    return res


def textes(ents: list[dict]) -> str:
    morceaux = []
    for e in ents:
        if e.get("type") == "assistant":
            morceaux += [p.get("text", "") for p in e.get("message", {}).get("content", [])
                         if isinstance(p, dict) and p.get("type") == "text"]
    return "\n".join(morceaux)


def modele(ents: list[dict]) -> str:
    for e in reversed(ents):
        m = e.get("message", {}).get("model") if e.get("type") == "assistant" else None
        if m:
            return m.lower()
    return ""


def conception_modifiee(ops: list[tuple[str, dict]]) -> bool:
    return any(nom in ("Edit", "Write", "MultiEdit", "NotebookEdit")
               and CHEMINS_CONCEPTION.search(str(inp.get("file_path", "")).replace("\\", "/"))
               for nom, inp in ops)


def deja_fait(ops: list[tuple[str, dict]]) -> bool:
    return any(nom == "Skill" and "deja-fait" in str(inp.get("skill", "")) for nom, inp in ops)


def source(ops: list[tuple[str, dict]]) -> bool:
    for nom, inp in ops:
        if "execute_sql" in nom or nom in ("Read", "Grep"):
            return True
        if nom == "Agent" and inp.get("subagent_type") == "synthese":
            return True
        if nom == "Bash" and (SQL.search(inp.get("command", "")) or LECTURE.search(inp.get("command", ""))):
            return True
    return False


def chiffre(text: str) -> bool:
    return any(CHIFFRE.search(" ".join(c)) for _, lignes in forme.tableaux(text) for c in lignes)


def lignes_hors_tableau(text: str) -> int:
    sans_code = police.CODE.sub("", text)
    return sum(1 for l in sans_code.splitlines() if l.strip() and not l.strip().startswith("|"))


REPORT = [
    "demain matin", "demain soir", "a faire demain", "fais demain", "apres-demain", "apres demain",
    "la semaine prochaine", "plus tard", "apres le prochain match", "ce week-end", "le mois prochain",
]
NE_PEUT_PAS = ["je ne peux pas", "je n'ai pas la possibilite", "impossible pour moi"]
ISSUE = ["je ne sais pas encore", "je le trouve", "preuve"]
HEREDOC = re.compile(r"<<-?\s*['\"]?\w+['\"]?")
ECRIT_FICHIER = re.compile(r"\b(cat|tee)\b[^\n|]*>|>>?\s*[\w./~\\-]+\s*<<|write_text\(|open\([^)]*['\"][wa]b?['\"]")


def reports(text: str) -> list[str]:
    """Phrases de report (horizon) dans les cellules « Action » des tableaux de plan (règle E1 de actives.md)."""
    trouves = []
    for cols, lignes in forme.tableaux(text):
        if forme.idx(cols, "action") < 0:
            continue
        ia = forme.idx(cols, "action")
        for l in lignes:
            cellule = police.norm(l[ia]) if ia < len(l) else ""
            trouves += [p for p in REPORT if p in cellule]
    return sorted(set(trouves))


def heredoc_ecrit(ops: list[tuple[str, dict]]) -> bool:
    for nom, inp in ops:
        cmd = str(inp.get("command", ""))
        if nom in ("Bash", "PowerShell") and HEREDOC.search(cmd) and ECRIT_FICHIER.search(cmd):
            return True
    return False


def agent_general(ops: list[tuple[str, dict]]) -> bool:
    return any(nom in ("Agent", "Task") and inp.get("subagent_type", "general-purpose") == "general-purpose"
               for nom, inp in ops)


def fautes_de(text: str, ents: list[dict]) -> list[str]:
    n = police.nettoie(text)
    t = tour(ents)
    ops_session, ops_tour = outils(ents), outils(t)
    dem = police.demandes(t)
    conception = bool(dem) and bool(police.CONCEPTION.search(police.norm(dem[-1]))) or conception_modifiee(ops_tour)
    f = []
    if conception_modifiee(ops_session):
        dit = police.norm(textes(ents) + "\n" + text)
        attendu = "/model sonnet" if "opus" in modele(ents) else "/model opus"
        if attendu not in dit:
            f.append(f"a : fichiers de conception modifiés sans rappel « {attendu} » — dis-le en une ligne "
                     "(« /model opus avant, /model sonnet après le commit »)")
    if forme.a_plan(text) and not deja_fait(ops_tour):
        f.append("b : tableau de plan sans le skill `deja-fait` chargé dans ce tour")
    if chiffre(text) and not source(ops_tour):
        f.append("c : tableau chiffré sans requête SQL, fichier lu ou `synthese` dans ce tour")
    f += [f"d : phrase fermée « {p} » — tranche (« fais X »), doute en une demi-ligne après" for p in FERMEES if p in n]
    if forme.a_plan(text) and reports(text):
        f.append("f : action reportée (" + ", ".join(reports(text)) + ") — horizon = aujourd'hui seulement, "
                 "ce qui n'est pas faisable ce soir n'est pas écrit")
    if any(p in n for p in NE_PEUT_PAS) and not any(p in n for p in ISSUE):
        f.append("g : « je ne peux pas » sans preuve — donne la mesure ou « je ne sais pas encore, je le trouve ainsi : <commande> »")
    if agent_general(ops_tour) and "introuvable" not in n:
        f.append("h : agent lancé en general-purpose — utilise le type propre de .claude/agents/ "
                 "(ou dis que le type est introuvable)")
    if heredoc_ecrit(ops_tour):
        f.append("i : fichier écrit par heredoc dans le terminal — utilise l'outil Write")
    if conception:
        nb = lignes_hors_tableau(text)
        if nb > SEUIL_LIGNES:
            f.append(f"e : réponse de conception de {nb} lignes (max {SEUIL_LIGNES}) — une phrase de résultat, 5 lignes")
        brut = police.CITATION.sub(" ", police.CODE.sub(" ", text))
        ids = sorted({m.group(0) for m in IDENTIFIANT.finditer(brut)} | {m.group(0) for m in REGLE_N.finditer(n)})
        if ids:
            f.append("e : identifiants internes (" + ", ".join(ids[:5]) + ") — dis ce qu'ils veulent dire en mots")
    return f


def main() -> int:
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    data = json.load(sys.stdin)
    if data.get("stop_hook_active") or data.get("hook_event_name", "Stop") != "Stop":
        return 0
    ents = forme.entrees(data.get("transcript_path", ""))
    text = data.get("last_assistant_message") or police.last_text(ents)
    fautes = fautes_de(text, ents)
    if fautes:
        print(json.dumps({"decision": "block", "reason": "Contrôle de sortie : " + " ; ".join(fautes) + "."},
                         ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
