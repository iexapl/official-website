// AXLTeco Website - Shared Scripts
document.addEventListener('DOMContentLoaded', function() {
  // Mobile menu toggle
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.querySelector('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function(e) {
      e.stopPropagation();
      var isOpen = nav.classList.contains('show');
      if (isOpen) {
        nav.classList.remove('show');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.textContent = '☰';
      } else {
        nav.classList.add('show');
        toggle.setAttribute('aria-expanded', 'true');
        toggle.textContent = '✕';
      }
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
      if (nav.classList.contains('show') && !nav.contains(e.target) && !toggle.contains(e.target)) {
        nav.classList.remove('show');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.textContent = '☰';
        // Also close any open dropdowns
        document.querySelectorAll('.nav-dropdown.open').forEach(function(dd) {
          dd.classList.remove('open');
        });
      }
    });
  }

  // Mobile dropdown toggle (click instead of hover)
  var dropdowns = document.querySelectorAll('.nav-dropdown');
  dropdowns.forEach(function(dd) {
    var trigger = dd.querySelector(':scope > a');
    if (trigger) {
      trigger.addEventListener('click', function(e) {
        // Only handle click on mobile (< 900px)
        if (window.innerWidth <= 900) {
          e.preventDefault();
          e.stopPropagation();
          var isOpen = dd.classList.contains('open');
          // Close sibling dropdowns
          dropdowns.forEach(function(other) {
            if (other !== dd) other.classList.remove('open');
          });
          dd.classList.toggle('open', !isOpen);
        }
      });
    }
  });

  // Set active nav link
  var current = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav a').forEach(function(a) {
    if (a.getAttribute('href') === current) {
      a.classList.add('active');
    }
  });

  // Back to top button
  var backToTop = document.createElement('button');
  backToTop.className = 'back-to-top';
  backToTop.setAttribute('aria-label', '返回顶部');
  backToTop.innerHTML = '↑';
  document.body.appendChild(backToTop);

  var scrollThreshold = 300;
  function updateBackToTop() {
    if (window.scrollY > scrollThreshold) {
      backToTop.classList.add('show');
    } else {
      backToTop.classList.remove('show');
    }
  }
  window.addEventListener('scroll', updateBackToTop, { passive: true });
  updateBackToTop();

  backToTop.addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // Scroll-triggered entrance animations
  var animatedSections = document.querySelectorAll('.section, .page-content');
  animatedSections.forEach(function(sec) {
    sec.classList.add('section-animate');
  });

  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

  animatedSections.forEach(function(sec) {
    observer.observe(sec);
  });

  // Form button ripple-like feedback (handled via CSS :active)
  // Add touch feedback for cards on mobile
  document.querySelectorAll('.card, .contact-card, .feature-item').forEach(function(el) {
    el.addEventListener('touchstart', function() {}, { passive: true });
  });
});
