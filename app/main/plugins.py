from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_session import Session
from itsdangerous import want_bytes


class SqlSession(Session):
    def init_app(self, app):
        """
        Patch an extra column onto Flask-Session's otherwise-lovely model
        user_id column is used to restore a user's server-side session upon login
        For convenience we'll also patch get and set methods onto the session_interface
        """
        super().init_app(app)
        app.session_interface.sql_session_model.__table_args__ = {'extend_existing' : True}
        app.session_interface.sql_session_model.extend_existing = True
        app.session_interface.sql_session_model.user_id = app.session_interface.db.Column(
            app.session_interface.db.Integer, app.session_interface.db.ForeignKey("user.id"), nullable=True
        )

        def get_user_session(id):
            """Given a user id, return None or tuple of (session_id, unpickled session data)"""
            session = app.session_interface.sql_session_model.query.filter_by(user_id=id).first()
            if session is not None:
                return (
                    session.session_id[len(app.session_interface.key_prefix):],
                    app.session_interface.serializer.loads(want_bytes(session.data))
                )

        def set_user_session(sess, uid):
            """Find existing session and assign a user_id to it. Can also set to None"""
            sid = sess.sid
            store_id = app.session_interface.key_prefix + sid
            existing_session = app.session_interface.sql_session_model.query.filter_by(session_id=store_id).first()
            if existing_session is None:
                app.logger.error(f"The store_id {store_id} isn't valid")
            elif existing_session.user_id is not None and uid is not None and existing_session.user_id != uid:
                app.logger.error("Session belongs to a different user. Shouldn't happen")
            else:
                existing_session.user_id = uid
                app.session_interface.db.session.add(existing_session)
                app.session_interface.db.session.commit()

        app.session_interface.get_user_session = get_user_session
        app.session_interface.set_user_session = set_user_session


def create_plugins():
    return SQLAlchemy(), Migrate(), Bcrypt(), LoginManager(), SqlSession()


plugins = create_plugins()
db, migrate, bcrypt, login_manager, sql_session = plugins