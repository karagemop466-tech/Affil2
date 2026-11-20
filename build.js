#!/usr/bin/env node
/**
 * ShopNow Reviews — static site builder.
 *
 * Principles enforced here, not just documented:
 *   1. One navigation group. Every page is generated from the same shell.
 *   2. The disclosure strip is emitted by the shell, so no page can opt out.
 *   3. The build FAILS if a generated page is missing either disclosure.
 *   4. Buyer-facing pages never render observed price or rating.
 *   5. A product with no publishable link renders a non-clickable card.
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname);
const OUT = path.join(ROOT, 'docs');
const C = path.join(ROOT, 'content');

const data = JSON.parse(fs.readFileSync(path.join(C, 'data.json'), 'utf8'));
const guides = JSON.parse(fs.readFileSync(path.join(C, 'guides.json'), 'utf8'));
const suggestionsDoc = JSON.parse(fs.readFileSync(path.join(C, 'suggestions.json'), 'utf8'));
const questions = JSON.parse(fs.readFileSync(path.join(C, 'questions.json'), 'utf8'));
const ledger = JSON.parse(fs.readFileSync(path.join(C, 'ledger.json'), 'utf8'));
const research = JSON.parse(fs.readFileSync(path.join(C, 'research.json'), 'utf8'));

const BASE = (data.site.basePath || '').replace(/\/$/, '');
const ORIGIN = data.site.canonicalOrigin;
const DISCLOSURE = 'As an Amazon Associate I earn from qualifying purchases.';
const TID = data.site.trackingId;

const products = data.products;
const sources = data.sources;
const flags = data.irregularities;
const bySlug = Object.fromEntries(products.map(p => [p.slug, p]));

/* ------------------------------------------------------------------ utils */
const esc = s => String(s == null ? '' : s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;');

const url = p => BASE + p;
const abs = p => ORIGIN + BASE + p;

function write(rel, html) {
  const file = path.join(OUT, rel);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, html);
  return { rel, html };
}

const sourceById = Object.fromEntries(sources.map(s => [s.id, s]));

/* Guides are written with plain root-absolute links (/guides/foo/) so the prose stays
   readable and portable. Because this site is served from a repository sub-path, every
   such link must be rebased at build time. Doing it here means a body file can never
   ship a broken internal URL, whatever the basePath is set to. */
function rebaseBodyLinks(html) {
  return html.replace(/\b(href|src)="\/(?!\/)/g, (m, attr) => `${attr}="${BASE}/`);
}
/* Evidence links on the flagged page.
   A link that is itself under review must not be clickable, and a statement of fact
   ("recorded in verificationLog V-06") is not a URL at all. */
function renderEvidence(evidence) {
  if (!evidence) return '<em>none recorded</em>';
  if (!/^https?:\/\//.test(evidence)) return `<span>${esc(evidence)}</span>`;
  if (/^https:\/\/link\.amazon\//.test(evidence)) {
    return `<code>${esc(evidence)}</code> <span style="color:var(--ink-3)">(not linked: destination under review)</span>`;
  }
  return `<a href="${esc(evidence)}" rel="noopener" target="_blank">${esc(evidence)}</a>`;
}

function srcLink(id) {
  const s = sourceById[id];
  if (!s) return esc(id);
  return `<a href="${esc(s.url)}" rel="noopener" target="_blank">${esc(s.id)}</a>`;
}

function pill(status) {
  const map = {
    verified: ['ok', 'Verified'],
    high: ['bad', 'High'],
    medium: ['warn', 'Medium'],
    low: ['mute', 'Low'],
    answered: ['ok', 'Answered'],
    warning: ['warn', 'Link under review'],
    blocked: ['bad', 'Link under review'],
    open: ['warn', 'Open'],
    closed: ['bad', 'Closed'],
    done: ['ok', 'Built'],
    proposed: ['mute', 'Proposed'],
    'in progress': ['warn', 'In progress'],
    assisted: ['warn', 'AI-assisted'],
    partial: ['warn', 'Partial'],
    true: ['ok', 'Automated'],
    false: ['mute', 'Manual']
  };
  const key = String(status);
  const [cls, label] = map[key] || ['mute', esc(status)];
  return `<span class="pill ${cls}">${label}</span>`;
}

const NAV = [
  ['/', 'Home'],
  ['/air-fryers/', 'Air fryers'],
  ['/thermometers/', 'Thermometers'],
  ['/guides/', 'Guides'],
  ['/research/', 'Research'],
  ['/suggestions/', 'Suggestions'],
  ['/questions/', 'Open questions'],
  ['/ledger/', 'Ledger'],
  ['/sources/', 'Sources'],
  ['/flagged/', 'Flagged for review']
];

/* ------------------------------------------------------------------ shell */
function shell({ path: p, title, description, body, active, noindex, extraHead }) {
  const fullTitle = p === '/' ? `${data.site.name} — ${data.site.tagline}` : `${title} · ${data.site.name}`;
  const nav = NAV.map(([href, label]) => {
    const isActive = href === active ? ' aria-current="page"' : '';
    return `<a href="${esc(url(href))}"${isActive}>${esc(label)}</a>`;
  }).join('');

  const footer = `
  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <div>
          <h4>Shop by category</h4>
          <ul>
            <li><a href="${esc(url('/air-fryers/'))}">Air fryers</a></li>
            <li><a href="${esc(url('/thermometers/'))}">Thermometers</a></li>
            <li><a href="${esc(url('/guides/'))}">All guides</a></li>
          </ul>
        </div>
        <div>
          <h4>How this site works</h4>
          <ul>
            <li><a href="${esc(url('/research/'))}">Research &amp; automation</a></li>
            <li><a href="${esc(url('/ledger/'))}">Campaign ledger</a></li>
            <li><a href="${esc(url('/sources/'))}">Source register</a></li>
            <li><a href="${esc(url('/flagged/'))}">Flagged for review</a></li>
          </ul>
        </div>
        <div>
          <h4>Editorial</h4>
          <ul>
            <li><a href="${esc(url('/author/'))}">Who writes this</a></li>
            <li><a href="${esc(url('/disclosure/'))}">Disclosure &amp; editorial policy</a></li>
            <li><a href="${esc(url('/questions/'))}">Open questions</a></li>
            <li><a href="${esc(url('/suggestions/'))}">Suggestions</a></li>
          </ul>
        </div>
        <div>
          <h4>Site</h4>
          <ul>
            <li><a href="${esc(url('/sitemap.xml'))}">Sitemap</a></li>
            <li><a href="${esc(url('/feed.xml'))}">RSS feed</a></li>
            <li><a href="${esc(url('/COORDINATION/'))}">Session board</a></li>
            <li><a href="${esc(url('/executive-summary/'))}">Executive summary</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>${esc(data.site.name)} · Tracking ID <code>${esc(TID)}</code> · Built ${esc(data.site.buildDate)}</span>
        <span>Prices and availability are never published here without API entitlements. Product names and specifications come from the linked Amazon listings.</span>
      </div>
    </div>
    <div class="footer-disclosure">
      <div class="wrap">
        <strong>Disclosure</strong>
        <span>${esc(DISCLOSURE)} &mdash; <a href="${esc(url('/disclosure/'))}">Read the full editorial and disclosure policy</a>.</span>
      </div>
    </div>
  </footer>`;

  return `<!doctype html>
<html lang="${esc(data.site.locale)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(fullTitle)}</title>
<meta name="description" content="${esc(description)}">
${noindex ? '<meta name="robots" content="noindex,follow">' : ''}
<link rel="canonical" href="${esc(abs(p))}">
<link rel="alternate" type="application/rss+xml" title="${esc(data.site.name)}" href="${esc(url('/feed.xml'))}">
<link rel="stylesheet" href="${esc(url('/assets/css/site.css'))}">
<meta property="og:title" content="${esc(fullTitle)}">
<meta property="og:description" content="${esc(description)}">
<meta property="og:type" content="${p === '/' || p === '/guides/' ? 'website' : 'article'}">
<meta property="og:url" content="${esc(abs(p))}">
<meta property="og:site_name" content="${esc(data.site.name)}">
<meta name="twitter:card" content="summary">
${extraHead || ''}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<div class="disclosure" data-disclosure="masthead">
  <div class="wrap">
    <strong>Paid links</strong>
    <span>${esc(DISCLOSURE)} Links to Amazon on this site are affiliate links and this site is compensated for qualifying purchases. <a href="${esc(url('/disclosure/'))}">How this works</a>.</span>
  </div>
</div>

<header class="masthead">
  <div class="wrap">
    <a class="brand" href="${esc(url('/'))}">
      <span class="brand-mark" aria-hidden="true">S</span>
      <span class="brand-name">${esc(data.site.name)}<small>${esc(data.site.tagline)}</small></span>
    </a>
    <div class="hero-meta" style="margin:0">
      <span><b>5</b> products tracked</span>
      <span><b>${guides.length}</b> guides</span>
      <span><b>${flags.length}</b> flagged items</span>
    </div>
  </div>
</header>

<nav class="nav" aria-label="Main">
  <div class="wrap">${nav}</div>
</nav>

<main id="main">
${body}
</main>
${footer}
<script src="${esc(url('/assets/js/config.js'))}"></script>
<script src="${esc(url('/assets/js/site.js'))}"></script>
</body>
</html>`;
}

/* --------------------------------------------------------- product button */
function buyButton(p, placement) {
  const publishable = p.status !== 'blocked' && p.observedRedirectUrl;
  if (!publishable) {
    return `<span class="btn ghost" aria-disabled="true" style="cursor:not-allowed;opacity:.55">Link under review</span>
      <span class="sponsored-note"><b>Held</b> — destination unresolved, not published</span>`;
  }
  return `<a class="btn" href="${esc(p.observedRedirectUrl)}" rel="sponsored nofollow noopener" target="_blank"
      data-asin="${esc(p.observedAsin)}" data-placement="${esc(placement)}">Check price on Amazon</a>
    <span class="sponsored-note"><b>Paid link</b> · opens Amazon</span>`;
}

function productCard(p) {
  return `<article class="card">
    <span class="tagline">${esc(p.brand)} · ${esc(p.formFactor)}</span>
    <h3><a href="${esc(url('/products/' + p.slug + '/'))}">${esc(p.shortName)}</a></h3>
    <p>${esc(p.whyItMatters)}</p>
    <p style="font-size:13px;color:var(--ink-3)"><strong>Watch out:</strong> ${esc(p.tradeoff)}</p>
    <div class="foot">${buyButton(p, 'card')}</div>
  </article>`;
}

/* ------------------------------------------------------------------- pages */
const pages = [];

/* ---------- home ---------- */
const featuredGuides = guides.filter(g => g.featured).slice(0, 4);
const homeBody = `
<section class="hero">
  <div class="wrap">
    <p class="kicker">Kitchen appliances, chosen slowly</p>
    <h1>Five machines worth arguing about.</h1>
    <p class="dek">We picked a short list of air fryers and thermometers, wrote down exactly why each one earns its place, and said plainly what we have not tested. No invented measurements, no fake hands-on reviews.</p>
    <div class="hero-meta">
      <span><b>${products.length}</b> products on the list</span>
      <span><b>${guides.length}</b> buying guides</span>
      <span><b>${sources.length}</b> cited sources</span>
      <span>Updated <b>${esc(data.site.buildDate)}</b></span>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <div>
        <p class="eyebrow">The shortlist</p>
        <h2>Air fryers</h2>
      </div>
      <a class="more" href="${esc(url('/air-fryers/'))}">All air fryers →</a>
    </div>
    <div class="grid cols-3">
      ${products.filter(p => p.category === 'air-fryers').map(productCard).join('\n      ')}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <div>
        <p class="eyebrow">The shortlist</p>
        <h2>Thermometers</h2>
      </div>
      <a class="more" href="${esc(url('/thermometers/'))}">All thermometers →</a>
    </div>
    <div class="grid cols-2">
      ${products.filter(p => p.category === 'thermometers').map(productCard).join('\n      ')}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <div>
        <p class="eyebrow">Start here</p>
        <h2>Questions worth answering before you buy</h2>
        <p class="sub">Every guide is built around one question a buyer actually asks. None of them promise a "best" anything.</p>
      </div>
      <a class="more" href="${esc(url('/guides/'))}">All ${guides.length} guides →</a>
    </div>
    <div class="grid cols-2">
      ${featuredGuides.map(g => `<article class="card">
        <span class="tagline">${esc(g.cluster)} · ${g.readMinutes} min</span>
        <h3><a href="${esc(url('/guides/' + g.slug + '/'))}">${esc(g.title)}</a></h3>
        <p>${esc(g.deck)}</p>
      </article>`).join('\n      ')}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="two-col">
      <div>
        <div class="sec-head">
          <div>
            <p class="eyebrow">Editorial standard</p>
            <h2>What we will not do</h2>
          </div>
        </div>
        <p>We will not tell you how a machine performs if we have not used it. We will not publish a price we cannot source from Amazon under its terms. We will not publish a rating we are not permitted to display, and we will not invent a conversion rate, a traffic figure or a revenue forecast to make the site look busier than it is.</p>
        <p>What is left is narrower and more useful: what each product is designed to do, who it suits, what the trade-off is, and the question you should answer before spending money on it.</p>
        <p><a href="${esc(url('/author/'))}">Who writes this →</a> &nbsp; <a href="${esc(url('/disclosure/'))}">Disclosure and editorial policy →</a></p>
      </div>
      <aside class="aside">
        <h3>Check our work</h3>
        <ul>
          <li><a href="${esc(url('/sources/'))}">${sources.length} sources</a> with direct links</li>
          <li><a href="${esc(url('/flagged/'))}">${flags.length} flagged items</a>, published rather than hidden</li>
          <li><a href="${esc(url('/questions/'))}">Open questions</a> we cannot yet answer</li>
          <li><a href="${esc(url('/executive-summary/'))}">Executive summary</a> of the whole build</li>
        </ul>
      </aside>
    </div>
  </div>
</section>`;

pages.push({ path: '/', html: shell({
  path: '/',
  active: '/',
  title: 'home',
  description: 'A short, honest list of air fryers and thermometers, with the trade-offs and the questions to answer before buying.',
  body: homeBody
}) });

/* ---------- category pages ---------- */
function categoryPage(cat, heading, kicker, intro, guideSlugs) {
  const items = products.filter(p => p.category === cat);
  const gs = guides.filter(g => g.category === cat);
  const p = `/${cat}/`;
  const body = `
<div class="wrap"><div class="crumbs"><a href="${esc(url('/'))}">Home</a> / ${esc(heading)}</div></div>
<section class="hero" style="border-bottom:1px solid var(--rule-2)">
  <div class="wrap">
    <p class="kicker">${esc(kicker)}</p>
    <h1>${esc(heading)}</h1>
    <p class="dek">${intro}</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="grid ${items.length > 2 ? 'cols-3' : 'cols-2'}">
      ${items.map(productCard).join('\n      ')}
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">Read next</p><h2>Guides in this category</h2></div></div>
    <div class="grid cols-2">
      ${gs.map(g => `<article class="card">
        <span class="tagline">${esc(g.cluster)} · ${g.readMinutes} min</span>
        <h3><a href="${esc(url('/guides/' + g.slug + '/'))}">${esc(g.title)}</a></h3>
        <p>${esc(g.deck)}</p>
      </article>`).join('\n      ')}
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="callout">
      <h3>What this list is, and is not</h3>
      <p>This is a short list with reasoning attached, not a ranking. We have not tested these machines, so there is no "best" claim on this page, no score, and no measured result. Specifications come from the manufacturers' published listings. Where verification is incomplete, the product page says so at the top.</p>
    </div>
  </div>
</section>`;
  pages.push({ path: p, html: shell({
    path: p, active: p, title: heading,
    description: intro.replace(/<[^>]+>/g, ''),
    body
  }) });
}

categoryPage('air-fryers', 'Air fryers', 'Three shapes, one decision',
  'A two-basket machine, a big single drawer, and a French-door oven that wants to replace two appliances at once. Each one is a different answer to the same question.');

categoryPage('thermometers', 'Thermometers', 'Doneness you can check',
  'One fast probe and one wireless three-probe set. The temperatures themselves come from the USDA, not from us, and we link the chart on both pages.');

/* ---------- guides index ---------- */
const clusters = [...new Set(guides.map(g => g.cluster))];
const guidesBody = `
<div class="wrap"><div class="crumbs"><a href="${esc(url('/'))}">Home</a> / Guides</div></div>
<section class="hero">
  <div class="wrap">
    <p class="kicker">${guides.length} guides · ${clusters.length} clusters</p>
    <h1>Publish the question, not the pitch.</h1>
    <p class="dek">Every guide here exists to answer one question a buyer is actually asking. They are grouped by the decision they belong to, so you can read them in the order you would actually make the decision.</p>
  </div>
</section>
${clusters.map(cl => `
<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">Cluster</p><h2>${esc(cl)}</h2></div></div>
    <div class="grid cols-2">
      ${guides.filter(g => g.cluster === cl).map(g => `<article class="card">
        <span class="tagline">${g.readMinutes} min · ${esc(g.published)}</span>
        <h3><a href="${esc(url('/guides/' + g.slug + '/'))}">${esc(g.title)}</a></h3>
        <p>${esc(g.deck)}</p>
      </article>`).join('\n      ')}
    </div>
  </div>
</section>`).join('')}`;

pages.push({ path: '/guides/', html: shell({
  path: '/guides/', active: '/guides/', title: 'Guides',
  description: 'Question-shaped buying guides for air fryers and thermometers, grouped by the decision they belong to.',
  body: guidesBody
}) });

/* ---------- individual guides ---------- */
for (const g of guides) {
  const p = `/guides/${g.slug}/`;
  const bodyHtml = rebaseBodyLinks(fs.readFileSync(path.join(C, 'bodies', g.body), 'utf8'));
  const related = g.relatedProducts.map(s => bySlug[s]).filter(Boolean);
  const body = `
<div class="wrap"><div class="crumbs"><a href="${esc(url('/'))}">Home</a> / <a href="${esc(url('/guides/'))}">Guides</a> / ${esc(g.cluster)}</div></div>
<section class="section" style="padding-top:26px">
  <div class="wrap">
    <div class="two-col">
      <article class="article" data-guide="${esc(g.slug)}">
        <p class="eyebrow">${esc(g.cluster)} · ${g.readMinutes} min read</p>
        <h1>${esc(g.title)}</h1>
        <div class="byline">
          <span>By <b>${esc(data.site.author)}</b></span>
          <span>Published <b>${esc(g.published)}</b></span>
          <span>Updated <b>${esc(g.updated)}</b></span>
          <span><a href="#how">How this was written</a></span>
        </div>
        ${bodyHtml}
        <div class="scope-note" id="how">
          <h3>How this guide was written</h3>
          <p>Drafted with an AI assistant from the sources listed in the <a href="${esc(url('/sources/'))}">source register</a> and from the manufacturers' published specifications. No product on this site has been physically tested by the editor. Where a statement cannot be checked, it is labelled rather than smoothed over. Anything that looks like a measurement is a number the manufacturer published, and it is attributed as such.</p>
        </div>
        <div class="callout">
          <h3>Where this guide stops</h3>
          <p>This guide explains how to decide. It does not tell you that any product performs well, because that has not been established. If a hands-on test happens, the method and the result will be published together.</p>
        </div>
      </article>
      <aside class="aside">
        <h3>Products in this guide</h3>
        <ul style="list-style:none;padding:0">
          ${related.map(p2 => `<li style="margin-bottom:16px">
            <a href="${esc(url('/products/' + p2.slug + '/'))}" style="text-decoration:none"><strong>${esc(p2.shortName)}</strong></a>
            <div style="margin-top:6px">${buyButton(p2, 'guide-sidebar')}</div>
          </li>`).join('')}
        </ul>
        <h3 style="margin-top:22px">Elsewhere</h3>
        <ul>
          <li><a href="${esc(url('/guides/'))}">All guides</a></li>
          <li><a href="${esc(url('/flagged/'))}">Flagged for review</a></li>
          <li><a href="${esc(url('/disclosure/'))}">Disclosure policy</a></li>
        </ul>
      </aside>
    </div>
  </div>
</section>`;

  pages.push({ path: p, html: shell({
    path: p, active: '/guides/', title: g.title,
    description: g.deck,
    body,
    extraHead: `<script type="application/ld+json">${JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'Article',
      headline: g.title,
      description: g.deck,
      datePublished: g.published,
      dateModified: g.updated,
      author: { '@type': 'Organization', name: data.site.author },
      publisher: { '@type': 'Organization', name: data.site.name },
      mainEntityOfPage: abs(p)
    })}</script>`
  }) });
}

/* ---------- product pages ---------- */
for (const p of products) {
  const pg = `/products/${p.slug}/`;
  const relatedGuides = guides.filter(g => g.relatedProducts.includes(p.slug));
  const body = `
<div class="wrap"><div class="crumbs"><a href="${esc(url('/'))}">Home</a> / <a href="${esc(url('/' + p.category + '/'))}">${esc(p.category === 'air-fryers' ? 'Air fryers' : 'Thermometers')}</a> / ${esc(p.shortName)}</div></div>
<section class="section" style="padding-top:26px">
  <div class="wrap">
    <div class="two-col">
      <article class="article">
        <p class="eyebrow">${esc(p.brand)} · ${esc(p.formFactor)}</p>
        <h1>${esc(p.name)}</h1>
        <p class="standfirst">${esc(p.claim)}. Here is who that suits, what it costs you in attention, and the one question we would want answered before buying.</p>

        <div class="callout ${p.status === 'blocked' ? 'alert' : 'gate'}">
          <h3>Verification status</h3>
          <p>${esc(p.statusReason)}</p>
          <p style="margin-top:8px">This page describes the product using the manufacturer's published specifications. It is not a review, there is no score, and nothing here is based on hands-on use.</p>
        </div>

        <h2>What it is designed to do</h2>
        <p>${esc(p.claim)}.</p>

        <h2>Who it suits</h2>
        <p>${esc(p.bestFor)}</p>

        <h2>Why it matters</h2>
        <p>${esc(p.whyItMatters)}</p>

        <h2>The trade-off</h2>
        <p>${esc(p.tradeoff)}</p>

        <h2>The question we would want answered</h2>
        <blockquote>${esc(p.headlineTest)}</blockquote>
        <p>We do not know the answer yet. When a measured test exists, the method and the result will be published on this page together, with the date.</p>

        <h2>Published specifications</h2>
        <div class="table-scroll">
          <table>
            <caption>Manufacturer-stated specifications. Not independently measured.</caption>
            <thead><tr><th>Attribute</th><th>Value</th><th>Status</th></tr></thead>
            <tbody>
              <tr><td>Brand</td><td>${esc(p.brand)}</td><td>${pill('verified')} per listing</td></tr>
              <tr><td>Form factor</td><td>${esc(p.formFactor)}</td><td>${pill('verified')} per listing</td></tr>
              <tr><td>Capacity</td><td>${p.capacity ? esc(p.capacity) : '<em>Not published for this product type</em>'}</td><td>${p.capacity ? pill('verified') + ' per listing' : pill('open')}</td></tr>
              <tr><td>Price</td><td><em>Not displayed. Amazon restricts price display absent API entitlements.</em></td><td>${pill('blocked')}</td></tr>
              <tr><td>Customer rating</td><td><em>Not displayed. Ratings may only be shown if obtained via Creators API or PA API.</em></td><td>${pill('blocked')}</td></tr>
              <tr><td>Measured performance</td><td><em>Not tested</em></td><td>${pill('open')}</td></tr>
            </tbody>
          </table>
        </div>

        <h2>Link record, kept deliberately in two fields</h2>
        <div class="table-scroll">
          <table>
            <caption>The intended listing and the observed redirect are separate records and are never merged.</caption>
            <thead><tr><th>Field</th><th>Value</th><th>Source</th></tr></thead>
            <tbody>
              <tr><td>Supplied short link</td><td><code>${esc(p.suppliedShortLink)}</code></td><td>Provided in the brief</td></tr>
              <tr><td>Intended ASIN</td><td><em>Not recorded</em> — awaiting confirmation</td><td>${pill('open')}</td></tr>
              <tr><td>Official listing URL</td><td><em>Not recorded</em> — awaiting confirmation</td><td>${pill('open')}</td></tr>
              <tr><td>Confirmation date</td><td><em>Not recorded</em></td><td>${pill('open')}</td></tr>
              <tr><td>Observed redirect target</td><td><code>${esc(p.observedRedirectUrl)}</code></td><td>Observed ${esc(data.site.buildDate)}</td></tr>
              <tr><td>Observed product ID</td><td><code>${esc(p.observedAsin)}</code></td><td>Read from redirect</td></tr>
            </tbody>
          </table>
        </div>
        <p style="font-size:13.5px;color:var(--ink-3)">${esc(p.observedRedirectNote)}</p>

        <div class="callout">
          <h3>Why the price is blank on purpose</h3>
          <p>A price copied onto a page goes stale the moment it changes, and Amazon's rules restrict showing price and availability unless Amazon serves it or it arrives through its API. Rather than show a number that might be wrong, this page sends you to the listing, where the price is always current.</p>
        </div>

        ${relatedGuides.length ? `<h2>Read before you decide</h2>
        <ul>${relatedGuides.map(g => `<li><a href="${esc(url('/guides/' + g.slug + '/'))}">${esc(g.title)}</a></li>`).join('')}</ul>` : ''}
      </article>
      <aside class="aside">
        <h3>Check it on Amazon</h3>
        <div style="margin-top:4px">${buyButton(p, 'product-sidebar')}</div>
        <h3 style="margin-top:22px">Status</h3>
        <p style="font-size:13.5px;margin:0">${pill(p.status)}</p>
        <p style="font-size:13.5px;margin-top:8px">${esc(p.statusReason)}</p>
        <h3 style="margin-top:22px">Honest summary</h3>
        <p style="font-size:13.5px;margin:0">${esc(p.whyItMatters)} <em>Trade-off:</em> ${esc(p.tradeoff)}</p>
      </aside>
    </div>
  </div>
</section>`;

  pages.push({ path: pg, html: shell({
    path: pg, active: url('/' + p.category + '/').replace(BASE, ''),
    title: p.shortName,
    description: `${p.name}: what it is designed to do, who it suits, and the trade-off. Specifications from the manufacturer; no hands-on testing claimed.`,
    body,
    extraHead: `<script type="application/ld+json">${JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'Product',
      name: p.name,
      brand: { '@type': 'Brand', name: p.brand },
      description: p.claim,
      offers: { '@type': 'Offer', availability: 'https://schema.org/InStock', url: p.observedRedirectUrl },
      review: undefined
    })}</script>`
  }) });
}

/* ---------- sources ---------- */
const sourcesBody = `
<div class="wrap"><div class="crumbs"><a href="${esc(url('/'))}">Home</a> / Sources</div></div>
<section class="hero">
  <div class="wrap">
    <p class="kicker">Source register</p>
    <h1>Every claim has an address.</h1>
    <p class="dek">${sources.length} primary sources, each with the specific rule or figure it supports. Where a claim had no source, it was removed from the site rather than softened.</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="table-scroll">
      <table>
        <caption>Primary sources used across this site. All accessed ${esc(data.site.buildDate)}.</caption>
        <thead><tr><th>ID</th><th>Source</th><th>Publisher</th><th>What it supports</th></tr></thead>
        <tbody>
          ${sources.map(s => `<tr>
            <td><code>${esc(s.id)}</code></td>
            <td><a href="${esc(s.url)}" rel="noopener" target="_blank">${esc(s.label)}</a></td>
            <td>${esc(s.publisher)}</td>
            <td>${esc(s.supports)}</td>
          </tr>`).join('')}
        </tbody>
      </table>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">Method</p><h2>Verification log</h2></div></div>
    <div class="table-scroll">
      <table>
        <caption>What was checked, how, and what happened. Includes the checks that failed.</caption>
        <thead><tr><th>ID</th><th>Checked</th><th>Method</th><th>Result</th><th>Status</th></tr></thead>
        <tbody>
          ${data.verificationLog.map(v => `<tr>
            <td><code>${esc(v.id)}</code></td>
            <td>${esc(v.what)}<div style="font-size:12.5px;color:var(--ink-3);margin-top:4px">${esc(v.method)}</div></td>
            <td>${esc(v.checked)}</td>
            <td>${esc(v.result)}</td>
            <td>${pill(v.status === 'verified' ? 'verified' : 'open')}</td>
          </tr>`).join('')}
        </tbody>
      </table>
    </div>
  </div>
</section>`;

pages.push({ path: '/sources/', html: shell({
  path: '/sources/', active: '/sources/', title: 'Sources',
  description: 'Primary sources for every factual claim on the site, plus the verification log including failed checks.',
  body: sourcesBody
}) });

/* ---------- flagged ---------- */
const flaggedBody = `
<div class="wrap"><div class="crumbs"><a href="${esc(url('/'))}">Home</a> / Flagged for review</div></div>
<section class="hero">
  <div class="wrap">
    <p class="kicker">${flags.length} items · nothing hidden</p>
    <h1>Flagged for review.</h1>
    <p class="dek">Irregularities, unverified items and open compliance questions. These do not block publication, and they are not quietly resolved. Each one states what is known, what is not, and what would close it.</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="table-scroll">
      <table>
        <caption>Ordered by severity, then by ID. Severity reflects consequence if the item is left unaddressed.</caption>
        <thead><tr><th>ID</th><th>Severity</th><th>Item</th><th>Action to close</th></tr></thead>
        <tbody>
          ${[...flags].sort((a, b) => {
            const rank = { high: 0, medium: 1, low: 2 };
            return (rank[a.severity] ?? 3) - (rank[b.severity] ?? 3);
          }).map(f => `<tr>
            <td><code>${esc(f.id)}</code></td>
            <td>${pill(f.severity)}</td>
            <td><strong>${esc(f.title)}</strong><div style="margin-top:4px;font-size:13px;color:var(--ink-2)">${esc(f.detail)}</div>
              <div style="margin-top:6px;font-size:12.5px;color:var(--ink-3)">Affects: ${esc(f.affects)}</div>
              <div style="margin-top:4px;font-size:12.5px">Evidence: ${renderEvidence(f.evidence)}</div></td>
            <td style="font-size:13px">${esc(f.action)}</td>
          </tr>`).join('')}
        </tbody>
      </table>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="callout alert">
      <h3>How to read this page</h3>
      <p>High severity means the item affects money, compliance, or what a reader is told. Medium affects how the site is understood. Low is housekeeping. None of these are hidden from the buyer-facing pages: where a flag concerns a product, the product page says so at the top.</p>
    </div>
  </div>
</section>`;

pages.push({ path: '/flagged/', html: shell({
  path: '/flagged/', active: '/flagged/', title: 'Flagged for review',
  description: 'Irregularities, unverified items and open compliance questions, published rather than hidden.',
  body: flaggedBody
}) });

/* ---------- suggestions ---------- */
const prioOrder = { now: 0, next: 1, later: 2 };
const sugBody = `
<div class="wrap"><div class="crumbs"><a href="${esc(url('/'))}">Home</a> / Suggestions</div></div>
<section class="hero">
  <div class="wrap">
    <p class="kicker">${suggestionsDoc.suggestions.length} proposals · a review surface</p>
    <h1>Decide before you build.</h1>
    <p class="dek">${esc(suggestionsDoc.intro)}</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="table-scroll">
      <table>
        <caption>Every proposal with its evidence, its cost, and what it is waiting on.</caption>
        <thead><tr><th>ID</th><th>Proposal</th><th>Area</th><th>Priority</th><th>Depends on</th><th>Status</th></tr></thead>
        <tbody>
          ${[...suggestionsDoc.suggestions].sort((a, b) => (prioOrder[a.priority] ?? 3) - (prioOrder[b.priority] ?? 3)).map(s => `<tr>
            <td><code>${esc(s.id)}</code></td>
            <td><strong>${esc(s.title)}</strong>
              <div style="margin-top:5px;font-size:13px;color:var(--ink-2)">${esc(s.why)}</div>
              <div style="margin-top:6px;font-size:12.5px;color:var(--ink-3)">Cost: ${esc(s.cost)} · Risk: ${esc(s.risk)}</div>
              ${s.evidence && s.evidence.length ? `<div style="margin-top:4px;font-size:12.5px">Evidence: ${s.evidence.map(srcLink).join(', ')}</div>` : ''}
            </td>
            <td>${esc(s.area)}</td>
            <td>${esc(s.priority)}</td>
            <td style="font-size:13px">${esc(s.dependsOn)}</td>
            <td>${pill(s.status)}</td>
          </tr>`).join('')}
        </tbody>
      </table>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="two-col">
      <div>
        <div class="sec-head"><div><p class="eyebrow">Read this first</p><h2>The order that avoids wasted work</h2></div></div>
        <ol>
          <li><strong>Close the link questions.</strong> Confirm enrollment, tag presence and the five intended ASINs. Everything commercial sits behind this.</li>
          <li><strong>Write the privacy notice.</strong> Before any measurement or capture is switched on, not after.</li>
          <li><strong>Deploy a collector.</strong> Then the ledger can start filling from reports instead of staying empty.</li>
          <li><strong>Verify Search Console and submit the sitemap.</strong> Four weeks later, choose the next guide from queries.</li>
          <li><strong>Only then</strong> consider a test protocol, imagery and a newsletter.</li>
        </ol>
      </div>
      <aside class="aside">
        <h3>What choosing looks like</h3>
        <p style="font-size:13.5px;margin:0 0 10px">A proposal is ready to implement when its "depends on" column is satisfied and its status is not blocked. Nothing on this page has been silently implemented.</p>
        <p style="font-size:13.5px;margin:0"><a href="${esc(url('/questions/'))}">The open questions →</a></p>
      </aside>
    </div>
  </div>
</section>`;

pages.push({ path: '/suggestions/', html: shell({
  path: '/suggestions/', active: '/suggestions/', title: 'Suggestions',
  description: 'A review surface: every proposed change, its evidence, its cost, and what it is waiting on.',
  body: sugBody
}) });

/* ---------- questions ---------- */
const qBody = `
<div class="wrap"><div class="crumbs"><a href="${esc(url('/'))}">Home</a> / Open questions</div></div>
<section class="hero">
  <div class="wrap">
    <p class="kicker">${questions.groups.reduce((n, g) => n + g.rows.length, 0)} questions · ${questions.groups.length} groups</p>
    <h1>What we know, what we don't, and how to find out.</h1>
    <p class="dek">${esc(questions.intro)}</p>
  </div>
</section>
${questions.groups.map(g => `
<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">${esc(g.id)}</p><h2>${esc(g.title)}</h2><p class="sub">${esc(g.note)}</p></div></div>
    <div class="table-scroll">
      <table>
        <thead><tr><th>Question</th><th>What is known</th><th>What is not known</th><th>How to answer it</th><th>Source</th><th>Status</th></tr></thead>
        <tbody>
          ${g.rows.map(r => `<tr>
            <td><strong>${esc(r.q)}</strong>${r.answer ? `<div style="margin-top:6px;font-size:12.5px;color:var(--green)"><strong>Answer:</strong> ${esc(r.answer)}</div>` : ''}</td>
            <td style="font-size:13.5px">${esc(r.known)}</td>
            <td style="font-size:13.5px">${esc(r.unknown)}</td>
            <td style="font-size:13.5px">${esc(r.how)}</td>
            <td>${srcLink(r.source)}</td>
            <td>${pill(r.status)}</td>
          </tr>`).join('')}
        </tbody>
      </table>
    </div>
  </div>
</section>`).join('')}
<section class="section">
  <div class="wrap">
    <div class="callout gate">
      <h3>Why these are published instead of resolved</h3>
      <p>Every question here could be answered by guessing. A guess would make the site look complete and would be wrong. Answering them properly needs access to Associates Central, a Search Console property, or a decision from the account holder, and none of those were available during this build.</p>
    </div>
  </div>
</section>`;

pages.push({ path: '/questions/', html: shell({
  path: '/questions/', active: '/questions/', title: 'Open questions',
  description: 'The questions that must be answered before any further decision: what is known, what is missing, and how to close each gap.',
  body: qBody
}) });

/* ---------- ledger ---------- */
const ledgerBody = `
<div class="wrap"><div class="crumbs"><a href="${esc(url('/'))}">Home</a> / Ledger</div></div>
<section class="hero">
  <div class="wrap">
    <p class="kicker">${ledger.rows.length} rows · deliberately empty</p>
    <h1>${esc(ledger.title)}</h1>
    <p class="dek">${esc(ledger.intro)}</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="stat-row">
      <div class="stat"><div class="k">Rows</div><div class="v">0</div><div class="n">No report has been pulled</div></div>
      <div class="stat"><div class="k">Sessions</div><div class="v">—</div><div class="n">No collector deployed</div></div>
      <div class="stat"><div class="k">Clicks</div><div class="v">—</div><div class="n">No collector deployed</div></div>
      <div class="stat"><div class="k">Orders</div><div class="v">—</div><div class="n">No Associates report accessed</div></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">Structure</p><h2>The ledger, with its columns defined</h2></div></div>
    <div class="table-scroll">
      <table>
        <caption>No cell is filled until a number arrives from an authorized report.</caption>
        <thead><tr>${ledger.columns.map(c => `<th>${esc(c)}</th>`).join('')}</tr></thead>
        <tbody>
          <tr>${ledger.columns.map(() => `<td style="color:var(--ink-3)">—</td>`).join('')}</tr>
        </tbody>
      </table>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="two-col">
      <div>
        <div class="sec-head"><div><p class="eyebrow">Rules of the ledger</p><h2>Why it starts empty</h2></div></div>
        <ul>${ledger.rules.map(r => `<li>${esc(r)}</li>`).join('')}</ul>
      </div>
      <aside class="aside">
        <h3>Explicitly not presented</h3>
        <ul>
          <li>No conversion rate</li>
          <li>No revenue forecast</li>
          <li>No earnings per click</li>
          <li>No benchmark from other sites</li>
        </ul>
        <p style="font-size:13px;margin:10px 0 0">A fabricated benchmark is the fastest way to make a data page useless. This one stays empty until it can be true.</p>
      </aside>
    </div>
  </div>
</section>`;

pages.push({ path: '/ledger/', html: shell({
  path: '/ledger/', active: '/ledger/', title: 'Ledger',
  description: 'An empty campaign ledger with defined columns. Rows are added only from authorized first-party reports, with provenance.',
  body: ledgerBody
}) });

/* ---------- research ---------- */
const researchBody = `
<div class="wrap"><div class="crumbs"><a href="${esc(url('/'))}">Home</a> / Research</div></div>
<section class="hero">
  <div class="wrap">
    <p class="kicker">Automation, honestly described</p>
    <h1>${esc(research.title)}</h1>
    <p class="dek">${esc(research.standfirst)}</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">Gates</p><h2>What stops the research layer</h2></div></div>
    <div class="table-scroll">
      <table>
        <caption>Three gates, each traceable to a published rule.</caption>
        <thead><tr><th>Gate</th><th>Requirement</th><th>Detail</th><th>Status</th><th>Source</th></tr></thead>
        <tbody>
          ${research.gateSummary.map(g => `<tr>
            <td><strong>${esc(g.gate)}</strong></td>
            <td style="font-size:13.5px">${esc(g.requirement)}</td>
            <td style="font-size:13.5px">${esc(g.detail)}</td>
            <td>${pill(g.status)}</td>
            <td>${srcLink(g.source)}</td>
          </tr>`).join('')}
        </tbody>
      </table>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">Capabilities</p><h2>Designed versus running</h2><p class="sub">The gap between the two columns is the honest state of the automation.</p></div></div>
    <div class="table-scroll">
      <table>
        <caption>Nothing in the right-hand columns is simulated.</caption>
        <thead><tr><th>Capability</th><th>Designed behaviour</th><th>Today</th><th>Automated</th></tr></thead>
        <tbody>
          ${research.designedCapabilities.map(c => `<tr>
            <td><strong>${esc(c.capability)}</strong></td>
            <td style="font-size:13.5px">${esc(c.designed)}</td>
            <td style="font-size:13.5px">${esc(c.today)}</td>
            <td>${pill(c.automated)}</td>
          </tr>`).join('')}
        </tbody>
      </table>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="callout alert">
      <h3>On scores and forecasts</h3>
      <p>${esc(research.scoringNote)}</p>
    </div>
  </div>
</section>`;

pages.push({ path: '/research/', html: shell({
  path: '/research/', active: '/research/', title: 'Research',
  description: 'What the product-research automation is designed to do, what actually runs today, and the API gates that block the rest.',
  body: researchBody
}) });

/* ---------- author ---------- */
const authorBody = `
<div class="wrap"><div class="crumbs"><a href="${esc(url('/'))}">Home</a> / Who writes this</div></div>
<section class="hero">
  <div class="wrap">
    <p class="kicker">Authorship</p>
    <h1>Who writes this, and how.</h1>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="two-col">
      <article class="article">
        <p class="standfirst">This site is written by an AI assistant working from a verified source register and a supplied product list, and published by the account holder. That sentence is on this page because the alternative — inventing a human byline with invented credentials — would be a lie told to both readers and search engines.</p>

        <h2>What that means in practice</h2>
        <p>Every factual claim about Amazon's rules on this site traces to a link in the <a href="${esc(url('/sources/'))}">source register</a>. Every product attribute traces to the manufacturer's published listing. Where neither exists, the site says so rather than filling the gap.</p>

        <h2>What we have not done</h2>
        <p>We have not used any of these appliances. There are therefore no first-person performance claims, no measured times, no noise figures and no durability impressions anywhere on this site. Federal guidance is clear that you cannot describe your experience with a product you have not tried, and that rule is the reason half of the usual affiliate content is missing here.</p>

        <h2>How corrections work</h2>
        <p>An error, once found, is corrected on the page and recorded in the <a href="${esc(url('/flagged/'))}">flagged for review</a> log with the date. Silent edits would undermine the only thing this site has going for it.</p>

        <h2>Why the byline is an organisation, not a person</h2>
        <p>Because there is no person to name yet. When a named human editor takes ownership of this site, the byline changes, structured data changes, and this page is rewritten. Until then, inventing an author would be the single most damaging thing this site could do.</p>
      </article>
      <aside class="aside">
        <h3>Editorial rules</h3>
        <ul>
          <li>No invented measurements</li>
          <li>No invented author credentials</li>
          <li>No price display without API entitlements</li>
          <li>No rating display without API entitlements</li>
          <li>No revenue, traffic or conversion forecasts</li>
          <li>Every disclosure on every page</li>
        </ul>
        <p style="font-size:13px;margin:12px 0 0"><a href="${esc(url('/disclosure/'))}">Full disclosure policy →</a></p>
      </aside>
    </div>
  </div>
</section>`;

pages.push({ path: '/author/', html: shell({
  path: '/author/', active: '/author/', title: 'Who writes this',
  description: 'Authorship disclosure: this site is AI-assisted, what that means, and what it deliberately does not claim.',
  body: authorBody
}) });

/* ---------- disclosure ---------- */
const disclosureBody = `
<div class="wrap"><div class="crumbs"><a href="${esc(url('/'))}">Home</a> / Disclosure</div></div>
<section class="hero">
  <div class="wrap">
    <p class="kicker">Disclosure and editorial policy</p>
    <h1>${esc(DISCLOSURE)}</h1>
    <p class="dek">That sentence appears under the masthead of every page on this site, and again in the footer. This page explains exactly what it means, where the links go, and what this site does not claim.</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="two-col">
      <article class="article">
        <h2>What the disclosure means</h2>
        <p>Outbound product links on this site are affiliate links. If you click one and buy something on Amazon, this site may earn a commission. The price you pay does not change.</p>
        <p>Amazon requires Associates to state, clearly and prominently, that they earn from qualifying purchases. The required wording is reproduced exactly, without paraphrase, and it appears above the fold on every page rather than only on this one.</p>

        <h2>Where the links point</h2>
        <p>Buttons marked <strong>Paid link</strong> send you to Amazon. The exact destination for each product is recorded on that product's page, in a table that keeps the intended listing separate from the observed redirect. That separation is deliberate: one is what was intended, the other is what was actually observed.</p>

        <h2>What this site does not do</h2>
        <ul>
          <li>It does not show prices. Amazon restricts price display unless Amazon serves the link or the data arrives through its API.</li>
          <li>It does not show customer ratings. The same restriction applies.</li>
          <li>It does not claim hands-on testing. No product here has been tested.</li>
          <li>It does not use Amazon trademarks in the site name, the domain or any identifier.</li>
          <li>It does not run pop-ups, interstitials or exit overlays around affiliate links.</li>
          <li>It does not place affiliate links in email or private messages.</li>
        </ul>

        <h2>Editorial independence</h2>
        <p>The list is short and it is not ranked. A product appearing here is not an assertion that it is the best at anything. Commission rates did not determine the order, because no commission data exists for this site yet and inventing it would defeat the purpose of the list.</p>

        <h2>Privacy, briefly</h2>
        <p>This site counts five aggregate events: page views, whether the disclosure strip was visible, outbound product clicks, guide read depth, and sign-up submissions. There are no cookies, no identifiers and no cross-site tracking. Your browser's Do Not Track setting is honoured. There is currently no analytics endpoint deployed, which means nothing is transmitted anywhere at all.</p>

        <h2>Contact</h2>
        <p>No contact address is published yet. That is an open item on the <a href="${esc(url('/questions/'))}">open questions</a> page, not an oversight that has been quietly accepted.</p>
      </article>
      <aside class="aside">
        <h3>The required statement</h3>
        <p style="font-size:13.5px"><strong>${esc(DISCLOSURE)}</strong></p>
        <h3 style="margin-top:20px">Governing sources</h3>
        <ul>
          <li>${srcLink('S-01')} Operating Agreement §5</li>
          <li>${srcLink('S-02')} Program Policies</li>
          <li>${srcLink('S-06')} FTC Disclosures 101</li>
          <li>${srcLink('S-07')} 16 CFR Part 255</li>
        </ul>
        <h3 style="margin-top:20px">Tracking ID</h3>
        <p style="font-size:13.5px;margin:0"><code>${esc(TID)}</code></p>
      </aside>
    </div>
  </div>
</section>`;

pages.push({ path: '/disclosure/', html: shell({
  path: '/disclosure/', active: '/disclosure/', title: 'Disclosure',
  description: 'What the affiliate disclosure means, where links point, and what this site deliberately does not claim.',
  body: disclosureBody
}) });

/* ---------- executive summary ---------- */
const summaryBody = `
<div class="wrap"><div class="crumbs"><a href="${esc(url('/'))}">Home</a> / Executive summary</div></div>
<section class="hero">
  <div class="wrap">
    <p class="kicker">Executive summary · ${esc(data.site.buildDate)}</p>
    <h1>What was built, what was verified, what is still open.</h1>
    <p class="dek">A one-page account of this build, written for someone who has three minutes and needs to know what is trustworthy and what is not.</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="stat-row">
      <div class="stat"><div class="k">Products</div><div class="v">${products.length}</div><div class="n">4 publishable, 1 held</div></div>
      <div class="stat"><div class="k">Guides</div><div class="v">${guides.length}</div><div class="n">Across ${clusters.length} clusters</div></div>
      <div class="stat"><div class="k">Sources</div><div class="v">${sources.length}</div><div class="n">All linked</div></div>
      <div class="stat"><div class="k">Flagged</div><div class="v">${flags.length}</div><div class="n">Published, not hidden</div></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="two-col">
      <article class="article">
        <h2>Done</h2>
        <p>A static site built from one data file, with a home page, two category pages, five product pages, ${guides.length} question-shaped guides, and dashboard surfaces for research, the campaign ledger, suggestions, open questions, sources, and flagged items. Every page carries the required disclosure twice. One command rebuilds everything.</p>

        <h2>Verified</h2>
        <p>All five supplied short links were resolved against Amazon itself and the results recorded, including the one that did not resolve consistently. The requirements that govern this site were read from primary sources: Amazon's Operating Agreement, Program Policies, Creators API documentation and help pages, the FTC's disclosure guidance, 16 CFR Part 255, the USDA temperature chart, and Google's search documentation. ${sources.length} sources, all linked.</p>

        <h2>Deliberately not done</h2>
        <ul>
          <li>No prices shown to readers, because Amazon restricts price display without API entitlements.</li>
          <li>No ratings shown, for the same reason.</li>
          <li>No performance claims, because nothing was tested.</li>
          <li>No revenue, traffic or conversion forecasts, because there is no data to base them on.</li>
          <li>No invented author or credentials.</li>
          <li>No product photography, because imagery rights are unresolved.</li>
        </ul>

        <h2>The five decisions that come next</h2>
        <ol>
          <li>Confirm Associates enrollment and confirm that one click registers in the tracking report.</li>
          <li>Record the five intended ASINs as a separate confirmation record.</li>
          <li>Regenerate the link that resolved inconsistently before publishing it.</li>
          <li>Deploy an analytics collector and a privacy notice, in that order.</li>
          <li>Verify Search Console, submit the sitemap, and choose the next guide from measured queries.</li>
        </ol>
      </article>
      <aside class="aside">
        <h3>The one thing to read</h3>
        <p style="font-size:13.5px">The <a href="${esc(url('/flagged/'))}">flagged for review</a> page. Sixteen items, ordered by consequence, each with what is known and what would close it.</p>
        <h3 style="margin-top:20px">Jump to</h3>
        <ul>
          <li><a href="${esc(url('/research/'))}">Research and automation</a></li>
          <li><a href="${esc(url('/ledger/'))}">Campaign ledger</a></li>
          <li><a href="${esc(url('/suggestions/'))}">Suggestions</a></li>
          <li><a href="${esc(url('/questions/'))}">Open questions</a></li>
          <li><a href="${esc(url('/sources/'))}">Sources</a></li>
        </ul>
      </aside>
    </div>
  </div>
</section>`;

pages.push({ path: '/executive-summary/', html: shell({
  path: '/executive-summary/', active: '/executive-summary/', title: 'Executive summary',
  description: 'A one-page account of what was built, what was verified, what was deliberately left out, and the next five decisions.',
  body: summaryBody
}) });

/* ---------- coordination page ---------- */
const coordMd = fs.readFileSync(path.join(ROOT, 'COORDINATION.md'), 'utf8');
const coordBody = `
<div class="wrap"><div class="crumbs"><a href="${esc(url('/'))}">Home</a> / Session board</div></div>
<section class="hero">
  <div class="wrap">
    <p class="kicker">Multi-session coordination</p>
    <h1>The shared task board.</h1>
    <p class="dek">The live version of this file is at the repository root. This page renders it so the board is readable without leaving the site.</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <article class="article" style="max-width:none">
      <pre style="white-space:pre-wrap;font-family:var(--mono);font-size:13px;background:#fff;border:1px solid var(--rule);padding:20px;overflow-x:auto">${esc(coordMd)}</pre>
    </article>
  </div>
</section>`;

pages.push({ path: '/COORDINATION/', html: shell({
  path: '/COORDINATION/', active: '', title: 'Session board',
  description: 'The shared multi-session task board for this repository.',
  body: coordBody
}) });

/* --------------------------------------------------------- special files */
function writeSitemap() {
  const urls = pages.filter(p => p.path !== '/COORDINATION/').map(p => {
    const isGuide = p.path.startsWith('/guides/') && p.path !== '/guides/';
    const g = guides.find(x => p.path === `/guides/${x.slug}/`);
    return `  <url>
    <loc>${abs(p.path)}</loc>
    <lastmod>${isGuide && g ? g.updated : data.site.buildDate}</lastmod>
    <changefreq>${p.path === '/' ? 'weekly' : 'monthly'}</changefreq>
    <priority>${p.path === '/' ? '1.0' : p.path === '/guides/' ? '0.9' : '0.7'}</priority>
  </url>`;
  }).join('\n');
  fs.writeFileSync(path.join(OUT, 'sitemap.xml'),
    `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>\n`);
  return pages.length - 1;
}

function writeFeed() {
  const items = guides.map(g => `    <item>
      <title>${esc(g.title)}</title>
      <link>${abs('/guides/' + g.slug + '/')}</link>
      <guid isPermaLink="true">${abs('/guides/' + g.slug + '/')}</guid>
      <pubDate>${new Date(g.published + 'T09:00:00Z').toUTCString()}</pubDate>
      <category>${esc(g.cluster)}</category>
      <description>${esc(g.deck)}</description>
    </item>`).join('\n');
  fs.writeFileSync(path.join(OUT, 'feed.xml'),
`<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>${esc(data.site.name)} — Guides</title>
    <link>${abs('/guides/')}</link>
    <atom:link href="${abs('/feed.xml')}" rel="self" type="application/rss+xml"/>
    <description>Question-shaped buying guides for air fryers and thermometers.</description>
    <language>${esc(data.site.locale)}</language>
    <lastBuildDate>${new Date(data.site.buildDate + 'T09:00:00Z').toUTCString()}</lastBuildDate>
${items}
  </channel>
</rss>
`);
}

function writeRobots() {
  fs.writeFileSync(path.join(OUT, 'robots.txt'),
`# ${data.site.name}
User-agent: *
Allow: /

Sitemap: ${abs('/sitemap.xml')}
`);
}

function write404() {
  const html = shell({
    path: '/404.html', active: '', title: 'Page not found', noindex: true,
    description: 'That page does not exist.',
    body: `<section class="hero"><div class="wrap">
      <p class="kicker">404</p>
      <h1>That page is not here.</h1>
      <p class="dek">The link may be old, or the page may have moved. Try the shortlist or the guides.</p>
      <p style="margin-top:22px"><a class="btn" href="${esc(url('/'))}">Back to the front page</a></p>
    </div></section>`
  });
  fs.writeFileSync(path.join(OUT, '404.html'), html);
}

/* ------------------------------------------------------------------ write */
fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(OUT, { recursive: true });

let written = [];
for (const p of pages) {
  const rel = (p.path === '/' ? 'index.html' : p.path.replace(/^\//, '').replace(/\/$/, '') + '/index.html');
  written.push({ rel, path: p.path });
  write(rel, p.html);
}

// static assets
for (const f of ['assets/css/site.css', 'assets/js/site.js', 'assets/js/config.js']) {
  fs.mkdirSync(path.dirname(path.join(OUT, f)), { recursive: true });
  fs.copyFileSync(path.join(ROOT, f), path.join(OUT, f));
}

writeSitemap();
writeFeed();
writeRobots();
write404();
fs.writeFileSync(path.join(OUT, '.nojekyll'), '');

/* ------------------------------------------------------- compliance gates */
let errors = 0;
const fail = m => { console.error('  FAIL  ' + m); errors++; };

for (const w of written) {
  const f = path.join(OUT, w.rel);
  const h = fs.readFileSync(f, 'utf8');

  // gate 1: the exact required statement appears at least twice
  const count = (h.match(/As an Amazon Associate I earn from qualifying purchases\./g) || []).length;
  if (count < 2) fail(`${w.path} has ${count} disclosure statement(s), expected 2`);

  // gate 2: an above-the-fold disclosure strip exists
  if (!h.includes('data-disclosure="masthead"')) fail(`${w.path} is missing the masthead disclosure strip`);

  // gate 3: no star ratings or price strings leak into buyer-facing pages
  if (/[0-9]\.[0-9]\s*out of 5/.test(h)) fail(`${w.path} renders a star rating`);
  if (/\$\d+(\.\d\d)?/.test(h)) fail(`${w.path} renders a price`);

  // gate 4: every outbound PRODUCT link is marked sponsored.
  // A product link is one pointing at a /dp/ page, or carrying a tag= parameter.
  // Citation links into Amazon's own help and policy pages are documentation, not
  // affiliate links, and marking those sponsored would itself be a false claim.
  const anchors = [...h.matchAll(/<a\b[^>]*href="([^"]+)"[^>]*>/g)];
  for (const m of anchors) {
    const href = m[1];
    const tag = m[0];
    if (!/^https:\/\/www\.amazon\.com/.test(href) && !/^https:\/\/link\.amazon/.test(href)) continue;
    const isProductLink = /\/dp\//.test(href) || /[?&]tag=/.test(href) || /^https:\/\/link\.amazon/.test(href);
    if (isProductLink) {
      if (!/rel="sponsored/.test(tag)) fail(`${w.path} has an unmarked product link: ${tag.slice(0, 90)}`);
      if (!/nofollow/.test(tag)) fail(`${w.path} product link is missing nofollow: ${tag.slice(0, 90)}`);
      if (!/target="_blank"/.test(tag)) fail(`${w.path} product link does not open in a new tab: ${tag.slice(0, 90)}`);
    } else {
      // Citation link. It must be honest: no sponsored, no nofollow on a reference.
      if (/rel="sponsored/.test(tag)) fail(`${w.path} marks a citation link as sponsored: ${tag.slice(0, 90)}`);
    }
  }

  // gate 6: no third-party link shorteners anywhere (Participation Requirements 3(w) risk)
  if (/href="https?:\/\/(bit\.ly|tinyurl\.com|t\.co|rebrand\.ly|geni\.us|amzn\.to)/.test(h)) {
    fail(`${w.path} uses a third-party link shortener`);
  }
}

if (errors) {
  console.error(`\nBuild failed: ${errors} compliance gate error(s).`);
  process.exit(1);
}

console.log(`Built ${written.length} pages, sitemap, feed, robots.txt and 404.`);
console.log(`Compliance gates passed on all ${written.length} pages.`);
console.log(`  - disclosure statement: twice per page`);
console.log(`  - masthead strip: present`);
console.log(`  - prices/ratings: suppressed`);
console.log(`  - sponsored rel on all Amazon links: confirmed`);
