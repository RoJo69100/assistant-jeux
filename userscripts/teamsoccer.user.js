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
// GÉNÉRÉ par pipelines/build_userscripts.py depuis userscripts/core.js et userscripts/jeux/teamsoccer.js : ne pas modifier ce fichier.

(function () {
  'use strict';

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

// Noyau commun des userscripts de collecte (refonte v3, brique « collecte »).
// Ce fichier n'est PAS un userscript : pipelines/build_userscripts.py le colle après userscripts/jeux/<jeu>.js
// (qui définit la constante JEU) dans une seule fonction : un fichier par jeu, aucune dépendance externe.
//
// Règle 1 : collecte passive. Lecture des réponses JSON que le site charge déjà (mode api) et de la page
// affichée (mode dom) ; aucune requête vers le jeu. Seule requête sortante : l'envoi vers Supabase.
//
// File persistante : une clé GM_setValue par capture (« cap:<date><n><hasard>:<taille> »). Une capture n'est
// supprimée qu'après la réponse 2xx de ingest_raw_pages ; tout échec la laisse en place et déclenche un nouvel essai.
// Les renvois sont sans risque : ingest_raw_pages ignore les doublons (on conflict do nothing).

if (window.top !== window.self) return;   // pas dans les iframes

const GAME = JEU.game;
const CLIENT = GAME + '.user.js@1.0.0';
const O = Object.assign({
  autoCount: 20,            // envoi dès 20 captures en attente
  idleMs: 60000,            // ... ou 60 s après la dernière capture
  maxBodyChars: 3_000_000,  // réponse JSON plus grosse : ignorée
  maxHtmlChars: 1_500_000,
  chunkItems: 30,           // captures par appel
  chunkChars: 1_500_000,    // caractères par appel (un appel contient toujours au moins une capture)
  maxQueueItems: 400,       // au-delà : les plus anciennes sautent, et le bouton le dit
  maxQueueChars: 40_000_000,
  domMinText: 200,
  domDebounceMs: 1500,
  retryMs: [30000, 60000, 120000, 300000],
}, JEU.opts || {});
const DOM = Object.assign({ auto: true, tables: 'rows', html: false, caption: false, linkSelector: null, fields: null }, JEU.dom || {});
const PREFIX = 'cap:';
const CLOUDFLARE_TITLE = /Just a moment|Un instant/i;
const CLOUDFLARE_TEXT = /Ray ID:[\s\S]*Cloudflare/i;

const page = unsafeWindow;
let ui = null;

// ---------- Configuration (menu Tampermonkey) ----------
const cfg = () => ({
  url: (GM_getValue('supabaseUrl', '') || '').replace(/\/+$/, ''),
  key: GM_getValue('supabaseKey', ''),
  token: GM_getValue('ingestToken', ''),
});
const autoOn = () => GM_getValue('auto', true);
const num = (k) => Number(GM_getValue(k, 0)) || 0;

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
GM_registerMenuCommand('Copie automatique des pages : activer / couper', () => {
  GM_setValue('auto', !autoOn());
  toast(`Copie automatique des pages : ${autoOn() ? 'activée' : 'coupée (seul le bouton copie la page)'}`);
  refresh();
});
GM_registerMenuCommand('Taille de la file en attente', () => {
  const s = queueStats();
  toast(`${s.n} en attente, ${(s.chars / 1e6).toFixed(2)} M caractères ; perdues ${num('dropped')}, rejetées ${num('rejected')}`);
});
GM_registerMenuCommand('Vider la file en attente', () => {
  for (const k of listKeys()) GM_deleteValue(k);
  GM_setValue('dropped', 0);
  GM_setValue('rejected', 0);
  refresh();
});

// ---------- File persistante ----------
let seq = 0;
const listKeys = () => GM_listValues().filter((k) => k.startsWith(PREFIX)).sort();
const sizeOf = (k) => Number(k.slice(k.lastIndexOf(':') + 1)) || 0;
const newKey = (size) => PREFIX + Date.now().toString(36).padStart(9, '0') + (++seq).toString(36).padStart(4, '0')
  + Math.random().toString(36).slice(2, 6) + ':' + size;

function queueStats() {
  const keys = listKeys();
  return { n: keys.length, chars: keys.reduce((t, k) => t + sizeOf(k), 0) };
}

// Reprise d'une ancienne file (versions 0.1.x de DerbyManager et Hardwood : tableau sous la clé « queue »).
function migrateOldQueue() {
  try {
    const old = GM_getValue('queue', null);
    if (!Array.isArray(old)) return;
    for (const item of old) { const s = JSON.stringify(item); GM_setValue(newKey(s.length), s); }
    GM_deleteValue('queue');
  } catch (_) { /* ignoré */ }
}

function enforceCaps() {
  const keys = listKeys();
  let total = keys.reduce((t, k) => t + sizeOf(k), 0);
  let lost = 0;
  while (keys.length > 1 && (keys.length > O.maxQueueItems || total > O.maxQueueChars)) {
    const k = keys.shift();
    total -= sizeOf(k);
    GM_deleteValue(k);
    lost++;
  }
  if (lost) GM_setValue('dropped', num('dropped') + lost);
}

let idleTimer = 0;
function armIdle() {
  clearTimeout(idleTimer);
  idleTimer = setTimeout(() => flush('inactivité'), O.idleMs);
}

function enqueue(item) {
  const s = JSON.stringify(item);
  const key = newKey(s.length);
  GM_setValue(key, s);
  enforceCaps();
  armIdle();
  refresh();
  if (listKeys().length >= O.autoCount) flush('seuil');
  return key;
}

// ---------- Capture passive : réponses JSON (mode api) ----------
function scrub(v) {
  if (Array.isArray(v)) return v.map(scrub);
  if (v && typeof v === 'object') {
    const o = {};
    for (const [k, x] of Object.entries(v)) o[k] = JEU.secretKeys.test(k) ? '[retiré]' : scrub(x);
    return o;
  }
  return v;
}

const isOwnSupabase = (url) => { const own = cfg().url; return own && url.startsWith(own); };
const extra = () => (JEU.extraPayload ? JEU.extraPayload() : {});
const lastSeen = new Map();   // source_url -> empreinte de la dernière réponse (évite d'empiler la même réponse sondée en boucle)
function fingerprint(t) { let h = 5381; for (let i = 0; i < t.length; i++) h = ((h * 33) ^ t.charCodeAt(i)) >>> 0; return t.length + ':' + h; }

function record(url, method, status, text) {
  try {
    const abs = new URL(url, location.href).href;
    if (JEU.skipUrl.test(abs) || isOwnSupabase(abs)) return;
    if (status < 200 || status >= 300 || !text || text.length > O.maxBodyChars) return;
    const body = JSON.parse(text);
    const fp = fingerprint(text);
    if (lastSeen.get(abs) === fp) return;
    lastSeen.set(abs, fp);
    if (JEU.onApi) JEU.onApi(abs);
    enqueue({
      game: GAME, page_type: JEU.pageType(location.href, location.origin), page_url: location.href,
      source: 'api', source_url: abs, captured_at: new Date().toISOString(),
      payload: { ...extra(), method, status, body: scrub(body) }, client: CLIENT,
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
  const origOpen = XHR.open;
  const origSend = XHR.send;
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

// ---------- Capture passive : page affichée (mode dom) ----------
const inPath = (rule, path) => rule === true || (rule instanceof RegExp && rule.test(path));

function tableData(t) {
  let headers; let rows;
  if (DOM.tables === 'thead') {
    headers = [...t.querySelectorAll('thead th, thead td')].map((c) => c.innerText.trim());
    rows = [...t.querySelectorAll('tbody tr')].map((r) => [...r.cells].map((c) => c.innerText.trim()));
  } else {
    const head = t.querySelector('thead tr') || t.querySelector('tr');
    headers = head ? [...head.cells].map((c) => c.innerText.trim()) : [];
    rows = [...t.querySelectorAll('tr')].filter((r) => r !== head).map((r) => [...r.cells].map((c) => c.innerText.trim()));
  }
  const o = {};
  if (DOM.caption) o.caption = (t.caption && t.caption.innerText.trim()) || null;
  o.headers = headers;
  o.rows = rows;
  if (DOM.linkSelector) {
    o.links = [...t.querySelectorAll(DOM.linkSelector)].map((a) => ({ text: a.innerText.trim(), href: a.getAttribute('href') }));
  }
  return o;
}

// Réglages (tactique, entraînement…) : ce qui est réglé, pas seulement affiché.
function fieldsData(root) {
  const F = DOM.fields;
  return [...root.querySelectorAll('select, input, textarea')]
    .filter((e) => !F.excludeTypes.test(e.type || '') && (e.name || e.id))
    .map((e) => {
      const sel = e.tagName === 'SELECT' ? e.selectedOptions[0] : null;
      const wrap = e.closest(F.wrapSelector);
      const f = {
        name: e.name || e.id,
        key: wrap && wrap !== e ? wrap.id : null,
        label: (e.labels && e.labels[0] && e.labels[0].innerText.trim()) || null,
        value: sel ? sel.value : (/checkbox|radio/i.test(e.type) ? (e.checked ? e.value || 'on' : null) : e.value),
        text: sel ? sel.innerText.trim() : undefined,
      };
      if (F.minMax) { f.min = e.min || undefined; f.max = e.max || undefined; }
      return f;
    })
    .filter((f) => f.value !== null && f.value !== '');
}

// Texte de la page sans le bouton du script.
function pageText(root) {
  if (ui) ui.box.style.display = 'none';
  const text = root.innerText || '';
  if (ui) ui.box.style.display = '';
  return text;
}

function domSnapshot() {
  const root = document.querySelector('main') || document.body;
  const tables = [...root.querySelectorAll('table')].map(tableData);
  const fields = DOM.fields ? fieldsData(root) : undefined;
  if (ui) ui.box.style.display = 'none';
  const text = root.innerText;
  const withHtml = inPath(DOM.html, location.pathname) && root.outerHTML.length <= O.maxHtmlChars;
  const html = withHtml ? root.outerHTML : null;
  if (ui) ui.box.style.display = '';
  const payload = { ...extra(), title: document.title, text, tables };
  if (DOM.fields) payload.fields = fields;
  if (DOM.html) payload.html = html;
  return {
    game: GAME, page_type: JEU.pageType(location.href, location.origin), page_url: location.href,
    source: 'dom', source_url: null, captured_at: new Date().toISOString(), payload, client: CLIENT,
  };
}

let lastDomKey = '';
const domKeys = new Map();   // page_url -> clé de la copie en attente (une copie par page : la dernière)
function autoSnapshot(force) {
  if (!force && (!autoOn() || !inPath(DOM.auto, location.pathname))) return;
  if (JEU.skipPage && JEU.skipPage.test(location.pathname)) return;
  const root = document.querySelector('main') || document.body;
  if (!root) return;
  const text = pageText(root);
  if (text.length < (DOM.minText || O.domMinText) || CLOUDFLARE_TITLE.test(document.title) || CLOUDFLARE_TEXT.test(text)) return;
  const key = location.href + '|' + text.length;
  if (!force && key === lastDomKey) return;
  lastDomKey = key;
  const prev = domKeys.get(location.href);
  if (prev) GM_deleteValue(prev);
  domKeys.set(location.href, enqueue(domSnapshot()));
}

let domTimer = 0;
function scheduleDom() {
  clearTimeout(domTimer);
  domTimer = setTimeout(() => autoSnapshot(false), O.domDebounceMs);
}
function watchDom() {
  new MutationObserver((muts) => {
    if (ui && muts.every((m) => ui.box.contains(m.target))) return;   // le bouton qui change ne déclenche pas de copie
    scheduleDom();
  }).observe(document, { childList: true, subtree: true, characterData: true });
  for (const m of ['pushState', 'replaceState']) {
    const orig = page.history[m];
    page.history[m] = function () {
      const r = orig.apply(this, arguments);
      setTimeout(refresh, 0);
      scheduleDom();
      return r;
    };
  }
  page.addEventListener('popstate', () => { refresh(); scheduleDom(); });
  scheduleDom();
}

// ---------- Envoi vers Supabase ----------
function post(body) {
  const c = cfg();
  const headers = { 'Content-Type': 'application/json', apikey: c.key };
  if (c.key.startsWith('eyJ')) headers.Authorization = `Bearer ${c.key}`;   // ancienne clé anon (JWT)
  return new Promise((resolve, reject) => {
    GM_xmlhttpRequest({
      method: 'POST', url: `${c.url}/rest/v1/rpc/ingest_raw_pages`, headers, data: body, timeout: 60000,
      onload: (r) => {
        if (r.status >= 200 && r.status < 300) { resolve(Number(r.responseText) || 0); return; }
        const e = new Error(`HTTP ${r.status} : ${String(r.responseText || '').slice(0, 200)}`);
        e.status = r.status;
        reject(e);
      },
      onerror: () => reject(new Error('réseau')),
      ontimeout: () => reject(new Error('délai dépassé')),
    });
  });
}

let busy = false;
let again = false;
let lastError = null;
let fails = 0;
let chunkLimit = O.chunkItems;
let retryTimer = 0;
const rejects = {};

const isAuthError = (e) => e.status === 401 || e.status === 403 || /jeton|28000/i.test(e.message || '');

function nextChunk(keys) {
  const out = [];
  let chars = 0;
  for (const k of keys) {
    if (out.length >= chunkLimit) break;
    const raw = GM_getValue(k, null);
    if (typeof raw !== 'string') { GM_deleteValue(k); continue; }
    if (out.length && chars + raw.length > O.chunkChars) break;
    out.push({ key: k, raw });
    chars += raw.length;
  }
  return out;
}

// Envoie tout ce qui est en attente. Chaque capture est supprimée seulement après la réponse 2xx de son paquet.
async function flush(reason) {
  if (busy) { again = true; return { sent: 0, inserted: 0, error: null, busy: true }; }
  const c = cfg();
  if (!c.url || !c.key || !c.token) {
    lastError = 'configuration Supabase manquante';
    refresh();
    return { sent: 0, inserted: 0, error: lastError };
  }
  busy = true;
  clearTimeout(retryTimer);
  let sent = 0;
  let inserted = 0;
  try {
    for (;;) {
      const chunk = nextChunk(listKeys());
      if (!chunk.length) break;
      const body = `{"p_token":${JSON.stringify(c.token)},"p_items":[${chunk.map((x) => x.raw).join(',')}]}`;
      try {
        inserted += await post(body);
      } catch (e) {
        const refus = e.status >= 400 && e.status < 500 && !isAuthError(e);
        if (refus && chunk.length > 1) {   // paquet refusé (trop gros, une capture invalide…) : coupé en deux, réessayé tout de suite
          chunkLimit = Math.max(1, Math.floor(chunk.length / 2));
          continue;
        }
        lastError = e.message;
        fails++;
        if (refus) {   // une capture seule refusée : écartée au bout de 5 essais, et comptée
          const k = chunk[0].key;
          rejects[k] = (rejects[k] || 0) + 1;
          if (rejects[k] >= 5) { GM_deleteValue(k); GM_setValue('rejected', num('rejected') + 1); }
        }
        const wait = O.retryMs[Math.min(fails - 1, O.retryMs.length - 1)];
        retryTimer = setTimeout(() => flush('nouvel essai'), wait);
        return { sent, inserted, error: lastError };
      }
      for (const x of chunk) GM_deleteValue(x.key);
      sent += chunk.length;
      lastError = null;
      fails = 0;
      GM_setValue('lastSend', new Date().toISOString());
    }
    chunkLimit = O.chunkItems;   // file vidée : taille de paquet normale au prochain envoi
    return { sent, inserted, error: null };
  } finally {
    busy = false;
    refresh();
    if (again) { again = false; setTimeout(() => flush('suite'), 0); }
  }
}

async function exportNow() {
  autoSnapshot(true);   // la page affichée, à jour
  const r = await flush('manuel');
  const holes = JEU.pagedStatus ? JEU.pagedStatus().filter((s) => s.missing.length).length > 0 : false;
  if (r.error) toast(`Échec : ${r.error} (${listKeys().length} en attente, nouvel essai automatique)`, true);
  else {
    const st = JEU.pagedStatus ? JEU.pagedStatus() : [];
    toast(`Exporté : ${r.sent} captures (${r.inserted} nouvelles)` + (st.length ? ' — ' + st.map((s) => s.text).join(' ; ') : ''), holes);
  }
  return r;
}

// Fermeture ou masquage de l'onglet : dernière copie de la page, puis envoi (ce qui ne part pas reste en file).
function leaving() {
  try { autoSnapshot(false); } catch (_) { /* ignoré */ }
  flush('fermeture');
}
document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') leaving(); });
page.addEventListener('pagehide', leaving);

// ---------- Interface ----------
const hhmm = (iso) => (iso ? new Date(iso).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Paris' }) : 'jamais');

function refresh() {
  if (!ui) return;
  const n = listKeys().length;
  const dropped = num('dropped');
  const st = JEU.pagedStatus ? JEU.pagedStatus() : [];
  const holes = st.some((s) => s.missing.length);
  const label = JEU.label ? JEU.label() : JEU.short;
  ui.btn.textContent = `⇪ ${label} · ${n} en attente · dernier envoi ${hhmm(GM_getValue('lastSend', ''))}`
    + (dropped ? ` · ${dropped} perdue(s)` : '') + (holes ? ' ⚠' : '');
  ui.btn.style.background = lastError || holes ? '#b42318' : dropped ? '#b54708' : (autoOn() ? (JEU.color || '#2b8a3e') : '#8a6d2b');
  ui.btn.title = `${JEU.pageType(location.href, location.origin)} — ${n} capture(s) en attente`
    + (lastError ? `\nÉchec d'envoi : ${lastError}` : '') + (dropped ? `\n${dropped} capture(s) perdue(s) (file pleine)` : '')
    + (st.length ? '\n' + st.map((s) => s.text).join('\n') : '') + (autoOn() ? '' : '\n(copie automatique coupée)');
}

function toast(msg, err) {
  if (!ui) { console.log(`[${GAME} export]`, msg); return; }
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
  btn.addEventListener('click', () => exportNow());
  box.append(msg, btn);
  document.body.appendChild(box);
  ui = { box, msg, btn, t: 0 };
  refresh();
  watchDom();
}

migrateOldQueue();
if (document.body) mount();
else document.addEventListener('DOMContentLoaded', mount);
setTimeout(() => { if (listKeys().length) flush('reprise'); }, 3000);   // file laissée par un onglet fermé

if (typeof __TEST_EXPORT__ !== 'undefined') {   // crochet des tests (pipelines/test_userscripts.py) ; absent en navigateur
  Object.assign(__TEST_EXPORT__, { flush, enqueue, listKeys, queueStats, exportNow, autoSnapshot, record, refresh, mount, ui: () => ui, options: O });
}
})();
