"""Liens des fichiers cités dans les plans et les réponses (règle de l'utilisateur du 25/11, BasketVibe et Hockey Nation).

Tout fichier d'outputs/ cité (fiche, brief, police, entraînement, académie, transferts, fait, plan) est un lien complet cliquable
sur main : https://github.com/RoJo69100/assistant-jeux/blob/main/outputs/... ; jamais un chemin nu, jamais la branche de travail.
Ordre sûr : le plan est écrit, commité, puis `fusion_main.py` pousse HEAD sur main ; le lien vise main, donc il résout dès la fusion
(le fichier cité existe dans l'arbre de travail : `cibles_absentes` le vérifie avant le commit).
"""
import re
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
MAIN = "https://github.com/RoJo69100/assistant-jeux/blob/main/"
_ANCIENS = re.compile(r"https://github\.com/RoJo69100/assistant-jeux/blob/(?!main/)[^/\s)]+(?:/[^/\s)]+)*?/(outputs/)")
# Chemin d'outputs/ cité nu (pas déjà dans un lien : ni précédé de « / », « ( » de lien markdown, ni de « [ »)
_CHEMIN = re.compile(r"(?<![\w/\[(-])`?(outputs/[\w.\-/àâäéèêëîïôöùûüç]+?\.(?:md|txt|json|csv))`?(?![\w/])")
# Nom de fichier seul d'outputs (police-…, fait-…, que-faire-…, AAAA-MM-JJ-…)
_NOM = re.compile(r"(?<![\w/\[(-])`?((?:police|fait|que-faire|aujourdhui)-\d{4}-\d{2}-\d{2}[\w\-]*\.md|\d{4}-\d{2}-\d{2}-[\w\-]+\.md)`?(?![\w/])")


def lien(chemin) -> str:
    """URL complète sur main d'un chemin relatif à la racine du dépôt."""
    return MAIN + str(chemin).lstrip("/")


def md(chemin) -> str:
    """Lien markdown cliquable : [chemin](URL main)."""
    return f"[{chemin}]({lien(chemin)})"


def _trouver(nom, racine=RACINE):
    trouves = sorted((Path(racine) / "outputs").rglob(nom))
    return trouves[0].relative_to(racine).as_posix() if len(trouves) == 1 else None


def lier(texte: str, racine=RACINE) -> str:
    """Remplace les liens vers une autre branche par main, et chaque chemin nu d'outputs/ (ou nom de fichier d'outputs trouvé une
    seule fois) par un lien markdown complet sur main."""
    texte = _ANCIENS.sub(MAIN + r"\1", texte)
    texte = _CHEMIN.sub(lambda m: md(m.group(1)), texte)

    def nom(m):
        c = _trouver(m.group(1), racine)
        return md(c) if c else m.group(0)
    return _NOM.sub(nom, texte)


def sans_lien(texte: str) -> list:
    """Fichiers cités sans lien sur main : chemins nus d'outputs/, noms de fichiers d'outputs, liens vers une autre branche."""
    return [m.group(1) for m in _CHEMIN.finditer(texte)] + [m.group(1) for m in _NOM.finditer(texte)] + \
        re.findall(r"https://github\.com/RoJo69100/assistant-jeux/blob/(?!main/)\S+", texte)


def cibles_absentes(texte: str, racine=RACINE) -> list:
    """Liens sur main dont le fichier n'existe pas dans l'arbre de travail (il ne sera donc pas sur main après la fusion)."""
    return [c for c in re.findall(re.escape(MAIN) + r"([^\s)\]]+)", texte) if not (Path(racine) / c).exists()]
