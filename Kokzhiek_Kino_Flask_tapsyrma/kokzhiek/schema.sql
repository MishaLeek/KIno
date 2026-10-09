DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS showtimes;
DROP TABLE IF EXISTS halls;
DROP TABLE IF EXISTS movies;

CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    genre TEXT NOT NULL,
    duration_min INTEGER NOT NULL,
    age_rating TEXT NOT NULL,
    director TEXT NOT NULL,
    language TEXT NOT NULL,
    year INTEGER NOT NULL,
    tagline TEXT NOT NULL,
    description TEXT NOT NULL,
    featured INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE halls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    rows_count INTEGER NOT NULL,
    seats_per_row INTEGER NOT NULL,
    kind TEXT NOT NULL CHECK (kind IN ('standard', 'vip'))
);

CREATE TABLE showtimes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER NOT NULL REFERENCES movies (id),
    hall_id INTEGER NOT NULL REFERENCES halls (id),
    starts_at TEXT NOT NULL,
    format TEXT NOT NULL CHECK (format IN ('2D', '3D')),
    price INTEGER NOT NULL
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    showtime_id INTEGER NOT NULL REFERENCES showtimes (id),
    full_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    total INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL REFERENCES orders (id) ON DELETE CASCADE,
    row_no INTEGER NOT NULL,
    seat_no INTEGER NOT NULL,
    kind TEXT NOT NULL CHECK (kind IN ('full', 'discount')),
    price INTEGER NOT NULL
);

CREATE INDEX idx_showtimes_movie ON showtimes (movie_id, starts_at);
CREATE INDEX idx_orders_showtime ON orders (showtime_id);
CREATE INDEX idx_tickets_order ON tickets (order_id);
