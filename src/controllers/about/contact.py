from flask import render_template, flash, redirect, url_for, request
from muffin_shop.blueprint import Blueprint
from muffin_shop.helpers.main.markdown import render_markdown
from muffin_shop.forms.about.contact_forms import ContactForm, AddBannedWordForm
from muffin_shop.helpers.main.email import send_email
from muffin_shop.models.main.models import User
from muffin_shop.helpers.about.contact import (
    push_email_into_buffer,
    get_all_emails_from_buffer,
    pop_email_from_buffer,
    add_banned_word,
    add_spam_specimen,
    spam_path,
    spam_specimen_path,
)
import os


blueprint = Blueprint(
    "contact",
    __name__,
)


@blueprint.index_route(endpoint="contact.contact_page", methods=["GET", "POST"])
def contact_page():
    form = ContactForm()
    if form.validate_on_submit():
        success = push_email_into_buffer(
            request.remote_addr,
            form.mail_subject.data,
            form.mail_body.data,
            form.contact.data,
        )
        if success:
            flash(
                f"Thank you for contacting {os.environ.get('SITE_AUTHOR', 'me')}",
                "success",
            )
        else:
            flash(
                f"Your last email was sent recently. Please try again tomorrow", "info"
            )
    return render_template(
        "about/contact.html", content=render_markdown("about/contact.md"), form=form
    )


@blueprint.admin_route("", methods=["GET", "POST"])
def admin_email_buffer():
    emails = get_all_emails_from_buffer()
    form = AddBannedWordForm()
    if form.validate_on_submit():
        word = form.banned_word.data.strip()
        if add_banned_word(word):
            flash(f'Banned "{word}"', "primary")
        else:
            flash("Word is already banned", "info")
    return render_template(
        "admin/email_buffer.html", emails=emails, form=form, title="Email Buffer"
    )


@blueprint.admin_route("/spam")
def admin_spam_buffer():
    return render_template(
        "admin/email_buffer.html",
        emails=get_all_emails_from_buffer(spam_path),
        form=None,
        title="Spam Buffer",
    )


@blueprint.admin_route("/spam/specimens")
def admin_spam_specimen_buffer():
    return render_template(
        "admin/email_buffer.html",
        emails=get_all_emails_from_buffer(spam_specimen_path),
        form=None,
        title="Spam Specimens",
    )


@blueprint.admin_route("/send/<int:index>/<buffer>")
def contact_page_send(index, buffer):
    if buffer == "spam":
        buffer = spam_path
        next_page = "contact.admin_spam_buffer"
    elif buffer == "specimens":
        buffer = spam_specimen_path
        next_page = "contact.admin_spam_specimen_buffer"
    else:
        buffer = None
        next_page = "contact.admin_email_buffer"
    recipient = User.query.get(1).email
    email = pop_email_from_buffer(index, buffer)
    send_email(
        email["subj"],
        f"{email['body']}\n\nPLEASE RESPOND TO:\n{email['contact']}",
        recipient,
        force=True,
    )
    flash(f"Email sent to {recipient}", "primary")
    return redirect(url_for(next_page))


@blueprint.admin_route("/delete/<int:index>/<buffer>")
def contact_page_delete(index, buffer):
    if buffer == "spam":
        buffer = spam_path
        next_page = "contact.admin_spam_buffer"
    elif buffer == "specimens":
        buffer = spam_specimen_path
        next_page = "contact.admin_spam_specimen_buffer"
    else:
        buffer = None
        next_page = "contact.admin_email_buffer"
    pop_email_from_buffer(index, buffer)
    flash("Email deleted", "danger")
    return redirect(url_for(next_page))


@blueprint.admin_route("/markspam/<int:index>")
def contact_page_markspam(index):
    email = pop_email_from_buffer(index)
    add_spam_specimen(email)
    flash("Email added to spam list", "primary")
    return redirect(url_for("contact.admin_email_buffer"))
