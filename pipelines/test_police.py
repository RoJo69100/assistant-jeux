"""Test du hook pipelines/police.py (aveux, H1, H2, H4, H5).

Lancer : python pipelines/test_police.py   (code 1 si un cas se trompe)
Les cas H1/H2 utilisent un jeu fictif « testjeu » : aucun fichier réel n'est lu ni écrit.
"""

import sys
import uuid

sys.path.insert(0, str(__file__.rsplit("pipelines", 1)[0] + "pipelines"))
import police  # noqa: E402

police.JEUX["testjeu"] = ["testjeu"]


def u(texte):
    return {"type": "user", "message": {"content": texte}}


def outil(cmd):
    return {"type": "assistant", "message": {"content": [{"type": "tool_use", "input": {"command": cmd}}]}}


PLAN_ACHAT = """Testjeu, ce soir.
| Priorité | Catégorie | Action |
|---|---|---|
| 🟥 URGENT | Transferts | Enchère maximale 300 000 sur Fuchs. |
| 🟩 SUIVI | Export | Exporter le marché. |
"""
PLAN_EXPORT = """Testjeu.
| Priorité | Catégorie | Action |
|---|---|---|
| 🟧 IMPORTANT | Export | Exporter la page du match. |
"""
PLAN_VENTE = PLAN_ACHAT.replace("Enchère maximale 300 000 sur Fuchs", "Mettre Henry en vente à 25 000")
AVEU = "Je n'ai pas tout lu le Discord, non relevé pour l'instant."
MANQUE_OK = "Il me manque la forme de Chara — cherché dans : gold.bv_roster_now, bronze."

CAS = [
    # (nom, texte, entrées, principal, préfixes de fautes attendues ; [] = passe)
    ("aveu bloqué", AVEU, [u("que faire sur basketvibe")], True, ["pas tout lu", "non releve"]),
    ("manque sourcé passe", MANQUE_OK, [u("analyse")], True, []),
    ("manque sans source bloqué", "Il me manque la forme.", [u("analyse")], True, ["« il me manque »"]),
    ("H4 conception : aveu cité passe", "Le hook bloque non lu et non relevé hors conception.",
     [u("concois l'étape 0a")], True, []),
    ("H4 citation code passe", "```\nINTERDITS = ['non lu']\n```\nFait.", [u("analyse")], True, []),
    ("H1+H2 achat sans dossier ni police", PLAN_ACHAT, [u("que faire")], True, ["H1 : décision achat", "H2 : décision achat"]),
    ("H1 levé par dossier.py lancé", PLAN_ACHAT, [u("que faire"), outil("python pipelines/dossier.py testjeu achat")],
     True, ["H2 : décision achat"]),
    ("vente reconnue", PLAN_VENTE, [u("que faire")], True, ["H1 : décision vente", "H2 : décision vente"]),
    ("export seul passe", PLAN_EXPORT, [u("que faire")], True, []),
    ("H4 conception + décision : H1 reste", PLAN_ACHAT, [u("conception des hooks")], True, ["H1", "H2"]),
    ("agent : pas de H1/H2", PLAN_ACHAT, [u("que faire")], False, []),
    ("H5 au-delà de 5 demandes", "Fait.", [u(f"demande {i}") for i in range(6)], True, ["H5"]),
    ("H5 pas si rétro proposée", "Fait. Je propose la rétro.", [u(f"demande {i}") for i in range(6)], True, []),
]


def main() -> int:
    erreurs = 0
    for nom, texte, ents, principal, attendu in CAS:
        session = "test-" + uuid.uuid4().hex
        f = police.fautes_de(texte, ents, principal, session)
        ok = len(f) == len(attendu) and all(any(x.startswith(a) for x in f) for a in attendu)
        if nom.startswith("H5 au-delà"):
            ok = ok and not police.fautes_de(texte, ents, principal, session)  # une seule fois
        erreurs += not ok
        print(("✅ " if ok else "❌ ") + nom + ("" if ok else f" — obtenu : {f}"))
    print(f"{len(CAS) - erreurs}/{len(CAS)}")
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
