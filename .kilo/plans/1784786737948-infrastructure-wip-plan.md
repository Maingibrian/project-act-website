# Plan: Create infrastructure-wip.html Placeholder Page

## Goal
Create a new standalone placeholder page at `infrastructure-wip.html` that previews the two upcoming infrastructure items (repurposed bins and jikos) using the site's existing dark-navy aesthetic. It serves as a temporary stand-in until the permanent infrastructure replacement page is ready.

## Scope
- New HTML: `infrastructure-wip.html` (separate file, new URL)
- New CSS: `css/infrastructure-wip.css`
- Do NOT touch existing `infrastructure.html`, its CSS, or nav links on other pages

---

## Page Sections (top to bottom)

### 1. Head
Copy the head pattern from `infrastructure.html` exactly:
- Same meta tags, favicon, font preloads
- Title: `Project A.C.T. — Infrastructure (Work in Progress)`
- Stylesheet: `css/infrastructure-wip.css`
- Deferred `js/main.js`

### 2. Navigation (`site-nav`)
Same fixed top-bar pattern as non-index pages. Link text and active state:
- Home (`index.html`)
- Reports Archive (`archive.html`)  
- **Infrastructure WIP** (`infrastructure-wip.html`) ← active

### 3. Hero Section
Class: `hero` (same grid structure as infrastructure)
- `hero-ghost` text: `BUILD`
- Left column:
  - Eyebrow: `★ Work in Progress`
  - Title: `Infrastructure<br><em>Coming Soon</em>`
  - Desc paragraph: Acknowledge this is a transitional placeholder while the full infrastructure page is being rebuilt.
  - No KPI row (keep hero clean)
- Right column:
  - Show a single abstract/capsule element (reuse `.capsule-container` styling from infrastructure)

### 4. Preview: What's Coming Section
Class: `section-origins` style
- Eyebrow: `What's Being Built`
- Title: `Two Pillars.<br><em>Zero Waste.</em>`
- Brief 1-2 sentence intro about the upcoming content

### 5. Two-Item Teaser Grid (the core content)
A centered 2-column grid (`.origins-grid` style), each column a card:

**Left card — Repurposed Bins**
- Eyebrow: `Upcycled Bins`
- Description: Bin units salvaged from factory floors, welded and sanitized in-house, anchor-bolted at coastal access points.
- Mock KPI strip (3 items): e.g. `20+` Units, `0` Capital Cost, `100%` Upcycled

**Right card — Jikos**
- Eyebrow: `Gas Cylinder Jikos`
- Description: Traditional cooking stoves crafted from empty long gas cylinders — giving industrial waste a second life in community kitchens.
- Mock KPI strip (3 items): e.g. `—` Units, `—` Capital Cost, `In Development`

Cards should match the existing `.kpi-row` / bordered card style.

### 6. "Full Page Coming" CTA Band
A simple centered callout between the cards and footer:
- Text: "The full Infrastructure page with deployment details, material specs, and community impact data is under construction."
- Small red accent

### 7. Footer
Reuse the exact `site-footer` markup and styling from `infrastructure.html`.

---

## CSS (`css/infrastructure-wip.css`)

1. Copy the full reset/token/animation/nav/footer boilerplate from `css/infrastructure.css`.
2. Keep the same `:root` custom properties (navy, red, glass, etc.).
3. Keep the same `.reveal`, `.reveal-left`, `.delay-1/2/3` animation classes.
4. Keep the same `site-nav`, `site-footer`, `hero-ghost`, `hero-left`, `hero-right`, `capsule-container` styles.
5. Add minor page-specific overrides:
   - Hero title size slightly smaller if needed for the longer "Coming Soon" line
   - `.wip-cards` grid (2 columns, gap 40px, max-width 1100px)
   - `.wip-card` styling: bordered glass card with internal padding
   - `.wip-card-eyebrow`, `.wip-card-title`, `.wip-card-desc`
   - `.wip-card-kpis` (same `.kpi-row` pattern reused)

No new animations or visual effects beyond what already exists in `infrastructure.css`.

---

## JavaScript
Same inline script block from `infrastructure.html`:
- Nav scroll class toggling + progress indicator
- Hero ghost parallax
- IntersectionObserver reveal + counter animation
- Reduced-motion preference handling

No new JS required.

---

## Validation Steps
1. Open `infrastructure-wip.html` locally; confirm page loads without 404s for CSS/JS/images.
2. Confirm nav shows "Infrastructure WIP" as active link.
3. Confirm hero, teaser cards, and footer render correctly at desktop width.
4. Resize to 768px and confirm grid collapses to single column, nav hides `.nav-sub`, cards stack.
5. Scroll and confirm `.reveal` animations trigger and counters animate.

---

## Out of Scope
- Adding a nav link to `infrastructure-wip.html` from the live `infrastructure.html` nav (left for follow-up).
- Populating real images or content (this is intentionally a preview).
- Any changes to existing pages, CSS, or nav components.
