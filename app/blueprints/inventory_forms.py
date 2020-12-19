from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length, Range


class CreateProductForm(FlaskForm):
    name = StringField(
        "name", validators=[DataRequired(), Length(min=1, max=40)]
    )
    price = DecimalField(
        "price", places=2, validators=[DataRequired()]
    )
    description = TextAreaField(
        "description", validators=[DataRequired(), Length(min=1, max=500)]
    )
    image = StringField(
        "image", validators=[DataRequired(), Length(min=1, max=30)]
    )
    stock = IntegerField(
        "stock", validators=[DataRequired(), Range(min=0)]
    )
    category_id = IntegerField(
        "category", validators=[DataRequired(), Range(min=1)]
    )
    submit = SubmitField("Create")