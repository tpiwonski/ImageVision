from flask import Flask
from imagevision.repositories.database import setup_database
from imagevision.controllers.ui import setup_ui
from imagevision.controllers.ajax import setup_ajax


def create_application(config=None):
    """
    Create the application.

    :param config: a configuration object to update
    :return: the application
    """
    app = Flask(__name__)
    app.config.from_json('config.json')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    if config:
        app.config.from_mapping(config)
    
    app.secret_key = 'loremipsum'

    setup_database(app)
    setup_ui(app)
    setup_ajax(app)

    return app
