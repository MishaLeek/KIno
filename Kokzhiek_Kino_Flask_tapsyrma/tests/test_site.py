from datetime import date, timedelta

from kokzhiek.seed import DEMO_ORDER
from tests.base import AppTestCase


class PublicPagesTests(AppTestCase):
    def test_public_pages_open(self):
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        for url in ("/", f"/?day={tomorrow}", "/movies", "/movies/temir-tulpar", "/tickets", "/rules"):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_unknown_movie_returns_404(self):
        response = self.client.get("/movies/joq-film")
        self.assertEqual(response.status_code, 404)
        self.assertIn("Бет табылмады", self.page(response))

    def test_past_showtime_is_closed(self):
        past = self.query("SELECT id FROM showtimes ORDER BY starts_at LIMIT 1")[0]
        self.assertEqual(self.client.get(f"/showtimes/{past['id']}").status_code, 404)


class TicketTests(AppTestCase):
    def test_demo_ticket_opens(self):
        response = self.client.get(f"/tickets/{DEMO_ORDER['code']}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Темір тұлпар", self.page(response))

    def test_lookup_finds_ticket(self):
        response = self.client.post("/tickets", data={"code": "demo2026", "email": DEMO_ORDER["email"]})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].endswith(f"/tickets/{DEMO_ORDER['code']}"))

    def test_lookup_rejects_wrong_email(self):
        response = self.client.post("/tickets", data={"code": DEMO_ORDER["code"], "email": "wrong@example.com"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("табылмады", self.page(response))
