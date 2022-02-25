"""
Root blueprint of the arcade module
"""
from flask import session, render_template, abort, request, current_app
from muffin_shop.blueprint import Blueprint
from muffin_shop.helpers.main.markdown import render_markdown
from muffin_shop.models.main.models import User
from muffin_shop.controllers.shop.shop import obfuscate_number


arcade_games = {
    "breakout": {
        "title": "Breakout",
        "blurb": "Bounce the ball off your paddle to destroy the bricks. Collect powerups!",
        "style": "width: 640px; height: 480px;",
        "multiplier": 0.5,
    },
    "jezzball": {
        "title": "Jezzball",
        "blurb": "Place walls to entrap the balls and flood-fill the level",
        "style": "width: 720px; height: 640px;",
        "multiplier": 0.2,
        "extra_html": "<button style='width: 9rem; height: 3rem;' id='swap_button' type='button'>Swap Direction</button>",
    },
    "speed-limit": {
        "title": "Speed Limit",
        "blurb": "Pass cars while obeying the speed limit! 🛑",
        "style": "width: 640px; height: 598px;",
        "multiplier": 0.01,
    },
    "rodents-revenge": {
        "title": "Rodent's Revenge",
        "blurb": "Push crates to trap the cats and collect cheese",
        "style": "background:purple; width: 912px; height: 1036px; border: 2px solid black;",
        "multiplier": 0.1,
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
        session["arcade_tokens"] = 0


@blueprint.index_route()
def arcade_index():
    return render_template(
        "arcade/arcade_index.html",
        arcade_description=render_markdown("arcade.md"),
        games=arcade_games.items(),
    )


@blueprint.route("/game/<filename>")
def game_page(filename):
    if filename not in arcade_games:
        abort(404)
    return render_template(
        "arcade/game_page.html",
        title=arcade_games[filename]["title"],
        filename=filename,
        style=f"--bs-gutter-x: 0; margin:auto; position: relative; {arcade_games[filename]['style']}",
        extra_html=""
        if "extra_html" not in arcade_games[filename]
        else arcade_games[filename]["extra_html"],
    )


@blueprint.route("/token/submit", methods=["POST"])
def token_submit():
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