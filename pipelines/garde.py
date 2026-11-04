"""Garde-fou avant une décision (refonte v2, étape 3.4).

Imprime, pour un jeu et un domaine : les leçons validées et règles dures (à suivre), les leçons retirées
(conseils interdits), les erreurs ouvertes, et — avec --sujet — les décisions passées sur le même sujet,
en signalant un revirement (achat puis vente, ou l'inverse) à déclarer comme correction avec plan de sortie (R-8).
Code 2 si un revirement est détecté (le rendu doit le déclarer).
Données : public.learn_export (psycopg si SUPABASE_DB_URL_RO, sinon REST avec SUPABASE_SECRET_KEY).
Les règles E du triage encore sans code (game nul, ×1) ne sont pas listées ici.
Usage : python -I pipelines/garde.py <jeu> <domaine> [--sujet NOM]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

OPPOSES = {"achat": "vente", "vente": "achat"}


def revirement(domaine: str, passees: list[tuple[str, str]]) -> bool:
    """passees : (domaine, statut) des décisions sur le même sujet ; vrai si le domaine opposé a été accepté ou fait."""
    oppose = OPPOSES.get(domaine)
    return bool(oppose) and any(d == oppose and s in ("accepted", "done") for d, s in passees)


def rapport(jeu: str, domaine: str, sujet: str | None, base: dict) -> tuple[list[str], int]:
    lecons = [l for l in base["lessons"] if l.get("domain") == domaine]
    suivre = [l for l in lecons if l["status"] in ("validated", "hard_rule")]
    interdits = [l for l in lecons if l["status"] == "retired"]
    L = [f"Leçons {jeu}/{domaine} : {len(suivre)} à suivre, {len(interdits)} retirées, "
         f"{len(lecons) - len(suivre) - len(interdits)} hypothèses (sur {len(lecons)})"]
    L += [f"  ✅ {l['id']} ({l['status']}, {l['n_for']} pour / {l['n_against']} contre) : {l['claim'][:300]}" for l in suivre]
    L += [f"  ⛔ {l['id']} retirée ({str(l['n_against']) + ' contradictions' if l['n_against'] else 'infirmée avant migration'}) :"
          f" ne pas reconseiller — {l['claim'][:300]}" for l in interdits]
    L += [f"  ⚠️ erreur E-{e['id']} ouverte (×{e['recurrence']}, garde : {e['enforcement']}) : {e['description']}"
          for e in base.get("errors", [])]
    code = 0
    if sujet:
        passees = [d for d in base["decisions"] if (d.get("sujet") or "").lower() == sujet.lower()]
        L += [f"  · D-{d['id']} {d['decided_at'][:10]} {d['domain']} ({d['status']}) : {d['label']}" for d in passees]
        if revirement(domaine, [(d["domain"], d["status"]) for d in passees]):
            L.append(f"  🔁 REVIREMENT sur {sujet} : le déclarer comme correction, avec le plan de sortie chiffré (R-8)")
            code = 2
    return L, code


def main(argv=None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("jeu")
    p.add_argument("domaine")
    p.add_argument("--sujet")
    a = p.parse_args(argv)
    from export_learnings_md import lire_base
    L, code = rapport(a.jeu, a.domaine, a.sujet, lire_base(a.jeu))
    print("\n".join(L))
    return code


if __name__ == "__main__":
    sys.exit(main())
