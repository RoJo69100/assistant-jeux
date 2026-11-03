"""Non-régression de gold.finance_health (générique) contre les anciennes vues par jeu (refonte v2, phase 1.4).

Compare dans les deux sens les colonnes communes (BV : date, solde, charges, salaires ; HN : plafond, masse, marge).
capacite_invest et reserve n'existaient pas dans les anciennes vues : pas de parité possible, règle dans core.game_params.
Chaque passage ajoute une ligne à outputs/refonte-v2/parite-finances.log (date, jeu, ok, écarts) ;
le critère de bascule est 7 dates distinctes sans écart pour chaque jeu.
Usage : python -I pipelines/finances_parite.py   (code 1 s'il y a un écart)
"""

import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python -I n'ajoute pas le dossier du script
from sql import url_ro  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent
JOURNAL = RACINE / "outputs/refonte-v2/parite-finances.log"
PAIRES = {
    "basketvibe": (
        "select as_of, balance, weekly_fixed_costs, weekly_salaries from gold.bv_finance_health",
        "select as_of, balance, charges_periode, salaries from gold.finance_health where game = 'basketvibe'",
    ),
    "hockeynation": (
        "select salary_cap, projected_salary, cap_space from silver.hn_cap_now",
        "select wage_cap, salaries, cap_space from gold.finance_health where game = 'hockeynation'",
    ),
}
REQUETE = """
with a as ({ancien}), n as ({nouveau})
(select 'ancien seul' as sens, row_to_json(x)::text from (select * from a except select * from n) x)
union all
(select 'nouveau seul', row_to_json(y)::text from (select * from n except select * from a) y)
"""


def jours_ok(jeu: str) -> int:
    if not JOURNAL.exists():
        return 0
    return len({l.split("\t")[0] for l in JOURNAL.read_text(encoding="utf-8").splitlines()
                if l.split("\t")[1:3] == [jeu, "ok"]})


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    import psycopg

    aujourdhui = dt.date.today().isoformat()
    lignes, echec = [], False
    with psycopg.connect(url_ro(), connect_timeout=15) as c, c.cursor() as cur:
        for jeu, (ancien, nouveau) in PAIRES.items():
            cur.execute(REQUETE.format(ancien=ancien, nouveau=nouveau))
            ecarts = cur.fetchall()
            echec |= bool(ecarts)
            lignes.append(f"{aujourdhui}\t{jeu}\t{'ecart' if ecarts else 'ok'}\t{len(ecarts)}")
            for sens, ligne in ecarts[:5]:
                print(f"❌ {jeu} {sens} : {ligne}")
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    with JOURNAL.open("a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lignes) + "\n")
    bilan = ", ".join(f"{j} {jours_ok(j)}/7 jours" for j in PAIRES)
    print(f"{'❌' if echec else '✅'} parité finances : {bilan}")
    return 1 if echec else 0


if __name__ == "__main__":
    sys.exit(main())
