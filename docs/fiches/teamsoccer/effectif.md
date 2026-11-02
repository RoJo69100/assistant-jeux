# Team Soccer — fiche Effectif

Lue par moi (session principale) après `resume.md` : l'agent `effectif` est retiré depuis le 2026-11-02 (étape 0d), son travail = les vues gold ci-dessous + ce livrable, sans brief d'agent. Case E2 de la checklist Team Soccer. Un bilan par club.

## Skills à lire
- `.claude/skills/teamsoccer-joueurs/SKILL.md` (compétences, sous-rôles, OVR, Forme, talents, âge, valeur, effectif 16–24)
- `.claude/skills/teamsoccer-entrainement/SKILL.md` (§ Âge : progression jusqu'à 27 ans, perte dès 28–29)

## Règles propres au jeu
1. **Effectif entre 16 et 24, enchères en cours comprises** [F:2026-10-18 Admin-Dev]. À 24, impossible d'enchérir ou de monter un jeune.
2. Le poste naturel découle des compétences (Gardien, Défense, Conduite, Finition) ; jouer hors du sous-rôle naturel baisse la note [skill joueurs]. Juge un joueur sur les **compétences clés de son poste**, pas sur l'OVR seul.
3. La Forme compte autant que le niveau : un joueur à 100 avec Forme 50 joue comme 85 [F:2026-08-28 Admin-Dev]. Signale toute Forme < 70.
4. Âge : +1 an par saison ; progression nette jusqu'à ~23 ans, nulle vers 27–28, perte ensuite. Talents perdus à 32 ans.
5. Valeur = prix de vente immédiat à la banque ; salaire ≈ 1 % de la valeur par semaine [Obs].

## Données
- `gold.ts_squad_report` : par club et zone, `players`, `avg_ovr`, `best_player`, `avg_forme`, `min_forme`, `avg_age`, `u21`, `age_29_plus`, blessés, suspendus, `on_two_yellows`, `weekly_wages`, `total_value`.
- `silver.ts_players` : un joueur par ligne (10 compétences, `ovr`, `forme`, `zone`, `second_skill`, `age`, `value`, `wage`, `talent`, `injury_days`, `suspended`, `yellow_cards`, statistiques officielles).
- `gold.ts_player_progress` (après deux relevés) ; `gold.ts_academy` pour la relève.

## Livrable
1. Bilan par zone pour chaque club, meilleurs et moins bons joueurs (compétences clés à l'appui).
2. **3 actions concrètes** par club (vendre, acheter, monter un jeune, changer de poste), compatibles avec la limite de 24 et le solde.
3. Projection 1 à 3 saisons : âges, relève par zone.

## Constat au 2026-10-19 [Obs SQL]
- Chomelix Cows (Div I) : 23/24 ; **gardiens faibles** (4 GB, meilleur OVR 60, 17 ans de moyenne) alors que la défense a un joueur à 90.
- Ben Ahmed Donkey : 22 joueurs, niveau homogène (OVR 55–64).
