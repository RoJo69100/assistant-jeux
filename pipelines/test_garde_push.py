"""Tests de garde_push.py : python -m pytest pipelines/test_garde_push.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from garde_push import verdict  # noqa: E402


def test_hors_push_ignore():
    assert verdict("PreToolUse", "git status -sb") is None
    assert verdict("PostToolUse", "git commit -q -m x", "## main") is None


def test_push_muet_refuse():
    assert verdict("PreToolUse", "git push -q") is not None
    assert verdict("PreToolUse", "git add . ; git push --quiet origin main") is not None


def test_push_lisible_accepte():
    assert verdict("PreToolUse", "git push") is None
    assert verdict("PreToolUse", "git commit -q -m x; git push") is None


def test_sans_suivi_distant():
    assert "aucune branche distante" in verdict("PostToolUse", "git push", "## refonte-v2")


def test_en_avance():
    assert "non confirmé" in verdict("PostToolUse", "git push", "## main...origin/main [ahead 1]")


def test_synchro():
    assert verdict("PostToolUse", "git push", "## main...origin/main") is None
