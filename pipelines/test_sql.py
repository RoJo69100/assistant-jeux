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

if __name__ == "__main__":
    echecs = 0
    for nom, q, attendu in CAS:
        try:
            sqlmod.verifie(q)
            accepte = True
        except SystemExit:
            accepte = False
        ok = accepte == attendu
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    print(f"{len(CAS) - echecs}/{len(CAS)}")
    sys.exit(1 if echecs else 0)
