"""Demande le rafraîchissement des vues matérialisées avant le que faire d'aujourd'hui (refonte v3, S4b).

Usage : python -I pipelines/rafraichir_avant_aujourdhui.py [--attendre]
Appelle public.rafraichir_avant_aujourdhui() en POST (HTTPS, clé de service) : la fonction écrit une demande, que le job pg_cron
« rafraichir-demande » exécute dans la minute. Pas par sql.py : sql_ro est en lecture seule et ne peut pas écrire la demande.
Réponses : « à jour : rafraîchi à HH:MM:SS » | « demandé … » | « déjà demandé … » | « en cours … ».
--attendre : repose la question toutes les 20 s (330 s au plus : un rafraîchissement complet dure ~3 min) jusqu'à « à jour ».
Dans une session, lancer avec un délai d'outil de 600 s (le délai par défaut de 120 s coupe l'attente).
"""
import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sql import lire_env  # noqa: E402


def appeler() -> str:
    base, cle = lire_env("SUPABASE_URL"), lire_env("SUPABASE_SECRET_KEY")
    if not base or not cle:
        sys.exit("SUPABASE_URL / SUPABASE_SECRET_KEY absents de .env et de l'environnement")
    req = urllib.request.Request(
        base.rstrip("/") + "/rest/v1/rpc/rafraichir_avant_aujourdhui", data=b"{}", method="POST",
        headers={"apikey": cle, "Authorization": f"Bearer {cle}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"erreur (https {e.code}) : {e.read().decode('utf-8', 'replace')[:300]}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--attendre", action="store_true")
    a = p.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    t0 = time.perf_counter()
    rep = appeler()
    print(rep, flush=True)
    while a.attendre and not rep.startswith("à jour") and time.perf_counter() - t0 < 330:
        time.sleep(20)
        rep = appeler()
        print(rep, flush=True)
    print(f"({time.perf_counter() - t0:.1f} s)")
    return 0 if rep.startswith("à jour") or not a.attendre else 1


if __name__ == "__main__":
    sys.exit(main())
