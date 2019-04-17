import os

from flask import Flask
from flask_caching import Cache


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        DATABASE=os.environ.get("DATABASE"),
        SITE_SECRET=os.environ.get("SITE_SECRET"),
        SITE_VERIFY_URL="https://www.google.com/recaptcha/api/siteverify",
        RECAPTCHA_RESPONSE_PARAM="g-recaptcha-response",
        CACHE_TYPE="simple",   # Flask-Caching related configs
        CACHE_DEFAULT_TIMEOUT=86400     # Timeout of one day
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database connection
    from captcha import database as db
    db.init_app(app)

    # plug the caching layer
    app.cache = Cache(app)

    # apply the blueprint to the app
    from captcha import user
    app.register_blueprint(user.bp)

    return app
