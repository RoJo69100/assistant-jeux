"""Test du hook pipelines/controle.py : un cas valide et un cas fautif par contrôle (a, c à j ; b retiré en S1).

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
PLAN_REPORT = """| Priorité | Catégorie | Action |
|---|---|---|
| 🟧 IMPORTANT | Export | Exporter la page du match demain matin. |
"""
PLAN_DEMAIN = """| Priorité | Catégorie | Action |
|---|---|---|
| 🟥 URGENT | Composition | Saisir ce soir la composition du match de demain 13:00. |
"""
CHIFFRE = """| Joueur | Points |
|---|---|
| Baron | 18 |
"""
LIGNES = {"composition": "🟥 URGENT | Composition | Saisir l'amical du jour.",
          "tactique": "🟥 URGENT | Tactique | Saisir la ligue.",
          "entrainement": "🟧 IMPORTANT | Entraînement | Garder les réglages.",
          "transferts": "🟧 IMPORTANT | Transferts | Enchérir sur Baron.",
          "finances": "🟩 SUIVI | Finances | Billets à 12.",
          "analyse": "🟩 SUIVI | Analyse | Lire la défaite."}


def plan_bv(sans=(), commentaire=""):
    corps = "\n".join(f"| {l} |" for c, l in LIGNES.items() if c not in sans)
    return f"BasketVibe\n\n| Priorité | Catégorie | Action |\n|---|---|---|\n{corps}\n\n{commentaire}\n"


PLAN_COMPLET = plan_bv()
PLAN_PRESQUE = plan_bv(("transferts",), "Transferts : aucune enchère en cours (gold.bv_agenda).")
PLAN_SANS_COMPO = plan_bv(("composition",), "Composition : aucun match aujourd'hui (gold.bv_agenda).")
BV_SQL = outil("Bash", {"command": "python -I pipelines/sql.py \"select * from gold.bv_agenda\""})
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
    ("a voie courte, rappel déclaré une fois", "Fait.",
     [demande("ce plan approuvé tient lieu de conception"), dit("/model opus avant", "claude-sonnet"),
      outil("Edit", {"file_path": "pipelines/x.py"}, "claude-opus")], True),
    ("a voie courte sans aucun rappel", "Fait.",
     [demande("ce plan approuvé tient lieu de conception"), outil("Edit", {"file_path": "pipelines/x.py"}, "claude-opus")], False),
    ("a fichier hors conception", "Noté.", [demande("j'ai fait l'export"), EDIT_OUT], True),
    # b : retiré en S1 (deja-fait chargé avant le plan, plus de blocage après)
    ("b plan sans deja-fait ne bloque plus", PLAN, [demande("la suite"), SQL], True),
    ("b plan avec deja-fait", PLAN, [demande("la suite"), SKILL, SQL], True),
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
    # f : horizon
    ("f action reportée", PLAN_REPORT, [demande("la suite"), SKILL, SQL], False),
    ("f composition d'un match de demain", PLAN_DEMAIN, [demande("la suite"), SKILL, SQL], True),
    ("f bloc Si hors colonne Action", PLAN + "\n**Si** :\n- titre acquis : faire tourner les jeunes plus tard.\n",
     [demande("la suite"), SQL], True),
    ("f tableau Si | Action non lu", PLAN + "\n| Si | Action |\n|---|---|\n| titre acquis | jeunes la semaine prochaine |\n",
     [demande("la suite"), SQL], True),
    ("f bloc Plan de saison", "### Plan de saison\nTitre, puis jeunes plus tard.\n\n" + PLAN,
     [demande("la suite"), SQL], True),
    ("f report dans Action après un bloc Si", "**Si** :\n- titre acquis.\n\n### Ce soir\n" + PLAN_REPORT,
     [demande("la suite"), SQL], False),
    # g : « je ne peux pas »
    ("g je ne peux pas sans preuve", "Je ne peux pas lire la base.", [demande("stats")], False),
    ("g je ne peux pas avec issue", "Je ne peux pas dire, je ne sais pas encore : je le trouve avec dossier.py.", [demande("stats")], True),
    # h : type d'agent
    ("h general-purpose", "Lancé.", [demande("analyse"), outil("Agent", {"subagent_type": "general-purpose"})], False),
    ("h type propre", "Lancé.", [demande("analyse"), outil("Agent", {"subagent_type": "match"})], True),
    ("h type introuvable déclaré", "Le type veille est introuvable, j'utilise general-purpose.",
     [demande("analyse"), outil("Agent", {"subagent_type": "general-purpose"})], True),
    # i : heredoc
    ("i heredoc qui écrit", "Fait.", [demande("écris"), outil("Bash", {"command": "cat > a.md <<'EOF'\nx\nEOF"})], False),
    ("i heredoc de lecture", "Fait.", [demande("lis"), outil("Bash", {"command": "python - <<'EOF'\nprint(1)\nEOF"})], True),
    ("j absence sans requête", "La Preview n'est pas en base.", [demande("preview ?")], False),
    ("j absence après requête", "La Preview n'est pas en base.",
     [demande("preview ?"), outil("Bash", {"command": "python -I pipelines/sql.py \"select page_type from bronze.raw_pages\""})], True),
    # k : registre fait
    ("k saisie déclarée sans registre", "Noté, bonne soirée.", [demande("les deux compos sont faites")], False),
    ("k j'ai exporté sans registre", "Merci.", [demande("j'ai exporté le personnel")], False),
    ("k saisie déclarée avec registre", "Noté.", [demande("j'ai saisi l'amical"), EDIT_OUT], True),
    ("k conception qui parle de fait", "Hook ajouté.", [demande("conçois le hook, j'ai fait le plan")], True),
    # l : catégories du « que faire »
    ("l plan incomplet", PLAN, [demande("que faire"), SQL], False),
    ("l plan complet", PLAN_COMPLET, [demande("que faire"), BV_SQL], True),
    ("l catégorie vide nommée sans requête", PLAN_PRESQUE, [demande("que faire")], False),
    ("l catégorie vide nommée après requête", PLAN_PRESQUE, [demande("que faire"), BV_SQL], True),
    ("l BasketVibe sans ligne Composition", PLAN_SANS_COMPO, [demande("que faire"), BV_SQL], False),
    ("l autre jeu, Composition dans le commentaire", PLAN_SANS_COMPO.replace("BasketVibe", "Hardwood"),
     [demande("que faire"), outil("Bash", {"command": "python -I pipelines/sql.py \"select * from gold.hw_agenda\""})], True),
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
