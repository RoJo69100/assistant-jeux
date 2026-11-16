-- Lecteur gold de /api/club/<id> (Hockey Nation) : gold.hn_exports_state, indiqué par l'utilisateur le 2026-11-16.
-- Note : la définition de la vue ne cite que les sous-routes /club/:id/... ; le rattachement vient de l'utilisateur, non d'une lecture du code.
insert into core.page_reader (game, motif, lecteur) values
  ('hockeynation', '^/api/club/<id>$', 'gold.hn_exports_state')
on conflict do nothing;
