import os
import sqlite3
from tassaron_flask.blueprint import Blueprint
from flask import render_template


blueprint = Blueprint(
    "huey",
    __name__,
)


@blueprint.admin_route("")
def task_overview():
    """
    Parse the Huey Results Database into a nice table for viewing
    """
    connection = sqlite3.connect(os.environ.get("HUEY_DB", "db/huey.db"))
    cursor = connection.cursor()
    cursor.execute("SELECT `value` FROM `kv`")
    values = cursor.fetchall()
    cursor.execute("SELECT `key` FROM `kv`")
    keys = cursor.fetchall()
    connection.close()
    return render_template("huey/task_overview.html", kv=list(zip(keys, values)))
