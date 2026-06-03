// app.jsx — main app: router + tweaks integration

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "density": "regular",
  "heroBg": "glow",
  "showGrid": true,
  "intro": "Найбільші футбольні турніри Західної України"
}/*EDITMODE-END*/;

function App() {
  const [route, setRoute] = React.useState({ page: 'hub' });
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);

  // Scroll to top on route change
  React.useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'instant' });
  }, [route]);

  // Apply tweaks side-effects
  React.useEffect(() => {
    document.documentElement.style.setProperty('--ui-density',
      t.density === 'compact' ? '0.85' :
      t.density === 'comfy' ? '1.12' : '1'
    );
    document.body.style.setProperty('--show-grid-opacity', t.showGrid ? '0.10' : '0');
    const grid = document.getElementById('grid-toggle-style');
    if (!grid) {
      const s = document.createElement('style');
      s.id = 'grid-toggle-style';
      document.head.appendChild(s);
    }
    document.getElementById('grid-toggle-style').textContent =
      `body::before { opacity: ${t.showGrid ? 0.10 : 0} !important; }`;
  }, [t.density, t.showGrid]);

  let pageEl;
  if (route.page === 'hub') pageEl = <Hub setRoute={setRoute} intro={t.intro} />;
  else if (route.page === 'tournament') pageEl = <TournamentPage id={route.id} setRoute={setRoute} />;
  else if (route.page === 'apply') pageEl = <ApplyPage setRoute={setRoute} presetTournament={route.id} />;
  else pageEl = <Hub setRoute={setRoute} intro={t.intro} />;

  return (
    <>
      {pageEl}

      <TweaksPanel>
        <TweakSection label="Сайт" />
        <TweakRadio label="Сторінка" value={route.page === 'tournament' ? route.id : route.page}
          options={['hub', 'leo-cup', 'leo-cup-autumn', 'ruh-cup', 'ruh-kids-cup', 'apply']}
          onChange={(v) => {
            if (v === 'hub' || v === 'apply') setRoute({ page: v });
            else setRoute({ page: 'tournament', id: v });
          }} />

        <TweakSection label="Стиль" />
        <TweakRadio label="Щільність" value={t.density}
          options={['compact', 'regular', 'comfy']}
          onChange={(v) => setTweak('density', v)} />
        <TweakToggle label="Фонова сітка" value={t.showGrid}
          onChange={(v) => setTweak('showGrid', v)} />
      </TweaksPanel>
    </>
  );
}

// Mount once everything is ready
ReactDOM.createRoot(document.getElementById('root')).render(<App />);
