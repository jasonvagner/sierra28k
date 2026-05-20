'use strict';

// ── State ─────────────────────────────────────────────────────────────────────
const S = {
  data: null,
  filterActivities: new Set(),  // empty = all; else set of activity_type strings
  filterDiffs: new Set(),       // empty = all; else set of difficulty numbers
  filterSearch: '',
  starredOnly: false,
  inSeasonOnly: false,
  collapsedZones: new Set(),   // zone ids that are collapsed
  starredZones: new Set(),   // zone ids (number)
  starredTypes: new Set(),   // "{zoneId}-{actType}"
  starredActs:  new Set(),   // activity ids (number)
};

const ACT_LABEL = {
  walk: 'Walk', family_walk: 'Family Walk', run: 'Run',
  hike: 'Hike', bouldering: 'Bouldering', peak_bagging: 'Peak Bagging',
};
const DIFF_LABEL = ['','Very Easy','Easy','Moderate','Hard','Very Hard'];

// ── localStorage ──────────────────────────────────────────────────────────────
const LS       = 'sierra28k-stars-v1';
const LS_VIEW  = 'sierra28k-view-v1';
const LS_ABOUT = 'sierra28k-about-seen';

function saveView() {
  try {
    localStorage.setItem(LS_VIEW, JSON.stringify({
      c: [...S.collapsedZones],
    }));
  } catch (_) {}
}

function loadView() {
  try {
    const p = JSON.parse(localStorage.getItem(LS_VIEW) || '{}');
    S.collapsedZones = new Set((p.c || []).map(Number));
  } catch (_) {}
}

function saveStars() {
  try {
    localStorage.setItem(LS, JSON.stringify({
      z: [...S.starredZones],
      t: [...S.starredTypes],
      a: [...S.starredActs],
    }));
  } catch (_) {}
}

function loadStars() {
  try {
    const p = JSON.parse(localStorage.getItem(LS) || '{}');
    S.starredZones = new Set((p.z || []).map(Number));
    S.starredTypes = new Set(p.t || []);
    S.starredActs  = new Set((p.a || []).map(Number));
  } catch (_) {}
}

// ── URL hash ──────────────────────────────────────────────────────────────────
function encodeHash() {
  const parts = [
    ...[...S.starredZones].map(z => 'z' + z),
    ...[...S.starredTypes].map(t => 't' + t),
    ...[...S.starredActs ].map(a => 'a' + a),
  ];
  return parts.length ? '#stars=' + encodeURIComponent(parts.join(',')) : '';
}

function decodeHash(hash) {
  if (!hash || !hash.startsWith('#stars=')) return;
  try {
    decodeURIComponent(hash.slice(7)).split(',').filter(Boolean).forEach(p => {
      if (p[0] === 'z') S.starredZones.add(Number(p.slice(1)));
      else if (p[0] === 't') S.starredTypes.add(p.slice(1));
      else if (p[0] === 'a') S.starredActs.add(Number(p.slice(1)));
    });
  } catch (_) {}
}

// ── Helpers ───────────────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);
const el = (tag, cls) => { const e = document.createElement(tag); if (cls) e.className = cls; return e; };
const tmpl = id => document.getElementById(id).content.cloneNode(true).firstElementChild;

// ── Season check ──────────────────────────────────────────────────────────────
const MONTHS = ['January','February','March','April','May','June',
                'July','August','September','October','November','December'];

function inSeason(best_months) {
  if (!best_months) return false;
  const s = best_months.trim();
  if (s === 'Year-round') return true;
  const now = new Date().getMonth(); // 0-based
  // Single month: "July" or "August"
  const single = MONTHS.indexOf(s);
  if (single !== -1) return now === single;
  // Range: "June–October" or "October–April" (– is en-dash U+2013)
  const sep = s.includes('–') ? '–' : '-';
  const parts = s.split(sep);
  if (parts.length === 2) {
    const start = MONTHS.indexOf(parts[0].trim());
    const end   = MONTHS.indexOf(parts[1].trim());
    if (start === -1 || end === -1) return false;
    if (start <= end) return now >= start && now <= end;
    // Wraps around year-end (e.g. Oct–Apr)
    return now >= start || now <= end;
  }
  return false;
}

// ── Filter logic ──────────────────────────────────────────────────────────────
function activityVisible(act, zoneId) {
  if (S.filterActivities.size > 0 && !S.filterActivities.has(act.activity_type)) return false;
  if (S.filterDiffs.size > 0 && !S.filterDiffs.has(act.difficulty)) return false;
  if (S.inSeasonOnly && !inSeason(act.best_months)) return false;
  if (S.starredOnly) {
    const typeKey = `${zoneId}-${act.activity_type}`;
    if (!S.starredActs.has(act.id) && !S.starredTypes.has(typeKey) && !S.starredZones.has(Number(zoneId))) {
      return false;
    }
  }
  return true;
}

// ── Render ────────────────────────────────────────────────────────────────────
function renderAll() {
  const container = $('zones-container');
  container.innerHTML = '';
  $('empty-state').hidden = true;

  const q = S.filterSearch.toLowerCase();
  for (const zone of S.data.zones) {
    const places = q
      ? zone.places.filter(p => p.name.toLowerCase().includes(q))
      : zone.places;
    container.appendChild(renderZone(zone, places));
  }

  const hasZones = S.data.zones.length > 0;
  container.hidden = !hasZones;
  $('empty-state').hidden = hasZones;
}

function renderZone(zone, places) {
  let hasAny = false;
  const placeEls = [];
  for (const place of places) {
    const pEl = renderPlace(place, zone.id);
    if (pEl) { placeEls.push(pEl); hasAny = true; }
  }

  const section = tmpl('tmpl-zone');
  section.dataset.zoneId = zone.id;

  // Zone star
  const zStar = section.querySelector('.zone-star');
  zStar.dataset.zoneId = zone.id;
  zStar.classList.toggle('starred', S.starredZones.has(zone.id));
  zStar.addEventListener('click', e => { e.stopPropagation(); toggleZone(zone.id, section, zStar); });

  section.querySelector('.zone-name').textContent = zone.name;
  section.querySelector('.zone-meta').textContent = `${places.length} places`;

  // Collapse — restore state, then toggle on click
  if (S.collapsedZones.has(zone.id)) section.classList.add('collapsed');
  const header = section.querySelector('.zone-header');
  header.addEventListener('click', e => {
    if (e.target.closest('.star-btn')) return;
    const nowCollapsed = section.classList.toggle('collapsed');
    if (nowCollapsed) S.collapsedZones.add(zone.id);
    else S.collapsedZones.delete(zone.id);
    saveView();
  });

  const placeList = section.querySelector('.place-list');
  if (hasAny) {
    placeEls.forEach(p => placeList.appendChild(p));
  } else {
    const msg = document.createElement('p');
    msg.className = 'zone-no-match';
    msg.textContent = 'No activities match the current filters.';
    placeList.appendChild(msg);
  }

  return section;
}

function renderPlace(place, zoneId) {
  const acts = place.activities.filter(a => activityVisible(a, zoneId));
  if (!acts.length) return null;

  const card = tmpl('tmpl-place');
  card.querySelector('.place-name').textContent = place.name;

  // Kid-friendly
  if (place.kid_friendly) {
    const kb = el('span', 'kid-badge');
    kb.textContent = 'Kid-friendly';
    card.querySelector('.place-badges').prepend(kb);
  }

  const actList = card.querySelector('.activities-list');
  acts.forEach(a => actList.appendChild(renderActivity(a, place, zoneId)));

  return card;
}

function renderActivity(act, place, zoneId) {
  const row = tmpl('tmpl-activity');
  row.dataset.actId = act.id;

  const isStarred = S.starredActs.has(act.id);
  if (isStarred) row.classList.add('is-starred');

  // Star button
  const starBtn = row.querySelector('.activity-star');
  starBtn.classList.toggle('starred', isStarred);
  starBtn.addEventListener('click', e => {
    e.stopPropagation();
    const now = S.starredActs.has(act.id);
    if (now) S.starredActs.delete(act.id); else S.starredActs.add(act.id);
    starBtn.classList.toggle('starred', !now);
    row.classList.toggle('is-starred', !now);
    saveStars();
    refreshStarUI();
    updatePanel();
  });

  // Type label
  const typeEl = row.querySelector('.act-type');
  typeEl.textContent = ACT_LABEL[act.activity_type] || act.activity_type;
  typeEl.classList.add('t-' + act.activity_type);

  // Stats
  const parts = [];
  if (act.difficulty) parts.push(DIFF_LABEL[act.difficulty]);
  if (act.distance_km) parts.push(act.distance_km.toFixed(1) + ' km');
  if (act.elevation_gain_m) parts.push('+' + Math.round(act.elevation_gain_m) + ' m');
  row.querySelector('.act-stats').textContent = parts.join(' · ');

  // Season
  const seasonEl = row.querySelector('.act-season');
  if (act.best_months) seasonEl.textContent = act.best_months;
  else seasonEl.remove();

  // Event pill
  if (act.run_type === 'event') {
    const pill = el('span', 'event-pill');
    pill.textContent = 'Event';
    row.querySelector('.activity-line1').appendChild(pill);
  }

  // Notes
  const notesEl = row.querySelector('.activity-notes');
  if (act.notes) notesEl.textContent = act.notes;
  else notesEl.remove();

  // Conditions
  const condEl = row.querySelector('.activity-conditions');
  if (act.conditions_note) condEl.textContent = '↳ ' + act.conditions_note;
  else condEl.remove();

  // Links row: info · search · map
  const linksEl = row.querySelector('.activity-links');
  const linkDefs = [];
  if (place.canonical_url) {
    let domain = '';
    try { domain = new URL(place.canonical_url).hostname.replace(/^www\./, ''); } catch(e) {}
    linkDefs.push({ text: 'info ↗', href: place.canonical_url, title: domain });
  }
  linkDefs.push({ text: 'search ↗', href: act.search_url });
  if (place.lat && place.lng)
    linkDefs.push({ text: 'map ↗', href: `https://maps.google.com/?q=${place.lat},${place.lng}` });

  linkDefs.forEach((def, i) => {
    if (i > 0) {
      const sep = document.createElement('span');
      sep.className = 'activity-link-sep';
      sep.textContent = '·';
      linksEl.appendChild(sep);
    }
    const a = document.createElement('a');
    a.href = def.href;
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
    a.className = 'activity-link';
    a.textContent = def.text;
    if (def.title) a.title = def.title;
    linksEl.appendChild(a);
  });

  return row;
}

// ── Star toggle helpers ────────────────────────────────────────────────────────
function toggleZone(zoneId, section, btn) {
  const id = Number(zoneId);
  if (S.starredZones.has(id)) S.starredZones.delete(id);
  else S.starredZones.add(id);
  btn.classList.toggle('starred', S.starredZones.has(id));
  saveStars(); refreshStarUI(); updatePanel();
}

function refreshStarUI() {
  const total = S.starredZones.size + S.starredTypes.size + S.starredActs.size;
  $('star-count').textContent = total;
  $('star-count').hidden = total === 0;
  $('btn-share').hidden = total === 0;
}

// ── Panel ─────────────────────────────────────────────────────────────────────
function buildStarredGroups() {
  if (!S.data) return [];
  const zoneMap = Object.fromEntries(S.data.zones.map(z => [z.id, z]));
  const actMap = {};
  for (const zone of S.data.zones)
    for (const place of zone.places)
      for (const act of place.activities)
        actMap[act.id] = { act, place, zone };

  const grouped = {};
  const add = (zid, item) => {
    if (!grouped[zid]) grouped[zid] = { zone: zoneMap[zid], items: [] };
    grouped[zid].items.push(item);
  };

  S.starredZones.forEach(zid => {
    if (zoneMap[zid]) add(zid, { label: zoneMap[zid].name, sub: 'Entire region', type: 'zone', key: zid });
  });
  S.starredTypes.forEach(key => {
    const [zidStr, type] = key.split('-');
    const zone = zoneMap[Number(zidStr)];
    if (zone) add(Number(zidStr), { label: ACT_LABEL[type] || type, sub: zone.name, type: 'type', key });
  });
  S.starredActs.forEach(aid => {
    const entry = actMap[aid];
    if (!entry) return;
    const { act, place, zone } = entry;
    const sub = [ACT_LABEL[act.activity_type], act.best_months, act.distance_km ? act.distance_km.toFixed(1) + ' km' : null]
      .filter(Boolean).join(' · ');
    add(zone.id, { label: place.name, sub, type: 'activity', key: aid, entry });
  });

  return Object.values(grouped).sort((a, b) => a.zone.id - b.zone.id);
}

function updatePanel() {
  const body = $('panel-list-body');
  const footer = $('panel-footer');
  const groups = buildStarredGroups();
  const total = S.starredZones.size + S.starredTypes.size + S.starredActs.size;

  if (total === 0) {
    body.innerHTML = '<p class="panel-empty">Star a region, activity type, or individual activity to build your list.</p>';
    footer.hidden = true;
    return;
  }
  footer.hidden = false;
  body.innerHTML = '';

  for (const group of groups) {
    const groupEl = el('div', 'panel-zone-group');
    const label = el('div', 'panel-zone-label');
    label.textContent = group.zone.name;
    groupEl.appendChild(label);

    for (const item of group.items) {
      const row = el('div', 'panel-item');
      const star = el('span', 'panel-star'); star.textContent = '★';
      const itemBody = el('div', 'panel-item-body');
      const name = el('div', 'panel-item-name'); name.textContent = item.label;
      const sub  = el('div', 'panel-item-sub');  sub.textContent  = item.sub;
      itemBody.append(name, sub);
      const rmBtn = el('button', 'panel-item-remove');
      rmBtn.textContent = '✕';
      rmBtn.addEventListener('click', () => {
        if (item.type === 'zone') S.starredZones.delete(Number(item.key));
        else if (item.type === 'type') S.starredTypes.delete(item.key);
        else S.starredActs.delete(Number(item.key));
        saveStars(); refreshStarUI(); updatePanel();
        // Also update the inline star button if still visible
        if (item.type === 'activity') {
          const rowEl = document.querySelector(`.activity-row[data-act-id="${item.key}"]`);
          if (rowEl) {
            rowEl.querySelector('.activity-star').classList.remove('starred');
            rowEl.classList.remove('is-starred');
          }
        }
      });
      row.append(star, itemBody, rmBtn);
      groupEl.appendChild(row);
    }
    body.appendChild(groupEl);
  }
}

// ── Share ─────────────────────────────────────────────────────────────────────
function shareLink() {
  return location.origin + location.pathname + encodeHash();
}
function shareText() {
  const g = buildStarredGroups();
  const lines = ['My Sierra 28K List', ''];
  g.forEach(group => {
    lines.push('=== ' + group.zone.name + ' ===');
    group.items.forEach(i => {
      lines.push('★ ' + i.label);
      if (i.sub) lines.push('  ' + i.sub);
      if (i.type === 'activity' && i.entry?.place?.canonical_url)
        lines.push('  ' + i.entry.place.canonical_url);
    });
    lines.push('');
  });
  lines.push('—\n' + shareLink());
  return lines.join('\n').trim();
}
function shareMd() {
  const g = buildStarredGroups();
  const lines = ['# My Sierra 28K List', ''];
  g.forEach(group => {
    lines.push('## ' + group.zone.name);
    group.items.forEach(i => {
      let line = '- **' + i.label + '**' + (i.sub ? ' — ' + i.sub : '');
      if (i.type === 'activity' && i.entry?.place?.canonical_url)
        line += ' · [info](' + i.entry.place.canonical_url + ')';
      lines.push(line);
    });
    lines.push('');
  });
  lines.push('---\n[View on Sierra 28K](' + shareLink() + ')');
  return lines.join('\n').trim();
}
function shareCsv() {
  const q = v => '"' + String(v ?? '').replace(/"/g, '""') + '"';
  const rows = [['Zone','Name','Type','Activity','Best Months','Difficulty','Distance (km)','Elevation (m)','Conditions','URL']];
  for (const group of buildStarredGroups()) {
    for (const item of group.items) {
      if (item.type === 'zone') {
        rows.push([q(group.zone.name), q(item.label), q('Region'), '', '', '', '', '', '', '']);
      } else if (item.type === 'type') {
        rows.push([q(group.zone.name), '', q('Activity Type'), q(item.label), '', '', '', '', '', '']);
      } else if (item.entry) {
        const { act, place } = item.entry;
        rows.push([
          q(group.zone.name), q(place.name), q('Activity'),
          q(ACT_LABEL[act.activity_type]), q(act.best_months),
          q(DIFF_LABEL[act.difficulty] || ''),
          q(act.distance_km != null ? act.distance_km.toFixed(1) : ''),
          q(act.elevation_gain_m != null ? Math.round(act.elevation_gain_m) : ''),
          q(act.conditions_note),
          q(place.canonical_url || ''),
        ]);
      }
    }
  }
  return rows.map(r => r.join(',')).join('\r\n');
}

async function copyText(text, label) {
  try {
    await navigator.clipboard.writeText(text);
    showFeedback('✓ ' + label + ' copied');
  } catch (_) { showFeedback('Copy failed — please copy manually'); }
}
function showFeedback(msg) {
  const fb = $('share-feedback');
  fb.textContent = msg;
  fb.hidden = false;
  clearTimeout(fb._t);
  fb._t = setTimeout(() => { fb.hidden = true; }, 2500);
}

// ── About modal ───────────────────────────────────────────────────────────────
function openAbout() {
  $('modal-about').hidden = false;
  document.body.style.overflow = 'hidden';
}
function closeAbout() {
  $('modal-about').hidden = true;
  document.body.style.overflow = '';
  try { localStorage.setItem(LS_ABOUT, '1'); } catch (_) {}
}

// ── Panel open/close ──────────────────────────────────────────────────────────
function openPanel() {
  updatePanel();
  const panel = $('panel-my-list');
  const overlay = $('panel-overlay');
  panel.hidden = false; overlay.hidden = false;
  requestAnimationFrame(() => panel.classList.add('open'));
  panel.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
  history.replaceState(null, '', encodeHash() || location.pathname);
}
function closePanel() {
  const panel = $('panel-my-list');
  panel.classList.remove('open');
  panel.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
  setTimeout(() => { panel.hidden = true; $('panel-overlay').hidden = true; }, 250);
}


// ── Boot ──────────────────────────────────────────────────────────────────────
async function init() {
  loadStars();
  loadView();
  decodeHash(location.hash);
  saveStars();

  let data;
  try {
    data = await (await fetch('./data.json')).json();
  } catch (e) {
    $('loading').innerHTML = '<p style="color:#c0392b;padding:40px 0;text-align:center">Failed to load. Please refresh.</p>';
    return;
  }

  S.data = data;
  $('loading').hidden = true;
  refreshStarUI();
  renderAll();

  // Multi-select activity chips (toggle each independently)
  document.querySelector('.filter-bar').addEventListener('click', e => {
    const chip = e.target.closest('[data-activity]');
    if (chip) {
      const type = chip.dataset.activity;
      if (S.filterActivities.has(type)) S.filterActivities.delete(type);
      else S.filterActivities.add(type);
      chip.classList.toggle('active', S.filterActivities.has(type));
      renderAll();
      return;
    }
    // Multi-select difficulty chips
    const diff = e.target.closest('[data-diff]');
    if (diff) {
      const d = Number(diff.dataset.diff);
      if (S.filterDiffs.has(d)) S.filterDiffs.delete(d);
      else S.filterDiffs.add(d);
      diff.classList.toggle('active', S.filterDiffs.has(d));
      renderAll();
      return;
    }
  });

  // Search
  let searchTimer;
  $('search-input').addEventListener('input', e => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => { S.filterSearch = e.target.value.trim(); renderAll(); }, 180);
  });

  // In season
  $('btn-in-season').addEventListener('click', () => {
    S.inSeasonOnly = !S.inSeasonOnly;
    $('btn-in-season').setAttribute('aria-pressed', S.inSeasonOnly);
    renderAll();
  });

  // Starred only
  $('btn-starred-only').addEventListener('click', () => {
    S.starredOnly = !S.starredOnly;
    $('btn-starred-only').setAttribute('aria-pressed', S.starredOnly);
    renderAll();
  });

  // Expand / Collapse all
  $('btn-expand-all').addEventListener('click', () => {
    S.collapsedZones.clear();
    document.querySelectorAll('.zone-section').forEach(s => s.classList.remove('collapsed'));
    saveView();
  });
  $('btn-collapse-all').addEventListener('click', () => {
    S.data.zones.forEach(z => S.collapsedZones.add(z.id));
    document.querySelectorAll('.zone-section').forEach(s => s.classList.add('collapsed'));
    saveView();
  });

  // Panel
  $('btn-my-list').addEventListener('click', openPanel);
  $('btn-share').addEventListener('click', openPanel);
  $('btn-close-panel').addEventListener('click', closePanel);
  $('panel-overlay').addEventListener('click', closePanel);
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closePanel(); });

  // Share buttons
  $('share-link').addEventListener('click', () => copyText(shareLink(), 'Link'));
  $('share-text').addEventListener('click', () => copyText(shareText(), 'Text'));
  $('share-md').addEventListener('click',   () => copyText(shareMd(),   'Markdown'));
  $('share-csv').addEventListener('click',  () => copyText(shareCsv(),  'CSV'));
  $('btn-clear-stars').addEventListener('click', () => {
    S.starredZones.clear(); S.starredTypes.clear(); S.starredActs.clear();
    saveStars(); refreshStarUI(); updatePanel(); renderAll();
  });

  // About modal
  $('btn-about').addEventListener('click', openAbout);
  $('btn-close-about').addEventListener('click', closeAbout);
  $('btn-got-it').addEventListener('click', closeAbout);
  $('modal-about').addEventListener('click', e => { if (e.target === $('modal-about')) closeAbout(); });

  // Show about on first visit (no prior stars/view = genuinely first time)
  try {
    if (!localStorage.getItem(LS_ABOUT)) openAbout();
  } catch (_) {}

  // Hash change (visiting a shared link)
  window.addEventListener('hashchange', () => {
    S.starredZones.clear(); S.starredTypes.clear(); S.starredActs.clear();
    decodeHash(location.hash);
    saveStars(); refreshStarUI(); updatePanel(); renderAll();
  });
}

document.addEventListener('DOMContentLoaded', init);
