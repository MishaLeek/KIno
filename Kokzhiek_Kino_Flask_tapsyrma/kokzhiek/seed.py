import random
from datetime import date, timedelta

CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

MOVIES = [
    {
        "slug": "dala-zhuldyzy",
        "title": "Дала жұлдызы",
        "genre": "Драма",
        "duration_min": 124,
        "age_rating": "12+",
        "director": "Әлия Сейітова",
        "language": "Қазақ тілінде",
        "year": 2026,
        "tagline": "Ауылдан сахнаға дейінгі жол",
        "description": [
            "Жетісудағы шағын ауылда тұратын он жеті жастағы Нұрай әнші болуды армандайды. Әкесі оның "
            "таңдауын түсінбейді, ал қалаға апаратын жол тек бір жазға ғана ашық.",
            "Фильм арман, отбасы және өзіңе адал болу туралы. Саундтрегін халық әндерінің жаңа өңделген "
            "нұсқалары құрайды.",
        ],
        "formats": ["2D"],
        "featured": 0,
    },
    {
        "slug": "temir-tulpar",
        "title": "Темір тұлпар",
        "genre": "Ғылыми фантастика",
        "duration_min": 138,
        "age_rating": "12+",
        "director": "Ержан Мұратов",
        "language": "Қазақ тілінде, орыс субтитрлері",
        "year": 2026,
        "tagline": "Болашақтың даласында ескі аңыз оянады",
        "description": [
            "2090 жыл. Даланы энергия станциялары басып кеткен, ал адамдар жылқыны тек кітаптан біледі. "
            "Жас инженер Арман ескі зертханадан аңыздағы тұлпарға ұқсас роботты табады.",
            "Олардың бірге өткен жолы технология мен табиғаттың, болашақ пен естеліктің арасындағы таңдау "
            "туралы. Фильм 3D форматында да көрсетіледі.",
        ],
        "formats": ["2D", "3D"],
        "featured": 1,
    },
    {
        "slug": "songy-keruen",
        "title": "Соңғы керуен",
        "genre": "Шытырман оқиғалы",
        "duration_min": 116,
        "age_rating": "6+",
        "director": "Бауыржан Әлиев",
        "language": "Қазақ тілінде",
        "year": 2025,
        "tagline": "Ұлы Жібек жолындағы ең ұзақ сапар",
        "description": [
            "XV ғасыр. Отырардан шыққан керуен шөл арқылы алыс қалаға жетуі керек. Керуенбасының он екі "
            "жасар ұлы бұл сапарға алғаш рет аттанады.",
            "Боран, жоғалған құдықтар және жолда табылған жаңа достар оны нағыз жол бастаушы етеді. "
            "Отбасымен көруге арналған фильм.",
        ],
        "formats": ["2D"],
        "featured": 0,
    },
    {
        "slug": "tungi-qala",
        "title": "Түнгі қала",
        "genre": "Детектив",
        "duration_min": 109,
        "age_rating": "16+",
        "director": "Дина Құрманова",
        "language": "Қазақ тілінде",
        "year": 2026,
        "tagline": "Қала ұйықтағанда ғана шындық ашылады",
        "description": [
            "Тергеуші Самат он жыл бұрын жабылған істің жаңа ізіне түседі. Әр түнгі қоңырау оны шешімге "
            "жақындатады, бірақ қаланың ескі құпиялары оңай ашылмайды.",
            "Шиеленісті сюжет, түнгі мегаполистің атмосферасы және соңғы минутқа дейін белгісіз соңы.",
        ],
        "formats": ["2D"],
        "featured": 0,
    },
    {
        "slug": "kishkentai-tulki",
        "title": "Кішкентай түлкі",
        "genre": "Анимация",
        "duration_min": 92,
        "age_rating": "0+",
        "director": "Әсел Жақыпова",
        "language": "Қазақ тілінде",
        "year": 2026,
        "tagline": "Орманның ең кішкентай батыры",
        "description": [
            "Қызықшыл түлкі күшігі Шұбар орманның арғы жағында не бар екенін білгісі келеді. Сапарында ол "
            "ақылды жапалақпен, қорқақ қоянмен және ашулы аюмен танысады.",
            "Достық, батылдық және туған жерді сүю туралы мультфильм. Кішкентай көрермендерге арналған, "
            "3D форматында да көрсетіледі.",
        ],
        "formats": ["2D", "3D"],
        "featured": 0,
    },
    {
        "slug": "altyn-kuz",
        "title": "Алтын күз",
        "genre": "Комедия",
        "duration_min": 101,
        "age_rating": "12+",
        "director": "Нұрлан Бекетов",
        "language": "Қазақ тілінде",
        "year": 2025,
        "tagline": "Бір той, үш отбасы, ешқандай жоспар",
        "description": [
            "Үлкен тойға үш күн қалғанда бәрі жоспардан шығып кетеді: асаба ауырып қалады, мейрамхана "
            "жабылады, ал күйеу жақтың туыстары бір күн ерте келеді.",
            "Жылы әзілге толы отбасылық комедия: күліп қана қоймай, жақындарыңызды бір сәт ойлап қаласыз.",
        ],
        "formats": ["2D"],
        "featured": 0,
    },
]

HALLS = [
    {"name": "1-зал", "rows": 8, "seats": 12, "kind": "standard",
     "slots": ["10:30", "13:20", "16:10", "19:00", "21:40"]},
    {"name": "2-зал", "rows": 7, "seats": 10, "kind": "standard",
     "slots": ["11:00", "13:50", "16:40", "19:30", "22:00"]},
    {"name": "VIP зал", "rows": 4, "seats": 8, "kind": "vip",
     "slots": ["12:30", "17:00", "20:15"]},
]

DAYS_AHEAD = 5

DEMO_ORDER = {
    "code": "DEMO-2026",
    "full_name": "Демо Көрермен",
    "phone": "+77001234567",
    "email": "demo@example.com",
}


def ticket_price(hall, slot, fmt):
    if hall["kind"] == "vip":
        return 4500
    price = 1800 if slot < "15:00" else 2300
    if fmt == "3D":
        price += 600
    return price


def random_code(rng):
    raw = "".join(rng.choice(CODE_ALPHABET) for _ in range(8))
    return f"{raw[:4]}-{raw[4:]}"


def add_order(db, showtime_id, code, buyer, seats, prices):
    cursor = db.execute(
        "INSERT INTO orders (code, showtime_id, full_name, phone, email, total) VALUES (?, ?, ?, ?, ?, ?)",
        (code, showtime_id, buyer["full_name"], buyer["phone"], buyer["email"], sum(p for _, p in prices)),
    )
    for (row, seat), (kind, price) in zip(seats, prices):
        db.execute(
            "INSERT INTO tickets (order_id, row_no, seat_no, kind, price) VALUES (?, ?, ?, ?, ?)",
            (cursor.lastrowid, row, seat, kind, price),
        )


def populate(db):
    movie_ids = []
    for movie in MOVIES:
        cursor = db.execute(
            "INSERT INTO movies (slug, title, genre, duration_min, age_rating, director, language, year,"
            " tagline, description, featured) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                movie["slug"], movie["title"], movie["genre"], movie["duration_min"], movie["age_rating"],
                movie["director"], movie["language"], movie["year"], movie["tagline"],
                "\n\n".join(movie["description"]), movie["featured"],
            ),
        )
        movie_ids.append(cursor.lastrowid)

    hall_ids = []
    for hall in HALLS:
        cursor = db.execute(
            "INSERT INTO halls (name, rows_count, seats_per_row, kind) VALUES (?, ?, ?, ?)",
            (hall["name"], hall["rows"], hall["seats"], hall["kind"]),
        )
        hall_ids.append(cursor.lastrowid)

    today = date.today()
    yesterday = (today - timedelta(days=1)).isoformat()
    for index in range(len(MOVIES)):
        db.execute(
            "INSERT INTO showtimes (movie_id, hall_id, starts_at, format, price) VALUES (?, ?, ?, '2D', 2300)",
            (movie_ids[(index + 1) % len(MOVIES)], hall_ids[0], f"{yesterday} 19:00"),
        )

    kassa = {"full_name": "Кассадан сатылған", "phone": "+77272000000", "email": "kassa@kokzhiek.example"}
    demo_target = None
    for day in range(DAYS_AHEAD):
        day_iso = (today + timedelta(days=day)).isoformat()
        for h, hall in enumerate(HALLS):
            for s, slot in enumerate(hall["slots"]):
                movie_index = (day * 2 + h * 3 + s) % len(MOVIES)
                movie = MOVIES[movie_index]
                fmt = "3D" if "3D" in movie["formats"] and h == 0 and s % 2 == 0 else "2D"
                price = ticket_price(hall, slot, fmt)
                cursor = db.execute(
                    "INSERT INTO showtimes (movie_id, hall_id, starts_at, format, price) VALUES (?, ?, ?, ?, ?)",
                    (movie_ids[movie_index], hall_ids[h], f"{day_iso} {slot}", fmt, price),
                )
                showtime_id = cursor.lastrowid
                rng = random.Random(showtime_id * 7919)
                all_seats = [(r, n) for r in range(1, hall["rows"] + 1) for n in range(1, hall["seats"] + 1)]
                share = 3 if slot >= "18:00" else 6
                sold = rng.sample(all_seats, rng.randint(0, len(all_seats) // share))
                if day == 1 and movie["slug"] == "temir-tulpar" and demo_target is None:
                    demo_target = (showtime_id, price)
                    sold = [seat for seat in sold if seat not in ((5, 6), (5, 7))]
                if sold:
                    add_order(db, showtime_id, random_code(rng), kassa, sorted(sold), [("full", price)] * len(sold))

    if demo_target:
        showtime_id, price = demo_target
        discounted = int(round(price * 0.7 / 10) * 10)
        add_order(db, showtime_id, DEMO_ORDER["code"], DEMO_ORDER, [(5, 6), (5, 7)],
                  [("discount", discounted), ("full", price)])
