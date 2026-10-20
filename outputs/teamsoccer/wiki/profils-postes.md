# Profil idéal par poste

Sources : skill teamsoccer-joueurs [G:Commencer à jouer 2.1] [G:Effectif — Notes et positions], teamsoccer-match [G:Moteur de match] [F:2026-05-28 Admin-Dev].

## Comment le jeu décide du poste
- Seules **4 compétences définissent le poste** : Gardien, Défense, Conduite, Finition. La plus haute donne la zone, la 2e le sous-rôle [G]. Tête, Passe, Centres et Contrôle ne sont jamais principales.
- **OVR = (Principale + 0,5 × Étoile + 0,2 × Secondaire 1 + 0,2 × Secondaire 2) / 1,9**, selon le sous-rôle naturel [G]. Les compétences « Étoile » et « Secondaires » de chaque sous-rôle ne sont pas publiées (checklist D34).
- L'OVR est un affichage : le moteur utilise les compétences [F:2026-05-08]. Mais la **note de match** se calcule dans le sous-rôle naturel : jouer hors poste baisse la note [G].
- Physique (Endurance, Vitesse) requis à tous les postes de champ [G].

## Compétences par poste [G:Commencer à jouer 2.1]
Principale en gras, puis secondaires. Bonus du moteur dans la zone naturelle [F:2026-05-28].

| Poste | Compétences | Ce que le moteur compare | Bonus de zone |
|---|---|---|---|
| Gardien (GB) | **Gardien**, Contrôle, (Passe) | Gardien contre Finition | — |
| Défenseur central (DC) | **Défense**, Contrôle, (Tête, Passe, Conduite) | Défense contre Conduite ; Tête sur les ballons aériens | Défense ×1,15 en zone défensive |
| Latéral (LAT) | **Défense**, Contrôle, (Passe, Conduite) | idem | Défense ×1,15 sur son flanc |
| Piston (WB) | **Défense**, Contrôle, (Centres, Conduite) | idem + Centres | idem |
| Milieu défensif (MD) | **Conduite**, (Contrôle, Défense, Passe) | Conduite contre Défense ; Contrôle à la réception | ×1,10 au milieu |
| Milieu central (MC) | **Conduite**, (Contrôle, Passe, Défense) | idem | ×1,10 au milieu |
| Milieu latéral / ailier (ML) | **Conduite**, (Contrôle, Centres, Passe) | idem + Centres | Centres ×1,20 depuis l'aile ; ×1,05 en défendant son flanc |
| Milieu offensif (MO) | **Conduite**, (Contrôle, Passe, Finition) | idem + tir | Finition ×1,05 pour un milieu qui tire |
| Avant-centre de tête (AC) | **Finition**, Contrôle, (Tête) | Finition contre Gardien ; Tête | Finition et Tête ×1,15 en zone de finition |
| Attaquant dribbleur (DR) | **Finition**, Contrôle, (Conduite) | Finition contre Gardien ; Conduite | idem |

- **Contrôle** est secondaire presque partout : il décide de chaque réception de passe [G:Moteur]. Un joueur complet réussit plus d'actions [G].
- **Consigne cohérente** avec la meilleure compétence du joueur : ×1,10 ; incohérente (un DC qui dribble) : ×0,90 [F:2026-05-28].
- Tir : but = Finition / (Finition + Gardien + 25), plafonné [F:2026-05-28]. Un bon gardien vaut donc autant qu'un bon buteur.
- Formations : 5 défenseurs = Défense +10 %, 3 = −10 % ; 3 attaquants = Finition +10 %, 1 = −10 % ; plus de milieux = plus de ballons [F:2026-06-02].

## Pièges observés dans nos effectifs
- **Libellé de zone trompeur à Ben Ahmed** : beaucoup de joueuses ont 60 partout et une seule compétence haute, donc la zone vient d'un départage. Ex. Suzuki et Schmidt sont « GB » avec Gardien 60 (leur point fort est la Passe, 81 et 84) ; la vraie gardienne est **Chae Abdel** (Gardien 79) [Obs 2026-10-20]. **Juger sur les compétences clés, pas sur la zone.**
- **Ounahi (Chomelix)** a Gardien 99 et Contrôle 100 mais est classé défenseur : test au but en amical proposé (brief effectif du 20/10), effet sur la note et sur la défense à mesurer.

## Meilleurs joueurs observés par zone (2026-10-20, `silver.ts_players`)
| Club | Zone | Joueur | Âge | OVR | Points forts |
|---|---|---|---|---|---|
| Chomelix | GB | Romain Thomas | 23 | 60 | Gardien 100, mais Vitesse 40, Endurance 51 |
| Chomelix | GB | Thomas David | 17 | 47 | Gardien 86, Contrôle 67 (relève) |
| Chomelix | DEF | Noussair Ounahi | 19 | 90 | Défense, Contrôle, Endurance, Vitesse 100, Tête 97, Gardien 99 |
| Chomelix | DEF | Nicolas Simon | 21 | 68 | Défense 100, Vitesse 89, Contrôle 71 |
| Chomelix | MIL | Lucas David | 26 | 67 | Conduite 100, Passe 89 |
| Chomelix | MIL | Adrien Roux | 25 | 67 | Conduite 100 |
| Chomelix | ATT | Lucas Moreau | 20 | 70 | Finition 100, Contrôle 81, Vitesse 80 |
| Chomelix | ATT | Pierre Bonnet | 24 | 67 | Finition 100 |
| Ben Ahmed | GB | Chae Abdel | 24 | 63 | Gardien 79 (la seule vraie gardienne) |
| Ben Ahmed | DEF | Yuki Fernández | 23 | 64 | Défense 81 |
| Ben Ahmed | DEF | Anna Fournier | 26 | 63 | Défense 77 |
| Ben Ahmed | MIL | Momoka Martínez, O. Mansour | 22–23 | 64 | Centres 81 ; **Conduite 60** (poste faible) |
| Ben Ahmed | ATT | Marie Müller | 20 | 64 | Finition 85, Vitesse 69 |
| Ben Ahmed | ATT | Juliette Yamamoto | 21 | 64 | Finition 84 |

Postes à renforcer (brief effectif du 20/10) : **gardien adulte à Chomelix** (Gardien > 90, Contrôle > 70) ; **milieux avec Conduite ≥ 80 à Ben Ahmed**, par le marché ou en entraînant la Conduite.
