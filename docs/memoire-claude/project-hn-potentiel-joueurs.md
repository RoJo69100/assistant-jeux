---
name: project-hn-potentiel-joueurs
description: "Hockey Nation — méthode de potentiel min/max d'un joueur (règle de l'utilisateur) et colonne Futur PRO/FRM/VIRER ; à appliquer avant tout échange"
metadata:
  node_type: memory
  type: project
  originSessionId: a6a6af01-9d37-4493-819e-15d2dc04d3dd
  modified: 2026-10-25T15:36:53.029Z
---

Règle de l'utilisateur du 2026-10-25 pour le potentiel d'un joueur : le talent faible fixe un plancher à toutes les autres compétences ; les deux talents forts fixent un plafond (le plus bas des deux plafonds, ex. 9 et 10 → 9). Minimum = compétences non plafonnées montées au plancher ; maximum = montées au plafond. Exemple Kabát : 68 → minimum 73, maximum 89. Spinka vu par l'utilisateur : 72 → 74 / 83 (ma règle donne 76 / 84, écart non résolu). Verdict Fort / Solide / Moyen / Nul par le minimum, plus colonne Futur : PRO, FRM ou VIRER.

**Obligatoire :** faire ce calcul pour toute recrue (draft, U17 qui arrive, échange, agent libre) et le refaire souvent quand l'utilisateur le demande (états d'équipe, avant un échange, une montée ou un renvoi) ; ne pas attendre qu'il le réclame.

**Why:** l'utilisateur veut savoir si un joueur à trader ou à garder vaut le coup, et où il a sa place plus tard (PRO, FRM, renvoi).
**How to apply:** charger le skill `hockeynation-potentiel-joueurs` (script `potentiel.py`, `tableau.py`) avant tout échange, montée d'U21 ou choix de draft ; donner minimum, maximum, spéciales, verdict, futur. Voir [[feedback-hn-format-equipes-coachs-scouts]].
