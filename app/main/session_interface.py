from datetime import datetime
from uuid import uuid4
import pickle

from flask import current_app
from flask.sessions import SessionInterface
from flask.sessions import SessionMixin
from itsdangerous import Signer, BadSignature, want_bytes
from werkzeug.datastructures import CallbackDict


class ServerSideSession(CallbackDict, SessionMixin):
    """
    Actual session object returned by the session interface.
    Original code from Flask-Session.
    """

    def __init__(self, initial=None, sid=None, permanent=None):
        def on_update(self):
            self.modified = True

        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        if permanent:
            self.permanent = permanent
        self.modified = False


class TassaronSessionInterface(SessionInterface):
    """
    Server-side session interface adapted from Flask-Session
    """

    serializer = pickle

    def __init__(self, app, db):
        """
        Original code from Flask-Session.
        Adapted from a pull request: https://github.com/fengsp/flask-session/pull/12

        Table schema modified by tassaron
        user_id column is used to restore a user's server-side session upon login
        """
        self.app = app
        self.db = db
        self.key_prefix = "session:"
        self.permanent = True
        table = "sessions"

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
                    return "<Session data %s>" % self.data

            self.sql_session_model = db.session_ext_session_model = Session
        else:
            self.sql_session_model = db.session_ext_session_model

    @staticmethod
    def _generate_sid():
        return uuid4().hex

    @staticmethod
    def _get_signer(app):
        return Signer(app.secret_key, salt=f"{app.name}_session", key_derivation="hmac")

    def get_user_session(self, id):
        """Given a user id, return None or tuple of (session_id, unpickled session data)"""
        session = self.sql_session_model.query.filter_by(user_id=id).first()
        if session is not None:
            return (
                session.session_id[len(self.key_prefix) :],
                self.serializer.loads(want_bytes(session.data)),
            )

    def set_user_session(self, sid, uid):
        """Find existing session and assign a user_id to it. Can also set to None"""
        store_id = self.key_prefix + sid
        existing_session = self.sql_session_model.query.filter_by(
            session_id=store_id
        ).first()
        if existing_session is None:
            current_app.logger.error(f"The store_id {store_id} isn't valid")
        elif (
            existing_session.user_id is not None
            and uid is not None
            and existing_session.user_id != uid
        ):
            current_app.logger.error(
                "Session belongs to a different user. Shouldn't happen"
            )
        else:
            existing_session.user_id = uid
            self.db.session.add(existing_session)
            self.db.session.commit()

    def open_session(self, app, request):
        """Original code from Flask-Session. Modified by tassaron"""
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = self._generate_sid()
            return ServerSideSession(sid=sid, permanent=self.permanent)
        signer = self._get_signer(app)
        if signer is None:
            return None
        try:
            sid_as_bytes = signer.unsign(sid)
            sid = sid_as_bytes.decode()
        except BadSignature:
            sid = self._generate_sid()
            return ServerSideSession(sid=sid, permanent=self.permanent)

        store_id = self.key_prefix + sid
        saved_session = self.sql_session_model.query.filter_by(
            session_id=store_id
        ).first()
        if saved_session and saved_session.expiry <= datetime.utcnow():
            # Delete expired session
            self.db.session.delete(saved_session)
            self.db.session.commit()
            saved_session = None
        if saved_session:
            try:
                val = saved_session.data
                data = self.serializer.loads(want_bytes(val))
                return ServerSideSession(data, sid=sid)
            except:
                return ServerSideSession(sid=sid, permanent=self.permanent)
        return ServerSideSession(sid=sid, permanent=self.permanent)

    def save_session(self, app, session, response):
        """Original code from Flask-Session. Modified by tassaron"""
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        store_id = self.key_prefix + session.sid
        saved_session = self.sql_session_model.query.filter_by(
            session_id=store_id
        ).first()
        if not session:
            if session.modified:
                if saved_session:
                    self.db.session.delete(saved_session)
                    self.db.session.commit()
                response.delete_cookie(
                    app.session_cookie_name, domain=domain, path=path
                )
            return

        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        expires = self.get_expiration_time(app, session)
        val = self.serializer.dumps(dict(session))
        if saved_session:
            saved_session.data = val
            saved_session.expiry = expires
            self.db.session.commit()
        else:
            new_session = self.sql_session_model(store_id, val, expires)
            self.db.session.add(new_session)
            self.db.session.commit()

        session_id = self._get_signer(app).sign(want_bytes(session.sid))
        response.set_cookie(
            app.session_cookie_name,
            session_id,
            expires=expires,
            httponly=httponly,
            domain=domain,
            path=path,
            secure=secure,
        )
