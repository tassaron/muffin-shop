"""
Handles logging in/registering/editing a user account
"""
from flask import (
    flash,
    request,
    session,
    render_template,
    current_app,
    redirect,
    url_for,
    abort,
)
import flask_login
from sqlalchemy.exc import IntegrityError
from is_safe_url import is_safe_url
from muffin_shop.helpers.main.plugins import db, rate_limiter
from muffin_shop.forms.main.forms import (
    ShortRegistrationForm,
    LoginForm,
    RequestPasswordResetForm,
    PasswordResetForm,
)
from muffin_shop.helpers.main.email import *
from muffin_shop.blueprint import Blueprint


import muffin_shop.models.main.models as Models
from muffin_shop.models.main.models import User, NewEmail


blueprint = Blueprint(
    "account",
    __name__,
)


@blueprint.route("/login", methods=["POST", "GET"])
@rate_limiter.limit("6/minute")
def login():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for(current_app.config["INDEX_ROUTE"]))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password_hash(form.password.data):
            flash("Logged in! ✔️", "success")

            if not current_app.config["CLIENT_SESSIONS"]:
                # Three goals in this terrifying section of code:
                # 1) assign a user id to the current session if the user has none yet
                # 2) ensure a full shopping cart carries over while logging in
                # 3) combine arcade tokens/prizes from logged-out to logged-in sessions

                restored_session_id, restored_session_data = current_app.session_interface.get_user_session(
                    user.id
                )

                if restored_session_data is None:
                    # no existing data, so we can assign this session as the user's first
                    current_app.session_interface.set_user_session(session.sid, user.id)
                else:
                    if session["cart"] == {}:
                        # cart is empty so copy the other session that has a full cart
                        session["cart"] = restored_session_data["cart"]
                    if "arcade_tokens" in session and "arcade_tokens" in restored_session_data:
                        session["arcade_tokens"] += restored_session_data["arcade_tokens"]
                    if "arcade_prizes" in session and "arcade_prizes" in restored_session_data:
                        for prize, quantity in restored_session_data["arcade_prizes"].items():
                            if prize in session["arcade_prizes"]:
                                session["arcade_prizes"][prize] += quantity
                            else:
                                session["arcade_prizes"][prize] = quantity

                    # assign this session as the user's new "existing session" & nullify the old one
                    # so future logins with empty cart will inherit the latest full cart
                    current_app.session_interface.set_user_session(
                        restored_session_id, None
                    )
                    current_app.session_interface.set_user_session(session.sid, user.id)

            flask_login.login_user(user, remember=form.rememberme.data)
            next_page = request.args.get("next")
            return (
                redirect(next_page)
                if next_page
                and is_safe_url(next_page, url_for(current_app.config["INDEX_ROUTE"]))
                else redirect(url_for(current_app.config["INDEX_ROUTE"]))
            )
        else:
            flash("Wrong email or password.", "danger")

    return render_template("account/login.html", form=form)


@blueprint.route("/reset_password", methods=["GET", "POST"])
@rate_limiter.limit("6/minute")
def reset_password():
    def do_reset(user):
        try:
            result = send_password_reset_email(user)
            flash("An email was sent with instructions to reset your password", "info")
            return redirect(url_for(".login"))
        except OutboxFull:
            flash(
                "Sorry, you have to wait a few hours before requesting another email",
                "info",
            )
        except Unverified:
            flash(
                "Your email address isn't verified so the email couldn't be sent",
                "warning",
            )

    if flask_login.current_user.is_authenticated:
        do_reset(flask_login.current_user)
        return redirect(url_for(current_app.config["INDEX_ROUTE"]))

    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        do_reset(user)
    return render_template("account/reset_password.html", form=form)


@blueprint.route("/reset_password/<token>", methods=["GET", "POST"])
@rate_limiter.limit("6/minute")
def change_password(token):
    user = User.verify_json_web_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for(".reset_password"))

    form = PasswordResetForm()
    if form.validate_on_submit():
        user.update_password(form.password.data)
        email = NewEmail.query.filter_by(user_id=user.id).first()
        if email is None:
            current_app.logger.warning(
                "The password token should expire before the email does... user_id: %s",
                user.id,
            )
        else:
            archive_email(email)
        flash("Your password has been updated!", "success")
        return redirect(url_for(".login"))

    return render_template("account/change_password.html", form=form)


@blueprint.route("/verify_email/<token>")
@flask_login.login_required
def verify_email(token):
    user = User.verify_json_web_token(token)
    if user is None or user != flask_login.current_user or user.email_verified == True:
        flash("That is an invalid or expired token", "warning")
    else:
        user.email_verified = True
        email = NewEmail.query.filter_by(user_id=user.id).first()
        if email is None:
            current_app.logger.warning(
                "The email verification token should expire before the email does... user_id: %s",
                user.id,
            )
        else:
            archive_email(email)
        flash("Your email has been verified!", "success")

    return redirect(url_for(current_app.config["INDEX_ROUTE"]))


@blueprint.route("/verify_email")
@flask_login.login_required
def request_email_verification():
    if flask_login.current_user.email_verified:
        abort(401)
    try:
        result = send_email_verification_email(flask_login.current_user)
    except OutboxFull:
        flash(
            "Sorry, you have to wait a few hours before requesting another email. "
            "Please remember to check your spam folder",
            "info",
        )
    else:
        flash(
            "An email was sent to the address you provided during registration", "info"
        )
    return redirect(url_for(current_app.config["INDEX_ROUTE"]))


@blueprint.route("/profile")
@flask_login.login_required
def user_dashboard():
    """Let the user see their email address and change their password"""
    return render_template(
        "account/view_profile.html",
        user=flask_login.current_user,
        profile_sections={},
    )


@blueprint.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    if not current_app.config["CLIENT_SESSIONS"]:
        # generate unique session id so the old session isn't overwritten
        session.sid = current_app.session_interface._generate_sid()

    # empty things that the user would expect to become empty
    session["cart"] = {}
    if "arcade_tokens" in session:
        session["arcade_tokens"] = 0
    if "arcade_prizes" in session:
        session["arcade_prizes"] = {}

    flash("Logged out", "info")
    return redirect(url_for(current_app.config["INDEX_ROUTE"]))


@blueprint.route("/register", methods=["GET", "POST"])
@rate_limiter.limit("6/minute")
def register():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for(current_app.config["INDEX_ROUTE"]))

    form = ShortRegistrationForm()
    if form.validate_on_submit():
        try:
            new_user = User(
                email=form.email.data, password=form.password.data, is_admin=False
            )
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            flash("That email is already taken. Log in below", "danger")
            db.session.rollback()
        else:
            flash("Successfully signed up! Log in below", "success")
            send_email_verification_email(new_user)
        return redirect(url_for("account.login"))

    return render_template("account/register.html", form=form)


@blueprint.admin_route("")
def admin_users_list():
    users = User.query.all()
    return render_template("account/admin_users.html", users=users)
