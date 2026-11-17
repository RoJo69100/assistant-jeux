"""Tests de pipelines/passage_quotidien.py (P1, 17/11) : sans réseau, sans base, sans CLI claude ni git (exécuteurs simulés).
Lancer : python -I pipelines/test_passage_quotidien.py   (code 1 si un cas se trompe)"""
import datetime as dt
import subprocess
import sys
import tempfile
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


CAS = [cas_garde_fous, cas_lancement, cas_rendu, cas_git]

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    echecs = 0
    jeux = [r for c in CAS for r in c()]
    for nom, ok in jeux:
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    print(f"{len(jeux) - echecs}/{len(jeux)}")
    sys.exit(1 if echecs else 0)
