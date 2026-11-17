"""Parité du plan du 17/11 (P2, suppression de l'ancien Bloc 0 et de l'ancien tableau « Aujourd'hui / Demain » du Bloc 1).

Fixture figée : pipelines/jeu_essai/2026-11-17/plan-avant-suppression-bloc-0-1.md = la sortie réelle de `aujourdhui.py basketvibe`
du 17/11 11:15 (après lancement des 2 agents tactique), avec la section d'état ET les anciens blocs 0 et 1. Chaque ligne des anciens
blocs doit : (a) avoir une ligne équivalente dans la section d'état (motif cherché dans la section), ou (b) porter une RAISON de
suppression écrite ci-dessous. Une ligne sans règle fait échouer le test.
"""
import re
import sys
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent / "jeu_essai" / "2026-11-17" / "plan-avant-suppression-bloc-0-1.md"

# (motif de l'ancienne ligne, "etat", motif de la ligne de la section d'état) ou (motif, "raison", texte de la raison)
REGLES = [
    (r"Page du match contre Opper Cards \(10/11\)", "raison",
     "match du 10/11 hors de la fenêtre de 7 jours de la section d'état (jours_non_analyses) ; le détail manquant (box, quarts, play-by-play) reste une demande d'étude des blocs 6 et 7"),
    (r"export à faire : Équipe \(aperçu, joueurs\)", "raison",
     "cet export ne débloque aucune transition d'un événement (P2.2 : un export n'est demandé que s'il débloque une transition) ; la fiche lit la base, pas la page"),
    (r"export à faire : Tactique \(", "raison",
     "cet export ne débloque aucune transition d'un événement (P2.2) ; la saisie du match est contrôlée contre la fiche par la section d'état"),
    (r"export à faire : Amical : tactique du match", "raison",
     "config amical : jamais d'aperçu ni d'export avant le match ; l'export de la page de l'amical n'est demandé qu'après le match (transition « joue »)"),
    (r"export à faire : le Marché|Marché : 0 capture", "raison",
     "décision : pas de ligne de fraîcheur du Marché ; aucune enchère n'est suivie (aucune cible), donc aucun événement n'en dépend ; le bloc 4 « Qui acheter » donne la date et le nombre d'annonces de l'export"),
    (r"export à faire : Personnel", "raison",
     "décision : pas de ligne de fraîcheur du Personnel ; aucune décision n'en dépend (règle de personnel non tranchée, bloc 10)"),
    (r"export à faire : historique global des transferts", "raison",
     "décision : pas de ligne ; l'historique alimente la table des prix du bloc 4, il ne débloque aucune transition d'événement"),
    (r"export à faire : l'aperçu du match de ligue du 18/11", "etat", r"exporte l'aperçu du match de ligue contre C\.B\.Granada"),
    (r"export à faire : la page du match →", "etat", r"exporte la page du match amical contre Union Heidelberg"),
    (r"Académie, rapport du 12/11 : .+ : tester", "etat", r"décision attendue : tester 3 prospects \(75 000\)"),
    (r"Boucle d'apprentissage", "etat", r"juge les décisions à mesurer"),
    (r"Amical contre Union Heidelberg \(mer\. 18/11\) : saisis le test E1", "etat",
     r"saisis et sauvegarde l'écran du match amical contre Union Heidelberg"),
    (r"Amical contre BG Bangers \(19/11\)", "etat", r"saisis et sauvegarde l'écran du match amical contre BG Bangers"),
    (r"point \d de l'analyste", "raison",
     "consigne 3 du 17/11 : le brief analyste est une entrée de l'agent tactique du match suivant, rien d'autre ; plus de ligne de plan dédiée"),
    (r"Composition : Ligue J8 contre C\.B\.Granada", "etat", r"exporte l'aperçu du match de ligue contre C\.B\.Granada"),
]


def sections(texte: str) -> dict:
    res, cle = {}, None
    for l in texte.splitlines():
        m = re.match(r"^## (Aujourd'hui — état par événement|Bloc (\d+)) ", l + " ")
        if m:
            cle = "etat" if m.group(2) is None else int(m.group(2))
            res[cle] = []
        elif cle is not None:
            res[cle].append(l)
    return res


def anciennes_lignes(s: dict) -> list:
    b0 = [l for l in s[0] if l.startswith("- ")]
    b1 = [l for l in s[1] if l.startswith("| ") and not l.startswith("| Priorité")]
    return b0 + b1


def cas_parite():
    s = sections(FIXTURE.read_text(encoding="utf-8"))
    etat = "\n".join(s["etat"])
    anciennes = anciennes_lignes(s)
    yield "parité : la fixture contient les anciens blocs 0 et 1 (au moins 15 lignes)", len(anciennes) >= 15
    for l in anciennes:
        regle = next((r for r in REGLES if re.search(r[0], l)), None)
        yield f"parité : une règle pour « {l[:70]} »", regle is not None
        if regle and regle[1] == "etat":
            yield f"parité : ligne équivalente dans la section d'état pour « {l[:60]} »", re.search(regle[2], etat) is not None
        elif regle:
            yield f"parité : raison de suppression écrite pour « {l[:60]} »", len(regle[2]) >= 40
    yield "parité : toute règle sert au moins une ancienne ligne", all(any(re.search(r[0], l) for l in anciennes) for r in REGLES)


def cas_plan_reel():
    """Le plan réel n'a plus ni bloc 0 ni bloc 1, garde la section d'état et les blocs 2 à 10 (rendu par que_faire_blocs)."""
    import que_faire_blocs as qfb
    yield "plan : TITRES garde ses 11 titres, dont les blocs 2 à 10", len(qfb.TITRES) == 11
    for nom in ("bloc_0", "bloc_1", "complements_bloc_1", "fautes_bloc_1"):
        yield f"plan : {nom} supprimé", not hasattr(qfb, nom)
    yield "plan : plus de lecture des points de l'analyste", not hasattr(qfb.auj.src, "lire_points_analyste")


CAS = [cas_parite, cas_plan_reel]

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    sys.stdout.reconfigure(encoding="utf-8")
    echecs = 0
    jeux = [r for c in CAS for r in c()]
    for nom, ok in jeux:
        echecs += not ok
        print(("OK " if ok else "ECHEC "), nom)
    print(f"{len(jeux) - echecs}/{len(jeux)}")
    sys.exit(1 if echecs else 0)
