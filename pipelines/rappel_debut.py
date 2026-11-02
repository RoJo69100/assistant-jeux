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


REGLES_GLOBALES = [
    "Réponse courte en français ; plan = tableau Priorité (🟥 URGENT / 🟧 IMPORTANT / 🟩 SUIVI, pastille + mot) | Catégorie | Action ; rien « pour plus tard ».",
    "Horizon = AUJOURD'HUI SEULEMENT : jamais « demain », « le 29 », « après le prochain match » comme étape.",
    "Je tranche : une action unique « fais X » ; pas de « peut-être », « à toi de voir », ni question oui/non si une requête ou une mesure peut décider.",
    "Avant tout plan ou « que faire » : skill `deja-fait` + requête SQL du même tour + registre `outputs/<jeu>/fait-AAAA-MM-JJ.md`.",
    "Conception (vues SQL, agents, fiches, hooks, scripts) : dire en une ligne « /model opus avant, /model sonnet après le commit ».",
    "Un jeu par session ; `/clear` après chaque commit ou changement de jeu ; `/compact` dès 15-30 % ; proposer `retro` + `mesure_session.py` avant `/clear`.",
    "Agents : `subagent_type` propre (jamais general-purpose), annoncer le nombre, ≤ 3 par passage, 20 par semaine, `police` avant toute décision, `analyste` sur défaite.",
    "Aucun chiffre, nom, date ou « absent » non vérifié : requête ou lecture du même tour. Résultat de match = `my_result` de la base.",
    "Une source se lit en entier ; « pas tout lu » / « il me manque X » sans « cherché dans : … » est interdit.",
    "Fichiers écrits avec l'outil Write (jamais heredoc) ; une modification = un commit ; mémoire écrite = copiée dans `docs/memoire-claude/`.",
    "Début de session : mémoire locale vs `docs/memoire-claude/` (copier si plus ancienne), skill `retro-session`, règles apprises.",
    "Un « je ne peux pas » est interdit : preuve (requête, mesure) ou « je ne sais pas encore, je le trouve ainsi : … ».",
]


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
    print("RÈGLES GLOBALES DE CLAUDE.md À APPLIQUER À CHAQUE RÉPONSE (les plus souvent violées) :")
    for i, r in enumerate(REGLES_GLOBALES, 1):
        print(f"G{i}. {r}")
    print(f"Règles apprises les plus récentes ({NB_REGLES}) :")
    for r in regles_recentes():
        print("- " + r)


if __name__ == "__main__":
    main()
