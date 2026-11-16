// Scénarios du noyau de collecte, sur les fichiers GÉNÉRÉS. Sortie : une ligne JSON par contrôle {nom, ok, detail}.
// Lancé par pipelines/test_userscripts.py (node userscripts/test/scenarios.js).
'use strict';
const { creerEnv } = require('./harness');

const sorties = [];
const controle = (nom, ok, detail) => sorties.push({ nom, ok: Boolean(ok), detail });
const url = (jeu) => ({ basketvibe: 'https://www.basketvibe.com/club/roster', derbymanager: 'https://derbymanager.com/teams/547', hardwood: 'https://onlinecollegebasketball.org/roster/940' }[jeu] || 'https://hockey-nation.com/club/roster');
const api = (env, i, corps) => env.core.record(`https://www.basketvibe.com/api/v1/x/${i}`, 'GET', 200, JSON.stringify(corps || { i }));

async function main() {
  // 1. persistance : les captures survivent à la fermeture de l'onglet (nouvel environnement, même stockage)
  {
    const store = new Map();
    const a = creerEnv({ jeu: 'basketvibe', url: url('basketvibe'), store, respond: () => ({ status: 500, text: 'panne' }) });
    for (let i = 0; i < 5; i++) api(a, i);
    const avant = a.core.listKeys().length;
    const b = creerEnv({ jeu: 'basketvibe', url: url('basketvibe'), store, respond: () => ({ status: 200, text: '5' }) });
    controle('persistance', avant === 5 && b.core.listKeys().length === 5, `${avant} captures avant, ${b.core.listKeys().length} après rechargement`);
    // 2. reprise : l'onglet rouvert envoie la file laissée par l'onglet fermé (3 s après le chargement)
    await b.advance(3500);
    controle('reprise après fermeture', b.calls.length >= 1 && b.core.listKeys().length === 0, `${b.calls.length} appel(s), ${b.core.listKeys().length} restantes`);
    const items = b.corps(0).p_items;
    controle('envoi : champs de la RPC seuls', items.length >= 5 && [...Object.keys(items[0])].sort().join() === 'captured_at,client,game,page_type,page_url,payload,source,source_url', Object.keys(items[0]).join());
    controle('CLIENT = version du script', /^basketvibe\.user\.js@1\.0\.0$/.test(items[0].client), items[0].client);
  }

  // 3. échec : rien n'est retiré, bouton rouge, nouvel essai automatique, puis succès
  {
    let panne = true;
    const e = creerEnv({ jeu: 'basketvibe', url: url('basketvibe'), respond: () => (panne ? { status: 500, text: 'panne' } : { status: 200, text: '3' }) });
    for (let i = 0; i < 3; i++) api(e, i);
    await e.core.flush('test'); await e.settle();
    const txt = e.bouton().textContent;
    controle('échec : captures conservées', e.core.listKeys().length === 3, `${e.core.listKeys().length} en attente`);
    controle('échec : bouton rouge « n en attente · dernier envoi »', e.bouton().style.background === '#b42318' && /3 en attente · dernier envoi jamais/.test(txt), `${txt} / ${e.bouton().style.background}`);
    panne = false;
    await e.advance(31000);
    controle('échec : nouvel essai puis retrait', e.core.listKeys().length === 0 && !/^#b42318$/.test(e.bouton().style.background), `${e.core.listKeys().length} restantes, ${e.bouton().textContent}`);
    controle('succès : heure du dernier envoi affichée', /dernier envoi \d\d:\d\d/.test(e.bouton().textContent), e.bouton().textContent);
  }

  // 4. déclencheurs : seuil de 20, inactivité de 60 s, masquage de l'onglet
  {
    const e = creerEnv({ jeu: 'basketvibe', url: url('basketvibe') });
    for (let i = 0; i < 19; i++) api(e, i);
    await e.settle();
    const avant = e.calls.length;
    api(e, 99); await e.settle();
    controle('envoi au seuil de 20', avant === 0 && e.calls.length === 1 && e.core.listKeys().length === 0, `appels avant ${avant}, après ${e.calls.length}`);
    const f = creerEnv({ jeu: 'basketvibe', url: url('basketvibe'), store: new Map([['auto', false]]) });
    await f.advance(4000);   // passé le contrôle de reprise à 3 s
    api(f, 1); api(f, 2);
    await f.advance(59000);
    const t59 = f.calls.length;
    await f.advance(2000);
    controle('envoi après 60 s d\'inactivité', t59 === 0 && f.calls.length === 1 && f.core.listKeys().length === 0, `à 59 s : ${t59} appel, à 61 s : ${f.calls.length}`);
    const g = creerEnv({ jeu: 'basketvibe', url: url('basketvibe') });
    api(g, 1);
    g.document.visibilityState = 'hidden';
    await g.fire('visibilitychange');
    controle('envoi au masquage (visibilitychange)', g.calls.length >= 1 && g.core.listKeys().length === 0, `${g.calls.length} appel(s)`);
    const h = creerEnv({ jeu: 'basketvibe', url: url('basketvibe') });
    api(h, 1);
    await h.fire('pagehide');
    controle('envoi à la fermeture (pagehide)', h.calls.length >= 1 && h.core.listKeys().length === 0, `${h.calls.length} appel(s)`);
  }

  // 5. paquet refusé (413) : coupé en deux jusqu'à passer, rien de perdu
  {
    const e = creerEnv({ jeu: 'basketvibe', url: url('basketvibe'), store: new Map([['auto', false]]), respond: (d) => (JSON.parse(d.data).p_items.length > 3 ? { status: 413, text: 'trop gros' } : { status: 200, text: '1' }) });
    for (let i = 0; i < 12; i++) api(e, i);
    await e.core.flush('test'); await e.settle();
    controle('paquet refusé : coupé puis envoyé', e.core.listKeys().length === 0, `${e.core.listKeys().length} restantes, ${e.calls.length} appels`);
  }

  // 6. file pleine : les plus anciennes sautent et le bouton le dit
  {
    const e = creerEnv({ jeu: 'basketvibe', url: url('basketvibe'), respond: () => ({ status: 500, text: 'panne' }) });
    e.core.options.maxQueueItems = 10; e.core.options.autoCount = 1000;
    for (let i = 0; i < 15; i++) api(e, i);
    controle('file pleine : plafond et compteur', e.core.listKeys().length === 10 && /5 perdue\(s\)/.test(e.bouton().textContent) && e.store.get('dropped') === 5, `${e.core.listKeys().length} gardées, ${e.bouton().textContent}`);
  }

  // 7. secrets masqués (api) et réponse identique non empilée
  {
    const e = creerEnv({ jeu: 'basketvibe', url: url('basketvibe'), respond: () => ({ status: 500, text: 'x' }) });
    api(e, 1, { access_token: 'SECRET', ok: { password: 'p', nom: 'n' } });
    api(e, 1, { access_token: 'SECRET', ok: { password: 'p', nom: 'n' } });
    const brut = [...e.store.entries()].filter(([k]) => k.startsWith('cap:')).map(([, v]) => v).join('');
    controle('secrets masqués', !/SECRET|"p"/.test(brut) && /\[retiré\]/.test(brut), brut.slice(0, 160));
    controle('même réponse sondée en boucle : une seule capture', e.core.listKeys().length === 1, `${e.core.listKeys().length}`);
  }

  // 8. reprise d'une ancienne file (DerbyManager / Hardwood 0.1.x : tableau sous « queue »)
  {
    const store = new Map([['queue', [{ game: 'hardwood', page_type: 'home', page_url: 'u', source: 'dom', source_url: null, captured_at: '2026-11-01T00:00:00Z', payload: {}, client: 'x' }, { game: 'hardwood', page_type: 'home', page_url: 'v', source: 'dom', source_url: null, captured_at: '2026-11-01T00:00:00Z', payload: {}, client: 'x' }]]]);
    const e = creerEnv({ jeu: 'hardwood', url: url('hardwood'), store, respond: () => ({ status: 500, text: 'x' }) });
    controle('ancienne file reprise', e.core.listKeys().length === 2 && !store.has('queue'), `${e.core.listKeys().length} captures, clé queue ${store.has('queue') ? 'présente' : 'supprimée'}`);
  }

  // 9. copie de la page (mode dom) : une seule copie par page, charge utile par jeu
  for (const jeu of ['basketvibe', 'derbymanager', 'hardwood', 'hockeynation']) {
    const e = creerEnv({ jeu, url: url(jeu), respond: () => ({ status: 500, text: 'x' }), htmlCapture: '<main>' + 'h'.repeat(400) + '</main>' });
    e.core.autoSnapshot(true); e.core.autoSnapshot(true);
    const items = [...e.store.entries()].filter(([k]) => k.startsWith('cap:')).map(([, v]) => JSON.parse(v));
    const it = items[0] || {};
    const cles = Object.keys(it.payload || {}).join();
    const attendu = { basketvibe: 'title,text,tables', derbymanager: 'club,club_name,team_id,club_from,title,text,tables,fields,html', hardwood: 'title,text,tables,fields,html', hockeynation: 'title,text,tables,html' }[jeu];
    controle(`copie de page ${jeu}`, items.length === 1 && it.source === 'dom' && cles === attendu, `${items.length} copie(s), clés : ${cles}`);
  }

  // 10. configuration absente : pas d'envoi, message clair, file intacte
  {
    const e = creerEnv({ jeu: 'basketvibe', url: url('basketvibe'), configurer: false });
    api(e, 1);
    const r = await e.core.flush('test');
    controle('sans configuration : rien envoyé', e.calls.length === 0 && /configuration/.test(r.error || '') && e.core.listKeys().length === 1, JSON.stringify(r));
  }

  // 11. clé API refusée (401) : la capture reste, pas de suppression
  {
    const e = creerEnv({ jeu: 'basketvibe', url: url('basketvibe'), store: new Map([['auto', false]]), respond: () => ({ status: 401, text: '{"code":"28000","message":"jeton invalide"}' }) });
    api(e, 1);
    await e.core.flush('test'); await e.advance(400000);
    controle('jeton refusé : capture jamais supprimée', e.core.listKeys().length === 1 && !e.store.get('rejected'), `${e.core.listKeys().length} en attente`);
  }

  // 12. capture refusée 5 fois seule (400) : écartée et comptée
  {
    const e = creerEnv({ jeu: 'basketvibe', url: url('basketvibe'), store: new Map([['auto', false]]), respond: () => ({ status: 400, text: 'invalide' }) });
    api(e, 1);
    await e.core.flush('test'); await e.advance(30000); await e.advance(60000); await e.advance(120000); await e.advance(300000);
    controle('capture refusée 5 fois : écartée et comptée', e.core.listKeys().length === 0 && e.store.get('rejected') === 1, `${e.core.listKeys().length} en attente, rejetées ${e.store.get('rejected')}`);
  }

  for (const s of sorties) console.log(JSON.stringify(s));
}

main().catch((e) => { console.log(JSON.stringify({ nom: 'exception', ok: false, detail: String(e && e.stack || e) })); process.exit(1); });
