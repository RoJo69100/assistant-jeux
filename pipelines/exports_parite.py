"""Non-régression de gold.exports_state (générique) contre les anciennes vues par jeu (refonte v2, phase 1.4).

Compare dans les deux sens (ordre, club, écran, dernier export, statut), six jeux.
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
# jeu -> (ancien, nouveau) au même format (ordre, club, écran, dernier export, statut), en texte.
# Hardwood : l'ancienne vue n'a pas d'ordre, date au format DD/MM HH24:MI ; ses deux lignes calculées
# (feuilles de match, pages joueur) ne sont pas des écrans et restent hors parité.
# Derby Manager : statuts « manquant / en retard / à jour » ramenés aux pastilles ; « commun » = sans club.
_N = ("select ordre::text, coalesce(club, '{sans}'), ecran, dernier_paris::text, statut"
      " from gold.exports_state where game = '{jeu}'")
_STD = "select ordre::text, '{sans}', ecran, dernier_paris::text, statut from {vue}"
ANCIENS = {
    "basketvibe": (_STD.format(sans="", vue="gold.bv_exports_state"), _N.format(sans="", jeu="basketvibe")),
    "hockeynation": (_STD.format(sans="", vue="gold.hn_exports_state"), _N.format(sans="", jeu="hockeynation")),
    "sixzeroleague": (_STD.format(sans="", vue="gold.sz_exports_state"), _N.format(sans="", jeu="sixzeroleague")),
    "teamsoccer": ("select ordre::text, club, ecran, dernier_paris::text, statut from gold.ts_exports_state",
                   _N.format(sans="les deux", jeu="teamsoccer")),
    "hardwood": ("select '', '', quoi, dernier, statut from gold.hw_exports_state"
                 " where quoi !~ '^(Feuilles de match|Pages joueur)'",
                 "select '', '', ecran, to_char(dernier_paris, 'DD/MM HH24:MI'), statut"
                 " from gold.exports_state where game = 'hardwood'"),
    "derbymanager": ("select ordre::text, case when club = 'commun' then '' else club end, page,"
                     " (derniere at time zone 'Europe/Paris')::text,"
                     " case etat when 'manquant' then '🟥 jamais' when 'en retard' then '🟧 à refaire'"
                     " else '🟩 à jour' end from gold.dm_exports_etat",
                     _N.format(sans="", jeu="derbymanager")),
}
REQUETE = """
with a as ({ancien}),
     n as ({nouveau})
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
        for jeu, (ancien, nouveau) in ANCIENS.items():
            cur.execute(REQUETE.format(ancien=ancien, nouveau=nouveau))
            ecarts = cur.fetchall()
            echec |= bool(ecarts)
            lignes.append(f"{aujourdhui}\t{jeu}\t{'ecart' if ecarts else 'ok'}\t{len(ecarts)}")
            for sens, ordre, club, ecran, dernier, statut in ecarts[:5]:
                print(f"❌ {jeu} {sens} : {ordre} {club} {ecran} — {dernier} {statut}")
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    with JOURNAL.open("a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lignes) + "\n")
    bilan = ", ".join(f"{j} {jours_ok(j)}/7 jours" for j in ANCIENS)
    print(f"{'❌' if echec else '✅'} parité exports : {bilan}")
    return 1 if echec else 0


if __name__ == "__main__":
    sys.exit(main())
