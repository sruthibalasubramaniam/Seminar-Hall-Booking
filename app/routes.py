from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime
from .models import Booking, SeminarHall, db
from flask_login import current_user, login_required

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("home.html")

@main_bp.route("/halls")
def halls():
    halls = SeminarHall.query.all()
    return render_template("halls.html", halls=halls)

@main_bp.route("/book", methods=["GET", "POST"])
@login_required
def book():
    if current_user.role != "club_head":
        flash("Only club heads can request bookings.", "danger")
        return redirect(url_for("main.halls"))

    if request.method == "POST":
        hall_id = request.form.get("hall_id")
        date = request.form.get("date")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")

        # Convert string to Python datetime
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        start_time_obj = datetime.strptime(start_time, "%H:%M").time()
        end_time_obj = datetime.strptime(end_time, "%H:%M").time()

        # Save booking
        booking = Booking(
            hall_id=hall_id,
            user_id=current_user.id,
            date=date_obj,
            start_time=start_time_obj,
            end_time=end_time_obj,
            status="pending"
        )
        db.session.add(booking)
        db.session.commit()

        flash("Booking request submitted! Awaiting approval.", "success")
        return redirect(url_for("main.my_bookings"))

    halls = SeminarHall.query.all()
    return render_template("book.html", halls=halls)

@main_bp.route("/my_bookings")
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template("my_bookings.html", bookings=bookings)
