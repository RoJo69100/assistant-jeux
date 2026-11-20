"""Interdit les f-strings dont une accolade contient le guillemet qui ferme la f-string.

Cette forme (PEP 701) n'existe qu'en Python 3.12 ; la routine tourne sur Python 3.11 et
s'arrête sur une SyntaxError. Vérification par tokenize :
- Python 3.12+ : jetons FSTRING_START / FSTRING_END, on cherche un guillemet identique imbriqué ;
- Python < 3.12 : le guillemet imbriqué coupe la f-string, il reste une accolade ouverte.
"""
import io
import subprocess
import sys
import tokenize
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent


def fichiers_py():
    sortie = subprocess.run(["git", "ls-files", "*.py"], cwd=RACINE, capture_output=True, text=True).stdout.split()
    if sortie:
        return [RACINE / p for p in sortie]
    return [p for p in RACINE.rglob("*.py") if ".git" not in p.parts]


def _accolades_desequilibrees(corps):
    """Vrai si le corps d'une f-string a une accolade ouverte jamais fermée (hors {{ }})."""
    prof, i, n = 0, 0, len(corps)
    while i < n:
        c = corps[i]
        if c in "{}" and corps[i + 1:i + 2] == c and prof == 0:
            i += 2
            continue
        prof += (c == "{") - (c == "}")
        i += 1
    return prof != 0


def occurrences(source):
    """Liste des (ligne, texte) où une f-string contient son propre guillemet dans une accolade."""
    trouves = []
    jetons = tokenize.generate_tokens(io.StringIO(source).readline)
    if sys.version_info >= (3, 12):
        pile = []
        for t in jetons:
            if t.type == tokenize.FSTRING_START:
                q = t.string[-1]
                if pile and pile[-1] == q:
                    trouves.append((t.start[0], t.line.strip()))
                pile.append(q)
            elif t.type == tokenize.FSTRING_END and pile:
                pile.pop()
            elif pile and t.type == tokenize.STRING and t.string[0] == pile[-1]:
                trouves.append((t.start[0], t.line.strip()))
        return sorted(set(trouves))
    for t in jetons:
        if t.type != tokenize.STRING:
            continue
        s = t.string
        k = 0
        while s[k] not in "'\"":
            k += 1
        if "f" not in s[:k].lower():
            continue
        n = 3 if s[k:k + 3] in ('"""', "'''") else 1
        if _accolades_desequilibrees(s[k + n:-n]):
            trouves.append((t.start[0], t.line.strip()))
    return trouves


class TestFStringCompat(unittest.TestCase):
    def test_detecteur_sur_exemple(self):
        mauvais = 'x = {"a": 1}\ny = f"{x["a"]}"\n'
        bon = "x = {'a': 1}\ny = f\"{x['a']} {{ok}}\"\n"
        self.assertTrue(occurrences(mauvais))
        self.assertFalse(occurrences(bon))

    def test_aucun_guillemet_imbrique(self):
        fautes = []
        for p in fichiers_py():
            try:
                src = p.read_text(encoding="utf-8")
            except OSError:
                continue
            try:
                for ligne, texte in occurrences(src):
                    fautes.append(f"{p.relative_to(RACINE)}:{ligne}: {texte[:80]}")
            except (tokenize.TokenError, IndentationError, SyntaxError):
                fautes.append(f"{p.relative_to(RACINE)}: illisible par tokenize")
        self.assertEqual(fautes, [], "f-string à guillemet imbriqué (Python 3.12 seulement)")


if __name__ == "__main__":
    unittest.main()
