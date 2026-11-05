"""Test du hook pipelines/police.py (aveux, H1, H2, H3, H4, H5, H6 ; H1/H2 limités aux gros transferts, S1).

Lancer : python pipelines/test_police.py   (code 1 si un cas se trompe)
Les cas H1/H2 utilisent un jeu fictif « testjeu » : aucun fichier réel n'est lu ni écrit.
"""

import sys
import uuid

sys.path.insert(0, str(__file__.rsplit("pipelines", 1)[0] + "pipelines"))
import police  # noqa: E402

police.JEUX["testjeu"] = ["testjeu"]
LECONS = {"L-001": "validated", "L-002": "retired"}
_lecons = police.lecons_du
police.lecons_du = lambda jeu: LECONS if jeu == "testjeu" else _lecons(jeu)
NEW = "python -I pipelines/decision.py new testjeu achat --label x"


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
PLAN_VENTE = PLAN_ACHAT.replace("Enchère maximale 300 000 sur Fuchs", "Mettre Henry en vente à 250 000")
PLAN_PETIT = PLAN_ACHAT.replace("300 000", "50 000")
PLAN_K = PLAN_ACHAT.replace("300 000", "120k")
PLAN_SANS_MONTANT = PLAN_ACHAT.replace("Enchère maximale 300 000 sur Fuchs", "Mettre Henry en vente")
PLAN_COMPO = """Testjeu, ce soir.
| Priorité | Catégorie | Action |
|---|---|---|
| 🟥 URGENT | Composition | Saisir le cinq de ligue : Baron PG. |
| 🟧 IMPORTANT | Entraînement | Baron : principale Tir. |
| 🟧 IMPORTANT | Finances | Baisser le prix des billets à 12. |
"""
police.SEUIL_GROS_MONTANT["testjeu"] = 100_000
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
    ("H1+H2 achat sans dossier ni police", PLAN_ACHAT, [u("que faire")], True, ["H1 : décision achat", "H2 : décision achat", "H3 : décision achat"]),
    ("H1 levé par dossier.py lancé", PLAN_ACHAT, [u("que faire"), outil("python pipelines/dossier.py testjeu achat")],
     True, ["H2 : décision achat", "H3 : décision achat"]),
    ("H3 levé par decision.py new", PLAN_ACHAT, [u("que faire"), outil(NEW)], True, ["H1", "H2"]),
    ("H3 domaine incompatible", PLAN_VENTE, [u("que faire"), outil(NEW)], True, ["H1", "H2", "H3"]),
    ("H6 leçon validée passe", "Testjeu : L-001 tient.", [u("analyse")], True, []),
    ("H6 leçon inconnue", "Testjeu : L-099 tient.", [u("analyse")], True, ["H6 : leçon(s) L-099 inconnue"]),
    ("H6 leçon retirée", "Testjeu : L-002 tient.", [u("analyse")], True, ["H6 : leçon(s) L-002 retirée"]),
    ("H6 agent : pas contrôlé", "Testjeu : L-099.", [u("analyse")], False, []),
    ("H6 deux jeux nommés : pas contrôlé", "Testjeu et Hockey Nation : L-099.", [u("analyse")], True, []),
    ("vente reconnue", PLAN_VENTE, [u("que faire")], True, ["H1 : décision vente", "H2 : décision vente", "H3 : décision vente"]),
    ("export seul passe", PLAN_EXPORT, [u("que faire")], True, []),
    ("S1 : achat sous le seuil sans dossier ni police", PLAN_PETIT, [u("que faire")], True, ["H3 : décision achat"]),
    ("S1 : montant 120k au-dessus du seuil", PLAN_K, [u("que faire")], True, ["H1", "H2", "H3"]),
    ("S1 : vente sans montant = contrôlée", PLAN_SANS_MONTANT, [u("que faire")], True, ["H1", "H2", "H3"]),
    ("S1 : composition, entraînement, finances sans H1/H2", PLAN_COMPO, [u("que faire")], True,
     ["H3 : décision composition", "H3 : décision entrainement", "H3 : décision finances"]),
    ("H4 conception + décision : H1 reste", PLAN_ACHAT, [u("conception des hooks")], True, ["H1", "H2", "H3"]),
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
