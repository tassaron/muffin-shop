from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField(
        "email", validators=[DataRequired(), Email(), Length(min=5, max=32)]
    )
    password = PasswordField(
        "password", validators=[Length(min=8, max=64), DataRequired()]
    )
    rememberme = BooleanField("remember me")
    submit = SubmitField("Log In")


class ShortRegistrationForm(FlaskForm):
    """A user registration form with just the email and password fields"""

    email = StringField(
        "email", validators=[DataRequired(), Email(), Length(min=5, max=32)]
    )
    password = PasswordField(
        "password", validators=[Length(min=8, max=64), DataRequired()]
    )
    confirmp = PasswordField(
        "confirm password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")
