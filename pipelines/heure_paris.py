"""Heure de Paris, jamais celle du shell (erreur 84, récidive du 2026-11-07 : `date` de Git Bash rendait l'UTC).

Hook UserPromptSubmit : la ligne imprimée entre dans le contexte de chaque tour, donc tout plan part de la bonne heure.
En ligne de commande (agents) : python -I pipelines/heure_paris.py
Sans base de fuseaux (tzdata absent) : règle européenne de l'heure d'été (dernier dimanche de mars et d'octobre, 01:00 UTC).
Tests : test_heure_paris.py.
"""

import sys
from datetime import datetime, timedelta, timezone

JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


def dernier_dimanche(annee: int, mois: int) -> datetime:
    d = datetime(annee, mois + 1, 1, 1, tzinfo=timezone.utc) - timedelta(days=1)
    return d - timedelta(days=(d.weekday() - 6) % 7)


def decalage_regle(utc: datetime) -> timedelta:
    ete = dernier_dimanche(utc.year, 3) <= utc < dernier_dimanche(utc.year, 10)
    return timedelta(hours=2 if ete else 1)


def paris(utc: datetime | None = None) -> datetime:
    utc = utc or datetime.now(timezone.utc)
    try:
        from zoneinfo import ZoneInfo
        return utc.astimezone(ZoneInfo("Europe/Paris"))
    except Exception:  # noqa: BLE001 - ZoneInfoNotFoundError sans tzdata
        return (utc + decalage_regle(utc)).replace(tzinfo=None)


def ligne(utc: datetime | None = None) -> str:
    p = paris(utc)
    return f"Heure de Paris : {JOURS[p.weekday()]} {p:%d/%m/%Y %H:%M} (source : pipelines/heure_paris.py, pas `date`)"


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(ligne())
