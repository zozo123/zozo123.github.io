#!/usr/bin/env python3
"""Render index.html, sitemap.xml, and llms.txt from data/works.json.

The page is static HTML so readers, crawlers, and answer engines see every
entry without JavaScript; js/main.js only adds motion and the live years-on-GitHub count.
Run: python3 tools/build_index.py
"""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://zozo123.github.io/"
HOME = "https://yossieliaz.netlify.app/"
NAME = "Yossi Eliaz"
TITLE = "Principal Engineer · AI Researcher · Lecturer · GTM Strategy & Partnerships"
SAME_AS = [
    "https://github.com/zozo123",
    "https://www.linkedin.com/in/yossi-eliaz/",
    "https://scholar.google.com/citations?user=NL1ZyOgAAAAJ",
    "https://x.com/YossiEliaz",
    HOME,
]
# Static fallback; js/main.js replaces it with the live value from the GitHub API.
YEARS_ON_GITHUB = 15


def h(value: object) -> str:
    return html.escape(str(value), quote=True)


def page_url(item: dict) -> str:
    return item.get("url") or f"{SITE}{item['slug']}/"


def thumb(item: dict) -> str:
    return item.get("image") or f"assets/thumbs/{item['slug']}.jpg"


def card(item: dict, number: int, *, plate: bool = False, flip: bool = False) -> str:
    fig = f"""<span class="fig-caption"><span class="fc-no">Fig. {number:02d}</span><span class="fc-live">{"● live page" if page_url(item).startswith(SITE) else "● slides &amp; code"}</span></span>"""
    body = f"""<span class="figure-body"><span class="figure-title">{h(item['title'])}</span><span class="figure-tldr">{h(item['tldr'])}</span><span class="mono figure-link">{"View live →" if page_url(item).startswith(SITE) else "View on GitHub →"}</span></span>"""
    image = f"""<span class="figure-thumb"><img src="{h(thumb(item))}" alt="{h(item['title'])}: page preview" width="760" height="400" loading="lazy"></span>"""
    if plate:
        cls = "figure-card plate plate-flip reveal" if flip else "figure-card plate reveal"
        return f"""<a class="{cls}" href="{h(page_url(item))}">{image}<span class="fig-side">{fig}{body}</span></a>"""
    return f"""<a class="figure-card reveal" href="{h(page_url(item))}">{image}{fig}{body}</a>"""


def selected_card(item: dict) -> str:
    return f"""<article class="figure-card selected-card reveal">
        <a class="figure-thumb" href="{h(page_url(item))}" tabindex="-1" aria-hidden="true"><img src="{h(thumb(item))}" alt="" width="760" height="400" loading="lazy"></a>
        <span class="fig-caption"><span class="fc-no">{h(item['kicker'])}</span><span class="fc-live">{"● live" if page_url(item).startswith(SITE) else "● code"}</span></span>
        <span class="figure-body"><a class="figure-title" href="{h(page_url(item))}">{h(item['title'])}</a><span class="figure-tldr">{h(item['tldr'])}</span><a class="mono figure-link" href="{h(item['link_url'])}">{h(item['link'])}</a></span>
      </article>"""


def section(sec: dict, start: int) -> tuple[str, int]:
    items = sec["items"]
    cards = []
    n = start
    for i, item in enumerate(items):
        n += 1
        closing = sec.get("plate") and i == len(items) - 1 and len(items) > 2 and (len(items) - 2) % 3 == 0
        cards.append(card(item, n, plate=bool(sec.get("plate") and (i == 0 or closing)), flip=bool(closing)))
    grid = "figure-grid figure-grid-2" if sec.get("grid2") else "figure-grid"
    markup = f"""
<section class="section" id="{h(sec['id'])}">
  <div class="asterism mono reveal" aria-hidden="true">✻&nbsp;&nbsp;✻&nbsp;&nbsp;✻</div>
  <div class="section-head reveal">
    <span class="mono section-no">{h(sec['no'])}</span>
    <h2>{sec['title_html']}</h2>
    <p class="section-sub">{h(sec['sub'])}</p>
  </div>
  <div class="{grid}">
    {''.join(cards)}
  </div>
</section>"""
    return markup, n


def json_ld(data: dict) -> str:
    person = {
        "@type": "Person",
        "@id": f"{HOME}#person",
        "name": NAME,
        "jobTitle": TITLE,
        "url": HOME,
        "sameAs": SAME_AS + [SITE],
        "alumniOf": {"@type": "CollegeOrUniversity", "name": "University of Houston"},
        "knowsAbout": ["AI agent sandboxes", "CI and build acceleration", "Computational genomics", "Machine learning", "Computer vision", "Physics"],
    }
    parts = [
        {"@type": "CreativeWork", "name": i["title"], "url": page_url(i), "description": i["tldr"], "author": {"@id": f"{HOME}#person"}}
        for i in data["selected"]
    ] + [
        {"@type": "CreativeWork", "name": i["title"], "url": page_url(i), "description": i["tldr"], "author": {"@id": f"{HOME}#person"}}
        for sec in data["sections"] for i in sec["items"]
    ]
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            person,
            {"@type": "WebSite", "@id": f"{SITE}#site", "url": SITE, "name": f"{NAME}: Writing & experiments", "author": {"@id": f"{HOME}#person"}},
            {"@type": "CollectionPage", "url": SITE, "name": f"{NAME}: Collected works", "isPartOf": {"@id": f"{SITE}#site"}, "author": {"@id": f"{HOME}#person"}, "hasPart": parts},
        ],
    }
    return json.dumps(graph, ensure_ascii=False, separators=(",", ":"))


def render(data: dict) -> str:
    sections = []
    n = 0
    for sec in data["sections"]:
        markup, n = section(sec, n)
        sections.append(markup)
    all_urls = [page_url(i) for i in data["selected"]] + [data["featured"]["url"]] + [page_url(i) for s in data["sections"] for i in s["items"]]
    total_pages = len({u for u in all_urls if u.startswith(SITE)})
    toc = "".join(
        f"""<li><a href="#{h(s['id'])}"><span class="toc-no">§{s['no'][-2:]}</span><span class="toc-t">{h(s['toc'])}</span><span class="toc-dots"></span><span class="toc-n">{len(s['items']):02d}</span></a></li>"""
        for s in data["sections"]
    )
    selected = "".join(selected_card(i) for i in data["selected"])
    f = data["featured"]
    description = "Writing, field guides, and live experiments by Yossi Eliaz on AI agent sandboxes, CI, genomics, and physics. Principal Engineer, AI Researcher, Lecturer, GTM Strategy & Partnerships."
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#f6f1e6">
<meta name="color-scheme" content="light">
<title>Yossi Eliaz — Collected works: writing &amp; experiments</title>
<meta name="description" content="{h(description)}">
<meta name="author" content="Yossi Eliaz">
<link rel="canonical" href="{SITE}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Yossi Eliaz">
<meta property="og:title" content="Yossi Eliaz — Collected works: writing &amp; experiments">
<meta property="og:description" content="Notes, measurements, and live experiments from building difficult systems: agent sandboxes, CI, genomics, and physics.">
<meta property="og:url" content="{SITE}">
<meta property="og:image" content="{SITE}assets/og/card.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Yossi Eliaz, Writing &amp; experiments">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@YossiEliaz">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="text/markdown" href="{SITE}llms.txt" title="Agent index">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,300..900&amp;family=Spectral:ital,wght@0,300;0,400;0,500;1,300;1,400&amp;family=IBM+Plex+Mono:wght@400;500;600&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
<script type="application/ld+json">{json_ld(data)}</script>
</head>
<body class="no-js">

<a class="skip-link mono" href="#main">Skip to content</a>

<svg class="grain-defs" width="0" height="0" aria-hidden="true">
  <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
</svg>
<div class="grain" aria-hidden="true"></div>

<header class="masthead">
  <div class="masthead-inner">
    <a class="mono mast-id" href="{SITE}">Y.&nbsp;Eliaz — Collected&nbsp;Works</a>
    <nav class="mast-nav mono" aria-label="Primary">
      <a href="#work">Work</a>
      <a href="#writing">§01 Agents</a>
      <a href="#science">§02 Science</a>
      <a href="#essays">§03 Essays</a>
      <a class="mast-feature" href="{SITE}the-living-layer/">THE LIVING LAYER</a>
      <a href="{HOME}">Profile&nbsp;↗</a>
      <a class="mast-gh" href="https://github.com/zozo123">GitHub&nbsp;↗</a>
    </nav>
  </div>
</header>

<main id="main">

<section class="hero" aria-labelledby="hero-name">
  <div class="hero-rule mono reveal in-load">
    <span class="hr-tag">eliaz : 2026 · living preprint · v3</span>
    <span class="hero-rule-line"></span>
    <span id="today-date">OCT 2026</span>
  </div>

  <h1 class="hero-title" id="hero-name">
    <span class="ht-line reveal in-load d1">Yossi</span>
    <span class="ht-line hero-title-row reveal in-load d2">
      <em>Eliaz</em>
      <span class="hero-portrait" aria-hidden="true">
        <img src="https://media.giphy.com/media/9zXG9hZsLAa3x4xEaV/giphy.gif" alt="" width="256" height="256" fetchpriority="high">
      </span>
    </span>
  </h1>

  <div class="hero-meta">
    <div class="hero-left reveal in-load d3">
      <p class="hero-abstract">
        <span class="mono abstract-label">Abstract</span>
        <strong>{h(TITLE)}.</strong> Build difficult systems. Make them useful.
        I build AI execution infrastructure, production ML, and scientific software, on a path from
        GPS/navigation and Android/Linux kernels through computational physics, genomics, and
        autonomous-driving perception to secure agent sandboxes. <span class="thin">PhD in Physics; Senior Lecturer at HIT.</span>
      </p>
      <div class="hero-affil mono">
        <span class="affil-label">Correspondence</span>
        <a href="https://github.com/zozo123">GitHub</a><sup>1</sup>
        <a href="https://scholar.google.com/citations?user=NL1ZyOgAAAAJ&amp;hl=en">Scholar</a><sup>2</sup>
        <a href="https://www.linkedin.com/in/yossi-eliaz/">LinkedIn</a><sup>3</sup>
        <a href="https://x.com/YossiEliaz">𝕏</a><sup>4</sup>
        <a href="https://youtube.com/channel/UCkm7FnFBfaKUNKQBLF7TDOQ">YouTube</a><sup>5</sup>
        <a href="{HOME}">Professional site</a><sup>6</sup>
      </div>
    </div>

    <nav class="toc reveal in-load d4" aria-label="Contents">
      <span class="mono toc-head">Contents</span>
      <ol class="mono">
        <li><a href="#work"><span class="toc-no">✦</span><span class="toc-t">Selected work</span><span class="toc-dots"></span><span class="toc-n">{len(data['selected']):02d}</span></a></li>
        {toc}
        <li><a href="#stats"><span class="toc-no">§06</span><span class="toc-t">Receipts</span><span class="toc-dots"></span><span class="toc-n">02</span></a></li>
      </ol>
    </nav>
  </div>

  <div class="hero-stats reveal in-load d5">
    <div class="stat"><span class="stat-n" data-count="{total_pages}">{total_pages}</span><span class="mono stat-l">live pages here</span></div>
    <div class="stat"><span class="stat-n" data-count="{YEARS_ON_GITHUB}" data-live="years">{YEARS_ON_GITHUB}</span><span class="mono stat-l">years on GitHub</span></div>
  </div>
</section>

<section class="section selected" id="work" aria-labelledby="work-title">
  <div class="section-head reveal">
    <span class="mono section-no">✦ Selected work</span>
    <h2 id="work-title">Now <em>building</em></h2>
    <p class="section-sub">Systems for coding agents, and one genome-scale measurement. Each states its limits.</p>
  </div>
  <div class="figure-grid">
    {selected}
  </div>
</section>

<div class="mission">
  <div class="mission-copy">
    <div class="mission-kicker">THESIS 001 • 2026</div>
    <div class="mission-title">THE LIVING LAYER</div>
    <div class="mission-body">A speculative architecture thesis.<br>What if sandboxes were the universal execution primitive, and one governed database held UI, logic, state, history, and policy?<br>Software would be instantiated, not deployed.</div>
  </div>
  <div class="mission-action">
    <a class="mission-link" href="{SITE}the-living-layer/">Read the thesis →</a>
    <div class="mission-meta">ESSAY • HYPOTHESIS • SINGLE FILE</div>
  </div>
</div>

<section class="latest" id="latest">
  <div class="latest-inner">
    <div class="latest-body reveal">
      <span class="mono kicker">{h(f['kicker'])}</span>
      <h2>{f['title_html']}</h2>
      <p>{h(f['tldr'])}</p>
      <a class="mono read-cta" href="{h(f['url'])}">Read it live&nbsp;→</a>
    </div>
    <a class="latest-plate reveal" href="{h(f['url'])}">
      <img src="assets/thumbs/{h(f['slug'])}.jpg" alt="{h(f['title'])}: live page" width="760" height="475" loading="lazy">
      <span class="mono plate-caption">Fig. 00 — captured live</span>
    </a>
  </div>
</section>
{''.join(sections)}

<section class="section" id="stats">
  <div class="asterism mono reveal" aria-hidden="true">✻&nbsp;&nbsp;✻&nbsp;&nbsp;✻</div>
  <div class="section-head reveal">
    <span class="mono section-no">§ 06</span>
    <h2>Receipts</h2>
    <p class="section-sub">Public activity, continuously updated.</p>
  </div>
  <div class="stats-cards reveal">
    <a href="https://stackoverflow.com/users/1031417/0x90" class="stat-embed">
      <img src="https://github-readme-stackoverflow.vercel.app/?userID=1031417&amp;layout=compact" alt="Stack Overflow profile of 0x90" width="495" height="195" loading="lazy">
      <span class="mono">Stack Overflow — 0x90</span>
    </a>
    <a href="https://github.com/zozo123" class="stat-embed">
      <img src="https://github-readme-streak-stats-six-orcin.vercel.app/?user=zozo123&amp;mode=weekly&amp;date_format=M%20j%5B%2C%20Y%5D" alt="GitHub weekly contribution streak for zozo123" width="495" height="195" loading="lazy">
      <span class="mono">GitHub streak — weekly</span>
    </a>
  </div>
</section>

</main>

<footer class="colophon">
  <div class="asterism mono" aria-hidden="true">✻&nbsp;&nbsp;✻&nbsp;&nbsp;✻</div>
  <p class="colophon-sign">Build → measure → <em>write it down.</em></p>
  <nav class="colophon-links mono" aria-label="Profiles">
    <a href="{HOME}">Professional site</a>
    <a href="https://github.com/zozo123">GitHub</a>
    <a href="https://www.linkedin.com/in/yossi-eliaz/">LinkedIn</a>
    <a href="https://scholar.google.com/citations?user=NL1ZyOgAAAAJ&amp;hl=en">Scholar</a>
    <a href="https://x.com/YossiEliaz">𝕏</a>
  </nav>
  <p class="mono colophon-note">Set in Fraunces, Spectral &amp; IBM Plex Mono · figures are live captures or share cards · © Yossi Eliaz</p>
</footer>

<script src="js/main.js"></script>
</body>
</html>
"""


def sitemap(data: dict) -> str:
    urls = [SITE] + [page_url(i) for i in data["selected"] if page_url(i).startswith(SITE)] + [data["featured"]["url"]]
    for item in (i for sec in data["sections"] for i in sec["items"]):
        urls += [page_url(item)] + item.get("alternates", [])
    seen, rows = set(), []
    for u in urls:
        if u.startswith(SITE) and u not in seen:
            seen.add(u)
            rows.append(f"<url><loc>{h(u)}</loc></url>")
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(rows) + "</urlset>\n"


def llms(data: dict) -> str:
    lines = [
        f"# {NAME}: Writing & experiments",
        "",
        f"> {NAME}: {TITLE.replace(' · ', ', ')}. Current work: AI execution infrastructure (agent sandboxes, CI runners, caching, build acceleration) as Principal Engineer, AI Systems at Incredibuild / islo.dev. Earlier work: computational genomics (3D genome, Hi-C, ENCODE pipelines, CRISPR), autonomous-driving perception at Mobileye, and physics (PhD, University of Houston). Senior Lecturer at HIT.",
        "",
        f"This site collects Yossi Eliaz's writing, field guides, and live experiments. Professional profile, CV, and publications: {HOME} (research index: {HOME}research/).",
        "",
        "## Selected work",
        "",
    ]
    lines += [f"- [{i['title']}]({page_url(i)}): {i['tldr']}" for i in data["selected"]]
    lines += ["", f"## Featured essay", "", f"- [{data['featured']['title']}]({data['featured']['url']}): {data['featured']['tldr']}"]
    for sec in data["sections"]:
        lines += ["", f"## {sec['toc']}", ""]
        lines += [f"- [{i['title']}]({page_url(i)}): {i['tldr']}" for i in sec["items"]]
    lines += ["", "## Profiles", ""] + [f"- {u}" for u in SAME_AS]
    return "\n".join(lines) + "\n"


def main() -> None:
    data = json.loads((ROOT / "data" / "works.json").read_text(encoding="utf-8"))
    (ROOT / "index.html").write_text(render(data), encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(sitemap(data), encoding="utf-8")
    (ROOT / "llms.txt").write_text(llms(data), encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n", encoding="utf-8")
    print("wrote index.html, sitemap.xml, llms.txt, robots.txt")


if __name__ == "__main__":
    main()
