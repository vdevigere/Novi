import logging

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    logging.getLogger(__name__).addHandler(logging.NullHandler())

    app = Flask(__name__)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from novi.web import routes
    app.register_blueprint(routes.blueprint)
    return app
