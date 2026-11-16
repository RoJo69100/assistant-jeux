// ==UserScript==
// @name         Derby Manager → Supabase (export bronze)
// @namespace    assistant-jeux
// @version      1.0.0
// @description  Derby Manager (derbymanager.com) : chaque page que tu ouvres est copiée (texte, tableaux, réglages, HTML, réponses JSON) dans une file gardée entre les pages, marquée du club (Queen of the South 547 / Marmandes 307), et envoyée automatiquement dans bronze.raw_pages. Aucune requête supplémentaire vers le site du jeu.
// @match        *://derbymanager.com/*
// @match        *://*.derbymanager.com/*
// @run-at       document-start
// @grant        unsafeWindow
// @grant        GM_xmlhttpRequest
// @grant        GM_getValue
// @grant        GM_setValue
// @grant        GM_deleteValue
// @grant        GM_listValues
// @grant        GM_registerMenuCommand
// @connect      supabase.co
// ==/UserScript==

// Deux clubs gérés : chaque copie porte payload.club (identifiant 547 ou 307, lu dans l'URL, sinon dans le nom du club
// affiché, sinon le dernier club vu).
const DM_CLUBS = [
  { id: '547', name: 'Queen of the South', re: /queen of the south/i },
  { id: '307', name: 'Marmandes', re: /marmande/i },
];

// Club de la page : URL /teams/547 ou /teams/307, sinon nom du club actif dans l'en-tête, sinon le dernier vu.
// « autre » = page d'un club adverse (son identifiant est gardé dans team_id).
function dmClub() {
  const m = location.pathname.match(/\/teams?\/(\d+)/i);
  if (m) {
    const c = DM_CLUBS.find((x) => x.id === m[1]);
    if (c) { GM_setValue('lastClub', c.id); return { club: c.id, club_name: c.name, team_id: m[1], club_from: 'url' }; }
    return { club: 'autre', club_name: null, team_id: m[1], club_from: 'url', active_club: GM_getValue('lastClub', null) };
  }
  const head = document.querySelector('header, nav, .navbar, #navbar, .sidebar, aside');
  const txt = head ? head.innerText : '';
  const hits = DM_CLUBS.filter((x) => x.re.test(txt));
  if (hits.length === 1) {
    GM_setValue('lastClub', hits[0].id);
    return { club: hits[0].id, club_name: hits[0].name, team_id: null, club_from: 'entete' };
  }
  const last = DM_CLUBS.find((x) => x.id === GM_getValue('lastClub', ''));
  return { club: last ? last.id : null, club_name: last ? last.name : null, team_id: null, club_from: last ? 'dernier_vu' : 'inconnu' };
}

const JEU = {
  game: 'derbymanager',
  short: 'DM',
  color: '#2b8a3e',
  secretKeys: /^(access_?token|refresh_?token|token|jwt|password|passwd|pwd|api_?key|secret|client_?secret|e-?mail|session_?id|csrf.*|_token|xsrf.*)$/i,
  skipUrl: /\/login\b|\/logout\b|analytics|sentry|google|doubleclick|facebook|cloudflare|cdn-cgi|pusher|broadcasting/i,
  skipPage: /\/(login|logout|register|account|password|settings)\b/i,   // pages sans données de jeu
  extraPayload: dmClub,
  label() { const c = dmClub(); return `DM ${c.club_name ? c.club_name.split(' ')[0] : c.club || '?'}`; },
  dom: {
    auto: true, tables: 'rows', html: true, caption: true,
    linkSelector: 'a[href*="/players/"], a[href*="/teams/"], a[href*="/matches/"]',
    fields: { excludeTypes: /password|hidden|submit|button|file/i, wrapSelector: '[id]', minMax: true },
  },
  pageType(href, origin) {
    const u = new URL(href, origin);
    const parts = u.pathname.split('/').filter(Boolean)
      .map((x) => (/^\d+$/.test(x) ? 'id' : x.toLowerCase().replace(/\.(php|aspx?|html?)$/, '')))
      .filter((x, i, a) => !(x === 'id' && a[i - 1] === 'id'));
    const base = parts.length ? parts.slice(0, 3).join('_') : 'home';
    const q = ['view', 'tab', 'page', 'type', 'mode'].map((k) => u.searchParams.get(k)).filter(Boolean).join('_');
    return (q ? `${base}_${q}` : base).slice(0, 80);
  },
};
