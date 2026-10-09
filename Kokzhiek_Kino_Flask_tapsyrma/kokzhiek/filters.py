import hashlib
from datetime import date, datetime, timedelta

MONTHS = (
    "қаңтар",
    "ақпан",
    "наурыз",
    "сәуір",
    "мамыр",
    "маусым",
    "шілде",
    "тамыз",
    "қыркүйек",
    "қазан",
    "қараша",
    "желтоқсан",
)
WEEKDAYS = ("дүйсенбі", "сейсенбі", "сәрсенбі", "бейсенбі", "жұма", "сенбі", "жексенбі")
NBSP = " "


def to_datetime(value):
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day)
    text = str(value)
    return datetime.strptime(text[:16], "%Y-%m-%d %H:%M") if len(text) >= 16 else datetime.strptime(text[:10], "%Y-%m-%d")


def format_number(value):
    return f"{int(round(value)):,}".replace(",", NBSP)


def format_money(value):
    return f"{format_number(value)}{NBSP}₸"


def format_date(value, weekday=True):
    moment = to_datetime(value)
    text = f"{moment.day}{NBSP}{MONTHS[moment.month - 1]}"
    if weekday:
        text += f", {WEEKDAYS[moment.weekday()]}"
    return text


def format_time(value):
    return to_datetime(value).strftime("%H:%M")


def day_label(value):
    day = to_datetime(value).date()
    today = date.today()
    if day == today:
        return "Бүгін"
    if day == today + timedelta(days=1):
        return "Ертең"
    return WEEKDAYS[day.weekday()].capitalize()


def format_duration(minutes):
    hours, rest = divmod(int(minutes), 60)
    return f"{hours}{NBSP}сағ {rest:02d}{NBSP}мин" if hours else f"{rest}{NBSP}мин"


def format_phone(value):
    digits = "".join(char for char in str(value) if char.isdigit())
    if len(digits) != 11:
        return value
    return f"+{digits[0]} {digits[1:4]} {digits[4:7]} {digits[7:9]} {digits[9:]}"


def barcode(code, height=56):
    digest = hashlib.sha256(str(code).encode("utf-8")).digest()
    bars, x = [], 0
    for byte in digest[:24]:
        for width in (1 + byte % 3, 1 + (byte >> 3) % 2):
            bars.append({"x": x, "w": width})
            x += width + 1 + (byte >> 5) % 2
    return {"bars": bars, "width": x, "height": height}


def init_app(app):
    app.jinja_env.filters.update(
        number=format_number,
        money=format_money,
        kzdate=format_date,
        hhmm=format_time,
        day_label=day_label,
        duration=format_duration,
        phone=format_phone,
    )
    app.jinja_env.globals["barcode"] = barcode

    @app.context_processor
    def inject_globals():
        return {"current_year": date.today().year}
