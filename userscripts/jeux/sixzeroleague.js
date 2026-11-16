// ==UserScript==
// @name         SixZero League → Supabase (export bronze)
// @namespace    assistant-jeux
// @version      1.0.1
// @description  Capture passive des données chargées par la page ouverte et envoi dans bronze.raw_pages (file persistante, envoi automatique). Aucune requête supplémentaire vers sixzeroleague.com.
// @match        https://sixzeroleague.com/*
// @match        https://www.sixzeroleague.com/*
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
  game: 'sixzeroleague',
  short: '60',
  color: '#e8590c',
  // + e-mails des autres managers (ownerUsername)
  secretKeys: /^(access_?token|refresh_?token|provider_?token|provider_?refresh_?token|id_?token|token|jwt|password|api_?key|secret|client_?secret|e-?mail|owner_?username)$/i,
  // /hubs/ = négociation SignalR (chat, compétitions, transferts) : jetons de connexion, aucune donnée de jeu.
  skipUrl: /\/auth\/v1\/|\/auth\/(refresh|token|login|logout|signin|signup)\b|\/_next\/|\/__nextjs|\/hubs\/|analytics|sentry|posthog|vercel-insights|google/i,
  // Données = réponses JSON ; le HTML n'est gardé que pour le wiki et l'aide.
  dom: { auto: true, tables: 'rows', html: /wiki|help|rules|faq|guide/i },
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
