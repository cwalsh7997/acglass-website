/* ================================================================
   AMERICAN COMMERCIAL GLASS — Main JavaScript v4
   Clean, performant interactions for Figma-style design
   ================================================================ */

document.addEventListener('DOMContentLoaded', () => {

  // ---- PAGE LOAD ----
  requestAnimationFrame(() => {
    document.body.classList.add('loaded');
  });

  // ---- HEADER SCROLL ----
  const header = document.getElementById('header');
  let ticking = false;

  if (header) {
    const onScroll = () => {
      header.classList.toggle('scrolled', window.scrollY > 50);
      ticking = false;
    };

    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(onScroll);
        ticking = true;
      }
    }, { passive: true });

    onScroll();
  }

  // ---- MOBILE NAVIGATION ----
  const mobileToggle = document.querySelector('.mobile-toggle');
  const mobileNav = document.getElementById('mobile-nav');
  const mobileClose = document.querySelector('.mobile-close');
  const mobileOverlay = document.querySelector('.mobile-overlay');

  const openMobile = () => {
    mobileNav?.classList.add('active');
    mobileOverlay?.classList.add('active');
    document.body.style.overflow = 'hidden';
  };

  const closeMobile = () => {
    mobileNav?.classList.remove('active');
    mobileOverlay?.classList.remove('active');
    document.body.style.overflow = '';
  };

  mobileToggle?.addEventListener('click', openMobile);
  mobileClose?.addEventListener('click', closeMobile);
  mobileOverlay?.addEventListener('click', closeMobile);
  mobileNav?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMobile));

  // ---- SCROLL REVEAL ----
  const reveals = document.querySelectorAll('.reveal');

  if (reveals.length && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.08,
      rootMargin: '0px 0px -60px 0px'
    });

    reveals.forEach(el => observer.observe(el));
  } else {
    reveals.forEach(el => el.classList.add('visible'));
  }

  // ---- COUNTER ANIMATION ----
  const statNumbers = document.querySelectorAll('.hero-stat-number[data-count]');

  if (statNumbers.length && 'IntersectionObserver' in window) {
    const countObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.dataset.count, 10);
          const suffix = el.dataset.suffix || '';
          const prefix = el.dataset.prefix || '';
          const duration = 2200;
          const startTime = performance.now();

          const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 4);
            const current = Math.round(target * eased);
            el.textContent = prefix + current.toLocaleString() + suffix;

            if (progress < 1) {
              requestAnimationFrame(animate);
            } else {
              el.textContent = prefix + target.toLocaleString() + suffix;
            }
          };

          requestAnimationFrame(animate);
          countObserver.unobserve(el);
        }
      });
    }, { threshold: 0.5 });

    statNumbers.forEach(el => countObserver.observe(el));
  }

  // ---- HERO PARALLAX (DESKTOP) ----
  const heroBg = document.querySelector('.hero-bg img');
  let parallaxTicking = false;

  if (heroBg && window.matchMedia('(min-width: 768px)').matches && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const updateParallax = () => {
      const y = window.scrollY;
      if (y < window.innerHeight * 1.2) {
        heroBg.style.transform = `scale(1.05) translateY(${y * 0.12}px)`;
      }
      parallaxTicking = false;
    };

    window.addEventListener('scroll', () => {
      if (!parallaxTicking) {
        requestAnimationFrame(updateParallax);
        parallaxTicking = true;
      }
    }, { passive: true });
  }

  // ---- PORTFOLIO FILTERING ----
  const filterBtns = document.querySelectorAll('.filter-btn');
  const portfolioCards = document.querySelectorAll('.portfolio-card');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const filter = btn.dataset.filter;
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      let delay = 0;
      portfolioCards.forEach(card => {
        const types = (card.dataset.type || '').split(',').map(t => t.trim());
        const match = filter === 'all' || types.includes(filter);

        if (match) {
          card.style.display = '';
          card.style.opacity = '0';
          card.style.transform = 'translateY(12px)';
          setTimeout(() => {
            card.style.transition = 'opacity 0.4s cubic-bezier(0.16,1,0.3,1), transform 0.4s cubic-bezier(0.16,1,0.3,1)';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
          }, delay);
          delay += 60;
        } else {
          card.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
          card.style.opacity = '0';
          card.style.transform = 'scale(0.97)';
          setTimeout(() => { card.style.display = 'none'; }, 200);
        }
      });
    });
  });

  // ---- FILE UPLOAD ----
  const fileUpload = document.querySelector('.file-upload');
  const fileInput = document.getElementById('plan-upload');

  if (fileUpload && fileInput) {
    fileUpload.addEventListener('click', () => fileInput.click());

    fileUpload.addEventListener('dragover', (e) => {
      e.preventDefault();
      fileUpload.style.borderColor = 'var(--gray-400)';
      fileUpload.style.background = 'var(--gray-50)';
    });

    fileUpload.addEventListener('dragleave', () => {
      fileUpload.style.borderColor = '';
      fileUpload.style.background = '';
    });

    fileUpload.addEventListener('drop', (e) => {
      e.preventDefault();
      fileUpload.style.borderColor = '';
      fileUpload.style.background = '';
      if (e.dataTransfer.files.length) {
        fileInput.files = e.dataTransfer.files;
        updateFileDisplay(e.dataTransfer.files);
      }
    });

    fileInput.addEventListener('change', () => updateFileDisplay(fileInput.files));
  }

  const updateFileDisplay = (files) => {
    const textEl = document.querySelector('.file-upload-text');
    if (textEl && files.length) {
      const names = Array.from(files).map(f => f.name).join(', ');
      textEl.innerHTML = `<strong>${files.length} file${files.length > 1 ? 's' : ''} selected:</strong> ${names}`;
      if (fileUpload) {
        fileUpload.style.borderColor = 'var(--accent)';
        fileUpload.style.borderStyle = 'solid';
      }
    }
  };

  // ---- SMOOTH ANCHOR SCROLLING ----
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        const headerH = header ? header.offsetHeight : 0;
        const y = target.getBoundingClientRect().top + window.scrollY - headerH - 24;
        window.scrollTo({ top: y, behavior: 'smooth' });
      }
    });
  });

  // ---- IMAGE LOAD ENHANCEMENT ----
  document.querySelectorAll('.project-card img, .portfolio-card img, .hero-bg img').forEach(img => {
    if (img.complete) {
      img.style.opacity = '1';
    } else {
      img.style.opacity = '0';
      img.style.transition = 'opacity 0.8s ease';
      img.addEventListener('load', () => { img.style.opacity = '1'; });
      img.addEventListener('error', () => {
        img.parentElement.style.background = 'linear-gradient(135deg, #111827, #1A4372)';
        img.style.display = 'none';
      });
    }
  });

});
