"""
Handles logging in/registering/editing a user account
"""
from flask import (
    Blueprint,
    flash,
    request,
    render_template,
    current_app,
    redirect,
    url_for,
    abort,
)
import flask_login
from sqlalchemy.exc import IntegrityError
from is_safe_url import is_safe_url
from tassaron_flask_template.main.plugins import db
from tassaron_flask_template.main.forms import (
    ShortRegistrationForm,
    LoginForm,
    RequestPasswordResetForm,
    PasswordResetForm,
)
from tassaron_flask_template.email import *


import tassaron_flask_template.main.models as Models

User = Models.User


blueprint = Blueprint(
    "account",
    __name__,
    static_folder="../static",
    template_folder="../templates/account",
)


@blueprint.route("/login", methods=["POST", "GET"])
def login():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for(current_app.config["INDEX_ROUTE"]))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password_hash(form.password.data):
            flash("Logged in! ✔️", "success")
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

    return render_template("login.html", form=form)


@blueprint.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for(current_app.config["INDEX_ROUTE"]))

    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        try:
            result = send_password_reset_email(user)
            flash("An email was sent with instructions to reset your password", "info")
            return redirect(url_for(".login"))
        except OutboxFull:
            flash("Sorry, you have to wait a few hours before requesting another email", "info")
        except Unverified:
            flash("Your email address isn't verified so the email couldn't be sent", "warning")
    return render_template("reset_password.html", form=form)


@blueprint.route("/reset_password/<token>", methods=["GET", "POST"])
def change_password(token):
    if flask_login.current_user.is_authenticated:
        return redirect(url_for(current_app.config["INDEX_ROUTE"]))

    user = User.verify_json_web_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for(".reset_password"))

    form = PasswordResetForm()
    if form.validate_on_submit():
        user.update_password(form.password.data)
        email = Models.NewEmail.query.filter_by(user_id=user.id).first()
        if email is None:
            current_app.logger.warning("The password token should expire before the email does... user_id: %s", user.id)
        else:
            old_email = Models.OldEmail.from_email(email)
            db.session.add(old_email)
            db.session.delete(email)
        db.session.commit()
        flash("Your password has been updated! Now you can log in")
        return redirect(url_for(".login"))

    return render_template("change_password.html", form=form)


@blueprint.route("/verify_email/<token>")
@flask_login.login_required
def verify_email(token):
    user = User.verify_json_web_token(token)
    if user is None or user != flask_login.current_user or user.email_verified == True:
        flash("That is an invalid or expired token", "warning")
    else:
        user.email_verified = True
        email = Models.NewEmail.query.filter_by(user_id=user.id).first()
        if email is None:
            current_app.logger.warning("The email verification token should expire before the email does... user_id: %s", user.id)
        else:
            old_email = Models.OldEmail.from_email(email)
            db.session.add(old_email)
            db.session.delete(email)
        db.session.commit()
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
            "info"
        )
    else:
        flash("An email was sent to the address you provided during registration", "info")
    return redirect(url_for(current_app.config["INDEX_ROUTE"]))


@blueprint.route("/profile")
@flask_login.login_required
def user_dashboard():
    """ Let the user manage their shipping address, change password """
    user_id = int(flask_login.current_user.get_id())
    sections = {}
    for module in current_app.modules.values():
        for section_name, model in module.get("profile_models", {}).items():
            model_name = model
            model = Models.__dict__[model_name]
            section_data = model.query.filter_by(user_id=user_id).first()
            # section_data could be None and the target could respond with defaults
            try:
                html = current_app.view_functions[module["model_views"][model_name]](
                    section_data
                )
            except KeyError:
                current_app.logger.critical(
                    "module %s has profile_model %s but no corresponding model view.",
                    (module["name"], model_name),
                )
                html = ""
            sections[model.__name__.lower()] = (section_name, html)
    return render_template(
        "view_profile.html",
        user=flask_login.current_user,
        profile_sections=sections
    )


@blueprint.route("/profile/edit")
@flask_login.login_required
def edit_user():
    return ""


@blueprint.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for(current_app.config["INDEX_ROUTE"]))


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for(current_app.config["INDEX_ROUTE"]))

    form = ShortRegistrationForm()
    if form.validate_on_submit():
        try:
            new_user = User(email=form.email.data, password=form.password.data, is_admin=False)
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            flash("That email is already taken. Log in below", "danger")
            db.session.rollback()
        else:
            flash("Successfully signed up! Log in below", "success")
            send_email_verification_email(new_user)
        return redirect(url_for("account.login"))

    return render_template("register.html", form=form)
