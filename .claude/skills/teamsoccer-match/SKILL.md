---
name: teamsoccer-match
description: Règles Team Soccer (football) de la composition et du moteur de match — 6 formations, mode Simple et 4 presets, mode Avancé (consignes par joueur dans 5 zones), style d'équipe, effets des formations (défense, finition, possession), duels et probabilités du moteur v3, bonus de poste et de consigne, banc et remplacements programmés, changements à la mi-temps, match pré-calculé 2 h avant, barres de secteurs, bots, constance du manager (moral). À charger pour construire une composition, préparer un match ou expliquer un résultat.
---

# Team Soccer — composition et moteur de match

Sources : voir teamsoccer-joueurs (**[G]** guide officiel capté le 2026-10-19, **[F]** forum global, **[P]** page du jeu, **[Obs]** nos données). Le moteur v3 a changé plusieurs fois (2026-05-28, 2026-06-02, 2026-08-27, 2026-09-22, 2026-10-18) : en cas de doute, la date la plus récente l'emporte.

## Préparer un match [G:Composition : mode Simple et mode Avancé]
- Matchs → le match → Configurer. **Enregistrer** sinon rien n'est appliqué ; on peut nommer une composition et la cocher « par défaut » pour les matchs suivants (3 emplacements, 5 en Premium) [G:Commencer à jouer 3.1].
- **Le match est pré-calculé environ 2 heures avant le coup d'envoi** : une composition ou des remplacements enregistrés après ne comptent pas, la version précédente s'applique [F:2026-06-28 Admin-Dev] [F:2026-08-15 PIPO68]. Depuis fin juin, une composition modifiée avant le coup d'envoi déclenche un nouveau calcul (cron toutes les 5 min) [F:2026-06-28 Admin-Dev] ; règle prudente : **tout enregistrer au moins 2 h avant**.
- Sans composition enregistrée, la composition par défaut est utilisée [F:2026-07-18 Paolo, tournois].
- « Composition automatique » place les 11 meilleurs et remplit le banc [G].
- Garder un **banc configuré en permanence dans la composition par défaut** (recommandation de l'admin) [F:2026-06-28 Admin-Dev].

## Formations [G:Commencer à jouer 3.1]
1-4-4-2 · 1-3-5-2 · 1-3-4-3 · 1-4-3-3 · 1-4-5-1 · 1-5-4-1 (1er chiffre = gardien). Changer de formation replace automatiquement les joueurs par ligne.

### Effets des formations sur le match [F:2026-06-02 Admin-Dev]
| Ligne | 3 joueurs | 4 joueurs | 5 joueurs |
|---|---|---|---|
| Défense | Défense −10 % | 0 | Défense +10 % |

| Attaque | 1 joueur | 2 joueurs | 3 joueurs |
|---|---|---|---|
| Finition | −10 % | 0 | +10 % |

**Possession** (sur environ 30 actions par match) : à milieu égal, l'équipe à domicile a **+4 actions**. Domicile 3 milieux vs extérieur 4 → égalité ; 3 vs 5 → +4 pour l'extérieur ; 4 vs 3 → +6 pour le domicile ; 5 vs 3 → +8 pour le domicile. Plus de milieux = plus de ballons.

## Mode Simple et presets [G:Composition] [F:2026-06-06 Admin-Dev]
- 4 presets : **Ultra défensif** (repli, dégagements, longs ballons) · **Équilibré** (passes et dribbles ; le guide conseille de commencer par lui) · **Offensif** (latéraux hauts, dribbles, centres) · **Pressing haut** (ligne haute, récupération haute). Le preset remplit les consignes des 11 selon le poste occupé.
- Le guide affirme que Simple et Avancé donnent exactement le même rendement. Mais les deux modes sont **indépendants** : passer de l'un à l'autre repart de zéro, et des remplacements d'un mode peuvent rester actifs dans l'autre [F:2026-08-15 Paolo] [F:2026-08-17 PIPO68]. L'admin conseille d'apprendre le mode Avancé [F:2026-08-15 PIPO68]. **Après enregistrement, vérifier l'onglet Avancé.**

## Mode Avancé [G:Composition] [G:Commencer à jouer 3.1]
3 étapes : Positionnement (11 + banc) → Consignes tactiques → Consignes de jeu.
- **Consignes par joueur dans 5 zones** : Ultra défensive, Défensive, Médiane, Offensive, Finition. Actions : dégager, passer (choisir le destinataire), dribbler (conduire), centrer (choisir le destinataire), tirer.
- **Style de l'équipe** : Très défensif, Défensif, Neutre (défaut), Offensif, Très offensif. **Ampleur contradictoire** : le guide (actuel) dit ±10 % / ±5 % sur Défense et Finition ; l'annonce moteur v3 du 2026-05-28 dit ±25 % / ±12,5 % (Très défensif : Défense ×1,25, Finition ×0,75). Les bots jouent Neutre [F:2026-05-28 Admin-Dev].
- Conseil du guide : partir d'un preset Simple et ne retoucher que 2 ou 3 joueurs.
- Pour qu'un défenseur ou un milieu marque, lui donner « dribbler… puis tirer » dans les zones ; mais les attaquants reçoivent alors moins de ballons [F:2026-09-15 PIPO68].

## Moteur de match v3 [G:Moteur de match] [F:2026-05-28 Admin-Dev]
Match pré-calculé ; le visionneur rejoue seulement. Le jeu avance par zone selon la consigne du porteur.
| Action | Compétences comparées |
|---|---|
| Duel avec ballon | Conduite (porteur) contre Défense (défenseur le plus proche) |
| Réception d'une passe ou d'un ballon disputé | Contrôle des deux joueurs ; la Passe du passeur augmente la chance de son coéquipier |
| Ballon aérien | Tête |
| Tir | Finition contre Gardien |
| Ballon perdu dans le vide (mauvaise passe en profondeur) | Vitesse : le plus rapide et le plus proche l'emporte |
| Dégagement | Éloigne le danger, ballon sans destinataire |
- **Probabilité d'un duel = attaque / (attaque + défense)**, aléa ±5 % (±10 % avant le 2026-05-28).
- **Tir** : but = Finition / (Finition + Gardien + 25), avec plafond (constante +60 au dénominateur, ~30 % au maximum, 55 % absolu).
- **Compression du score** : quand l'équipe dominante mène, son efficacité baisse : +2 buts ×0,80, +3 ×0,55, +4 ×0,35, +5 ×0,20. Penalties : fréquence 4 %, conversion 72 % (annonce du 2026-05-28 ; l'admin citait 85 % le 2026-06-27).
- **Bonus de poste** (zone naturelle) : DC en zone défensive et latéral sur son flanc : Défense ×1,15 ; milieu au milieu ×1,10 ; ailier qui défend son flanc ×1,05 ; attaquant en zone de finition : Finition et Tête ×1,15 ; ailier qui centre depuis l'aile : Centres ×1,20 ; milieu qui tire : Finition ×1,05. Hors zone naturelle : pas de bonus.
- **Consigne cohérente** avec la meilleure compétence du joueur (dribble pour un bon dribbleur, tir pour un buteur…) : ×1,10 ; incohérente (ex. DC qui dribble) : ×0,90. Sans consigne : pas de multiplicateur.
- Forme et fatigue : voir teamsoccer-joueurs (Forme = plafond, Endurance = baisse toutes les 5 min).
- Le guide conclut : des joueurs complets (beaucoup de compétences) réussissent plus d'actions.

## Bots et managers récents
- Club BOT : toutes ses compétences ×0,90 [F:2026-05-28 Admin-Dev] ; en plus, Gardien et Finition du bot −10 %, −18 % ou −25 % selon l'écart de niveau, dans tous les matchs depuis le 2026-09-07 [F:2026-09-07 Admin-Dev]. Les bots perdent plus de 90 % de leurs matchs.
- Manager humain inscrit depuis moins de 14 jours : compétences de champ ×1,05 [F:2026-05-28 Admin-Dev].
- Un club inactif depuis 45 jours devient BOT ; un nouveau manager reprend un club bot [F:2026-08-29 PIPO68].

## Banc et remplacements [G:Composition 5] [F:2026-06-27 Admin-Dev]
- Choisir les remplaçants **et le poste que chacun couvre**. Un bon banc couvre gardien, défenseur, milieu, attaquant.
- **Blessure** : remplacement automatique (poste couvert exact → même ligne → n'importe quel remplaçant). Banc vide → l'équipe joue à 10.
- **Remplacements programmés** (minute, sortant, entrant) : à configurer à part ; mettre des joueurs sur le banc ne suffit pas. Utile avec la fatigue : un remplaçant entre avec tout son plafond de Forme.
- **Mi-temps** : pause de 5 minutes avec changements tactiques et remplacements, dans tous les matchs officiels, sélections comprises, depuis le 2026-10-16 [F:2026-10-16 PIPO68]. Il faut regarder le match en direct pour s'en servir.

## Barres de secteurs [G:Équilibre des secteurs]
- 8 barres 0–100 sous le terrain : Gardien, Défense centrale, Latéral gauche, Latéral droit, Milieu, Aile gauche, Aile droite, Attaque. Calculées avec les compétences du joueur à cet emplacement et le **nombre de joueurs** dans la zone (3 centraux renforcent l'axe, 5 milieux dominent le centre). Zone vide = moitié de la moyenne des zones voisines (marquée ~).
- Le rapport de match compare les 8 secteurs aux adversaires. **Purement informatif : ne change pas la simulation** [G].

## Constance du manager (MC) et moral [G:MC] [F:2026-09-08 PIPO68]
5 cercles de 3 points (15 au total), page Statistiques du club. Le niveau au moment du match augmente les compétences des joueurs **jusqu'à +10 points**.
| Cercle | Points |
|---|---|
| 🔴 Régularité | Connexions consécutives : 5 jours+ = 3, 3–4 = 2, 1–2 = 1 |
| 🟠 Participation | 1 par match joué dans la semaine par le premier club, max 3 (ligue, coupes, amicaux, tournois, Room Madness) |
| 🟡 Économie | Trésorerie : > 2 500 000 $ = 3, > 1 500 000 $ = 2, > 200 000 $ = 1 |
| 🔵 Gestion | 1 composition enregistrée + 1 entraînements assignés + 1 activité de la semaine (marché, enchère ou académie) |
| 🟢 Classement dans le pays | Top 9 = 3, 10e–20e = 2, 21e–40e = 1 |
- Le moral repart chaque lundi [F:2026-09-14 PIPO68]. Selon une étude de la communauté, vendre des joueurs baisserait l'esprit d'équipe [F:2026-07-01 PIPO68] (non confirmé).
- Conséquence pratique : se connecter chaque jour, jouer l'amical de la semaine, enregistrer la composition et l'entraînement, faire une action de marché ou d'académie. **Une trésorerie négative donne 0 au cercle jaune** [Obs : nos deux clubs sont négatifs au 2026-10-19].

## [Obs] Nos données
- API : `lineups` (formation, style, positions, banc, remplaçants), `match_lineups` (consignes tactiques par match), `matches` (scores, tirs au but, coupe, amical).
