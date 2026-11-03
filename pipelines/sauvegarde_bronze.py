"""Sauvegarde incrémentale du bronze (refonte v2, 0.6) : le plan Supabase est Free, donc pas de sauvegarde automatique.

Usage : python -I pipelines/sauvegarde_bronze.py [--dossier CHEMIN] [--verifier-seulement]
Exporte `bronze.raw_pages` et `bronze.discord_messages` (id > dernier id sauvegardé) en NDJSON compressé, un fichier par passage,
dans ~/backups/assistant-jeux/ (hors Git). L'état est dans etat.json ; le comptage cumulé est vérifié contre la base
(le bronze est immuable : count(id <= dernier id) doit être égal au total exporté).
Lecture seule via SUPABASE_DB_URL_RO (rôle assistant_ro). Aucune écriture en base.
Restauration : lire chaque .ndjson.gz, une ligne = un objet JSON de la table ; les colonnes sont celles de la table.
"""
import argparse
import gzip
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
TABLES = {"raw_pages": "bronze.raw_pages", "discord_messages": "bronze.discord_messages"}
LOT = 500
JOURS_ALERTE = 10


def url_ro() -> str:
    for ligne in (RACINE / ".env").read_text(encoding="utf-8").splitlines():
        if ligne.startswith("SUPABASE_DB_URL_RO="):
            return ligne.split("=", 1)[1].strip()
    sys.exit("SUPABASE_DB_URL_RO absent de .env")


def etat_lu(dossier: Path) -> dict:
    f = dossier / "etat.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


def jours_depuis(dossier: Path) -> float | None:
    """Âge en jours de la dernière sauvegarde (None si jamais faite) ; utilisé par rappel_debut.py."""
    e = etat_lu(dossier)
    dates = [v["date"] for v in e.values() if isinstance(v, dict) and "date" in v]
    if not dates:
        return None
    dernier = max(datetime.fromisoformat(d) for d in dates)
    return (datetime.now(timezone.utc) - dernier).total_seconds() / 86400


def exporter(conn, nom: str, table: str, dossier: Path, etat: dict) -> int:
    dernier = etat.get(nom, {}).get("last_id", 0)
    cumul = etat.get(nom, {}).get("count", 0)
    maintenant = datetime.now(timezone.utc)
    fichier = dossier / f"{nom}-{maintenant:%Y%m%dT%H%M%SZ}-apres{dernier}.ndjson.gz"
    n = 0
    max_id = dernier
    with conn.cursor(name=f"sauv_{nom}") as cur, gzip.open(fichier, "wt", encoding="utf-8", newline="\n") as out:
        cur.itersize = LOT
        cur.execute(f"select to_jsonb(t) as ligne from {table} t where id > %s order by id", (dernier,))
        for (ligne,) in cur:
            out.write(json.dumps(ligne, ensure_ascii=False, default=str) + "\n")
            max_id = max(max_id, ligne["id"])
            n += 1
    if n == 0:
        fichier.unlink()
    else:
        etat[nom] = {"last_id": max_id, "count": cumul + n, "date": maintenant.isoformat(), "dernier_fichier": fichier.name}
    return n


def verifier(conn, nom: str, table: str, etat: dict) -> tuple[bool, str]:
    e = etat.get(nom)
    if not e:
        return False, f"{nom} : jamais sauvegardé"
    (en_base,) = conn.execute(f"select count(*) from {table} where id <= %s", (e["last_id"],)).fetchone()
    ok = en_base == e["count"]
    return ok, f"{nom} : {e['count']} lignes sauvegardées, {en_base} en base jusqu'à l'id {e['last_id']} — {'identique' if ok else 'ÉCART'}"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dossier", default=str(Path.home() / "backups" / "assistant-jeux"))
    p.add_argument("--verifier-seulement", action="store_true")
    a = p.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    import psycopg

    dossier = Path(a.dossier)
    dossier.mkdir(parents=True, exist_ok=True)
    etat = etat_lu(dossier)
    with psycopg.connect(url_ro(), connect_timeout=15) as conn:
        conn.read_only = True
        if not a.verifier_seulement:
            for nom, table in TABLES.items():
                n = exporter(conn, nom, table, dossier, etat)
                print(f"{nom} : {n} nouvelles lignes")
            (dossier / "etat.json").write_text(json.dumps(etat, indent=1), encoding="utf-8")
        bons = [verifier(conn, nom, table, etat) for nom, table in TABLES.items()]
    for ok, msg in bons:
        print(("✅ " if ok else "❌ ") + msg)
    return 0 if all(ok for ok, _ in bons) else 1


if __name__ == "__main__":
    sys.exit(main())
