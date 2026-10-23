# Team Soccer — fiche Transferts

Lue par l'agent `transferts` après `commun.md`. Case E6 de la checklist Team Soccer.

## Skills à lire
- `.claude/skills/teamsoccer-club/SKILL.md` (§ Marché : vente à la banque, enchère du manager, limite d'achat, revente bloquée)
- `.claude/skills/teamsoccer-joueurs/SKILL.md` (compétences clés par poste, âge, valeur, salaire)

## Règles propres au jeu
1. **Vendre** : à la banque, immédiat, au prix de la fiche, sans commission ; ou enchère du manager de 72 h, prix de départ ≤ valeur, **10 % de commission** [F:2026-10-18 Admin-Dev].
2. **Acheter** : **1 achat par semaine**, les enchères en tête comptent, remise à zéro le lundi 00:00 (heure des Canaries) ; **solde négatif = pas d'achat** ; effectif ≤ 24 enchères comprises ; **revente interdite 7 semaines** [G:Limites hebdomadaires de transferts].
3. Un nouveau joueur commence à Forme 85 [skill joueurs] et coûte ≈ 1 % de sa valeur par semaine.
4. Les deux clubs sont des économies séparées : un club ne peut pas financer l'autre.

5. **Verdict nommé** (demande de l'utilisateur, 2026-10-23) : pour chaque annonce, « lui est bon / lui n'est pas bon » avec raison chiffrée contre les titulaires et le banc du club (OVR, compétences clés, prix contre capacité, fin, offres, âge), jamais de seuil générique. La Forme affichée dans l'annonce ne compte pas : une recrue démarre à Forme 85.
6. **Club de l'annonce** : `silver.ts_transfer_listings` n'a pas de club. Attribution par le sexe des noms et par le lot de relevé (`seen_at` : 12:57 = noms masculins → Chomelix, 12:58 = noms féminins → Ben Ahmed au 2026-10-23). Si une annonce est douteuse : écrire « il me manque : le club de l'annonce X ; voici comment on l'obtient ensemble : l'utilisateur ouvre le Marché de chaque club (Chomelix puis Ben Ahmed) et exporte séparément, le lot exporté donne le club ». Un export Marché par club lève le doute.
7. Heures de fin : `deadline` est en UTC ; convertir en heure de Paris avec `at time zone 'Europe/Paris'` (heure d'hiver dès le 25/10 03:00).

## Données
- `silver.ts_transfer_listings` : `listing_type` (bank / manager), `asking_price`, `bids`, `deadline`, `seller`, joueur à plat (`position`, `age`, `ovr`, `forme`, `value`, 10 compétences).
- `silver.ts_my_bids` : annonces où un de mes clubs a enchéri.
- `silver.ts_players`, `gold.ts_squad_report` (besoins par zone), `gold.ts_finance_status` (solde, projection).

## Livrable
- Pour un joueur : intérêt pour l'effectif (poste, compétences clés, âge), prix correct ou non, **enchère maximale**, en rappelant la limite d'un achat par semaine et le solde.
- Liste des joueurs à vendre par club, banque ou enchère, avec le gain net et l'effet sur la masse salariale.

## Constat au 2026-10-19 [Obs SQL]
- Les deux soldes sont négatifs : aucun achat possible avant le retour au positif.
