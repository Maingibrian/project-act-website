/* ═════════════════════════════════════════════════════════════════════
   PROJECT A.C.T. — SHARED NAVIGATION BAR LOGIC (nav.js)
   Dropdown toggle & keyboard accessibility
   ═════════════════════════════════════════════════════════════════════ */

(function () {
    'use strict';

    function initNavDropdowns() {
        var dropdowns = document.querySelectorAll('.hero__nav-dropdown');

        dropdowns.forEach(function (dd) {
            var btn = dd.querySelector('.hero__nav-link');
            if (!btn) return;

            // Toggle on click
            btn.addEventListener('click', function (e) {
                e.stopPropagation();
                var isOpen = dd.classList.contains('is-open');

                // Close any other open dropdowns
                dropdowns.forEach(function (other) {
                    other.classList.remove('is-open');
                    var otherBtn = other.querySelector('.hero__nav-link');
                    if (otherBtn) otherBtn.setAttribute('aria-expanded', 'false');
                });

                if (!isOpen) {
                    dd.classList.add('is-open');
                    btn.setAttribute('aria-expanded', 'true');
                }
            });
        });

        // Close on outside click
        document.addEventListener('click', function () {
            dropdowns.forEach(function (dd) {
                dd.classList.remove('is-open');
                var btn = dd.querySelector('.hero__nav-link');
                if (btn) btn.setAttribute('aria-expanded', 'false');
            });
        });

        // Close on Escape key
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                dropdowns.forEach(function (dd) {
                    dd.classList.remove('is-open');
                    var btn = dd.querySelector('.hero__nav-link');
                    if (btn) btn.setAttribute('aria-expanded', 'false');
                });
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initNavDropdowns);
    } else {
        initNavDropdowns();
    }
})();
