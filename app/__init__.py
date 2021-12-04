import os

from dotenv import load_dotenv
from flask import Flask, current_app
from app.models import db, migrate


def create_app(config='config.py'):
    # load env
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    # init app
    app = Flask(__name__)
    app.config.from_pyfile(config)
    db.init_app(app)
    migrate.init_app(app, db)

    # import route here
    from app.routes import api

    # set routes
    app.register_blueprint(api, url_prefix='/api')
    

    @app.route("/")
    def home():
        return f"Welcome to {current_app.config['APP_NAME']}!"

    return app
