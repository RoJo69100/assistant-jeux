// ==UserScript==
// @name         Hardwood → Supabase (export bronze)
// @namespace    assistant-jeux
// @version      0.1.2
// @description  Hardwood (onlinecollegebasketball.org) : chaque page que tu ouvres est copiée (texte, tableaux, HTML) dans une file gardée entre les pages ; un clic sur le bouton envoie toute la file dans bronze.raw_pages. Aucune requête supplémentaire vers le site du jeu.
// @match        *://onlinecollegebasketball.org/*
// @match        *://*.onlinecollegebasketball.org/*
// @run-at       document-start
// @grant        unsafeWindow
// @grant        GM_xmlhttpRequest
// @grant        GM_getValue
// @grant        GM_setValue
// @grant        GM_registerMenuCommand
// @connect      supabase.co
// ==/UserScript==

// Base : multijeux.user.js 0.1.0. Différence : le site recharge la page à chaque clic, donc la file est gardée
// dans le stockage Tampermonkey (GM_setValue) et chaque page est copiée automatiquement à l'ouverture.
// Désactive Hardwood dans multijeux.user.js si tu l'y avais activé (sinon double envoi).
(function () {
  'use strict';

  if (window.top !== window.self) return;           // pas dans les iframes

  const GAME = 'hardwood';
  const CLIENT = 'hardwood.user.js@0.1.1';
  const MAX_HTML_CHARS = 1_500_000;
  const MAX_QUEUE = 150;                            // pages en attente au plus (les plus anciennes sautent)
  const MAX_BODY_CHARS = 3_000_000;
  const SECRET_KEYS = /^(access_?token|refresh_?token|token|jwt|password|passwd|pwd|api_?key|secret|client_?secret|e-?mail|session_?id|csrf.*)$/i;
  const SKIP_URL = /\/login\b|\/logout\b|analytics|sentry|google|doubleclick|facebook|cloudflare|cdn-cgi/i;
  const SKIP_PAGE = /\/(login|logout|register|account|password)\b/i;   // pages sans données de jeu

  const page = unsafeWindow;
  const cfg = () => ({
    url: (GM_getValue('supabaseUrl', '') || '').replace(/\/+$/, ''),
    key: GM_getValue('supabaseKey', ''),
    token: GM_getValue('ingestToken', ''),
  });
  const queue = () => GM_getValue('queue', []);
  const saveQueue = (q) => GM_setValue('queue', q.slice(-MAX_QUEUE));
  const autoOn = () => GM_getValue('auto', true);

  // ---------- Menu ----------
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
    alert('Configuration enregistrée');
  });
  GM_registerMenuCommand('Exporter maintenant', () => exportNow());
  GM_registerMenuCommand('Copie automatique : activer / couper', () => {
    GM_setValue('auto', !autoOn());
    alert(`Copie automatique des pages : ${autoOn() ? 'activée' : 'coupée (seul le bouton copie la page)'}`);
    refresh();
  });
  GM_registerMenuCommand('Vider la file en attente', () => { saveQueue([]); refresh(); });

  function pageType(href) {
    const u = new URL(href, location.origin);
    const parts = u.pathname.split('/').filter(Boolean)
      .map((x) => (/^\d+$/.test(x) ? 'id' : x.toLowerCase().replace(/\.(php|aspx?|html?)$/, '')))
      .filter((x, i, a) => !(x === 'id' && a[i - 1] === 'id'));   // news/0/1 → news_id
    const base = parts.length ? parts.slice(0, 3).join('_') : 'home';
    const q = ['page', 'view', 'tab', 'type', 'mode'].map((k) => u.searchParams.get(k)).filter(Boolean).join('_');
    return (q ? `${base}_${q}` : base).slice(0, 80);
  }

  function scrub(v) {
    if (Array.isArray(v)) return v.map(scrub);
    if (v && typeof v === 'object') {
      const o = {};
      for (const [k, x] of Object.entries(v)) o[k] = SECRET_KEYS.test(k) ? '[retiré]' : scrub(x);
      return o;
    }
    return v;
  }

  function push(item) {
    const q = queue();
    q.push(item);
    saveQueue(q);
    refresh();
  }

  // ---------- Capture passive des réponses JSON (si le site en charge) ----------
  const isOwnSupabase = (url) => { const own = cfg().url; return own && url.startsWith(own); };
  function record(url, method, status, text) {
    try {
      const abs = new URL(url, location.href).href;
      if (SKIP_URL.test(abs) || isOwnSupabase(abs)) return;
      if (status < 200 || status >= 300 || !text || text.length > MAX_BODY_CHARS) return;
      const body = JSON.parse(text);
      push({
        game: GAME, page_type: pageType(location.href), page_url: location.href,
        source: 'api', source_url: abs, captured_at: new Date().toISOString(),
        payload: { method, status, body: scrub(body) }, client: CLIENT,
      });
    } catch (_) { /* pas du JSON : ignoré */ }
  }
  const isJson = (ct) => /json/i.test(ct || '');
  const origFetch = page.fetch;
  if (origFetch) {
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
  }
  const XHR = page.XMLHttpRequest && page.XMLHttpRequest.prototype;
  if (XHR) {
    const origOpen = XHR.open, origSend = XHR.send;
    XHR.open = function (method, url) { this.__cap = { method, url }; return origOpen.apply(this, arguments); };
    XHR.send = function () {
      this.addEventListener('load', function () {
        try {
          if (!this.__cap || !isJson(this.getResponseHeader('content-type'))) return;
          const t = this.responseType === '' || this.responseType === 'text' ? this.responseText : JSON.stringify(this.response);
          record(this.__cap.url, this.__cap.method, this.status, t);
        } catch (_) { /* ignoré */ }
      });
      return origSend.apply(this, arguments);
    };
  }

  // ---------- Copie de la page affichée (les données de Hardwood sont dans le HTML) ----------
  function domSnapshot() {
    const root = document.querySelector('main') || document.body;
    const tables = [...root.querySelectorAll('table')].map((t) => {
      const head = t.querySelector('thead tr') || t.querySelector('tr');
      return {
        caption: (t.caption && t.caption.innerText.trim()) || null,
        headers: head ? [...head.cells].map((c) => c.innerText.trim()) : [],
        rows: [...t.querySelectorAll('tr')].filter((r) => r !== head).map((r) => [...r.cells].map((c) => c.innerText.trim())),
      };
    });
    // Valeurs des formulaires (écrans Game Tactics / Game Management, entraînement) : ce qui est réglé, pas seulement affiché.
    // Le site range chaque réglage dans <span id="green_light_242667"> : on garde cet id (réglage + joueur).
    // Le choix neutre a un libellé vide (« ») : on garde donc aussi la valeur brute de l'option.
    const fields = [...root.querySelectorAll('select, input, textarea')]
      .filter((e) => !/password|hidden|submit|button/i.test(e.type || '') && (e.name || e.id))
      .map((e) => {
        const span = e.closest('span[id]');
        const sel = e.tagName === 'SELECT' ? e.selectedOptions[0] : null;
        return {
          name: e.name || e.id,
          key: span ? span.id : null,
          label: (e.labels && e.labels[0] && e.labels[0].innerText.trim()) || null,
          value: sel ? sel.value : (/checkbox|radio/i.test(e.type) ? (e.checked ? e.value || 'on' : null) : e.value),
          text: sel ? sel.innerText.trim() : undefined,
        };
      })
      .filter((f) => f.value !== null && f.value !== '');
    if (ui) ui.box.style.display = 'none';
    const text = root.innerText;
    const html = root.outerHTML.length <= MAX_HTML_CHARS ? root.outerHTML : null;
    if (ui) ui.box.style.display = '';
    return {
      game: GAME, page_type: pageType(location.href), page_url: location.href,
      source: 'dom', source_url: null, captured_at: new Date().toISOString(),
      payload: { title: document.title, text, tables, fields, html }, client: CLIENT,
    };
  }

  // Copie automatique à l'ouverture de chaque page (et après un changement de contenu), sans doublon.
  let lastKey = '', timer = 0;
  function autoSnapshot(force) {
    if (!force && (!autoOn() || SKIP_PAGE.test(location.pathname))) return;
    const root = document.querySelector('main') || document.body;
    // Page de vérification Cloudflare (anglais ou français) : jamais envoyée, elle écraserait la vraie page en silver.
    if (!root || root.innerText.length < 200 || /Just a moment|Un instant/i.test(document.title)
        || /Ray ID:[\s\S]*Cloudflare/i.test(root.innerText)) return;
    const key = location.href + '|' + root.innerText.length;
    if (!force && key === lastKey) return;
    lastKey = key;
    const q = queue().filter((x) => !(x.source === 'dom' && x.page_url === location.href));   // une copie par page, la dernière
    q.push(domSnapshot());
    saveQueue(q);
    refresh();
  }
  function watch() {
    new MutationObserver(() => { clearTimeout(timer); timer = setTimeout(() => autoSnapshot(false), 1500); })
      .observe(document.body, { childList: true, subtree: true, characterData: true });
    setTimeout(() => autoSnapshot(false), 1500);
  }

  // ---------- Envoi vers Supabase ----------
  function post(items) {
    const c = cfg();
    const headers = { 'Content-Type': 'application/json', apikey: c.key };
    if (c.key.startsWith('eyJ')) headers.Authorization = `Bearer ${c.key}`;
    return new Promise((resolve, reject) => {
      GM_xmlhttpRequest({
        method: 'POST', url: `${c.url}/rest/v1/rpc/ingest_raw_pages`, headers,
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
    if (!c.url || !c.key || !c.token) { toast('Configure Supabase via le menu Tampermonkey', true); return; }
    busy = true;
    autoSnapshot(true);                               // la page affichée, à jour (réglages compris)
    const batch = queue();
    const chunks = [];
    let cur = [], size = 0;
    for (const b of batch) {
      const s = JSON.stringify(b).length;
      if (cur.length && (cur.length >= 30 || size + s > 1_500_000)) { chunks.push(cur); cur = []; size = 0; }
      cur.push(b); size += s;
    }
    if (cur.length) chunks.push(cur);
    let inserted = 0, sent = 0;
    try {
      for (const ch of chunks) { inserted += await post(ch); sent += ch.length; }
      saveQueue([]);
      toast(`Exporté : ${batch.length} pages (${inserted} nouvelles)`);
    } catch (e) {
      saveQueue(batch.slice(sent));
      toast(`Échec après ${sent}/${batch.length} : ${e.message}`, true);
    } finally { busy = false; refresh(); }
  }

  // ---------- Interface ----------
  let ui = null;
  function refresh() {
    if (!ui) return;
    const n = queue().length;
    ui.btn.textContent = `⇪ Hardwood ${n}`;
    ui.btn.title = `${pageType(location.href)} — ${n} page(s) en attente${autoOn() ? '' : ' (copie automatique coupée)'}`;
    ui.btn.style.background = autoOn() ? '#2b8a3e' : '#8a6d2b';
  }
  function toast(msg, err) {
    if (!ui) { console.log('[hardwood export]', msg); return; }
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
    btn.style.cssText = 'cursor:pointer;border:0;border-radius:6px;padding:8px 12px;color:#fff;font-weight:600;box-shadow:0 2px 6px #0006';
    btn.addEventListener('click', exportNow);
    box.append(msg, btn);
    document.body.appendChild(box);
    ui = { box, msg, btn, t: 0 };
    refresh();
    watch();
  }
  if (document.body) mount();
  else document.addEventListener('DOMContentLoaded', mount);
})();
