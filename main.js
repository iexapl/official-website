// AXLTeco Website - Shared Scripts
document.addEventListener('DOMContentLoaded', function() {
  // Mobile menu toggle
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.querySelector('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function() {
      nav.classList.toggle('show');
    });
  }
  // Set active nav link
  var current = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav a').forEach(function(a) {
    if (a.getAttribute('href') === current) {
      a.classList.add('active');
    }
  });
});
