"""Contrôle de la couverture des captures (migration gold 077 : gold.couverture_captures, gold.derniere_capture, gold.bv_captures_manquantes).

Lancer : python -I pipelines/test_couverture_captures.py   (code 1 si un contrôle échoue)
Partie A (hors ligne, toujours) : les lignes du plan BasketVibe et Hockey Nation à partir de données figées.
Partie B (base réelle via pipelines/sql.py) : cohérence des trois vues ; ignorée, et dite ignorée, si la base n'est pas joignable
(pas de .env). Les mêmes requêtes ont été passées par le connecteur Supabase le jour de la migration (voir le journal).
"""
import datetime as dt
import importlib.util
import sys
from pathlib import Path

DOSSIER = Path(__file__).resolve().parent
sys.path.insert(0, str(DOSSIER))
import aujourdhui_hockeynation as hn  # noqa: E402
import test_aujourdhui as ta  # noqa: E402

auj = ta.auj


def main() -> int:
    echecs = 0

    def controle(nom, ok, detail=""):
        nonlocal echecs
        echecs += 0 if ok else 1
        print(f"{'ok ' if ok else 'ÉCHEC'} {nom}{' : ' + detail if detail else ''}")

    # --- A. plan BasketVibe ---
    d = ta.figees()
    d["gold.derniere_capture"] = (["ligne"], [("Dernière capture il y a 2 h",)])
    d["gold.bv_captures_manquantes"] = (["kind", "ref", "libelle", "day", "manque", "age_j"], [
        ("match", "m1", "Opper Cards", dt.date(2026, 11, 10), "box, quarts, play-by-play", None),
        ("club", "kk-bedex", "KK Bedex", None, "effectif", 9.5),
        ("club", "autre", "Autre club", None, "effectif", 8.0),
    ])
    p = auj.plan(d, {}, ta.JOUR, ta.SOIR)
    controle("BV : « Dernière capture il y a X h » dans les autres points", "Dernière capture il y a 2 h" in p["infos"], str(p["infos"][:2]))
    controle("BV : match sans box/quarts/play-by-play réclamé",
             any("Opper Cards (10/11) : box, quarts, play-by-play manquent" in e for e in p["exports"]), str(p["exports"][:3]))
    controle("BV : clubs à plus de 7 jours regroupés en une ligne",
             sum("club(s) adverse(s) vieux de plus de 7 jours" in e for e in p["exports"]) == 1
             and any("2 club(s)" in e and "KK Bedex" in e for e in p["exports"]))
    p0 = auj.plan(ta.figees(), {}, ta.JOUR, ta.SOIR)
    controle("BV : sans les vues, aucune ligne ajoutée", not any("Dernière capture" in i for i in p0["infos"]) and not any("manquent" in e for e in p0["exports"]))
    controle("BV : requêtes déclarées", "gold.derniere_capture" in auj.REQUETES and "gold.bv_captures_manquantes" in auj.REQUETES)
    d["gold.base_taille"] = (["ligne"], [("Base : 287 Mo sur 500 (plan gratuit), croissance ~1,7 Mo/jour sur 7 jours",)])
    pb = auj.plan(d, {}, ta.JOUR, ta.SOIR)
    controle("BV : ligne « Base : X Mo sur 500 » dans les autres points",
             any(i.startswith("Base : 287 Mo sur 500") for i in pb["infos"]), str(pb["infos"][:3]))
    controle("BV : sans la vue base, aucune ligne Base", not any(i.startswith("Base :") for i in p0["infos"]))
    controle("BV : requête base_taille déclarée", "gold.base_taille" in auj.REQUETES)

    # --- A. plan Hockey Nation ---
    donnees = ta.charger() if hasattr(ta, "charger") else None
    import test_aujourdhui_hockeynation as th  # noqa: E402
    dn = th.charger()
    cols, rows = dn["divers"]
    dn["divers"] = (cols, rows + [("capture", {"game": "hockeynation", "ligne": "Dernière capture il y a 195 h"})])
    r = hn.plan_du_jour(dn, th.JOUR, th.FAIT, th.LEARNINGS, th.DEPUIS)
    controle("HN : « Dernière capture il y a X h » en tête du temps 1", "Dernière capture il y a 195 h" in r["temps1"].splitlines()[:4], r["temps1"].splitlines()[:3].__str__())
    r0 = hn.plan_du_jour(th.charger(), th.JOUR, th.FAIT, th.LEARNINGS, th.DEPUIS)
    controle("HN : sans la vue, aucune ligne ajoutée", "Dernière capture" not in r0["temps1"])

    # --- B. base réelle ---
    try:
        spec = importlib.util.spec_from_file_location("sqlmod", DOSSIER / "sql.py")
        sqlmod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sqlmod)
        _, l = sqlmod.executer("select count(*) from gold.derniere_capture")
        vivant = True
    except BaseException as e:  # noqa: BLE001 - SystemExit de sql.py sans .env
        vivant = False
        print(f"IGNORÉ partie B (base non joignable depuis cette machine : {str(e)[:80]})")
    if vivant:
        def un(sql):
            return sqlmod.executer(sql)[1][0]
        n_jeux = un("select count(distinct game) from bronze.raw_pages")[0]
        controle("derniere_capture : une ligne par jeu", un("select count(*) from gold.derniere_capture")[0] == n_jeux, f"{n_jeux} jeux")
        controle("couverture_captures : une ligne par (jeu, page_type)",
                 un("select count(*) from gold.couverture_captures")[0] == un("select count(*) from (select distinct game, page_type from bronze.raw_pages) t")[0])
        controle("couverture_captures : total = bronze.raw_pages",
                 un("select sum(n_total) from gold.couverture_captures")[0] == un("select count(*) from bronze.raw_pages")[0])
        controle("derniere_capture : libellé", un("select bool_and(ligne ~ '^Dernière capture il y a (moins d''1|[0-9]+) h$') from gold.derniere_capture")[0] is True)
        controle("bv_captures_manquantes : clubs > 7 jours seulement",
                 un("select count(*) from gold.bv_captures_manquantes where kind = 'club' and age_j <= 7")[0] == 0)
        controle("bv_captures_manquantes : matchs des 14 derniers jours joués",
                 un("select count(*) from gold.bv_captures_manquantes m where kind = 'match' and (m.day < (now() at time zone 'Europe/Paris')::date - 14 "
                    "or m.manque = '')")[0] == 0)

    print(f"\n{'TOUT VERT' if not echecs else str(echecs) + ' ÉCHEC(S)'}")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
