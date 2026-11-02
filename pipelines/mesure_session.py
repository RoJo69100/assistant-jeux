"""Mesure le coût d'une session Claude Code à partir de son journal .jsonl.

Usage : python -I pipelines/mesure_session.py [chemin.jsonl] [--md sortie.md]
Sans chemin : la session la plus récente du projet.
Sort, par demande de l'utilisateur : durée, tokens (lus en cache, écrits en cache, sortie),
contexte maximal, outils appelés, agents lancés ; puis les fichiers relus plusieurs fois,
les agents (tokens et durée de leur propre journal) et les requêtes SQL les plus lourdes.
Le calcul est fait ici ; je lis le rapport moi-même (agent `optimisation` retiré le 2026-11-02, étape 0d).
"""
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

def _dossier_projet():
    """Dossier des journaux du projet courant (nom = chemin du dépôt, non alphanumériques -> '-')."""
    import re
    racine = str(Path(__file__).resolve().parent.parent)
    return Path.home() / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9]", "-", racine)


PROJET = _dossier_projet()
CONTEXTE_MAX = 200_000  # fenêtre de référence pour le % de contexte


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None


def lire(path):
    with open(path, encoding="utf-8") as f:
        for ligne in f:
            try:
                yield json.loads(ligne)
            except json.JSONDecodeError:
                continue


def usage_total(entrees):
    """Somme des usages des messages assistant (un message = une requête API, dédoublonné par requestId)."""
    vus, tot, ctx_max, debut, fin = set(), Counter(), 0, None, None
    for o in entrees:
        t = ts(o.get("timestamp"))
        if t:
            debut = debut or t
            fin = t
        if o.get("type") != "assistant":
            continue
        rid = o.get("requestId") or o.get("uuid")
        u = (o.get("message") or {}).get("usage") or {}
        if rid in vus or not u:
            continue
        vus.add(rid)
        for k in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens", "output_tokens"):
            tot[k] += u.get(k) or 0
        ctx = (u.get("input_tokens") or 0) + (u.get("cache_read_input_tokens") or 0) + (u.get("cache_creation_input_tokens") or 0)
        ctx_max = max(ctx_max, ctx)
    tot["requetes"] = len(vus)
    tot["contexte_max"] = ctx_max
    tot["duree_min"] = round((fin - debut).total_seconds() / 60, 1) if debut and fin else 0
    return tot


def texte_utilisateur(o):
    c = (o.get("message") or {}).get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in c):
            return None
        return " ".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
    return None


def analyser(path):
    entrees = list(lire(path))
    demandes, cur = [], None
    lectures = Counter()
    sql = []
    agents_appels = {}

    for o in entrees:
        if o.get("type") == "user" and not o.get("isMeta") and not o.get("isSidechain"):
            txt = texte_utilisateur(o)
            if txt and not txt.lstrip().startswith("<"):
                cur = {"texte": txt.strip().replace("\n", " ")[:80], "entrees": [], "outils": Counter(), "agents": []}
                demandes.append(cur)
        if cur is not None:
            cur["entrees"].append(o)
        if o.get("type") != "assistant":
            continue
        for b in (o.get("message") or {}).get("content") or []:
            if not isinstance(b, dict) or b.get("type") != "tool_use":
                continue
            nom, inp = b.get("name", "?"), b.get("input") or {}
            if cur is not None:
                cur["outils"][nom] += 1
            if nom == "Read":
                lectures[inp.get("file_path", "?")] += 1
            elif nom.endswith("execute_sql"):
                sql.append((b.get("id"), (inp.get("query") or "")[:90].replace("\n", " ")))
            elif nom in ("Agent", "Task"):
                desc = inp.get("description") or inp.get("subagent_type") or "?"
                agents_appels[b.get("id")] = desc
                if cur is not None:
                    cur["agents"].append(desc)

    # taille des résultats SQL (caractères renvoyés dans le contexte)
    taille = {}
    for o in entrees:
        if o.get("type") != "user":
            continue
        c = (o.get("message") or {}).get("content")
        if isinstance(c, list):
            for b in c:
                if isinstance(b, dict) and b.get("type") == "tool_result":
                    taille[b.get("tool_use_id")] = len(json.dumps(b.get("content"), ensure_ascii=False))

    # journaux des sous-agents
    agents = []
    dossier = Path(path).with_suffix("") / "subagents"
    for f in sorted(dossier.glob("*.jsonl")) if dossier.exists() else []:
        ent = list(lire(f))
        u = usage_total(ent)
        premier = next((texte_utilisateur(o) for o in ent if o.get("type") == "user"), "") or ""
        relus = Counter()
        for o in ent:
            if o.get("type") == "assistant":
                for b in (o.get("message") or {}).get("content") or []:
                    if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Read":
                        relus[(b.get("input") or {}).get("file_path", "?")] += 1
        agents.append({"fichier": f.name, "debut": premier.strip().replace("\n", " ")[:70], "u": u, "lus": len(relus),
                       "relus": relus})

    return entrees, demandes, lectures, sql, taille, agents


def rapport(path):
    entrees, demandes, lectures, sql, taille, agents = analyser(path)
    tot = usage_total(entrees)
    L = []
    L.append(f"# Mesure de session — {Path(path).name}")
    L.append("")
    L.append(f"Durée {tot['duree_min']} min · {tot['requetes']} requêtes · contexte max {tot['contexte_max']:,} "
             f"({100 * tot['contexte_max'] // CONTEXTE_MAX} %) · relu en cache {tot['cache_read_input_tokens']:,} · "
             f"écrit en cache {tot['cache_creation_input_tokens']:,} · sortie {tot['output_tokens']:,}")
    L.append("")
    L.append("## Par demande de l'utilisateur")
    L.append("| # | Demande | Durée (min) | Requêtes | Contexte max | Relu en cache | Sortie | Outils | Agents |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for i, d in enumerate(demandes, 1):
        u = usage_total(d["entrees"])
        outils = ", ".join(f"{k.split('__')[-1]}×{v}" for k, v in d["outils"].most_common(4))
        L.append(f"| {i} | {d['texte']} | {u['duree_min']} | {u['requetes']} | {u['contexte_max']:,} | "
                 f"{u['cache_read_input_tokens']:,} | {u['output_tokens']:,} | {outils} | {len(d['agents'])} |")
    L.append("")
    L.append("## Agents (journaux des sous-agents)")
    L.append("| Agent (début de la demande) | Durée (min) | Requêtes | Relu en cache | Sortie | Fichiers lus | Relus 2× ou plus |")
    L.append("|---|---|---|---|---|---|---|")
    for a in sorted(agents, key=lambda a: -a["u"]["cache_read_input_tokens"]):
        u = a["u"]
        doublons = sum(1 for v in a["relus"].values() if v > 1)
        L.append(f"| {a['debut']} | {u['duree_min']} | {u['requetes']} | {u['cache_read_input_tokens']:,} | "
                 f"{u['output_tokens']:,} | {a['lus']} | {doublons} |")
    communs = Counter()
    for a in agents:
        communs.update(a["relus"].keys())
    L.append("")
    L.append("## Fichiers lus par plusieurs agents (candidats à un résumé partagé)")
    for f, n in communs.most_common(12):
        if n > 1:
            L.append(f"- {n} agents : `{f}`")
    L.append("")
    L.append("## Fichiers relus dans la session principale")
    for f, n in lectures.most_common(10):
        if n > 1:
            L.append(f"- {n}× `{f}`")
    L.append("")
    L.append("## Résultats SQL les plus lourds (caractères ajoutés au contexte)")
    for tid, q in sorted(sql, key=lambda x: -taille.get(x[0], 0))[:8]:
        L.append(f"- {taille.get(tid, 0):,} car. : `{q}`")
    return "\n".join(L)


def main():
    args = sys.argv[1:]
    md = None
    if "--md" in args:
        i = args.index("--md")
        md = args[i + 1]
        del args[i:i + 2]
    path = args[0] if args else max(PROJET.glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
    txt = rapport(path)
    if md:
        Path(md).parent.mkdir(parents=True, exist_ok=True)
        Path(md).write_text(txt, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(txt)


if __name__ == "__main__":
    main()
