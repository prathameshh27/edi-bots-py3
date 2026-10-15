// The Bots manual (same look as the Bots Studio knowledge base): builds the menu, the "on this page" list and the search box.
// Everything is plain JavaScript and data in this folder, so the pages also work when
// opened straight from disk (no web server, no internet).
(function () {
  // Light or dark: the same choice as in Bots Studio and its knowledge base (kept in the browser under the same name), else as the computer is set.
  var THEME_KEY = 'mantine-color-scheme-value';
  function storedTheme() { try { return localStorage.getItem(THEME_KEY); } catch (e) { return null; } }
  function isDark() {
    var t = storedTheme();
    if (t === 'dark' || t === 'light') return t === 'dark';
    return !!(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);
  }
  function applyTheme() {
    var t = storedTheme();
    if (t === 'dark' || t === 'light') document.documentElement.setAttribute('data-theme', t);
    else document.documentElement.removeAttribute('data-theme');
  }
  applyTheme();

  // The list of pages is written by docs/manual/build.py into assets/pages.js.
  var PAGES = window.MANUAL_PAGES || [];
  window.KB_PAGES = PAGES;

  var here = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
  if (here.indexOf('.html') < 0) here = 'index.html';
  var main = document.querySelector('main.kb-main');
  if (!main) return;

  function el(tag, attrs, html) {
    var e = document.createElement(tag);
    for (var k in attrs || {}) e.setAttribute(k, attrs[k]);
    if (html != null) e.innerHTML = html;
    return e;
  }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  // ---- top bar -------------------------------------------------------------
  var top = el('header', { class: 'kb-top' },
    '<button class="kb-menu-btn" type="button" aria-label="Menu">Menu</button>' +
    '<a class="kb-brand" href="index.html">Bots <span>4</span> · Manual</a>' +
    '<div class="kb-search"><input type="search" placeholder="Search: a word, a button name, an error message…" aria-label="Search the manual">' +
    '<div class="kb-results" role="listbox"></div></div>');
  document.body.insertBefore(top, document.body.firstChild);
  var themeBtn = el('button', { class: 'kb-theme', type: 'button' });
  function labelTheme() { themeBtn.textContent = isDark() ? 'Light mode' : 'Dark mode'; }
  themeBtn.addEventListener('click', function () {
    try { localStorage.setItem(THEME_KEY, isDark() ? 'light' : 'dark'); } catch (e) { /* storage blocked: stays as the computer is set */ }
    applyTheme(); labelTheme();
  });
  labelTheme();
  top.appendChild(themeBtn);

  // ---- menu ----------------------------------------------------------------
  var nav = el('nav', { class: 'kb-nav', 'aria-label': 'Pages' });
  var group = '';
  PAGES.forEach(function (p) {
    if (p.group !== group) { group = p.group; nav.appendChild(el('h4', {}, esc(group))); }
    nav.appendChild(el('a', { href: p.file, class: p.file === here ? 'current' : '' }, esc(p.title)));
  });
  top.querySelector('.kb-menu-btn').addEventListener('click', function () { nav.classList.toggle('open'); });

  // ---- "on this page" ------------------------------------------------------
  var toc = el('aside', { class: 'kb-toc', 'aria-label': 'On this page' });
  var heads = main.querySelectorAll('h2[id], h3[id]');
  if (heads.length) {
    toc.appendChild(el('h4', {}, 'On this page'));
    heads.forEach(function (h) {
      toc.appendChild(el('a', { href: '#' + h.id, class: h.tagName === 'H3' ? 'sub' : '' }, esc(h.textContent)));
    });
  }

  var shell = el('div', { class: 'kb-shell' });
  main.parentNode.insertBefore(shell, main);
  shell.appendChild(nav); shell.appendChild(main); shell.appendChild(toc);

  // ---- previous / next -----------------------------------------------------
  var at = PAGES.findIndex(function (p) { return p.file === here; });
  var prev = PAGES[at - 1], next = PAGES[at + 1];
  var updated = document.body.getAttribute('data-updated');
  main.appendChild(el('div', { class: 'kb-footer' },
    '<span>' + (prev ? '← <a href="' + prev.file + '">' + esc(prev.title) + '</a>' : '') + '</span>' +
    '<span>' + (updated ? 'Page last updated ' + esc(updated) : '') + '</span>' +
    '<span>' + (next ? '<a href="' + next.file + '">' + esc(next.title) + '</a> →' : '') + '</span>'));

  // ---- click a picture to see it full size ---------------------------------
  main.addEventListener('click', function (e) {
    if (e.target.tagName !== 'IMG' || !e.target.closest('figure')) return;
    var z = el('div', { class: 'kb-zoom' });
    z.appendChild(el('img', { src: e.target.src, alt: e.target.alt }));
    z.addEventListener('click', function () { z.remove(); });
    document.body.appendChild(z);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { var z = document.querySelector('.kb-zoom'); if (z) z.remove(); }
  });

  // ---- search --------------------------------------------------------------
  // KB_INDEX is written by docs/manual/build.py: one entry per section of every page.
  var input = top.querySelector('input'), box = top.querySelector('.kb-results');
  var index = window.KB_INDEX || [];
  var active = -1;

  function search(q) {
    var words = q.toLowerCase().split(/\s+/).filter(function (w) { return w.length > 1; });
    if (!words.length) return [];
    var out = [];
    index.forEach(function (s) {
      var title = (s.heading + ' ' + s.page).toLowerCase(), body = s.text.toLowerCase(), score = 0;
      for (var i = 0; i < words.length; i++) {
        var inTitle = title.indexOf(words[i]) >= 0, inBody = body.indexOf(words[i]) >= 0;
        if (!inTitle && !inBody) return;
        score += inTitle ? 10 : 0;
        score += inBody ? 1 + Math.min(body.split(words[i]).length - 1, 5) : 0;
      }
      out.push({ s: s, score: score });
    });
    out.sort(function (a, b) { return b.score - a.score; });
    return out.slice(0, 12).map(function (r) { return r.s; });
  }
  function snippet(text, words) {
    var low = text.toLowerCase(), pos = -1;
    for (var i = 0; i < words.length && pos < 0; i++) pos = low.indexOf(words[i]);
    var start = Math.max(0, pos - 50), piece = (start ? '…' : '') + text.slice(start, start + 150) + '…';
    piece = esc(piece);
    words.forEach(function (w) {
      piece = piece.replace(new RegExp('(' + w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig'), '<mark>$1</mark>');
    });
    return piece;
  }
  function show() {
    var q = input.value.trim();
    active = -1;
    if (q.length < 2) { box.classList.remove('open'); return; }
    var words = q.toLowerCase().split(/\s+/).filter(function (w) { return w.length > 1; });
    var hits = search(q);
    if (!index.length) box.innerHTML = '<div class="none">The search list is missing. Run docs/manual/build.py to create it.</div>';
    else if (!hits.length) box.innerHTML = '<div class="none">Nothing found for “' + esc(q) + '”. Try one word, or look in Troubleshooting.</div>';
    else box.innerHTML = hits.map(function (s) {
      return '<a href="' + s.file + (s.anchor ? '#' + s.anchor : '') + '"><div class="where">' + esc(s.page) + '</div><div><b>' +
        esc(s.heading) + '</b></div><div class="snippet">' + snippet(s.text, words) + '</div></a>';
    }).join('');
    box.classList.add('open');
  }
  input.addEventListener('input', show);
  input.addEventListener('focus', show);
  input.addEventListener('keydown', function (e) {
    var links = box.querySelectorAll('a');
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      active = Math.max(0, Math.min(links.length - 1, active + (e.key === 'ArrowDown' ? 1 : -1)));
      links.forEach(function (a, i) { a.classList.toggle('active', i === active); });
      if (links[active]) links[active].scrollIntoView({ block: 'nearest' });
    } else if (e.key === 'Enter' && links.length) {
      location.href = links[Math.max(active, 0)].href;
    } else if (e.key === 'Escape') {
      box.classList.remove('open'); input.blur();
    }
  });
  document.addEventListener('click', function (e) { if (!e.target.closest('.kb-search')) box.classList.remove('open'); });
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && document.activeElement !== input && !/INPUT|TEXTAREA/.test(document.activeElement.tagName)) {
      e.preventDefault(); input.focus();
    }
  });
})();
