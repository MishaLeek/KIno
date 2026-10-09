import os
import tempfile
import unittest
from datetime import date, timedelta

from kokzhiek import create_app
from kokzhiek.catalog import taken_seats
from kokzhiek.db import get_db

BUYER = {
    "full_name": "Айгерім Серікова",
    "phone": "+7 701 555 12 34",
    "email": "aigerim@example.com",
    "discounted": "0",
    "agree": "on",
}


class AppTestCase(unittest.TestCase):
    def setUp(self):
        handle, self.db_path = tempfile.mkstemp(suffix=".sqlite")
        os.close(handle)
        os.unlink(self.db_path)
        self.app = create_app({"TESTING": True, "DATABASE": self.db_path, "CSRF_ENABLED": False})
        self.client = self.app.test_client()

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def query(self, sql, params=()):
        with self.app.app_context():
            return get_db().execute(sql, params).fetchall()

    def pick_showtime(self, kind="standard"):
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        rows = self.query(
            "SELECT s.id, s.price, s.movie_id, s.starts_at, m.title, h.rows_count, h.seats_per_row"
            " FROM showtimes s JOIN halls h ON h.id = s.hall_id JOIN movies m ON m.id = s.movie_id"
            " WHERE date(s.starts_at) >= ? AND h.kind = ? ORDER BY s.starts_at LIMIT 1",
            (tomorrow, kind),
        )
        return rows[0]

    def free_seats(self, showtime, count):
        with self.app.app_context():
            taken = taken_seats(showtime["id"])
        seats = [
            f"{row}-{number}"
            for row in range(1, showtime["rows_count"] + 1)
            for number in range(1, showtime["seats_per_row"] + 1)
            if (row, number) not in taken
        ]
        return seats[:count]

    def buy(self, showtime, seats, **changes):
        data = dict(BUYER, **changes)
        data["seats"] = seats
        return self.client.post(f"/showtimes/{showtime['id']}/buy", data=data)

    def order_by_code(self, code):
        rows = self.query("SELECT * FROM orders WHERE code = ?", (code,))
        return rows[0] if rows else None

    def page(self, response):
        return response.get_data(as_text=True)
