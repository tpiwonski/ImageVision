from flask import Flask
from imagevision.ui.controllers import setup_ui
from imagevision.repositories.database import setup_database


def create_application():
    app = Flask(__name__)
    app.config.from_json('config.json')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    setup_database(app)
    setup_ui(app)

    return app
