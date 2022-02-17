from tassaron_flask.blueprint import Blueprint


blueprint = Blueprint(
    "checkout",
    __name__,
)


@blueprint.route("/success")
def successful_checkout():
    return "success"


@blueprint.route("/cancel")
def cancel_checkout():
    return "cancelled"
