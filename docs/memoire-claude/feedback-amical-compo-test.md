---
name: feedback-amical-compo-test
description: "Amical BasketVibe = composition de TEST (jamais le cinq de coupe/ligue), même FORMAT tactique, un seul test, adversaires = « les 12 : <focus en mot>, <zone> » en mots, jamais mélangé avec des chiffres, sans noms ni aperçu à demander"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 843acf0f-3771-498a-b909-79972f0d77c2
  modified: 2026-10-31T19:12:40.716Z
---

Pour un amical, je rends tout de suite le tableau joueur × Q (format parfait [[feedback-format-tactique-parfait]]) avec une composition de test : remplaçants qui jouent, étoiles au repos ou en prolongation, réglages par joueur repris du dernier amical (`gold.bv_saisie_joueurs`). Adversaires : tableau Adversaire | Poste | Focus défensif (1–5) | Zone, UNE LIGNE PAR JOUEUR (exigé par le hook `pipelines/forme.py`, 2026-10-31 ; noms inconnus = chercher en base d'abord, sinon « Adversaire 1..12 » dans l'ordre de l'écran) ; colonne « Minutes » (pas « Min »). Un seul test : zone (Rim/Middle/Perimeter, suivie dans `gold.bv_zone_jouee`) ou un réglage de nos joueurs.

**Why:** 2026-10-29, colère : je lui ai donné le cinq de la coupe pour l'amical, demandé l'aperçu de l'adversaire, et attendu qu'il réclame le tableau. « L'adversaire on s'en fout », « je te dis de reprendre le même format, pas les mêmes données ».

**How to apply:** jamais demander d'export pour préparer un amical ; analyser les résultats d'amicaux pour décider plus tard ; pas de preset d'amical [[feedback-rendu-demain-seulement]].
