from flask import abort, url_for
from typing import List, Optional


class ArcadeSession:
    id = 1


class ArcadeAdapter:
    """
    Adapts the shop checkout system to use arcade tokens
    """

    def __init__(self, products: List[dict]):
        self.products = products

    def start_session(
        self,
        success_url: str,
        cancel_url: str,
        mode: str,
        email_address: Optional[str] = None,
    ) -> ArcadeSession:
        self.session = ArcadeSession()
        self.session.id = str(ArcadeSession.id)
        ArcadeSession.id += 1
        self.session.url = url_for("about_page")
        return self.session

    @staticmethod
    def webhook():
        abort(404)
