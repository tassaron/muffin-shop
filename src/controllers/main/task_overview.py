import os
import sqlite3
from muffin_shop.blueprint import Blueprint
from flask import render_template
from muffin_shop.helpers.main.tasks import huey


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
    binary_values = cursor.fetchall()
    cursor.execute("SELECT `key` FROM `kv`")
    keys = cursor.fetchall()
    connection.close()
    values = [huey.serializer.deserialize(value[0]) for value in binary_values]
    keys = [key[0] for key in keys]
    return render_template("admin/admin_kv_table.html", title="Huey Task Results", kv=list(zip(keys, values)))
