// hub.jsx — Landing hub with horizontal seasons wheel
const { useState: useStateHub, useEffect: useEffectHub, useRef: useRefHub } = React;

function Hub({ setRoute }) {
  const tournaments = window.TOURNAMENTS;
  const [active, setActive] = useStateHub(0);
  const [drag, setDrag] = useStateHub({ x: 0, dx: 0, on: false });
  const wrapRef = useRefHub();

  const t = tournaments[active];

  // Auto-advance hint (subtle)
  useEffectHub(() => {
    const onKey = (e) => {
      if (e.key === 'ArrowRight') setActive(a => (a + 1) % tournaments.length);
      if (e.key === 'ArrowLeft')  setActive(a => (a - 1 + tournaments.length) % tournaments.length);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [tournaments.length]);

  const goPrev = () => setActive(a => (a - 1 + tournaments.length) % tournaments.length);
  const goNext = () => setActive(a => (a + 1) % tournaments.length);

  // Drag handlers
  const onDown = (e) => {
    const x = e.clientX ?? e.touches?.[0]?.clientX ?? 0;
    setDrag({ x, dx: 0, on: true });
  };
  const onMove = (e) => {
    if (!drag.on) return;
    const x = e.clientX ?? e.touches?.[0]?.clientX ?? 0;
    setDrag(d => ({ ...d, dx: x - d.x }));
  };
  const onUp = () => {
    if (!drag.on) return;
    if (drag.dx > 60) goPrev();
    else if (drag.dx < -60) goNext();
    setDrag({ x: 0, dx: 0, on: false });
  };

  return (
    <div className={`page ${t.theme}`} style={{ minHeight:'100vh' }}>
      <Header current="hub" setRoute={setRoute} />

      {/* HERO with season wheel */}
      <section style={hubStyles.hero}
        onMouseDown={onDown} onMouseMove={onMove} onMouseUp={onUp} onMouseLeave={onUp}
        onTouchStart={onDown} onTouchMove={onMove} onTouchEnd={onUp}
      >
        {/* Vignette gradient driven by accent */}
        <div style={hubStyles.glow} />

        <div className="container" style={{ position:'relative', zIndex:2 }}>
          {/* Eyebrow row */}
          <div style={hubStyles.heroEyebrow}>
            <div className="pill accent">
              <span className="live-dot" />
              Заявки відкриті · сезон {new Date().getFullYear()}
            </div>
            <div className="mono" style={{ color:'var(--fg-2)', fontSize:11, letterSpacing:'.18em' }}>
              ЛЬВІВ · UA · {new Date().getFullYear()}
            </div>
          </div>

          {/* Massive season title */}
          <div style={hubStyles.titleRow}>
            <div style={{ flex:1, minWidth: 0 }}>
              <div className="eyebrow" style={{ marginBottom: 14, color:'var(--accent)' }}>
                {String(active+1).padStart(2,'0')} / 0{tournaments.length} · {t.season.toUpperCase()} {t.year}
              </div>
              <h1 className="display" style={hubStyles.megaTitle}>
                {t.title.split(' ').map((w, i) => (
                  <span key={i} style={{ display:'block', color: i === 0 ? 'var(--fg-0)' : 'var(--accent)' }}>{w}</span>
                ))}
              </h1>
              <div style={{ marginTop: 18, fontSize: 18, color:'var(--fg-1)', maxWidth: 520 }}>
                {t.description}
              </div>

              <div style={{ marginTop: 30, display:'flex', gap:12, flexWrap:'wrap' }}>
                <button className="btn btn-primary" onClick={() => setRoute({ page:'tournament', id:t.id })}>
                  Перейти до турніру <Arrow />
                </button>
                <button className="btn btn-ghost" onClick={() => setRoute({ page:'apply' })}>
                  Подати заявку
                </button>
              </div>
            </div>

            {/* Big season "card" right */}
            <div style={{...hubStyles.heroCard, transform: `translateX(${drag.dx*0.2}px) rotate(${drag.dx*0.02}deg)` }}>
              <div style={hubStyles.heroCardInner}>
                <div style={{ display:'flex', justifyContent:'space-between', alignItems:'flex-start' }}>
                  <div className="eyebrow" style={{ color:'var(--accent)' }}>{t.seasonEn.toUpperCase()}</div>
                  <SeasonIcon season={t.seasonEn} size={28} color="var(--accent)" />
                </div>
                <div className="display" style={{ fontSize: 'clamp(80px, 12vw, 180px)', color:'var(--accent)', textAlign:'center', marginTop: 20, marginBottom: 10, lineHeight: 0.9 }}>
                  {t.year}
                </div>
                <div className="display" style={{ fontSize: 22, textAlign:'center', color:'var(--fg-0)' }}>
                  {t.season}
                </div>
                <div style={hubStyles.heroCardDivider} />
                <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap: 12 }}>
                  <div>
                    <div className="eyebrow" style={{ fontSize: 9 }}>Дати</div>
                    <div className="mono" style={{ fontSize: 13, color:'var(--fg-0)', marginTop: 4 }}>{t.dates}</div>
                  </div>
                  <div>
                    <div className="eyebrow" style={{ fontSize: 9 }}>Команд</div>
                    <div className="mono" style={{ fontSize: 13, color:'var(--fg-0)', marginTop: 4 }}>{t.teams}</div>
                  </div>
                  <div>
                    <div className="eyebrow" style={{ fontSize: 9 }}>Локація</div>
                    <div className="mono" style={{ fontSize: 13, color:'var(--fg-0)', marginTop: 4 }}>{t.location}</div>
                  </div>
                  <div>
                    <div className="eyebrow" style={{ fontSize: 9 }}>Формат</div>
                    <div className="mono" style={{ fontSize: 13, color:'var(--fg-0)', marginTop: 4 }}>{t.format}</div>
                  </div>
                </div>
              </div>

              {/* Decorative number */}
              <div style={hubStyles.heroCardNum}>
                {String(active+1).padStart(2,'0')}
              </div>
            </div>
          </div>

          {/* Wheel selector */}
          <div style={hubStyles.wheel}>
            <button onClick={goPrev} style={hubStyles.wheelBtn} aria-label="Previous"><Arrow dir="left" size={16} /></button>
            <div style={hubStyles.wheelTrack}>
              {tournaments.map((tr, i) => {
                const isActive = i === active;
                return (
                  <button key={tr.id} onClick={() => setActive(i)} style={{
                    ...hubStyles.wheelItem,
                    ...(isActive ? hubStyles.wheelItemActive : {}),
                    borderColor: isActive ? `var(--${tr.id === 'leo-cup' ? 'spring' : tr.id === 'leo-cup-autumn' ? 'autumn' : tr.id === 'ruh-cup' ? 'winter' : 'kids'})` : 'var(--line)',
                  }}>
                    <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', width:'100%' }}>
                      <span className="eyebrow" style={{ fontSize:10, color: isActive ? `var(--${tr.id === 'leo-cup' ? 'spring' : tr.id === 'leo-cup-autumn' ? 'autumn' : tr.id === 'ruh-cup' ? 'winter' : 'kids'})` : 'var(--fg-3)' }}>
                        {String(i+1).padStart(2,'0')}
                      </span>
                      <SeasonIcon season={tr.seasonEn} size={16} color={isActive ? `var(--${tr.id === 'leo-cup' ? 'spring' : tr.id === 'leo-cup-autumn' ? 'autumn' : tr.id === 'ruh-cup' ? 'winter' : 'kids'})` : 'var(--fg-3)'} />
                    </div>
                    <div className="display" style={{ fontSize: 22, marginTop: 14, color: isActive ? 'var(--fg-0)' : 'var(--fg-1)', textAlign:'left' }}>
                      {tr.title}
                    </div>
                    <div style={{ fontSize: 12, marginTop: 6, color:'var(--fg-2)', textAlign:'left' }}>
                      {tr.season} · {tr.year}
                    </div>
                    {isActive && <div style={hubStyles.wheelItemBar} />}
                  </button>
                );
              })}
            </div>
            <button onClick={goNext} style={hubStyles.wheelBtn} aria-label="Next"><Arrow dir="right" size={16} /></button>
          </div>
        </div>
      </section>

      {/* Marquee */}
      <Marquee
        items={['4 СЕЗОНИ', 'ОДИН ФУТБОЛ', 'ЛЬВІВ 2026', '600+ ГРАВЦІВ', 'ДЛЯ ДІТЕЙ ВІД 6 РОКІВ', 'НАЙМАСОВІШІ ТУРНІРИ УКРАЇНИ']}
      />

      {/* GLOBAL STATS strip */}
      <section style={{ padding:'80px 0' }}>
        <div className="container">
          <div className="section-head">
            <div>
              <div className="eyebrow">01 / Цифри сезону</div>
              <h2>Один рік. <span style={{ color:'var(--accent)' }}>Чотири турніри.</span></h2>
            </div>
            <div style={{ color:'var(--fg-2)', maxWidth: 360, fontSize: 14 }}>
              Команди з усієї України збираються у Львові чотири рази на рік, щоб боротися за головний трофей.
            </div>
          </div>

          <div style={hubStyles.statsGrid}>
            <StatCell value={208} label="Команд за рік" hint="ACROSS 4 EVENTS" />
            <StatCell value={316} label="Матчів" hint="REGULAR + PLAYOFF" />
            <StatCell value={1381} label="Голів" hint="2025 SEASON" />
            <StatCell value={28} label="Міст-учасників" hint="UA + EU" />
          </div>
        </div>
      </section>

      {/* SEASONS — small grid recap */}
      <section style={{ padding:'40px 0 80px' }}>
        <div className="container">
          <div className="section-head">
            <div>
              <div className="eyebrow">02 / Календар</div>
              <h2>Календар сезону</h2>
            </div>
          </div>

          <div style={hubStyles.seasonsRecap}>
            {tournaments.map((tr, i) => (
              <div key={tr.id} className={tr.theme} style={hubStyles.seasonCard} onClick={() => setRoute({ page:'tournament', id:tr.id })}>
                <div style={{ display:'flex', justifyContent:'space-between', alignItems:'flex-start' }}>
                  <div className="eyebrow" style={{ color:'var(--accent)' }}>{String(i+1).padStart(2,'0')}</div>
                  <div className="pill"><span className="dot" style={{ background:'var(--accent)' }} /> {tr.season}</div>
                </div>
                <div className="display" style={{ fontSize: 44, marginTop: 32, lineHeight: 0.95 }}>
                  {tr.title}
                </div>
                <div style={{ color:'var(--fg-2)', fontSize: 13, marginTop: 6 }}>{tr.subtitle}</div>

                <div style={{ marginTop: 28, display:'grid', gridTemplateColumns:'1fr 1fr', gap: 14 }}>
                  <div>
                    <div className="eyebrow" style={{ fontSize:9 }}>Дати</div>
                    <div className="mono" style={{ fontSize:12, marginTop:4 }}>{tr.dates}</div>
                  </div>
                  <div>
                    <div className="eyebrow" style={{ fontSize:9 }}>Команд</div>
                    <div className="mono" style={{ fontSize:12, marginTop:4 }}>{tr.teams}</div>
                  </div>
                </div>

                <div style={{ marginTop: 28, display:'flex', justifyContent:'space-between', alignItems:'center' }}>
                  <div className="mono" style={{ fontSize:11, color:'var(--fg-2)', letterSpacing:'.1em' }}>{tr.tagline.toUpperCase()}</div>
                  <span style={{ color:'var(--accent)' }}><Arrow dir="right" /></span>
                </div>

                <Countdown target={tr.startsAt} accent="var(--accent)" compact />
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Imagery placeholder gallery teaser */}
      <section style={{ padding:'40px 0 100px' }}>
        <div className="container">
          <div className="section-head">
            <div>
              <div className="eyebrow">03 / Архів</div>
              <h2>Минулі турніри</h2>
            </div>
            <button className="btn btn-ghost">Дивитись усе <Arrow /></button>
          </div>
          <div style={hubStyles.galleryGrid}>
            {[
              { h: 240, label: 'OPENING CEREMONY · MAY 2025' },
              { h: 320, label: 'FINAL MATCH · U12' },
              { h: 240, label: 'WINNER PHOTO' },
              { h: 240, label: 'CROWD · TRIBUNES' },
              { h: 320, label: 'GOAL · 89th MIN' },
              { h: 240, label: 'TROPHY HANDOVER' },
            ].map((g, i) => (
              <div key={i} className="placeholder" style={{ height: g.h }} data-label={g.label} />
            ))}
          </div>
        </div>
      </section>

      <Footer setRoute={setRoute} />
    </div>
  );
}

function StatCell({ value, label, hint }) {
  return (
    <div style={hubStyles.statCell}>
      <div style={{ display:'flex', alignItems:'baseline', gap: 6 }}>
        <div className="display mono" style={{ fontSize: 'clamp(54px, 7vw, 96px)', color:'var(--accent)', lineHeight: 0.9 }}>
          <StatNumber value={value} />
        </div>
        <div className="mono" style={{ color:'var(--accent)', fontSize: 22, opacity:0.5 }}>+</div>
      </div>
      <div style={{ marginTop: 14, fontFamily:'var(--f-display)', fontSize: 22, letterSpacing:'.01em' }}>
        {label}
      </div>
      <div className="eyebrow" style={{ marginTop: 6, fontSize: 10 }}>{hint}</div>
    </div>
  );
}

const hubStyles = {
  hero: {
    position:'relative',
    padding: '60px 0 80px',
    minHeight: 720,
    overflow:'hidden',
    cursor: 'grab',
  },
  glow: {
    position:'absolute', inset: 0,
    background: 'radial-gradient(ellipse 60% 50% at 70% 30%, color-mix(in oklab, var(--accent) 22%, transparent), transparent 60%)',
    pointerEvents:'none',
    transition:'background .6s',
  },
  heroEyebrow: { display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom: 60 },
  titleRow: { display:'grid', gridTemplateColumns:'1fr 1fr', gap: 60, alignItems:'center' },
  megaTitle: {
    fontSize: 'clamp(72px, 12vw, 200px)',
    lineHeight: 0.85,
    margin: 0,
    letterSpacing: '0.005em',
  },
  heroCard: {
    position:'relative',
    background:'var(--bg-1)',
    border:'1px solid var(--line)',
    borderRadius: 24,
    padding: 36,
    boxShadow: '0 30px 80px -30px color-mix(in oklab, var(--accent) 35%, transparent)',
    transition: 'transform .25s ease-out',
    overflow:'hidden',
  },
  heroCardInner: { position:'relative', zIndex:2 },
  heroCardDivider: { height:1, background:'var(--line)', margin: '24px 0' },
  heroCardNum: {
    position:'absolute', right: -10, bottom: -40,
    fontFamily:'var(--f-display)', fontSize: 280, lineHeight: 1,
    color:'color-mix(in oklab, var(--accent) 8%, transparent)',
    pointerEvents:'none', zIndex: 1,
  },

  wheel: { display:'flex', gap: 12, marginTop: 60, alignItems:'stretch' },
  wheelTrack: { display:'grid', gridTemplateColumns:'repeat(4, 1fr)', gap: 8, flex: 1 },
  wheelItem: {
    position:'relative', textAlign:'left',
    padding: '16px 18px', background:'var(--bg-1)', border:'1px solid var(--line)',
    borderRadius: 14, cursor:'default', transition:'all .2s',
    display:'flex', flexDirection:'column', alignItems:'flex-start',
    minHeight: 110,
  },
  wheelItemActive: { background:'var(--bg-2)' },
  wheelItemBar: {
    position:'absolute', left: 0, right: 0, bottom: 0, height: 3,
    background:'var(--accent)',
    borderBottomLeftRadius: 14, borderBottomRightRadius: 14,
  },
  wheelBtn: {
    width: 56, background:'var(--bg-1)', border:'1px solid var(--line)',
    color:'var(--fg-0)', borderRadius: 14, cursor:'default',
    display:'flex', alignItems:'center', justifyContent:'center',
  },

  statsGrid: { display:'grid', gridTemplateColumns:'repeat(4, 1fr)', gap: 1, background:'var(--line)', border:'1px solid var(--line)', borderRadius: 20, overflow:'hidden' },
  statCell: { background:'var(--bg-1)', padding: '40px 32px' },

  seasonsRecap: { display:'grid', gridTemplateColumns:'repeat(4, 1fr)', gap: 18 },
  seasonCard: {
    position:'relative', cursor:'default',
    background:'var(--bg-1)', border:'1px solid var(--line)',
    borderRadius: 20, padding: 28,
    transition: 'all .25s',
    minHeight: 360, display:'flex', flexDirection:'column',
  },

  galleryGrid: { display:'grid', gridTemplateColumns:'repeat(3, 1fr)', gap: 18 },
};

window.Hub = Hub;
