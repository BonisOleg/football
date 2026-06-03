(function () {
  function initMobileNav() {
    const stack = document.querySelector('.site-header-stack');
    const chrome = document.querySelector('.site-chrome');
    const toggle = document.getElementById('site-nav-toggle');
    const burger = document.querySelector('[data-nav-toggle]');
    const nav = document.getElementById('site-nav');
    const mobileNavQuery = window.matchMedia('(max-width: 760px)');

    if (!toggle || !nav) {
      return;
    }

    let lockedScrollY = 0;

    const syncHeaderHeight = () => {
      if (!chrome || !stack) {
        return;
      }
      const height = `${chrome.offsetHeight}px`;
      stack.style.setProperty('--site-header-height', height);
    };

    const lockPageScroll = () => {
      lockedScrollY = window.scrollY;
      document.documentElement.classList.add('is-nav-open');
    };

    const unlockPageScroll = () => {
      document.documentElement.classList.remove('is-nav-open');
      window.scrollTo(0, lockedScrollY);
    };

    const setExpanded = (open) => {
      burger?.setAttribute('aria-expanded', open ? 'true' : 'false');
    };

    const setMenuOpen = (open) => {
      if (open && mobileNavQuery.matches) {
        syncHeaderHeight();
        lockPageScroll();
      } else if (!open) {
        unlockPageScroll();
      }
      setExpanded(open);
    };

    toggle.addEventListener('change', () => {
      setMenuOpen(toggle.checked);
    });

    mobileNavQuery.addEventListener('change', () => {
      if (!mobileNavQuery.matches && toggle.checked) {
        toggle.checked = false;
        setMenuOpen(false);
      }
    });

    nav.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        toggle.checked = false;
        setMenuOpen(false);
      });
    });

    syncHeaderHeight();
    window.addEventListener('resize', syncHeaderHeight);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMobileNav);
  } else {
    initMobileNav();
  }
})();
