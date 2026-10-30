# Tactique BasketVibe, COUPE ce soir 30/10 18:00 Paris, EXTÉRIEUR à Yannick Skulls (fixture 720d9d11), brief du 2026-10-30

Amont lus : lecteur-exports 30/10, tactique 29/10, tactique amical 31/10. Élimination directe : cinq de coupe (pas la compo de test). Moteur v4. Plan NON sauvegardé (`saved` faux, preset Cup, export 30/10 10:13 Paris) : tout est à saisir et à SAUVEGARDER AVANT 18:00, puis exporter la page du match. Ne pas faire « Save as preset ». Coupe = aucune fatigue, blessure, expérience [News 2026-10-23] : ces minutes ne coûtent rien à l'amical de demain 08:00.
Base : plan PSG du 29/10 réellement saisi par l'utilisateur (`gold.bv_saisie_joueurs`, fixture dc345bfb, sauvegardé : C-097, C-098, C-099 appliqués). On le reprend tel quel, on ne change que les focus défensifs (adversaire différent).

## Écran 1 : composition
| | PG | SG | SF | PF | C |
|---|---|---|---|---|---|
| Q1 | Richard | Bonnet | Gimenez | Lefebvre | Fournier |
| Q2 | Richard | Bonnet | Gimenez | Lefebvre | Fournier |
| Q3 | Richard | Bonnet | Gimenez | Lefebvre | Fournier |
| Q4 | **Boyer** | Bonnet | Gimenez | Lefebvre | **Ungureanu** |
| Prolongation | **Boyer** | **Dang** | Gimenez | Lefebvre | **Ungureanu** |
Pas de remplacement programmé. Depth chart inchangé (SG Bonnet > Dang > Henry ; PF Lefebvre > Albano > Legrand).

## Écran 2 : consignes (écran 1 à 5), 16 joueurs, ordre de l'écran
| Joueur | Poste | Q1 | Q2 | Q3 | Q4 | Prol. | Min | Off. focus | Rôle | Tir | Agress. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baron | PG | — | — | — | — | — | 0 | 1 | 1 | 3 | 3 |
| Boyer | PG | — | — | — | PG | PG | 12 (+5) | 2 | 2 | 3 | 3 |
| Richard | PG | PG | PG | PG | — | — | 36 | 1 | 1 | **2** | 3 |
| Bonnet | SG | SG | SG | SG | SG | — | 48 | 5 | 5 | 5 | 3 |
| Dang | SG | — | — | — | — | SG | 0 (+5) | 3 | 3 | 3 | 3 |
| Henry | SG | — | — | — | — | — | 0 | 4 | 4 | 4 | 3 |
| Leclerc | SG | — | — | — | — | — | 0 | 4 | 4 | 5 | 3 |
| Durand | SF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Gimenez | SF | SF | SF | SF | SF | SF | 48 (+5) | **4** | 3 | 3 | 3 |
| Lecomte | SF | — | — | — | — | — | 0 | 3 | 3 | 2 | 3 |
| Albano | PF | — | — | — | — | — | 0 | 3 | 3 | 3 | 3 |
| Lefebvre | PF | PF | PF | PF | PF | PF | 48 (+5) | 4 | 4 | 1 | 3 |
| Legrand | PF | — | — | — | — | — | 0 | 3 | 3 | 1 | 3 |
| Bernard | C | — | — | — | — | — | 0 | 2 | 2 | 1 | 3 |
| Fournier | C | C | C | C | — | — | 36 | 2 | 2 | 1 | 3 |
| Ungureanu | C | — | — | — | C | C | 12 (+5) | 3 | 3 | 3 | 3 |
Les valeurs en gras sont celles du plan PSG sauvegardé (le preset Cup les remet à 3/3). Tout le reste = valeurs du preset Cup affichées. Agressivité 3 partout : coupe sans fatigue ni blessure. Klein (vendu) et Fontaine (absent du relevé) : ne pas placer.

## Écran 3 : focus défensif (1 Give up, 2 Light, 3 Normal, 4 Intense, 5 Lock) et zone
Zone : l'export de la coupe porte bien un champ `area_step` (3 = Middle) sur les 13 adversaires ; la fiche et le skill disent « amicaux seulement » et V-20261027-3 (coupe/ligue) reste une hypothèse non tranchée (C-089 ouvert). Décision : Middle (3) partout, aucun test de zone dans un match à élimination. Si l'écran n'affiche pas de sélecteur de zone, ne rien toucher.
| Adversaire (ordre de l'export) | Poste | Fourchettes utiles | Focus | Zone |
|---|---|---|---|---|
| Gautier | PG (23) | 2PT 0-20, 3PT 21-40, Pass 21-40 | **2 Light** | Middle (3) |
| Jourdan | PG (19) | blessé, retour 06/11 | 3 | Middle (3) |
| Lacroix | PG (26) | Déf, Pass, Dribble 61-80 (passeur) | 3 | Middle (3) |
| Marchal | PG (17) | 3PT 21-40, reste 41-60 | **2 Light** | Middle (3) |
| Guerin | SG (28) | 3PT, Déf, Ath 61-80 | **4 Intense** | Middle (3) |
| Lopez | SG (25) | 3PT 21-40, reste 41-60 | 3 | Middle (3) |
| Dupont | SF (25) | 2PT, 3PT, Ath 61-80 | **5 Lock** | Middle (3) |
| Roussel | SF (27) | blessé, retour 05/11 | 3 | Middle (3) |
| Bernard | PF (29) | 3PT 61-80, Pass 0-20 | 3 | Middle (3) |
| Fontaine | PF (26) | 2PT, Déf 61-80 | 3 | Middle (3) |
| Meyer | PF (18) | tout 41-60 | **2 Light** | Middle (3) |
| Cousin | C (29) | Déf 61-80 | 3 | Middle (3) |
| Laporte | C (31) | Pass, Ath 61-80 ; 3PT 0-20 | 3 | Middle (3) |
13 adversaires listés (pas 12). Aucun Give up. Jourdan et Roussel sont blessés : leur focus n'a pas d'effet, 3 par neutralité.

## Réglages d'équipe
Preset : laisser « Cup » (celui affiché) ; sauvegarder le plan du match uniquement. Remplacements programmés : aucun (le cinq change au début du quart [M§6.2]). Aucun autre réglage d'équipe à modifier.

## Analyse chiffrée de l'adversaire (`skill_brackets`, fourchettes de 20 points ; 0 joueur au-dessus de 80)
| Poste | Meilleurs | Lecture |
|---|---|---|
| PG | Lacroix (Déf/Pass/Dribble 61-80) ; Gautier 2PT 0-20 ; Jourdan blessé | meneur correct, peu de score ; PG faible |
| SG | Guerin (3PT, Déf, Ath 61-80) ; Lopez 41-60 | seul tireur à 3 pts |
| SF | Dupont (2PT et 3PT 61-80, Ath 61-80) ; Roussel blessé (2PT 61-80, Reb 0-20) | seul scoreur complet |
| PF | Fontaine (2PT, Déf 61-80) ; Bernard (3PT 61-80, Pass 0-20) ; Meyer 41-60 | moyen |
| C | Cousin (Déf 61-80) ; Laporte (217 cm, Pass/Ath 61-80, 3PT 0-20) | Fournier/Ungureanu à l'aise |
Équipe sans compétence 81-99 (contre PSG : Robert 2PT 81-99, Dupont PSG Passes 81-99) : plus faible que PSG sur le papier. Nous : Lefebvre 63, Gimenez 59,7, Richard 56, Fournier 52,3, Bonnet 51,4 (`gold.bv_roster_now`, PS indicatif). Limites : fourchettes seulement, aucun historique contre Skulls, tactique adverse inconnue, extérieur sans effet connu (aucun avantage du terrain en coupe [News 2026-10-23]). Confiance faible.

## Contrôle SQL
5 joueurs distincts par quart (Q1-Q4, Prol.) : oui. Emplacements : `height_eff` 100 pour Richard PG, Boyer PG, Bonnet SG, Dang SG, Gimenez SF, Lefebvre PF, Fournier C, Ungureanu C (`gold.bv_slot_fit`). Quarts consécutifs : Bonnet, Gimenez, Lefebvre 4 (48 min, PS × 0,8 en Q4 [M§5.7]) ; Richard, Fournier 3. Q4 comparé (`fit_with_form`, 36 min passées ×0,8) : Fournier 52,8 -> 42,2 contre Ungureanu 47,9 ; Richard 56,6 -> 45,3 contre Boyer 48,2 ; Bonnet 51,9 -> 41,5 contre Dang 50,4 (Dang meilleur sur le papier, mais Bonnet reste le seul tireur 3PT 72 : inchangé pour garder un test lisible) ; Gimenez 48,2 contre Durand 43,2 et Lefebvre 50,9 contre Legrand 48,8 : ils restent. Blessés ou en vente alignés : 0 (Henry, Lecomte en vente, 0 minute). Forme 6 (Ungureanu 5), relevé du 30/10, postérieur au dimanche 25/10. Total 240 min (+25 prolongation).
Fatigue (`gold.bv_roster_now`, 30/10) : titulaires de coupe 0 ; Boyer 0,38 et Ungureanu 0,47 jouent 12 min : coupe sans fatigue [News 2026-10-23], effet de leur fatigue actuelle sur le Q4 non chiffré (hypothèse : négligeable). Conflit avec l'amical de demain 08:00 : AUCUN. Leclerc et Lecomte (36 min demain, fatigue 0,60 et 0,74) ne jouent pas ce soir, les jeunes (Baron, Leclerc, Lecomte, Bernard) restent à 0 minute, le programme de l'amical n'est pas touché. Boyer et Ungureanu y jouent 24 min comme prévu : pas de fatigue ajoutée par la coupe.

## Contrôle des conseils C-097 à C-099
Match PSG du 29/10 absent de la base (`silver.bv_matches` : `scheduled_lineups`, sans score ; absent de `gold.bv_match_report`). Appliqués : OUI, prouvé par le plan sauvegardé (fixture dc345bfb : Boyer et Ungureanu Q4, Richard tir 2, Gimenez focus 4, Robert 5, Baudry/Leroy/Arnaud 2). Effet : NON VÉRIFIABLE. Le fixture Skulls existe aujourd'hui, donc nous sommes qualifiés (inférence, score inconnu). Il me manque l'export de la page du match PSG : à faire ce soir seulement si la page est encore accessible, sinon C-097 à C-099 restent ouverts. Repère : coupe Maccabi 28/10, Q4 -4 après 48 min des titulaires (pire quart, marges +6, +16, +9, -4).

## Trois points testables (export de la page du match après 18:00, plan sauvegardé)
1. Q4 : marge Q4 ≥ -3 avec Boyer/Ungureanu (C-097). J'avais tort si Q4 ≤ -8 ou si l'éval/min d'Ungureanu est sous celle de Fournier en Q4.
2. Focus : Dupont < 20 pts avec Lock et Guerin < 20 pts avec Intense. J'avais tort si Dupont ≥ 25 pts, ou si Gautier + Marchal + Meyer cumulent ≥ 30 pts en Light.
3. Résultat : victoire de plus de 10 points (équipe sans 81-99, Maccabi +27). J'avais tort si l'écart est inférieur à 10 ou si un adversaire hors Dupont et Guerin dépasse 25 pts.
