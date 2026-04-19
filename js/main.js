/* ============================================
   AMERICAN COMMERCIAL GLASS — V2 ENGINE
   Custom cursor, scroll reveals, drag scroll,
   counters, parallax, marquee
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

  // ---------- CUSTOM CURSOR ----------
  const dot = document.querySelector('.cursor-dot');
  const ring = document.querySelector('.cursor-ring');

  if (dot && ring && window.innerWidth > 768) {
    let mouseX = 0, mouseY = 0;
    let ringX = 0, ringY = 0;

    document.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      dot.style.left = mouseX + 'px';
      dot.style.top = mouseY + 'px';
    });

    function animateRing() {
      ringX += (mouseX - ringX) * 0.15;
      ringY += (mouseY - ringY) * 0.15;
      ring.style.left = ringX + 'px';
      ring.style.top = ringY + 'px';
      requestAnimationFrame(animateRing);
    }
    animateRing();

    // Hover effects on interactive elements
    const hoverTargets = document.querySelectorAll('a, button, .project-card, .project-grid-item, .service-card, .mfg-card');
    hoverTargets.forEach(el => {
      el.addEventListener('mouseenter', () => document.body.classList.add('cursor-hover'));
      el.addEventListener('mouseleave', () => document.body.classList.remove('cursor-hover'));
    });
  }

  // ---------- NAVIGATION ----------
  const nav = document.querySelector('.nav');
  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');

  window.addEventListener('scroll', () => {
    if (window.pageYOffset > 80) {
      nav.classList.add('scrolled');
    } else {
      // Only remove scrolled on pages where hero exists
      if (document.querySelector('.hero')) {
        nav.classList.remove('scrolled');
      }
    }
  });

  if (navToggle) {
    navToggle.addEventListener('click', () => {
      navToggle.classList.toggle('active');
      navLinks.classList.toggle('open');
      document.body.style.overflow = navLinks.classList.contains('open') ? 'hidden' : '';
    });

    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navToggle.classList.remove('active');
        navLinks.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
  }

  // ---------- SCROLL REVEAL ----------
  const revealElements = document.querySelectorAll('[data-reveal], [data-reveal-fade], [data-reveal-scale]');

  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const delay = entry.target.dataset.delay || 0;
        setTimeout(() => {
          entry.target.classList.add('revealed');
        }, parseInt(delay));
        revealObserver.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.08,
    rootMargin: '0px 0px -60px 0px'
  });

  revealElements.forEach(el => revealObserver.observe(el));

  // ---------- COUNTER ANIMATION ----------
  const counters = document.querySelectorAll('[data-count]');

  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const target = entry.target;
        const end = parseInt(target.dataset.count);
        const suffix = target.dataset.suffix || '';
        const prefix = target.dataset.prefix || '';
        const duration = 2200;
        const startTime = performance.now();

        function updateCounter(currentTime) {
          const elapsed = currentTime - startTime;
          const progress = Math.min(elapsed / duration, 1);
          const eased = 1 - Math.pow(1 - progress, 4);
          const current = Math.floor(end * eased);
          target.textContent = prefix + current.toLocaleString() + suffix;
          if (progress < 1) requestAnimationFrame(updateCounter);
        }
        requestAnimationFrame(updateCounter);
        counterObserver.unobserve(target);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(el => counterObserver.observe(el));

  // ---------- DRAG-TO-SCROLL PORTFOLIO ----------
  const scrollContainers = document.querySelectorAll('.portfolio-scroll');

  scrollContainers.forEach(container => {
    let isDown = false;
    let startX;
    let scrollLeft;

    container.addEventListener('mousedown', (e) => {
      isDown = true;
      container.style.cursor = 'grabbing';
      startX = e.pageX - container.offsetLeft;
      scrollLeft = container.scrollLeft;
    });

    container.addEventListener('mouseleave', () => {
      isDown = false;
      container.style.cursor = 'grab';
    });

    container.addEventListener('mouseup', () => {
      isDown = false;
      container.style.cursor = 'grab';
    });

    container.addEventListener('mousemove', (e) => {
      if (!isDown) return;
      e.preventDefault();
      const x = e.pageX - container.offsetLeft;
      const walk = (x - startX) * 1.5;
      container.scrollLeft = scrollLeft - walk;
    });

    // Progress bar
    const progressBar = container.parentElement.querySelector('.portfolio-progress-bar');
    if (progressBar) {
      container.addEventListener('scroll', () => {
        const scrollPercentage = container.scrollLeft / (container.scrollWidth - container.clientWidth);
        progressBar.style.transform = `translateX(${scrollPercentage * (200 - progressBar.offsetWidth)}px)`;
      });
    }
  });

  // ---------- PORTFOLIO FILTERS ----------
  const filterBtns = document.querySelectorAll('.filter-btn');
  const gridItems = document.querySelectorAll('.project-grid-item[data-category]');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const filter = btn.dataset.filter;
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      gridItems.forEach(item => {
        if (filter === 'all' || item.dataset.category === filter) {
          item.style.display = '';
          requestAnimationFrame(() => {
            item.style.opacity = '1';
            item.style.transform = 'scale(1)';
          });
        } else {
          item.style.opacity = '0';
          item.style.transform = 'scale(0.95)';
          setTimeout(() => { item.style.display = 'none'; }, 400);
        }
      });
    });
  });

  // ---------- SMOOTH ANCHOR SCROLL ----------
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ---------- FORM MAILTO HANDLER ----------
  const contactForm = document.querySelector('#contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const name = this.querySelector('[name="name"]')?.value || '';
      const company = this.querySelector('[name="company"]')?.value || '';
      const email = this.querySelector('[name="email"]')?.value || '';
      const phone = this.querySelector('[name="phone"]')?.value || '';
      const projectType = this.querySelector('[name="project-type"]')?.value || '';
      const message = this.querySelector('[name="message"]')?.value || '';

      const subject = encodeURIComponent(`Project Inquiry from ${name} — ${company}`);
      const body = encodeURIComponent(
        `Name: ${name}\nCompany: ${company}\nEmail: ${email}\nPhone: ${phone}\nProject Type: ${projectType}\n\nMessage:\n${message}`
      );
      window.location.href = `mailto:connor@acglass.com?subject=${subject}&body=${body}`;
    });
  }

  // ---------- ACTIVE NAV LINK ----------
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPage || (currentPage === '' && href === 'index.html')) {
      link.classList.add('active');
    }
  });

  // ---------- PARALLAX ON HERO ----------
  const heroVisual = document.querySelector('.hero-bg');
  if (heroVisual) {
    window.addEventListener('scroll', () => {
      const scrolled = window.pageYOffset;
      if (scrolled < window.innerHeight) {
        heroVisual.style.transform = `translateY(${scrolled * 0.3}px)`;
      }
    });
  }

});
