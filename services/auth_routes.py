from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user_model import User
from security.password_utils import hash_password, verify_password
from services.mfa_service import generate_mfa_code
from services.email_service import send_email
from database.db_init import db
from flask_login import login_user
from models.mfa_model import MFACode

auth_bp = Blueprint("auth", __name__)


# -------- Register --------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password),
            role=role
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please login.")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# -------- Login --------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and verify_password(password, user.password_hash):

            code = generate_mfa_code(user.id)

            send_email(
                user.email,
                "SafeShare MFA Code",
                f"Your SafeShare login code is: {code}"
            )

            return redirect(url_for("auth.verify_mfa", user_id=user.id))

        flash("Invalid credentials")

    return render_template("login.html")


# -------- MFA Verify --------
@auth_bp.route("/verify_mfa/<int:user_id>", methods=["GET", "POST"])
def verify_mfa(user_id):

    if request.method == "POST":

        entered_code = request.form["code"]

        mfa = MFACode.query.filter_by(user_id=user_id).order_by(MFACode.id.desc()).first()

        if mfa and not mfa.is_expired() and mfa.code == entered_code:

            user = User.query.get(user_id)
            login_user(user)

            flash("Login successful")
            return redirect(url_for("auth.dashboard"))

        flash("Invalid or expired code")

    return render_template("mfa_verify.html")


# -------- Dashboard Redirect --------
@auth_bp.route("/dashboard")
def dashboard():

    from flask_login import current_user

    if current_user.role == "client":
        return render_template("dashboard_client.html")

    return render_template("dashboard_recipient.html")
