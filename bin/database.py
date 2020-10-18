#!/usr/bin/env python3
"""
Database management script for a shop application. Use during initial setup or upgrade.
"""
from rainbow_shop.models import *
import os
import string
import random
from email_validator import validate_email, EmailNotValidError


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
    db.session.add(User(email="admin@example.com", password="test", is_admin=True))
    db.session.add(User(email="user@example.com", password="test", is_admin=False))
    db.session.add(ProductCategory(name="Fruits"))
    db.session.add(ProductCategory(name="Roots"))
    db.session.add(
        Product(
            name="Tomato",
            description="Vine-ripened and delicious!",
            price=4.50,
            category_id=1,
            stock=10,
            image="tomato.jpg",
        )
    )
    db.session.add(
        Product(
            name="Potato",
            description="A real tuber from the ground",
            price=3.70,
            category_id=2,
            stock=1,
            image="potato.jpg",
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
    parser.description = "Database management script for this shop application"
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("new", help="create a blank db file", nargs="?")
    actions.add_argument(
        "test", help="create a new db with filler data for testing", nargs="?"
    )
    parser.add_argument(
        "--db",
        help="URI to the database",
        default=db.app.config["SQLALCHEMY_DATABASE_URI"],
    )
    args = parser.parse_args()

    if args.new == "new":
        prompt_deletion(create_new_db, args.db)

    elif args.new == "test":
        prompt_deletion(create_test_db, args.db)
    else:
        parser.print_help()
