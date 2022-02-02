"""
Ensure that a user cannot receive a second email until they've taken action
on the previous one, or until enough time has passed
"""
from tassaron_flask.helpers.main.app_factory import create_app, init_app
from tassaron_flask.helpers.main.plugins import db
from tassaron_flask.models.main.models import User
from tassaron_flask.helpers.main.email import *
from huey.api import Result
import os
import tempfile


def test_email_outbox_for_reset_password():
    app = create_app()
    db_fd, db_path = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite+pysqlite:///" + db_path
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["TESTING"] = True
    app.config["SERVER_NAME"] = "localhost:5000"
    app = init_app(app)
    with app.app_context():
        db.create_all()
        user = User(email="test@example.com", email_verified=True, password="password", is_admin=False)
        db.session.add(user)
        db.session.commit()
        client = app.test_client()
        # sending email to user should first succeed
        result = send_password_reset_email(user)
        assert type(result) == Result

        # sending email to user should now fail
        try:
            send_password_reset_email(user)
        except OutboxFull:
            pass
        else:
            assert "Didn't raise OutboxFull" == True

        # visiting the reset_password view won't clear the outbox
        client.get(f"/account/reset_password/{result()}")
        try:
            send_password_reset_email(user)
        except OutboxFull:
            pass
        else:
            assert "Didn't raise OutboxFull" == True

        # confirming a new password will actually clear the outbox
        client.post(
            f"/account/reset_password/{result()}",
            data={"password": "password", "confirm_password": "password"},
        )
        # sending email should now succeed!
        result = send_password_reset_email(user)
        assert type(result) == Result
    os.close(db_fd)
    os.unlink(db_path)


def test_email_outbox_isolated_per_user():
    app = create_app()
    db_fd, db_path = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite+pysqlite:///" + db_path
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["TESTING"] = True
    app.config["SERVER_NAME"] = "localhost:5000"
    app = init_app(app)
    with app.app_context():
        db.create_all()
        user1 = User(email="1@example.com", email_verified=True, password="password", is_admin=False)
        user2 = User(email="2@example.com", email_verified=True, password="password", is_admin=False)
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        send_password_reset_email(user1)
        # sending email to user2 should not be affected
        result = send_password_reset_email(user2)
        assert type(result) == Result
    os.close(db_fd)
    os.unlink(db_path)