from flask import render_template, request
from muffin_shop.models.main.models import User, OldEmail, NewEmail
from muffin_shop.blueprint import Blueprint


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
    )
