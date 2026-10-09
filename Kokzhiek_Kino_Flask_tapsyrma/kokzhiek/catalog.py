from datetime import date, datetime, timedelta

from .db import get_db

DAYS_SHOWN = 5

SHOWTIME_QUERY = """
    SELECT s.id, s.movie_id, s.hall_id, s.starts_at, s.format, s.price,
           m.slug, m.title, m.genre, m.duration_min, m.age_rating,
           h.name AS hall_name, h.rows_count, h.seats_per_row, h.kind AS hall_kind,
           h.rows_count * h.seats_per_row - (
               SELECT COUNT(*) FROM tickets t
               JOIN orders o ON o.id = t.order_id
               WHERE o.showtime_id = s.id
           ) AS seats_left
    FROM showtimes s
    JOIN movies m ON m.id = s.movie_id
    JOIN halls h ON h.id = s.hall_id
"""


def now_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def upcoming_days():
    today = date.today()
    return [today + timedelta(days=offset) for offset in range(DAYS_SHOWN)]


def list_movies():
    return get_db().execute(
        """
        SELECT m.*,
               (SELECT MIN(s.starts_at) FROM showtimes s
                 WHERE s.movie_id = m.id AND s.starts_at > ?) AS next_showtime
        FROM movies m
        ORDER BY m.featured DESC, m.id
        """,
        (now_text(),),
    ).fetchall()


def get_movie(slug):
    return get_db().execute("SELECT * FROM movies WHERE slug = ?", (slug,)).fetchone()


def featured_movie():
    return get_db().execute("SELECT * FROM movies ORDER BY featured DESC, id LIMIT 1").fetchone()


def schedule_for_day(day):
    rows = get_db().execute(
        SHOWTIME_QUERY + " WHERE date(s.starts_at) = ? AND s.starts_at > ? ORDER BY s.movie_id, s.starts_at",
        (day.isoformat(), now_text()),
    ).fetchall()
    movies = {row["id"]: row for row in list_movies()}
    schedule = []
    for row in rows:
        if not schedule or schedule[-1]["movie"]["id"] != row["movie_id"]:
            schedule.append({"movie": movies[row["movie_id"]], "showtimes": []})
        schedule[-1]["showtimes"].append(row)
    return schedule


def showtimes_for_movie(movie_id):
    rows = get_db().execute(
        SHOWTIME_QUERY + " WHERE s.movie_id = ? AND s.starts_at > ? ORDER BY s.starts_at",
        (movie_id, now_text()),
    ).fetchall()
    days = []
    for row in rows:
        day = row["starts_at"][:10]
        if not days or days[-1]["day"] != day:
            days.append({"day": day, "showtimes": []})
        days[-1]["showtimes"].append(row)
    return days


def get_showtime(showtime_id):
    return get_db().execute(
        SHOWTIME_QUERY + " WHERE s.id = ? AND s.starts_at > ?", (showtime_id, now_text())
    ).fetchone()


def taken_seats(showtime_id):
    rows = get_db().execute(
        """
        SELECT t.row_no, t.seat_no
        FROM tickets t
        JOIN orders o ON o.id = t.order_id
        WHERE o.showtime_id = ?
        """,
        (showtime_id,),
    )
    return {(row["row_no"], row["seat_no"]) for row in rows}
