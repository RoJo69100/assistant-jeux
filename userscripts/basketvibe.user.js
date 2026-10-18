// ==UserScript==
// @name         BasketVibe → Supabase (export bronze)
// @namespace    assistant-jeux
// @version      0.1.3
// @description  Capture passive des données chargées par la page ouverte et envoi dans bronze.raw_pages. Aucune requête supplémentaire vers basketvibe.com.
// @match        https://www.basketvibe.com/*
// @match        https://basketvibe.com/*
// @run-at       document-start
// @grant        unsafeWindow
// @grant        GM_xmlhttpRequest
// @grant        GM_getValue
// @grant        GM_setValue
// @grant        GM_registerMenuCommand
// @connect      supabase.co
// ==/UserScript==

(function () {
  'use strict';

  const GAME = 'basketvibe';
  const CLIENT = 'basketvibe.user.js@0.1.1';
  const MAX_CAPTURES = 300;
  const MAX_BODY_CHARS = 3_000_000;
  const SECRET_KEYS = /^(access_?token|refresh_?token|provider_?token|provider_?refresh_?token|id_?token|token|jwt|password|api_?key|secret|client_?secret)$/i;
  const SKIP_URL = /\/auth\/|\/_next\/|\/__nextjs|analytics|sentry|posthog|vercel-insights|google/i;

  const page = unsafeWindow;
  const captures = [];   // en attente d'envoi
  let ui = null;

  // ---------- Config (menu Tampermonkey) ----------
  const cfg = () => ({
    url: (GM_getValue('supabaseUrl', '') || '').replace(/\/+$/, ''),
    key: GM_getValue('supabaseKey', ''),
    token: GM_getValue('ingestToken', ''),
  });

  GM_registerMenuCommand('Configurer Supabase', () => {
    const c = cfg();
    const url = prompt('URL Supabase (https://xxxx.supabase.co)', c.url);
    if (url === null) return;
    const key = prompt('Clé publishable (sb_publishable_…) ou anon', c.key);
    if (key === null) return;
    const token = prompt("Jeton d'ingestion (INGEST_TOKEN)", c.token);
    if (token === null) return;
    GM_setValue('supabaseUrl', url.trim());
    GM_setValue('supabaseKey', key.trim());
    GM_setValue('ingestToken', token.trim());
    toast('Configuration enregistrée');
  });
  GM_registerMenuCommand('Exporter maintenant', () => exportNow());
  GM_registerMenuCommand('Vider les captures en attente', () => { captures.length = 0; refresh(); });

  // ---------- Type de page à partir de la route ----------
  // Routes confirmées par samples/basketvibe ; les autres (joueur, classement, calendrier) sont à vérifier.
  function pageType(href) {
    const u = new URL(href, location.origin);
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
  }

  // ---------- Capture passive ----------
  function scrub(v) {
    if (Array.isArray(v)) return v.map(scrub);
    if (v && typeof v === 'object') {
      const o = {};
      for (const [k, x] of Object.entries(v)) o[k] = SECRET_KEYS.test(k) ? '[retiré]' : scrub(x);
      return o;
    }
    return v;
  }

  function isOwnSupabase(url) {
    const own = cfg().url;
    return own && url.startsWith(own);
  }

  function record(url, method, status, text) {
    try {
      const abs = new URL(url, location.href).href;
      if (SKIP_URL.test(abs) || isOwnSupabase(abs)) return;
      if (status < 200 || status >= 300 || !text || text.length > MAX_BODY_CHARS) return;
      const body = JSON.parse(text);
      captures.push({
        game: GAME,
        page_type: pageType(location.href),
        page_url: location.href,
        source: 'api',
        source_url: abs,
        captured_at: new Date().toISOString(),
        payload: { method, status, body: scrub(body) },
        client: CLIENT,
      });
      if (captures.length > MAX_CAPTURES) captures.shift();
      refresh();
    } catch (_) { /* pas du JSON : ignoré */ }
  }

  const isJson = (ct) => /json/i.test(ct || '');

  const origFetch = page.fetch;
  page.fetch = function (input, init) {
    const p = origFetch.apply(this, arguments);
    p.then((res) => {
      if (!isJson(res.headers.get('content-type'))) return;
      const url = typeof input === 'string' ? input : (input && input.url) || String(input);
      const method = (init && init.method) || (input && input.method) || 'GET';
      res.clone().text().then((t) => record(url, method, res.status, t)).catch(() => {});
    }).catch(() => {});
    return p;
  };

  const XHR = page.XMLHttpRequest.prototype;
  const origOpen = XHR.open;
  const origSend = XHR.send;
  XHR.open = function (method, url) {
    this.__bv = { method, url };
    return origOpen.apply(this, arguments);
  };
  XHR.send = function () {
    this.addEventListener('load', function () {
      try {
        if (!this.__bv || !isJson(this.getResponseHeader('content-type'))) return;
        const t = this.responseType === '' || this.responseType === 'text'
          ? this.responseText
          : JSON.stringify(this.response);
        record(this.__bv.url, this.__bv.method, this.status, t);
      } catch (_) { /* ignoré */ }
    });
    return origSend.apply(this, arguments);
  };

  // ---------- Instantané DOM (filet de sécurité, lu depuis la page déjà affichée) ----------
  function domSnapshot() {
    const root = document.querySelector('main') || document.body;
    const tables = [...root.querySelectorAll('table')].map((t) => ({
      headers: [...t.querySelectorAll('thead th, thead td')].map((c) => c.innerText.trim()),
      rows: [...t.querySelectorAll('tbody tr')].map((r) => [...r.cells].map((c) => c.innerText.trim())),
    }));
    // Masquer le bouton du script pour qu'il n'apparaisse pas dans le texte capturé.
    if (ui) ui.box.style.display = 'none';
    const text = root.innerText;
    if (ui) ui.box.style.display = '';
    return {
      game: GAME,
      page_type: pageType(location.href),
      page_url: location.href,
      source: 'dom',
      source_url: null,
      captured_at: new Date().toISOString(),
      payload: { title: document.title, text, tables },
      client: CLIENT,
    };
  }

  // ---------- Envoi vers Supabase ----------
  function post(items) {
    const c = cfg();
    const headers = { 'Content-Type': 'application/json', apikey: c.key };
    if (c.key.startsWith('eyJ')) headers.Authorization = `Bearer ${c.key}`; // ancienne clé anon (JWT)
    return new Promise((resolve, reject) => {
      GM_xmlhttpRequest({
        method: 'POST',
        url: `${c.url}/rest/v1/rpc/ingest_raw_pages`,
        headers,
        data: JSON.stringify({ p_token: c.token, p_items: items }),
        onload: (r) => (r.status >= 200 && r.status < 300
          ? resolve(Number(r.responseText) || 0)
          : reject(new Error(`HTTP ${r.status} : ${r.responseText.slice(0, 200)}`))),
        onerror: () => reject(new Error('réseau')),
      });
    });
  }

  let busy = false;
  async function exportNow() {
    if (busy) return;
    const c = cfg();
    if (!c.url || !c.key || !c.token) {
      toast('Configure Supabase via le menu Tampermonkey', true);
      return;
    }
    busy = true;
    const batch = captures.splice(0, captures.length);
    batch.push(domSnapshot());
    try {
      let inserted = 0;
      for (let i = 0; i < batch.length; i += 50) inserted += await post(batch.slice(i, i + 50));
      toast(`Exporté : ${batch.length} captures (${inserted} nouvelles)`);
    } catch (e) {
      captures.unshift(...batch.filter((b) => b.source === 'api'));
      toast(`Échec : ${e.message}`, true);
    } finally {
      busy = false;
      refresh();
    }
  }

  // ---------- Interface ----------
  function refresh() {
    if (!ui) return;
    ui.btn.textContent = `⇪ BV ${captures.length}`;
    ui.btn.title = `${pageType(location.href)} — ${captures.length} réponse(s) en attente`;
  }

  function toast(msg, err) {
    if (!ui) { console.log('[BV export]', msg); return; }
    ui.msg.textContent = msg;
    ui.msg.style.background = err ? '#b42318' : '#1f6f43';
    ui.msg.style.display = 'block';
    clearTimeout(ui.t);
    ui.t = setTimeout(() => { ui.msg.style.display = 'none'; }, 4000);
  }

  function mount() {
    const box = document.createElement('div');
    box.style.cssText = 'position:fixed;right:12px;bottom:12px;z-index:2147483647;font:13px system-ui;display:flex;flex-direction:column;align-items:flex-end;gap:6px';
    const msg = document.createElement('div');
    msg.style.cssText = 'display:none;color:#fff;padding:6px 10px;border-radius:6px;max-width:320px';
    const btn = document.createElement('button');
    btn.style.cssText = 'cursor:pointer;border:0;border-radius:6px;padding:8px 12px;background:#e8590c;color:#fff;font-weight:600;box-shadow:0 2px 6px #0006';
    btn.addEventListener('click', exportNow);
    box.append(msg, btn);
    document.body.appendChild(box);
    ui = { box, msg, btn, t: 0 };
    refresh();
  }

  if (document.body) mount();
  else document.addEventListener('DOMContentLoaded', mount);

  // Navigation SPA : mettre à jour l'info-bulle quand la route change.
  for (const m of ['pushState', 'replaceState']) {
    const orig = page.history[m];
    page.history[m] = function () {
      const r = orig.apply(this, arguments);
      setTimeout(refresh, 0);
      return r;
    };
  }
  page.addEventListener('popstate', refresh);
})();
