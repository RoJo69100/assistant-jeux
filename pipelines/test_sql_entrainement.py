"""Tests de structure des migrations SQL entraînement (22/11) : lecture du texte des fichiers, aucune base requise.
La vérification sur données (13/11 -> 22/11, k = 2) se fait par requête de lecture seule : voir le journal de la session."""
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SILVER = (RACINE / "sql/silver/009_bv_week_on_training.sql").read_text(encoding="utf-8")
GOLD = (RACINE / "sql/gold/005_bv_training.sql").read_text(encoding="utf-8")


def vue(texte, nom):
    m = re.search(rf"create or replace view {re.escape(nom)} .*?;\n", texte, re.S)
    return m.group(0) if m else ""


def cas():
    hebdo = vue(SILVER, "silver.bv_player_weekly")
    jour = vue(SILVER, "silver.bv_player_daily")
    gains = vue(GOLD, "gold.bv_training_gains_exact")
    # 1. une semaine avec un relevé sans entraînement après un relevé avec : le relevé précis passe avant le dernier jour
    yield "silver : le relevé avec valeurs précises passe avant le dernier jour tout court", \
        re.search(r"order by .*\(d\.two_point_exact is not null\) desc, d\.day desc", hebdo, re.S) is not None
    # 2. un trou de 2 semaines : plus d'exigence « exactement 7 jours », gain par entraînement = écart / k
    yield "gold : plus d'exigence de 7 jours exactement", "= 7" not in gains
    yield "gold : k semaines d'écart, gain = écart / k, colonnes k et ecart", \
        "/ 7) as k" in gains and "/ p.k, 3) as gain" in gains and "as k" in gains and "as ecart" in gains
    yield "gold : le relevé précédent est le relevé précis précédent", "where w.two_point_exact is not null" in gains
    # 3. capture d'entraînement sans Aperçu le même jour (22/11) : le jour est gardé
    yield "silver : une capture d'entraînement sans Aperçu le même jour n'est plus perdue", \
        "union" in jour and "from silver.bv_player_training" in jour.split("union")[1].split("select o2")[0]
    yield "silver : les champs d'aperçu viennent du dernier aperçu antérieur", "o2.day <= j.day" in jour


JEUX = list(cas())

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    echecs = 0
    for nom, ok in JEUX:
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    print(f"{len(JEUX) - echecs}/{len(JEUX)}")
    sys.exit(1 if echecs else 0)
