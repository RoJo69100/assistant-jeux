"""Registre du Match Engine de Hockey Nation : où en est chaque règle (L-xxx) et chaque variable de la carte composition.

Lecture seule, sans modèle, 6 requêtes (executer() de sql.py). Critères écrits avant calcul :
docs/refonte-v3/journal-matchengine.md (C1 à C5). Verdict d'un taux : intervalle de Wilson à 95 % entièrement du bon côté du
seuil (SEUILS) ou séparé de l'autre taux, sinon « indéterminé : n trop petit ». Une règle marquée ⛔ / retirée n'est pas affichée. Une règle qui demande les joueurs sur la glace par tir ou par unité est écrite
« non mesurable : il manque X », sans chiffre. Les matchs FRM / U21 / U17 sont comptés à part, marqués
« expérience sans notre choix ».

Lecture de « pour » et « contre » : nombre de matchs (ou de joueurs) dont la mesure va dans le sens de la règle / à son encontre.
Confiance : faible si n < n requis / 2, moyenne si n < n requis, solide ensuite. Hors taux (PIM, plus/moins, séries), « confirmé » / « infirmé » seulement en solide.

Usage : python -I pipelines/match_engine_etat.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python -I n'ajoute pas le dossier du script
import sql as sqlmod  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent
FICHIERS_REGLES = (RACINE / "outputs/hockeynation/learnings.md", RACINE / "docs/decisions/cartes/hockeynation/composition.md")

DEBUT_S27 = "2026-10-31"  # première journée de la saison en cours (premier match de ligue le 2026-11-01)
# Seuils des verdicts de taux : une seule valeur par seuil, écrite ici avec sa source. Le skill et le journal
# (docs/refonte-v3/journal-matchengine.md, C2) renvoient à ce dictionnaire sans recopier les chiffres.
SEUILS = {
    "pp": (0.207, "L-006, outputs/hockeynation/learnings.md : PP de la saison précédente, 29 buts sur 140 supériorités (mesure). "
                  "Le 23 % des conseils C-014, C-027, C-050 est un objectif posé sans mesure, pas un seuil du registre."),
    "gardien_defaite": (0.870, "L-002, outputs/hockeynation/learnings.md : gardien sous .870 dans 8 des 12 défaites de la saison précédente."),
    "p3": (0.880, "C-060, outputs/hockeynation/learnings.md : arrêts de Kovalev en P3 ≥ .880."),
}
SEUIL_PP = SEUILS["pp"][0]
SEUIL_P3 = SEUILS["p3"][0]
SEUIL_GARDIEN_D = SEUILS["gardien_defaite"][0]

# Nos équipes (id du jeu → libellé), clubs et équipes hors club (nation, tournoi) ; même liste que le bloc `equipes` de
# docs/attentes/jeux/hockeynation.yaml (test_match_engine_etat le vérifie).
EQUIPES_ID = {
    "50cf5f9e-4fb2-4469-9f57-e291fe5ce3cd": "PRO", "9c3df9ae-5e1b-4b3b-a9d3-3b593b5c18e9": "FRM",
    "e44a02bc-bc7a-42de-b853-2271d74a00bd": "U21", "02b15998-21ca-4b55-94d2-64d65037c83a": "U17",
    "b19873de-482d-431f-9cb8-f62aa7a16572": "ISL", "e403da50-d117-4276-8554-2130789f460d": "ISL21",
    "18f5fa55-a9ae-4ece-ba1c-a2866ff8d280": "HUA",
}
_VALEURS = ", ".join(f"('{i}', '{e}')" for i, e in EQUIPES_ID.items())

# Colonnes du match : côté « nous » (cote) et côté adverse (autre), tout calculé en SQL.
_SELECT = """
select game_id, team_level, game_type, jour, my_result, bn, bo,"""
Q_MATCHS_M = """
with m as (select g.game_id, g.team_level, g.game_type, g.scheduled_at::date as jour, g.my_result,
 case when g.home_is_mine then 'home' else 'away' end as cote, case when g.home_is_mine then 'away' else 'home' end as autre,
 case when g.home_is_mine then g.home_score else g.away_score end as bn, case when g.home_is_mine then g.away_score else g.home_score end as bo,
 d.teams, d.periods, d.summary, d.boxscore, d.players from silver.hn_games g join silver.hn_game_detail d using (game_id)
 where g.home_is_mine or g.away_is_mine)"""
# 25/11 (consigne de l'utilisateur) : registre sur TOUS les matchs en base, toutes équipes, toutes saisons, autres clubs inclus.
# Chaque match donne deux observations (domicile et extérieur) ; game_id = « uuid/cote » ; résultat = score final (result).
Q_TOUS_M = f"""
with c(id, eq) as (values {_VALEURS}),
m as (select d.game_id::text || '/' || x.cote as game_id, coalesce(c.eq, 'autres clubs') as team_level,
 coalesce(g.game_type, case when d.teams->x.cote->>'level' in ('WORLD', 'NTU21') then 'WC' when d.teams->x.cote->>'level' = 'TOUR' then 'Tournament' else 'Inconnu' end) as game_type,
 d.scheduled_at::date as jour, x.cote, x.autre,
 (d.result->>(x.cote || 'Score'))::int as bn, (d.result->>(x.autre || 'Score'))::int as bo,
 case when (d.result->>(x.cote || 'Score'))::int > (d.result->>(x.autre || 'Score'))::int then 'W' else 'L' end as my_result,
 d.teams, d.periods, d.summary, d.boxscore, d.players
 from silver.hn_game_detail d left join silver.hn_games g using (game_id)
 cross join (values ('home', 'away'), ('away', 'home')) x(cote, autre)
 left join c on c.id = d.teams->x.cote->>'id'
 where d.result ? 'homeScore')"""
_COLONNES = """
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
Q_MATCHS = Q_MATCHS_M + _SELECT + _COLONNES
Q_TOUS = Q_TOUS_M + _SELECT + _COLONNES

Q_GARDIENS = """
select g.game_id, p->>'lastname' as nom, (b.value->>'toi')::int as toi, (b.value->>'saves')::int as arrets,
 (b.value->>'shotsFaced')::int as tirs, (b.value->>'goalsAgainst')::int as buts
from silver.hn_games g join silver.hn_game_detail d using (game_id), jsonb_each(d.boxscore) b,
 jsonb_array_elements(d.players->(case when g.home_is_mine then 'home' else 'away' end)) p
where (g.home_is_mine or g.away_is_mine) and b.value ? 'saves' and p->>'id'=b.key"""

# Gardiens des deux côtés de tous les matchs (même clé « uuid/cote » que Q_TOUS).
Q_GARDIENS_TOUS = """
select d.game_id::text || '/' || x.cote as game_id, p->>'lastname' as nom, (b.value->>'toi')::int as toi, (b.value->>'saves')::int as arrets,
 (b.value->>'shotsFaced')::int as tirs, (b.value->>'goalsAgainst')::int as buts
from silver.hn_game_detail d cross join (values ('home'), ('away')) x(cote), jsonb_each(d.boxscore) b,
 jsonb_array_elements(d.players->x.cote) p
where b.value ? 'saves' and p->>'id'=b.key"""

# Test « shift length court » : réglage de la lineup A à chaque export de lineups PRO (seule source : aucun réglage dans les pages
# de match). Un match n'est compté que s'il est encadré par deux exports qui donnent la même valeur (réglage fixé, prouvé).
Q_SHIFT = """
select captured_at, (body->0->'gameplan'->>'shiftLength')::int as shift from silver.hn_api
where route = '/team/:id/lineups' and endpoint like '%/50cf5f9e-4fb2-4469-9f57-e291fe5ce3cd/%' and body->0->>'id' = 'A'
 and body->0->'gameplan' ? 'shiftLength' order by captured_at"""
Q_PRO_MATCHS = """
select g.game_id::text as game_id, g.scheduled_at, g.game_type, g.my_result,
 case when g.home_is_mine then g.away_score else g.home_score end as bo,
 (d.teams->(case when g.home_is_mine then 'away' else 'home' end)->'stats'->>'shots')::int as te,
 (d.teams->(case when g.home_is_mine then 'away' else 'home' end)->'stats'->>'xGoalsFor')::float as xe
from silver.hn_games g join silver.hn_game_detail d using (game_id) where g.team_level = 'PRO' and g.my_result is not null"""
SHIFT_LIBELLE = {0: "court", 1: "normal", 2: "long"}  # 0 = court : lu le 2026-10-31 après la décision du 2026-10-29 (resume.md)

Q_JOUEURS = """
select p->>'lastname' as nom, g.my_result as res, count(*) as n, sum((b.value->>'goals')::int) as buts, sum((b.value->>'shots')::int) as tirs,
 sum((b.value->>'diff')::int) as diff, sum((b.value->>'pim')::int) as pim
from silver.hn_games g join silver.hn_game_detail d using (game_id), jsonb_each(d.boxscore) b,
 jsonb_array_elements(d.players->(case when g.home_is_mine then 'home' else 'away' end)) p
where g.team_level='PRO' and (g.home_is_mine or g.away_is_mine) and p->>'id'=b.key and not b.value ? 'saves'
group by 1, 2"""

# Temps de glace par ligne : lineup A, dernière saisie au plus tard le jour du match (pas d'heure de saisie en base).
Q_GLACE = """
with l as materialized (select day, player_id::text as pid, line from silver.hn_lineups where lineup='A' and line in ('L1','L2','L3','L4')),
j as materialized (select g.game_id, g.scheduled_at::date as jour, (select max(x.day) from l x where x.day<=g.scheduled_at::date) as dl
 from silver.hn_games g where g.team_level='PRO' and (g.home_is_mine or g.away_is_mine))
select j.game_id, j.jour, l.line, sum((b.value->>'toi')::int) as toi, count(*) as joueurs
from j join silver.hn_game_detail d using (game_id) cross join jsonb_each(d.boxscore) b join l on l.day=j.dl and l.pid=b.key
group by 1,2,3 order by 2,1,3"""  # 25/11 : lineups lues une fois (la sous-requête corrélée dépassait le délai SQL)

Q_JOURS = "select count(distinct day) as jours, min(day) as premier, max(day) as dernier from silver.hn_lineups"

Q_DSC ="select distinct on (name) name, dsc from silver.hn_players where team_level='PRO' and dsc is not null order by name, as_of desc"

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


def wilson(k, n, z=1.96):
    """Intervalle de Wilson à 95 % d'une proportion k / n ; None si n = 0."""
    if not n:
        return None
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    demi = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return max(0.0, centre - demi), min(1.0, centre + demi)


def ic(k, n):
    w = wilson(k, n)
    return f"IC95 {100 * w[0]:.1f}–{100 * w[1]:.1f} %" if w else "IC95 —"


def v_seuil(k, n, seuil, sens):
    """Taux k / n contre un seuil fixe. sens « sous » : la règle dit taux < seuil ; « au-dessus » : taux ≥ seuil.
    Ferme seulement si l'intervalle de Wilson est entièrement d'un côté du seuil."""
    w = wilson(k, n)
    if not w:
        return "aucun match"
    pour, contre = (w[1] < seuil, w[0] >= seuil) if sens == "sous" else (w[0] >= seuil, w[1] < seuil)
    return "confirmé" if pour else "infirmé" if contre else f"indéterminé : n trop petit ({ic(k, n)})"


def v_ecart(a, b, sens="a_sous_b"):
    """Deux taux (k, n) comparés. « a_sous_b » : la règle dit que a est plus bas que b ; « sans_ecart » : la règle dit
    qu'il n'y a pas d'écart (un chevauchement ne le prouve pas : seul un écart net la contredit)."""
    wa, wb = wilson(*a), wilson(*b)
    if not wa or not wb:
        return "indéterminé : un des deux groupes est vide"
    sous, dessus = wa[1] < wb[0], wa[0] > wb[1]
    if sens == "a_sous_b" and sous:
        return "confirmé"
    if (sens == "a_sous_b" and dessus) or (sens == "sans_ecart" and (sous or dessus)):
        return "infirmé"
    return f"indéterminé : n trop petit ({ic(*a)} contre {ic(*b)})"


def ligne(regle, n, pour, contre, requis, mesure, equipe="PRO", v=None):
    """v : verdict déjà calculé (règles de taux, intervalle de Wilson) ; sinon verdict par nombre de matchs."""
    conf = confiance(n, requis)
    return {"regle": regle, "equipe": equipe, "n": n, "pour": pour, "contre": contre, "requis": requis,
            "confiance": conf, "verdict": v or verdict(pour, contre, conf), "mesure": mesure}


def retirees(textes):
    """Numéros L-nnn des règles dont la ligne de tableau porte ⛔ ou « retirée » (journal des enseignements, carte composition)."""
    ids = set()
    for texte in textes:
        for l in texte.splitlines():
            m = re.match(r"\|\s*(L-\d{3})\b", l)
            if m and ("⛔" in l or "retirée" in l):
                ids.add(m.group(1))
    return ids


def lire_retirees():
    return retirees(p.read_text(encoding="utf-8") for p in FICHIERS_REGLES if p.exists())


def evaluer(ms, gardiens, joueurs, dsc, equipe="PRO", complet=True, tous_types=False, propres=True):
    """ms : matchs (dict) d'une équipe ; gardiens / joueurs / dsc : lecture PRO seulement (complet=True).
    tous_types : tous les matchs joués (ligue, playoffs, amicaux, tournoi, nation), pas la ligue seule (25/11).
    propres=False : sans les règles propres à notre PRO (PP de la saison, S27, Kovalev)."""
    ligue = [m for m in ms if (m["my_result"] if tous_types else m["game_type"] == "League")]
    defaites = [m for m in ligue if m["my_result"] == "L"]
    victoires = [m for m in ligue if m["my_result"] == "W"]
    s27 = [m for m in ligue if str(m["jour"]) >= DEBUT_S27]
    out = []
    # L-001 réalisation
    pour = sum(1 for m in defaites if m["tn"] and m["te"] and m["bn"] / m["tn"] < m["bo"] / m["te"])
    out.append(ligne("L-001 réalisation, pas volume", len(defaites), pour, len(defaites) - pour, 10,
                     f"D : nous {pct(sum(m['bn'] for m in defaites), sum(m['tn'] for m in defaites))}, eux {pct(sum(m['bo'] for m in defaites), sum(m['te'] for m in defaites))} ; "
                     f"V : nous {pct(sum(m['bn'] for m in victoires), sum(m['tn'] for m in victoires))}, eux {pct(sum(m['bo'] for m in victoires), sum(m['te'] for m in victoires))}", equipe,
                     v=v_ecart((sum(m["bn"] for m in defaites), sum(m["tn"] for m in defaites)), (sum(m["bn"] for m in victoires), sum(m["tn"] for m in victoires)))))
    # L-004 mises au jeu (pour = on gagne les mises au jeu et on perd quand même : aucun lien)
    avec = [m for m in defaites if m["fow"] + m["fol"]]
    pour = sum(1 for m in avec if m["fow"] >= m["fol"])
    fd = (sum(m["fow"] for m in defaites), sum(m["fow"] + m["fol"] for m in defaites))
    fv = (sum(m["fow"] for m in victoires), sum(m["fow"] + m["fol"] for m in victoires))
    out.append(ligne("L-004 mises au jeu sans lien avec le résultat", len(avec), pour, len(avec) - pour, 10,
                     f"D {pct(*fd)} ; V {pct(*fv)}", equipe, v=v_ecart(fd, fv, "sans_ecart")))
    # L-006 PK / L-019 PP : un match sans ppAttempts (clé absente) est écarté, jamais compté comme 0
    lu = lambda g: [m for m in g if m["ppn"] is not None and m["ppe"] is not None]  # noqa: E731
    ecartes = len([m for m in ligue if m not in lu(ligue)])
    pk = lambda g: pct(sum(m["ppe"] - m["ppge"] for m in g), sum(m["ppe"] for m in g))  # noqa: E731
    dp, vp, sp = lu(defaites), lu(victoires), lu(s27)
    pour = sum(1 for m in dp if m["ppge"] > 0)
    kd = (sum(m["ppe"] - m["ppge"] for m in dp), sum(m["ppe"] for m in dp))  # infériorités survécues / subies
    kv = (sum(m["ppe"] - m["ppge"] for m in vp), sum(m["ppe"] for m in vp))
    out.append(ligne("L-006 PK plus bas en défaite", len(dp), pour, len(dp) - pour, 10,
                     f"PK D {pk(dp)} ({sum(m['ppe'] for m in dp)} sup. adverses) ; PK V {pk(vp)} ; {ecartes} match(s) écarté(s), ppAttempts absent", equipe,
                     v=v_ecart(kd, kv)))
    att, buts = sum(m["ppn"] for m in sp), sum(m["ppgn"] for m in sp)
    if propres:
        out.append(ligne(f"L-019 PP de la saison en cours au moins au seuil PP ({100 * SEUIL_PP:.1f} %)", att, buts, att - buts, 20,
                         f"PP {pct(buts, att)} ({ic(buts, att)}) ; buts SH encaissés {sum(m['shge'] for m in s27)} ; PP ligue toute base {pct(sum(m['ppgn'] for m in lu(ligue)), sum(m['ppn'] for m in lu(ligue)))} ; pour = buts, contre = supériorités sans but",
                         equipe, v=v_seuil(buts, att, SEUIL_PP, "au-dessus")))
    # L-015 / L-017 xG
    xd = [m for m in defaites if m["xn"] > m["xe"]]
    pour = sum(1 for m in xd if m["tn"] and m["te"] and m["bn"] / m["tn"] < m["bo"] / m["te"])
    rn = (sum(m["bn"] for m in xd), sum(m["tn"] for m in xd))
    re_ = (sum(m["bo"] for m in xd), sum(m["te"] for m in xd))
    out.append(ligne("L-015 xG pour nous, réussite contre nous (défaites)", len(xd), pour, len(xd) - pour, 10,
                     f"{len(xd)} défaites sur {len(defaites)} avec xG nous > eux ; réussite nous {pct(*rn)}, eux {pct(*re_)}", equipe, v=v_ecart(rn, re_)))
    xs = [m for m in s27 if m["xn"] > m["xe"]]
    pour = sum(1 for m in xs if m["my_result"] == "L")
    if propres:
        out.append(ligne("L-017 S27 : xG positif et résultat négatif", len(xs), pour, len(xs) - pour, 10,
                         f"S27 ligue {len(s27)} matchs, {sum(1 for m in s27 if m['my_result'] == 'W')} V ; pertes de palet {sum(m['gvn'] for m in s27)}", equipe))
    # L-016 / L-018 P3 du gardien (matchs où un seul gardien a joué 3600 s)
    complets = {}
    for g in gardiens:
        if g["toi"] == 3600:
            complets[g["game_id"]] = g
    for nom, regle, filtre in ((("Kovalev", "L-016 Kovalev recule en P3 de 2 points (toutes saisons)", lambda m: True),
                                ("Kovalev", "L-018 Kovalev P3 en S27", lambda m: str(m["jour"]) >= DEBUT_S27)) if propres else ()):
        sel = [m for m in ms if m["game_id"] in complets and complets[m["game_id"]]["nom"] == nom and filtre(m)]
        k3, n3 = sum(m["s3"] - m["g3"] for m in sel), sum(m["s3"] for m in sel)
        k12, n12 = sum(m["s12"] - m["g12"] for m in sel), sum(m["s12"] for m in sel)
        if regle.startswith("L-016"):
            pour = sum(1 for m in sel if m["s3"] and m["s12"] and 1 - m["g3"] / m["s3"] < 1 - m["g12"] / m["s12"] - 0.02)
            mesure = f"P3 {pct(k3, n3)} ({ic(k3, n3)}) ; P1-P2 {pct(k12, n12)} (filet vide compris) ; seuil = taux P1-P2 moins 2 points"
            v = v_seuil(k3, n3, k12 / n12 - 0.02, "sous") if n12 else "aucun match"
        else:
            pour = sum(1 for m in sel if m["s3"] and 1 - m["g3"] / m["s3"] < SEUIL_P3)
            mesure = f"P3 {pct(k3, n3)} ({ic(k3, n3)}) (seuil {SEUIL_P3:.3f})"
            v = v_seuil(k3, n3, SEUIL_P3, "sous")
        out.append(ligne(regle, len(sel), pour, len(sel) - pour, 10, mesure, equipe, v=v))
    # L-002 gardien sous .870 en défaite
    titulaire = {}
    for g in gardiens:
        if g["tirs"] is not None and g["tirs"] > titulaire.get(g["game_id"], {"tirs": -1})["tirs"]:
            titulaire[g["game_id"]] = g
    sel = [(m, titulaire[m["game_id"]]) for m in defaites if m["game_id"] in titulaire and titulaire[m["game_id"]]["tirs"]]
    pour = sum(1 for _, g in sel if g["arrets"] / g["tirs"] < SEUIL_GARDIEN_D)
    vic = [titulaire[m["game_id"]] for m in victoires if m["game_id"] in titulaire and titulaire[m["game_id"]]["tirs"]]
    ka, na = sum(g["arrets"] for _, g in sel), sum(g["tirs"] for _, g in sel)
    out.append(ligne("L-002 gardien sous .870 en défaite", len(sel), pour, len(sel) - pour, 10,
                     f"D {pct(ka, na)} ({ic(ka, na)}) ; V {pct(sum(g['arrets'] for g in vic), sum(g['tirs'] for g in vic))}", equipe,
                     v=v_seuil(ka, na, SEUIL_GARDIEN_D, "sous")))
    # L-003 rang de départ d'affilée
    rangs, prec, rang = [], {}, {}
    for m in ligue:  # rang compté par équipe (une suite de départs n'a de sens que dans la même équipe) ; autres clubs exclus
        g = titulaire.get(m["game_id"])
        eq = m.get("team_level") or equipe
        if not g or eq == "autres clubs":
            continue
        rang[eq] = rang.get(eq, 0) + 1 if g["nom"] == prec.get(eq) else 1
        prec[eq] = g["nom"]
        rangs.append((rang[eq], g))
    r1 = [g for r, g in rangs if r == 1 and g["tirs"]]
    moy1 = sum(g["arrets"] for g in r1) / sum(g["tirs"] for g in r1) if r1 else None
    hauts = [g for r, g in rangs if r >= 3 and g["tirs"]]
    pour = sum(1 for g in hauts if moy1 is not None and g["arrets"] / g["tirs"] < moy1)
    a3, a1 = (sum(g["arrets"] for g in hauts), sum(g["tirs"] for g in hauts)), (sum(g["arrets"] for g in r1), sum(g["tirs"] for g in r1))
    out.append(ligne("L-003 fatigue : départs d'affilée (3e et plus)", len(hauts), pour, len(hauts) - pour, 20,
                     f"1er départ {pct(*a1)} ; 3e et plus {pct(*a3)}", equipe, v=v_ecart(a3, a1)))
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
    jd = (sum(d["L"][0] for _, d in cibles), sum(d["L"][1] for _, d in cibles))
    jv = (sum(d["W"][0] for _, d in cibles), sum(d["W"][1] for _, d in cibles))
    out.append(ligne("L-007 joueurs muets en défaite (30 tirs et plus)", len(defaites), pour, len(cibles) - pour, 10,
                     f"{len(cibles)} joueurs ; pour = taux de réussite plus bas en D qu'en V ; ensemble D {pct(*jd)}, V {pct(*jv)}", v=v_ecart(jd, jv)))
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


def lire_glace():
    cols, lignes = sqlmod.executer(Q_GLACE)
    glace = [dict(zip(cols, l)) for l in lignes]
    cols, lignes = sqlmod.executer(Q_JOURS)
    return glace, dict(zip(cols, lignes[0]))


def mmss(s):
    return f"{int(s) // 60}:{int(s) % 60:02d}"


def temps_de_glace(glace, jours):
    """Tableau « temps de glace par ligne » par match PRO, ou une seule ligne si la jointure ne donne rien."""
    if not glace:
        return [f"non mesurable : il manque la lineup en vigueur à la date du match — `silver.hn_lineups` ne garde que {jours['jours']} jour(s) "
                f"({jours['premier']} au {jours['dernier']}). La jointure ne donne de toute façon ni les changements de ligne en cours de match "
                "ni le temps par unité de jeu de puissance ou d'infériorité séparée."]
    par = {}
    for g in glace:
        par.setdefault((str(g["jour"]), g["game_id"]), {})[g["line"]] = g["toi"]
    txt = ["| Jour du match | L1 (5 joueurs, paire D comprise) | L2 | L3 | L4 |", "|---|---|---|---|---|"]
    for (jour, _), lg in sorted(par.items()):
        txt.append(f"| {jour} | " + " | ".join(mmss(lg[x]) if x in lg else "—" for x in ("L1", "L2", "L3", "L4")) + " |")
    txt.append("Somme des `toi` des joueurs de la ligne dans la lineup A saisie le jour du match ou avant ; sans heure de saisie, la lineup réellement jouée n'est pas prouvée.")
    return txt


def _dt(x):
    import datetime as dt
    if isinstance(x, dt.datetime):
        return x if x.tzinfo else x.replace(tzinfo=dt.timezone.utc)
    return dt.datetime.fromisoformat(str(x).replace("Z", "+00:00").replace(" ", "T", 1))


def reglage_fixe(instant, releves):
    """Valeur du réglage à `instant` si deux relevés l'encadrent avec la même valeur (réglage fixé, prouvé) ; sinon None.
    releves : [(datetime, valeur)] triés."""
    t = _dt(instant)
    avant = [v for d, v in releves if _dt(d) <= t]
    apres = [v for d, v in releves if _dt(d) >= t]
    return avant[-1] if avant and apres and avant[-1] == apres[0] else None


def poisson_ic(k, n, z=1.96):
    """Moyenne k / n d'un compte (buts par match) et IC95 par l'approximation normale de Poisson."""
    if not n:
        return None
    m, e = k / n, z * (k ** 0.5) / n
    return m, max(0.0, m - e), m + e


def test_shift(releves, matchs, requis=10):
    """Test « shift length court » (C4 : échéance 10 matchs). Seuls les matchs PRO dont le réglage est fixé et prouvé (encadré
    par deux exports de lineups de même valeur) comptent. Mesure d'équipe (buts encaissés, arrêts) : la mesure par la L1 demande
    les joueurs sur la glace par but, absents. Verdict : arrêts « court » contre « normal » (intervalles de Wilson séparés)."""
    groupes = {}
    for m in matchs:
        v = reglage_fixe(m["scheduled_at"], releves)
        if v is not None and m["te"] is not None and m["bo"] is not None:
            groupes.setdefault(v, []).append(m)
    lignes_ = ["| shift length | matchs (fixé et prouvé) | buts encaissés / match (IC95) | tirs subis / match | xG adverse / match | arrêts (IC95) | confiance |",
               "|---|---|---|---|---|---|---|"]
    stats = {}
    for v in sorted(groupes):
        g = groupes[v]
        ga, sa, n = sum(m["bo"] for m in g), sum(m["te"] for m in g), len(g)
        xa = sum(m["xe"] or 0 for m in g)
        p = poisson_ic(ga, n)
        stats[v] = (sa - ga, sa)
        lignes_.append(f"| {SHIFT_LIBELLE.get(v, v)} | {n} | {p[0]:.2f} ({p[1]:.2f}–{p[2]:.2f}) | {sa / n:.1f} | {xa / n:.2f} | "
                       f"{pct(sa - ga, sa)} ({ic(sa - ga, sa)}) | {confiance(n, requis)} |")
    lire = lambda v: ("échoué : arrêts plus bas en court, retour à normal" if v == "confirmé" else  # noqa: E731
                      "réussi : arrêts plus hauts en court" if v == "infirmé" else v)
    if 0 in stats and 1 in stats:
        verdict_ = lire(v_ecart(stats[0], stats[1]))  # « confirmé » = court encaisse plus (arrêts plus bas) : le test a échoué
    else:
        verdict_ = "indéterminé : un des deux réglages n'a aucun match fixé et prouvé"
        # Référence indicative, hors verdict : matchs d'avant le premier export, réglage supposé égal au premier relevé.
        if releves and 0 in stats:
            premier = _dt(releves[0][0])
            ref = [m for m in matchs if _dt(m["scheduled_at"]) < premier and m["te"] is not None and m["bo"] is not None]
            if ref and releves[0][1] != 0:
                ga, sa, n = sum(m["bo"] for m in ref), sum(m["te"] for m in ref), len(ref)
                p = poisson_ic(ga, n)
                lignes_.append(f"| {SHIFT_LIBELLE.get(releves[0][1], releves[0][1])} — référence NON prouvée (avant le premier export, "
                               f"{premier.date()}) | {n} | {p[0]:.2f} ({p[1]:.2f}–{p[2]:.2f}) | {sa / n:.1f} | "
                               f"{sum(m['xe'] or 0 for m in ref) / n:.2f} | {pct(sa - ga, sa)} ({ic(sa - ga, sa)}) | {confiance(n, requis)} |")
                verdict_ += f" ; contre la référence non prouvée : {lire(v_ecart(stats[0], (sa - ga, sa)))}"
    conf = confiance(min(len(groupes.get(0, [])), len(groupes.get(1, []))), requis)
    exclus = len(matchs) - sum(len(g) for g in groupes.values())
    lignes_.append(f"Verdict : {verdict_} ; confiance {conf} ; {exclus} match(s) PRO exclus (réglage non prouvé : aucun export de lineups "
                   "avant le match ou valeur changée entre deux exports). Force de l'adversaire non corrigée.")
    return lignes_


def rapport(ms, gardiens, joueurs, dsc, retirees=frozenset(), glace=None, jours=None, tous=None, gardiens_tous=None, shift=None):
    """tous / gardiens_tous : toutes les observations (deux par match, autres clubs inclus, Q_TOUS) ; sans elles, l'ancien
    regroupement FRM+U21+U17. shift : (relevés, matchs PRO) du test « shift length court »."""
    pro = [m for m in ms if m["team_level"] == "PRO"]
    out = evaluer(pro, [g for g in gardiens if g["game_id"] in {m["game_id"] for m in pro}], joueurs, dsc, tous_types=tous is not None)
    if tous is not None:
        matchs = len({m["game_id"].split("/")[0] for m in tous})
        for l in evaluer(tous, gardiens_tous or [], [], {}, complet=False, tous_types=True, propres=False):
            l["equipe"] = f"tous les matchs ({matchs} matchs, {len(tous)} équipes-matchs, autres clubs inclus)"
            if l["n"]:
                out.append(l)
    else:
        autres = [m for m in ms if m["team_level"] != "PRO"]
        ids = {m["game_id"] for m in autres}
        for l in evaluer(autres, [g for g in gardiens if g["game_id"] in ids], [], {}, complet=False):
            l["equipe"] = "FRM+U21+U17 (expérience sans notre choix)"
            if l["n"]:
                out.append(l)
    out = [l for l in out if l["regle"].split(" ")[0] not in retirees]  # règle retirée : ni mesurée ni affichée
    cols = ["regle", "equipe", "n", "pour", "contre", "requis", "confiance", "verdict", "mesure"]
    en_tete = ["règle", "équipe", "n matchs", "pour", "contre", "n requis", "confiance", "verdict", "mesure"]
    txt = ["| " + " | ".join(en_tete) + " |", "|" + "---|" * len(cols)]
    txt += ["| " + " | ".join(str(l[c]).replace("|", "/") for c in cols) + " |" for l in out]
    for regle, manque in NON_MESURABLE:
        if regle.split(" ")[0] not in retirees:
            txt.append(f"| {regle} | — | — | — | — | — | — | non mesurable : il manque {manque} | — |")
    if shift is not None:
        txt += ["", "Test « shift length court » (matchs PRO où le réglage est fixé)", *test_shift(*shift)]
    if jours is not None:
        txt += ["", "Temps de glace par ligne (matchs PRO)", *temps_de_glace(glace or [], jours)]
    return "\n".join(txt)


def lire_tous():
    """Toutes les observations (Q_TOUS, Q_GARDIENS_TOUS) et les données du test shift (Q_SHIFT, Q_PRO_MATCHS)."""
    res = []
    for q in (Q_TOUS, Q_GARDIENS_TOUS, Q_SHIFT, Q_PRO_MATCHS):
        cols, lignes = sqlmod.executer(q)
        res.append([dict(zip(cols, l)) for l in lignes])
    tous, gardiens_tous, shift, pro = res
    return tous, gardiens_tous, ([(r["captured_at"], r["shift"]) for r in shift], pro)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    glace, jours = lire_glace()
    tous, gardiens_tous, shift = lire_tous()
    print(rapport(*lire(), retirees=lire_retirees(), glace=glace, jours=jours, tous=tous, gardiens_tous=gardiens_tous, shift=shift))
    return 0


if __name__ == "__main__":
    sys.exit(main())
