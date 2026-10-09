from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, url_for

from . import catalog, orders
from .validators import normalize_code, validate_order

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    days = catalog.upcoming_days()
    selected = days[0]
    requested = request.args.get("day")
    for day in days:
        if day.isoformat() == requested:
            selected = day
    return render_template(
        "index.html",
        days=days,
        selected=selected,
        schedule=catalog.schedule_for_day(selected),
        featured=catalog.featured_movie(),
    )


@bp.route("/movies")
def movies():
    return render_template("movies/list.html", movies=catalog.list_movies())


@bp.route("/movies/<slug>")
def movie_detail(slug):
    movie = catalog.get_movie(slug)
    if movie is None:
        abort(404)
    return render_template("movies/detail.html", movie=movie, days=catalog.showtimes_for_movie(movie["id"]))


def render_showtime(showtime, form=None, errors=None):
    return render_template(
        "showtimes/detail.html",
        showtime=showtime,
        taken=catalog.taken_seats(showtime["id"]),
        form=form or {},
        errors=errors or {},
        max_seats=current_app.config["MAX_SEATS"],
        discount_percent=current_app.config["DISCOUNT_PERCENT"],
        discount_price=orders.discount_price(showtime["price"]),
    )


@bp.route("/showtimes/<int:showtime_id>")
def showtime(showtime_id):
    found = catalog.get_showtime(showtime_id)
    if found is None:
        abort(404)
    return render_showtime(found)


@bp.route("/showtimes/<int:showtime_id>/buy", methods=("POST",))
def buy(showtime_id):
    found = catalog.get_showtime(showtime_id)
    if found is None:
        abort(404)

    data, errors = validate_order(
        request.form, found, catalog.taken_seats(found["id"]), current_app.config["MAX_SEATS"]
    )
    if errors:
        return render_showtime(found, data, errors)

    code = orders.create(found, data)
    flash("Төлем сәтті өтті. Билеттеріңіз дайын.", "success")
    return redirect(url_for("main.ticket", code=code))


@bp.route("/tickets/<code>")
def ticket(code):
    found = orders.get_by_code(code)
    if found is None:
        abort(404)
    order, tickets = found
    return render_template("tickets/detail.html", order=order, tickets=tickets)


@bp.route("/tickets", methods=("GET", "POST"))
def lookup():
    form, error = {}, None
    if request.method == "POST":
        form = {
            "code": normalize_code(request.form.get("code", "")),
            "email": request.form.get("email", "").strip().lower(),
        }
        found = orders.find(form["code"], form["email"]) if form["code"] and form["email"] else None
        if found is not None:
            return redirect(url_for("main.ticket", code=found[0]["code"]))
        error = "Мұндай коды мен email мекенжайы бар тапсырыс табылмады. Деректерді тексеріп, қайталап көріңіз."
    return render_template("tickets/lookup.html", form=form, error=error)


@bp.route("/rules")
def rules():
    return render_template("rules.html")
