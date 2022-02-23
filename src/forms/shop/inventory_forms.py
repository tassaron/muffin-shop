from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DecimalField, IntegerField
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Length,
    NumberRange,
    Optional,
)


class ProductForm(FlaskForm):
    name = StringField("name", validators=[DataRequired(), Length(min=1, max=40)])
    price = DecimalField("price", places=2, validators=[DataRequired()])
    description = TextAreaField(
        "description", validators=[DataRequired(), Length(min=1, max=500)]
    )
    image = StringField("image", validators=[DataRequired(), Length(min=5, max=36)])
    stock = IntegerField("stock", validators=[InputRequired(), NumberRange(min=0)])
    category_id = IntegerField(
        "category", validators=[DataRequired(), NumberRange(min=1)]
    )
    submit = SubmitField("Submit")


class ProductCategoryForm(FlaskForm):
    name = StringField("name", validators=[DataRequired(), Length(min=1, max=20)])
    image = StringField("image", validators=[DataRequired(), Length(min=5, max=36)])
    sorting_order = IntegerField(
        "sorting_order", validators=[Optional(), NumberRange(min=1)]
    )
    submit = SubmitField("Submit")
