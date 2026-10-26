# Hockey Nation — demande Étude des adversaires (2026-10-23)

Jeu : **Hockey Nation**. Tu es l'agent chargé de l'étude des adversaires. Lis d'abord `.claude/skills/hockeynation-adversaires/SKILL.md` (méthode, compétences clés confirmées, données), `docs/fiches/hockeynation/commun.md`, `outputs/hockeynation/learnings.md`, puis les briefs du jour `outputs/hockeynation/briefs/2026-10-23-*.md` (match, effectif, tactique-v2). Skills liés : `hockeynation-joueurs`, `hockeynation-coachs-entrainement`, `hockeynation-match-calendrier`.

## À étudier
Les 4 clubs exportés : **Leszno Bulls** (référence, +27 de score total sur nous), **Seoul Pilots**, **Miami Maidiacs**, **Jessup Baldos**. Un bloc par club, même format.

## Pour chaque club (tableau court, joueurs et coachs nommés)
1. Point fort : preuve chiffrée (score total par poste contre le nôtre, `gold.hn_club_compare` / `gold.hn_depth_chart`), et notre réponse.
2. Staff : head coach (OFP, DFP, BAT, PP, PK ; compétences spéciales actives), assistants, comparés aux nôtres (Aalst/Bondar plan). Ce que PP/PK du coach adverse change contre notre PP (20,7 %) et notre PK (76,3 %).
3. Gardiens : END du titulaire (seuil 7+), part de ses matchs joués dans nos rencontres (`silver.hn_game_detail`), compétences spéciales.
4. Résultats contre nous dans les 33 matchs PRO (`silver.hn_game_detail`) : score, tirs, unités spéciales, joueurs adverses décisifs. Ne pas dépasser ce que les données montrent.
5. Discipline (DSC faible = pénalités) : joueurs nommés.
6. Un réglage concret pour nos lignes A et nos unités spéciales (lineup du brief tactique-v2) contre ce club.

## Fin du brief
(a) Ce qui manque, avec la façon de le réunir ensemble ; (b) règles non trouvées ; (c) 3 enseignements (C-nnn) à ajouter au journal `outputs/hockeynation/learnings.md`.

Règles : aucun flou, aucun « peut-être », un réglage par ligne ; source citée pour chaque règle ; donnée absente = ligne « il me manque X, on le réunit ensemble comme ça : … ». Nos joueurs seulement dans nos lignes (aucun joueur des adversaires). Écris le livrable `outputs/hockeynation/briefs/2026-10-23-adversaires.md` avec l'outil Write ; ne modifie aucun autre fichier hors learnings ; pas de commit.
