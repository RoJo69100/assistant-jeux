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
VUES = {"vendre": "gold.bv_sell_candidates", "matchs_autres": "matchs d'autres clubs"}


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
    for nom in ("prix_cases", "gold.bv_sell_replacement", "matchs_captes", "matchs_ajoutes"):
        donnees[nom], _, _ = lire(nom)
    rendu = "\n".join(qfb.bloc_4(donnees, {}, None, 1.0) + qfb.bloc_6(donnees, [], auj_jour(), None, "")[0])
    for nom in VUES:
        yield f"plan : pas de « vue {nom} illisible »", f"vue {nom} illisible" not in rendu
    autres = auj.lignes_de(donnees, "matchs_autres") if donnees["matchs_autres"] else []
    yield f"matchs d'autres clubs comptés ({len(autres)})", len(autres) > 0


def auj_jour():
    from heure_paris import paris
    return paris().date()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    jeux = list(cas())
    echecs = 0
    for n, ok in jeux:
        echecs += not ok
        print("OK " if ok else "ECHEC ", n)
    print(f"{len(jeux) - echecs}/{len(jeux)}")
    sys.exit(1 if echecs else 0)
