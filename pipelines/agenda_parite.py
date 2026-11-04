"""Non-régression de gold.agenda (générique) contre les anciens agendas par jeu (refonte v2, phase 1.4).

Compare dans les deux sens (jour, heure, priorité, catégorie, texte) sur la fenêtre de 7 jours.
Écart voulu toléré : une ligne de l'ancien datée du lendemain avec la même heure et le même texte
(règle « avant le coup d'envoi » d'un match de 00:00, que l'ancienne vue datait du jour du match).
Chaque passage ajoute une ligne à outputs/refonte-v2/parite-agenda.log (date, jeu, ok, écarts) ;
le critère de fin de phase 1 est 7 dates distinctes sans écart pour chaque jeu.
Usage : python -I pipelines/agenda_parite.py   (code 1 s'il y a un écart non toléré)
"""

import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python -I n'ajoute pas le dossier du script
from sql import url_ro  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent
JOURNAL = RACINE / "outputs/refonte-v2/parite-agenda.log"
NOUVEAU = "select day, at_time, priority, category, action from gold.agenda where game = '{jeu}'"
# jeu -> (ancien, nouveau) au même format (day, at_time, priority, category, action).
# Hockey Nation : l'ancien calendrier n'a ni heure, ni priorité, ni catégorie ; on compare le jour et le texte
# (sans le préfixe « Jn : », casse ignorée) sur la fenêtre de 7 jours.
ANCIENS = {
    "basketvibe": ("select day, at_time, priority, category, action from gold.bv_agenda", NOUVEAU.format(jeu="basketvibe")),
    "hockeynation": (
        "select t.day1 + c.day - 1 as day, null::time as at_time, 0 as priority, '' as category, lower(c.event) as action"
        " from gold.hn_calendar c, gold.hn_today t where t.day1 + c.day - 1 between current_date and current_date + 6",
        "select day, null::time as at_time, 0 as priority, '' as category,"
        " lower(regexp_replace(action, '^J[0-9]+ : ', '')) as action from gold.agenda"
        " where game = 'hockeynation' and rule_id ~ '^j[0-9]+$'",
    ),
}
REQUETE = """
with a as ({ancien}),
     n as ({nouveau}),
     ao as (select * from a except select * from n),
     no as (select * from n except select * from a)
select 'ancien seul', ao.* from ao
 where not exists (select 1 from no where no.day = ao.day - 1 and no.at_time = ao.at_time and no.action = ao.action)
union all
select 'nouveau seul', no.* from no
 where not exists (select 1 from ao where ao.day = no.day + 1 and ao.at_time = no.at_time and ao.action = no.action)
order by 2, 3
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
            for sens, day, heure, _p, cat, action in ecarts[:5]:
                print(f"❌ {jeu} {sens} : {day} {heure} {cat} — {action}")
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    with JOURNAL.open("a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lignes) + "\n")
    bilan = ", ".join(f"{j} {jours_ok(j)}/7 jours" for j in ANCIENS)
    print(f"{'❌' if echec else '✅'} parité agenda : {bilan}")
    return 1 if echec else 0


if __name__ == "__main__":
    sys.exit(main())
