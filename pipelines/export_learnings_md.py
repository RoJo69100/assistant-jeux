"""Régénère outputs/<jeu>/learnings.md depuis learn.* (refonte v2, étape 3.5) : le fichier devient un export.

Le fichier existant sert de gabarit (en-têtes, journal des matchs, notes) ; chaque ligne L-nnn / C-nnn est remplacée
par sa ligne en base (origine.ligne). Si le statut en base a changé depuis la migration (évaluateur, retrait),
la cellule Statut est réécrite. Les leçons et décisions créées en base après la migration sont ajoutées en fin de
leur tableau. Une ligne du fichier absente de la base est une erreur (code 1).
Lecture : psycopg (SUPABASE_DB_URL_RO) si disponible, sinon REST public.learn_export (SUPABASE_SECRET_KEY).

Usage : python -I pipelines/export_learnings_md.py [<jeu> …] [--check]   (--check : compare sans écrire)
"""

import argparse
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from migrer_learnings import JEUX, LIGNE, RACINE, cellules, env, statut_conseil, statut_lecon, ENTIER, IDS_MATCH  # noqa: E402

LIBELLE = {"validated": "confirmé (learn)", "hard_rule": "règle dure (learn)", "retired": "infirmé, retirée (learn)",
           "hypothesis": "à surveiller (learn)", "proposed": "ouvert", "accepted": "accepté", "done": "appliqué",
           "rejected": "non appliqué", "expired": "caduc"}


def lire_base(jeu: str) -> dict:
    try:
        import psycopg
        from sql import url_ro
        with psycopg.connect(url_ro(), connect_timeout=15) as c, c.cursor() as cur:
            cur.execute("select public.learn_export(%s)", (jeu,))
            return cur.fetchone()[0]
    except (Exception, SystemExit):  # pas de psycopg, pas d'URL ou fonction réservée à service_role : REST
        pass
    url, cle = env("SUPABASE_URL"), env("SUPABASE_SECRET_KEY")
    if not url or not cle:
        sys.exit("❌ ni SUPABASE_DB_URL_RO ni SUPABASE_URL + SUPABASE_SECRET_KEY")
    req = urllib.request.Request(url.rstrip("/") + "/rest/v1/rpc/learn_export", method="POST",
                                 data=json.dumps({"p_game": jeu}).encode(),
                                 headers={"apikey": cle, "Authorization": f"Bearer {cle}",
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def ligne_base(o: dict, statut: str, section: str) -> str:
    """Ligne d'origine, cellule Statut réécrite si la base a changé de statut depuis la migration."""
    c = cellules(o["ligne"])
    if section == "L":
        m = ENTIER.match(c[-3])
        initial = statut_lecon(c[-2], int(m.group(1)) if m else len(IDS_MATCH.findall(c[-3])))
    else:
        initial = statut_conseil(c[-2])
    if statut == initial:
        return o["ligne"]
    c[-2] = LIBELLE[statut]
    return "| " + " | ".join(c) + " |"


def nouvelle(x: dict, section: str, avec_club: bool) -> str:
    club = ["—"] if avec_club else []
    if section == "L":
        c = [x["id"].split(":", 1)[-1], *club, x["created_at"][:10], x["claim"],
             f"{x['n_for']} pour / {x['n_against']} contre", LIBELLE[x["status"]], "learn.lesson"]
    else:
        c = [f"D-{x['id']}", *club, x["decided_at"][:10], x["label"], json.dumps(x["prediction"], ensure_ascii=False),
             LIBELLE[x["status"]], x.get("verdict") or "—"]
    return "| " + " | ".join(s.replace("|", "/").replace("\n", " ") for s in c) + " |"


def exporter(jeu: str, base: dict) -> tuple[str, list[str]]:
    lecons = {x["origine"]["ordre"]: x for x in base["lessons"] if x.get("origine")}
    conseils = {x["origine"]["ordre"]: x for x in base["decisions"] if x.get("origine")}
    neuves = {"L": [x for x in base["lessons"] if not x.get("origine")],
              "C": [x for x in base["decisions"] if not x.get("origine")]}
    lignes = (RACINE / f"outputs/{jeu}/learnings.md").read_text(encoding="utf-8").split("\n")
    sortie, erreurs, rang = [], [], {"L": 0, "C": 0}
    section, avec_club, derniere = None, False, {}
    for ligne in lignes:
        if ligne.startswith("## "):
            section = "L" if "Enseignement" in ligne else "C" if "Conseil" in ligne else None
        if ligne.startswith("| ID"):
            avec_club = "Club" in cellules(ligne)[:3]
        m = LIGNE.match(ligne)
        if m and section and m.group(1)[0] == section:
            table = lecons if section == "L" else conseils
            x = table.get(rang[section])
            rang[section] += 1
            if not x or x["origine"]["ref"] != m.group(1):
                erreurs.append(f"{jeu} {m.group(1)} (rang {rang[section] - 1}) absent de la base")
                sortie.append(ligne)
            else:
                sortie.append(ligne_base(x["origine"], x["status"], section))
            derniere[section] = (len(sortie), avec_club)
            continue
        sortie.append(ligne)
    for s in ("C", "L"):  # C d'abord : l'insertion ne décale pas l'index de L (L est avant C)
        if neuves[s] and s in derniere:
            i, club = derniere[s]
            sortie[i:i] = [nouvelle(x, s, club) for x in neuves[s]]
    for s, table in (("L", lecons), ("C", conseils)):
        if len(table) > rang[s]:
            erreurs.append(f"{jeu} : {len(table) - rang[s]} ligne(s) {s} en base sans place dans le fichier")
    return "\n".join(sortie), erreurs


def main(argv=None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    a = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    a.add_argument("jeux", nargs="*")
    a.add_argument("--check", action="store_true")
    args = a.parse_args(argv)
    code = 0
    for jeu in args.jeux or JEUX:
        f = RACINE / f"outputs/{jeu}/learnings.md"
        texte, erreurs = exporter(jeu, lire_base(jeu))
        identique = texte == f.read_text(encoding="utf-8")
        for e in erreurs:
            print(f"❌ {e}")
        if erreurs:
            code = 1
        if args.check:
            print(f"{'✅' if identique else '🔁'} {jeu} : {'identique à la base' if identique else 'à régénérer'}")
        elif not identique:
            f.write_text(texte, encoding="utf-8")
            print(f"✍️ {jeu} : régénéré")
        else:
            print(f"✅ {jeu} : déjà à jour")
    return code


if __name__ == "__main__":
    sys.exit(main())
