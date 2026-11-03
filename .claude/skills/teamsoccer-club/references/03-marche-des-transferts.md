## Marché des transferts
### Vendre : deux systèmes depuis le 2026-10-18 [F:2026-10-18 Admin-Dev] [G:Valeur des joueurs]
1. **Vente à la banque TeamSoccer** : immédiate, **au prix de la fiche**, sans commission. La banque remet ensuite le joueur aux enchères ; s'il ne trouve pas preneur, il disparaît du jeu.
2. **Enchère du manager** (bouton « Mettre aux enchères ») : **72 heures**, prix de départ fixé par le vendeur **au plus égal à la valeur de la fiche**. Sans enchère, le joueur revient gratuitement. Vendu : l'acheteur paie l'enchère finale, le vendeur reçoit **90 %** (10 % de commission). Impossible d'annuler une fois une offre reçue ; ni le vendeur ni ses autres clubs ne peuvent enchérir.
- Ventes illimitées pour tous [F:2026-09-11 Admin-Dev].
- V-20261027-5 (hypothèse, deux cas) : prix de départ des enchères de manager parfois très bas : un jeune de 15 ans parti à **6 000 $** (PIPO68 : « 6 000 est le prix de départ, on ne sait pas jusqu'où monte l'enchère » [F:2026-10-19/20]) ; une joueuse valant 2 000 en enchère de manager le 2026-10-21 [F:CHARLY_GARCIA]. Une enchère maximale placée tôt peut emporter un joueur sous sa valeur ; à chercher dans `silver.ts_transfer_listings` (achat limité à 1 par semaine).

### Acheter [G:Limites hebdomadaires de transferts] [F:2026-10-18 Admin-Dev]
- Enchères sur la page Marché (« Your offers » regroupe les joueurs suivis). **+2 minutes de prolongation** si une offre arrive à la fin.
- **Limite d'achat** : compte de 30 jours ou moins = illimité ; au-delà, **1 achat par semaine, les enchères en tête comptent**. Remise à zéro le lundi 00:00 (heure Atlantique/Canaries).
- **Revente interdite pendant 7 semaines** après un achat. Effectif entre 16 et 24, enchères en cours comprises ; budget suffisant exigé (solde négatif = pas d'achat).
- Joueurs libres : ajoutés par le site à intervalles réguliers depuis le 2026-07-18, au prix réel [F:2026-07-18, 2026-07-19 Admin-Dev].
- En vente, les compétences du joueur sont visibles (on peut juger son OVR et sa valeur avant d'enchérir).
- [P:Marché] Au 2026-10-19 : environ 55 annonces ; prix de départ de 50 645 $ (OVR 31, 16 ans) à 2 034 483 $ (OVR 85, 20 ans).

