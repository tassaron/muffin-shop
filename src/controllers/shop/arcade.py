"""
This shop has an arcade inside. How cool!
"""
from flask import session, render_template, abort
from muffin_shop.blueprint import Blueprint


arcade_games = {
    "style": "--bs-gutter-x: 0; margin:auto; position: relative;",
    "speed-limit": {
        "title": "Speed Limit",
        "style": "width: 640px; height: 598px;",
    },
    "rodents-revenge": {
        "title": "Rodent's Revenge",
        "style": "background:purple; width: 912px; height: 1036px; border: 2px solid black;",
    },
}


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


@blueprint.route("/game/<filename>")
def game_page(filename):
    if filename not in ("rodents-revenge", "speed-limit"):
        abort(404)
    return render_template(
        "arcade/game_page.html", title=arcade_games[filename]["title"], filename=filename, style=f"{arcade_games['style']} {arcade_games[filename]['style']}"
    )
