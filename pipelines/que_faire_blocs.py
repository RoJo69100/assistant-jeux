"""Le « que faire » BasketVibe en 11 blocs (étape 5n), gabarit : docs/attentes/gabarit-que-faire-basketvibe.md.

Plan : docs/refonte-v3/plan-5n-que-faire.md. Ce module range les actions de aujourdhui.plan() dans les blocs 0 à 10
et rend le document. Règle commune : un bloc vide s'écrit « donnée manquante : exporte <écran> », jamais une commande.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import forme  # noqa: E402

# Mots entiers qui sont une commande à l'utilisateur ; un participe (« lancée dans ce passage ») n'en est pas une.
INTERDITS = re.compile(r"(?<!\w)(?:lance|relance|exécute|lancer|relancer|exécuter|python)(?!\w)|pipelines/", re.IGNORECASE)

# Consignes destinées à Claude (pas à l'utilisateur) : elles sortent de l'affichage.
CONSIGNE = re.compile(r"(?:lance|relance|lancer|relancer) l'agent|python -I", re.IGNORECASE)

# Catégories de forme.CATEGORIES (sans accents) -> texte affiché.
AFFICHAGE = {"composition": "Composition", "tactique": "Tactique", "entrainement": "Entraînement", "transferts": "Transferts",
             "academie/draft": "Académie/Draft", "finances": "Finances", "export": "Export", "question": "Question",
             "analyse": "Analyse"}
assert set(AFFICHAGE) == set(forme.CATEGORIES)

# « il me manque <vue> (<erreur>) — export <écran> » : le bloc se déduit de l'écran demandé.
MANQUE_ECRAN = [("Finances", 8, "finances"), ("Marché", 4, "transferts"), ("Personnel", 9, "finances"),
                ("Académie", 9, "academie/draft"), ("Entraînement", 9, "entrainement"),
                ("page du dernier match", 7, "analyse")]

# (motif, bloc, catégorie) : première règle qui correspond au début du texte (ou à la forme indiquée) ; ordre = priorité.
REGLES = [
    (r"Entraînement \(", 9, "entrainement"),
    (r"Composition : minutes aux jeunes", 2, "composition"),
    (r"Composition ", 3, "composition"),
    (r"Réexporte l'aperçu", 0, "export"),
    (r"rejeu non disponible", 0, "export"),
    (r"Analyse : ", 7, "analyse"),
    (r"Finances : ", 8, "finances"),
    (r"Réduis le poste", 8, "finances"),
    (r"Semaine type déficitaire", 8, "finances"),
    (r"Vendre ", 4, "transferts"),
    (r"Mets .+ en vente", 4, "transferts"),
    (r"Enchère (?:sur|maximale) ", 4, "transferts"),
    (r"Acheter un ", 4, "transferts"),
    (r"Académie, rapport", 9, "academie/draft"),
    (r"Boucle d'apprentissage", 7, "analyse"),
    (r"Conseil \S+ à juger", 7, "analyse"),
    (r"Revue de la semaine", 7, "analyse"),
    (r"Amical contre ", 2, "composition"),
    (r"(?:Ligue|Coupe) ", 3, "composition"),
    (r"Sors ", 3, "composition"),
    (r"[^:]{1,80} : corrige à l'écran \S+ réglages", 3, "composition"),
    (r".+ blessé, retour le", 3, "composition"),
    (r".+ : fatigue \d", 3, "composition"),
    (r".+ : forme \d", 3, "composition"),
    (r"Match de ligue joué non exporté", 0, "export"),
    # actions de gold.bv_agenda
    (r"Avant .+? : preset amical", 2, "composition"),
    (r"Avant .+? : vérifier le preset de ligue", 3, "composition"),
    (r"Avant .+? : vérifier et sauvegarder les choix d'entraînement", 9, "entrainement"),
    (r"(?:Avant|Après) .+ : exporter ", 0, "export"),
]


def manque(export: str, debloque: str = "") -> str:
    """Ligne d'un bloc vide : « donnée manquante : exporte <écran> » (+ « (<ce que ça débloque>) »)."""
    return f"donnée manquante : exporte {export}" + (f" ({debloque})" if debloque else "")


def classer(action: str) -> tuple:
    """(numéro de bloc, catégorie affichée) d'après le début du texte d'une action de aujourdhui.plan()."""
    texte = action.strip()
    if texte.startswith("il me manque"):
        ecran = texte.rsplit("export ", 1)[-1]
        for mot, bloc, cat in MANQUE_ECRAN:
            if mot.lower() in ecran.lower():
                return bloc, AFFICHAGE[cat]
        return 0, AFFICHAGE["export"]
    for motif, bloc, cat in REGLES:
        if re.match(motif, texte):
            return bloc, AFFICHAGE[cat]
    return 10, AFFICHAGE["question"]


def separer(actions: list) -> tuple:
    """(actions affichables, consignes de session).

    Une action (limite, prio, action, détail, source) dont le texte est une consigne à Claude (« lance l'agent … »,
    « python -I … ») sort de l'affichage et va dans les consignes. Si seul le détail en contient une, l'action reste
    affichée avec un détail vide et le détail va dans les consignes."""
    affichables, consignes = [], []
    for a in actions:
        limite, prio, texte, detail, source = a
        if CONSIGNE.search(texte):
            consignes.append(texte + (f" — {detail}" if detail else ""))
        elif detail and CONSIGNE.search(detail):
            consignes.append(detail)
            affichables.append((limite, prio, texte, "", source))
        else:
            affichables.append(a)
    return affichables, consignes
