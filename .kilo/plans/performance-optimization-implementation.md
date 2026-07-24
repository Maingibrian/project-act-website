# Performance Optimization Implementation Plan

## Objective
Improve page load speed while keeping the current design intact. Focus on compression, lazy loading, caching, and asset optimization.

## Baseline
- Homepage critical transfer: ~4.94 MB
- Total site assets: 217 MB (100 files)
- Hero video: 133 MB (Video 1.mp4)
- Largest image: act-logo.png (1.9 MB)
- CSS: 11 of 12 files unminified

## Tasks & Agents

### Wave 1: Asset Optimization (parallel)
1. **Video Optimization Agent**: Compress/replace Video 1.mp4 with optimized version, update index.html references
2. **Image Optimization Agent**: Compress all JPEGs/PNGs, optimize act-logo.png, add srcset where beneficial
3. **CSS Minification Agent**: Minify all 11 unminified CSS files using clean-css or csso
4. **Cache Headers Agent**: Add _headers file with cache-control for static assets

### Wave 2: Code Optimizations (parallel, after Wave 1)
5. **Lazy Loading Agent**: Add loading="lazy" to below-fold images across all HTML pages
6. **Font Loading Agent**: Ensure all pages use preload+onload trick for Google Fonts

### Wave 3: Validation (after Wave 2)
7. **Measurement Agent**: Run Playwright scripts to verify load time improvements

## Expected Improvements
- Hero video: 133 MB → < 10 MB (or lazy-loaded)
- act-logo.png: 1.9 MB → < 50 KB
- All images: avg 40-60% size reduction
- CSS: ~30-40% size reduction via minification
- Cache hits: 100% on repeat visits

## Rollback
- Keep originals in Images/originals/ and css/originals/ before overwriting
