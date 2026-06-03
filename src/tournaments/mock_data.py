"""Static mock data for bracket, schedule, scorers (v1 — no DB models)."""

TEAMS_POOL = [
    {"name": "РУХ", "city": "Львів", "short": "РУХ"},
    {"name": "Карпати", "city": "Львів", "short": "КАР"},
    {"name": "ЛНУ Академія", "city": "Львів", "short": "ЛНУ"},
    {"name": "Левеня", "city": "Львів", "short": "ЛЕВ"},
    {"name": "Динамо", "city": "Київ", "short": "ДИН"},
    {"name": "Шахтар Академія", "city": "Київ", "short": "ШАХ"},
    {"name": "Зоря", "city": "Луганськ", "short": "ЗОР"},
    {"name": "Нива", "city": "Тернопіль", "short": "НИВ"},
    {"name": "Прикарпаття", "city": "Івано-Франківськ", "short": "ПРИ"},
    {"name": "Буковина", "city": "Чернівці", "short": "БУК"},
    {"name": "Волинь", "city": "Луцьк", "short": "ВОЛ"},
    {"name": "Минай", "city": "Ужгород", "short": "МИН"},
    {"name": "Полісся", "city": "Житомир", "short": "ПОЛ"},
    {"name": "Кремінь", "city": "Кременчук", "short": "КРМ"},
    {"name": "Сокіл", "city": "Львів", "short": "СОК"},
    {"name": "Галичина", "city": "Дрогобич", "short": "ГАЛ"},
]

TOP_SCORERS = [
    {"name": "Назар Кравченко", "team": "РУХ", "age": "U-12", "goals": 14},
    {"name": "Артем Стеценко", "team": "Карпати", "age": "U-12", "goals": 12},
    {"name": "Микита Шевчук", "team": "Динамо", "age": "U-11", "goals": 11},
    {"name": "Олексій Ткач", "team": "Левеня", "age": "U-12", "goals": 9},
    {"name": "Юрій Дзюба", "team": "Шахтар Академія", "age": "U-12", "goals": 8},
]

BRACKET_MOCK = {
    "r16": [
        {"a": TEAMS_POOL[0], "b": TEAMS_POOL[1], "sA": 3, "sB": 1, "status": "finished"},
        {"a": TEAMS_POOL[2], "b": TEAMS_POOL[3], "sA": 2, "sB": 0, "status": "finished"},
        {"a": TEAMS_POOL[4], "b": TEAMS_POOL[5], "sA": 1, "sB": 2, "status": "finished"},
        {"a": TEAMS_POOL[6], "b": TEAMS_POOL[7], "sA": 4, "sB": 2, "status": "finished"},
    ],
    "sf": [
        {"a": TEAMS_POOL[0], "b": TEAMS_POOL[2], "sA": 2, "sB": 1, "status": "live"},
        {"a": TEAMS_POOL[5], "b": TEAMS_POOL[6], "sA": 0, "sB": 0, "status": "upcoming"},
    ],
    "final": {
        "a": TEAMS_POOL[0],
        "b": TEAMS_POOL[6],
        "sA": "–",
        "sB": "–",
        "status": "upcoming",
    },
}

SCHEDULE_MOCK = [
    {"day": 1, "time": "9:00", "field": "Поле A", "a": TEAMS_POOL[0], "b": TEAMS_POOL[7], "age": "U-12", "status": "finished", "sA": 3, "sB": 1},
    {"day": 1, "time": "11:00", "field": "Поле B", "a": TEAMS_POOL[1], "b": TEAMS_POOL[8], "age": "U-10", "status": "finished", "sA": 2, "sB": 2},
    {"day": 1, "time": "13:00", "field": "Поле C", "a": TEAMS_POOL[2], "b": TEAMS_POOL[9], "age": "U-11", "status": "finished", "sA": 1, "sB": 0},
    {"day": 2, "time": "9:00", "field": "Поле A", "a": TEAMS_POOL[3], "b": TEAMS_POOL[10], "age": "U-13", "status": "finished", "sA": 4, "sB": 1},
    {"day": 2, "time": "11:00", "field": "Поле B", "a": TEAMS_POOL[4], "b": TEAMS_POOL[11], "age": "U-12", "status": "live", "sA": 1, "sB": 1},
    {"day": 2, "time": "13:00", "field": "Поле C", "a": TEAMS_POOL[5], "b": TEAMS_POOL[12], "age": "U-10", "status": "upcoming", "sA": None, "sB": None},
]

GALLERY_TEASER = [
    {
        "h": 240,
        "label": "OPENING CEREMONY · MAY 2025",
        "src": "images/gallery/opening-ceremony.jpg",
        "alt": "Церемонія відкриття LEO CUP — командне фото",
    },
    {
        "h": 320,
        "label": "FINAL MATCH · U12",
        "src": "images/gallery/final-match-u12.jpg",
        "alt": "Фінал U12 — команди на полі після матчу",
    },
    {
        "h": 240,
        "label": "WINNER PHOTO",
        "src": "images/gallery/winner-photo.jpg",
        "alt": "Переможці LEO CUP з кубком",
    },
    {
        "h": 240,
        "label": "CROWD · TRIBUNES",
        "src": "images/gallery/crowd-tribunes.jpg",
        "alt": "Уболівальники та переможці на турнірі",
    },
    {
        "h": 320,
        "label": "GOAL · 89th MIN",
        "src": "images/gallery/goal-89min.jpg",
        "alt": "Гострий момент матчу — боротьба за мʼяч",
    },
    {
        "h": 240,
        "label": "TROPHY HANDOVER",
        "src": "images/gallery/trophy-handover.jpg",
        "alt": "Вручення кубка переможцям",
    },
]

MARQUEE_ITEMS = [
    "ОДИН ФУТБОЛ",
    "ЛЬВІВ 2026",
    "600+ ГРАВЦІВ",
    "ДЛЯ ДІТЕЙ ВІД 6 РОКІВ",
    "НАЙМАСОВІШІ ТУРНІРИ УКРАЇНИ",
]

ARCHIVE_GALLERY = GALLERY_TEASER + [
    {
        "h": 320,
        "label": "TEAM HUDDLE · 2024",
        "src": "images/gallery/opening-ceremony.jpg",
        "alt": "Командне коло перед матчем",
    },
    {
        "h": 240,
        "label": "MEDALS · U11",
        "src": "images/gallery/winner-photo.jpg",
        "alt": "Нагородження гравців U11",
    },
    {
        "h": 240,
        "label": "FIELD WARMUP",
        "src": "images/gallery/final-match-u12.jpg",
        "alt": "Розминка команди на полі",
    },
]

ARCHIVE_EDITIONS = [
    {
        "year": "2025",
        "title": "LEO CUP",
        "season": "Весна",
        "teams": 58,
        "matches": 72,
        "goals": 312,
        "theme_class": "theme-spring",
    },
    {
        "year": "2025",
        "title": "LEO CUP",
        "season": "Осінь",
        "teams": 44,
        "matches": 56,
        "goals": 248,
        "theme_class": "theme-autumn",
    },
    {
        "year": "2025",
        "title": "RUH CUP",
        "season": "Зима",
        "teams": 36,
        "matches": 48,
        "goals": 196,
        "theme_class": "theme-winter",
    },
    {
        "year": "2024",
        "title": "RUH KIDS CUP",
        "season": "Зима",
        "teams": 52,
        "matches": 64,
        "goals": 284,
        "theme_class": "theme-kids",
    },
]
