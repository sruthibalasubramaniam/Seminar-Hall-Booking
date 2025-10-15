from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from .models import User, db


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)   # ✅ this logs in the user
            flash("Login successful!", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Invalid email or password", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect(url_for("auth.login"))



@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        existing = User.query.filter_by(email=email).first()
        if existing:
            flash("Email already registered", "warning")
        else:
            user = User(email=email)



            flash("Signup successful! Please login.", "success")
            return redirect(url_for("auth.login"))

    return render_template("signup.html")



@auth_bp.route("/logout")
def logout():
    # For now just redirect
    flash("You have been logged out", "info")
    return redirect(url_for("main.home"))
