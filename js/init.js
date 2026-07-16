// init.js - handles page ready class and scroll-reveal animations

document.addEventListener('DOMContentLoaded', () => {
  // Add page-ready class to trigger body fade-in
  document.body.classList.add('page-ready');

  // IntersectionObserver for scroll-reveal elements
  const revealElements = document.querySelectorAll('.scroll-reveal');
  const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1,
  };
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  revealElements.forEach(el => revealObserver.observe(el));
});
