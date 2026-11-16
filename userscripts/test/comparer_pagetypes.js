// Compare, sur l'échantillon tiré de bronze, le page_type produit AVANT (copie figée) et APRÈS (userscripts/jeux/<jeu>.js).
// Sortie : un JSON par jeu {jeu, total, identiques, differences:[{chemin, avant, apres}], hors_base:[{chemin, base, apres}]}.
'use strict';
const fs = require('fs');
const path = require('path');
const AVANT = require('./pagetype_avant');
const echantillon = require('./echantillon_pages.json');

const JEUX = ['basketvibe', 'sixzeroleague', 'teamsoccer', 'hockeynation', 'derbymanager', 'hardwood']
  .filter((j) => fs.existsSync(path.join(__dirname, '..', 'jeux', `${j}.js`)));
const ORIGINES = {
  basketvibe: 'https://www.basketvibe.com', sixzeroleague: 'https://sixzeroleague.com', teamsoccer: 'https://teamsoccer.org',
  hockeynation: 'https://hockey-nation.com', derbymanager: 'https://derbymanager.com', hardwood: 'https://onlinecollegebasketball.org',
};

function chargerJeu(jeu) {
  const src = fs.readFileSync(path.join(__dirname, '..', 'jeux', `${jeu}.js`), 'utf8');
  const corps = src.replace(/^\/\/ ==UserScript==[\s\S]*?\/\/ ==\/UserScript==\n/, '');
  const stub = { GM_getValue: () => null, GM_setValue() {}, document: { querySelector: () => null }, location: { pathname: '/' } };
  return new Function(...Object.keys(stub), corps + '\nreturn JEU;')(...Object.values(stub));
}

const sortie = [];
for (const jeu of JEUX) {
  const J = chargerJeu(jeu);
  const origine = ORIGINES[jeu];
  const lignes = echantillon[jeu];
  const differences = [];
  const horsBase = [];
  let identiques = 0;
  for (const [typeBase, chemin] of lignes) {
    const href = origine + chemin;
    const avant = AVANT[jeu](href, origine);
    const apres = J.pageType(href, origine);
    if (avant === apres) identiques++; else differences.push({ chemin, avant, apres });
    if (apres !== typeBase) horsBase.push({ chemin, base: typeBase, apres });
  }
  const nouveaux = (echantillon[`${jeu}_nouveau`] || []).map(([attendu, chemin]) => ({ chemin, attendu, apres: J.pageType(origine + chemin, origine), avant: AVANT[jeu](origine + chemin, origine) }));
  sortie.push({ jeu, total: lignes.length, identiques, differences, hors_base: horsBase, nouveaux });
}
console.log(JSON.stringify(sortie));
