"""
This shop has an arcade inside. How cool!
"""
from flask import session, render_template, abort
from muffin_shop.blueprint import Blueprint


blueprint = Blueprint(
    "arcade",
    __name__,
)


@blueprint.app_context_processor
def inject_arcade_tokens():
    return {
        "arcade_tokens": session["arcade_tokens"],
    }


@blueprint.before_app_request
def create_arcade_session():
    if "arcade_tokens" not in session:
        session["arcade_tokens"] = 100


styles = {
    "speed-limit": "width: 640px; height: 598px;",
    "rodents-revenge": "background:purple; width: 912px; height: 1036px; border: 2px solid black;",
}
global_style = "--bs-gutter-x: 0; margin:auto;"


@blueprint.route("/game/<filename>")
def game_page(filename):
    if filename not in ("rodents-revenge", "speed-limit"):
        abort(404)
    return render_template(
        "arcade/game_page.html", filename=filename, style=f"{global_style} {styles[filename]}"
    )
