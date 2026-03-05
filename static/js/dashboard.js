/**
 * ═══════════════════════════════════════
 * AutoKlik – dashboard.js
 * Logique pour l'interface d'administration
 * ═══════════════════════════════════════
 */

document.addEventListener('DOMContentLoaded', () => {

    // ── 1. SIDEBAR MOBILE ─────────────────────────────
    const btnToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');

    if (btnToggle && sidebar && overlay) {
        btnToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
            overlay.classList.toggle('hidden');
        });

        overlay.addEventListener('click', () => {
            sidebar.classList.remove('open');
            overlay.classList.add('hidden');
        });
    }


    // ── 2. TOASTS DISMISSAL ───────────────────────────
    document.querySelectorAll('.dash-toast').forEach(toast => {
        const closeBtn = toast.querySelector('.toast-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                toast.style.opacity = '0';
                toast.style.transform = 'translateY(-10px)';
                setTimeout(() => toast.remove(), 300);
            });
        }

        // Auto-dismiss après 5 secondes
        setTimeout(() => {
            if (toast.parentElement) {
                toast.style.opacity = '0';
                toast.style.transform = 'translateY(-10px)';
                setTimeout(() => toast.remove(), 300);
            }
        }, 5000);
    });


    // ── 3. ACTIVE NAV LINKS ───────────────────────────
    const currentPath = window.location.pathname;
    document.querySelectorAll('.dash-nav-link').forEach(link => {
        const linkPath = link.getAttribute('data-url');
        if (linkPath && currentPath === linkPath) {
            link.classList.add('is-active');
        }
    });


    // ── 4. HTMX EVENTS (Feedback visuel) ─────────────
    document.body.addEventListener('htmx:beforeRequest', (evt) => {
        const target = evt.detail.elt;
        if (target.tagName === 'BUTTON') {
            target.classList.add('opacity-50', 'pointer-events-none');
        }
    });

    document.body.addEventListener('htmx:afterRequest', (evt) => {
        const target = evt.detail.elt;
        if (target.tagName === 'BUTTON') {
            target.classList.remove('opacity-50', 'pointer-events-none');
        }
    });

});
