"""Contrôle de la brique « collecte » (userscripts/core.js + userscripts/jeux/*.js → userscripts/*.user.js).

Lancer : python -I pipelines/test_userscripts.py   (code 1 si un contrôle échoue ; demande node)
Contrôles :
  1. les six fichiers générés sont à jour (build_userscripts.py --check), sans @require, avec les @grant attendus ;
  2. page_type avant/après identique sur l'échantillon tiré de bronze (userscripts/test/echantillon_pages.json), par jeu ;
     seules les routes ajoutées à BasketVibe (/cup/<id>, /c/<slug>) ont un type nouveau ;
  3. scénarios du noyau (file persistante, déclencheurs d'envoi, retrait après OK seulement, nouvel essai, bouton, file pleine) ;
  4. taille de la file persistée : 20 copies de page au 95e centile de chaque jeu tiennent sous le plafond de la file.
"""
import json
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
import importlib.util

spec = importlib.util.spec_from_file_location("build_userscripts", Path(__file__).resolve().parent / "build_userscripts.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)
JEUX = build.jeux_migres()
GRANTS = ["unsafeWindow", "GM_xmlhttpRequest", "GM_getValue", "GM_setValue", "GM_deleteValue", "GM_listValues", "GM_registerMenuCommand"]
# 95e centile de la charge utile d'une copie de page (source dom), bronze.raw_pages, 30 derniers jours au 2026-11-16
P95_DOM = {"basketvibe": 79_043, "sixzeroleague": 654_047, "teamsoccer": 245_165, "hockeynation": 469_854, "derbymanager": 1_415_253, "hardwood": 284_704}


def lancer(*args):
    return subprocess.run(args, cwd=RACINE, capture_output=True, text=True)


def main() -> int:
    echecs = 0

    def controle(nom: str, ok: bool, detail: str):
        nonlocal echecs
        echecs += 0 if ok else 1
        print(f"{'ok ' if ok else 'ÉCHEC'} {nom} : {detail}")

    if lancer("node", "-v").returncode != 0:
        print("ÉCHEC node absent")
        return 1

    # 1. génération
    r = lancer(sys.executable, "-I", "pipelines/build_userscripts.py", "--check")
    controle("fichiers générés à jour", r.returncode == 0, (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else "")
    for jeu in JEUX:
        t = (RACINE / "userscripts" / f"{jeu}.user.js").read_text(encoding="utf-8")
        manque = [g for g in GRANTS if f"// @grant        {g}" not in t]
        controle(f"{jeu} : en-tête", "@require" not in t and not manque and "__VERSION__" not in t and "__TEST_EXPORT__" in t,
                 f"@grant manquants {manque}" if manque else f"sans @require, {len(t.splitlines())} lignes")

    # 2. page_type avant / après
    r = lancer("node", "userscripts/test/comparer_pagetypes.js")
    if r.returncode != 0:
        controle("comparaison page_type", False, r.stderr.strip()[:300])
    else:
        for res in json.loads(r.stdout):
            jeu = res["jeu"]
            dif = res["differences"]
            controle(f"{jeu} : page_type avant = après", not dif, f"{res['identiques']}/{res['total']} identiques" + (f", écarts {dif[:3]}" if dif else ""))
            if res["hors_base"]:
                print(f"     info : {len(res['hors_base'])} page_type de la base diffèrent du script (anciennes versions du script) : "
                      + "; ".join(f"{h['chemin']} base={h['base']} script={h['apres']}" for h in res["hors_base"][:3]))
            for n in res["nouveaux"]:
                controle(f"{jeu} : route ajoutée {n['chemin'][:34]}", n["apres"] == n["attendu"] and n["avant"] == "unknown", f"avant {n['avant']}, après {n['apres']}")

    # 3. scénarios du noyau
    r = lancer("node", "userscripts/test/scenarios.js")
    lignes = [json.loads(l) for l in r.stdout.splitlines() if l.startswith("{")]
    if not lignes:
        controle("scénarios du noyau", False, (r.stderr or r.stdout).strip()[:300])
    for s in lignes:
        controle(s["nom"], s["ok"], s["detail"])

    # 4. taille de la file
    r = lancer("node", "userscripts/test/mesure_file.js", json.dumps({j: P95_DOM[j] for j in JEUX}))
    if r.returncode != 0:
        controle("taille de la file", False, (r.stderr or r.stdout).strip()[:300])
    else:
        for res in json.loads(r.stdout):
            controle(f"{res['jeu']} : file de 20 copies (95e centile)", res["chars"] <= res["plafond"],
                     f"{res['chars'] / 1e6:.2f} M caractères, plafond {res['plafond'] / 1e6:.0f} M, {res['n']} captures")

    print(f"\n{'TOUT VERT' if not echecs else str(echecs) + ' ÉCHEC(S)'}")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
