from flask import current_app, render_template, flash, redirect, url_for
from flask_login import current_user
from werkzeug.datastructures import MultiDict
from tassaron_flask_template.blueprint import Blueprint
from tassaron_flask_template.decorators import admin_required
from tassaron_flask_template.plugins import db
from .inventory_forms import ProductForm
from .inventory_models import Product
import os


blueprint = Blueprint("inventory", __name__, template_folder="../templates/inventory")


@blueprint.route("")
@admin_required
def list_products():
    return render_template("list_products.html", products=Product.query.all())


@blueprint.route("/create", methods=["GET", "POST"])
@admin_required
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        kwargs = {
            "name": form.name.data,
            "price": form.price.data,
            "description": form.description.data,
            "image": form.image.data,
            "stock": form.stock.data,
            "category_id": form.category_id.data,
        }
        try:
            product = Product(**kwargs)
        except:
            abort(400)
        db.session.add(product)
        db.session.commit()
        flash(f"Added {product.name}!", "success")
        return redirect(url_for(".list_products"))
    return render_template("edit_product.html", title="Create New Product", form=form)


@blueprint.route("/delete/<int:id>")
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    flash(f"Product {product.name} deleted!", "danger")
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for(".list_products"))


@blueprint.route("/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    form = ProductForm()
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.description = form.description.data
        product.image = form.image.data
        product.stock = form.stock.data
        product.category_id = form.category_id.data
        db.session.add(product)
        db.session.commit()
        flash(f"Updated {product.name}!", "success")
        return redirect(url_for(".list_products"))
    filled_form = {
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "image": product.image,
        "stock": product.stock,
        "category_id": product.category_id,
    }
    form = ProductForm(formdata=MultiDict(filled_form))
    return render_template("edit_product.html", title=f"Edit {product.name}", form=form)
