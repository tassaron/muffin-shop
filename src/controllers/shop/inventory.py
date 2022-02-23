from flask import render_template, flash, redirect, url_for, abort
from werkzeug.datastructures import MultiDict
from muffin_shop.blueprint import Blueprint
from muffin_shop.helpers.main.plugins import db
from muffin_shop.forms.shop.inventory_forms import ProductForm, ProductCategoryForm
from muffin_shop.models.shop.inventory_models import Product, ProductCategory
import os


blueprint = Blueprint("inventory", __name__)


##############
# PRODUCTS
##############


@blueprint.admin_route("")
def list_products():
    return render_template("inventory/list_products.html", products=Product.query.all())


@blueprint.admin_route("/create", methods=["GET", "POST"])
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        kwargs = {
            "name": form.name.data,
            "price": int(form.price.data * 100),
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
    return render_template(
        "inventory/edit_product.html", title="Create New Product", form=form
    )


@blueprint.admin_route("/delete/<int:id>")
def delete_product(id):
    product = Product.query.get_or_404(id)
    flash(f"Product {product.name} deleted!", "danger")
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for(".list_products"))


@blueprint.admin_route("/edit/<int:id>", methods=["GET", "POST"])
def edit_product(id):
    product = Product.query.get_or_404(id)
    form = ProductForm()
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = int(form.price.data * 100)
        product.description = form.description.data
        product.image = form.image.data
        product.stock = form.stock.data
        product.category_id = form.category_id.data
        product.payment_uuid = None
        db.session.add(product)
        db.session.commit()
        flash(f"Updated {product.name}!", "success")
        return redirect(url_for(".list_products"))
    filled_form = {
        "name": product.name,
        "price": product.price / 100,
        "description": product.description,
        "image": product._image,
        "stock": product.stock,
        "category_id": product.category_id,
    }
    form = ProductForm(formdata=MultiDict(filled_form))
    return render_template(
        "inventory/edit_product.html", title=f"Edit {product.name}", form=form
    )


##############
# CATEGORIES
##############


@blueprint.admin_route("/categories")
def list_product_categories():
    return render_template(
        "inventory/list_product_categories.html", categories=ProductCategory.query.all()
    )


@blueprint.admin_route("/categories/create", methods=["GET", "POST"])
def create_product_category():
    form = ProductCategoryForm()
    if form.validate_on_submit():
        kwargs = {
            "name": form.name.data,
            "image": form.image.data,
        }
        try:
            category = ProductCategory(**kwargs)
        except:
            abort(400)
        db.session.add(category)
        db.session.commit()
        flash(f"Added {category.name} category!", "success")
        return redirect(url_for(".list_product_categories"))
    return render_template(
        "inventory/edit_product_category.html", title="Create New Category", form=form
    )


@blueprint.admin_route("/categories/delete/<int:id>")
def delete_product_category(id):
    category = ProductCategory.query.get_or_404(id)
    flash(f"Category {category.name} deleted!", "danger")
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for(".list_product_categories"))


@blueprint.admin_route("/categories/edit/<int:id>", methods=["GET", "POST"])
def edit_product_category(id):
    category = ProductCategory.query.get_or_404(id)
    form = ProductCategoryForm()
    if form.validate_on_submit():
        category.name = form.name.data
        category.image = form.image.data
        db.session.add(category)
        db.session.commit()
        flash(f"Updated {category.name} category!", "success")
        return redirect(url_for(".list_product_categories"))
    filled_form = {
        "name": category.name,
        "image": category._image,
    }
    form = ProductCategoryForm(formdata=MultiDict(filled_form))
    return render_template(
        "inventory/edit_product_category.html",
        title=f"Edit {category.name} Category",
        form=form,
    )
