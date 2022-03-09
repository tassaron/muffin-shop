from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
)


class BlogPostForm(FlaskForm):
    content = TextAreaField(
        "content", validators=[DataRequired(), Length(min=1, max=5000)]
    )
    submit = SubmitField("Submit")
