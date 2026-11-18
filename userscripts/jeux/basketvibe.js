// ==UserScript==
// @name         BasketVibe → Supabase (export bronze)
// @namespace    assistant-jeux
// @version      1.1.0
// @description  Capture passive des données chargées par la page ouverte et envoi dans bronze.raw_pages (file persistante, envoi automatique). Aucune requête supplémentaire vers basketvibe.com.
// @match        https://www.basketvibe.com/*
// @match        https://basketvibe.com/*
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

const JEU = {
  game: 'basketvibe',
  short: 'BV',
  color: '#e8590c',
  secretKeys: /^(access_?token|refresh_?token|provider_?token|provider_?refresh_?token|id_?token|token|jwt|password|api_?key|secret|client_?secret)$/i,
  skipUrl: /\/auth\/v1\/|\/auth\/(refresh|token|login|logout|signin|signup)\b|\/_next\/|\/__nextjs|analytics|sentry|posthog|vercel-insights|google/i,
  // Copie de la page : texte + tableaux (thead/tbody), pas de HTML. Copie automatique sur toutes les pages.
  dom: { auto: true, tables: 'thead', html: false },
  // Routes confirmées par samples/basketvibe. /cup/<id> (match de coupe) et /c/<slug> (page publique d'un club) :
  // classées « unknown » avant la version 1.0.0 de ce script.
  pageType(href, origin) {
    const u = new URL(href, origin);
    const p = u.pathname.replace(/\/+$/, '') || '/';
    const tab = u.searchParams.get('tab');
    const withTab = (base) => (tab ? `${base}_${tab}` : base);
    if (p === '/club/roster') return withTab('roster');          // effectif, ?tab=skills, ?tab=statistics
    if (p === '/club/training') return withTab('training');      // ?tab=progress
    if (p === '/club/tactics') return withTab('tactics');
    if (p === '/club/finance') return withTab('finance');        // ?tab=sponsor
    if (p === '/club/personnel') return withTab('personnel');
    if (p === '/club/academy') return withTab('academy');
    if (p.startsWith('/transfers')) return withTab('transfers');
    if (/^\/match\/[^/]+$/.test(p)) return withTab('match');
    if (/^\/friendly\/[^/]+$/.test(p)) return withTab('friendly');
    if (/^\/cup\/[^/]+$/.test(p)) return withTab('cup');
    if (/^\/c\/[^/]+$/.test(p)) return withTab('club_public');   // ?tab=statistics (effectif), schedule, history…
    if (p === '/club') return withTab('club');
    if (p === '/news') return 'news';
    if (p === '/notifications') return 'notifications';
    if (/^\/player\/[^/]+$/.test(p)) return withTab('player');
    if (p === '/league/table') return withTab('standings');      // ?tab=clubs, schedule, teams, players, injuries, transfers
    if (p === '/league/schedule') return withTab('schedule');
    if (p.startsWith('/league')) return withTab('league');
    if (p === '/competition/cups') return withTab('cups');
    if (p === '/world') return withTab('world');
    return 'unknown';
  },
};
