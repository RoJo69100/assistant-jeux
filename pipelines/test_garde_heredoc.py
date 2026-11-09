"""Tests figés de garde_heredoc.py (critère T1) : python -I pipelines/test_garde_heredoc.py"""

import json
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
from garde_heredoc import verdict  # noqa: E402

REFUSES = [
    ("cat > f <<EOF", "cat > CLAUDE.md <<'EOF'\n# titre\nEOF"),
    ("cat <<EOF > f", "cat <<EOF > docs/a.md\nligne\nEOF"),
    ("cat <<-EOF >> f", "cat <<-EOF >> a.txt\n\tligne\n\tEOF"),
    ("espace avant délimiteur", "cd x && cat > CLAUDE.md << 'EOF'\ntexte\nEOF"),
    ("tee f <<EOF", "tee pipelines/x.py <<\"EOF\"\nprint(1)\nEOF"),
    ("python - <<PY", "python - <<'PY'\nopen('f', 'w').write('x')\nPY"),
    ("python3 <<EOF", "python3 <<EOF\nprint(1)\nEOF"),
    ("chemin python", "/usr/bin/python3 -I - <<EOF\nprint(1)\nEOF"),
    ("cat <<EOF seul", "cat <<EOF\nbonjour\nEOF"),
    ("redirection autre commande", "mysql <<EOF > sortie.txt\nselect 1;\nEOF"),
    ("heredoc en tête", "<<EOF cat > f.md\nx\nEOF"),
    ("cat <<EOF | tee", "cat <<EOF | tee f.md\nx\nEOF"),
    ("substitution hors commit", "echo \"$(cat <<'EOF'\nx\nEOF\n)\" > f.md"),
    ("commit puis fichier", "git commit -m \"$(cat <<'EOF'\nmsg\nEOF\n)\" && cat > f.md <<EOF2\nx\nEOF2"),
]

ACCEPTES = [
    ("git commit $(cat <<EOF)", "git commit -m \"$(cat <<'EOF'\nTitre > détail\n\nCo-Authored-By: X\nEOF\n)\""),
    ("git -C commit", "git -C repo commit -m \"$(cat <<EOF\nmsg >> x\nEOF\n)\""),
    ("commit puis push", "git commit -m \"$(cat <<'EOF'\nmsg\nEOF\n)\"; git status"),
    ("psql sans redirection", "psql <<EOF\nselect 1;\nEOF"),
    ("here-string", "cat <<< \"texte\""),
    ("grep de <<", "grep -n \"<<\" pipelines/x.py"),
    ("sans heredoc", "python -I pipelines/sql.py \"select 1\" > /dev/null"),
    ("redirection sans heredoc", "git log --oneline > /dev/null 2>&1"),
    ("heredoc vers /dev/null", "psql <<EOF >/dev/null 2>&1\nselect 1;\nEOF"),
]


def hook(commande: str, outil: str = "Bash") -> tuple[int, str]:
    entree = json.dumps({"hook_event_name": "PreToolUse", "tool_name": outil, "tool_input": {"command": commande}})
    r = subprocess.run([sys.executable, "-I", str(ICI / "garde_heredoc.py")], input=entree,
                       capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stderr


def main() -> int:
    resultats = []
    for nom, cmd in REFUSES:
        resultats.append((f"refusé : {nom}", verdict(cmd) is not None))
    for nom, cmd in ACCEPTES:
        resultats.append((f"accepté : {nom}", verdict(cmd) is None))
    code, err = hook(REFUSES[0][1])
    resultats.append(("hook : code 2 et « écris le fichier avec Write »", code == 2 and "écris le fichier avec Write" in err))
    resultats.append(("hook : commande acceptée = code 0", hook(ACCEPTES[0][1])[0] == 0))
    resultats.append(("hook : outil autre que Bash ignoré", hook(REFUSES[0][1], "Read")[0] == 0))
    echecs = 0
    for nom, ok in resultats:
        echecs += not ok
        print("OK " if ok else "ECHEC ", nom)
    print(f"{len(resultats) - echecs}/{len(resultats)}")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
