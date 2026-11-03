"""Génère les vues core.* (union des adaptateurs) depuis docs/attentes/jeux/*.yaml (refonte v2, phase 1).

Chaque jeu déclare dans sa config une section « core: » : une ligne par entité branchée,
  player_daily:  { limites: [morale, suspended] }
ce qui veut dire : la vue adapt.<jeu>_player_daily existe et les colonnes citées sont nulles par construction.
Le contrat (colonnes, types, clés) est ici ; pipelines/contrat_core.py le contrôle sur la base.

Sans option : écrit sql/core/002_core_views.sql (à appliquer ensuite par migration Supabase).
Avec --check : code 1 si le fichier n'est pas à jour (branché sur recette.py).
"""

import argparse
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SORTIE = RACINE / "sql/core/002_core_views.sql"

# entité -> (colonnes (nom, type postgres, non nul), clé d'unicité)
CONTRAT = {
    "player_daily": ([
        ("game", "text", True), ("team_id", "text", True), ("club_label", "text", False),
        ("player_id", "text", True), ("day", "date", True), ("name", "text", True),
        ("position", "text", False), ("age", "integer", False), ("rating", "numeric", False),
        ("form", "numeric", False), ("fatigue", "numeric", False), ("morale", "numeric", False),
        ("injured", "boolean", False), ("suspended", "boolean", False), ("salary", "numeric", False),
        ("contract_end", "date", False), ("market_value", "numeric", False), ("is_academy", "boolean", True),
        ("skills", "jsonb", False), ("extras", "jsonb", False),
    ], ("game", "team_id", "player_id", "day")),
    "fixture": ([
        ("game", "text", True), ("team_id", "text", True), ("fixture_id", "text", True),
        ("competition_kind", "text", True), ("round_no", "integer", False), ("rounds_total", "integer", False),
        ("day", "date", True), ("scheduled_at", "timestamp with time zone", False), ("played", "boolean", True),
        ("my_score", "integer", False), ("opp_score", "integer", False), ("my_result", "text", False),
        ("opponent", "text", False), ("home", "boolean", False), ("extras", "jsonb", False),
    ], ("game", "team_id", "fixture_id")),
    "standing": ([
        ("game", "text", True), ("team_id", "text", True), ("team_label", "text", False),
        ("is_mine", "boolean", True), ("season_id", "text", False), ("day", "date", True),
        ("round_no", "integer", False), ("rank", "integer", True), ("played", "integer", False),
        ("points", "integer", False), ("wins", "integer", False), ("draws", "integer", False),
        ("losses", "integer", False), ("gf", "integer", False), ("ga", "integer", False),
        ("extras", "jsonb", False),
    ], ("game", "season_id", "day", "team_id")),
    "finance_daily": ([
        ("game", "text", True), ("team_id", "text", True), ("day", "date", True),
        ("balance", "numeric", False), ("income", "numeric", False), ("expenses", "numeric", False),
        ("salaries", "numeric", False), ("wage_cap", "numeric", False), ("capacite_invest", "numeric", False),
        ("extras", "jsonb", False),
    ], ("game", "team_id", "day")),
}

LIGNE_CORE = re.compile(r"^  ([a-z_]+):\s*\{\s*limites:\s*\[([^\]]*)\]", re.M)


def branchements() -> dict[str, dict[str, list[str]]]:
    """jeu -> entité -> colonnes déclarées nulles, lu dans la section core: de chaque config."""
    jeux = {}
    for f in sorted((RACINE / "docs/attentes/jeux").glob("*.yaml")):
        if f.name.startswith("_"):
            continue
        texte = f.read_text(encoding="utf-8")
        m = re.search(r"^core:.*\n((?:  .*\n?)*)", texte, re.M)
        if not m:
            continue
        entites = {}
        for nom, limites in LIGNE_CORE.findall(m.group(1)):
            if nom not in CONTRAT:
                sys.exit(f"{f.name} : entité core inconnue « {nom} »")
            entites[nom] = [c.strip() for c in limites.split(",") if c.strip()]
        jeux[f.stem] = entites
    return jeux


def generer() -> str:
    jeux = branchements()
    morceaux = ["-- Généré par pipelines/build_core.py depuis docs/attentes/jeux/*.yaml : ne pas modifier à la main.\n"]
    for entite, (colonnes, _cle) in CONTRAT.items():
        sources = [j for j, e in jeux.items() if entite in e]
        if not sources:
            continue
        liste = ", ".join(c for c, _t, _n in colonnes)
        selects = "\nunion all\n".join(f"select {liste} from adapt.{j}_{entite}" for j in sources)
        morceaux.append(f"create or replace view core.{entite} with (security_invoker = true) as\n{selects};\n"
                        f"grant select on core.{entite} to assistant_ro;\n")
    return "\n".join(morceaux)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="code 1 si le fichier généré n'est pas à jour")
    args = ap.parse_args()
    attendu = generer()
    if args.check:
        actuel = SORTIE.read_text(encoding="utf-8") if SORTIE.exists() else ""
        if actuel != attendu:
            print(f"{SORTIE.relative_to(RACINE)} pas à jour : lancer python pipelines/build_core.py")
            return 1
        print("vues core à jour")
        return 0
    SORTIE.write_text(attendu, encoding="utf-8", newline="\n")
    print(f"écrit {SORTIE.relative_to(RACINE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
