#!/usr/bin/env python3
"""
Database management script for a shop application. Use during initial setup or testing.
"""
import argparse
from muffin_shop.helpers.main.app_factory import create_app
from muffin_shop.models.main.models import *
from muffin_shop.helpers.main.plugins import db
from muffin_shop.helpers.main.session_interface import TassaronSessionInterface
from muffin_shop.models.shop.inventory_models import *
import os
import string
import random
from email_validator import validate_email, EmailNotValidError


app = create_app()
db.init_app(app)
app.session_interface = TassaronSessionInterface(app, db)


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
    admin = User(email=email, password=password, email_verified=True, is_admin=True)
    db.session.add(admin)
    db.session.commit()
    """
    print("Initializing app (needed to construct URLs)...")
    from muffin_shop.main import init_app
    init_app(app)
    print("Sending verification email...")
    from muffin_shop.email import send_email_verification_email
    send_email_verification_email(admin)
    """
    print(f"Admin's temporary password is {password}")


def create_test_db():
    db.create_all()
    add_test_users()
    db.session.commit()


def create_test_db_shop():
    db.create_all()
    add_test_users()
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
            name="Veggies",
            image="potato.jpg",
        )
    )
    db.session.add(
        ProductCategory(
            name="Flowers",
            image="potato.jpg",
        )
    )
    db.session.add(
        ProductCategory(
            name="Baked Goods",
            image="potato.jpg",
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
    db.session.add(
        Product(
            name="Tomato",
            price=1.0,
            description="Fruit from a lovely friend",
            image="potato.jpg",
            stock=10,
            category_id=1,
        )
    )
    db.session.add(
        Product(
            name="Campanula",
            price=1.5,
            description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            image="potato.jpg",
            stock=100,
            category_id=2,
        )
    )
    db.session.add(
        Product(
            name="Hot Cake",
            price=1.0,
            description="It sure sells like it!",
            image="potato.jpg",
            stock=0,
            category_id=3,
        )
    )
    db.session.commit()


def add_test_users():
    db.session.add(User(email="admin@example.com", email_verified=True, password="password", is_admin=True))
    db.session.add(User(email="user@example.com", password="password", is_admin=False))


def main():
    """
    Run commandline argument parser
    """
    def prompt_deletion(func):
        dirname = os.path.abspath(os.path.dirname(args.db).split(":///", 1)[1])
        basename = os.path.basename(args.db)
        filename = "/".join((dirname, basename))
        if os.path.exists(filename):
            print(f"This task will delete the current { basename }.")
            if args.yes == False:
                resp = input("Proceed? [y/N] ")
                if resp.strip().lower() != "y":
                    return
            os.remove(filename)
        elif not os.path.exists(dirname):
            os.makedirs(dirname)
        return func()

    parser = argparse.ArgumentParser()
    parser.description = "Database creation script for this Flask application"
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("new", help="create a blank db file", nargs="?")
    actions.add_argument(
        "test", help="create a new db with filler data for testing", nargs="?"
    )
    parser.add_argument(
        "--yes", "-y", "-f",
        help="assume yes (delete the database)",
        default=False,
        action="store_true",
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
            prompt_deletion(create_new_db)

        elif args.new == "test":
            if args.shop:
                prompt_deletion(create_test_db_shop)
            else:
                prompt_deletion(create_test_db)
        else:
            parser.print_help()


if __name__ == "__main__":
    main()
