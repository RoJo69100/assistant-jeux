// ==UserScript==
// @name         Hockey Nation → Supabase (export bronze)
// @namespace    assistant-jeux
// @version      1.0.0
// @description  Capture passive des données chargées par la page ouverte et envoi dans bronze.raw_pages (file persistante, envoi automatique). Aucune requête supplémentaire vers hockey-nation.com.
// @match        https://hockey-nation.com/*
// @match        https://www.hockey-nation.com/*
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

// ---------- Recherches paginées (Coach Center, agents libres, Trade Center) ----------
// Une page cliquée trop vite peut être annulée par le site avant d'arriver : on note les pages reçues
// par recherche (route + tri) et on signale les trous, pour que l'utilisateur y revienne.
const HN_PAGED = /\/api\/(coach-center|free-agent-center|trade-center)\/search\b/;
const HN_LABEL = { 'coach-center': 'Coach Center', 'free-agent-center': 'Agents libres', 'trade-center': 'Trade Center' };
const hnPaged = {};  // clé → { label, pages: Set }

const JEU = {
  game: 'hockeynation',
  short: 'HN',
  color: '#e8590c',
  // + e-mails des autres managers (ownerUsername)
  secretKeys: /^(access_?token|refresh_?token|provider_?token|provider_?refresh_?token|id_?token|token|jwt|password|api_?key|secret|client_?secret|e-?mail|owner_?username)$/i,
  skipUrl: /\/auth\/v1\/|\/auth\/(refresh|token|login|logout|signin|signup)\b|\/_next\/|\/__nextjs|analytics|sentry|posthog|vercel-insights|google/i,
  // Données = réponses JSON ; le HTML n'est gardé que pour le wiki, l'aide, les prix et l'historique des versions.
  dom: { auto: true, tables: 'rows', html: /wiki|help|rules|faq|guide|version-history|awards/i },
  // Routes du site encore inconnues : type générique tiré du chemin (identifiants remplacés par « id »).
  pageType(href, origin) {
    const u = new URL(href, origin);
    const parts = u.pathname.split('/').filter(Boolean)
      .map((x) => (/^\d+$|^[0-9a-f-]{8,}$/i.test(x) ? 'id' : x.toLowerCase().replace(/\.(php|aspx?|html?)$/, '')));
    const base = parts.length ? parts.slice(0, 3).join('_') : 'home';
    const q = ['page', 'view', 'tab', 'subpage'].map((k) => u.searchParams.get(k)).filter(Boolean).join('_');
    return (q ? `${base}_${q}` : base).slice(0, 80);
  },
  onApi(abs) {
    const m = abs.match(HN_PAGED);
    if (!m) return;
    const u = new URL(abs);
    const n = Number(u.searchParams.get('page') || 1);
    u.searchParams.delete('page');
    const key = u.pathname + '?' + u.searchParams.toString();
    const p = hnPaged[key] || (hnPaged[key] = { label: `${HN_LABEL[m[1]]} (${u.searchParams.get('sort') || 'défaut'})`, pages: new Set() });
    p.pages.add(n);
  },
  pagedStatus() {
    return Object.values(hnPaged).map((p) => {
      const max = Math.max(...p.pages);
      const missing = [];
      for (let i = 1; i <= max; i++) if (!p.pages.has(i)) missing.push(i);
      return { text: `${p.label} : ${p.pages.size} pages${missing.length ? `, manquent ${missing.join(', ')}` : ', complet'}`, missing };
    });
  },
};
