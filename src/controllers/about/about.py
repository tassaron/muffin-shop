from flask import render_template, flash, redirect, url_for, request
from muffin_shop.blueprint import Blueprint
from muffin_shop.helpers.main.markdown import render_markdown
from muffin_shop.helpers.about.contact import push_email_into_buffer, get_all_emails_from_buffer, pop_email_from_buffer, add_banned_word
from muffin_shop.forms.about.contact_forms import ContactForm, AddBannedWordForm
from muffin_shop.helpers.main.email import send_email
from muffin_shop.models.main.models import User
import os


blueprint = Blueprint(
    "about",
    __name__,
)


@blueprint.index_route()
def about_page():
    return render_template("about/about.html", about=render_markdown("about/about.md"))


@blueprint.route("/bio")
def bio_page():
    return render_template("about/bio.html", content=render_markdown("about/bio.md"))


@blueprint.route("/resume")
def resume_page():
    return render_template("about/resume.html", content=render_markdown("about/resume.md"))


@blueprint.route("/contact", methods=["GET", "POST"])
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
            flash(f"Thank you for contacting {os.environ.get('SITE_AUTHOR', 'me')}", "success")
        else:
            flash(f"Your last email was sent recently. Please try again tomorrow", "info")
    return render_template("about/contact.html", content=render_markdown("about/contact.md"), form=form)


@blueprint.admin_route("", methods=["GET", "POST"])
def admin_email_buffer():
    emails = get_all_emails_from_buffer()
    form = AddBannedWordForm()
    if form.validate_on_submit():
        word = form.banned_word.data.strip()
        if add_banned_word(word):
            flash(f"Banned \"{word}\"")
        else:
            flash("Word is already banned", "info")
    return render_template("admin/email_buffer.html", emails=emails, form=form)


@blueprint.admin_route("/send/<int:index>")
def contact_page_send(index):
    recipient = User.query.get(1).email
    email = pop_email_from_buffer(index)
    send_email(
        email["subj"],
        f"{email['body']}\n\nPLEASE RESPOND TO:\n{email['contact']}",
        recipient,
        force=True,
    )
    flash(f"Email sent to {recipient}", "primary")
    return redirect(url_for("about.admin_email_buffer"))


@blueprint.admin_route("/delete/<int:index>")
def contact_page_delete(index):
    pop_email_from_buffer(index)
    flash("Email deleted", "danger")
    return redirect(url_for("about.admin_email_buffer"))