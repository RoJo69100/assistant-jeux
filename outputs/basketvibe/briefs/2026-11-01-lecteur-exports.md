# Lecteur d'exports BasketVibe - 2026-11-01 (exports 07:38-07:53 UTC = 08:38-08:53 Paris)

## 1. Coupe (FR Cup, schedule id 32021, 07:42:33 UTC)
| Match | Date / heure Paris | Dom/ext | Adversaire | fixture_id | Résultat |
|---|---|---|---|---|---|
| Cup tour 4 | 31/10 18:00 | domicile | Ploppers | a536c811-ca2a-4a49-96c9-7498dab6c717 | JOUÉ : 82-72, GAGNÉ (human_team_is_home=true, won=true, notif 31/10 17:50 UTC). Silver : scores et my_result NULL |
| Cup tour 5 (dernier tour exporté) | 01/11 18:00 | EXTÉRIEUR | Reims Monarchs (domicile) | 16c8812a-92b7-44ef-bc93-abd99f062488 | scheduled, can_edit_match_tactics=true, tactique non enregistrée |
Reims a gagné ses 4 tours (119-112 Pessac ext., 98-93 Landais ext., 102-95 Basket pastis, 104-97 Gin Team). Le mot « finale » n'est écrit nulle part : tour 5 = suite du même rythme quotidien, finale non prouvée.

## 2. Aperçus
| Adversaire | Aperçu exporté ? | Contenu |
|---|---|---|
| Chara legends (J1 ligue, lun 02/11 20:00 Paris, extérieur, fixture a20c70d8-2518-4b75-9c0b-dc82cecb1b22) | OUI, match id 32023 (scheduled_lineups) + 32024 + 32025 | 12 joueurs avec fourchettes (voir ci-dessous), rang 7, chance estimée 50/50, aucune forme (0 match de ligue) |
| Reims Monarchs (coupe 01/11) | NON : aucune page aperçu pour 16c8812a | seulement 4 box scores (pages unknown 31900, 31932, 31949, 31981) |
| Galit sa gobyerno (amical lun 02/11 08:00 Paris, domicile, fixture adef49a3-e42b-4a42-b587-7f567dc4dfe7) | NON : nom absent de tout le brut sauf la liste schedule | rien sur l'effectif |

Chara legends (fourchettes, skills_visibility=bracket ; D=defense P=passing S=stamina 2P=two_point R=rebond A=athl 3P=three_point BH=ball_handling) :
| Joueur | Poste | Âge | Forme | Taille | Fourchettes notables |
|---|---|---|---|---|---|
| Aguayo | PF | 25 | 7 | 208 | P 61-80 ; 3P/2P/R/D 41-60 ; A,BH 21-40 |
| Durán | C | 28 | 6 | 207 | D 61-80 ; reste 41-60 |
| Díaz | PG | 29 | 6 | 188 | P 61-80 ; reste 41-60 |
| Hernández | PF | 26 | 5 | 203 | D 61-80, R 61-80 |
| Molina | SF | 29 | 5 | 203 | faible : tout 21-40 sauf R et BH 41-60 |
| Moreno | SG | 25 | 5 | 193 | A 61-80, 3P 61-80 |
| Navarro | C | 19 | 7 | 209 | tout 41-60 sauf S,3P 21-40 |
| Romero | PG | 31 | 5 | 189 | D 61-80 ; A 21-40 |
| Soler | C | 23 | 6 | 222 | 3P 61-80 ; 2P 21-40 |
| Suárez | SG | 27 | 7 | 193 | tout 41-60 |
| Vargas | PG | 18 | 5 | 181 | tout 21-40 sauf P,BH 41-60 |
| Vázquez | SF | 26 | 6 | 199 | D 61-80, A 61-80 ; P,BH 21-40 |
Seul match exporté de Chara (id 32013, coupe tour 1, 28/10, domicile, perdu 72-92 contre Basktballerz) : minutes Molina 48, Hernández 48, Aguayo 48, Durán 41,5, Moreno 33,1, Soler 14,9, Suárez 6,5, Vázquez 0 ; points Hernández 27, Aguayo 12, Molina 11, Durán 9. Rotation courte à 5-7 joueurs.
Tactique visible de Chara (focus défensifs, zone) : NON exposée par l'aperçu (le defensive_focus de 32024 est MON réglage, tout « normal », area_step 3).

Reims Monarchs, match du 31/10 (id 31900, gagné 104-97 à domicile ; Q1 37-24) : Aubert SG 40 pts (6 tirs à 3), Marchal SF 18, Caron PF 10, Klein PG 10, Michel C 217 cm 6, Fournier C 8 en 24 min, Kuhlmann SF 6 tirs à 3 (6 pts), Girard SF, Boucher PG. Cinq de départ 36 min chacun : Aubert, Caron, Klein, Marchal, Michel. Pas de compétences (aucun aperçu).

## 3. Ce que silver ne lit pas
- 31/10 cup vs Ploppers : silver.bv_matches a scores NULL et my_result NULL (ligne issue d'un aperçu du 31/10 09:48 UTC, jamais mise à jour). Vrai résultat : W 82-72. La page schedule 32021 et la notification cup_match_finished le prouvent ; le fixture cup n'est pas relu depuis `cup_fixtures`.
- Matchs d'adversaires (Reims, Chara) : lignes présentes dans silver.bv_matches avec my_side NULL (OK), mais les box scores adverses ne donnent ni fourchettes ni tactique.
- Fourchettes `skill_brackets` des adversaires (aperçu 32023) : gold.bv_next_opponents ne donne que rang/ts%, pas d'effectif adverse.
- Pas d'aperçu de coupe ni d'amical : gold.bv_exports_state signale « Amical : tactique du match » 47 h, « Mes enchères » 47 h, « Match de ligue : box » 132 h, Personnel 168 h.

## 4. Classement erroné du script
- unknown (45 lignes) : box scores finis (kind=finished, fixture_kind cup/friendly), box par quart (period/players), play_by_play, seasons, league, session/unread_count, HTML. Critère : clés du body.
- friendly (9) : notifications (clé `notifications`), box finished de MON amical vs Granada Sentinel, roster et tactique : à classer par clés.
- schedule 32020/21/22 : trois contenus (friendlies, cup_fixtures, fixtures de ligue).
- match 32024/32025/32026 : tactique/roster/HTML, pas des fiches de match.

## 5. Reste à exporter
- Aperçu du match de coupe contre Reims Monarchs (ouvrir Schedule > Cups > le match du 01/11 18:00 > Preview), avant 18:00 Paris, pour avoir leurs fourchettes.
- Aperçu de l'amical contre Galit sa gobyerno (Schedule > Friendlies > match du 02/11 08:00 > Preview).
