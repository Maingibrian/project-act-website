# Website Performance Optimization Plan

## Baseline Measurements

| Metric | Value |
|--------|-------|
| Total site assets | 217 MB (100 files) |
| Hero background videos | 133 MB (Video 1.mp4) + 60 MB (Video 2.mp4) |
| CSS (unminified) | 486 KB across 12 files |
| JS (unminified) | 12 KB (main.js) |
| Homepage critical transfer | 4.94 MB |
| Local load event time | ~1.5s |
| Homepage resource count | 16 requests |

### Estimated Real-World Load Times

| Connection | Critical Path | Video Load | Total |
|------------|---------------|------------|-------|
| Fast broadband (10 Mbps) | ~4s | ~106s | ~110s |
| 4G (5 Mbps) | ~8s | ~213s | ~221s (~3.7 min) |
| 3G (1 Mbps) | ~40s | ~1066s | ~1106s (~18 min) |

The hero video (`Video 1.mp4`, 133 MB, `preload="auto"`) dominates load time. The browser only loads the first supported `<source>`, so Video 2 is unused but still shipped.

## Root Causes

1. **Uncompressed video**: 133 MB hero background with no bitrate reduction, resolution scaling, or modern codec (WebM/AV1).
2. **Unminified CSS**: 11 of 12 CSS files are raw source; only `index.min.css` is minified.
3. **Unoptimized images**: `act-logo.png` is 1.9 MB; all images are raw JPEG/PNG with no compression or modern formats (WebP/AVIF).
4. **No responsive images**: No `srcset`/`sizes` for different viewport densities.
5. **No caching policy**: `netlify.toml` has no cache-control headers for static assets.
6. **Unused assets shipped**: Video 2.mp4 is referenced but never played; many images may be below-fold but load eagerly.

## Optimization Tasks

### 1. Hero Video Optimization (Highest Impact)
- Replace `Video 1.mp4` with a compressed, lower-resolution version (target < 5 MB) or use a lightweight WebM/AV1 variant.
- Reduce resolution to 720p or lower; target bitrate ~1-2 Mbps.
- Add `poster` attribute with an optimized static image as fallback.
- Consider removing `preload="auto"` and using `preload="metadata"` or lazy-loading the video until user interaction.
- Remove `Video 2.mp4` entirely or replace with a single optimized source.

### 2. Image Optimization (High Impact)
- Convert `act-logo.png` to SVG or compress to < 50 KB.
- Run all JPEGs through compression (mozjpeg/oxipng) targeting < 200 KB for above-fold, < 100 KB for gallery images.
- Convert key images to WebP/AVIF with JPEG fallbacks.
- Add `srcset` + `sizes` for hero and intervention images.
- Implement native lazy loading (`loading="lazy"`) for below-fold images.

### 3. CSS Minification & Consolidation (Medium Impact)
- Minify all 11 unminified CSS files (archive, contact, copacabana, donate, eye-camp, green-olive, infrastructure, kuruitu, vipingo, world-environment-day).
- Consider extracting shared nav/footer into a single shared CSS file to reduce per-page CSS.
- Target total CSS bundle < 150 KB.

### 4. JS Minification (Low Impact)
- Minify `js/main.js` to `main.min.js`.
- Defer non-critical JS; `main.js` already uses `defer`.

### 5. Font Loading (Low Impact)
- Ensure all pages use `preload` + `onload` trick (currently only `index.html` does this).
- Consider subsetting fonts or using `font-display: swap` (already set via Google Fonts URL).

### 6. Netlify Caching Headers (Low Impact, High Leverage)
- Add `_headers` file or `netlify.toml` rules to cache static assets (CSS, JS, images, fonts) for 1 year with content-hash filenames.
- Enable Brotli/Gzip compression (Netlify does this automatically for text assets).

## Expected Improvements

| Metric | Before | After Target |
|--------|--------|--------------|
| Total hero video size | 133 MB | < 10 MB |
| Homepage critical transfer | 4.94 MB | < 2 MB |
| Local load event | 1.5s | < 0.8s |
| 4G total load | ~221s | < 10s |
| 3G total load | ~1106s | < 20s |

## Validation Steps

1. Run local measurement script (`measure_cdp.py`) before and after each change.
2. Use Lighthouse CI or `npx lighthouse` on local server for audits.
3. Verify on Netlify deploy preview before production push.
4. Check that mobile redirect (`index.mobile.html`) still functions after changes.
5. Confirm no broken image/video references across all 13 HTML pages.

## Open Questions

- Should the hero video be replaced entirely with a static image for maximum performance? (Recommended: yes, or offer a lightweight video variant.)
- Are there specific images that must remain high-resolution for print/archive purposes? If so, move them off the critical path.
- Do you want me to implement these optimizations now, or refine the plan first?
