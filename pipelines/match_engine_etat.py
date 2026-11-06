"""Registre du Match Engine de Hockey Nation : où en est chaque règle (L-xxx) et chaque variable de la carte composition.

Lecture seule, sans modèle, 4 requêtes (executer() de sql.py). Critères écrits avant calcul :
docs/refonte-v3/journal-matchengine.md. Une règle qui demande les joueurs sur la glace par tir ou par unité est écrite
« non mesurable : il manque X », sans chiffre. Les matchs FRM / U21 / U17 sont comptés à part, marqués
« expérience sans notre choix ».

Lecture de « pour » et « contre » : nombre de matchs (ou de joueurs) dont la mesure va dans le sens de la règle / à son encontre.
Confiance : faible si n < n requis / 2, moyenne si n < n requis, solide ensuite. « confirmé » / « infirmé » seulement en solide.

Usage : python -I pipelines/match_engine_etat.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python -I n'ajoute pas le dossier du script
import sql as sqlmod  # noqa: E402

DEBUT_S27 = "2026-10-31"
SEUIL_P3 = 0.880
SEUIL_GARDIEN_D = 0.870

# Colonnes du match : côté « nous » (cote) et côté adverse (autre), tout calculé en SQL.
Q_MATCHS = f"""
with m as (select g.game_id, g.team_level, g.game_type, g.scheduled_at::date as jour, g.my_result,
 case when g.home_is_mine then 'home' else 'away' end as cote, case when g.home_is_mine then 'away' else 'home' end as autre,
 case when g.home_is_mine then g.home_score else g.away_score end as bn, case when g.home_is_mine then g.away_score else g.home_score end as bo,
 d.teams, d.periods, d.summary, d.boxscore, d.players from silver.hn_games g join silver.hn_game_detail d using (game_id)
 where g.home_is_mine or g.away_is_mine)
select game_id, team_level, game_type, jour, my_result, bn, bo,
 (teams->cote->'stats'->>'shots')::int as tn, (teams->autre->'stats'->>'shots')::int as te,
 (teams->cote->'stats'->>'xGoalsFor')::float as xn, (teams->autre->'stats'->>'xGoalsFor')::float as xe,
 (teams->cote->'stats'->>'giveaways')::int as gvn, (teams->cote->'stats'->>'ppAttempts')::int as ppn, (teams->autre->'stats'->>'ppAttempts')::int as ppe,
 (select count(*) from jsonb_array_elements(summary->'scoring') s where s->>'strength'='PP' and s->>'teamId'=teams->cote->>'id') as ppgn,
 (select count(*) from jsonb_array_elements(summary->'scoring') s where s->>'strength'='PP' and s->>'teamId'=teams->autre->>'id') as ppge,
 (select count(*) from jsonb_array_elements(summary->'scoring') s where s->>'strength'='SH' and s->>'teamId'=teams->autre->>'id') as shge,
 (select coalesce(sum((b.value->>'faceoffsWon')::int),0) from jsonb_each(boxscore) b where b.key in (select p->>'id' from jsonb_array_elements(players->cote) p)) as fow,
 (select coalesce(sum((b.value->>'faceoffsLost')::int),0) from jsonb_each(boxscore) b where b.key in (select p->>'id' from jsonb_array_elements(players->cote) p)) as fol,
 (select coalesce(sum((e->autre->>'shots')::int),0) from jsonb_array_elements(periods) e where (e->>'period')::int<=2) as s12,
 (select coalesce(sum((e->autre->>'goals')::int),0) from jsonb_array_elements(periods) e where (e->>'period')::int<=2) as g12,
 (select coalesce(sum((e->autre->>'shots')::int),0) from jsonb_array_elements(periods) e where (e->>'period')::int=3) as s3,
 (select coalesce(sum((e->autre->>'goals')::int),0) from jsonb_array_elements(periods) e where (e->>'period')::int=3) as g3,
 (select p->>'lastname' from jsonb_array_elements(players->cote) p where p->>'captain'='true' limit 1) as capitaine
from m order by jour, game_id"""

Q_GARDIENS = """
select g.game_id, p->>'lastname' as nom, (b.value->>'toi')::int as toi, (b.value->>'saves')::int as arrets,
 (b.value->>'shotsFaced')::int as tirs, (b.value->>'goalsAgainst')::int as buts
from silver.hn_games g join silver.hn_game_detail d using (game_id), jsonb_each(d.boxscore) b,
 jsonb_array_elements(d.players->(case when g.home_is_mine then 'home' else 'away' end)) p
where (g.home_is_mine or g.away_is_mine) and b.value ? 'saves' and p->>'id'=b.key"""

Q_JOUEURS = """
select p->>'lastname' as nom, g.my_result as res, count(*) as n, sum((b.value->>'goals')::int) as buts, sum((b.value->>'shots')::int) as tirs,
 sum((b.value->>'diff')::int) as diff, sum((b.value->>'pim')::int) as pim
from silver.hn_games g join silver.hn_game_detail d using (game_id), jsonb_each(d.boxscore) b,
 jsonb_array_elements(d.players->(case when g.home_is_mine then 'home' else 'away' end)) p
where g.team_level='PRO' and (g.home_is_mine or g.away_is_mine) and p->>'id'=b.key and not b.value ? 'saves'
group by 1, 2"""

Q_DSC = "select distinct on (name) name, dsc from silver.hn_players where team_level='PRO' and dsc is not null order by name, as_of desc"

NON_MESURABLE = [
    ("V1 lineup saisie 1 h avant (−30 %)", "l'heure de saisie par match"),
    ("V2 joueur hors poste (−20 %)", "un match joué avec un joueur hors poste et un témoin"),
    ("V3 endurance par unité : effet sur les buts", "les joueurs sur la glace par but (temps de glace et fatigue par ligne : lecture à part, lineup × boxscore)"),
    ("V6 power play : effet de la composition d'une unité", "les joueurs sur la glace par tir"),
    ("V7 infériorité : effet de la composition d'une unité", "les joueurs sur la glace par tir"),
    ("V9 plan de jeu short : buts encaissés par L1", "les joueurs sur la glace par but (plus/moins net seulement)"),
    ("V11 case vide ou joueur parti (−5 %)", "des matchs joués avec case vide"),
    ("V12 test en amical", "des amicaux avec un seul réglage changé (2 amicaux en base)"),
    ("V13 FRM/U21/U17 : poste principal", "les lignes réellement alignées FRM/U21/U17"),
    ("V14 avis des amis", "une donnée de match (avis seulement)"),
    ("L-001 sans filet vide", "le marqueur « filet vide » (taux brut utilisé)"),
    ("L-004 meilleur FOF des 5 sur la glace", "la présence sur la glace par mise au jeu"),
    ("L-006 effet du PK sur le résultat", "les joueurs sur la glace par unité"),
    ("L-008 effet de la discipline sur les résultats", "l'effet isolé d'un joueur sur la glace"),
    ("L-010 effet du contre-emploi", "le même joueur à son poste naturel"),
    ("L-005 sortie sur écart ≥ 3 buts", "le score à l'instant de sortie dans ce script (lisible dans summary.scoring)"),
]


def confiance(n, requis):
    return "faible" if n < requis / 2 else "moyenne" if n < requis else "solide"


def verdict(pour, contre, conf, sens="pour"):
    """sens : ce que « pour » veut dire pour la règle. Un verdict ferme demande une confiance solide."""
    if pour + contre == 0:
        return "aucun match"
    if pour == contre:
        return "indécis"
    gagne = pour > contre
    if conf == "solide":
        return "confirmé" if gagne else "infirmé"
    return "à surveiller (penche pour)" if gagne else "à surveiller (penche contre)"


def pct(a, b):
    return f"{100 * a / b:.1f} %" if b else "—"


def ligne(regle, n, pour, contre, requis, mesure, equipe="PRO"):
    conf = confiance(n, requis)
    return {"regle": regle, "equipe": equipe, "n": n, "pour": pour, "contre": contre, "requis": requis,
            "confiance": conf, "verdict": verdict(pour, contre, conf), "mesure": mesure}


def evaluer(ms, gardiens, joueurs, dsc, equipe="PRO", complet=True):
    """ms : matchs (dict) d'une équipe ; gardiens / joueurs / dsc : lecture PRO seulement (complet=True)."""
    ligue = [m for m in ms if m["game_type"] == "League"]
    defaites = [m for m in ligue if m["my_result"] == "L"]
    victoires = [m for m in ligue if m["my_result"] == "W"]
    s27 = [m for m in ligue if str(m["jour"]) >= DEBUT_S27]
    out = []
    # L-001 réalisation
    pour = sum(1 for m in defaites if m["tn"] and m["te"] and m["bn"] / m["tn"] < m["bo"] / m["te"])
    out.append(ligne("L-001 réalisation, pas volume", len(defaites), pour, len(defaites) - pour, 10,
                     f"D : nous {pct(sum(m['bn'] for m in defaites), sum(m['tn'] for m in defaites))}, eux {pct(sum(m['bo'] for m in defaites), sum(m['te'] for m in defaites))} ; "
                     f"V : nous {pct(sum(m['bn'] for m in victoires), sum(m['tn'] for m in victoires))}, eux {pct(sum(m['bo'] for m in victoires), sum(m['te'] for m in victoires))}", equipe))
    # L-004 mises au jeu (pour = on gagne les mises au jeu et on perd quand même : aucun lien)
    avec = [m for m in defaites if m["fow"] + m["fol"]]
    pour = sum(1 for m in avec if m["fow"] >= m["fol"])
    out.append(ligne("L-004 mises au jeu sans lien avec le résultat", len(avec), pour, len(avec) - pour, 10,
                     f"D {pct(sum(m['fow'] for m in defaites), sum(m['fow'] + m['fol'] for m in defaites))} ; V {pct(sum(m['fow'] for m in victoires), sum(m['fow'] + m['fol'] for m in victoires))}", equipe))
    # L-006 PK / L-019 PP : un match sans ppAttempts (clé absente) est écarté, jamais compté comme 0
    lu = lambda g: [m for m in g if m["ppn"] is not None and m["ppe"] is not None]  # noqa: E731
    ecartes = len([m for m in ligue if m not in lu(ligue)])
    pk = lambda g: pct(sum(m["ppe"] - m["ppge"] for m in g), sum(m["ppe"] for m in g))  # noqa: E731
    dp, vp, sp = lu(defaites), lu(victoires), lu(s27)
    pour = sum(1 for m in dp if m["ppge"] > 0)
    out.append(ligne("L-006 PK plus bas en défaite", len(dp), pour, len(dp) - pour, 10,
                     f"PK D {pk(dp)} ({sum(m['ppe'] for m in dp)} sup. adverses) ; PK V {pk(vp)} ; {ecartes} match(s) écarté(s), ppAttempts absent", equipe))
    att, buts = sum(m["ppn"] for m in sp), sum(m["ppgn"] for m in sp)
    out.append(ligne("L-019 PP S27 au moins 23 %", att, 1 if att and buts / att >= 0.23 else 0, 1 if att and buts / att < 0.23 else 0, 20,
                     f"PP S27 {pct(sum(m['ppgn'] for m in sp), sum(m['ppn'] for m in sp))} ; buts SH encaissés S27 {sum(m['shge'] for m in s27)} ; PP ligue toute base {pct(sum(m['ppgn'] for m in lu(ligue)), sum(m['ppn'] for m in lu(ligue)))}", equipe))
    # L-015 / L-017 xG
    xd = [m for m in defaites if m["xn"] > m["xe"]]
    pour = sum(1 for m in xd if m["tn"] and m["te"] and m["bn"] / m["tn"] < m["bo"] / m["te"])
    out.append(ligne("L-015 xG pour nous, réussite contre nous (défaites)", len(xd), pour, len(xd) - pour, 10,
                     f"{len(xd)} défaites sur {len(defaites)} avec xG nous > eux", equipe))
    xs = [m for m in s27 if m["xn"] > m["xe"]]
    pour = sum(1 for m in xs if m["my_result"] == "L")
    out.append(ligne("L-017 S27 : xG positif et résultat négatif", len(xs), pour, len(xs) - pour, 10,
                     f"S27 ligue {len(s27)} matchs, {sum(1 for m in s27 if m['my_result'] == 'W')} V ; pertes de palet {sum(m['gvn'] for m in s27)}", equipe))
    # L-016 / L-018 P3 du gardien (matchs où un seul gardien a joué 3600 s)
    complets = {}
    for g in gardiens:
        if g["toi"] == 3600:
            complets[g["game_id"]] = g
    for nom, regle, filtre in (("Kovalev", "L-016 Kovalev recule en P3 de 2 points (toutes saisons)", lambda m: True),
                               ("Kovalev", "L-018 Kovalev P3 en S27", lambda m: str(m["jour"]) >= DEBUT_S27)):
        sel = [m for m in ms if m["game_id"] in complets and complets[m["game_id"]]["nom"] == nom and filtre(m)]
        if regle.startswith("L-016"):
            pour = sum(1 for m in sel if m["s3"] and m["s12"] and 1 - m["g3"] / m["s3"] < 1 - m["g12"] / m["s12"] - 0.02)
            mesure = f"P3 {pct(sum(m['s3'] - m['g3'] for m in sel), sum(m['s3'] for m in sel))} ; P1-P2 {pct(sum(m['s12'] - m['g12'] for m in sel), sum(m['s12'] for m in sel))} (filet vide compris)"
        else:
            pour = sum(1 for m in sel if m["s3"] and 1 - m["g3"] / m["s3"] < SEUIL_P3)
            mesure = f"P3 {pct(sum(m['s3'] - m['g3'] for m in sel), sum(m['s3'] for m in sel))} (seuil {SEUIL_P3:.3f})"
        out.append(ligne(regle, len(sel), pour, len(sel) - pour, 10, mesure, equipe))
    # L-002 gardien sous .870 en défaite
    titulaire = {}
    for g in gardiens:
        if g["tirs"] is not None and g["tirs"] > titulaire.get(g["game_id"], {"tirs": -1})["tirs"]:
            titulaire[g["game_id"]] = g
    sel = [(m, titulaire[m["game_id"]]) for m in defaites if m["game_id"] in titulaire and titulaire[m["game_id"]]["tirs"]]
    pour = sum(1 for _, g in sel if g["arrets"] / g["tirs"] < SEUIL_GARDIEN_D)
    vic = [titulaire[m["game_id"]] for m in victoires if m["game_id"] in titulaire and titulaire[m["game_id"]]["tirs"]]
    out.append(ligne("L-002 gardien sous .870 en défaite", len(sel), pour, len(sel) - pour, 10,
                     f"D {pct(sum(g['arrets'] for _, g in sel), sum(g['tirs'] for _, g in sel))} ; V {pct(sum(g['arrets'] for g in vic), sum(g['tirs'] for g in vic))}", equipe))
    # L-003 rang de départ d'affilée
    rangs, prec, rang = [], None, 0
    for m in ligue:
        g = titulaire.get(m["game_id"])
        if not g:
            continue
        rang = rang + 1 if g["nom"] == prec else 1
        prec = g["nom"]
        rangs.append((rang, g))
    r1 = [g for r, g in rangs if r == 1 and g["tirs"]]
    moy1 = sum(g["arrets"] for g in r1) / sum(g["tirs"] for g in r1) if r1 else None
    hauts = [g for r, g in rangs if r >= 3 and g["tirs"]]
    pour = sum(1 for g in hauts if moy1 is not None and g["arrets"] / g["tirs"] < moy1)
    out.append(ligne("L-003 fatigue : départs d'affilée (3e et plus)", len(hauts), pour, len(hauts) - pour, 20,
                     f"1er départ {pct(sum(g['arrets'] for g in r1), sum(g['tirs'] for g in r1))} ; 3e et plus {pct(sum(g['arrets'] for g in hauts), sum(g['tirs'] for g in hauts))}", equipe))
    # L-005 sorties du gardien : conforme si arrêts < 60 % (l'autre branche n'est pas lue ici)
    sorties = [g for g in titulaire.values() if g["toi"] < 3600 and g["tirs"]]
    pour = sum(1 for g in sorties if g["arrets"] / g["tirs"] < 0.60)
    out.append(ligne("L-005 sortie du gardien sous 60 % d'arrêts", len(sorties), pour, len(sorties) - pour, 10,
                     "branche « écart ≥ 3 buts » non lue ici", equipe))
    out[-1]["verdict"] = "partiel : une branche non lue"
    if not complet:
        return out
    # Règles par joueur (PRO)
    # L-007 joueur muet : réalisation en défaite contre victoire, joueurs à 30 tirs au moins
    par = {}
    for j in joueurs:
        d = par.setdefault(j["nom"], {"L": [0, 0], "W": [0, 0], "diff": 0, "n": 0, "pim": 0})
        if j["res"] in ("L", "W"):
            d[j["res"]][0] += j["buts"]
            d[j["res"]][1] += j["tirs"]
        d["diff"] += j["diff"]
        d["pim"] += j["pim"]
        d["n"] += j["n"]
    cibles = [(n, d) for n, d in par.items() if d["L"][1] + d["W"][1] >= 30 and d["L"][1] and d["W"][1]]
    pour = sum(1 for _, d in cibles if d["L"][0] / d["L"][1] < d["W"][0] / d["W"][1])
    out.append(ligne("L-007 joueurs muets en défaite (30 tirs et plus)", len(defaites), pour, len(cibles) - pour, 10,
                     f"{len(cibles)} joueurs ; pour = taux de réussite plus bas en D qu'en V"))
    # L-008 discipline
    def dsc_de(nom):
        v = {d for n, d in dsc.items() if n.endswith(" " + nom)}
        return v.pop() if len(v) == 1 else None
    bas = [d for n, d in par.items() if (dsc_de(n) or 99) <= 4 and d["n"]]
    haut = [d for n, d in par.items() if (dsc_de(n) or -1) >= 7 and d["n"]]
    pm = lambda g: sum(d["pim"] for d in g) / max(1, sum(d["n"] for d in g))  # noqa: E731
    out.append(ligne("L-008 DSC bas, plus de PIM", len(ms), 1 if bas and haut and pm(bas) > pm(haut) else 0, 1 if bas and haut and pm(bas) <= pm(haut) else 0, 20,
                     f"PIM/match DSC ≤ 4 : {pm(bas):.2f} ({len(bas)} joueurs) ; DSC ≥ 7 : {pm(haut):.2f} ({len(haut)} joueurs)"))
    # L-009 capitaine
    caps = {}
    for m in ligue:
        if m["capitaine"]:
            c = caps.setdefault(m["capitaine"], [0, 0])
            c[0] += m["my_result"] == "W"
            c[1] += 1
    ecart = (max(c[0] / c[1] for c in caps.values()) - min(c[0] / c[1] for c in caps.values())) if len(caps) > 1 else 0
    out.append(ligne("L-009 capitaine sans effet", min([c[1] for c in caps.values()] or [0]), 1 if ecart < 0.20 else 0, 1 if ecart >= 0.20 else 0, 10,
                     " ; ".join(f"{k} {c[0]}/{c[1]}" for k, c in sorted(caps.items(), key=lambda x: -x[1][1]))))
    # L-010 contre-emploi : plus/moins par match
    noms = [n for n in ("Conte", "Blednov", "Flink", "Sutherland", "Eskelinen") if n in par]
    pour = sum(1 for n in noms if par[n]["diff"] >= 0)
    out.append(ligne("L-010 contre-emploi : plus/moins non négatif", len(ms), pour, len(noms) - pour, 10,
                     " ; ".join(f"{n} {par[n]['diff']:+d}/{par[n]['n']} m" for n in noms)))
    # L-011 série d'Ottawa : descriptif
    po = [m for m in ms if m["game_type"] == "Playoffs"]
    out.append({"regle": "L-011 série perdue 0-3 (descriptif)", "equipe": "PRO", "n": len(po), "pour": "—", "contre": "—", "requis": "—",
                "confiance": "faible", "verdict": "descriptif, jamais de verdict",
                "mesure": f"tirs {sum(m['tn'] for m in po)}-{sum(m['te'] for m in po)} ; PP {sum(m['ppgn'] for m in po)}/{sum(m['ppn'] for m in po)} ; PP adverse {sum(m['ppge'] for m in po)}/{sum(m['ppe'] for m in po)}"})
    return out


def lire():
    cols, lignes = sqlmod.executer(Q_MATCHS)
    ms = [dict(zip(cols, l)) for l in lignes]
    cols, lignes = sqlmod.executer(Q_GARDIENS)
    gardiens = [dict(zip(cols, l)) for l in lignes]
    cols, lignes = sqlmod.executer(Q_JOUEURS)
    joueurs = [dict(zip(cols, l)) for l in lignes]
    cols, lignes = sqlmod.executer(Q_DSC)
    dsc = {l[0]: l[1] for l in lignes}
    return ms, gardiens, joueurs, dsc


def rapport(ms, gardiens, joueurs, dsc):
    pro = [m for m in ms if m["team_level"] == "PRO"]
    out = evaluer(pro, [g for g in gardiens if g["game_id"] in {m["game_id"] for m in pro}], joueurs, dsc)
    autres = [m for m in ms if m["team_level"] != "PRO"]
    ids = {m["game_id"] for m in autres}
    for l in evaluer(autres, [g for g in gardiens if g["game_id"] in ids], [], {}, complet=False):
        l["equipe"] = "FRM+U21+U17 (expérience sans notre choix)"
        if l["n"]:
            out.append(l)
    cols = ["regle", "equipe", "n", "pour", "contre", "requis", "confiance", "verdict", "mesure"]
    en_tete = ["règle", "équipe", "n matchs", "pour", "contre", "n requis", "confiance", "verdict", "mesure"]
    txt = ["| " + " | ".join(en_tete) + " |", "|" + "---|" * len(cols)]
    txt += ["| " + " | ".join(str(l[c]).replace("|", "/") for c in cols) + " |" for l in out]
    for regle, manque in NON_MESURABLE:
        txt.append(f"| {regle} | — | — | — | — | — | — | non mesurable : il manque {manque} | — |")
    return "\n".join(txt)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    print(rapport(*lire()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
