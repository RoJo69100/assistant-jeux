// Mesure la taille de la file persistée : 20 copies de page de la taille donnée (argument JSON {jeu: octets}), par jeu,
// passées par la vraie fonction enqueue() du fichier généré (clés GM_setValue comprises).
'use strict';
const { creerEnv } = require('./harness');

const tailles = JSON.parse(process.argv[2]);
const sortie = [];
for (const [jeu, taille] of Object.entries(tailles)) {
  const e = creerEnv({ jeu, url: 'https://exemple.test/page', respond: () => ({ status: 500, text: 'panne' }) });
  e.core.options.autoCount = 1000;   // pas d'envoi : on mesure la file pleine
  for (let i = 0; i < 20; i++) {
    e.core.enqueue({ game: jeu, page_type: 'x', page_url: `https://exemple.test/p${i}`, source: 'dom', source_url: null,
      captured_at: new Date().toISOString(), payload: { text: 'a'.repeat(taille) }, client: 'test' });
  }
  const s = e.core.queueStats();
  sortie.push({ jeu, n: s.n, chars: s.chars, plafond: e.core.options.maxQueueChars });
}
console.log(JSON.stringify(sortie));
