"""Non-régression de gold.exports_state (générique) contre les anciennes vues par jeu (refonte v2, phase 1.4).

Compare dans les deux sens (ordre, écran, pour quoi, dernier export, statut).
Chaque passage ajoute une ligne à outputs/refonte-v2/parite-exports.log (date, jeu, ok, écarts) ;
le critère de bascule est 7 dates distinctes sans écart pour chaque jeu.
Usage : python -I pipelines/exports_parite.py   (code 1 s'il y a un écart)
"""

import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python -I n'ajoute pas le dossier du script
from sql import url_ro  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent
JOURNAL = RACINE / "outputs/refonte-v2/parite-exports.log"
ANCIENS = {"basketvibe": "gold.bv_exports_state", "hockeynation": "gold.hn_exports_state"}
REQUETE = """
with a as (select ordre, ecran, pour_quoi, dernier_paris, statut from {ancien}),
     n as (select ordre, ecran, pour_quoi, dernier_paris, statut from gold.exports_state where game = %s)
(select 'ancien seul', * from (select * from a except select * from n) x)
union all
(select 'nouveau seul', * from (select * from n except select * from a) y)
order by 2, 1
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
        for jeu, ancien in ANCIENS.items():
            cur.execute(REQUETE.format(ancien=ancien), (jeu,))
            ecarts = cur.fetchall()
            echec |= bool(ecarts)
            lignes.append(f"{aujourdhui}\t{jeu}\t{'ecart' if ecarts else 'ok'}\t{len(ecarts)}")
            for sens, ordre, ecran, _pq, dernier, statut in ecarts[:5]:
                print(f"❌ {jeu} {sens} : {ordre} {ecran} — {dernier} {statut}")
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    with JOURNAL.open("a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lignes) + "\n")
    bilan = ", ".join(f"{j} {jours_ok(j)}/7 jours" for j in ANCIENS)
    print(f"{'❌' if echec else '✅'} parité exports : {bilan}")
    return 1 if echec else 0


if __name__ == "__main__":
    sys.exit(main())
