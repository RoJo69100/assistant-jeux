"""Test du hook pipelines/controle.py : un cas valide et un cas fautif par contrôle (a à e).

Lancer : python pipelines/test_controle.py   (code 1 si un cas se trompe)
"""

import sys

sys.path.insert(0, str(__file__.rsplit("pipelines", 1)[0] + "pipelines"))
import controle  # noqa: E402


def demande(t):
    return {"type": "user", "message": {"content": t}}


def outil(nom, inp, model="claude-sonnet"):
    return {"type": "assistant", "message": {"model": model, "content": [{"type": "tool_use", "name": nom, "input": inp}]}}


def dit(t, model="claude-sonnet"):
    return {"type": "assistant", "message": {"model": model, "content": [{"type": "text", "text": t}]}}


PLAN = """| Priorité | Catégorie | Action |
|---|---|---|
| 🟩 SUIVI | Export | Exporter la page du match. |
"""
CHIFFRE = """| Joueur | Points |
|---|---|
| Baron | 18 |
"""
SQL = outil("mcp__supabase__execute_sql", {"query": "select 1"})
SKILL = outil("Skill", {"skill": "deja-fait"})
EDIT_SQL = outil("Edit", {"file_path": "/x/assistant-jeux/sql/gold/070_vue.sql"})
EDIT_OUT = outil("Write", {"file_path": "/x/assistant-jeux/outputs/basketvibe/fait-2026-11-02.md"})
LONG = "\n".join(f"ligne {i}" for i in range(20))

CAS = [
    # a : modèle
    ("a conception sans rappel", "Fait.", [demande("ajoute la vue"), EDIT_SQL], False),
    ("a conception avec rappel opus", "Fait. /model sonnet après le commit.",
     [demande("ajoute la vue"), dit("/model opus avant", "claude-sonnet"), EDIT_SQL], True),
    ("a session opus sans retour sonnet", "Fait.", [demande("ajoute la vue"), outil("Edit", {"file_path": "pipelines/x.py"}, "claude-opus")], False),
    ("a session opus avec retour sonnet", "Fait, /model sonnet après le commit.",
     [demande("ajoute la vue"), outil("Edit", {"file_path": "pipelines/x.py"}, "claude-opus")], True),
    ("a fichier hors conception", "Noté.", [demande("j'ai fait l'export"), EDIT_OUT], True),
    # b : deja-fait
    ("b plan sans deja-fait", PLAN, [demande("que faire"), SQL], False),
    ("b plan avec deja-fait", PLAN, [demande("que faire"), SKILL, SQL], True),
    ("b deja-fait d'un tour précédent", PLAN, [demande("que faire"), SKILL, SQL, demande("et après"), SQL], False),
    # c : preuve
    ("c tableau chiffré sans source", CHIFFRE, [demande("stats")], False),
    ("c tableau chiffré avec SQL", CHIFFRE, [demande("stats"), SQL], True),
    ("c tableau chiffré avec synthese", CHIFFRE, [demande("stats"), outil("Agent", {"subagent_type": "synthese"})], True),
    # d : phrases fermées
    ("d veux-tu que", "Veux-tu que je lance la vue ?", [demande("stats")], False),
    ("d peut-être", "Il faut peut-être vendre Baron.", [demande("stats")], False),
    ("d citée entre guillemets", "Interdit désormais : « veux-tu que ».", [demande("stats")], True),
    ("d décision tranchée", "Vends Baron aujourd'hui.", [demande("stats")], True),
    # e : concision et identifiants
    ("e conception trop longue", LONG, [demande("conçois le hook")], False),
    ("e conception courte", "Hook ajouté, 12 tests passent.", [demande("conçois le hook")], True),
    ("e identifiant interne", "Fait, comme le demande R-1 et la règle 75.", [demande("conçois le hook")], False),
    ("e longue hors conception", LONG, [demande("raconte le match")], True),
]

if __name__ == "__main__":
    echecs = 0
    for nom, texte, ents, attendu in CAS:
        fautes = controle.fautes_de(texte, ents)
        ok = (not fautes) == attendu
        echecs += not ok
        print(("✅" if ok else "❌"), nom, "" if ok else f"— {fautes}")
    print(f"{len(CAS) - echecs}/{len(CAS)}")
    sys.exit(1 if echecs else 0)
