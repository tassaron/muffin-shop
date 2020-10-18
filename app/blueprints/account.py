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
from is_safe_url import is_safe_url
from rainbow_shop.__init__ import db
from rainbow_shop.forms import ShortRegistrationForm, LoginForm
from rainbow_shop.models import User


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
        if user and user.check_password_hash(user.password, form.password.data):
            flask_login.login_user(user, remember=form.rememberme.data)
            next_page = request.args.get("next")
            return (
                redirect(next_page)
                if next_page and is_safe_url(next_page)
                else redirect(url_for("storefront.index"))
            )
        else:
            flash("Wrong email or password.", "danger")

    return render_template("login.html", form=form)


@flask_login.login_required
@blueprint.route("/profile")
def user_dashboard():
    """ Let the user manage their shipping address, change password """
    pass


@blueprint.route("/profile/edit")
def edit_user():
    pass


@blueprint.route("/changepassword", methods=["GET", "POST"])
def change_password():
    pass


@blueprint.route("/logout")
def logout():
    flask_login.logout_user()
    return redirect(url_for("storefront.index"))


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for("storefront.index"))

    form = ShortRegistrationForm()
    if form.validate_on_submit():
        db.session.add(
            User(email=form.email.data, password=form.password.data, is_admin=False)
        )
        db.session.commit()
        flash("Successly signed up! Now you can log in", "success")
        return redirect(url_for("account.login"))

    return render_template("register.html", form=form)
