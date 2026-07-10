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

// ── NAVIGATION TOGGLE ──
function initNavToggle() {
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');
    if (!navToggle || !navLinks) return;

    navToggle.addEventListener('click', () => {
        navToggle.classList.toggle('open');
        navLinks.classList.toggle('open');
    });

    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            navToggle.classList.remove('open');
            navLinks.classList.remove('open');
        });
    });
}

// ── NAVIGATION PROGRESS BAR ──
function initNavProgress() {
    const nav = document.getElementById('siteNav');
    const navIndicator = document.getElementById('navProgressIndicator');
    const progressBar = document.getElementById('progress-bar');
    if (!nav || !progressBar) return;

    window.addEventListener('scroll', () => {
        nav.classList.toggle('scrolled', window.scrollY > 40);
        const docH = document.documentElement.scrollHeight - window.innerHeight;
        const pct = docH > 0 ? (window.scrollY / docH) * 100 : 0;
        progressBar.style.width = pct + '%';
        if (navIndicator) navIndicator.style.width = pct + '%';
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

// ── INIT ALL SHARED COMPONENTS ──
document.addEventListener('DOMContentLoaded', () => {
    initReveal();
    initHeroCounters();
    initOutcomeCounters();
    initNavToggle();
    initNavProgress();
    initSectionTracker();
    initSlider();
    handleReducedMotion();
});

// ── EXPORT FOR PAGE-SPECIFIC USE ──
window.ACT = {
    toggleGallery,
    runCounter,
    initReveal
};