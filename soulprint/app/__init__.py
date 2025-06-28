from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    from . import config
    app.config.from_object(config)

    db.init_app(app)

    from .routes import bp
    app.register_blueprint(bp)

    return app
