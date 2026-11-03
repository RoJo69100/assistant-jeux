"""Hook SessionStart : met dans le contexte les TITRES des règles actives (docs/regles/actives.md) et le rappel de décision.

Refonte v2 (0.3-D, 2026-11-03) : l'ancienne version imprimait G1-G12 et 12 règles apprises en entier (~1 500 tokens).
Ici, seul le déclencheur de chaque règle est imprimé ; le texte complet est dans actives.md, lu à la demande.
Les 3 exports les plus en retard viendront de `gold.sante_collecte` quand `pipelines/sql.py` existera (0.4).
"""
import io
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
ACTIVES = RACINE / "docs" / "regles" / "actives.md"
LONGUEUR_TITRE = 48


def titres():
    if not ACTIVES.exists():
        return ["(docs/regles/actives.md introuvable : le lire à la main)"]
    sortie = []
    for ligne in ACTIVES.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^([KE]\d+)\. (Quand .*?)(?: →|$)", ligne)
        if m:
            sortie.append(f"{m.group(1)} {m.group(2)[:LONGUEUR_TITRE]}")
    return sortie


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    print("RAPPEL DE DÉBUT DE SESSION (pipelines/rappel_debut.py)")
    print("Décision (achat, vente, enchère, composition, défaite, entraînement, académie, finances) : "
          "`python pipelines/dossier.py <jeu> <type>` AVANT de répondre.")
    print("MCP Supabase : essayer une requête avant d'écrire « pas de base » ; non authentifié = "
          "à autoriser dans les connecteurs claude.ai, pas une panne.")
    print("Règles actives (texte complet : docs/regles/actives.md) :")
    for t in titres():
        print("- " + t)


if __name__ == "__main__":
    main()
