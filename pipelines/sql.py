"""Requêtes SQL compactes en lecture seule (refonte v2, 0.4).

Usage :
  python -I pipelines/sql.py "select game, count(*) from bronze.raw_pages group by 1" [--max-rows 30] [--max-col 60]
  python -I pipelines/sql.py --page-id 123 --payload-path "players,0,name"      (un morceau de payload bronze)
Rôle Postgres `assistant_ro` (select sur silver et gold, métadonnées seules de bronze), chaîne SUPABASE_DB_URL_RO dans .env.
Sortie : tableau Markdown compact, `limit` ajouté, cellules tronquées, « n lignes / tronqué » en pied.
Toute écriture est refusée ici (une seule instruction select/with/explain) et par le rôle (transaction en lecture seule).
"""
import argparse
import os
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DEBUT_OK = re.compile(r"^\s*(select|with|explain|table|values)\b", re.I)
PAYLOAD = re.compile(r"\b(payload|content)\b", re.I)
ECRITURE = re.compile(r"\b(insert|update|delete|drop|alter|create|truncate|grant|revoke|copy|call|do|vacuum)\b", re.I)


def url_ro() -> str:
    env = RACINE / ".env"
    if env.exists():
        for ligne in env.read_text(encoding="utf-8").splitlines():
            if ligne.startswith("SUPABASE_DB_URL_RO="):
                return ligne.split("=", 1)[1].strip()
    if os.environ.get("SUPABASE_DB_URL_RO"):  # session cloud : variable de l'environnement, pas de .env
        return os.environ["SUPABASE_DB_URL_RO"].strip()
    sys.exit("SUPABASE_DB_URL_RO absent de .env et de l'environnement (voir sql/silver/ops_001_role_assistant_ro.sql)")


def verifie(requete: str) -> str:
    q = requete.strip().rstrip(";").strip()
    if ";" in q:
        sys.exit("refusé : une seule instruction")
    if not DEBUT_OK.match(q):
        sys.exit("refusé : lecture seule (select / with / explain)")
    sans_chaines = re.sub(r"'[^']*'", "''", q)
    if ECRITURE.search(sans_chaines):
        sys.exit("refusé : mot d'écriture dans la requête")
    if re.search(r"\bbronze\.", sans_chaines, re.I) and PAYLOAD.search(sans_chaines):
        sys.exit("refusé : pas de payload bronze entier ; utilise --page-id N --payload-path a,b,c")
    return q


def cellule(v, largeur: int) -> str:
    s = "" if v is None else str(v).replace("\n", " ").replace("|", "/")
    return s if len(s) <= largeur else s[:largeur - 1] + "…"


def tableau(colonnes, lignes, largeur: int) -> str:
    sortie = ["| " + " | ".join(colonnes) + " |", "|" + "---|" * len(colonnes)]
    sortie += ["| " + " | ".join(cellule(v, largeur) for v in l) + " |" for l in lignes]
    return "\n".join(sortie)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("requete", nargs="?")
    p.add_argument("--max-rows", type=int, default=30)
    p.add_argument("--max-col", type=int, default=60)
    p.add_argument("--page-id", type=int)
    p.add_argument("--payload-path", help="chemin JSON séparé par des virgules, ex. players,0,name")
    a = p.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    import psycopg

    if a.payload_path is not None:
        if a.page_id is None:
            sys.exit("--payload-path demande --page-id")
        chemin = [x for x in a.payload_path.split(",") if x != ""]
        sql, params = "select bronze.payload_at(%s, %s) as valeur", (a.page_id, chemin)
    elif a.requete:
        q = verifie(a.requete)
        sql, params = f"select * from ({q}) t limit {a.max_rows + 1}", None
    else:
        p.error("donne une requête ou --page-id et --payload-path")

    with psycopg.connect(url_ro(), connect_timeout=15) as c, c.cursor() as cur:
        cur.execute(sql, params)
        cols = [d.name for d in cur.description]
        lignes = cur.fetchall()
    tronque = len(lignes) > a.max_rows
    lignes = lignes[:a.max_rows]
    print(tableau(cols, lignes, a.max_col))
    print(f"\n{len(lignes)} lignes" + (f" (tronqué à {a.max_rows}, ajoute un filtre ou --max-rows)" if tronque else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
