from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, StringField, SubmitField
from wtforms.validators import Length, DataRequired, Email, Optional


class ContactForm(FlaskForm):
    mail_subject = StringField("Your Name", validators=[Length(min=1, max=250)])
    mail_body = TextAreaField("Message", validators=[DataRequired(), Length(min=5)])
    contact = StringField("Your Email Address", validators=[DataRequired(), Email()])
    submit = SubmitField("Send Message")


class AddBannedWordForm(FlaskForm):
    banned_word = StringField(
        "Ban word/URL", validators=[DataRequired(), Length(min=7, max=5000)]
    )
    submit = SubmitField("Ban")
