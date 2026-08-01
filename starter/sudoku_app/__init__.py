import os

from flask import Flask

from .routes.main import register_routes
from .services.game_service import GameService


def create_app():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, '..', 'templates'),
        static_folder=os.path.join(base_dir, '..', 'static'),
    )
    app.config['SECRET_KEY'] = 'dev-secret-key'

    app.extensions['game_service'] = GameService()
    register_routes(app)
    return app


app = create_app()
CURRENT = app.extensions['game_service'].current
