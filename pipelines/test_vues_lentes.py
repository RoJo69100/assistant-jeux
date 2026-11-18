"""Vues lentes du plan BasketVibe (18/11) : « vendre » (gold.bv_sell_candidates) et « matchs_autres » doivent répondre en moins de
5 s et ne jamais donner « vue … illisible » dans le plan. Test sur la base réelle (lecture seule, mêmes requêtes que aujourdhui.py).
Lancer : python -I pipelines/test_vues_lentes.py   (code 1 si un cas se trompe)"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import aujourdhui as auj  # noqa: E402
import que_faire_blocs as qfb  # noqa: E402
import sql as sqlmod  # noqa: E402

LIMITE_S = 5.0
VUES = {"vendre": "gold.bv_sell_candidates", "matchs_autres": "matchs d'autres clubs",
        "gold.bv_sell_replacement": "remplaçant par poste, migration 088"}


def lire(nom):
    t0 = time.perf_counter()
    try:
        return sqlmod.executer(auj.REQUETES[nom]), None, time.perf_counter() - t0
    except SystemExit as e:
        return None, str(e), time.perf_counter() - t0
    except Exception as e:  # noqa: BLE001
        return None, f"{type(e).__name__}: {e}", time.perf_counter() - t0


def cas():
    donnees = {}
    for nom, quoi in VUES.items():
        d, err, s = lire(nom)
        donnees[nom] = d
        yield f"{nom} ({quoi}) : lisible ({err or 'ok'})", d is not None
        yield f"{nom} ({quoi}) : {s:.1f} s < {LIMITE_S:.0f} s", s < LIMITE_S
    # le plan n'imprime pas « illisible » pour ces deux vues (bloc 4 et bloc 6 du rendu)
    for nom in ("prix_cases", "matchs_captes", "matchs_ajoutes"):
        donnees[nom], _, _ = lire(nom)
    rendu = "\n".join(qfb.bloc_4(donnees, {}, None, 1.0) + qfb.bloc_6(donnees, [], auj_jour(), None, "")[0])
    for nom in VUES:
        yield f"plan : pas de « vue {nom} illisible »", f"vue {nom} illisible" not in rendu
    autres = auj.lignes_de(donnees, "matchs_autres") if donnees["matchs_autres"] else []
    yield f"matchs d'autres clubs comptés ({len(autres)})", len(autres) > 0


MIGRATION_MINS = Path(__file__).resolve().parent.parent / "sql" / "gold" / "089_bv_sell_minutes_sur_4.sql"


def cas_minutes_sur_4():
    """18/11 : league_min_last4 = somme des minutes sur les 4 derniers matchs de ligue de l'équipe / 4 (0 pour un match non joué).
    Le CTE `mins` de la migration (entre -- MINS-DEBUT et -- MINS-FIN) tourne sur des lignes synthétiques."""
    if not MIGRATION_MINS.exists():
        yield f"migration {MIGRATION_MINS.name} présente", False
        return
    t = MIGRATION_MINS.read_text(encoding="utf-8")
    cte = t[t.index("-- MINS-DEBUT"):t.index("-- MINS-FIN")].split("\n", 1)[1].rstrip().rstrip(",")
    lignes = ("lignes(fixture_id, competition, match_day, player_id, min) as (values "
              "('f0','league',1,'A',30),('f0','league',1,'B',40),('f1','league',2,'A',30),('f2','league',3,'A',30),"
              "('f3','league',4,'A',30),('f4','league',5,'A',30),('f4','league',5,'B',12),('c1','cup',6,'B',40))")
    q = "with " + lignes + ", " + cte.replace("gold.bv_match_player_lines", "lignes") + " select player_id, league_min_last4 from mins order by 1"
    _, l = sqlmod.executer(q)
    r = {a: float(b) for a, b in l}
    yield f"1 match de 12 min sur les 4 derniers de ligue → 3,0 ({r.get('B')})", r.get("B") == 3.0
    yield f"4 matchs de 30 min → 30,0 ({r.get('A')})", r.get("A") == 30.0


def auj_jour():
    from heure_paris import paris
    return paris().date()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    jeux = list(cas()) + list(cas_minutes_sur_4())
    echecs = 0
    for n, ok in jeux:
        echecs += not ok
        print("OK " if ok else "ECHEC ", n)
    print(f"{len(jeux) - echecs}/{len(jeux)}")
    sys.exit(1 if echecs else 0)
