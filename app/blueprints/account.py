"""
Handles logging in/registering/editing a user account
"""
from flask import Blueprint, flash, request, render_template, current_app
import flask_login
from is_safe_url import is_safe_url
from rainbow_shop.forms import ShortRegistrationForm, LoginForm


blueprint = Blueprint("account", __name__, template_folder="../templates/account")


@blueprint.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        form = LoginForm()
        return render_template("login.html", form=form)

    if form.validate_on_submit():
        pass


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
    pass


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        form = ShortRegistrationForm()
        return render_template("register.html", form=form)

    if form.validate_on_submit():
        pass
