import secrets

from flask import current_app

from .db import get_db

CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

ORDER_QUERY = """
    SELECT o.*, s.starts_at, s.format, s.price AS base_price,
           m.title, m.slug, m.genre, m.duration_min, m.age_rating,
           h.name AS hall_name
    FROM orders o
    JOIN showtimes s ON s.id = o.showtime_id
    JOIN movies m ON m.id = s.movie_id
    JOIN halls h ON h.id = s.hall_id
"""


def new_code():
    raw = "".join(secrets.choice(CODE_ALPHABET) for _ in range(8))
    return f"{raw[:4]}-{raw[4:]}"


def discount_price(price):
    percent = current_app.config["DISCOUNT_PERCENT"]
    return int(round(price * (100 - percent) / 100 / 10) * 10)


def ticket_prices(price, count, discounted):
    reduced = discount_price(price)
    return [("discount", reduced) if index < discounted else ("full", price) for index in range(count)]


def create(showtime, data):
    prices = ticket_prices(showtime["price"], len(data["seats"]), data["discounted"])
    db = get_db()
    code = new_code()
    while db.execute("SELECT 1 FROM orders WHERE code = ?", (code,)).fetchone():
        code = new_code()
    cursor = db.execute(
        "INSERT INTO orders (code, showtime_id, full_name, phone, email, total) VALUES (?, ?, ?, ?, ?, ?)",
        (code, showtime["id"], data["full_name"], data["phone"], data["email"], sum(p for _, p in prices)),
    )
    for (row, seat), (kind, price) in zip(data["seats"], prices):
        db.execute(
            "INSERT INTO tickets (order_id, row_no, seat_no, kind, price) VALUES (?, ?, ?, ?, ?)",
            (cursor.lastrowid, row, seat, kind, price),
        )
    db.commit()
    return code


def get_by_code(code):
    db = get_db()
    order = db.execute(ORDER_QUERY + " WHERE o.code = ?", (code.upper(),)).fetchone()
    if order is None:
        return None
    tickets = db.execute(
        "SELECT row_no, seat_no, kind, price FROM tickets WHERE order_id = ? ORDER BY row_no, seat_no",
        (order["id"],),
    ).fetchall()
    return order, tickets


def find(code, email):
    found = get_by_code(code)
    if found is None or found[0]["email"] != email:
        return None
    return found
