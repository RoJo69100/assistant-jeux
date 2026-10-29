-- Hockey Nation (2026-10-29) : tableau des scouts avec les joueurs à repérer écrits dans des colonnes (règle de rendu de l'utilisateur)
-- + faits déclarés le 29/10 (offres de coachs, Dosymkhanov déplacé, rachat Eskelinen).
create or replace view gold.hn_scout_liste with (security_invoker = true) as
select scout,
       count(*) filter (where categorie = 'A poste + nation') as nb_top,
       count(*) filter (where categorie = 'B poste') as nb_poste,
       count(*) filter (where categorie = 'C nation') as nb_nation,
       count(*) as nb_total,
       string_agg(rang || ' ' || joueur, ', ' order by rang) filter (where categorie = 'A poste + nation') as top_poste_nation,
       string_agg(rang || ' ' || joueur, ', ' order by rang) filter (where categorie = 'B poste') as poste_autres_nations,
       string_agg(rang || ' ' || joueur, ', ' order by rang) filter (where categorie = 'C nation') as nation_autres_postes
from gold.hn_scout_targets
group by scout
order by count(*) filter (where categorie = 'A poste + nation') desc, count(*) desc;

insert into silver.hn_declared (kind, name, detail, declared_on) values
  ('coach_offre', 'Liming Meng', 'U21 assistant à la place de Dal Ahn (offre envoyée)', date '2026-10-29'),
  ('coach_offre', 'Roger Howe', 'U21 head à la place de Voiciks Grigorjevs (offre envoyée)', date '2026-10-29'),
  ('coach_offre', 'Jack Robertson', 'U17 assistant à la place de Cyril Fehérváry (offre envoyée)', date '2026-10-29'),
  ('coach_offre', 'Vasyl Dunka', 'U17 assistant à la place de Maximilian Helgstedt (offre envoyée)', date '2026-10-29'),
  ('joueur_deplace', 'Dosymkhanov', 'PRO → U21 fait le 29/10', date '2026-10-29'),
  ('rachat', 'Eskelinen', 'rachat fait le 29/10 : pénalité 1 285 000 $ par saison en S27, S28, S29', date '2026-10-29')
on conflict (kind, name) do update set detail = excluded.detail, declared_on = excluded.declared_on;
