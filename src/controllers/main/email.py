from flask import render_template, request, redirect, url_for
from muffin_shop.models.main.models import OldEmail, NewEmail, EmailTypes
from muffin_shop.blueprint import Blueprint
from muffin_shop.helpers.main.email import archive_email


blueprint = Blueprint(
    "email",
    __name__,
)


@blueprint.admin_route("")
def admin_email_list():
    user_id = request.args.get("user_id", None)
    if user_id:
        title = f"Email Records for User {user_id}"
        old_emails = OldEmail.query.filter_by(user_id=user_id).all()
        new_emails = NewEmail.query.filter_by(user_id=user_id).all()
    else:
        title = "Email Records"
        old_emails = OldEmail.query.all()
        new_emails = NewEmail.query.all()
    return render_template(
        "main/admin_email.html",
        title=title,
        old_emails=old_emails,
        new_emails=new_emails,
        email_types=EmailTypes,
    )


@blueprint.admin_route("/archive/<int:email_id>")
def admin_force_archive_email(email_id):
    email = NewEmail.query.get_or_404(email_id)
    archive_email(email)
    return redirect(url_for(".admin_email_list"))
