#!/usr/bin/env python3
"""
Database management script for a shop application. Use during initial setup or testing.
"""
from tassaron_flask_template.__init__ import create_app
from tassaron_flask_template.models import *
from tassaron_flask_template.blueprints.inventory_models import *
import os
import string
import random
from email_validator import validate_email, EmailNotValidError


app = create_app()
db.init_app(app)


def random_password(length):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(password_characters) for i in range(length))


def create_new_db(email=None):
    db.create_all()
    while not email:
        try:
            email = validate_email(
                input("Email address for admin: ").strip()
            ).ascii_email
        except EmailNotValidError:
            pass
    password = random_password(16)
    db.session.add(User(email=email, password=password, is_admin=True))
    db.session.commit()
    print(f"Admin's temporary password is {password}")


def create_test_db():
    db.create_all()
    db.session.add(User(email="admin@example.com", password="password", is_admin=True))
    db.session.add(User(email="user@example.com", password="password", is_admin=False))
    db.session.commit()


def create_test_db_shop():
    db.create_all()
    db.session.add(User(email="admin@example.com", password="password", is_admin=True))
    db.session.add(User(email="user@example.com", password="password", is_admin=False))
    db.session.add(
        ShippingAddress(
            user_id=2,
            first_name="Bri",
            last_name="Rainey",
            phone="5550005555",
            address1="123 Fake St",
            address2="Apt 9",
            postal_code="A0B1C2",
            city="Anytown",
            province="ON",
        )
    )
    db.session.add(
        ProductCategory(
            name="Food",
        )
    )
    db.session.add(
        Product(
            name="Potato",
            price=1.0,
            description="Tuber from the ground",
            image="potato.jpg",
            stock=1,
            category_id=1,
        )
    )
    db.session.commit()


def prompt_deletion(func, uri):
    dirname = os.path.abspath(os.path.dirname(uri).split(":///", 1)[1])
    basename = os.path.basename(uri)
    filename = "/".join((dirname, basename))
    if os.path.exists(filename):
        print(f"This task will delete the current { basename }.")
        resp = input("Proceed? [y/N] ")
        if resp.strip().lower() != "y":
            return
        os.remove(filename)
    elif not os.path.exists(dirname):
        os.makedirs(dirname)
    return func()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.description = "Database creation script for this shop application"
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("new", help="create a blank db file", nargs="?")
    actions.add_argument(
        "test", help="create a new db with filler data for testing", nargs="?"
    )
    parser.add_argument(
        "--shop",
        help="create a new db with filler data for testing the shop",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--db",
        help="URI to the database",
        default=app.config["SQLALCHEMY_DATABASE_URI"],
    )
    args = parser.parse_args()

    with app.app_context():
        if args.new == "new":
            prompt_deletion(create_new_db, args.db)

        elif args.new == "test":
            if args.shop:
                prompt_deletion(create_test_db_shop, args.db)
            else:
                prompt_deletion(create_test_db, args.db)
        else:
            parser.print_help()
