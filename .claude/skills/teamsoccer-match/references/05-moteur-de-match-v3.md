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

