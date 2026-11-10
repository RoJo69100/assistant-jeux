"""Contrôle de sensibilité de la carte de faisabilité (question 2) : prix d'un joueur sans les ventes à prix symbolique.

Même modèle que pipelines/etudes/carte_faisabilite.py (log du prix ~ PS + âge + poste, référence PG, bootstrap par jour de vente),
ventes hors agents libres, prix >= seuil. Usage : python -I pipelines/etudes/carte_faisabilite_marche_seuil.py [seuil] [tirages] [graine]
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # pipelines/ ; python -I ne l'ajoute pas
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from etude_evenements_basketvibe import lire  # noqa: E402


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    seuil = float(sys.argv[1]) if len(sys.argv) > 1 else 1000
    B = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    graine = int(sys.argv[3]) if len(sys.argv) > 3 else 20261110
    print(f"graine = {graine} ; tirages bootstrap = {B} ; seuil de prix = {seuil:.0f}")
    H = lire("select sold_on, position, age, ps, fee, was_free_agent from gold.bv_transfer_history where ps is not null and fee > 0")
    H = H[~H.was_free_agent.astype(str).str.lower().isin(["true", "t", "1"]) & H.position.notna()].copy()
    for c in ("age", "ps", "fee"):
        H[c] = pd.to_numeric(H[c]).astype(float)
    n_tot = len(H)
    H = H[H.fee >= seuil].copy()
    H["sold_on"] = H.sold_on.astype(str).str[:10]
    H["per"] = np.where(H.sold_on <= "2026-10-26", "saison 1 (<= 26/10)", "saison 2 (>= 27/10)")
    print(f"- ventes gardées : {len(H)} sur {n_tot}")
    rng = np.random.default_rng(graine)
    for per, h in H.groupby("per"):
        h = h.reset_index(drop=True)
        autres = [p for p in sorted(h.position.unique()) if p != "PG"]
        X = np.column_stack([np.ones(len(h)), h.ps.values, h.age.values] + [(h.position.values == p).astype(float) for p in autres])
        y = np.log(h.fee.values)
        fit = lambda ix: np.linalg.lstsq(X[ix], y[ix], rcond=None)[0]  # noqa: E731
        c0 = fit(np.arange(len(h)))
        r2 = 1 - ((y - X @ c0) ** 2).sum() / ((y - y.mean()) ** 2).sum()
        lst = [np.flatnonzero(h.sold_on.values == u) for u in pd.unique(h.sold_on.values)]
        tirs = np.array([fit(np.concatenate([lst[i] for i in rng.integers(0, len(lst), len(lst))])) for _ in range(B)])
        print(f"\n### {per} : {len(h)} ventes, {len(lst)} jours, R2 = {r2:.2f}")
        print("| facteur | effet sur le prix | IC 95 % |")
        print("|---|---|---|")
        for j, nm in enumerate(["const", "ps", "age"] + autres):
            if nm == "const":
                continue
            sc = 5.0 if nm == "ps" else 1.0
            lo, hi = np.percentile(tirs[:, j] * sc, [2.5, 97.5])
            lab = {"ps": "+5 PS", "age": "+1 an"}.get(nm, f"{nm} contre PG")
            print(f"| {lab} | {math.expm1(c0[j] * sc):+.1%} | [{math.expm1(lo):+.1%} ; {math.expm1(hi):+.1%}] |")


if __name__ == "__main__":
    main()
