# Team Soccer — Chomelix Cows (team 18) — Hypothèse « Ounahi au but » — 2026-10-20

Étude seule : les compositions des coupes du 21 et 22/10 ne sont pas touchées.
À refaire si : un export change Gardien/Défense/Forme de Ounahi, R. Thomas, Simon, T. Thomas ou Dubois (nouvel export après le vendredi 2026-10-23) ; blessure ou suspension d'un de ces cinq ; achat d'un gardien ; correction de la règle OVR par sous-rôle (skill joueurs) ; adversaire du 26/10 connu (note).

## Verdict : l'hypothèse ne tient pas (prémisse fausse)
**Faits** [Obs SQL 2026-10-20, `silver.ts_players`, dernier jour] :
- Le meilleur gardien n'a pas Gardien 60 : **Romain Thomas (GK, 23 ans) a Gardien 100, Contrôle 66, Forme 98 ; c'est son OVR qui est 60** (les autres compétences sont basses : Défense 57, Vitesse 40, Endurance 51). Le brief Effectif du 2026-10-20 a donc comparé « Gardien 99 » à son OVR, pas à son Gardien.
- Ounahi (DEF, 19 ans) : Gardien 99, Contrôle 100, Défense 100, Tête 97, Vitesse 100, Endurance 100, OVR 90, Forme 98.
- Autres défenseurs : Simon (OVR 68, Déf 100, Contrôle 71), T. Thomas (66, Déf 100, Contrôle 59), Dubois (65, Déf 100, Contrôle 69), P. Leroy (56,8, Déf 63), Enzo Roux (43,3, Déf 82, Forme 74).

**Règles** :
- Tir : but = Finition / (Finition + Gardien + 25), plafond ~30 % (55 % absolu) [skill teamsoccer-match, Moteur v3]. Gardien 99 au lieu de 100 : gain nul, légère perte (ex. Finition 80 : 39,0 % avec 100 contre 39,2 % avec 99 avant plafond ; calcul de l'agent sur la formule).
- Compétences clés du gardien : Gardien puis Contrôle, Passe en secondaire [skill teamsoccer-joueurs]. Thomas : 100 / 66 ; Ounahi : 99 / 100. Seul le Contrôle (réception, duels au pied) change, et le skill ne chiffre pas son poids pour un gardien.
- Bonus de poste : DC en zone défensive, Défense ×1,15 ; aucun bonus de poste n'est listé pour le gardien [skill teamsoccer-match]. Ounahi quitterait donc un poste à bonus pour un poste sans bonus listé.
- Note de match calculée dans le sous-rôle naturel : jouer hors poste baisse la note (indicatrice seulement) [skill teamsoccer-joueurs, Notes de match]. L'OVR se calcule selon le sous-rôle naturel et le skill ne donne pas les compétences Étoile/Secondaires par sous-rôle [skill teamsoccer-joueurs, OVR] : on ne peut pas prédire un « OVR de gardien » d'Ounahi ; le OVR 90 ne se transpose pas au but.

**Avis** (confiance moyenne à bonne) :
- Gain au but : quasi nul (Gardien 99 contre 100). Éventuel plus : Contrôle 100 contre 66, effet non chiffré par les règles.
- Perte en défense : le 4e défenseur serait Leroy (Défense 63, Forme 100, 32 ans) ou Enzo Roux (Défense 82, OVR 43, Forme 74, ×0,92). Ounahi (Déf 100 ×1,15 DC) → Leroy : Défense de la ligne en forte baisse sur un poste, en plus de perdre Tête 97 sur les ballons aériens (ses 2 buts de la tête, L-001/L-002). Le DC de remplacement le plus crédible est Dubois ou T. Thomas s'ils ne sont pas déjà alignés (ils le sont probablement dans le 1-4-x) : le reliquat sort alors du banc.
- Conséquence côté gardien : R. Thomas, sorti du but, ne pourrait remplacer personne (Défense 57, Vitesse 40) : il serait un gaspillage ou un banc de luxe. Les 3 juniors gardiens (T. David 86, É. Roux 69, H. Martin 61) n'apportent rien en échange.
- Risques : 1) perte nette de Défense/Tête, 2) un seul échantillon de 90 minutes (bruit des tirs : peu d'événements), 3) en amical aucun risque de blessure [skill joueurs, F:2026-09-07] mais aucun carton non plus : le test ne dit rien sur la gestion des cartons, 4) un match d'adversaire inconnu (Ajax Amsterdam, `opponent_rating` nul, `gold.ts_upcoming`) ne permet pas de fixer une base.

## Le trou au poste GB n'existe pas
R. Thomas Gardien 100 couvre déjà le but. La vraie fragilité est la **profondeur** : un seul gardien adulte, remplaçant à Gardien 86 (T. David, OVR 47,3). Le plan B actuel reste T. David (banc `coverRole` gb), pas Ounahi. Corriger le brief Effectif (action 1 « tester Ounahi au but ») et celle de vendre Leroy « pour viser un vrai gardien » : le besoin est d'un doublure, pas d'un titulaire.

## Protocole de test (facultatif) — amical Ajax Amsterdam
Match 2080875, **2026-10-26 02:00 Paris, composition avant 2026-10-26 00:00** (`gold.ts_upcoming`, compétition « inconnu » dans la vue : confirmer que c'est l'amical). Je ne recommande pas ce test comme priorité ; il ne vaut que si l'on veut vérifier le Contrôle d'un gardien. Une seule variable :
- Composition de référence : celle du dernier match de ligue en 1-4-4-2.
- Variante : Ounahi au but ; R. Thomas sur le banc (couvre gb) ; DC = Simon, T. Thomas, Dubois + Leroy (ou Enzo Roux) à la place d'Ounahi ; mêmes consignes, même style, même banc.
- Mesures, via `gold.ts_match_report` (`opp_shots`, `opp_on_target`, buts encaissés, `my_lost`, secteurs `my_weakest_zone`) et `gold.ts_player_match_ratings` (note d'Ounahi au but, de Leroy en DC) :
  1. tirs adverses et tirs cadrés (le gardien n'influe que sur le duel de tir) ;
  2. buts encaissés / tirs cadrés (base : R. Thomas, 2 buts sur 3 cadrés sur 2 matchs, L-005) ;
  3. barre Défense centrale et note de la défense ;
  4. buts de la tête marqués (on perd la Tête 97 d'Ounahi) et ballons perdus (`my_lost`).
- Seuil de lecture : ne rien conclure d'un seul match ; une dégradation nette (Défense centrale en baisse et plus de tirs cadrés adverses) ferme la piste. Pas de gain mesurable = rester avec R. Thomas.
- Confiance : faible (un seul match, adversaire inconnu).

## Décision recommandée
Garder R. Thomas au but et Ounahi DC. Si l'utilisateur veut quand même tester, le faire uniquement au 26/10 (amical).
