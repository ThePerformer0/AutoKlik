/**
 * AutoKlik – main.js
 */
(function () {
  'use strict';

  // ── Navbar scroll shadow ─────────────────────────────
  var header = document.getElementById('site-header');
  if (header) {
    window.addEventListener('scroll', function () {
      header.classList.toggle('scrolled', window.scrollY > 40);
    }, { passive: true });
  }

  // ── Active nav link (match current URL) ──────────────
  var currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(function (link) {
    if (link.getAttribute('data-url') === currentPath) {
      link.classList.add('is-active');
      link.classList.remove('text-white/55');
      link.classList.add('text-white');
    }
  });

  // ── Mobile burger menu ────────────────────────────────
  var burgerBtn  = document.getElementById('burger-btn');
  var burgerIcon = document.getElementById('burger-icon');
  var mobileMenu = document.getElementById('mobile-menu');

  if (burgerBtn && mobileMenu) {
    burgerBtn.addEventListener('click', function () {
      var isOpen = !mobileMenu.classList.contains('hidden');
      mobileMenu.classList.toggle('hidden', isOpen);

      if (burgerIcon) {
        burgerIcon.classList.toggle('fa-bars',  isOpen);
        burgerIcon.classList.toggle('fa-xmark', !isOpen);
      }
    });

    // Close on outside click
    document.addEventListener('click', function (e) {
      if (!burgerBtn.contains(e.target) && !mobileMenu.contains(e.target)) {
        mobileMenu.classList.add('hidden');
        if (burgerIcon) {
          burgerIcon.classList.add('fa-bars');
          burgerIcon.classList.remove('fa-xmark');
        }
      }
    });
  }

  // ── Toast auto-dismiss ────────────────────────────────
  document.querySelectorAll('.toast').forEach(function (toast) {
    // Close button
    var closeBtn = toast.querySelector('.toast-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', function () {
        dismissToast(toast);
      });
    }
    // Auto after 5s
    setTimeout(function () { dismissToast(toast); }, 5000);
  });

  function dismissToast(el) {
    el.style.transition = 'opacity .35s ease, transform .35s ease';
    el.style.opacity    = '0';
    el.style.transform  = 'translateX(12px)';
    setTimeout(function () { el.remove(); }, 360);
  }

})();