from kokzhiek.catalog import taken_seats
from tests.base import AppTestCase


class PurchaseTests(AppTestCase):
    def test_showtime_page_opens(self):
        showtime = self.pick_showtime()
        response = self.client.get(f"/showtimes/{showtime['id']}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Орын таңдаңыз", self.page(response))

    def test_order_form_field_names_match_server(self):
        showtime = self.pick_showtime()
        page = self.page(self.client.get(f"/showtimes/{showtime['id']}"))
        for name in ("seats", "discounted", "full_name", "phone", "email", "agree"):
            with self.subTest(field=name):
                self.assertIn(
                    f'name="{name}"',
                    page,
                    f"Тапсырыс формасында name=\"{name}\" өрісі жоқ, сервер оны күтеді.",
                )

    def test_discount_count_is_read_as_number(self):
        showtime = self.pick_showtime()
        response = self.buy(showtime, self.free_seats(showtime, 2), discounted="1")
        self.assertEqual(response.status_code, 302, "Жеңілдікті билеті бар тапсырыс сәтті өтуі керек.")

    def test_purchase_redirects_to_ticket(self):
        showtime = self.pick_showtime()
        response = self.buy(showtime, self.free_seats(showtime, 1))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/tickets/", response.headers["Location"])

    def test_order_is_saved_for_selected_showtime(self):
        showtime = self.pick_showtime()
        response = self.buy(showtime, self.free_seats(showtime, 2))
        code = response.headers["Location"].rsplit("/", 1)[-1]
        order = self.order_by_code(code)
        self.assertIsNotNone(order)
        self.assertEqual(
            order["showtime_id"],
            showtime["id"],
            "Тапсырыс көрермен таңдаған сеансқа емес, басқа сеансқа жазылды.",
        )

    def test_bought_seats_become_taken(self):
        showtime = self.pick_showtime()
        seats = self.free_seats(showtime, 2)
        self.buy(showtime, seats)
        with self.app.app_context():
            taken = taken_seats(showtime["id"])
        for value in seats:
            row, number = map(int, value.split("-"))
            self.assertIn((row, number), taken, "Сатып алынған орын залда бос болып көрінеді.")

    def test_ticket_page_shows_selected_movie_and_time(self):
        showtime = self.pick_showtime()
        response = self.buy(showtime, self.free_seats(showtime, 1))
        ticket = self.page(self.client.get(response.headers["Location"]))
        self.assertIn(showtime["title"], ticket, "Билетте басқа фильмнің атауы тұр.")
        self.assertIn(showtime["starts_at"][11:16], ticket, "Билетте сеанстың уақыты дұрыс емес.")

    def test_total_price_with_discount(self):
        showtime = self.pick_showtime()
        response = self.buy(showtime, self.free_seats(showtime, 3), discounted="1")
        order = self.order_by_code(response.headers["Location"].rsplit("/", 1)[-1])
        reduced = int(round(showtime["price"] * 0.7 / 10) * 10)
        self.assertEqual(order["total"], showtime["price"] * 2 + reduced)

    def test_seat_cannot_be_bought_twice(self):
        showtime = self.pick_showtime()
        seats = self.free_seats(showtime, 1)
        self.buy(showtime, seats)
        response = self.buy(showtime, seats, email="other@example.com")
        self.assertEqual(response.status_code, 200)
        self.assertIn("сатылып кетті", self.page(response))

    def test_at_least_one_seat_is_required(self):
        showtime = self.pick_showtime()
        response = self.buy(showtime, [])
        self.assertEqual(response.status_code, 200)
        self.assertIn("кемінде бір орын", self.page(response))

    def test_discount_cannot_exceed_seats(self):
        showtime = self.pick_showtime()
        response = self.buy(showtime, self.free_seats(showtime, 1), discounted="3")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Жеңілдікті билеттер саны", self.page(response))

    def test_invalid_phone_is_rejected(self):
        showtime = self.pick_showtime()
        response = self.buy(showtime, self.free_seats(showtime, 1), phone="123")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Телефон нөмірін", self.page(response))

    def test_rules_must_be_accepted(self):
        showtime = self.pick_showtime()
        response = self.buy(showtime, self.free_seats(showtime, 1), agree="")
        self.assertEqual(response.status_code, 200)
        self.assertIn("ережелерімен келісу", self.page(response))
