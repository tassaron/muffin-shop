from flask import abort, url_for, session
from typing import List, Optional
from uuid import uuid4


class ArcadeSession:
    def __init__(self):
        self.id = uuid4().hex
        self.url = url_for("arcade.arcade_give_prize", uuid=self.id)


class ArcadeAdapter:
    """
    Adapts the shop checkout system to use arcade tokens
    """

    def __init__(self, *args):
        pass

    def start_session(self, *args) -> ArcadeSession:
        return ArcadeSession()

    @staticmethod
    def webhook():
        abort(404)
