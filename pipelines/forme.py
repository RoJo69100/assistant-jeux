"""Hook Stop : refuse une réponse dont un tableau sort du format fixe validé par l'utilisateur.

Le hook lit tous les tableaux Markdown de la dernière réponse, reconnaît chaque format par son
en-tête et le contrôle. Un tableau d'un format inconnu passe ; une réponse sans tableau passe.
Formats contrôlés (sources : CLAUDE.md « Règles universelles de rendu », attentes R-12, mémoire
feedback-*) :
  plan          Priorité | Catégorie | Action — pastille carrée + mot, catégories fixes, pas de « rien à faire »
  entrainement  Joueur | Principale | Secondaire (tous, ordre de l'export) ou Joueur | Actuel | À mettre
                (seulement ceux qui changent) — ordre de docs/ordre-export/<jeu>-entrainement.json
  tactique      Joueur | Poste | Q1–Q4 | Prol. | Minutes | Off. focus | Rôle | Tir | Agress. (postes PG→C)
  adversaires   Adversaire | Poste | Focus défensif (1–5) | Zone (Rim/Middle/Perimeter), une ligne par joueur
  hw-tactique   Réglage | Actuel | À mettre — Pace, Inside/Outside, Zone, Pressure, Extend
  hw-recrues    Priorité | Poste | Cible | Remplaçant 1 | Remplaçant 2 — 4 lignes, jamais « High »
  ts-compo      empl. × Ultra déf./Défensive/Médiane/Offensive/Finition + « Remplacements programmés »,
                cible obligatoire après « Passer », les deux clubs
  hn-effectif   Poste | Joueur | Note | Endurance | FOF ; hn-plan : Paramètre | Cible | Dans le jeu
Dans tous les cas : aucun interdit des tests docs/attentes/tests/*.yaml. Le texte entre « », "" ou `` est ignoré.
Une seule relance (stop_hook_active).
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
POSTES = ["pg", "sg", "sf", "pf", "c"]
ZONES = ["rim", "middle", "perimeter"]
CITATION = re.compile(r"«[^»]*»|\"[^\"]*\"|“[^”]*”|`[^`]*`")
VIDE = re.compile(r"rien a faire|rien de special|aucune action")


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower().replace("’", "'").replace("*", ""))
    return "".join(c for c in s if not unicodedata.combining(c)).strip()


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


def tableaux(text: str) -> list[tuple[list[str], list[list[str]]]]:
    """(en-tête normalisé, lignes brutes) de chaque tableau Markdown."""
    res, bloc = [], []
    for l in text.splitlines() + [""]:
        if l.strip().startswith("|"):
            bloc.append(l.strip())
            continue
        if len(bloc) >= 2:
            cell = lambda r: [c.strip() for c in r.strip("|").split("|")]
            lignes = [cell(r) for r in bloc[2:] if not re.fullmatch(r"[|\s:-]+", r)]
            res.append(([norm(c) for c in cell(bloc[0])], lignes))
        bloc = []
    return res


def idx(cols: list[str], *cles: str) -> int:
    for i, c in enumerate(cols):
        if any(k in c for k in cles):
            return i
    return -1


def ordre_ok(noms: list[str], ref: list[str]) -> bool:
    """Les noms connus apparaissent dans l'ordre de la référence."""
    pos = [ref.index(n) for n in noms if n in ref]
    return pos == sorted(pos)


def plan(cols, lignes):
    f = []
    if cols[:3] != ["priorite", "categorie", "action"]:
        f.append("plan : colonnes attendues Priorité | Catégorie | Action")
    for c in lignes:
        if not any(c[0].replace("*", "").startswith(p) for p in PASTILLES):
            f.append(f"plan : ligne sans pastille carrée + mot ({c[0][:25]})")
        if len(c) > 1 and norm(c[1]) not in CATEGORIES:
            f.append(f"plan : catégorie hors liste ({c[1][:25]})")
        if VIDE.search(norm(" ".join(c))):
            f.append("plan : ligne « rien à faire »")
    return f


def entrainement(cols, lignes, jeu="basketvibe"):
    f, ref = [], []
    p = RACINE / f"docs/ordre-export/{jeu}-entrainement.json"
    if p.exists():
        ref = json.loads(p.read_text(encoding="utf-8"))["noms"]
    complet = idx(cols, "principale") >= 0
    if not complet and (idx(cols, "actuel") < 0 or idx(cols, "a mettre") < 0):
        return ["entraînement : colonnes attendues Joueur | Principale | Secondaire (tous) ou Joueur | Actuel | À mettre (changements)"]
    noms = [c[0].replace("*", "").strip() for c in lignes]
    if ref and not ordre_ok(noms, ref):
        f.append("entraînement : joueurs pas dans l'ordre de l'export (" + ", ".join(ref[:4]) + "…)")
    if not complet:
        i, j = idx(cols, "actuel"), idx(cols, "a mettre")
        f += [f"entraînement : {c[0]} ne change pas (garde seulement ceux qui changent)"
              for c in lignes if norm(c[i]) == norm(c[j])]
    elif ref and len(lignes) < len(ref) and len(lignes) > 0:
        f.append(f"entraînement : {len(lignes)} joueurs sur {len(ref)} dans un tableau « tous » ; "
                 "rends tous les joueurs, ou le tableau Actuel | À mettre des seuls changements")
    return f


def ordre_postes(lignes, ip, in_=0):
    f, prev = [], (-1, "")
    for c in lignes:
        poste = norm(c[ip]).split("/")[0].strip()
        if poste not in POSTES:
            f.append(f"poste inconnu ({c[ip][:10]})")
            continue
        cle = (POSTES.index(poste), norm(c[in_]))
        if cle < prev:
            f.append(f"ordre PG→C puis alphabétique rompu à {c[in_][:20]}")
            break
        prev = cle
    return f


def tactique(cols, lignes):
    f = []
    for k in ["poste", "q1", "q2", "q3", "q4", "prol", "minutes", "off", "role", "tir", "agress"]:
        if idx(cols, k) < 0:
            f.append(f"tactique : colonne manquante {k}")
    if idx(cols, "poste") >= 0:
        f += ["tactique : " + x for x in ordre_postes(lignes, idx(cols, "poste"))]
    return f


def adversaires(cols, lignes):
    f = []
    ip, ifo, iz = idx(cols, "poste"), idx(cols, "focus"), idx(cols, "zone")
    if min(ip, ifo, iz) < 0:
        return ["adversaires : colonnes attendues Adversaire | Poste | Focus défensif (1–5) | Zone"]
    for c in lignes:
        if "," in c[0] or " et " in norm(c[0]):
            f.append(f"adversaires : plusieurs joueurs sur une ligne ({c[0][:30]}) — une ligne par joueur")
        if not re.fullmatch(r"[1-5]", c[ifo].replace("*", "").strip()):
            f.append(f"adversaires : focus hors 1–5 ({c[ifo][:10]})")
        if norm(c[iz]) not in ZONES:
            f.append(f"adversaires : zone hors Rim/Middle/Perimeter ({c[iz][:12]})")
    return f + ["adversaires : " + x for x in ordre_postes(lignes, ip)]


def hw_tactique(cols, lignes):
    ordre = ["pace", "inside", "zone", "pressure", "extend"]
    vus = [k for c in lignes for k in ordre if norm(c[0]).startswith(k)]
    f = []
    if vus != ordre:
        f.append("Hardwood tactique : lignes attendues dans l'ordre de l'écran Pace, Inside/Outside, Zone %, Pressure %, Extend")
    return f


def hw_recrues(cols, lignes):
    f = []
    if len(lignes) != 4:
        f.append(f"Hardwood recrues : {len(lignes)} lignes, il en faut 4 cibles")
    if any(re.search(r"\bhigh\b", norm(" ".join(c))) for c in lignes) or any("high" in c for c in cols):
        f.append("Hardwood recrues : niveau High interdit")
    return f


def hn(cols, lignes):
    if idx(cols, "parametre") >= 0:
        return [] if idx(cols, "cible") >= 0 and idx(cols, "dans le jeu") >= 0 else ["HN plan : colonnes Paramètre | Cible | Dans le jeu"]
    return [f"HN effectif : colonne manquante {k}" for k in ["poste", "joueur", "note", "endurance", "fof"] if idx(cols, k) < 0]


def ts_compo(cols, lignes):
    f = [f"Team Soccer : colonne manquante {k}" for k in ["ultra", "defensive", "mediane", "offensive", "finition"] if idx(cols, k) < 0]
    return f


def fautes_tableaux(text: str) -> list[str]:
    f = []
    for cols, lignes in tableaux(text):
        if not cols or not lignes:
            continue
        j = " ".join(cols)
        if cols[0] == "priorite" and len(cols) > 1 and cols[1] == "categorie":
            f += plan(cols, lignes)
        elif cols[0] == "priorite" and "cible" in j and "remplacant" in j:
            f += hw_recrues(cols, lignes)
        elif cols[0] == "joueur" and (idx(cols, "principale") >= 0 or (idx(cols, "actuel") >= 0 and idx(cols, "a mettre") >= 0)):
            f += entrainement(cols, lignes)
        elif cols[0] == "reglage":
            f += hw_tactique(cols, lignes)
        elif "adversaire" in cols[0]:
            f += adversaires(cols, lignes)
        elif cols[0] == "joueur" and idx(cols, "q1") >= 0:
            f += tactique(cols, lignes)
        elif idx(cols, "ultra") >= 0 or ("empl" in j and idx(cols, "finition") >= 0):
            f += ts_compo(cols, lignes)
        elif idx(cols, "parametre") >= 0 and idx(cols, "cible") >= 0 or ("joueur" in j and (cols[0] == "poste" or "fof" in j)):
            f += hn(cols, lignes)
    return f


def fautes_texte(text: str, n: str) -> list[str]:
    f = []
    if "ultra" in n and "finition" in n:  # composition Team Soccer
        if "remplacements programmes" not in n:
            f.append("Team Soccer : ligne « Remplacements programmés » absente")
        for club in ("chomelix cows", "ben ahmed donkey"):
            if club not in n:
                f.append(f"Team Soccer : club absent ({club})")
        for m in re.finditer(r"passer(?![^|\n]{0,40}(defenseur|milieu|attaquant))", n):
            f.append("Team Soccer : « Passer » sans cible (défenseurs / milieux / attaquants)")
            break
    return f


def fautes_de(text: str) -> list[str]:
    n = norm(CITATION.sub(" ", text))
    f = fautes_tableaux(text) + fautes_texte(text, n)
    f += [f"interdit : {i}" for i in interdits() if norm(i) in n]
    return list(dict.fromkeys(f))


def main() -> int:
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    data = json.load(sys.stdin)
    if data.get("stop_hook_active"):
        return 0
    text = data.get("last_assistant_message") or last_text(data.get("transcript_path", ""))
    fautes = fautes_de(text)
    if not fautes:
        return 0
    print(json.dumps({"decision": "block", "reason": (
        "Forme : réponse hors format (" + " ; ".join(fautes) + "). Réécris-la dans le format fixe validé : "
        "plan = Priorité | Catégorie | Action avec 🟥 URGENT / 🟧 IMPORTANT / 🟩 SUIVI ; entraînement = joueurs dans "
        "l'ordre de l'export (select * from gold.bv_saisie_entrainement order by ordre) ou seulement ceux qui changent ; "
        "tactique et adversaires = une ligne par joueur, ordre PG→C ; voir pipelines/forme.py pour chaque format.")},
        ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
