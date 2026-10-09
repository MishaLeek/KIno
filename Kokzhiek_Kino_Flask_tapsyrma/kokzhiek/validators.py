import re

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")
SEAT_PATTERN = re.compile(r"^(\d{1,2})-(\d{1,2})$")
CODE_PATTERN = re.compile(r"[^A-Z0-9]")


def normalize_phone(raw):
    digits = re.sub(r"\D", "", raw)
    if len(digits) == 11 and digits[0] in "78":
        digits = digits[1:]
    if len(digits) != 10:
        return None
    return "+7" + digits


def normalize_code(raw):
    code = CODE_PATTERN.sub("", raw.upper())
    if len(code) == 8:
        return f"{code[:4]}-{code[4:]}"
    return code


def parse_seats(values, showtime):
    seats = []
    for value in values:
        match = SEAT_PATTERN.match(value)
        if match is None:
            return None
        row, number = int(match.group(1)), int(match.group(2))
        if not (1 <= row <= showtime["rows_count"] and 1 <= number <= showtime["seats_per_row"]):
            return None
        if (row, number) not in seats:
            seats.append((row, number))
    return sorted(seats)


def validate_order(form, showtime, taken, max_seats):
    data = {
        "full_name": " ".join(form["full_name"].split()),
        "phone": form["phone"].strip(),
        "email": form["email"].strip().lower(),
        "discounted": form.get("discounted", 0, type=int),
        "agree": form.get("agree") == "on",
    }
    errors = {}

    seats = parse_seats(form.getlist("seats"), showtime)
    data["seats"] = seats or []
    if seats is None:
        errors["seats"] = "Орындар дұрыс таңдалмаған. Бетті жаңартып, орындарды қайта таңдаңыз."
    elif not seats:
        errors["seats"] = "Залдың сызбасынан кемінде бір орын таңдаңыз."
    elif len(seats) > max_seats:
        errors["seats"] = f"Бір тапсырыста {max_seats} орыннан артық болмауы керек."
    elif any(seat in taken for seat in seats):
        errors["seats"] = "Таңдалған орындардың бірі сатылып кетті. Басқа орын таңдаңыз."

    if not 0 <= data["discounted"] <= len(data["seats"]):
        errors["discounted"] = "Жеңілдікті билеттер саны таңдалған орындар санынан аспауы керек."

    if not 2 <= len(data["full_name"]) <= 60:
        errors["full_name"] = "Аты-жөніңізді жазыңыз (2–60 таңба)."

    phone = normalize_phone(data["phone"])
    if phone is None:
        errors["phone"] = "Телефон нөмірін +7 700 123 45 67 форматында енгізіңіз."
    else:
        data["phone"] = phone

    if len(data["email"]) > 120 or not EMAIL_PATTERN.match(data["email"]):
        errors["email"] = "Email мекенжайын дұрыс енгізіңіз: билет осы мекенжайға байланады."

    if not data["agree"]:
        errors["agree"] = "Сатып алу үшін кинотеатр ережелерімен келісу қажет."

    return data, errors
