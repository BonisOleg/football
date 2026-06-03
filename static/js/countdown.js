const pad = (n) => String(n).padStart(2, '0');

const tick = (el) => {
  const target = new Date(el.dataset.startsAt).getTime();
  const diff = Math.max(0, target - Date.now());
  const d = Math.floor(diff / 86400000);
  const h = Math.floor((diff / 3600000) % 24);
  const m = Math.floor((diff / 60000) % 60);
  const s = Math.floor((diff / 1000) % 60);

  const days = el.querySelector('[data-cd-days]');
  const hours = el.querySelector('[data-cd-hours]');
  const mins = el.querySelector('[data-cd-mins]');
  const secs = el.querySelector('[data-cd-secs]');

  if (days) days.textContent = pad(d);
  if (hours) hours.textContent = pad(h);
  if (mins) mins.textContent = pad(m);
  if (secs) secs.textContent = pad(s);
};

document.querySelectorAll('[data-countdown]').forEach((el) => {
  tick(el);
  setInterval(() => tick(el), 1000);
});
