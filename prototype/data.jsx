// Tournament data — 4 seasons.
// Pure data, exposed via window.TOURNAMENTS so all jsx scripts share it.

const TOURNAMENTS = [
  {
    id: 'leo-cup',
    title: 'LEO CUP',
    subtitle: 'Spring Edition',
    season: 'Весна',
    seasonEn: 'Spring',
    year: '2026',
    theme: 'theme-spring',
    accent: 'var(--spring)',
    iconHint: 'GRASS · LIME',
    dates: '15 — 17 травня 2026',
    startsAt: '2026-05-15T09:00:00+03:00',
    location: 'СК «Сокіл», Львів',
    teams: 64,
    matches: 96,
    goals: 412,
    ageGroups: ['U-8', 'U-9', 'U-10', 'U-11', 'U-12', 'U-13'],
    format: '8+1, два тайми по 20 хв',
    prize: 'Кубки + медалі + індивідуальні нагороди',
    feeUah: '4 200',
    description: 'Найбільший весняний турнір серед дитячих футбольних шкіл Західної України. Понад 600 юних футболістів виходять на поле під відкритим небом.',
    highlight: 'Понад 600 учасників щорічно',
    tagline: 'Свято весняного футболу',
  },
  {
    id: 'leo-cup-autumn',
    title: 'LEO CUP',
    subtitle: 'Autumn Edition',
    season: 'Осінь',
    seasonEn: 'Autumn',
    year: '2026',
    theme: 'theme-autumn',
    accent: 'var(--autumn)',
    iconHint: 'AMBER · LEAVES',
    dates: '10 — 12 жовтня 2026',
    startsAt: '2026-10-10T09:00:00+03:00',
    location: 'СК «Сокіл», Львів',
    teams: 48,
    matches: 72,
    goals: 318,
    ageGroups: ['U-7', 'U-8', 'U-9', 'U-10', 'U-11'],
    format: '6+1, два тайми по 20 хв',
    prize: 'Кубки + медалі + MVP турніру',
    feeUah: '4 000',
    description: 'Осіння серія Leo Cup — фінальний турнір сезону на природному газоні. Зустріч найсильніших шкіл Львова, Києва, Тернополя та Івано-Франківська.',
    highlight: 'Фінал сезону наживо',
    tagline: 'Підсумок року на полі',
  },
  {
    id: 'ruh-cup',
    title: 'RUH CUP',
    subtitle: 'Winter Edition',
    season: 'Зима',
    seasonEn: 'Winter',
    year: '2026',
    theme: 'theme-winter',
    accent: 'var(--winter)',
    iconHint: 'ICE · BLUE',
    dates: '23 — 25 січня 2026',
    startsAt: '2026-01-23T09:00:00+03:00',
    location: 'Манеж РУХ, Львів',
    teams: 40,
    matches: 64,
    goals: 287,
    ageGroups: ['U-13', 'U-14', 'U-15', 'U-16', 'U-17'],
    format: '5+1, два тайми по 15 хв',
    prize: 'Кубок RUH + персональні нагороди',
    feeUah: '4 500',
    description: 'Зимовий турнір під дахом для старших вікових груп. Швидкий, технічний футбол у манежі — справжній іспит майстерності.',
    highlight: 'Топ-академії країни',
    tagline: 'Майстерність під дахом',
  },
  {
    id: 'ruh-kids-cup',
    title: 'RUH KIDS CUP',
    subtitle: 'Winter Kids',
    season: 'Зима',
    seasonEn: 'Winter',
    year: '2026',
    theme: 'theme-kids',
    accent: 'var(--kids)',
    iconHint: 'FIRE · RED',
    dates: '6 — 8 лютого 2026',
    startsAt: '2026-02-06T09:00:00+03:00',
    location: 'Манеж РУХ, Львів',
    teams: 56,
    matches: 84,
    goals: 364,
    ageGroups: ['U-6', 'U-7', 'U-8', 'U-9'],
    format: '4+1, два тайми по 12 хв',
    prize: 'Медалі всім + кубки фіналістам',
    feeUah: '3 800',
    description: 'Турнір для наймолодших — перші великі змагання у житті. Безпечне поле, дружня атмосфера, фотограф і відеограф для кожної команди.',
    highlight: 'Перший турнір для малечі',
    tagline: 'Перші перемоги',
  },
];

// Sample teams (used across pages — varied composition feels real)
const TEAMS_POOL = [
  { name: 'РУХ', city: 'Львів', short: 'РУХ' },
  { name: 'Карпати', city: 'Львів', short: 'КАР' },
  { name: 'ЛНУ Академія', city: 'Львів', short: 'ЛНУ' },
  { name: 'Левеня', city: 'Львів', short: 'ЛЕВ' },
  { name: 'Динамо', city: 'Київ', short: 'ДИН' },
  { name: 'Шахтар Академія', city: 'Київ', short: 'ШАХ' },
  { name: 'Зоря', city: 'Луганськ', short: 'ЗОР' },
  { name: 'Нива', city: 'Тернопіль', short: 'НИВ' },
  { name: 'Прикарпаття', city: 'Івано-Франківськ', short: 'ПРИ' },
  { name: 'Буковина', city: 'Чернівці', short: 'БУК' },
  { name: 'Волинь', city: 'Луцьк', short: 'ВОЛ' },
  { name: 'Минай', city: 'Ужгород', short: 'МИН' },
  { name: 'Полісся', city: 'Житомир', short: 'ПОЛ' },
  { name: 'Кремінь', city: 'Кременчук', short: 'КРМ' },
  { name: 'Сокіл', city: 'Львів', short: 'СОК' },
  { name: 'Галичина', city: 'Дрогобич', short: 'ГАЛ' },
  { name: 'Бескид', city: 'Стрий', short: 'БЕС' },
  { name: 'Ліга-99', city: 'Львів', short: 'L99' },
  { name: 'Олімпік', city: 'Донецьк', short: 'ОЛІ' },
  { name: 'Юність', city: 'Чернігів', short: 'ЮНІ' },
];

// Bracket (8 teams, single elimination)
function makeBracket(seed = 0) {
  const pick = TEAMS_POOL.slice(seed, seed + 8);
  const r16 = []; // quarterfinals (4 matches)
  for (let i = 0; i < 8; i += 2) {
    const a = pick[i], b = pick[i + 1];
    const sA = Math.floor(Math.random() * 4);
    const sB = sA === 3 ? 1 : Math.floor(Math.random() * 4);
    r16.push({ a, b, sA, sB, status: 'finished' });
  }
  const sf = []; // semifinals
  for (let i = 0; i < 4; i += 2) {
    const wA = r16[i].sA > r16[i].sB ? r16[i].a : r16[i].b;
    const wB = r16[i+1].sA > r16[i+1].sB ? r16[i+1].a : r16[i+1].b;
    const sA = Math.floor(Math.random() * 3);
    const sB = sA === 2 ? 0 : Math.floor(Math.random() * 3);
    sf.push({ a: wA, b: wB, sA, sB, status: i === 0 ? 'live' : 'upcoming' });
  }
  const fA = sf[0].sA > sf[0].sB ? sf[0].a : sf[0].b;
  const fB = sf[1].sA > sf[1].sB ? sf[1].a : sf[1].b;
  const final = { a: fA, b: fB, sA: '–', sB: '–', status: 'upcoming' };
  return { r16, sf, final };
}

// Top scorers
const TOP_SCORERS = [
  { name: 'Назар Кравченко', team: 'РУХ', age: 'U-12', goals: 14 },
  { name: 'Артем Стеценко', team: 'Карпати', age: 'U-12', goals: 12 },
  { name: 'Микита Шевчук', team: 'Динамо', age: 'U-11', goals: 11 },
  { name: 'Олексій Ткач', team: 'Левеня', age: 'U-12', goals: 9 },
  { name: 'Юрій Дзюба', team: 'Шахтар Академія', age: 'U-12', goals: 8 },
];

// Sample schedule (matches)
function makeSchedule() {
  const fields = ['Поле A', 'Поле B', 'Поле C'];
  const out = [];
  for (let day = 1; day <= 3; day++) {
    for (let i = 0; i < 6; i++) {
      const a = TEAMS_POOL[(day + i) % TEAMS_POOL.length];
      const b = TEAMS_POOL[(day + i + 7) % TEAMS_POOL.length];
      out.push({
        day,
        time: `${9 + i * 2}:${i % 2 ? '30' : '00'}`,
        field: fields[i % 3],
        a, b,
        age: ['U-8','U-10','U-12','U-13'][i % 4],
        status: day === 1 ? 'finished' : (day === 2 && i < 3 ? 'finished' : (day === 2 && i === 3 ? 'live' : 'upcoming')),
        sA: day === 1 || (day === 2 && i < 3) ? Math.floor(Math.random()*4) : null,
        sB: day === 1 || (day === 2 && i < 3) ? Math.floor(Math.random()*4) : null,
      });
    }
  }
  return out;
}

window.TOURNAMENTS = TOURNAMENTS;
window.TEAMS_POOL = TEAMS_POOL;
window.TOP_SCORERS = TOP_SCORERS;
window.makeBracket = makeBracket;
window.makeSchedule = makeSchedule;
