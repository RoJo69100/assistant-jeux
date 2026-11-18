"""Étiquettes `[expérience=<id>:<niveau>]` déduites des données (18/11) : python -I pipelines/experiences_deduites.py [--ecrire]

Un amical joué (gold.bv_amical_reglage) depuis `debut` reçoit une ligne au registre `outputs/basketvibe/fait-<jour du match>.md`
quand : (1) son écran sauvegardé est contrôlé en base (gold.bv_saisie_joueurs, kind amical, sauvegarde_match vrai sur
toutes les lignes du fixture) ; (2) au plus une dimension du réglage joué diffère du `neutre` du YAML ; (3) cette dimension
(ou, tout neutre, l'expérience en cours) correspond à un niveau du YAML. Deux dimensions modifiées : aucune ligne.
Source écrite : « déduit de l'écran sauvegardé et du réglage joué ». Sans --ecrire : affiche seulement. Idempotent.
Tests : test_experiences_deduites.py.
"""
import datetime as dt
import importlib.util
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
BASE = RACINE / "outputs/basketvibe"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from aujourdhui_sources import FICHIER_EXPERIENCES, lire_experiences  # noqa: E402

SOURCE = "déduit de l'écran sauvegardé et du réglage joué"
DIMS = ("agress", "zone", "tir", "primary")


def valeurs(a: dict) -> dict:
    """Valeur de chaque dimension pour une ligne de gold.bv_amical_reglage."""
    return {"agress": a.get("agress_cran") if a.get("agress_uniforme") in (True, "True", "true") else None,
            "zone": a.get("zone"), "tir": int(a.get("tir_cran4_joueurs") or 0), "primary": int(a.get("primary_quarts") or 0)}


def ecarts(v: dict, neutre: dict) -> set:
    """Dimensions qui diffèrent du neutre."""
    d = set()
    if v["agress"] is None or int(v["agress"]) != int(neutre["agress_cran"]):
        d.add("agress")
    if v["zone"] != neutre["zone"]:
        d.add("zone")
    if v["tir"] > int(neutre["tir_cran4_max"]):
        d.add("tir")
    if v["primary"] > int(neutre["primary_quarts_max"]):
        d.add("primary")
    return d


def specs(exp: dict) -> dict:
    """{niveau: [(dimension, test)]} pour les niveaux vérifiables d'une expérience (`joue` ou `zone`)."""
    res = {}
    for niv, j in (exp.get("joue") or {}).items():
        c = []
        if "agress_cran" in j:
            c.append(("agress", lambda v, x=int(j["agress_cran"]): v is not None and int(v) == x))
        if "tir_cran4_min" in j:
            c.append(("tir", lambda v, x=int(j["tir_cran4_min"]): v >= x))
        if "primary_quarts_min" in j:
            c.append(("primary", lambda v, x=int(j["primary_quarts_min"]): v >= x))
        if c:
            res[str(niv)] = c
    for niv, z in (exp.get("zone") or {}).items():
        res.setdefault(str(niv), []).append(("zone", lambda v, x=z: v == x))
    return res


def en_cours(file: list, comptes: dict):
    for e in file:
        if comptes.get(e["id"], 0) < int(e.get("amicaux_vises") or 0):
            return e["id"]
    return None


def etiqueter(a: dict, file: list, neutre: dict, comptes: dict):
    """(id, niveau) ou None pour un amical déjà contrôlé (écran sauvegardé)."""
    v = valeurs(a)
    d = ecarts(v, neutre)
    if len(d) > 1:
        return None
    cands = []
    for e in file:
        for niv, conds in specs(e).items():
            dims = {k for k, _ in conds}
            if d <= dims and all(t(v[k]) for k, t in conds):
                cands.append((e["id"], niv))
    if not d:  # tout neutre : seulement l'expérience en cours, à son niveau neutre
        cur = en_cours(file, comptes)
        cands = [c for c in cands if c[0] == cur]
    return cands[0] if len({c[0] for c in cands}) == 1 and len(cands) == 1 else None


def plan(amicaux: list, controles: set, conf: dict, faits: list) -> list:
    """Lignes à écrire, dans l'ordre des matchs : [{'jour', 'cle', 'id', 'niveau', 'opponent'}]."""
    file, neutre, debut = conf["experiences"], conf["neutre"], conf.get("debut")
    debut = dt.date.fromisoformat(str(debut)) if debut else None
    comptes = {}
    deja = set()
    for f in faits:
        comptes[f["id"]] = comptes.get(f["id"], 0) + 1
        if f.get("cle"):
            deja.add((f["cle"]["nom"].lower(), f["cle"]["date"]))
    res = []
    for a in sorted(amicaux, key=lambda x: str(x["match_day"])):
        jour = dt.date.fromisoformat(str(a["match_day"])[:10])
        if (debut and jour < debut) or str(a["fixture_id"]) not in controles:
            continue
        if (str(a["opponent"]).lower(), jour) in deja:
            continue
        e = etiqueter(a, file, neutre, comptes)
        if e:
            comptes[e[0]] = comptes.get(e[0], 0) + 1
            res.append({"jour": jour, "cle": f"{a['opponent']} {jour:%d/%m}", "id": e[0], "niveau": e[1],
                        "opponent": a["opponent"]})
    return res


def ligne(p: dict, quand: str) -> str:
    return (f"- [{quand}] [clé={p['cle']}] Amical joué contre {p['opponent']} ({p['jour']:%d/%m}) "
            f"[expérience={p['id']}:{p['niveau']}] — source : {SOURCE}")


def ecrire(lignes_plan: list, base: Path, quand: str) -> None:
    for p in lignes_plan:
        f = base / f"fait-{p['jour'].isoformat()}.md"
        texte = f.read_text(encoding="utf-8") if f.is_file() else ""
        if f"[clé={p['cle']}]" in texte and "[expérience=" in texte:
            continue
        f.write_text(texte + ("" if not texte or texte.endswith("\n") else "\n") + ligne(p, quand) + "\n", encoding="utf-8")


def charger_sql():
    spec = importlib.util.spec_from_file_location("sqlmod", Path(__file__).resolve().parent / "sql.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.executer


def dicts(r):
    cols, rows = r
    return [r if isinstance(r, dict) else dict(zip(cols, r)) for r in rows]


def main() -> int:
    import yaml
    conf = yaml.safe_load(FICHIER_EXPERIENCES.read_text(encoding="utf-8"))
    executer = charger_sql()
    amicaux = dicts(executer("select fixture_id::text as fixture_id, match_day, opponent, agress_uniforme, agress_cran, "
                             "zone, tir_cran4_joueurs, primary_quarts from gold.bv_amical_reglage"))
    controles = {str(x["fixture_id"]) for x in dicts(executer(
        "select fixture_id from gold.bv_saisie_joueurs where kind = 'amical' group by fixture_id "
        "having bool_and(sauvegarde_match)"))}
    hp = __import__("subprocess").run([sys.executable, "-I", str(RACINE / "pipelines/heure_paris.py")],
                                      capture_output=True, text=True).stdout
    m = re.search(r"(\d{2})/(\d{2})/\d{4} (\d{2}:\d{2})", hp)
    quand = f"déduit le {m.group(1)}/{m.group(2)} {m.group(3)} Paris" if m else "déduit"
    aujourd = dt.date.fromisoformat(f"{hp.split('/')[2][:4]}-{m.group(2)}-{m.group(1)}") if m else dt.date.today()
    faits = (lire_experiences(BASE, aujourd) or {}).get("faits", [])
    p = plan(amicaux, controles, conf, faits)
    for x in p:
        print(f"fait-{x['jour'].isoformat()}.md : {ligne(x, quand)}")
    print(f"{len(p)} amical(s) étiqueté(s)")
    if "--ecrire" in sys.argv:
        ecrire(p, BASE, quand)
    return 0


if __name__ == "__main__":
    sys.exit(main())
