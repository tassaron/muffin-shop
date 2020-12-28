from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length, Email, EqualTo
from .models import User


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

    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "password", validators=[Length(min=8, max=64), DataRequired()]
    )
    confirmp = PasswordField(
        "confirm password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")


class RequestPasswordResetForm(FlaskForm):
    """User requests that their password be reset"""

    email = StringField("email", validators=[DataRequired(), Email()])
    submit = SubmitField("Reset Your Password")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email.")


class PasswordResetForm(FlaskForm):
    """User submits a new password after verifying email"""

    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=64)]
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Password")
