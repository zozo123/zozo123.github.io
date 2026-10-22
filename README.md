# Yossi Eliaz — Writing & experiments

Notes, measurements, and experiments from building difficult systems: AI agent sandboxes, CI,
genomics, and physics.

- Live writing site: https://zozo123.github.io/
- Professional profile and CV: https://yossieliaz.netlify.app/

This is a static site with no build step: `index.html`, `css/`, `js/`, and `assets/`.
The selected work and reading links are plain HTML and work without JavaScript. The expandable
archive is generated from `FIGSETS` in `js/main.js`; edit that data to add or reorder posts.
Typography: Fraunces, Spectral, and IBM Plex Mono. The share card is `assets/og/card.svg`, rendered
to `card.png` at 1200×630 (`rsvg-convert -w 1200 -h 630 assets/og/card.svg -o assets/og/card.png`).

## Preview

```bash
python3 -m http.server 8417
# open http://localhost:8417/
```

## Validate

```bash
npx --yes html-validate@11.6.0 index.html
node --check js/main.js
```

## Deploy

GitHub Pages publishes the root of the `master` branch. The separate Netlify professional site
is built from a private repository.

## Wasted Cycles Installer

The extensionless [`cycles`](cycles) endpoint provides the memorable, GitHub-native run path:

```bash
curl -fsSL https://zozo123.github.io/cycles | sh
```

It downloads the matching release archive, verifies it against the published SHA-256
manifest, extracts it in an unpredictable temporary directory, and removes it on exit.
Pin a production install by passing the version to the receiving shell:

```bash
curl -fsSL https://zozo123.github.io/cycles |
  WASTED_CYCLES_VERSION=v0.6.1 sh
```

The earlier [`wasted`](wasted) and [`w`](w) paths remain compatibility aliases.

## Refresh thumbnails

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --hide-scrollbars --window-size=1280,800 --timeout=15000 \
  --screenshot=shot.png "https://zozo123.github.io/<repo>/"
sips -s format jpeg -s formatOptions 72 --resampleWidth 760 shot.png \
  --out assets/thumbs/<repo>.jpg
```
