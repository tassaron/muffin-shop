"""
Root blueprint of the arcade module
"""
from flask import session, render_template, abort, request, current_app
from muffin_shop.blueprint import Blueprint
from muffin_shop.helpers.main.markdown import render_markdown
from muffin_shop.models.main.models import User
from muffin_shop.controllers.shop.shop import obfuscate_number


blueprint = Blueprint(
    "arcade",
    __name__,
)


@blueprint.app_context_processor
def inject_arcade_tokens():
    return {
        "arcade_tokens": session["arcade_tokens"],
        "mobile_friendly": True,
    }


@blueprint.before_app_request
def create_arcade_session():
    if "arcade_tokens" not in session:
        session["arcade_tokens"] = 0


@blueprint.index_route()
def arcade_index():
    arcade_games = current_app.modules[".arcade"]["games"]
    return render_template(
        "arcade/arcade_index.html",
        arcade_description=render_markdown("arcade.md"),
        games=arcade_games.items(),
    )


@blueprint.route("/game/<filename>")
def game_page(filename):
    arcade_games = current_app.modules[".arcade"]["games"]
    if filename not in arcade_games:
        abort(404)
    return render_template(
        "arcade/game_page.html",
        title=arcade_games[filename]["title"],
        filename=filename,
        style=f"--bs-gutter-x: 0; border: 2px black solid; margin:auto; position: relative; {arcade_games[filename]['style']}",
        extra_html=""
        if "extra_html" not in arcade_games[filename]
        else arcade_games[filename]["extra_html"],
        mobile_friendly=False,
    )


@blueprint.route("/token/submit", methods=["POST"])
def token_submit():
    arcade_games = current_app.modules[".arcade"]["games"]
    data = request.get_json()
    if data["filename"] not in arcade_games:
        abort(400)
    try:
        new_score = int(
            int(data["score"]) * arcade_games[data["filename"]]["multiplier"]
        )
        session["arcade_tokens"] += new_score
        return {"payout": new_score}
    except (KeyError, ValueError, TypeError):
        abort(400)


@blueprint.route("/token/leaderboard")
def arcade_token_leaderboard():
    users = User.query.all()
    server_side_sessions = [current_app.session_interface.get_user_session(user.id) for user in users]
    server_side_sessions.remove(None)
    return render_template(
        "arcade/token_leaderboard.html",
        users=[(obfuscate_number(int(sss[1]["_user_id"])), sss[1]["arcade_tokens"]) for sss in server_side_sessions]
    )