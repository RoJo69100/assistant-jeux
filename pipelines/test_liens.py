"""Règle des liens (25/11) : tout fichier d'outputs/ cité dans un plan est un lien complet sur main.
Échoue si un plan écrit (BasketVibe ou Hockey Nation) cite un fichier sans lien, vers une autre branche, ou vers un fichier absent.

Lancer : python -I pipelines/test_liens.py   (code 1 si un cas se trompe)
"""
import datetime as dt
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import liens as L  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent
PLANS = ["outputs/basketvibe/que-faire-*.md", "outputs/basketvibe/aujourdhui-*.md", "outputs/hockeynation/aujourdhui-*.md"]
DEPUIS = "2026-11-25"  # règle posée le 25/11 : les plans antérieurs ne sont pas réécrits


def cas():
    t = "Lis outputs/basketvibe/briefs/2026-11-25-transferts.md, police-2026-11-25.md et https://github.com/RoJo69100/assistant-jeux/blob/claude/x/outputs/a.md"
    yield "détecte un chemin nu, un nom seul et un lien de branche", len(L.sans_lien(t)) == 3
    u = L.lier(t)
    yield "lier : plus aucun fichier sans lien", L.sans_lien(u) == []
    yield "lier : le lien est complet et sur main", "](https://github.com/RoJo69100/assistant-jeux/blob/main/outputs/basketvibe/briefs/2026-11-25-transferts.md)" in u
    yield "lier : un lien de branche est ramené sur main", "blob/main/outputs/a.md" in u and "blob/claude/" not in u
    yield "lier : idempotent", L.lier(u) == u
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "outputs").mkdir()
        (Path(tmp) / "outputs" / "x.md").write_text("x", encoding="utf-8")
        yield "ordre plan écrit puis fusion : lien vers un fichier présent accepté, absent signalé", \
            L.cibles_absentes(L.md("outputs/x.md") + " " + L.md("outputs/y.md"), tmp) == ["outputs/y.md"]
    import etat_jour as ej
    yield "etat_jour : lien de fiche sur main", "/blob/main/" in ej.lien_fiche("briefs/a.md") and L.sans_lien(ej.lien_fiche("briefs/a.md")) == []
    import aujourdhui_hockeynation as hn
    yield "Hockey Nation : quatre équipes à fiche tactique", [e for e, _, _ in hn.FICHES_TACTIQUE] == ["PRO", "ISL", "ISL21", "HUA"]
    for motif in PLANS:
        for f in sorted(RACINE.glob(motif)):
            if f.name[-13:-3] < DEPUIS:
                continue
            txt = f.read_text(encoding="utf-8")
            rel = f.relative_to(RACINE)
            yield f"{rel} : aucun fichier cité sans lien sur main", L.sans_lien(txt) == []
            yield f"{rel} : chaque lien vise un fichier présent (il sera sur main après la fusion)", L.cibles_absentes(txt) == []
    hn_plan = RACINE / f"outputs/hockeynation/aujourdhui-{DEPUIS}.md"
    if hn_plan.exists():
        t2 = hn_plan.read_text(encoding="utf-8").split("temps 2", 1)[-1]
        tact = [l for l in t2.splitlines() if "| Tactique |" in l]
        yield "Hockey Nation temps 2 : chaque ligne Tactique porte le lien de sa fiche", bool(tact) and all("/blob/main/outputs/hockeynation/briefs/" in l and "-tactique-" in l for l in tact)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    jeux = list(cas())
    echecs = 0
    for n, ok in jeux:
        echecs += not ok
        print("OK " if ok else "ECHEC ", n)
    print(f"{len(jeux) - echecs}/{len(jeux)}")
    sys.exit(1 if echecs else 0)
