from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    StringField,
    SubmitField
)
from wtforms.validators import Length, DataRequired, Email


class ContactForm(FlaskForm):
    mail_subject = StringField("Your Name: ", validators=[Length(min=5, max=250)])
    mail_body = TextAreaField(validators=[DataRequired(), Length(min=5)])
    contact = StringField("Your Email or Phone Number: ", validators=[DataRequired(), Email()])
    submit = SubmitField("Send Message")