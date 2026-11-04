"""Non-régression de gold.daily_alerts (générique) contre les anciennes vues par jeu (refonte v2, phase 1.4).

Compare dans les deux sens (priorité, domaine, texte), hors domaines à écart voulu (VOULUS, raison citée).
Chaque passage ajoute une ligne à outputs/refonte-v2/parite-alertes.log (date, jeu, ok, écarts) ;
le critère de bascule est 7 dates distinctes sans écart pour chaque jeu.
Usage : python -I pipelines/alertes_parite.py   (code 1 s'il y a un écart)
"""

import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python -I n'ajoute pas le dossier du script
from sql import url_ro  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent
JOURNAL = RACINE / "outputs/refonte-v2/parite-alertes.log"
# (priorité, domaine, texte, club) ; club = équipe de l'ancienne vue (Team Soccer), sinon nul.
ANCIENS = {
    "basketvibe": "select priority, category, alert, null::text from gold.bv_daily_alerts",
    "hockeynation": "select prio, domaine, alerte, null::text from gold.hn_daily_alerts",
    "teamsoccer": "select priority, category, alert, team from gold.ts_daily_alerts",
    "sixzeroleague": "select priority, category, alert, null::text from gold.sz_daily_alerts",
    "hardwood": "select prio, categorie, alerte, null::text from gold.hw_daily_alerts",
}
# Domaines où la vue générique diffère exprès (sources dans core.alert_rule).
VOULUS = {
    "basketvibe": {
        "export": "fraîcheur lue dans gold.exports_state (parité à part : exports_parite.py)",
        "match": "matchs de coupe et de ligue passés sans résultat signalés ; compétition en français",
    },
    "hockeynation": {"match": "matchs passés encore « upcoming » signalés (nouveau domaine)"},
    "teamsoccer": {"export": "un écran par ligne et par club, lu dans gold.exports_state (exports_parite.py)"},
    "sixzeroleague": {"export": "14 écrans au lieu de 5, même hors saison, lus dans gold.exports_state"},
}
REQUETE = """
with a as (select * from ({ancien}) x(prio, domaine, alerte, club) where domaine <> all(%s)),
     n as (select prio, domaine, alerte, club from gold.daily_alerts where game = %s and domaine <> all(%s))
(select 'ancien seul', * from (select * from a except select * from n) x)
union all
(select 'nouveau seul', * from (select * from n except select * from a) y)
order by 3, 4, 1
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
            exclus = list(VOULUS.get(jeu, {}))
            cur.execute(REQUETE.format(ancien=ancien), (exclus, jeu, exclus))
            ecarts = cur.fetchall()
            echec |= bool(ecarts)
            lignes.append(f"{aujourdhui}\t{jeu}\t{'ecart' if ecarts else 'ok'}\t{len(ecarts)}")
            for sens, prio, domaine, alerte, club in ecarts[:5]:
                print(f"❌ {jeu} {sens} : {prio} {domaine} {club or ''} — {alerte}")
            for domaine, raison in VOULUS.get(jeu, {}).items():
                print(f"⚪ {jeu} {domaine} hors parité : {raison}")
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    with JOURNAL.open("a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lignes) + "\n")
    bilan = ", ".join(f"{j} {jours_ok(j)}/7 jours" for j in ANCIENS)
    print(f"{'❌' if echec else '✅'} parité alertes : {bilan}")
    return 1 if echec else 0


if __name__ == "__main__":
    sys.exit(main())
