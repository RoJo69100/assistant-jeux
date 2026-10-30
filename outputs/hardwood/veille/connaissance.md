# Hardwood — connaissance (index)

Première veille intégrale du 2026-10-30 : Discord complet (230 000 messages, 2018-02 → 2026-10-28, canaux #general, #advice, #polls, #recruiting-updates, #recruiting-discussion), guide de recrutement (Google Doc), tables `public.hardwood_*` en base. Manuel `onlinecollegebasketball.org/rules` non lu (Cloudflare) : à capturer avec `userscripts/hardwood.user.js`.

Développeur : Steve (`admin06826` sur Discord, 1 542 messages). Il parle peu des règles : la plupart des faits viennent des joueurs anciens (naph7777, furysk, eljefe7705, gards710, mdoman12). Statut de chaque fait dans les fichiers ci-dessous : confirmé / complété / contredit / en doute.

| Thème | Fichier |
|---|---|
| Structure, calendrier, compétitions, classement, finances | [v-calendrier-competitions.md](v-calendrier-competitions.md) |
| Recrutement, contacts, bourses, potentiel, redshirt | [v-recrutement.md](v-recrutement.md) |
| Compétences, postes, fatigue, blessures, progression, coachs | [v-joueurs-entrainement.md](v-joueurs-entrainement.md) |
| Game Tactics, Game Management, moteur | [v-tactique.md](v-tactique.md) |

**2026-10-30, manuel capturé** (`bronze.raw_pages` page_type `rules`) et confronté à la veille. Les règles retenues sont dans les skills `hardwood-regles`, `hardwood-recrutement` et `hardwood-tactique` (chaque fait marqué [R] manuel, [D] Discord, [E] export). Le manuel confirme : la pyramide et les divisions, 3 montées et 6 descentes, 13 bourses, le redshirt à 5 matchs, l'Overwork, le plafond de 45 points et le report « 10 + moitié », la règle « un coach par jour », l'absence d'argent et de transferts. Il ajoute : le coaching le jeudi et le dimanche (heure du Pacifique), les minutes de repos de Staggered A/B/C, la règle « seul le premier ajustement de mi-temps qui se déclenche s'applique », le minimum de 15 min pour un titulaire, la difficulté pour une D3 d'attirer des 4 et 5 étoiles, et le changement d'assistant possible seulement avant la saison de conférence ou après la saison. Aucune contradiction trouvée ; restent non chiffrés : malus hors poste, bonus du terrain, formule du RPI.

**2026-10-30, document d'aide de l'utilisateur** (`data/manual/hardwoord/Aide docs.txt`, marqué [A] dans les skills) : tableau des phrases du scout (épinglé sur Discord) — **contredit** 9 valeurs de `public.hardwood_ref_scouting_ranges` (ex. « good shooter » 13-16 et non 13-19, « sluggish » 0-9 et non 0-6, « below average ball handler » 0-12 et non 0-2, défense complète = somme IDef + PDef) → nouvelle table `silver.hw_ref_scout_phrases` ; tableau potentiel → plafond de SI **confirmé** (pot 9-17) ; phrases de coach → notes (nouveau) ; compétences clés par poste (nouveau, `silver.hw_ref_position_keys`) ; HS SR → FR, JC SO → JR, 3-4 recrues par classe dont un grand (complété) ; fatigue : joueurs reposés entre deux matchs (complété) ; seuils des ajustements de mi-temps expliqués par Neph (2022-04-09, nouveau).
