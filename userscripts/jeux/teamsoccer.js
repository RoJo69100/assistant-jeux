// ==UserScript==
// @name         Team Soccer → Supabase (export bronze)
// @namespace    assistant-jeux
// @version      1.0.0
// @description  Capture passive des données chargées par la page ouverte et envoi dans bronze.raw_pages (file persistante, envoi automatique). Aucune requête supplémentaire vers teamsoccer.org.
// @match        https://teamsoccer.org/*
// @match        https://www.teamsoccer.org/*
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

// Site React sans données dans le HTML : la source est la capture des réponses JSON.
// Deux équipes sur le même compte : chaque capture garde l'adresse de la page, l'équipe se lit dans les réponses.
const JEU = {
  game: 'teamsoccer',
  short: 'TS',
  color: '#e8590c',
  secretKeys: /^(access_?token|refresh_?token|provider_?token|provider_?refresh_?token|id_?token|token|jwt|password|api_?key|secret|client_?secret|e-?mail|owner_?username)$/i,
  skipUrl: /\/auth\/v1\/|\/auth\/(refresh|token|login|logout|signin|signup)\b|\/_next\/|\/__nextjs|\/~api\/analytics|\/__l5e\/|analytics|sentry|posthog|vercel-insights|google/i,
  // Le HTML n'est gardé que pour le visualiseur de match (silver.ts_match_detail lit payload.html) ; texte seul ailleurs :
  // des dizaines de sujets de forum avec leur HTML dépassaient la taille d'envoi.
  dom: { auto: true, tables: 'rows', html: /match-viewer/i },
  // Routes encore inconnues : type générique tiré du chemin (identifiants remplacés par « id »).
  pageType(href, origin) {
    const u = new URL(href, origin);
    const parts = u.pathname.split('/').filter(Boolean)
      .map((x) => (/^\d+$|^[0-9a-f-]{8,}$/i.test(x) ? 'id' : x.toLowerCase().replace(/\.(php|aspx?|html?)$/, '')));
    const base = parts.length ? parts.slice(0, 3).join('_') : 'home';
    const q = ['page', 'view', 'tab', 'subpage'].map((k) => u.searchParams.get(k)).filter(Boolean).join('_');
    return (q ? `${base}_${q}` : base).slice(0, 80);
  },
};
