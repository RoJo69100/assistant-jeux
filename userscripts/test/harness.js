// Banc d'essai du noyau de collecte : exécute un userscript GÉNÉRÉ (userscripts/<jeu>.user.js) dans un navigateur factice
// (stockage GM partagé entre « rechargements », horloge factice, serveur factice). Utilisé par pipelines/test_userscripts.py.
'use strict';
const fs = require('fs');
const path = require('path');

const RACINE = path.resolve(__dirname, '..');

function fauxElement() {
  const el = {
    style: {}, children: [], textContent: '', title: '',
    append(...c) { el.children.push(...c); }, appendChild(c) { el.children.push(c); return c; },
    addEventListener() {}, contains() { return false; }, querySelectorAll() { return []; }, querySelector() { return null; },
    innerText: '', outerHTML: '<div></div>',
  };
  return el;
}

// opts : { jeu, store (Map partagée), url, respond(details) -> {status, text}, texteCapture, htmlCapture }
function creerEnv(opts) {
  const store = opts.store || new Map();
  const timers = [];
  let now = 0;
  let nextId = 1;
  const calls = [];
  const handlers = { document: {}, window: {} };
  const url = new URL(opts.url);
  const body = fauxElement();
  body.innerText = opts.texteCapture || 'x'.repeat(300);
  body.outerHTML = opts.htmlCapture || '<body>' + body.innerText + '</body>';
  const document = {
    body, title: 'Page', visibilityState: 'visible',
    createElement: () => fauxElement(),
    querySelector: (s) => (s === 'main' ? null : body),
    querySelectorAll: () => [],
    addEventListener: (t, f) => { (handlers.document[t] = handlers.document[t] || []).push(f); },
  };
  const location = { href: url.href, origin: url.origin, pathname: url.pathname };
  const fetchFaux = () => Promise.resolve({ headers: { get: () => 'application/json' }, clone() { return this; }, text: () => Promise.resolve('{}'), status: 200 });
  const unsafeWindow = {
    fetch: fetchFaux,
    XMLHttpRequest: { prototype: { open() {}, send() {} } },
    history: { pushState() {}, replaceState() {} },
    addEventListener: (t, f) => { (handlers.window[t] = handlers.window[t] || []).push(f); },
  };
  const windowFaux = { top: null, self: null };
  windowFaux.top = windowFaux; windowFaux.self = windowFaux;

  const sandbox = {
    unsafeWindow, window: windowFaux, document, location, URL, console, prompt: () => null, alert() {},
    MutationObserver: class { observe() {} },
    setTimeout: (fn, ms) => { const id = nextId++; timers.push({ id, at: now + (ms || 0), fn }); return id; },
    clearTimeout: (id) => { const i = timers.findIndex((t) => t.id === id); if (i >= 0) timers.splice(i, 1); },
    GM_getValue: (k, d) => (store.has(k) ? store.get(k) : d),
    GM_setValue: (k, v) => { store.set(k, v); },
    GM_deleteValue: (k) => { store.delete(k); },
    GM_listValues: () => [...store.keys()],
    GM_registerMenuCommand: () => {},
    GM_xmlhttpRequest: (d) => {
      calls.push(d);
      const r = (opts.respond || (() => ({ status: 200, text: '1' })))(d);
      Promise.resolve().then(() => {
        if (r.erreur) d.onerror(); else d.onload({ status: r.status, responseText: r.text });
      });
    },
    __TEST_EXPORT__: {},
  };
  if (!store.has('supabaseUrl') && opts.configurer !== false) {
    store.set('supabaseUrl', 'https://exemple.supabase.co');
    store.set('supabaseKey', 'sb_publishable_test');
    store.set('ingestToken', 'jeton-test');
  }
  const code = fs.readFileSync(path.join(RACINE, `${opts.jeu}.user.js`), 'utf8');
  const noms = Object.keys(sandbox);
  new Function(...noms, code)(...noms.map((n) => sandbox[n]));

  const settle = async () => { for (let i = 0; i < 8; i++) await new Promise((r) => setImmediate(r)); };
  return {
    core: sandbox.__TEST_EXPORT__, store, calls, document, body, handlers, settle,
    bouton: () => sandbox.__TEST_EXPORT__.ui().btn,
    async advance(ms) {
      const fin = now + ms;
      for (;;) {
        timers.sort((a, b) => a.at - b.at);
        const t = timers[0];
        if (!t || t.at > fin) break;
        timers.shift(); now = t.at; t.fn();
        await settle();
      }
      now = fin;
      await settle();
    },
    async fire(type) {
      for (const f of handlers.document[type] || []) f();
      for (const f of handlers.window[type] || []) f();
      await settle();
    },
    corps: (i = 0) => JSON.parse(calls[i].data),
  };
}

const reponse = (i, texte) => JSON.stringify({ n: i, texte });
module.exports = { creerEnv, reponse, RACINE };
