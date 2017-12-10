from flask import Flask
from imagevision.controllers.ui import setup_ui
from imagevision.repositories.database import setup_database
from imagevision.controllers.api import setup_api


def create_application():
    app = Flask(__name__)
    app.config.from_json('config.json')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    app.secret_key = 'loremipsum'

    setup_database(app)
    setup_ui(app)
    setup_api(app)

    return app
