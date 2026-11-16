"""Génère les userscripts de collecte (un fichier par jeu, sans @require) depuis userscripts/core.js et userscripts/jeux/<jeu>.js.

Sans option : écrit userscripts/<jeu>.user.js pour chaque jeu.
Avec --check : code 1 si un fichier généré n'est pas à jour (ou si un jeu n'a pas son fichier), sans rien écrire.
Chaque jeux/<jeu>.js commence par le bloc « ==UserScript== » complet (nom, version, @match, @grant) puis définit la constante JEU
(voir core.js). La version du bloc devient le CLIENT de chaque capture (« <jeu>.user.js@<version> »).
"""

import argparse
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DOSSIER = RACINE / "userscripts"
TOUS = ["basketvibe", "sixzeroleague", "teamsoccer", "hockeynation", "derbymanager", "hardwood"]  # ordre de migration
GRANTS = {"unsafeWindow", "GM_xmlhttpRequest", "GM_getValue", "GM_setValue", "GM_deleteValue", "GM_listValues", "GM_registerMenuCommand"}
BANDEAU = "// GÉNÉRÉ par pipelines/build_userscripts.py depuis userscripts/core.js et userscripts/jeux/{jeu}.js : ne pas modifier ce fichier."
BLOC = re.compile(r"\A(// ==UserScript==\n.*?// ==/UserScript==\n)(.*)\Z", re.S)


def jeux_migres() -> list:
    """Les jeux qui ont leur userscripts/jeux/<jeu>.js (les autres gardent leur ancien script autonome)."""
    return [j for j in TOUS if (DOSSIER / "jeux" / f"{j}.js").is_file()]


def construire(jeu: str) -> str:
    source = (DOSSIER / "jeux" / f"{jeu}.js").read_text(encoding="utf-8")
    m = BLOC.match(source)
    if not m:
        raise SystemExit(f"{jeu}.js : bloc ==UserScript== absent en tête de fichier")
    entete, corps = m.group(1), m.group(2)
    grants = set(re.findall(r"^// @grant\s+(\S+)", entete, re.M))
    if grants != GRANTS:
        raise SystemExit(f"{jeu}.js : @grant attendus {sorted(GRANTS)}, trouvés {sorted(grants)}")
    if re.search(r"^// @require", entete, re.M):
        raise SystemExit(f"{jeu}.js : @require interdit (un fichier par jeu, sans dépendance externe)")
    version = re.search(r"^// @version\s+(\S+)", entete, re.M)
    if not version:
        raise SystemExit(f"{jeu}.js : @version absente")
    if not re.search(rf"game: '{jeu}'", corps):
        raise SystemExit(f"{jeu}.js : JEU.game doit valoir '{jeu}'")
    core = (DOSSIER / "core.js").read_text(encoding="utf-8").replace("__VERSION__", version.group(1))
    return (entete + BANDEAU.format(jeu=jeu) + "\n\n(function () {\n  'use strict';\n\n"
            + corps.strip("\n") + "\n\n" + core.strip("\n") + "\n})();\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="code 1 si un fichier généré n'est pas à jour")
    args = parser.parse_args()
    perimes = []
    for jeu in jeux_migres():
        texte = construire(jeu)
        cible = DOSSIER / f"{jeu}.user.js"
        if args.check:
            if not cible.is_file() or cible.read_text(encoding="utf-8") != texte:
                perimes.append(cible.name)
        else:
            cible.write_text(texte, encoding="utf-8")
            print(f"écrit {cible.relative_to(RACINE)} ({len(texte)} caractères)")
    if perimes:
        print("pas à jour : " + ", ".join(perimes) + " — lancer python -I pipelines/build_userscripts.py")
        return 1
    if args.check:
        print("userscripts à jour")
    return 0


if __name__ == "__main__":
    sys.exit(main())
