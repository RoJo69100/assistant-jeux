"""Tests de pipelines/passage_quotidien.py (P1, 17/11) : sans réseau, sans base, sans CLI claude ni git (exécuteurs simulés).
Lancer : python -I pipelines/test_passage_quotidien.py   (code 1 si un cas se trompe)"""
import datetime as dt
import os
import subprocess
import sys
import tempfile
import types
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import passage_quotidien as pq  # noqa: E402

JOUR = dt.date(2026, 11, 17)


def entree(agent="tactique", statut="a_lancer", avant=None, raison=None, sortie="briefs/2026-11-17-tactique-adv-a-18-11.md"):
    return {"agent": agent, "id": "m1", "evenement": "ligue contre Adv A, 18/11", "sortie": sortie, "consigne": "fiche",
            "avant": avant, "statut": statut, "raison": raison}


def executeur(codes, ecrit=None):
    """Exécuteur simulé : rend les codes dans l'ordre ; `ecrit` (chemin, texte) est écrit au lancement de claude."""
    appels = []

    def run(cmd, **kw):
        appels.append(cmd)
        if cmd[0] == "claude" and ecrit:
            Path(ecrit[0]).parent.mkdir(parents=True, exist_ok=True)
            Path(ecrit[0]).write_text(ecrit[1], encoding="utf-8")
        return subprocess.CompletedProcess(cmd, codes.pop(0) if codes else 0, "", "erreur simulée\n")
    run.appels = appels
    return run


def cas_garde_fous():
    s = pq.SEUIL
    yield "garde-fou : seuil lu dans police.SEUIL_GROS_MONTANT (250 000)", s == 250000
    yield "garde-fou : 300 000 sans police du jour → ligne police", any("police" in l for l in pq.garde_fous("enchère max 300 000", ""))
    yield "garde-fou : 300 000 avec police du jour → rien", pq.garde_fous("enchère max 300 000", "verdict police") == []
    yield "garde-fou : 75 000 → rien", pq.garde_fous("tester 3 prospects (75 000)", "") == []
    yield "garde-fou : une date ou une heure n'est pas une somme", pq.garde_fous("2026-11-17 20:00 m11", "") == []
    sommes = " ; ".join(f"enchère max {s}" for s in ("257 500", "302 500", "480 000", "803 750", "75 000", "302 500"))
    g = pq.garde_fous(sommes, "")
    yield "garde-fou 25/11 : plusieurs sommes → UNE seule ligne 🟥 (nombre, plus petite, plus grande)", len(g) == 1 \
        and "4 sommes de 257 500 à 803 750" in g[0] and g[0].startswith("🟥 Transferts")
    p = pq.consigne_agent(entree(), JOUR)
    yield "garde-fou : la consigne d'agent interdit achat, vente et enchère et donne l'horizon du jour", \
        "aucun achat" in p and "aucune enchère" in p and "2026-11-17" in p and "250 000" in p and "police" in p


def cas_lancement():
    with tempfile.TemporaryDirectory() as tmp:
        e = entree()
        ok, raison = pq.lancer_agent(e, JOUR, base=tmp, executer=executeur([]), claude=None)
        yield "lancement : CLI claude absente → raison, pas de silence", not ok and "claude" in raison
        ok, raison = pq.lancer_agent(entree(agent="police", avant="python -I pipelines/dossier.py basketvibe achat", sortie="police-2026-11-17.md"),
                                     JOUR, base=tmp, executer=executeur([1]), claude="claude")
        yield "lancement : commande préalable en échec (dossier) → police non lancée, raison donnée", not ok and "dossier.py" in raison
        ok, raison = pq.lancer_agent(e, JOUR, base=tmp, executer=executeur([2]), claude="claude")
        yield "lancement : code retour non nul → raison avec le code", not ok and "code 2" in raison
        ok, raison = pq.lancer_agent(e, JOUR, base=tmp, executer=executeur([0]), claude="claude")
        yield "lancement : sortie absente après l'exécution → raison", not ok and "sortie" in raison
        run = executeur([0], ecrit=(Path(tmp) / e["sortie"], "Ligue contre Adv A (18/11)\n"))
        ok, raison = pq.lancer_agent(e, JOUR, base=tmp, executer=run, claude="claude")
        yield "lancement : sortie écrite → lancé", ok and raison is None and run.appels[0][:2] == ["claude", "-p"] and "tactique" in run.appels[0]

        def lent(cmd, **kw):
            raise subprocess.TimeoutExpired(cmd, 60)
        ok, raison = pq.lancer_agent(e, JOUR, base=tmp, executer=lent, claude="claude", timeout_min=1)
        yield "lancement : délai dépassé → raison", not ok and "délai" in raison


def cas_rendu():
    res = [dict(entree(), lance=True, raison=None), dict(entree(agent="analyste", statut="deja_fait", raison="sortie déjà présente (x)")),
           dict(entree(agent="academie", statut="refus", raison="plafond de 3 agents d'analyse par passage atteint")),
           dict(entree(agent="police"), lance=False, raison="CLI claude introuvable")]
    st = pq.statut_agents(res)
    yield "rendu : une seule ligne de statut", "\n" not in st and st.startswith("Agents :")
    nl = pq.non_lances(res)
    yield "rendu : chaque échec donne « agent X non lancé : raison »", \
        nl == ["agent academie non lancé : plafond de 3 agents d'analyse par passage atteint", "agent police non lancé : CLI claude introuvable"]
    yield "rendu : sans agent prévu, la ligne de statut le dit", pq.statut_agents([]) == "Agents : aucun à lancer"
    t = pq.que_faire(JOUR, "## plan\n| a |", res, ["🟥 garde"], None)
    yield "rendu : le que-faire porte statut, non-lancés, garde-fous puis le plan", \
        t.index("Agents :") < t.index("agent academie non lancé") < t.index("🟥 garde") < t.index("## plan")
    yield "rendu : règle 2 rappelée en tête", "aucun achat, aucune vente, aucune enchère" in t
    yield "rendu : plan non fiable dit en clair", "plan non fiable" in pq.que_faire(JOUR, "", [], [], "plan non fiable : 9 requêtes sur 10 en échec")


def cas_git():
    run = executeur([0, 1, 0, 1, 0])  # add, diff (changements), commit, push en échec, push
    ok, msg = pq.commit_push(["outputs/basketvibe/que-faire-2026-11-17.md"], JOUR, executer=run, branche="b", attente=lambda s: None)
    cmds = [" ".join(c[:3]) for c in run.appels]
    yield "git : add, commit, push réessayé après un échec réseau", ok and cmds[0].startswith("git add") and cmds[2].startswith("git commit") \
        and cmds.count("git push -u") == 2
    run = executeur([0, 0])  # add, diff (rien)
    ok, msg = pq.commit_push(["x"], JOUR, executer=run, branche="b", attente=lambda s: None)
    yield "git : rien à commiter → pas d'échec, pas de push", ok and not any(c[:2] == ["git", "push"] for c in run.appels)

    run = executeur([0, 1, 0, 0])
    ok, msg = pq.commit_push(["outputs"], JOUR, executer=run, attente=lambda s: None, base_sha="abc")
    push = next(c for c in run.appels if c[:2] == ["git", "push"])
    yield "git : push sur claude/passage-quotidien, jamais sur main", ok and msg == "poussé sur claude/passage-quotidien" \
        and push[-1] == "HEAD:refs/heads/claude/passage-quotidien" and not any("main" in x for c in run.appels for x in c) \
        and "--force-with-lease=refs/heads/claude/passage-quotidien:abc" in push

    pushes = []

    def refus(c, **kw):  # add, diff (changements), commit : ok ; chaque push : 403
        push = c[:2] == ["git", "push"]
        pushes.append(push)
        code = 1 if push or c[:3] == ["git", "diff", "--cached"] else 0
        err = "remote: Permission denied\nfatal: unable to access 'https://github.com/x/y/': The requested URL returned error: 403" if push else ""
        return types.SimpleNamespace(returncode=code, stdout="", stderr=err)
    ok, msg = pq.commit_push(["x"], JOUR, executer=refus, attente=lambda s: None)
    yield "git : push refusé (403) sur claude/ → « 403 même sur claude/ — droits d'écriture… », sans nouvelle tentative", not ok \
        and msg == "403 même sur claude/ — droits d'écriture de l'application GitHub à donner" and sum(pushes) == 1


def _git(d, *a):
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    return subprocess.run(["git", *a], cwd=d, capture_output=True, text=True, env=env, check=True)


def cas_restauration():
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        _git(t, "init", "-q", "--bare", "-b", "main", "origine.git")
        _git(t, "clone", "-q", "origine.git", "a")
        a = t / "a"
        (a / "outputs" / "basketvibe").mkdir(parents=True)
        (a / "outputs" / "basketvibe" / "commun.md").write_text("main", encoding="utf-8")
        _git(a, "add", ".")
        _git(a, "commit", "-q", "-m", "main")
        _git(a, "push", "-q", "origin", "main")
        sans = pq.restaurer(racine=a)
        yield "restauration : branche absente → rien, sans erreur", sans[0] is None and "absente" in sans[1]
        _git(a, "checkout", "-q", "-b", "claude/passage-quotidien")
        (a / "outputs" / "basketvibe" / "commun.md").write_text("branche", encoding="utf-8")
        (a / "outputs" / "basketvibe" / "brief-tactique-2026-11-16.md").write_text("brief", encoding="utf-8")
        (a / "outputs" / "basketvibe" / "que-faire-2026-11-16.md").write_text("qf", encoding="utf-8")
        _git(a, "add", ".")
        _git(a, "commit", "-q", "-m", "passage")
        _git(a, "push", "-q", "origin", "claude/passage-quotidien")
        _git(t, "clone", "-q", "-b", "main", "origine.git", "b")
        b = t / "b"
        sha, msg = pq.restaurer(racine=b)
        o = b / "outputs" / "basketvibe"
        yield "restauration : fichiers absents de main repris depuis la branche", sha and "2 fichier(s)" in msg \
            and (o / "brief-tactique-2026-11-16.md").read_text(encoding="utf-8") == "brief" and (o / "que-faire-2026-11-16.md").is_file()
        yield "restauration : un fichier présent sur main reste celui de main", (o / "commun.md").read_text(encoding="utf-8") == "main"


def cas_etiquettes():
    """18/11 : l'étiquette d'expérience est écrite par la routine, sans intervention, avant le plan."""
    with tempfile.TemporaryDirectory() as t:
        f = Path(t) / "fait-2026-11-14.md"

        def run(cmd, **kw):
            run.cmd = cmd
            if "--ecrire" in cmd:
                f.write_text("- [clé=Artificial Instinct 14/11] [expérience=E1:A]\n", encoding="utf-8")
            return subprocess.CompletedProcess(cmd, 0, "1 amical(s) étiqueté(s)\n", "")
        msg = pq.etiqueter_experiences(run)
        yield "étiquettes : experiences_deduites.py --ecrire lancé, étiquette écrite sans intervention", \
            "experiences_deduites.py" in run.cmd[2] and "[expérience=E1:A]" in f.read_text(encoding="utf-8") \
            and msg == "étiquettes d'expérience : 1 amical(s) étiqueté(s)"
        echec = pq.etiqueter_experiences(lambda c, **k: subprocess.CompletedProcess(c, 1, "", "base injoignable\n"))
        yield "étiquettes : échec → une ligne, pas d'arrêt", echec.startswith("étiquettes d'expérience en échec (code 1")
    ordre = []
    sauve = (pq.etiqueter_experiences, pq.rejouer, sys.argv)
    pq.etiqueter_experiences = lambda: ordre.append("etiquettes") or "ok"

    def rejouer():
        ordre.append("plan")
        raise RuntimeError("arrêt du test")
    pq.rejouer, sys.argv = rejouer, ["passage_quotidien.py", "--sans-git", "--sans-agents"]
    try:
        pq.main()
    except RuntimeError:
        pass
    finally:
        pq.etiqueter_experiences, pq.rejouer, sys.argv = sauve
    yield "étiquettes : écrites avant le plan dans main()", ordre == ["etiquettes", "plan"]
    yield "étiquettes : fait-*.md dans outputs/, publié par commit_push(['outputs']) sur la branche de la routine", \
        "commit_push([\"outputs\"]" in Path(pq.__file__).read_text(encoding="utf-8") and pq.BRANCHE_PASSAGE != "main"


def cas_police():
    """18/11 : police lancée par la routine pour toute enchère/achat de maximum > seuil finissant dans les 36 h, 3 au plus."""
    m = dt.datetime(2026, 11, 18, 14, 45)
    fin = m + dt.timedelta(hours=9)
    cibles = [{"nom": "Alan Szewczyk", "max": 550_000, "fin": fin}, {"nom": "Petit Prix", "max": 250_000, "fin": fin},
              {"nom": "Loin Loin", "max": 900_000, "fin": m + dt.timedelta(hours=40)}]
    bargains = [{"name": "Zoran Vujovic", "bid_ceiling_resale": 300_000, "ends_paris": str(fin)},
                {"name": "Ivo Trois", "bid_ceiling_resale": 400_000, "ends_paris": str(fin)},
                {"name": "Quatre Refus", "bid_ceiling_resale": 500_000, "ends_paris": str(fin)}]
    c = pq.candidats_police(cibles, bargains, m)
    noms = [x["nom"] for x in c]
    yield "police : > 250 000 et fin dans 36 h retenu", "Alan Szewczyk" in noms and "Zoran Vujovic" in noms
    yield "police : = 250 000 pas de police", "Petit Prix" not in noms
    yield "police : fin au-delà de 36 h exclue", "Loin Loin" not in noms
    with tempfile.TemporaryDirectory() as tmp:
        appels = []

        def run(cmd, **k):
            appels.append(cmd)
            if cmd[0] == "claude":
                nom = cmd[2].split("Joueur : ")[1].split(",")[0]
                f = Path(tmp) / "police-2026-11-18.md"
                verdict = "ne pas acheter " + nom if nom == "Zoran Vujovic" else f"enchère max 550 000 sur {nom}"
                with f.open("a", encoding="utf-8") as h:
                    h.write(f"\n## achat — {nom} — 14:50\n- Décision : {verdict}\n")
            return subprocess.CompletedProcess(cmd, 0, "", "")
        res = pq.lancer_polices(c, dt.date(2026, 11, 18), base=tmp, executer=run, claude="claude",
                                horloge=lambda: dt.datetime(2026, 11, 18, 14, 52))
        lances = [r for r in res if r["lance"]]
        refus = [r for r in res if not r["lance"]]
        yield "police : ligne > 250 000 → dossier.py puis claude -p --agent police", \
            appels[0][:5] == ["python", "-I", "pipelines/dossier.py", "basketvibe", "achat"] \
            and appels[1][0] == "claude" and appels[1][1] == "-p" and appels[1][3:5] == ["--agent", "police"]
        yield "police : 3 lancées au plus", len(lances) == 3 and sum(1 for a in appels if a[0] == "claude") == 3
        yield "police : 4e ligne refusée avec message", len(refus) == 1 and refus[0]["nom"] == "Quatre Refus" \
            and "plafond de 3 polices par passage" in refus[0]["raison"] \
            and any("Quatre Refus" in l and "plafond" in l for l in pq.polices_non_lancees(res))
        txt = (Path(tmp) / "police-2026-11-18.md").read_text(encoding="utf-8")
        rendu = ("| 🟥 URGENT | Transferts | Enchère sur Alan Szewczyk (SG) : maximum 550 000 |\n"
                 "- Enchère maximale 300 000 sur Zoran Vujovic (SF, PS 40.5)\n"
                 "| Alan Szewczyk | SG | 28 | 56,4 |\n- Enchère sur Petit Prix : maximum 250 000")
        frais = pq.annoter(rendu, res, txt, dt.datetime(2026, 11, 18, 14, 0), dt.datetime(2026, 11, 18, 14, 55))
        l = frais.splitlines()
        yield "plan : « police faite à HH:MM, prix de l'export de HH:MM » sur la ligne", \
            l[0].endswith("— police faite à 14:52, prix de l'export de 14:00 |") and "police faite" not in l[3]
        yield "plan : ligne de données du marché non annotée", "police" not in l[2]
        yield "plan : prix frais (< 2 h) sans « à relire »", "à relire" not in frais
        vieux = pq.annoter(rendu, res, txt, dt.datetime(2026, 11, 18, 11, 0), dt.datetime(2026, 11, 18, 14, 55))
        yield "plan : prix de plus de 2 h → « à relire en jeu avant d'enchérir »", \
            "prix de l'export de 11:00 — à relire en jeu avant d'enchérir" in vieux.splitlines()[0]
        yield "plan : « ne pas acheter » en premier sur la ligne", \
            l[1].startswith("- Police : ne pas acheter — Enchère maximale 300 000 sur Zoran Vujovic")
        yield "plan : la ligne reste une proposition (aucun ordre au jeu)", \
            all(a[0] in ("python", "claude") for a in appels) and "Interdit : aucun achat" in appels[1][2]
    yield "seuil inchangé : 250 000", pq.SEUIL == 250_000


def cas_police_plan():
    """19/11 : la police automatique couvre aussi les lignes d'offres et de vente du plan au-dessus de 250 000 (dossier puis police),
    plafond de 3 polices par passage inchangé."""
    import test_etat_jour as T
    m = dt.datetime(2026, 11, 19, 10, 0)
    ann = (T.ANN + ["height_cm", "best_slot", "best_fit"], [["g1", "Gros Gain", "SG", 24, 50, 260000, "2026-11-19T22:00:00", 10000, None, "SG", 58.1],
                                                               ["g2", "Petit Gain", "SG", 24, 50, 1000, "2026-11-19T22:00:00", 10000, None, "SG", 58.1]])
    cases = T._plan_19()["prix_cases_poste"]
    cases = (cases[0], cases[1] + [["SG", 50, "22-25", 4, 100000, 200000, 300000, 90000, 400000]])
    d = dict(T.marche(**T._plan_19()), annonces_actives=ann, prix_cases_poste=cases, tolerance_vente=(["value"], [[1.0]]),
             **{"gold.finance_health": (["capacite_invest"], [[900000]])})
    S = {"cibles": [], "police": "", "refus_police": ""}
    c = pq.candidats_plan(d, S, m)
    yield "police du plan : offre de max 300 000 et vente de Baron à 400 000 retenues, offre à 1 000 (max 300 000) aussi", \
        sorted((x["nom"], x["type"]) for x in c) == [("Gros Gain", "achat"), ("Nolan Baron", "vente"), ("Petit Gain", "achat")]
    yield "police du plan : refus « ne pas vendre » ou police déjà faite aujourd'hui → exclu", \
        "Nolan Baron" not in [x["nom"] for x in pq.candidats_plan(d, dict(S, refus_police="ne pas vendre nolan baron"), m)] \
        and "Gros Gain" not in [x["nom"] for x in pq.candidats_plan(d, dict(S, police="## achat — gros gain"), m)]
    v = next(x for x in c if x["type"] == "vente")
    yield "police du plan : consigne et dossier de type vente, « ne pas vendre » si refus", "Type : vente" in pq.consigne_police(v, m.date()) \
        and "2026-11-19-vente.md" in pq.consigne_police(v, m.date()) and "ne pas vendre Nolan Baron" in pq.consigne_police(v, m.date())
    vus = []
    def lancer(cands, jour):
        vus.extend(cands)
        orig, pq.lancer_agent = pq.lancer_agent, lambda *a, **k: (False, "test")
        try:
            return pq.lancer_polices(cands, jour)
        finally:
            pq.lancer_agent = orig
    plus = [{"nom": f"N{i}", "max": 500000, "fin": None, "type": "vente"} for i in range(3)]
    _, res = pq.passage_police((d, {}, 1, ""), m.date(), m, S, "rendu", lancer=lancer, plan_cands=c + plus)
    yield "police du plan : candidats du plan passés à la routine, plafond de 3 par passage", len(vus) == 6 \
        and sum("plafond de 3 polices" in str(r["raison"]) for r in res) == 3


def cas_relance():
    import datetime as dt2
    import tempfile
    with tempfile.TemporaryDirectory() as t:
        j = dt2.date(2026, 11, 23)
        yield "relance : sans instantané, pas d'heure de passage", pq.horodatage_passage(t, j) is None
        (Path(t) / "aujourdhui-2026-11-23.md").write_text("<!-- généré le 2026-11-23 10:40 -->\nplan\n", encoding="utf-8")
        depuis = pq.horodatage_passage(t, j)
        yield "relance : heure du dernier passage lue dans l'instantané", depuis == dt2.datetime(2026, 11, 23, 10, 40)
    prevus = [{"agent": "tactique", "id": "m-ligue", "statut": "a_lancer", "raison": None},
              {"agent": "academie", "id": "academie-1", "statut": "a_lancer", "raison": None},
              {"agent": "entrainement", "id": "entr-1", "statut": "deja_fait", "raison": "x"}]
    etats = [{"id": "m-ligue", "arrivee": dt2.datetime(2026, 11, 23, 15, 41)},
             {"id": "academie-1", "arrivee": dt2.datetime(2026, 11, 19, 9, 0)}, {"id": "entr-1", "arrivee": None}]
    res = {e["id"]: e for e in pq.filtrer_relance(prevus, etats, depuis)}
    yield "relance : l'aperçu exporté à 15:41 lance l'agent tactique", res["m-ligue"]["statut"] == "a_lancer"
    yield "relance : le rapport d'académie du 19/11 n'est pas nouveau", res["academie-1"]["statut"] == "inchange" and "10:40" in res["academie-1"]["raison"]
    yield "relance : un agent déjà fait reste « deja_fait »", res["entr-1"]["statut"] == "deja_fait"
    yield "relance : sans passage antérieur, rien n'est filtré", pq.filtrer_relance(prevus, etats, None) == prevus
    yield "relance : un agent « inchange » n'est jamais listé comme non lancé en échec", pq.non_lances([res["academie-1"], res["entr-1"]]) == []


def cas_plan_22():
    import etat_jour as ej
    table = "| Nom | Prix attendu |\n|---|---|\n| Zed (PF) | 300 000 |"
    yield "garde-fou : une somme > 250 000 dans une table de prix (pas seulement une ligne d'action) sans police -> ligne rouge", \
        any("300 000" in l for l in pq.garde_fous(table, ""))
    o = {"case_min_ventes": 3, "matchs_rotation": 4, "minutes_hors_rotation": 6, "vente_marge_profit": 0.1}
    x = {"type": "vente", "nom": "Zed", "poste": "PF", "age": 27, "note": 47.9, "prix": 5250.0, "mediane": 5250.0, "n_case": 4,
         "min_moy": 3.0, "mini": 350.0, "maxi": 65000.0, "remplacant": "Lef", "ecart": -15.1, "tolerance": 1.0, "prix_achat": None, "salaire": 12000.0}
    yield "vente : la ligne affiche le salaire hebdomadaire libéré", "libère 12 000 de salaire hebdomadaire" in ej.texte_transfert(x, o).replace(chr(160), " ").replace(chr(8239), " ")
    yield "vente : sans salaire connu, pas de mention inventée", "libère" not in ej.texte_transfert(dict(x, salaire=None), o)


FICHE_23 = """# Tactique — Wrzos 23/11
## À saisir
### Écran 1 — Composition
| | PG | SG | SF | PF | C |
|---|---|---|---|---|---|
| Q1 | Richard | Bonnet | Gimenez | Fournier | Lefebvre |
### Écran 2 — Consignes
| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Min | Off. focus | Rôle | Tir | Agress. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Richard | PG | PG | — | PG | PG | PG | 36 | 2 | 1 | 2 | 3 |
| Albano | PF | — | — | PF | — | — | 12 | 3 | 3 | 1 | 3 |
| Durand | SF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
### Écran 3 — Adversaires
| Adversaire | Poste | Focus défensif (1-5) | Zone |
|---|---|---|---|
| Mazur | PG | 3 | Perimeter (1) |
## Après sauvegarde, vérifie
secret
"""


def cas_fiches_23_11():
    """23/11 : lien sur chaque ligne Composition, écrans recopiés au que-faire, aucun joueur en vente dans une fiche."""
    import etat_jour as ej
    fiche = {"fichier": "briefs/2026-11-23-tactique-wrzos.md", "ok": True, "defauts": []}
    ev = {"genre": "ligue", "adversaire": "Wrzos", "jour": dt.date(2026, 11, 23), "verrou": dt.datetime(2026, 11, 23, 19, 45), "fiche": fiche}
    cfg = {"matchs": {"ligue": {"libelle": "match de ligue"}}}
    _, texte, _ = ej._match_gabarit(dict(ev, ecran={"defauts": [{"correction": "mets minutes de Richard à 36"}]}), "ecran", dt.datetime(2026, 11, 23, 17), cfg)
    yield "lien : la ligne « corrige l'écran » porte le lien GitHub complet du brief", \
        "https://github.com/RoJo69100/assistant-jeux/blob/claude/passage-quotidien/outputs/basketvibe/briefs/2026-11-23-tactique-wrzos.md" in texte
    rendu = "| 🟥 URGENT | Composition | corrige | x |\n| 🟧 IMPORTANT | Entraînement | y |\n| 🟧 IMPORTANT | Composition | saisis |"
    yield "lien : lignes_composition ne renvoie que les lignes Composition", len(pq.lignes_composition(rendu)) == 2
    with tempfile.TemporaryDirectory() as t:
        (Path(t) / "briefs").mkdir()
        (Path(t) / "briefs" / "2026-11-23-tactique-wrzos.md").write_text(FICHE_23, encoding="utf-8")
        (Path(t) / "briefs" / "2026-11-23-tactique-loin.md").write_text(FICHE_23.replace("Wrzos", "Loin"), encoding="utf-8")
        m = dt.datetime(2026, 11, 23, 17, 0)
        etats = [{"type": "match", "evenement": "ligue Wrzos", "fiche": "briefs/2026-11-23-tactique-wrzos.md", "echeance": dt.datetime(2026, 11, 23, 19, 45)},
                 {"type": "match", "evenement": "amical Loin", "fiche": "briefs/2026-11-23-tactique-loin.md", "echeance": dt.datetime(2026, 11, 25, 7, 45)}]
        s = pq.a_saisir(etats, m, base=t)
        yield "saisie : section « À saisir aujourd'hui » avec les écrans 1, 2 et 3 recopiés du brief dans les 24 h", \
            s.startswith("## À saisir aujourd'hui") and "### Écran 1" in s and "### Écran 2" in s and "### Écran 3" in s and "| Albano | PF |" in s
        yield "saisie : un brief à plus de 24 h et le reste du brief (annexe) n'y sont pas", "Loin" not in s and "secret" not in s
        yield "saisie : le que-faire contient la section", "## À saisir aujourd'hui" in pq.que_faire(dt.date(2026, 11, 23), "plan", [], [], None, saisie=s)
        v = pq.joueurs_en_vente("| 🟧 | Transferts | vente : Anselmo Albano (PF, 27 ans, note 48), prix attendu 6 000 |")
        yield "vente : le nom du joueur en vente est lu au plan", v == ["Anselmo Albano"]
        yield "vente : une fiche qui fait jouer un joueur en vente est signalée", \
            pq.fiches_avec_vendus(t, ["briefs/2026-11-23-tactique-wrzos.md"], v) == [("briefs/2026-11-23-tactique-wrzos.md", "Albano")]
        yield "vente : une fiche sans le joueur (ou à 0 minute) n'est pas signalée", \
            pq.fiches_avec_vendus(t, ["briefs/2026-11-23-tactique-wrzos.md"], ["Pierre Durand"]) == []
    yield "vente : la consigne de l'agent tactique interdit de faire jouer le joueur en vente", \
        "Anselmo Albano" in pq.consigne_agent(entree(), JOUR, ["Anselmo Albano"]) and "Ne fais jouer" not in pq.consigne_agent(entree(), JOUR)


def cas_plafonds_separes():
    """23/11 : trois fiches tactiques ne bloquent plus l'agent académie (tactique hors du plafond de 3 agents d'analyse)."""
    import etat_jour as ej
    cfg = {"agents_plafond": 3, "agents_hors_plafond": ["analyste", "police", "tactique"],
           "agents": [{"type": "match", "prochain": "fiche", "agent": "tactique", "sortie": "briefs/{jour}-t-{cle}.md"},
                      {"type": "academie", "prochain": "rapport", "agent": "academie", "sortie": "briefs/{jour}-academie.md"}]}
    etats = [{"type": "match", "prochain": "fiche", "action": True, "cle": f"m{i}", "id": f"m{i}", "evenement": f"match {i}"} for i in range(4)]
    etats.append({"type": "academie", "prochain": "rapport", "action": True, "cle": "a", "id": "a", "evenement": "académie"})
    with tempfile.TemporaryDirectory() as t:
        (Path(t) / "t").mkdir()
        for a in ("tactique", "academie"):
            (Path(t) / "t" / f"{a}.md").write_text("x", encoding="utf-8")
        res = ej.agents_a_lancer(etats, cfg, base=Path(t) / "b", jour=JOUR, dossier_agents=Path(t) / "t")
    yield "plafonds : 4 fiches tactiques puis l'académie → les 5 sont à lancer", [e["statut"] for e in res] == ["a_lancer"] * 5
    cfg2 = dict(cfg, agents_hors_plafond=["analyste", "police"])
    with tempfile.TemporaryDirectory() as t:
        (Path(t) / "t").mkdir()
        for a in ("tactique", "academie"):
            (Path(t) / "t" / f"{a}.md").write_text("x", encoding="utf-8")
        res2 = ej.agents_a_lancer(etats, cfg2, base=Path(t) / "b", jour=JOUR, dossier_agents=Path(t) / "t")
    yield "plafonds : contre-épreuve, tactique dans le plafond → l'académie est refusée", res2[-1]["statut"] == "refus"
    yield "plafonds : le yaml du jeu met tactique hors plafond", "tactique" in ej.charger_config()["agents_hors_plafond"]


def cas_base_indisponible():
    """24/11 : base saturée (66 requêtes sur 66 en échec) → rien n'est écrasé, ligne 🟥 dans un fichier à part, sortie."""
    def panne(sql):
        raise SystemExit("erreur SQL (https 503) : base simulée en échec")
    appels = []

    def une_sur_trois(sql):
        appels.append(sql)
        if len(appels) == 1:
            raise TimeoutError("lecture expirée")
        return [{"ok": 1}]
    yield "base : 3 sondes sur 3 en échec → panne", (pq.sonde_base(panne) or "").startswith("3 sondes sur 3 en échec")
    yield "base : 1 sonde sur 3 en échec → pas de panne", pq.sonde_base(une_sur_trois) is None

    import aujourdhui as auj
    with tempfile.TemporaryDirectory() as t:
        base = Path(t)
        qf = base / f"que-faire-{JOUR.isoformat()}.md"
        qf.write_text("plan du matin\n", encoding="utf-8")
        brief = base / "briefs" / "2026-11-17-tactique-adv-a-18-11.md"
        brief.parent.mkdir()
        brief.write_text("brief du matin\n", encoding="utf-8")
        avant = {p: p.read_text(encoding="utf-8") for p in (qf, brief)}
        engages = []
        anciens = (pq.BASE, auj.charger_sql, auj.heure_paris_naive, sys.argv, pq.etiqueter_experiences, pq.rejouer)
        pq.BASE = base
        auj.charger_sql = lambda: types.SimpleNamespace(executer=panne)
        auj.heure_paris_naive = lambda: dt.datetime(2026, 11, 17, 18, 30)
        sys.argv = ["passage_quotidien.py", "--relance", "--sans-git"]
        pq.etiqueter_experiences = lambda *a, **k: engages.append("etiquettes") or ""
        pq.rejouer = lambda: engages.append("rejouer")
        try:
            code = pq.main()
        finally:
            pq.BASE, auj.charger_sql, auj.heure_paris_naive, sys.argv, pq.etiqueter_experiences, pq.rejouer = anciens
        f = pq.fichier_indisponible(base, JOUR)
        lignes = f.read_text(encoding="utf-8").splitlines() if f.is_file() else [""]
        yield "base : passage en panne → code 2", code == 2
        yield "base : que-faire et brief du matin inchangés", all(p.read_text(encoding="utf-8") == v for p, v in avant.items())
        yield "base : aucun autre fichier écrit", sorted(p.name for p in base.iterdir()) == sorted(["briefs", qf.name, f.name])
        yield "base : ligne 🟥 « base indisponible » en tête du fichier à part", lignes[0].startswith("🟥 base indisponible : 3 sondes")
        yield "base : ni étiquettes, ni plan, ni agents après la sonde en échec", engages == []
        pousses = []
        pq.sortie_base_indisponible(JOUR, dt.datetime(2026, 11, 17, 18, 40), "plan non fiable : 66 requêtes sur 66 en échec",
                                    base=base, commit=lambda fs: pousses.append(fs) or (True, "poussé"))
        lignes = f.read_text(encoding="utf-8").splitlines()
        yield "base : deuxième panne en tête, la première reste dessous", "18:40" in lignes[0] and "18:30" in lignes[1]
        yield "base : seul ce fichier est commité", len(pousses) == 1 and len(pousses[0]) == 1 and pousses[0][0].endswith(f.name)


def cas_vues_perimees():
    """25/11 : une vue matérialisée de plus de 3 h, avec des pages arrivées depuis → 🟥 « vues périmées », rien d'écrasé."""
    def vues(raf, last, maxp, maint="2026-11-17T17:30:00+00:00"):
        def run(sql):
            if sql == pq.SQL_FRAICHEUR:
                return (["rafraichi_a", "last_page_id", "max_page", "maintenant"], [(raf, last, maxp, maint)])
            return (["ok"], [(1,)])
        return run
    m = pq.vues_perimees(vues("2026-11-17T12:30:00+00:00", 100, 105)) or ""
    yield "vues : 5 h et des pages arrivées depuis → périmées", m.startswith("vues périmées")
    yield "vues : l'âge de chaque vue (7 vues, 5.0 h)", all(f"{v} 5.0 h" in m for v in pq.VUES_MAT) and len(pq.VUES_MAT) == 7
    yield "vues : heure de Paris du dernier rafraîchissement", "17/11 à 13:30" in m
    yield "vues : 2 h seulement → pas périmées", pq.vues_perimees(vues("2026-11-17T15:30:00+00:00", 100, 105)) is None
    yield "vues : 11 h mais aucune page depuis → pas périmées", pq.vues_perimees(vues("2026-11-17T06:30:00+00:00", 105, 105)) is None
    yield "vues : 3 h tout juste → pas périmées", pq.vues_perimees(vues("2026-11-17T14:30:00+00:00", 100, 105)) is None
    yield "vues : jamais rafraîchies → périmées, âge inconnu", "âge inconnu" in (pq.vues_perimees(vues(None, None, 105)) or "")

    def casse(sql):
        raise SystemExit("erreur SQL")
    yield "vues : lecture impossible → pas de blocage ici (la sonde couvre la panne)", pq.vues_perimees(casse) is None

    import aujourdhui as auj
    with tempfile.TemporaryDirectory() as t:
        base = Path(t)
        qf = base / f"que-faire-{JOUR.isoformat()}.md"
        qf.write_text("plan du matin\n", encoding="utf-8")
        engages = []
        anciens = (pq.BASE, auj.charger_sql, auj.heure_paris_naive, sys.argv, pq.etiqueter_experiences, pq.rejouer)
        pq.BASE = base
        auj.charger_sql = lambda: types.SimpleNamespace(executer=vues("2026-11-17T12:30:00+00:00", 100, 105))
        auj.heure_paris_naive = lambda: dt.datetime(2026, 11, 17, 18, 30)
        sys.argv = ["passage_quotidien.py", "--sans-git"]
        pq.etiqueter_experiences = lambda *a, **k: engages.append("etiquettes") or ""
        pq.rejouer = lambda: engages.append("rejouer")
        try:
            code = pq.main()
        finally:
            pq.BASE, auj.charger_sql, auj.heure_paris_naive, sys.argv, pq.etiqueter_experiences, pq.rejouer = anciens
        f = pq.fichier_indisponible(base, JOUR)
        tete = f.read_text(encoding="utf-8").splitlines()[0] if f.is_file() else ""
        yield "vues : passage → code 2, ligne 🟥 « vues périmées » en tête", code == 2 and tete.startswith("🟥 vues périmées : core.standing 5.0 h")
        yield "vues : que-faire inchangé, aucun autre fichier", qf.read_text(encoding="utf-8") == "plan du matin\n" \
            and sorted(p.name for p in base.iterdir()) == sorted([qf.name, f.name])
        yield "vues : ni étiquettes, ni plan, ni agents", engages == []


CAS = [cas_vues_perimees, cas_base_indisponible, cas_plafonds_separes, cas_fiches_23_11,cas_plan_22,cas_garde_fous, cas_lancement, cas_rendu, cas_git, cas_restauration, cas_etiquettes, cas_police, cas_police_plan, cas_relance]

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    echecs = 0
    jeux = [r for c in CAS for r in c()]
    for nom, ok in jeux:
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    print(f"{len(jeux) - echecs}/{len(jeux)}")
    sys.exit(1 if echecs else 0)
