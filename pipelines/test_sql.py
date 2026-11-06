"""Test de pipelines/sql.py : refus des écritures et du payload bronze entier (sans connexion à la base).

Lancer : python pipelines/test_sql.py   (code 1 si un cas se trompe)
"""
import importlib.util
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("sqlmod", Path(__file__).resolve().parent / "sql.py")
sqlmod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sqlmod)

CAS = [
    ("select simple", "select 1", True),
    ("with", "with a as (select 1) select * from a", True),
    ("point-virgule final", "select 1;", True),
    ("sha256 bronze", "select id, payload_sha256 from bronze.raw_pages", True),
    ("mot d'écriture dans une chaîne", "select 'update' as x", True),
    ("update", "update gold.x set a = 1", False),
    ("delete", "delete from silver.x", False),
    ("deux instructions", "select 1; select 2", False),
    ("drop caché", "select 1 from t where a in (select 1) and drop", False),
    ("payload bronze", "select payload from bronze.raw_pages", False),
    ("content bronze", "select content from bronze.discord_messages", False),
    ("payload hors bronze", "select payload from silver.bv_x", True),
]

def bascule_https():
    """Postgres répond mais refuse l'authentification : la lecture passe en https ; autre erreur : relancée."""
    class Refus(Exception):
        pass

    vus = []
    sqlmod.via_pg = lambda sql, params: (_ for _ in ()).throw(Refus('FATAL: password authentication failed for user "postgres"'))
    sqlmod.via_https = lambda sql: vus.append(sql) or (["ok"], [(1,)])
    r = sqlmod.lire_pg_ou_https("select 1")
    yield "auth refusée : bascule https", r == (["ok"], [(1,)]) and vus == ["select 1"]
    sqlmod.via_pg = lambda sql, params: (_ for _ in ()).throw(Refus("syntax error"))
    try:
        sqlmod.lire_pg_ou_https("select 1")
        yield "autre erreur : relancée", False
    except Refus:
        yield "autre erreur : relancée", len(vus) == 1


if __name__ == "__main__":
    echecs = 0
    extra = list(bascule_https())
    for nom, ok in extra:
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    total = len(CAS) + len(extra)
    for nom, q, attendu in CAS:
        try:
            sqlmod.verifie(q)
            accepte = True
        except SystemExit:
            accepte = False
        ok = accepte == attendu
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    print(f"{total - echecs}/{total}")
    sys.exit(1 if echecs else 0)
