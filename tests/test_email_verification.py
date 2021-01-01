from tassaron_flask_template.main import create_app, init_app
from tassaron_flask_template.main.plugins import db
from tassaron_flask_template.main.models import User
from tassaron_flask_template.email import *
from huey.api import Result
import tempfile
import os


def test_email_verification():
    app = create_app()
    db_fd, db_path = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite+pysqlite:///" + db_path
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["TESTING"] = True
    app.config["CLIENT_SESSIONS"] = True
    app.config["SERVER_NAME"] = "localhost:5000"
    app = init_app(app)
    with app.app_context():
        db.create_all()
        user = User(email="test@example.com", password="password", is_admin=False)
        db.session.add(user)
        db.session.commit()
        client = app.test_client()
        client.post(
            "/account/login",
            data={"email": "test@example.com", "password": "password"},
        )
        # email_verified is false after initial registration
        assert user.email_verified == False

        # sending email to user should fail
        try:
            result = send_password_reset_email(user)
        except Unverified:
            pass
        else:
            assert "Didn't raise Unverified" == True

        # verify email
        result = send_email_verification_email(user)
        client.get(f"/account/verify_email/{result()}")
        assert user.email_verified == True

        # sending email should now succeed!
        # client.get("/account/logout", follow_redirects=True)
        result = send_password_reset_email(user)
        assert type(result) == Result

        # updating the email will unverify it again
        user.update_email("")
        assert user.email_verified == False
    os.close(db_fd)
    os.unlink(db_path)