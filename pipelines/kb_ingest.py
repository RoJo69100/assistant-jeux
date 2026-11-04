"""Ingestion Discord → kb.claim par lots (refonte v2, étape 4.3). Aucun appel de modèle ici : le script prépare
les lots, l'agent `veille` (Sonnet) extrait les affirmations en JSON strict, le script valide et importe.

  estimer [--min-len 60]                 volume restant par jeu après le curseur (messages, caractères, ≈ jetons)
  lot <jeu> [--taille 50] [--min-len 60] lot suivant après le curseur, en texte compact, + consigne JSON
  charger <jeu> <fichier.json> --jusqua <id>
                                         valide le JSON de l'agent, importe (kb_import) et avance le curseur à <id>

JSON attendu : [{"text": "…", "domain": "<thème>", "author": "…", "said_at": "AAAA-MM-JJ", "msg_id": "…",
                 "status": "confirme|complete|contredit|en_doute|obsolete"}] ; domaine parmi migrer_kb.THEMES.
Le backfill complet se lance seulement après accord écrit de l'utilisateur sur le budget (plan 4.3).
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kb  # noqa: E402
import migrer_kb  # noqa: E402

SOURCE = "bronze.discord_messages"
OFFICIELS = sorted({a for v in migrer_kb.OFFICIELS.values() for a in v} | {"gazellemag", "hnadmin", "d0ghouse"})
DOMAINES = {d for d, _ in migrer_kb.THEMES} | {"divers"}
STATUTS = {"confirme", "complete", "contredit", "en_doute", "obsolete"}
CONSIGNE = ("Extrais chaque affirmation utile sur le jeu (règle, mécanique, chiffre, conseil daté). Une affirmation par "
            "objet, en français, sans inventer : JSON strict, liste d'objets {text, domain, author, said_at, msg_id, "
            f"status}} ; domain ∈ {sorted(DOMAINES)} ; status = confirme si l'auteur est officiel ({', '.join(OFFICIELS)}), "
            "sinon en_doute (complete si un autre auteur confirme dans le lot). Bavardage, blagues, questions sans "
            "réponse : rien. Liste vide si rien.")


def estimer(min_len: int) -> list[dict]:
    return kb.appel("kb_estimer", {"p_min_len": min_len, "p_officiels": OFFICIELS},
                    "select public.kb_estimer(%s, %s)", (min_len, OFFICIELS))


def curseur(jeu: str) -> str | None:
    return next((e["curseur"] for e in estimer(0) if e["game"] == jeu), None)


def lot(jeu: str, taille: int, min_len: int) -> list[dict]:
    apres = curseur(jeu)
    return kb.appel("kb_lot", {"p_game": jeu, "p_after": apres, "p_limit": taille, "p_min_len": min_len,
                               "p_officiels": OFFICIELS},
                    "select public.kb_lot(%s, %s, %s, %s, %s)", (jeu, apres, taille, min_len, OFFICIELS))


def valider(jeu: str, items: list) -> tuple[list[dict], list[str]]:
    ok, err = [], []
    for i, x in enumerate(items):
        if not isinstance(x, dict) or not str(x.get("text", "")).strip() or not x.get("msg_id"):
            err.append(f"#{i} : text et msg_id obligatoires")
            continue
        if x.get("domain") not in DOMAINES:
            err.append(f"#{i} : domaine {x.get('domain')!r} inconnu")
            continue
        st = x.get("status", "en_doute")
        if st not in STATUTS:
            err.append(f"#{i} : statut {st!r} inconnu")
            continue
        auteur = (x.get("author") or "").strip() or None
        officiel = auteur is not None and auteur.lower() in OFFICIELS
        ok.append({"game": jeu, "domain": x["domain"], "text": x["text"].strip()[:4000],
                   "source_kind": "devlog" if officiel else "discord",
                   "source_ref": f"{SOURCE}#{x['msg_id']}", "author": auteur, "said_at": x.get("said_at"),
                   "status": st, "import_key": hashlib.md5(f"{jeu}|discord|{x['msg_id']}|{x['text']}".encode()).hexdigest(),
                   "origine": {"source": SOURCE, "msg_id": str(x["msg_id"])}})
    return ok, err


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    e = sp.add_parser("estimer")
    e.add_argument("--min-len", type=int, default=60)
    lo = sp.add_parser("lot")
    lo.add_argument("jeu")
    lo.add_argument("--taille", type=int, default=50)
    lo.add_argument("--min-len", type=int, default=60)
    ch = sp.add_parser("charger")
    ch.add_argument("jeu")
    ch.add_argument("fichier")
    ch.add_argument("--jusqua", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "estimer":
        for x in estimer(a.min_len):
            print(f"{x['game']} : {x['messages']} messages ({x['officiels']} officiels), {x['caracteres']} caractères "
                  f"≈ {round(x['caracteres'] / 3.6 / 1000)} k jetons d'entrée, {-(-x['messages'] // 50)} lots de 50 ; "
                  f"curseur {x['curseur'] or 'aucun'}")
        return 0
    jeu = kb.ALIAS.get(a.jeu, a.jeu)
    if a.cmd == "lot":
        msgs = lot(jeu, a.taille, a.min_len)
        print(CONSIGNE)
        for m in msgs:
            print(f"[{m['id']}] {str(m['at'])[:10]} {m['channel']} {m['author']} : {' '.join(m['text'].split())}")
        print(f"— {len(msgs)} messages ; fin du lot : --jusqua {msgs[-1]['id'] if msgs else '(rien)'}")
        return 0 if msgs else 1
    items = json.loads(Path(a.fichier).read_text(encoding="utf-8"))
    ok, err = valider(jeu, items if isinstance(items, list) else [])
    if err:
        print("❌ JSON refusé, curseur inchangé :\n" + "\n".join(err))
        return 1
    r = migrer_kb.envoyer({"game": jeu, "claims": ok, "support": [],
                           "cursor": {"source": SOURCE, "last_id": a.jusqua}})
    print(f"{len(ok)} affirmations envoyées → {r}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
