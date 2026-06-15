const hero = document.getElementById('home-hero');
if (hero) {
  const dynamic = document.getElementById('hero-dynamic');
  const items = [...hero.querySelectorAll('[data-wheel-index]')];
  const count = items.length;
  let active = Number(hero.dataset.initialWheelIndex ?? 0);
  let cardDrag = null;

  const mobileMq = window.matchMedia('(max-width: 760px)');
  const reducedMotionMq = window.matchMedia('(prefers-reduced-motion: reduce)');
  const wheelTrack = hero.querySelector('.hero__wheel-track');
  const cardStage = dynamic?.querySelector('.hero__card-stage');

  const SWIPE_THRESHOLD = 60;
  const SWIPE_TRANSLATE_RATIO = 0.2;
  const SWIPE_ROTATE_RATIO = 0.02;

  const getCard = () => dynamic?.querySelector('[data-hero-card]');

  const parseHeroRow = (html) => {
    const temp = document.createElement('div');
    temp.innerHTML = html.trim();
    return {
      main: temp.querySelector('.hero__main'),
      card: temp.querySelector('[data-hero-card]'),
    };
  };

  const applyHeroContent = ({ main, card }) => {
    if (!dynamic) return;

    const currentMain = dynamic.querySelector('.hero__main');
    const stage = dynamic.querySelector('.hero__card-stage');

    if (currentMain && main) {
      currentMain.replaceWith(main);
    }
    if (stage && card) {
      stage.innerHTML = '';
      stage.append(card);
    }
  };

  const scrollWheelToActive = () => {
    if (!wheelTrack) return;
    const btn = items[active];
    if (!btn) return;

    const trackRect = wheelTrack.getBoundingClientRect();
    const btnRect = btn.getBoundingClientRect();
    const offset =
      btnRect.left -
      trackRect.left -
      (trackRect.width - btnRect.width) / 2 +
      wheelTrack.scrollLeft;

    wheelTrack.scrollTo({
      left: offset,
      behavior: reducedMotionMq.matches ? 'auto' : 'smooth',
    });
  };

  const setTheme = (theme) => {
    if (dynamic) {
      dynamic.dataset.themeTarget = theme;
    }
    document.body.className = `page ${theme}`;
  };

  const updateHeroBg = (url) => {
    const normalized = (url || '').trim();
    let bg = hero.querySelector('.hero__bg');

    if (normalized) {
      if (!bg) {
        bg = document.createElement('div');
        bg.className = 'hero__bg';
        bg.setAttribute('aria-hidden', 'true');
        hero.insertBefore(bg, hero.querySelector('.hero__glow'));
      }
      bg.style.backgroundImage = `url('${normalized}')`;
      hero.classList.add('hero--has-bg');
      hero.dataset.heroBg = normalized;
    } else {
      bg?.remove();
      hero.classList.remove('hero--has-bg');
      delete hero.dataset.heroBg;
    }
  };

  const swapPanel = (html, direction) => {
    if (!dynamic) return;

    const parts = parseHeroRow(html);
    const card = getCard();
    const animate = direction && !reducedMotionMq.matches && card;

    if (!animate) {
      applyHeroContent(parts);
      return;
    }

    card.classList.add('hero-card--swap-out');
    card.addEventListener(
      'animationend',
      () => {
        applyHeroContent(parts);
        const nextCard = getCard();
        if (!nextCard) return;
        nextCard.classList.add('hero-card--swap-in');
        nextCard.addEventListener(
          'animationend',
          () => nextCard.classList.remove('hero-card--swap-in'),
          { once: true },
        );
      },
      { once: true },
    );
  };

  const setActive = (index, direction = 0, fetchContent = true) => {
    if (!count) return;
    active = Math.max(0, Math.min(index, count - 1));
    items.forEach((btn, i) => {
      const on = i === active;
      btn.classList.toggle('is-active', on);
      btn.setAttribute('aria-selected', on ? 'true' : 'false');
    });

    const btn = items[active];
    const theme = btn.dataset.theme;
    if (theme) setTheme(theme);
    updateHeroBg(btn.dataset.heroBg);

    const url = btn.dataset.partialUrl;
    if (fetchContent && dynamic && url) {
      fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
        .then((r) => r.text())
        .then((html) => swapPanel(html, direction))
        .catch(() => {});
    }

    scrollWheelToActive();
  };

  const goPrev = () => setActive(active - 1, -1);
  const goNext = () => setActive(active + 1, 1);

  items.forEach((btn) => {
    btn.addEventListener('click', () => {
      const idx = Number(btn.dataset.wheelIndex);
      const dir = idx > active ? 1 : idx < active ? -1 : 0;
      setActive(idx, dir);
    });
  });

  hero.querySelector('[data-wheel-prev]')?.addEventListener('click', goPrev);
  hero.querySelector('[data-wheel-next]')?.addEventListener('click', goNext);

  window.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') goNext();
    if (e.key === 'ArrowLeft') goPrev();
  });

  const applyCardDrag = (card, dx) => {
    if (reducedMotionMq.matches) return;
    card.style.setProperty('--hero-swipe-x', `${dx * SWIPE_TRANSLATE_RATIO}px`);
    card.style.setProperty('--hero-card-rotate', `${dx * SWIPE_ROTATE_RATIO}deg`);
  };

  const resetCardDrag = (card) => {
    if (!card) return;
    card.classList.remove('is-swiping');
    card.style.removeProperty('--hero-swipe-x');
    card.style.removeProperty('--hero-card-rotate');
  };

  const bindCardSwipe = () => {
    if (!cardStage) return;

    cardStage.addEventListener('pointerdown', (e) => {
      if (e.button !== 0) return;

      const card = e.target.closest('[data-hero-card]');
      if (!card) return;

      cardDrag = {
        card,
        id: e.pointerId,
        x: e.clientX,
        on: true,
      };
      card.classList.add('is-swiping');
      card.setPointerCapture(e.pointerId);
    });

    cardStage.addEventListener(
      'pointermove',
      (e) => {
        if (!cardDrag?.on || cardDrag.id !== e.pointerId) return;

        const dx = e.clientX - cardDrag.x;
        cardDrag.dx = dx;
        applyCardDrag(cardDrag.card, dx);
        e.preventDefault();
      },
      { passive: false },
    );

    const finishSwipe = (e) => {
      if (!cardDrag?.on || cardDrag.id !== e.pointerId) return;

      const { card } = cardDrag;
      try {
        card.releasePointerCapture(e.pointerId);
      } catch {
        /* pointer already released */
      }

      const dx = cardDrag.dx ?? 0;
      resetCardDrag(card);
      cardDrag = null;

      if (dx > SWIPE_THRESHOLD) goPrev();
      else if (dx < -SWIPE_THRESHOLD) goNext();
    };

    cardStage.addEventListener('pointerup', finishSwipe);
    cardStage.addEventListener('pointercancel', finishSwipe);
    cardStage.addEventListener('pointerleave', (e) => {
      if (cardDrag?.on && cardDrag.id === e.pointerId) finishSwipe(e);
    });
  };

  bindCardSwipe();
  setActive(active, 0, false);
  requestAnimationFrame(scrollWheelToActive);
}
