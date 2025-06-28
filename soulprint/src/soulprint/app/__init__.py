from flask import Flask
from .config import Config
from .models.db import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Import routes inside the function to avoid circular imports
    from .routes import routes
    app.register_blueprint(routes)

    return app
