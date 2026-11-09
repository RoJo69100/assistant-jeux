"""Revue hebdomadaire du modèle BasketVibe (étape 6a, critères R1-R9 de docs/refonte-v3/journal-aujourdhui.md).

Usage : python -I pipelines/revue_hebdo.py basketvibe [--jour AAAA-MM-JJ]
Écrit outputs/basketvibe/revue-hebdo-AAAA-MM-JJ.md (une page, 60 lignes au plus) et l'instantané
outputs/basketvibe/revue-hebdo/instantane-AAAA-MM-JJ.json (somme des « contre » des leçons, types de pages non lus).
Lecture seule sur la base. Aucune interprétation, aucun conseil : un chiffre, son n et sa source par section ;
« n insuffisant » ou « donnée manquante » quand la base ne permet pas de répondre.
Semaine = les 7 jours finissant le jour de Paris (pipelines/heure_paris.py, jamais l'horloge du shell).
Étape 6c (V4) : ligne « Version du moteur » sous l'en-tête (core.engine_version) ; une version absente de l'instantané
précédent fait lister les décisions ouvertes d'avant son début, sans rien marquer.
"""
import argparse
import datetime as dt
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python -I n'ajoute pas le dossier du script
import aujourdhui as auj  # noqa: E402
import aujourdhui_sources as src  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent
BASE = RACINE / "outputs/basketvibe"
PLAYBOOK = RACINE / "docs/refonte-v3/playbook-basketvibe.md"
N_MIN_VERDICTS = 10  # R2 : sous ce nombre de verdicts, la part contredite est « n insuffisant » (consigne de l'étape 6a)
JOURS_BLOQUEE = 14   # R3 : hypothèse sans nouvelle mesure depuis 14 jours (consigne de l'étape 6a)
MAX_LIGNES = 60
# R2 : une requête de prédiction qui lit un réglage saisi ou joué mesure l'exécution ; sinon l'effet
EXECUTION = ("tier", "bv_match_tactics", "bv_saisie", "player_directives", "bv_amical_reglage", "bv_zone_jouee")
# R7 : paramètre du playbook → clé de core.game_params (aucune autre clé n'existe le 09/11)
PARAM_CLES = {"Âge de déclin": "age_declin"}
# R5 : `etude_evenements_basketvibe.py calculs` mesuré à 11,4 s le 2026-11-09 17:00 Paris, au-delà de 10 s : non lancé
ETUDE = "non calculé : `etude_evenements_basketvibe.py calculs` dure 11,4 s (mesure du 09/11), au-delà de 10 s"
STATUTS = {"hypothesis": "hypothèse", "validated": "validée", "retired": "retirée"}
VERDICTS = {"confirmed": "confirmé", "contradicted": "contredit", "inconclusive": "non concluant"}


def requetes(jour: dt.date) -> dict:
    d, f = (jour - dt.timedelta(days=6)).isoformat(), (jour + dt.timedelta(days=1)).isoformat()
    return {
        "verdicts": "select distinct on (o.decision_id) o.decision_id, d.domain, o.verdict, o.measured_at, "
                    "d.prediction ->> 'metric' as metric, coalesce(d.prediction ->> 'requete', '') as requete "
                    "from learn.outcome o join learn.decision d on d.id = o.decision_id where d.game = 'basketvibe' "
                    f"and o.measured_at >= '{d}' and o.measured_at < '{f}' order by o.decision_id, o.measured_at desc",
        "attente": "select d.id, d.domain from learn.decision d where d.game = 'basketvibe' "
                   f"and d.decided_at >= '{d}' and d.decided_at < '{f}' "
                   "and not exists (select 1 from learn.outcome o where o.decision_id = d.id)",
        "lecons": "select l.id, l.status, l.n_for, l.n_against, (select max(o.measured_at) from learn.decision x "
                  "join learn.outcome o on o.decision_id = x.id where x.lesson_id = l.id) as derniere_mesure "
                  "from learn.lesson l where l.game = 'basketvibe' order by l.id",
        "matchs": "select match_day, competition, opponent, my_result, my_pts, opp_pts, margin from gold.bv_match_report "
                  f"where match_day >= '{d}' and match_day < '{f}' order by match_day, competition",
        "amical_reglage": "select fixture_id, match_day, opponent, agress_cran, primary_quarts, tir_cran4_joueurs "
                          "from gold.bv_amical_reglage",
        "couverture": "select count(*) filter (where lu_par_silver = 'non') as non_lus, count(*) as types "
                      "from gold.bv_couverture_pages",
        "params": "select key, value, source, verified_on from core.game_params where game = 'basketvibe'",
        # V4 (6c) : versions du moteur et décisions ouvertes (proposées ou faites, sans verdict), jour de Paris
        "versions": "select version, competition_kind, start_date, end_date from core.engine_version where game = 'basketvibe'",
        "ouvertes": "select d.id, (d.decided_at at time zone 'Europe/Paris')::date as jour from learn.decision d "
                    "where d.game = 'basketvibe' and d.status in ('proposed', 'done') "
                    "and not exists (select 1 from learn.outcome o where o.decision_id = d.id) order by d.id",
    }


def lire_tout(executer, jour):
    """{nom: [dict]} ; une requête en échec donne None (la section dit « donnée manquante »)."""
    def une(sql):
        try:
            cols, lignes = executer(sql)
            return [dict(zip(cols, l)) for l in lignes]
        except SystemExit:
            return None
    q = requetes(jour)
    with ThreadPoolExecutor(max_workers=len(q)) as pool:
        fut = {k: pool.submit(une, v) for k, v in q.items()}
    return {k: f.result() for k, f in fut.items()}


def pct(a, b):
    return f"{100 * a / b:.0f} %".replace(".", ",")


def mesure(v):
    """R2 : 'exécution' si la requête de la prédiction lit un réglage saisi ou joué, sinon 'effet'."""
    return "exécution" if any(m in (v.get("requete") or "") for m in EXECUTION) else "effet"


def sec_decisions(verdicts, attente):
    t = ["## 1. Décisions : prédictions contre résultats"]
    if verdicts is None or attente is None:
        return t + ["donnée manquante : learn.outcome ou learn.decision illisible", ""]
    doms = sorted({v["domain"] for v in verdicts} | {a["domain"] for a in attente})
    if not doms:
        return t + ["0 verdict et 0 décision en attente cette semaine (n = 0) — source : learn.outcome × learn.decision", ""]
    t += ["| Domaine | Confirmés | Contredits | Non concluants | En attente | Mesure | Part contredite (n) |",
          "|---|---|---|---|---|---|---|"]
    for dom in doms:
        vs = [v for v in verdicts if v["domain"] == dom]
        c = {k: sum(v["verdict"] == k for v in vs) for k in VERDICTS}
        ex = sum(mesure(v) == "exécution" for v in vs)
        n = len(vs)
        part = f"n insuffisant (n = {n})" if n < N_MIN_VERDICTS else f"{pct(c['contradicted'], n)} (n = {n})"
        t.append(f"| {dom} | {c['confirmed']} | {c['contradicted']} | {c['inconclusive']} | "
                 f"{sum(a['domain'] == dom for a in attente)} | effet {n - ex}, exécution {ex} | {part} |")
    t += ["", f"Verdicts : {len(verdicts)} ; en attente (décidées dans la semaine, sans verdict) : {len(attente)}. "
          "Source : learn.outcome × learn.decision ; mesure = exécution si la requête lit un réglage saisi ou joué.", ""]
    return t


def sec_lecons(lecons, jour, precedent):
    t = ["## 2. Leçons"]
    if lecons is None:
        return t + ["donnée manquante : learn.lesson illisible", ""]
    if not lecons:
        return t + ["0 leçon (n = 0) — source : learn.lesson", ""]
    etats = {}
    for l in lecons:
        etats[l["status"]] = etats.get(l["status"], 0) + 1
    t.append("États : " + " ; ".join(f"{STATUTS.get(k, k)} {v}" for k, v in sorted(etats.items()))
             + f" (n = {len(lecons)}) — source : learn.lesson")
    total = sum(int(l["n_against"] or 0) for l in lecons)
    if precedent is None:
        t.append(f"« Contre » ajoutés cette semaine : pas d'instantané précédent (total actuel {total})")
    else:
        t.append(f"« Contre » ajoutés depuis l'instantané du {precedent['jour']} : {total - precedent['n_against']} "
                 f"(total {total})")
    limite = jour - dt.timedelta(days=JOURS_BLOQUEE)
    bloquees = [l["id"] for l in lecons if l["status"] == "hypothesis"
                and (l["derniere_mesure"] is None or auj._jour(l["derniere_mesure"]) < limite)]
    n_hyp = sum(l["status"] == "hypothesis" for l in lecons)
    t.append(f"Hypothèses sans nouvelle mesure depuis {JOURS_BLOQUEE} jours : {len(bloquees)} sur {n_hyp}"
             + (f" ({', '.join(str(i).replace('basketvibe:', '') for i in bloquees)})" if bloquees else "")
             + " — mesure = learn.outcome d'une décision liée (lesson_id)")
    return t + [""]


def sec_matchs(matchs):
    t = ["## 3. Matchs de la semaine"]
    if matchs is None:
        return t + ["donnée manquante : gold.bv_match_report illisible", ""]
    if not matchs:
        t.append("0 match exporté cette semaine (n = 0) — source : gold.bv_match_report")
    else:
        t += ["| Jour | Compétition | Adversaire | Résultat | Score | Marge |", "|---|---|---|---|---|---|"]
        for m in matchs:
            t.append(f"| {auj._jour(m['match_day']):%d/%m} | {m['competition']} | {str(m['opponent']).replace('|', chr(92) + '|')} | "
                     f"{m['my_result'] or '—'} | {m['my_pts']}-{m['opp_pts']} | {int(m['margin']):+d} |")
        comp = {}
        for m in matchs:
            comp[m["competition"]] = comp.get(m["competition"], 0) + 1
        moy = sum(float(m["margin"]) for m in matchs) / len(matchs)
        t += ["", f"Marge moyenne : {moy:+.1f}".replace(".", ",") + f" (n = {len(matchs)}) ; par compétition : "
              + " ; ".join(f"{k} {v}" for k, v in sorted(comp.items())) + " — résultat = my_result, source : gold.bv_match_report"]
    t.append("Matchs les plus mal prédits : donnée manquante : aucune prédiction de marge en base")
    return t + [""]


def sec_experiences(experiences, joues, jour):
    t = ["## 4. Expériences amicales"]
    if experiences is None:
        return t + ["donnée manquante : docs/attentes/experiences-amicales-basketvibe.yaml illisible", ""]
    if joues is None:
        return t + ["donnée manquante : gold.bv_amical_reglage illisible", ""]
    v = auj.verifier(experiences, joues)
    t.append(" ; ".join(f"{e['id']} {v[e['id']]['verifies']} vérifié{'s' if v[e['id']]['verifies'] > 1 else ''} "
                        f"sur {e['amicaux_vises']}" for e in experiences["file"])
             + f" (faits déclarés : {len(experiences['faits'])}) — source : registre fait-*.md × gold.bv_amical_reglage")
    if jour.isoweekday() == 7:
        t.append(f"n disponible des chiffres de l'étude : {ETUDE}")
    return t + [""]


def sec_a_conclure(experiences, joues):
    """S3 (étape 6b) : expériences dont les amicaux vérifiés atteignent le visé ; aucun verdict n'est écrit."""
    t = ["## 5. Expériences à conclure"]
    if experiences is None or joues is None:
        return t + ["donnée manquante : fichier d'expériences ou gold.bv_amical_reglage illisible", ""]
    v = auj.verifier(experiences, joues)
    pretes = [e for e in experiences["file"] if v[e["id"]]["verifies"] >= int(e["amicaux_vises"])]
    source = " — source : fichier d'expériences (clé lecons) × gold.bv_amical_reglage ; verdict non écrit"
    if not pretes:
        t.append(f"aucune expérience à conclure (0 sur {len(experiences['file'])} au nombre visé d'amicaux vérifiés)" + source)
    for i, e in enumerate(pretes):
        lecons = ", ".join(e.get("lecons") or []) or "aucune (leçon à créer, voir le fichier d'expériences)"
        t.append(f"verdict à produire : {e['id']}, n = {v[e['id']]['verifies']}, leçons {lecons}"
                 + (source if i == len(pretes) - 1 else ""))
    return t + [""]


def sec_donnees(couverture, precedent):
    t = ["## 6. Données non collectées"]
    if not couverture:
        return t + ["donnée manquante : gold.bv_couverture_pages illisible", ""], None
    n, types = int(couverture[0]["non_lus"]), int(couverture[0]["types"])
    ecart = "pas d'instantané précédent" if precedent is None or precedent.get("non_lus") is None \
        else f"écart avec l'instantané du {precedent['jour']} : {n - precedent['non_lus']:+d}"
    t.append(f"Types de pages reçus et non lus : {n} sur {types} ; {ecart} — source : gold.bv_couverture_pages")
    return t + [""], n


def cle_version(v):
    return f"basketvibe/{v['competition_kind']}/{v['version']}/{auj._jour(v['start_date']).isoformat()}"


def lignes_version(versions, ouvertes, jour, precedent):
    """V4 (6c) : (lignes sous l'en-tête, clés des versions pour l'instantané). Lecture seule, rien n'est marqué."""
    if versions is None or ouvertes is None:
        return ["Version du moteur : donnée manquante (core.engine_version ou learn.decision illisible)"], None
    en_cours = {}
    for v in versions:
        fin = v["end_date"]
        if auj._jour(v["start_date"]) <= jour and (fin is None or auj._jour(fin) >= jour):
            en_cours[v["competition_kind"]] = v["version"]
    debuts = [auj._jour(v["start_date"]) for v in versions if auj._jour(v["start_date"]) <= jour]
    dernier = max(debuts) if debuts else None
    n = sum(auj._jour(o["jour"]) < dernier for o in ouvertes) if dernier else 0
    t = [f"Version du moteur : ligue {en_cours.get('ligue', 'non attribuée')}, amical {en_cours.get('amical', 'non attribuée')} ; "
         f"décisions ouvertes d'une version antérieure : {n}"
         + (f" (avant le {dernier:%d/%m})" if dernier else "") + " — source : core.engine_version × learn.decision"]
    cles = sorted(cle_version(v) for v in versions)
    if precedent is not None and precedent.get("versions") is not None:
        for v in sorted(versions, key=cle_version):
            if cle_version(v) in precedent["versions"]:
                continue
            debut = auj._jour(v["start_date"])
            ids = [str(o["id"]) for o in ouvertes if auj._jour(o["jour"]) < debut]
            t.append(f"Nouvelle version {v['competition_kind']} {v['version']} (depuis le {debut:%d/%m}) : conseils ouverts d'avant "
                     f"({len(ids)}) : {', '.join(ids) or 'aucun'} ; rien n'est marqué")
    return t, cles


def lire_parametres(texte):
    """R7 : lignes (paramètre, valeur, où) du tableau « ### Paramètres écrits à la main » du playbook."""
    res, dans = [], False
    for l in texte.splitlines():
        if l.startswith("### Paramètres écrits à la main"):
            dans = True
            continue
        if dans and l.startswith("#"):
            break
        if dans and l.startswith("|"):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            if len(c) >= 3 and c[0] != "Paramètre" and not set(c[0]) <= set("-: "):
                res.append(tuple(c[:3]))
    return res


def sec_parametres(parametres, params):
    t = ["## 7. Paramètres écrits à la main"]
    if not parametres:
        return t + ["donnée manquante : tableau « Paramètres écrits à la main » absent du playbook", ""]
    cles = {p["key"]: p for p in params or []}
    t += ["| Paramètre | Valeur | Dernier calcul (core.game_params) |", "|---|---|---|"]
    jamais = 0
    for nom, valeur, _ in parametres:
        p = cles.get(PARAM_CLES.get(nom, ""))
        if p is None:
            jamais += 1
            t.append(f"| {nom} | {valeur} | jamais calculé |")
        else:
            t.append(f"| {nom} | {valeur} | {p['verified_on']} ({p['source']}) |")
    t += ["", f"{jamais} sur {len(parametres)} jamais calculés — source : playbook-basketvibe.md, core.game_params"
          + ("" if params is not None else " (core.game_params illisible)"), ""]
    return t


def precedent_instantane(dossier, jour):
    """Instantané le plus récent daté d'avant `jour` (celui d'il y a 7 jours ou plus en priorité) ; None s'il n'y en a pas."""
    snaps = []
    for f in Path(dossier).glob("instantane-*.json"):
        m = re.match(r"instantane-(\d{4}-\d{2}-\d{2})\.json$", f.name)
        if m and dt.date.fromisoformat(m.group(1)) < jour:
            snaps.append((dt.date.fromisoformat(m.group(1)), f))
    if not snaps:
        return None
    vieux = [s for s in snaps if s[0] <= jour - dt.timedelta(days=7)]
    d, f = max(vieux or snaps, key=lambda s: s[0])
    x = json.loads(f.read_text(encoding="utf-8"))
    x["jour"] = f"{d:%d/%m}"
    return x


def page(donnees, jour, experiences, parametres, precedent):
    """(lignes de la page, instantané à écrire)."""
    t = [f"# Revue de la semaine BasketVibe — du {jour - dt.timedelta(days=6):%d/%m} au {jour:%d/%m/%Y}", "",
         "Chiffres seuls, sans interprétation ni conseil. Source et n à chaque section."]
    v, cles = lignes_version(donnees.get("versions"), donnees.get("ouvertes"), jour, precedent)
    t += v + [""]
    t += sec_decisions(donnees.get("verdicts"), donnees.get("attente"))
    t += sec_lecons(donnees.get("lecons"), jour, precedent)
    t += sec_matchs(donnees.get("matchs"))
    t += sec_experiences(experiences, donnees.get("amical_reglage"), jour)
    t += sec_a_conclure(experiences, donnees.get("amical_reglage"))
    d, non_lus = sec_donnees(donnees.get("couverture"), precedent)
    t += d
    t += sec_parametres(parametres, donnees.get("params"))
    lecons = donnees.get("lecons")
    snap = {"n_against": sum(int(l["n_against"] or 0) for l in lecons) if lecons else None, "non_lus": non_lus,
            "versions": cles}
    return t, snap


def borner(lignes):
    """R1 : une page de MAX_LIGNES lignes au plus ; au-delà, les dernières lignes sont remplacées par une ligne qui le dit."""
    if len(lignes) <= MAX_LIGNES:
        return lignes
    return lignes[:MAX_LIGNES - 1] + [f"(page coupée : {len(lignes) - MAX_LIGNES + 1} lignes de plus non affichées)"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("jeu")
    ap.add_argument("--jour", help="AAAA-MM-JJ ; défaut : le jour de Paris")
    a = ap.parse_args()
    if a.jeu != "basketvibe":
        sys.exit("seul basketvibe est pris en charge")
    debut = time.time()
    jour = dt.date.fromisoformat(a.jour) if a.jour else auj.heure_paris_naive().date()
    donnees = lire_tout(auj.charger_sql().executer, jour)
    dossier = BASE / "revue-hebdo"
    lignes, snap = page(donnees, jour, src.lire_experiences(BASE, jour), lire_parametres(PLAYBOOK.read_text(encoding="utf-8")),
                        precedent_instantane(dossier, jour))
    lignes = borner(lignes)
    sortie = BASE / f"revue-hebdo-{jour.isoformat()}.md"
    sortie.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    dossier.mkdir(parents=True, exist_ok=True)
    (dossier / f"instantane-{jour.isoformat()}.json").write_text(json.dumps(snap) + "\n", encoding="utf-8")
    print(f"écrit {sortie.relative_to(RACINE)} ({len(lignes)} lignes, {time.time() - debut:.1f} s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
