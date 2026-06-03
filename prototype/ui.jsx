// ui.jsx — shared UI atoms: Logo, Header, Footer, SeasonIcon, Countdown
const { useState, useEffect, useMemo, useRef } = React;

// Seasonal "L" shield logo — original geometric mark (not branded)
function Logo({ size = 36, accent = 'var(--accent)' }) {
  return (
    <svg width={size} height={size} viewBox="0 0 40 40" fill="none" style={{ display:'block' }}>
      <path d="M6 4 L20 4 L34 4 L34 28 L20 36 L6 28 Z" stroke={accent} strokeWidth="2" fill="none" />
      <path d="M14 12 L14 24 L24 24" stroke="var(--fg-0)" strokeWidth="2.5" strokeLinecap="square" strokeLinejoin="miter" fill="none" />
      <circle cx="28" cy="14" r="2" fill={accent} />
    </svg>
  );
}

// Tiny season glyph (sun/leaf/snowflake/flame) — abstract geometric, not pictographic
function SeasonIcon({ season, size = 22, color = 'currentColor' }) {
  const s = size;
  if (season === 'Spring') return (
    <svg width={s} height={s} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="1.8" strokeLinecap="round">
      <path d="M12 3 v18" />
      <path d="M12 8 C8 8 6 6 6 4" />
      <path d="M12 12 C16 12 18 10 18 8" />
      <path d="M12 16 C8 16 6 14 6 12" />
    </svg>
  );
  if (season === 'Autumn') return (
    <svg width={s} height={s} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 3 C7 7 5 11 5 14 a7 7 0 0 0 14 0 c0-3-2-7-7-11Z" />
      <path d="M12 6 v15" />
    </svg>
  );
  if (season === 'Winter') return (
    <svg width={s} height={s} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="1.8" strokeLinecap="round">
      <path d="M12 3 v18 M3 12 h18 M5.5 5.5 L18.5 18.5 M18.5 5.5 L5.5 18.5" />
    </svg>
  );
  return null;
}

// Football icon (rotating)
function BallIcon({ size = 22, color = 'currentColor', spin = false }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="1.6" style={{ animation: spin ? 'spin 8s linear infinite' : 'none', transformOrigin:'center' }}>
      <circle cx="12" cy="12" r="9" />
      <path d="M12 3 L15 9 L21 10" />
      <path d="M12 3 L9 9 L3 10" />
      <path d="M15 9 L17 16 L12 19 L7 16 L9 9" />
      <path d="M3 10 L7 16 M21 10 L17 16 M12 19 L12 21" />
    </svg>
  );
}

// Arrow
function Arrow({ dir = 'right', size = 14 }) {
  const rot = { right: 0, left: 180, up: -90, down: 90 }[dir] || 0;
  return (
    <svg width={size} height={size} viewBox="0 0 14 14" fill="none" style={{ transform:`rotate(${rot}deg)`, display:'inline-block' }}>
      <path d="M2 7 H12 M8 3 L12 7 L8 11" stroke="currentColor" strokeWidth="1.7" strokeLinecap="square" />
    </svg>
  );
}

// Header — sticky top nav
function Header({ route, setRoute, current }) {
  const links = window.TOURNAMENTS.map(t => ({ id: t.id, label: t.title + (t.subtitle.includes('Autumn') ? ' Осінь' : t.subtitle.includes('Kids') ? ' Kids' : ''), short: t.title + (t.id === 'leo-cup-autumn' ? ' Осінь' : t.id === 'ruh-kids-cup' ? ' Kids' : '') }));
  return (
    <header style={styles_ui.header}>
      <div className="container" style={styles_ui.headerInner}>
        <a onClick={() => setRoute({ page: 'hub' })} style={styles_ui.logoLink}>
          <Logo size={32} accent="var(--accent)" />
          <span style={styles_ui.logoText}>
            <span style={{ color:'var(--fg-0)' }}>RUH</span>
            <span style={{ color:'var(--accent)' }}>·</span>
            <span style={{ color:'var(--fg-0)' }}>LEO</span>
            <span style={{ color:'var(--fg-2)', fontSize:11, marginLeft:6, letterSpacing:'.18em' }}>CUP</span>
          </span>
        </a>

        <nav style={styles_ui.nav}>
          <a onClick={() => setRoute({ page: 'hub' })} className={current === 'hub' ? 'nav-active' : ''} style={{...styles_ui.navLink, ...(current === 'hub' ? styles_ui.navLinkActive : {})}}>Головна</a>
          {window.TOURNAMENTS.map(t => (
            <a key={t.id} onClick={() => setRoute({ page: 'tournament', id: t.id })} style={{...styles_ui.navLink, ...(current === t.id ? styles_ui.navLinkActive : {})}}>
              {t.id === 'leo-cup' ? 'Leo Cup' :
               t.id === 'leo-cup-autumn' ? 'Leo Cup Осінь' :
               t.id === 'ruh-cup' ? 'Ruh Cup' : 'Ruh Kids'}
            </a>
          ))}
          <a onClick={() => setRoute({ page: 'apply' })} style={{...styles_ui.navLink, ...(current === 'apply' ? styles_ui.navLinkActive : {})}}>Заявка</a>
        </nav>

        <button className="btn btn-primary" onClick={() => setRoute({ page: 'apply' })}>
          Подати заявку <Arrow />
        </button>
      </div>
    </header>
  );
}

// Footer
function Footer({ setRoute }) {
  return (
    <footer style={styles_ui.footer}>
      <div className="container">
        <div style={styles_ui.footerGrid}>
          <div>
            <div style={{ display:'flex', alignItems:'center', gap:12, marginBottom:18 }}>
              <Logo size={40} />
              <div className="display" style={{ fontSize:26 }}>RUH · LEO CUP</div>
            </div>
            <p style={{ color:'var(--fg-2)', maxWidth:340, fontSize:14, lineHeight:1.6, margin:0 }}>
              Наймасовіші футбольні турніри Західної України. Чотири сезони — чотири фестивалі футболу для дітей від 6 років.
            </p>
          </div>

          <div>
            <div className="eyebrow" style={{ marginBottom:16 }}>Турніри</div>
            <ul style={styles_ui.footerList}>
              {window.TOURNAMENTS.map(t => (
                <li key={t.id}>
                  <a onClick={() => { setRoute({ page:'tournament', id:t.id }); window.scrollTo({top:0}); }} style={styles_ui.footerLink}>
                    {t.title} <span style={{ color:'var(--fg-3)', marginLeft:6 }}>· {t.season} {t.year}</span>
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <div className="eyebrow" style={{ marginBottom:16 }}>Контакти</div>
            <ul style={styles_ui.footerList}>
              <li className="mono" style={{ fontSize:14, color:'var(--fg-0)' }}>+38 068 890 28 44</li>
              <li className="mono" style={{ fontSize:14, color:'var(--fg-0)' }}>ruhcupleocup@gmail.com</li>
              <li style={{ color:'var(--fg-2)', fontSize:13, marginTop:4 }}>Львів, Україна</li>
            </ul>
          </div>

          <div>
            <div className="eyebrow" style={{ marginBottom:16 }}>Соцмережі</div>
            <div style={{ display:'flex', gap:10, flexWrap:'wrap' }}>
              {['INST','TG','YT','TT','FB'].map(s => (
                <a key={s} style={styles_ui.socialBtn}>{s}</a>
              ))}
            </div>
          </div>
        </div>

        <div style={styles_ui.footerBottom}>
          <div className="mono" style={{ fontSize:11, color:'var(--fg-3)', letterSpacing:'.14em' }}>
            © 2026 RUH LEO CUP · ALL RIGHTS RESERVED
          </div>
          <div className="mono" style={{ fontSize:11, color:'var(--fg-3)', letterSpacing:'.14em' }}>
            REDESIGN CONCEPT · NOT AFFILIATED
          </div>
        </div>
      </div>
    </footer>
  );
}

// Countdown — counts down to target ISO date
function Countdown({ target, accent = 'var(--accent)', compact = false }) {
  const [now, setNow] = useState(Date.now());
  useEffect(() => {
    const id = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(id);
  }, []);
  const t = new Date(target).getTime();
  const diff = Math.max(0, t - now);
  const d = Math.floor(diff / 86400000);
  const h = Math.floor((diff / 3600000) % 24);
  const m = Math.floor((diff / 60000) % 60);
  const s = Math.floor((diff / 1000) % 60);
  const items = [['Дні', d], ['Год', h], ['Хв', m], ['Сек', s]];
  return (
    <div style={{ display:'flex', gap: compact ? 10 : 18 }}>
      {items.map(([label, val], i) => (
        <div key={label} style={{...styles_ui.cdCell, padding: compact ? '10px 14px' : '18px 22px' }}>
          <div className="display mono" style={{ fontSize: compact ? 28 : 48, color: accent, lineHeight:1 }}>
            {String(val).padStart(2,'0')}
          </div>
          <div className="eyebrow" style={{ fontSize: compact ? 9 : 11, marginTop:6 }}>{label}</div>
        </div>
      ))}
    </div>
  );
}

// Stats counter (animated)
function StatNumber({ value, suffix = '', duration = 1100 }) {
  const [n, setN] = useState(0);
  const ref = useRef();
  useEffect(() => {
    let raf;
    const start = performance.now();
    const tick = (t) => {
      const p = Math.min(1, (t - start) / duration);
      const eased = 1 - Math.pow(1 - p, 3);
      setN(Math.round(eased * value));
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [value]);
  return <span ref={ref} className="display mono">{n}{suffix}</span>;
}

// Marquee bar
function Marquee({ items, accent = 'var(--accent)' }) {
  const txt = items.join('  ●  ');
  const full = `${txt}  ●  ${txt}  ●  ${txt}`;
  return (
    <div style={styles_ui.marquee}>
      <div style={styles_ui.marqueeTrack}>
        <span style={{ color: accent }}>{full}</span>
        <span style={{ color: accent }}>{full}</span>
      </div>
    </div>
  );
}

const styles_ui = {
  header: {
    position:'sticky', top:0, zIndex: 100,
    background: 'color-mix(in oklab, var(--bg-0) 78%, transparent)',
    backdropFilter: 'blur(18px) saturate(140%)',
    WebkitBackdropFilter: 'blur(18px) saturate(140%)',
    borderBottom: '1px solid var(--line)',
  },
  headerInner: {
    display:'flex', alignItems:'center', justifyContent:'space-between',
    gap: 24, padding: '16px 32px', height: 72,
  },
  logoLink: { display:'flex', alignItems:'center', gap:12, cursor:'default' },
  logoText: { fontFamily:'var(--f-display)', fontSize:22, letterSpacing:'.02em', display:'flex', alignItems:'center' },
  nav: { display:'flex', alignItems:'center', gap: 4 },
  navLink: {
    padding: '8px 14px', fontSize: 13, color:'var(--fg-1)',
    borderRadius: 8, cursor:'default', transition:'background .15s, color .15s',
    fontWeight: 500,
  },
  navLinkActive: { background:'var(--bg-2)', color:'var(--accent)' },

  footer: { borderTop:'1px solid var(--line)', marginTop: 80, paddingTop: 60, paddingBottom: 30, background:'var(--bg-0)' },
  footerGrid: { display:'grid', gridTemplateColumns:'1.5fr 1fr 1fr 1fr', gap: 40, paddingBottom: 40, borderBottom:'1px solid var(--line)' },
  footerList: { listStyle:'none', padding:0, margin:0, display:'flex', flexDirection:'column', gap: 10 },
  footerLink: { fontSize: 14, color:'var(--fg-1)', cursor:'default' },
  socialBtn: {
    display:'inline-flex', alignItems:'center', justifyContent:'center',
    width: 44, height: 44, borderRadius: 12,
    background:'var(--bg-2)', border:'1px solid var(--line)',
    fontFamily:'var(--f-mono)', fontSize: 10, letterSpacing:'.08em',
    color:'var(--fg-1)', cursor:'default',
  },
  footerBottom: {
    display:'flex', justifyContent:'space-between', alignItems:'center', flexWrap:'wrap', gap:12,
    paddingTop: 22,
  },

  cdCell: {
    background:'var(--bg-1)', border:'1px solid var(--line)', borderRadius: 14,
    minWidth: 92, textAlign:'center',
  },

  marquee: { overflow:'hidden', borderTop:'1px solid var(--line)', borderBottom:'1px solid var(--line)', padding:'14px 0', whiteSpace:'nowrap' },
  marqueeTrack: { display:'inline-flex', gap: 24, animation:'marquee 40s linear infinite', fontFamily:'var(--f-display)', fontSize: 28, letterSpacing:'.04em' },
};

// CSS keyframes inject
if (!document.getElementById('ui-keyframes')) {
  const st = document.createElement('style');
  st.id = 'ui-keyframes';
  st.textContent = `
    @keyframes spin { from { transform: rotate(0); } to { transform: rotate(360deg); } }
    @keyframes marquee { from { transform: translateX(0); } to { transform: translateX(-50%); } }
    .nav-active { background: var(--bg-2); color: var(--accent) !important; }
  `;
  document.head.appendChild(st);
}

Object.assign(window, { Logo, SeasonIcon, BallIcon, Arrow, Header, Footer, Countdown, StatNumber, Marquee });
