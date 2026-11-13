"""Saisie de composition d'un match BasketVibe, prête à saisir (étape 5j, Y1).

Usage : python -I pipelines/composition.py "<adversaire>"
Source : le dernier brief tactique valide pour ce match (outputs/basketvibe/briefs/AAAA-MM-JJ-tactique[-amical].md :
type du match, adversaire nommé dans le titre, tableau de saisie et tableau des adversaires). Rien n'est inventé :
sans fiche valide, « aucune fiche : lance l'agent tactique ».
Amical : le réglage du test en cours (docs/attentes/experiences-amicales-basketvibe.yaml) remplace celui du brief
(agressivité) et les valeurs constantes de l'expérience (zone, focus défensif) sont nommées « constant pendant E<n> »
sous le tableau, pour que les tableaux restent valables pour pipelines/forme.py.
Ordre de l'écran : PG, SG, SF, PF, C puis nom (gold.bv_saisie_adversaires, forme.py, attente R-10).
"""
import datetime as dt
import re
import sys
from pathlib import Path

DOSSIER = Path(__file__).resolve().parent
sys.path.insert(0, str(DOSSIER))
import aujourdhui as auj  # noqa: E402
import forme  # noqa: E402

src = auj.src
BASE = DOSSIER.parent / "outputs" / "basketvibe"
POSTES = ["pg", "sg", "sf", "pf", "c"]
ENTETE = ["Joueur", "Poste", "Q1", "Q2", "Q3", "Q4", "Prol.", "Minutes", "Off. focus", "Rôle", "Tir", "Agress."]
CLES = ["joueur", "poste", "q1", "q2", "q3", "q4", "prol", "min", "off", "role", "tir", "agress"]
ENTETE_ADV = ["Adversaire", "Poste", "Focus défensif (1-5)", "Zone"]
FOCUS = {1: "Give up", 2: "Light", 3: "Normal", 4: "Intense", 5: "Lock"}
ZONE = re.compile(r"\b(Rim|Middle|Perimeter)\b")
AUCUNE = "aucune fiche : lance l'agent tactique"


def adversaire_du_titre(titre: str):
    m = re.search(r"contre ([^,(]+)", titre) or re.search(r"J\d+ : ([^(,]+)", titre)
    return m.group(1).strip() if m else None


def brief_pour(base, jour, adversaire, amical):
    """(date, chemin, texte) du brief le plus récent du type demandé, daté d'au plus `jour`, qui nomme l'adversaire."""
    trouves = []
    for f in (Path(base) / "briefs").glob("*.md"):
        m = src.BRIEF.match(f.name)
        if not m or (m.group(2) == "-amical") != amical or Path(f).stat().st_size == 0:
            continue
        date = dt.date.fromisoformat(m.group(1))
        if date > jour:
            continue
        texte = f.read_text(encoding="utf-8")
        if auj.meme_match(adversaire_du_titre(texte.splitlines()[0]) if texte else None, adversaire):
            trouves.append((date, f, texte))
    return max(trouves, key=lambda x: x[0]) if trouves else None


def _cellule(c: str) -> str:
    return c.replace("*", "").strip()


def lire_fiche(texte: str):
    """(joueurs, adversaires) lus dans le brief, ou None si l'un des deux tableaux manque.
    joueurs : une liste de 12 cellules (ENTETE) ; adversaires : [nom, poste, focus 1-5, zone]."""
    joueurs, adversaires = None, None
    for cols, lignes in forme.tableaux(texte):
        if not cols:
            continue
        if joueurs is None and cols[0] == "joueur" and forme.idx(cols, "q1") >= 0:
            ix = [forme.idx(cols, k) for k in CLES]
            if min(ix) >= 0:
                joueurs = [[_cellule(l[i]) if i < len(l) else "" for i in ix] for l in lignes if len(l) > max(ix)]
        elif "adversaire" in cols[0] and forme.idx(cols, "focus") >= 0:
            ip, ifo, iz = forme.idx(cols, "poste"), forme.idx(cols, "focus"), forme.idx(cols, "zone")
            lus = []
            for l in lignes:
                f = re.match(r"\s*(\d)", _cellule(l[ifo])) if ifo < len(l) else None
                if not f or ip < 0 or "tous" in forme.norm(l[0]):
                    continue  # ligne de remplacement (« tous les joueurs ») ou focus illisible
                z = ZONE.search(l[iz]) if 0 <= iz < len(l) else None
                lus.append([_cellule(l[0]), _cellule(l[ip]), int(f.group(1)), z.group(1) if z else None])
            if lus:
                adversaires = lus  # le dernier tableau valide l'emporte (focus réel après l'aperçu)
    if adversaires:
        zones = re.findall(r"Zone (Rim|Middle|Perimeter)\b", texte)
        for a in adversaires:
            a[3] = a[3] or (zones[-1] if zones else None)
    if not joueurs or not adversaires or any(a[3] is None for a in adversaires):
        return None
    return joueurs, adversaires


def _rang(poste: str, nom: str):
    p = forme.norm(poste).split("/")[0].strip()
    return (POSTES.index(p) if p in POSTES else 9, forme.norm(nom))


def tableau(entete, lignes) -> str:
    return "\n".join(["| " + " | ".join(entete) + " |", "|" + "---|" * len(entete)] + ["| " + " | ".join(str(c) for c in l) + " |" for l in lignes])


def composer(adversaire, base, jour, amical, test=None) -> str:
    """Texte de la saisie ; `test` = (expérience, niveau, saisi) de aujourdhui.test_en_cours pour un amical."""
    b = brief_pour(base, jour, adversaire, amical)
    fiche = lire_fiche(b[2]) if b else None
    if not fiche:
        return AUCUNE
    return _saisie(b, fiche, amical, test)


def composer_amical(brief_du_jour, test=None):
    """5n T3 : tableau de saisie lu dans le brief tactique d'amical qu'on lui donne (celui du jour, choisi par l'appelant) ;
    None si le brief est absent, n'est pas un brief d'amical (`AAAA-MM-JJ-tactique-amical.md`) ou n'a pas de tableaux valides.
    Ne lit jamais le dernier amical joué ni un brief d'un autre jour : il ne lit que le fichier reçu."""
    if brief_du_jour is None:
        return None
    f = Path(brief_du_jour)
    m = src.BRIEF.match(f.name)
    if not m or m.group(2) != "-amical" or not f.is_file() or f.stat().st_size == 0:
        return None
    texte = f.read_text(encoding="utf-8")
    fiche = lire_fiche(texte)
    return _saisie((dt.date.fromisoformat(m.group(1)), f, texte), fiche, True, test) if fiche else None


def composer_fiche(fichier):
    """Phase 0 : tableau de saisie de ligue ou de coupe lu dans le brief qu'on lui donne (fiche de la veille pour ce même match) ;
    None si le fichier n'est pas un brief daté de ligue ou de coupe ou n'a pas de tableaux valides. Ne cherche aucun autre brief."""
    f = Path(fichier)
    m = src.BRIEF.match(f.name)
    if not m or m.group(2) == "-amical" or not f.is_file() or f.stat().st_size == 0:
        return None
    texte = f.read_text(encoding="utf-8")
    fiche = lire_fiche(texte)
    return _saisie((dt.date.fromisoformat(m.group(1)), f, texte), fiche, False, None) if fiche else None


def _saisie(b, fiche, amical, test):
    joueurs, adv = fiche
    notes = []
    if amical and test:
        e, niveau, _ = test
        cran = ((e.get("joue") or {}).get(niveau) or {}).get("agress_cran")
        if cran is not None:
            for j in joueurs:
                j[11] = str(cran + 1)
            notes.append(f"agressivité {cran + 1} à l'écran sur tous les joueurs : réglage du test {e['id']} niveau {niveau}, "
                         "à la place de celui du brief")
        cst = e.get("constants") or {}
        zone_test = ((e.get("zone") or {}).get(niveau))
        zone, focus = cst.get("zone") or zone_test, cst.get("focus")
        if zone:
            for a in adv:
                a[3] = zone
        if focus:
            for a in adv:
                a[2] = int(focus)
        morceaux = []
        if zone:
            morceaux.append(f"zone {zone}" + (f" : constant pendant {e['id']}" if cst.get("zone") else f" : réglage du test {e['id']} niveau {niveau}"))
        if focus:
            morceaux.append(f"focus défensif {int(focus)} ({FOCUS[int(focus)]}) : constant pendant {e['id']}")
        if morceaux:
            notes.append(" ; ".join(morceaux))
    joueurs.sort(key=lambda j: _rang(j[1], j[0]))
    adv.sort(key=lambda a: _rang(a[1], a[0]))
    sortie = [f"Fiche : briefs/{b[1].name} (brief du {b[0]:%d/%m}).", "", tableau(ENTETE, joueurs), "",
              tableau(ENTETE_ADV, adv)]
    if notes:
        sortie += [""] + notes
    return "\n".join(sortie)


def main() -> int:
    if len(sys.argv) < 2:
        sys.exit('usage : python -I pipelines/composition.py "<adversaire>"')
    adversaire = sys.argv[1]
    sys.stdout.reconfigure(encoding="utf-8")
    jour = auj.heure_paris_naive().date()
    donnees, genre, test = {}, None, None
    try:
        sqlmod = auj.charger_sql()
        for k in ("calendrier", "amical_reglage"):
            donnees[k] = sqlmod.executer(auj.REQUETES[k])
        for r in auj.lignes_de(donnees, "calendrier"):
            if auj.en_date(r["day"]) >= jour and auj.meme_match(r["opponent"], adversaire):
                genre = r["competition_kind"]
                if genre == "amical":
                    v = r.get("verrou_paris") or r.get("coup_envoi_paris")
                    am = {"match": r["opponent"], "date": auj.en_date(r["day"]), "limite": auj.en_heure(v) if v else None}
                    test = auj.test_en_cours(src.lire_experiences(BASE, jour), am, auj.lignes_de(donnees, "amical_reglage"))
                break
    except Exception as e:  # noqa: BLE001 - base illisible : on compose sans le test et on le dit
        print(f"il me manque calendrier ({str(e)[:60]}) : réglage du test non appliqué, type de match deviné d'après les briefs")
    for amical in ([genre == "amical"] if genre else [False, True]):
        texte = composer(adversaire, BASE, jour, amical, test)
        if texte != AUCUNE or genre:
            print(texte)
            return 0
    print(AUCUNE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
