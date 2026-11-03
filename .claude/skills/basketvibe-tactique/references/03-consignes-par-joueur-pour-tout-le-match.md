## Consignes par joueur (pour tout le match) [M§6.3]
1. **Passe ou tir** : 5 crans, de passeur à scoreur. Oriente qui tire ; ce n'est pas un bonus de compétence.
2. **Focus offensif** : 5 crans, de Low à Primary en passant par Normal. Part relative de l'attaque qui passe par lui (dernière passe, tir, pertes de balle). Exemple : deux scoreurs, l'un Primary et l'autre Normal → le Primary tente ~1/3 de tirs en plus.
3. **Focus de tir** : 5 crans, de 2 pts à 3 pts. Au maximum ~2 tirs à 3 pour 1 tir à 2 ; toute l'équipe au maximum plafonne à ~50 % de tirs à 3.
4. **Agressivité défensive** : 0 soft · 2 équilibrée (défaut) · 4 agressive.

| | Soft (0) | Équilibrée (2) | Agressive (4) |
|---|---|---|---|
| Défense en duel direct | ~−14 | 0 | ~+14 |
| Défense moyenne des 5 | ~−4,4 | 0 | ~+4,4 |
| Tirs adverses provoquant une faute | ~12 % | ~16,5 % | ~21 % |
| Fatigue après match | ×0,75 | ×1,00 | ×1,65 |
| Risque de blessure | ×0,85 | ×1,00 | ×2,00 |

- Les fautes dépendent de l'agressivité **moyenne des 5 sur le terrain** ; la fatigue, de l'agressivité de chaque joueur.
- Ordre de grandeur, à niveaux égaux (~70) : adversaire à ~53 % aux tirs en soft contre ~48 % en agressif. Soit ~4–5 points encaissés de plus en soft qu'en équilibré, et ~3–4 de moins en agressif.
- ⚠️ **Moteur v4 (ligue à partir de la saison 2) : risque de blessure retouché** [News 2026-10-19]. Par rapport à une défense neutre : **Soft ×0,60** (v3 : ×0,85), **Medium soft ×0,80** (v3 : ×0,95). Les valeurs Neutre, Medium aggressive et Aggressive ne sont pas annoncées (le tableau v3 ci-dessus reste la seule référence). **Au-delà de 36 min, +40 % de risque de blessure au dernier quart** pour ce joueur. Effet annoncé : 48 min en Soft ≈ inchangé (0,60 × 1,40 = 0,84) ; 5×48 en défense normale ou agressive = « far more injuries ». Dernier message du dev : plus de changement prévu pour le v4. Interprétation (confiance moyenne) : la News étiquette ces deux points « v4, friendlies only », or les amicaux n'ont pas de blessure [M§1.2] ; ils visent donc la ligue v4. Texte de la News relu en base (`gold.bv_veille_feed`, 2026-10-19) le 2026-10-23.
- Le moteur respecte les consignes : il ne redirige pas le ballon vers le joueur en forme [M§6.3].

