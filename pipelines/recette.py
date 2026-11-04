"""Recette d'un jeu : contrôle les tests de docs/attentes/tests/<jeu>.yaml.

Sans option :
  1. chaque fichier de « nouveau_jeu.fichiers » existe ;
  2. chaque vue citée (gold.* / silver.*) est créée quelque part dans sql/ ;
  3. chaque ligne de docs/couverture/<jeu>.md est rattachée à au moins un test (champ couvre).
Avec --reponse <fichier> --jour <lun…dim> : contrôle une réponse rendue (interdits, pastilles,
mots du jour). Le texte entre « », "" ou `` est ignoré (citations).
Avec --tous (étape 0b, 2026-11-02 ; à lancer avant chaque commit de conception) :
  1. rejoue les tests (forme, police, controle, sql, contexte_budget), le budget de contexte,
     les vues core à jour (build_core --check), le contrat core (contrat_core) et la parité de
     gold.agenda, gold.exports_state, gold.daily_alerts et gold.finance_health avec les anciennes vues
     (agenda_parite, exports_parite, alertes_parite, finances_parite) ;
  2. pour chaque jeu : resume.md présent, learnings.md présent, tests docs/attentes/tests/<jeu>.yaml
     (recette complète s'ils existent), chaque vue gold/silver/bronze citée dans docs/fiches/<jeu>/ et
     docs/decisions/cartes/<jeu>/ créée dans sql/, et le résumé du cartographe (cartes, leçons sans check).
Sortie : une grille ✅/❌ ; code 1 s'il y a au moins un ❌.
"""

import argparse
import re
import subprocess
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
        vals += [a or b.strip() for a, b in re.findall(r'"([^"]*)"|([^,"]+)', m.group(1)) if a or b.strip()]
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


JEUX = ["basketvibe", "hockeynation", "teamsoccer", "sixzeroleague", "derbymanager", "hardwood"]
OBJET = re.compile(r"\b(?:gold|silver|bronze)\.[a-z0-9_]*[a-z0-9]\b")


def lancer(script: str, *args: str) -> tuple[bool, str]:
    r = subprocess.run([sys.executable, str(RACINE / "pipelines" / script), *args], capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    der = (r.stdout.strip().splitlines() or [""])[-1]
    ko = [l for l in r.stdout.splitlines() if l.startswith("❌")]
    return r.returncode == 0, f"{script} : {der}" + (f" — {'; '.join(ko[:3])}" if ko else "")


def objets_absents(jeu: str, sql: str) -> tuple[int, list[str]]:
    dossiers = [RACINE / f"docs/fiches/{jeu}", RACINE / f"docs/decisions/cartes/{jeu}"]
    txt = "\n".join(p.read_text(encoding="utf-8", errors="replace").lower()
                    for d in dossiers if d.is_dir() for p in d.glob("*.md"))
    abandon = re.compile(r"ne pas (lire|utiliser)|remplac|defectu|défectu|obsolete|obsolète|supprim|abandonn")
    objets = sorted({o for l in txt.splitlines() for o in OBJET.findall(l)
                     if not any(abandon.search(seg) for seg in re.split(r";|\.\s", l) if o in seg)})
    return len(objets), [o for o in objets
                         if not re.search(rf"(view|table|function)\s+(if not exists\s+)?{re.escape(o)}\b", sql)]


def tous() -> list[tuple[bool, str]]:
    sys.path.insert(0, str(RACINE / "pipelines"))
    import cartographe
    res = [lancer(t) for t in ("test_forme.py", "test_police.py", "test_controle.py", "test_sql.py", "test_contexte_budget.py", "test_decision.py")]
    res.append(lancer("contexte_budget.py"))
    res.append(lancer("build_core.py", "--check"))
    res.append(lancer("contrat_core.py"))
    res.append(lancer("agenda_parite.py"))
    res.append(lancer("exports_parite.py"))
    res.append(lancer("alertes_parite.py"))
    res.append(lancer("finances_parite.py"))
    sql ="\n".join(p.read_text(encoding="utf-8", errors="replace").lower() for p in (RACINE / "sql").rglob("*.sql"))
    for jeu in JEUX:
        res.append((True, f"— {jeu} —"))
        res.append(((RACINE / f"docs/fiches/{jeu}/resume.md").exists(), f"{jeu} : resume.md"))
        res.append(((RACINE / f"outputs/{jeu}/learnings.md").exists(), f"{jeu} : learnings.md"))
        if (RACINE / f"docs/attentes/tests/{jeu}.yaml").exists():
            res += [(ok, f"{jeu} : {txt}") for ok, txt in recette(jeu)]
        else:
            res.append((False, f"{jeu} : tests docs/attentes/tests/{jeu}.yaml absents"))
        n, absents = objets_absents(jeu, sql)
        res.append((not absents, f"{jeu} : vues citées présentes dans sql/ : {n - len(absents)}/{n}"
                    + (f" — absentes : {', '.join(absents)}" if absents else "")))
        a = cartographe.analyse(jeu)
        res.append((not a["manquantes"] and not a["sans"],
                    f"{jeu} : cartes {len(a['cartes'])}/{len(cartographe.TYPES)}, leçons sans check {len(a['sans'])}"))
    return res


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("jeu", nargs="?")
    ap.add_argument("--tous", action="store_true", help="tous les jeux + tests des hooks")
    ap.add_argument("--reponse")
    ap.add_argument("--jour", choices=["lun", "mar", "mer", "jeu", "ven", "sam", "dim"])
    a = ap.parse_args()
    if not a.tous and not a.jeu:
        ap.error("donne un jeu ou --tous")
    if a.reponse and not a.jour:
        ap.error("--reponse demande --jour")
    res = tous() if a.tous else controle_reponse(a.jeu, a.reponse, a.jour) if a.reponse else recette(a.jeu)
    for ok, txt in res:
        print(("✅ " if ok else "❌ ") + txt)
    return 0 if all(ok for ok, _ in res) else 1


if __name__ == "__main__":
    sys.exit(main())
