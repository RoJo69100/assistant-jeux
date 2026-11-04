"""Test de pipelines/migrer_kb.py (thème, statut, genre de source, auteurs). Lancer : python -I pipelines/test_migrer_kb.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import migrer_kb as m  # noqa: E402

CAS = [
    ("thème tactique", m.theme("11. Tactique et rôles"), "tactique"),
    ("thème rôles DM", m.theme("Rôles"), "roles"),
    ("thème bugs", m.theme("13. Bugs et pièges"), "bugs"),
    ("thème changements", m.theme("6. Changements de règles (la plus récente l'emporte)"), "versions"),
    ("thème par défaut", m.theme("1. Structure", "calendrier"), "calendrier"),
    ("statut confirmé", m.statut("CONFIRMÉ", False), "confirme"),
    ("statut complété", m.statut("complété (avis)", False), "complete"),
    ("statut contredit", m.statut("contredit : le skill fait foi", False), "contredit"),
    ("statut obsolète", m.statut("obsolète depuis v4", True), "obsolete"),
    ("statut vide officiel", m.statut("", True), "confirme"),
    ("statut vide joueur", m.statut("", False), "en_doute"),
    ("genre news", m.genre("basketvibe", "News", "", ""), "patchnote"),
    ("genre dev", m.genre("derbymanager", "#discussion 2024-06-19 dev", "dev", ""), "devlog"),
    ("genre sql", m.genre("sixzeroleague", "SQL", "", ""), "observation"),
    ("genre forum", m.genre("teamsoccer", "QA 06-06", "polsu", ""), "forum"),
    ("genre discord", m.genre("hardwood", "#general 2019-08-20", "bradenwoa", ""), "discord"),
    ("auteurs multiples", m.auteurs("redcapediver ; furysk ; gordie_79"), ["redcapediver", "furysk", "gordie_79"]),
]


def main() -> int:
    ko = 0
    for nom, obtenu, attendu in CAS:
        ok = obtenu == attendu
        ko += not ok
        print(("✅ " if ok else "❌ ") + nom + ("" if ok else f" — obtenu {obtenu!r}"))
    print(f"{len(CAS) - ko}/{len(CAS)}")
    return 1 if ko else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
