from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField, StringField
from wtforms.validators import Optional, Length
from muffin_shop.helpers.main.images import Images


class UploadForm(FlaskForm):
    image = FileField(
        validators=[
            FileAllowed(Images, "Image files only"),
            FileRequired("Must be an image file"),
        ]
    )
    title = StringField("title", validators=[Optional(), Length(min=1, max=60)])
    submit = SubmitField("Upload")
