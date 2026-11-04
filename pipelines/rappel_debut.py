"""Hook SessionStart : met dans le contexte les TITRES des règles actives (docs/regles/actives.md) et le rappel de décision.

Refonte v2 (0.3-D, 2026-11-03) : l'ancienne version imprimait G1-G12 et 12 règles apprises en entier (~1 500 tokens).
Ici, seul le déclencheur de chaque règle est imprimé ; le texte complet est dans actives.md, lu à la demande.
Les 3 exports les plus en retard viendront de `gold.sante_collecte` quand `pipelines/sql.py` existera (0.4).
"""
import io
import re
import subprocess
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


def alerte_sauvegarde():
    """Une ligne seulement si la sauvegarde du bronze a plus de 10 jours (ou n'existe pas)."""
    sys.path.insert(0, str(RACINE / "pipelines"))
    try:
        import sauvegarde_bronze as sb
        age = sb.jours_depuis(Path.home() / "backups" / "assistant-jeux")
    except Exception:
        return None
    if age is None:
        return "SAUVEGARDE BRONZE : jamais faite — `python -I pipelines/sauvegarde_bronze.py`."
    if age > sb.JOURS_ALERTE:
        return f"SAUVEGARDE BRONZE : {age:.0f} jours — `python -I pipelines/sauvegarde_bronze.py`."
    return None


def alerte_branches_cloud():
    """Une ligne si une branche cloud `ccr-*` a des commits que ni HEAD ni origin/main ne contiennent (travail d'une autre session)."""
    def git(*args):
        return subprocess.run(["git", *args], cwd=RACINE, capture_output=True, text=True, timeout=30).stdout
    try:
        subprocess.run(["git", "fetch", "--all", "-q"], cwd=RACINE, capture_output=True, timeout=30)
        noms = git("for-each-ref", "--format=%(refname:short)", "refs/remotes/origin/ccr-*").split()
        en_avance = [n for n in noms if git("rev-list", "--count", f"HEAD..{n}", "^origin/main").strip() not in ("", "0")]
    except Exception:
        return None
    if en_avance:
        return f"BRANCHES CLOUD EN AVANCE : {len(en_avance)} (`git branch -r`, `git show <branche>:chemin`)."
    return None


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if (a := alerte_sauvegarde()):
        print(a)
    if (b := alerte_branches_cloud()):
        print(b)
    print("RAPPEL DE DÉBUT DE SESSION")
    print("Décision (achat, vente, enchère, composition, défaite, entraînement, académie, finances) : "
          "`python pipelines/dossier.py <jeu> <type>` d'abord.")    print("MCP Supabase : requête d'abord avant « pas de base » ; non authentifié = à autoriser (claude.ai).")
    print("Règles actives (docs/regles/actives.md) :")
    for t in titres():
        print("- " + t)


if __name__ == "__main__":
    main()
