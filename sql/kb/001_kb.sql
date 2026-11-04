-- Refonte v2, phase 4 : base de connaissances interrogeable (plan, annexe B.3, étapes 4.1 à 4.4).
-- kb.claim : une affirmation sourcée par ligne ; outputs/<jeu>/veille/connaissance*.md devient un export.
-- kb.support : un auteur de plus qui dit la même chose (+0,10, max +0,30).
-- kb.ingest_cursor : reprise de l'ingestion Discord (dernier id traité par jeu).
-- Pas de « drop » (règle N3).

create schema if not exists kb;
revoke all on schema kb from public, anon, authenticated;
grant usage on schema kb to assistant_ro, service_role;

create table if not exists kb.claim (
  id             bigint generated always as identity primary key,
  game           text not null,
  domain         text not null,
  text           text not null,
  source_kind    text not null check (source_kind in
                 ('manuel','devlog','patchnote','discord','forum','chat','observation')),
  source_ref     text not null,
  author         text,
  said_at        timestamptz,
  game_version   text,
  status         text not null default 'en_doute'
                 check (status in ('confirme','complete','contredit','en_doute','obsolete')),
  confidence     numeric(3,2) not null default 0.30 check (confidence between 0 and 1),
  superseded_by  bigint references kb.claim(id),
  contradicts    bigint[] not null default '{}',
  data_check_sql text,
  data_checked_at timestamptz,
  data_verdict   text check (data_verdict in ('confirmé','infirmé','indécis')),
  import_key     text unique,                 -- md5(jeu|fichier|texte) : import idempotent
  origine        jsonb,                       -- {fichier, ligne, section, statut_lu}
  created_at     timestamptz not null default now(),
  fts            tsvector generated always as (to_tsvector('french', text)) stored
);
create index if not exists kb_claim_fts on kb.claim using gin (fts);
create index if not exists kb_claim_game_domain on kb.claim (game, domain, confidence desc);

create table if not exists kb.support (
  claim_id   bigint not null references kb.claim(id),
  author     text not null,
  source_ref text,
  said_at    timestamptz,
  primary key (claim_id, author)
);

create table if not exists kb.ingest_cursor (
  game       text not null,
  source     text not null,                   -- ex. bronze.discord_messages
  last_id    text not null,
  updated_at timestamptz not null default now(),
  primary key (game, source)
);

alter table kb.claim enable row level security;
alter table kb.support enable row level security;
alter table kb.ingest_cursor enable row level security;
create policy assistant_ro_select on kb.claim for select to assistant_ro using (true);
create policy assistant_ro_select on kb.support for select to assistant_ro using (true);
create policy assistant_ro_select on kb.ingest_cursor for select to assistant_ro using (true);
grant select on kb.claim, kb.support, kb.ingest_cursor to assistant_ro;

-- 4.2 Score de confiance. Base selon la source, +0,10 par auteur d'accord (max +0,30),
-- ×0,5 si antérieure au dernier patch du domaine, +0,20 si nos données confirment ;
-- « contredit » si nos données infirment ou si une affirmation contraire plus fiable existe.
create or replace function kb.recompute_confidence(p_game text default null)
returns int
language plpgsql
security definer
set search_path = kb, public
as $$
declare n int;
begin
  with patch as (
    select game, domain, max(said_at) as p from kb.claim
    where source_kind = 'patchnote' and said_at is not null group by 1, 2),
  sup as (select claim_id, count(distinct author) as n from kb.support group by 1)
  update kb.claim c set
    confidence = least(1, greatest(0,
        (case c.source_kind when 'manuel' then 0.90 when 'devlog' then 0.90 when 'patchnote' then 0.90
                            when 'observation' then 0.80 when 'discord' then 0.40 when 'forum' then 0.35
                            else 0.30 end
         + least(0.30, 0.10 * coalesce(s.n, 0)))
        * case when p.p is not null and c.source_kind <> 'patchnote' and c.said_at < p.p then 0.5 else 1 end
        + case when c.data_verdict = 'confirmé' then 0.20 else 0 end))::numeric(3,2),
    status = case when c.data_verdict = 'infirmé' then 'contredit' else c.status end
  from kb.claim c2
  left join sup s on s.claim_id = c2.id
  left join patch p on p.game = c2.game and p.domain = c2.domain
  where c.id = c2.id and (p_game is null or c.game = p_game);
  get diagnostics n = row_count;

  update kb.claim c set status = 'contredit'
  where (p_game is null or c.game = p_game) and c.status not in ('obsolete', 'contredit')
    and exists (select 1 from kb.claim x
                where (x.id = any(c.contradicts) or c.id = any(x.contradicts))
                  and x.status <> 'obsolete' and x.confidence > c.confidence);
  return n;
end $$;
revoke all on function kb.recompute_confidence(text) from public, anon, authenticated;
grant execute on function kb.recompute_confidence(text) to service_role;

-- Import depuis pipelines/migrer_kb.py (REST, clé secrète) : idempotent par import_key, puis recalcul.
create or replace function public.kb_import(p jsonb)
returns jsonb
language plpgsql
security definer
set search_path = kb, public
as $$
declare n_c int; n_s int;
begin
  insert into kb.claim (game, domain, text, source_kind, source_ref, author, said_at, status, import_key, origine)
  select x->>'game', x->>'domain', x->>'text', x->>'source_kind', x->>'source_ref', x->>'author',
         (x->>'said_at')::timestamptz, x->>'status', x->>'import_key', x->'origine'
  from jsonb_array_elements(coalesce(p->'claims', '[]')) x
  on conflict (import_key) do nothing;
  get diagnostics n_c = row_count;

  insert into kb.support (claim_id, author, source_ref, said_at)
  select c.id, y->>'author', y->>'source_ref', (y->>'said_at')::timestamptz
  from jsonb_array_elements(coalesce(p->'support', '[]')) y
  join kb.claim c on c.import_key = y->>'import_key'
  where c.author is distinct from y->>'author'
  on conflict do nothing;
  get diagnostics n_s = row_count;

  perform kb.recompute_confidence(p->>'game');
  return jsonb_build_object('claims', n_c, 'support', n_s,
                            'total', (select count(*) from kb.claim where game = p->>'game'));
end $$;
revoke all on function public.kb_import(jsonb) from public, anon, authenticated;
grant execute on function public.kb_import(jsonb) to service_role;

-- 4.4 Lecture par requête : TOUTES les affirmations du thème (domaine exact, sinon recherche plein texte),
-- avec le compteur total / affichées. Lecture seule.
create or replace function public.kb_search(p_game text, p_theme text, p_min_conf numeric default 0)
returns jsonb
language sql
stable
security definer
set search_path = kb, public
as $$
  with t as (
    select c.* from kb.claim c
    where c.game = p_game
      and (c.domain = p_theme
           or (not exists (select 1 from kb.claim d where d.game = p_game and d.domain = p_theme)
               and c.fts @@ websearch_to_tsquery('french', p_theme)))),
  a as (select * from t where status <> 'obsolete' and confidence >= p_min_conf)
  select jsonb_build_object(
    'total', (select count(*) from t),
    'affichees', (select count(*) from a),
    'obsoletes', (select count(*) from t where status = 'obsolete'),
    'sous_seuil', (select count(*) from t where status <> 'obsolete' and confidence < p_min_conf),
    'claims', coalesce((select jsonb_agg(jsonb_build_object(
        'id', id, 'domain', domain, 'text', text, 'source_kind', source_kind, 'source_ref', source_ref,
        'author', author, 'said_at', said_at::date, 'status', status, 'confidence', confidence,
        'contradicts', contradicts, 'data_verdict', data_verdict)
        order by confidence desc, said_at desc nulls last, id) from a), '[]'))
$$;
revoke all on function public.kb_search(text, text, numeric) from public, anon, authenticated;
grant execute on function public.kb_search(text, text, numeric) to service_role, assistant_ro;
