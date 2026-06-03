// apply.jsx — Application form page
const { useState: useStateAp } = React;

function ApplyPage({ setRoute, presetTournament = null }) {
  const [form, setForm] = useStateAp({
    teamName: '',
    age: '',
    coach: '',
    phone: '',
    email: '',
    tournament: presetTournament || 'leo-cup',
    city: '',
    players: 12,
    note: '',
  });
  const [submitted, setSubmitted] = useStateAp(false);
  const set = (k, v) => setForm(f => ({ ...f, [k]: v }));

  const selected = window.TOURNAMENTS.find(t => t.id === form.tournament) || window.TOURNAMENTS[0];

  if (submitted) {
    return (
      <div className={`page ${selected.theme}`}>
        <Header current="apply" setRoute={setRoute} />
        <section style={{ padding:'120px 0', position:'relative', overflow:'hidden' }}>
          <div style={apStyles.successGlow} />
          <div className="container" style={{ position:'relative', textAlign:'center', maxWidth: 720 }}>
            <div className="eyebrow" style={{ color:'var(--accent)', marginBottom: 20 }}>· ЗАЯВКУ ПРИЙНЯТО ·</div>
            <h1 className="display" style={{ fontSize:'clamp(60px, 9vw, 140px)', lineHeight: 0.9, margin: 0 }}>
              Дякуємо,<br/><span style={{ color:'var(--accent)' }}>{form.teamName || 'команда'}!</span>
            </h1>
            <p style={{ color:'var(--fg-1)', fontSize: 17, marginTop: 30, lineHeight: 1.6 }}>
              Ми зв'яжемося з вами протягом 24 годин для підтвердження участі у турнірі <strong style={{ color:'var(--accent)' }}>{selected.title} · {selected.season} {selected.year}</strong>.
            </p>
            <div style={{ marginTop: 40, display:'flex', gap: 12, justifyContent:'center', flexWrap:'wrap' }}>
              <button className="btn btn-primary" onClick={() => setRoute({ page:'tournament', id: form.tournament })}>
                До сторінки турніру <Arrow />
              </button>
              <button className="btn btn-ghost" onClick={() => { setSubmitted(false); setRoute({ page:'hub' }); }}>На головну</button>
            </div>
          </div>
        </section>
        <Footer setRoute={setRoute} />
      </div>
    );
  }

  return (
    <div className={`page ${selected.theme}`}>
      <Header current="apply" setRoute={setRoute} />

      <section style={{ padding: '60px 0 40px', position:'relative', overflow:'hidden' }}>
        <div style={apStyles.heroGlow} />
        <div className="container" style={{ position:'relative' }}>
          <div className="eyebrow" style={{ color:'var(--accent)', marginBottom: 16 }}>· ЗАЯВКА КОМАНДИ ·</div>
          <h1 className="display" style={{ fontSize:'clamp(60px, 9vw, 140px)', lineHeight: 0.85, margin: 0 }}>
            Реєструйте<br/><span style={{ color:'var(--accent)' }}>команду</span>
          </h1>
          <p style={{ color:'var(--fg-1)', maxWidth: 540, fontSize: 16, marginTop: 22 }}>
            Заявка приймається лише від офіційних представників школи, академії або клубу. Після подання з вами зв'яжеться менеджер турніру.
          </p>
        </div>
      </section>

      <section style={{ padding: '40px 0 80px' }}>
        <div className="container">
          <div style={apStyles.formGrid}>
            {/* Left: form */}
            <form onSubmit={(e) => { e.preventDefault(); setSubmitted(true); }} style={apStyles.formBox}>
              <div className="eyebrow" style={{ marginBottom: 6 }}>01 / Турнір</div>
              <div className="display" style={{ fontSize: 28, marginBottom: 20 }}>Оберіть подію</div>

              <div style={apStyles.tournamentChoice}>
                {window.TOURNAMENTS.map(t => (
                  <button key={t.id} type="button" onClick={() => set('tournament', t.id)} className={t.theme} style={{
                    ...apStyles.choiceBtn,
                    ...(form.tournament === t.id ? apStyles.choiceBtnActive : {})
                  }}>
                    <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', width:'100%' }}>
                      <span className="eyebrow" style={{ fontSize: 9, color: form.tournament === t.id ? 'var(--accent)' : 'var(--fg-3)' }}>
                        {t.season} {t.year}
                      </span>
                      <SeasonIcon season={t.seasonEn} size={14} color={form.tournament === t.id ? 'var(--accent)' : 'var(--fg-3)'} />
                    </div>
                    <div className="display" style={{ fontSize: 18, textAlign:'left', marginTop: 14 }}>{t.title}</div>
                    <div style={{ fontSize: 11, color:'var(--fg-2)', textAlign:'left', marginTop: 4 }}>{t.dates}</div>
                  </button>
                ))}
              </div>

              <div style={apStyles.divider} />

              <div className="eyebrow" style={{ marginBottom: 6 }}>02 / Команда</div>
              <div className="display" style={{ fontSize: 28, marginBottom: 20 }}>Дані команди</div>

              <div style={apStyles.fieldRow}>
                <div>
                  <label>Назва команди *</label>
                  <input required value={form.teamName} onChange={e => set('teamName', e.target.value)} placeholder="Напр. ФК «Левеня»" />
                </div>
                <div>
                  <label>Вікова категорія *</label>
                  <select value={form.age} onChange={e => set('age', e.target.value)} required>
                    <option value="">Оберіть</option>
                    {selected.ageGroups.map(a => <option key={a} value={a}>{a}</option>)}
                  </select>
                </div>
              </div>

              <div style={apStyles.fieldRow}>
                <div>
                  <label>Місто *</label>
                  <input required value={form.city} onChange={e => set('city', e.target.value)} placeholder="Львів" />
                </div>
                <div>
                  <label>Кількість гравців у заявці</label>
                  <input type="number" min="6" max="22" value={form.players} onChange={e => set('players', e.target.value)} />
                </div>
              </div>

              <div style={apStyles.divider} />

              <div className="eyebrow" style={{ marginBottom: 6 }}>03 / Контактна особа</div>
              <div className="display" style={{ fontSize: 28, marginBottom: 20 }}>Зв'язок</div>

              <div style={apStyles.fieldRow}>
                <div>
                  <label>ПІБ тренера / представника *</label>
                  <input required value={form.coach} onChange={e => set('coach', e.target.value)} placeholder="Іван Іваненко" />
                </div>
                <div>
                  <label>Телефон *</label>
                  <input required type="tel" value={form.phone} onChange={e => set('phone', e.target.value)} placeholder="+38 0__ ___ __ __" />
                </div>
              </div>

              <div style={{ marginBottom: 16 }}>
                <label>E-mail *</label>
                <input required type="email" value={form.email} onChange={e => set('email', e.target.value)} placeholder="coach@school.ua" />
              </div>

              <div style={{ marginBottom: 24 }}>
                <label>Коментар (необов'язково)</label>
                <textarea rows="3" value={form.note} onChange={e => set('note', e.target.value)} placeholder="Особливі побажання, кількість супроводу тощо" style={{ resize:'vertical', fontFamily:'var(--f-body)' }} />
              </div>

              <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', flexWrap:'wrap', gap: 12 }}>
                <div style={{ fontSize: 12, color:'var(--fg-2)', maxWidth: 320 }}>
                  Натискаючи кнопку, ви погоджуєтесь з регламентом турніру та правилами обробки персональних даних.
                </div>
                <button type="submit" className="btn btn-primary">Подати заявку <Arrow /></button>
              </div>
            </form>

            {/* Right: summary aside */}
            <aside style={apStyles.aside}>
              <div className="eyebrow" style={{ marginBottom: 16 }}>Ваш вибір</div>
              <div className="display" style={{ fontSize: 36, lineHeight: 0.95, color:'var(--accent)' }}>
                {selected.title}
              </div>
              <div style={{ fontSize: 13, color:'var(--fg-2)', marginTop: 6 }}>
                {selected.subtitle} · {selected.season} {selected.year}
              </div>

              <div style={apStyles.asideInfo}>
                <div style={apStyles.asideRow}><span>Дати</span><span className="mono">{selected.dates}</span></div>
                <div style={apStyles.asideRow}><span>Локація</span><span className="mono">{selected.location}</span></div>
                <div style={apStyles.asideRow}><span>Формат</span><span className="mono">{selected.format}</span></div>
                <div style={apStyles.asideRow}><span>Команд</span><span className="mono">{selected.teams}</span></div>
                <div style={apStyles.asideRow}><span>Вікові групи</span><span className="mono" style={{ textAlign:'right', maxWidth: 150 }}>{selected.ageGroups.join(', ')}</span></div>
              </div>

              <div style={apStyles.feeBox}>
                <div className="eyebrow" style={{ fontSize: 10 }}>Внесок за команду</div>
                <div className="display" style={{ fontSize: 48, color:'var(--accent)', marginTop: 4, lineHeight: 1 }}>
                  {selected.feeUah} <span style={{ fontSize: 22 }}>₴</span>
                </div>
              </div>

              <div style={apStyles.contactBlock}>
                <div className="eyebrow" style={{ marginBottom: 12, fontSize: 10 }}>Потрібна консультація?</div>
                <div className="mono" style={{ fontSize: 14, color:'var(--fg-0)' }}>+38 068 890 28 44</div>
                <div className="mono" style={{ fontSize: 13, color:'var(--fg-1)', marginTop: 4 }}>ruhcupleocup@gmail.com</div>
              </div>

              <div style={apStyles.countdownBox}>
                <div className="eyebrow" style={{ fontSize: 10, marginBottom: 10 }}>До старту турніру</div>
                <Countdown target={selected.startsAt} compact />
              </div>
            </aside>
          </div>
        </div>
      </section>

      <Footer setRoute={setRoute} />
    </div>
  );
}

const apStyles = {
  heroGlow: { position:'absolute', inset: 0, background:'radial-gradient(ellipse 50% 40% at 20% 30%, color-mix(in oklab, var(--accent) 18%, transparent), transparent 60%)' },
  successGlow: { position:'absolute', inset: 0, background:'radial-gradient(ellipse 60% 60% at 50% 40%, color-mix(in oklab, var(--accent) 22%, transparent), transparent 60%)' },

  formGrid: { display:'grid', gridTemplateColumns:'1.5fr 1fr', gap: 28, alignItems:'flex-start' },
  formBox: {
    background:'var(--bg-1)', border:'1px solid var(--line)', borderRadius: 24,
    padding: 40,
  },
  tournamentChoice: { display:'grid', gridTemplateColumns:'repeat(2, 1fr)', gap: 10, marginBottom: 6 },
  choiceBtn: {
    background:'var(--bg-2)', border:'1.5px solid var(--line)', borderRadius: 12,
    padding: 16, cursor:'default', display:'flex', flexDirection:'column',
    alignItems:'flex-start', transition: 'all .2s',
  },
  choiceBtnActive: {
    background:'color-mix(in oklab, var(--accent) 8%, var(--bg-2))',
    borderColor:'var(--accent)',
  },

  divider: { height: 1, background:'var(--line)', margin:'34px 0 30px' },
  fieldRow: { display:'grid', gridTemplateColumns:'1fr 1fr', gap: 18, marginBottom: 16 },

  aside: {
    position:'sticky', top: 96,
    background:'var(--bg-1)', border:'1px solid var(--line)', borderRadius: 24,
    padding: 32,
  },
  asideInfo: { margin: '24px 0', display:'flex', flexDirection:'column', gap: 14, paddingTop: 22, borderTop:'1px solid var(--line)' },
  asideRow: { display:'flex', justifyContent:'space-between', alignItems:'flex-start', fontSize: 13, color:'var(--fg-1)', gap: 12 },
  feeBox: { padding: 20, background:'var(--bg-2)', border:'1px solid var(--line)', borderRadius: 14, marginBottom: 18 },
  contactBlock: { padding: '18px 0 0', borderTop:'1px solid var(--line)' },
  countdownBox: { marginTop: 22, paddingTop: 22, borderTop:'1px solid var(--line)' },
};

window.ApplyPage = ApplyPage;
