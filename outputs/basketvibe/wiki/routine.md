# Routine BasketVibe

Heures de Paris. Sources : skill basketvibe-saison [M§1.3], routine décidée avec l'utilisateur (2026-10-16 / 18). Pour la liste du jour, demander « qu'est-ce que je fais aujourd'hui ? » (skill basketvibe-aujourdhui, vue `gold.bv_agenda`).

## Chaque jour
| Heure | Action | Pourquoi |
|---|---|---|
| Avant 07:45 | Vérifier le **preset amical** sur l'amical du jour | Verrouillage 15 min avant le coup d'envoi [M§1.3] |
| ~08:55 | **Exporter la page de l'amical** | Agent Match (delta) ; les amicaux sont le banc d'essai du moteur v4 [News 2026-10-11] |
| Dans la journée | **Programmer un amical** s'il manque un jour (10 au maximum programmés [M§1.2]) | ~17 500 de recette chacun [Obs] : sans amical quotidien, la semaine type passe dans le rouge (brief finances du 18/10) |
| Selon les enchères | Suivre la fin des enchères (anti-snipe 3 min, phase à l'aveugle possible jusqu'à +20 min [M§11.3]) | Brief transferts |

## Jours de ligue (lundi, mercredi, samedi)
| Heure | Action |
|---|---|
| Avant 19:45 | Exporter la **Preview** du match (effectif adverse à jour), vérifier le **preset de ligue**, régler le **focus défensif** sur la page du match [M§6.6] |
| ~20:50 | **Exporter la page du match** → agent Match, puis agent Tactique pour le match suivant |

Rappel : un preset modifié doit être **re-sélectionné sur chaque match déjà planifié** [Com 2026-09-05].

## Chaque semaine
| Quand | Action |
|---|---|
| **Samedi soir** | Vérifier et **sauvegarder l'entraînement** (fiche de l'agent Entraînement) avant dimanche 04:00 [Obs] |
| **Dimanche après 04:00** | **Exporter Entraînement + Finances + Personnel** : progression, forme, paie, sponsor, homegrown → agents Entraînement et Finances |
| **Jeudi après 09:00** | **Exporter Académie** (nouveau rapport du scout) → agent Académie. Investissement à sauvegarder **avant** jeudi 09:00 [M§4.2]. Finances en option (l'API ne montre que 20 transactions) |
| Après chaque export du marché | Agent Transferts (les enchères bougent vite : export de moins de 24 h) |
| Après un export Discord / des News | Agent Veille : propositions de mise à jour des skills, à valider |

## Chaque saison (8 semaines, 22 journées)
- **Début** : choisir le sponsor avant la 1re journée (sinon Stability) [M§10.1.2] ; forme remise à 6, fatigue à 0, popularité à 70 % [M§5.5, §5.6, §10.1.1].
- **Fin** : salaires recalculés (plus chers si les joueurs ont progressé) [M§10.2] ; +1 an pour tous ; retraites à 38 ans [M§4] ; primes de classement [M§10.1.4]. Psychologues et marketing inutiles la dernière semaine (forme et popularité remises à zéro).
- **Saison 2** : la ligue passe au moteur v4 (fatigue plus punitive, duels plus marqués) [Dev 2026-09-30, News 2026-10-16 / 17].
