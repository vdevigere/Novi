import logging
import logging.config

from flask import Flask

from novi.client.database import engine
from novi.core.models import Base
from novi.web import evaluated_flags_endpoint
from novi.web import flags_endpoint


def init_db(script):
    logging.getLogger(__name__).debug(f"Initializing database with script: {script}")
    with engine.begin() as con:
        Base.metadata.create_all(engine)
        with open(script) as file:
            con.connection.executescript(file.read())


def create_app(script=None, test_config=None):
    # create and configure the app
    try:
        logging.config.fileConfig("logging.conf")
    except (FileNotFoundError, RuntimeError):
        logging.config.dictConfig({
            'version': 1,
            'formatters': {
                'simpleFormatter': {
                    'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                }
            },
            'handlers': {
                'consoleHandler': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'simpleFormatter',
                    # 'args': ['sys.stdout']
                }
            },
            'root': {
                'level': 'DEBUG',
                'handlers': ['consoleHandler']
            }
        })

    app = Flask(__name__)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    if script is not None:
        init_db(script)

    app.register_blueprint(flags_endpoint.blueprint)
    app.register_blueprint(evaluated_flags_endpoint.blueprint)
    return app
