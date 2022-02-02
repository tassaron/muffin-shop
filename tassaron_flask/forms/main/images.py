from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from tassaron_flask.helpers.main.images import Images


class UploadForm(FlaskForm):
    image = FileField(
        validators=[
            FileAllowed(Images, "Image files only"),
            FileRequired("Must be an image file"),
        ]
    )
    submit = SubmitField("Upload")