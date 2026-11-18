"""Test de experiences_deduites.py (logique seule, sans base).

Lancer : python -I pipelines/test_experiences_deduites.py   (code 1 si un cas se trompe)
"""
import datetime as dt
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from aujourdhui_sources import FICHIER_EXPERIENCES  # noqa: E402
from experiences_deduites import plan  # noqa: E402

CONF = yaml.safe_load(FICHIER_EXPERIENCES.read_text(encoding="utf-8"))


def am(fid, jour, agress=2, zone="Perimeter", tir=0, primary=0, uniforme=True, opp="Adv"):
    return {"fixture_id": fid, "match_day": jour, "opponent": f"{opp}{fid}", "agress_uniforme": uniforme,
            "agress_cran": agress if uniforme else None, "zone": zone, "tir_cran4_joueurs": tir, "primary_quarts": primary}


def etiq(amicaux, controles=None, faits=()):
    controles = {a["fixture_id"] for a in amicaux} if controles is None else controles
    return [(p["id"], p["niveau"]) for p in plan(amicaux, controles, CONF, list(faits))]


CAS = [
    ("deux réglages modifiés (agressivité 4 + zone Middle) = aucune ligne",
     etiq([am("a", "2026-11-12", agress=4, zone="Middle")]), []),
    ("deux réglages modifiés (tir 2 + Primary 4) = aucune ligne",
     etiq([am("a", "2026-11-12", tir=2, primary=4)]), []),
    ("tout neutre, E1 en cours = E1:A", etiq([am("a", "2026-11-12")]), [("E1", "A")]),
    ("seule l'agressivité à 4 = E1:B", etiq([am("a", "2026-11-12", agress=4)]), [("E1", "B")]),
    ("seule la zone Rim = E5:C", etiq([am("a", "2026-11-12", zone="Rim")]), [("E5", "C")]),
    ("seuls 2 tireurs au cran 4 = E2:A", etiq([am("a", "2026-11-12", tir=2)]), [("E2", "A")]),
    ("agressivité non uniforme = aucune ligne", etiq([am("a", "2026-11-12", uniforme=False)]), []),
    ("écran sauvegardé non contrôlé = aucune ligne", etiq([am("a", "2026-11-12")], controles=set()), []),
    ("amical avant debut (09/11) = aucune ligne", etiq([am("a", "2026-11-09")]), []),
    ("déjà au registre (même clé) = aucune ligne",
     etiq([am("a", "2026-11-12")], faits=[{"id": "E1", "niveau": "A",
                                           "cle": {"nom": "Adva", "date": dt.date(2026, 11, 12)}}]), []),
    ("E1 terminée (4 faits) : tout neutre = E5:A",
     etiq([am("a", "2026-11-12")], faits=[{"id": "E1", "niveau": "A", "cle": None}] * 4), [("E5", "A")]),
]


def main() -> int:
    ko = [(n, g, a) for n, g, a in CAS if g != a]
    for n, g, a in ko:
        print(f"KO {n} : obtenu {g}, attendu {a}")
    print(f"{len(CAS) - len(ko)}/{len(CAS)}")
    return 1 if ko else 0


if __name__ == "__main__":
    sys.exit(main())
