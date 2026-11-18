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


CAS = [cas_garde_fous, cas_lancement, cas_rendu, cas_git, cas_restauration, cas_etiquettes]

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    echecs = 0
    jeux = [r for c in CAS for r in c()]
    for nom, ok in jeux:
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    print(f"{len(jeux) - echecs}/{len(jeux)}")
    sys.exit(1 if echecs else 0)
