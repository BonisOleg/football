const animate = (el) => {
  const target = Number(el.dataset.value || 0);
  const duration = 1100;
  const start = performance.now();

  const step = (t) => {
    const p = Math.min(1, (t - start) / duration);
    const eased = 1 - (1 - p) ** 3;
    el.textContent = String(Math.round(eased * target));
    if (p < 1) requestAnimationFrame(step);
  };

  requestAnimationFrame(step);
};

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting && !entry.target.dataset.counted) {
        entry.target.dataset.counted = '1';
        animate(entry.target);
      }
    });
  },
  { threshold: 0.3 },
);

document.querySelectorAll('[data-stat-counter]').forEach((el) => observer.observe(el));
