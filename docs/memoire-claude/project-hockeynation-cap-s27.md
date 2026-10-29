---
name: project-hockeynation-cap-s27
description: "Hockey Nation S27 — rachat Eskelinen (pénalité 1 285 000 $/saison S27-S29), déficit de plafond restant, Dosymkhanov en U21, offres de coachs envoyées le 29/10"
metadata:
  node_type: memory
  type: project
  originSessionId: e9f79813-9a90-4327-8302-c94389b83069
  modified: 2026-10-29T15:37:41.230Z
---

Le 2026-10-29 l'utilisateur a : racheté Eskelinen (pénalité 1 285 000 $ par saison en S27, S28 et S29, à garder dans tous les calculs de plafond), descendu Dosymkhanov en U21, envoyé les offres de coachs Meng (U21 assistant, remplace Ahn), Howe (U21 head), Robertson et Dunka (U17). Strobel offert en PRO à la place de Baier. Les échanges (Pålsson, Eskelinen) n'ont pas abouti : plus de trade. Il dit qu'il lui manque encore 2 185 000 $ de plafond (mon calcul depuis l'export : 3 470 000 $, le jeu fait foi). Jasiński et Carpentier ne peuvent pas bouger ; Hakkarainen et Kaneda peuvent aller en FRM ou U21.

**Why:** les vues gold se recalculent à partir de `silver.hn_declared` ; sans cette mémoire je referais les mêmes erreurs (Carpentier, Jasiński, Vrábel en U21).
**How to apply:** lire `silver.hn_declared` avant tout plan Hockey Nation ; mettre à jour la table à chaque « j'ai fait X ». Voir [[feedback-hockeynation-rendu-tableaux]].
