"""Test de pipelines/scan_agent.py (contrôle des transcriptions de l'agent data-scientist).

Lancer : python -I pipelines/test_scan_agent.py   (code 1 si un cas se trompe)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scan_agent  # noqa: E402

INTERDITS = ["docs/refonte-v3/etude-evenements-basketvibe.md", "docs/superpowers/"]


def outil(nom, inp, uid="u1"):
    return {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": uid, "name": nom, "input": inp}]}}


def resultat(texte, uid="u1"):
    return {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": uid, "content": texte}]}}


def faute(nom, inp):
    return bool(scan_agent.hors_bornes(scan_agent.appels([outil(nom, inp)]), INTERDITS))


def _fichier_avec(texte):
    import tempfile
    f = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8")
    f.write(texte)
    f.close()
    return f.name


def nb_fuites(entrees):
    return len(scan_agent.fuites(entrees))


CAS = [
    ("bash sql lecture", not faute("Bash", {"command": 'python -I pipelines/sql.py "select 1" --max-rows 30'})),
    ("bash script d'étude", not faute("Bash", {"command": "python -I pipelines/etudes/t1.py"})),
    ("bash sql chemin absolu", not faute("Bash", {"command": 'python -I /home/user/assistant-jeux/pipelines/sql.py "select 1" --max-rows 30'})),
    ("bash script d'étude chemin absolu", not faute("Bash", {"command": "python -I /home/user/assistant-jeux/pipelines/etudes/t1.py"})),
    ("bash chemin absolu hors dépôt", faute("Bash", {"command": 'python -I /home/user/autre/pipelines/sql.py "select 1"'})),
    ("bash chemin absolu script hors dossier", faute("Bash", {"command": "python -I /home/user/assistant-jeux/pipelines/etude_evenements_calculs.py calculs"})),
    ("bash chemin absolu table kb", faute("Bash", {"command": 'python -I /home/user/assistant-jeux/pipelines/sql.py "select * from kb.notes"'})),
    ("bash cat", faute("Bash", {"command": "cat x"})),
    ("bash composé", faute("Bash", {"command": 'python -I pipelines/sql.py "select 1" && cat x'})),
    ("bash script hors dossier", faute("Bash", {"command": "python -I pipelines/etude_evenements_calculs.py calculs"})),
    ("sql table kb", faute("Bash", {"command": 'python -I pipelines/sql.py "select * from kb.notes"'})),
    ("sql table learn en join", faute("Bash", {"command": 'python -I pipelines/sql.py "select 1 from silver.a join learn.b on true"'})),
    ("script qui lit kb", faute("Write", {"file_path": "/x/pipelines/etudes/a.py", "content": "executer('select * from kb.x')"})),
    ("write docs/etudes", not faute("Write", {"file_path": "/home/user/assistant-jeux/docs/etudes/a.md", "content": "ok"})),
    ("write pipelines/etudes", not faute("Write", {"file_path": "/home/user/assistant-jeux/pipelines/etudes/a.py", "content": "ok"})),
    ("write hors dossier", faute("Write", {"file_path": "/home/user/assistant-jeux/pipelines/x.py", "content": "ok"})),
    ("edit interdit", faute("Edit", {"file_path": "/home/user/assistant-jeux/docs/etudes/a.md"})),
    ("read interdit", faute("Read", {"file_path": "/home/user/assistant-jeux/docs/refonte-v3/etude-evenements-basketvibe.md"})),
    ("read dossier interdit", faute("Read", {"file_path": "/home/user/assistant-jeux/docs/superpowers/plans/p.md"})),
    ("read autorisé", not faute("Read", {"file_path": "/home/user/assistant-jeux/pipelines/sql.py"})),
    ("grep sans chemin", faute("Grep", {"pattern": "cercle"})),
    ("grep sur docs", faute("Grep", {"pattern": "cercle", "path": "/home/user/assistant-jeux/docs"})),
    ("grep chemin sûr", not faute("Grep", {"pattern": "def groupe", "path": "/home/user/assistant-jeux/pipelines/etude_evenements_basketvibe.py"})),
    ("glob sans chemin", not faute("Glob", {"pattern": "pipelines/*.py"})),
    ("rapport final", not faute("SubagentHandback", {"message": "fin"})),
    ("outil absent de l'en-tête", faute("WebFetch", {"url": "x"})),
    ("fuite 6,81 trouvée", nb_fuites([outil("Read", {"file_path": "a"}), resultat("pente +6,81 [x]")]) == 1),
    ("fuite 9.01 et 4.02", nb_fuites([outil("Bash", {"command": "c"}), resultat("[4.02 ; 9.01]")]) == 2),
    ("pas de fuite 16.81 ni date", nb_fuites([outil("Bash", {"command": "c"}), resultat("16.81 2026-09-01 6.812")]) == 0),
    ("fuite en liste de blocs", nb_fuites([outil("Bash", {"command": "c"}), resultat([{"type": "text", "text": "6.81"}])]) == 1),
    ("fuite dans attachment", nb_fuites([{"type": "attachment", "attachment": {"content": "vu 4,02"}}]) == 1),
    ("liste des interdits réelle sans chaîne de fuite", scan_agent.chaines_dans(Path(__file__).resolve().parent.parent / "docs/etudes/interdits-t1.txt") == []),
    ("chaînes de fuite détectées dans un fichier", scan_agent.chaines_dans(_fichier_avec("# chaînes 6,81 et 9.01\na/b.md\n")) == ["6,81", "9.01"]),
    ("outil d'origine retrouvé", scan_agent.fuites([outil("Grep", {"pattern": "p"}, "k"), resultat("6.81", "k")])[0]["outil"] == "Grep"),
]

if __name__ == "__main__":
    echecs = 0
    for nom, ok in CAS:
        echecs += not ok
        print("✅" if ok else "❌", nom)
    print(f"{len(CAS) - echecs}/{len(CAS)}")
    sys.exit(1 if echecs else 0)
