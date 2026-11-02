"""Hook SessionStart : met les règles apprises récentes et la consigne « tout lire / carte d'abord » dans le contexte.

Ajouté le 2026-11-02 (reproche : « c'est écrit dans les règles mais tu ne les as pas lues »). Le texte imprimé ici
entre dans le contexte de la session sans que j'aie à ouvrir un fichier. Coût : ~1 500 tokens par session.
"""
import io
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
REGLES = RACINE / "docs" / "retro" / "regles-apprises.md"
NB_REGLES = 12  # les plus récentes (le fichier range la plus récente en haut)


def regles_recentes():
    if not REGLES.exists():
        return ["(docs/retro/regles-apprises.md introuvable : le lire à la main)"]
    sortie = []
    for ligne in REGLES.read_text(encoding="utf-8").splitlines():
        if re.match(r"^\d+\.\s", ligne):
            sortie.append(ligne[:400])
            if len(sortie) >= NB_REGLES:
                break
    return sortie


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    cartes = sorted(p.name for p in (RACINE / "docs" / "decisions" / "cartes").glob("*") if p.is_dir())
    print("RAPPEL DE DÉBUT DE SESSION (hook pipelines/rappel_debut.py)")
    print("1. Toute décision (achat, vente, enchère, composition, défaite, entraînement, académie, finances) : "
          "`python pipelines/dossier.py <jeu> <type>` AVANT de répondre. Si la carte existe, il rend la carte "
          "(où lire chaque variable) + le nouveau : « ça a déjà été traité, je le traite de la même façon ». "
          "Sinon tout lire en entier. Jamais `grep`/`sed` partiel d'une source, jamais « pas tout lu ».")
    print("2. Cartes présentes pour : " + ", ".join(cartes) + ".")
    print("3. Un jeu par session ; `/clear` après chaque jeu commité ; horizon = aujourd'hui seulement ; "
          "règle globale de forme (CLAUDE.md) > règle d'un jeu.")
    print("4. MCP Supabase : essayer une requête avant d'écrire « pas de base » ; non authentifié = "
          "à autoriser dans les connecteurs claude.ai, pas une panne.")
    print(f"Règles apprises les plus récentes ({NB_REGLES}) :")
    for r in regles_recentes():
        print("- " + r)


if __name__ == "__main__":
    main()
