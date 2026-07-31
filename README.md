# yossi eliaz — a living preprint

Personal website for [Yossi Eliaz](https://github.com/zozo123), carrying the full content of the
GitHub profile README — every live essay, demo, stat and planner — styled as an annotated
scientific preprint.

- **Type**: static site, no build step (`index.html` + `css/` + `js/` + `assets/`)
- **Typography**: Fraunces · Spectral · IBM Plex Mono (Google Fonts)
- **Thumbnails**: real screenshots of each live GitHub Pages site, captured with headless Chrome
  (`assets/thumbs/*.jpg`, 760px wide, ~50KB each)
- **Cards data**: edit `js/main.js` (`FIGSETS`) to add or reorder posts

## Preview

```bash
python3 -m http.server 8417
# → http://localhost:8417/
```

## Deploy

Any static host works — GitHub Pages, Netlify (`yossieliaz.netlify.app`), Vercel. No config needed.

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
