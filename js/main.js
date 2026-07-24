/**
* Project A.C.T. — Shared JavaScript Utilities
* Consolidated shared code across all pages
*/

// ── REVEAL ANIMATION ──
function initReveal() {
    const revealEls = document.querySelectorAll('.reveal, .reveal-left, .reveal-scale, .reveal-delay-1, .reveal-delay-2, .reveal-delay-3');
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) entry.target.classList.add('active');
        });
    }, { threshold: 0.12, rootMargin: '0px 0px -30px 0px' });
    revealEls.forEach(el => revealObserver.observe(el));
}

// ── COUNTER ANIMATION ──
function runCounter(el, delay = 0) {
    setTimeout(() => {
        const target = parseFloat(el.getAttribute('data-target'));
        if (isNaN(target)) return;
        const duration = 2200;
        const interval = 16;
        const steps = duration / interval;
        let step = 0;
        const tick = setInterval(() => {
            step++;
            const progress = 1 - Math.pow(1 - step / steps, 4);
            const current = progress * target;
            if (Number.isInteger(target)) {
                el.textContent = Math.round(current).toLocaleString();
            } else {
                el.textContent = current.toFixed(1);
            }
            if (step >= steps) {
                el.textContent = target.toLocaleString();
                clearInterval(tick);
            }
        }, interval);
    }, delay);
}

function initHeroCounters(delay = 600) {
    document.querySelectorAll('.hero-kpi-num[data-target]').forEach(el => {
        runCounter(el, delay);
    });
}

function initOutcomeCounters() {
    const outcomeCounters = document.querySelectorAll('.counter[data-target]');
    const outcomeObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                runCounter(entry.target, 0);
                outcomeObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    outcomeCounters.forEach(el => outcomeObserver.observe(el));
}

// ── NAVIGATION TOGGLE (legacy - no longer needed with redesign hero nav) ──
function initNavToggle() {
    // Kept for backwards compatibility; the redesign uses inline hero nav
}

// ── SCROLL PROGRESS BAR ──
function initNavProgress() {
    const progressBar = document.getElementById('progress-bar');
    if (!progressBar) return;

    window.addEventListener('scroll', () => {
        const docH = document.documentElement.scrollHeight - window.innerHeight;
        const pct = docH > 0 ? (window.scrollY / docH) * 100 : 0;
        progressBar.style.width = pct + '%';
    }, { passive: true });
}

// ── SECTION TRACKER ──
function initSectionTracker() {
    const trackerDots = document.querySelectorAll('.tracker-dot');
    const sections = ['hero', 'philosophy', 'legacy', 'interventions', 'phase6', 'outcomes', 'archive', 'footer'];
    const sectionEls = sections.map(id => document.getElementById(id)).filter(Boolean);

    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.id;
                trackerDots.forEach(dot => dot.classList.remove('active'));
                const activeDot = document.querySelector(`.tracker-dot[data-section="${id}"]`);
                if (activeDot) activeDot.classList.add('active');
            }
        });
    }, { threshold: 0.3 });

    sectionEls.forEach(el => sectionObserver.observe(el));
}

// ── GALLERY TOGGLE ──
function toggleGallery() {
    const hidden = document.getElementById('galleryHidden');
    const btn = document.getElementById('galleryToggle');
    if (!hidden || !btn) return;
    hidden.classList.toggle('open');
    btn.classList.toggle('open');
    btn.innerHTML = hidden.classList.contains('open') ? 'Show Less <span>↑</span>' : 'Show More <span>↓</span>';
}

// ── BEFORE/AFTER SLIDER ──
function initSlider() {
    const slider = document.getElementById('slider');
    const after = document.getElementById('sliderAfter');
    const handle = document.getElementById('sliderHandle');
    if (!slider || !after || !handle) return;

    let dragging = false;

    const updateSlider = (clientX) => {
        const rect = slider.getBoundingClientRect();
        let x = clientX - rect.left;
        x = Math.max(0, Math.min(x, rect.width));
        const pct = (x / rect.width) * 100;
        after.style.width = pct + '%';
        handle.style.left = pct + '%';
    };

    handle.addEventListener('mousedown', (e) => {
        dragging = true;
        e.preventDefault();
    });
    window.addEventListener('mouseup', () => dragging = false);
    window.addEventListener('mousemove', (e) => {
        if (dragging) updateSlider(e.clientX);
    });

    handle.addEventListener('touchstart', (e) => {
        dragging = true;
    });
    window.addEventListener('touchend', () => dragging = false);
    window.addEventListener('touchmove', (e) => {
        if (dragging) updateSlider(e.touches[0].clientX);
    });
}

// ── STICKY NAV WITH FLIP ANIMATION ──
function initStickyNav() {
    var nav = document.querySelector('.hero__nav');
    if (!nav) return;

    var isStuck = false;
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var STICKY_THRESHOLD = 60;

    function checkSticky() {
        var shouldStick = window.scrollY >= STICKY_THRESHOLD;
        if (shouldStick && !isStuck) {
            isStuck = true;
            flipStick(nav, reduce);
        } else if (!shouldStick && isStuck) {
            isStuck = false;
            flipUnstick(nav, reduce);
        }
    }

    window.addEventListener('scroll', checkSticky, { passive: true });
    checkSticky();
}

function flipStick(nav, reduce) {
    // Capture "first" rect (before class change)
    var first = nav.getBoundingClientRect();

    // Apply the stuck class (sets CSS transform: translateX(-50%))
    nav.classList.add('is-stuck');

    if (reduce) return; // skip animation for reduced motion

    // Capture "last" rect (after class change)
    var last = nav.getBoundingClientRect();

    // Calculate translate deltas only — the scale/shrink into the pill
    // shape is handled by the CSS transition on background/padding
    var dx = first.left - last.left;
    var dy = first.top - last.top;

    // Invert: lock visual position to where it was before class change
    nav.style.transition = 'none';
    nav.style.transform = 'translate(' + dx + 'px, ' + dy + 'px)';
    void nav.offsetWidth;

    // Animate from inverted position to the CSS transform (translateX(-50%))
    nav.style.transition = 'transform 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
    nav.style.transform = '';

    // Clean up inline transition after animation completes
    setTimeout(function () {
        nav.style.transition = '';
    }, 700);
}

function flipUnstick(nav, reduce) {
    // Capture "first" rect (while still stuck with CSS translateX(-50%))
    var first = nav.getBoundingClientRect();

    // Remove stuck class — nav snaps to original absolute position
    nav.classList.remove('is-stuck');

    if (reduce) return; // skip animation for reduced motion

    // Capture "last" rect (now in original position, no transform)
    var last = nav.getBoundingClientRect();

    // Invert: hold visual position where it was before class removal
    var dx = first.left - last.left;
    var dy = first.top - last.top;
    nav.style.transition = 'none';
    nav.style.transform = 'translate(' + dx + 'px, ' + dy + 'px)';
    void nav.offsetWidth;

    // Animate back to original (no transform at all)
    nav.style.transition = 'transform 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
    nav.style.transform = '';

    setTimeout(function () {
        nav.style.transition = '';
    }, 700);
}

// ── REDUCED MOTION HANDLING ──
function handleReducedMotion() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        document.querySelectorAll('.ghost-text span').forEach(s => s.style.animation = 'none');
        document.querySelectorAll('.pill-a.exit, .pill-b.enter, .pill-b.exit, .pill-a.enter').forEach(el => {
            el.style.transition = 'transform 0.01s';
        });
        const tickerTrack = document.querySelector('.ticker-track');
        if (tickerTrack) tickerTrack.style.animation = 'none';
    }
}

// ── DRAMATIC PAGE INTRO ──
function initPageIntro() {
    const intro = document.getElementById('page-intro');
    const logo = document.getElementById('introLogo');
    const textLine = document.getElementById('introTextLine');
    const words = document.querySelectorAll('.intro-word');
    const flare = document.getElementById('introFlare');
    const logotype = document.querySelector('.intro-logotype');

    if (!intro || !logo) return;

    // Skip intro if reduced motion
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        intro.style.display = 'none';
        document.body.style.overflow = '';
        return;
    }

    // Lock scroll during intro
    document.body.style.overflow = 'hidden';

    // Sequence timeline
    const tl = {
        logoIn: 200,        // Start logo animation
        logotypeIn: 500,    // Start "A.C.T." text fade-in
        flareIn: 400,       // Start flare sweep
        textIn: 1200,       // Start text words appearing
        hold: 2800,         // Hold full view
        fadeOut: 3800,      // Start fade out
        complete: 4600      // Remove overlay
    };

    // Step 1: Logo scales in dramatically
    setTimeout(() => {
        logo.classList.add('animate-in');
    }, tl.logoIn);

    // Step 2: "A.C.T." logotype fades in below logo
    setTimeout(() => {
        if (logotype) logotype.classList.add('animate-in');
    }, tl.logotypeIn);

    // Step 3: Light flare sweeps across
    setTimeout(() => {
        flare.classList.add('animate-in');
    }, tl.flareIn);

    // Step 4: Words appear staggered (vertical: Action / Changes / Things.)
    setTimeout(() => {
        textLine.classList.add('animate-in');
        words.forEach((word, i) => {
            const delay = parseFloat(word.dataset.delay) || 0;
            setTimeout(() => {
                word.classList.add('animate-in');
            }, delay * 1000);
        });
    }, tl.textIn);

    // Step 5: Fade out the entire overlay
    setTimeout(() => {
        intro.classList.add('fade-out');
    }, tl.fadeOut);

    // Step 6: Remove overlay, unlock scroll, trigger page animations
    setTimeout(() => {
        intro.classList.add('hidden');
        document.body.style.overflow = '';

        // Now trigger all page animations
        initReveal();
        initHeroCounters(800);
        initOutcomeCounters();
        initNavToggle();
        initNavProgress();
        initSectionTracker();
        initStickyNav();
        initSlider();
        handleReducedMotion();
    }, tl.complete);
}

// ── INIT ALL SHARED COMPONENTS ──
document.addEventListener('DOMContentLoaded', () => {
    // Start the dramatic intro first
    initPageIntro();
});

// ── EXPORT FOR PAGE-SPECIFIC USE ──
window.ACT = {
    toggleGallery,
    runCounter,
    initReveal
};