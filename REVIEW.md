# MTM public website review

Base: `main` at `f42bfb6a45c4f7306f705b0c7002060ca19340e2`.

## Behavior

- MTM uses a warm cream/green palette, its existing watercolor artwork and actual app icon, consistent navigation, active-page indication, footer, and accessible mobile menu.
- The homepage leads into three practical topic groups. All ten existing articles keep their original substantive guidance and add readable layouts, breadcrumbs, section navigation, category links, and related guides.
- Resources supports combined text/topic filtering, a result count, an empty state/reset, and an external-resource directory sourced from the MTM app.
- Products carries six existing retailer/collection links, four existing safety-bed manufacturer links, the app's existing general Amazon skill-building search, and the FDA safety source. There are no invented products, prices, ratings, affiliate tags, or retailer images.
- The external-resource directory adds 20 links from the app. The source repository and exact commit are recorded in the README.
- Affiliate wording now correctly says SVW is not currently an affiliate. No present-tense Amazon Associate claim remains.
- MTM and Serenity Kitchen have their own static sharing images, titles, icons, and canonical URLs. Parent-site pages keep SVW branding.
- Both app landing pages include hidden, inactive App Store, Google Play, and Windows controls with no placeholder URLs. Launch instructions are in the README.
- Shared `styles.css` and `script.js` are unchanged. The visible Kitchen HTML was compared against main and is unchanged. SVW gains a scoped MTM resource entry and navigation link.

## Validation

- Five automated test groups pass: local links/assets/fragments and unique IDs; per-brand sharing metadata; MTM headings/static content; hidden store controls; no affiliate claims/tags.
- JavaScript syntax check passes.
- All 14 MTM pages checked in the browser at 390px and 1280px widths: no horizontal overflow or missing images.
- MTM landing, Resources, Products, Support, SVW homepage, and Kitchen landing checked at 320px: no horizontal overflow.
- Mobile menu opening, Escape dismissal/focus return, and link navigation verified.
- Topic filtering, combined search, no-match feedback, and reset verified (10 → 3 → 1 → 0 → 10 results).
- Article section navigation verified against the target anchor.
- Browser fallback with script tags removed: navigation and all ten guides remain available; inactive search controls stay hidden.
- Hidden download controls remain invisible for both apps; no store placeholders appear in the accessibility tree.
- Desktop/mobile screenshots reviewed, including MTM landing, article, resources, products, and unchanged Kitchen presentation.

## Review limits

Third-party destinations are copied from the app, not certified for availability or suitability. Spot checks confirmed Comfrt, the projector and WIBACKER listings, and the FDA source. The web reader could not retrieve the two PatPat listings; their exact app URLs are retained without claims about current stock, price, or seller details. The directory deliberately points to current provider information instead of asserting changing eligibility rules or benefits.

Social preview metadata is validated locally. Existing Facebook/message previews may stay cached until the new HTML is deployed and the sharing service refreshes it. No live cache refresh or main-branch deployment is implied by these local checks.
