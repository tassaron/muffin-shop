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
)
import flask_login
from sqlalchemy.exc import IntegrityError
from is_safe_url import is_safe_url
from tassaron_flask_template.plugins import db
from tassaron_flask_template.forms import ShortRegistrationForm, LoginForm, RequestPasswordResetForm, PasswordResetForm
from tassaron_flask_template.models import User, ShippingAddress
from tassaron_flask_template.email import send_password_reset_email


blueprint = Blueprint(
    "account",
    __name__,
    static_folder="../static",
    template_folder="../templates/account",
)


@blueprint.route("/login", methods=["POST", "GET"])
def login():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for("storefront.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password_hash(form.password.data):
            flash("Logged in! ✔️", "success")
            flask_login.login_user(user, remember=form.rememberme.data)
            next_page = request.args.get("next")
            return (
                redirect(next_page)
                if next_page and is_safe_url(next_page, url_for("storefront.index"))
                else redirect(url_for("storefront.index"))
            )
        else:
            flash("Wrong email or password.", "danger")

    return render_template("login.html", form=form)


@blueprint.route("/resetpassword", methods=["GET", "POST"])
def reset_password():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for("storefront.index"))
    
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_password_reset_email(user)
        flash("An email was sent with instructions to reset your password", "info")
        return redirect(url_for(".login"))
    return render_template("reset_password.html", form=form)


@blueprint.route("/resetpassword/<token>", methods=["GET", "POST"])
def change_password(token):
    if flask_login.current_user.is_authenticated:
        return redirect(url_for("storefront.index"))

    user = User.verify_password_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for(".reset_password"))
    
    form = PasswordResetForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash("Your password has been updated! Now you can log in")
        return redirect((url_for(".login")))

    return render_template("change_password.html", form=form)


# Everything below this point is for logged-in users
#---------------------------------------------------


@blueprint.route("/profile")
@flask_login.login_required
def user_dashboard():
    """ Let the user manage their shipping address, change password """
    user_id = int(flask_login.current_user.get_id())
    # shipping = ShippingAddress.query.filter_by(id=user_id).first()
    return f"{str(user_id)}"


@blueprint.route("/profile/edit")
@flask_login.login_required
def edit_user():
    pass


@blueprint.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for("storefront.index"))


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for("storefront.index"))

    form = ShortRegistrationForm()
    if form.validate_on_submit():
        try:
            db.session.add(
                User(email=form.email.data, password=form.password.data, is_admin=False)
            )
            db.session.commit()
        except IntegrityError:
            flash("That email is already taken. Log in below", "danger")
            db.session.rollback()
        else:
            flash("Successly signed up! Now you can log in", "success")
        return redirect(url_for("account.login"))

    return render_template("register.html", form=form)
