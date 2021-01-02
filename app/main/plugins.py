from flask import current_app
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_session import Session, SqlAlchemySessionInterface
from itsdangerous import want_bytes


class TassaronSessionInterface(SqlAlchemySessionInterface):
    """
    Add get and set methods onto the FlaskSessionInterface provided by Flask-Session
    """
    def __init__(
            self, app, db, table, key_prefix, use_signer=False, permanent=True):
        """
        Copy of parent's __init__ with fixes merged: https://github.com/fengsp/flask-session/pull/12
        Patch an extra column onto Flask-Session's otherwise-lovely model
        user_id column is used to restore a user's server-side session upon login
        """
        if db is None:
            db = SQLAlchemy(app)
        self.db = db
        self.key_prefix = key_prefix
        self.use_signer = use_signer
        self.permanent = permanent

        if table not in self.db.metadata:
            # ^ Only create Session Model if it doesn't already exist
            # Fixes the SQLAlchemy "extend_existing must be true" exception during tests
            class Session(self.db.Model):
                __tablename__ = table

                id = self.db.Column(self.db.Integer, primary_key=True)
                session_id = self.db.Column(self.db.String(256), unique=True)
                data = self.db.Column(self.db.Text)
                expiry = self.db.Column(self.db.DateTime)
                user_id = self.db.Column(
                    self.db.Integer, self.db.ForeignKey("user.id"), nullable=True
                )

                def __init__(self, session_id, data, expiry):
                    self.session_id = session_id
                    self.data = data
                    self.expiry = expiry

                def __repr__(self):
                    return '<Session data %s>' % self.data

            self.sql_session_model = db.session_ext_session_model = Session
        else:
            self.sql_session_model = db.session_ext_session_model
        
    def get_user_session(self, id):
        """Given a user id, return None or tuple of (session_id, unpickled session data)"""
        session = self.sql_session_model.query.filter_by(user_id=id).first()
        if session is not None:
            return (
                session.session_id[len(self.key_prefix):],
                self.serializer.loads(want_bytes(session.data))
            )

    def set_user_session(self, sid, uid):
        """Find existing session and assign a user_id to it. Can also set to None"""
        store_id = self.key_prefix + sid
        existing_session = self.sql_session_model.query.filter_by(session_id=store_id).first()
        if existing_session is None:
            current_app.logger.error(f"The store_id {store_id} isn't valid")
        elif existing_session.user_id is not None and uid is not None and existing_session.user_id != uid:
            current_app.logger.error("Session belongs to a different user. Shouldn't happen")
        else:
            existing_session.user_id = uid
            self.db.session.add(existing_session)
            self.db.session.commit()


class SqlSession(Session):
    """
    Add our customized session interface to Flask-Session
    """
    def init_app(self, app):
        super().init_app(app)
        app.session_interface = TassaronSessionInterface(
            app, app.config['SESSION_SQLALCHEMY'],
            "sessions", "session:", True, True
        )


def create_plugins():
    return SQLAlchemy(), Migrate(), Bcrypt(), LoginManager(), SqlSession()


plugins = create_plugins()
db, migrate, bcrypt, login_manager, sql_session = plugins