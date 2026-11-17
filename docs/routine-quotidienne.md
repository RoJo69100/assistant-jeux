# Routine quotidienne BasketVibe (P1, décision D2)

Le passage quotidien vit dans une **routine planifiée Claude** (tâche planifiée, une session neuve à chaque déclenchement), pas dans GitHub Actions. L'utilisateur crée la routine lui-même ; ce fichier en donne le réglage et le prompt.

## Réglage
- Dépôt : `rojo69100/assistant-jeux`, environnement avec accès Supabase (variables `SUPABASE_*` du `.env`).
- Fréquence : chaque jour. Heure proposée : 10:40 heure de Paris (après le rapport d'académie du jeudi 09:00 et le traitement du dimanche 04:00, bien avant le verrou de ligue 19:45). À ajuster : l'amical de 08:00 du lendemain se prépare dans ce passage.
- Modèle : Sonnet, effort medium (sessions d'exécution, CLAUDE.md).
- Incertitude : `passage_quotidien.py` lance chaque agent par `claude -p --agent <nom>`. Si la CLI n'est pas authentifiée dans la session de la routine, le que-faire le dit (« agent X non lancé : … ») au lieu de se taire.

## Prompt de la routine (à coller tel quel)

```
Passage quotidien BasketVibe. Un seul jeu : basketvibe. Horizon d'action = aujourd'hui (heure de Paris : python -I pipelines/heure_paris.py).
Plafond : 15 appels d'outil. Aucun texte entre les appels d'outil.

1. python -I pipelines/passage_quotidien.py
   (rejoue le plan, lance les agents de la table `agents` de docs/attentes/jeux/basketvibe.yaml, écrit
   outputs/basketvibe/que-faire-AAAA-MM-JJ.md, commit et push)
2. Si le code retour vaut 2 (plan non fiable) ou si « git : » n'indique pas « poussé » ni « rien à commiter » : ne relance rien,
   rapporte la sortie telle quelle.
3. Interdits : aucun achat, aucune vente, aucune enchère (règle 2) ; aucune somme au-dessus de 250 000 sans `python pipelines/dossier.py
   basketvibe achat` puis l'agent police ; ne lance aucun agent hors du script ; ne modifie aucun fichier à la main.

Réponse finale, 5 lignes au plus : la ligne « Agents : … » du script, chaque ligne « agent X non lancé : raison », la ligne « git : … »,
puis le chemin du que-faire du jour.
```
