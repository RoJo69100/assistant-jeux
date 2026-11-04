---
name: feedback-hn-matchs-scouts-pas-finances
description: Hockey Nation en cours de saison : ne se préoccuper que des matchs et des scouts ; pas d'exports finances/salary cap/coaching staff ; proposer seul les prospects à scouter dès qu'un scout a fini
metadata:
  type: feedback
---

Hockey Nation, hors début de saison ou recrutement : l'utilisateur ne veut **que les matchs et le scouting**. Ne pas lui demander d'exports Salary cap, Club finances, Coaching staff, Contract talks (« ces trucs de merde », 2026-11-04).

**Why :** ces écrans ne servent qu'en début d'année ou pour recruter ; les redemander l'a énervé. Il a aussi reproché de ne pas avoir remarqué que plusieurs scouts avaient fini leur mission.

**How to apply :**
- À chaque « que faire » Hockey Nation : analyser tous les matchs terminés des 4 équipes depuis le dernier brief (`silver.hn_games`, `team_level`), pas un échantillon.
- Lire l'export `office_scouting` : tout scout avec « Assign » est libre ; lui proposer seul un prospect de `gold.hn_scout_targets` (un par scout, top 6 de la classe d'abord, poste+nation d'abord, sans doublon). `silver.hn_scouting_assignments` peut contredire la page : la page l'emporte.
- **Un scout ne reçoit qu'un prospect de SON poste** (puis sa nation) : jamais un RD américain sur un C coréen (colère 2026-11-04). Le besoin d'équipe départage entre prospects du même poste, il ne déplace pas un scout vers un autre poste. Le score maison (stats clés par poste, spéciales joueur/coach) vise **l'effectif de l'utilisateur**, pas seulement la draft.
- Voir [[feedback-initiative-multi-jeux]] et [[project-veille-integrale-autres-jeux]].
