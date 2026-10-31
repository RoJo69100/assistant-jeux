"""Recette d'un jeu : contrôle les tests de docs/attentes/tests/<jeu>.yaml.

Sans option :
  1. chaque fichier de « nouveau_jeu.fichiers » existe ;
  2. chaque vue citée (gold.* / silver.*) est créée quelque part dans sql/ ;
  3. chaque ligne de docs/couverture/<jeu>.md est rattachée à au moins un test (champ couvre).
Avec --reponse <fichier> --jour <lun…dim> : contrôle une réponse rendue (interdits, pastilles,
mots du jour). Le texte entre « », "" ou `` est ignoré (citations).
Sortie : une grille ✅/❌ ; code 1 s'il y a au moins un ❌.
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
CITATION = re.compile(r"«[^»]*»|\"[^\"]*\"|“[^”]*”|`[^`]*`")
LIGNE_COUV = re.compile(r"^\|\s*(\+?\w+)\s*\|", re.M)
VUE = re.compile(r"\b(?:gold|silver)\.[a-z0-9_]+")


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower().replace("’", "'"))
    return "".join(c for c in s if not unicodedata.combining(c))


def liste(texte: str, cle: str) -> list[str]:
    """Valeurs de toutes les listes « cle: [a, b, "c"] » du yaml (format plat, une ligne)."""
    vals = []
    for m in re.finditer(rf"^\s*{cle}:\s*\[(.*)\]\s*$", texte, re.M):
        vals += [v.strip().strip('"').strip("'") for v in m.group(1).split(",") if v.strip()]
    return vals


def bloc(texte: str, cle: str) -> str:
    """Bloc indenté sous « cle: » (jusqu'à la prochaine clé de même niveau ou moins)."""
    m = re.search(rf"^(\s*){cle}:\s*$", texte, re.M)
    if not m:
        return ""
    ind = len(m.group(1))
    lignes = []
    for l in texte[m.end():].splitlines()[1:]:
        if l.strip() and not l.lstrip().startswith("#") and len(l) - len(l.lstrip()) <= ind:
            break
        lignes.append(l)
    return "\n".join(lignes)


def recette(jeu: str) -> list[tuple[bool, str]]:
    test = (RACINE / f"docs/attentes/tests/{jeu}.yaml").read_text(encoding="utf-8")
    res = []

    nj = bloc(test, "nouveau_jeu")
    fichiers = re.findall(r"^\s*-\s+(\S+\.\w+)\s*$", bloc(nj, "fichiers"), re.M)
    manquants = [f for f in fichiers if not (RACINE / f).exists()]
    res.append((not manquants, f"Fichiers du nouveau jeu : {len(fichiers) - len(manquants)}/{len(fichiers)}"
                + (f" — manquent : {', '.join(manquants)}" if manquants else "")))

    sql = "\n".join(p.read_text(encoding="utf-8", errors="replace").lower() for p in (RACINE / "sql").rglob("*.sql"))
    vues = sorted(set(VUE.findall(test)))
    absentes = [v for v in vues if not re.search(rf"view\s+(if not exists\s+)?{re.escape(v)}\b", sql)]
    res.append((not absentes, f"Vues citées existantes dans sql/ : {len(vues) - len(absentes)}/{len(vues)}"
                + (f" — absentes : {', '.join(absentes)}" if absentes else "")))

    couv = (RACINE / f"docs/couverture/{jeu}.md").read_text(encoding="utf-8")
    lignes = [i for i in LIGNE_COUV.findall(couv) if i.lower() not in ("ligne", "#")]
    couvertes = set(liste(test, "couvre"))
    orphelines = [i for i in dict.fromkeys(lignes) if i not in couvertes]
    inconnues = sorted(couvertes - set(lignes))
    res.append((not orphelines, f"Lignes de couverture rattachées à un test : {len(set(lignes)) - len(orphelines)}/{len(set(lignes))}"
                + (f" — sans test : {', '.join(orphelines)}" if orphelines else "")))
    if inconnues:
        res.append((False, f"Tests qui citent une ligne absente de la couverture : {', '.join(inconnues)}"))
    return res


def controle_reponse(jeu: str, fichier: str, jour: str) -> list[tuple[bool, str]]:
    test = (RACINE / f"docs/attentes/tests/{jeu}.yaml").read_text(encoding="utf-8")
    brut = Path(fichier).read_text(encoding="utf-8")
    n = norm(CITATION.sub(" ", brut))
    res = []
    fautes = [i for i in liste(test, "interdits") if norm(i) in n]
    res.append((not fautes, "Aucun interdit" if not fautes else f"Interdits trouvés : {', '.join(fautes)}"))
    pastilles = liste(test, "pastilles")
    res.append((any(p in brut for p in pastilles), "Pastille carrée + mot présente"))
    attendus = liste(bloc(bloc(test, "jours"), jour), "doit_contenir")
    absents = [m for m in attendus if norm(m) not in n]
    res.append((not absents, f"Mots du {jour} : {len(attendus) - len(absents)}/{len(attendus)}"
                + (f" — manquent : {', '.join(absents)}" if absents else "")))
    return res


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("jeu")
    ap.add_argument("--reponse")
    ap.add_argument("--jour", choices=["lun", "mar", "mer", "jeu", "ven", "sam", "dim"])
    a = ap.parse_args()
    if a.reponse and not a.jour:
        ap.error("--reponse demande --jour")
    res = controle_reponse(a.jeu, a.reponse, a.jour) if a.reponse else recette(a.jeu)
    for ok, txt in res:
        print(("✅ " if ok else "❌ ") + txt)
    return 0 if all(ok for ok, _ in res) else 1


if __name__ == "__main__":
    sys.exit(main())
