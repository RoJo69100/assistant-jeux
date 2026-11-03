"""Test de contrat core (refonte v2, phase 1.3) : chaque adaptateur respecte-t-il le contrat de build_core.py ?

Par jeu et par entité branchée (section core: de docs/attentes/jeux/<jeu>.yaml) :
  colonnes et types, clés non nulles, unicité de la clé, plages (0–1, 0–100, valeurs permises),
  colonnes entièrement nulles (⚪ si déclarées dans limites, ❌ sinon), fraîcheur (dernier jour).
Sortie : une grille ✅ / ⚪ / ❌ par jeu ; code 1 s'il y a au moins un ❌.
Usage : python -I pipelines/contrat_core.py [--jeu basketvibe] [--fraicheur 8]
"""

import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python -I n'ajoute pas le dossier du script
from build_core import CONTRAT, branchements  # noqa: E402
from sql import url_ro  # noqa: E402

# entité -> contrôles de plage : (libellé, condition SQL qui doit être vraie pour chaque ligne)
PLAGES = {
    "player_daily": [
        ("rating 0–100", "rating is null or rating between 0 and 100"),
        ("form 0–1", "form is null or form between 0 and 1"),
        ("fatigue 0–1", "fatigue is null or fatigue between 0 and 1"),
        ("morale 0–1", "morale is null or morale between 0 and 1"),
    ],
    "fixture": [
        ("competition_kind permis", "competition_kind in ('ligue','coupe','amical','playoff','autre')"),
        ("my_result W/D/L", "my_result is null or my_result in ('W','D','L')"),
        ("résultat si joué", "not played or my_result is not null"),
        ("pas de résultat si non joué", "played or my_result is null"),
    ],
    "standing": [("rank ≥ 1", "rank >= 1"), ("points ≥ 0", "points is null or points >= 0")],
    "finance_daily": [],
    "market_listing": [
        ("rating 0–100", "rating is null or rating between 0 and 100"),
        ("prix ≥ 0", "price is null or price >= 0"),
        ("enchères ≥ 0", "bids is null or bids >= 0"),
    ],
    "academy_prospect": [
        ("rating 0–100", "rating_min is null or (rating_min between 0 and 100 and rating_max between rating_min and 100)"),
        ("potentiel 0–100", "potential_min is null or (potential_min between 0 and 100 and potential_max between potential_min and 100)"),
        ("status permis", "status is null or status in ('candidat','teste','signe','ecarte','autre')"),
    ],
    "staff": [
        ("role permis", "role in ('coach','medecin','kine','psychologue','marketing','scout','autre')"),
        ("level 0–100", "level is null or level between 0 and 100"),
        ("salaire ≥ 0", "salary is null or salary >= 0"),
    ],
    "training_plan": [
        ("intensity 0–1", "intensity is null or intensity between 0 and 1"),
        ("un focus au moins", "focus_primary is not null or focus_secondary is not null"),
    ],
}
# Constats (pas des échecs) : signalés pour qu'on fasse l'export qui manque.
CONSTATS = {
    "fixture": ("matchs passés sans résultat (export manquant ?)", "not played and day < current_date"),
}


def controle(cur, jeu: str, entite: str, limites: list[str], fraicheur: int) -> list[tuple[str, str, str]]:
    vue = f"adapt.{jeu}_{entite}"
    colonnes, cle = CONTRAT[entite]
    res = []
    cur.execute("select column_name, data_type from information_schema.columns "
                "where table_schema = 'adapt' and table_name = %s order by ordinal_position", (f"{jeu}_{entite}",))
    reel = dict(cur.fetchall())
    if not reel:
        return [("❌", "vue", f"{vue} introuvable")]
    attendu = {c: t for c, t, _n in colonnes}
    fautes = [f"{c} absente" for c in attendu if c not in reel]
    fautes += [f"{c} {reel[c]} au lieu de {t}" for c, t in attendu.items() if c in reel and reel[c] != t]
    fautes += [f"{c} en trop" for c in reel if c not in attendu]
    res.append(("❌" if fautes else "✅", "colonnes et types", "; ".join(fautes)))
    if fautes:
        return res

    cur.execute(f"select count(*) from {vue}")
    n = cur.fetchone()[0]
    res.append(("❌" if n == 0 else "✅", "lignes", str(n)))
    if n == 0:
        return res

    nn = [c for c, _t, obligatoire in colonnes if obligatoire]
    cur.execute(f"select {', '.join(f'count(*) filter (where {c} is null)' for c in nn)} from {vue}")
    nuls = [f"{c} : {k}" for c, k in zip(nn, cur.fetchone()) if k]
    res.append(("❌" if nuls else "✅", "clés non nulles", "; ".join(nuls)))

    cur.execute(f"select count(*) - count(distinct ({', '.join(cle)})) from {vue}")
    dup = cur.fetchone()[0]
    res.append(("❌" if dup else "✅", f"unicité ({', '.join(cle)})", f"{dup} doublons" if dup else ""))

    for libelle, cond in PLAGES[entite]:
        cur.execute(f"select count(*) from {vue} where not ({cond})")
        k = cur.fetchone()[0]
        res.append(("❌" if k else "✅", libelle, f"{k} lignes hors plage" if k else ""))

    facultatives = [c for c, _t, obligatoire in colonnes if not obligatoire]
    cur.execute(f"select {', '.join(f'count({c})' for c in facultatives)} from {vue}")
    vides = {c for c, k in zip(facultatives, cur.fetchone()) if k == 0}
    non_declarees = sorted(vides - set(limites))
    declarees_pleines = sorted(set(limites) - vides)
    if non_declarees:
        res.append(("❌", "colonnes vides non déclarées", ", ".join(non_declarees)))
    if declarees_pleines:
        res.append(("❌", "limites déclarées mais remplies", ", ".join(declarees_pleines)))
    if limites and not declarees_pleines:
        res.append(("⚪", "non fourni (déclaré)", ", ".join(limites)))

    cur.execute(f"select max(day) from {vue} where day <= current_date")
    dernier = cur.fetchone()[0]
    age = (dt.date.today() - dernier).days if dernier else None
    res.append(("❌" if age is None or age > fraicheur else "✅", "fraîcheur",
                f"dernier jour {dernier} ({age} j)" if dernier else "aucun jour passé"))

    if entite in CONSTATS:
        libelle, cond = CONSTATS[entite]
        cur.execute(f"select count(*), string_agg(distinct day::text, ', ') from {vue} where {cond}")
        k, jours = cur.fetchone()
        if k:
            res.append(("⚪", libelle, f"{k} : {jours}"))
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jeu")
    ap.add_argument("--fraicheur", type=int, default=8, help="jours au-delà desquels une entité est périmée")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    import psycopg

    jeux = branchements()
    if a.jeu:
        jeux = {a.jeu: jeux.get(a.jeu, {})}
    echec, nb_ko = False, 0
    with psycopg.connect(url_ro(), connect_timeout=15) as c, c.cursor() as cur:
        for jeu, entites in jeux.items():
            print(f"\n## {jeu}")
            if not entites:
                print("❌ aucune entité core déclarée")
                echec = True
                continue
            print("| entité | | contrôle | détail |\n|---|---|---|---|")
            for entite in CONTRAT:
                if entite not in entites:
                    print(f"| {entite} | ⚪ | non branchée | |")
                    continue
                for marque, nom, detail in controle(cur, jeu, entite, entites[entite], a.fraicheur):
                    echec |= marque == "❌"
                    nb_ko += marque == "❌"
                    print(f"| {entite} | {marque} | {nom} | {detail} |")
    print(f"\n{'❌' if echec else '✅'} contrat core : {', '.join(jeux)} ; {nb_ko} contrôle(s) en échec")
    return 1 if echec else 0


if __name__ == "__main__":
    sys.exit(main())
