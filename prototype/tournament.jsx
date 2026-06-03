// tournament.jsx — Tournament detail page
const { useState: useStateTr, useMemo: useMemoTr, useEffect: useEffectTr } = React;

function TournamentPage({ id, setRoute }) {
  const t = window.TOURNAMENTS.find(x => x.id === id);
  if (!t) return null;

  const bracket = useMemoTr(() => window.makeBracket(window.TOURNAMENTS.findIndex(x => x.id === id) * 2), [id]);
  const schedule = useMemoTr(() => window.makeSchedule(), [id]);

  return (
    <div className={`page ${t.theme}`}>
      <Header current={t.id} setRoute={setRoute} />

      <TrHero t={t} setRoute={setRoute} />
      <TrAbout t={t} />
      <TrBracket bracket={bracket} t={t} />
      <TrSchedule schedule={schedule} t={t} />
      <TrStats t={t} />
      <TrTeams t={t} />
      <TrGallery t={t} />
      <TrCta t={t} setRoute={setRoute} />

      <Footer setRoute={setRoute} />
    </div>
  );
}

/* ───── HERO ───── */
function TrHero({ t, setRoute }) {
  const idx = window.TOURNAMENTS.findIndex(x => x.id === t.id);
  return (
    <section style={trStyles.hero}>
      <div style={trStyles.heroGlow} />

      <div className="container" style={{ position:'relative', zIndex:2 }}>
        {/* Breadcrumb */}
        <div style={{ display:'flex', alignItems:'center', gap: 12, marginBottom: 30 }}>
          <a onClick={() => setRoute({ page:'hub' })} className="mono" style={{ color:'var(--fg-2)', fontSize:11, letterSpacing:'.14em', cursor:'default' }}>
            ГОЛОВНА
          </a>
          <span style={{ color:'var(--fg-3)' }}>/</span>
          <span className="mono" style={{ color:'var(--accent)', fontSize:11, letterSpacing:'.14em' }}>
            {t.title.toUpperCase()} · {t.season.toUpperCase()} {t.year}
          </span>
        </div>

        <div style={trStyles.heroGrid}>
          <div>
            <div className="eyebrow" style={{ color:'var(--accent)', marginBottom: 18 }}>
              <span className="live-dot" style={{ display:'inline-block', verticalAlign:'middle', marginRight: 8 }} />
              {String(idx+1).padStart(2,'0')} / 04 · {t.season.toUpperCase()} {t.year}
            </div>

            <h1 className="display" style={trStyles.title}>
              {t.title.split(' ').map((w, i) => (
                <span key={i} style={{ display:'block', color: i === 0 ? 'var(--fg-0)' : 'var(--accent)' }}>{w}</span>
              ))}
            </h1>

            <div style={{ display:'flex', gap: 8, marginTop: 22, flexWrap:'wrap' }}>
              <div className="pill accent">{t.dates}</div>
              <div className="pill">{t.location}</div>
              <div className="pill">{t.format}</div>
            </div>

            <p style={{ fontSize: 17, color:'var(--fg-1)', maxWidth: 540, marginTop: 24, lineHeight: 1.55 }}>
              {t.description}
            </p>

            <div style={{ marginTop: 30, display:'flex', gap:12, flexWrap:'wrap' }}>
              <button className="btn btn-primary" onClick={() => setRoute({ page:'apply' })}>
                Подати заявку команди <Arrow />
              </button>
              <button className="btn btn-ghost">
                Регламент турніру
              </button>
            </div>
          </div>

          {/* Right column: visual + countdown */}
          <div>
            <div style={trStyles.heroVisualWrap}>
              <div className="placeholder" style={{ height: 380, borderRadius: 22 }} data-label={`${t.title} · KEY ART`} />
              <div style={trStyles.heroVisualTag}>
                <span className="live-dot" />
                <span className="mono" style={{ fontSize: 10, letterSpacing:'.16em' }}>{t.iconHint}</span>
              </div>
              <div style={trStyles.heroVisualPrize}>
                <div className="eyebrow" style={{ fontSize:9 }}>Призовий</div>
                <div className="display" style={{ fontSize: 28, color:'var(--accent)', lineHeight: 1 }}>
                  ТОР-3 + MVP
                </div>
              </div>
            </div>

            <div style={trStyles.heroCountdown}>
              <div className="eyebrow" style={{ marginBottom: 12 }}>До старту турніру</div>
              <Countdown target={t.startsAt} />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ───── ABOUT ───── */
function TrAbout({ t }) {
  const facts = [
    { label: 'Вікові групи', value: t.ageGroups.join(' · ') },
    { label: 'Формат', value: t.format },
    { label: 'Локація', value: t.location },
    { label: 'Внесок', value: `${t.feeUah} ₴ за команду` },
    { label: 'Нагороди', value: t.prize },
    { label: 'Тривалість', value: '3 дні · ранок до вечора' },
  ];
  return (
    <section style={{ padding: '100px 0 60px' }}>
      <div className="container">
        <div className="section-head">
          <div>
            <div className="eyebrow">01 / Про турнір</div>
            <h2>{t.tagline}.</h2>
          </div>
          <div style={{ maxWidth: 380, color:'var(--fg-2)', fontSize: 14, lineHeight: 1.6 }}>
            {t.highlight}. Участь у турнірі — це досвід, який залишиться з гравцями на все життя.
          </div>
        </div>

        <div style={trStyles.aboutGrid}>
          {facts.map((f, i) => (
            <div key={i} style={trStyles.factCell}>
              <div className="eyebrow" style={{ fontSize: 10 }}>{f.label}</div>
              <div style={{ marginTop: 10, fontSize: 16, fontWeight: 500, color:'var(--fg-0)' }}>{f.value}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ───── BRACKET ───── */
function TrBracket({ bracket, t }) {
  return (
    <section style={{ padding: '60px 0' }}>
      <div className="container">
        <div className="section-head">
          <div>
            <div className="eyebrow">02 / Сітка турніру</div>
            <h2>Сітка <span style={{ color:'var(--accent)' }}>play-off</span></h2>
          </div>
          <div style={{ display:'flex', gap:10 }}>
            <div className="pill">U-12 · ОСНОВНА СІТКА</div>
            <button className="btn btn-ghost" style={{ padding:'10px 16px', fontSize: 12 }}>Інші вікові групи</button>
          </div>
        </div>

        <div style={trStyles.bracketWrap}>
          {/* Round 1: 4 matches */}
          <BracketRound title="1/4 фіналу" matches={bracket.r16} />
          {/* Round 2: 2 matches */}
          <BracketRound title="1/2 фіналу" matches={bracket.sf} />
          {/* Final */}
          <BracketRound title="Фінал" matches={[bracket.final]} isFinal />
        </div>
      </div>
    </section>
  );
}

function BracketRound({ title, matches, isFinal = false }) {
  return (
    <div style={trStyles.bracketCol}>
      <div className="eyebrow" style={{ marginBottom: 16, color:'var(--accent)' }}>{title}</div>
      <div style={{ display:'flex', flexDirection:'column', justifyContent:'space-around', gap: 16, flex: 1 }}>
        {matches.map((m, i) => <BracketMatch key={i} m={m} isFinal={isFinal} />)}
      </div>
    </div>
  );
}

function BracketMatch({ m, isFinal }) {
  const aWin = m.sA !== '–' && m.sB !== '–' && m.sA > m.sB && m.status === 'finished';
  const bWin = m.sA !== '–' && m.sB !== '–' && m.sB > m.sA && m.status === 'finished';
  return (
    <div style={{...trStyles.match, ...(isFinal ? trStyles.matchFinal : {}), ...(m.status === 'live' ? trStyles.matchLive : {})}}>
      {m.status === 'live' && (
        <div style={trStyles.liveTag}><span className="live-dot" /> LIVE</div>
      )}
      {isFinal && (
        <div style={trStyles.finalTag}>
          <BallIcon size={14} color="var(--accent)" />
          <span className="mono" style={{ fontSize: 10, letterSpacing:'.14em', color:'var(--accent)' }}>FINAL</span>
        </div>
      )}
      <BracketTeam team={m.a} score={m.sA} win={aWin} />
      <div style={trStyles.matchDivider} />
      <BracketTeam team={m.b} score={m.sB} win={bWin} />
    </div>
  );
}

function BracketTeam({ team, score, win }) {
  return (
    <div style={trStyles.teamRow}>
      <div style={{ display:'flex', alignItems:'center', gap: 10, flex:1, minWidth:0 }}>
        <div style={{ ...trStyles.teamLogo, color: win ? 'var(--accent)' : 'var(--fg-2)' }}>
          {team.short}
        </div>
        <div style={{ minWidth:0 }}>
          <div style={{ fontSize: 13, fontWeight: 600, color: win ? 'var(--fg-0)' : 'var(--fg-1)', overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap' }}>
            {team.name}
          </div>
          <div className="mono" style={{ fontSize: 10, color:'var(--fg-3)', letterSpacing:'.06em' }}>{team.city.toUpperCase()}</div>
        </div>
      </div>
      <div className="display mono" style={{ fontSize: 22, color: win ? 'var(--accent)' : 'var(--fg-1)', minWidth: 24, textAlign:'right' }}>
        {score}
      </div>
    </div>
  );
}

/* ───── SCHEDULE ───── */
function TrSchedule({ schedule, t }) {
  const [day, setDay] = useStateTr(2);
  const dayMatches = schedule.filter(m => m.day === day);
  return (
    <section style={{ padding: '60px 0' }}>
      <div className="container">
        <div className="section-head">
          <div>
            <div className="eyebrow">03 / Розклад</div>
            <h2>Розклад матчів</h2>
          </div>
          <div style={trStyles.daySwitcher}>
            {[1,2,3].map(d => (
              <button key={d} onClick={() => setDay(d)} style={{
                ...trStyles.dayBtn,
                ...(day === d ? trStyles.dayBtnActive : {})
              }}>
                День {d}
                <span className="mono" style={{ fontSize: 10, color: day === d ? 'oklch(0.2 0.01 250)' : 'var(--fg-3)' }}>
                  {d === 1 ? '15.05' : d === 2 ? '16.05' : '17.05'}
                </span>
              </button>
            ))}
          </div>
        </div>

        <div style={trStyles.scheduleList}>
          <div style={trStyles.scheduleHead}>
            <div>Час</div><div>Поле</div><div>Команди</div><div>Група</div><div>Рахунок</div><div>Статус</div>
          </div>
          {dayMatches.map((m, i) => (
            <div key={i} style={trStyles.scheduleRow}>
              <div className="mono" style={{ fontSize: 14, color:'var(--fg-0)' }}>{m.time}</div>
              <div className="mono" style={{ fontSize: 12, color:'var(--fg-2)' }}>{m.field}</div>
              <div style={{ display:'flex', alignItems:'center', gap: 8 }}>
                <span style={trStyles.miniLogo}>{m.a.short}</span>
                <span style={{ fontSize: 13 }}>{m.a.name}</span>
                <span style={{ color:'var(--fg-3)', margin:'0 6px' }}>vs</span>
                <span style={trStyles.miniLogo}>{m.b.short}</span>
                <span style={{ fontSize: 13 }}>{m.b.name}</span>
              </div>
              <div><div className="pill" style={{ padding:'3px 8px' }}>{m.age}</div></div>
              <div className="display mono" style={{ fontSize: 18 }}>
                {m.sA !== null ? `${m.sA} : ${m.sB}` : <span style={{ color:'var(--fg-3)' }}>—</span>}
              </div>
              <div>
                {m.status === 'live' && <span style={{ display:'flex', alignItems:'center', gap: 6, color:'var(--accent)', fontSize: 12, fontWeight: 600 }}><span className="live-dot" /> LIVE</span>}
                {m.status === 'finished' && <span className="mono" style={{ fontSize: 11, color:'var(--fg-2)', letterSpacing:'.1em' }}>ЗАВЕРШЕНО</span>}
                {m.status === 'upcoming' && <span className="mono" style={{ fontSize: 11, color:'var(--fg-3)', letterSpacing:'.1em' }}>СКОРО</span>}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ───── STATS ───── */
function TrStats({ t }) {
  return (
    <section style={{ padding: '60px 0' }}>
      <div className="container">
        <div className="section-head">
          <div>
            <div className="eyebrow">04 / Статистика</div>
            <h2>Цифри турніру</h2>
          </div>
          <div style={{ color:'var(--fg-2)', fontSize: 14, maxWidth: 320 }}>
            Дані оновлюються в реальному часі під час турніру.
          </div>
        </div>

        <div style={trStyles.statsRow}>
          <div style={trStyles.statBig}>
            <div className="display mono" style={{ fontSize: 'clamp(80px, 12vw, 160px)', color:'var(--accent)', lineHeight: 0.85 }}>
              <StatNumber value={t.teams} />
            </div>
            <div className="display" style={{ fontSize: 22 }}>команд</div>
            <div className="eyebrow" style={{ marginTop: 8, fontSize: 10 }}>TEAMS REGISTERED</div>
          </div>
          <div style={trStyles.statBig}>
            <div className="display mono" style={{ fontSize: 'clamp(80px, 12vw, 160px)', color:'var(--accent)', lineHeight: 0.85 }}>
              <StatNumber value={t.matches} />
            </div>
            <div className="display" style={{ fontSize: 22 }}>матчів</div>
            <div className="eyebrow" style={{ marginTop: 8, fontSize: 10 }}>SCHEDULED MATCHES</div>
          </div>
          <div style={trStyles.statBig}>
            <div className="display mono" style={{ fontSize: 'clamp(80px, 12vw, 160px)', color:'var(--accent)', lineHeight: 0.85 }}>
              <StatNumber value={t.goals} />
            </div>
            <div className="display" style={{ fontSize: 22 }}>голів</div>
            <div className="eyebrow" style={{ marginTop: 8, fontSize: 10 }}>TOTAL GOALS</div>
          </div>
        </div>

        <div style={trStyles.scorers}>
          <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom: 22 }}>
            <div>
              <div className="eyebrow" style={{ marginBottom: 6 }}>Бомбардири</div>
              <div className="display" style={{ fontSize: 32 }}>Top Scorers</div>
            </div>
            <div className="pill">U-12 · {t.season.toUpperCase()} {t.year}</div>
          </div>

          <div style={trStyles.scorersList}>
            {window.TOP_SCORERS.map((s, i) => (
              <div key={i} style={trStyles.scorerRow}>
                <div className="display mono" style={{ fontSize: 32, width: 44, color: i === 0 ? 'var(--accent)' : 'var(--fg-2)' }}>
                  {String(i+1).padStart(2,'0')}
                </div>
                <div style={{ flex:1 }}>
                  <div style={{ fontSize: 15, fontWeight: 600 }}>{s.name}</div>
                  <div className="mono" style={{ fontSize: 11, color:'var(--fg-2)', letterSpacing:'.06em' }}>{s.team.toUpperCase()} · {s.age}</div>
                </div>
                <div style={{ display:'flex', alignItems:'center', gap: 10 }}>
                  <div style={trStyles.goalBar}>
                    <div style={{ width: `${(s.goals / 14) * 100}%`, height:'100%', background:'var(--accent)', borderRadius: 2 }} />
                  </div>
                  <div className="display mono" style={{ fontSize: 26, color: i === 0 ? 'var(--accent)' : 'var(--fg-0)', width: 44, textAlign:'right' }}>
                    {s.goals}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

/* ───── TEAMS ───── */
function TrTeams({ t }) {
  const teams = window.TEAMS_POOL.slice(0, 16);
  return (
    <section style={{ padding: '60px 0' }}>
      <div className="container">
        <div className="section-head">
          <div>
            <div className="eyebrow">05 / Учасники</div>
            <h2>{teams.length} команд-учасниць</h2>
          </div>
          <div style={{ display:'flex', gap:8 }}>
            <div className="pill accent">УСІ</div>
            {t.ageGroups.slice(0, 4).map(a => <div key={a} className="pill">{a}</div>)}
          </div>
        </div>

        <div style={trStyles.teamsGrid}>
          {teams.map((tm, i) => (
            <div key={i} style={trStyles.teamCard}>
              <div style={trStyles.teamCardLogo}>{tm.short}</div>
              <div style={{ flex:1, minWidth: 0 }}>
                <div style={{ fontSize: 14, fontWeight: 600, color:'var(--fg-0)' }}>{tm.name}</div>
                <div className="mono" style={{ fontSize: 11, color:'var(--fg-2)', letterSpacing:'.06em', marginTop: 2 }}>
                  {tm.city.toUpperCase()}
                </div>
              </div>
              <div className="mono" style={{ fontSize: 11, color:'var(--fg-3)', letterSpacing:'.1em' }}>
                #{String(i+1).padStart(2,'0')}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ───── GALLERY ───── */
function TrGallery({ t }) {
  return (
    <section style={{ padding: '60px 0' }}>
      <div className="container">
        <div className="section-head">
          <div>
            <div className="eyebrow">06 / Галерея</div>
            <h2>Минулі сезони</h2>
          </div>
          <button className="btn btn-ghost">Архів повністю <Arrow /></button>
        </div>

        <div style={trStyles.galleryGrid}>
          <div className="placeholder" style={{ gridColumn: 'span 2', gridRow: 'span 2', minHeight: 460 }} data-label={`${t.title} · FINAL ${parseInt(t.year)-1}`} />
          <div className="placeholder" style={{ minHeight: 220 }} data-label="TEAM PHOTO" />
          <div className="placeholder" style={{ minHeight: 220 }} data-label="GOAL CELEBRATION" />
          <div className="placeholder" style={{ minHeight: 220 }} data-label="WINNER CUP" />
          <div className="placeholder" style={{ minHeight: 220 }} data-label="CROWD" />
        </div>
      </div>
    </section>
  );
}

/* ───── CTA ───── */
function TrCta({ t, setRoute }) {
  return (
    <section style={{ padding: '100px 0 40px' }}>
      <div className="container">
        <div style={trStyles.cta}>
          <div style={trStyles.ctaGlow} />
          <div style={{ position:'relative', zIndex: 2, display:'grid', gridTemplateColumns:'1.5fr 1fr', gap: 40, alignItems:'center' }}>
            <div>
              <div className="eyebrow" style={{ color:'var(--accent)', marginBottom: 16 }}>07 / Заявка</div>
              <div className="display" style={{ fontSize: 'clamp(48px, 7vw, 96px)', lineHeight: 0.9 }}>
                Готові вийти<br/>на поле?
              </div>
              <div style={{ color:'var(--fg-1)', marginTop: 20, fontSize: 16, maxWidth: 480, lineHeight: 1.55 }}>
                Заявки приймаються від офіційних представників школи або клубу. Реєстрація закривається за 14 днів до старту турніру.
              </div>
              <div style={{ marginTop: 30, display:'flex', gap: 12, flexWrap:'wrap' }}>
                <button className="btn btn-primary" onClick={() => setRoute({ page:'apply' })}>Подати заявку <Arrow /></button>
                <button className="btn btn-ghost">Завантажити регламент</button>
              </div>
            </div>
            <div>
              <div className="eyebrow" style={{ marginBottom: 14 }}>До закриття реєстрації</div>
              <Countdown target={t.startsAt} compact />
              <div style={{ marginTop: 24, padding: 18, background:'var(--bg-2)', border:'1px solid var(--line)', borderRadius: 14 }}>
                <div className="eyebrow" style={{ fontSize: 10 }}>Внесок за команду</div>
                <div className="display" style={{ fontSize: 40, color:'var(--accent)', marginTop: 4 }}>{t.feeUah} ₴</div>
                <div style={{ color:'var(--fg-2)', fontSize: 12, marginTop: 4 }}>включно з нагородами, медалями та оргвитратами</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

const trStyles = {
  hero: { position:'relative', padding:'40px 0 80px', overflow:'hidden' },
  heroGlow: {
    position:'absolute', inset: 0,
    background:'radial-gradient(ellipse 50% 40% at 80% 20%, color-mix(in oklab, var(--accent) 18%, transparent), transparent 60%)',
  },
  heroGrid: { display:'grid', gridTemplateColumns:'1.1fr 1fr', gap: 60, alignItems:'center' },
  title: {
    fontSize:'clamp(80px, 12vw, 180px)',
    lineHeight: 0.85, margin: 0,
  },
  heroVisualWrap: { position:'relative' },
  heroVisualTag: {
    position:'absolute', top: 18, left: 18,
    display:'flex', alignItems:'center', gap: 8,
    padding: '8px 12px',
    background:'oklch(0.13 0.01 250 / .8)', backdropFilter:'blur(10px)',
    border:'1px solid var(--line)', borderRadius: 999,
    color:'var(--accent)',
  },
  heroVisualPrize: {
    position:'absolute', bottom: 18, right: 18,
    padding: 16, background:'oklch(0.13 0.01 250 / .85)', backdropFilter:'blur(10px)',
    border:'1px solid var(--line-strong)', borderRadius: 14,
  },
  heroCountdown: { marginTop: 28 },

  aboutGrid: { display:'grid', gridTemplateColumns:'repeat(3, 1fr)', gap: 1, background:'var(--line)', border:'1px solid var(--line)', borderRadius: 20, overflow:'hidden' },
  factCell: { background:'var(--bg-1)', padding: '24px 26px', minHeight: 110 },

  bracketWrap: { display:'grid', gridTemplateColumns:'repeat(3, 1fr)', gap: 28, background:'var(--bg-1)', border:'1px solid var(--line)', borderRadius: 20, padding: 30, minHeight: 540 },
  bracketCol: { display:'flex', flexDirection:'column' },
  match: {
    position:'relative',
    background:'var(--bg-2)', border:'1px solid var(--line)',
    borderRadius: 12, padding: '14px 16px',
    display:'flex', flexDirection:'column', gap: 4,
    transition: 'border-color .2s',
  },
  matchFinal: {
    background:'color-mix(in oklab, var(--accent) 8%, var(--bg-2))',
    border:'1px solid color-mix(in oklab, var(--accent) 50%, transparent)',
  },
  matchLive: { border:'1px solid var(--accent)' },
  liveTag: {
    position:'absolute', top: -10, right: 12,
    display:'flex', alignItems:'center', gap: 6,
    padding: '3px 9px', background:'var(--bg-0)', border:'1px solid var(--accent)',
    borderRadius: 999, color:'var(--accent)', fontSize: 10, fontWeight: 700, letterSpacing:'.14em',
  },
  finalTag: {
    position:'absolute', top: -10, left: 12,
    display:'flex', alignItems:'center', gap: 6,
    padding:'3px 10px', background:'var(--bg-0)', border:'1px solid var(--accent)',
    borderRadius: 999,
  },
  teamRow: { display:'flex', alignItems:'center', justifyContent:'space-between', gap: 12, padding: '6px 0' },
  teamLogo: {
    width: 36, height: 36, borderRadius: 8,
    background:'var(--bg-0)', border:'1px solid var(--line)',
    display:'flex', alignItems:'center', justifyContent:'center',
    fontFamily:'var(--f-mono)', fontSize: 11, letterSpacing:'.02em',
    flexShrink: 0,
  },
  matchDivider: { height: 1, background:'var(--line)', margin:'2px 0' },

  daySwitcher: { display:'flex', gap: 4, padding: 4, background:'var(--bg-1)', border:'1px solid var(--line)', borderRadius: 10 },
  dayBtn: {
    display:'flex', alignItems:'center', gap: 10,
    padding:'9px 16px', borderRadius: 7,
    background:'transparent', border:'none', color:'var(--fg-1)',
    fontSize: 13, fontWeight: 500, cursor:'default',
  },
  dayBtnActive: { background:'var(--accent)', color:'oklch(0.18 0.01 250)' },

  scheduleList: { background:'var(--bg-1)', border:'1px solid var(--line)', borderRadius: 16, overflow:'hidden' },
  scheduleHead: {
    display:'grid', gridTemplateColumns:'70px 110px 1fr 110px 90px 110px', gap: 16,
    padding:'14px 22px', background:'var(--bg-2)', borderBottom:'1px solid var(--line)',
    fontFamily:'var(--f-mono)', fontSize: 10, letterSpacing:'.14em', textTransform:'uppercase', color:'var(--fg-2)',
  },
  scheduleRow: {
    display:'grid', gridTemplateColumns:'70px 110px 1fr 110px 90px 110px', gap: 16,
    padding:'16px 22px', alignItems:'center',
    borderBottom:'1px solid var(--line)',
  },
  miniLogo: {
    width: 28, height: 28, borderRadius: 6,
    background:'var(--bg-2)', border:'1px solid var(--line)',
    display:'inline-flex', alignItems:'center', justifyContent:'center',
    fontFamily:'var(--f-mono)', fontSize: 9, letterSpacing:'0',
    flexShrink: 0,
  },

  statsRow: { display:'grid', gridTemplateColumns:'repeat(3, 1fr)', gap: 1, background:'var(--line)', border:'1px solid var(--line)', borderRadius: 20, overflow:'hidden' },
  statBig: { background:'var(--bg-1)', padding: '50px 36px' },

  scorers: { marginTop: 40 },
  scorersList: { display:'flex', flexDirection:'column', gap: 2, background:'var(--line)', border:'1px solid var(--line)', borderRadius: 16, overflow:'hidden' },
  scorerRow: {
    display:'flex', alignItems:'center', gap: 18,
    padding: '18px 24px', background:'var(--bg-1)',
  },
  goalBar: { width: 140, height: 4, background:'var(--bg-3)', borderRadius: 2, overflow:'hidden' },

  teamsGrid: { display:'grid', gridTemplateColumns:'repeat(4, 1fr)', gap: 12 },
  teamCard: {
    display:'flex', alignItems:'center', gap: 14,
    padding: '16px 18px',
    background:'var(--bg-1)', border:'1px solid var(--line)', borderRadius: 12,
    transition:'border-color .2s',
  },
  teamCardLogo: {
    width: 42, height: 42, borderRadius: 8,
    background:'var(--bg-2)', border:'1px solid var(--line)',
    display:'flex', alignItems:'center', justifyContent:'center',
    fontFamily:'var(--f-mono)', fontSize: 12, color:'var(--accent)', fontWeight: 600,
    flexShrink: 0,
  },

  galleryGrid: { display:'grid', gridTemplateColumns:'repeat(4, 1fr)', gap: 14 },

  cta: {
    position:'relative', overflow:'hidden',
    background:'var(--bg-1)', border:'1px solid var(--line)',
    borderRadius: 28, padding: 60,
  },
  ctaGlow: {
    position:'absolute', inset: 0,
    background:'radial-gradient(circle at 90% 50%, color-mix(in oklab, var(--accent) 22%, transparent), transparent 60%)',
  },
};

window.TournamentPage = TournamentPage;
