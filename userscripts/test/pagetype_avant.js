// Copie figée des fonctions pageType() des six userscripts AVANT la brique « collecte » (commit b1bee8c).
// Sert de référence à pipelines/test_userscripts.py (comparaison avant/après). Ne pas modifier.
const AVANT = {
  basketvibe(href, origin) {
    const u = new URL(href, origin);
    const p = u.pathname.replace(/\/+$/, '') || '/';
    const tab = u.searchParams.get('tab');
    const withTab = (base) => (tab ? `${base}_${tab}` : base);
    if (p === '/club/roster') return withTab('roster');
    if (p === '/club/training') return withTab('training');
    if (p === '/club/tactics') return withTab('tactics');
    if (p === '/club/finance') return withTab('finance');
    if (p === '/club/personnel') return withTab('personnel');
    if (p === '/club/academy') return withTab('academy');
    if (p.startsWith('/transfers')) return withTab('transfers');
    if (/^\/match\/[^/]+$/.test(p)) return withTab('match');
    if (/^\/friendly\/[^/]+$/.test(p)) return withTab('friendly');
    if (p === '/club') return withTab('club');
    if (p === '/news') return 'news';
    if (p === '/notifications') return 'notifications';
    if (/^\/player\/[^/]+$/.test(p)) return withTab('player');
    if (p === '/league/table') return withTab('standings');
    if (p === '/league/schedule') return withTab('schedule');
    if (p.startsWith('/league')) return withTab('league');
    if (p === '/competition/cups') return withTab('cups');
    if (p === '/world') return withTab('world');
    return 'unknown';
  },
  generique(href, origin) {   // sixzeroleague, teamsoccer, hockeynation (code identique)
    const u = new URL(href, origin);
    const parts = u.pathname.split('/').filter(Boolean)
      .map((x) => (/^\d+$|^[0-9a-f-]{8,}$/i.test(x) ? 'id' : x.toLowerCase().replace(/\.(php|aspx?|html?)$/, '')));
    const base = parts.length ? parts.slice(0, 3).join('_') : 'home';
    const q = ['page', 'view', 'tab', 'subpage'].map((k) => u.searchParams.get(k)).filter(Boolean).join('_');
    return (q ? `${base}_${q}` : base).slice(0, 80);
  },
  derbymanager(href, origin) {
    const u = new URL(href, origin);
    const parts = u.pathname.split('/').filter(Boolean)
      .map((x) => (/^\d+$/.test(x) ? 'id' : x.toLowerCase().replace(/\.(php|aspx?|html?)$/, '')))
      .filter((x, i, a) => !(x === 'id' && a[i - 1] === 'id'));
    const base = parts.length ? parts.slice(0, 3).join('_') : 'home';
    const q = ['view', 'tab', 'page', 'type', 'mode'].map((k) => u.searchParams.get(k)).filter(Boolean).join('_');
    return (q ? `${base}_${q}` : base).slice(0, 80);
  },
  hardwood(href, origin) {
    const u = new URL(href, origin);
    const parts = u.pathname.split('/').filter(Boolean)
      .map((x) => (/^\d+$/.test(x) ? 'id' : x.toLowerCase().replace(/\.(php|aspx?|html?)$/, '')))
      .filter((x, i, a) => !(x === 'id' && a[i - 1] === 'id'));
    const base = parts.length ? parts.slice(0, 3).join('_') : 'home';
    const q = ['page', 'view', 'tab', 'type', 'mode'].map((k) => u.searchParams.get(k)).filter(Boolean).join('_');
    return (q ? `${base}_${q}` : base).slice(0, 80);
  },
};
AVANT.sixzeroleague = AVANT.generique;
AVANT.teamsoccer = AVANT.generique;
AVANT.hockeynation = AVANT.generique;
module.exports = AVANT;
