"""Hook SessionStart : en session cloud (CLAUDE_CODE_REMOTE=true), installe requirements.txt si psycopg manque.

Sur les PC locaux : ne fait rien. N'échoue jamais (code 0) pour ne pas bloquer le démarrage.
"""

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent


def main() -> int:
    if os.environ.get("CLAUDE_CODE_REMOTE") != "true" or importlib.util.find_spec("psycopg"):
        return 0
    r = subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", str(RACINE / "requirements.txt")],
                       capture_output=True, text=True)
    print("DÉPENDANCES : installées (cloud)." if r.returncode == 0
          else f"DÉPENDANCES : échec de pip install — {r.stderr.strip()[-200:]}")
    if not os.environ.get("SUPABASE_DB_URL_RO") and not (RACINE / ".env").exists():
        print("SUPABASE_DB_URL_RO absente : sql.py et la recette ne liront pas la base ; connecteur Supabase en repli.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
