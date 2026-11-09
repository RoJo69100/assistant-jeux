"""Lecteurs de fichiers de `aujourdhui.py` (BasketVibe) : le travail déjà fait dans la journée, sans modèle ni agent.

Chaque fonction lit `base` (= outputs/basketvibe, ou un jeu d'essai de même forme) et rend des dictionnaires ;
aucune n'écrit. Critères L1 à L4 de docs/refonte-v3/journal-aujourdhui.md.
  lire_tactique   L1  briefs `<jour>-tactique.md` et `-tactique-amical.md` : match, verrou, tests « Faux si »
  lire_restes     L3  lignes « reste à corriger / à faire » du registre `fait-<jour>.md`, un réglage par couple
  lire_cibles     L2  décisions d'achat ouvertes (learn.decision) + fin d'enchère en base + dossier + police
  lire_conseils   L4  conseils ouverts de learnings.md dont la date du critère tombe aujourd'hui ou demain
"""
import datetime as dt
import re
from pathlib import Path

BRIEF = re.compile(r"^(\d{4}-\d{2}-\d{2})-tactique(-amical)?\.md$")
SEUIL_VIEUX = 3  # jours : un brief plus ancien pour un match du jour est signalé (skill, étape 3)
JOURS = ["lun.", "mar.", "mer.", "jeu.", "ven.", "sam.", "dim."]
CLAUSE = re.compile(r"([A-Za-zÉé]+\.?\s?\d)\s+pour\s+(.+?)(?=,\s*[A-Za-zÉé]+\.?\s?\d\s+pour|\s*$)")
CIBLE = re.compile(r"([^\s,;()]+)\s+(PG|SG|SF|PF|C)\s+\(max\s+([\d\s  ]+?)\)")
DATE_JM = re.compile(r"\b(\d{2})/(\d{2})\b")


def _jm(jour: dt.date, j: str, m: str) -> dt.date:
    return dt.date(jour.year, int(m), int(j))


def _nettoie(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"\*\*|`", "", s)).strip()


def dernier_brief(base, jour: dt.date, amical: bool):
    """(date, chemin) du brief le plus récent du type demandé, daté d'au plus `jour` ; None s'il n'y en a pas."""
    trouves = []
    for f in (Path(base) / "briefs").glob("*.md"):
        m = BRIEF.match(f.name)
        if m and bool(m.group(2)) == amical and dt.date.fromisoformat(m.group(1)) <= jour:
            trouves.append((dt.date.fromisoformat(m.group(1)), f))
    return max(trouves, key=lambda x: x[0]) if trouves else None


def preuves(texte: str) -> list[str]:
    """Tests « prouvera que j'avais tort » : puces « Test » de la section Prouvera, puis phrases « Faux si »."""
    res = []
    sec = re.search(r"^#+\s*(?:\d+\.\s*)?Prouvera[^\n]*\n(.*?)(?=^#|\Z)", texte, re.S | re.M)
    if sec:
        for l in sec.group(1).splitlines():
            l = l.strip()
            if l.startswith("- Test") and "voir ci-dessus" not in l:
                res.append(_nettoie(l[2:]))
    for f in re.finditer(r"Faux si.*?(?:\.(?=\s|$))", texte, re.S):
        p = _nettoie(f.group(0))
        if p not in res:
            res.append(p)
    return res


def lire_tactique(base, jour: dt.date) -> list[dict]:
    """Un dict par match à venir : type, match, date, verrou, preuves, fichier, age (jours), vieux."""
    res = []
    for amical in (False, True):
        b = dernier_brief(base, jour, amical)
        if not b:
            continue
        date_brief, f = b
        texte = f.read_text(encoding="utf-8")
        titre = texte.splitlines()[0] if texte else ""
        v = re.search(r"verrou (\d{2}:\d{2})", titre) or re.search(r"(\d{2}:\d{2}) \(verrou\)", titre)
        d = DATE_JM.search(titre)
        date = _jm(jour, d.group(1), d.group(2)) if d else None
        if date and date < jour:
            continue  # match déjà joué
        m = re.search(r"contre ([^,]+)", titre) if amical else re.search(r"J\d+ : ([^(,]+)", titre)
        manche = re.search(r"\b(J\d+)\b", titre)
        age = (jour - date_brief).days
        res.append({
            "type": "amical" if amical else "ligue", "match": (m.group(1).strip() if m else "match inconnu"),
            "manche": manche.group(1) if manche and not amical else None,
            "lieu": "domicile" if re.search(r"domicile", titre, re.I) else "extérieur" if re.search(r"ext[ée]rieur", titre, re.I) else None,
            "date": date, "verrou": v.group(1) if v else None, "preuves": preuves(texte),
            "fichier": f"briefs/{f.name}", "age": age, "vieux": age > SEUIL_VIEUX,
        })
    return res


def lire_restes(base, jour: dt.date) -> list[dict]:
    """Lignes du registre qui disent « reste à corriger / à faire » : une action, jamais seulement « déjà fait »."""
    f = Path(base) / f"fait-{jour.isoformat()}.md"
    if not f.exists():
        return []
    res = []
    for l in f.read_text(encoding="utf-8").splitlines():
        m = re.search(r"reste à (?:corriger|faire)[^:]*:\s*(.+?)\s*$", l, re.I)
        if not m:
            continue
        reglages = []
        for c in CLAUSE.finditer(m.group(1)):
            for nom in re.split(r",\s*|\s+et\s+", c.group(2).rstrip(". ")):
                reglages.append((c.group(1).strip(), nom.strip()))
        quand = re.search(r"\((\d{2})/(\d{2}) (\d{2}:\d{2})\)", l)
        adv = re.search(r"contre ([^(—]+?)\s*(?:\(|—|$)", l)
        res.append({
            "match": adv.group(1).strip() if adv else None,
            "date": _jm(jour, quand.group(1), quand.group(2)) if quand else None,
            "heure": quand.group(3) if quand else None,
            "reglages": reglages, "texte": m.group(1), "fichier": f.name,
        })
    return res


SAISIE = re.compile(r"\bdu (\d{2})/(\d{2}) contre ([^(—\n]+?)\s*(?:\(|—|$)", re.I)


def lire_saisies(base, jour: dt.date) -> list[dict]:
    """Saisies de match à venir déclarées dans n'importe quel registre `fait-<j>.md` daté d'au plus `jour` (critère PB5) :
    une ligne « saisie … du JJ/MM contre <adversaire> » dont la date est celle d'aujourd'hui ou plus tard."""
    res = []
    for f in sorted(Path(base).glob("fait-*.md")):
        m = re.match(r"^fait-(\d{4}-\d{2}-\d{2})\.md$", f.name)
        if not m or dt.date.fromisoformat(m.group(1)) > jour:
            continue
        for l in f.read_text(encoding="utf-8").splitlines():
            if not re.search(r"\bsaisi", l, re.I) or re.search(r"reste à", l, re.I):
                continue
            s = SAISIE.search(l)
            if not s:
                continue
            date = _jm(jour, s.group(1), s.group(2))
            if date >= jour:
                res.append({"match": s.group(3).strip(), "date": date, "fichier": f.name})
    return res


def lire_cibles(decisions: list[dict], encheres: list[dict], base, jour: dt.date) -> list[dict]:
    """Une cible par « Nom POSTE (max N) » des décisions d'achat ouvertes ; fin d'enchère lue dans `encheres`."""
    base = Path(base)
    police = (base / f"police-{jour.isoformat()}.md").exists()
    dossier = (base / "dossier" / f"{jour.isoformat()}-achat.md").exists()
    res = []
    for dec in decisions:
        for nom, poste, montant in CIBLE.findall(str(dec.get("label", ""))):
            fin = None
            for e in encheres:
                if nom.lower() in str(e.get("name", "")).lower():
                    fin = dt.datetime.fromisoformat(str(e["fin_paris"])[:19])
            res.append({"nom": nom, "poste": poste, "max": int(re.sub(r"\D", "", montant)), "fin": fin,
                        "decision": dec.get("id"), "police": police, "dossier": dossier,
                        "raison": str(dec.get("hypothesis", ""))})
    return res


def lire_conseils(base, jour: dt.date) -> list[dict]:
    """Conseils « ouvert » de learnings.md dont la dernière date du critère est aujourd'hui ou demain."""
    f = Path(base) / "learnings.md"
    if not f.exists():
        return []
    res = []
    for l in f.read_text(encoding="utf-8").splitlines():
        if not re.match(r"\| C-\d+", l):
            continue
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) < 5 or not c[4].lower().startswith("ouvert"):
            continue
        dates = [_jm(jour, j, m) for j, m in DATE_JM.findall(c[3]) if 1 <= int(m) <= 12 and 1 <= int(j) <= 31]
        if dates and jour <= max(dates) <= jour + dt.timedelta(days=1):
            res.append({"id": c[0], "conseil": _nettoie(c[2]), "echeance": max(dates)})
    return res
