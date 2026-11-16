"""Sauvegarde incrémentale du bronze (refonte v2, 0.6) : le plan Supabase est Free, donc pas de sauvegarde automatique.

Usage : python -I pipelines/sauvegarde_bronze.py [--dossier CHEMIN] [--verifier-seulement] [--lot N]
Exporte `bronze.raw_pages` et `bronze.discord_messages` (id > dernier id sauvegardé) en NDJSON compressé, un fichier par passage,
dans ~/backups/assistant-jeux/ par défaut (hors Git : le dépôt est public, ne jamais y commiter une sauvegarde).
L'état est dans etat.json ; le comptage cumulé est vérifié contre la base
(le bronze est immuable : count(id <= dernier id) doit être égal au total exporté).
Lecture seule, par le transport de pipelines/sql.py (HTTPS public.sql_ro en session cloud, Postgres direct sinon) :
SUPABASE_URL + SUPABASE_SECRET_KEY, ou SUPABASE_DB_URL_RO (voir sql.py). Aucune écriture en base.
Pagination par id (`id > dernier order by id limit LOT`) ; le lot est divisé par deux si une réponse échoue (délai de 20 s de sql_ro,
taille de réponse) puis remonte. Le fichier est écrit en `.part` et renommé à la fin : un arrêt en cours de route ne laisse pas de doublon.
Restauration : lire chaque .ndjson.gz, une ligne = un objet JSON de la table ; les colonnes sont celles de la table.
"""
import argparse
import gzip
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python -I n'ajoute pas le dossier du script
from sql import executer  # noqa: E402

TABLES = {"raw_pages": "bronze.raw_pages", "discord_messages": "bronze.discord_messages"}
LOT = 100
JOURS_ALERTE = 10


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


def lot_suivant(table: str, apres: int, taille: int) -> list[dict]:
    """Lignes (dict) d'id > apres, par id croissant. Divise le lot par deux si la réponse échoue."""
    while True:
        try:
            _, lignes = executer(f"select to_jsonb(r) as ligne from {table} r where r.id > {int(apres)} order by r.id limit {int(taille)}")
            return [json.loads(l[0]) if isinstance(l[0], str) else l[0] for l in lignes]
        except SystemExit as e:  # via_https quitte sur une erreur HTTP / SQL
            if taille <= 1:
                raise
            taille = max(1, taille // 2)
            print(f"  lot réduit à {taille} ({str(e)[:90]})", file=sys.stderr)


def exporter(nom: str, table: str, dossier: Path, etat: dict, lot: int) -> int:
    dernier = etat.get(nom, {}).get("last_id", 0)
    cumul = etat.get(nom, {}).get("count", 0)
    maintenant = datetime.now(timezone.utc)
    fichier = dossier / f"{nom}-{maintenant:%Y%m%dT%H%M%SZ}-apres{dernier}.ndjson.gz"
    part = fichier.with_name(fichier.name + ".part")
    n, max_id, taille = 0, dernier, lot
    with gzip.open(part, "wt", encoding="utf-8", newline="\n") as out:
        while True:
            lignes = lot_suivant(table, max_id, taille)
            if not lignes:
                break
            for ligne in lignes:
                out.write(json.dumps(ligne, ensure_ascii=False, default=str) + "\n")
                max_id = max(max_id, ligne["id"])
            n += len(lignes)
            if n % (10 * lot) < len(lignes):
                print(f"  {nom} : {n} lignes (id {max_id})", file=sys.stderr)
    if n == 0:
        part.unlink()
    else:
        part.rename(fichier)
        etat[nom] = {"last_id": max_id, "count": cumul + n, "date": maintenant.isoformat(), "dernier_fichier": fichier.name}
        (dossier / "etat.json").write_text(json.dumps(etat, indent=1), encoding="utf-8")  # état à jour après chaque table
    return n


def verifier(nom: str, table: str, etat: dict) -> tuple[bool, str]:
    e = etat.get(nom)
    if not e:
        return False, f"{nom} : jamais sauvegardé"
    _, lignes = executer(f"select count(*) as n from {table} where id <= {int(e['last_id'])}")
    en_base = int(lignes[0][0])
    ok = en_base == e["count"]
    return ok, f"{nom} : {e['count']} lignes sauvegardées, {en_base} en base jusqu'à l'id {e['last_id']} — {'identique' if ok else 'ÉCART'}"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dossier", default=str(Path.home() / "backups" / "assistant-jeux"))
    p.add_argument("--verifier-seulement", action="store_true")
    p.add_argument("--lot", type=int, default=LOT)
    a = p.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    dossier = Path(a.dossier)
    dossier.mkdir(parents=True, exist_ok=True)
    etat = etat_lu(dossier)
    if not a.verifier_seulement:
        for nom, table in TABLES.items():
            n = exporter(nom, table, dossier, etat, a.lot)
            print(f"{nom} : {n} nouvelles lignes")
    bons = [verifier(nom, table, etat) for nom, table in TABLES.items()]
    for ok, msg in bons:
        print(("✅ " if ok else "❌ ") + msg)
    return 0 if all(ok for ok, _ in bons) else 1


if __name__ == "__main__":
    sys.exit(main())
