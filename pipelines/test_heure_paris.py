"""Test de pipelines/heure_paris.py : fuseau réel et règle de secours (sans tzdata).

Lancer : python pipelines/test_heure_paris.py   (code 1 si un cas se trompe)
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import heure_paris as h  # noqa: E402

U = lambda *a: datetime(*a, tzinfo=timezone.utc)  # noqa: E731

CAS = [
    ("hiver : UTC+1 (07/11 11:20 UTC)", h.paris(U(2026, 11, 7, 11, 20)).strftime("%H:%M"), "12:20"),
    ("été : UTC+2 (15/07 10:00 UTC)", h.paris(U(2026, 7, 15, 10, 0)).strftime("%H:%M"), "12:00"),
    ("règle : passage à l'été le 29/03/2026 01:00 UTC", str(h.decalage_regle(U(2026, 3, 29, 1, 0))), "2:00:00"),
    ("règle : veille du passage", str(h.decalage_regle(U(2026, 3, 29, 0, 59))), "1:00:00"),
    ("règle : retour à l'hiver le 25/10/2026 01:00 UTC", str(h.decalage_regle(U(2026, 10, 25, 1, 0))), "1:00:00"),
    ("règle : dernier dimanche d'octobre 2026", h.dernier_dimanche(2026, 10).strftime("%d"), "25"),
    ("ligne : jour et heure", h.ligne(U(2026, 11, 7, 11, 20))[:40], "Heure de Paris : samedi 07/11/2026 12:20"),
]

if __name__ == "__main__":
    echecs = 0
    for nom, obtenu, attendu in CAS:
        ok = obtenu == attendu
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom, "" if ok else f"→ {obtenu!r} au lieu de {attendu!r}")
    print(f"{len(CAS) - echecs}/{len(CAS)}")
    sys.exit(1 if echecs else 0)
