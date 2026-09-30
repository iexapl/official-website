// AXLTeco Website - Shared Scripts
const FORMSPREE_ENDPOINT = 'https://formspree.io/f/YOUR_FORM_ID';

document.addEventListener('DOMContentLoaded', function() {
  // Initialize Lucide icons
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }

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
      } else {
        nav.classList.add('show');
        toggle.setAttribute('aria-expanded', 'true');
      }
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
      if (nav.classList.contains('show') && !nav.contains(e.target) && !toggle.contains(e.target)) {
        nav.classList.remove('show');
        toggle.setAttribute('aria-expanded', 'false');
        document.querySelectorAll('.nav-dropdown.open').forEach(function(dd) {
          dd.classList.remove('open');
        });
      }
    });
  }

  // Mobile dropdown toggle
  var dropdowns = document.querySelectorAll('.nav-dropdown');
  dropdowns.forEach(function(dd) {
    var trigger = dd.querySelector(':scope > a');
    if (trigger) {
      trigger.addEventListener('click', function(e) {
        if (window.innerWidth <= 900) {
          e.preventDefault();
          e.stopPropagation();
          var isOpen = dd.classList.contains('open');
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
  backToTop.setAttribute('aria-label', 'Back to top');
  backToTop.innerHTML = '<i data-lucide="chevron-up"></i>';
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

  // Touch feedback for cards
  document.querySelectorAll('.card, .contact-card, .feature-item').forEach(function(el) {
    el.addEventListener('touchstart', function() {}, { passive: true });
  });

  // Contact form handling
  var contactForm = document.getElementById('contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', async function(e) {
      e.preventDefault();
      var submitBtn = contactForm.querySelector('button[type="submit"]');
      var originalText = submitBtn ? submitBtn.textContent : 'Submit';
      var alertBox = document.getElementById('form-alert');
      var messageField = contactForm.querySelector('textarea[name="message"]');

      // Minimum length check (anti-spam)
      if (messageField && messageField.value.trim().length < 20) {
        if (alertBox) {
          alertBox.className = 'form-alert error';
          alertBox.textContent = window._formLang && window._formLang.msgTooShort || 'Message must be at least 20 characters.';
          alertBox.style.display = 'block';
        }
        return;
      }

      // Honey pot check
      var gotcha = contactForm.querySelector('input[name="_gotcha"]');
      if (gotcha && gotcha.value) {
        return; // Bot detected
      }

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = window._formLang && window._formLang.sending || 'Sending...';
      }

      try {
        var formData = new FormData(contactForm);
        var res = await fetch(FORMSPREE_ENDPOINT, {
          method: 'POST',
          body: formData,
          headers: { 'Accept': 'application/json' }
        });

        if (res.ok) {
          if (alertBox) {
            alertBox.className = 'form-alert success';
            alertBox.textContent = window._formLang && window._formLang.success || 'Thank you! We will reply within 24 hours.';
            alertBox.style.display = 'block';
          }
          contactForm.reset();
          if (submitBtn) {
            submitBtn.textContent = window._formLang && window._formLang.sent || 'Sent!';
            submitBtn.style.background = '#22c55e';
            setTimeout(function() {
              submitBtn.textContent = originalText;
              submitBtn.style.background = '';
              submitBtn.disabled = false;
            }, 3000);
          }
          setTimeout(function() {
            if (alertBox) alertBox.style.display = 'none';
          }, 8000);
        } else {
          throw new Error('Formspree error');
        }
      } catch (err) {
        if (alertBox) {
          alertBox.className = 'form-alert error';
          alertBox.textContent = (window._formLang && window._formLang.error || 'Submission failed. Please try again or contact us via WhatsApp: ') + '09110215649';
          alertBox.style.display = 'block';
        }
        if (submitBtn) {
          submitBtn.textContent = originalText;
          submitBtn.disabled = false;
        }
      }
    });
  }
});
