"""
Root blueprint of the arcade module
"""
from flask import (
    session,
    render_template,
    abort,
    request,
    current_app,
    redirect,
    url_for,
)
from muffin_shop.blueprint import Blueprint
from muffin_shop.helpers.main.plugins import db
from muffin_shop.helpers.main.markdown import render_markdown
from muffin_shop.helpers.shop.util import convert_raw_cart_data_to_products
from muffin_shop.models.main.models import User
from muffin_shop.models.shop.checkout_models import Transaction
from muffin_shop.helpers.shop.util import obfuscate_number
from sqlalchemy.exc import IntegrityError


blueprint = Blueprint(
    "arcade",
    __name__,
)


@blueprint.app_context_processor
def inject_arcade_tokens():
    return {
        "arcade_prizes": convert_raw_cart_data_to_products(session["arcade_prizes"]),
        "arcade_tokens": session["arcade_tokens"],
        "mobile_friendly": True,
    }


@blueprint.before_app_request
def create_arcade_session():
    if "arcade_tokens" not in session:
        session["arcade_tokens"] = 0
    if "arcade_prizes" not in session:
        # same format as the shopping cart
        session["arcade_prizes"] = {}


@blueprint.index_route(endpoint="arcade.arcade_index")
def arcade_index():
    arcade_games = current_app.modules[".arcade"]["games"]
    return render_template(
        "arcade/arcade_index.html",
        arcade_header=render_markdown("arcade/header.md"),
        arcade_footer=render_markdown("arcade/footer.md"),
        games=arcade_games.items(),
    )


@blueprint.route("/game/<filename>")
def game_page(filename):
    arcade_games = current_app.modules[".arcade"]["games"]
    if filename not in arcade_games:
        abort(404)
    arcade_game = arcade_games[filename];
    description = "" if "description" not in arcade_game else f"<p>{arcade_game['description']}</p>"
    return render_template(
        "arcade/game_page.html",
        title=arcade_game["title"],
        description=f"<p>{arcade_game['blurb']}</p>{description}",
        tutorial="" if "tutorial" not in arcade_game else arcade_game["tutorial"],
        filename=filename,
        style=f"--bs-gutter-x: 0; border: 2px black solid; margin:auto; position: relative; {arcade_game['style']}",
        extra_html=""
        if "extra_html" not in arcade_game
        else arcade_game["extra_html"],
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
    server_side_sessions = [
        current_app.session_interface.get_user_session(user.id) for user in users
    ]
    try:
        server_side_sessions.remove(None)
    except ValueError:
        pass
    return render_template(
        "arcade/token_leaderboard.html",
        users=[
            (obfuscate_number(int(sss[1]["_user_id"])), sss[1]["arcade_tokens"])
            for sss in server_side_sessions
        ],
    )


@blueprint.route("/getprize/<uuid>")
def arcade_give_prize(uuid):
    if "transaction_id" not in session or session["transaction_id"] != uuid:
        abort(400)

    # determine total price
    products = convert_raw_cart_data_to_products(session["transaction_cart"])
    total_price = sum([product["price"] * product["quantity"] for product in products])
    if total_price > session["arcade_tokens"]:
        # the player can't afford these prizes
        return redirect(url_for("checkout.cancel_checkout", session_id=uuid))

    try:
        transaction = Transaction.query.filter_by(uuid=uuid).first()
        if transaction.price is not None:
            abort(400)
        transaction.price = total_price
        db.session.add(transaction)
        db.session.commit()
    except AttributeError as e:
        current_app.logger.error("No transaction?? %s", e)
    except IntegrityError:
        current_app.logger.error(
            "Error updating transaction record after giving prizes"
        )
        db.session.rollback()

    session["arcade_tokens"] -= total_price
    for prize, quantity in session["transaction_cart"].items():
        if prize in session["arcade_prizes"]:
            session["arcade_prizes"][prize] += quantity
        else:
            session["arcade_prizes"][prize] = quantity

    # redirect to success page which will deplete the shop inventory
    return redirect(url_for("checkout.successful_checkout", session_id=uuid))
