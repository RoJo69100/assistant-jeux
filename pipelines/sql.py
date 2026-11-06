"""Requêtes SQL compactes en lecture seule (refonte v2, 0.4).

Usage :
  python -I pipelines/sql.py "select game, count(*) from bronze.raw_pages group by 1" [--max-rows 30] [--max-col 60]
  python -I pipelines/sql.py --page-id 123 --payload-path "players,0,name"      (un morceau de payload bronze)
Rôle Postgres `assistant_ro` (select sur silver et gold, métadonnées seules de bronze), chaîne SUPABASE_DB_URL_RO dans .env.
Transport : Postgres direct (port 5432) si joignable, sinon HTTPS via la fonction public.sql_ro (sql/silver/ops_005),
qui tourne en assistant_ro ; il faut alors SUPABASE_URL et SUPABASE_SECRET_KEY. Forcer : SQL_TRANSPORT=pg|https.
Sortie : tableau Markdown compact, `limit` ajouté, cellules tronquées, « n lignes / tronqué » en pied.
Toute écriture est refusée ici (une seule instruction select/with/explain) et par le rôle (transaction en lecture seule).
"""
import argparse
import json
import os
import re
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DEBUT_OK = re.compile(r"^\s*(select|with|explain|table|values)\b", re.I)
PAYLOAD = re.compile(r"\b(payload|content)\b", re.I)
ECRITURE = re.compile(r"\b(insert|update|delete|drop|alter|create|truncate|grant|revoke|copy|call|do|vacuum)\b", re.I)


def lire_env(nom: str) -> str | None:
    env = RACINE / ".env"
    if env.exists():
        for ligne in env.read_text(encoding="utf-8").splitlines():
            if ligne.startswith(nom + "="):
                return ligne.split("=", 1)[1].strip()
    v = os.environ.get(nom)  # session cloud : variable de l'environnement, pas de .env
    return v.strip() if v else None


def url_ro() -> str:
    return lire_env("SUPABASE_DB_URL_RO") or sys.exit(
        "SUPABASE_DB_URL_RO absent de .env et de l'environnement (voir sql/silver/ops_001_role_assistant_ro.sql)")


def transport() -> str:
    choix = os.environ.get("SQL_TRANSPORT", "auto")
    if choix in ("pg", "https"):
        return choix
    if os.environ.get("CLAUDE_CODE_REMOTE") == "true":  # session cloud : le port 5432 est bloqué, la sonde coûtait ~6,5 s par appel
        return "https"
    url = lire_env("SUPABASE_DB_URL_RO")
    if url:
        p = urllib.parse.urlparse(url)
        try:
            socket.create_connection((p.hostname, p.port or 5432), timeout=3).close()
            return "pg"
        except OSError:
            pass
    return "https"


def via_pg(sql: str, params):
    import psycopg
    with psycopg.connect(url_ro(), connect_timeout=15) as c, c.cursor() as cur:
        cur.execute(sql, params)
        return [d.name for d in cur.description], cur.fetchall()


def lignes_de(corps):
    """Liste de lignes (dict) depuis la réponse de sql_ro. Une réponse encodée deux fois (chaîne JSON au lieu de liste)
    est décodée ; les chaînes ordinaires des cellules ne sont jamais touchées."""
    brut = corps
    try:
        if isinstance(corps, str):
            corps = json.loads(corps)
        lignes = [json.loads(l) if isinstance(l, str) else l for l in corps]
        if all(isinstance(l, dict) for l in lignes):
            return lignes
    except (ValueError, TypeError):
        pass
    sys.exit(f"réponse inattendue de sql_ro : {type(brut).__name__} : {str(brut)[:200]}")


def via_https(sql: str):
    base, cle = lire_env("SUPABASE_URL"), lire_env("SUPABASE_SECRET_KEY")
    if not base or not cle:
        sys.exit("port 5432 fermé et SUPABASE_URL / SUPABASE_SECRET_KEY absents : pas de transport possible")
    url = base.rstrip("/") + "/rest/v1/rpc/sql_ro?" + urllib.parse.urlencode({"q": sql})
    req = urllib.request.Request(url, headers={"apikey": cle, "Authorization": f"Bearer {cle}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            lignes = lignes_de(json.load(r))
    except urllib.error.HTTPError as e:
        corps = e.read().decode("utf-8", "replace")
        try:
            corps = json.loads(corps).get("message", corps)
        except ValueError:
            pass
        sys.exit(f"erreur SQL (https {e.code}) : {corps}")
    cols = list(lignes[0].keys()) if lignes else []
    return cols, [tuple(json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v
                        for v in l.values()) for l in lignes]


def rpc_post(nom: str, corps: dict):
    """Appelle une fonction d'écriture de la base en POST (HTTPS, clé de service) ; renvoie le JSON de la réponse."""
    base, cle = lire_env("SUPABASE_URL"), lire_env("SUPABASE_SECRET_KEY")
    if not base or not cle:
        sys.exit("SUPABASE_URL / SUPABASE_SECRET_KEY absents de .env et de l'environnement")
    req = urllib.request.Request(base.rstrip("/") + f"/rest/v1/rpc/{nom}", data=json.dumps(corps).encode("utf-8"),
                                 method="POST", headers={"apikey": cle, "Authorization": f"Bearer {cle}",
                                                         "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"erreur (https {e.code}) : {e.read().decode('utf-8', 'replace')[:300]}")


AUTH_REFUSEE = []  # une fois refusé (ou coupe-circuit « too many authentication failures »), on ne réessaye plus Postgres


def auth_refusee(e: Exception) -> bool:
    return "authentication" in str(e).lower()


def lire_pg_ou_https(sql: str, params=None):
    """Postgres direct ; si le serveur répond mais refuse l'authentification, bascule en HTTPS (même requête)."""
    try:
        if AUTH_REFUSEE:
            raise RuntimeError("authentication refusée plus tôt dans ce processus")
        return via_pg(sql, params)
    except Exception as e:  # noqa: BLE001 - psycopg.OperationalError, importé à la demande
        if not auth_refusee(e):
            raise
        AUTH_REFUSEE.append(1)
        if params:
            sql = sql % tuple(litteral(str(p)) if p is not None else "null" for p in params)
        return via_https(sql)


def executer(sql: str, params=None):
    """Lecture sur le transport de sql.py (HTTPS en cloud, Postgres direct sinon) : (colonnes, lignes).
    `params` (%s) n'est pris en charge qu'en Postgres direct ; en HTTPS, la requête doit être littérale (voir litteral())."""
    if transport() == "https":
        if params:
            sql = sql % tuple(litteral(str(p)) if p is not None else "null" for p in params)
        return via_https(sql)
    return lire_pg_ou_https(sql, params)


def litteral(s: str) -> str:
    return "'" + s.replace("'", "''") + "'"


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
    mode = transport()

    if a.payload_path is not None:
        if a.page_id is None:
            sys.exit("--payload-path demande --page-id")
        chemin = [x for x in a.payload_path.split(",") if x != ""]
        sql, params = "select bronze.payload_at(%s, %s) as valeur", (a.page_id, chemin)
        if mode == "https":
            tableau_sql = "array[" + ",".join(litteral(x) for x in chemin) + "]::text[]"
            sql, params = f"select bronze.payload_at({int(a.page_id)}, {tableau_sql}) as valeur", None
    elif a.requete:
        q = verifie(a.requete)
        sql, params = f"select * from ({q}) t limit {a.max_rows + 1}", None
    else:
        p.error("donne une requête ou --page-id et --payload-path")

    cols, lignes = via_https(sql) if mode == "https" else lire_pg_ou_https(sql, params)
    tronque = len(lignes) > a.max_rows
    lignes = lignes[:a.max_rows]
    print(tableau(cols, lignes, a.max_col))
    print(f"\n{len(lignes)} lignes" + (f" (tronqué à {a.max_rows}, ajoute un filtre ou --max-rows)" if tronque else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
