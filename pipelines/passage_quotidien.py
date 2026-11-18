"""Passage quotidien BasketVibe (P1, 17/11 ; décision D2 : lancé par une routine planifiée Claude, pas par GitHub Actions).

1. Rejoue le plan du jour (mêmes lectures et même rendu que `aujourdhui.py`, instantané `aujourdhui-AAAA-MM-JJ.md` compris).
2. Calcule l'état de chaque événement (`etat_jour`) et lance les agents de `etat_jour.agents_a_lancer` (table `agents` de
   docs/attentes/jeux/basketvibe.yaml), chacun par `claude -p --agent <nom>`, avec sa sortie attendue.
3. Écrit outputs/basketvibe/que-faire-AAAA-MM-JJ.md : ligne de statut des agents, une ligne « agent X non lancé : raison » par
   échec (jamais un silence), garde-fous, puis le plan.
0. Restaure depuis origin/claude/passage-quotidien les fichiers d'outputs/ absents de main (un fichier présent reste celui de main).
4. Commit et push de outputs/ sur claude/passage-quotidien, jamais sur main (la routine reçoit 403 sur main) ; la fusion vers main
   est un geste de session (fusion_main.py). « git : » dit « poussé sur claude/passage-quotidien » ou le refus 403.

Garde-fous : aucun achat, vente ni enchère (règle 2) — le script ne parle à aucun jeu, chaque agent reçoit l'interdiction ;
toute somme au-dessus de police.SEUIL_GROS_MONTANT sans trace police du jour donne une ligne 🟥 ; la police passe par
`dossier.py` d'abord (colonne `avant` de la table).

Lancer : python -I pipelines/passage_quotidien.py [--sans-agents] [--sans-git]
"""
import argparse
import re
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))  # python -I n'ajoute pas le dossier du script
RACINE = ICI.parent
BASE = RACINE / "outputs" / "basketvibe"
JEU = "basketvibe"

from police import SEUIL_GROS_MONTANT  # noqa: E402

SEUIL = SEUIL_GROS_MONTANT[JEU]
_CLAUDE = object()  # sentinelle : chercher la CLI dans le PATH
SOMME = re.compile(r"(?<![\d\-/:.])(\d{1,3}(?:[  ]\d{3})+)(?![\d\-/:])")
OUTILS = "Read,Grep,Glob,Write,Edit,Bash(python:*),Bash(python3:*)"


def _fr(n: int) -> str:
    return f"{n:,}".replace(",", " ")


# ---- Garde-fous ------------------------------------------------------------------------------------------------------------

def garde_fous(texte: str, police_du_jour: str) -> list:
    """Lignes 🟥 : une par somme au-dessus du seuil de gros montant quand l'agent police n'a laissé aucune trace aujourd'hui."""
    if police_du_jour.strip():
        return []
    sommes = sorted({int(re.sub(r"\D", "", m)) for m in SOMME.findall(texte)} - {None})
    return [f"🟥 Transferts : somme de {_fr(s)} au-dessus de {_fr(SEUIL)} sans police du jour — aucune action avant "
            f"`python -I pipelines/dossier.py {JEU} achat` puis l'agent police" for s in sommes if s > SEUIL]


def consigne_agent(e: dict, jour) -> str:
    return (f"Jeu : BasketVibe. Horizon d'action = aujourd'hui {jour.isoformat()} (aucune action reportée à un autre jour). "
            f"Événement : {e['evenement']}. À faire : {e['consigne']}. "
            f"Écris ta sortie dans outputs/{JEU}/{e['sortie']} (fichier non vide). "
            f"Interdit : aucun achat, aucune vente, aucune enchère (règle 2) — tu proposes, l'utilisateur exécute. "
            f"Toute somme au-dessus de {_fr(SEUIL)} : écris « police requise », sans plafond d'enchère.")


# ---- Lancement des agents --------------------------------------------------------------------------------------------------

def _derniere(s) -> str:
    lignes = [l for l in (s or "").strip().splitlines() if l.strip()]
    return lignes[-1][:160] if lignes else "sans message"


def lancer_agent(e: dict, jour, base=BASE, executer=subprocess.run, claude=_CLAUDE, timeout_min=15) -> tuple:
    """(lancé ?, raison) : commande préalable (`avant`), puis `claude -p --agent`, puis contrôle de la sortie attendue."""
    claude = shutil.which("claude") if claude is _CLAUDE else claude
    if not claude:
        return False, "CLI claude introuvable"
    try:
        if e.get("avant"):
            r = executer(shlex.split(e["avant"]), cwd=RACINE, capture_output=True, text=True, timeout=300)
            if r.returncode:
                return False, f"commande préalable « {e['avant']} » en échec (code {r.returncode} : {_derniere(r.stderr)})"
        cmd = [claude, "-p", consigne_agent(e, jour), "--agent", e["agent"], "--permission-mode", "acceptEdits",
               "--allowedTools", OUTILS, "--output-format", "text"]
        r = executer(cmd, cwd=RACINE, capture_output=True, text=True, timeout=timeout_min * 60)
    except subprocess.TimeoutExpired:
        return False, f"délai de {timeout_min} min dépassé"
    except OSError as x:
        return False, f"lancement impossible ({x})"
    if r.returncode:
        return False, f"code {r.returncode} : {_derniere(r.stderr or r.stdout)}"
    f = Path(base) / e["sortie"]
    if not f.is_file() or f.stat().st_size == 0:
        return False, f"sortie {e['sortie']} absente après l'exécution"
    return True, None


def lancer_tous(prevus: list, jour, base=BASE, timeout_min=15, **kw) -> list:
    res = []
    for e in prevus:
        e = dict(e)
        if e["statut"] == "a_lancer":
            e["lance"], e["raison"] = lancer_agent(e, jour, base=base, timeout_min=timeout_min, **kw)
        res.append(e)
    return res


# ---- Rendu -----------------------------------------------------------------------------------------------------------------

def non_lances(res: list) -> list:
    return [f"agent {e['agent']} non lancé : {e['raison']}" for e in res
            if e["statut"] == "refus" or (e["statut"] == "a_lancer" and not e.get("lance"))]


def statut_agents(res: list) -> str:
    if not res:
        return "Agents : aucun à lancer"
    morceaux = []
    for e in res:
        if e["statut"] == "deja_fait":
            morceaux.append(f"{e['agent']} déjà fait ({e['sortie']})")
        elif e["statut"] == "a_lancer" and e.get("lance"):
            morceaux.append(f"{e['agent']} lancé → {e['sortie']}")
        else:
            morceaux.append(f"{e['agent']} non lancé ({e['raison']})")
    n = sum(1 for e in res if e.get("lance"))
    return f"Agents : {n} lancé{'s' if n > 1 else ''} sur {len(res)} prévu{'s' if len(res) > 1 else ''} — " + " · ".join(morceaux)


def que_faire(jour, plan: str, res: list, gardes: list, alerte) -> str:
    t = [f"# Que faire — BasketVibe — {jour:%d/%m/%Y}", "",
         "Propositions seulement : aucun achat, aucune vente, aucune enchère sans ton accord écrit (règle 2).", ""]
    if alerte:
        t += [f"🟥 {alerte}", ""]
    t += [statut_agents(res), ""]
    t += [f"- {l}" for l in non_lances(res)] + ([""] if non_lances(res) else [])
    t += gardes + ([""] if gardes else [])
    return "\n".join(t + [plan.rstrip(), ""])


# ---- Git -------------------------------------------------------------------------------------------------------------------

BRANCHE_PASSAGE = "claude/passage-quotidien"  # 17/11 : la routine n'a pas le droit de pousser sur main (403) ; la fusion vers main
# reste un geste de session (fusion_main.py), jamais automatique


def restaurer(executer=subprocess.run, racine=None, branche=BRANCHE_PASSAGE) -> tuple:
    """(sha de la branche ou None, message) : si origin/<branche> existe, restaure depuis elle les fichiers d'outputs/ absents du
    dépôt (briefs, que-faire, learnings des passages pas encore fusionnés) ; un fichier présent reste celui de main."""
    racine = Path(racine or RACINE)
    run = lambda c: executer(c, cwd=racine, capture_output=True, text=True)  # noqa: E731
    r = run(["git", "fetch", "origin", branche])
    if r.returncode:
        return None, f"branche {branche} absente : rien à restaurer"
    sha = run(["git", "rev-parse", "FETCH_HEAD"]).stdout.strip() or None
    r = run(["git", "ls-tree", "-r", "--name-only", "FETCH_HEAD", "--", "outputs/"])
    manquants = [f for f in r.stdout.splitlines() if f.strip() and not (racine / f).exists()]
    if not manquants:
        return sha, f"restauration depuis {branche} : aucun fichier manquant"
    r = run(["git", "checkout", "FETCH_HEAD", "--", *manquants])
    if r.returncode:
        return sha, f"restauration depuis {branche} en échec : {_derniere(r.stderr)}"
    return sha, f"restauration depuis {branche} : {len(manquants)} fichier(s) d'outputs/ repris"


def commit_push(fichiers: list, jour, executer=subprocess.run, branche=BRANCHE_PASSAGE, attente=time.sleep, base_sha=None) -> tuple:
    """(ok, message) : add, commit si quelque chose change, push de HEAD sur `branche` (claude/passage-quotidien, jamais main)
    avec 4 nouvelles tentatives (2, 4, 8, 16 s). La branche est réécrite depuis HEAD (--force-with-lease sur le sha lu par
    restaurer) : ses fichiers absents de main ont été restaurés avant le commit, rien n'est perdu."""
    run = lambda c: executer(c, cwd=RACINE, capture_output=True, text=True)  # noqa: E731
    r = run(["git", "add", "--", *fichiers])
    if r.returncode:
        return False, f"git add en échec : {_derniere(r.stderr)}"
    if run(["git", "diff", "--cached", "--quiet"]).returncode == 0:
        return True, "rien à commiter"
    r = run(["git", "commit", "-m", f"Passage quotidien BasketVibe du {jour.isoformat()} (routine planifiée)"])
    if r.returncode:
        return False, f"git commit en échec : {_derniere(r.stderr or r.stdout)}"
    lease = f"--force-with-lease=refs/heads/{branche}:{base_sha}" if base_sha else f"--force-with-lease=refs/heads/{branche}:"
    for i in range(5):
        r = run(["git", "push", "-u", lease, "origin", f"HEAD:refs/heads/{branche}"])
        if r.returncode == 0:
            return True, f"poussé sur {branche}"
        if "403" in f"{r.stderr or ''}{r.stdout or ''}":
            return False, PUSH_403  # refus de droits : réessayer ne change rien
        if i < 4:
            attente(2 ** (i + 1))
    return False, f"git push en échec : {_derniere(r.stderr)}"


PUSH_403 = "403 même sur claude/ — droits d'écriture de l'application GitHub à donner"


# ---- Étiquettes d'expérience ----------------------------------------------------------------------------------------------

def etiqueter_experiences(executer=subprocess.run) -> str:
    """18/11 : `experiences_deduites.py --ecrire` avant le plan ; les lignes écrites dans outputs/basketvibe/fait-*.md partent
    avec les autres sorties de la routine (commit_push sur claude/passage-quotidien, jamais main). Échec : une ligne, jamais un arrêt."""
    try:
        r = executer([sys.executable, "-I", str(ICI / "experiences_deduites.py"), "--ecrire"], cwd=RACINE,
                     capture_output=True, text=True, timeout=300)
    except (OSError, subprocess.TimeoutExpired) as x:
        return f"étiquettes d'expérience : lancement impossible ({x})"
    if r.returncode:
        return f"étiquettes d'expérience en échec (code {r.returncode} : {_derniere(r.stderr or r.stdout)})"
    return f"étiquettes d'expérience : {_derniere(r.stdout)}"


# ---- Rejeu du plan ---------------------------------------------------------------------------------------------------------

def rejouer():
    """(jour, maintenant, rendu du plan, lignes d'état, sources, alerte) : lectures et rendu de aujourdhui.py, instantané écrit."""
    import aujourdhui as auj
    import etat_jour as ej
    maintenant = auj.heure_paris_naive()
    jour = maintenant.date()
    donnees, erreurs, n = auj.lire_tout(auj.charger_sql().executer)
    fait, S = auj.lire_fait(jour), auj.lire_sources(donnees, jour)
    _, rendu = auj.rendre_jour(auj.plan(donnees, erreurs, jour, maintenant, fait, S), donnees, erreurs, jour, maintenant, S, fait=fait)
    alerte = f"plan non fiable : {len(erreurs)} requêtes sur {n} en échec" if auj.echec_massif(erreurs, n) else None
    if not alerte:
        auj.ecrire_instantane(BASE / f"aujourdhui-{jour.isoformat()}.md", f"<!-- généré le {maintenant:%Y-%m-%d %H:%M} -->\n{rendu}\n", erreurs, n)
    cfg = ej.charger_config()
    etats = ej.lignes(ej.construire(donnees, S, BASE, jour, maintenant, cfg), cfg, maintenant)
    return jour, maintenant, rendu, etats, S, alerte, cfg


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--sans-agents", action="store_true", help="calcule les agents prévus sans les lancer")
    ap.add_argument("--sans-git", action="store_true", help="n'écrit ni commit ni push")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    import aujourdhui_sources as src
    import etat_jour as ej
    base_sha = None
    if not a.sans_git:
        base_sha, msg = restaurer()
        print(msg)
    print(etiqueter_experiences())  # avant le plan : le niveau du prochain amical suit l'étiquette écrite
    jour, _, rendu, etats, S, alerte, cfg = rejouer()
    prevus = ej.agents_a_lancer(etats, cfg, BASE, jour)
    if alerte or a.sans_agents:
        raison = alerte or "passage sans agents (--sans-agents)"
        res = [dict(e, statut="refus", raison=raison) if e["statut"] == "a_lancer" else e for e in prevus]
    else:
        res = lancer_tous(prevus, jour, timeout_min=cfg.get("agent_timeout_min", 15))
    sorties = "\n".join((BASE / e["sortie"]).read_text(encoding="utf-8") for e in res if (BASE / e["sortie"]).is_file())
    gardes = garde_fous(rendu + "\n" + sorties, src.lire_police(BASE, jour))
    f = BASE / f"que-faire-{jour.isoformat()}.md"
    f.write_text(que_faire(jour, rendu, res, gardes, alerte), encoding="utf-8")
    print(statut_agents(res))
    for l in non_lances(res):
        print(l)
    code = 2 if alerte else 0
    if not a.sans_git:
        ok, msg = commit_push(["outputs"], jour, base_sha=base_sha)
        print(f"git : {msg}")
        code = code or (0 if ok else 1)
    return code


if __name__ == "__main__":
    sys.exit(main())
