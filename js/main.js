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
    }, { passive: true });

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
    // Sprint 011 (round 2): guard against pages using the newer `.hd-nav`
    // header markup, where `.nav` doesn't exist and `nav` is null. Those
    // pages' scroll-driven header state is handled by js/acg-chrome.js;
    // this listener only needs to run on legacy `.nav` pages.
    if (!nav) return;
    if (window.pageYOffset > 80) {
      nav.classList.add('scrolled');
    } else {
      // Only remove scrolled on pages where hero exists
      if (document.querySelector('.hero')) {
        nav.classList.remove('scrolled');
      }
    }
  }, { passive: true });

  if (navToggle && navLinks) {
    const mobileNavQuery = window.matchMedia('(max-width: 900px)');

    const setMenuState = (open, returnFocus = false) => {
      navToggle.classList.toggle('active', open);
      navLinks.classList.toggle('open', open);
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';

      if (mobileNavQuery.matches && !open) {
        navLinks.setAttribute('inert', '');
      } else {
        navLinks.removeAttribute('inert');
      }

      if (returnFocus) navToggle.focus();
    };

    const syncMenuForViewport = () => {
      if (!mobileNavQuery.matches) {
        setMenuState(false);
        return;
      }
      setMenuState(navLinks.classList.contains('open'));
    };

    syncMenuForViewport();

    if (typeof mobileNavQuery.addEventListener === 'function') {
      mobileNavQuery.addEventListener('change', syncMenuForViewport);
    } else {
      mobileNavQuery.addListener(syncMenuForViewport);
    }

    navToggle.addEventListener('click', () => {
      setMenuState(!navLinks.classList.contains('open'));
    });

    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        setMenuState(false);
      });
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && navLinks.classList.contains('open')) {
        setMenuState(false, true);
      }
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
      }, { passive: true });
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
    }, { passive: true });
  }

});

  // ============================================
  // ---------- GA4 CONVERSION EVENTS ----------
  // ============================================
  function trackEvent(name, params = {}) {
    if (typeof gtag === 'function') {
      gtag('event', name, params);
    }
    if (window.dataLayer) {
      window.dataLayer.push({ event: name, ...params });
    }
  }

  // Phone clicks (tel: links)
  document.querySelectorAll('a[href^="tel:"]').forEach(a => {
    a.addEventListener('click', () => trackEvent('phone_click', {
      phone_number: a.getAttribute('href').replace('tel:', ''),
      page_location: location.pathname
    }));
  });

  // Email clicks (mailto: links)
  document.querySelectorAll('a[href^="mailto:"]').forEach(a => {
    a.addEventListener('click', () => trackEvent('email_click', {
      email_address: a.getAttribute('href').replace('mailto:', ''),
      page_location: location.pathname
    }));
  });

  // Send Us Plans CTA clicks (anywhere on site)
  document.querySelectorAll('a').forEach(a => {
    const text = (a.textContent || '').trim().toLowerCase();
    const href = a.getAttribute('href') || '';
    if (text.includes('send us plans') ||
        text.includes('submit plans') ||
        text === 'send plans' ||
        href.endsWith('/send-plans.html') ||
        href.endsWith('send-plans.html')) {
      a.addEventListener('click', () => trackEvent('cta_submit_plans_click', {
        cta_text: (a.textContent || '').trim(),
        page_location: location.pathname,
        cta_href: href
      }));
    }
  });

  // Scope Engine start/complete
  if (location.pathname.includes('scope-engine')) {
    trackEvent('scope_engine_start', { page_location: location.pathname });
  }

  // PDF download tracking
  document.querySelectorAll('a[href$=".pdf"]').forEach(a => {
    a.addEventListener('click', () => trackEvent('resource_download', {
      file_name: (a.getAttribute('href') || '').split('/').pop(),
      file_url: a.getAttribute('href'),
      link_text: (a.textContent || '').trim()
    }));
  });

  // Portfolio case study view (when on a project detail page)
  const isProjectPage = location.pathname.match(/-clubhouse\.html|-twelve\.html|-prime-|panther-|wild-blue|atlantic-fields|eau-palm/i);
  if (isProjectPage) {
    trackEvent('portfolio_case_study_view', {
      project_slug: location.pathname.replace(/^\//, '').replace('.html', ''),
      page_location: location.pathname
    });
  }

  // ============================================
  // ---------- STICKY MOBILE CTA BAR ----------
  // ============================================
  // Only show on mobile (<=768px), hide on /send-plans.html + /contact.html
  if (window.innerWidth <= 768 &&
      !/send-plans\.html|contact\.html/.test(location.pathname)) {
    const bar = document.createElement('div');
    bar.className = 'mobile-cta-bar';
    bar.innerHTML = `
      <a href="tel:+17724867711" class="mcb-btn mcb-call" aria-label="Call ACG">
        <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M20 15.5c-1.25 0-2.45-.2-3.57-.57a1 1 0 00-1.02.24l-2.2 2.2a15.05 15.05 0 01-6.59-6.59l2.2-2.21a1 1 0 00.25-1A11.36 11.36 0 018.5 4a1 1 0 00-1-1H4a1 1 0 00-1 1 17 17 0 0017 17 1 1 0 001-1v-3.5a1 1 0 00-1-1z"/></svg>
        <span>Call</span>
      </a>
      <a href="mailto:connor@acglass.com" class="mcb-btn mcb-email" aria-label="Email ACG">
        <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M20 4H4a2 2 0 00-2 2v12a2 2 0 002 2h16a2 2 0 002-2V6a2 2 0 00-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
        <span>Email</span>
      </a>
      <a href="/send-plans.html" class="mcb-btn mcb-plans" aria-label="Send us plans">
        <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6zm4 18H6V4h7v5h5v11zM8 14h8v2H8zm0 4h8v2H8zm0-8h4v2H8z"/></svg>
        <span>Send Plans</span>
      </a>
    `;
    document.body.appendChild(bar);
    // Apply body padding so content clears the fixed bar
    document.body.style.paddingBottom = '72px';
  }
