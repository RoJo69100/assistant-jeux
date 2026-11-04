"""Garde-fou avant une décision (refonte v2, étape 3.4).

Imprime, pour un jeu et un domaine : les leçons validées et règles dures (à suivre), les leçons retirées
(conseils interdits), les erreurs ouvertes, et — avec --sujet — les décisions passées sur le même sujet,
en signalant un revirement (achat puis vente, ou l'inverse) à déclarer comme correction avec plan de sortie (R-8).
Code 2 si un revirement est détecté (le rendu doit le déclarer).
Usage : python -I pipelines/garde.py <jeu> <domaine> [--sujet NOM]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sql import url_ro  # noqa: E402

OPPOSES = {"achat": "vente", "vente": "achat"}


def revirement(domaine: str, passees: list[tuple[str, str]]) -> bool:
    """passees : (domaine, statut) des décisions sur le même sujet ; vrai si le domaine opposé a été accepté ou fait."""
    oppose = OPPOSES.get(domaine)
    return bool(oppose) and any(d == oppose and s in ("accepted", "done") for d, s in passees)


def main(argv=None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("jeu")
    p.add_argument("domaine")
    p.add_argument("--sujet")
    a = p.parse_args(argv)
    import psycopg

    code = 0
    with psycopg.connect(url_ro(), connect_timeout=15) as c, c.cursor() as cur:
        cur.execute("select id, status, n_for, n_against, claim from learn.lesson"
                    " where game = %s and domain = %s order by status, id", (a.jeu, a.domaine))
        lecons = cur.fetchall()
        suivre = [l for l in lecons if l[1] in ("validated", "hard_rule")]
        interdits = [l for l in lecons if l[1] == "retired"]
        print(f"Leçons {a.jeu}/{a.domaine} : {len(suivre)} à suivre, {len(interdits)} retirées, "
              f"{len(lecons) - len(suivre) - len(interdits)} hypothèses (sur {len(lecons)})")
        for i, st, nf, na, claim in suivre:
            print(f"  ✅ {i} ({st}, {nf} pour / {na} contre) : {claim}")
        for i, st, nf, na, claim in interdits:
            print(f"  ⛔ {i} retirée ({na} contradictions) : ne pas reconseiller — {claim}")
        cur.execute("select id, description, recurrence, enforcement from learn.error"
                    " where closed_at is null and (game = %s or game is null) order by recurrence desc, id", (a.jeu,))
        for i, desc, rec, enf in cur.fetchall():
            print(f"  ⚠️ erreur E-{i} ouverte (×{rec}, garde : {enf}) : {desc}")
        if a.sujet:
            cur.execute("select id, domain, status, decided_at::date, label from learn.decision"
                        " where game = %s and lower(sujet) = lower(%s) order by decided_at", (a.jeu, a.sujet))
            passees = cur.fetchall()
            for i, dom, st, quand, label in passees:
                print(f"  · D-{i} {quand} {dom} ({st}) : {label}")
            if revirement(a.domaine, [(d, s) for _, d, s, _, _ in passees]):
                print(f"  🔁 REVIREMENT sur {a.sujet} : le déclarer comme correction, avec le plan de sortie chiffré (R-8)")
                code = 2
    return code


if __name__ == "__main__":
    sys.exit(main())
