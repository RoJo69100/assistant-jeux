"""Lecture de la base de connaissances par thème (refonte v2, étape 4.4) : remplace le chargement en bloc
des skills *-communaute et de connaissance.md.

Rend TOUTES les affirmations du thème (domaine exact, sinon recherche plein texte française) avec le compteur
« N total / N affichées » que la police vérifie. Une ligne par affirmation : #id, confiance, statut, date, auteur, texte.
Lecture : psycopg (SUPABASE_DB_URL_RO) si disponible, sinon REST public.kb_search (SUPABASE_SECRET_KEY).

Usage : python -I pipelines/kb.py <jeu> <thème> [--min-conf 0.5] [--domaines]
        jeu : nom complet ou alias (bv, hn, ts, sz, dm, hw) ; --domaines liste les thèmes du jeu et leur nombre.
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from migrer_learnings import env  # noqa: E402

ALIAS = {"bv": "basketvibe", "hn": "hockeynation", "ts": "teamsoccer", "sz": "sixzeroleague", "szl": "sixzeroleague",
         "dm": "derbymanager", "hw": "hardwood"}
STATUT = {"confirme": "conf", "complete": "compl", "contredit": "CONTREDIT", "en_doute": "doute", "obsolete": "obs"}


def appel(fonction: str, args: dict, sql: str, params: tuple):
    try:
        import psycopg
        from sql import url_ro
        with psycopg.connect(url_ro(), connect_timeout=15) as c, c.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchone()[0]
    except (Exception, SystemExit):
        pass
    url, cle = env("SUPABASE_URL"), env("SUPABASE_SECRET_KEY")
    if not url or not cle:
        sys.exit("❌ ni SUPABASE_DB_URL_RO ni SUPABASE_URL + SUPABASE_SECRET_KEY")
    req = urllib.request.Request(url.rstrip("/") + f"/rest/v1/rpc/{fonction}", method="POST",
                                 data=json.dumps(args).encode(),
                                 headers={"apikey": cle, "Authorization": f"Bearer {cle}",
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"❌ Supabase {e.code} : {e.read().decode(errors='replace')[:300]}")


def chercher(jeu: str, theme: str, min_conf: float) -> dict:
    return appel("kb_search", {"p_game": jeu, "p_theme": theme, "p_min_conf": min_conf},
                 "select public.kb_search(%s, %s, %s)", (jeu, theme, min_conf))


def ligne(c: dict) -> str:
    texte = re.sub(r"\s+", " ", c["text"].replace("`", "")).strip()
    date = (c.get("said_at") or "")[:10]
    extra = f" ⚔#{','.join(map(str, c['contradicts']))}" if c.get("contradicts") else ""
    extra += f" [données : {c['data_verdict']}]" if c.get("data_verdict") else ""
    return (f"#{c['id']} {float(c['confidence']):.2f} {STATUT.get(c['status'], c['status'])} {date} "
            f"{c.get('author') or c['source_kind']} — {texte}{extra}")


def rendu(jeu: str, theme: str, r: dict, min_conf: float) -> str:
    tete = (f"{jeu} · {theme} : {r['total']} total / {r['affichees']} affichées "
            f"({r['obsoletes']} obsolètes, {r['sous_seuil']} sous {min_conf:.2f})")
    return "\n".join([tete] + [ligne(c) for c in r["claims"]])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("jeu")
    ap.add_argument("theme", nargs="?", default="")
    ap.add_argument("--min-conf", type=float, default=0.0)
    ap.add_argument("--domaines", action="store_true")
    a = ap.parse_args(argv)
    jeu = ALIAS.get(a.jeu.lower(), a.jeu.lower())
    if a.domaines or not a.theme:
        doms = appel("kb_domains", {"p_game": jeu}, "select public.kb_domains(%s)", (jeu,))
        print(f"{jeu} : " + " · ".join(f"{d['domain']} {d['n']}" for d in doms))
        return 0
    r = chercher(jeu, a.theme, a.min_conf)
    print(rendu(jeu, a.theme, r, a.min_conf))
    return 0 if r["total"] else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
