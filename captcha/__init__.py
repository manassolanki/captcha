import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE='localhost:27017',
        SITE_VERIFY_URL='https://www.google.com/recaptcha/api/siteverify',
        SITE_SECRET='6LfC1Z4UAAAAAH10D1vOEpkUtZuNPuD7v-cyqkeX',
        RECAPTCHA_RESPONSE_PARAM='g-recaptcha-response'
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # register the database connection
    from captcha import database as db
    db.init_app(app)

    # apply the blueprint to the app
    from captcha import user
    app.register_blueprint(user.bp)

    return app
