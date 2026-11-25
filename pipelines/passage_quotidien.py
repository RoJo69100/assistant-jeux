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
Police des gros transferts (18/11) : toute enchère ou achat proposé de maximum > SEUIL dont l'enchère finit dans les 36 h →
`dossier.py <jeu> achat` puis `claude -p --agent police` (3 au plus par passage, au-delà une ligne de refus) ; sortie
outputs/basketvibe/police-AAAA-MM-JJ.md, poussée avec outputs/ sur claude/passage-quotidien. La ligne du plan dit « police faite
à HH:MM, prix de l'export de HH:MM » (+ « à relire en jeu avant d'enchérir » au-delà de 2 h ; refus de la police en premier).

Lancer : python -I pipelines/passage_quotidien.py [--sans-agents] [--sans-git] [--relance]
"""
import argparse
import datetime as dt
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
    """UNE ligne 🟥 (25/11, consigne de l'utilisateur : 25 lignes regroupées) quand des sommes dépassent le seuil de gros montant
    et que l'agent police n'a laissé aucune trace aujourd'hui : nombre de sommes, plus petite et plus grande."""
    if police_du_jour.strip():
        return []
    sommes = sorted(s for s in {int(re.sub(r"\D", "", m)) for m in SOMME.findall(texte)} if s > SEUIL)
    if not sommes:
        return []
    quoi = f"somme de {_fr(sommes[0])}" if len(sommes) == 1 else f"{len(sommes)} sommes de {_fr(sommes[0])} à {_fr(sommes[-1])}"
    return [f"🟥 Transferts : {quoi} au-dessus de {_fr(SEUIL)} sans police du jour — aucune action avant "
            f"`python -I pipelines/dossier.py {JEU} achat` puis l'agent police"]


def consigne_agent(e: dict, jour, vendus=()) -> str:
    interdits = f"Ne fais jouer aucun de ces joueurs (leur vente est proposée au plan) : {', '.join(vendus)}. " if vendus else ""
    return (interdits +f"Jeu : BasketVibe. Horizon d'action = aujourd'hui {jour.isoformat()} (aucune action reportée à un autre jour). "
            f"Événement : {e['evenement']}. À faire : {e['consigne']}. "
            f"Écris ta sortie dans outputs/{JEU}/{e['sortie']} (fichier non vide). "
            f"Interdit : aucun achat, aucune vente, aucune enchère (règle 2) — tu proposes, l'utilisateur exécute. "
            f"Toute somme au-dessus de {_fr(SEUIL)} : écris « police requise », sans plafond d'enchère.")


# ---- Lancement des agents --------------------------------------------------------------------------------------------------

def _derniere(s) -> str:
    lignes = [l for l in (s or "").strip().splitlines() if l.strip()]
    return lignes[-1][:160] if lignes else "sans message"


def lancer_agent(e: dict, jour, base=BASE, executer=subprocess.run, claude=_CLAUDE, timeout_min=15, vendus=()) -> tuple:
    """(lancé ?, raison) : commande préalable (`avant`), puis `claude -p --agent`, puis contrôle de la sortie attendue."""
    claude = shutil.which("claude") if claude is _CLAUDE else claude
    if not claude:
        return False, "CLI claude introuvable"
    try:
        if e.get("avant"):
            r = executer(shlex.split(e["avant"]), cwd=RACINE, capture_output=True, text=True, timeout=300)
            if r.returncode:
                return False, f"commande préalable « {e['avant']} » en échec (code {r.returncode} : {_derniere(r.stderr)})"
        cmd = [claude, "-p", e.get("prompt") or consigne_agent(e, jour, vendus), "--agent", e["agent"], "--permission-mode", "acceptEdits",
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


# ---- Relance (22/11) --------------------------------------------------------------------------------------------------------
# Second passage du jour (16:30 Paris) : un aperçu de match exporté après le passage de 10:40 n'a aucune fiche avant le lendemain.
# --relance ne lance que les agents dont le prérequis (aperçu, page, rapport) est arrivé après le dernier passage du jour.

def horodatage_passage(base, jour):
    """Heure de Paris du dernier passage du jour (« généré le AAAA-MM-JJ HH:MM » de l'instantané) ; None sans instantané."""
    f = Path(base) / f"aujourdhui-{jour.isoformat()}.md"
    if not f.is_file():
        return None
    m = re.search(r"généré le (\d{4}-\d{2}-\d{2} \d{2}:\d{2})", f.read_text(encoding="utf-8")[:300])
    return dt.datetime.strptime(m.group(1), "%Y-%m-%d %H:%M") if m else None


def filtrer_relance(prevus: list, etats: list, depuis) -> list:
    """Agents « a_lancer » dont la ligne d'état n'a pas reçu de prérequis après `depuis` : statut « inchange » (jamais lancés).
    Sans passage antérieur (depuis None), rien n'est filtré."""
    if depuis is None:
        return prevus
    arrivee = {l.get("id"): l.get("arrivee") for l in etats}
    res = []
    for e in prevus:
        a = arrivee.get(e["id"])
        if e["statut"] == "a_lancer" and not (a is not None and a > depuis):
            e = dict(e, statut="inchange", raison=f"aucun prérequis arrivé depuis le passage de {depuis:%H:%M}")
        res.append(e)
    return res


# ---- Police des gros transferts (18/11) ------------------------------------------------------------------------------------
# Toute enchère ou achat proposé dont le maximum dépasse SEUIL et dont l'enchère finit dans les 36 h : dossier.py puis l'agent
# police, lancés par la routine (3 au plus par passage). La ligne reste une proposition : accord écrit requis (règle 2).
POLICES_MAX = 3
HORIZON_POLICE_H = 36
PRIX_FRAIS_H = 2
REFUS = ("ne pas acheter", "ne pas vendre")


def _date(v):
    if v in (None, ""):
        return None
    return v if isinstance(v, dt.datetime) else dt.datetime.fromisoformat(str(v)[:19])


def candidats_police(cibles: list, bargains: list, maintenant, seuil=SEUIL, horizon_h=HORIZON_POLICE_H) -> list:
    """Décisions d'achat ouvertes (S['cibles'] : max) et affaires du marché (bid_ceiling_resale) de maximum > seuil dont la fin
    tombe dans les `horizon_h` heures ; fin inconnue : exclue (pas de plafond à donner loin de la fin). Un joueur une fois."""
    lim, vus, res = maintenant + dt.timedelta(hours=horizon_h), set(), []
    lignes = [(c.get("nom"), c.get("max"), c.get("fin")) for c in cibles] \
        + [(r.get("name"), r.get("bid_ceiling_resale"), r.get("ends_paris")) for r in bargains]
    for nom, mx, fin in lignes:
        fin = _date(fin)
        if not nom or mx in (None, "") or float(mx) <= seuil or fin is None or not maintenant < fin <= lim \
                or str(nom).lower() in vus:
            continue
        vus.add(str(nom).lower())
        res.append({"nom": str(nom), "max": float(mx), "fin": fin})
    return res


def candidats_plan(donnees, S, maintenant, seuil=SEUIL, horizon_h=HORIZON_POLICE_H) -> list:
    """19/11 (consigne de l'utilisateur) : lignes d'offres et de vente du plan (etat_jour.offres_du_jour / ventes_du_jour, mêmes seuils
    que le plan) dont le montant dépasse le seuil : offre = max(enchère max, prix), fin dans les horizon_h heures ; vente = prix
    attendu, annonce à créer (pas de fin). Joueur déjà nommé par la police du jour (S['police']) : exclu."""
    import aujourdhui as auj
    import etat_jour as ej
    import que_faire_blocs as qfb
    o = ej.charger_offres()
    cap = next((r.get("capacite_invest") for r in auj.lignes_de(donnees, "gold.finance_health")), None)
    ouvertes = [c for c in S.get("cibles", []) if c.get("fin") is None or c["fin"] > maintenant]
    cap = None if cap in (None, "") else float(cap) - sum(float(c["max"]) for c in ouvertes)
    refus, deja = S.get("refus_police", ""), str(S.get("police", "")).lower()
    of = ej.offres_du_jour(donnees, o, cap, maintenant, [c["nom"] for c in S.get("cibles", [])], refus)["offres"][:int(o["max_offres"])]
    ventes = ej.ventes_du_jour(donnees, o, qfb._tolerance(donnees), f"{S.get('police', '')}\n{refus}")[:int(o["max_ventes"])]
    lim, res = maintenant + dt.timedelta(hours=horizon_h), []
    for x in of:
        mx, fin = max(float(x["max"]), float(x["prix"])), x.get("fin")
        if mx > seuil and fin is not None and maintenant < fin <= lim:
            res.append({"nom": x["nom"], "max": mx, "fin": fin, "type": "achat"})
    res += [{"nom": x["nom"], "max": float(x["prix"]), "fin": None, "type": "vente"} for x in ventes if float(x["prix"]) > seuil]
    return [c for c in res if c["nom"].lower() not in deja]


def consigne_police(c: dict, jour) -> str:
    t = c.get("type", "achat")  # 19/11 : achat (enchère) ou vente (ligne de vente du plan)
    verbe = "acheter" if t == "achat" else "vendre"
    quand = f"fin d'enchère {c['fin']:%d/%m %H:%M}" if c.get("fin") else "annonce à créer"
    return (f"Jeu : BasketVibe. Type : {t}. Joueur : {c['nom']}, {'maximum proposé' if t == 'achat' else 'prix attendu'} {_fr(int(c['max']))}, "
            f"{quand}. Horizon d'action = aujourd'hui {jour.isoformat()}. "
            f"Dossier : outputs/{JEU}/dossier/{jour.isoformat()}-{t}.md. Brouillon : la ligne du plan du jour sur {c['nom']}. "
            f"Plafond : 12 appels d'outil, 3 minutes. Ajoute à outputs/{JEU}/police-{jour.isoformat()}.md une section "
            f"« ## {t} — {c['nom']} — HH:MM » (Verdict, Décision ; écris « ne pas {verbe} {c['nom']} » si tu refuses). "
            f"Interdit : aucun achat, aucune vente, aucune enchère (règle 2) — tu proposes, l'utilisateur exécute.")


def lancer_polices(cands: list, jour, base=BASE, horloge=None, plafond=POLICES_MAX, **kw) -> list:
    """[{nom, lance, raison, heure}] : dossier.py (`avant`) puis `claude -p --agent police` pour les `plafond` premiers ;
    au-delà, refus avec message. Lancée = la trace du jour nomme le joueur après l'exécution."""
    if horloge is None:
        import aujourdhui as auj
        horloge = auj.heure_paris_naive
    sortie, res = f"police-{jour.isoformat()}.md", []
    for i, c in enumerate(cands):
        r = dict(c, lance=False, raison=None, heure=None)
        if i >= plafond:
            r["raison"] = f"plafond de {plafond} polices par passage atteint — lance-la en session (dossier.py puis agent police)"
        else:
            e = {"agent": "police", "sortie": sortie, "prompt": consigne_police(c, jour),
                 "avant": f"python -I pipelines/dossier.py {JEU} {c.get('type', 'achat')} --mots {shlex.quote(c['nom'])} --date {jour.isoformat()}"}
            ok, raison = lancer_agent(e, jour, base=base, timeout_min=kw.pop("timeout_min", 5), **kw)
            f = Path(base) / sortie
            if ok and c["nom"].lower() not in f.read_text(encoding="utf-8").lower():
                ok, raison = False, f"{sortie} ne nomme pas {c['nom']} après l'exécution"
            r.update(lance=ok, raison=raison, heure=horloge() if ok else None)
        res.append(r)
    return res


def polices_non_lancees(res: list) -> list:
    return [f"police non lancée pour {r['nom']} (maximum {_fr(int(r['max']))}) : {r['raison']}" for r in res if not r["lance"]]


def verdict_police(police_txt: str, nom: str):
    """« ne pas acheter » / « ne pas vendre » si une section de la trace police qui nomme `nom` le dit, sinon None."""
    for s in re.split(r"\n(?=## )", police_txt.lower()):
        if nom.lower() in s:
            v = next((x for x in REFUS if f"{x} {nom.lower()}" in s
                      or any(x in l for l in s.splitlines() if l.lstrip("- ").startswith("décision"))), None)
            if v:
                return v
    return None


def annoter(rendu: str, res: list, police_txt: str, prix_export, maintenant) -> str:
    """Lignes d'enchère ou d'achat du plan qui nomment un joueur contrôlé : « police faite à HH:MM, prix de l'export de HH:MM »
    (+ « à relire en jeu avant d'enchérir » si les prix ont plus de 2 h) ; refus de la police écrit en premier."""
    faits = [r for r in res if r["lance"]]
    out = []
    for l in rendu.splitlines():
        r = next((r for r in faits if r["nom"].lower() in l.lower()
                  and re.search(r"ench[èe]r|achet|achat|revente", l, re.I)), None)
        if r is None or not l.lstrip().startswith(("-", "|")):
            out.append(l)
            continue
        if prix_export is None:
            fin = f" — police faite à {r['heure']:%H:%M}, heure de l'export des prix inconnue — à relire en jeu avant d'enchérir"
        else:
            jour = "" if prix_export.date() == maintenant.date() else f" du {prix_export:%d/%m}"
            fin = f" — police faite à {r['heure']:%H:%M}, prix de l'export{jour} de {prix_export:%H:%M}"
            if maintenant - prix_export > dt.timedelta(hours=PRIX_FRAIS_H):
                fin += " — à relire en jeu avant d'enchérir"
        v = verdict_police(police_txt, r["nom"])
        tete = f"Police : {v} — " if v else ""
        if l.lstrip().startswith("|"):
            cel = l.rstrip().split("|")
            i = 3 if len(cel) >= 5 else len(cel) - 2
            cel[i] = f" {tete}{cel[i].strip()}{fin} "
            out.append("|".join(cel))
        else:
            ind, corps = l[:len(l) - len(l.lstrip())], l.lstrip()[1:].lstrip()
            out.append(f"{ind}- {tete}{corps}{fin}")
    return "\n".join(out)


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


def lignes_composition(rendu: str) -> list:
    """Lignes du tableau du plan de catégorie Composition (23/11 : chacune porte le lien GitHub complet du brief)."""
    return [l for l in rendu.splitlines() if re.match(r"\|[^|]*\|\s*Composition\s*\|", l)]


def a_saisir(etats: list, maintenant, base=BASE, horizon_h=24) -> str:
    """Section « À saisir aujourd'hui » : tableaux Écran 1, 2 et 3 de chaque brief dont l'échéance tombe dans les `horizon_h` heures,
    recopiés tels quels (23/11 : l'utilisateur n'ouvre rien d'autre)."""
    fin = maintenant + dt.timedelta(hours=horizon_h)
    blocs, vus = [], set()
    for e in etats:
        f, ech = e.get("fiche"), e.get("echeance")
        if e.get("type") != "match" or not f or ech is None or not (maintenant <= ech <= fin) or f in vus:
            continue
        chemin = Path(base) / f
        if not chemin.is_file():
            continue
        vus.add(f)
        m = re.search(r"^### Écran 1.*?(?=^## |\Z)", chemin.read_text(encoding="utf-8"), re.S | re.M)
        if m:
            blocs.append(f"### {e['evenement']} — échéance {ech:%d/%m %H:%M}\n\n" + m.group(0).strip())
    return ("## À saisir aujourd'hui\n\n" + "\n\n".join(blocs) + "\n") if blocs else ""


def joueurs_en_vente(rendu: str) -> list:
    """Noms des joueurs dont une ligne « vente : Prénom Nom (… » est au plan."""
    return sorted({m.strip() for m in re.findall(r"vente : ([^,(|]+?) \(", rendu)})


def fiches_avec_vendus(base, fichiers, vendus: list) -> list:
    """(fiche, nom) pour chaque joueur en vente qui a des minutes > 0 à l'Écran 2 d'une fiche."""
    import composition as comp
    res = []
    for f in sorted(set(fichiers)):
        chemin = Path(base) / f
        lue = comp.lire_fiche(chemin.read_text(encoding="utf-8")) if chemin.is_file() else None
        for c in (lue[0] if lue else []):
            joue = re.sub(r"\D", "", str(c[7])) not in ("", "0")
            if joue and any(v.lower().split()[-1] == str(c[0]).lower().split()[-1] for v in vendus):
                res.append((str(f), str(c[0])))
    return res


def que_faire(jour, plan: str, res: list, gardes: list, alerte, polices=(), saisie="") -> str:
    t = [f"# Que faire — BasketVibe — {jour:%d/%m/%Y}", "",
         "Propositions seulement : aucun achat, aucune vente, aucune enchère sans ton accord écrit (règle 2).", ""]
    if alerte:
        t += [f"🟥 {alerte}", ""]
    t += [statut_agents(res), ""]
    t += [f"- {l}" for l in non_lances(res)] + ([""] if non_lances(res) else [])
    if polices:
        n = sum(1 for r in polices if r["lance"])
        t += [f"Police : {n} lancée{'s' if n > 1 else ''} sur {len(polices)} (maximum > {_fr(SEUIL)}, fin dans {HORIZON_POLICE_H} h, "
              f"{POLICES_MAX} au plus) → police-{jour.isoformat()}.md", ""]
        t += [f"- {l}" for l in polices_non_lancees(polices)] + ([""] if polices_non_lancees(polices) else [])
    t += gardes + ([""] if gardes else [])
    t += [saisie] if saisie else []
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


# ---- Base indisponible (24/11) ----------------------------------------------------------------------------------------------
# Le 24/11 à 17:40, base saturée : 66 requêtes sur 66 en échec, et le passage --relance a écrasé le que-faire du matin.
# Désormais : plus de la moitié des requêtes en échec (sonde avant toute écriture, puis lecture du plan) → rien n'est écrasé
# (que-faire, briefs, instantané, outputs) ; une ligne 🟥 « base indisponible » en tête d'un fichier à part, puis sortie (code 2).
SONDES = ("select 1 as ok", "select count(*) as n from core.rafraichi_etat", "select max(id) as m from bronze.raw_pages")


def sonde_base(executer, sondes=SONDES):
    """Message d'échec si plus de la moitié des sondes échouent, sinon None. `executer(sql)` lève en cas d'échec."""
    import aujourdhui as auj
    erreurs = []
    for q in sondes:
        try:
            executer(q)
        except SystemExit as e:  # sql.py termine par sys.exit(message)
            erreurs.append(str(e))
        except Exception as e:  # noqa: BLE001
            erreurs.append(f"{type(e).__name__}: {e}")
    if auj.echec_massif(erreurs, len(sondes)):
        return f"{len(erreurs)} sondes sur {len(sondes)} en échec ({_derniere(erreurs[-1])})"
    return None


def fichier_indisponible(base, jour):
    return Path(base) / f"base-indisponible-{jour.isoformat()}.md"


# ---- Vues périmées (25/11) --------------------------------------------------------------------------------------------------
# Les 7 vues matérialisées sont rafraîchies ensemble, dans une seule transaction (core.rafraichir_vues) : elles ont toutes l'âge
# de core.rafraichi_etat.rafraichi_a. Une vue n'est périmée que si des pages sont arrivées depuis ce rafraîchissement (sinon elle
# est exacte, même vieille d'une nuit) et qu'il date de plus de PEREMPTION_H heures.
VUES_MAT = ("core.standing", "core.player_daily", "gold.match_objective", "gold.daily_alerts", "gold.bv_sell_candidates",
            "gold.bv_sell_replacement", "gold.bv_matchs_autres")
PEREMPTION_H = 3
SQL_FRAICHEUR = ("select rafraichi_a, last_page_id, (select max(id) from bronze.raw_pages) as max_page, now() as maintenant "
                 "from core.rafraichi_etat where id = 1")


def _instant(v):
    if v in (None, ""):
        return None
    return v if isinstance(v, dt.datetime) else dt.datetime.fromisoformat(str(v).replace("Z", "+00:00"))


def vues_perimees(executer, seuil_h=PEREMPTION_H, vues=VUES_MAT):
    """Message « vues périmées : vue âge, … » si des pages sont arrivées depuis le dernier rafraîchissement et qu'il a plus de
    `seuil_h` heures ; None sinon (lecture impossible comprise : la sonde de la base couvre déjà la panne)."""
    try:
        cols, lignes = executer(SQL_FRAICHEUR)
    except (SystemExit, Exception):  # noqa: BLE001
        return None
    if not lignes:
        return None
    r = dict(zip(cols, lignes[0]))
    raf, maint = _instant(r.get("rafraichi_a")), _instant(r.get("maintenant"))
    if r.get("last_page_id") is not None and r.get("max_page") is not None and int(r["last_page_id"]) >= int(r["max_page"]):
        return None
    if raf is not None and maint is not None and (maint - raf).total_seconds() <= seuil_h * 3600:
        return None
    if raf is None or maint is None:
        return "vues périmées : " + " · ".join(f"{v} âge inconnu" for v in vues) + " (aucun rafraîchissement réussi connu)"
    age = (maint - raf).total_seconds() / 3600
    from zoneinfo import ZoneInfo
    quand = raf.astimezone(ZoneInfo("Europe/Paris"))
    return ("vues périmées : " + " · ".join(f"{v} {age:.1f} h" for v in vues)
            + f" (dernier rafraîchissement le {quand:%d/%m à %H:%M}, pages arrivées depuis ; plafond {seuil_h} h)")


def sortie_base_indisponible(jour, maintenant, raison, base=None, commit=None, titre="base indisponible") -> int:
    """Écrit la ligne 🟥 en tête de base-indisponible-AAAA-MM-JJ.md (les lignes plus anciennes du jour restent dessous) ;
    ne touche à aucun autre fichier. `commit(fichiers)` (optionnel) ne pousse que ce fichier. Code retour 2.
    Une `raison` qui commence par « vues périmées » s'écrit telle quelle."""
    f = fichier_indisponible(BASE if base is None else base, jour)
    tete = raison if raison.startswith("vues périmées") else f"{titre} : {raison}"
    ligne = (f"🟥 {tete} (passage de {maintenant:%H:%M}) — que-faire, briefs et outputs du jour "
             f"inchangés ; aucun agent lancé.")
    ancien = f.read_text(encoding="utf-8") if f.is_file() else ""
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(ligne + "\n" + ancien, encoding="utf-8")
    print(ligne)
    if commit:
        ok, msg = commit([str(f.relative_to(RACINE)) if f.is_relative_to(RACINE) else str(f)])
        print(f"git : {msg}")
    return 2


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
    return jour, maintenant, rendu, etats, S, alerte, cfg, (donnees, erreurs, n, fait)


def passage_police(ctx, jour, maintenant, S, rendu, refus=None, lancer=None, plan_cands=None):
    """(rendu annoté, résultats police) : candidats > SEUIL finissant dans 36 h → lancer_polices ; si une police a tourné, le
    plan est rendu de nouveau (la trace du jour lève « police d'abord ») et l'instantané réécrit ; puis annoter()."""
    import aujourdhui as auj
    import aujourdhui_sources as src
    donnees, erreurs, n, fait = ctx
    cands = candidats_police(S.get("cibles", []), auj.lignes_de(donnees, "gold.bv_market_bargains"), maintenant)
    vus = {c["nom"].lower() for c in cands}  # 19/11 : + lignes d'offres et de vente du plan au-dessus du seuil
    cands += [c for c in (plan_cands if plan_cands is not None else candidats_plan(donnees, S, maintenant)) if c["nom"].lower() not in vus]
    if not cands:
        return rendu, []
    if refus:
        return rendu, [dict(c, lance=False, raison=refus, heure=None) for c in cands]
    res = (lancer or lancer_polices)(cands, jour)
    if any(r["lance"] for r in res):
        S = auj.lire_sources(donnees, jour)
        _, rendu = auj.rendre_jour(auj.plan(donnees, erreurs, jour, maintenant, fait, S), donnees, erreurs, jour, maintenant, S, fait=fait)
        auj.ecrire_instantane(BASE / f"aujourdhui-{jour.isoformat()}.md",
                              f"<!-- généré le {maintenant:%Y-%m-%d %H:%M} -->\n{rendu}\n", erreurs, n)
    m = next((r for r in auj.lignes_de(donnees, "gold.bv_exports_state") if r.get("ecran") == "Marché (enchères)"), {})
    return annoter(rendu, res, src.lire_police(BASE, jour), _date(m.get("dernier_paris")), maintenant), res


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--sans-agents", action="store_true", help="calcule les agents prévus sans les lancer")
    ap.add_argument("--sans-git", action="store_true", help="n'écrit ni commit ni push")
    ap.add_argument("--relance", action="store_true", help="second passage : seulement les agents dont le prérequis est arrivé depuis le dernier passage")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    import aujourdhui_sources as src
    import etat_jour as ej
    base_sha = None
    if not a.sans_git:
        base_sha, msg = restaurer()
        print(msg)
    import aujourdhui as auj0
    commit = None if a.sans_git else (lambda fs: commit_push(fs, auj0.heure_paris_naive().date(), base_sha=base_sha))
    h0 = auj0.heure_paris_naive()
    executer = auj0.charger_sql().executer
    panne = sonde_base(executer) or vues_perimees(executer)  # avant toute écriture (étiquettes, instantané, que-faire)
    if panne:
        return sortie_base_indisponible(h0.date(), h0, panne, commit=commit)
    depuis = horodatage_passage(BASE, h0.date()) if a.relance else None  # avant que rejouer() réécrive l'instantané
    print(etiqueter_experiences())  # avant le plan : le niveau du prochain amical suit l'étiquette écrite
    jour, maintenant, rendu, etats, S, alerte, cfg, ctx = rejouer()
    if alerte:  # échec massif des lectures du plan : rien n'est écrasé
        return sortie_base_indisponible(jour, maintenant, alerte, commit=commit)
    prevus = ej.agents_a_lancer(etats, cfg, BASE, jour)
    if a.relance:
        prevus = filtrer_relance(prevus, etats, depuis)
    if alerte or a.sans_agents:
        raison = alerte or "passage sans agents (--sans-agents)"
        res = [dict(e, statut="refus", raison=raison) if e["statut"] == "a_lancer" else e for e in prevus]
    else:
        res = lancer_tous(prevus, jour, timeout_min=cfg.get("agent_timeout_min", 15), vendus=joueurs_en_vente(rendu))
        if any(e.get("lance") for e in res):  # les fiches viennent d'être écrites : relire les états
            etats = ej.lignes(ej.construire(ctx[0], S, BASE, jour, maintenant, cfg), cfg, maintenant)
    rendu, polices = passage_police(ctx, jour, maintenant, S, rendu,
                                    refus=alerte or ("passage sans agents (--sans-agents)" if a.sans_agents else None))
    sorties = "\n".join((BASE / e["sortie"]).read_text(encoding="utf-8") for e in res if (BASE / e["sortie"]).is_file())
    gardes = garde_fous(rendu + "\n" + sorties, src.lire_police(BASE, jour))
    f = BASE / f"que-faire-{jour.isoformat()}.md"
    gardes += [f"🟥 Composition : la fiche {x} fait jouer {n}, dont la vente est proposée au plan — retire-le de la fiche"
               for x, n in fiches_avec_vendus(BASE, [e["fiche"] for e in etats if e.get("fiche")], joueurs_en_vente(rendu))]
    import liens  # 25/11 : tout fichier cité est un lien complet sur main
    f.write_text(liens.lier(que_faire(jour, rendu, res, gardes, alerte, polices, a_saisir(etats, maintenant))), encoding="utf-8")
    print(statut_agents(res))
    for l in lignes_composition(rendu):
        print(l)
    for l in non_lances(res) + polices_non_lancees(polices):
        print(l)
    code = 2 if alerte else 0
    if not a.sans_git:
        ok, msg = commit_push(["outputs"], jour, base_sha=base_sha)
        print(f"git : {msg}")
        code = code or (0 if ok else 1)
    return code


if __name__ == "__main__":
    sys.exit(main())
