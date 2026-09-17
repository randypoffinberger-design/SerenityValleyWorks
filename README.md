# Serenity Valley Works public website

Static HTML, CSS, and small progressive-enhancement scripts, served by GitHub Pages. No build step or package dependencies.

## Local preview and checks

```text
python -m http.server 8765 --bind 127.0.0.1
python -m unittest discover -s tests
node --check morethanmeasured/mtm.js
```

Open `http://127.0.0.1:8765/`. Review desktop and narrow mobile layouts before merging a pull request into `main`.

MTM has a standalone warm theme in `morethanmeasured/mtm-theme.css`. Its navigation and all guide content work without JavaScript; `mtm.js` adds the mobile menu, resource filters, and printing. `home-mtm.css` only styles the MTM entry on the SVW homepage. Kitchen continues using the existing shared styles.

## App links and disclosures

The shopping and resource links were copied from `randypoffinberger-design/Free-to-be-me` at commit `a517516b9425693510830a7c9763e916fd8760e1`, principally the sensory, sleep, communication, outings, skill-building, and potty sections of `app.js`. The MTM icon also comes from that app's `assets/icons/icon-512.png`.

Current state: **not an affiliate**. Do not add affiliate tags or the present-tense Amazon Associate identification until participation is established. If that changes, review current Amazon requirements, add the required site identification, label relevant paid links beside each link, and update the privacy policy. Do not copy retailer images, prices, ratings, or reviews into the site without a verified authorized source. Keep manufacturer and assistance links distinguished from shopping recommendations.

## Enable a download at launch

Both app landing pages contain a `section[data-app-downloads]` with `hidden`. Inside are separate Apple, Google Play, and Windows controls identified by `data-store`. They intentionally have no `href` and remain outside the visible UI and accessibility tree. Their styling is in `store-downloads.css`.

For a release:

1. Set the relevant control's `href` to the verified official store page or Windows distribution URL. Confirm the app, publisher, platform, and Windows installer/signing details.
2. Remove `aria-disabled` from that control. Keep unavailable platform controls individually `hidden`.
3. Remove `hidden` from the section only when at least one download is ready. Update the app's in-development copy to match actual availability.
4. Update the pre-launch test expectations and test links and mobile layout before merging.

Never use placeholder store URLs or publish an unfinished installer.

## Share previews

Every page has static canonical, Open Graph, Twitter, favicon, and touch-icon metadata. MTM uses its own app icon; Kitchen uses `assets/sk-icon.png`; SVW uses its existing logo. Both directory and `index.html` entry URLs receive the same canonical identity. Metadata must remain in HTML so crawlers can read it without JavaScript.

Social platforms may cache an old preview. After publishing, verify the public HTML and use the platform's share debugger/refresh tool if an old SVW image persists. A local preview cannot refresh third-party share caches.
