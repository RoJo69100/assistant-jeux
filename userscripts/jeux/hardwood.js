// ==UserScript==
// @name         Hardwood → Supabase (export bronze)
// @namespace    assistant-jeux
// @version      1.0.0
// @description  Hardwood (onlinecollegebasketball.org) : chaque page que tu ouvres est copiée (texte, tableaux, réglages, HTML) dans une file gardée entre les pages et envoyée automatiquement dans bronze.raw_pages. Aucune requête supplémentaire vers le site du jeu.
// @match        *://onlinecollegebasketball.org/*
// @match        *://*.onlinecollegebasketball.org/*
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

// Le site recharge la page à chaque clic : la file est gardée dans le stockage Tampermonkey et chaque page est copiée
// automatiquement à l'ouverture. Désactive Hardwood dans multijeux.user.js si tu l'y avais activé (sinon double envoi).
const JEU = {
  game: 'hardwood',
  short: 'HW',
  color: '#2b8a3e',
  secretKeys: /^(access_?token|refresh_?token|token|jwt|password|passwd|pwd|api_?key|secret|client_?secret|e-?mail|session_?id|csrf.*)$/i,
  skipUrl: /\/login\b|\/logout\b|analytics|sentry|google|doubleclick|facebook|cloudflare|cdn-cgi/i,
  skipPage: /\/(login|logout|register|account|password)\b/i,   // pages sans données de jeu
  // Les données de Hardwood sont dans le HTML. Chaque réglage est rangé dans <span id="green_light_242667"> : on garde cet id.
  dom: {
    auto: true, tables: 'rows', html: true, caption: true,
    fields: { excludeTypes: /password|hidden|submit|button/i, wrapSelector: 'span[id]', minMax: false },
  },
  pageType(href, origin) {
    const u = new URL(href, origin);
    const parts = u.pathname.split('/').filter(Boolean)
      .map((x) => (/^\d+$/.test(x) ? 'id' : x.toLowerCase().replace(/\.(php|aspx?|html?)$/, '')))
      .filter((x, i, a) => !(x === 'id' && a[i - 1] === 'id'));   // news/0/1 → news_id
    const base = parts.length ? parts.slice(0, 3).join('_') : 'home';
    const q = ['page', 'view', 'tab', 'type', 'mode'].map((k) => u.searchParams.get(k)).filter(Boolean).join('_');
    return (q ? `${base}_${q}` : base).slice(0, 80);
  },
};
